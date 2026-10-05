"""Higher Applications of Maths — Data and Distributions.

Mirrors Data_and_Distributions_Worksheet.docx (Higher Apps/Worksheets/Statistics): types of data and
sampling, statistical diagrams, median / quartiles / outliers, describing distributions, comparing data
sets, and the COUNTIF frequency-table spreadsheet (styled on 2025 Q12). Levels follow the worksheet's
sections, plus "Spreadsheet: Frequency Table".

Software output is shown exactly as R prints it (default quantile type 7; summary() to 4 significant
figures, a single value to 7). Distractors and wrong options are the errors in the course reports and
marking instructions: 'numerical' instead of 'discrete numerical' (2023 Q3(a)); 'people might lie' /
'small sample size' (2023 Q3(b) MI); 'more people could be listening this year' (2025 Q5(b)); 'sample size
must be the same' (2022 Q3(d)); a right-skewed histogram called normal or skewed left, and the mean chosen
for skewed data (2025 Q5(a)); 'travelled further' / 'more varied' with no statistic (2024 Q6(a)(ii));
'a smaller range' instead of the IQR (2025 Q9(a)); a participant hidden or not removed (2025 Q12).
"""
import math
import random
import statistics

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill

from core.engine.spreadsheet_solution import solution_metadata, workbook_bytes
from core.models.distractors import distractors
from core.models.question_model import Question, make_part, multipart_worked_solution

TOPIC, QTYPE = "Statistics", "Data and Distributions"
_DIAG = "topics.statistics.data_distributions_diagrams"


def _g(x, dp=2):
    x = round(x + 0.0, dp)
    s = f"{x:,.{dp}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def _r(x, dp=2):
    return round(x + 1e-9, dp)


def _diagram(kind, *args, width=480):
    return {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DIAG, "kind": kind, "args": list(args), "width": width}}


# ── R output ─────────────────────────────────────────────────────────────────────────────────
def _q7(x, p):
    s = sorted(x); h = (len(s) - 1) * p; lo = math.floor(h); hi = min(lo + 1, len(s) - 1)
    return s[lo] + (h - lo) * (s[hi] - s[lo])


def _dec(x, digits):
    if x == 0:
        return 0
    mant, exp = f"{abs(x):.{digits - 1}e}".split("e")
    mant = mant.replace(".", "").rstrip("0") or "0"
    return max(0, len(mant) - 1 - int(exp))


def _r_summary(var, x):
    """(printed lines, printed values [min, Q1, median, mean, Q3, max])."""
    vals = [min(x), _q7(x, .25), _q7(x, .5), statistics.mean(x), _q7(x, .75), max(x)]
    d = max(_dec(v, 4) for v in vals)
    strs = [f"{v:.{d}f}" for v in vals]
    names = ["Min.", "1st Qu.", "Median", "Mean", "3rd Qu.", "Max."]
    w = max(len(s) for s in strs + names)
    return ([f"> summary({var})", " ".join(n.rjust(w) for n in names), " ".join(s.rjust(w) for s in strs)],
            [float(s) for s in strs])


def _r_one(cmd, v):
    s = f"{v:.{_dec(v, 7)}f}"
    return [f"> {cmd}", f"[1] {s}"], float(s)


def _code(lines):
    return "```\n" + "\n".join(lines) + "\n```"


# ── notes: the worksheet's worked examples and ⚠ errors, per level ──────────────────────────
NOTES_TYPES = """
**Types of data** — categorical: **nominal** (no order: island, eye colour) or **ordinal** (an order:
poor / fair / good / excellent). Numerical: **discrete** (counted, or only certain values: number of
bags, age in years) or **continuous** (measured: time, mass).

**Example (worksheet).** Ferry passengers, Ullapool–Stornoway: age in years — discrete numerical; home
island — nominal categorical; journey time — continuous numerical; rating — ordinal categorical; number
of bags — discrete numerical. A survey handed out on one Saturday sailing in August is not a random
sample: mostly tourists, so island residents travelling in winter are under-represented.

**Population** = everyone you want to know about; **sample** = the part you collect data from. In a
**random** sample everyone has an equal chance of being chosen.

⚠ **Common error:** writing just 'numerical' — in 2023 (Q3(a)) many wrote 'numerical' rather than
'discrete numerical'; for gender only '(nominal) categorical' was accepted. 'People might lie' and
'small sample size' were not accepted as reasons a sample is unrepresentative (2023 marking instructions).
"""

NOTES_OUTLIERS = """
**Quartiles and outliers.** IQR = Q3 − Q1. An **outlier** is below Q1 − 1.5 × IQR or above
Q3 + 1.5 × IQR. In R, `summary(X)` gives the quartiles. Remove a value only if it is impossible or an
error (a negative age); a genuine extreme value stays in.

**Example (worksheet).** Ages of 15 walkers: 21, 24, 27, 33, 33, 35, 38, 41, 44, 46, 55, 55, 57, 58, 89.
Median = 8th value = 41; Q1 = 33, Q3 = 55; IQR = 22; 1.5 × IQR = 33. Limits: 33 − 33 = 0 and
55 + 33 = **88**. 89 > 88, so 89 is an outlier — a genuine age, so it stays in.

⚠ **Common error:** using the range (or 'the box plot is smaller') to describe spread — not accepted in
the 2025 marking instructions (Q9(a)); use the interquartile range, which outliers don't affect.
"""

