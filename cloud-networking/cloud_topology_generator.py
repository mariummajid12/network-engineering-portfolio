import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(26, 18))
ax.set_xlim(0, 26)
ax.set_ylim(0, 18)
ax.axis('off')
fig.patch.set_facecolor('#F0F4F8')
ax.set_facecolor('#F0F4F8')

# ── Symbol library ─────────────────────────────────────────────────────────────

def draw_router(ax, x, y, label, sublabel='', color='#1565C0', size=0.48):
    c = Circle((x, y), size, facecolor=color, edgecolor='white', linewidth=2.2, zorder=5)
    ax.add_patch(c)
    ax.annotate('', xy=(x+size*0.78, y), xytext=(x-size*0.78, y),
                arrowprops=dict(arrowstyle='->', color='white', lw=2.0), zorder=6)
    ax.annotate('', xy=(x, y+size*0.78), xytext=(x, y-size*0.78),
                arrowprops=dict(arrowstyle='->', color='white', lw=2.0), zorder=6)
    ax.text(x, y-size-0.20, label, ha='center', va='top',
            fontsize=7.5, fontweight='bold', color='#1A237E',
            fontfamily='monospace', zorder=7)
    if sublabel:
        ax.text(x, y-size-0.42, sublabel, ha='center', va='top',
                fontsize=6, color='#455A64', zorder=7)

def draw_switch(ax, x, y, label, sublabel='', color='#1565C0', size=0.44):
    w, h = size*2.8, size*0.88
    rect = FancyBboxPatch((x-w/2, y-h/2), w, h,
                          boxstyle="round,pad=0.07",
                          facecolor=color, edgecolor='white',
                          linewidth=2, zorder=5)
    ax.add_patch(rect)
    # Port lines
    for i in range(6):
        px = x - size*0.95 + i * size*0.38
        ax.plot([px, px], [y+h*0.28, y+h*0.58],
                color='white', linewidth=1.6, zorder=6)
        ax.plot([px-0.04, px+0.04], [y+h*0.58, y+h*0.58],
                color='white', linewidth=1.6, zorder=6)
    ax.annotate('', xy=(x+size*0.62, y-0.04), xytext=(x-size*0.62, y-0.04),
                arrowprops=dict(arrowstyle='<->', color='white', lw=1.4), zorder=6)
    ax.text(x, y-h/2-0.18, label, ha='center', va='top',
            fontsize=7.5, fontweight='bold', color=color,
            fontfamily='monospace', zorder=7)
    if sublabel:
        ax.text(x, y-h/2-0.38, sublabel, ha='center', va='top',
                fontsize=6, color='#455A64', zorder=7)

def draw_gpu_node(ax, x, y, label, color='#1B5E20'):
    """GPU server — distinctive shape with GPU chip indicators"""
    # Main body
    rect = FancyBboxPatch((x-0.52, y-0.36), 1.04, 0.72,
                          boxstyle="round,pad=0.07",
                          facecolor='#263238', edgecolor=color,
                          linewidth=2, zorder=5)
    ax.add_patch(rect)
    # GPU chip grid (2x2)
    for gi in range(2):
        for gj in range(2):
            gx = x - 0.22 + gi * 0.28
            gy = y + 0.08 - gj * 0.22
            chip = FancyBboxPatch((gx-0.09, gy-0.07), 0.18, 0.14,
                                  boxstyle="round,pad=0.02",
                                  facecolor=color, edgecolor='white',
                                  linewidth=0.8, zorder=6)
            ax.add_patch(chip)
    # LED
    dot = Circle((x-0.35, y-0.2), 0.04, facecolor='#69F0AE',
                 edgecolor='none', zorder=7)
    ax.add_patch(dot)
    ax.text(x, y-0.50, label, ha='center', va='top',
            fontsize=6, color='#37474F', fontweight='bold', zorder=7)

