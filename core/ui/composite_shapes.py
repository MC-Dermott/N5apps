"""Exam-style diagrams of composite shapes (copied from the worksheet pipeline's
.pipeline-tools/n5_new_topics/shapes.py so the app draws the same pictures as the worksheet).
`path` can be a file-like object (BytesIO). Rendered by question_ui for metadata["diagram"] ==
"composite_shape", diagram_params = {"kind": <function name>, "args": [...]}.

Each function draws one kind of shape from its dimensions and saves a PNG. The outline is drawn as
one path (straight edges plus sampled arcs), so the shape has no stray internal lines. The joins
between parts are shown as dashed lines, the way the SQA papers draw them. Labels are dimension
arrows with the text written beside them. Drawings are to scale, so they need sensible numbers.

    rect_semi(L, w, labels)        rectangle L × w with a semi-circle on the right-hand w side
    track(L, w, labels)            rectangle with a semi-circle on both w sides
    square_quarter(s, gap, labels) square with a quarter circle (radius s) on its right
    arch(W, H, r, labels)          rectangle W × H with two quarter circles (radius r) on top corners
    tri_semi(a, b, labels)         right-angled triangle (legs a up, b across), semi-circle on the hypotenuse
    door(w, h, d, labels)          shaded rectangle with a white semi-circular window at the top
    house(w, h, t, labels)         rectangle with an isosceles triangle (height t) on top
    patio(L, w, r, labels)         shaded rectangle with a white circle in the middle
    square_semis(s, d, labels)     square with a semi-circle (diameter d) on each side
    path_round(L, w, p, labels)    white lawn L × w with a shaded path of width p all round
    semi(d, label) / quarter(r, label)
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

FILL = "#dbe9f6"
SHADE = "#b9b9b9"


def _arc(cx, cy, r, a0, a1, n=80):
    t = np.radians(np.linspace(a0, a1, n))
    return list(zip(cx + r * np.cos(t), cy + r * np.sin(t)))


def _fig(w, h):
    s = min(3.3 / w, 1.6 / h)          # drawn at the size it is printed, so labels stay 9–10 pt
    fig, ax = plt.subplots(figsize=(w * s + 0.9, h * s + 0.7), dpi=200)
    ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def _outline(ax, pts, fill=FILL, lw=1.6):
    xs, ys = zip(*(pts + [pts[0]]))
    ax.fill(xs, ys, color=fill, zorder=1)
    ax.plot(xs, ys, color="black", lw=lw, zorder=3)


def _dashed(ax, p, q):
    ax.plot([p[0], q[0]], [p[1], q[1]], color="black", lw=0.9, ls=(0, (4, 3)), zorder=2)


def _dim(ax, p, q, text, off, size=9):
    """Double-headed dimension arrow from p to q, pushed `off` along the left-hand normal, with the
    label sitting on the arrow (white background)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * off, dx / L * off
    a, b = (p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny)
    ax.annotate("", xy=b, xytext=a, annotation_clip=False,
                arrowprops=dict(arrowstyle="<->", lw=0.9, shrinkA=0, shrinkB=0), zorder=4)
    ax.plot([a[0], b[0]], [a[1], b[1]], alpha=0)          # so the limits include the arrow
    if text:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, text, ha="center", va="center", fontsize=size,
                zorder=5, bbox=dict(fc="white", ec="none", pad=0.8))


def _label(ax, x, y, text, size=9, **kw):
    ax.text(x, y, text, ha="center", va="center", fontsize=size, zorder=5, **kw)


def _save(fig, ax, path, pad):
    ax.margins(pad)
    fig.tight_layout(pad=0.2)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    return path


def _o(size):
    return 0.09 * size


def rect_semi(L, w, labels, path):
    r = w / 2
    pts = [(0, 0), (L, 0)] + _arc(L, r, r, -90, 90) + [(L, w), (0, w)]
    fig, ax = _fig(L + r, w)
    _outline(ax, pts); _dashed(ax, (L, 0), (L, w))
    o = _o(L + r)
    _dim(ax, (0, 0), (L, 0), labels[0], -o)
    _dim(ax, (0, w), (0, 0), labels[1], -o)
    return _save(fig, ax, path, 0.08)


