# topology_pkg

A reusable Python package for generating professional network topology diagrams. Powers all topology diagrams across the `network-engineering-portfolio` — one consistent set of Cisco-style symbols, colours, and styles across every lab.

---

## Package Structure

```
topology_pkg/
├── __init__.py     # Public API — draw_topology() and draw_all()
├── __main__.py     # Enables python -m topology_pkg
├── styles.py       # Centralised colour palette, zone styles, legend configs
├── symbols.py      # Reusable drawing functions (router, switch, firewall, GPU...)
├── bgp.py          # BGP Multi-AS Enterprise Network layout
├── dc.py           # Data Centre EVPN/VXLAN Leaf-Spine layout
├── firewall.py     # Firewall & Network Security Architecture layout
├── cloud.py        # Cloud AI/ML GPU Fabric (Multi-Pod Spine-Leaf) layout
└── cli.py          # CLI entry point
```

**`styles.py`** is the single source of truth for every colour, zone fill, link colour, and legend definition. Change a colour here and it propagates to all four diagrams automatically.

**`symbols.py`** contains all drawing functions. Each function takes a matplotlib `Axes` object and draws directly onto it using data coordinates — fully reusable across any layout.

---

## Installation

```bash
pip install matplotlib
```

No other dependencies required.

---

## Usage

### Command line

```bash
# Generate one diagram (saved to current directory)
python -m topology_pkg bgp
python -m topology_pkg dc
python -m topology_pkg firewall
python -m topology_pkg cloud

# Specify output path
python -m topology_pkg bgp --output images/bgp_topology.png

# Generate all four diagrams at once
python -m topology_pkg all --output-dir images/
```

### Python API

```python
from topology_pkg import draw_topology, draw_all

# Generate a single diagram
draw_topology("bgp", output_path="images/bgp_topology.png")

# Generate all diagrams
paths = draw_all(output_dir="images/")
for name, path in paths.items():
    print(f"{name}: {path}")
```

### Import a specific layout directly

```python
from topology_pkg.dc import build as build_dc

build_dc("my_dc.png")
```

### Use individual drawing functions in a custom diagram

```python
import matplotlib.pyplot as plt
from topology_pkg.symbols import draw_router, draw_switch, draw_link
from topology_pkg.styles import BG_COLOR, LINKS

fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
fig.patch.set_facecolor(BG_COLOR)

draw_router(ax, 3.0, 4.0, "RTR-1", "10.0.0.1/32", color="#1565C0")
draw_switch(ax, 9.0, 4.0, "SW-1",  "Nexus 9300",   color="#2E7D32")
draw_link(ax, 3.5, 4.0, 8.3, 4.0, LINKS["ibgp"], width=2, label="iBGP")

plt.savefig("custom.png", dpi=150, bbox_inches="tight")
```

---

## Available Topologies

| Name | Diagram | Key Technologies |
|------|---------|-----------------|
| `bgp` | BGP Multi-AS Enterprise Network | eBGP, iBGP, Route Reflector, IPSec VPN |
| `dc` | Data Centre EVPN/VXLAN Leaf-Spine | BGP EVPN, VXLAN, vPC, Arista / Cisco / Juniper |
| `firewall` | Firewall & Security Architecture | Juniper SRX, Fortinet FortiGate, DMZ, IDS/IPS |
| `cloud` | Cloud AI/ML GPU Fabric | Super-spine, 400GbE, RoCEv2, NVIDIA A100/H100 |

---

## Available Symbols

| Function | Symbol | Represents |
|----------|--------|-----------|
| `draw_router()` | Circle with crossing arrows | Router (Cisco-style) |
| `draw_border_router()` | Double-ring circle with arrows | Border / edge router |
| `draw_switch()` | Rectangle with port stubs | Switch (L2/L3) |
| `draw_firewall()` | Shield with padlock | Firewall / security device |
| `draw_cloud()` | Overlapping circles | Internet, WAN, cloud provider |
| `draw_server()` | Stacked rack bars with LED | Generic server |
| `draw_gpu_node()` | Dark chassis with GPU chip grid | GPU server (DGX A100/H100) |
| `draw_storage()` | Rounded box with platter lines | NAS / SAN / Ceph storage |
| `draw_medical_device()` | Box with medical cross | IoMT device (MRI, ICU monitor) |
| `draw_workstation()` | Monitor + stand | Desktop / clinical workstation |
| `draw_zone()` | Labelled background rectangle | Network security zone |
| `draw_link()` | Styled line with optional label | Network link |
| `draw_legend()` | Horizontal legend row | Diagram legend |

---

## Extending the Package

### Add a new topology

1. Create `topology_pkg/my_topology.py` with a `build(output_path)` function:

```python
# my_topology.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from .symbols import draw_router, draw_switch, draw_link, draw_zone, draw_legend
from .styles import BG_COLOR, LINKS, ZONES, LEGENDS

def build(output_path: str = "my_topology.png") -> str:
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16); ax.set_ylim(0, 10); ax.axis("off")
    fig.patch.set_facecolor(BG_COLOR)

    # draw your topology here...

    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    return output_path
```

2. Register it in `__init__.py`:

```python
from . import my_topology
_TOPOLOGIES["my_topology"] = my_topology.build
```

3. Optionally add a legend config in `styles.py` under `LEGENDS["my_topology"]`.

### Add a new symbol

Add a new function to `symbols.py` following the same signature pattern:

```python
def draw_my_device(ax, x, y, label, sublabel="", color=None, size=0.44):
    color = color or COLORS["server_generic"]
    # draw using matplotlib primitives...
    ax.text(x, y - size - 0.2, label, ha="center", ...)
```

---

## Design Decisions

**Why matplotlib and not a graph library?** Full pixel-level control over symbol shapes, colours, and layout. Tools like NetworkX or Graphviz produce adequate node-link graphs but cannot render Cisco-style symbols or zone backgrounds with this level of precision.

**Why separate `styles.py`?** Consistency across diagrams matters for a portfolio. A single colour change in `styles.py` (e.g. switching the spine switch colour) updates every diagram that uses it, rather than hunting through five separate files.

**Why `draw_all()` in `__init__.py`?** Lets anyone regenerate the entire portfolio's worth of diagrams with one command, useful if styles are updated or new topologies are added.
