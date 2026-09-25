import random
from core.models.question_model import Question
from core.models.time_bar import time_bar_segments, time_bar_steps
from topics.numeracy.time_conversion import _hm_string


def _fmt(x):
    """Plain decimal string — never scientific notation, no trailing zeros."""
    s = f"{round(x, 6):.6f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def _num(x):
    x = round(x, 6)
    return int(x) if x == int(x) else x


def _clock(total_minutes):
    h, m = divmod(total_minutes % 1440, 60)
    return f"{h:02d}:{m:02d}"


def _bar_scaffold(start, end, mode):
    """The time-bar steps (core.models.time_bar) as scaffold steps."""
    steps = []
    for step in time_bar_steps(start, end, mode):
        s = {"prompt": step["prompt"], "answer": step["answer"]}
        if step["kind"] == "duration":
            s["answer_type"] = "duration"
        steps.append(s)
    return steps


def _bar_lines(start, end, mode):
    """One worked-solution line counting through the time bar, e.g.
    '10:48 → 11:00 = 12 min;  11:00 + 3 hours = 14:00;  14:00 + 5 min = 14:05'."""
    segs = time_bar_segments(start, end)
    size = lambda a, b: f"{(b - a) // 60} hour{'s' if b - a != 60 else ''}" if (b - a) % 60 == 0 else f"{b - a} min"
    if mode == "interval":
        return ";  ".join(f"{_clock(a)} → {_clock(b)} = {size(a, b)}" for a, b, _ in segs)
    if mode == "forward":
        parts = []
        for k, (a, b, kind) in enumerate(segs):
            if k == 0 and kind == "lead":
                parts.append(f"{_clock(a)} → {_clock(b)} = {size(a, b)}")
            else:
                parts.append(f"{_clock(a)} + {size(a, b)} = {_clock(b)}")
        return ";  ".join(parts)
    parts = []
    for k, (a, b, kind) in enumerate(reversed(segs)):
        if k == 0 and kind == "tail":
            parts.append(f"{_clock(b)} back to {_clock(a)} = {size(a, b)}")
        else:
            parts.append(f"{_clock(b)} − {size(a, b)} = {_clock(a)}")
    return ";  ".join(parts)


def _bar_meta(start, end, mode, start_label="", end_label="", ask_total=False):
    """`ask_total`: the time to add/take away is worked out in the question (T = D ÷ S, plus any
    delay), so the widget makes the pupil find it instead of showing it."""
    return {"diagram": "time_bar",
            "diagram_params": {"start": start, "end": end, "mode": mode, "start_label": start_label,
                               "end_label": end_label, "ask_total": ask_total}}


NOTES_FORMULA = """
**The Three Formulas:**

**D = S × T**  **S = D ÷ T**  **T = D ÷ S**

(D = distance, S = speed, T = time)

Write down what you know and what you want to find, then choose the formula that gives what
you want.

**Example:** A CalMac ferry travels 78 km at an average speed of 24 km/h. How long does the
crossing take?
- Know: D = 78 km, S = 24 km/h.  Want: T  →  use T = D ÷ S
- T = 78 ÷ 24 = 3.25
- **The crossing takes 3.25 hours.**
"""

NOTES_HOURS_MINUTES = """
**Speed, Distance and Time — Hours and Minutes:**

A time must be a **decimal number of hours** before it goes into a formula.

- Minutes → decimal hours: **÷ 60** (e.g. 45 minutes = 45 ÷ 60 = 0.75 hours)
- Decimal hours → minutes: multiply the decimal part **× 60** (e.g. 0.4 hours = 24 minutes)

**Example 1:** A ferry sails 51 km at an average speed of 12 km/h. How long does the crossing
take? Give your answer in hours and minutes.
- T = D ÷ S = 51 ÷ 12 = 4.25 hours
- 0.25 × 60 = 15 minutes
- **The crossing takes 4 hours 15 minutes.**

**Example 2:** A bus travels for 2 hours 45 minutes at an average speed of 48 km/h. How far does
it travel?
- 45 minutes = 45 ÷ 60 = 0.75 hours, so T = 2.75 hours
- D = S × T = 48 × 2.75 = 132
- **The bus travels 132 km.**
"""

NOTES_CLOCK = """
**Departure and Arrival Times:**

**Finding an arrival time:** find the journey time with T = D ÷ S, change it into hours and
minutes, then add it on to the departure time.

**Finding a speed from two clock times:** count up from the departure time to the arrival time
to get the journey time, change it into a decimal number of hours, then use S = D ÷ T.

**Example:** A bus leaves Stornoway at 09:40 and travels 54 km at 40 km/h. When does it arrive?
- T = 54 ÷ 40 = 1.35 hours
- 0.35 × 60 = 21 → 1 hour 21 minutes
- 09:40 + 1 hour 21 minutes = **11:01**
"""

NOTES_UNITS = """
**Converting Distance Units:**

**1 km = 1000 m  1 m = 100 cm  1 cm = 10 mm**

The distance unit must match the distance unit in the speed — a speed in m/s needs a distance
in metres, a speed in cm/s needs a distance in centimetres, and so on.

- Bigger unit → smaller unit: **multiply**
- Smaller unit → bigger unit: **divide**

**Example 1:** A runner runs at an average speed of 5 m/s. How long does it take her to run 3 km?
- The speed is in m/s, so change km to m: 3 km = 3 × 1000 = 3000 m
- T = D ÷ S = 3000 ÷ 5 = 600
- **It takes her 600 seconds.**

**Example 2:** A snail crawls 36 mm in 12 seconds. Calculate its average speed in cm/s.
- The answer is needed in cm/s, so change mm to cm: 36 mm = 36 ÷ 10 = 3.6 cm
- S = D ÷ T = 3.6 ÷ 12 = 0.3
- **The snail's average speed is 0.3 cm/s.**
"""


# ---------------------------------------------------------------------------
# Level 1 — Choosing and using the correct formula (whole/half hours)
# ---------------------------------------------------------------------------

