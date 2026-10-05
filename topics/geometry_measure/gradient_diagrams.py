"""Exam-style gradient diagrams for N5 Applications of Maths (worksheet and N5apps).

The same file lives in two places and must be kept identical:
  Resources/Apps/.pipeline-tools/n5_new_topics/gradient_diagrams.py   (worksheet / homework)
  N5apps/topics/geometry_measure/gradient_diagrams.py                 (app, via metadata
      {"diagram": "composite_shape", "diagram_params": {"module_path": ..., "kind": ..., "args": [...]}})

Each function draws from its real dimensions (to scale) and saves a PNG to `path` (a file path or
a BytesIO). Lengths passed in must be in ONE unit; the labels carry the units shown to pupils.

    ramp(v, h, labels, path)           right-angled slope rising left to right. labels = [vertical,
                                       horizontal, sloping]; "" or None leaves a side unlabelled,
                                       "?" marks the side to find
    hill(bottom, top, horiz, labels, path)
                                       straight path from a point `bottom` m above sea level to one
                                       `top` m above sea level; labels = [bottom, top, horizontal] (short, e.g. "21 m"),
                                       written beside the dashed height lines
    graph(x1, y1, x2, y2, path)        coordinate grid with the line through A(x1, y1) and B(x2, y2)
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

FILL = "#dbe9f6"


def _save(fig, ax, path, pad=0.06):
    ax.margins(pad)
    fig.tight_layout(pad=0.2)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.06, format="png")
    plt.close(fig)
    return path


def _arrow(ax, a, b):
    ax.annotate("", xy=b, xytext=a, annotation_clip=False,
                arrowprops=dict(arrowstyle="<->", lw=0.9, shrinkA=0, shrinkB=0), zorder=4)
    ax.plot([a[0], b[0]], [a[1], b[1]], alpha=0)


def _text(ax, x, y, s, **kw):
    kw.setdefault("ha", "center"); kw.setdefault("va", "center")
    ax.text(x, y, s, fontsize=9.5, zorder=5, **kw)


def ramp(v, h, labels, path):
    """Right-angled triangle: horizontal h along the bottom, vertical v up the right-hand side."""
    v, h = float(v), float(h)
    labels = list(labels) + [None] * (3 - len(labels))
    lv, lh, ls = labels[:3]
    s = min(3.4 / h, 1.7 / v) if v > 0 else 3.4 / h   # drawn at print size: ≤ 3.4 in wide, ≤ 1.7 in tall
    W = h * s
    hin = max(v * s, 0.05)
    fig, ax = plt.subplots(figsize=(W + 1.4, hin + 0.9), dpi=200)
    ax.set_aspect("equal"); ax.axis("off")
    pts = [(0, 0), (h, 0), (h, v)]
    xs, ys = zip(*(pts + [pts[0]]))
    ax.fill(xs, ys, color=FILL, zorder=1)
    ax.plot(xs, ys, color="black", lw=1.6, zorder=3)
    u = h / W * 0.11                          # 0.11 inch in data units
    q = min(u * 1.1, v * 0.45) if v > 0 else u   # right-angle mark
    ax.plot([h - q, h - q, h], [0, q, q], color="black", lw=0.8, zorder=3)
    if lh:
        _arrow(ax, (0, -2.0 * u), (h, -2.0 * u))
        _text(ax, h / 2, -2.0 * u, lh, bbox=dict(fc="white", ec="none", pad=0.8))
    if lv:
        _arrow(ax, (h + 1.6 * u, 0), (h + 1.6 * u, v))
        _text(ax, h + 2.4 * u, v / 2, lv, ha="left")
    if ls:
        L = math.hypot(h, v)
        nx, ny = -v / L, h / L                # left-hand normal of the slope (points up-left)
        _text(ax, h / 2 + nx * 2.2 * u, v / 2 + ny * 2.2 * u, ls, ha="center")
    ax.plot([-0.3 * u, h + 9 * u], [-3.2 * u, v + 2.6 * u], alpha=0)   # room for the labels
    return _save(fig, ax, path, 0.02)


def hill(bottom, top, horiz, labels, path):
    """Path from `bottom` (left) up to `top` (right), heights above a dashed sea-level line, to scale."""
    b, t, H = float(bottom), float(top), float(horiz)
    W = 3.4
    s = W / H
    fig, ax = plt.subplots(figsize=(W + 1.6, t * s + 1.0), dpi=200)
    ax.set_aspect("equal"); ax.axis("off")
    u = H / W * 0.11
    ax.fill([0, H, H, 0], [0, 0, t, b], color=FILL, zorder=1)
    ax.plot([0, H], [b, t], color="black", lw=1.8, zorder=3)
    ax.plot([-1.5 * u, H + 1.5 * u], [0, 0], color="#1f4e8c", lw=1.0, ls=(0, (5, 3)), zorder=2)
    ax.text(H + 1.8 * u, 0, "sea level", ha="left", va="center", fontsize=8, color="#1f4e8c")
    ax.plot([0, 0], [0, b], color="black", lw=0.8, ls=(0, (3, 2)))
    ax.plot([H, H], [0, t], color="black", lw=0.8, ls=(0, (3, 2)))
    ax.plot([0, H], [b, t], "o", color="black", ms=3.5, zorder=4)
    lb, lt, lh = (list(labels) + [None] * 3)[:3]
    if lb:
        _text(ax, -0.8 * u, max(b / 2, 0.9 * u), lb, ha="right")
    if lt:
        _text(ax, H + 0.8 * u, max(t / 2, 2.2 * u), lt, ha="left")
    if lh:
        _arrow(ax, (0, -2.0 * u), (H, -2.0 * u))
        _text(ax, H / 2, -2.0 * u, lh, bbox=dict(fc="white", ec="none", pad=0.8))
    ax.plot([-6 * u, H + 10 * u], [-3.2 * u, t + 1.5 * u], alpha=0)
    return _save(fig, ax, path, 0.02)


def graph(x1, y1, x2, y2, path):
    """Coordinate grid from 0 with the straight line through A and B."""
    X = max(x1, x2) + 2; Y = max(y1, y2) + 2
    fig, ax = plt.subplots(figsize=(0.28 * X + 0.6, 0.28 * Y + 0.5), dpi=200)
    ax.set_aspect("equal")
    for i in range(X + 1):
        ax.plot([i, i], [0, Y], color="#cfcfcf", lw=0.6, zorder=0)
    for j in range(Y + 1):
        ax.plot([0, X], [j, j], color="#cfcfcf", lw=0.6, zorder=0)
    ax.set_xlim(0, X); ax.set_ylim(0, Y)
    ax.set_xticks(range(0, X + 1, 2)); ax.set_yticks(range(0, Y + 1, 2))
    ax.tick_params(labelsize=7, length=2)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_xlabel("x", fontsize=8, labelpad=1); ax.set_ylabel("y", fontsize=8, labelpad=1, rotation=0)
    # line across the grid
    m = (y2 - y1) / (x2 - x1)
    xa, xb = 0, X
    ya, yb = y1 + m * (xa - x1), y1 + m * (xb - x1)
    if ya < 0:
        xa, ya = x1 - y1 / m, 0
    if yb > Y:
        xb, yb = x1 + (Y - y1) / m, Y
    ax.plot([xa, xb], [ya, yb], color="black", lw=1.4, zorder=2)
    for (x, y, n) in ((x1, y1, "A"), (x2, y2, "B")):
        ax.plot([x], [y], "o", color="black", ms=3.5, zorder=3)
        ax.text(x - 0.35, y + 0.35, n, fontsize=9, ha="right", va="bottom", zorder=4,
                bbox=dict(fc="white", ec="none", pad=0.3))
    fig.tight_layout(pad=0.2)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.06, format="png")
    plt.close(fig)
    return path
