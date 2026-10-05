"""Diagrams for the Higher Correlation and Regression worksheet (and the app, which keeps an identical
copy at N5apps/topics/statistics/correlation_regression_diagrams.py). Every function ends with a `path`
argument, which can be a filename or a BytesIO.

    scatter(xs, ys, path, xlabel, ylabel, title, line=False, xpad=0.08, ypad=0.12, mark=None)
        an exam-style scatter plot of Y on X ("Scatterplot of Y on X"); line=True adds the least-squares
        regression line across the range of the data; mark=(x, y) adds an open circle (a predicted point)
    panels(kinds, path, seed=0)
        three or four small unlabelled scatter plots "Plot A/B/C/D" of a given kind: "strong_pos",
        "moderate_pos", "weak_pos", "strong_neg", "moderate_neg", "weak_neg", "none", "curve"
    time_series(labels, values, path, xlabel, ylabel, title, ma=None)
        a line graph of a time series (e.g. quarterly figures); ma = list of [position, value] centred
        moving averages (position 1.5 = halfway between the 2nd and 3rd points) drawn as a dashed trend line
    app_scatter / app_panels / app_time_series  the same, with the path as the LAST argument (for the app's
        "composite_shape" diagram dispatch: fn(*args, path_or_buffer))
"""
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DOT = "#1f3864"
LINE = "#c0392b"


def _save(fig, path):
    fig.savefig(path, bbox_inches="tight", pad_inches=0.05, dpi=200, format="png")
    plt.close(fig)
    return path


def _fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return my - b * mx, b


def _axes(ax):
    ax.grid(True, color="#dddddd", linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def scatter(xs, ys, path, xlabel="x", ylabel="y", title=None, line=False, xpad=0.08, ypad=0.12, mark=None):
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    ax.scatter(xs, ys, s=22, color=DOT, zorder=3)
    lo, hi = min(xs), max(xs)
    if line:
        a, b = _fit(xs, ys)
        ax.plot([lo, hi], [a + b * lo, a + b * hi], color=LINE, linewidth=1.6, zorder=2)
    if mark:
        ax.scatter([mark[0]], [mark[1]], s=60, facecolors="none", edgecolors=LINE, linewidths=1.6, zorder=4)
    xr = (hi - lo) or 1
    yl, yh = min(ys + ([mark[1]] if mark else [])), max(ys + ([mark[1]] if mark else []))
    yr = (yh - yl) or 1
    xl = min(lo, mark[0]) if mark else lo
    xh = max(hi, mark[0]) if mark else hi
    ax.set_xlim(xl - xpad * xr, xh + xpad * xr)
    ax.set_ylim(yl - ypad * yr, yh + ypad * yr)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(labelsize=8)
    ax.set_title(title or f"Scatterplot of {ylabel} on {xlabel}", fontsize=10)
    _axes(ax)
    return _save(fig, path)


def _panel_data(kind, rnd, n=22):
    xs = [rnd.uniform(0, 10) for _ in range(n)]
    noise = {"strong": 0.6, "moderate": 1.6, "weak": 3.0}
    if kind == "none":
        ys = [rnd.uniform(0, 10) for _ in xs]
    elif kind == "curve":
        ys = [10 - 0.4 * (x - 5) ** 2 + rnd.gauss(0, 0.5) for x in xs]
    else:
        strength, sign = kind.split("_")
        s = 1 if sign == "pos" else -1
        ys = [5 + s * 0.8 * (x - 5) + rnd.gauss(0, noise[strength]) for x in xs]
    return xs, ys


def panels(kinds, path, seed=0):
    rnd = random.Random(seed)
    fig, axs = plt.subplots(1, len(kinds), figsize=(2.1 * len(kinds), 2.1))
    for ax, kind, letter in zip(axs, kinds, "ABCD"):
        xs, ys = _panel_data(kind, rnd)
        ax.scatter(xs, ys, s=9, color=DOT)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(f"Plot {letter}", fontsize=10)
        ax.set_xlabel("x", fontsize=8); ax.set_ylabel("y", fontsize=8)
    fig.tight_layout()
    return _save(fig, path)


def time_series(labels, values, path, xlabel="time", ylabel="value", title=None, ma=None):
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    t = list(range(len(values)))
    ax.plot(t, values, color=DOT, marker="o", markersize=4, linewidth=1.4, label="data")
    if ma:
        pts = [(p, v) for p, v in ma]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=LINE, linestyle="--", marker="s", markersize=3,
                linewidth=1.4, label="moving average")
        ax.legend(fontsize=8, frameon=False)
    ax.set_xticks(t)
    ax.set_xticklabels(labels, fontsize=7, rotation=0 if len(labels) <= 8 else 45)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_ylim(0, max(values) * 1.15)
    if title:
        ax.set_title(title, fontsize=10)
    _axes(ax)
    return _save(fig, path)


# ── app wrappers: the app calls fn(*args, path_or_buffer), with the path LAST ───────────────────
def app_scatter(xs, ys, xlabel, ylabel, title, line, mark, path):
    return scatter(xs, ys, path, xlabel, ylabel, title, line=line, mark=tuple(mark) if mark else None)


def app_panels(kinds, seed, path):
    return panels(kinds, path, seed=seed)


def app_time_series(labels, values, xlabel, ylabel, title, ma, path):
    return time_series(labels, values, path, xlabel, ylabel, title, ma=ma)