NOTES_DESCRIBE = """
**Describing a distribution.** Symmetric / approximately **normal** → **mean and standard deviation**.
**Skewed to the right** (positively skewed, tail to the right, mean > median) or **skewed to the left**
(negatively skewed, tail to the left, mean < median) → **median and interquartile range**. Generate the
measure (`mean(X)`, `sd(X)`, `summary(X)`, `IQR(X)`) and STATE the value you choose.

**Example (worksheet).** Hours of listening in one week (community radio, 52 listeners): the histogram
has a long tail to the right → skewed to the right → median = **10.4 hours**, IQR = 5.775 hours (the mean,
11.78, is pulled up by a few long listeners).

⚠ **Common error:** in 2025 (Q5(a)) most candidates called a right-skewed histogram 'normal', 'skewed
to the left' or 'unevenly distributed', and many didn't identify the appropriate measure of location —
the mean scored only if the candidate had said the data were normal.
"""

NOTES_COMPARE = """
**Comparing data sets** — one comment on **location**, one on **spread**, in context, naming the
statistic. Mean and standard deviation for normal data; median and IQR for skewed data or box plots.

**Example (worksheet).** Salmon from two cages: Cage A mean 4.71 kg, sd 0.33 kg; Cage B mean 4.40 kg,
sd 0.57 kg. *On average, the salmon in Cage A are heavier (mean 4.71 kg compared with 4.40 kg). The
masses in Cage A are more consistent (standard deviation 0.33 kg compared with 0.57 kg).*

⚠ **Common error:** 'the golf ball travelled further' and 'the new golf ball is more varied' were common
in 2024 (Q6(a)(ii)) — say 'on average' and name the statistic. In 2025 (Q9(a)) 'because it was more
varied' or 'a smaller range' didn't score — refer to the interquartile range.
"""

NOTES_SHEET = """
**Frequency table in a spreadsheet** (styled on 2025 Q12). Delete the withdrawn participant's row —
don't hide it — and enter every response (the 'no's too). Then count each category with
`=COUNTIF($C$6:$C$34,F6)` and fill down; chart categorical data with a bar chart or pie chart, with a
title and axis labels.

⚠ **Common error:** in 2025 a few candidates hid the row instead of deleting it, or entered only the
'yes' responses (course report, Q12(a)(b)).
"""


# ── Level 1: types of data and sampling ─────────────────────────────────────────────────────
_TYPES = ["Discrete numerical", "Continuous numerical", "Nominal categorical", "Ordinal categorical"]
_VARIABLES = [
    ("the number of brothers and sisters a pupil has", 0), ("a person's age in years", 0),
    ("the number of bags a ferry passenger has", 0), ("the number of sheep treated for ticks each month", 0),
    ("the number of cars a household owns", 0), ("a pupil's shoe size (4, 4½, 5, …)", 0),
    ("the time taken to travel to school, in minutes", 1), ("the mass of a lamb, in kilograms", 1),
    ("a person's hand span, in centimetres", 1), ("the crossing time of a ferry", 1),
    ("the length of a mackerel, in cm", 1),
    ("a pupil's favourite subject", 2), ("a passenger's home island", 2), ("the colour of a car", 2),
    ("a person's gender", 2), ("how a pupil travels to school (walk, bus, car, cycle)", 2),
    ("a rating of a service (poor, fair, good, excellent)", 3), ("T-shirt size (S, M, L, XL)", 3),
    ("agreement with a statement (strongly disagree … strongly agree)", 3),
]


def _q_data_type():
    var, k = random.choice(_VARIABLES)
    right = _TYPES[k]
    opts = _TYPES + ["Numerical"]
    random.shuffle(opts)
    return Question(
        question_text=f"State the type of data that best describes {var}.",
        correct_answer=right, topic=TOPIC, question_type=QTYPE, notes=NOTES_TYPES,
        worked_solution=[f"{var[0].upper() + var[1:]}: **{right.lower()}**.",
                         "Give the full type — 'numerical' alone scored 0 (2023 course report, Q3(a))."],
        metadata={"options": opts},
        distractors=[{"value": "Numerical", "mistake": "not the full type — 'numerical' rather than 'discrete numerical' "
                                                       "or 'continuous numerical' (2023 course report, Q3(a))."}])


