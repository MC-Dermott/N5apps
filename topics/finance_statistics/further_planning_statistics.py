"""Higher Planning and Statistics — further question types from the specification examples (Nov 2026):
project-software output, delays and float, cost-benefit; counts and proportions, median/IQR for skewed data,
size of an effect, reading confidence intervals."""
import math
import random

from core.models.further import g, gbp, md_table, part, question, r2, step

# ── Planning ───────────────────────────────────────────────────────────────────
_TEMPLATES = [
    {"A": [], "B": ["A"], "C": ["A"], "D": ["B"], "E": ["B", "C"], "F": ["D", "E"], "G": ["E"], "H": ["F", "G"]},
    {"A": [], "B": [], "C": ["A"], "D": ["A", "B"], "E": ["B"], "F": ["C", "D"], "G": ["D", "E"], "H": ["F", "G"]},
    {"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"], "E": ["C"], "F": ["D"], "G": ["D", "E"], "H": ["F", "G"]},
]
NOTES_NET = """
**Activity networks.** Forward scan: earliest start = the largest (earliest start + duration) of the predecessors.
Backward scan: latest finish = the smallest (latest finish − duration) of the successors.
Float (slack) = latest finish − duration − earliest start. Critical activities have float 0. Delaying an activity by more than
its float delays the whole project by the excess.
"""
NOTES_CBA = """
**Cost-benefit analysis** (feasibility): total costs = set-up + running costs over the period; total benefits = savings over the period.
A project is feasible if the benefits exceed the costs. The four factors a project leader considers: reason for initiating,
feasibility, planning the activities, controlling the activities and team.
"""


def _scans(acts):
    es, ef = {}, {}

    def E(a):
        if a not in es:
            es[a] = max([E(p) + acts[p][0] for p in acts[a][1]] or [0]); ef[a] = es[a] + acts[a][0]
        return es[a]
    for a in acts:
        E(a)
    end = max(ef.values()); succ = {a: [b for b in acts if a in acts[b][1]] for a in acts}; lf = {}

    def L(a):
        if a not in lf:
            lf[a] = min([L(b) - acts[b][0] for b in succ[a]] or [end])
        return lf[a]
    for a in acts:
        L(a)
    return es, ef, lf, {a: lf[a] - ef[a] for a in acts}, end


def _network():
    t = random.choice(_TEMPLATES)
    while True:
        acts = {a: (random.randint(2, 6), p) for a, p in t.items()}
        es, ef, lf, fl, end = _scans(acts)
        crit = [a for a in acts if fl[a] == 0]
        non = [a for a in acts if fl[a] > 0]
        if 3 <= len(crit) <= 6 and non and len({fl[a] for a in non}) >= 2:
            return acts, es, ef, lf, fl, end, crit, non


def _task_table(acts, es, ef, fl):
    return md_table(["Task", "Duration (days)", "Start (day)", "Finish (day)", "Predecessors", "Total slack (days)"],
                    [[a, acts[a][0], es[a] + 1, ef[a], ", ".join(acts[a][1]) or "–", fl[a]] for a in sorted(acts)])


def generate_software_output():
    acts, es, ef, lf, fl, end, crit, non = _network()
    d = random.choice([a for a in non]); delay = fl[d] + random.randint(1, 3)
    ctx = "A project management program gives this output (days are numbered from day 1).\n\n" + _task_table(acts, es, ef, fl)
    parts = [part("(a)", "How many days does the project take?", end, [f"The last finish day = **{end}**"], marks=1),
             part("(b)", "How many tasks are critical (zero total slack)?", len(crit), [f"Critical: {', '.join(crit)} → **{len(crit)}**"], marks=1),
             part("(c)", f"Task {d} is delayed by {delay} days. By how many days is the whole project delayed?", delay - fl[d],
                  [f"Slack of {d} = {fl[d]} days; delay beyond slack = {delay} − {fl[d]} = **{delay - fl[d]}** days"], [step(f"Slack of {d}", fl[d])], marks=2)]
    return question("Planning", "Networks", ctx, parts, NOTES_NET, "Project Software Output")


