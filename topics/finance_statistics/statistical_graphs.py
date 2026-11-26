"""N5 — Statistical Graphs: bar charts (comparative and compound), conversion graphs and stem-and-leaf diagrams.

Covers the course specification's "extracting and interpreting data from different graphical forms" (charts
where the scale is not obvious, comparative/compound bar charts, conversion line graphs, stem and leaf).
"""
import random

from core.models.distractors import distractors
from core.models.question_model import Question, make_part, multipart_worked_solution

TOPIC, QTYPE = "Finance and Statistics", "Statistical Graphs"
_DIAG = "topics.finance_statistics.statistical_graphs_diagrams"

NOTES_BARS = """
**Comparative bar charts** — two bars side by side for each category.

1. Work out what **one small square** is worth before reading anything.
2. Read each bar you need, then add, subtract or compare.

**Example:** The scale is labelled every 10 and each labelled gap has 5 small squares, so one small square is
10 ÷ 5 = **2**. A bar ending three squares above 20 shows 20 + 3 × 2 = **26**.
"""

NOTES_STACKED = """
**Compound (stacked) bar charts** — each bar is split into parts.

A part's value = **top of the part − bottom of the part**.

**Example:** In one bar the Adult part goes from 0 to 24 and the Child part from 24 to 40.
- Adults = 24, children = 40 − 24 = **16**
- Adults : children = 24 : 16 = **3 : 2**

⚠ **Common error:** reading the height of the top of an upper part as its value.
"""

NOTES_CONVERSION = """
**Conversion graphs** — go from the value you know to the line, then across (or down) to the other scale.

For a value **bigger than the graph shows**, read a smaller value and multiply it up.

**Example:** The graph shows 50 miles = 80 km. For 300 miles: 300 ÷ 50 = 6, so 6 × 80 = **480 km**.
"""

NOTES_STEM = """
**Stem-and-leaf diagrams** — the stem is the tens digit and the leaf is the units digit. The leaves are in
**order**, there is a **key**, and **n** (the number of values) can be found by counting the leaves.

**Example:** 1 | 4 7 9 &nbsp; 2 | 0 3 3 8 &nbsp; 3 | 1 5 &nbsp; (key: 1 | 4 = 14)
- n = 9, so the median is the 5th value = **23**
- Mode = **23**, range = 35 − 14 = **21**
"""

_BAR_CONTEXTS = [
    ("the number of tickets sold by a cinema", "Number of tickets", "Day", ["Mon", "Tue", "Wed", "Thu", "Fri"],
     ["Adult", "Child"], "tickets"),
    ("the number of books borrowed from a library", "Number of books", "Month", ["Jan", "Feb", "Mar", "Apr", "May"],
     ["Fiction", "Non-fiction"], "books"),
    ("the number of bikes hired from two hire shops", "Number of bikes", "Month", ["May", "Jun", "Jul", "Aug"],
     ["Shop A", "Shop B"], "bikes"),
    ("the number of club members at a sports centre", "Number of members", "Year", ["2022", "2023", "2024", "2025"],
     ["Junior", "Senior"], "members"),
]


def _chart(kind, args, width=520):
    return {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DIAG, "kind": kind, "args": args, "width": width}}