_SURVEYS = [
    ("An online survey link is emailed to voters in the Western Isles asking which party they will vote for. The results "
     "are used to predict the result across Scotland.",
     ["It is a local survey, not a national one — the Western Isles may vote differently from the rest of Scotland",
      "Not everyone has internet or email access, so some voters can't take part"],
     [("People might lie about who they will vote for", "not accepted in the 2023 marking instructions (Q3(b)) — it "
                                                       "isn't about who is in the sample."),
      ("The sample size is too small", "not accepted in the 2023 marking instructions (Q3(b))."),
      ("People might change their mind before the election", "not accepted in the 2023 marking instructions (Q3(b)).")]),
    ("A questionnaire about the library's opening hours is handed to everyone visiting Stornoway library on Tuesday "
     "mornings. The results are used to represent the views of the whole town.",
     ["Only people who already use the library on Tuesday mornings are asked — people at work or school are left out"],
     [("People might not tell the truth", "it isn't about who is in the sample (2023 marking instructions, Q3(b))."),
      ("The sample size is too small", "not accepted as a reason in the 2023 marking instructions (Q3(b)).")]),
]


def _q_representative():
    text, rights, wrongs = random.choice(_SURVEYS)
    right = random.choice(rights)
    wrong = random.sample(wrongs, min(2, len(wrongs)))
    opts = [right] + [w for w, _ in wrong]
    random.shuffle(opts)
    return Question(
        question_text=text + " Which is a valid reason why the results are not a representative sample?",
        correct_answer=right, topic=TOPIC, question_type=QTYPE, notes=NOTES_TYPES,
        worked_solution=[f"**{right}.**", "A valid reason is about WHO is in the sample — not everyone in the population "
                                          "had an equal chance of being included."],
        metadata={"options": opts}, distractors=[{"value": w, "mistake": m} for w, m in wrong])


_GATHER = [
    ("A radio station asks listeners how many hours they listen in one week in July, and uses the data to estimate "
     "listening hours last summer.",
     "Only one week in July — it doesn't represent the whole summer (extrapolation); the hours are also self-recorded",
     ("More people could be listening this year", "not a valid reason — many candidates gave it in 2025 (Q5(b), "
                                                  "course report).")),
    ("Beekeepers are asked to submit the number of hives they own in the National Hive Count.",
     "Some beekeepers might not take part, and the numbers are self-submitted, so they could contain errors",
     ("Some honeybees have died since the count", "not accepted in the 2026 marking instructions (Q11(a)).")),
    ("A newspaper draws a straight line through the last two years' puffin counts and claims 'No puffins by 2031!'.",
     "It is extrapolation — the line is carried far beyond the data and ignores the earlier data points",
     ("Puffins will breed, so they won't die out", "not accepted — 'bees will reproduce' scored 0 in the 2026 marking "
                                                   "instructions (Q11(b)); refer to the data or the graph.")),
    ("A vet will compare the proportion of sheep with ticks on two islands using a z-test for two proportions.",
     "The sheep in each sample must be chosen randomly",
     ("The two samples must be the same size", "not needed for proportions — a common wrong answer in 2022 (Q3(d), "
                                               "course report).")),
]


def _q_gathering():
    text, right, (wrong, why) = random.choice(_GATHER)
    extra = "The data was collected over a whole year, so it is too much data"
    opts = [right, wrong, extra]
    random.shuffle(opts)
    ask = ("Which is a valid design condition?" if "z-test" in text else
           "Which is a valid reason the data or claim may misrepresent the situation?")
    return Question(question_text=f"{text} {ask}", correct_answer=right, topic=TOPIC, question_type=QTYPE,
                    notes=NOTES_TYPES, worked_solution=[f"**{right}.**"], metadata={"options": opts},
                    distractors=[{"value": wrong, "mistake": why}])


def generate_data_distributions_types(calc_mode=False):
    return random.choice([_q_data_type, _q_data_type, _q_representative, _q_gathering])()


# ── Level 2: outliers ────────────────────────────────────────────────────────────────────────
_OUT_CONTEXTS = [("time", "minutes", "time, in minutes, shoppers spent in a supermarket", 25, 5.5, 1),
                 ("mass", "kg", "mass, in kg, of lambs at market", 40, 5, 1),
                 ("visitors", "visitors", "number of visitors each day to a tweed shop", 55, 7, 0),
                 ("wait", "minutes", "waiting time, in minutes, at a GP surgery", 18, 4, 1)]


def _sample(mu, sigma, n, dp):
    return [round(max(0.5, random.gauss(mu, sigma)), dp) for _ in range(n)]


