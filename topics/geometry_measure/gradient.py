"""Gradient — National 4 (generate_gradient_question_n4) and National 5 (levels 1–5).

The N5 levels mirror Gradient_Worksheet.docx (N5 Apps/Worksheets/Geometry and Measure):
  1 gradient = vertical ÷ horizontal as a fraction in its simplest form (ramps, slipways, roofs, graphs)
  2 changing to the same units first (cm/m, mm/cm, m/km)
  3 heights above sea level (the DIFFERENCE is the vertical) and coordinates
  4 comparing a gradient with a regulation, a minimum or a tolerance; working backwards
  5 Pythagoras when the sloping length is given (calculator)
Diagrams are drawn by topics/geometry_measure/gradient_diagrams.py (the same drawings as the worksheet).

Distractors are the errors in the course reports and marking instructions: horizontal ÷ vertical
(2024 P1 Q4, 2026 P1 Q6, 2025 P2 Q10b), units not converted (2018, 2022, 2023, 2024, 2026), a height
above sea level used instead of the difference, or the two heights added (2022 P1 Q7, 2025 P2 Q10b),
the sloping length used as the horizontal distance, and squares added in Pythagoras (2023 P2 Q3).

Fraction answers are strings "p/q" in simplest form (the app's checkers parse "a/b").
"""
import random
import math
from fractions import Fraction

from core.models.distractors import distractors
from core.models.question_model import Question, make_part, multipart_worked_solution

NOTES = """
**Gradient:**

Gradient measures how steep a slope is.

**gradient = vertical rise ÷ horizontal distance**

⚠️ **Units must match** before you divide — convert rise and run to the same unit first.

**Useful conversions:**
- 1 m = 100 cm → divide cm by 100 to get m
- 1 km = 1000 m → multiply km by 1000 to get m

**Example:** A ramp rises 30 cm over a horizontal distance of 6 m.
- Convert: 30 cm = 0.3 m
- Gradient = 0.3 ÷ 6 = **0.05**
"""

# ---------------------------------------------------------------------------
# Predefined number pairs that give clean gradient answers after unit conversion
# ---------------------------------------------------------------------------

# (rise_cm, run_m) → gradient = rise_cm / (100 × run_m)
_CM_M_PAIRS = [
    (30,  6), (25,  5), (40,  8), (50,  4), (20,  8),
    (15,  6), (10,  4), (60,  4), (75,  5), (50, 10),
    (80,  5), (45,  9), (36,  9), (24,  6), (48,  8),
]
# calc_mode: (50,4)→0.125, (20,8)→0.025, (15,6)→0.025, (10,4)→0.025 all exceed 2 d.p.
_CM_M_PAIRS_CALC = [
    (30,  6), (25,  5), (40,  8), (60,  4), (75,  5),
    (50, 10), (80,  5), (45,  9), (36,  9), (24,  6), (48,  8),
]

# (rise_m, run_km) → gradient = rise_m / (run_km × 1000)
_M_KM_PAIRS = [
    ( 50, 2), ( 80, 4), (100, 2), (150, 3), ( 60, 3),
    ( 75, 3), (120, 4), (200, 5), ( 40, 2), ( 90, 3),
    (100, 5), (160, 4), (120, 6), (180, 6), (250, 5),
]
# calc_mode: (50,2)→0.025 and (75,3)→0.025 exceed 2 d.p.
_M_KM_PAIRS_CALC = [
    ( 80, 4), (100, 2), (150, 3), ( 60, 3),
    (120, 4), (200, 5), ( 40, 2), ( 90, 3),
    (100, 5), (160, 4), (120, 6), (180, 6), (250, 5),
]

_CM_M_CONTEXTS = [
    ("ramp",     "A ramp"),
    ("path",     "A path"),
    ("driveway", "A driveway"),
    ("slope",    "A slope"),
]

_M_KM_CONTEXTS = [
    ("road",          "A road"),
    ("hillside path", "A hillside path"),
    ("railway line",  "A railway line"),
    ("hill track",    "A hill track"),
]

_PLACES = [
    "Aviemore",    "Pitlochry",    "Callander",   "Dunkeld",     "Braemar",
    "Aberfeldy",   "Killin",       "Crianlarich", "Tyndrum",     "Glencoe",
    "Kinlochleven","Spean Bridge", "Newtonmore",  "Kingussie",   "Carrbridge",
    "Tomintoul",   "Blairgowrie",  "Comrie",      "Balquhidder", "Strathyre",
    "Ardlui",      "Lochearnhead", "Thornhill",   "Aberfoyle",   "Killearn",
]

# 2dp decimal parts added to heights for realism
_DECIMALS = [0.12, 0.23, 0.34, 0.45, 0.47, 0.56, 0.67, 0.68, 0.78, 0.89]


def _gcd(a, b):
    return math.gcd(int(abs(a)), int(abs(b)))


def _frac_str(num, den):
    g = _gcd(num, den)
    n, d = num // g, den // g
    return str(n) if d == 1 else f"{n}/{d}"


def generate_gradient_question_n4(calc_mode=False):
    return _gradient_cm_m(calc_mode)


