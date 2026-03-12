"""
styles.py
---------
Centralised colour palette and style constants shared across all topology
diagrams. Change a colour here and it propagates everywhere.
"""

# ── Background ────────────────────────────────────────────────────────────────
BG_COLOR = "#F0F4F8"

# ── Device colours ────────────────────────────────────────────────────────────
COLORS = {
    # Network devices
    "router":        "#1565C0",
    "switch_core":   "#1565C0",
    "switch_spine":  "#1B5E20",
    "switch_leaf":   "#2E7D32",
    "switch_access": "#388E3C",
    "switch_dmz":    "#E65100",
    "switch_corp":   "#1B5E20",
    "firewall":      "#D84315",
    "border_router": "#4527A0",
    "ids":           "#1565C0",
    "super_spine":   "#0D47A1",

    # Server / endpoint types
    "server_generic": "#37474F",
    "server_dc":      "#1565C0",
    "server_dmz":     "#546E7A",
    "server_mgmt":    "#4527A0",
    "gpu_training":   "#2E7D32",
    "gpu_inference":  "#4A148C",
    "storage":        "#4527A0",
    "medical_device": "#880E4F",
    "workstation":    "#37474F",

    # Cloud / WAN
    "cloud_internet": "#B71C1C",
    "cloud_generic":  "#546E7A",
    "cloud_peering":  "#37474F",
    "cloud_vpn":      "#4527A0",
}

# ── Link colours ──────────────────────────────────────────────────────────────
LINKS = {
    "untrust":     "#EF5350",
    "dmz":         "#FFA726",
    "trust":       "#66BB6A",
    "mgmt":        "#5C6BC0",
    "vpn":         "#AB47BC",
    "ha_sync":     "#FF6F00",
    "siem":        "#7B1FA2",
    "ebgp":        "#EF5350",
    "ibgp":        "#1976D2",
    "ibgp_rr":     "#2E7D32",
    "ospf":        "#1976D2",
    "spine_up":    "#42A5F5",
    "leaf_access": "#66BB6A",
    "vpc_peer":    "#E65100",
    "nvlink":      "#FF6F00",
    "super_spine": "#42A5F5",
    "ecmp":        "#E65100",
    "clinical":    "#F48FB1",
    "corporate":   "#A5D6A7",
    "dc_link":     "#90CAF9",
    "transit":     "#EF5350",
}

# ── Zone fills and borders ────────────────────────────────────────────────────
ZONES = {
    "internet":   {"fill": "#FFEBEE", "border": "#B71C1C"},
    "perimeter":  {"fill": "#FFF3E0", "border": "#E65100"},
    "dmz":        {"fill": "#FFFDE7", "border": "#F9A825"},
    "trust":      {"fill": "#E8F5E9", "border": "#2E7D32"},
    "spine":      {"fill": "#E8F5E9", "border": "#1B5E20"},
    "leaf":       {"fill": "#E8F5E9", "border": "#2E7D32"},
    "super_spine":{"fill": "#E3F2FD", "border": "#0D47A1"},
    "dc":         {"fill": "#E3F2FD", "border": "#1565C0"},
    "clinical":   {"fill": "#FCE4EC", "border": "#880E4F"},
    "corporate":  {"fill": "#E8F5E9", "border": "#1B5E20"},
    "pod_a":      {"fill": "#FFF3E0", "border": "#E65100"},
    "pod_b":      {"fill": "#F3E5F5", "border": "#4A148C"},
    "pod_c":      {"fill": "#FFEBEE", "border": "#B71C1C"},
    "storage":    {"fill": "#E8EAF6", "border": "#283593"},
    "gpu_train":  {"fill": "#FFF8E1", "border": "#E65100"},
    "gpu_infer":  {"fill": "#F3E5F5", "border": "#4A148C"},
    "wan":        {"fill": "#F3E5F5", "border": "#6A1B9A"},
    "findings":   {"fill": "#FAFAFA", "border": "#37474F"},
}

# ── Vulnerability severity ────────────────────────────────────────────────────
VULN_SEVERITY = {
    "critical": {"color": "#B71C1C", "label": "CRIT", "led": "#FF5252"},
    "high":     {"color": "#E65100", "label": "HIGH", "led": "#FFD740"},
    "medium":   {"color": "#F9A825", "label": "MED",  "led": "#FFD740"},
    "low":      {"color": "#388E3C", "label": "LOW",  "led": "#69F0AE"},
    None:       {"color": None,      "label": None,   "led": "#69F0AE"},
}

# ── Legend items per diagram ──────────────────────────────────────────────────
LEGENDS = {
    "bgp": [
        (LINKS["ebgp"],    "-",  "eBGP (external)"),
        (LINKS["ibgp"],    "-",  "iBGP (internal)"),
        (LINKS["ibgp_rr"], "--", "iBGP Route Reflector"),
        (LINKS["vpn"],     "-",  "IPSec VPN / BGP over tunnel"),
        (LINKS["transit"], "--", "ISP transit"),
    ],
    "dc": [
        (LINKS["ospf"],      "-",  "Spine uplinks (OSPF underlay)"),
        (LINKS["spine_up"],  "-",  "Leaf-to-spine (100GbE)"),
        (LINKS["vpc_peer"],  "--", "vPC peer-link (MLAG)"),
        (LINKS["leaf_access"], "-", "Server access — Pod A"),
        (LINKS["vpn"],       "-",  "Server access — Pod B"),
        (LINKS["untrust"],   "-",  "Server access — Pod C"),
    ],
    "firewall": [
        (LINKS["untrust"],  "-",  "Untrust / Internet"),
        (LINKS["dmz"],      "-",  "DMZ traffic"),
        (LINKS["trust"],    "-",  "Trust / Internal"),
        (LINKS["vpn"],      "-",  "IPSec VPN"),
        (LINKS["mgmt"],     "-",  "IDS/IPS inline"),
        (LINKS["ha_sync"],  "--", "HA Sync"),
        (LINKS["siem"],     "--", "SIEM logging"),
    ],
    "cloud": [
        (LINKS["super_spine"], "-",  "Super-spine uplinks"),
        (LINKS["leaf_access"], "-",  "Pod 1 fabric (400GbE)"),
        (LINKS["vpn"],         "-",  "Pod 2 fabric (400GbE)"),
        (LINKS["dc_link"],     "-",  "Pod 3 fabric (100GbE)"),
        (LINKS["nvlink"],      "-",  "NVLink / RoCEv2 GPU rail"),
        (LINKS["ecmp"],        "--", "Intra-spine ECMP"),
    ],
}