def draw_storage(ax, x, y, label):
    """Storage node — cylinder-like shape"""
    color = '#4527A0'
    rect = FancyBboxPatch((x-0.44, y-0.28), 0.88, 0.56,
                          boxstyle="round,pad=0.06",
                          facecolor='#EDE7F6', edgecolor=color,
                          linewidth=1.8, zorder=5)
    ax.add_patch(rect)
    # Lines to suggest disk platters
    for li in range(3):
        ly = y - 0.12 + li * 0.12
        ax.plot([x-0.3, x+0.3], [ly, ly], color=color,
                linewidth=1, alpha=0.5, zorder=6)
    ax.text(x, y-0.42, label, ha='center', va='top',
            fontsize=6, color=color, fontweight='bold', zorder=7)

def draw_firewall(ax, x, y, label, sublabel='', color='#D84315', size=0.46):
    shield_x = [x-size*0.68, x+size*0.68, x+size*0.68, x, x-size*0.68]
    shield_y = [y+size*0.82, y+size*0.82, y-size*0.16, y-size*0.88, y-size*0.16]
    shield = plt.Polygon(list(zip(shield_x, shield_y)),
                         facecolor=color, edgecolor='white', linewidth=2, zorder=5)
    ax.add_patch(shield)
    lock = FancyBboxPatch((x-0.15, y-0.09), 0.30, 0.22,
                          boxstyle="round,pad=0.03",
                          facecolor='white', edgecolor=color,
                          linewidth=1.3, zorder=6)
    ax.add_patch(lock)
    arc = mpatches.Arc((x, y+0.13), 0.21, 0.21, angle=0,
                       theta1=0, theta2=180,
                       color='white', linewidth=2.2, zorder=7)
    ax.add_patch(arc)
    ax.text(x, y-size-0.22, label, ha='center', va='top',
            fontsize=7.5, fontweight='bold', color='#BF360C',
            fontfamily='monospace', zorder=7)
    if sublabel:
        ax.text(x, y-size-0.44, sublabel, ha='center', va='top',
                fontsize=6, color='#455A64', zorder=7)

def draw_cloud(ax, x, y, label, color='#37474F'):
    for dx, dy, r in [(0,0.05,0.48),(0.4,0.14,0.35),(-0.4,0.14,0.35),(0,0.38,0.33)]:
        c = Circle((x+dx, y+dy), r, facecolor=color, edgecolor='white',
                   linewidth=1.4, zorder=4, alpha=0.92)
        ax.add_patch(c)
    rect = FancyBboxPatch((x-0.48, y-0.28), 0.96, 0.34,
                          boxstyle="square,pad=0",
                          facecolor=color, edgecolor='none', zorder=3, alpha=0.92)
    ax.add_patch(rect)
    ax.text(x, y-0.48, label, ha='center', va='top',
            fontsize=7.5, fontweight='bold', color=color,
            fontfamily='monospace', zorder=7)

def link(ax, x1, y1, x2, y2, color, width=1.8, style='-', alpha=0.65, label=''):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=width,
            linestyle=style, zorder=2, alpha=alpha, solid_capstyle='round')
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.08, my, label, ha='left', va='center', fontsize=5.8,
                color='#455A64', zorder=8,
                bbox=dict(boxstyle='round,pad=0.12', facecolor='white',
                          edgecolor='#B0BEC5', alpha=0.92))

def zone(ax, x, y, w, h, label, fill, border, label_size=8):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=fill, edgecolor=border,
                          linewidth=2, alpha=0.45, zorder=0)
    ax.add_patch(rect)
    ax.text(x+0.2, y+h-0.14, label, ha='left', va='top',
            fontsize=label_size, color=border, fontweight='bold', alpha=0.95)

# ══════════════════════════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════════════════════════
ax.text(13, 17.65, 'Cloud Data Centre — AI/ML GPU Fabric  |  Spine-Leaf with Multi-Pod Architecture',
        ha='center', fontsize=15, fontweight='bold', color='#1A237E')
ax.text(13, 17.25,
        'Arista 7800R3 Super-Spine  ·  Cisco Nexus 9336C Spine  ·  Arista 7050CX3 Leaf  ·  400GbE Fabric  ·  RoCEv2 / RDMA  ·  BGP EVPN  ·  VXLAN',
        ha='center', fontsize=8.5, color='#455A64')

