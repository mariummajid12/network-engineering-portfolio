"""
dc.py
-----
Data Centre EVPN/VXLAN Leaf-Spine topology layout.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from .symbols import (
    draw_switch, draw_border_router, draw_server,
    draw_zone, draw_link, draw_legend,
)
from .styles import BG_COLOR, LINKS, ZONES, LEGENDS


def build(output_path: str = "dc_topology.png") -> str:
    """Render the Data Centre topology diagram and save to *output_path*."""
    fig, ax = plt.subplots(figsize=(22, 14))
    ax.set_xlim(0, 22); ax.set_ylim(0, 14); ax.axis("off")
    fig.patch.set_facecolor(BG_COLOR); ax.set_facecolor(BG_COLOR)

    # ── Title ─────────────────────────────────────────────────────────────────
    ax.text(11, 13.6, "Data Centre Network — EVPN/VXLAN Leaf-Spine Topology",
            ha="center", fontsize=15, fontweight="bold", color="#1A237E")
    ax.text(11, 13.2,
            "Arista 7050CX3 Spine  ·  Cisco Nexus 9300 Leaf  ·  "
            "Juniper QFX Border  ·  BGP EVPN  ·  VXLAN Overlay",
            ha="center", fontsize=9, color="#455A64")

    # ── Zones ─────────────────────────────────────────────────────────────────
    draw_zone(ax,  0.3, 10.2, 21.2, 2.8,  "SPINE LAYER — IP Fabric Underlay (OSPF)",     **ZONES["super_spine"])
    draw_zone(ax,  0.3,  7.0, 21.2, 2.8,  "LEAF LAYER — BGP EVPN / VXLAN VTEPs",         **ZONES["spine"])
    draw_zone(ax,  0.3,  0.4,  6.8, 6.3,  "POD A — Tenant 1 (VNI 10100)",                **ZONES["pod_a"])
    draw_zone(ax,  7.4,  0.4,  7.0, 6.3,  "POD B — Tenant 2 (VNI 10200)",                **ZONES["pod_b"])
    draw_zone(ax, 14.7,  0.4,  6.8, 6.3,  "POD C — Storage / DMZ (VNI 10300)",           **ZONES["pod_c"])

    # ── Spine ─────────────────────────────────────────────────────────────────
    draw_switch(ax,  4.5, 11.8, "SPINE-1", "Arista 7050CX3 | Lo0: 10.0.0.1/32", "#1565C0")
    draw_switch(ax, 11.0, 11.8, "SPINE-2", "Arista 7050CX3 | Lo0: 10.0.0.2/32", "#1565C0")
    draw_switch(ax, 17.5, 11.8, "SPINE-3", "Arista 7050CX3 | Lo0: 10.0.0.3/32", "#1565C0")
    draw_border_router(ax, 11.0, 10.4, "BORDER-LEAF",
                       "Juniper QFX5100 | Lo0: 10.0.1.1 | External / WAN", "#4527A0")
    draw_link(ax, 5.68, 11.8, 9.82, 11.8,  "#1976D2", 1.5, "--", 0.4)
    draw_link(ax, 12.18, 11.8, 16.32, 11.8, "#1976D2", 1.5, "--", 0.4)
    draw_link(ax,  4.5, 11.37, 10.52, 10.68, LINKS["ospf"], 2.0, "-", 0.65, "OSPF p2p")
    draw_link(ax, 11.0, 11.37, 11.0,  10.9,  LINKS["ospf"], 2.0, "-", 0.65)
    draw_link(ax, 17.5, 11.37, 11.48, 10.68, LINKS["ospf"], 2.0, "-", 0.65)

    # ── Leaves ────────────────────────────────────────────────────────────────
    leaf_data = [
        ( 3.0, 8.5, "LEAF-1A", "Nexus 9300 | VTEP 10.1.1.1"),
        ( 7.0, 8.5, "LEAF-1B", "Nexus 9300 | VTEP 10.1.1.2"),
        (11.0, 8.5, "LEAF-2A", "Nexus 9300 | VTEP 10.1.2.1"),
        (15.0, 8.5, "LEAF-2B", "Nexus 9300 | VTEP 10.1.2.2"),
        (19.0, 8.5, "LEAF-3A", "Nexus 9300 | VTEP 10.1.3.1"),
    ]
    for lx, ly, ln, ls in leaf_data:
        draw_switch(ax, lx, ly, ln, ls, "#2E7D32", 0.40)
    draw_link(ax,  4.38, 8.5,  5.62, 8.5, LINKS["vpc_peer"], 2.5, "--", 0.9, "vPC")
    draw_link(ax, 12.38, 8.5, 13.62, 8.5, LINKS["vpc_peer"], 2.5, "--", 0.9, "vPC")
    for lx, ly, _, _ in leaf_data:
        for sx in [4.5, 11.0, 17.5]:
            draw_link(ax, sx, 11.37, lx, 8.72, LINKS["spine_up"], 1.4, "-", 0.25)

    # ── Servers ───────────────────────────────────────────────────────────────
    pod_a = [(1.2,5.8,"WEB-01"),(2.8,5.8,"WEB-02"),
             (1.5,4.3,"APP-01"),(3.2,4.3,"APP-02"),(5.2,5.0,"DB-01")]
    for sx, sy, sl in pod_a:
        draw_server(ax, sx, sy, sl, "#2E7D32")
        draw_link(ax, sx, sy+0.42, 3.0 if sx<4.5 else 7.0, 8.28, LINKS["leaf_access"], 1.2, "-", 0.5)

    pod_b = [(8.0,5.8,"APP-03"),(9.5,5.8,"APP-04"),
             (8.2,4.3,"MQ-01"),(10.2,4.3,"CACHE"),(12.5,5.0,"API-01")]
    for sx, sy, sl in pod_b:
        draw_server(ax, sx, sy, sl, "#6A1B9A")
        draw_link(ax, sx, sy+0.42, 7.0 if sx<10.5 else 11.0, 8.28, LINKS["vpn"], 1.2, "-", 0.5)

    pod_c = [(15.5,5.8,"SAN-01"),(17.2,5.8,"SAN-02"),
             (15.8,4.3,"FW-01"),(18.8,5.0,"MGMT-01")]
    for sx, sy, sl in pod_c:
        draw_server(ax, sx, sy, sl, "#B71C1C")
        draw_link(ax, sx, sy+0.42, 15.0 if sx<17.5 else 19.0, 8.28, LINKS["untrust"], 1.2, "-", 0.5)

    # ── Legend ────────────────────────────────────────────────────────────────
    ax.add_patch(FancyBboxPatch((0.3, 0.05), 21.2, 0.32,
                 boxstyle="round,pad=0.08", facecolor="#ECEFF1",
                 edgecolor="#90A4AE", linewidth=1, zorder=8))
    draw_legend(ax, LEGENDS["dc"], x_start=0.6, y=0.21, spacing=3.5)

    plt.tight_layout(pad=0.3)
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    return output_path