# who/ref: subject, and how to refer back to it; speeds: (calculator, non-calculator) choices
_L1_CONTEXTS = [
    {"who": "A CalMac ferry", "ref": "the ferry", "trip": "crossing", "unit": "km/h", "tunit": "hours",
     "speeds": (range(12, 31), [12, 15, 20, 25, 30])},
    {"who": "A cyclist on the Hebridean Way", "ref": "the cyclist", "trip": "ride", "unit": "km/h", "tunit": "hours",
     "speeds": (range(12, 25), [12, 14, 15, 16, 18, 20])},
    {"who": "A car", "ref": "the car", "trip": "journey", "unit": "km/h", "tunit": "hours",
     "speeds": (range(40, 91), [40, 50, 60, 70, 80, 90])},
    {"who": "A lorry", "ref": "the lorry", "trip": "journey", "unit": "km/h", "tunit": "hours",
     "speeds": (range(40, 71), [40, 50, 60, 70])},
    {"who": "A hillwalker", "ref": "the hillwalker", "trip": "walk", "unit": "km/h", "tunit": "hours",
     "speeds": ([3, 3.5, 4, 4.5, 5, 5.5, 6], [3, 4, 5, 6])},
    {"who": "A fishing boat", "ref": "the boat", "trip": "trip", "unit": "km/h", "tunit": "hours",
     "speeds": (range(8, 21), [8, 10, 12, 15, 20])},
    {"who": "A plane", "ref": "the plane", "trip": "flight", "unit": "km/h", "tunit": "hours",
     "speeds": (range(150, 321, 10), [150, 200, 250, 300])},
    {"who": "A coach", "ref": "the coach", "trip": "journey", "unit": "mph", "tunit": "hours",
     "speeds": (range(30, 61), [30, 40, 45, 50, 60])},
]

_L1_HOURS = ([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5], [1, 1.5, 2, 2.5, 3, 4])

_DIST_UNIT = {"km/h": "km", "mph": "miles", "m/s": "m"}


def _l1_runner(calc_mode):
    speed = random.choice([4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8] if not calc_mode else [4, 5, 6, 8])
    time = random.choice(range(20, 201, 5) if not calc_mode else range(20, 101, 10))
    return {"who": "A runner", "ref": "the runner", "trip": "run", "unit": "m/s", "tunit": "seconds"}, speed, time


def generate_sdt_l1(calc_mode=False):
    """Choose the correct formula; times are whole or half hours (or seconds for m/s)."""
    if random.random() < 0.2:
        ctx, speed, time = _l1_runner(calc_mode)
    else:
        ctx = random.choice(_L1_CONTEXTS)
        speed = random.choice(list(ctx["speeds"][1 if calc_mode else 0]))
        time = random.choice(_L1_HOURS[1 if calc_mode else 0])
    distance = _num(speed * time)
    dunit = _DIST_UNIT[ctx["unit"]]
    unknown = random.choice(["distance", "speed", "time"])

    if unknown == "distance":
        q = (f"{ctx['who']} travels at an average speed of {_fmt(speed)} {ctx['unit']} for "
             f"{_fmt(time)} {ctx['tunit']}.\n\nHow far does {ctx['ref']} travel, in {dunit}?")
        formula, calc, answer, ans_unit = "D = S × T", f"{_fmt(speed)} × {_fmt(time)}", distance, dunit
    elif unknown == "speed":
        q = (f"{ctx['who']} travels {_fmt(distance)} {dunit} in {_fmt(time)} {ctx['tunit']}.\n\n"
             f"Calculate the average speed of {ctx['ref']} in {ctx['unit']}.")
        formula, calc, answer, ans_unit = "S = D ÷ T", f"{_fmt(distance)} ÷ {_fmt(time)}", speed, ctx["unit"]
    else:
        q = (f"{ctx['who']} travels {_fmt(distance)} {dunit} at an average speed of "
             f"{_fmt(speed)} {ctx['unit']}.\n\nHow long does the {ctx['trip']} take, in {ctx['tunit']}?")
        formula, calc, answer, ans_unit = "T = D ÷ S", f"{_fmt(distance)} ÷ {_fmt(speed)}", time, ctx["tunit"]

    scaffold_steps = [
        {"prompt": "Which quantity are you finding — distance, speed or time?", "answer": unknown},
        {"prompt": f"Use {formula} to calculate the {unknown}", "answer": answer},
    ]
    worked = [
        f"Finding the {unknown}, so use **{formula}**",
        f"{formula[0]} = {calc} = {_fmt(answer)}",
        f"**The {unknown} is {_fmt(answer)} {ans_unit}.**",
    ]
    return Question(
        question_text=q,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Speed, Distance and Time",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_FORMULA,
    )


# ---------------------------------------------------------------------------
# Level 2 — Hours and minutes (answer in h/min, or a given h/min time to convert)
# ---------------------------------------------------------------------------

_L2_CONTEXTS = [
    {"who": "A ferry", "ref": "the ferry", "verb": "sails", "trip": "crossing", "speeds": (range(12, 33), [12, 15, 16, 20, 24, 30])},
    {"who": "A cyclist", "ref": "the cyclist", "verb": "rides", "trip": "ride", "speeds": (range(12, 25), [12, 15, 16, 18, 20, 24])},
    {"who": "A delivery van", "ref": "the van", "verb": "travels", "trip": "journey", "speeds": (range(30, 71), [30, 40, 48, 50, 60])},
    {"who": "A hillwalker", "ref": "the hillwalker", "verb": "walks", "trip": "walk", "speeds": (range(3, 7), [3, 4, 5, 6])},
    {"who": "A train", "ref": "the train", "verb": "travels", "trip": "journey", "speeds": (range(60, 121), [60, 80, 90, 100, 120])},
    {"who": "A yacht", "ref": "the yacht", "verb": "sails", "trip": "voyage", "speeds": (range(8, 19), [8, 10, 12, 15])},
    {"who": "A bus", "ref": "the bus", "verb": "travels", "trip": "journey", "speeds": (range(30, 61), [30, 40, 45, 48, 60])},
]


def _journey(calc_mode, speeds, min_lo=30, min_hi=330):
    """Pick (speed, total_minutes) so the time is not a whole number of hours, the decimal
    time terminates (minutes a multiple of 3, or 6/15 for non-calc) and the distance comes out
    to at most 1 d.p."""
    step_ok = (lambda m: m % 15 == 0 or m % 6 == 0) if calc_mode else (lambda m: m % 3 == 0)
    mins = [m for m in range(min_lo, min_hi + 1) if m % 60 and step_ok(m)]
    for _ in range(500):
        speed = random.choice(list(speeds))
        total = random.choice(mins)
        if (speed * total * 10) % 60 == 0:
            return speed, total
    return 20, 135


