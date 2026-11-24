"""N5 Finance and Statistics — Comparing Data Sets.

Mirrors Comparing_Data_Sets_Worksheet.docx (N5 Apps/Worksheets/Finance and Statistics): median and
quartiles (SQA method — the median of each half, the median left out when n is odd), interquartile
range and consistency, mean and standard deviation (n − 1), and comparing the mean and standard
deviation in context. Distractors are the errors in the course reports and marking instructions:
an unordered list, the semi-interquartile range, ÷ n, no square root, and comments that use
'on average' for spread or talk about 'the data' / 'the standard deviation'.
"""
import math
import random

from core.models.distractors import distractors
from core.models.question_model import Question, make_part, multipart_worked_solution

TOPIC, QTYPE = "Finance and Statistics", "Comparing Data Sets"

NOTES_QUARTILES = """
**Median and quartiles**

1. Write the list **in order**.
2. Median = the middle value (or halfway between the middle two).
3. Lower quartile Q1 = median of the lower half; upper quartile Q3 = median of the upper half
   (when there's an odd number of values, leave the median out of both halves).

**Example (from the worksheet):** A fisherman records the number of creels he hauls each day for 12
days: 14, 22, 9, 17, 30, 12, 25, 19, 8, 21, 16, 27.
- Ordered: 8, 9, 12, 14, 16, 17, 19, 21, 22, 25, 27, 30
- Median = (17 + 19) ÷ 2 = **18**
- Q1 = (12 + 14) ÷ 2 = **13**,  Q3 = (22 + 25) ÷ 2 = **23.5**

⚠ An unordered list loses the median mark (2024 and 2025 marking instructions).
"""

NOTES_IQR = """
**Interquartile range and spread**

IQR = Q3 − Q1. The **larger** the IQR, the **more spread out** the data.

**Example (from the worksheet):** Q1 = 13 and Q3 = 23.5, so IQR = 23.5 − 13 = **10.5**. A second boat
has an IQR of 6, so *the numbers of creels hauled for the first boat are more spread out than for the second boat.*

⚠ Don't halve the IQR (that's the semi-interquartile range — 2019 course report), don't use
"on average" about spread, and say whose **what** is more spread out (2022–2025 course reports).
"""

NOTES_SD = """
**Mean and standard deviation** (formula on the formulae list)

s = √( Σ(x − x̄)² ÷ (n − 1) )

**Example (from the worksheet):** Six bags of peat weigh 24, 27, 22, 26, 25, 26 kg.
- Σx = 150, mean x̄ = 150 ÷ 6 = **25**
- x − x̄: −1, 2, −3, 1, 0, 1;  (x − x̄)²: 1, 4, 9, 1, 0, 1;  Σ(x − x̄)² = 16
- s = √(16 ÷ 5) = **1.79**

⚠ Divide by n − 1, not n, and don't forget the square root (2024 marking instructions).
"""

NOTES_COMPARE = """
**Comparing the mean and standard deviation** — one comment about each, in context.

**Example (from the worksheet):** Tarbert peat bags: mean 25 kg, s = 1.79 kg. Stornoway: mean 23.4 kg,
s = 2.6 kg.
- *On average, the weight of the Tarbert bags is bigger than the weight of the Stornoway bags.*
- *The weight of the Stornoway bags is more spread out than the weight of the Tarbert bags.*

⚠ "On average … more spread out" gets no mark, and neither does "the standard deviation is more spread
out" or "the data is more spread out" — say whose **what** (every course report 2018–2026). You don't need to
quote the numbers.
"""

NOTES_LINE = """
**Line graphs** — show how something changes over time.

- **Reading a value:** go up from the label to the line, then across to the scale. Work out what **one small
  square** is worth first.
- **Increase or decrease:** subtract the earlier value from the later one.
- **Drawing one:** choose a scale for each axis, label both axes, plot each point as a small cross and join
  the points with a ruler.

**Example (from the worksheet):** the number of visitors to the Stornoway museum each month: January 120,
February 150, March 210, April 280, May 340, June 310. Months go along the bottom and visitors up the side,
0 to 400 in steps of 50; plot each point, then join them with a ruler.
"""

