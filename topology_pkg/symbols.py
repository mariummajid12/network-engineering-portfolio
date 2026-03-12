"""
symbols.py
----------
Reusable Cisco-style network symbol drawing functions.
Every function takes a matplotlib Axes object (ax) as its first argument
and draws directly onto it. All positional arguments use data coordinates.
"""

import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.pyplot as plt

from .styles import COLORS, VULN_SEVERITY


# ── Helpers ────────────────────────────────────────────────────────────────────

def _shadow(ax, x, y, w, h, zorder=3):
    """Subtle drop shadow for any rectangular element."""
    ax.add_patch(FancyBboxPatch(
        (x + 0.04, y - 0.04), w, h,
        boxstyle="round,pad=0.12",
        facecolor="#00000015", edgecolor="none",
        linewidth=0, zorder=zorder,
    ))


def _vuln_badge(ax, x, y, severity):
    """Coloured severity badge overlaid on a device symbol."""
    if severity is None:
        return
    cfg = VULN_SEVERITY[severity]
    badge = FancyBboxPatch(
        (x + 0.28, y + 0.06), 0.38, 0.18,
        boxstyle="round,pad=0.03",
        facecolor=cfg["color"], edgecolor="white",
        linewidth=0.8, zorder=8,
    )
    ax.add_patch(badge)
    ax.text(x + 0.47, y + 0.15, cfg["label"],
            ha="center", va="center",
            fontsize=5.5, fontweight="bold", color="white", zorder=9)


# ── Network device symbols ─────────────────────────────────────────────────────

def draw_router(ax, x, y, label, sublabel="", color=None, size=0.48):
    """
    Cisco-style router: filled circle with bidirectional crossing arrows.

    Parameters
    ----------
    ax       : matplotlib Axes
    x, y     : centre position in data coordinates
    label    : primary label drawn below the symbol
    sublabel : smaller secondary label (e.g. loopback address)
    color    : fill colour; defaults to COLORS["router"]
    size     : radius of the circle
    """
    color = color or COLORS["router"]
    ax.add_patch(Circle(
        (x, y), size,
        facecolor=color, edgecolor="white", linewidth=2.2, zorder=5,
    ))
    ax.annotate("", xy=(x + size * 0.78, y), xytext=(x - size * 0.78, y),
                arrowprops=dict(arrowstyle="->", color="white", lw=2.0), zorder=6)
    ax.annotate("", xy=(x, y + size * 0.78), xytext=(x, y - size * 0.78),
                arrowprops=dict(arrowstyle="->", color="white", lw=2.0), zorder=6)
    ax.text(x, y - size - 0.22, label,
            ha="center", va="top", fontsize=7.5, fontweight="bold",
            color="#1A237E", fontfamily="monospace", zorder=7)
    if sublabel:
        ax.text(x, y - size - 0.44, sublabel,
                ha="center", va="top", fontsize=6.0, color="#455A64", zorder=7)


def draw_border_router(ax, x, y, label, sublabel="", color=None, size=0.50):
    """
    Border / edge router: double-ring circle with crossing arrows.
    Visual distinction from a plain router indicates external-facing role.
    """
    color = color or COLORS["border_router"]
    ax.add_patch(Circle(
        (x, y), size,
        facecolor=color, edgecolor="white", linewidth=2.5, zorder=5,
    ))
    ax.add_patch(Circle(
        (x, y), size * 0.75,
        facecolor="none", edgecolor="white", linewidth=1.5, zorder=6, alpha=0.5,
    ))
    ax.annotate("", xy=(x + size * 0.78, y), xytext=(x - size * 0.78, y),
                arrowprops=dict(arrowstyle="->", color="white", lw=2.2), zorder=7)
    ax.annotate("", xy=(x, y + size * 0.78), xytext=(x, y - size * 0.78),
                arrowprops=dict(arrowstyle="->", color="white", lw=2.2), zorder=7)
    ax.text(x, y - size - 0.22, label,
            ha="center", va="top", fontsize=8.0, fontweight="bold",
            color="#311B92", fontfamily="monospace", zorder=8)
    if sublabel:
        ax.text(x, y - size - 0.46, sublabel,
                ha="center", va="top", fontsize=6.0, color="#455A64", zorder=8)


def draw_switch(ax, x, y, label, sublabel="", color=None, size=0.44):
    """
    Cisco-style switch: rectangular body with port stubs on top and a
    bidirectional arrow inside indicating switching function.

    Parameters
    ----------
    size : controls overall scale; width = size*2.8, height = size*0.88
    """
    color = color or COLORS["switch_core"]
    w, h = size * 2.8, size * 0.88
    _shadow(ax, x - w / 2, y - h / 2, w, h)
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.07",
        facecolor=color, edgecolor="white", linewidth=2, zorder=5,
    ))
    # Port stubs
    for i in range(6):
        px = x - size * 0.95 + i * size * 0.38
        ax.plot([px, px], [y + h * 0.28, y + h * 0.58],
                color="white", linewidth=1.6, zorder=6)
        ax.plot([px - 0.04, px + 0.04], [y + h * 0.58, y + h * 0.58],
                color="white", linewidth=1.6, zorder=6)
    ax.annotate("", xy=(x + size * 0.62, y - 0.04), xytext=(x - size * 0.62, y - 0.04),
                arrowprops=dict(arrowstyle="<->", color="white", lw=1.4), zorder=6)
    ax.text(x, y - h / 2 - 0.18, label,
            ha="center", va="top", fontsize=7.5, fontweight="bold",
            color=color, fontfamily="monospace", zorder=7)
    if sublabel:
        ax.text(x, y - h / 2 - 0.38, sublabel,
                ha="center", va="top", fontsize=6.0, color="#455A64", zorder=7)


