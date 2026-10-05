"""N5 Finance and Statistics — Probability and Expected Frequency.

Mirrors Probability_and_Expected_Frequency_Worksheet.docx (N5 Apps/Worksheets/Finance and Statistics):
1. probability as a fraction, decimal or percentage (including items already drawn and NOT events),
2. probability from tables, two-way tables and pie charts,
3. combined events from a sample-space table (two spinners, a dice and a coin),
4. expected frequency = probability × number of trials,
5. more or less than expected, and which game gives the best chance.
This is separate from topics/numeracy/probability.py (N5 Numeracy) and topics/statistics/probability.py
(Higher), which are used elsewhere.

Distractors are the errors in the course reports and marking instructions: the wrong total in the
denominator (2024 P2 Q3: 7/49), the grand total or the wrong row/column of a two-way table, a number of
people instead of a probability (2019 P1 Q3b), not simplifying when asked, a ratio (2018–2026 MI), a
probability greater than 1 (2018 MI COR 35/13), 36 outcomes as if two dice (2018 CR), multiplying the
separate probabilities (2023 MI COR 9/25), an expected frequency found by dividing (2022 MI COR
700 ÷ 15) or not multiplied at all, a percentage not divided by 100, and expected wins compared with
prize money (2025 P1 Q8b).
"""
import math
import random
from fractions import Fraction

from core.models.distractors import distractors
from core.models.question_model import Question, make_part, multipart_worked_solution

TOPIC, QTYPE = "Finance and Statistics", "Probability and Expected Frequency"
_DIAG = "topics.finance_statistics.probability_expected_diagrams"

NOTES_SIMPLE = """
**Probability as a fraction, decimal or percentage**

P(event) = number of favourable outcomes ÷ total number of outcomes

**Example (from the worksheet):** A bag of Harris Tweed offcuts holds 7 blue, 9 green and 4 red pieces.
One piece is picked at random. Calculate the probability that it is blue, as a fraction, a decimal and
a percentage.
- Total = 7 + 9 + 4 = 20
- P(blue) = **7/20**
- Decimal: 7 ÷ 20 = **0.35**
- Percentage: 0.35 × 100 = **35%**

⚠ Never write a probability as a ratio — 11 : 35 doesn't get the final mark (2022 and 2025 marking
instructions). Use the right total: in 2024 Paper 2 Q3 six of the 49 balls had already been drawn,
so the total was 43 — the answer 7/49 scored 0.
"""

NOTES_TABLES = """
**Probability from tables and charts**

Find the right total first. If the question picks from one group ("an S4 pupil is chosen at random"),
the total is that group's total, not everyone. For a pie chart the total is 360°.

**Example (from the worksheet):**

| | Bus | Car | Walk | Total |
|---|---|---|---|---|
| S3 | 34 | 12 | 14 | 60 |
| S4 | 26 | 18 | 16 | 60 |
| Total | 60 | 30 | 30 | 120 |

- (a) A pupil is chosen at random: P(walks) = 30/120 = **1/4**
- (b) An S4 pupil is chosen at random: P(car) = 18/60 = **3/10** (only the S4 row)

⚠ Give a probability, not a number of people — in 2019 Paper 1 Q3(b) most candidates worked out how
many employees were in the pie chart sectors instead (course report).
"""

NOTES_COMBINED = """
**Combined events — the sample-space table**

Put one spinner (or the coin) down the side and the other along the top, and fill in every outcome.
Total outcomes = rows × columns.

**Example (from the worksheet):** Spinner A has 1, 2, 3, 4; spinner B has 1, 2, 3, 4, 5, 6. The numbers
are multiplied; a prize is won if the answer is less than 6.

| A × B | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 1 | 2 | 3 | 4 | 5 | 6 |
| 2 | 2 | 4 | 6 | 8 | 10 | 12 |
| 3 | 3 | 6 | 9 | 12 | 15 | 18 |
| 4 | 4 | 8 | 12 | 16 | 20 | 24 |

- Total outcomes = 4 × 6 = 24;  products less than 6: 9
- P(win) = 9/24 = **3/8**

⚠ In 2018 many used 36 outcomes, as if the spinners were two dice (course report). Multiplying the
separate probabilities (3/5 × 3/5 = 9/25) scored 1 out of 3 in 2023, and a 6 × 6 table for a dice
and a coin scored 0 in 2026.
"""

NOTES_EXPECTED = """
**Expected frequency**

Expected frequency = probability × number of trials. The probability can be a fraction, a decimal or
a percentage, and the answer doesn't have to be a whole number.

**Example (from the worksheet):** 35% of visitors to the Callanish Stones arrive by bus. On one day
there are 380 visitors. How many would you expect to arrive by bus?
- Probability = 35% = 35 ÷ 100 = 0.35
- Expected = 0.35 × 380 = **133 visitors**

⚠ Multiply — don't divide. 700 ÷ 15 = 46.6 scored 0 in 2022 Paper 1 Q12, where many candidates
didn't know how to find an expected frequency (course report).
"""

