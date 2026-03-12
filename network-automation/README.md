# Network Automation — Configuration Backup Tool

A Python tool that connects to network devices via SSH to collect device information and back up running configurations. Supports Cisco IOS, Cisco NX-OS, and Juniper JunOS.

Built using [Netmiko](https://github.com/ktbyers/netmiko) — the industry-standard Python library for multi-vendor network device automation.

## Why This Matters

Manual configuration backups are error-prone and time-consuming. In production environments with dozens of devices, automation ensures backups happen consistently, are timestamped, and are stored in a structured format ready for audit or disaster recovery.

## What It Does

- Connects to network devices via SSH
- Collects version info, interface status, BGP summary, and running configuration
- Saves timestamped configuration backups per device
- Generates a JSON summary for each device (useful for CMDB integration)
- Produces a final backup report across all devices
- **Mock mode** — runs without real hardware for testing and demonstration

## Supported Platforms

| Platform | device_type |
|----------|-------------|
| Cisco IOS / IOS-XE | `cisco_ios` |
| Cisco NX-OS | `cisco_nxos` |
| Juniper JunOS | `juniper_junos` |

## Files

| File | Description |
|------|-------------|
| `network_backup.py` | Main backup and collection script |
| `inventory.yaml.example` | Example multi-device inventory file |

## Usage

### Demo mode (no real devices needed)
```bash
python network_backup.py --mock
```

### Single device
```bash
python network_backup.py --host 192.168.1.1 --device-type cisco_ios --username admin
```

### Custom output directory
```bash
python network_backup.py --host 192.168.1.1 --device-type juniper_junos --username admin --output-dir /backups/weekly
```

## Example Output

```
============================================================
  NETWORK BACKUP TOOL — MOCK / DEMO MODE
  Simulating connections to 3 devices
============================================================

[CORE-RTR-01] Collecting data...

  Device  : CORE-RTR-01 (192.168.1.1)
  Type    : cisco_ios

[VERSION INFO]
  Cisco IOS Software, Version 15.7(3)M4
  Uptime: 47 days, 3 hours, 22 minutes

[INTERFACES]
  GigabitEthernet0/0     10.0.0.1    up    up
  GigabitEthernet0/1     192.168.1.1 up    up

[BGP SUMMARY]
  Neighbor   AS    MsgRcvd  Up/Down   State/PfxRcd
  10.0.0.2   65002  1423    2d03h     24
  10.0.0.3   65003   987    1d12h     18

============================================================
  BACKUP COMPLETE — 3 devices processed
============================================================
  ✓  CORE-RTR-01    192.168.1.1    SUCCESS
  ✓  DIST-SW-01     192.168.1.2    SUCCESS
  ✓  EDGE-FW-01     192.168.1.3    SUCCESS
```

## Backup Output Structure

```
backups/
├── CORE-RTR-01_192.168.1.1/
│   ├── config_20260312_143000.txt
│   └── summary_20260312_143000.json
├── DIST-SW-01_192.168.1.2/
│   ├── config_20260312_143001.txt
│   └── summary_20260312_143001.json
└── backup_report.json
```

## Requirements

```bash
pip install netmiko
```

Python 3.7+ required. Mock mode works with no dependencies beyond the standard library.

## Real-World Application

This type of automation is used for:
- **Change management** — capturing pre/post-change config snapshots
- **Disaster recovery** — ensuring recent configs are always available for restore
- **Compliance auditing** — timestamped config history for audit trails
- **Network documentation** — automated inventory of device versions and interfaces