# ══════════════════════════════════════════════════════════════════════════════
# ZONES
# ══════════════════════════════════════════════════════════════════════════════
zone(ax,  0.3, 14.5, 25.2, 2.8,  'INTERNET EDGE & WAN', '#FFEBEE', '#B71C1C', 8)
zone(ax,  0.3, 11.2, 25.2, 2.9,  'SUPER-SPINE LAYER — Cross-Pod Routing (BGP / OSPF Underlay)', '#E3F2FD', '#0D47A1', 8)
zone(ax,  0.3,  7.8, 25.2, 3.0,  'SPINE LAYER — Per-Pod IP Fabric (400GbE)', '#E8F5E9', '#1B5E20', 8)
zone(ax,  0.3,  0.4,  7.8, 7.1,  'POD 1 — GPU Cluster A  (AI Training)', '#FFF8E1', '#E65100', 8)
zone(ax,  8.4,  0.4,  8.8, 7.1,  'POD 2 — GPU Cluster B  (AI Inference)', '#F3E5F5', '#4A148C', 8)
zone(ax, 17.5,  0.4,  8.0, 7.1,  'POD 3 — Storage & Management', '#E8EAF6', '#283593', 8)

# ══════════════════════════════════════════════════════════════════════════════
# INTERNET EDGE
# ══════════════════════════════════════════════════════════════════════════════
draw_cloud(ax,  3.5, 16.1, 'INTERNET\n/ WAN', '#B71C1C')
draw_cloud(ax, 10.5, 16.1, 'CLOUD PEERING\nAWS / Azure / GCP', '#37474F')
draw_cloud(ax, 17.5, 16.1, 'MPLS / SD-WAN\nBranch Offices', '#4527A0')

draw_firewall(ax,  3.5, 14.9, 'EDGE-FW-1', 'Juniper SRX4600 | Active', '#D84315')
draw_firewall(ax,  7.5, 14.9, 'EDGE-FW-2', 'Juniper SRX4600 | Standby', '#D84315')
draw_router(ax,   13.0, 14.9, 'PEERING-RTR', 'Cisco ASR 9000 | BGP | AS65000', '#1565C0')
draw_router(ax,   20.0, 14.9, 'WAN-RTR', 'Juniper MX204 | MPLS | SD-WAN', '#1565C0')

# HA link
link(ax, 4.44, 14.9, 6.56, 14.9, '#FF6F00', 2, '--', 0.85, 'HA Sync')

# Cloud to edge
link(ax,  3.5, 15.62,  3.5, 15.38, '#EF5350', 2.2, '-', 0.8)
link(ax, 10.5, 15.62, 13.0, 15.38, '#546E7A', 2.2, '-', 0.8, 'BGP peering')
link(ax, 17.5, 15.62, 20.0, 15.38, '#7B1FA2', 2.2, '-', 0.8, 'MPLS')
link(ax,  7.5, 14.52,  7.5, 11.85, '#EF5350', 2, '-', 0.7, 'Untrust→SS')
link(ax,  3.5, 14.52,  3.8, 11.85, '#EF5350', 2, '-', 0.7)

# ══════════════════════════════════════════════════════════════════════════════
# SUPER-SPINE LAYER
# ══════════════════════════════════════════════════════════════════════════════
ss_positions = [
    (3.8,  12.8, 'SS-1', 'Arista 7800R3\nLo0: 10.0.0.1'),
    (8.8,  12.8, 'SS-2', 'Arista 7800R3\nLo0: 10.0.0.2'),
    (13.8, 12.8, 'SS-3', 'Arista 7800R3\nLo0: 10.0.0.3'),
    (19.8, 12.8, 'SS-4', 'Arista 7800R3\nLo0: 10.0.0.4'),
]
for sx, sy, sl, sub in ss_positions:
    draw_switch(ax, sx, sy, sl, sub, '#0D47A1')