NOTES_COMPARE = """
**More or less than expected?**

Work out the expected number (or the expected prize money), compare it with what really happened,
and say MORE or LESS.

**Example (from the worksheet):** The probability of winning hook-a-duck is 0.2. The game was played
90 times and each winner was paid £3. £60 was paid out. More or less than expected?
- Expected wins = 0.2 × 90 = 18
- Expected prize money = 18 × £3 = £54
- £60 is more than £54, so **MORE** prize money was paid out than expected.

To compare chances, change them all to decimals (or percentages) first.

⚠ "More" with no working scores 0 (2022, 2023 and 2025 marking instructions). In 2025 many found
0.15 × 80 = 12 wins but didn't go on to the prize money — compare like with like.
"""


# ── helpers ───────────────────────────────────────────────────────────────────────────────────
def _frac(a, b):
    f = Fraction(a, b)
    return f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)


def _g(x):
    x = float(x)
    return str(int(round(x))) if abs(x - round(x)) < 1e-9 else f"{x:.6f}".rstrip("0").rstrip(".")


def _num(v):
    s = str(v)
    if ":" in s:
        return None
    if "/" in s:
        a, b = s.split("/")
        return int(a) / int(b)
    try:
        return float(s)
    except ValueError:
        return None


def _two_dp(F, T):
    return abs(round(F / T, 2) - F / T) < 1e-12


def _p_answer(F, T, form):
    """(correct_answer, final worked line, extra scaffold step or None) for F/T in the given form."""
    if form == "fraction":
        ans = _frac(F, T)
        return ans, (f"P = {F}/{T} = **{ans}**" if ans != f"{F}/{T}" else f"P = **{ans}**")
    if form == "decimal":
        ans = round(F / T, 2)
        return ans, f"P = {F}/{T} = {F} ÷ {T} = **{_g(ans)}**"
    ans = round(100 * F / T, 2)
    return ans, f"P = {F}/{T} = {F} ÷ {T} = {_g(F / T)};  {_g(F / T)} × 100 = **{_g(ans)}%**"


def _form_text(form):
    return {"fraction": "Give your answer as a fraction in its simplest form.",
            "decimal": "Give your answer as a decimal.",
            "percent": "Give your answer as a percentage."}[form]


def _p_distractors(F, T, form, wrong):
    """Distractors for a probability F/T asked in `form`. `wrong` = [(F', T', mistake)] for wrong
    fractions (wrong total, wrong row …), converted to the asked form. Adds the usual ratio / not
    simplified / upside-down / forgot ×100 ones. Anything numerically equal to the answer is dropped,
    except the unsimplified fraction (a test needs the simplest form)."""
    ans, _ = _p_answer(F, T, form)[:2]
    cands = []
    for f2, t2, why in wrong:
        if t2 <= 0:
            continue
        if form == "fraction":
            cands.append((_frac(f2, t2), why))
        elif form == "decimal":
            cands.append((round(f2 / t2, 2), why))
        else:
            cands.append((round(100 * f2 / t2, 2), why))
    if form == "fraction" and _frac(F, T) != f"{F}/{T}":
        cands.append((f"{F}/{T}", "the question asks for the fraction in its simplest form — divide the top "
                                  "and bottom by the same number."))
    cands.append((f"{F}:{T}", "a probability is a fraction, decimal or percentage — never a ratio "
                              "(marking instructions 2018–2026: 11 : 35 loses the mark)."))
    cands.append((f"{T}/{F}" if form == "fraction" else round(T / F, 2),
                  "a probability can't be more than 1 — it's favourable ÷ total, not total ÷ favourable "
                  "(2018 marking instructions: 35/13)."))
    if form == "percent":
        cands.append((round(F / T, 2), "that's the decimal — multiply by 100 for a percentage."))
    out = []
    for v, why in cands:
        n = _num(v)
        if n is not None and abs(n - F / T * (100 if form == "percent" else 1)) < 0.01 and v != f"{F}/{T}":
            continue
        out.append((v, why))
    return distractors(ans, out)


def _md_table(headers, rows):
    lines = ["| " + " | ".join(map(str, headers)) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(map(str, r)) + " |" for r in rows]
    return "\n".join(lines)


# ── Level 1: probability as a fraction, decimal or percentage ───────────────────────────────────
_BAGS = [
    ("A bag of Harris Tweed offcuts holds", "pieces", [("blue", "blue"), ("green", "green"), ("red", "red"),
                                                       ("brown", "brown")], "piece"),
    ("A box of sweets from a Stornoway shop holds", "sweets", [("toffees", "a toffee"), ("mints", "a mint"),
                                                               ("fudges", "a fudge"), ("jellies", "a jelly")], "sweet"),
    ("On the Lochmaddy ferry there are", "vehicles", [("cars", "a car"), ("vans", "a van"), ("lorries", "a lorry"),
                                                      ("motorbikes", "a motorbike")], "vehicle"),
    ("A crofter's flock has", "sheep", [("Blackface", "a Blackface"), ("Cheviot", "a Cheviot"),
                                        ("Hebridean", "a Hebridean"), ("Shetland", "a Shetland")], "sheep"),
]