def draw_firewall(ax, x, y, label, sublabel="", color=None, size=0.46):
    """
    Firewall symbol: shield shape with padlock overlay.
    Shield is the universally recognised security perimeter icon.
    """
    color = color or COLORS["firewall"]
    sx = [x - size * 0.70, x + size * 0.70, x + size * 0.70, x, x - size * 0.70]
    sy = [y + size * 0.85, y + size * 0.85, y - size * 0.18, y - size * 0.92, y - size * 0.18]
    ax.add_patch(plt.Polygon(
        list(zip(sx, sy)),
        facecolor=color, edgecolor="white", linewidth=2, zorder=5,
    ))
    ax.add_patch(FancyBboxPatch(
        (x - 0.15, y - 0.09), 0.30, 0.22,
        boxstyle="round,pad=0.03",
        facecolor="white", edgecolor=color, linewidth=1.3, zorder=6,
    ))
    ax.add_patch(mpatches.Arc(
        (x, y + 0.13), 0.21, 0.21,
        theta1=0, theta2=180,
        color="white", linewidth=2.2, zorder=7,
    ))
    ax.text(x, y - size - 0.24, label,
            ha="center", va="top", fontsize=7.5, fontweight="bold",
            color="#BF360C", fontfamily="monospace", zorder=7)
    if sublabel:
        ax.text(x, y - size - 0.46, sublabel,
                ha="center", va="top", fontsize=6.0, color="#455A64", zorder=7)


def draw_cloud(ax, x, y, label, color=None):
    """
    Cloud / internet symbol: overlapping circles with rectangular base.
    Used to represent internet, WAN, cloud providers, and ISPs.
    """
    color = color or COLORS["cloud_generic"]
    for dx, dy, r in [(0, 0.04, 0.44), (0.37, 0.13, 0.32),
                      (-0.37, 0.13, 0.32), (0, 0.34, 0.30)]:
        ax.add_patch(Circle(
            (x + dx, y + dy), r,
            facecolor=color, edgecolor="white",
            linewidth=1.3, zorder=4, alpha=0.92,
        ))
    ax.add_patch(FancyBboxPatch(
        (x - 0.44, y - 0.26), 0.88, 0.32,
        boxstyle="square,pad=0",
        facecolor=color, edgecolor="none", zorder=3, alpha=0.92,
    ))
    ax.text(x, y - 0.44, label,
            ha="center", va="top", fontsize=7.5, fontweight="bold",
            color=color, fontfamily="monospace", zorder=7)


# ── Server / endpoint symbols ──────────────────────────────────────────────────

def draw_server(ax, x, y, label, color=None, vuln=None):
    """
    Generic server symbol: three stacked rack unit bars with an LED indicator.
    LED color reflects vulnerability severity when `vuln` is provided.

    Parameters
    ----------
    vuln : one of "critical", "high", "medium", "low", or None
    """
    color = color or COLORS["server_generic"]
    led_color = VULN_SEVERITY[vuln]["led"]
    for i in range(3):
        bar_y = y + i * 0.16 - 0.16
        ax.add_patch(FancyBboxPatch(
            (x - 0.38, bar_y), 0.76, 0.13,
            boxstyle="round,pad=0.03",
            facecolor=color if i == 2 else "#546E7A",
            edgecolor="white", linewidth=0.8, zorder=5,
        ))
        ax.add_patch(Circle(
            (x + 0.26, bar_y + 0.065), 0.03,
            facecolor=led_color, edgecolor="none", zorder=6,
        ))
    _vuln_badge(ax, x, y, vuln)
    ax.text(x, y - 0.26, label,
            ha="center", va="top", fontsize=6.0,
            color="#37474F", fontweight="bold", zorder=7)


def draw_gpu_node(ax, x, y, label, color=None):
    """
    GPU server symbol: dark chassis with a 2×2 grid of GPU chip squares.
    Represents DGX nodes or GPU-accelerated compute servers.
    """
    color = color or COLORS["gpu_training"]
    ax.add_patch(FancyBboxPatch(
        (x - 0.52, y - 0.36), 1.04, 0.72,
        boxstyle="round,pad=0.07",
        facecolor="#263238", edgecolor=color, linewidth=2, zorder=5,
    ))
    for gi in range(2):
        for gj in range(2):
            gx = x - 0.22 + gi * 0.28
            gy = y + 0.08 - gj * 0.22
            ax.add_patch(FancyBboxPatch(
                (gx - 0.09, gy - 0.07), 0.18, 0.14,
                boxstyle="round,pad=0.02",
                facecolor=color, edgecolor="white", linewidth=0.8, zorder=6,
            ))
    ax.add_patch(Circle(
        (x - 0.35, y - 0.2), 0.04,
        facecolor="#69F0AE", edgecolor="none", zorder=7,
    ))
    ax.text(x, y - 0.50, label,
            ha="center", va="top", fontsize=6.0,
            color="#37474F", fontweight="bold", zorder=7)


