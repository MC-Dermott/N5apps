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
**Interquartile range and consistency**

IQR = Q3 − Q1. The **smaller** the IQR, the **more consistent** the data.

**Example (from the worksheet):** Q1 = 13 and Q3 = 23.5, so IQR = 23.5 − 13 = **10.5**. A second boat
has an IQR of 6, so *the numbers of creels hauled by the second boat were more consistent.*

⚠ Don't halve the IQR (that's the semi-interquartile range — 2019 course report), don't use
"on average" about spread, and say whose **what** is more consistent (2022–2025 course reports).
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
- *On average, the bags from Tarbert were heavier.*
- *The weights of the Tarbert bags were more consistent.*

⚠ "On average … more varied" gets no mark, and so does "the standard deviation was more consistent"
or "the data is more varied" — every course report 2018–2026. You don't need to quote the numbers.
"""

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
    """IQR and a comment on consistency."""
    names = random.sample(["Iona", "Calum", "Mairi", "Ruaridh", "Eilidh", "Finlay", "Kirsty", "Lewis"], 2)
    what, unit = random.choice(_LISTS)
    n = random.choice([8, 10, 12])
    xs = _data(n)
    q1, _, q3 = _quartiles(xs)
    iqr = q3 - q1
    other = max(1, round(iqr + random.choice([-1, 1]) * random.choice([2, 3, 4, 5])))
    if other == iqr:
        other += 2
    more = names[1] if other < iqr else names[0]
    right = f"{more}'s {unit} were more consistent."
    options = [right,
               f"On average, {more}'s {unit} were more consistent.",
               f"{more}'s interquartile range was more consistent.",
               f"{names[0] if more == names[1] else names[1]}'s {unit} were more consistent."]
    random.shuffle(options)
    parts = [
        make_part("(a)", f"Calculate the interquartile range for {names[0]}'s data.", iqr,
                  scaffold_steps=[{"prompt": "Q1", "answer": q1}, {"prompt": "Q3", "answer": q3}],
                  worked_solution=[f"Q1 = {_fmt(q1)}, Q3 = {_fmt(q3)}", f"IQR = {_fmt(q3)} − {_fmt(q1)} = {_fmt(iqr)}"],
                  distractors=distractors(iqr, [(iqr / 2, "that's the semi-interquartile range — don't halve "
                                                          "it (2019 course report; 2024 and 2025 marking "
                                                          "instructions).")])),
        make_part("(b)", f"{names[1]}'s {unit} have an interquartile range of {other}. Which comment is valid?",
                  right, options=options,
                  worked_solution=[f"{_fmt(iqr)} vs {other}: the smaller IQR is more consistent.", right],
                  distractors=[{"value": o, "mistake": m} for o, m in [
                      (options[options.index(f"On average, {more}'s {unit} were more consistent.")],
                       "'on average' is for the mean or median, not for consistency (course reports "
                       "2022–2025)."),
                      (options[options.index(f"{more}'s interquartile range was more consistent.")],
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
    ("peat bags from Tarbert", "peat bags from Stornoway", "weights of the bags", "kg", "heavier", "lighter"),
    ("lambs on Crofter A's croft", "lambs on Crofter B's croft", "lambs' weights", "kg", "heavier", "lighter"),
    ("visitors to Callanish", "visitors to the Blackhouse Village", "numbers of visitors", "", "higher", "lower"),
    ("crossings from Ullapool", "crossings from Oban", "crossing times", "minutes", "longer", "shorter"),
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
    cons = a if sa < sb else b
    other = b if cons == a else a
    mean_right = f"On average, the {what} for {hi} were {up} than for {lo}."
    mean_opts = [mean_right, f"On average, the {what} for {lo} were {up} than for {hi}.",
                 f"The mean for {hi} was higher.", f"On average, the {what} for {hi} were more varied."]
    sd_right = f"The {what} for {cons} were more consistent."
    sd_opts = [sd_right, f"On average, the {what} for {other} were more varied.",
               f"The standard deviation for {cons} was more consistent.", f"The data for {other} is more varied."]
    random.shuffle(mean_opts); random.shuffle(sd_opts)
    unit = f" {u}" if u else ""
    parts = [
        make_part("(a)", "Which is a valid comment about the mean?", mean_right, options=mean_opts,
                  worked_solution=[mean_right],
                  distractors=[{"value": f"The mean for {hi} was higher.", "mistake": "say what the mean is "
                                "telling you, in context — 'the mean was higher' isn't accepted (2024 marking "
                                "instructions)."},
                               {"value": f"On average, the {what} for {hi} were more varied.",
                                "mistake": "'more varied' is about spread, not the average (course reports "
                                           "2018–2026)."}]),
        make_part("(b)", "Which is a valid comment about the standard deviation?", sd_right, options=sd_opts,
                  worked_solution=[sd_right],
                  distractors=[{"value": f"On average, the {what} for {other} were more varied.",
                                "mistake": "'on average' is for the mean, not the spread (course reports "
                                           "2018–2026)."},
                               {"value": f"The standard deviation for {cons} was more consistent.",
                                "mistake": "the comment must be about the " + what + ", not the standard "
                                           "deviation (2024 marking instructions)."},
                               {"value": f"The data for {other} is more varied.",
                                "mistake": "say what the data is — 'the data' isn't in context (2019 and 2025 "
                                           "course reports)."}]),
    ]
    text = (f"{a[0].upper() + a[1:]}: mean {ma}{unit}, standard deviation {sa}{unit}.\n\n"
            f"{b[0].upper() + b[1:]}: mean {mb}{unit}, standard deviation {sb}{unit}.")
    return Question(question_text=text, correct_answer=mean_right, topic=TOPIC, question_type=QTYPE,
                    parts=parts, worked_solution=multipart_worked_solution(parts), notes=NOTES_COMPARE)


def generate_comparing_question(calc_mode=False):
    return random.choice([generate_comparing_l1, generate_comparing_l2, generate_comparing_l3,
                          generate_comparing_l4])(calc_mode=calc_mode)
