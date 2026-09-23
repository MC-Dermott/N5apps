import random
from core.models.question_model import Question
from topics.numeracy.time_conversion import _hm_string


def _fmt(x):
    """Plain decimal string — never scientific notation, no trailing zeros."""
    s = f"{round(x, 6):.6f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def _num(x):
    x = round(x, 6)
    return int(x) if x == int(x) else x


def _clock(total_minutes):
    h, m = divmod(total_minutes, 60)
    return f"{h:02d}:{m:02d}"


NOTES_FORMULA = """
**The Three Formulas:**

**D = S × T**  **S = D ÷ T**  **T = D ÷ S**

(D = distance, S = speed, T = time)

Write down what you know and what you want to find, then choose the formula that gives what
you want.

**Example:** A CalMac ferry travels 78 km at an average speed of 24 km/h. How long does the
crossing take?
- Know: D = 78 km, S = 24 km/h. Want: T → use T = D ÷ S
- T = 78 ÷ 24 = **3.25 hours**
"""

NOTES_HOURS_MINUTES = """
**Speed, Distance and Time — Hours and Minutes:**

A time must be a **decimal number of hours** before it goes into a formula.

- Minutes → decimal hours: **÷ 60** (e.g. 45 minutes = 45 ÷ 60 = 0.75 hours)
- Decimal hours → minutes: multiply the decimal part **× 60** (e.g. 0.4 hours = 24 minutes)

**Example 1:** A ferry sails 51 km at 12 km/h. How long does it take, in hours and minutes?
- T = 51 ÷ 12 = 4.25 hours
- 0.25 × 60 = 15 → **4 hours 15 minutes**

**Example 2:** A bus travels for 2 hours 45 minutes at 48 km/h. How far does it travel?
- 45 ÷ 60 = 0.75, so T = 2.75 hours
- D = 48 × 2.75 = **132 km**
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

**Example:** A runner runs at 5 m/s. How long does it take her to run 3 km?
- 3 km = 3 × 1000 = 3000 m
- T = 3000 ÷ 5 = **600 seconds**
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

    return Question(
        question_text=q, correct_answer=answer, topic="Numeracy",
        question_type="Speed, Distance and Time", scaffold_steps=scaffold_steps,
        worked_solution=worked, notes=NOTES_CLOCK,
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


def generate_sdt_question(calc_mode=False):
    return random.choice([
        generate_sdt_l1,
        generate_sdt_l2,
        generate_sdt_l3,
        generate_sdt_l4,
    ])(calc_mode=calc_mode)