def draw_storage(ax, x, y, label):
    """
    Storage node symbol: rounded rectangle with horizontal platter lines,
    suggesting a disk array or NAS/SAN device.
    """
    color = COLORS["storage"]
    ax.add_patch(FancyBboxPatch(
        (x - 0.44, y - 0.28), 0.88, 0.56,
        boxstyle="round,pad=0.06",
        facecolor="#EDE7F6", edgecolor=color, linewidth=1.8, zorder=5,
    ))
    for li in range(3):
        ly = y - 0.12 + li * 0.12
        ax.plot([x - 0.30, x + 0.30], [ly, ly],
                color=color, linewidth=1.0, alpha=0.5, zorder=6)
    ax.text(x, y - 0.42, label,
            ha="center", va="top", fontsize=6.0,
            color=color, fontweight="bold", zorder=7)


def draw_medical_device(ax, x, y, label, vuln=None):
    """
    Medical / IoMT device symbol: rounded box with a red cross overlay.
    Represents MRI machines, ICU monitors, infusion pumps, etc.
    """
    color = COLORS["medical_device"]
    ax.add_patch(FancyBboxPatch(
        (x - 0.42, y - 0.32), 0.84, 0.64,
        boxstyle="round,pad=0.07",
        facecolor="#FCE4EC", edgecolor=color, linewidth=2, zorder=5,
    ))
    ax.plot([x, x], [y + 0.20, y - 0.20], color=color, linewidth=3, zorder=6)
    ax.plot([x - 0.18, x + 0.18], [y, y],  color=color, linewidth=3, zorder=6)
    _vuln_badge(ax, x, y, vuln)
    ax.text(x, y - 0.46, label,
            ha="center", va="top", fontsize=6.0,
            color=color, fontweight="bold", zorder=7)


def draw_workstation(ax, x, y, label, vuln=None):
    """
    Workstation / desktop symbol: monitor screen + stand.
    """
    color = COLORS["workstation"]
    ax.add_patch(FancyBboxPatch(
        (x - 0.36, y - 0.08), 0.72, 0.42,
        boxstyle="round,pad=0.05",
        facecolor="#B0BEC5", edgecolor=color, linewidth=1.5, zorder=5,
    ))
    ax.plot([x, x],              [y - 0.08, y - 0.22], color=color, linewidth=2.5, zorder=6)
    ax.plot([x - 0.16, x + 0.16], [y - 0.22, y - 0.22], color=color, linewidth=2.5, zorder=6)
    _vuln_badge(ax, x, y, vuln)
    ax.text(x, y - 0.36, label,
            ha="center", va="top", fontsize=6.0,
            color=color, fontweight="bold", zorder=7)


# ── Zone and link helpers ──────────────────────────────────────────────────────

def draw_zone(ax, x, y, w, h, label, fill, border, label_size=8):
    """
    Draws a labelled background zone rectangle.

    Parameters
    ----------
    fill   : background fill colour (semi-transparent)
    border : border / label colour
    """
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.15",
        facecolor=fill, edgecolor=border,
        linewidth=2, alpha=0.45, zorder=0,
    ))
    ax.text(x + 0.20, y + h - 0.14, label,
            ha="left", va="top",
            fontsize=label_size, color=border,
            fontweight="bold", alpha=0.95)


def draw_link(ax, x1, y1, x2, y2, color, width=1.8, style="-", alpha=0.65, label=""):
    """
    Draws a styled line between two points.
    An optional midpoint label is placed in a white box for readability.
    """
    ax.plot([x1, x2], [y1, y2],
            color=color, linewidth=width,
            linestyle=style, zorder=2, alpha=alpha,
            solid_capstyle="round")
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.08, my, label,
                ha="left", va="center", fontsize=5.8, color="#455A64", zorder=8,
                bbox=dict(boxstyle="round,pad=0.12", facecolor="white",
                          edgecolor="#B0BEC5", alpha=0.92))


def draw_legend(ax, items, x_start=0.5, y=0.18, spacing=3.5):
    """
    Draws a horizontal legend row.

    Parameters
    ----------
    items    : list of (color, linestyle, label) tuples
    x_start  : left anchor in data coordinates
    y        : vertical position
    spacing  : horizontal spacing between items
    """
    from matplotlib.patches import FancyBboxPatch as FBP
    for i, (color, linestyle, label) in enumerate(items):
        ox = x_start + i * spacing
        ax.plot([ox, ox + 0.48], [y, y],
                color=color, linewidth=2.2, linestyle=linestyle, zorder=9)
        ax.text(ox + 0.62, y, label,
                va="center", fontsize=7.0, color="#37474F", zorder=9)
