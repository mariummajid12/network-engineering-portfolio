"""
firewall.py
-----------
Firewall & Network Security Architecture topology layout.
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


def build(output_path: str = "fw_topology.png") -> str:
    """Render the Firewall topology diagram and save to *output_path*."""
    fig, ax = plt.subplots(figsize=(22, 15))
    ax.set_xlim(0, 22); ax.set_ylim(0, 15); ax.axis("off")
    fig.patch.set_facecolor(BG_COLOR); ax.set_facecolor(BG_COLOR)

    # ── Title ─────────────────────────────────────────────────────────────────
    ax.text(11, 14.6, "Firewall & Network Security Architecture",
            ha="center", fontsize=16, fontweight="bold", color="#1A237E")
    ax.text(11, 14.2,
            "Juniper SRX  ·  Fortinet FortiGate  ·  Zone-Based Policy  ·  "
            "IPSec VPN  ·  DMZ  ·  IDS/IPS  ·  SIEM",
            ha="center", fontsize=9, color="#455A64")

    # ── Zones ─────────────────────────────────────────────────────────────────
    draw_zone(ax,  0.3, 11.5, 21.2, 2.2, "UNTRUST ZONE — Internet / WAN",              **ZONES["internet"])
    draw_zone(ax,  0.3,  8.2, 21.2, 2.9, "PERIMETER — Dual Firewall HA (Active/Passive)", **ZONES["perimeter"])
    draw_zone(ax,  0.3,  5.2,  9.5, 2.7, "DMZ — Publicly Accessible Services",         **ZONES["dmz"])
    draw_zone(ax, 10.2,  5.2, 11.3, 2.7, "TRUST — Internal Network",                   **ZONES["trust"])
    draw_zone(ax,  0.3,  0.5, 21.2, 4.4, "INTERNAL SEGMENTS",                          **ZONES["dc"])

    # ── Internet edge ─────────────────────────────────────────────────────────
    draw_cloud(ax,  5.5, 13.0, "INTERNET\nISP | 203.0.113.0/30",   "#B71C1C")
    draw_cloud(ax, 16.5, 13.0, "BRANCH VPN\n198.51.100.0/30",      "#880E4F")
    draw_firewall(ax,  5.5, 9.5, "FW-ACTIVE",  "Juniper SRX4200 | 203.0.113.2")
    draw_firewall(ax, 16.5, 9.5, "FW-PASSIVE", "Fortinet FortiGate 600E | HA Standby")
    draw_link(ax,  5.5, 12.4,  5.5, 10.4, LINKS["untrust"], 2.5, "-", 0.8, "Untrust")
    draw_link(ax, 16.5, 12.4, 16.5, 10.4, LINKS["vpn"],     2.5, "-", 0.8, "IPSec VPN")
    draw_link(ax,  6.4,  9.5, 15.6,  9.5, LINKS["ha_sync"], 2.5, "--", 0.85, "HA Sync / Heartbeat")

    # IDS/IPS block
    ax.add_patch(FancyBboxPatch((10.45, 9.12), 1.1, 0.76,
                 boxstyle="round,pad=0.1", facecolor="#1565C0",
                 edgecolor="white", linewidth=2, zorder=5))
    ax.text(11.0, 9.71, "◉", ha="center", va="center", fontsize=14, color="white", zorder=6)
    ax.text(11.0, 8.92, "IDS/IPS", ha="center", fontsize=8.5, fontweight="bold",
            color="#0D47A1", fontfamily="monospace", zorder=7)
    ax.text(11.0, 8.68, "Inline | Snort/Suricata", ha="center", fontsize=6.5,
            color="#455A64", zorder=7)
    draw_link(ax,  6.5, 9.5, 10.45, 9.5, LINKS["mgmt"], 2.0, "-", 0.8)
    draw_link(ax, 11.55, 9.5, 15.6, 9.5, LINKS["mgmt"], 2.0, "-", 0.8)

    # ── DMZ ───────────────────────────────────────────────────────────────────
    draw_switch(ax, 4.8, 6.8, "DMZ-SW", "Cisco Catalyst | VLAN 100", "#F57F17")
    for sx, sl in [(1.2,"WEB-01"),(2.8,"WEB-02"),(4.5,"MAIL"),(6.2,"DNS-EXT"),(7.8,"PROXY")]:
        draw_server(ax, sx, 5.6, sl, "#795548")
        draw_link(ax, sx, 5.88, 4.8, 6.57, LINKS["dmz"], 1.3, "-", 0.55)
    draw_link(ax, 5.5, 8.62, 4.8, 7.28, LINKS["dmz"],   2.0, "-", 0.8, "DMZ zone")

    # ── Trust ─────────────────────────────────────────────────────────────────
    draw_switch(ax, 15.5, 6.8, "CORE-SW", "Cisco Nexus 9300 | VLAN 200-400", "#2E7D32")
    for sx, sl in [(12.0,"APP-SRV"),(13.8,"DB-SRV"),(15.5,"FILE-SRV"),(17.2,"AD-DC")]:
        draw_server(ax, sx, 5.6, sl, "#2E7D32")
        draw_link(ax, sx, 5.88, 15.5, 6.57, LINKS["trust"], 1.3, "-", 0.55)
    draw_link(ax,  5.5, 8.62, 15.5, 7.28, LINKS["trust"],  2.0, "-", 0.8, "Trust zone")

    # SIEM
    draw_server(ax, 19.8, 6.1, "SIEM", "#1565C0")
    draw_link(ax, 19.8, 5.72, 19.8, 4.85, LINKS["siem"], 1.5, "--", 0.65, "Logs")

    # ── Internal segments ─────────────────────────────────────────────────────
    segs = [
        (2.2,  2.6, "VLAN 200\nUSERS\n10.10.0.0/24",      "#E8EAF6", "#3949AB"),
        (6.0,  2.6, "VLAN 300\nSERVERS\n10.20.0.0/24",    "#E8F5E9", "#2E7D32"),
        (10.0, 2.6, "VLAN 400\nVoIP / IoT\n10.30.0.0/24", "#FFF8E1", "#F9A825"),
        (14.0, 2.6, "VLAN 500\nMANAGEMENT\n10.99.0.0/24", "#EDE7F6", "#6A1B9A"),
        (18.2, 2.6, "OOB MGMT\nOut-of-Band\n10.255.0.0/24","#FCE4EC","#880E4F"),
    ]
    for sx, sy, label, fill, border in segs:
        ax.add_patch(FancyBboxPatch((sx-1.5, sy-0.7), 3.0, 1.4,
                     boxstyle="round,pad=0.12", facecolor=fill,
                     edgecolor=border, linewidth=1.8, alpha=0.85, zorder=3))
        ax.text(sx, sy, label, ha="center", va="center", fontsize=7.5,
                color=border, fontweight="bold", zorder=4, linespacing=1.5)
        dest_x = 15.5 if sx > 9 else sx
        dest_y = 6.57 if sx > 9 else 4.9
        draw_link(ax, sx, sy+0.7, dest_x, dest_y, border, 1.2, "-", 0.4)

    # ── Legend ────────────────────────────────────────────────────────────────
    ax.add_patch(FancyBboxPatch((0.3, 0.05), 21.2, 0.38,
                 boxstyle="round,pad=0.08", facecolor="#ECEFF1",
                 edgecolor="#90A4AE", linewidth=1, zorder=8))
    draw_legend(ax, LEGENDS["firewall"], x_start=0.6, y=0.24, spacing=3.0)

    plt.tight_layout(pad=0.3)
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    return output_path
