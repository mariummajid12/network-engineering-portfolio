import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import matplotlib.patheffects as pe

fig, ax = plt.subplots(figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')
ax.set_facecolor('#F8F9FA')

SPINE_COLOR   = '#1565C0'
LEAF_COLOR    = '#2E7D32'
BORDER_COLOR  = '#6A1B9A'
SERVER_COLOR  = '#37474F'
LINK_SPINE    = '#1976D2'
LINK_LEAF     = '#388E3C'
LINK_VPC      = '#E65100'
LINK_SERVER   = '#78909C'
ZONE_COLORS   = ['#E3F2FD', '#E8F5E9', '#FFF3E0', '#F3E5F5', '#FFEBEE']

def switch_box(ax, x, y, label, sublabel, color):
    rect = FancyBboxPatch((x-1.2, y-0.45), 2.4, 0.9,
                          boxstyle="round,pad=0.12",
                          facecolor=color, edgecolor='white',
                          linewidth=2, alpha=0.95, zorder=4)
    ax.add_patch(rect)
    shadow = FancyBboxPatch((x-1.18, y-0.47), 2.4, 0.9,
                             boxstyle="round,pad=0.12",
                             facecolor='#00000022', edgecolor='none',
                             linewidth=0, zorder=3)
    ax.add_patch(shadow)
    ax.text(x, y+0.12, label, ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='white',
            fontfamily='monospace', zorder=5)
    ax.text(x, y-0.2, sublabel, ha='center', va='center',
            fontsize=7, color='#E3F2FD', alpha=0.92, zorder=5)

def server_box(ax, x, y, label):
    rect = FancyBboxPatch((x-0.65, y-0.28), 1.3, 0.56,
                          boxstyle="round,pad=0.08",
                          facecolor='#ECEFF1', edgecolor='#607D8B',
                          linewidth=1.2, alpha=0.95, zorder=4)
    ax.add_patch(rect)
    ax.text(x, y+0.06, '[S]', ha='center', va='center',
            fontsize=8, fontweight='bold', color='#37474F', zorder=5)
    ax.text(x, y-0.14, label, ha='center', va='center',
            fontsize=6.5, color='#546E7A', zorder=5)

def link(ax, x1, y1, x2, y2, color, style='-', width=2, alpha=0.7, label=''):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=width,
            linestyle=style, zorder=2, alpha=alpha, solid_capstyle='round')
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.1, my, label, ha='left', va='center', fontsize=6.5,
                color='#455A64', zorder=6,
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                          edgecolor='#B0BEC5', alpha=0.9))

def zone_box(ax, x, y, w, h, title, fill_color, border_color):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=fill_color, edgecolor=border_color,
                          linewidth=1.8, alpha=0.6, zorder=0)
    ax.add_patch(rect)
    ax.text(x+0.2, y+h-0.12, title, ha='left', va='top',
            fontsize=8.5, color=border_color, fontweight='bold', alpha=0.9)

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(10, 13.55, 'Data Centre Network — EVPN/VXLAN Leaf-Spine Topology',
        ha='center', va='center', fontsize=15, fontweight='bold', color='#1A237E')
ax.text(10, 13.15, 'Arista 7050CX3 Spine  ·  Cisco Nexus 9300 Leaf  ·  Juniper QFX Border Leaf  ·  BGP EVPN  ·  VXLAN Overlay',
        ha='center', va='center', fontsize=9, color='#455A64')

# ── Zone backgrounds ──────────────────────────────────────────────────────────
zone_box(ax, 0.3, 10.0, 19.4, 2.7,  'SPINE LAYER — IP Fabric Underlay (OSPF / BGP)', '#E3F2FD', '#1565C0')
zone_box(ax, 0.3,  6.5, 19.4, 3.0,  'LEAF LAYER — BGP EVPN Control Plane / VXLAN Data Plane', '#E8F5E9', '#2E7D32')
zone_box(ax, 0.3,  0.3,  5.8, 5.8,  'POD A — Tenant 1  (L2 VNI: 10100 / L3 VNI: 50100)', '#FFF3E0', '#E65100')
zone_box(ax, 6.4,  0.3,  6.1, 5.8,  'POD B — Tenant 2  (L2 VNI: 10200 / L3 VNI: 50200)', '#F3E5F5', '#6A1B9A')
zone_box(ax, 12.8, 0.3,  6.9, 5.8,  'POD C — Storage / DMZ  (VNI: 10300)', '#FFEBEE', '#B71C1C')

# ── Spine layer ───────────────────────────────────────────────────────────────
switch_box(ax, 4.5,  11.6, 'SPINE-1', 'Arista 7050CX3 | Lo0: 10.0.0.1/32', SPINE_COLOR)
switch_box(ax, 10.0, 11.6, 'SPINE-2', 'Arista 7050CX3 | Lo0: 10.0.0.2/32', SPINE_COLOR)
switch_box(ax, 15.5, 11.6, 'SPINE-3', 'Arista 7050CX3 | Lo0: 10.0.0.3/32', SPINE_COLOR)