def _simple_count():
    intro, things, kinds, one = random.choice(_BAGS)
    k = random.choice([2, 3])
    names = random.sample(kinds, k)
    form = random.choice(["fraction", "fraction", "decimal", "percent"])
    for _ in range(500):
        counts = [random.randint(2, 18) for _ in names]
        T = sum(counts)
        F = counts[0]
        if form == "fraction" or _two_dp(F, T):
            break
    else:
        counts = [7, 9, 4][:k]; T = sum(counts); F = counts[0]; form = "fraction"
    want, want_one = names[0]
    listing = ", ".join(f"{c} {n}" for c, (n, _) in zip(counts[:-1], names[:-1])) + \
        f" and {counts[-1]} {names[-1][0]}"
    text = (f"{intro} {listing}. One {one} is chosen at random. Calculate the probability that it is {want_one}. "
            f"{_form_text(form)}")
    ans, last = _p_answer(F, T, form)
    worked = [f"Total = {' + '.join(map(str, counts))} = {T}", f"Favourable ({want}) = {F}", last]
    steps = [{"prompt": f"Total number of {things}", "answer": T},
             {"prompt": f"Number of {want}", "answer": F},
             {"prompt": "The probability", "answer": ans}]
    wrong = [(F, T - F, f"the bottom of the fraction is the TOTAL ({T}), not the number that aren't {want}.")]
    return text, ans, worked, steps, _p_distractors(F, T, form, wrong)


def _simple_removed():
    N = random.choice([30, 40, 45, 49, 50, 60])
    below = random.choice([6, 8, 10, 12])
    k = random.choice([4, 5, 6])
    for _ in range(500):
        drawn = sorted(random.sample(range(1, N + 1), k))
        gone = [x for x in drawn if x < below]
        if 1 <= len(gone) <= 2:
            break
    left = N - k
    F = below - 1 - len(gone)
    what = random.choice(["Balls in a draw at a Castlebay ceilidh", "Raffle tickets at the Uist games",
                          "Balls in a Stornoway charity lottery"])
    text = (f"{what} are numbered 1 to {N}. {k} have already been drawn and not replaced: "
            f"{', '.join(map(str, drawn[:-1]))} and {drawn[-1]}. Calculate the probability that the next one "
            f"drawn is a number less than {below}. {_form_text('fraction')}")
    ans, last = _p_answer(F, left, "fraction")
    worked = [f"Left: {N} − {k} = {left}", f"Less than {below} still in the draw: {below - 1} − {len(gone)} = {F}",
              last]
    steps = [{"prompt": "How many are left to draw from?", "answer": left},
             {"prompt": f"How many of those are less than {below}?", "answer": F},
             {"prompt": "The probability", "answer": ans}]
    wrong = [(below - 1, N, f"some have already been drawn and not replaced — in 2024 Paper 2 Q3, 7/49 scored 0. "
                            f"Use the {left} that are left."),
             (F, N, f"the total is the {left} left, not all {N}."),
             (below - 1, left, f"{', '.join(map(str, gone))} {'has' if len(gone) == 1 else 'have'} already been "
                               f"drawn, so {'it isn' if len(gone) == 1 else 'they aren'}'t favourable any more.")]
    return text, ans, worked, steps, _p_distractors(F, left, "fraction", wrong)


