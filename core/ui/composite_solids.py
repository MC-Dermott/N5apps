"""Exam-style 3D diagrams (oblique projection) — copied from the worksheet pipeline's
.pipeline-tools/n5_new_topics/solids.py so the app draws the same pictures as the Volume worksheet.
Rendered by question_ui for metadata["diagram"] == "composite_shape" with "module": "solids". Same conventions as
shapes.py: each function takes dimensions, a list of label strings and a path (or BytesIO).

    prism(poly, depth, labels, path)        any convex cross-section drawn on the front, extruded back
                                            labels = [(i, j, text, off) ...] dimension arrows between
                                            front vertices i and j, plus ("depth", text) for the depth
    cuboid(l, w, h, labels)                 labels = [l, w, h]
    tri_prism(b, h, L, labels)              isosceles triangle cross-section; labels = [b, h, L]
    cylinder(d, h, labels)                  labels = [d, h]
    sphere(d, label) / hemisphere(d, label) / cone(d, h, labels)
    cuboid_cylinder(l, w, h, d, hc, labels) cylinder standing on a cuboid (bottle); labels = [l, w, h, d, hc]
    cube_hemisphere(s, labels)              hemisphere (diameter s) on a cube; labels = [s]
    house_prism(b, h, t, L, labels)         cuboid with a triangular prism roof; labels = [b, h, t, L]
    cylinder_hemisphere(d, h, labels)       silo: cylinder with a hemisphere on top; labels = [d, h]

Hidden edges are dashed. Drawings are to scale.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from core.ui.composite_shapes import _dim, _label, _save  # noqa: E402

FILL, SIDE, TOP = "#dbe9f6", "#c4d9ee", "#e9f2fb"
K, ANG = 0.5, math.radians(35)          # depth drawn at half size, 35° up to the right
E = 0.32                                # ellipse squash for circles seen from above


def _shift(depth):
    return depth * K * math.cos(ANG), depth * K * math.sin(ANG)


def _fig(w, h):
    s = min(3.3 / w, 1.9 / h)
    fig, ax = plt.subplots(figsize=(w * s + 0.9, h * s + 0.7), dpi=200)
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def _poly(ax, pts, fill, z):
    xs, ys = zip(*pts)
    ax.fill(xs, ys, color=fill, zorder=z, lw=0)


def _line(ax, p, q, hidden=False, z=6):
    ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=0.8 if hidden else 1.4,
            ls=(0, (3, 3)) if hidden else "-", zorder=z)


def _draw_prism(ax, poly, depth, x0=0, y0=0, z=1):
    """Draw a prism (front face = poly, convex, anticlockwise) and return its front vertices."""
    dx, dy = _shift(depth)
    F = [(x + x0, y + y0) for x, y in poly]
    B = [(x + dx, y + dy) for x, y in F]
    n = len(F)
    vis = []
    for i in range(n):
        (ax_, ay), (bx, by) = F[i], F[(i + 1) % n]
        nx, ny = by - ay, -(bx - ax_)                 # outward normal of an anticlockwise polygon
        vis.append(nx * dx + ny * dy > 1e-9)
    for i in range(n):
        if vis[i]:
            _poly(ax, [F[i], F[(i + 1) % n], B[(i + 1) % n], B[i]], TOP if dy and F[i][1] == F[(i + 1) % n][1] else SIDE, z)
    _poly(ax, F, FILL, z + 0.5)
    for i in range(n):
        j = (i + 1) % n
        _line(ax, F[i], F[j], z=z + 2)
        _line(ax, B[i], B[j], hidden=not vis[i], z=z + 2)
        _line(ax, F[i], B[i], hidden=not (vis[i] or vis[i - 1]), z=z + 2)
    return F, (dx, dy)


def prism(poly, depth, labels, path):
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    dx, dy = _shift(depth)
    fig, ax = _fig(max(xs) - min(xs) + dx, max(ys) - min(ys) + dy)
    F, _ = _draw_prism(ax, poly, depth)
    _labels(ax, F, (dx, dy), labels, max(max(xs) - min(xs), max(ys) - min(ys)))
    return _save(fig, ax, path, 0.08)


def _labels(ax, F, shift, labels, size):
    o = 0.1 * size
    for lab in labels:
        if lab[0] == "depth":
            # along the bottom-right depth edge
            i = max(range(len(F)), key=lambda k: (F[k][0] - F[k][1] * 0.01))
            p = min((F[k] for k in range(len(F)) if abs(F[k][0] - F[i][0]) < 1e-9), key=lambda v: v[1])
            q = (p[0] + shift[0], p[1] + shift[1])
            _dim(ax, p, q, lab[1], -o * 1.2)
        else:
            i, j, text, off = lab
            _dim(ax, F[i], F[j], text, off * o)


def cuboid(l, w, h, labels, path):
    return prism([(0, 0), (l, 0), (l, h), (0, h)], w,
                 [(0, 1, labels[0], -1), (3, 0, labels[2], -1), ("depth", labels[1])], path)


def tri_prism(b, h, L, labels, path):
    poly = [(0, 0), (b, 0), (b / 2, h)]
    dx, dy = _shift(L)
    fig, ax = _fig(b + dx, h + dy)
    F, _ = _draw_prism(ax, poly, L)
    _labels(ax, F, (dx, dy), [(0, 1, labels[0], -1), ("depth", labels[2])], max(b, h))
    _line(ax, (b / 2, 0), (b / 2, h), hidden=True, z=8)
    _label(ax, b / 2 + 0.09 * max(b, h), h * 0.4, labels[1], size=9)
    return _save(fig, ax, path, 0.08)


def house_prism(b, h, t, L, labels, path):
    poly = [(0, 0), (b, 0), (b, h), (b / 2, h + t), (0, h)]
    dx, dy = _shift(L)
    fig, ax = _fig(b + dx, h + t + dy)
    F, _ = _draw_prism(ax, poly, L)
    _line(ax, (0, h), (b, h), hidden=True, z=8)
    _labels(ax, F, (dx, dy), [(0, 1, labels[0], -1), (4, 0, labels[1], -1), ("depth", labels[3])], max(b, h + t))
    _dim(ax, (b / 2, h), (b / 2, h + t), labels[2], 0.001)
    return _save(fig, ax, path, 0.08)


# ── round solids ──────────────────────────────────────────────────────────────────────────────
def _ell(cx, cy, r, a0, a1, n=90):
    t = np.radians(np.linspace(a0, a1, n))
    return list(zip(cx + r * np.cos(t), cy + E * r * np.sin(t)))


def _curve(ax, pts, hidden=False, z=6):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color="black", lw=0.8 if hidden else 1.4, ls=(0, (3, 3)) if hidden else "-", zorder=z)


def _draw_cylinder(ax, cx, y0, r, h, z=3, top=True):
    _poly(ax, _ell(cx, y0, r, 180, 360) + _ell(cx, y0 + h, r, 0, 180), SIDE, z)
    if top:
        _poly(ax, _ell(cx, y0 + h, r, 0, 360), TOP, z + 0.5)
        _curve(ax, _ell(cx, y0 + h, r, 0, 360), z=z + 2)
    _curve(ax, _ell(cx, y0, r, 180, 360), z=z + 2)
    _curve(ax, _ell(cx, y0, r, 0, 180), hidden=True, z=z + 2)
    _line(ax, (cx - r, y0), (cx - r, y0 + h), z=z + 2)
    _line(ax, (cx + r, y0), (cx + r, y0 + h), z=z + 2)


def _draw_dome(ax, cx, y0, r, z=3):
    t = np.radians(np.linspace(0, 180, 90))
    dome = list(zip(cx + r * np.cos(t), y0 + r * np.sin(t)))
    _poly(ax, dome + _ell(cx, y0, r, 180, 360), FILL, z)
    _curve(ax, dome, z=z + 2)
    _curve(ax, _ell(cx, y0, r, 180, 360), z=z + 2)
    _curve(ax, _ell(cx, y0, r, 0, 180), hidden=True, z=z + 2)


def cylinder(d, h, labels, path):
    r = d / 2
    fig, ax = _fig(d, h + 2 * E * r)
    _draw_cylinder(ax, 0, 0, r, h)
    _dim(ax, (-r, h), (r, h), labels[0], 0.001)
    _dim(ax, (r, 0), (r, h), labels[1], 0.14 * max(d, h) * -1)
    return _save(fig, ax, path, 0.1)


def sphere(d, label, path):
    r = d / 2
    fig, ax = _fig(d, d)
    t = np.radians(np.linspace(0, 360, 180))
    circ = list(zip(r * np.cos(t), r * np.sin(t)))
    _poly(ax, circ, FILL, 1); _curve(ax, circ)
    _curve(ax, _ell(0, 0, r, 180, 360)); _curve(ax, _ell(0, 0, r, 0, 180), hidden=True)
    _dim(ax, (-r, 0), (r, 0), label, 0.001)
    return _save(fig, ax, path, 0.1)


def hemisphere(d, label, path):
    r = d / 2
    fig, ax = _fig(d, r + E * r)
    _draw_dome(ax, 0, 0, r)
    _dim(ax, (-r, 0), (r, 0), label, -E * r - 0.12 * d)
    return _save(fig, ax, path, 0.1)


def cone(d, h, labels, path):
    r = d / 2
    fig, ax = _fig(d, h + E * r)
    _poly(ax, [(-r, 0), (0, h), (r, 0)] + _ell(0, 0, r, 360, 180), FILL, 1)
    _line(ax, (-r, 0), (0, h)); _line(ax, (r, 0), (0, h))
    _curve(ax, _ell(0, 0, r, 180, 360)); _curve(ax, _ell(0, 0, r, 0, 180), hidden=True)
    _line(ax, (0, 0), (0, h), hidden=True)
    _label(ax, 0.1 * max(d, h), h * 0.45, labels[1], size=9)
    _dim(ax, (-r, 0), (r, 0), labels[0], -E * r - 0.1 * d)
    return _save(fig, ax, path, 0.1)


def cuboid_cylinder(l, w, h, d, hc, labels, path):
    dx, dy = _shift(w)
    r = d / 2
    fig, ax = _fig(l + dx, h + dy + hc + E * r)
    F, _ = _draw_prism(ax, [(0, 0), (l, 0), (l, h), (0, h)], w)
    cx, cy = l / 2 + dx / 2, h + dy / 2
    _draw_cylinder(ax, cx, cy, r, hc, z=12)
    size = max(l + dx, h + hc)
    _labels(ax, F, (dx, dy), [(0, 1, labels[0], -1), (3, 0, labels[2], -1), ("depth", labels[1])], size)
    _dim(ax, (cx - r, cy + hc), (cx + r, cy + hc), labels[3], 0.001)
    _dim(ax, (cx + r, cy), (cx + r, cy + hc), labels[4], -0.1 * size)
    return _save(fig, ax, path, 0.08)


def cube_hemisphere(s, labels, path):
    dx, dy = _shift(s)
    r = s / 2
    fig, ax = _fig(s + dx, s + dy + r)
    F, _ = _draw_prism(ax, [(0, 0), (s, 0), (s, s), (0, s)], s)
    _draw_dome(ax, s / 2 + dx / 2, s + dy / 2, r * 0.98, z=12)
    _labels(ax, F, (dx, dy), [(0, 1, labels[0], -1), (3, 0, labels[0], -1), ("depth", labels[0])], s + dx)
    return _save(fig, ax, path, 0.08)


def cylinder_hemisphere(d, h, labels, path):
    r = d / 2
    fig, ax = _fig(d, h + r + E * r)
    _draw_cylinder(ax, 0, 0, r, h, top=False)
    _draw_dome(ax, 0, h, r, z=8)
    _dim(ax, (-r, -E * r - 0.12 * d), (r, -E * r - 0.12 * d), labels[0], 0.001)
    _dim(ax, (r, 0), (r, h), labels[1], -0.14 * max(d, h))
    return _save(fig, ax, path, 0.1)
