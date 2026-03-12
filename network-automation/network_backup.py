"""
network_backup.py
-----------------
Connects to network devices via SSH (using Netmiko) to collect
device information and back up running configurations.

Supports real devices and a --mock mode for demonstration
without requiring physical or virtual hardware.

Supported device types: Cisco IOS, Cisco NX-OS, Juniper JunOS

Usage:
    # Run in mock/demo mode (no real devices needed)
    python network_backup.py --mock

    # Run against a real device
    python network_backup.py --host 192.168.1.1 --device-type cisco_ios --username admin --password secret

    # Run against multiple devices from inventory file
    python network_backup.py --inventory inventory.yaml

Author: Marium Majid
Portfolio: Network Security & Automation
"""

import os
import argparse
import datetime
import getpass
import json
from pathlib import Path

# ── Mock data ─────────────────────────────────────────────────────────────────

MOCK_DEVICES = [
    {
        "host": "192.168.1.1",
        "device_type": "cisco_ios",
        "hostname": "CORE-RTR-01",
    },
    {
        "host": "192.168.1.2",
        "device_type": "cisco_ios",
        "hostname": "DIST-SW-01",
    },
    {
        "host": "192.168.1.3",
        "device_type": "juniper_junos",
        "hostname": "EDGE-FW-01",
    },
]

MOCK_OUTPUTS = {
    "cisco_ios": {
        "show version": """\
Cisco IOS Software, Version 15.7(3)M4, RELEASE SOFTWARE
Technical Support: http://www.cisco.com/techsupport
ROM: System Bootstrap, Version 15.7(3)M4
Uptime: 47 days, 3 hours, 22 minutes
System image file is "flash:c2900-universalk9-mz.SPA.157-3.M4.bin"
Processor board ID FTX1234ABCD
4 FastEthernet interfaces, 2 Gigabit Ethernet interfaces
Configuration register is 0x2102""",

        "show ip interface brief": """\
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     10.0.0.1        YES NVRAM  up                    up
GigabitEthernet0/1     192.168.1.1     YES NVRAM  up                    up
FastEthernet0/0        unassigned      YES NVRAM  administratively down down
Loopback0              1.1.1.1         YES NVRAM  up                    up""",

        "show ip bgp summary": """\
BGP router identifier 1.1.1.1, local AS number 65001
BGP table version is 142, main routing table version 142
Neighbor        V    AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
10.0.0.2        4 65002    1423    1401      142    0    0 2d03h          24
10.0.0.3        4 65003     987     965      142    0    0 1d12h          18""",

        "show running-config": """\
!
version 15.7
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname CORE-RTR-01
!
interface GigabitEthernet0/0
 description UPLINK-TO-ISP
 ip address 10.0.0.1 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 description LAN-SEGMENT
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
router bgp 65001
 neighbor 10.0.0.2 remote-as 65002
 neighbor 10.0.0.3 remote-as 65003
!
line vty 0 4
 transport input ssh
!
end""",
    },

    "juniper_junos": {
        "show version": """\
Junos: 21.4R3.15
JUNOS Base OS boot [21.4R3.15]
Model: srx300
JUNOS Software Release [21.4R3.15]
Hostname: EDGE-FW-01
Uptime: 12 days, 6 hours, 44 minutes""",

        "show interfaces terse": """\
Interface               Admin Link Proto    Local                 Remote
ge-0/0/0                up    up
ge-0/0/0.0              up    up   inet     203.0.113.1/30
ge-0/0/1                up    up
ge-0/0/1.0              up    up   inet     192.168.10.1/24
lo0                     up    up
lo0.0                   up    up   inet     10.255.255.3""",

        "show bgp summary": """\
Groups: 2 Peers: 2 Down peers: 0
Table          Tot Paths  Act Paths Suppressed    History Damp State    Pending
inet.0               42         38          0          0          0          0
Peer                     AS      InPkt     OutPkt    OutQ   Flaps Last Up/Dwn State
203.0.113.2           65100       4521       4498       0       1     5d 2:14 42/0/0/0""",

        "show configuration": """\
system {
    host-name EDGE-FW-01;
    time-zone Europe/Luxembourg;
}
interfaces {
    ge-0/0/0 {
        description "UPLINK-TO-ISP";
        unit 0 {
            family inet {
                address 203.0.113.1/30;
            }
        }
    }
    ge-0/0/1 {
        description "LAN-TRUST-ZONE";
        unit 0 {
            family inet {
                address 192.168.10.1/24;
            }
        }
    }
}
security {
    zones {
        security-zone trust {
            interfaces {
                ge-0/0/1.0;
            }
        }
        security-zone untrust {
            interfaces {
                ge-0/0/0.0;
            }
        }
    }
}""",
    }
}

# ── Device commands by platform ───────────────────────────────────────────────

COMMANDS = {
    "cisco_ios": {
        "version":    "show version",
        "interfaces": "show ip interface brief",
        "bgp":        "show ip bgp summary",
        "config":     "show running-config",
    },
    "cisco_nxos": {
        "version":    "show version",
        "interfaces": "show interface brief",
        "bgp":        "show bgp summary",
        "config":     "show running-config",
    },
    "juniper_junos": {
        "version":    "show version",
        "interfaces": "show interfaces terse",
        "bgp":        "show bgp summary",
        "config":     "show configuration",
    },
}

# ── Core functions ─────────────────────────────────────────────────────────────