def generate_sdt_l2(calc_mode=False):
    ctx = random.choice(_L2_CONTEXTS)
    speed, total = _journey(calc_mode, ctx["speeds"][1 if calc_mode else 0])
    hours = total / 60
    whole, mins = divmod(total, 60)
    distance = _num(speed * hours)
    hm = _hm_string(total)
    variant = random.choice(["find_time", "find_distance", "find_speed"])

    if variant == "find_time":
        q = (f"{ctx['who']} {ctx['verb']} {_fmt(distance)} km at an average speed of {speed} km/h.\n\n"
             f"How long does the {ctx['trip']} take? Give your answer in hours and minutes.")
        dec_part = round(hours - whole, 4)
        scaffold_steps = [
            {"prompt": "Use T = D ÷ S to find the time as a decimal number of hours",
             "answer": _num(hours)},
            {"prompt": "Multiply the decimal part by 60 to find the minutes", "answer": mins},
            {"prompt": "Write the time in hours and minutes", "answer": hm, "answer_type": "duration"},
        ]
        worked = [
            f"T = D ÷ S = {_fmt(distance)} ÷ {speed} = {_fmt(hours)} hours",
            f"{_fmt(dec_part)} × 60 = {mins} minutes",
            f"**The {ctx['trip']} takes {hm}.**",
        ]
        return Question(
            question_text=q, correct_answer=hm, topic="Numeracy",
            question_type="Speed, Distance and Time", scaffold_steps=scaffold_steps,
            worked_solution=worked, notes=NOTES_HOURS_MINUTES,
            metadata={"answer_type": "duration"},
        )

    mins_dec = round(mins / 60, 4)
    convert_steps = [
        {"prompt": f"Change {mins} minutes into a decimal number of hours", "answer": mins_dec},
        {"prompt": f"Write {hm} as a decimal number of hours", "answer": _num(hours)},
    ]
    convert_lines = [
        f"{mins} minutes = {mins} ÷ 60 = {_fmt(mins_dec)} hours, so T = {_fmt(hours)} hours",
    ]
    if variant == "find_distance":
        q = (f"{ctx['who']} {ctx['verb']} at an average speed of {speed} km/h for {hm}.\n\n"
             f"How far does {ctx['ref']} travel, in km?")
        answer, unit = distance, "km"
        convert_steps.append({"prompt": "Use D = S × T to find the distance", "answer": distance})
        convert_lines += [f"D = S × T = {speed} × {_fmt(hours)} = {_fmt(distance)}",
                          f"**{ctx['ref'].capitalize()} travels {_fmt(distance)} km.**"]
    else:
        q = (f"{ctx['who']} {ctx['verb']} {_fmt(distance)} km in {hm}.\n\n"
             f"Calculate the average speed of {ctx['ref']} in km/h.")
        answer, unit = speed, "km/h"
        convert_steps.append({"prompt": "Use S = D ÷ T to find the speed", "answer": speed})
        convert_lines += [f"S = D ÷ T = {_fmt(distance)} ÷ {_fmt(hours)} = {speed}",
                          f"**The average speed is {speed} km/h.**"]

    return Question(
        question_text=q, correct_answer=answer, topic="Numeracy",
        question_type="Speed, Distance and Time", scaffold_steps=convert_steps,
        worked_solution=convert_lines, notes=NOTES_HOURS_MINUTES,
    )


# ---------------------------------------------------------------------------
# Level 3 — Departure and arrival times
# ---------------------------------------------------------------------------

# `mins`: a realistic range for the journey time, so distances stay plausible for the real route.
_L3_ROUTES = [
    {"who": "A bus", "from": "Stornoway", "to": "Tarbert", "speeds": (range(35, 56), [40, 45, 50]), "mins": (60, 100)},
    {"who": "A bus", "from": "Stornoway", "to": "Leverburgh", "speeds": (range(35, 56), [40, 45, 50]), "mins": (100, 150)},
    {"who": "The ferry", "from": "Oban", "to": "Castlebay", "speeds": (range(28, 37), [30, 32, 36]), "mins": (270, 310)},
    {"who": "The ferry", "from": "Ullapool", "to": "Stornoway", "speeds": (range(28, 37), [30, 32, 36]), "mins": (145, 175)},
    {"who": "A coach", "from": "Inverness", "to": "Ullapool", "speeds": (range(45, 66), [50, 60]), "mins": (80, 110)},
    {"who": "A train", "from": "Glasgow", "to": "Mallaig", "speeds": (range(45, 56), [45, 50]), "mins": (300, 340)},
]


def generate_sdt_l3(calc_mode=False):
    route = random.choice(_L3_ROUTES)
    speed, total = _journey(calc_mode, route["speeds"][1 if calc_mode else 0], *route["mins"])
    hours = total / 60
    distance = _num(speed * hours)
    hm = _hm_string(total)
    depart = random.randrange(6 * 60, 16 * 60 + 1, 5)
    arrive = depart + total
    whole, mins = divmod(total, 60)

    if random.random() < 0.5:
        q = (f"{route['who']} leaves {route['from']} at {_clock(depart)} and travels "
             f"{_fmt(distance)} km to {route['to']} at an average speed of {speed} km/h.\n\n"
             f"At what time does it arrive in {route['to']}? Give your answer as a 24-hour time, "
             f"e.g. 09:05.")
        scaffold_steps = [
            {"prompt": "Use T = D ÷ S to find the journey time as a decimal number of hours",
             "answer": _num(hours)},
            {"prompt": "Write the journey time in hours and minutes", "answer": hm,
             "answer_type": "duration"},
            {"prompt": f"Add the journey time on to {_clock(depart)}", "answer": _clock(arrive)},
        ]
        worked = [
            f"T = D ÷ S = {_fmt(distance)} ÷ {speed} = {_fmt(hours)} hours",
            f"{_fmt(round(hours - whole, 4))} × 60 = {mins}, so the journey takes {hm}",
            f"{_clock(depart)} + {hm} = {_clock(arrive)}",
            f"**It arrives in {route['to']} at {_clock(arrive)}.**",
        ]
        answer = _clock(arrive)
        bar = _bar_meta(depart, arrive, "forward", f"Leaves {route['from']}", f"Arrives {route['to']}",
                        ask_total=True)
    else:
        q = (f"{route['who']} leaves {route['from']} at {_clock(depart)} and arrives in "
             f"{route['to']} at {_clock(arrive)}. The journey is {_fmt(distance)} km.\n\n"
             f"Calculate the average speed in km/h.")
        scaffold_steps = [
            {"prompt": "How long does the journey take?", "answer": hm, "answer_type": "duration"},
            {"prompt": "Write the journey time as a decimal number of hours", "answer": _num(hours)},
            {"prompt": "Use S = D ÷ T to find the speed", "answer": speed},
        ]
        worked = [
            f"{_clock(depart)} to {_clock(arrive)} = {hm}",
            f"{mins} ÷ 60 = {_fmt(round(mins / 60, 4))}, so T = {_fmt(hours)} hours",
            f"S = D ÷ T = {_fmt(distance)} ÷ {_fmt(hours)} = {speed}",
            f"**The average speed is {speed} km/h.**",
        ]
        answer = speed
        bar = _bar_meta(depart, arrive, "interval", f"Leaves {route['from']}", f"Arrives {route['to']}")

    return Question(
        question_text=q, correct_answer=answer, topic="Numeracy",
        question_type="Speed, Distance and Time", scaffold_steps=scaffold_steps,
        worked_solution=worked, notes=NOTES_CLOCK, metadata=bar,
    )