def _q_outlier_limit():
    var, unit, what, mu, sig, dp = random.choice(_OUT_CONTEXTS)
    data = _sample(mu, sig, random.randint(30, 45), dp)
    data.append(round(mu + random.uniform(4, 6) * sig, dp))
    lines, s = _r_summary(var, data)
    q1, q3 = s[1], s[4]
    iqr = _r(q3 - q1, 4)
    upper = random.random() < 0.6
    lim = _r(q3 + 1.5 * iqr, 4) if upper else _r(q1 - 1.5 * iqr, 4)
    word = "upper" if upper else "lower"
    text = (f"The R output summarises the {what} (n = {len(data)}). Calculate the {word} limit for outliers "
            f"({'Q3 + 1.5 × IQR' if upper else 'Q1 − 1.5 × IQR'}).")
    wrong = [(_r(q3 + iqr if upper else q1 - iqr, 4), "you left out the 1.5: the limit is 1.5 × IQR beyond the quartile."),
             (_r(s[2] + 1.5 * iqr if upper else s[2] - 1.5 * iqr, 4), "start from the quartile, not the median."),
             (_r(q3 + 1.5 * (s[5] - s[0]) if upper else q1 - 1.5 * (s[5] - s[0]), 4),
              "use the interquartile range, not the range (2025 marking instructions, Q9(a)).")]
    return Question(
        question_text=text, correct_answer=lim, topic=TOPIC, question_type=QTYPE, notes=NOTES_OUTLIERS,
        scaffold_steps=[{"prompt": "IQR = Q3 − Q1", "answer": iqr},
                        {"prompt": "1.5 × IQR", "answer": _r(1.5 * iqr, 4)},
                        {"prompt": f"{word.capitalize()} limit ({unit})", "answer": lim}],
        worked_solution=[f"IQR = {_g(q3)} − {_g(q1)} = {_g(iqr, 4)}", f"1.5 × IQR = {_g(1.5 * iqr, 4)}",
                         f"{word.capitalize()} limit = {_g(q3 if upper else q1)} {'+' if upper else '−'} "
                         f"{_g(1.5 * iqr, 4)} = **{_g(lim, 4)} {unit}**",
                         f"Largest value {_g(s[5])}: {'an outlier' if s[5] > q3 + 1.5 * iqr else 'not an outlier'}."],
        metadata={"table": _code(lines)}, distractors=distractors(lim, wrong))


def _q_outlier_count():
    # n = 4k + 3 with ties at the quartile positions, so every quartile method gives the same answer
    k = random.choice([3, 4])
    n = 4 * k + 3
    while True:
        base = sorted(random.randint(20, 60) for _ in range(n))
        base[k] = base[k - 1]                     # Q1 = kth value (1-indexed) = (k+1)th
        base[3 * k + 2] = base[3 * k + 1]         # Q3 = (3k+2)th = (3k+3)th
        base = sorted(base)
        q1, q3 = base[k - 1], base[3 * k + 1]
        if base[k] != q1 or base[3 * k + 2] != q3 or q3 - q1 < 4:
            continue
        iqr = q3 - q1
        hi, lo = q3 + 1.5 * iqr, q1 - 1.5 * iqr
        n_out = random.choice([1, 2])
        extremes = [int(hi + random.randint(2, 12)) for _ in range(n_out)]
        if any(v <= hi for v in extremes):
            continue
        # replace the largest values with the outliers, keeping the quartile positions intact
        data = sorted(base[:-n_out] + extremes)
        if (_q7(data, .25), _q7(data, .75)) != (q1, q3):
            continue
        break
    count = sum(1 for v in data if v > hi or v < lo)
    text = (f"The ordered data are: {', '.join(map(str, data))}. Q1 = {q1} and Q3 = {q3}. How many of the values are "
            f"outliers?")
    return Question(
        question_text=text, correct_answer=float(count), topic=TOPIC, question_type=QTYPE, notes=NOTES_OUTLIERS,
        scaffold_steps=[{"prompt": "IQR", "answer": float(iqr)},
                        {"prompt": "Upper limit Q3 + 1.5 × IQR", "answer": _r(hi)},
                        {"prompt": "Number of outliers", "answer": float(count)}],
        worked_solution=[f"IQR = {q3} − {q1} = {iqr}", f"Limits: {q1} − {_g(1.5 * iqr)} = {_g(lo)} and {q3} + "
                         f"{_g(1.5 * iqr)} = {_g(hi)}", f"Values outside the limits: **{count}**"],
        distractors=distractors(float(count), [(float(sum(1 for v in data if v > q3 + iqr or v < q1 - iqr)),
                                                "you used Q3 + IQR — the limit is Q3 + 1.5 × IQR.")]))


_REMOVE = [("A data set of patients' ages contains the value −4.", "Remove it — it is an impossible value (a data entry "
            "error)", "Keep it — every value must stay in the data"),
           ("A data set of pupils' heights contains the value 17.2 m.", "Remove it — it is an impossible value (a data "
            "entry error)", "Keep it — it is an outlier, but outliers must always be kept"),
           ("A walker's age of 89 is an outlier in a data set of walkers' ages.", "Keep it — it is unusual but a "
            "genuine value", "Remove it — outliers must always be removed"),
           ("The number of visitors to a shop on the day a cruise ship called is an outlier.", "Keep it — it is a "
            "genuine value", "Remove it — outliers must always be removed")]


def _q_outlier_remove():
    text, right, wrong = random.choice(_REMOVE)
    opts = [right, wrong]
    random.shuffle(opts)
    return Question(question_text=text + " Should it be removed before the data are analysed?", correct_answer=right,
                    topic=TOPIC, question_type=QTYPE, notes=NOTES_OUTLIERS, worked_solution=[f"**{right}.**"],
                    metadata={"options": opts},
                    distractors=[{"value": wrong, "mistake": "remove a value only if it is impossible or an error; a "
                                                             "genuine extreme value stays in (course spec)."}])