def _simple_not():
    for _ in range(500):
        T = random.choice([20, 25, 40, 50, 60, 80])
        n = random.randint(2, T // 3)
        form = random.choice(["fraction", "decimal"])
        if form == "fraction" or _two_dp(T - n, T):
            break
    item = random.choice([("A lucky dip at the Uist games has", "prizes", "ferry vouchers", "a ferry voucher"),
                          ("A Barra café's raffle has", "prizes", "hampers", "a hamper"),
                          ("A tub at a Lewis gala holds", "plastic ducks", "winning ducks", "a winning duck")])
    F = T - n
    text = (f"{item[0]} {T} {item[1]}. {n} of them are {item[2]}. One is chosen at random. Calculate the "
            f"probability that it is NOT {item[3]}. {_form_text(form)}")
    ans, last = _p_answer(F, T, form)
    worked = [f"Not {item[3]}: {T} − {n} = {F}", last]
    steps = [{"prompt": f"How many are NOT {item[3]}?", "answer": F}, {"prompt": "The probability", "answer": ans}]
    wrong = [(n, T, f"that's the probability that it IS {item[3]} — the question asks for NOT.")]
    return text, ans, worked, steps, _p_distractors(F, T, form, wrong)


def generate_probability_expected_l1(calc_mode=False):
    """Probability as a fraction, decimal or percentage."""
    text, ans, worked, steps, dis = random.choice([_simple_count, _simple_removed, _simple_not])()
    return Question(question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=worked, notes=NOTES_SIMPLE, distractors=dis)


# ── Level 2: tables and charts ─────────────────────────────────────────────────────────────────
_TWO_WAY = [
    ("how S3 and S4 pupils at a Lewis school travel to school", ["S3", "S4"], ["Bus", "Car", "Walk"], "pupil",
     "{r} pupil", "this pupil travels by {c}"),
    ("the activities chosen at a Stornoway leisure centre", ["Adults", "Children"],
     ["Swimming", "Gym", "Yoga"], "person", "{r_one}", "this person chose {c}"),
    ("the lambs born on two crofts", ["Croft A", "Croft B"], ["Male", "Female"], "lamb", "lamb from {r}",
     "this lamb is {c}"),
    ("whether flights from Barra airport left on time", ["Summer", "Winter"], ["On time", "Late"], "flight",
     "{r} flight", "this flight was {c}"),
]
_ONE = {"Adults": "adult", "Children": "child"}


def _two_way():
    title, rows, cols, one, group_fmt, ev_fmt = random.choice(_TWO_WAY)
    vals = [[random.randint(4, 40) for _ in cols] for _ in rows]
    ri, ci = random.randrange(len(rows)), random.randrange(len(cols))
    given = random.choice(["row", "row", "col"])
    form = "fraction"
    if given == "row":
        F, T = vals[ri][ci], sum(vals[ri])
        grp = group_fmt.format(r=rows[ri], r_one=_ONE.get(rows[ri], rows[ri]))
        ev = ev_fmt.format(c=cols[ci].lower())
        text_q = (f"A{'n' if grp[0].lower() in 'aeiou' else ''} {grp} is chosen at random. Calculate the probability "
                  f"that {ev}.")
        wrong_line = (vals[ri][ci], sum(v[ci] for v in vals),
                      f"you used the {cols[ci]} column's total — the question picks from the {rows[ri]} row only.")
        tot_line = f"{rows[ri]} total = {' + '.join(map(str, vals[ri]))} = {T}"
    else:
        F, T = vals[ri][ci], sum(v[ci] for v in vals)
        text_q = (f"A {one} in the '{cols[ci]}' column is chosen at random. Calculate the probability that it is "
                  f"from {rows[ri]}.")
        wrong_line = (vals[ri][ci], sum(vals[ri]),
                      f"you used the {rows[ri]} row's total — the question picks from the {cols[ci]} column only.")
        tot_line = f"{cols[ci]} total = {' + '.join(str(v[ci]) for v in vals)} = {T}"
    grand = sum(map(sum, vals))
    text = f"The table shows {title}. {text_q} {_form_text(form)}"
    ans, last = _p_answer(F, T, form)
    worked = [tot_line, f"Favourable = {F}", last]
    steps = [{"prompt": "The total for the group the question picks from", "answer": T},
             {"prompt": "The probability", "answer": ans}]
    wrong = [(F, grand, f"the {one} is chosen from one group, not from all {grand} — use that group's total "
                        f"({T})."), wrong_line]
    table = _md_table([""] + cols, [[r] + v for r, v in zip(rows, vals)])
    return text, ans, worked, steps, _p_distractors(F, T, form, wrong), {"table": table}


def _pie():
    labels = random.choice([["Lewis", "Harris", "Uist", "Barra"], ["Bus", "Car", "Walk", "Bike"],
                            ["Ceilidh", "Pipe band", "Choir", "Gaelic drama"]])
    for _ in range(500):
        a = [random.randint(3, 15) * 10 for _ in range(3)]
        if sum(a) < 330:
            angles = a + [360 - sum(a)]
            if angles[-1] >= 30 and len(set(angles)) == 4:
                break
    N = random.choice([36, 72, 90, 180])
    pick = random.sample(range(4), 2)
    F = angles[pick[0]] + angles[pick[1]]
    names = f"{labels[pick[0]]} or {labels[pick[1]]}"
    text = (f"{N} people were asked to choose one option. The pie chart shows the results. Calculate the "
            f"probability that a person chosen at random chose {names}. {_form_text('fraction')}")
    ans, last = _p_answer(F, 360, "fraction")
    worked = [f"{names}: {angles[pick[0]]}° + {angles[pick[1]]}° = {F}°", "Total = 360°", last]
    steps = [{"prompt": "Total angle for the chosen sectors (degrees)", "answer": F},
             {"prompt": "The probability", "answer": ans}]
    people = F / 360 * N
    dis = _p_distractors(F, 360, "fraction", [(angles[pick[0]], 360, "add BOTH sectors' angles.")])
    if abs(people - round(people)) < 1e-9:
        dis = distractors(ans, [(d["value"], d["mistake"]) for d in dis] +
                          [(int(round(people)), "that's the number of people — the question asks for a probability "
                                                "(2019 Paper 1 Q3(b) course report).")])
    meta = {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DIAG, "kind": "pie", "args": [labels, angles]}}
    return text, ans, worked, steps, dis, meta