# ---------------------------------------------------------------------------
# Level 4 — Converting distance units (adjacent units only: km/m, m/cm, cm/mm)
# ---------------------------------------------------------------------------

# `mult`: how many of the speed's distance unit make one `other` unit.
_L4_CONTEXTS = [
    {"who": "A runner", "ref": "the runner", "verb": "runs", "sunit": "m", "other": "km", "mult": 1000,
     "speeds": ([3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8], [3, 4, 5, 6, 8]), "times": (range(100, 1201, 20), range(100, 1001, 100))},
    {"who": "A drone", "ref": "the drone", "verb": "flies", "sunit": "m", "other": "km", "mult": 1000,
     "speeds": (range(5, 16), [5, 6, 8, 10, 12]), "times": (range(60, 601, 20), range(100, 601, 100))},
    {"who": "A swimmer", "ref": "the swimmer", "verb": "swims", "sunit": "m", "other": "km", "mult": 1000,
     "speeds": ([1, 1.2, 1.4, 1.5, 1.6, 1.8, 2], [1, 1.5, 2]), "times": (range(100, 1001, 50), range(100, 1001, 100))},
    {"who": "A robot vacuum cleaner", "ref": "the robot vacuum cleaner", "verb": "moves", "sunit": "cm", "other": "m", "mult": 100,
     "speeds": (range(15, 41), [15, 20, 25, 30, 40]), "times": (range(8, 61, 2), range(10, 61, 10))},
    {"who": "A conveyor belt in a fish processing plant", "ref": "the conveyor belt", "verb": "moves", "sunit": "cm", "other": "m", "mult": 100,
     "speeds": (range(20, 51, 5), [20, 25, 30, 40, 50]), "times": (range(10, 61, 2), range(10, 61, 10))},
    {"who": "A toy car", "ref": "the toy car", "verb": "travels", "sunit": "cm", "other": "m", "mult": 100,
     "speeds": (range(20, 81, 5), [20, 30, 40, 50, 60]), "times": (range(4, 31), range(5, 31, 5))},
    {"who": "A snail", "ref": "the snail", "verb": "crawls", "sunit": "mm", "other": "cm", "mult": 10,
     "speeds": ([0.5, 1, 1.5, 2, 2.5, 3], [1, 1.5, 2, 3]), "times": (range(20, 241, 4), range(20, 201, 20))},
    {"who": "A caterpillar", "ref": "the caterpillar", "verb": "crawls", "sunit": "mm", "other": "cm", "mult": 10,
     "speeds": ([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5], [2, 3, 4, 5]), "times": (range(20, 241, 4), range(20, 201, 20))},
    {"who": "The nozzle of a 3D printer", "ref": "the nozzle", "verb": "moves", "sunit": "cm", "other": "mm", "mult": 0.1,
     "speeds": ([2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 8], [2, 3, 4, 5]), "times": (range(4, 31), range(5, 31, 5))},
    {"who": "An ant", "ref": "the ant", "verb": "scurries", "sunit": "cm", "other": "mm", "mult": 0.1,
     "speeds": ([1.5, 2, 2.5, 3, 3.5, 4], [2, 3, 4]), "times": (range(5, 41), range(5, 41, 5))},
]


def _convert_line(value, frm, to, mult):
    if mult >= 1:
        return f"{_fmt(value)} {frm} = {_fmt(value)} × {_fmt(mult)} = {_fmt(value * mult)} {to}"
    div = round(1 / mult)
    return f"{_fmt(value)} {frm} = {_fmt(value)} ÷ {div} = {_fmt(value * mult)} {to}"


def generate_sdt_l4(calc_mode=False):
    ctx = random.choice(_L4_CONTEXTS)
    idx = 1 if calc_mode else 0
    speed = random.choice(list(ctx["speeds"][idx]))
    time = random.choice(list(ctx["times"][idx]))
    d_s = _num(speed * time)                   # distance in the speed's unit
    d_o = _num(d_s / ctx["mult"])              # distance in the adjacent unit
    su, ou = ctx["sunit"], ctx["other"]
    sp = f"{_fmt(speed)} {su}/s"
    variant = random.choice(["find_distance", "find_time", "find_speed"])

    if variant == "find_distance":
        q = (f"{ctx['who']} {ctx['verb']} at an average speed of {sp} for {time} seconds.\n\n"
             f"How far does {ctx['ref']} travel? Give your answer in {ou}.")
        scaffold_steps = [
            {"prompt": f"Use D = S × T to find the distance in {su}", "answer": d_s},
            {"prompt": f"Convert your answer into {ou}", "answer": d_o},
        ]
        worked = [
            f"D = S × T = {_fmt(speed)} × {time} = {_fmt(d_s)} {su}",
            _convert_line(d_s, su, ou, 1 / ctx["mult"]),
            f"**{ctx['ref'].capitalize()} travels {_fmt(d_o)} {ou}.**",
        ]
        answer = d_o
    elif variant == "find_time":
        q = (f"{ctx['who']} {ctx['verb']} at an average speed of {sp}.\n\n"
             f"How long does it take {ctx['ref']} to travel {_fmt(d_o)} {ou}? Give your answer in seconds.")
        scaffold_steps = [
            {"prompt": f"Convert {_fmt(d_o)} {ou} into {su}", "answer": d_s},
            {"prompt": "Use T = D ÷ S to find the time in seconds", "answer": time},
        ]
        worked = [
            _convert_line(d_o, ou, su, ctx["mult"]),
            f"T = D ÷ S = {_fmt(d_s)} ÷ {_fmt(speed)} = {time}",
            f"**It takes {ctx['ref']} {time} seconds.**",
        ]
        answer = time
    else:
        q = (f"{ctx['who']} {ctx['verb']} {_fmt(d_o)} {ou} in {time} seconds.\n\n"
             f"Calculate the average speed of {ctx['ref']} in {su}/s.")
        scaffold_steps = [
            {"prompt": f"Convert {_fmt(d_o)} {ou} into {su}", "answer": d_s},
            {"prompt": f"Use S = D ÷ T to find the speed in {su}/s", "answer": speed},
        ]
        worked = [
            _convert_line(d_o, ou, su, ctx["mult"]),
            f"S = D ÷ T = {_fmt(d_s)} ÷ {time} = {_fmt(speed)}",
            f"**The average speed is {sp}.**",
        ]
        answer = speed

    return Question(
        question_text=q, correct_answer=answer, topic="Numeracy",
        question_type="Speed, Distance and Time", scaffold_steps=scaffold_steps,
        worked_solution=worked, notes=NOTES_UNITS,
    )


