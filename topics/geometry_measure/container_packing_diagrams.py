"""Exam-style diagrams for N5 Container Packing: the item and the container drawn side by side,
the way the SQA papers show them (each drawn to its own scale, with its own dimension labels).

    panels(specs, path)    specs = list of dicts, one per panel, drawn left to right:
        {"kind": "cuboid", "dims": [l, w, h], "labels": [l, w, h], "caption": str, "up": bool}
        {"kind": "cylinder", "dims": [d, h], "labels": [d, h], "caption": str}
        {"kind": "rect", "dims": [l, w], "labels": [l, w], "caption": str}
    l runs left to right along the front, w is the depth (drawn back at 35°), h is the height.
    "up": True adds a "this way up" arrow on the front face.

The app keeps a copy (N5apps topics/geometry_measure/container_packing_diagrams.py) built on
core/ui/composite_solids.py instead of solids.py; keep the two in step.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

try:
    from solids import _draw_prism, _draw_cylinder, _labels, _shift, E, FILL
    from shapes import _dim
except ImportError:                                   # inside the app
    from core.ui.composite_solids import _draw_prism, _draw_cylinder, _labels, _shift, E, FILL  # noqa: F401
    from core.ui.composite_shapes import _dim  # noqa: F401

PW, PH = 1.6, 1.15          # each panel's drawing box, inches


def _extent(s):
    k, d = s["kind"], s["dims"]
    if k == "cuboid":
        dx, dy = _shift(d[1])
        return d[0] + dx, d[2] + dy
    if k == "cylinder":
        return d[0], d[1] + 2 * E * d[0] / 2
    return d[0], d[1]


def _cuboid(ax, s):
    l, w, h = s["dims"]
    dx, dy = _shift(w)
    F, _ = _draw_prism(ax, [(0, 0), (l, 0), (l, h), (0, h)], w)
    size = max(l + dx, h + dy)
    _labels(ax, F, (dx, dy), [(0, 1, s["labels"][0], -1), (3, 0, s["labels"][2], -1),
                              ("depth", s["labels"][1])], size)
    if s.get("up"):
        a = min(0.6 * h, 0.35 * l)
        ax.annotate("", xy=(0.5 * l, h / 2 + a / 2), xytext=(0.5 * l, h / 2 - a / 2),
                    arrowprops=dict(arrowstyle="-|>", lw=1.6, color="#B00020"), zorder=9)
    return -0.2 * size


def _cylinder(ax, s):
    d, h = s["dims"]
    r = d / 2
    _draw_cylinder(ax, 0, 0, r, h)
    size = max(d, h)
    _dim(ax, (-r, h), (r, h), s["labels"][0], 0.001)
    _dim(ax, (r, 0), (r, h), s["labels"][1], -0.16 * size)
    return -E * r - 0.12 * size


def _rect(ax, s):
    l, w = s["dims"]
    ax.fill([0, l, l, 0], [0, 0, w, w], color=FILL, zorder=1)
    ax.plot([0, l, l, 0, 0], [0, 0, w, w, 0], color="black", lw=1.4, zorder=3)
    size = max(l, w)
    _dim(ax, (0, 0), (l, 0), s["labels"][0], -0.12 * size)
    _dim(ax, (0, w), (0, 0), s["labels"][1], -0.12 * size)
    return -0.21 * size


def panels(specs, path):
    scales = []
    for s in specs:
        w, h = _extent(s)
        scales.append(min(PW / w, PH / h))
    widths = [_extent(s)[0] * k + 0.9 for s, k in zip(specs, scales)]
    fig, axes = plt.subplots(1, len(specs), figsize=(sum(widths), PH + 1.0), dpi=200,
                             gridspec_kw={"width_ratios": widths})
    if len(specs) == 1:
        axes = [axes]
    for ax, s in zip(axes, specs):
        ax.set_aspect("equal"); ax.axis("off")
        y = {"cuboid": _cuboid, "cylinder": _cylinder, "rect": _rect}[s["kind"]](ax, s)
        if s.get("caption"):
            cap = s["caption"] + ("  (this way up ↑)" if s.get("up") else "")
            ax.text(_extent(s)[0] / 2, y, cap, ha="center", va="top", fontsize=9.5, style="italic",
                    color="black", zorder=5)
        ax.margins(0.08)
    fig.tight_layout(pad=0.3, w_pad=1.2)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    return path