def generate_gradient_question(calc_mode=False):
    """National 5: any of the worksheet's five levels (defined below)."""
    return random.choice([generate_gradient_l1, generate_gradient_l2, generate_gradient_l3,
                          generate_gradient_l4, generate_gradient_l5])(calc_mode=calc_mode)


# ---------------------------------------------------------------------------
# Type 1 — Simple slope: rise in cm, run in m
# ---------------------------------------------------------------------------

def _gradient_cm_m(calc_mode=False):
    rise_cm, run_m = random.choice(_CM_M_PAIRS_CALC if calc_mode else _CM_M_PAIRS)
    rise_m_float = rise_cm / 100
    gradient = rise_cm / (run_m * 100)   # integer division avoids float rounding
    g_frac = _frac_str(rise_cm, run_m * 100)

    noun, subject = random.choice(_CM_M_CONTEXTS)

    question_text = (
        f"{subject} rises {rise_cm} cm over a horizontal distance of {run_m} m. "
        f"Calculate the gradient of the {noun}."
    )

    scaffold_steps = [
        {
            "prompt": "Convert the rise to metres",
            "answer": rise_m_float,
        },
        {
            "prompt": "Calculate the gradient (rise ÷ run)",
            "answer": gradient,
        },
    ]

    worked = [
        f"Convert rise: {rise_cm} cm ÷ 100 = {rise_m_float:g} m",
        "gradient = vertical rise ÷ horizontal distance",
        f"gradient = {rise_m_float:g} ÷ {run_m}",
        f"gradient = {g_frac} = {gradient:g}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=gradient,
        topic="Geometry and Measure",
        question_type="Gradient",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Type 2 — Simple slope: rise in m, run in km
# ---------------------------------------------------------------------------

def _gradient_m_km(calc_mode=False):
    rise_m, run_km = random.choice(_M_KM_PAIRS_CALC if calc_mode else _M_KM_PAIRS)
    run_m = run_km * 1000
    gradient = rise_m / run_m
    g_frac = _frac_str(rise_m, run_m)

    noun, subject = random.choice(_M_KM_CONTEXTS)

    question_text = (
        f"{subject} rises {rise_m} m over a horizontal distance of {run_km} km. "
        f"Calculate the gradient of the {noun}."
    )

    scaffold_steps = [
        {
            "prompt": "Convert the horizontal distance to metres",
            "answer": float(run_m),
        },
        {
            "prompt": "Calculate the gradient (rise ÷ run)",
            "answer": gradient,
        },
    ]

    worked = [
        f"Convert run: {run_km} km × 1000 = {run_m} m",
        "gradient = vertical rise ÷ horizontal distance",
        f"gradient = {rise_m} ÷ {run_m}",
        f"gradient = {g_frac} = {gradient:g}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=gradient,
        topic="Geometry and Measure",
        question_type="Gradient",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Type 3 — Height above sea level word problem
# ---------------------------------------------------------------------------

def _gradient_sea_level(calc_mode=False):
    rise_m, run_km = random.choice(_M_KM_PAIRS_CALC if calc_mode else _M_KM_PAIRS)
    run_m = run_km * 1000
    gradient = rise_m / run_m
    g_frac = _frac_str(rise_m, run_m)

    place_a, place_b = random.sample(_PLACES, 2)

    base_a = random.randint(80, 350)
    decimal = random.choice(_DECIMALS)
    height_a = round(base_a + decimal, 2)
    height_b = round(height_a + rise_m, 2)

    question_text = (
        f"{place_a} is {height_a:.2f} m above sea level. "
        f"{place_b} is {height_b:.2f} m above sea level. "
        f"The horizontal distance between them is {run_km} km. "
        f"Calculate the gradient of the road between {place_a} and {place_b}."
    )

    scaffold_steps = [
        {
            "prompt": "Find the difference in height",
            "answer": float(rise_m),
        },
        {
            "prompt": "Convert the horizontal distance to metres",
            "answer": float(run_m),
        },
        {
            "prompt": "Calculate the gradient (rise ÷ run)",
            "answer": gradient,
        },
    ]

    worked = [
        f"Rise = {height_b:.2f} − {height_a:.2f} = {rise_m} m",
        f"Horizontal distance = {run_km} km × 1000 = {run_m} m",
        "gradient = vertical rise ÷ horizontal distance",
        f"gradient = {rise_m} ÷ {run_m}",
        f"gradient = {g_frac} = {gradient:g}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=gradient,
        topic="Geometry and Measure",
        question_type="Gradient",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ═══════════════════════════════════════════════════════════════════════════════════════════════
# National 5 — levels mirroring Gradient_Worksheet.docx
# ═══════════════════════════════════════════════════════════════════════════════════════════════
TOPIC, QTYPE = "Geometry and Measure", "Gradient"
_DIAG = "topics.geometry_measure.gradient_diagrams"
_FR = "Give your answer as a fraction in its simplest form."

NOTES_FRACTION = """
**Gradient = vertical height ÷ horizontal distance**

The bigger the gradient, the steeper the slope. Give a gradient as a **fraction in its simplest
form** unless you're asked for a decimal. No decimals inside a fraction: 2.4/3.2 = 24/32 = 3/4.

**Example (from the worksheet):** A wheelchair ramp at Castlebay School rises 30 cm over a
horizontal distance of 360 cm. Calculate the gradient of the ramp.
- Gradient = vertical ÷ horizontal = 30/360
- Simplest form: 30/360 = **1/12**

⚠ Vertical on top: 12/180 scored 0 in 2026, and 165/850 scored 0 in 2024 (marking instructions).
Simplify fully (2022, 2024, 2026 course reports), but don't "simplify" a fraction that already is
in its simplest form — 17/33 = 1/2 lost the mark in 2024.
"""

NOTES_UNITS = """
**Change to the same units first**

1 m = 100 cm, 1 cm = 10 mm, 1 km = 1000 m. Change the bigger unit into the smaller one, so the
numbers stay whole. Write the conversion down — it is a mark.

**Example (from the worksheet):** A ramp in Stornoway rises 150 cm over a horizontal distance of
9 m. Calculate the gradient of the ramp.
- Same units (m to cm): 9 × 100 = 900 cm
- Gradient = vertical ÷ horizontal = 150/900
- Simplest form: 150/900 = **1/6**

⚠ In 2026 most candidates made no attempt to change to the same units (course report): 180/12 = 15
scored only 1 of 2. The same mistake was common in 2018, 2022, 2023 and 2024.
"""

NOTES_SEA = """
**Heights above sea level and coordinates**

Given two heights above sea level, the vertical distance is the **difference**. Draw a sketch if
there isn't one. On a graph, vertical = change in y and horizontal = change in x.

**Example (from the worksheet):** Clisham is 799 m above sea level. A walk starts at a car park
199 m above sea level, a horizontal distance of 3 km from the top. Calculate the average gradient.
- Vertical = 799 − 199 = 600 m
- Horizontal (km to m): 3 × 1000 = 3000 m
- Gradient = 600/3000 = **1/5**

⚠ In 2022, 420/3000 (the height of the top, not the difference) was common, and many didn't draw
a diagram. In 2025 some used 71/250 or (48 + 71)/250 (marking instructions).
"""

NOTES_COMPARE = """
**Comparing gradients and regulations**

Change the gradients to decimals; the bigger gradient is the steeper slope. Write down both numbers
you compare, then the conclusion — a conclusion with no working gets no mark. For a tolerance such
as 0.35 ± 0.01, write down both limits first. Working backwards: height = gradient × horizontal;
horizontal = height ÷ gradient.

**Example (from the worksheet):** The maximum gradient allowed for a wheelchair ramp is 1/12. A ramp
at Lochmaddy rises 35 cm over a horizontal distance of 5 m. Does it meet the regulations?
- Same units (m to cm): 5 × 100 = 500 cm
- Gradient = 35/500 = 7/100
- As decimals: 7 ÷ 100 = 0.07; 1 ÷ 12 = 0.08
- 0.07 < 0.08, so **yes**, the ramp meets the regulations

⚠ In 2017 most couldn't compare gradients written as fractions; in 2018 many gave a conclusion with
no working; in 2023 many didn't find the limits or change the gradient to a decimal (course reports).
"""

NOTES_PYTH = """
**Pythagoras and gradient**

If you're given the **sloping** length, use Pythagoras to find the missing side first. The sloping
length is the hypotenuse, so **subtract** the squares. Then gradient = vertical ÷ horizontal.

**Example (from the worksheet):** The slipway at Leverburgh is 13 m long and covers a horizontal
distance of 12 m. Calculate its gradient.
- Vertical² = 13² − 12² = 25
- Vertical = √25 = 5 m
- Gradient = 5 ÷ 12 = **5/12**

⚠ Don't divide by the sloping length (5/13), and don't add the squares — adding instead of
subtracting was common in 2023 Paper 2 Q3 (marking instructions).
"""

_POOL = [(1, 12), (1, 15), (1, 8), (1, 16), (1, 20), (3, 40), (2, 25), (1, 6), (3, 20), (2, 15),
         (1, 10), (3, 10), (1, 5), (1, 4), (3, 8), (2, 5), (5, 12), (3, 4), (7, 24), (1, 24), (7, 80)]


def _g(x):
    x = float(x)
    return str(int(round(x))) if abs(x - round(x)) < 1e-9 else f"{x:.6f}".rstrip("0").rstrip(".")


def _r(x):
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _fs(f):
    return f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)


def _val(a):
    return float(Fraction(a)) if isinstance(a, str) else float(a)


def _dist(answer, cands):
    """distractors(), comparing fraction-string answers numerically (drops anything within 0.01)."""
    a = _val(answer)
    keep = [(v, m) for v, m in cands if v is not None and v > 0 and abs(_val(v) - a) >= 0.01]
    return distractors(a if isinstance(answer, str) else answer, keep)


def _diagram(kind, *args):
    return {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DIAG, "kind": kind, "args": list(args)}}


def _scaled(lo_v, hi_v, lo_h, hi_h, step=1, need_simplify=True):
    """A pool fraction p/q and multiplier m so that v = p·m, h = q·m are in range (m a multiple of step)."""
    for _ in range(2000):
        p, q = random.choice(_POOL)
        m = step * random.randint(1, int(hi_h / step) + 1)
        v, h = p * m, q * m
        if lo_v <= v <= hi_v and lo_h <= h <= hi_h and (m > 1 or not need_simplify):
            return Fraction(p, q), v, h
    raise RuntimeError("no numbers")


def _inverted(h, v):
    return (round(h / v, 4), "you divided the horizontal distance by the vertical height — gradient is vertical ÷ "
                             "horizontal (2026 Paper 1 Q6: 12/180 scored 0; 2024 Paper 1 Q4: 165/850 scored 0).")


# ── Level 1: gradient as a fraction in its simplest form ──────────────────────────────────────
_L1_CONTEXTS = {
    "cm": [("A wheelchair ramp at {p} school", "the ramp", "rises"), ("A skate ramp in {p}", "the ramp", "rises"),
           ("A ramp at the {p} community hall", "the ramp", "rises")],
    "m": [("The slipway at {p}", "the slipway", "drops"), ("A peat track near {p}", "the track", "rises"),
          ("A hill path near {p}", "the path", "rises")],
}
_ISLAND_PLACES = ["Castlebay", "Lochboisdale", "Lochmaddy", "Tarbert", "Leverburgh", "Stornoway", "Balivanich",
                  "Uig", "Barvas", "Ness", "Daliburgh", "Northbay", "Back", "Carloway", "Bernera"]


def generate_gradient_l1(calc_mode=False):
    kind = random.choices(["cm", "m", "dec", "graph"], [3, 3, 2, 2])[0]
    if kind == "graph":
        while True:
            x1, y1 = random.randint(0, 4), random.randint(0, 4)
            dx, dy = random.randint(2, 8), random.randint(1, 6)
            if dy < dx and (math.gcd(dx, dy) > 1 or random.random() < 0.3):
                break
        x2, y2 = x1 + dx, y1 + dy
        f = Fraction(dy, dx)
        steps = [{"prompt": "Vertical distance (change in y)", "answer": float(dy)},
                 {"prompt": "Horizontal distance (change in x)", "answer": float(dx)},
                 {"prompt": "Gradient, as a fraction in its simplest form", "answer": _fs(f)}]
        return Question(
            question_text=f"The graph shows a straight line through A({x1}, {y1}) and B({x2}, {y2}). Calculate the "
                          f"gradient of the line. {_FR}",
            correct_answer=_fs(f), topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
            worked_solution=[f"Vertical = {y2} − {y1} = {dy}; horizontal = {x2} − {x1} = {dx}",
                             f"Gradient = {dy}/{dx} = **{_fs(f)}**"],
            notes=NOTES_FRACTION, metadata=_diagram("graph", x1, y1, x2, y2),
            distractors=_dist(_fs(f), [_inverted(dx, dy),
                                       (round(y2 / x2, 4), "use the CHANGE in y and the change in x, not B's "
                                                           "coordinates on their own.")]))
    if kind == "cm":
        f, v, h = _scaled(10, 120, 60, 1200, step=5); u = "cm"
    elif kind == "m":
        f, v, h = _scaled(1, 40, 4, 600); u = "m"
    else:
        f, v10, h10 = _scaled(10, 60, 15, 120)
        while v10 % 10 == 0 and h10 % 10 == 0:
            f, v10, h10 = _scaled(10, 60, 15, 120)
        v, h, u = v10 / 10, h10 / 10, "m"
    ctx, noun, verb = random.choice(_L1_CONTEXTS["cm" if kind == "cm" else "m"])
    if kind == "cm" and f > Fraction(1, 12):
        ctx = "A skate ramp in {p}"                       # too steep for a wheelchair ramp
    if kind == "dec":
        ctx, noun, verb = "A roof", "the roof", "rises"
    place = random.choice(_ISLAND_PLACES)
    text = (f"{ctx.format(p=place)} {verb} {_g(v)} {u} over a horizontal distance of {_g(h)} {u}, as shown. "
            f"Calculate the gradient of {noun}. {_FR}")
    lines = [f"Gradient = vertical ÷ horizontal = {_g(v)}/{_g(h)}"]
    steps = []
    if kind == "dec":
        iv, ih = round(v * 10), round(h * 10)
        lines.append(f"No decimals in a fraction: {_g(v)}/{_g(h)} = {iv}/{ih}")
        steps.append({"prompt": "Multiply top and bottom by 10 — the new numerator (top)", "answer": float(iv)})
        a, b = iv, ih
    else:
        a, b = int(v), int(h)
        steps.append({"prompt": "Highest common factor of the vertical and horizontal distances",
                      "answer": float(math.gcd(a, b))})
    lines.append(f"Simplest form: {a}/{b} = **{_fs(f)}**")
    steps.append({"prompt": "Gradient, as a fraction in its simplest form", "answer": _fs(f)})
    return Question(question_text=text, correct_answer=_fs(f), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=lines, notes=NOTES_FRACTION,
                    metadata=_diagram("ramp", v, h, [f"{_g(v)} {u}", f"{_g(h)} {u}"]),
                    distractors=_dist(_fs(f), [_inverted(h, v)]))


# ── Level 2: changing to the same units ───────────────────────────────────────────────────────
_UNITS = [  # (vertical unit, horizontal unit, factor, v range, horizontal (big unit) range)
    ("cm", "m", 100, (10, 200), (1, 20)),
    ("mm", "cm", 10, (20, 600), (20, 400)),
    ("m", "km", 1000, (20, 900), (0.5, 12)),
]


def generate_gradient_l2(calc_mode=False):
    uv, uh, k, (v0, v1), (h0, h1) = random.choice(_UNITS)
    for _ in range(5000):
        f, v, hs = _scaled(v0, v1, h0 * k, h1 * k, need_simplify=False)
        hb = hs / k
        if abs(hb * 10 - round(hb * 10)) < 1e-9 and hs != v:
            break
    noun = {"cm": "ramp", "mm": "ramp", "m": "road"}[uv]
    place = random.choice(_ISLAND_PLACES)
    what = {"cm": f"A ramp at the back door of a shop in {place}", "mm": "A small ramp for a garden shed",
            "m": f"The road out of {place}"}[uv]
    text = (f"{what} rises {_g(v)} {uv} over a horizontal distance of {_g(hb)} {uh}. Calculate the gradient of "
            f"the {noun}. {_FR}")
    steps = [{"prompt": f"Change the horizontal distance to {uv}", "answer": float(hs)},
             {"prompt": "Gradient, as a fraction in its simplest form", "answer": _fs(f)}]
    lines = [f"Same units ({uh} to {uv}): {_g(hb)} × {k} = {_g(hs)} {uv}",
             f"Gradient = vertical ÷ horizontal = {_g(v)}/{_g(hs)}",
             f"Simplest form: {_g(v)}/{_g(hs)} = **{_fs(f)}**"]
    meta = _diagram("ramp", v, hs, [f"{_g(v)} {uv}", f"{_g(hb)} {uh}"]) if uv != "m" else {}
    return Question(question_text=text, correct_answer=_fs(f), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=lines, notes=NOTES_UNITS, metadata=meta,
                    distractors=_dist(_fs(f), [
                        (round(v / hb, 4), f"the units aren't the same — change {_g(hb)} {uh} to {_g(hs)} {uv} "
                                           f"first (2026 Paper 1 Q6: 180/12 = 15 scored 1 of 2)."),
                        _inverted(hs, v),
                        (round(hb / v, 4), "upside down AND the units aren't the same (2024 Paper 1 Q4 marking "
                                           "instructions: 165/850 scored 0)."),
                    ]))


# ── Level 3: heights above sea level and coordinates ──────────────────────────────────────────
_HILLS = ["Harris", "Barra", "South Uist", "North Uist", "Lewis", "Benbecula", "Vatersay", "Eriskay"]


def generate_gradient_l3(calc_mode=False):
    if random.random() < 0.3:
        while True:
            x1, y1 = random.randint(-5, 6), random.randint(-5, 6)
            dx, dy = random.randint(2, 12), random.randint(1, 9)
            if dy < dx and math.gcd(dx, dy) > 1 and x1 != 0 and x1 + dx != 0:
                break
        x2, y2 = x1 + dx, y1 + dy
        f = Fraction(dy, dx)
        steps = [{"prompt": "Vertical distance (change in y)", "answer": float(dy)},
                 {"prompt": "Horizontal distance (change in x)", "answer": float(dx)},
                 {"prompt": "Gradient, as a fraction in its simplest form", "answer": _fs(f)}]
        return Question(
            question_text=f"A straight path on a map goes through the points A({x1}, {y1}) and B({x2}, {y2}). "
                          f"Calculate the gradient of the path. {_FR}",
            correct_answer=_fs(f), topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
            worked_solution=[f"Vertical = {y2} − ({y1}) = {dy}" if y1 < 0 else f"Vertical = {y2} − {y1} = {dy}",
                             f"Horizontal = {x2} − ({x1}) = {dx}" if x1 < 0 else f"Horizontal = {x2} − {x1} = {dx}",
                             f"Gradient = {dy}/{dx} = **{_fs(f)}**"],
            notes=NOTES_SEA,
            distractors=_dist(_fs(f), [_inverted(dx, dy),
                                       (round(y2 / x2, 4) if y2 > 0 and x2 > 0 else None,
                                        "use the CHANGE in y and the change in x, not B's coordinates.")]))
    km = random.random() < 0.7
    for _ in range(5000):
        if km:
            f, d, hm = _scaled(60, 900, 500, 6000, step=10)
            if hm % 100 == 0:
                break
        else:
            f, d, hm = _scaled(20, 200, 150, 990, step=5)
            break
    bottom = random.randint(3, 150); top = bottom + d
    island = random.choice(_HILLS)
    hshow = f"{_g(hm / 1000)} km" if km else f"{hm} m"
    text = (f"The top of a hill on {island} is {top} m above sea level. A path to the top starts {bottom} m above sea level, a "
            f"horizontal distance of {hshow} from the top. Calculate the average gradient of the path. {_FR}")
    steps = [{"prompt": "Vertical distance (difference in height), in m", "answer": float(d)}]
    lines = [f"Vertical = {top} − {bottom} = {d} m"]
    if km:
        steps.append({"prompt": "Horizontal distance in m", "answer": float(hm)})
        lines.append(f"Horizontal (km to m): {_g(hm / 1000)} × 1000 = {hm} m")
    steps.append({"prompt": "Gradient, as a fraction in its simplest form", "answer": _fs(f)})
    lines.append(f"Gradient = {d}/{hm} = **{_fs(f)}**")
    return Question(question_text=text, correct_answer=_fs(f), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=lines, notes=NOTES_SEA,
                    metadata=_diagram("hill", bottom, top, hm, [f"{bottom} m", f"{top} m", hshow]),
                    distractors=_dist(_fs(f), [
                        (round(top / hm, 4), f"{top} m is the height of the top above sea level — use the "
                                             f"DIFFERENCE, {top} − {bottom} (2022 Paper 1 Q7: 420/3000)."),
                        (round(bottom / hm, 4), "use the difference in height, not the bottom's height (2025 "
                                                "Paper 2 Q10(b): 48/250)."),
                        (round((top + bottom) / hm, 4), "SUBTRACT the heights, don't add them (2025 Paper 2 "
                                                        "Q10(b): (48 + 71)/250)."),
                        _inverted(hm, d),
                        (round(d / (hm / 1000), 4) if km else None,
                         "the units aren't the same — change km to m first (2022 course report)."),
                    ]))


# ── Level 4: comparing gradients, regulations and working backwards ───────────────────────────
def _yes_no(ok, yes, no):
    return (yes if ok else no), [yes, no]


def _l4_regulation():
    lim = random.choice([(1, 12), (1, 15), (1, 20)])
    L = Fraction(*lim)
    for _ in range(5000):
        f, v, hs = _scaled(10, 120, 100, 2000, step=5, need_simplify=False)
        hb = hs / 100
        a, b = _r(float(f)), _r(float(L))
        if abs(hb * 10 - round(hb * 10)) < 1e-9 and a != b and (a < b) == (f < L) and 0.03 <= float(f) <= 0.15:
            break
    ok = f <= L
    place = random.choice(_ISLAND_PLACES)
    context = (f"The maximum gradient allowed for a {'wheelchair ramp' if lim[1] == 12 else 'footpath ramp'} is "
               f"{lim[0]}/{lim[1]}. A ramp at {place} rises {_g(v)} cm over a horizontal distance of {_g(hb)} m.")
    yes, no = "Yes — it meets the regulations", "No — it does not meet the regulations"
    ans, opts = _yes_no(ok, yes, no)
    pa = make_part("(a)", f"Calculate the gradient of the ramp. {_FR}", _fs(f),
                   scaffold_steps=[{"prompt": "Horizontal distance in cm", "answer": float(hs)},
                                   {"prompt": "Gradient, as a fraction in its simplest form", "answer": _fs(f)}],
                   worked_solution=[f"Same units (m to cm): {_g(hb)} × 100 = {_g(hs)} cm",
                                    f"Gradient = {_g(v)}/{_g(hs)} = {_fs(f)}"],
                   distractors=_dist(_fs(f), [(round(v / hb, 4), "change the metres to centimetres first (2018 "
                                                                 "Paper 1 Q15: 25/4 scored 1 of 3)."),
                                              _inverted(hs, v)]))
    pb = make_part("(b)", "Does the ramp meet the regulations? Use your working to justify your answer.", ans,
                   options=opts,
                   scaffold_steps=[{"prompt": "Your gradient as a decimal, to 2 d.p.", "answer": _r(float(f))},
                                   {"prompt": f"The maximum, {lim[0]}/{lim[1]}, as a decimal to 2 d.p.",
                                    "answer": _r(float(L))}],
                   worked_solution=[f"As decimals: {_fs(f)} = {_g(_r(float(f)))}; {lim[0]}/{lim[1]} = "
                                    f"{_g(_r(float(L)))}",
                                    f"{_g(_r(float(f)))} {'<' if ok else '>'} {_g(_r(float(L)))}, so "
                                    f"{'yes, it meets' if ok else 'no, it does not meet'} the regulations"],
                   distractors=[{"value": no if ok else yes,
                                 "mistake": "compare the gradients as decimals — the bigger decimal is the steeper "
                                            "slope (2017 and 2018 course reports)."}])
    return context, [pa, pb]


def _l4_tolerance():
    for _ in range(5000):
        target = random.choice([0.3, 0.32, 0.35, 0.4, 0.45]); tol = random.choice([0.01, 0.02])
        v = random.randint(20, 90); hb = random.choice([1.2, 1.5, 1.6, 1.8, 2, 2.1, 2.4, 2.5])
        G = v / (hb * 100)
        lo, hi = _r(target - tol), _r(target + tol)
        g2 = _r(G)
        inside = lo <= G <= hi
        if abs(G - target) < 0.1 and abs(G - lo) > 0.004 and abs(G - hi) > 0.004 and abs(G - target) > 0.002 \
                and (lo <= g2 <= hi) == inside:
            break
    ans, opts = _yes_no(inside, "Suitable", "Not suitable")
    context = (f"A skatepark ramp is {v} cm high with a horizontal distance of {_g(hb)} m. To be suitable it must "
               f"have a gradient of {_g(target)} ± {_g(tol)}.")
    pa = make_part("(a)", "Calculate the gradient of the ramp, as a decimal to 2 decimal places.", g2,
                   scaffold_steps=[{"prompt": "Horizontal distance in cm", "answer": float(round(hb * 100))},
                                   {"prompt": "Gradient, to 2 d.p.", "answer": g2}],
                   worked_solution=[f"Same units (m to cm): {_g(hb)} × 100 = {_g(hb * 100)} cm",
                                    f"Gradient = {v} ÷ {_g(hb * 100)} = {_g(g2)}"],
                   distractors=_dist(g2, [(_r(v / hb), "change the metres to centimetres first (2023 Paper 1 Q9 "
                                                       "course report)."),
                                          (_r(hb * 100 / v), "upside down — vertical ÷ horizontal.")]))
    pb = make_part("(b)", "Is the ramp suitable? Use your working to justify your answer.", ans, options=opts,
                   scaffold_steps=[{"prompt": "Lower limit", "answer": lo}, {"prompt": "Upper limit", "answer": hi}],
                   worked_solution=[f"Limits: {_g(target)} − {_g(tol)} = {_g(lo)}; {_g(target)} + {_g(tol)} = {_g(hi)}",
                                    (f"{_g(lo)} < {_g(g2)} < {_g(hi)}, so suitable" if inside else
                                     f"{_g(g2)} {'<' if G < lo else '>'} {_g(lo if G < lo else hi)}, so not "
                                     f"suitable")],
                   distractors=[{"value": "Not suitable" if inside else "Suitable",
                                 "mistake": "write down BOTH limits and compare your decimal with them (2023 Paper 1 "
                                            "Q9: many didn't find the limits)."}])
    return context, [pa, pb]


def _l4_minimum():
    for _ in range(5000):
        bottom = random.randint(5, 80); d = random.randint(12, 60); h = random.choice([150, 200, 250, 300, 400])
        mn = random.choice([0.1, 0.12, 0.15])
        G = d / h; g2 = _r(G)
        if g2 != mn and (g2 > mn) == (G > mn) and abs(G - mn) > 0.004:
            break
    top = bottom + d
    ok = G > mn
    ans, opts = _yes_no(ok, "Yes", "No")
    context = (f"The bottom of a hill is {bottom} m above sea level and the top is {top} m above sea level. The "
               f"horizontal distance between them is {h} m. A training plan needs a hill with a gradient greater "
               f"than {_g(mn)}.")
    pa = make_part("(a)", "Calculate the gradient of the hill, as a decimal to 2 decimal places.", g2,
                   scaffold_steps=[{"prompt": "Vertical distance (difference in height), in m", "answer": float(d)},
                                   {"prompt": "Gradient, to 2 d.p.", "answer": g2}],
                   worked_solution=[f"Vertical = {top} − {bottom} = {d} m", f"Gradient = {d} ÷ {h} = {_g(g2)}"],
                   distractors=_dist(g2, [(_r(top / h), f"use the difference in height, {top} − {bottom} (2025 "
                                                        f"Paper 2 Q10(b): 71/250)."),
                                          (_r(bottom / h), "use the difference in height (2025 Paper 2 Q10(b): "
                                                           "48/250)."),
                                          (_r((top + bottom) / h), "subtract the heights, don't add them (2025 "
                                                                   "Paper 2 Q10(b): (48 + 71)/250)."),
                                          (_r(h / d), "upside down — vertical ÷ horizontal (2025 Paper 2 Q10(b): "
                                                      "250/23).")]))
    pb = make_part("(b)", "Is the hill steep enough? Use your working to justify your answer.", ans, options=opts,
                   worked_solution=[f"{_g(g2)} {'>' if ok else '<'} {_g(mn)}, so {'yes' if ok else 'no'}"],
                   distractors=[{"value": "No" if ok else "Yes",
                                 "mistake": "compare your decimal with the minimum — it must be GREATER."}])
    return context, [pa, pb]


def _l4_height():
    p, q = random.choice([(1, 12), (1, 15), (1, 20)])
    h = q * random.choice([0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8]) * random.choice([1, 1, 2])
    H = _r(h * p / q); Hc = _r(H * 100)
    text = (f"The maximum gradient for a ramp is {p}/{q}. A ramp has a horizontal distance of {_g(h)} m. Calculate "
            f"the greatest height, in centimetres, that it can rise.")
    return Question(question_text=text, correct_answer=Hc, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Greatest height in metres (gradient × horizontal)", "answer": H},
                                    {"prompt": "Greatest height in centimetres", "answer": Hc}],
                    worked_solution=[f"Height = gradient × horizontal = {p}/{q} × {_g(h)} = {_g(H)} m",
                                     f"In centimetres: {_g(H)} × 100 = **{_g(Hc)} cm**"],
                    notes=NOTES_COMPARE,
                    distractors=_dist(Hc, [(H, "the question asks for centimetres — × 100."),
                                           (_r(h * q), "height = gradient × horizontal — you divided by the "
                                                       "gradient."),
                                           (_r(h * q * 100), "height = gradient × horizontal — you divided by the "
                                                             "gradient.")]))