# ---------------------------------------------------------------------------
# Level 5 — Time intervals (time bar: start → next o'clock → last o'clock → finish)
# ---------------------------------------------------------------------------

NOTES_TIME_INTERVALS = """
**Time Intervals — the Time Bar:**

Draw a time bar and split it at: the **start time** → the **next o'clock** → the **last o'clock
before the finish** → the **finish time**.

- Step 1: the minutes up to the next o'clock
- Step 2: the whole hours
- Step 3: the minutes after the last o'clock
- Add the pieces together

To **find a finish time**, add the pieces on in that order. To **find a start time**, work
backwards from the finish time in the same way.

**Example 1:** The ferry leaves Oban at 07:35 and arrives in Castlebay at 12:20. How long does
the crossing take?

[[time_bar 07:35-12:20 interval | Leaves Oban | Arrives Castlebay]]

- Step 1:  07:35 → 08:00 = 25 minutes
- Step 2:  08:00 → 12:00 = 4 hours
- Step 3:  12:00 → 12:20 = 20 minutes
- Total = 25 min + 4 hours + 20 min.  **The crossing takes 4 hours 45 minutes.**

**Example 2:** A train leaves Glasgow at 10:48. The journey to Oban takes 3 hours 17 minutes.
What time does the train arrive in Oban?

[[time_bar 10:48-14:05 forward | Leaves Glasgow | Arrives Oban]]

- Step 1:  10:48 → 11:00 = 12 minutes.  Time still to add: 3 h 17 min − 12 min = 3 h 5 min
- Step 2:  11:00 + 3 hours = 14:00.  Time still to add: 5 min
- Step 3:  14:00 + 5 minutes = 14:05
- **The train arrives in Oban at 14:05.**

**Example 3:** A family must check in at Glasgow Airport by 14:10. The drive from Fort William
takes 2 hours 25 minutes. What is the latest time they can leave Fort William?

[[time_bar 11:45-14:10 backward | Leave Fort William | Check in at airport]]

- Work backwards from 14:10.
- Step 1:  14:10 → back to 14:00 = 10 minutes.  Time still to take away: 2 h 25 min − 10 min = 2 h 15 min
- Step 2:  14:00 − 2 hours = 12:00.  Time still to take away: 15 min
- Step 3:  12:00 − 15 minutes = 11:45
- **The latest they can leave is 11:45.**
"""

# `mins`: realistic range for the time taken; `starts`: (earliest, latest) start, minutes after
# midnight; `overnight`: allowed to run past midnight.
_L5_CONTEXTS = [
    {"who": "The ferry", "ref": "the ferry", "leave": "leaves Oban", "arrive": "arrives in Castlebay",
     "leave_q": "leave Oban", "arrive_q": "arrive in Castlebay", "trip": "the crossing", "trip_a": "a crossing",
     "mins": (265, 315), "starts": (360, 840), "labels": ("Leaves Oban", "Arrives Castlebay")},
    {"who": "The ferry", "ref": "the ferry", "leave": "leaves Ullapool", "arrive": "arrives in Stornoway",
     "leave_q": "leave Ullapool", "arrive_q": "arrive in Stornoway", "trip": "the crossing", "trip_a": "a crossing",
     "mins": (145, 175), "starts": (360, 1080), "labels": ("Leaves Ullapool", "Arrives Stornoway")},
    {"who": "A bus", "ref": "the bus", "leave": "leaves Portree", "arrive": "arrives in Inverness",
     "leave_q": "leave Portree", "arrive_q": "arrive in Inverness", "trip": "the journey", "trip_a": "a journey",
     "mins": (170, 215), "starts": (360, 960), "labels": ("Leaves Portree", "Arrives Inverness")},
    {"who": "A train", "ref": "the train", "leave": "leaves Glasgow", "arrive": "arrives in Mallaig",
     "leave_q": "leave Glasgow", "arrive_q": "arrive in Mallaig", "trip": "the journey", "trip_a": "a journey",
     "mins": (300, 345), "starts": (360, 900), "labels": ("Leaves Glasgow", "Arrives Mallaig")},
    {"who": "A plane", "ref": "the plane", "leave": "leaves Glasgow", "arrive": "lands in Tenerife",
     "leave_q": "leave Glasgow", "arrive_q": "land in Tenerife", "trip": "the flight", "trip_a": "a flight",
     "mins": (255, 290), "starts": (1260, 1430), "overnight": True, "note": " All times are UK time.",
     "labels": ("Leaves Glasgow", "Lands in Tenerife")},
    {"who": "The overnight coach", "ref": "the coach", "leave": "leaves Glasgow", "arrive": "arrives in London",
     "leave_q": "leave Glasgow", "arrive_q": "arrive in London", "trip": "the journey", "trip_a": "a journey",
     "mins": (480, 560), "starts": (1260, 1410), "overnight": True, "labels": ("Leaves Glasgow", "Arrives London")},
    {"who": "A hillwalker", "ref": "the hillwalker", "leave": "sets off up Ben Nevis", "arrive": "gets back down",
     "leave_q": "set off", "arrive_q": "get back down", "trip": "the walk", "trip_a": "a walk",
     "mins": (260, 340), "starts": (420, 660), "labels": ("Sets off", "Gets back down")},
    {"who": "A shift at a Lewis salmon farm", "ref": "the shift", "leave": "starts", "arrive": "finishes",
     "leave_q": "start", "arrive_q": "finish", "trip": "the shift", "trip_a": "a shift",
     "mins": (420, 560), "starts": (300, 540), "labels": ("Shift starts", "Shift finishes")},
]


def _pick_interval(ctx):
    """(start, end) with neither on the hour and at least one whole hour in between, so the
    time bar has all three pieces."""
    for _ in range(1000):
        start = random.randint(*ctx["starts"])
        end = start + random.randint(*ctx["mins"])
        if start % 60 and end % 60 and end // 60 - (start // 60 + 1) >= 1 \
                and (ctx.get("overnight") or end < 1440):
            return start, end
    return 455, 740


