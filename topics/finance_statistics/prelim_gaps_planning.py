"""Higher Planning — levels filling the gaps found when the prelim learning outcomes were mapped to the app (Nov 2026):
comparing and converting PERT and Gantt charts; expected value of benefits and costs in a decision; the four factors a
project leader considers."""
import random

from core.models.further import gbp, md_table, part, question, r2, step
from topics.finance_statistics.further_planning_statistics import NOTES_NET, _network

NOTES_COMPARE = NOTES_NET + """
**PERT and Gantt.** Activities are **nodes** in a PERT chart and **bars** in a Gantt chart. Bar length shows duration;
arrow length in a PERT chart means nothing. A PERT chart shows **precedence** (which activities must finish first) and
makes the critical path and slack easy to find. A Gantt chart is simple to read, shows overlaps and the project length,
but does **not** show precedence.
"""
NOTES_EV = """
**Expected value = expected profit − expected cost.** Expected profit = probability of the profit × profit.
Expected cost = probability of the cost × cost. Choose the option with the **highest** expected value (or the lowest
expected cost), then think about the worst case: an expected value is a long-run average, not what happens once.
"""
NOTES_PROJECT = """
**Four factors for a project:** the **reason for initiating** it (solving a problem or improving a system); its
**feasibility** (cost-benefit analysis); **planning** the activities (what they are, how long they take, their order,
for example with PERT or Gantt charts); **controlling** the activities and the team (checking progress against the plan
and acting when something slips).
"""

_STATEMENTS = [
    ("Activities are shown as bars in a Gantt chart and as nodes in a PERT chart.", True),
    ("The length of an arrow in a PERT chart shows how long an activity takes.", False),
    ("The length of a bar in a Gantt chart shows how long an activity takes.", True),
    ("A Gantt chart on its own shows which activities must be finished before another can start.", False),
    ("The layout of a PERT chart shows the order in which activities must be done.", True),
    ("A Gantt chart makes it easy to see which activities are happening at the same time.", True),
    ("Slack time is easier to determine from a PERT chart's early and late times than from a list of tasks.", True),
    ("A critical activity has the largest float in the project.", False),
    ("The project length can be read from the end of the last bar on a Gantt chart.", True),
]


def generate_pert_gantt_compare():
    acts, es, ef, lf, fl, end, crit, non = _network()
    d = random.choice(non)
    day = random.randint(2, end - 1)
    running = sorted(a for a in acts if es[a] < day <= es[a] + acts[a][0])
    t = md_table(["Activity", "Starts after day", "Duration (days)", "Float (days)"],
                 [[a, es[a], acts[a][0], fl[a]] for a in sorted(acts)])
    p = md_table(["Activity", "Predecessors"], [[a, ", ".join(acts[a][1]) or "–"] for a in sorted(acts)])
    ctx = ("The data below were read from a **Gantt chart** drawn with every activity starting as early as possible. "
           "The Gantt chart does not show precedence, so the predecessors are given separately.\n\n" + t + "\n\n" + p)
    picked = random.sample(_STATEMENTS, 3)
    parts = [
        part("(a)", "To redraw this as a PERT chart: what is the latest finish time of activity " + d + "?", lf[d],
             [f"Latest finish = earliest start + duration + float = {es[d]} + {acts[d][0]} + {fl[d]} = **{lf[d]}**"], marks=2),
        part("(b)", f"How many activities are in progress during day {day}? (Day {day} runs from time {day - 1} to time {day}.)",
             len(running), [f"In progress: {', '.join(running)} → **{len(running)}**"], marks=1),
        part("(c)", "What is the length of the project, in days?", end, [f"The last bar ends at **{end}**"], marks=1),
    ]
    for label, (s, truth) in zip(["(d)", "(e)", "(f)"], picked):
        parts.append(part(label, f"True or false? {s}", "True" if truth else "False",
                          [f"**{'True' if truth else 'False'}**"], options=["True", "False"], marks=1))
    return question("Planning", "Networks", ctx, parts, NOTES_COMPARE, "Comparing and Converting PERT and Gantt")


