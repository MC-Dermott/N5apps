"""Exam-style right-angled triangle diagrams for N5 Pythagoras (worksheet, homework and the N5apps app).

The same file is copied to N5apps/topics/geometry_measure/pythagoras_diagrams.py, so it only uses
matplotlib/numpy. Every function draws to scale from its lengths and saves a PNG to `path` (a file
name or a BytesIO). Side labels sit outside the shape, beside the middle of each side; a label of
"" is left off. Right angles are marked with a small square.

    right_tri(a, b, labels, path, flip=False)   legs a (up) and b (across); labels [a, b, hyp]
    ramp(a, b, labels, path)                    right_tri with flip=True (for the app: positional args only)
    ladder(h, d, labels, path)                  wall, ground and a ladder; labels [ladder, height, foot]
    rect_diag(L, W, labels, path)               rectangle with a diagonal; labels [L, W, diagonal]
    isosceles(base, side, labels, path)         dashed height, right angle; labels [base, side, height]
    gable(w, hr, side, labels, path)            rectangle w × hr with an isosceles roof; labels [w, hr, side]
    badge(a, b, labels, path)                   right-angled triangle with a semi-circle on the hypotenuse
    two_tri_ext(h, x1, x2, labels, path)        2024 P2 Q6 shape: labels [h, TA, AB, TB, names T H A B, HA]
    patio_lawn(ad, dc, ab, labels, path)        2023 P2 Q3 shape: triangle ADC with triangle ACB on AC
    split_tri(bl, br, h, labels, path)          triangle split by its height; labels [left slope, right slope,
                                                left base, right base, height]
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

FILL = "#dbe9f6"


def _fig(w, h):
    s = min(3.3 / w, 1.7 / h)
    fig, ax = plt.subplots(figsize=(w * s + 1.1, h * s + 0.7), dpi=200)
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def _poly(ax, pts, fill=FILL, lw=1.6):
    xs, ys = zip(*(list(pts) + [pts[0]]))
    ax.fill(xs, ys, color=fill, zorder=1)
    ax.plot(xs, ys, color="black", lw=lw, zorder=3)


def _line(ax, p, q, ls="-", lw=1.6, color="black", z=3):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=z)


def _right(ax, c, u, v, s):
    """Right-angle square at corner c, sides along unit vectors u and v, size s."""
    p1 = (c[0] + u[0] * s, c[1] + u[1] * s)
    p2 = (p1[0] + v[0] * s, p1[1] + v[1] * s)
    p3 = (c[0] + v[0] * s, c[1] + v[1] * s)
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color="black", lw=0.9, zorder=4)


def _side(ax, p, q, text, away, off, size=9, rotate=False):
    """Label side p–q at its midpoint, pushed `off` away from the point `away` (e.g. the centroid)."""
    if not text:
        return
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    if (away[0] - mx) * nx + (away[1] - my) * ny > 0:
        nx, ny = -nx, -ny
    ha = "center"
    if abs(nx) > 0.35:
        ha = "left" if nx > 0 else "right"
    va = "center"
    if abs(ny) > 0.9:
        va = "bottom" if ny > 0 else "top"
    rot = 0
    if rotate:
        rot = math.degrees(math.atan2(dy, dx))
        if rot > 90:
            rot -= 180
        if rot < -90:
            rot += 180
        ha, va = "center", "center"
        off *= 1.6
    ax.text(mx + nx * off, my + ny * off, text, ha=ha, va=va, fontsize=size, rotation=rot,
            rotation_mode="anchor", zorder=5)
    ax.plot([mx + nx * off * 2.2], [my + ny * off * 2.2], alpha=0)


def _name(ax, p, text, dx, dy, size=8.5):
    if text:
        ax.text(p[0] + dx, p[1] + dy, text, ha="center", va="center", fontsize=size, zorder=5)


def _save(fig, ax, path, pad=0.08):
    ax.margins(pad)
    fig.tight_layout(pad=0.2)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.06, format="png")
    plt.close(fig)
    return path


def _cent(pts):
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))


def right_tri(a, b, labels, path, flip=False):
    """Legs a (vertical) and b (horizontal). flip=False: right angle bottom-left; True: bottom-right (a ramp)."""
    if flip:
        R, P, Q = (b, 0), (0, 0), (b, a)
        u, v = (-1, 0), (0, 1)
    else:
        R, P, Q = (0, 0), (b, 0), (0, a)
        u, v = (1, 0), (0, 1)
    fig, ax = _fig(b, a)
    _poly(ax, [R, P, Q])
    s = 0.07 * min(max(a, b), 4 * min(a, b))
    _right(ax, R, u, v, min(s, 0.45 * min(a, b)))
    c = _cent([R, P, Q]); o = 0.035 * max(a, b)
    _side(ax, R, Q, labels[0], c, o)
    _side(ax, R, P, labels[1], c, o)
    _side(ax, P, Q, labels[2], c, o)
    return _save(fig, ax, path)


def ladder(h, d, labels, path):
    """A ladder of length √(h² + d²) leaning against a wall: foot d from the wall, top h up it."""
    G = max(d * 1.25, 0.75 * h)                            # ground drawn wide enough to read the labels
    fig, ax = _fig(G, h * 1.12)
    top = h * 1.12
    ax.fill([-0.08 * d - 0.04 * h, 0, 0, -0.08 * d - 0.04 * h], [0, 0, top, top], color="#c9c9c9", zorder=1)
    _line(ax, (0, 0), (0, top), lw=1.6)
    _line(ax, (-0.1 * d, 0), (G, 0), lw=1.6)
    L = math.hypot(h, d); ux, uy = -d / L, h / L          # along the ladder, foot → top
    nx, ny = uy, -ux                                       # unit normal (pointing right/down)
    w = 0.045 * L                                          # the rails sit on the true line and just inside it
    for k in (0, 1):
        _line(ax, (d + k * nx * w, k * ny * w), (k * nx * w, h + k * ny * w), lw=1.3)
    for t in np.linspace(0.08, 0.92, 9):
        x, y = d + ux * L * t, uy * L * t
        _line(ax, (x, y), (x + nx * w, y + ny * w), lw=0.8)
    s = 0.06 * max(h, d)
    _right(ax, (0, 0), (1, 0), (0, 1), s)
    o = 0.04 * max(h, d)
    _side(ax, (d, 0), (0, h), labels[0], (0, 0), o * 2.6)
    _side(ax, (0, 0), (0, h), labels[1], (d, h / 2), o * 2.4)
    _side(ax, (0, 0), (d, 0), labels[2], (d / 2, h), o)
    return _save(fig, ax, path)


def rect_diag(L, W, labels, path):
    fig, ax = _fig(L, W)
    _poly(ax, [(0, 0), (L, 0), (L, W), (0, W)])
    _line(ax, (0, 0), (L, W), lw=1.3, ls=(0, (5, 3)))
    s = 0.05 * min(L, W) + 0.02 * max(L, W)
    s = min(s, 0.3 * min(L, W))
    _right(ax, (L, 0), (-1, 0), (0, 1), s)
    c = (L / 2, W / 2); o = 0.035 * max(L, W)
    _side(ax, (0, 0), (L, 0), labels[0], c, o)
    _side(ax, (L, 0), (L, W), labels[1], c, o)
    if labels[2]:
        ang = math.degrees(math.atan2(W, L))
        nx, ny = -W / math.hypot(L, W), L / math.hypot(L, W)
        ax.text(L * 0.42 + nx * o * 1.3, W * 0.42 + ny * o * 1.3, labels[2], rotation=ang, rotation_mode="anchor",
                ha="center", va="center", fontsize=9, zorder=5, bbox=dict(fc=FILL, ec="none", pad=0.5))
    return _save(fig, ax, path)


def isosceles(base, side, labels, path):
    h = math.sqrt(side ** 2 - (base / 2) ** 2)
    A, B, C, D = (0, 0), (base, 0), (base / 2, h), (base / 2, 0)
    fig, ax = _fig(base, h)
    _poly(ax, [A, B, C])
    _line(ax, D, C, ls=(0, (4, 3)), lw=0.9)
    s = 0.06 * max(base, h)
    _right(ax, D, (1, 0), (0, 1), min(s, 0.3 * h))
    c = _cent([A, B, C]); o = 0.035 * max(base, h)
    _side(ax, A, B, labels[0], c, o)
    _side(ax, A, C, labels[1], c, o)
    _side(ax, B, C, labels[1] if len(labels) < 4 else labels[3], c, o)
    if len(labels) > 2 and labels[2]:
        ax.text(base / 2 - 0.02 * base, h * 0.45, labels[2], ha="right", va="center", fontsize=9, zorder=5)
    return _save(fig, ax, path)


def gable(w, hr, side, labels, path):
    """End wall of a house: rectangle w × hr with an isosceles triangle (sloping sides `side`) on top."""
    t = math.sqrt(side ** 2 - (w / 2) ** 2)
    pts = [(0, 0), (w, 0), (w, hr), (w / 2, hr + t), (0, hr)]
    fig, ax = _fig(w, hr + t)
    _poly(ax, pts)
    _line(ax, (0, hr), (w, hr), ls=(0, (4, 3)), lw=0.9)
    _line(ax, (w / 2, hr), (w / 2, hr + t), ls=(0, (4, 3)), lw=0.9)
    s = 0.05 * max(w, hr + t)
    _right(ax, (w / 2, hr), (1, 0), (0, 1), min(s, 0.3 * t))
    c = (w / 2, (hr + t) / 2); o = 0.035 * max(w, hr + t)
    _side(ax, (0, 0), (w, 0), labels[0], c, o)
    _side(ax, (0, 0), (0, hr), labels[1], c, o)
    _side(ax, (0, hr), (w / 2, hr + t), labels[2], c, o)
    _side(ax, (w, hr), (w / 2, hr + t), labels[2], c, o)
    return _save(fig, ax, path)


def badge(a, b, labels, path):
    """Right-angled triangle (legs a up, b across) with a semi-circle on its hypotenuse (2025 P2 Q6)."""
    c = math.hypot(a, b)
    ang = math.degrees(math.atan2(-a, b))
    t = np.radians(np.linspace(ang, ang + 180, 90))
    arc = list(zip(b / 2 + c / 2 * np.cos(t), a / 2 + c / 2 * np.sin(t)))
    pts = [(0, 0), (b, 0)] + arc + [(0, a)]
    fig, ax = _fig(b + c / 2, a + c / 2)
    _poly(ax, pts)
    _line(ax, (0, a), (b, 0), ls=(0, (4, 3)), lw=0.9)
    _right(ax, (0, 0), (1, 0), (0, 1), 0.07 * max(a, b))
    o = 0.035 * (max(a, b) + c / 2)
    _side(ax, (0, 0), (0, a), labels[0], (b, a / 2), o)
    _side(ax, (0, 0), (b, 0), labels[1], (b / 2, a), o)
    return _save(fig, ax, path)


def two_tri_ext(h, x1, x2, labels, path):
    """Top T is h above H; A is x1 along the ground from H and B a further x2. Solid T–A, dotted T–B
    (the 2024 P2 Q6 lighthouse). labels [h, TA, AB, TB, name T, name H, name A, name B]."""
    T, H, A, B = (0, h), (0, 0), (x1, 0), (x1 + x2, 0)
    W = x1 + x2
    fig, ax = _fig(W, h)
    _line(ax, H, T); _line(ax, H, B); _line(ax, T, A)
    _line(ax, T, B, ls=(0, (2, 2.5)), lw=1.3)
    _right(ax, H, (1, 0), (0, 1), 0.05 * max(W, h))
    for p in (T, H, A, B):
        ax.plot(*p, "o", ms=3, color="black", zorder=6)
    o = 0.03 * max(W, h)
    c = (W * 0.6, h * 0.25)
    _side(ax, H, T, labels[0], c, o)
    _side(ax, T, A, labels[1], (W, 0), o, rotate=False)
    _side(ax, A, B, labels[2], (W / 2, h), o)
    if labels[3]:
        _side(ax, T, B, labels[3], (0, 0), o)
    if len(labels) > 8 and labels[8]:
        _side(ax, H, A, labels[8], (x1 / 2, h), o)
    names = (labels + ["", "", "", ""])[4:8]
    _name(ax, T, names[0], 0, 0.07 * max(W, h))
    _name(ax, H, names[1], 0, -0.13 * max(W, h) if not labels[2] else -0.07 * max(W, h))
    _name(ax, A, names[2], 0, -0.13 * max(W, h))
    _name(ax, B, names[3], 0, -0.13 * max(W, h))
    return _save(fig, ax, path)


def split_tri(bl, br, h, labels, path):
    """Triangle split into two right-angled triangles by its height h. labels [left slope, right slope,
    left base, right base, height]."""
    B, D, C, A = (0, 0), (bl, 0), (bl + br, 0), (bl, h)
    W = bl + br
    fig, ax = _fig(W, h)
    _poly(ax, [B, C, A])
    _line(ax, D, A, ls=(0, (4, 3)), lw=0.9)
    s = 0.05 * max(W, h)
    _right(ax, D, (1, 0), (0, 1), min(s, 0.3 * min(br, h)))
    o = 0.035 * max(W, h)
    c = _cent([A, B, C])
    _side(ax, B, A, labels[0], c, o)
    _side(ax, C, A, labels[1], c, o)
    _side(ax, B, D, labels[2], (bl / 2, h), o)
    _side(ax, D, C, labels[3], (bl + br / 2, h), o)
    if len(labels) > 4 and labels[4]:
        ax.text(bl - 0.015 * W, h * 0.45, labels[4], ha="right", va="center", fontsize=9, zorder=5)
    return _save(fig, ax, path)


def patio_lawn(ad, dc, ab, labels, path):
    """2023 P2 Q3 shape: right-angled triangle ADC (right angle at D, AD up, DC across) and right-angled
    triangle ACB on its hypotenuse (right angle at C, AB the hypotenuse). labels [AD, DC, AB, names A, B, C, D]."""
    D, A, C = (0, 0), (0, ad), (dc, 0)
    ac = math.hypot(ad, dc); bc = math.sqrt(ab ** 2 - ac ** 2)
    ux, uy = (C[0] - A[0]) / ac, (C[1] - A[1]) / ac
    px, py = uy, -ux                                    # perpendicular to AC
    if px * (D[0] - C[0]) + py * (D[1] - C[1]) > 0:
        px, py = -px, -py
    B = (C[0] + px * bc, C[1] + py * bc)
    xs = [0, dc, B[0]]; ys = [0, ad, B[1]]
    fig, ax = _fig(max(xs) - min(xs), max(ys) - min(ys))
    _poly(ax, [A, C, B], fill="#e3f1df")
    _poly(ax, [D, C, A])
    size = max(max(xs) - min(xs), max(ys) - min(ys))
    _right(ax, D, (1, 0), (0, 1), 0.035 * size)
    _right(ax, C, (-ux, -uy), (px, py), 0.035 * size)
    o = 0.03 * size
    _side(ax, D, A, labels[0], C, o)
    _side(ax, D, C, labels[1], A, o)
    _side(ax, A, B, labels[2], C, o)
    names = (list(labels) + ["", "", "", ""])[3:7]
    for p, n, (dx, dy) in zip((A, B, C, D), names, ((-0.04, 0.02), (0.03, 0.02), (0.03, -0.03), (-0.03, -0.03))):
        _name(ax, p, n, dx * size, dy * size)
    return _save(fig, ax, path)


def ramp(a, b, labels, path):
    """right_tri with the right angle bottom-right, rising to the right (a ramp). labels [height, across, slope]."""
    return right_tri(a, b, labels, path, flip=True)