def generate_sdt_l5(calc_mode=False):
    ctx = random.choice(_L5_CONTEXTS)
    start, end = _pick_interval(ctx)
    total = end - start
    hm = _hm_string(total)
    note = ctx.get("note", "")
    mode = random.choice(["interval", "forward", "backward"])
    meta = _bar_meta(start, end, mode, *ctx["labels"])

    if mode == "interval":
        q = (f"{ctx['who']} {ctx['leave']} at {_clock(start)} and {ctx['arrive']} at {_clock(end)}.{note}\n\n"
             f"How long does {ctx['trip']} take?")
        answer = hm
        worked = [_bar_lines(start, end, mode), f"**{ctx['trip'].capitalize()} takes {hm}.**"]
        meta["answer_type"] = "duration"
    elif mode == "forward":
        q = (f"{ctx['who']} {ctx['leave']} at {_clock(start)}. {ctx['trip'].capitalize()} takes {hm}.{note}\n\n"
             f"What time does {ctx['ref']} {ctx['arrive_q']}? Give your answer as a 24-hour time, e.g. 09:05.")
        answer = _clock(end)
        worked = [_bar_lines(start, end, mode), f"**{ctx['ref'].capitalize()} {ctx['arrive']} at {answer}.**"]
    else:
        q = (f"{ctx['who']} {ctx['arrive']} at {_clock(end)} after {ctx['trip_a']} of {hm}.{note}\n\n"
             f"What time did {ctx['ref']} {ctx['leave_q']}? Give your answer as a 24-hour time, e.g. 09:05.")
        answer = _clock(start)
        worked = [_bar_lines(start, end, mode), f"**{ctx['ref'].capitalize()} {ctx['leave']} at {answer}.**"]

    return Question(
        question_text=q, correct_answer=answer, topic="Numeracy",
        question_type="Speed, Distance and Time", scaffold_steps=_bar_scaffold(start, end, mode),
        worked_solution=worked, notes=NOTES_TIME_INTERVALS, metadata=meta,
    )


# ---------------------------------------------------------------------------
# Level 6 — Speed, distance and time with time intervals
# ---------------------------------------------------------------------------

NOTES_SDT_INTERVALS = """
**Speed, Distance and Time with Time Intervals:**

**Finding an arrival (or departure) time:**
1. Use **T = D ÷ S** to find the journey time as a decimal number of hours
2. Change it into hours and minutes (decimal part × 60)
3. Use a time bar to add it on to the departure time (or take it away from the arrival time)

**Finding a speed from two clock times:** use a time bar to find the journey time, change it
into a decimal number of hours, then use **S = D ÷ T**.

**Example 1:** Callum drives 95.4 miles from Glasgow to Oban at an average speed of 36 mph. He
leaves Glasgow at 08:47. What time does he arrive in Oban?

[[time_bar 08:47-11:26 forward | Leaves Glasgow | Arrives Oban]]

- T = D ÷ S = 95.4 ÷ 36 = 2.65 hours
- 0.65 × 60 = 39 minutes, so the journey takes 2 hours 39 minutes
- Step 1:  08:47 → 09:00 = 13 min.  Still to add: 2 h 26 min
- Step 2:  09:00 + 2 hours = 11:00.   Step 3:  11:00 + 26 min = 11:26
- **Callum arrives in Oban at 11:26.**

**Example 2:** The ferry leaves Mallaig at 09:40 and arrives in Lochboisdale at 13:10. The
crossing is 87.5 km. Calculate the average speed of the ferry.

[[time_bar 09:40-13:10 interval | Leaves Mallaig | Arrives Lochboisdale]]

- Journey time = 20 min + 3 hours + 10 min = 3 hours 30 minutes
- 30 minutes = 30 ÷ 60 = 0.5 hours, so T = 3.5 hours
- S = D ÷ T = 87.5 ÷ 3.5 = 25
- **The average speed of the ferry is 25 km/h.**
"""

_NAMES = ["Finlay", "Eilidh", "Callum", "Morag", "Iain", "Kirsty", "Ruaridh", "Catriona", "Calum", "Mhairi"]

# frm/to: place names; at_to: how to say "arriving there"; unit: speed unit.
_L6_ROUTES = [
    {"who": "A bus", "ref": "the bus", "frm": "Stornoway", "to": "Tarbert", "at_to": "in Tarbert", "unit": "km/h",
     "speeds": (range(35, 56), [40, 45, 50]), "mins": (60, 100)},
    {"who": "A coach", "ref": "the coach", "frm": "Inverness", "to": "Ullapool", "at_to": "in Ullapool", "unit": "km/h",
     "speeds": (range(45, 66), [50, 60]), "mins": (80, 110)},
    {"who": "The ferry", "ref": "the ferry", "frm": "Oban", "to": "Castlebay", "at_to": "in Castlebay", "unit": "km/h",
     "speeds": (range(28, 37), [30, 32, 36]), "mins": (270, 310)},
    {"who": "The ferry", "ref": "the ferry", "frm": "Mallaig", "to": "Lochboisdale", "at_to": "in Lochboisdale", "unit": "km/h",
     "speeds": (range(22, 31), [24, 25, 30]), "mins": (190, 225)},
    {"who": "A train", "ref": "the train", "frm": "Glasgow", "to": "Inverness", "at_to": "in Inverness", "unit": "km/h",
     "speeds": (range(70, 91), [75, 80, 90]), "mins": (190, 225)},
    {"who": "A train", "ref": "the train", "frm": "Edinburgh", "to": "Aberdeen", "at_to": "in Aberdeen", "unit": "mph",
     "speeds": (range(45, 61), [50, 55, 60]), "mins": (135, 160)},
    {"who": "A fishing boat", "ref": "the boat", "frm": "the fishing grounds", "to": "Kinlochbervie",
     "at_to": "back in Kinlochbervie", "unit": "km/h", "speeds": (range(12, 19), [12, 15, 18]), "mins": (150, 260)},
    {"commute": True, "frm": "home", "to": "work", "at_to": "at work", "unit": "mph",
     "speeds": (range(30, 51), [30, 36, 40, 45, 48]), "mins": (20, 80)},
]


def _route_people(route):
    """(subject for the question text, how to refer back to it)."""
    if route.get("commute"):
        name = random.choice(_NAMES)
        return name, name
    return route["who"], route["ref"]


def _sdt_steps(distance, speed, total):
    """Scaffold + worked lines for T = D ÷ S then hours and minutes."""
    hours = total / 60
    whole, mins = divmod(total, 60)
    hm = _hm_string(total)
    steps = [
        {"prompt": "Use T = D ÷ S to find the journey time as a decimal number of hours", "answer": _num(hours)},
        {"prompt": "Write the journey time in hours and minutes", "answer": hm, "answer_type": "duration"},
    ]
    lines = [f"T = D ÷ S = {_fmt(distance)} ÷ {speed} = {_fmt(hours)} hours",
             f"{_fmt(round(hours - whole, 4))} × 60 = {mins}, so the journey takes {hm}"]
    return steps, lines


def _start_time(total, lo=360, hi=1020):
    """A departure time that isn't on the hour, finishing before midnight."""
    while True:
        start = random.randint(lo, hi)
        if start % 60 and (start + total) % 60 and start + total < 1440:
            return start