def _freq():
    for _ in range(500):
        freqs = [random.randint(2, 16) for _ in range(5)]
        T = sum(freqs)
        above = random.choice([2, 3])
        F = sum(freqs[above:])
        if _two_dp(F, T) and 0 < F < T:
            break
    what = random.choice([("people in each car on the Sound of Barra ferry", "car", "people in it"),
                          ("goals scored by a Stornoway football team in each match", "match", "goals scored"),
                          ("lambs born to each ewe on a Uist croft", "ewe", "lambs")])
    text = (f"The table shows the number of {what[0]}. A {what[1]} is chosen at random. Calculate the probability "
            f"that it had more than {above} {what[2]}. {_form_text('decimal')}")
    ans, last = _p_answer(F, T, "decimal")
    worked = [f"Total = {' + '.join(map(str, freqs))} = {T}",
              f"More than {above}: {' + '.join(map(str, freqs[above:]))} = {F}", last]
    steps = [{"prompt": "Total frequency", "answer": T}, {"prompt": f"Number with more than {above}", "answer": F},
             {"prompt": "The probability", "answer": ans}]
    wrong = [(F, 5, "the total is the sum of the frequencies, not the number of columns."),
             (F - freqs[above], T, f"'more than {above}' doesn't include {above} — but it does include every "
                                   f"value above it."),
             (F + freqs[above - 1], T, f"'more than {above}' doesn't include {above}.")]
    table = _md_table([what[2].capitalize(), "1", "2", "3", "4", "5"], [["Frequency"] + freqs])
    return text, ans, worked, steps, _p_distractors(F, T, "decimal", wrong), {"table": table}


def generate_probability_expected_l2(calc_mode=False):
    """Probability from two-way tables, frequency tables and pie charts."""
    text, ans, worked, steps, dis, meta = random.choice([_two_way, _two_way, _pie, _freq])()
    return Question(question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                    worked_solution=worked, notes=NOTES_TABLES, distractors=dis, metadata=meta)


# ── Level 3: combined events ───────────────────────────────────────────────────────────────────
_RULES = [
    ("The numbers are multiplied. A prize is won if the answer is less than {k}.", lambda a, b, k: a * b < k, "×"),
    ("The numbers are multiplied. A prize is won if the answer is greater than {k}.", lambda a, b, k: a * b > k, "×"),
    ("The numbers are added. A prize is won if the total is greater than {k}.", lambda a, b, k: a + b > k, "+"),
    ("The numbers are added. A prize is won if the total is {k} or more.", lambda a, b, k: a + b >= k, "+"),
    ("A prize is won if spinner B lands on a larger number than spinner A.", lambda a, b, k: b > a, None),
]


def _spinners():
    for _ in range(1000):
        A = sorted(random.sample(range(0, 9), random.choice([3, 4, 5])))
        B = sorted(random.sample(range(1, 13), random.choice([4, 5, 6])))
        text_r, rule, op = random.choice(_RULES)
        vals = [a * b if op == "×" else a + b for a in A for b in B] if op else [0]
        k = random.choice(sorted(set(vals))[1:-1] or [1]) if op else 0
        F = sum(1 for a in A for b in B if rule(a, b, k))
        T = len(A) * len(B)
        if 2 <= F <= T - 2 and T != 36:
            break
    text = (f"A game at the Barra gala uses the two fair spinners shown. {text_r.format(k=k)} Calculate the "
            f"probability of winning a prize. {_form_text('fraction')}")
    ans, last = _p_answer(F, T, "fraction")
    cell = f"each cell is A {op} B" if op else "tick each cell where B is larger than A"
    worked = [f"Table: spinner A ({', '.join(map(str, A))}) down the side, spinner B ({', '.join(map(str, B))}) "
              f"along the top; {cell}.", f"Total outcomes = {len(A)} × {len(B)} = {T}",
              f"Winning outcomes = {F}", last]
    steps = [{"prompt": "Total number of outcomes (rows × columns)", "answer": T},
             {"prompt": "Number of winning outcomes", "answer": F},
             {"prompt": "The probability", "answer": ans}]
    wrong = [(F, 36, "the spinners aren't two dice — there are "
                     f"{len(A)} × {len(B)} = {T} outcomes, not 36 (2018 Paper 1 Q14 course report)."),
             (F, len(A) + len(B), f"total outcomes = {len(A)} × {len(B)} = {T} (multiply, don't add).")]
    meta = {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DIAG, "kind": "spinners", "args": [A, B, ["spinner A", "spinner B"]]}}
    return text, ans, worked, steps, _p_distractors(F, T, "fraction", wrong), meta


