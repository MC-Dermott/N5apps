"""Line graph drawn for Comparing Data Sets level 5 (same look as the worksheet's Section 6 graphs).

Called by core/ui/question_ui.py's "composite_shape" diagram dispatch with
diagram_params = {"module_path": "topics.finance_statistics.comparing_data_diagrams",
                  "kind": "line_graph", "args": [labels, values, ymax, ylabel, xlabel]}.
Values are multiples of 5; the grid has a line every 5 and a label every 10."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def line_graph(labels, values, ymax, ylabel, xlabel, path_or_buffer):
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=130)
    ax.plot(range(len(values)), values, color="#1f4e79", marker="x", lw=1.6, ms=7)
    ax.set_xticks(range(len(values)))
    ax.set_xticklabels(labels)
    ax.set_xlim(-0.4, len(values) - 0.6)
    ax.set_ylim(0, ymax)
    ax.set_yticks(range(0, ymax + 1, 10))
    ax.set_yticks(range(0, ymax + 1, 5), minor=True)
    ax.grid(True, which="major", color="#8aa4c8", lw=0.7)
    ax.grid(True, which="minor", color="#d5deee", lw=0.4)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(path_or_buffer, format="png")
    plt.close(fig)


def scatter_graph(xs, ys, xrange_, yrange_, xlabel, ylabel, line, path_or_buffer):
    """Scattergraph on squared paper with the line of best fit already drawn (Comparing Data Sets level 6).
    xrange_ = (min, max, minor step, label step); yrange_ likewise; line = (a, b) for y = a + b x, drawn across the data."""
    import numpy as np
    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=130)
    ax.set_xlim(xrange_[0], xrange_[1])
    ax.set_ylim(yrange_[0], yrange_[1])
    for rng, draw in ((xrange_, ax.axvline), (yrange_, ax.axhline)):
        for v in np.arange(rng[0], rng[1] + 1e-9, rng[2]):
            major = abs((v - rng[0]) / rng[3] - round((v - rng[0]) / rng[3])) < 1e-9
            draw(v, color="#8aa4c8" if major else "#d5deee", lw=0.7 if major else 0.4, zorder=0)
    ax.set_xticks(np.arange(xrange_[0], xrange_[1] + 1e-9, xrange_[3]))
    ax.set_yticks(np.arange(yrange_[0], yrange_[1] + 1e-9, yrange_[3]))
    ax.scatter(xs, ys, marker="x", color="#1f4e79", s=40, zorder=3)
    a, b = line
    x0, x1 = min(xs), max(xs)
    ax.plot([x0, x1], [a + b * x0, a + b * x1], color="#b00020", lw=1.5, zorder=2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    fig.savefig(path_or_buffer, format="png")
    plt.close(fig)