def generate_sdt_l6(calc_mode=False):
    route = random.choice(_L6_ROUTES)
    who, ref = _route_people(route)
    speed, total = _journey(calc_mode, route["speeds"][1 if calc_mode else 0], *route["mins"])
    hours = total / 60
    distance = _num(speed * hours)
    du = _DIST_UNIT[route["unit"]]
    start = _start_time(total)
    end = start + total
    labels = (f"Leaves {route['frm']}", f"Arrives {route['at_to']}")
    variant = random.choice(["arrive", "latest", "speed"])

    if variant == "arrive":
        q = (f"{who} leaves {route['frm']} at {_clock(start)} and travels {_fmt(distance)} {du} to "
             f"{route['to']} at an average speed of {speed} {route['unit']}.\n\n"
             f"What time does {ref} arrive {route['at_to']}? Give your answer as a 24-hour time, e.g. 09:05.")
        steps, lines = _sdt_steps(distance, speed, total)
        steps += _bar_scaffold(start, end, "forward")
        lines += [_bar_lines(start, end, "forward"), f"**{ref[0].upper() + ref[1:]} arrives {route['at_to']} at {_clock(end)}.**"]
        answer, mode = _clock(end), "forward"
    elif variant == "latest":
        q = (f"{who} must arrive {route['at_to']} by {_clock(end)}. The journey from {route['frm']} is "
             f"{_fmt(distance)} {du}, at an average speed of {speed} {route['unit']}.\n\n"
             f"What is the latest time {ref} can leave {route['frm']}? Give your answer as a 24-hour time, e.g. 09:05.")
        steps, lines = _sdt_steps(distance, speed, total)
        steps += _bar_scaffold(start, end, "backward")
        lines += [_bar_lines(start, end, "backward"), f"**The latest {ref} can leave is {_clock(start)}.**"]
        answer, mode = _clock(start), "backward"
    else:
        q = (f"{who} leaves {route['frm']} at {_clock(start)} and arrives {route['at_to']} at "
             f"{_clock(end)}. The journey is {_fmt(distance)} {du}.\n\n"
             f"Calculate the average speed in {route['unit']}.")
        whole, mins = divmod(total, 60)
        steps = _bar_scaffold(start, end, "interval") + [
            {"prompt": "Write the journey time as a decimal number of hours", "answer": _num(hours)},
            {"prompt": "Use S = D ÷ T to find the speed", "answer": speed},
        ]
        lines = [_bar_lines(start, end, "interval") + f"  →  {_hm_string(total)}",
                 f"{mins} ÷ 60 = {_fmt(round(mins / 60, 4))}, so T = {_fmt(hours)} hours",
                 f"S = D ÷ T = {_fmt(distance)} ÷ {_fmt(hours)} = {speed}",
                 f"**The average speed is {speed} {route['unit']}.**"]
        answer, mode = speed, "interval"

    return Question(
        question_text=q, correct_answer=answer, topic="Numeracy",
        question_type="Speed, Distance and Time", scaffold_steps=steps, worked_solution=lines,
        notes=NOTES_SDT_INTERVALS, metadata=_bar_meta(start, end, mode, *labels, ask_total=True),
    )


# ---------------------------------------------------------------------------
# Level 7 — MORE ADVANCED: journeys with delays, stops and breaks
# ---------------------------------------------------------------------------

NOTES_DELAYS = """
**★ More Advanced — Journeys with Delays and Stops:**

- **Add** any delay, stop or break on to the journey time **before** you use the time bar.
- When finding a **speed**, **take the stops away first** — S = D ÷ T only uses the time spent
  moving.

**Example:** The ferry from Ullapool to Stornoway is due to leave at 09:50 but is delayed by
25 minutes. The crossing is 86.4 km and the ferry sails at an average speed of 32 km/h. What
time does it arrive in Stornoway?

[[time_bar 09:50-12:57 forward | Timetabled departure | Arrives Stornoway]]

- T = D ÷ S = 86.4 ÷ 32 = 2.7 hours;  0.7 × 60 = 42, so the crossing takes 2 hours 42 minutes
- Total time from 09:50 = 2 h 42 min + 25 min delay = 3 hours 7 minutes
- Step 1:  09:50 → 10:00 = 10 min.  Step 2:  10:00 + 2 hours = 12:00.  Step 3:  12:00 + 57 min = 12:57
- **The ferry arrives in Stornoway at 12:57.**
"""

_ADV = "**★ More advanced**\n\n"

_L7_DELAY = [r for r in _L6_ROUTES if r.get("who") in ("The ferry", "A train", "A coach")]
_L7_STOPS = [
    {"who": "A train", "ref": "the train", "frm": "Inverness", "to": "Kyle of Lochalsh", "at_to": "in Kyle of Lochalsh",
     "speeds": (range(50, 66), [50, 55, 60]), "mins": (120, 160), "stop": "stations"},
    {"who": "A train", "ref": "the train", "frm": "Glasgow", "to": "Oban", "at_to": "in Oban",
     "speeds": (range(50, 66), [50, 55, 60]), "mins": (150, 190), "stop": "stations"},
    {"who": "A bus", "ref": "the bus", "frm": "Stornoway", "to": "Leverburgh", "at_to": "in Leverburgh",
     "speeds": (range(35, 51), [40, 45, 48]), "mins": (80, 130), "stop": "villages"},
]
_L7_BREAK = [
    {"who": "A lorry driver", "ref": "the driver", "frm": "Ullapool", "to": "Glasgow", "at_to": "in Glasgow",
     "speeds": (range(48, 61), [48, 50, 54, 60]), "mins": (330, 420)},
    {"who": "A lorry driver", "ref": "the driver", "frm": "Stornoway", "to": "Edinburgh", "at_to": "in Edinburgh",
     "speeds": (range(45, 61), [45, 50, 60]), "mins": (360, 450)},
    {"who": "A coach driver", "ref": "the driver", "frm": "Oban", "to": "Aberdeen", "at_to": "in Aberdeen",
     "speeds": (range(48, 61), [48, 50, 60]), "mins": (270, 330)},
]
_L7_SPEED = [
    {"who": "A coach", "ref": "the coach", "frm": "Oban", "to": "Glasgow", "at_to": "in Glasgow",
     "speeds": (range(45, 61), [48, 50, 60]), "mins": (140, 180), "where": "in Tyndrum"},
    {"who": "A bus", "ref": "the bus", "frm": "Portree", "to": "Inverness", "at_to": "in Inverness",
     "speeds": (range(40, 56), [40, 45, 48, 50]), "mins": (180, 240), "where": "in Kyle of Lochalsh"},
    {"who": "A train", "ref": "the train", "frm": "Glasgow", "to": "Mallaig", "at_to": "in Mallaig",
     "speeds": (range(45, 56), [45, 48, 50]), "mins": (270, 320), "where": "at Fort William"},
]


