"""Diagrams for Higher Hypothesis Testing — the app copy of
.pipeline-tools/haom_statistics/hypothesis_testing_diagrams.py. Every function ends with `path_or_buffer`.

    ci_plot(intervals, labels, xlabel, path_or_buffer)   95% confidence intervals as horizontal bars with the
                                                         estimate marked, against a dashed line at 0
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY = "#1f3864"


def _save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.05, dpi=200, format="png")
    plt.close(fig)
    return path


def _fmt(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def ci_plot(intervals, labels, xlabel, path_or_buffer):
    n = len(intervals)
    fig, ax = plt.subplots(figsize=(5.6, 0.75 + 0.55 * n))
    lo = min(min(a, 0) for a, _ in intervals); hi = max(max(b, 0) for _, b in intervals)
    pad = 0.12 * (hi - lo or 1)
    ax.set_xlim(lo - pad, hi + pad); ax.set_ylim(-0.6, n - 0.4)
    ax.axvline(0, color="#c00000", ls="--", lw=1.2)
    ax.text(0, n - 0.45, " 0 (no difference)", color="#c00000", fontsize=8, va="bottom", ha="left")
    for i, ((a, b), lab) in enumerate(zip(intervals, labels)):
        y = n - 1 - i
        ax.plot([a, b], [y, y], color=NAVY, lw=2.5, solid_capstyle="butt")
        ax.plot([a, a], [y - 0.15, y + 0.15], color=NAVY, lw=2); ax.plot([b, b], [y - 0.15, y + 0.15], color=NAVY, lw=2)
        ax.plot([(a + b) / 2], [y], "o", color=NAVY, ms=5)
        ax.text(a, y + 0.2, _fmt(a), fontsize=8, ha="center", va="bottom")
        ax.text(b, y + 0.2, _fmt(b), fontsize=8, ha="center", va="bottom")
    ax.set_yticks(range(n)); ax.set_yticklabels(list(reversed(labels)), fontsize=9)
    ax.set_xlabel(xlabel, fontsize=9); ax.tick_params(axis="x", labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return _save(fig, path_or_buffer)