def generate_data_distributions_outliers(calc_mode=False):
    return random.choice([_q_outlier_limit, _q_outlier_limit, _q_outlier_count, _q_outlier_remove])()


# ── Level 3: describing distributions ───────────────────────────────────────────────────────
_SHAPE_TEXT = {"normal": "Symmetric — approximately normally distributed",
               "right": "Skewed to the right (positively skewed)",
               "left": "Skewed to the left (negatively skewed)"}
_DESC_CONTEXTS = [("hours", "hours listened in one week", 6, 10, 3, 1),
                  ("time", "crossing time (minutes)", 150, 165, 4, 1),
                  ("mark", "test mark (%)", 50, 70, 8, 0),
                  ("late", "minutes late", 0, 12, 4, 0)]


def _skew(x):
    m = statistics.mean(x); s = statistics.stdev(x)
    return sum(((v - m) / s) ** 3 for v in x) / len(x)


def _shaped_data(shape, ctx):
    var, label, floor, centre, spread, dp = ctx
    for _ in range(200):
        n = random.randint(50, 70)
        if shape == "normal":
            x = [round(random.gauss(centre, spread), dp) for _ in range(n)]
        elif shape == "right":
            x = [round(floor + random.gammavariate(1.6, spread * 1.3), dp) for _ in range(n)]
        else:
            top = centre + 4 * spread
            x = [round(top - random.gammavariate(1.6, spread * 1.3), dp) for _ in range(n)]
        sk = _skew(x)
        if (shape == "normal" and abs(sk) < 0.25) or (shape == "right" and sk > 0.9) or (shape == "left" and sk < -0.9):
            return x
    raise RuntimeError("no data")


def _edges(x):
    lo, hi = min(x), max(x)
    span = hi - lo
    for w in (0.5, 1, 2, 2.5, 4, 5, 10, 20):
        if span / w <= 14:
            break
    a = math.floor(lo / w) * w
    e = [a]
    while e[-1] <= hi:
        e.append(round(e[-1] + w, 6))
    return e


def generate_data_distributions_describe(calc_mode=False):
    shape = random.choice(["normal", "right", "left"])
    ctx = random.choice(_DESC_CONTEXTS)
    var, label = ctx[0], ctx[1]
    x = _shaped_data(shape, ctx)
    lines, s = _r_summary(var, x)
    mo, mean7 = _r_one(f"mean({var})", statistics.mean(x))
    right = _SHAPE_TEXT[shape]
    opts = list(_SHAPE_TEXT.values()) + ["Unevenly distributed"]
    random.shuffle(opts)
    wrong_shape = [{"value": _SHAPE_TEXT[k], "mistake": "look at which side the long tail is on — most candidates "
                                                        "misdescribed the histogram in 2025 (Q5(a)(ii))."}
                   for k in _SHAPE_TEXT if k != shape]
    wrong_shape.append({"value": "Unevenly distributed", "mistake": "not a description of the shape (2025 course report)."})
    part_a = make_part("(a)", "Describe the distribution of the data shown in the histogram.", right, options=opts,
                       worked_solution=[f"**{right}.**"], distractors=wrong_shape)
    if shape == "normal":
        ans, other, mname, oname = mean7, s[2], "mean", "median"
    else:
        ans, other, mname, oname = s[2], mean7, "median", "mean"
    part_b = make_part(
        "(b)", "Hence state the appropriate measure of location.", ans,
        scaffold_steps=[{"prompt": f"Which measure: mean or median? Enter the {mname}.", "answer": ans}],
        worked_solution=[f"{'Symmetric (normal)' if shape == 'normal' else 'Skewed'} data → the **{mname}**: "
                         f"**{_g(ans, 4)}**",
                         f"(Not the {oname}, {_g(other, 4)} — the measure must match the shape: 2025 Q5(a)(iii).)"],
        distractors=distractors(ans, [(other, f"the {oname} isn't appropriate for "
                                              f"{'normal' if shape == 'normal' else 'skewed'} data (2025 marking "
                                              f"instructions, Q5(a)(iii)).")]))
    parts = [part_a, part_b]
    return Question(
        question_text=f"A data set of {len(x)} values ({label}) is shown in the histogram, with its R output.",
        correct_answer=parts[-1].correct_answer, topic=TOPIC, question_type=QTYPE, parts=parts,
        worked_solution=multipart_worked_solution(parts), notes=NOTES_DESCRIBE,
        metadata={"table": _code(lines + mo), **_diagram("histogram", x, _edges(x), label, "Histogram of the data")})