# Super-spine mesh links
for i in range(len(ss_positions)):
    for j in range(i+1, len(ss_positions)):
        x1, y1 = ss_positions[i][0], ss_positions[i][1]
        x2, y2 = ss_positions[j][0], ss_positions[j][1]
        link(ax, x1, y1, x2, y2, '#1565C0', 1.2, '--', 0.3)

# Peering/WAN routers to super-spines
link(ax, 13.0, 14.52, 13.8, 13.18, '#546E7A', 1.8, '-', 0.6)
link(ax, 20.0, 14.52, 19.8, 13.18, '#7B1FA2', 1.8, '-', 0.6)

# ══════════════════════════════════════════════════════════════════════════════
# SPINE LAYER  (2 spines per pod)
# ══════════════════════════════════════════════════════════════════════════════
# Pod 1 spines
draw_switch(ax,  2.5, 9.0, 'SP1-A', 'Nexus 9336C\n400GbE | Lo: 10.1.0.1', '#1B5E20')
draw_switch(ax,  5.8, 9.0, 'SP1-B', 'Nexus 9336C\n400GbE | Lo: 10.1.0.2', '#1B5E20')
# Pod 2 spines
draw_switch(ax, 10.5, 9.0, 'SP2-A', 'Nexus 9336C\n400GbE | Lo: 10.2.0.1', '#1B5E20')
draw_switch(ax, 14.0, 9.0, 'SP2-B', 'Nexus 9336C\n400GbE | Lo: 10.2.0.2', '#1B5E20')
# Pod 3 spines
draw_switch(ax, 19.5, 9.0, 'SP3-A', 'Nexus 9336C\n400GbE | Lo: 10.3.0.1', '#1B5E20')
draw_switch(ax, 23.0, 9.0, 'SP3-B', 'Nexus 9336C\n400GbE | Lo: 10.3.0.2', '#1B5E20')

# Super-spine to spine (each SS connects to all pods)
ss_xs = [s[0] for s in ss_positions]
pod1_sp = [2.5, 5.8]
pod2_sp = [10.5, 14.0]
pod3_sp = [19.5, 23.0]

for ssx in ss_xs:
    for spx in pod1_sp + pod2_sp + pod3_sp:
        link(ax, ssx, 12.41, spx, 9.39, '#42A5F5', 1.2, '-', 0.2)

# Intra-pod spine peer links
link(ax,  3.72, 9.0,  4.58, 9.0, '#E65100', 2, '--', 0.85, 'ECMP')
link(ax, 11.72, 9.0, 12.78, 9.0, '#4A148C', 2, '--', 0.85, 'ECMP')
link(ax, 20.72, 9.0, 21.78, 9.0, '#283593', 2, '--', 0.85, 'ECMP')

# ══════════════════════════════════════════════════════════════════════════════
# LEAF SWITCHES & GPU NODES — POD 1 (AI Training)
# ══════════════════════════════════════════════════════════════════════════════
leaf1_data = [(1.5, 7.1, 'LEAF1-A', 'Arista 7050CX3\nVTEP 10.1.1.1'),
              (5.0, 7.1, 'LEAF1-B', 'Arista 7050CX3\nVTEP 10.1.1.2')]

for lx, ly, ln, ls in leaf1_data:
    draw_switch(ax, lx, ly, ln, ls, '#2E7D32', 0.40)

# Spine to leaf — pod 1
for lx, ly, _, _ in leaf1_data:
    for spx in pod1_sp:
        link(ax, spx, 8.61, lx, 7.49, '#66BB6A', 1.3, '-', 0.3)

# GPU nodes under leaf1-A
gpu1a = [(0.8,5.5,'A100-01'),(1.5,5.5,'A100-02'),(2.2,5.5,'A100-03')]
for gx, gy, gl in gpu1a:
    draw_gpu_node(ax, gx, gy, gl, '#2E7D32')
    link(ax, gx, gy+0.36, 1.5, 6.72, '#A5D6A7', 1.2, '-', 0.6)

