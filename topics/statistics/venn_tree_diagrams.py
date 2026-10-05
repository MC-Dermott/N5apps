"""Venn and tree diagrams for Higher Applications of Maths — Probability (Venn and Tree Diagrams).
The worksheet library builds its pictures with the same file (copied to
.pipeline-tools/haom_statistics/venn_tree_diagrams.py). Every function ends with a `path` argument, which
can be a filename or a BytesIO, so the app can call it as fn(*args, buffer).

    venn2(labels, regions, path, title=None)     two sets in a rectangle; regions = {"A", "B", "AB", "none"}
    venn3(labels, regions, path, title=None)     three sets; regions = {"A", "B", "C", "AB", "AC", "BC",
                                                 "ABC", "none"} ("A" = A only, "AB" = A and B but not C …)
    tree(stages, first, second, path, outcomes=None, title=None)
                                                 a two-stage probability tree: stages = (heading 1, heading 2),
                                                 first = [[label, p], …], second = one [[label, p], …] list per
                                                 first branch, outcomes = the combined probability of each
                                                 path (top to bottom), or None for no outcome column.

    tree_q(stages, first, second, outcomes, path)
                                                 the same, with every argument before `path` (the app's
                                                 fn(*args, buffer) call convention).

A region value or probability of None is drawn as an empty box for the pupil to fill in. Values may be
numbers or strings ("4/9", "0.25").
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

EDGE = "#1F3864"
FILLS = ["#cfe3f5", "#f8d9c4", "#d6efd0"]


def _save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.06, dpi=200, format="png")
    plt.close(fig)
    return path


def _fmt(v):
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v)


def _value(ax, x, y, v, size=11):
    """A region count, or an empty answer box when v is None."""
    if v is None:
        ax.add_patch(Rectangle((x - 0.17, y - 0.11), 0.34, 0.22, fill=True, facecolor="white",
                               edgecolor="black", lw=1.0, zorder=5))
    else:
        ax.text(x, y, _fmt(v), ha="center", va="center", fontsize=size, zorder=6,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.75))


def _frame(ax, x0, y0, x1, y1, none):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, edgecolor="black", lw=1.4))
    # the 'none' count goes INSIDE the rectangle, outside every circle (2024 MI: "must be within the diagram")
    _value(ax, x1 - 0.32, y0 + 0.24, none)


def venn2(labels, regions, path, title=None):
    fig, ax = plt.subplots(figsize=(4.4, 2.75))
    r = 1.0
    ca, cb = (-0.62, 0.0), (0.62, 0.0)
    for (c, f) in zip((ca, cb), FILLS):
        ax.add_patch(Circle(c, r, facecolor=f, alpha=0.45, edgecolor=EDGE, lw=1.6))
    _frame(ax, -2.15, -1.32, 2.15, 1.45, regions.get("none"))
    ax.text(-2.05, 1.22, labels[0], ha="left", va="center", fontsize=10.5, fontweight="bold")
    ax.text(2.05, 1.22, labels[1], ha="right", va="center", fontsize=10.5, fontweight="bold")
    _value(ax, -1.05, 0.0, regions.get("A"))
    _value(ax, 0.0, 0.0, regions.get("AB"))
    _value(ax, 1.05, 0.0, regions.get("B"))
    ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.37, 1.5); ax.set_aspect("equal"); ax.axis("off")
    if title:
        ax.set_title(title, fontsize=10)
    return _save(fig, path)


def venn3(labels, regions, path, title=None):
    fig, ax = plt.subplots(figsize=(4.6, 3.95))
    r = 1.0
    ca, cb, cc = (-0.58, 0.38), (0.58, 0.38), (0.0, -0.6)
    for c, f in zip((ca, cb, cc), FILLS):
        ax.add_patch(Circle(c, r, facecolor=f, alpha=0.45, edgecolor=EDGE, lw=1.6))
    _frame(ax, -2.3, -1.95, 2.3, 1.85, regions.get("none"))
    ax.text(ca[0] - 0.3, 1.6, labels[0], ha="center", va="center", fontsize=10.5, fontweight="bold")
    ax.text(cb[0] + 0.3, 1.6, labels[1], ha="center", va="center", fontsize=10.5, fontweight="bold")
    ax.text(-2.2, -1.75, labels[2], ha="left", va="center", fontsize=10.5, fontweight="bold")
    pos = {"A": (-1.0, 0.62), "B": (1.0, 0.62), "C": (0.0, -1.12), "AB": (0.0, 0.88),
           "AC": (-0.66, -0.36), "BC": (0.66, -0.36), "ABC": (0.0, 0.05)}
    for k, (x, y) in pos.items():
        _value(ax, x, y, regions.get(k))
    ax.set_xlim(-2.35, 2.35); ax.set_ylim(-2.0, 1.9); ax.set_aspect("equal"); ax.axis("off")
    if title:
        ax.set_title(title, fontsize=10)
    return _save(fig, path)


def _branch_label(ax, x0, y0, x1, y1, p, above):
    xm, ym = x0 + 0.5 * (x1 - x0), y0 + 0.5 * (y1 - y0)
    dy = 0.3 if above else -0.3
    if p is None:
        ax.add_patch(Rectangle((xm - 0.32, ym + dy - 0.16), 0.64, 0.32, facecolor="white", edgecolor="black",
                               lw=1.0, zorder=5))
    else:
        ax.text(xm, ym + dy, _fmt(p), ha="center", va="center", fontsize=10, zorder=6)


CH = 0.15          # width of one character of a 10 pt label, in data units


def tree(stages, first, second, path, outcomes=None, title=None):
    n1 = len(first)
    leaves = sum(len(s) for s in second)
    gap = 1.0
    H = leaves * gap
    leaf_y = [H - gap / 2 - i * gap for i in range(leaves)]
    k = 0; node_y = []; leaf_rows = []
    for s in second:
        ys = leaf_y[k:k + len(s)]; leaf_rows.append(ys); node_y.append(sum(ys) / len(ys)); k += len(s)
    root = (0.0, sum(node_y) / n1)
    x1 = 2.6
    w1 = max(len(l) for l, _ in first) * CH
    xs = x1 + w1 + 0.25
    x2 = xs + 2.6
    w2 = max(len(l2) for s in second for l2, _ in s) * CH
    right = x2 + w2
    xo = max(right + 1.0, x2 + w2 / 2 + len(stages[1]) * 0.09 + 1.3)
    if outcomes is not None:
        right = xo + 0.9
    fig, ax = plt.subplots(figsize=(right * 0.62 + 0.3, H * 0.62 + 0.5))
    ax.text(x1 + w1 / 2, H + 0.25, stages[0], ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.text(x2 + w2 / 2, H + 0.25, stages[1], ha="center", va="bottom", fontsize=10, fontweight="bold")
    if outcomes is not None:
        ax.text(xo, H + 0.25, "probability", ha="center", va="bottom", fontsize=10, fontweight="bold")
    i_leaf = 0
    for i, ((lab, p), y) in enumerate(zip(first, node_y)):
        ax.plot([root[0], x1 - 0.1], [root[1], y], color="black", lw=1.2)
        _branch_label(ax, root[0], root[1], x1 - 0.1, y, p, y >= root[1])
        ax.text(x1, y, lab, ha="left", va="center", fontsize=10)
        for (lab2, p2), y2 in zip(second[i], leaf_rows[i]):
            ax.plot([xs, x2 - 0.1], [y, y2], color="black", lw=1.2)
            _branch_label(ax, xs, y, x2 - 0.1, y2, p2, y2 >= y)
            ax.text(x2, y2, lab2, ha="left", va="center", fontsize=10)
            if outcomes is not None:
                v = outcomes[i_leaf]
                if v is None:
                    ax.add_patch(Rectangle((xo - 0.55, y2 - 0.16), 1.1, 0.32, facecolor="white", edgecolor="black",
                                           lw=1.0))
                else:
                    ax.text(xo, y2, _fmt(v), ha="center", va="center", fontsize=10)
            i_leaf += 1
    ax.set_xlim(-0.2, right); ax.set_ylim(-0.1, H + 0.75); ax.set_aspect("equal"); ax.axis("off")
    if title:
        ax.set_title(title, fontsize=10)
    return _save(fig, path)


def tree_q(stages, first, second, outcomes, path):
    """tree() for the app: every argument comes before the path/buffer."""
    return tree(stages, first, second, path, outcomes=outcomes)