def track(L, w, labels, path):
    r = w / 2
    pts = [(0, 0), (L, 0)] + _arc(L, r, r, -90, 90) + [(L, w), (0, w)] + _arc(0, r, r, 90, 270)
    fig, ax = _fig(L + w, w)
    _outline(ax, pts); _dashed(ax, (0, 0), (0, w)); _dashed(ax, (L, 0), (L, w))
    o = _o(L + w)
    _dim(ax, (0, w), (L, w), labels[0], o)
    _dim(ax, (L * 0.22, 0), (L * 0.22, w), labels[1], 0.001)
    return _save(fig, ax, path, 0.08)


def square_quarter(s, gap, labels, path):
    pts = [(0, 0), (2 * s, 0)] + _arc(s, 0, s, 0, 90) + [(0, s)]
    fig, ax = _fig(2 * s, s)
    _outline(ax, pts); _dashed(ax, (s, 0), (s, s))
    o = _o(2 * s)
    _dim(ax, (s, 0), (0, 0), labels[0], o)
    if gap:
        g0 = 2 * s - gap
        ax.plot([g0, 2 * s], [0, 0], color=FILL, lw=3.5, zorder=3.5)
        _dim(ax, (g0, 0), (2 * s, 0), "", -o * 0.8)
        _label(ax, g0 + gap / 2, -o * 1.7, f"gap {labels[1]}", size=8.5)
    return _save(fig, ax, path, 0.1)


def arch(W, H, r, labels, path):
    pts = [(0, 0), (W, 0), (W, H)] + _arc(W - r, H, r, 0, 90) + [(r, H + r)] + _arc(r, H, r, 90, 180)
    fig, ax = _fig(W, H + r)
    _outline(ax, pts)
    _dashed(ax, (0, H), (W, H)); _dashed(ax, (r, H), (r, H + r)); _dashed(ax, (W - r, H), (W - r, H + r))
    o = _o(W)
    _dim(ax, (W, 0), (0, 0), labels[0], o)
    _dim(ax, (0, H), (0, 0), labels[1], o)
    _dim(ax, (W - r, H), (W, H), labels[2], 0.18 * r, size=8.5)
    return _save(fig, ax, path, 0.08)


def tri_semi(a, b, labels, path):
    h = math.hypot(a, b)
    ang = math.degrees(math.atan2(-a, b))      # from (0, a) to (b, 0)
    cx, cy = b / 2, a / 2
    pts = [(0, 0), (b, 0)] + _arc(cx, cy, h / 2, ang, ang + 180) + [(0, a)]
    fig, ax = _fig(b + h / 2, a + h / 2)
    _outline(ax, pts); _dashed(ax, (0, a), (b, 0))
    q = 0.07 * max(a, b)
    ax.plot([q, q, 0], [0, q, q], color="black", lw=0.9, zorder=3)
    o = _o(max(a, b) + h / 2)
    _dim(ax, (b, 0), (0, 0), labels[1], o)
    _dim(ax, (0, 0), (0, a), labels[0], o)
    return _save(fig, ax, path, 0.08)


def door(w, h, d, labels, path):
    r = d / 2
    fig, ax = _fig(w, h)
    _outline(ax, [(0, 0), (w, 0), (w, h), (0, h)], fill=SHADE)
    top = h - 0.1 * h - r
    win = _arc(w / 2, top, r, 0, 180)
    _outline(ax, win, fill="white", lw=1.2)
    o = _o(h * 0.8)
    _dim(ax, (0, 0), (w, 0), labels[0], -o)
    _dim(ax, (w, 0), (w, h), labels[1], o)
    _dim(ax, (w / 2 - r, top), (w / 2 + r, top), labels[2], -0.06 * h, size=8.5)
    return _save(fig, ax, path, 0.1)