# GPU nodes under leaf1-B
gpu1b = [(4.3,5.5,'A100-04'),(5.0,5.5,'A100-05'),(5.7,5.5,'A100-06')]
for gx, gy, gl in gpu1b:
    draw_gpu_node(ax, gx, gy, gl, '#2E7D32')
    link(ax, gx, gy+0.36, 5.0, 6.72, '#A5D6A7', 1.2, '-', 0.6)

# NVLink / RoCEv2 rail links between GPUs (intra-pod)
for i in range(len(gpu1a)-1):
    link(ax, gpu1a[i][0]+0.52, gpu1a[i][1],
         gpu1a[i+1][0]-0.52, gpu1a[i+1][1],
         '#FF6F00', 1.5, '-', 0.7)
for i in range(len(gpu1b)-1):
    link(ax, gpu1b[i][0]+0.52, gpu1b[i][1],
         gpu1b[i+1][0]-0.52, gpu1b[i+1][1],
         '#FF6F00', 1.5, '-', 0.7)

# GPU rack labels
ax.text(1.5, 4.95, 'GPU Rack A  |  NVIDIA A100 80GB  |  NVLink + RoCEv2',
        ha='center', fontsize=6, color='#E65100', style='italic', zorder=7)
ax.text(5.0, 4.95, 'GPU Rack B  |  NVIDIA A100 80GB  |  NVLink + RoCEv2',
        ha='center', fontsize=6, color='#E65100', style='italic', zorder=7)

# ══════════════════════════════════════════════════════════════════════════════
# LEAF SWITCHES & GPU NODES — POD 2 (AI Inference)
# ══════════════════════════════════════════════════════════════════════════════
leaf2_data = [(9.5,  7.1, 'LEAF2-A', 'Arista 7050CX3\nVTEP 10.2.1.1'),
              (13.0, 7.1, 'LEAF2-B', 'Arista 7050CX3\nVTEP 10.2.1.2'),
              (16.0, 7.1, 'LEAF2-C', 'Arista 7050CX3\nVTEP 10.2.1.3')]

for lx, ly, ln, ls in leaf2_data:
    draw_switch(ax, lx, ly, ln, ls, '#4A148C', 0.40)

for lx, ly, _, _ in leaf2_data:
    for spx in pod2_sp:
        link(ax, spx, 8.61, lx, 7.49, '#CE93D8', 1.3, '-', 0.3)

# GPU nodes — pod 2 (H100 for inference)
gpu2a = [(8.8,5.5,'H100-01'),(9.5,5.5,'H100-02'),(10.2,5.5,'H100-03')]
gpu2b = [(12.3,5.5,'H100-04'),(13.0,5.5,'H100-05'),(13.7,5.5,'H100-06')]
gpu2c = [(15.3,5.5,'H100-07'),(16.0,5.5,'H100-08'),(16.7,5.5,'H100-09')]

for grp, lx in [(gpu2a,9.5),(gpu2b,13.0),(gpu2c,16.0)]:
    for gx, gy, gl in grp:
        draw_gpu_node(ax, gx, gy, gl, '#4A148C')
        link(ax, gx, gy+0.36, lx, 6.72, '#CE93D8', 1.2, '-', 0.6)
    for i in range(len(grp)-1):
        link(ax, grp[i][0]+0.52, grp[i][1],
             grp[i+1][0]-0.52, grp[i+1][1],
             '#FF6F00', 1.5, '-', 0.7)

ax.text(12.5, 4.95, 'GPU Racks C/D/E  |  NVIDIA H100 80GB SXM  |  NVLink4 + RoCEv2  |  Inference Cluster',
        ha='center', fontsize=6, color='#4A148C', style='italic', zorder=7)

# ══════════════════════════════════════════════════════════════════════════════
# LEAF SWITCHES & STORAGE — POD 3
# ══════════════════════════════════════════════════════════════════════════════
leaf3_data = [(19.0, 7.1, 'LEAF3-A', 'Arista 7050CX3\nVTEP 10.3.1.1'),
              (22.5, 7.1, 'LEAF3-B', 'Arista 7050CX3\nVTEP 10.3.1.2')]