def generate_delays_and_float():
    acts, es, ef, lf, fl, end, crit, non = _network()
    c = random.choice(crit); n = random.choice(non); cost = random.choice([200, 250, 300, 400, 500]); dc = random.randint(1, 3); dn = fl[n] + random.randint(1, 3)
    rows = [[a, acts[a][0], ", ".join(acts[a][1]) or "–"] for a in sorted(acts)]
    ctx = ("The activities of a project are below. The owner is charged " + gbp(cost) + " for every day the project finishes after its planned end.\n\n"
           + md_table(["Activity", "Duration (days)", "Predecessors"], rows))
    parts = [part("(a)", "Carry out forward and backward scans. What is the minimum project time (days)?", end, [f"Forward scan gives a minimum time of **{end} days**"], marks=3),
             part("(b)", f"What is the float of activity {n}?", fl[n], [f"Latest finish − duration − earliest start = **{fl[n]}** days"], marks=2),
             part("(c)", f"Activity {n} is delayed by {dn} days. What extra cost does the owner pay?", (dn - fl[n]) * cost,
                  [f"Overrun = {dn} − {fl[n]} = {dn - fl[n]} days; cost = {dn - fl[n]} × {cost} = **{gbp((dn - fl[n]) * cost)}**"], marks=2),
             part("(d)", f"Activity {c} (critical) is delayed by {dc} days. What extra cost does the owner pay?", dc * cost,
                  [f"{c} has no float, so the project is delayed by {dc} days: {dc} × {cost} = **{gbp(dc * cost)}**"], marks=1)]
    return question("Planning", "Networks", ctx, parts, NOTES_NET, "Delays and Float")


def generate_cost_benefit():
    setup, run, save, yrs = random.choice(range(4000, 12001, 1000)), random.choice([300, 400, 500, 600]), random.choice([1800, 2200, 2600, 3000]), random.choice([4, 5, 6])
    costs, ben = setup + run * yrs, save * yrs
    ctx = f"A school plans a new booking system. It costs {gbp(setup)} to set up and {gbp(run)} a year to run, and saves staff time worth {gbp(save)} a year. Consider {yrs} years."
    parts = [part("(a)", "Find the total cost over the period.", costs, [f"{setup} + {yrs} × {run} = **{gbp(costs)}**"], marks=1),
             part("(b)", "Find the total benefit over the period.", ben, [f"{yrs} × {save} = **{gbp(ben)}**"], marks=1),
             part("(c)", "Is the project feasible on cost-benefit alone?", "Yes" if ben > costs else "No",
                  [f"Benefit {gbp(ben)} compared with cost {gbp(costs)} → **{'Yes' if ben > costs else 'No'}**"], options=["Yes", "No"], marks=1),
             part("(d)", "Name one other factor a project leader must consider.", "Reason for initiating; planning activities; controlling activities and team members",
                  ["e.g. the reason for starting the project, planning its activities, or controlling the team."], explain=True, marks=1)]
    return question("Planning", "Risk and Expected Value", ctx, parts, NOTES_CBA, "Cost-Benefit of a Project")


# ── Statistics ─────────────────────────────────────────────────────────────────
NOTES_COUNTS = """
**Counts and proportions.** Proportion = count ÷ total (a decimal or a percentage). In a spreadsheet use COUNTIF(range, "category");
in R use table() and prop.table().
"""
NOTES_SKEW = """
**Skewed data.** Mean and standard deviation are pulled by extreme values; use the **median and interquartile range**
(Q3 − Q1) for skewed numerical data, and mean and standard deviation for roughly symmetric (normal) data.
"""
NOTES_EFFECT = """
**Size of an effect.** A significant result may still be unimportant. Express the difference as a percentage of what is being
measured to decide whether it matters in context.
"""
NOTES_CI = """
**Confidence intervals** show the uncertainty in an estimate: wider = more uncertain (smaller samples), narrower = less uncertain.
A 95% interval means that if the study were repeated many times, about 95% of the intervals would contain the true value.
"""


def _q7(x, p):
    x = sorted(x); h = (len(x) - 1) * p; lo = int(h)
    return x[lo] + (h - lo) * (x[min(lo + 1, len(x) - 1)] - x[lo])


def generate_counts_proportions():
    cats = random.choice([["Football", "Netball", "Swimming", "Other"], ["Bus", "Walk", "Car", "Cycle"], ["Tea", "Coffee", "Juice", "Water"]])
    counts = [random.choice(range(6, 31, 3)) for _ in cats]; n = sum(counts); top = max(range(len(cats)), key=lambda i: counts[i])
    if counts.count(counts[top]) > 1:
        counts[top] += 3; n += 3
    ctx = f"{n} pupils chose a favourite: " + ", ".join(f"{c} {k}" for c, k in zip(cats, counts)) + "."
    i2 = random.choice([i for i in range(len(cats)) if i != top])
    parts = [part("(a)", "Which category is the most popular?", cats[top], [f"The largest count: **{cats[top]}** ({counts[top]})"], options=cats, marks=1),
             part("(b)", f"Find the proportion who chose {cats[i2]} (as a decimal to 2 d.p.).", round(counts[i2] / n, 2), [f"{counts[i2]} ÷ {n} = **{counts[i2] / n:.2f}**"], marks=1),
             part("(c)", f"What percentage chose {cats[top]} (1 d.p.)?", round(counts[top] / n * 100, 1), [f"{counts[top]} ÷ {n} × 100 = **{counts[top] / n * 100:.1f}%**"], marks=1)]
    return question("Statistics", "Data and Distributions", ctx, parts, NOTES_COUNTS, "Counts and Proportions")