def _l4_horizontal():
    grad = random.choice([0.05, 0.08, 0.1, 0.04, 0.125, 0.06])
    v = random.choice([0.3, 0.4, 0.5, 0.6, 0.75, 0.9, 1.2, 1.5])
    H = _r(v / grad)
    text = (f"A path must have a gradient of {_g(grad)}. It has to rise {_g(v)} m. Calculate the horizontal distance "
            f"it needs, in metres.")
    return Question(question_text=text, correct_answer=H, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Horizontal distance = height ÷ gradient (m)", "answer": H}],
                    worked_solution=[f"Horizontal = height ÷ gradient = {_g(v)} ÷ {_g(grad)} = **{_g(H)} m**"],
                    notes=NOTES_COMPARE,
                    distractors=_dist(H, [(_r(v * grad), "horizontal = height ÷ gradient — you multiplied."),
                                          (_r(grad / v), "horizontal = height ÷ gradient — you divided the wrong "
                                                         "way round.")]))


def generate_gradient_l4(calc_mode=False):
    make = random.choice([_l4_regulation, _l4_tolerance, _l4_minimum, _l4_height, _l4_horizontal])
    if make in (_l4_height, _l4_horizontal):
        return make()
    context, parts = make()
    return Question(question_text=context, correct_answer=parts[-1].correct_answer, topic=TOPIC,
                    question_type=QTYPE, worked_solution=multipart_worked_solution(parts), notes=NOTES_COMPARE,
                    parts=parts)


