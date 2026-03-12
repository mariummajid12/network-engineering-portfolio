"""
cloud.py
--------
Cloud Data Centre AI/ML GPU Fabric topology layout.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from .symbols import (
    draw_router, draw_switch, draw_firewall, draw_cloud,
    draw_server, draw_gpu_node, draw_storage, draw_border_router,
    draw_zone, draw_link, draw_legend,
)
from .styles import BG_COLOR, LINKS, ZONES, LEGENDS


def build(output_path: str = "cloud_topology.png") -> str:
    """Render the Cloud/GPU topology diagram and save to *output_path*."""
    fig, ax = plt.subplots(figsize=(26, 18))
    ax.set_xlim(0, 26); ax.set_ylim(0, 18); ax.axis("off")
    fig.patch.set_facecolor(BG_COLOR); ax.set_facecolor(BG_COLOR)

    # ── Title ─────────────────────────────────────────────────────────────────
    ax.text(13, 17.65,
            "Cloud Data Centre — AI/ML GPU Fabric  |  Spine-Leaf with Multi-Pod Architecture",
            ha="center", fontsize=15, fontweight="bold", color="#1A237E")
    ax.text(13, 17.25,
            "Arista 7800R3 Super-Spine  ·  Cisco Nexus 9336C Spine  ·  Arista 7050CX3 Leaf  ·  "
            "400GbE Fabric  ·  RoCEv2 / RDMA  ·  BGP EVPN  ·  VXLAN",
            ha="center", fontsize=8.5, color="#455A64")

    # ── Zones ─────────────────────────────────────────────────────────────────
    draw_zone(ax,  0.3, 14.5, 25.2, 2.8,  "INTERNET EDGE & WAN",                                    **ZONES["internet"])
    draw_zone(ax,  0.3, 11.2, 25.2, 2.9,  "SUPER-SPINE LAYER — Cross-Pod Routing (BGP / OSPF Underlay)", **ZONES["super_spine"])
    draw_zone(ax,  0.3,  7.8, 25.2, 3.0,  "SPINE LAYER — Per-Pod IP Fabric (400GbE)",               **ZONES["spine"])
    draw_zone(ax,  0.3,  0.4,  7.8, 7.1,  "POD 1 — GPU Cluster A  (AI Training)",                  **ZONES["gpu_train"])
    draw_zone(ax,  8.4,  0.4,  8.8, 7.1,  "POD 2 — GPU Cluster B  (AI Inference)",                 **ZONES["gpu_infer"])
    draw_zone(ax, 17.5,  0.4,  8.0, 7.1,  "POD 3 — Storage & Management",                          **ZONES["storage"])

    # ── Edge ──────────────────────────────────────────────────────────────────
    draw_cloud(ax,  3.5, 16.1, "INTERNET\n/ WAN",              "#B71C1C")
    draw_cloud(ax, 10.5, 16.1, "CLOUD PEERING\nAWS/Azure/GCP","#37474F")
    draw_cloud(ax, 17.5, 16.1, "MPLS / SD-WAN\nBranch Offices","#4527A0")
    draw_firewall(ax,  3.5, 14.9, "EDGE-FW-1", "Juniper SRX4600 | Active")
    draw_firewall(ax,  7.5, 14.9, "EDGE-FW-2", "Juniper SRX4600 | Standby")
    draw_router(ax,  13.0, 14.9, "PEERING-RTR", "Cisco ASR 9000 | BGP | AS65000", "#1565C0")
    draw_router(ax,  20.0, 14.9, "WAN-RTR",     "Juniper MX204 | MPLS | SD-WAN",   "#1565C0")
    draw_link(ax,  3.5, 15.62,  3.5, 15.38, LINKS["untrust"], 2.2, "-", 0.8)
    draw_link(ax, 10.5, 15.62, 13.0, 15.38, "#546E7A", 2.2, "-", 0.8, "BGP peering")
    draw_link(ax, 17.5, 15.62, 20.0, 15.38, LINKS["vpn"],     2.2, "-", 0.8, "MPLS")
    draw_link(ax,  4.44, 14.9,  6.56, 14.9,  LINKS["ha_sync"], 2.0, "--", 0.85, "HA")
    draw_link(ax,  7.5, 14.52,  7.5, 11.85, LINKS["untrust"], 2.0, "-", 0.7, "Untrust→SS")
    draw_link(ax,  3.5, 14.52,  3.8, 11.85, LINKS["untrust"], 2.0, "-", 0.7)

    # ── Super-spines ──────────────────────────────────────────────────────────
    ss = [(3.8,12.8,"SS-1","Arista 7800R3\nLo0: 10.0.0.1"),
          (8.8,12.8,"SS-2","Arista 7800R3\nLo0: 10.0.0.2"),
          (13.8,12.8,"SS-3","Arista 7800R3\nLo0: 10.0.0.3"),
          (19.8,12.8,"SS-4","Arista 7800R3\nLo0: 10.0.0.4")]
    for sx, sy, sl, sub in ss:
        draw_switch(ax, sx, sy, sl, sub, "#0D47A1")
    for i in range(len(ss)):
        for j in range(i+1, len(ss)):
            draw_link(ax, ss[i][0], ss[i][1], ss[j][0], ss[j][1], "#1565C0", 1.2, "--", 0.3)
    draw_link(ax, 13.0, 14.52, 13.8, 13.18, "#546E7A", 1.8, "-", 0.6)
    draw_link(ax, 20.0, 14.52, 19.8, 13.18, LINKS["vpn"],    1.8, "-", 0.6)

    # ── Spines ────────────────────────────────────────────────────────────────
    spines = [
        ( 2.5, 9.0, "SP1-A", "Nexus 9336C\n400GbE | Lo: 10.1.0.1"),
        ( 5.8, 9.0, "SP1-B", "Nexus 9336C\n400GbE | Lo: 10.1.0.2"),
        (10.5, 9.0, "SP2-A", "Nexus 9336C\n400GbE | Lo: 10.2.0.1"),
        (14.0, 9.0, "SP2-B", "Nexus 9336C\n400GbE | Lo: 10.2.0.2"),
        (19.5, 9.0, "SP3-A", "Nexus 9336C\n400GbE | Lo: 10.3.0.1"),
        (23.0, 9.0, "SP3-B", "Nexus 9336C\n400GbE | Lo: 10.3.0.2"),
    ]
    for sx, sy, sl, sub in spines:
        draw_switch(ax, sx, sy, sl, sub, "#1B5E20")
    pod1_sp  = [2.5, 5.8]
    pod2_sp  = [10.5, 14.0]
    pod3_sp  = [19.5, 23.0]
    for ssx, ssy, _, _ in ss:
        for spx in pod1_sp + pod2_sp + pod3_sp:
            draw_link(ax, ssx, ssy+0.41, spx, 9.39, LINKS["super_spine"], 1.2, "-", 0.2)
    draw_link(ax,  3.72, 9.0,  4.58, 9.0, LINKS["ecmp"], 2.0, "--", 0.85, "ECMP")
    draw_link(ax, 11.72, 9.0, 12.78, 9.0, LINKS["ecmp"], 2.0, "--", 0.85, "ECMP")
    draw_link(ax, 20.72, 9.0, 21.78, 9.0, LINKS["ecmp"], 2.0, "--", 0.85, "ECMP")

    # ── Leaves ────────────────────────────────────────────────────────────────
    leaves = [
        ( 3.0, 7.1, "LEAF1-A", "Arista 7050CX3\nVTEP 10.1.1.1", "#2E7D32", pod1_sp),
        ( 7.0, 7.1, "LEAF1-B", "Arista 7050CX3\nVTEP 10.1.1.2", "#2E7D32", pod1_sp),
        ( 9.5, 7.1, "LEAF2-A", "Arista 7050CX3\nVTEP 10.2.1.1", "#4A148C", pod2_sp),
        (13.0, 7.1, "LEAF2-B", "Arista 7050CX3\nVTEP 10.2.1.2", "#4A148C", pod2_sp),
        (16.0, 7.1, "LEAF2-C", "Arista 7050CX3\nVTEP 10.2.1.3", "#4A148C", pod2_sp),
        (19.0, 7.1, "LEAF3-A", "Arista 7050CX3\nVTEP 10.3.1.1", "#283593", pod3_sp),
        (22.5, 7.1, "LEAF3-B", "Arista 7050CX3\nVTEP 10.3.1.2", "#283593", pod3_sp),
    ]
    leaf_link_colors = {
        "#2E7D32": LINKS["leaf_access"],
        "#4A148C": LINKS["vpn"],
        "#283593": LINKS["dc_link"],
    }
    for lx, ly, ln, ls, lc, lspines in leaves:
        draw_switch(ax, lx, ly, ln, ls, lc, 0.40)
        for spx in lspines:
            draw_link(ax, spx, 8.61, lx, 7.49, leaf_link_colors[lc], 1.3, "-", 0.3)

    # ── GPU nodes — Pod 1 ─────────────────────────────────────────────────────
    gpu1a = [(0.8,5.5,"A100-01"),(1.5,5.5,"A100-02"),(2.2,5.5,"A100-03")]
    gpu1b = [(4.3,5.5,"A100-04"),(5.0,5.5,"A100-05"),(5.7,5.5,"A100-06")]
    for gx, gy, gl in gpu1a:
        draw_gpu_node(ax, gx, gy, gl, "#2E7D32")
        draw_link(ax, gx, gy+0.36, 3.0, 6.72, LINKS["leaf_access"], 1.2, "-", 0.6)
    for gx, gy, gl in gpu1b:
        draw_gpu_node(ax, gx, gy, gl, "#2E7D32")
        draw_link(ax, gx, gy+0.36, 7.0, 6.72, LINKS["leaf_access"], 1.2, "-", 0.6)
    for grp in [gpu1a, gpu1b]:
        for i in range(len(grp)-1):
            draw_link(ax, grp[i][0]+0.52, grp[i][1], grp[i+1][0]-0.52, grp[i+1][1],
                      LINKS["nvlink"], 1.5, "-", 0.7)
    ax.text(1.5, 4.95, "GPU Rack A  |  NVIDIA A100 80GB  |  NVLink + RoCEv2",
            ha="center", fontsize=6, color="#E65100", style="italic", zorder=7)
    ax.text(5.0, 4.95, "GPU Rack B  |  NVIDIA A100 80GB  |  NVLink + RoCEv2",
            ha="center", fontsize=6, color="#E65100", style="italic", zorder=7)

    # ── GPU nodes — Pod 2 ─────────────────────────────────────────────────────
    gpu2_groups = [
        ([(8.8,5.5,"H100-01"),(9.5,5.5,"H100-02"),(10.2,5.5,"H100-03")],  9.5),
        ([(12.3,5.5,"H100-04"),(13.0,5.5,"H100-05"),(13.7,5.5,"H100-06")],13.0),
        ([(15.3,5.5,"H100-07"),(16.0,5.5,"H100-08"),(16.7,5.5,"H100-09")],16.0),
    ]
    for grp, lx in gpu2_groups:
        for gx, gy, gl in grp:
            draw_gpu_node(ax, gx, gy, gl, "#4A148C")
            draw_link(ax, gx, gy+0.36, lx, 6.72, LINKS["vpn"], 1.2, "-", 0.6)
        for i in range(len(grp)-1):
            draw_link(ax, grp[i][0]+0.52, grp[i][1], grp[i+1][0]-0.52, grp[i+1][1],
                      LINKS["nvlink"], 1.5, "-", 0.7)
    ax.text(12.5, 4.95,
            "GPU Racks C/D/E  |  NVIDIA H100 80GB SXM  |  NVLink4 + RoCEv2  |  Inference Cluster",
            ha="center", fontsize=6, color="#4A148C", style="italic", zorder=7)

    # ── Storage & mgmt — Pod 3 ────────────────────────────────────────────────
    for sx, sl in [(18.2,"NFS-01"),(19.2,"NFS-02"),(20.2,"CEPH-01")]:
        draw_storage(ax, sx, 5.6, sl)
        draw_link(ax, sx, 5.88, 19.0, 6.72, LINKS["dc_link"], 1.2, "-", 0.55)
    for mx, ml in [(21.8,"MGMT-01"),(22.8,"SIEM"),(23.8,"JUMP")]:
        ax.add_patch(FancyBboxPatch((mx-0.42, 5.34), 0.84, 0.52,
                     boxstyle="round,pad=0.06", facecolor="#E8EAF6",
                     edgecolor="#283593", linewidth=1.5, zorder=5))
        ax.text(mx, 5.6+0.04, ml[:4], ha="center", va="center",
                fontsize=6.5, fontweight="bold", color="#283593", zorder=6)
        ax.text(mx, 5.16, ml, ha="center", va="top",
                fontsize=5.8, color="#37474F", zorder=7)
        draw_link(ax, mx, 5.86, 22.5, 6.72, LINKS["dc_link"], 1.2, "-", 0.55)
    ax.text(21.0, 4.95, "Storage: Ceph / NFS  |  Management: SIEM, Jump Host",
            ha="center", fontsize=6, color="#283593", style="italic", zorder=7)

    # ── Legend ────────────────────────────────────────────────────────────────
    ax.add_patch(FancyBboxPatch((0.3, 0.05), 25.2, 0.34,
                 boxstyle="round,pad=0.08", facecolor="#ECEFF1",
                 edgecolor="#90A4AE", linewidth=1, zorder=8))
    draw_legend(ax, LEGENDS["cloud"], x_start=0.55, y=0.22, spacing=4.1)

    plt.tight_layout(pad=0.2)
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    return output_path