# ── Level 4: comparing data sets ────────────────────────────────────────────────────────────
_PAIRS = [("salmon", "Cage A", "Cage B", "mass", "kg", "heavier", "lighter", 4.6, 0.35, 2),
          ("mackerel", "Boat A", "Boat B", "length", "cm", "longer", "shorter", 33, 2.0, 1),
          ("swimmers", "Club A", "Club B", "50 m time", "s", "slower", "faster", 32, 1.6, 1),
          ("golf balls", "Current", "New", "distance", "m", "further", "less far", 270, 8.5, 1)]


def _q_compare_normal():
    what, A, B, meas, unit, more, less, mu, sig, dp = random.choice(_PAIRS)
    sa, sb = sig * random.uniform(0.6, 0.9), sig * random.uniform(1.2, 1.6)
    if random.random() < 0.5:
        sa, sb = sb, sa
    da = [round(random.gauss(mu * random.uniform(1.0, 1.05), sa), dp) for _ in range(30)]
    db = [round(random.gauss(mu * random.uniform(0.93, 0.98), sb), dp) for _ in range(30)]
    ma, mb = statistics.mean(da), statistics.mean(db)
    va, vb = statistics.stdev(da), statistics.stdev(db)
    out = (_r_one(f"mean({A[-1] if ' ' in A else A.lower()})", ma)[0] +
           _r_one(f"mean({B[-1] if ' ' in B else B.lower()})", mb)[0] +
           _r_one(f"sd({A[-1] if ' ' in A else A.lower()})", va)[0] +
           _r_one(f"sd({B[-1] if ' ' in B else B.lower()})", vb)[0])
    hiA = ma > mb
    big, small = (A, B) if hiA else (B, A)
    loc = (f"On average, the {what} from {big} are {more} than those from {small} (mean {_g(max(ma, mb))} {unit} "
           f"compared with {_g(min(ma, mb))} {unit})")
    cons, var_ = (A, B) if va < vb else (B, A)
    spr = (f"The {meas}s for {cons} are more consistent than for {var_} (standard deviation {_g(min(va, vb))} {unit} "
           f"compared with {_g(max(va, vb))} {unit})")
    bad_loc = f"The {what} from {big} are {more}"
    bad_loc2 = f"The {what} from {big} are {more}, shown by the higher mean"
    bad_spr = f"The {what} from {var_} are more varied"
    bad_spr2 = (f"The standard deviation is higher for {var_}, which shows that on average {var_} has a wider spread")
    pa = make_part("(a)", "Which is a valid comparison of LOCATION?", loc, options=random.sample([loc, bad_loc, bad_loc2], 3),
                   worked_solution=[f"**{loc}.**", "Say 'on average' and name the statistic with its values."],
                   distractors=[{"value": bad_loc, "mistake": "no 'on average' and no statistic — common in 2024 (Q6(a)(ii), "
                                                             "course report)."},
                                {"value": bad_loc2, "mistake": "not accepted in the 2024 marking instructions — say 'on "
                                                               "average' and give the means."}])
    pb = make_part("(b)", "Which is a valid comparison of SPREAD?", spr, options=random.sample([spr, bad_spr, bad_spr2], 3),
                   worked_solution=[f"**{spr}.**"],
                   distractors=[{"value": bad_spr, "mistake": "no statistic named — 'the new golf ball is more varied' was "
                                                             "common in 2024 (course report)."},
                                {"value": bad_spr2, "mistake": "not accepted in the 2024 marking instructions (spread "
                                                               "isn't 'on average')."}])
    parts = [pa, pb]
    return Question(
        question_text=f"Random samples of 30 {what} were measured ({meas}, in {unit}) for {A} and {B}. The data are "
                      f"approximately normally distributed. The R output is shown.",
        correct_answer=parts[-1].correct_answer, topic=TOPIC, question_type=QTYPE, parts=parts,
        worked_solution=multipart_worked_solution(parts), notes=NOTES_COMPARE, metadata={"table": _code(out)})


_BOX_CONTEXTS = [("Mass of lambs at 8 weeks (kg)", "Grass only", "Grass + supplement", 18, 3),
                 ("Mass of chicks at 3 weeks (g)", "Feed A", "Feed B", 250, 40),
                 ("Time to complete a puzzle (minutes)", "S1", "S6", 14, 3)]