NOTES_SCATTER = """
**Scatter graphs** — each pair of values is one **cross**; the points are **not joined**.

- **Correlation:** *positive* (both go up together), *negative* (one goes up as the other goes down) or *none*.
- **Line of best fit:** a straight, ruled line through the middle of the points, with points above **and** below it,
  across the full range of the data (not through the origin). To **estimate**, go up from the given value to the
  line, then across to the scale.
- An estimate **outside the range of the data** is less reliable.

**Example (from the worksheet):** temperature (°C) and ice creams sold: (12, 35), (14, 45), (15, 46), (17, 57),
(18, 56), (20, 72), (22, 74), (24, 88). Positive correlation; at 19 °C the line gives about 64 ice creams.
"""

# (x label, y label, x range, a, b) with y = a + b x on the line of best fit (integers, so estimates are exact)
_SCATTER_CONTEXTS = [
    ("Temperature (°C)", "Ice creams sold", (10, 26), -10, 4, "temperature", "ice creams sold"),
    ("Distance (miles)", "Time (minutes)", (3, 24), 5, 3, "distance", "time"),
    ("Age of car (years)", "Value (£ hundreds)", (1, 9), 100, -9, "age", "value"),
    ("Hours of revision", "Test score", (1, 9), 25, 7, "hours of revision", "test score"),
    ("Hours of sunshine", "Visitors", (2, 10), 10, 11, "hours of sunshine", "visitors"),
]

_LINE_CONTEXTS = [
    ("the number of cars on the Leverburgh ferry each day", "Number of cars", "Day", "cars",
     ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "day"),
    ("the number of visitors to the Stornoway museum each month", "Number of visitors", "Month", "visitors",
     ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "month"),
    ("the number of passengers on the Barra ferry each month", "Number of passengers", "Month", "passengers",
     ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "month"),
]

_LISTS = [
    ("the number of creels hauled each day", "creels"),
    ("the number of cars on each ferry sailing", "cars"),
    ("the number of lambs born on each croft", "lambs"),
    ("the number of visitors to a museum each day", "visitors"),
    ("the time, in minutes, of each walk to school", "minutes"),
    ("the number of scones sold each day", "scones"),
]