def generate_sdt_l7(calc_mode=False):
    """More advanced: an extra time period (delay, stops, a break) on top of the journey."""
    variant = random.choice(["delay", "stops", "break", "speed"])
    ci = 1 if calc_mode else 0

    if variant == "delay":
        r = random.choice(_L7_DELAY)
        speed, travel = _journey(calc_mode, r["speeds"][ci], *r["mins"])
        distance = _num(speed * travel / 60)
        du = _DIST_UNIT[r["unit"]]
        extra = random.choice(range(10, 56, 5))
        total = travel + extra
        start = _start_time(total)
        end = start + total
        q = (f"{r['who']} is due to leave {r['frm']} at {_clock(start)} but is delayed by {extra} minutes. "
             f"The journey is {_fmt(distance)} {du} and {r['ref']} travels at an average speed of "
             f"{speed} {r['unit']}.\n\nWhat time does it arrive {r['at_to']}? Give your answer as a 24-hour "
             f"time, e.g. 09:05.")
        steps, lines = _sdt_steps(distance, speed, travel)
        steps.append({"prompt": f"Add on the {extra} minute delay. How long after {_clock(start)} does it "
                                f"arrive?", "answer": _hm_string(total), "answer_type": "duration"})
        lines.append(f"Total time from {_clock(start)} = {_hm_string(travel)} + {extra} min = {_hm_string(total)}")
        mode, answer = "forward", _clock(end)
        labels = ("Timetabled departure", f"Arrives {r['to']}")
        lines += [_bar_lines(start, end, mode), f"**It arrives {r['at_to']} at {answer}.**"]
    elif variant == "stops":
        r = random.choice(_L7_STOPS)
        speed, travel = _journey(calc_mode, r["speeds"][ci], *r["mins"])
        distance = _num(speed * travel / 60)
        n, each = random.randint(2, 6), random.randint(2, 5)
        extra = n * each
        total = travel + extra
        start = _start_time(total)
        end = start + total
        q = (f"{r['who']} leaves {r['frm']} at {_clock(start)} and travels {_fmt(distance)} km to {r['to']} "
             f"at an average speed of {speed} km/h while moving. It stops at {n} {r['stop']} on the way, "
             f"for {each} minutes at each.\n\nWhat time does it arrive {r['at_to']}? Give your answer as a "
             f"24-hour time, e.g. 09:05.")
        steps, lines = _sdt_steps(distance, speed, travel)
        steps += [{"prompt": "How many minutes does it spend stopped altogether?", "answer": extra},
                  {"prompt": "What is the total time for the whole journey, including stops?",
                   "answer": _hm_string(total), "answer_type": "duration"}]
        lines.append(f"Stops = {n} × {each} = {extra} min, so total time = {_hm_string(travel)} + "
                     f"{extra} min = {_hm_string(total)}")
        mode, answer = "forward", _clock(end)
        labels = (f"Leaves {r['frm']}", f"Arrives {r['to']}")
        lines += [_bar_lines(start, end, mode), f"**It arrives {r['at_to']} at {answer}.**"]
    elif variant == "break":
        r = random.choice(_L7_BREAK)
        speed, travel = _journey(calc_mode, r["speeds"][ci], *r["mins"])
        distance = _num(speed * travel / 60)
        extra = random.choice([30, 40, 45, 50, 60])
        total = travel + extra
        start = _start_time(total, 240, 900)
        end = start + total
        q = (f"{r['who']} must arrive {r['at_to']} by {_clock(end)}. The journey from {r['frm']} is "
             f"{_fmt(distance)} km, driven at an average speed of {speed} km/h, and {r['ref']} must also "
             f"take a {extra} minute break on the way.\n\nWhat is the latest time {r['ref']} can leave "
             f"{r['frm']}? Give your answer as a 24-hour time, e.g. 09:05.")
        steps, lines = _sdt_steps(distance, speed, travel)
        steps.append({"prompt": f"Add on the {extra} minute break. What is the total time needed?",
                      "answer": _hm_string(total), "answer_type": "duration"})
        lines.append(f"Total time = {_hm_string(travel)} + {extra} min = {_hm_string(total)}")
        mode, answer = "backward", _clock(start)
        labels = (f"Leaves {r['frm']}", f"Arrives {r['to']}")
        lines += [_bar_lines(start, end, mode), f"**The latest {r['ref']} can leave is {answer}.**"]
    else:
        r = random.choice(_L7_SPEED)
        speed, travel = _journey(calc_mode, r["speeds"][ci], *r["mins"])
        distance = _num(speed * travel / 60)
        extra = random.choice([10, 15, 20, 25, 30, 40, 45])
        total = travel + extra
        start = _start_time(total)
        end = start + total
        hours = travel / 60
        tw, tm = divmod(travel, 60)
        q = (f"{r['who']} leaves {r['frm']} at {_clock(start)} and arrives {r['at_to']} at {_clock(end)}. "
             f"On the way it stops {r['where']} for {extra} minutes. The journey is {_fmt(distance)} km.\n\n"
             f"Calculate the average speed of {r['ref']} while it is moving, in km/h.")
        mode, answer = "interval", speed
        steps = _bar_scaffold(start, end, mode) + [
            {"prompt": f"Take away the {extra} minute stop. How long is it actually moving?",
             "answer": _hm_string(travel), "answer_type": "duration"},
            {"prompt": "Write the moving time as a decimal number of hours", "answer": _num(hours)},
            {"prompt": "Use S = D ÷ T to find the speed", "answer": speed},
        ]
        lines = [_bar_lines(start, end, mode) + f"  →  {_hm_string(total)}",
                 f"Moving time = {_hm_string(total)} − {extra} min = {_hm_string(travel)}",
                 f"{tm} ÷ 60 = {_fmt(round(tm / 60, 4))}, so T = {_fmt(hours)} hours",
                 f"S = D ÷ T = {_fmt(distance)} ÷ {_fmt(hours)} = {speed}",
                 f"**The average speed while moving is {speed} km/h.**"]
        labels = (f"Leaves {r['frm']}", f"Arrives {r['to']}")

    if mode != "interval":
        steps += _bar_scaffold(start, end, mode)
    return Question(
        question_text=_ADV + q, correct_answer=answer, topic="Numeracy",
        question_type="Speed, Distance and Time", scaffold_steps=steps, worked_solution=lines,
        notes=NOTES_DELAYS, metadata=_bar_meta(start, end, mode, *labels, ask_total=True),
    )


def generate_sdt_question(calc_mode=False):
    return random.choice([
        generate_sdt_l1,
        generate_sdt_l2,
        generate_sdt_l3,
        generate_sdt_l4,
        generate_sdt_l5,
        generate_sdt_l6,
        generate_sdt_l7,
    ])(calc_mode=calc_mode)
