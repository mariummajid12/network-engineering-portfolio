import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

fig, ax = plt.subplots(1, 1, figsize=(16, 11))
ax.set_xlim(0, 16)
ax.set_ylim(0, 11)
ax.axis('off')
fig.patch.set_facecolor('#0D1117')
ax.set_facecolor('#0D1117')

def router(ax, x, y, label, sublabel, color, textcolor='white'):
    # Outer glow
    circle_glow = plt.Circle((x, y), 0.72, color=color, alpha=0.15, zorder=2)
    ax.add_patch(circle_glow)
    # Main circle
    circle = plt.Circle((x, y), 0.58, color=color, zorder=3, linewidth=2)
    ax.add_patch(circle)
    # Border
    circle_border = plt.Circle((x, y), 0.58, fill=False, edgecolor='white', linewidth=1.5, alpha=0.4, zorder=4)
    ax.add_patch(circle_border)
    # Router icon lines
    ax.plot([x-0.25, x+0.25], [y+0.1, y+0.1], color='white', linewidth=2, zorder=5, alpha=0.9)
    ax.plot([x-0.25, x+0.25], [y-0.05, y-0.05], color='white', linewidth=2, zorder=5, alpha=0.9)
    ax.plot([x-0.25, x+0.25], [y-0.2, y-0.2], color='white', linewidth=2, zorder=5, alpha=0.9)
    # Labels
    ax.text(x, y-0.95, label, ha='center', va='top', fontsize=9.5, fontweight='bold',
            color='white', zorder=6, fontfamily='monospace')
    ax.text(x, y-1.25, sublabel, ha='center', va='top', fontsize=7.5,
            color=color, zorder=6, alpha=0.9)

def link(ax, x1, y1, x2, y2, label='', color='#4FC3F7', style='-', width=2):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=width,
            linestyle=style, zorder=1, alpha=0.7,
            solid_capstyle='round')
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my, label, ha='center', va='center', fontsize=7,
                color='#B0BEC5', zorder=7,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#1A2332', edgecolor='none', alpha=0.85))

def cloud(ax, x, y, label):
    ellipse = mpatches.Ellipse((x, y), 2.2, 1.1, color='#1E3A5F', zorder=1, alpha=0.8)
    ax.add_patch(ellipse)
    ellipse_border = mpatches.Ellipse((x, y), 2.2, 1.1, fill=False,
                                       edgecolor='#4FC3F7', linewidth=1.5, linestyle='--', zorder=2, alpha=0.6)
    ax.add_patch(ellipse_border)
    ax.text(x, y+0.1, '☁', ha='center', va='center', fontsize=16, color='#4FC3F7', zorder=3)
    ax.text(x, y-0.45, label, ha='center', va='center', fontsize=7.5,
            color='#90CAF9', fontweight='bold', zorder=3)

def zone_box(ax, x, y, w, h, label, color):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                           facecolor=color, edgecolor=color,
                           linewidth=1.5, alpha=0.07, zorder=0)
    ax.add_patch(rect)
    rect2 = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                            fill=False, edgecolor=color,
                            linewidth=1, alpha=0.3, zorder=0, linestyle='--')
    ax.add_patch(rect2)
    ax.text(x+0.2, y+h-0.1, label, ha='left', va='top', fontsize=8,
            color=color, alpha=0.7, fontweight='bold')

# ── Zone backgrounds ──────────────────────────────────────────────────────────
zone_box(ax, 0.3, 1.2, 15.4, 2.2, 'ISP / UPSTREAM (AS65100)', '#FF7043')
zone_box(ax, 0.3, 4.0, 15.4, 5.8, 'ENTERPRISE NETWORK', '#42A5F5')
zone_box(ax, 0.5, 4.3, 4.5, 5.0, 'DATA CENTRE (AS65001)', '#66BB6A')
zone_box(ax, 5.5, 4.3, 4.5, 5.0, 'BRANCH (AS65002)', '#FFA726')
zone_box(ax, 10.5, 4.3, 4.8, 5.0, 'CLOUD (AS65003)', '#AB47BC')

# ── ISP routers ───────────────────────────────────────────────────────────────
router(ax, 4,   2.2, 'ISP-RTR-1', 'AS65100 | 203.0.113.1', '#FF7043')
router(ax, 12,  2.2, 'ISP-RTR-2', 'AS65100 | 198.51.100.1', '#FF7043')

