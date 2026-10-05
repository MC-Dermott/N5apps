"""Diagrams for the Higher Mathematical Modelling worksheet — the app copy (the original is
.pipeline-tools/haom_modelling/modelling_diagrams.py, plus the app wrappers at the end). Every function ends with a `path` argument, which
can be a filename or a BytesIO.

    container(kind, path)                    side view of a container: "cylinder", "cone_down" (point at the
                                             bottom, like a funnel), "cone_up" (point at the top), "sphere",
                                             "flask" (wide bottom, narrow neck), "bowl" (hemisphere)
    sketch_graphs(kinds, path, ylabel)       three unlabelled depth–time sketches "Graph A/B/C"; kinds from
                                             "linear", "fast_slow" (concave down), "slow_fast" (concave up),
                                             "s_shape" (fast–slow–fast), "two_rates" (slow then fast, two lines)
    line_graph(x0, y0, x1, y1, path, xlabel, ylabel, xmax, ymax, title, points=False)
                                             a straight-line model on a grid (exam-style axes)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

FILL = "#cfe3f5"


def _save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.05, dpi=200, format="png")
    plt.close(fig)
    return path


def _profile(kind):
    """Right-hand half-width w(h) of a container of height 1 (h from 0 to 1)."""
    h = np.linspace(0, 1, 200)
    if kind == "cylinder":
        w = np.full_like(h, 0.45)
    elif kind == "cone_down":
        w = 0.04 + 0.5 * h
    elif kind == "cone_up":
        w = 0.04 + 0.5 * (1 - h)
    elif kind == "sphere":
        w = 0.5 * np.sqrt(np.clip(1 - (2 * h - 1) ** 2, 0, 1)) + 0.01
    elif kind == "bowl":
        w = 0.55 * np.sqrt(np.clip(1 - (1 - h) ** 2, 0, 1)) + 0.01
    elif kind == "flask":
        w = np.where(h < 0.55, 0.5, np.where(h < 0.7, 0.5 - (h - 0.55) / 0.15 * 0.36, 0.14))
    else:
        raise ValueError(kind)
    return h, w


def container(kind, path):
    h, w = _profile(kind)
    fig, ax = plt.subplots(figsize=(1.7, 1.9))
    xs = np.concatenate([-w[::-1], w]); ys = np.concatenate([h[::-1], h])
    level = 0.42
    m = h <= level
    ax.fill(np.concatenate([-w[m][::-1], w[m]]), np.concatenate([h[m][::-1], h[m]]), color=FILL, lw=0)
    open_top = kind not in ("sphere", "cone_up")
    if open_top:
        ax.plot(-w, h, color="black", lw=1.6); ax.plot(w, h, color="black", lw=1.6)
        ax.plot([-w[0], w[0]], [0, 0], color="black", lw=1.6)
    else:
        ax.plot(xs, ys, color="black", lw=1.6)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.65, 0.65); ax.set_ylim(-0.05, 1.05)
    return _save(fig, path)


_SHAPES = {
    "linear": lambda t: t,
    "fast_slow": lambda t: 1 - (1 - t) ** 2,
    "slow_fast": lambda t: t ** 2,
    "s_shape": lambda t: 0.5 + 0.5 * np.sign(2 * t - 1) * np.abs(2 * t - 1) ** (1 / 3),
    "two_rates": lambda t: np.where(t < 0.6, t * 0.5, 0.3 + (t - 0.6) / 0.4 * 0.7),
}


def sketch_graphs(kinds, path, ylabel="depth of water", xlabel="time"):
    fig, axes = plt.subplots(1, len(kinds), figsize=(2.1 * len(kinds), 1.9))
    t = np.linspace(0, 1, 200)
    for ax, k, letter in zip(axes, kinds, "ABCDE"):
        ax.plot(t, _SHAPES[k](t), color="black", lw=1.6)
        ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.08); ax.set_xticks([]); ax.set_yticks([])
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.set_title(f"Graph {letter}", fontsize=10)
        ax.set_xlabel(xlabel, fontsize=8); ax.set_ylabel(ylabel, fontsize=8)
    fig.tight_layout()
    return _save(fig, path)


def line_graph(x0, y0, x1, y1, path, xlabel="time (minutes)", ylabel="depth of water (centimetres)",
               xmax=None, ymax=None, title=None, points=False, draw=True):
    """Exam-style grid with (optionally) the straight-line model from (x0, y0) to (x1, y1)."""
    xmax = xmax or x1 + 2
    ymax = ymax or y1 * 1.1
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    if draw:
        if points:
            xs = np.linspace(x0, x1, 8)
            ax.plot(xs, y0 + (y1 - y0) * (xs - x0) / (x1 - x0), "o", color="#1f4e8c", ms=4)
        else:
            ax.plot([x0, x1], [y0, y1], color="#1f4e8c", lw=2)
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax)
    ax.grid(True, color="#cccccc", lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel(xlabel, fontsize=9); ax.set_ylabel(ylabel, fontsize=9)
    if title:
        ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    return _save(fig, path)


# ── app wrappers: every renderer call is fn(*args, path) ──────────────────────────────────────
def container_and_graphs(kind, kinds, path):
    """The container on the left and the three Graph A/B/C sketches beside it, in one picture."""
    fig = plt.figure(figsize=(8.4, 1.9))
    ax0 = fig.add_axes([0.0, 0.05, 0.17, 0.9])
    h, w = _profile(kind)
    m = h <= 0.42
    ax0.fill(np.concatenate([-w[m][::-1], w[m]]), np.concatenate([h[m][::-1], h[m]]), color=FILL, lw=0)
    if kind in ("sphere", "cone_up"):
        ax0.plot(np.concatenate([-w[::-1], w]), np.concatenate([h[::-1], h]), color="black", lw=1.6)
    else:
        ax0.plot(-w, h, color="black", lw=1.6); ax0.plot(w, h, color="black", lw=1.6)
        ax0.plot([-w[0], w[0]], [0, 0], color="black", lw=1.6)
    ax0.set_aspect("equal"); ax0.axis("off"); ax0.set_xlim(-0.65, 0.65); ax0.set_ylim(-0.05, 1.05)
    t = np.linspace(0, 1, 200)
    for i, (k, letter) in enumerate(zip(kinds, "ABC")):
        ax = fig.add_axes([0.25 + i * 0.26, 0.2, 0.2, 0.65])
        ax.plot(t, _SHAPES[k](t), color="black", lw=1.6)
        ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.08); ax.set_xticks([]); ax.set_yticks([])
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.set_title(f"Graph {letter}", fontsize=10); ax.set_xlabel("time", fontsize=8)
        ax.set_ylabel("depth of water", fontsize=8)
    return _save(fig, path)


def rate_graph(x1, y1, xlabel, ylabel, path):
    return line_graph(0, 0, x1, y1, path, xlabel, ylabel, xmax=x1 * 1.15, ymax=y1 * 1.1, points=True)