def _dice_coin():
    conds = [("an even number", lambda d: d % 2 == 0), ("an odd number", lambda d: d % 2 == 1),
             ("a multiple of 3", lambda d: d % 3 == 0), ("a number greater than 4", lambda d: d > 4),
             ("1", lambda d: d == 1), ("6", lambda d: d == 6), ("a number less than 3", lambda d: d < 3),
             ("a prime number", lambda d: d in (2, 3, 5))]
    (t_txt, t_ok), (h_txt, h_ok) = random.sample(conds, 2)
    wins = [f"T{d}" for d in range(1, 7) if t_ok(d)] + [f"H{d}" for d in range(1, 7) if h_ok(d)]
    F, T = len(wins), 12
    name = random.choice(["Ann", "Iain", "Mairi", "Calum", "Eilidh"])
    text = (f"{name} rolls a fair six-sided dice and flips a fair coin. {name} wins if the coin lands on tails and "
            f"the dice lands on {t_txt}, or if the coin lands on heads and the dice lands on {h_txt}. Calculate the "
            f"probability of winning. {_form_text('fraction')}")
    ans, last = _p_answer(F, T, "fraction")
    worked = ["Table: coin down the side (H, T), dice along the top (1 to 6).", "Total outcomes = 2 × 6 = 12",
              f"Winning: {', '.join(wins)} — {F} outcomes", last]
    steps = [{"prompt": "Total number of outcomes", "answer": 12}, {"prompt": "Number of winning outcomes", "answer": F},
             {"prompt": "The probability", "answer": ans}]
    t_n = sum(1 for d in range(1, 7) if t_ok(d)); h_n = sum(1 for d in range(1, 7) if h_ok(d))
    wrong = [(F, 36, "a dice and a coin give 2 × 6 = 12 outcomes — a 6 × 6 table scored 0 in 2026 Paper 1 Q11."),
             (t_n + h_n, 6, "use a 2 × 6 table: the coin matters too, so the total is 12."),
             (t_n * h_n, 36, "multiplying the dice probabilities doesn't work here — list the outcomes in a 2 × 6 "
                             "table (2026 Paper 1 Q11).")]
    return text, ans, worked, steps, _p_distractors(F, T, "fraction", wrong), {}


def _not_win():
    colours = random.sample(["red", "blue", "green", "yellow", "white"], random.choice([4, 5]))
    nums = list(range(1, random.choice([4, 5, 6]) + 1))
    good = random.sample(colours, 2)
    parity = random.choice(["even", "odd"])
    good_n = [n for n in nums if (n % 2 == 0) == (parity == "even")]
    W = 2 * len(good_n)
    T = len(colours) * len(nums)
    F = T - W
    text = (f"A game uses the two fair spinners shown. A prize is won if the colour spinner lands on {good[0]} or "
            f"{good[1]} AND the number spinner lands on an {parity} number. Calculate the probability of NOT "
            f"winning a prize. {_form_text('fraction')}")
    ans, last = _p_answer(F, T, "fraction")
    worked = [f"Total outcomes = {len(colours)} × {len(nums)} = {T}",
              f"Winning: {good[0]} or {good[1]} with {', '.join(map(str, good_n))} — 2 × {len(good_n)} = {W}",
              f"Not winning = {T} − {W} = {F}", last]
    steps = [{"prompt": "Total number of outcomes", "answer": T}, {"prompt": "Number of winning outcomes", "answer": W},
             {"prompt": "Number of outcomes that DON'T win", "answer": F}, {"prompt": "The probability", "answer": ans}]
    nc, nn = len(colours) - 2, len(nums) - len(good_n)
    wrong = [(nc * nn, T, f"multiplying the separate 'not' probabilities ({nc}/{len(colours)} × {nn}/{len(nums)}) "
                          "misses outcomes like a winning colour with a losing number — 9/25 scored 1 out of 3 in "
                          "2023 Paper 1 Q5."),
             (W, T, "that's the probability of WINNING — the question asks for NOT winning.")]
    meta = {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DIAG, "kind": "spinners",
                               "args": [colours, nums, ["colour spinner", "number spinner"]]}}
    return text, ans, worked, steps, _p_distractors(F, T, "fraction", wrong), meta


def generate_probability_expected_l3(calc_mode=False):
    """Combined events from a sample-space table."""
    text, ans, worked, steps, dis, meta = random.choice([_spinners, _spinners, _dice_coin, _not_win])()
    return Question(question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                    worked_solution=worked, notes=NOTES_COMBINED, distractors=dis, metadata=meta)


# ── Level 4: expected frequency ───────────────────────────────────────────────────────────────
_EXP = [("The probability that a parcel sent to Stornoway arrives damaged is {p}.", "A courier delivers {n} parcels",
         "arrive damaged", "parcels"),
        ("The probability that a Uist ewe has twins is {p}.", "A crofter has {n} ewes", "have twins", "ewes"),
        ("The probability that a ferry sailing from Oban is cancelled in winter is {p}.",
         "There are {n} winter sailings", "be cancelled", "sailings"),
        ("{p} of the creels a fisherman hauls have a lobster in them.", "He hauls {n} creels", "have a lobster",
         "creels")]