_VENTURES = [
    ("A market trader", "a stall at a music festival", "a stall at a food fair"),
    ("A farmer", "a crop of strawberries", "a crop of potatoes"),
    ("A theatre company", "an outdoor show", "an indoor show"),
    ("A bakery", "a new range of cakes", "a new sandwich range"),
    ("A phone company", "launching in spring", "launching in autumn"),
]


def generate_ev_decisions():
    who, a, b = random.choice(_VENTURES)
    while True:
        pa, pb = random.choice([0.55, 0.6, 0.65, 0.7]), random.choice([0.8, 0.85, 0.9])
        ga, la = random.choice(range(5000, 12001, 500)), random.choice(range(1500, 4001, 500))
        gb, lb = random.choice(range(3000, 7001, 500)), random.choice(range(500, 1501, 250))
        ea = r2(pa * ga - (1 - pa) * la)
        eb = r2(pb * gb - (1 - pb) * lb)
        if abs(ea - eb) > 100 and ea > 0 and eb > 0 and la > lb:
            break
    ctx = (f"{who} must choose **one** of two plans.\n\n" + md_table(
        ["Plan", "Probability of success", "Profit if it succeeds", "Loss if it fails"],
        [[f"A: {a}", pa, gbp(ga), gbp(la)], [f"B: {b}", pb, gbp(gb), gbp(lb)]]))
    best = "Plan A" if ea > eb else "Plan B"
    parts = [
        part("(a)", "Find the expected value of plan A.", ea, [f"{pa} × {ga} − {r2(1 - pa)} × {la} = **{gbp(ea)}**"],
             [step("Expected profit", r2(pa * ga)), step("Expected cost", r2((1 - pa) * la))], marks=3),
        part("(b)", "Find the expected value of plan B.", eb, [f"{pb} × {gb} − {r2(1 - pb)} × {lb} = **{gbp(eb)}**"],
             [step("Expected profit", r2(pb * gb)), step("Expected cost", r2((1 - pb) * lb))], marks=2),
        part("(c)", "Which plan is better on expected value?", best, [f"**{best}** has the higher expected value"],
             options=["Plan A", "Plan B"], marks=1),
        part("(d)", "Give a reason why a cautious decision maker might choose plan B. (Reveal the expected answer.)",
             f"Plan B is more likely to succeed and its possible loss ({gbp(lb)}) is smaller than plan A's ({gbp(la)}).",
             ["B has the higher chance of success and the smaller possible loss."], explain=True, marks=1),
    ]
    return question("Planning", "Risk and Expected Value", ctx, parts, NOTES_EV, "Expected Value Decisions")


_FACTORS = ["Reason for initiating the project", "Feasibility of the project", "Planning project activities",
            "Controlling project activities and team members"]
_FACTOR_ITEMS = [
    [("The current booking system is slow and often loses orders.", 0), ("A new system would improve how customers are served.", 0)],
    [("Set-up and running costs are compared with the money the project will save.", 1), ("A cost-benefit analysis is carried out.", 1)],
    [("A PERT chart is drawn showing each task, its duration and what must come before it.", 2), ("The tasks are listed and put in order with estimated times.", 2)],
    [("A weekly meeting compares progress with the Gantt chart.", 3), ("A team member is moved to help with a task that has fallen behind.", 3)],
]


def generate_project_factors():
    items = [random.choice(group) for group in _FACTOR_ITEMS]
    random.shuffle(items)
    parts = [part(label, f"Which of the four project factors is this? “{text}”", _FACTORS[k], [f"**{_FACTORS[k]}**"],
                  options=list(_FACTORS), marks=1)
             for label, (text, k) in zip(["(a)", "(b)", "(c)", "(d)"], items)]
    return question("Planning", "Risk and Expected Value", "A company is thinking about a new project.", parts,
                    NOTES_PROJECT, "Managing a Project")


GAPS = {
    ("Planning", "Networks"): {"Comparing and Converting PERT and Gantt": generate_pert_gantt_compare},
    ("Planning", "Risk and Expected Value"): {"Expected Value Decisions": generate_ev_decisions,
                                              "Managing a Project": generate_project_factors},
}