def generate_median_iqr():
    base = sorted(random.randint(18, 30) for _ in range(11)); extreme = random.choice([70, 85, 95, 110]); data = sorted(base + [extreme])
    med, q1, q3 = _q7(data, .5), _q7(data, .25), _q7(data, .75); mu = sum(data) / len(data)
    ctx = "Annual salaries (£ thousands) of 12 employees: " + ", ".join(map(str, data)) + ". (Use the QUARTILE.INC / R method for quartiles.)"
    parts = [part("(a)", "Find the median (£ thousands).", med, [f"Middle two values average: **{med:g}**"], marks=1),
             part("(b)", "Find the interquartile range (£ thousands, 2 d.p.).", round(q3 - q1, 2), [f"Q1 = {q1:g}, Q3 = {q3:g}; IQR = **{q3 - q1:.2f}**"], [step("Q1", round(q1, 2)), step("Q3", round(q3, 2))], marks=2),
             part("(c)", "Which pair of measures best summarises these data?", "Median and interquartile range",
                  [f"The {extreme} makes the data skewed to the right (the mean is {mu:.1f}), so use the **median and IQR**"],
                  options=["Mean and standard deviation", "Median and interquartile range"], marks=1)]
    return question("Statistics", "Data and Distributions", ctx, parts, NOTES_SKEW, "Median and IQR for Skewed Data")


def generate_effect_size():
    kind = random.choice(["shop", "airline"])
    if kind == "shop":
        d, base, ctx_ = random.choice([60, 80, 100, 120]), random.choice([120, 150, 180]), "the difference in a weekly shop for the same products at two supermarkets"
    else:
        d, base, ctx_ = random.choice([100, 200, 500]), random.choice([1_200_000_000, 2_400_000_000, 3_600_000_000]), "the yearly fuel saving for an airline whose fuel costs the amount below"
    pct = d / base * 100
    ans = "Important" if pct >= 5 else "Negligible"
    txt = f"A two-sample t-test finds a mean difference of £{d}. This is {ctx_}" + (f" (a weekly shop of £{base})." if kind == "shop" else f" (£{base:,} a year).")
    dp = 1 if kind == "shop" else 6
    parts = [part("(a)", f"Express the difference as a percentage of the amount ({dp} d.p.).", round(pct, dp), [f"{d} ÷ {base:,} × 100 = **{pct:.{dp}f}%**"], marks=2),
             part("(b)", "Is the difference important in context?", ans, [f"{pct:.{dp}f}% of the total → **{ans}**"], options=["Important", "Negligible"], marks=1)]
    return question("Statistics", "Hypothesis Testing", txt, parts, NOTES_EFFECT, "Size of an Effect")


def generate_ci_reading():
    mu = random.choice([310, 320, 340]); s = random.choice([12, 15, 18]); n1, n2 = random.choice([(8, 80), (10, 100), (12, 120)])
    from core.models.further import g as _g
    t = {8: 2.365, 10: 2.262, 12: 2.201, 80: 1.990, 100: 1.984, 120: 1.980}
    h1, h2 = t[n1] * s / math.sqrt(n1), t[n2] * s / math.sqrt(n2)
    ctx = f"Two studies estimate a mean reaction time (ms). Study 1 (n = {n1}) gives a 95% CI of ({mu - h1:.1f}, {mu + h1:.1f}); Study 2 (n = {n2}) gives ({mu - h2:.1f}, {mu + h2:.1f})."
    parts = [part("(a)", "Which study shows less uncertainty?", "Study 2", ["The narrower interval → **Study 2**"], options=["Study 1", "Study 2"], marks=1),
             part("(b)", "Find the width of the Study 1 interval (1 d.p.).", round(2 * h1, 1), [f"{mu + h1:.1f} − {mu - h1:.1f} = **{2 * h1:.1f}**"], marks=1),
             part("(c)", "In a simulator, 100 samples are taken at the 95% level. About how many intervals would you expect NOT to contain the true mean?", 5,
                  ["About 5% of 100 = **5**"], marks=1)]
    return question("Statistics", "Hypothesis Testing", ctx, parts, NOTES_CI, "Reading Confidence Intervals")


FURTHER = {
    ("Planning", "Networks"): {"Project Software Output": generate_software_output, "Delays and Float": generate_delays_and_float},
    ("Planning", "Risk and Expected Value"): {"Cost-Benefit of a Project": generate_cost_benefit},
    ("Statistics", "Data and Distributions"): {"Counts and Proportions": generate_counts_proportions, "Median and IQR for Skewed Data": generate_median_iqr},
    ("Statistics", "Hypothesis Testing"): {"Size of an Effect": generate_effect_size, "Reading Confidence Intervals": generate_ci_reading},
}