for lx, ly, ln, ls in leaf3_data:
    draw_switch(ax, lx, ly, ln, ls, '#283593', 0.40)

for lx, ly, _, _ in leaf3_data:
    for spx in pod3_sp:
        link(ax, spx, 8.61, lx, 7.49, '#90CAF9', 1.3, '-', 0.3)

# Storage nodes
storage_nodes = [(18.2, 5.6, 'NFS-01'), (19.2, 5.6, 'NFS-02'),
                 (20.2, 5.6, 'CEPH-01')]
for sx, sy, sl in storage_nodes:
    draw_storage(ax, sx, sy, sl)
    link(ax, sx, sy+0.28, 19.0, 6.72, '#90CAF9', 1.2, '-', 0.55)

# Mgmt servers
from matplotlib.patches import FancyBboxPatch as FBP
mgmt_nodes = [(21.8,5.6,'MGMT-01'),(22.8,5.6,'SIEM'),(23.8,5.6,'JUMP')]
for mx, my, ml in mgmt_nodes:
    r = FancyBboxPatch((mx-0.42, my-0.26), 0.84, 0.52,
                       boxstyle="round,pad=0.06",
                       facecolor='#E8EAF6', edgecolor='#283593',
                       linewidth=1.5, zorder=5)
    ax.add_patch(r)
    ax.text(mx, my+0.04, ml[:4], ha='center', va='center',
            fontsize=6.5, fontweight='bold', color='#283593', zorder=6)
    ax.text(mx, my-0.38, ml, ha='center', va='top',
            fontsize=5.8, color='#37474F', zorder=7)
    link(ax, mx, my+0.26, 22.5, 6.72, '#90CAF9', 1.2, '-', 0.55)

ax.text(21.0, 4.95, 'Storage: Ceph / NFS  |  Management: SIEM, Jump Host',
        ha='center', fontsize=6, color='#283593', style='italic', zorder=7)

# ══════════════════════════════════════════════════════════════════════════════
# BANDWIDTH ANNOTATIONS on key links
# ══════════════════════════════════════════════════════════════════════════════
ax.text(6.3, 12.0, '400GbE\nuplinks', ha='center', fontsize=6,
        color='#0D47A1', style='italic', zorder=8)
ax.text(6.3, 8.7, '400GbE\nleaf↔spine', ha='center', fontsize=6,
        color='#1B5E20', style='italic', zorder=8)

# ══════════════════════════════════════════════════════════════════════════════
# LEGEND
# ══════════════════════════════════════════════════════════════════════════════
leg = FancyBboxPatch((0.3, 0.05), 25.2, 0.34,
                     boxstyle="round,pad=0.08",
                     facecolor='#ECEFF1', edgecolor='#90A4AE',
                     linewidth=1, zorder=8)
ax.add_patch(leg)
legend_items = [
    ('#42A5F5', '-',  'Super-spine uplinks'),
    ('#66BB6A', '-',  'Pod 1 fabric (400GbE)'),
    ('#CE93D8', '-',  'Pod 2 fabric (400GbE)'),
    ('#90CAF9', '-',  'Pod 3 fabric (100GbE)'),
    ('#FF6F00', '-',  'NVLink / RoCEv2 GPU rail'),
    ('#1B5E20', '--', 'Intra-spine ECMP'),
    ('#FF4444', '--', 'HA Sync'),
]
for i, (c, ls, lbl) in enumerate(legend_items):
    ox = 0.55 + i * 3.58
    ax.plot([ox, ox+0.48], [0.22, 0.22], color=c, linewidth=2.2,
            linestyle=ls, zorder=9)
    ax.text(ox+0.62, 0.22, lbl, va='center', fontsize=7,
            color='#37474F', zorder=9)

plt.tight_layout(pad=0.2)
plt.savefig('/mnt/user-data/outputs/cloud_topology.png', dpi=150,
            bbox_inches='tight', facecolor='#F0F4F8')
print("Done!")