def _median(xs):
    xs = sorted(xs); n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def _quartiles(xs):
    xs = sorted(xs); n = len(xs)
    return _median(xs[:n // 2]), _median(xs), _median(xs[(n + 1) // 2:])


def _fmt(x):
    return f"{x:g}"


def _data(n):
    base = random.randint(10, 40)
    return [base + random.randint(-9, 20) for _ in range(n)]


def generate_comparing_l1(calc_mode=False):
    """Median and quartiles (non-calculator)."""
    what, unit = random.choice(_LISTS)
    n = random.choice([8, 10, 11, 12, 13])
    xs = _data(n)
    q1, md, q3 = _quartiles(xs)
    ordered = sorted(xs)
    data = ", ".join(map(str, xs))
    unordered_median = (xs[n // 2 - 1] + xs[n // 2]) / 2 if n % 2 == 0 else xs[n // 2]
    parts = [
        make_part("(a)", "Calculate the median.", md,
                  scaffold_steps=[{"prompt": "How many values are there?", "answer": n}],
                  worked_solution=[f"Ordered: {', '.join(map(str, ordered))}", f"Median = {_fmt(md)}"],
                  distractors=distractors(md, [(unordered_median, "you didn't put the list in order first — "
                                                                  "an unordered list loses the mark (marking "
                                                                  "instructions).")])),
        make_part("(b)", "Calculate the lower quartile.", q1,
                  worked_solution=[f"Lower half: {', '.join(map(str, ordered[:n // 2]))}", f"Q1 = {_fmt(q1)}"]),
        make_part("(c)", "Calculate the upper quartile.", q3,
                  worked_solution=[f"Upper half: {', '.join(map(str, ordered[(n + 1) // 2:]))}", f"Q3 = {_fmt(q3)}"]),
    ]
    return Question(question_text=f"The data shows {what}:\n\n**{data}**", correct_answer=md, topic=TOPIC,
                    question_type=QTYPE, parts=parts, worked_solution=multipart_worked_solution(parts),
                    notes=NOTES_QUARTILES)


def generate_comparing_l2(calc_mode=False):
    """IQR and a comment on which data set is more spread out."""
    names = random.sample(["Iona", "Calum", "Mairi", "Ruaridh", "Eilidh", "Finlay", "Kirsty", "Lewis"], 2)
    what, unit = random.choice(_LISTS)
    n = random.choice([8, 10, 12])
    xs = _data(n)
    q1, _, q3 = _quartiles(xs)
    iqr = q3 - q1
    other = max(1, round(iqr + random.choice([-1, 1]) * random.choice([2, 3, 4, 5])))
    if other == iqr:
        other += 2
    big, small = (names[0], names[1]) if iqr > other else (names[1], names[0])
    right = f"{big}'s {unit} are more spread out than {small}'s {unit}."
    options = [right,
               f"On average, {big}'s {unit} are more spread out than {small}'s {unit}.",
               f"The interquartile range of {big} is more spread out than {small}'s.",
               f"{small}'s {unit} are more spread out than {big}'s {unit}."]
    random.shuffle(options)
    parts = [
        make_part("(a)", f"Calculate the interquartile range for {names[0]}'s data.", iqr,
                  scaffold_steps=[{"prompt": "Q1", "answer": q1}, {"prompt": "Q3", "answer": q3}],
                  worked_solution=[f"Q1 = {_fmt(q1)}, Q3 = {_fmt(q3)}", f"IQR = {_fmt(q3)} − {_fmt(q1)} = {_fmt(iqr)}"],
                  distractors=distractors(iqr, [(iqr / 2, "that's the semi-interquartile range — don't halve "
                                                          "it (2019 course report; 2024 and 2025 marking "
                                                          "instructions).")])),
        make_part("(b)", f"{names[1]}'s {unit} have an interquartile range of {other}. Which comment about the spread is valid?",
                  right, options=options,
                  worked_solution=[f"{_fmt(iqr)} vs {other}: the larger IQR is more spread out.", right],
                  distractors=[{"value": o, "mistake": m} for o, m in [
                      (options[options.index(f"On average, {big}'s {unit} are more spread out than {small}'s {unit}.")],
                       "'on average' is for the mean or median, not for the spread (course reports "
                       "2022–2025)."),
                      (options[options.index(f"The interquartile range of {big} is more spread out than {small}'s.")],
                       "the comment must be about the " + unit + ", not the IQR (marking instructions)."),
                  ]]),
    ]
    return Question(question_text=f"{names[0]} recorded {what}:\n\n**{', '.join(map(str, xs))}**",
                    correct_answer=iqr, topic=TOPIC, question_type=QTYPE, parts=parts,
                    worked_solution=multipart_worked_solution(parts), notes=NOTES_IQR)


def generate_comparing_l3(calc_mode=False):
    """Mean and standard deviation (calculator)."""
    what, unit = random.choice(_LISTS)
    n = random.choice([5, 6, 7])
    for _ in range(200):
        xs = _data(n)
        if sum(xs) % n == 0:
            break
    mu = sum(xs) / n
    ss = sum((x - mu) ** 2 for x in xs)
    sd = round(math.sqrt(ss / (n - 1)), 2)
    parts = [
        make_part("(a)", "Calculate the mean.", round(mu, 2),
                  worked_solution=[f"Mean = {sum(xs)} ÷ {n} = {_fmt(round(mu, 2))}"]),
        make_part("(b)", "Calculate the standard deviation, to 2 decimal places.", sd,
                  scaffold_steps=[{"prompt": "Σ(x − x̄)²", "answer": round(ss, 2)},
                                  {"prompt": f"Divide by n − 1 = {n - 1}", "answer": round(ss / (n - 1), 2)}],
                  worked_solution=[f"(x − x̄)²: {', '.join(_fmt(round((x - mu) ** 2, 2)) for x in xs)}",
                                   f"Σ(x − x̄)² = {_fmt(round(ss, 2))}",
                                   f"s = √({_fmt(round(ss, 2))} ÷ {n - 1}) = {sd}"],
                  distractors=distractors(sd, [
                      (round(math.sqrt(ss / n), 2), f"you divided by n = {n} — divide by n − 1 = {n - 1} "
                                                    f"(2024 marking instructions)."),
                      (round(ss / (n - 1), 2), "you forgot the square root (2024 marking instructions)."),
                      (round(math.sqrt(ss) / (n - 1), 2), "you took the square root before dividing — the "
                                                          "square root goes over the whole fraction."),
                  ])),
    ]
    return Question(question_text=f"The data shows {what}:\n\n**{', '.join(map(str, xs))}**",
                    correct_answer=sd, topic=TOPIC, question_type=QTYPE, parts=parts,
                    worked_solution=multipart_worked_solution(parts), notes=NOTES_SD)


_PAIRS = [
    ("the Tarbert bags", "the Stornoway bags", "weights", "kg", "heavier", "lighter"),
    ("Crofter A's lambs", "Crofter B's lambs", "weights", "kg", "heavier", "lighter"),
    ("Callanish", "the Blackhouse Village", "numbers of visitors", "", "higher", "lower"),
    ("Ullapool", "Oban", "crossing times", "minutes", "longer", "shorter"),
]


def generate_comparing_l4(calc_mode=False):
    """Two valid comparisons of mean and standard deviation (choose the valid comments)."""
    a, b, what, u, up, down = random.choice(_PAIRS)
    ma, mb = round(random.uniform(20, 60), 1), None
    mb = round(ma + random.choice([-1, 1]) * random.uniform(1.5, 8), 1)
    sa = round(random.uniform(1, 6), 2)
    sb = round(sa + random.choice([-1, 1]) * random.uniform(0.8, 4), 2)
    sb = max(sb, 0.5)
    hi, lo = (a, b) if ma > mb else (b, a)
    cons = a if sa > sb else b          # the data set that is MORE spread out
    other = b if cons == a else a
    mean_right = f"On average, the {what} for {hi} are bigger than for {lo}."
    mean_opts = [mean_right, f"On average, the {what} for {lo} are bigger than for {hi}.",
                 f"The mean for {hi} was higher.", f"On average, the {what} for {hi} are more spread out."]
    sd_right = f"The {what} for {cons} are more spread out than for {other}."
    sd_opts = [sd_right, f"On average, the {what} for {cons} are more spread out than for {other}.",
               f"The standard deviation for {cons} is more spread out.", f"The data for {cons} is more spread out."]
    random.shuffle(mean_opts); random.shuffle(sd_opts)
    unit = f" {u}" if u else ""
    parts = [
        make_part("(a)", "Which is a valid comment about the mean?", mean_right, options=mean_opts,
                  worked_solution=[mean_right],
                  distractors=[{"value": f"The mean for {hi} was higher.", "mistake": "say what the mean is "
                                "telling you, in context — 'the mean was higher' isn't accepted (2024 marking "
                                "instructions)."},
                               {"value": f"On average, the {what} for {hi} are more spread out.",
                                "mistake": "'more spread out' is about the spread, not the average (course reports "
                                           "2018–2026)."}]),
        make_part("(b)", "Which is a valid comment about the standard deviation?", sd_right, options=sd_opts,
                  worked_solution=[sd_right],
                  distractors=[{"value": f"On average, the {what} for {cons} are more spread out than for {other}.",
                                "mistake": "'on average' is for the mean, not the spread (course reports "
                                           "2018–2026)."},
                               {"value": f"The standard deviation for {cons} is more spread out.",
                                "mistake": "the comment must be about the " + what + ", not the standard "
                                           "deviation (2024 marking instructions)."},
                               {"value": f"The data for {cons} is more spread out.",
                                "mistake": "say what the data is — 'the data' isn't in context (2019 and 2025 "
                                           "course reports)."}]),
    ]
    text = (f"{b[0].upper() + b[1:]}: mean {mb}{unit}, standard deviation {sb}{unit}.\n\n"
            f"{a[0].upper() + a[1:]}: mean {ma}{unit}, standard deviation {sa}{unit}.")
    return Question(question_text=text, correct_answer=mean_right, topic=TOPIC, question_type=QTYPE,
                    parts=parts, worked_solution=multipart_worked_solution(parts), notes=NOTES_COMPARE)


def _line_data(n):
    """n values, multiples of 5, one clear maximum, at least one rise (every graph has an increase to ask about)."""
    while True:
        v = [random.randrange(15, 71, 5)]
        for _ in range(n - 1):
            v.append(min(max(v[-1] + random.choice([-20, -15, -10, -5, 5, 10, 15, 20, 25]), 10), 90))
        if v.count(max(v)) == 1 and any(b > a for a, b in zip(v, v[1:])) and max(v) - min(v) >= 25:
            return v


def generate_comparing_l5(calc_mode=False):
    """Reading a line graph: a value, an increase and the peak (the worksheet's Section 6)."""
    what, ylabel, xlabel, unit, labels, noun = random.choice(_LINE_CONTEXTS)
    n = len(labels)
    vals = _line_data(n)
    ymax = (max(vals) // 10) * 10 + 20
    i = random.randrange(n)
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if vals[b] > vals[a] and b - a >= 2]
    a, b = random.choice(pairs or [(x, y) for x in range(n) for y in range(x + 1, n) if vals[y] > vals[x]])
    peak = labels[vals.index(max(vals))]
    diff = vals[b] - vals[a]
    parts = [
        make_part("(a)", f"Write down the {ylabel.lower()} on {labels[i]}." if noun == "day" else
                  f"Write down the {ylabel.lower()} in {labels[i]}.", vals[i],
                  scaffold_steps=[{"prompt": "What is one small square worth on the vertical scale?", "answer": 5}],
                  worked_solution=[f"Go up from {labels[i]} to the line, then across to the scale: {vals[i]}."]),
        make_part("(b)", f"Calculate the increase in the {ylabel.lower().replace('number of ', 'number of ')} "
                         f"from {labels[a]} to {labels[b]}.", diff,
                  scaffold_steps=[{"prompt": f"Value on {labels[a]}", "answer": vals[a]},
                                  {"prompt": f"Value on {labels[b]}", "answer": vals[b]}],
                  worked_solution=[f"{vals[b]} − {vals[a]} = {diff}"],
                  distractors=distractors(diff, [(vals[b], "you read the later value instead of subtracting "
                                                           "the earlier one from it.")])),
        make_part("(c)", f"On which {noun} was the {ylabel.lower()} greatest?", peak, options=labels,
                  worked_solution=[f"The highest point on the graph is {labels[vals.index(max(vals))]} "
                                   f"({max(vals)})."]),
    ]
    q = Question(question_text=f"The graph shows {what}.", correct_answer=vals[i], topic=TOPIC,
                 question_type=QTYPE, parts=parts, worked_solution=multipart_worked_solution(parts),
                 notes=NOTES_LINE)
    q.metadata["diagram"] = "composite_shape"
    q.metadata["diagram_params"] = {"module_path": "topics.finance_statistics.comparing_data_diagrams",
                                    "kind": "line_graph", "args": [labels, vals, ymax, ylabel, xlabel],
                                    "width": 520}
    return q


def generate_comparing_l6(calc_mode=False):
    """Scattergraph with its line of best fit drawn: correlation, an estimate, and reliability (2025 P1 Q4, 2026 P1 Q8)."""
    xl, yl, (lo, hi), a, b, xn, yn = random.choice(_SCATTER_CONTEXTS)
    n = min(random.choice([8, 9, 10]), hi - lo - 1)     # leave at least one x free for the estimate
    xs = sorted(random.sample(range(lo, hi + 1), n))
    while True:
        ys = [a + b * x + random.choice([-4, -3, -2, 2, 3, 4]) * max(1, abs(b) // 3) // 1 for x in xs]
        res = [y - (a + b * x) for x, y in zip(xs, ys)]
        r = sum((x - sum(xs) / n) * (y - sum(ys) / n) for x, y in zip(xs, ys)) / math.sqrt(
            sum((x - sum(xs) / n) ** 2 for x in xs) * sum((y - sum(ys) / n) ** 2 for y in ys))
        if sum(v > 0 for v in res) >= 3 and sum(v < 0 for v in res) >= 3 and min(ys) > 0 and abs(r) > 0.95:
            break
    ymax = ((max(ys + [a + b * xs[0], a + b * xs[-1]]) // 10) + 2) * 10
    xmax = hi + 2
    inside = range(min(xs) + 1, max(xs))                     # inside the range of the data
    xe_options = [x for x in inside if x not in xs and (a + b * x) % 5 == 0] or \
                 [x for x in inside if (a + b * x) % 5 == 0]
    if not xe_options:                                       # rare: re-roll the data
        return generate_comparing_l6(calc_mode)
    xe = random.choice(xe_options)
    ye = a + b * xe
    positive = b > 0
    far = max(xs) + random.choice([5, 7, 9])
    corr_opts = ["Positive correlation", "Negative correlation", "No correlation"]
    corr = corr_opts[0] if positive else corr_opts[1]
    rel_right = "Less reliable: the value is outside the range of the data."
    rel_opts = [rel_right, "Just as reliable: the line goes through every point.",
                "Not possible: a line of best fit cannot be used to estimate.",
                "More reliable: it is a long way from the other points."]
    random.shuffle(rel_opts)
    parts = [
        make_part("(a)", "Describe the correlation.", corr, options=corr_opts,
                  worked_solution=[f"As the {xn} {'increases' if positive else 'increases'}, the {yn} "
                                   f"{'increases' if positive else 'decreases'}: {corr.lower()}."]),
        make_part("(b)", f"Use the line of best fit to estimate the {yn} when the {xn} is {xe}.", ye,
                  scaffold_steps=[{"prompt": "What is one small square worth on the vertical scale?", "answer": 5}],
                  worked_solution=[f"Go up from {xe} to the line, then across to the scale: {ye}."]),
        make_part("(c)", f"A pupil uses the line to estimate the {yn} when the {xn} is {far}. Which statement is correct?",
                  rel_right, options=rel_opts,
                  worked_solution=[rel_right + f" The data only goes up to {max(xs)}."]),
    ]
    q = Question(question_text=f"The scattergraph shows {xn} and {yn}, with a line of best fit drawn.",
                 correct_answer=corr, topic=TOPIC, question_type=QTYPE, parts=parts,
                 worked_solution=multipart_worked_solution(parts), notes=NOTES_SCATTER)
    q.metadata["diagram"] = "composite_shape"
    q.metadata["diagram_params"] = {"module_path": "topics.finance_statistics.comparing_data_diagrams",
                                    "kind": "scatter_graph",
                                    "args": [xs, ys, (0, xmax, 1, 2 if xmax <= 14 else 4), (0, ymax, 5, 10), xl, yl, (a, b)],
                                    "width": 560}
    return q


def generate_comparing_question(calc_mode=False):
    return random.choice([generate_comparing_l1, generate_comparing_l2, generate_comparing_l3,
                          generate_comparing_l4, generate_comparing_l5, generate_comparing_l6])(calc_mode=calc_mode)
