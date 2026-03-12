import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(20, 13))
ax.set_xlim(0, 20)
ax.set_ylim(0, 13)
ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')
ax.set_facecolor('#F8F9FA')

# Colors
INTERNET_COLOR  = '#B71C1C'
FW_COLOR        = '#E65100'
DMZ_COLOR       = '#F57F17'
TRUST_COLOR     = '#1B5E20'
MGMT_COLOR      = '#1A237E'
SERVER_COLOR    = '#37474F'
LINK_COLORS     = {'untrust': '#EF5350', 'dmz': '#FFA726',
                   'trust': '#66BB6A', 'mgmt': '#5C6BC0', 'vpn': '#AB47BC'}

def box(ax, x, y, w, h, title, sub, color, title_size=9.5):
    shadow = FancyBboxPatch((x-w/2+0.04, y-h/2-0.04), w, h,
                             boxstyle="round,pad=0.12", facecolor='#00000015',
                             edgecolor='none', zorder=3)
    ax.add_patch(shadow)
    rect = FancyBboxPatch((x-w/2, y-h/2), w, h,
                          boxstyle="round,pad=0.12",
                          facecolor=color, edgecolor='white',
                          linewidth=2, alpha=0.95, zorder=4)
    ax.add_patch(rect)
    ax.text(x, y+(0.12 if sub else 0), title, ha='center', va='center',
            fontsize=title_size, fontweight='bold', color='white',
            fontfamily='monospace', zorder=5)
    if sub:
        ax.text(x, y-0.22, sub, ha='center', va='center',
                fontsize=7, color='#E3F2FD', alpha=0.92, zorder=5)

def server(ax, x, y, label, color='#ECEFF1', border='#607D8B'):
    rect = FancyBboxPatch((x-0.7, y-0.3), 1.4, 0.6,
                          boxstyle="round,pad=0.08",
                          facecolor=color, edgecolor=border,
                          linewidth=1.3, zorder=4)
    ax.add_patch(rect)
    ax.text(x, y+0.07, '[SVR]', ha='center', va='center',
            fontsize=7, fontweight='bold', color=SERVER_COLOR, zorder=5)
    ax.text(x, y-0.14, label, ha='center', va='center',
            fontsize=6.5, color='#546E7A', zorder=5)

def link(ax, x1, y1, x2, y2, color, width=2, style='-', alpha=0.75, label=''):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=width,
            linestyle=style, zorder=2, alpha=alpha, solid_capstyle='round')
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx+0.1, my, label, ha='left', va='center', fontsize=6.5,
                color='#455A64', zorder=6,
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                          edgecolor='#B0BEC5', alpha=0.9))

def zone(ax, x, y, w, h, label, fill, border):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                          facecolor=fill, edgecolor=border,
                          linewidth=1.8, alpha=0.55, zorder=0)
    ax.add_patch(rect)
    ax.text(x+0.2, y+h-0.12, label, ha='left', va='top',
            fontsize=8.5, color=border, fontweight='bold', alpha=0.9)

# ── Title ─────────────────────────────────────────────────────────────────────
ax.text(10, 12.6, 'Firewall & Network Security Architecture',
        ha='center', fontsize=15, fontweight='bold', color='#1A237E')
ax.text(10, 12.2, 'Juniper SRX · Fortinet FortiGate · Zone-Based Security · IPSec VPN · DMZ Design · IDS/IPS',
        ha='center', fontsize=9, color='#455A64')

# ── Zones ─────────────────────────────────────────────────────────────────────
zone(ax,  0.3, 10.2, 19.4, 1.6,  'UNTRUST ZONE — Internet / WAN', '#FFEBEE', '#B71C1C')
zone(ax,  0.3,  7.0, 19.4, 2.8,  'PERIMETER — Dual Firewall (Active/Passive HA)', '#FFF3E0', '#E65100')
zone(ax,  0.3,  4.2,  9.2, 2.5,  'DMZ — Publicly Accessible Services', '#FFFDE7', '#F9A825')
zone(ax,  9.8,  4.2,  9.9, 2.5,  'TRUST ZONE — Internal Network', '#E8F5E9', '#2E7D32')
zone(ax,  0.3,  0.3, 19.4, 3.6,  'INTERNAL SEGMENTS', '#E8EAF6', '#283593')

# ── Internet / ISP ────────────────────────────────────────────────────────────
box(ax, 5.0,  11.2, 3.0, 0.7, 'INTERNET', 'ISP-1 | 203.0.113.0/30', INTERNET_COLOR)
box(ax, 15.0, 11.2, 3.0, 0.7, 'BRANCH VPN', 'Remote site | 198.51.100.0/30', '#880E4F')

# ── Firewalls ─────────────────────────────────────────────────────────────────
box(ax, 5.0,  8.2, 3.8, 0.85, 'FW-ACTIVE', 'Juniper SRX4200 | 203.0.113.2 | Active', FW_COLOR)
box(ax, 15.0, 8.2, 3.8, 0.85, 'FW-PASSIVE', 'Fortinet FortiGate 600E | Standby HA', FW_COLOR)

# HA link
link(ax, 6.9, 8.2, 13.1, 8.2, '#FF6F00', 2.5, '--', 0.9, 'HA Sync / Heartbeat')

# ── DMZ switches & servers ────────────────────────────────────────────────────
box(ax, 4.8, 6.0, 2.8, 0.7, 'DMZ-SW', 'Cisco Catalyst | VLAN 100', DMZ_COLOR)
server(ax, 1.5, 5.0, 'WEB-01', '#FFF9C4', '#F9A825')
server(ax, 3.2, 5.0, 'WEB-02', '#FFF9C4', '#F9A825')
server(ax, 5.0, 5.0, 'MAIL-SRV', '#FFF9C4', '#F9A825')
server(ax, 6.8, 5.0, 'DNS-EXT', '#FFF9C4', '#F9A825')
server(ax, 8.5, 5.0, 'PROXY', '#FFF9C4', '#F9A825')