def get_mock_output(device_type, command):
    """Return simulated device output for mock mode."""
    platform = device_type if device_type in MOCK_OUTPUTS else "cisco_ios"
    return MOCK_OUTPUTS[platform].get(command, f"% Command '{command}' not available in mock mode")


def collect_device_info(host, device_type, username=None, password=None, mock=False):
    """
    Connect to a device and collect version, interface, BGP, and config data.
    In mock mode, returns simulated output without SSH connection.
    """
    commands = COMMANDS.get(device_type, COMMANDS["cisco_ios"])
    results = {}

    if mock:
        for key, cmd in commands.items():
            results[key] = get_mock_output(device_type, cmd)
        return results

    try:
        from netmiko import ConnectHandler
    except ImportError:
        print("[ERROR] Netmiko not installed. Run: pip install netmiko")
        print("[INFO]  Use --mock flag to run without real devices.")
        exit(1)

    device = {
        "device_type": device_type,
        "host": host,
        "username": username,
        "password": password,
    }

    print(f"  Connecting to {host}...")
    with ConnectHandler(**device) as conn:
        for key, cmd in commands.items():
            print(f"  Running: {cmd}")
            results[key] = conn.send_command(cmd)

    return results


def save_backup(host, hostname, device_type, results, output_dir):
    """Save collected device data to timestamped backup files."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    device_dir = Path(output_dir) / f"{hostname}_{host}"
    device_dir.mkdir(parents=True, exist_ok=True)

    # Save full config
    config_file = device_dir / f"config_{timestamp}.txt"
    with open(config_file, "w") as f:
        f.write(f"# Device  : {hostname} ({host})\n")
        f.write(f"# Type    : {device_type}\n")
        f.write(f"# Backed up: {datetime.datetime.now().isoformat()}\n")
        f.write("#" + "=" * 60 + "\n\n")
        f.write(results.get("config", "# No config collected"))

    # Save summary JSON
    summary = {
        "host": host,
        "hostname": hostname,
        "device_type": device_type,
        "timestamp": timestamp,
        "version": results.get("version", ""),
        "interfaces": results.get("interfaces", ""),
        "bgp_summary": results.get("bgp", ""),
    }
    summary_file = device_dir / f"summary_{timestamp}.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    return config_file, summary_file


def print_summary(host, hostname, device_type, results):
    """Print a formatted device summary to the console."""
    print(f"\n{'=' * 60}")
    print(f"  Device  : {hostname} ({host})")
    print(f"  Type    : {device_type}")
    print(f"{'=' * 60}")

    print(f"\n[VERSION INFO]")
    for line in results.get("version", "").splitlines()[:5]:
        print(f"  {line}")

    print(f"\n[INTERFACES]")
    for line in results.get("interfaces", "").splitlines():
        print(f"  {line}")

    print(f"\n[BGP SUMMARY]")
    for line in results.get("bgp", "").splitlines():
        print(f"  {line}")


def run_mock():
    """Run against all mock devices and display results."""
    print("\n" + "=" * 60)
    print("  NETWORK BACKUP TOOL — MOCK / DEMO MODE")
    print("  Simulating connections to 3 devices")
    print("=" * 60)

    output_dir = "backups"
    report = []

    for device in MOCK_DEVICES:
        host = device["host"]
        device_type = device["device_type"]
        hostname = device["hostname"]

        print(f"\n[{hostname}] Collecting data... (mock)")
        results = collect_device_info(host, device_type, mock=True)
        print_summary(host, hostname, device_type, results)

        config_file, summary_file = save_backup(
            host, hostname, device_type, results, output_dir
        )

        report.append({
            "host": host,
            "hostname": hostname,
            "status": "SUCCESS",
            "config_backup": str(config_file),
            "summary": str(summary_file),
        })
        print(f"\n  Config backup : {config_file}")
        print(f"  Summary JSON  : {summary_file}")

    # Final report
    print(f"\n{'=' * 60}")
    print(f"  BACKUP COMPLETE — {len(report)} devices processed")
    print(f"{'=' * 60}")
    for entry in report:
        status_icon = "✓" if entry["status"] == "SUCCESS" else "✗"
        print(f"  {status_icon}  {entry['hostname']:20s} {entry['host']:16s} {entry['status']}")

    report_path = Path(output_dir) / "backup_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n  Full report saved to: {report_path}")


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Network device configuration backup tool."
    )
    parser.add_argument("--mock", action="store_true",
                        help="Run in demo mode without real devices")
    parser.add_argument("--host", help="Device IP address")
    parser.add_argument("--device-type", default="cisco_ios",
                        choices=["cisco_ios", "cisco_nxos", "juniper_junos"],
                        help="Device platform type")
    parser.add_argument("--username", help="SSH username")
    parser.add_argument("--password", help="SSH password (omit to be prompted)")
    parser.add_argument("--output-dir", default="backups",
                        help="Directory to save backups (default: ./backups)")
    args = parser.parse_args()

    if args.mock:
        run_mock()
        return

    if not args.host:
        parser.error("--host is required unless using --mock mode")

    username = args.username or input("Username: ")
    password = args.password or getpass.getpass("Password: ")

    print(f"\nConnecting to {args.host}...")
    results = collect_device_info(
        args.host, args.device_type, username, password, mock=False
    )
    hostname = args.host  # fallback if hostname not parsed
    print_summary(args.host, hostname, args.device_type, results)
    config_file, summary_file = save_backup(
        args.host, hostname, args.device_type, results, args.output_dir
    )
    print(f"\n  Config backup : {config_file}")
    print(f"  Summary JSON  : {summary_file}")


if __name__ == "__main__":
    main()
