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