def _q_compare_box():
    label, A, B, mid, u = random.choice(_BOX_CONTEXTS)
    while True:
        # the narrower box has the WIDER range — so 'smaller range' picks the wrong group (2025 Q9(a))
        q1a = mid - random.randint(1, 2) * u; q3a = q1a + random.randint(1, 2) * u          # small IQR
        q1b = mid - random.randint(2, 3) * u; q3b = q1b + random.randint(3, 4) * u          # large IQR
        mna, mxa = q1a - random.randint(2, 3) * u, q3a + random.randint(2, 3) * u
        mnb, mxb = q1b - random.randint(0, 1) * u - u // 2, q3b + u // 2
        iqa, iqb = q3a - q1a, q3b - q1b
        if iqa < iqb and (mxa - mna) > (mxb - mnb) and mnb > 0 and mna > 0:
            break
    meda = (q1a + q3a) // 2; medb = (q1b + q3b) // 2
    if random.random() < 0.5:
        groups = [[A, mna, q1a, meda, q3a, mxa], [B, mnb, q1b, medb, q3b, mxb]]
    else:
        groups = [[B, mnb, q1b, medb, q3b, mxb], [A, mna, q1a, meda, q3a, mxa]]
    right = f"{A}: its interquartile range is smaller ({iqa} compared with {iqb})"
    wrong = f"{B}: it has a smaller range ({mxb - mnb} compared with {mxa - mna})"
    wrong2 = f"{B}: its box plot is smaller"
    pa = make_part("(a)", "Explain which group has the least variability.", right,
                   options=random.sample([right, wrong, wrong2], 3), worked_solution=[f"**{right}.**"],
                   distractors=[{"value": wrong, "mistake": "'a smaller range' was not accepted in the 2025 marking "
                                                           "instructions (Q9(a)) — use the IQR."},
                                {"value": wrong2, "mistake": "'the boxplot is smaller' was not accepted (2025 marking "
                                                             "instructions, Q9(a))."}])
    pb = make_part("(b)", f"Find the interquartile range for {A}.", float(iqa),
                   scaffold_steps=[{"prompt": f"Upper quartile for {A}", "answer": float(q3a)},
                                   {"prompt": f"Lower quartile for {A}", "answer": float(q1a)},
                                   {"prompt": "IQR = Q3 − Q1", "answer": float(iqa)}],
                   worked_solution=[f"IQR = {q3a} − {q1a} = **{iqa}**"],
                   distractors=distractors(float(iqa), [(float(mxa - mna), "that's the range (maximum − minimum), not the "
                                                                           "interquartile range."),
                                                        (float(meda), "that's the median.")]))
    parts = [pa, pb]
    return Question(question_text=f"The comparative box plot shows {label.split(' (')[0].lower()} for two groups.",
                    correct_answer=parts[-1].correct_answer, topic=TOPIC, question_type=QTYPE, parts=parts,
                    worked_solution=multipart_worked_solution(parts), notes=NOTES_COMPARE,
                    metadata=_diagram("boxplots", groups, label, label.split(" (")[0]))


def generate_data_distributions_compare(calc_mode=False):
    return random.choice([_q_compare_normal, _q_compare_box])()


# ── Level 5: spreadsheet — frequency table (styled on 2025 Q12) ────────────────────────────
_YELLOW = PatternFill("solid", fgColor="FFF2CC")
_HEAD = PatternFill("solid", fgColor="1F3864")
_SURVEY_SETS = [("How do you usually travel to school?", "Travel method", ["Walk", "Bus", "Car", "Cycle"],
                 "Does your journey take more than 20 minutes?"),
                ("What is your eye colour?", "Eye colour", ["Blue", "Brown", "Green"], "Are you colour blind?"),
                ("Which island do you live on?", "Island", ["Lewis", "Harris", "Uist", "Barra"],
                 "Do you travel on a ferry at least once a month?")]


def _survey_workbook(sv, n, cats, years, yes_set, withdrawn, solved):
    q, head, levels, yq = sv
    wb = Workbook(); ws = wb.active; ws.title = "Survey"
    for c, w in zip("ABCDEFG", [12, 11, 15, 24, 3, 22, 12]):
        ws.column_dimensions[c].width = w
    ws["A1"] = "Survey responses"; ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Completed solution: the withdrawn participant's row is deleted; the frequencies are COUNTIF formulas."
                if solved else "Complete the 'Participant Responses' table and the 'Summary' table.")
    ws["A4"] = "Participant Responses"; ws["A4"].font = Font(bold=True)
    ws["F4"] = "Summary"; ws["F4"].font = Font(bold=True)
    for c, h in zip("ABCD", ["Participant", "Year group", head, yq]):
        ws[f"{c}5"] = h; ws[f"{c}5"].fill = _HEAD; ws[f"{c}5"].font = Font(bold=True, color="FFFFFF")
        ws[f"{c}5"].alignment = Alignment(wrap_text=True, horizontal="center")
    for c, h in zip("FG", [head, "Frequency"]):
        ws[f"{c}5"] = h; ws[f"{c}5"].fill = _HEAD; ws[f"{c}5"].font = Font(bold=True, color="FFFFFF")
    ids = [i for i in range(1, n + 1) if not (solved and i == withdrawn)]
    for r, i in enumerate(ids, start=6):
        ws[f"A{r}"] = i; ws[f"B{r}"] = years[i - 1]; ws[f"C{r}"] = cats[i - 1]; ws[f"D{r}"].fill = _YELLOW
        if solved:
            ws[f"D{r}"] = "yes" if i in yes_set else "no"
    last = 5 + len(ids)
    values, filled = {}, []
    if solved:
        filled += [f"D{r}" for r in range(6, last + 1)]
        for r, i in enumerate(ids, start=6):
            values[f"D{r}"] = "yes" if i in yes_set else "no"
    for k, lev in enumerate(levels):
        r = 6 + k
        ws[f"F{r}"] = lev; ws[f"G{r}"].fill = _YELLOW
        if solved:
            ws[f"G{r}"] = f"=COUNTIF($C$6:$C${last},F{r})"
            values[f"G{r}"] = sum(1 for i in ids if cats[i - 1] == lev); filled.append(f"G{r}")
    ws["F11"] = f"Number answering 'yes'"; ws["G11"].fill = _YELLOW
    if solved:
        ws["G11"] = f'=COUNTIF($D$6:$D${last},"yes")'
        values["G11"] = sum(1 for i in ids if i in yes_set); filled.append("G11")
        ch = BarChart(); ch.type = "col"; ch.title = f"{head} of participants"; ch.legend = None
        ch.x_axis.title = head; ch.y_axis.title = "Frequency"
        ch.add_data(Reference(ws, min_col=7, min_row=5, max_row=5 + len(levels)), titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=6, min_row=6, max_row=5 + len(levels)))
        ws.add_chart(ch, "F13")
    return wb, ws, values, filled, last