# Border leaf
switch_box(ax, 10.0, 10.4, 'BORDER-LEAF', 'Juniper QFX5100 | Lo0: 10.0.1.1 | External / WAN', BORDER_COLOR)

# Spine interconnects
link(ax, 5.7,  11.6, 8.8,  11.6, LINK_SPINE, '--', 1.5, 0.4)
link(ax, 11.2, 11.6, 14.3, 11.6, LINK_SPINE, '--', 1.5, 0.4)

# Spine to border leaf
link(ax, 4.5,  11.15, 9.0,  10.62, LINK_SPINE, '-', 2.2, 0.7, 'OSPF p2p')
link(ax, 10.0, 11.15, 10.0, 10.85, LINK_SPINE, '-', 2.2, 0.7)
link(ax, 15.5, 11.15, 11.0, 10.62, LINK_SPINE, '-', 2.2, 0.7)

# ── Leaf layer ────────────────────────────────────────────────────────────────
leaf_positions = [(3.0, 'LEAF-1A', '10.1.1.1'),
                  (6.5, 'LEAF-1B', '10.1.1.2'),
                  (10.0,'LEAF-2A', '10.1.2.1'),
                  (13.5,'LEAF-2B', '10.1.2.2'),
                  (17.0,'LEAF-3A', '10.1.3.1')]

for lx, lname, vtep in leaf_positions:
    switch_box(ax, lx, 7.8, lname, f'Nexus 9300 | VTEP {vtep}', LEAF_COLOR)

# vPC peer links
link(ax, 4.2,  7.8, 5.3,  7.8, LINK_VPC, '--', 2.5, 0.9, 'vPC\npeer')
link(ax, 11.2, 7.8, 12.3, 7.8, LINK_VPC, '--', 2.5, 0.9, 'vPC\npeer')

# Spine to leaf (all connections)
for lx, _, _ in leaf_positions:
    for sx in [4.5, 10.0, 15.5]:
        link(ax, sx, 11.15, lx, 8.25, LINK_LEAF, '-', 1.5, 0.3)

# ── Servers ───────────────────────────────────────────────────────────────────
# Pod A servers
pod_a = [(1.2,4.8,'WEB-01'),(2.8,4.8,'WEB-02'),
         (1.2,3.5,'APP-01'),(2.8,3.5,'APP-02'),
         (4.8,4.1,'DB-01')]
for sx, sy, sl in pod_a:
    server_box(ax, sx, sy, sl)
    lx = 3.0 if sx < 4 else 6.5
    link(ax, sx, sy+0.28, lx, 7.35, LINK_SERVER, '-', 1.2, 0.5)

# Pod B servers
pod_b = [(7.2,4.8,'APP-03'),(8.8,4.8,'APP-04'),
         (7.2,3.5,'MQ-01'), (9.5,3.5,'CACHE-01'),
         (11.5,4.1,'API-01')]
for sx, sy, sl in pod_b:
    server_box(ax, sx, sy, sl)
    lx = 10.0 if sx < 10 else 13.5
    link(ax, sx, sy+0.28, lx, 7.35, LINK_SERVER, '-', 1.2, 0.5)

# Pod C servers
pod_c = [(13.8,4.8,'SAN-01'),(15.5,4.8,'SAN-02'),
         (13.8,3.5,'FW-01'), (17.5,4.0,'MGMT-01')]
for sx, sy, sl in pod_c:
    server_box(ax, sx, sy, sl)
    lx = 13.5 if sx < 15 else 17.0
    link(ax, sx, sy+0.28, lx, 7.35, LINK_SERVER, '-', 1.2, 0.5)

# ── Legend ────────────────────────────────────────────────────────────────────
leg = FancyBboxPatch((0.3, -0.05), 19.4, 0.32,
                     boxstyle="round,pad=0.08",
                     facecolor='#ECEFF1', edgecolor='#B0BEC5',
                     linewidth=1, alpha=1, zorder=5)
ax.add_patch(leg)
items = [
    (LINK_SPINE,  '-',  'Spine uplinks (OSPF underlay)'),
    (LINK_LEAF,   '-',  'Leaf-to-spine (100GbE)'),
    (LINK_VPC,    '--', 'vPC peer-link (MLAG)'),
    (LINK_SERVER, '-',  'Server access (10GbE)'),
    (BORDER_COLOR,'-',  'Border leaf (external routing)'),
]
for i, (c, ls, lbl) in enumerate(items):
    ox = 0.6 + i * 3.8
    ax.plot([ox, ox+0.55], [0.11, 0.11], color=c, linewidth=2.2, linestyle=ls, zorder=6)
    ax.text(ox+0.7, 0.11, lbl, va='center', fontsize=7.5, color='#37474F', zorder=6)

plt.tight_layout(pad=0.3)
plt.savefig('/mnt/user-data/outputs/dc_topology.png', dpi=150,
            bbox_inches='tight', facecolor='#F8F9FA')
print("Done!")
