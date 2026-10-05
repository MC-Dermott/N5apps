"""Diagrams for the Higher Applications of Maths "Data and Distributions" worksheet, homework and app.
The app copy is N5apps/topics/statistics/data_distributions_diagrams.py (identical file). Every function
ends with a `path` argument, which can be a filename or a BytesIO, and takes only JSON-friendly arguments
(lists, numbers, strings) so the app can call it from metadata["diagram_params"].

    histogram(values, edges, xlabel, title, path)       frequency histogram, bars touching, true scale
    shapes(kinds, path)                                 three histograms "A", "B", "C"; kinds from
                                                        "normal", "right" (tail to the right), "left"
    boxplots(groups, label, title, path)                comparative box plots on one scale; groups =
                                                        [[name, min, Q1, median, Q3, max], ...]
    bar_chart(labels, counts, xlabel, ylabel, title, path)
    misleading_bar(labels, values, ymin, ylabel, title, path)   bar chart with a truncated vertical axis
    line_trend(xs, ys, x_end, ylabel, title, path)      data points joined, with a dashed straight line
                                                        drawn on to x_end (an extrapolated headline)
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402,F401

BAR = "#9cc3e6"
EDGE = "#1f3864"


def _save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.06, dpi=200, format="png")
    plt.close(fig)
    return path


def _nice_step(span, target=6):
    raw = span / target
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            return m * mag
    return 10 * mag


def histogram(values, edges, xlabel, title, path):
    counts = [0] * (len(edges) - 1)
    for v in values:
        for i in range(len(edges) - 1):
            last = i == len(edges) - 2
            if edges[i] <= v < edges[i + 1] or (last and v == edges[-1]):
                counts[i] += 1
                break
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    for i, c in enumerate(counts):
        ax.bar(edges[i], c, width=edges[i + 1] - edges[i], align="edge", color=BAR, edgecolor=EDGE, lw=0.9)
    ax.set_xlim(edges[0], edges[-1])
    top = max(counts)
    step = 1 if top <= 8 else 2 if top <= 16 else 5
    ax.set_yticks(range(0, top + step + 1, step))
    ax.set_ylim(0, top + step * 0.6)
    ax.set_xticks(edges if len(edges) <= 14 else edges[::2])
    ax.grid(axis="y", color="#dddddd", lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel(xlabel, fontsize=9); ax.set_ylabel("Frequency", fontsize=9)
    ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    return _save(fig, path)


_SHAPE_COUNTS = {
    "normal": [1, 3, 7, 12, 16, 12, 7, 3, 1],
    "right": [6, 15, 17, 12, 8, 5, 3, 2, 1],
    "left": [1, 2, 3, 5, 8, 12, 17, 15, 6],
}


def shapes(kinds, path):
    fig, axes = plt.subplots(1, len(kinds), figsize=(2.3 * len(kinds), 1.9))
    if len(kinds) == 1:
        axes = [axes]
    for ax, k, letter in zip(axes, kinds, "ABCDE"):
        c = _SHAPE_COUNTS[k]
        ax.bar(range(len(c)), c, width=1.0, color=BAR, edgecolor=EDGE, lw=0.8)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.set_title(f"Histogram {letter}", fontsize=10)
        ax.set_xlabel("value", fontsize=8); ax.set_ylabel("frequency", fontsize=8)
    fig.tight_layout()
    return _save(fig, path)


def boxplots(groups, label, title, path):
    """Horizontal comparative box plots on a common, labelled scale (to scale)."""
    n = len(groups)
    fig, ax = plt.subplots(figsize=(5.4, 0.75 + 0.85 * n))
    lo = min(g[1] for g in groups); hi = max(g[5] for g in groups)
    step = _nice_step(hi - lo, 8)
    a = math.floor(lo / step) * step; b = math.ceil(hi / step) * step
    if b - hi < step * 0.2:
        b += step
    if lo - a < step * 0.2:
        a -= step
    for i, (name, mn, q1, med, q3, mx) in enumerate(groups):
        y = n - 1 - i
        ax.add_patch(plt.Rectangle((q1, y - 0.25), q3 - q1, 0.5, fill=True, facecolor=BAR, edgecolor=EDGE, lw=1.2))
        ax.plot([med, med], [y - 0.25, y + 0.25], color=EDGE, lw=2.2)
        ax.plot([mn, q1], [y, y], color=EDGE, lw=1.2); ax.plot([q3, mx], [y, y], color=EDGE, lw=1.2)
        ax.plot([mn, mn], [y - 0.13, y + 0.13], color=EDGE, lw=1.2)
        ax.plot([mx, mx], [y - 0.13, y + 0.13], color=EDGE, lw=1.2)
    ax.set_yticks(range(n)); ax.set_yticklabels([g[0] for g in groups][::-1], fontsize=9)
    ax.set_ylim(-0.6, n - 0.4)
    ticks = []
    t = a
    while t <= b + 1e-9:
        ticks.append(round(t, 6)); t += step
    ax.set_xticks(ticks); ax.set_xlim(a, b)
    ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(step / 5))
    ax.grid(axis="x", which="both", color="#e3e3e3", lw=0.5); ax.set_axisbelow(True)
    ax.set_xlabel(label, fontsize=9); ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    return _save(fig, path)


def bar_chart(labels, counts, xlabel, ylabel, title, path):
    fig, ax = plt.subplots(figsize=(5.4, 2.8))
    ax.bar(range(len(counts)), counts, width=0.6, color=BAR, edgecolor=EDGE, lw=0.9)
    ax.set_xticks(range(len(counts))); ax.set_xticklabels(labels, fontsize=8)
    top = max(counts)
    step = _nice_step(top, 6)
    ax.set_yticks([k * step for k in range(int(top // step) + 2)])
    ax.set_ylim(0, (int(top // step) + 1) * step)
    ax.grid(axis="y", color="#dddddd", lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel(xlabel, fontsize=9); ax.set_ylabel(ylabel, fontsize=9); ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    return _save(fig, path)


def misleading_bar(labels, values, ymin, ylabel, title, path):
    fig, ax = plt.subplots(figsize=(3.8, 2.9))
    ax.bar(range(len(values)), [v - ymin for v in values], bottom=ymin, width=0.55, color=BAR, edgecolor=EDGE, lw=0.9)
    ax.set_xticks(range(len(values))); ax.set_xticklabels(labels, fontsize=9)
    top = max(values)
    step = _nice_step(top - ymin, 5)
    ax.set_ylim(ymin, math.ceil(top / step) * step + step * 0.5)
    ax.set_yticks([ymin + k * step for k in range(int((ax.get_ylim()[1] - ymin) // step) + 1)])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.grid(axis="y", color="#dddddd", lw=0.6); ax.set_axisbelow(True)
    ax.set_ylabel(ylabel, fontsize=9); ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    return _save(fig, path)


def line_trend(xs, ys, x_end, ylabel, title, path):
    fig, ax = plt.subplots(figsize=(5.4, 2.8))
    ax.plot(xs, ys, "o-", color=EDGE, lw=1.4, ms=4)
    # straight line through the last two points, carried on to x_end (the newspaper's projection)
    (x0, y0), (x1, y1) = (xs[-2], ys[-2]), (xs[-1], ys[-1])
    slope = (y1 - y0) / (x1 - x0)
    ax.plot([x1, x_end], [y1, y1 + slope * (x_end - x1)], "--", color="#b00020", lw=1.3)
    ax.set_xlim(xs[0] - 0.5, x_end + 0.5)
    ax.set_xticks(list(range(xs[0], x_end + 1, 2 if x_end - xs[0] > 8 else 1)))
    top = max(ys)
    step = _nice_step(top, 6)
    ax.set_ylim(0, math.ceil(top / step) * step + step)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.grid(color="#dddddd", lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel("year", fontsize=9); ax.set_ylabel(ylabel, fontsize=9); ax.set_title(title, fontsize=10)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    return _save(fig, path)
