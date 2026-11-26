"""Charts for Statistical Graphs and the boxplot levels of Comparing Data Sets, for the "composite_shape"
renderer (diagram_params["module_path"]). Each function takes (*args, path_or_buffer) and saves a PNG."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from matplotlib.ticker import MultipleLocator  # noqa: E402

_SHADES = ["#1f4e79", "#c9d6ea"]


def _grid(ax, major, minor, axis="y"):
    for ax_name in (("y",) if axis == "y" else ("x", "y")):
        a = ax.yaxis if ax_name == "y" else ax.xaxis
        a.set_major_locator(MultipleLocator(major))
        a.set_minor_locator(MultipleLocator(minor))
    ax.grid(True, which="major", axis=axis, color="#8aa4c8", lw=0.7)
    ax.grid(True, which="minor", axis=axis, color="#d5deee", lw=0.4)
    ax.set_axisbelow(True)


def bars(cats, series, names, stacked, ymax, major, minor, ylabel, xlabel, path):
    fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=130)
    xs = range(len(cats))
    if stacked:
        base = [0] * len(cats)
        for i, (vals, name) in enumerate(zip(series, names)):
            ax.bar(xs, vals, 0.55, bottom=base, color=_SHADES[i], edgecolor="black", label=name)
            base = [b + v for b, v in zip(base, vals)]
    else:
        w = 0.38
        for i, (vals, name) in enumerate(zip(series, names)):
            ax.bar([x + (i - 0.5) * w for x in xs], vals, w, color=_SHADES[i], edgecolor="black", label=name)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(cats)
    ax.set_ylim(0, ymax)
    _grid(ax, major, minor)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False)
    fig.tight_layout()
    fig.savefig(path, format="png")
    plt.close(fig)


def conversion(xmax, rate, xmajor, xminor, ymajor, yminor, xlabel, ylabel, path):
    """Straight-line conversion graph y = rate × x."""
    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=130)
    ax.plot([0, xmax], [0, rate * xmax], color="#b00020", lw=1.6)
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, rate * xmax)
    for a, major, minor in ((ax.xaxis, xmajor, xminor), (ax.yaxis, ymajor, yminor)):
        a.set_major_locator(MultipleLocator(major))
        a.set_minor_locator(MultipleLocator(minor))
    ax.grid(True, which="major", color="#8aa4c8", lw=0.7)
    ax.grid(True, which="minor", color="#d5deee", lw=0.4)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(path, format="png")
    plt.close(fig)


def boxplots(plots, xmin, xmax, major, xlabel, path):
    """plots = [(name, [low, Q1, median, Q3, high])], drawn one above the other against one scale."""
    fig, ax = plt.subplots(figsize=(7.0, 1.0 + 0.8 * len(plots)), dpi=130)
    for i, (name, (lo, q1, med, q3, hi)) in enumerate(plots):
        y = len(plots) - i
        ax.add_patch(Rectangle((q1, y - 0.25), q3 - q1, 0.5, fill=False, lw=1.5, zorder=3))
        for a, b in (((med, med), (y - 0.25, y + 0.25)), ((lo, q1), (y, y)), ((q3, hi), (y, y)),
                     ((lo, lo), (y - 0.14, y + 0.14)), ((hi, hi), (y - 0.14, y + 0.14))):
            ax.plot(a, b, color="black", lw=1.5, zorder=3)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(0.4, len(plots) + 0.6)
    ax.set_yticks(range(len(plots), 0, -1))
    ax.set_yticklabels([name for name, _ in plots])
    ax.tick_params(axis="y", length=0)
    ax.xaxis.set_major_locator(MultipleLocator(major))
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.grid(True, which="major", axis="x", color="#8aa4c8", lw=0.7)
    ax.grid(True, which="minor", axis="x", color="#d5deee", lw=0.4)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel(xlabel)
    fig.tight_layout()
    fig.savefig(path, format="png")
    plt.close(fig)