# ── Level 5: Pythagoras when the sloping length is given ──────────────────────────────────────
_TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37)]


def _pyth_numbers():
    """(L, h, v², v, G): sloping L and horizontal h to ≤ 2 d.p.; v² and v as the worksheet rounds them."""
    for _ in range(5000):
        if random.random() < 0.5:
            a, b, c = random.choice(_TRIPLES)
            k = random.choice([0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 1])
            v_exact, h, L = a * k, round(b * k, 2), round(c * k, 2)
        else:
            h = round(random.uniform(2, 12), 1); L = round(h + random.uniform(0.1, 1.5), 1)
            v_exact = math.sqrt(L * L - h * h)
        v2 = _r(L * L - h * h); v = _r(math.sqrt(v2)); G = _r(v / h)
        if 0.05 <= v_exact / h <= 0.9 and L <= 15 and G == _r(v_exact / h) and v2 > 0 and h > 0.5:
            return L, h, v2, v, G
    raise RuntimeError("no numbers")


def generate_gradient_l5(calc_mode=False):
    L, h, v2, v, G = _pyth_numbers()
    what = random.choice(["A ramp", "A slipway", "A boat ramp", "A driveway", "A roof rafter"])
    steps = [{"prompt": "Vertical² = sloping² − horizontal²", "answer": v2},
             {"prompt": "Vertical distance (square root), to 2 d.p.", "answer": v},
             {"prompt": "Gradient = vertical ÷ horizontal, to 2 d.p.", "answer": G}]
    lines = [f"Vertical² = {_g(L)}² − {_g(h)}² = {_g(v2)}", f"Vertical = √{_g(v2)} = {_g(v)} m",
             f"Gradient = {_g(v)} ÷ {_g(h)} = **{_g(G)}**"]
    meta = _diagram("ramp", v, h, ["", f"{_g(h)} m", f"{_g(L)} m"])
    wrong = [(_r(v / L), f"divide by the HORIZONTAL distance ({_g(h)} m), not the sloping length."),
             (_r(math.sqrt(L * L + h * h) / h), "the sloping length is the hypotenuse — SUBTRACT the squares "
                                                "(adding instead of subtracting: 2023 Paper 2 Q3)."),
             (_r(h / v), "upside down — vertical ÷ horizontal."),
             (_r(v2 / h), "you forgot the square root.")]
    text = (f"{what} is {_g(L)} m long (the sloping length) and covers a horizontal distance of {_g(h)} m, as shown. "
            f"Calculate its gradient, to 2 decimal places.")
    if random.random() < 0.3:
        mx = random.choice([0.2, 0.25, 0.3, 0.4, 0.5])
        if G != mx and (G < mx) == (v / h < mx):
            ok = v / h <= mx
            ans, opts = _yes_no(ok, "Safe", "Not safe")
            pa = make_part("(a)", "Calculate the gradient of the ramp, to 2 decimal places.", G, scaffold_steps=steps,
                           worked_solution=[ln.replace("**", "") for ln in lines], distractors=_dist(G, wrong))
            pb = make_part("(b)", f"The ramp is safe if its gradient is no more than {_g(mx)}. Is it safe? Use your "
                                  f"working to justify your answer.", ans, options=opts,
                           worked_solution=[f"{_g(G)} {'<' if ok else '>'} {_g(mx)}, so {ans.lower()}"],
                           distractors=[{"value": opts[1] if ok else opts[0],
                                         "mistake": "compare your gradient with the maximum."}])
            parts = [pa, pb]
            return Question(question_text=f"A boat ramp is {_g(L)} m long (the sloping length) and covers a "
                                          f"horizontal distance of {_g(h)} m, as shown.",
                            correct_answer=ans, topic=TOPIC, question_type=QTYPE,
                            worked_solution=multipart_worked_solution(parts), notes=NOTES_PYTH, metadata=meta,
                            parts=parts)
    return Question(question_text=text, correct_answer=G, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                    worked_solution=lines, notes=NOTES_PYTH, metadata=meta, distractors=_dist(G, wrong))
