"""Static diagrams for Core Skills questions, drawn via the generic composite_shape hook
(metadata {"diagram": "composite_shape", "diagram_params": {"module_path": ..., "kind": ...,
"args": [...]}}). Each function saves a PNG to `path` (a file path or BytesIO)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

SHADE = "#5b9bd5"


def _save(fig, path):
    fig.tight_layout(pad=0.2)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.08, format="png")
    plt.close(fig)
    return path


def scale(lo, hi, major, minor, marker, unit, path):
    """Horizontal graduated scale. Major marks are numbered, minor marks are not; an arrow points
    at `marker`."""
    fig, ax = plt.subplots(figsize=(7.2, 1.7))
    ax.plot([lo, hi], [0, 0], color="#2c3e50", lw=2)
    n_minor = int(round((hi - lo) / minor))
    for i in range(n_minor + 1):
        v = lo + i * minor
        is_major = abs((v - lo) / major - round((v - lo) / major)) < 1e-9
        ax.plot([v, v], [0, 0.35 if is_major else 0.18], color="#2c3e50", lw=1.6 if is_major else 1)
        if is_major:
            txt = f"{v:g}"
            ax.text(v, -0.28, txt, ha="center", va="top", fontsize=11)
    ax.annotate("", xy=(marker, 0.02), xytext=(marker, 0.9),
                arrowprops=dict(arrowstyle="-|>", color="#c0392b", lw=2))
    if unit:
        ax.text(hi, -0.75, unit, ha="right", va="top", fontsize=11, style="italic")
    pad = (hi - lo) * 0.04
    ax.set_xlim(lo - pad, hi + pad)
    ax.set_ylim(-1.0, 1.0)
    ax.axis("off")
    return _save(fig, path)


def shaded_grid(rows, cols, shaded, path):
    """rows x cols grid of equal squares with `shaded` of them filled."""
    fig, ax = plt.subplots(figsize=(max(1.6, cols * 0.55), max(1.2, rows * 0.55)))
    for i in range(rows * cols):
        r, c = divmod(i, cols)
        ax.add_patch(Rectangle((c, rows - 1 - r), 1, 1, facecolor=SHADE if i < shaded else "white",
                               edgecolor="#2c3e50", lw=1.5))
    ax.set_xlim(-0.05, cols + 0.05)
    ax.set_ylim(-0.05, rows + 0.05)
    ax.set_aspect("equal")
    ax.axis("off")
    return _save(fig, path)