def generate_data_distributions_spreadsheet(calc_mode=False):
    sv = random.choice(_SURVEY_SETS)
    q, head, levels, yq = sv
    n = random.randint(26, 36)
    weights = [random.randint(1, 5) for _ in levels]
    cats = random.choices(levels, weights=weights, k=n)
    for k, lev in enumerate(levels):                 # every category appears at least once
        cats[k] = lev
    random.shuffle(cats)
    years = [f"S{random.randint(1, 6)}" for _ in range(n)]
    yes_set = sorted(random.sample(range(1, n + 1), random.randint(3, 6)))
    withdrawn = random.choice([i for i in range(8, n + 1) if i not in yes_set])
    wbq, _, _, _, _ = _survey_workbook(sv, n, cats, years, yes_set, withdrawn, False)
    wbs, wss, values, filled, last = _survey_workbook(sv, n, cats, years, yes_set, withdrawn, True)
    target_k = random.randrange(len(levels))
    if random.random() < 0.3:
        cell, ans = "G11", float(values["G11"])
        ask = "the number answering 'yes' (cell G11)"
        with_w = float(len(yes_set))
    else:
        cell, ans = f"G{6 + target_k}", float(values[f"G{6 + target_k}"])
        ask = f"the frequency of '{levels[target_k]}' (cell {cell})"
        with_w = float(sum(1 for c in cats if c == levels[target_k]))
    text = (f"A random sample of {n} pupils answered: '{q}' and '{yq} (yes / no)'. Participants "
            f"{', '.join(map(str, yes_set[:-1]))} and {yes_set[-1]} answered 'yes'; all others answered 'no'. "
            f"Participant {withdrawn} has withdrawn their consent. Download the spreadsheet, delete participant "
            f"{withdrawn}'s row, complete column D, and use COUNTIF to complete the Summary table. Give {ask}.")
    return Question(
        question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE, notes=NOTES_SHEET,
        scaffold_steps=[{"prompt": "How many participants remain after the withdrawal?", "answer": float(n - 1)},
                        {"prompt": f"Answer for {cell}", "answer": ans}],
        worked_solution=[f"Delete row {5 + withdrawn} (participant {withdrawn}) — delete, don't hide.",
                         f"G6: =COUNTIF($C$6:$C${last},F6), filled down; G11: =COUNTIF($D$6:$D${last},\"yes\")",
                         f"{cell} = **{int(ans)}**", "Chart the categorical data with a bar chart or pie chart, with a "
                                                     "title and axis labels (2025 Q12(c))."],
        metadata={"spreadsheet_bytes": workbook_bytes(wbq), "spreadsheet_filename": "survey_responses.xlsx",
                  "spreadsheet_answer_cell": ("Survey", cell),
                  **solution_metadata(wbs, wss, values, filled, min_row=5, max_row=last, max_col=7,
                                      filename="survey_responses_solution.xlsx")},
        distractors=distractors(ans, [(with_w, f"participant {withdrawn}'s response is still being counted — delete the "
                                               f"row (2025 course report, Q12(b)).")]))


# Calculator Questions level (house layout for a topic with spreadsheet questions), weighted by
# past-paper marks: types/sampling 2022 Q3(a,b,d,e) + 2023 Q3 + 2025 Q5(b) + 2026 Q11(a,b) ≈ 11;
# describing 2025 Q5(a) = 4; comparing 2024 Q6(a) + 2025 Q9(a) = 5; outliers not yet examined
_CALCULATOR_MIX = [(generate_data_distributions_types, 4), (generate_data_distributions_outliers, 1),
                   (generate_data_distributions_describe, 2), (generate_data_distributions_compare, 2)]


def generate_data_distributions_calculator(calc_mode=False):
    gens, weights = zip(*_CALCULATOR_MIX)
    return random.choices(gens, weights=weights)[0]()


def generate_data_distributions_question(calc_mode=False):
    return random.choice([generate_data_distributions_calculator, generate_data_distributions_spreadsheet])()