def generate_probability_expected_l4(calc_mode=False):
    """Expected frequency = probability × number of trials (fraction, decimal or percentage)."""
    lead, trials, outcome, unit = random.choice(_EXP)
    form = random.choice(["decimal", "percent", "fraction", "prize"])
    worked, wrong = [], []
    if form == "decimal":
        p = random.choice([0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.12, 0.15, 0.25])
        n = random.choice([150, 200, 250, 300, 350, 400, 450, 600, 700])
        ps, E = _g(p), round(p * n, 2)
        worked = [f"Expected = probability × number of {unit}", f"Expected = {ps} × {n} = **{_g(E)}**"]
        steps = [{"prompt": "Expected frequency = probability × number of trials", "answer": E}]
        wrong = [(p, "multiply the probability by the number of trials."),
                 (round(n / (p * 100), 2), "multiply, don't divide (2022 Paper 1 Q12: 700 ÷ 15 scored 0).")]
    elif form == "percent":
        pc = random.choice([5, 8, 12, 15, 20, 25, 35, 40, 45])
        n = random.choice([120, 160, 180, 200, 240, 300, 380, 400])
        p, ps, E = pc / 100, f"{pc}%", round(pc * n / 100, 2)
        worked = [f"Probability = {pc}% = {pc} ÷ 100 = {_g(p)}", f"Expected = {_g(p)} × {n} = **{_g(E)}**"]
        steps = [{"prompt": "The probability as a decimal", "answer": p},
                 {"prompt": "Expected frequency", "answer": E}]
        wrong = [(pc * n, f"change {pc}% to a decimal ({_g(p)}) before multiplying."),
                 (round(n / pc, 2), "multiply, don't divide (2022 Paper 1 Q12: 700 ÷ 15 scored 0).")]
    elif form == "fraction":
        b = random.choice([3, 4, 5, 8, 10, 20, 25])
        a = random.choice([x for x in range(1, b) if math.gcd(x, b) == 1 and 2 * x <= b])
        n = b * random.randint(4, 30)
        p, ps, E = a / b, f"{a}/{b}", a * n // b
        worked = [f"{n} ÷ {b} = {n // b}", f"{a}/{b} of {n} = {n // b} × {a} = **{E}**"]
        steps = [{"prompt": f"{n} ÷ {b}", "answer": n // b}, {"prompt": "Expected frequency", "answer": E}]
        wrong = [(n // b, f"that's 1/{b} of {n} — multiply by {a} as well."),
                 (round(b * n / a, 2), f"multiply by {a}/{b}, don't divide.")]
    else:
        p = random.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.4])
        n = random.choice([40, 60, 80, 100, 120, 140, 160])
        prize = random.choice([2, 3, 4, 5])
        wins = round(p * n, 2)
        E = round(wins * prize, 2)
        text = (f"The probability of winning a game at the Uist games is {_g(p)}. The game is played {n} times and "
                f"each winner gets £{prize}. How much prize money should the organisers expect to pay out?")
        worked = [f"Expected wins = {_g(p)} × {n} = {_g(wins)}", f"Expected prize money = {_g(wins)} × £{prize} = "
                                                                  f"**£{E:.2f}**"]
        steps = [{"prompt": "Expected number of wins", "answer": wins},
                 {"prompt": "Expected prize money (£)", "answer": E}]
        wrong = [(wins, f"that's the number of wins — multiply by the £{prize} prize (2025 Paper 1 Q8(b))."),
                 (round(n * prize, 2), "not every game is won — multiply by the probability too.")]
        return Question(question_text=text, correct_answer=E, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                        worked_solution=worked, notes=NOTES_EXPECTED, distractors=distractors(E, wrong))
    text = (f"{lead.format(p=ps)} {trials.format(n=n)}. How many would you expect to {outcome}?").replace(
        "{p}", ps)
    text = text[0].upper() + text[1:]
    return Question(question_text=text, correct_answer=E, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                    worked_solution=worked, notes=NOTES_EXPECTED, distractors=distractors(E, wrong))


# ── Level 5: more or less than expected; best chance ───────────────────────────────────────────
def _compare():
    prize_game = random.random() < 0.5
    opts = ["More than expected", "Less than expected"]
    if prize_game:
        p = random.choice([0.1, 0.12, 0.15, 0.2, 0.25])
        n = random.choice([60, 80, 100, 120, 150, 200])
        prize = random.choice([2, 3, 4, 5])
        wins = round(p * n, 2)
        target = round(wins * prize, 2)
        if abs(wins - round(wins)) > 1e-9:
            return _compare()
        actual = int(target + random.choice([-1, 1]) * prize * random.randint(1, 3))
        text = (f"The probability of winning a game at the Stornoway fun day is {_g(p)}. The game was played {n} "
                f"times and each winner was paid £{prize}. A total of £{actual} was paid out in prizes.")
        word = "More" if actual > target else "Less"
        pa = make_part("(a)", "Calculate the expected prize money (£).", target,
                       scaffold_steps=[{"prompt": "Expected number of wins", "answer": wins},
                                       {"prompt": "Expected prize money (£)", "answer": target}],
                       worked_solution=[f"Expected wins = {_g(p)} × {n} = {_g(wins)}",
                                        f"Expected prize money = {_g(wins)} × £{prize} = £{_g(target)}"],
                       distractors=distractors(target, [
                           (wins, f"that's the number of wins — compare MONEY with money: × £{prize} (2025 Paper 1 "
                                  f"Q8(b))."),
                           (round(n / actual, 2), "multiply the probability by the number of games — don't divide.")]))
        conclusion = f"£{actual} is {word.lower()} than £{_g(target)}, so {word.upper()} than expected."
    else:
        ctx = random.choice([("a lamb needs help at birth", "lambs were born on a Harris croft", "needed help"),
                             ("a parcel arrives damaged", "parcels were delivered to Benbecula", "arrived damaged"),
                             ("a visitor to Callanish arrives by bus", "visitors came on one day", "came by bus")])
        pc = random.random() < 0.5
        p = random.choice([0.04, 0.05, 0.06, 0.08, 0.15, 0.2, 0.25, 0.35])
        n = random.choice([100, 150, 200, 250, 300, 350, 400, 500])
        target = round(p * n, 2)
        if abs(target - round(target)) > 1e-9 or target < 4:
            return _compare()
        actual = int(target + random.choice([-1, 1]) * random.randint(1, 4))
        ps = f"{_g(p * 100)}%" if pc else _g(p)
        text = (f"The {'percentage chance' if pc else 'probability'} that {ctx[0]} is {ps}. {n} {ctx[1]}, and "
                f"{actual} {ctx[2]}.")
        word = "More" if actual > target else "Less"
        pa = make_part("(a)", "Calculate the expected number.", target,
                       scaffold_steps=[{"prompt": "Expected = probability × number of trials", "answer": target}],
                       worked_solution=[f"Expected = {_g(p)} × {n} = {_g(target)}"],
                       distractors=distractors(target, [
                           (round(n / actual, 2), f"multiply, don't divide — {n} ÷ {actual} scored 0 in 2022 Paper 1 "
                                                  f"Q12 (marking instructions)."),
                           (round(p * 100 * n, 2) if pc else None, "change the percentage to a decimal first."),
                           (p, "multiply the probability by the number of trials.")]))
        conclusion = f"{actual} is {word.lower()} than {_g(target)}, so {word.upper()} than expected."
    right = f"{word} than expected"
    pb = make_part("(b)", "Is this more or less than expected?", right, options=opts,
                   worked_solution=[conclusion])
    parts = [pa, pb]
    return Question(question_text=text, correct_answer=pa.correct_answer, topic=TOPIC, question_type=QTYPE,
                    parts=parts, worked_solution=multipart_worked_solution(parts), notes=NOTES_COMPARE)


def _best():
    for _ in range(1000):
        b = random.choice([4, 5, 8, 10, 20, 25])
        a = random.choice([x for x in range(1, b) if math.gcd(x, b) == 1])
        frac_v = a / b
        pc = random.choice(range(10, 60, 2))
        dec = random.choice([0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5])
        vals = [frac_v, pc / 100, dec]
        if len({round(v, 4) for v in vals}) == 3 and max(vals) - sorted(vals)[1] >= 0.02:
            break
    games = [("Game A", f"{a}/{b}", frac_v), ("Game B", f"{pc}%", pc / 100), ("Game C", _g(dec), dec)]
    random.shuffle(games)
    games = [(new, s, v) for new, (_, s, v) in zip(["Game A", "Game B", "Game C"], games)]
    best = max(games, key=lambda x: x[2])[0]
    text = ("At a gala, the chance of winning " + ", ".join(f"{lab} is {s}" for lab, s, _ in games[:-1]) +
            f" and the chance of winning {games[-1][0]} is {games[-1][1]}. Which game gives the best chance of "
            f"winning?")
    worked = [f"{lab}: {s} = {_g(round(v, 4))}" for lab, s, v in games] + \
             [f"The biggest is {_g(round(max(g[2] for g in games), 4))}, so **{best}**."]
    steps = [{"prompt": f"{lab} as a decimal", "answer": round(v, 4)} for lab, s, v in games]
    steps.append({"prompt": "Which game gives the best chance?", "answer": best})

    def raw(s):
        return float(s.rstrip("%").split("/")[0])
    naive = max(games, key=lambda x: raw(x[1]))[0]
    dis = []
    if naive != best:
        dis.append({"value": naive, "mistake": "compare them as decimals or percentages first — the biggest-looking "
                                               "number isn't always the biggest chance."})
    return Question(question_text=text, correct_answer=best, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                    worked_solution=worked, notes=NOTES_COMPARE, distractors=dis,
                    metadata={"options": ["Game A", "Game B", "Game C"]})


def generate_probability_expected_l5(calc_mode=False):
    """More or less than expected (with prize money), and comparing chances."""
    return random.choice([_compare, _compare, _best])()


def generate_probability_expected_question(calc_mode=False):
    return random.choice([generate_probability_expected_l1, generate_probability_expected_l2,
                          generate_probability_expected_l3, generate_probability_expected_l4,
                          generate_probability_expected_l5])(calc_mode=calc_mode)