for sx in [1.5, 3.2, 5.0, 6.8, 8.5]:
    link(ax, sx, 5.3, 4.8, 5.65, LINK_COLORS['dmz'], 1.3, '-', 0.6)

# ── Internal core ─────────────────────────────────────────────────────────────
box(ax, 14.5, 6.0, 2.8, 0.7, 'CORE-SW', 'Cisco Nexus | L3 | VLAN 200-400', TRUST_COLOR)

# Internal servers
server(ax, 11.0, 5.0, 'APP-SRV', '#E8F5E9', '#388E3C')
server(ax, 12.8, 5.0, 'DB-SRV',  '#E8F5E9', '#388E3C')
server(ax, 14.5, 5.0, 'FILE-SRV','#E8F5E9', '#388E3C')
server(ax, 16.2, 5.0, 'AD-DC',   '#E8F5E9', '#388E3C')
server(ax, 18.0, 5.0, 'SIEM',    '#E3F2FD', '#1565C0')

for sx in [11.0, 12.8, 14.5, 16.2, 18.0]:
    link(ax, sx, 5.3, 14.5, 5.65, LINK_COLORS['trust'], 1.3, '-', 0.6)

# ── Internal segments ─────────────────────────────────────────────────────────
segments = [
    (2.5,  2.2, 'VLAN 200\nUSER SEGMENT\n10.10.0.0/24', '#E8EAF6', '#3949AB'),
    (6.5,  2.2, 'VLAN 300\nSERVER SEGMENT\n10.20.0.0/24', '#E8F5E9', '#2E7D32'),
    (10.5, 2.2, 'VLAN 400\nVOIP / IoT\n10.30.0.0/24',   '#FFF8E1', '#F9A825'),
    (14.5, 2.2, 'VLAN 500\nMANAGEMENT\n10.99.0.0/24',   '#EDE7F6', '#6A1B9A'),
    (18.2, 2.2, 'OOB MGMT\nOut-of-Band\n10.255.0.0/24', '#FCE4EC', '#880E4F'),
]
for sx, sy, label, fill, border in segments:
    rect = FancyBboxPatch((sx-1.6, sy-0.65), 3.2, 1.3,
                          boxstyle="round,pad=0.12",
                          facecolor=fill, edgecolor=border,
                          linewidth=1.5, alpha=0.85, zorder=3)
    ax.add_patch(rect)
    ax.text(sx, sy, label, ha='center', va='center',
            fontsize=7.5, color=border, fontweight='bold', zorder=4,
            linespacing=1.4)
    link(ax, sx, sy+0.65, 14.5 if sx > 8 else sx, 5.65 if sx > 8 else 4.35,
         border, 1.3, '-', 0.5)

# ── Management box ────────────────────────────────────────────────────────────
box(ax, 10.0, 8.2, 3.2, 0.85, 'IDS/IPS', 'Inline inspection | Snort/Suricata', '#1565C0')

# ── Links ─────────────────────────────────────────────────────────────────────
# Internet to FW
link(ax, 5.0, 10.85, 5.0, 8.63, LINK_COLORS['untrust'], 2.5, '-', 0.8, 'Untrust')
# Branch VPN to FW-PASSIVE
link(ax, 15.0, 10.85, 15.0, 8.63, LINK_COLORS['vpn'], 2.5, '-', 0.8, 'IPSec VPN')
# FW to DMZ
link(ax, 5.0, 7.78, 4.8, 6.35, LINK_COLORS['dmz'], 2, '-', 0.8, 'DMZ zone')
# FW to CORE
link(ax, 5.0, 7.78, 14.5, 6.35, LINK_COLORS['trust'], 2, '-', 0.8, 'Trust zone')
# FW to IDS/IPS
link(ax, 8.9, 8.2, 8.4, 8.2, LINK_COLORS['mgmt'], 2, '-', 0.8)
link(ax, 11.6, 8.2, 13.1, 8.2, LINK_COLORS['mgmt'], 2, '-', 0.8)
# SIEM
link(ax, 18.0, 4.7, 18.0, 3.55, '#1565C0', 1.5, '--', 0.6, 'Log/events')

# ── Legend ────────────────────────────────────────────────────────────────────
leg = FancyBboxPatch((0.3, -0.05), 19.4, 0.32,
                     boxstyle="round,pad=0.08",
                     facecolor='#ECEFF1', edgecolor='#B0BEC5',
                     linewidth=1, zorder=5)
ax.add_patch(leg)
items = [
    (LINK_COLORS['untrust'], '-',  'Untrust / Internet'),
    (LINK_COLORS['dmz'],     '-',  'DMZ traffic'),
    (LINK_COLORS['trust'],   '-',  'Trust / Internal'),
    (LINK_COLORS['vpn'],     '-',  'IPSec VPN'),
    (LINK_COLORS['mgmt'],    '-',  'Management / IDS'),
    ('#FF6F00',              '--', 'HA Sync'),
]
for i, (c, ls, lbl) in enumerate(items):
    ox = 0.6 + i * 3.2
    ax.plot([ox, ox+0.5], [0.11, 0.11], color=c, linewidth=2.2, linestyle=ls, zorder=6)
    ax.text(ox+0.65, 0.11, lbl, va='center', fontsize=7.5, color='#37474F', zorder=6)

plt.tight_layout(pad=0.3)
plt.savefig('/mnt/user-data/outputs/fw_topology.png', dpi=150,
            bbox_inches='tight', facecolor='#F8F9FA')
print("Done!")