# ── Enterprise edge ───────────────────────────────────────────────────────────
router(ax, 2.7, 6.2, 'EDGE-RTR-1', 'AS65001 | 10.0.0.1', '#42A5F5')
router(ax, 4.2, 8.5, 'DC-CORE-1',  'AS65001 | 10.1.0.1',  '#66BB6A')
router(ax, 2.5, 8.5, 'DC-CORE-2',  'AS65001 | 10.1.0.2',  '#66BB6A')

router(ax, 7.7, 6.2, 'BRANCH-RTR', 'AS65002 | 172.16.0.1', '#FFA726')
router(ax, 7.7, 8.5, 'BRANCH-SW',  'AS65002 | 172.16.1.1', '#FFA726')

router(ax, 12.9, 6.2, 'CLOUD-GW',  'AS65003 | 10.100.0.1', '#AB47BC')
cloud(ax, 13.2, 8.8, 'AWS / Azure\nVPC')

# ── Links ─────────────────────────────────────────────────────────────────────
# ISP to edge
link(ax, 4, 2.78, 2.7, 5.62, 'eBGP\n203.0.113.0/30', '#FF7043', width=2.5)
link(ax, 12, 2.78, 12.9, 5.62, 'eBGP\n198.51.100.0/30', '#FF7043', width=2.5)
# ISP to ISP (transit)
link(ax, 4.58, 2.2, 11.42, 2.2, 'Transit', '#FF7043', style='--', width=1.5)

# Edge to branch
link(ax, 3.28, 6.2, 7.12, 6.2, 'eBGP\n10.0.1.0/30', '#4FC3F7', width=2)
# Edge to cloud gw
link(ax, 3.28, 6.2, 12.32, 6.2, 'eBGP / IPSec VPN', '#AB47BC', style='--', width=1.5)
# Edge to DC core
link(ax, 2.7, 6.78, 2.6, 7.92, 'iBGP', '#66BB6A', width=2)
link(ax, 2.7, 6.78, 4.1, 7.92, 'iBGP', '#66BB6A', width=2)
# DC core redundancy
link(ax, 2.5, 8.5, 4.2, 8.5, 'iBGP RR\nredundancy', '#66BB6A', width=1.5)
# Branch internal
link(ax, 7.7, 6.78, 7.7, 7.92, 'iBGP', '#FFA726', width=2)
# Cloud GW to cloud
link(ax, 12.9, 6.78, 13.1, 8.2, 'BGP over\nIPSec', '#AB47BC', style='--', width=1.5)

# ── Legend ────────────────────────────────────────────────────────────────────
legend_x, legend_y = 0.5, 0.85
ax.add_patch(FancyBboxPatch((legend_x-0.2, legend_y-0.5), 8.5, 0.75,
             boxstyle="round,pad=0.1", facecolor='#1A2332',
             edgecolor='#4FC3F7', linewidth=1, alpha=0.9))
ax.plot([legend_x, legend_x+0.6], [legend_y, legend_y], color='#FF7043', linewidth=2.5)
ax.text(legend_x+0.8, legend_y, 'eBGP (external)', color='#B0BEC5', fontsize=8, va='center')
ax.plot([legend_x+3.2, legend_x+3.8], [legend_y, legend_y], color='#66BB6A', linewidth=2.5)
ax.text(legend_x+4.0, legend_y, 'iBGP (internal)', color='#B0BEC5', fontsize=8, va='center')
ax.plot([legend_x+6.4, legend_x+7.0], [legend_y, legend_y], color='#AB47BC',
        linewidth=2, linestyle='--')
ax.text(legend_x+7.2, legend_y, 'IPSec VPN', color='#B0BEC5', fontsize=8, va='center')

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(8, 10.6, 'BGP Multi-AS Enterprise Network Topology',
        ha='center', va='center', fontsize=14, fontweight='bold',
        color='white', fontfamily='monospace')
ax.text(8, 10.25, 'eBGP · iBGP · Route Reflector · IPSec VPN · Multi-homed ISP',
        ha='center', va='center', fontsize=9, color='#90CAF9', alpha=0.85)

plt.tight_layout(pad=0.5)
plt.savefig('/mnt/user-data/outputs/bgp_topology.png', dpi=150,
            bbox_inches='tight', facecolor='#0D1117')
print("Done!")