def house(w, h, t, labels, path):
    pts = [(0, 0), (w, 0), (w, h), (w / 2, h + t), (0, h)]
    fig, ax = _fig(w, h + t)
    _outline(ax, pts); _dashed(ax, (0, h), (w, h)); _dashed(ax, (w / 2, h), (w / 2, h + t))
    o = _o(w)
    _dim(ax, (0, 0), (w, 0), labels[0], -o)
    _dim(ax, (0, h), (0, 0), labels[1], -o)
    if len(labels) > 2 and labels[2]:
        _dim(ax, (w / 2, h), (w / 2, h + t), labels[2], -0.001 - o * 0.4)
    if len(labels) > 3 and labels[3]:
        L = math.hypot(w / 2, t)
        _label(ax, 0.75 * w + t / L * o * 1.3, h + t / 2 + w / 2 / L * o * 1.3, labels[3], size=9)
    return _save(fig, ax, path, 0.08)


def patio(L, w, r, labels, path):
    fig, ax = _fig(L, w)
    _outline(ax, [(0, 0), (L, 0), (L, w), (0, w)], fill=SHADE)
    _outline(ax, _arc(L / 2, w / 2, r, 0, 360)[:-1], fill="white", lw=1.2)
    ax.plot([L / 2, L / 2 + r], [w / 2, w / 2], color="black", lw=0.9, zorder=4)
    _label(ax, L / 2 + r / 2, w / 2 + r * 0.25, labels[2], size=8.5)
    o = _o(L)
    _dim(ax, (0, 0), (L, 0), labels[0], -o)
    _dim(ax, (L, 0), (L, w), labels[1], o)
    return _save(fig, ax, path, 0.08)


def square_semis(s, d, labels, path):
    r, m = d / 2, s / 2
    pts = ([(0, 0), (m - r, 0)] + _arc(m, 0, r, 180, 360) + [(s, 0), (s, m - r)] + _arc(s, m, r, -90, 90) +
           [(s, s), (m + r, s)] + _arc(m, s, r, 0, 180) + [(0, s), (0, m + r)] + _arc(0, m, r, 90, 270))
    fig, ax = _fig(s + d, s + d)
    _outline(ax, pts)
    for p, q in (((m - r, 0), (m + r, 0)), ((s, m - r), (s, m + r)), ((m - r, s), (m + r, s)),
                 ((0, m - r), (0, m + r))):
        _dashed(ax, p, q)
    _dim(ax, (s * 0.12, 0), (s * 0.12, s), labels[0], 0.001)
    _dim(ax, (m - r, s), (m + r, s), labels[1], -0.001 - s * 0.08, size=8.5)
    return _save(fig, ax, path, 0.06)


def path_round(L, w, p, labels, path):
    fig, ax = _fig(L + 2 * p, w + 2 * p)
    _outline(ax, [(-p, -p), (L + p, -p), (L + p, w + p), (-p, w + p)], fill=SHADE)
    _outline(ax, [(0, 0), (L, 0), (L, w), (0, w)], fill="#e3f1df", lw=1.2)
    _label(ax, L / 2, w / 2, "lawn", size=8.5)
    o = _o(L)
    _dim(ax, (0, w * 0.25), (L, w * 0.25), labels[0], 0.001)
    _dim(ax, (L * 0.8, 0), (L * 0.8, w), labels[1], 0.001)
    _dim(ax, (L, w * 0.6), (L + p, w * 0.6), "", 0.001)
    _label(ax, L + p / 2, w * 0.6 + o * 0.9, labels[2], size=8.5)
    return _save(fig, ax, path, 0.08)


def semi(d, label, path):
    r = d / 2
    fig, ax = _fig(d, r)
    _outline(ax, _arc(r, 0, r, 0, 180))
    _dim(ax, (0, 0), (d, 0), label, -_o(d))
    return _save(fig, ax, path, 0.1)


def quarter(r, label, path):
    fig, ax = _fig(r, r)
    _outline(ax, [(0, 0)] + _arc(0, 0, r, 0, 90))
    q = 0.08 * r
    ax.plot([q, q, 0], [0, q, q], color="black", lw=0.9, zorder=3)
    _dim(ax, (0, 0), (r, 0), label, -_o(r))
    return _save(fig, ax, path, 0.1)
