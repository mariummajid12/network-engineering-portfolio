# Network Engineering Portfolio

Practical network engineering projects by **Marium Majid**, Network Engineer with 7+ years of experience across enterprise, data centre, and cloud environments.

This portfolio demonstrates hands-on skills in network automation, configuration management, infrastructure design, and multi-vendor platform engineering across Cisco, Juniper, Arista, and Fortinet.

---

## Projects

### ⚙️ Network Automation: Configuration Backup Tool
**[`network-automation/`](./network-automation/)**

Connects to network devices via SSH to collect device information and back up running configurations. Supports Cisco IOS, Cisco NX-OS, and Juniper JunOS.

- Automated config backup with timestamped versioning
- Collects version info, interface status, and BGP summary per device
- Generates structured JSON summaries for CMDB integration
- Mock mode — runs without real hardware for demonstration

```bash
# Demo mode — no real devices needed
python network_backup.py --mock

# Single device
python network_backup.py --host 192.168.1.1 --device-type cisco_ios --username admin
```

---

### 🔀 BGP & Routing Labs
**[`bgp-routing/`](./bgp-routing/)**

*(Coming soon)*

BGP configuration examples, route policy design, and troubleshooting scenarios across Cisco IOS/IOS-XR and Juniper JunOS. Covers eBGP, iBGP, route reflectors, communities, and prefix filtering.

---

### 🏢 Data Centre Networking
**[`data-centre/`](./data-centre/)**

*(Coming soon)*

EVPN/VXLAN fabric design and configuration examples for data centre environments. Covers leaf-spine architecture, BGP EVPN control plane, and L2/L3 overlay design on Cisco Nexus and Arista.

---

### 🔒 Firewall & Security Infrastructure
**[`firewall-security/`](./firewall-security/)**

*(Coming soon)*

Firewall policy design, VPN configuration, and network segmentation examples across Juniper SRX and Fortinet platforms. Covers zone-based security, IKEv2 VPN, and DMZ architecture.

---

### ☁️ Cloud & Hybrid Networking
**[`cloud-networking/`](./cloud-networking/)**

*(Coming soon)*

Hybrid cloud connectivity patterns from hands-on experience at DigitalOcean. Covers secure cloud-to-on-premise connectivity, network segmentation in cloud environments, and infrastructure-as-code for network provisioning.

---

## Platforms & Technologies

| Category | Technologies |
|----------|-------------|
| Routing & Switching | Cisco IOS · IOS-XR · Cisco Nexus · Arista · Juniper MX/EX |
| Security | Juniper SRX · Fortinet FortiGate · VPN · Firewall Policy |
| Protocols | BGP · MPLS · EVPN · VXLAN · IS-IS · OSPF · STP · HSRP · VRRP |
| Data Centre | Leaf-Spine · EVPN/VXLAN · Cisco Nexus · Arista |
| Cloud | DigitalOcean · Hybrid Cloud Connectivity · AWS/Azure (familiar) |
| Automation | Python · Netmiko · Ansible · Git · NetBox |
| Monitoring | ThousandEyes · Grafana · Kentik · AKIPS · Alerta |

---

## About Me

- 7+ years in network engineering across enterprise, data centre, and cloud (DigitalOcean, Jazz, Nayatel)
- MSc Cybersecurity & Cyber Defense - University of Luxembourg (final semester)
- Research intern at LIST - secure communication protocols for 6G network digital twin systems
- Certified ScrumMaster | Certified Scrum Product Owner 

📎 [LinkedIn](https://linkedin.com/in/marium-majid-95a770131) | 🔐 [Cybersecurity Portfolio](https://github.com/mariummajid12/cybersecurity-portfolio)

---

## Skills Demonstrated

`Python` `Netmiko` `Ansible` `Cisco IOS` `Cisco Nexus` `Juniper JunOS` `Arista` `Fortinet` `BGP` `MPLS` `EVPN` `VXLAN` `Data Centre` `Cloud Networking` `Network Automation` `Firewall` `VPN`
