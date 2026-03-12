"""
cli.py
------
Command-line interface for topology_pkg.

Usage
-----
Generate a single topology::

    python -m topology_pkg bgp
    python -m topology_pkg dc --output images/dc_topology.png

Generate all topologies::

    python -m topology_pkg all --output-dir images/
"""

import argparse
import sys
from . import draw_topology, draw_all, _TOPOLOGIES


def main():
    parser = argparse.ArgumentParser(
        prog="python -m topology_pkg",
        description="Network topology diagram generator",
    )
    parser.add_argument(
        "topology",
        choices=[*_TOPOLOGIES.keys(), "all"],
        help='Topology to generate, or "all" to generate every diagram',
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        metavar="PATH",
        help="Output file path (ignored when topology=all)",
    )
    parser.add_argument(
        "--output-dir", "-d",
        default=".",
        metavar="DIR",
        help='Output directory when topology=all (default: current directory)',
    )

    args = parser.parse_args()

    if args.topology == "all":
        print(f"Generating all topologies → {args.output_dir}/")
        paths = draw_all(args.output_dir)
        for name, path in paths.items():
            print(f"  ✓  {name:12s}  →  {path}")
    else:
        out = args.output or f"{args.topology}_topology.png"
        print(f"Generating {args.topology} topology → {out}")
        draw_topology(args.topology, out)
        print(f"  ✓  Saved to {out}")


if __name__ == "__main__":
    main()
