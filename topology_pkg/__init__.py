"""
topology_pkg
============
Network topology diagram generator for the network-engineering-portfolio.

Provides a single high-level entry point ``draw_topology`` that dispatches
to the appropriate layout module, plus direct access to each module's
``build`` function for finer control.

Usage
-----
Generate one diagram::

    from topology_pkg import draw_topology
    draw_topology("bgp", output_path="bgp_topology.png")

Generate all diagrams::

    from topology_pkg import draw_all
    draw_all(output_dir="images/")

Import a specific layout directly::

    from topology_pkg.dc import build as build_dc
    build_dc("my_dc.png")

Available topology names
------------------------
- ``"bgp"``       BGP Multi-AS Enterprise Network
- ``"dc"``        Data Centre EVPN/VXLAN Leaf-Spine
- ``"firewall"``  Firewall & Network Security Architecture
- ``"cloud"``     Cloud AI/ML GPU Fabric (Multi-Pod Spine-Leaf)
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("topology_pkg")
except PackageNotFoundError:
    __version__ = "0.1.0"

from . import bgp, dc, firewall, cloud
from .symbols import (
    draw_router,
    draw_border_router,
    draw_switch,
    draw_firewall,
    draw_cloud,
    draw_server,
    draw_gpu_node,
    draw_storage,
    draw_medical_device,
    draw_workstation,
    draw_zone,
    draw_link,
    draw_legend,
)
from .styles import COLORS, LINKS, ZONES, LEGENDS, BG_COLOR

# ── Dispatch table ─────────────────────────────────────────────────────────────
_TOPOLOGIES: dict = {
    "bgp":      bgp.build,
    "dc":       dc.build,
    "firewall": firewall.build,
    "cloud":    cloud.build,
}


def draw_topology(name: str, output_path: str | None = None) -> str:
    """
    Generate a single topology diagram.

    Parameters
    ----------
    name        : topology identifier — one of "bgp", "dc", "firewall",
                  "cloud", "va"
    output_path : destination file path; defaults to ``<name>_topology.png``
                  in the current working directory

    Returns
    -------
    str
        Resolved path to the saved PNG file.

    Raises
    ------
    ValueError
        If *name* is not a recognised topology identifier.

    Examples
    --------
    >>> from topology_pkg import draw_topology
    >>> draw_topology("bgp", "images/bgp_topology.png")
    'images/bgp_topology.png'
    """
    if name not in _TOPOLOGIES:
        valid = ", ".join(f'"{k}"' for k in _TOPOLOGIES)
        raise ValueError(
            f'Unknown topology "{name}". Valid options are: {valid}'
        )
    if output_path is None:
        output_path = f"{name}_topology.png"
    return _TOPOLOGIES[name](output_path=output_path)


def draw_all(output_dir: str = ".") -> dict[str, str]:
    """
    Generate all topology diagrams.

    Parameters
    ----------
    output_dir : directory where PNG files will be written

    Returns
    -------
    dict
        Mapping of topology name → saved file path.

    Examples
    --------
    >>> from topology_pkg import draw_all
    >>> paths = draw_all("images/")
    >>> for name, path in paths.items():
    ...     print(f"{name}: {path}")
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    results = {}
    for name in _TOPOLOGIES:
        out = os.path.join(output_dir, f"{name}_topology.png")
        print(f"  Generating {name}...", end=" ", flush=True)
        results[name] = draw_topology(name, out)
        print("done")
    return results


__all__ = [
    # High-level API
    "draw_topology",
    "draw_all",
    # Sub-modules
    "bgp", "dc", "firewall", "cloud",
    # Symbol functions (re-exported for convenience)
    "draw_router", "draw_border_router", "draw_switch", "draw_firewall",
    "draw_cloud", "draw_server", "draw_gpu_node", "draw_storage",
    "draw_medical_device", "draw_workstation",
    "draw_zone", "draw_link", "draw_legend",
    # Style constants
    "COLORS", "LINKS", "ZONES", "LEGENDS", "BG_COLOR",
]