def generate_statistical_graphs_l1(calc_mode=False):
    """Comparative bar chart: what one square is worth, a total and a difference."""
    what, ylabel, xlabel, cats, names, unit = random.choice(_BAR_CONTEXTS)
    while True:
        s1 = [random.randrange(8, 62, 2) for _ in cats]
        s2 = [random.randrange(8, 62, 2) for _ in cats]
        i = random.randrange(len(cats))
        if abs(s1[i] - s2[i]) >= 6 and any(v % 10 for v in s1):
            break
    ymax = (max(s1 + s2) // 10 + 1) * 10
    total = sum(s1)
    diff = abs(s1[i] - s2[i])
    parts = [
        make_part("(a)", "What is one small square worth on the vertical scale?", 2,
                  worked_solution=["5 small squares between labels 10 apart: 10 ÷ 5 = 2"]),
        make_part("(b)", f"Find the difference between the {names[0]} and {names[1]} {unit} for {cats[i]}.", diff,
                  scaffold_steps=[{"prompt": f"{names[0]} for {cats[i]}", "answer": s1[i]},
                                  {"prompt": f"{names[1]} for {cats[i]}", "answer": s2[i]}],
                  worked_solution=[f"{max(s1[i], s2[i])} − {min(s1[i], s2[i])} = {diff}"],
                  distractors=distractors(diff, [(diff // 2, "that counts each small square as 1 — each is worth 2.")])),
        make_part("(c)", f"Calculate the total number of {names[0]} {unit} shown.", total,
                  worked_solution=[" + ".join(map(str, s1)) + f" = {total}"],
                  distractors=distractors(total, [(sum(s2), f"you added the {names[1]} bars.")])),
    ]
    q = Question(question_text=f"The comparative bar chart shows {what}.", correct_answer=total, topic=TOPIC,
                 question_type=QTYPE, parts=parts, worked_solution=multipart_worked_solution(parts), notes=NOTES_BARS)
    q.metadata.update(_chart("bars", [cats, [s1, s2], names, False, ymax, 10, 2, ylabel, xlabel], 580))
    return q


def generate_statistical_graphs_l2(calc_mode=False):
    """Compound bar chart, then a ratio (simplest form) or a percentage."""
    what, ylabel, xlabel, cats, names, unit = random.choice(_BAR_CONTEXTS)
    from math import gcd
    while True:
        s1 = [random.randrange(10, 42, 2) for _ in cats]
        s2 = [random.randrange(6, 32, 2) for _ in cats]
        i = random.randrange(len(cats))
        a, b = s1[i], s2[i]
        g = gcd(a, b)
        if a != b and g >= 4 and a // g <= 9 and b // g <= 9:
            break
    ymax = (max(x + y for x, y in zip(s1, s2)) // 10 + 1) * 10
    right = f"{a // g} : {b // g}"
    wrong = [(f"{b // g} : {a // g}", f"the order matters — {names[0]} comes first."),
             (f"{a // g} : {(a + b) // g}", f"that uses the height of the whole bar. The {names[1]} part is "
                                            f"top − bottom = {a + b} − {a}."),
             (f"{a} : {b}", "simplify the ratio fully.")]
    opts, seen = [right], {right}
    for v, _ in wrong:
        if v not in seen:
            opts.append(v)
            seen.add(v)
    random.shuffle(opts)
    pc = round(b / (a + b) * 100, 1)
    parts = [
        make_part("(a)", f"How many {names[1]} {unit} are shown for {cats[i]}?", b,
                  scaffold_steps=[{"prompt": f"Top of the {cats[i]} bar", "answer": a + b},
                                  {"prompt": f"Top of the {names[0]} part", "answer": a}],
                  worked_solution=[f"{a + b} − {a} = {b}"],
                  distractors=distractors(b, [(a + b, "that's the height of the whole bar — subtract the part below.")])),
        make_part("(b)", f"Write the ratio of {names[0]} to {names[1]} {unit} for {cats[i]} in its simplest form.",
                  right, options=opts, worked_solution=[f"{a} : {b} = {right} (dividing by {g})"],
                  distractors=[{"value": v, "mistake": m} for v, m in wrong if v != right]),
        make_part("(c)", f"What percentage of the {unit} for {cats[i]} were {names[1]}? Give your answer to "
                         f"1 decimal place.", pc,
                  worked_solution=[f"{b} ÷ {a + b} × 100 = {pc}%"],
                  distractors=distractors(pc, [(round(b / a * 100, 1),
                                                f"divide by the total, {a + b}, not by the other part.")])),
    ]
    q = Question(question_text=f"The compound bar chart shows {what}.", correct_answer=b, topic=TOPIC,
                 question_type=QTYPE, parts=parts, worked_solution=multipart_worked_solution(parts),
                 notes=NOTES_STACKED)
    q.metadata.update(_chart("bars", [cats, [s1, s2], names, True, ymax, 10, 2, ylabel, xlabel], 580))
    return q


# (x label, y label, y per x, x max, x major, x minor, y major, y minor, x unit, y unit)
_CONVERSIONS = [
    ("Miles", "Kilometres", 1.6, 50, 10, 2.5, 16, 4, "miles", "km"),
    ("Pounds (£)", "Euros (€)", 1.2, 100, 20, 5, 24, 6, "pounds", "euros"),
    ("Gallons", "Litres", 4.5, 20, 4, 1, 18, 4.5, "gallons", "litres"),
    ("Kilograms", "Pounds (lb)", 2.2, 50, 10, 2.5, 22, 5.5, "kg", "lb"),
]


def generate_statistical_graphs_l3(calc_mode=False):
    """Conversion graph: read both ways, then scale up beyond the graph."""
    xl, yl, rate, xmax, xmaj, xmin, ymaj, ymin, xu, yu = random.choice(_CONVERSIONS)
    k1, k2 = random.sample([k for k in range(1, 5)], 2)      # grid points on both scales
    x1, x2 = k1 * xmaj, k2 * xmaj
    y1, y2 = round(rate * x1, 2), round(rate * x2, 2)
    factor = random.randint(6, 15)
    big = x1 * factor
    big_y = round(y1 * factor, 2)
    parts = [
        make_part("(a)", f"Use the graph to change {x1:g} {xu} into {yu}.", y1,
                  worked_solution=[f"Up from {x1:g} to the line, then across: {y1:g} {yu}"]),
        make_part("(b)", f"Use the graph to change {y2:g} {yu} into {xu}.", x2,
                  worked_solution=[f"Across from {y2:g} to the line, then down: {x2:g} {xu}"]),
        make_part("(c)", f"Change {big:g} {xu} into {yu}.", big_y,
                  scaffold_steps=[{"prompt": f"How many lots of {x1:g} {xu} are in {big:g} {xu}?", "answer": factor},
                                  {"prompt": f"{y1:g} {yu} × that number", "answer": big_y}],
                  worked_solution=[f"{big:g} ÷ {x1:g} = {factor}", f"{factor} × {y1:g} = {big_y:g} {yu}"],
                  distractors=distractors(big_y, [(round(big / rate, 2), "you converted in the wrong direction.")])),
    ]
    q = Question(question_text=f"The graph converts between {xu} and {yu}.", correct_answer=big_y, topic=TOPIC,
                 question_type=QTYPE, parts=parts, worked_solution=multipart_worked_solution(parts),
                 notes=NOTES_CONVERSION)
    q.metadata.update(_chart("conversion", [xmax, rate, xmaj, xmin, ymaj, ymin, xl, yl]))
    return q


_STEM_CONTEXTS = [("the ages of the people in a walking group", "years"),
                  ("the times taken to finish a puzzle", "minutes"),
                  ("the marks scored in a test", "marks"),
                  ("the number of customers in a café each day", "customers")]


def generate_statistical_graphs_l4(calc_mode=False):
    """Stem-and-leaf diagram: n, mode, median, range and a probability."""
    what, unit = random.choice(_STEM_CONTEXTS)
    while True:
        n = random.choice([11, 13, 15])
        xs = sorted(random.randint(12, 58) for _ in range(n))
        counts = {v: xs.count(v) for v in xs}
        top = max(counts.values())
        modes = [v for v, c in counts.items() if c == top]
        limit = random.choice([30, 40])
        above = sum(v > limit for v in xs)
        if top >= 2 and len(modes) == 1 and len({v // 10 for v in xs}) == 5 and 0 < above < n:
            break
    mode, med, rng = modes[0], xs[n // 2], xs[-1] - xs[0]
    rows = [f"{s} | " + " ".join(str(v % 10) for v in xs if v // 10 == s) for s in range(1, 6)]
    block = "```\n" + "\n".join(rows) + f"\n\nKey: 2 | 5 = 25 {unit}\n```"
    from math import gcd
    g = gcd(above, n)
    prob = f"{above // g}/{n // g}"
    parts = [
        make_part("(a)", "Write down the mode.", mode,
                  worked_solution=[f"The value that appears most often is {mode}."],
                  distractors=distractors(mode, [(mode % 10, "give the whole value (stem and leaf), not just the leaf.")])),
        make_part("(b)", "Find the median.", med,
                  scaffold_steps=[{"prompt": "How many values (leaves) are there?", "answer": n}],
                  worked_solution=[f"n = {n}, so the median is value number {n // 2 + 1}: {med}"],
                  distractors=distractors(med, [(med % 10, "give the whole value (stem and leaf), not just the leaf.")])),
        make_part("(c)", "Find the range.", rng, worked_solution=[f"{xs[-1]} − {xs[0]} = {rng}"]),
        make_part("(d)", f"One value is chosen at random. What is the probability that it is more than {limit}? "
                         f"Give a fraction in its simplest form.", prob,
                  worked_solution=[f"{above} values out of {n} are more than {limit}: {prob}"]),
    ]
    return Question(question_text=f"The stem-and-leaf diagram shows {what}.\n\n{block}", correct_answer=med,
                    topic=TOPIC, question_type=QTYPE, parts=parts,
                    worked_solution=multipart_worked_solution(parts), notes=NOTES_STEM)


def generate_statistical_graphs_question(calc_mode=False):
    return random.choice([generate_statistical_graphs_l1, generate_statistical_graphs_l2,
                          generate_statistical_graphs_l3, generate_statistical_graphs_l4])(calc_mode=calc_mode)
