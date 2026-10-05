"""Drawings for Probability and Expected Frequency (N5): fair spinners and a pie chart with its angles.
Each function takes (*args, path_or_buffer) and saves a PNG, for the "composite_shape" renderer in
core/ui/question_ui.py (diagram_params["module_path"]). Same drawings as the worksheet
(.pipeline-tools/n5_new_topics/probability_diagrams.py in the worksheet library)."""
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Wedge, FancyArrow  # noqa: E402

_FILL = {"red": "#f4b6b6", "blue": "#b6cdf4", "green": "#bfe6bf", "yellow": "#f7eaa6", "white": "#ffffff",
         "orange": "#f8cfa0", "purple": "#d9c2ef", "pink": "#f6c6dc"}


def _spinner(ax, cx, labels, name):
    n = len(labels)
    for i, lab in enumerate(labels):
        a0 = 90 - (i + 1) * 360 / n
        ax.add_patch(Wedge((cx, 0), 1, a0, a0 + 360 / n, facecolor=_FILL.get(str(lab).lower(), "#ffffff"),
                           edgecolor="black", lw=1.4))
        mid = math.radians(a0 + 180 / n)
        size = 15 if len(str(lab)) <= 2 else (11 if len(str(lab)) <= 5 else 9)
        ax.text(cx + 0.62 * math.cos(mid), 0.62 * math.sin(mid), str(lab), ha="center", va="center", fontsize=size)
    ax.add_patch(FancyArrow(cx, 0, 0.1, 0.24, width=0.035, head_width=0.11, head_length=0.1, color="black"))
    ax.plot([cx], [0], "o", color="black", ms=5)
    if name:
        ax.text(cx, -1.25, name, ha="center", va="center", fontsize=13)


def spinners(a, b, names, path):
    """Two fair spinners side by side. a, b: section labels in order round the spinner."""
    fig, ax = plt.subplots(figsize=(6.4, 3.0), dpi=200)
    _spinner(ax, -1.35, a, names[0] if names else "")
    _spinner(ax, 1.35, b, names[1] if names else "")
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-1.45, 1.1); ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(); fig.savefig(path, format="png"); plt.close(fig)
    return path


def spinner(a, name, path):
    """One fair spinner."""
    fig, ax = plt.subplots(figsize=(3.0, 3.0), dpi=200)
    _spinner(ax, 0, a, name)
    ax.set_xlim(-1.2, 1.2); ax.set_ylim(-1.45, 1.1); ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(); fig.savefig(path, format="png"); plt.close(fig)
    return path


def pie(labels, angles, path):
    """Pie chart with each sector's angle written in it and its name outside (angles sum to 360)."""
    assert abs(sum(angles) - 360) < 1e-9
    fig, ax = plt.subplots(figsize=(4.6, 3.6), dpi=200)
    start = 90
    greys = ["#ffffff", "#e6e6e6", "#cccccc", "#f2f2f2", "#d9d9d9", "#bfbfbf"]
    for i, (lab, ang) in enumerate(zip(labels, angles)):
        ax.add_patch(Wedge((0, 0), 1, start - ang, start, facecolor=greys[i % len(greys)], edgecolor="black", lw=1.3))
        mid = math.radians(start - ang / 2)
        ax.text(0.6 * math.cos(mid), 0.6 * math.sin(mid), f"{ang:g}°", ha="center", va="center", fontsize=13)
        ax.text(1.18 * math.cos(mid), 1.18 * math.sin(mid), lab, ha="left" if math.cos(mid) >= 0 else "right",
                va="center", fontsize=13)
        start -= ang
    ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.25, 1.25); ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout(); fig.savefig(path, format="png"); plt.close(fig)
    return path
