"""
bgp.py
------
BGP Multi-AS Enterprise Network topology layout.
Calls symbols and styles; returns a saved PNG path.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from .symbols import (
    draw_router, draw_switch, draw_firewall, draw_cloud,
    draw_server, draw_zone, draw_link, draw_legend,
)
from .styles import BG_COLOR, LINKS, ZONES, LEGENDS


def build(output_path: str = "bgp_topology.png") -> str:
    """
    Render the BGP topology diagram and save to *output_path*.
    Returns the resolved output path.
    """
    fig, ax = plt.subplots(figsize=(22, 14))
    ax.set_xlim(0, 22); ax.set_ylim(0, 14); ax.axis("off")
    fig.patch.set_facecolor(BG_COLOR); ax.set_facecolor(BG_COLOR)

    # ── Title ─────────────────────────────────────────────────────────────────
    ax.text(11, 13.6, "BGP Multi-AS Enterprise Network Topology",
            ha="center", fontsize=16, fontweight="bold", color="#1A237E")
    ax.text(11, 13.2,
            "eBGP  ·  iBGP  ·  Route Reflector  ·  Multi-homed ISP  ·  IPSec VPN  ·  Cisco IOS  ·  Juniper JunOS",
            ha="center", fontsize=9, color="#455A64")

    # ── Zones ─────────────────────────────────────────────────────────────────
    draw_zone(ax,  0.3, 10.4, 21.2, 2.8,  "ISP / UPSTREAM (AS65100)",        **ZONES["internet"])
    draw_zone(ax,  0.3,  6.8, 21.2, 3.2,  "ENTERPRISE EDGE",                  **ZONES["dc"])
    draw_zone(ax,  0.3,  0.4,  6.5, 6.0,  "DATA CENTRE (AS65001)",            **ZONES["trust"])
    draw_zone(ax,  7.2,  0.4,  7.1, 6.0,  "BRANCH OFFICE (AS65002)",          **ZONES["pod_a"])
    draw_zone(ax, 14.8,  0.4,  6.7, 6.0,  "CLOUD (AS65003)",                  **ZONES["wan"])

    # ── ISP ───────────────────────────────────────────────────────────────────
    draw_cloud(ax,  4.5, 12.2, "ISP-RTR-1\nAS65100 | 203.0.113.1", "#C62828")
    draw_cloud(ax, 17.5, 12.2, "ISP-RTR-2\nAS65100 | 198.51.100.1", "#C62828")
    draw_link(ax, 5.1, 12.2, 16.9, 12.2, LINKS["transit"], 1.8, "--", 0.4, "Transit")

    # ── Enterprise edge ───────────────────────────────────────────────────────
    draw_router(ax,  4.5,  8.5, "EDGE-RTR-1", "AS65001 | 10.0.0.1/32", "#1565C0")
    draw_router(ax, 11.0,  8.5, "EDGE-RTR-2", "AS65001 | 10.0.0.2/32", "#1565C0")
    draw_firewall(ax, 17.5, 8.5, "EDGE-FW",   "Juniper SRX | IPSec termination")
    draw_link(ax, 5.5, 8.5, 9.95, 8.5,  LINKS["ibgp"], 2.0, "-", 0.7, "iBGP")
    draw_link(ax, 4.5, 11.68, 4.5, 9.02,  LINKS["ebgp"],  2.5, "-", 0.8, "eBGP\n203.0.113.0/30")
    draw_link(ax, 17.5, 11.68, 17.5, 9.48, LINKS["ebgp"],  2.5, "-", 0.8, "eBGP\n198.51.100.0/30")
    draw_link(ax, 12.05, 8.5, 16.55, 8.5,  LINKS["vpn"],   2.0, "-", 0.7, "eBGP / IPSec")

    # ── Data Centre ───────────────────────────────────────────────────────────
    draw_router(ax, 2.0, 6.0, "DC-CORE-1", "AS65001 | RR | 10.1.0.1", "#2E7D32")
    draw_router(ax, 5.5, 6.0, "DC-CORE-2", "AS65001 | RR | 10.1.0.2", "#2E7D32")
    draw_switch(ax, 2.0, 4.0, "DC-SW-1",   "Nexus 9300 | VLAN 100", "#388E3C")
    draw_switch(ax, 5.5, 4.0, "DC-SW-2",   "Nexus 9300 | VLAN 200", "#388E3C")
    dc_servers = [(1.0,2.2,"WEB-01"),(2.5,2.2,"APP-01"),(4.2,2.2,"DB-01"),(5.8,2.2,"BACKUP")]
    for sx, sy, sl in dc_servers:
        draw_server(ax, sx, sy, sl, "#2E7D32")
        draw_link(ax, sx, sy+0.45, 2.0 if sx<3.5 else 5.5, 3.76, LINKS["leaf_access"], 1.2, "-", 0.5)
    draw_link(ax, 2.0, 5.48, 2.0, 4.24, "#388E3C", 1.8, "-", 0.7)
    draw_link(ax, 5.5, 5.48, 5.5, 4.24, "#388E3C", 1.8, "-", 0.7)
    draw_link(ax, 2.55, 6.0, 4.95, 6.0, LINKS["ibgp_rr"], 1.8, "--", 0.6, "iBGP RR")
    draw_link(ax, 2.0, 6.52, 4.5, 7.98, LINKS["ibgp"], 2.0, "-", 0.7, "iBGP")
    draw_link(ax, 5.5, 6.52, 4.5, 7.98, LINKS["ibgp"], 2.0, "-", 0.7)

    # ── Branch ────────────────────────────────────────────────────────────────
    draw_router(ax, 10.7, 6.0, "BRANCH-RTR", "AS65002 | 172.16.0.1", "#E65100")
    draw_switch(ax, 10.7, 4.0, "BRANCH-SW",  "Catalyst | VLAN 10",   "#EF6C00")
    branch_servers = [(9.2,2.2,"WORKST-01"),(10.7,2.2,"WORKST-02"),(12.2,2.2,"PRINT-SRV")]
    for sx, sy, sl in branch_servers:
        draw_server(ax, sx, sy, sl, "#E65100")
        draw_link(ax, sx, sy+0.45, 10.7, 3.76, LINKS["dmz"], 1.2, "-", 0.5)
    draw_link(ax, 10.7, 5.48, 10.7, 4.24, "#EF6C00", 1.8, "-", 0.7)
    draw_link(ax, 10.7, 6.52, 11.0, 7.98, "#E65100", 2.0, "-", 0.8, "eBGP\n10.0.1.0/30")

    # ── Cloud ─────────────────────────────────────────────────────────────────
    draw_router(ax, 18.2, 6.0, "CLOUD-GW", "AS65003 | 10.100.0.1", "#6A1B9A")
    draw_switch(ax, 18.2, 4.0, "CLOUD-SW", "Virtual Switch | VPC",  "#7B1FA2")
    cloud_servers = [(16.5,2.2,"VM-WEB"),(18.2,2.2,"VM-APP"),(19.9,2.2,"VM-DB")]
    for sx, sy, sl in cloud_servers:
        draw_server(ax, sx, sy, sl, "#6A1B9A")
        draw_link(ax, sx, sy+0.45, 18.2, 3.76, LINKS["vpn"], 1.2, "-", 0.5)
    draw_link(ax, 18.2, 5.48, 18.2, 4.24, "#7B1FA2", 1.8, "-", 0.7)
    draw_link(ax, 18.2, 6.52, 17.5, 7.98, "#7B1FA2", 2.0, "-", 0.8, "BGP/IPSec")

    # ── Legend ────────────────────────────────────────────────────────────────
    ax.add_patch(FancyBboxPatch((0.3, 0.05), 21.2, 0.32,
                 boxstyle="round,pad=0.08", facecolor="#ECEFF1",
                 edgecolor="#90A4AE", linewidth=1, zorder=8))
    draw_legend(ax, LEGENDS["bgp"], x_start=0.6, y=0.21, spacing=4.2)

    plt.tight_layout(pad=0.3)
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    return output_path
