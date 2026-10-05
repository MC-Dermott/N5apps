"""Pythagoras' theorem — National 4 (generate_pythagoras_question_n4) and National 5.

National 5 mirrors Pythagoras_Worksheet.docx (N5 Apps/Worksheets/Geometry and Measure) in five levels,
generate_pythagoras_l1 … _l5 (see the block further down), dispatched by generate_pythagoras_question().
The older generators (generate_pythagoras_basic, generate_two_triangle_question,
generate_isosceles_height_question) are kept but are no longer in the N5 dispatcher.
"""
import random
import math
from core.models.question_model import Question

NOTES = """
**Pythagoras' Theorem:**

In a right-angled triangle: **a² + b² = c²**  (where **c** is the hypotenuse)

- **Finding the hypotenuse:** c = √(a² + b²)
- **Finding a shorter side:** a = √(c² − b²)

**Common Pythagorean triples:** 3-4-5 · 5-12-13 · 8-15-17

**Example:** A right-angled triangle has shorter sides 6 and 8. Find the hypotenuse.
- c = √(6² + 8²) = √(36 + 64) = √100 = **10**
"""

TRIPLES = [
    (3, 4, 5), (5, 12, 13), (8, 15, 17),
    (6, 8, 10), (9, 12, 15), (5, 5, None),  # non-triple handled specially
]

CLEAN_TRIPLES = [
    (3, 4, 5), (5, 12, 13), (8, 15, 17),
    (6, 8, 10), (9, 12, 15), (10, 24, 26),
    (12, 16, 20), (15, 20, 25), (7, 24, 25),
]


def generate_pythagoras_basic():
    """Whole-number hypotenuse or shorter side from a Pythagorean triple (kept from the original app)."""
    a, b, c = random.choice(CLEAN_TRIPLES)
    scale = random.choice([1, 2, 3])
    a, b, c = a * scale, b * scale, c * scale

    find_hyp = random.choice([True, False])

    if find_hyp:
        question_text = (
            f"A right-angled triangle has shorter sides of {a} cm and {b} cm. "
            f"Calculate the length of the hypotenuse."
        )
        answer = c
        scaffold_steps = [
            {"prompt": "Square the first shorter side", "answer": float(a ** 2)},
            {"prompt": "Square the second shorter side", "answer": float(b ** 2)},
            {"prompt": "Add the two squared values together", "answer": float(a**2 + b**2)},
            {"prompt": "Take the square root to find the hypotenuse", "answer": float(c)},
        ]
        worked = [
            "c² = a² + b²",
            f"c² = {a}² + {b}² = {a**2} + {b**2} = {a**2 + b**2}",
            f"c = √{a**2 + b**2} = {c} cm",
        ]
    else:
        question_text = (
            f"A right-angled triangle has a hypotenuse of {c} cm and one shorter side of {b} cm. "
            f"Calculate the length of the missing side."
        )
        answer = a
        scaffold_steps = [
            {"prompt": "Square the hypotenuse", "answer": float(c ** 2)},
            {"prompt": "Square the known shorter side", "answer": float(b ** 2)},
            {"prompt": "Subtract to find the missing squared value", "answer": float(c**2 - b**2)},
            {"prompt": "Take the square root to find the missing side", "answer": float(a)},
        ]
        worked = [
            "a² = c² − b²",
            f"a² = {c}² − {b}² = {c**2} − {b**2} = {c**2 - b**2}",
            f"a = √{c**2 - b**2} = {a} cm",
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Geometry and Measure",
        question_type="Pythagoras Theorem",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Two-triangle question type
# ---------------------------------------------------------------------------

TWO_TRIANGLE_NOTES = """
**Pythagoras in two triangles:**

When a triangle is split into two right-angled triangles by a straight line dropped
at right angles to the base, you need two steps:

1. Use Pythagoras in the **first triangle** to find the height
2. Use that height in the **second triangle** to find the missing side

**Finding a shorter side:** a = √(c² − b²)

**Finding the longest side:** c = √(a² + b²)

**Example:** Triangle ABD has AD = 5, AB = 13. Triangle BDC has DC = 8.
- Height BD = √(13² − 5²) = √(169 − 25) = √144 = 12
- AC = √(12² + 8²) = √(144 + 64) = √208 ≈ **14.4**
"""

# (AD, BD, AB, DC, AC) — exact Pythagorean triples in both sub-triangles
_N4_TRIPLES = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17)]


def generate_pythagoras_question_n4():
    a, b, c = random.choice(_N4_TRIPLES)
    find_hyp = random.choice([True, False])

    if find_hyp:
        question_text = (
            f"A right-angled triangle has shorter sides of {a} cm and {b} cm. "
            f"Calculate the length of the hypotenuse."
        )
        answer = c
        scaffold_steps = [
            {"prompt": "Square the first shorter side", "answer": float(a ** 2)},
            {"prompt": "Square the second shorter side", "answer": float(b ** 2)},
            {"prompt": "Add the two squared values together", "answer": float(a**2 + b**2)},
            {"prompt": "Take the square root to find the hypotenuse", "answer": float(c)},
        ]
        worked = [
            "c² = a² + b²",
            f"c² = {a}² + {b}² = {a**2} + {b**2} = {a**2 + b**2}",
            f"c = √{a**2 + b**2} = {c} cm",
        ]
    else:
        question_text = (
            f"A right-angled triangle has a hypotenuse of {c} cm and one shorter side of {b} cm. "
            f"Calculate the length of the missing side."
        )
        answer = a
        scaffold_steps = [
            {"prompt": "Square the hypotenuse", "answer": float(c ** 2)},
            {"prompt": "Square the known shorter side", "answer": float(b ** 2)},
            {"prompt": "Subtract to find the missing squared value", "answer": float(c**2 - b**2)},
            {"prompt": "Take the square root to find the missing side", "answer": float(a)},
        ]
        worked = [
            "a² = c² − b²",
            f"a² = {c}² − {b}² = {c**2} − {b**2} = {c**2 - b**2}",
            f"a = √{c**2 - b**2} = {a} cm",
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Geometry and Measure",
        question_type="Pythagoras Theorem",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


_TWO_TRI_SETUPS = [
    (12,  5, 13,  9, 15),
    (12,  9, 15,  5, 13),
    ( 8, 15, 17,  6, 10),
    ( 8,  6, 10, 15, 17),
    (20, 15, 25, 21, 29),
    (24,  7, 25, 10, 26),
    (15, 20, 25, 36, 39),
    (16, 12, 20, 30, 34),
    (12, 16, 20,  5, 13),
]

_TWO_TRI_CONTEXTS = [
    {
        "intro": "The diagram shows a triangular garden.",
        "perp_note": "A straight path cuts down from the top of the garden to the base at right angles, splitting it into two right-angled triangles.",
        "ask": "The gardener wants to put fencing along the side marked ?. Calculate its length.",
        "unit": "m",
    },
    {
        "intro": "The diagram shows a triangular field.",
        "perp_note": "A drainage ditch runs straight down from the top of the field to the base at right angles.",
        "ask": "Calculate the length of fencing needed for the side marked ?.",
        "unit": "m",
    },
    {
        "intro": "The diagram shows a triangular section of a park.",
        "perp_note": "A straight path runs from the top of the triangle down to the base at right angles.",
        "ask": "A fence is to be built along the side marked ?. Calculate its length.",
        "unit": "m",
    },
    {
        "intro": "The diagram shows a triangular piece of fabric.",
        "perp_note": "A straight cut at right angles to the base divides it into two right-angled triangles.",
        "ask": "Ribbon is to be sewn along the edge marked ?. Calculate the length of ribbon needed.",
        "unit": "cm",
    },
    {
        "intro": "The diagram shows a triangular flower bed.",
        "perp_note": "A straight edge runs from the top of the bed straight down to the base at right angles.",
        "ask": "Edging strip is needed along the side marked ?. Calculate its length.",
        "unit": "m",
    },
]


def generate_two_triangle_question():
    AD, BD, AB, DC, AC = random.choice(_TWO_TRI_SETUPS)
    ctx = random.choice(_TWO_TRI_CONTEXTS)
    unit = ctx["unit"]
    find_ac = random.choice([True, False])

    # "left base" = BD, "right base" = DC
    # find_ac=True  → unknown is right sloping side (AC), known sloping side is AB (left)
    # find_ac=False → unknown is left sloping side (AB), known sloping side is AC (right)

    if find_ac:
        known = f"The left base is {BD} {unit}, the right base is {DC} {unit} and the left sloping side is {AB} {unit}."
        answer = float(AC)
        step1_side, step1_ans = "left", float(AD)
        step2_side = "right"
        worked = [
            f"Find the height using the left triangle:",
            f"height² = {AB}² − {BD}² = {AB**2} − {BD**2} = {AB**2 - BD**2}",
            f"height = √{AD**2} = {AD} {unit}",
            f"Find the missing side using the right triangle:",
            f"missing side² = {AD}² + {DC}² = {AD**2} + {DC**2} = {AD**2 + DC**2}",
            f"missing side = √{AC**2} = {AC} {unit}",
        ]
    else:
        known = f"The left base is {BD} {unit}, the right base is {DC} {unit} and the right sloping side is {AC} {unit}."
        answer = float(AB)
        step1_side, step1_ans = "right", float(AD)
        step2_side = "left"
        worked = [
            f"Find the height using the right triangle:",
            f"height² = {AC}² − {DC}² = {AC**2} − {DC**2} = {AC**2 - DC**2}",
            f"height = √{AD**2} = {AD} {unit}",
            f"Find the missing side using the left triangle:",
            f"missing side² = {AD}² + {BD}² = {AD**2} + {BD**2} = {AD**2 + BD**2}",
            f"missing side = √{AB**2} = {AB} {unit}",
        ]

    question_text = (
        f"{ctx['intro']} "
        f"{ctx['perp_note']} "
        f"{known} "
        f"{ctx['ask']}"
    )

    scaffold_steps = [
        {
            "prompt": f"Use Pythagoras in the {step1_side} triangle to find the height",
            "answer": step1_ans,
        },
        {
            "prompt": f"Use the height in the {step2_side} triangle to find the missing side",
            "answer": answer,
        },
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Geometry and Measure",
        question_type="Pythagoras (Two Triangles)",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=TWO_TRIANGLE_NOTES,
        metadata={
            "diagram": "two_triangle",
            "unit": unit,
            "diagram_params": {
                "BD": BD, "DC": DC, "AD": AD, "AB": AB, "AC": AC,
                "find_ac": find_ac,
            },
        },
    )


# ---------------------------------------------------------------------------
# Isosceles height question type
# ---------------------------------------------------------------------------

ISOSCELES_NOTES = """
**Finding the height of an isosceles triangle:**

An isosceles triangle has two equal sloping sides. Dropping a line straight
down from the top to the middle of the base splits it into two identical
right-angled triangles.

In each right-angled triangle:
- The **sloping side** is the longest side
- **Half the base** is one of the shorter sides
- The **height** is the other shorter side

Use Pythagoras: **height² = sloping side² − half base²**

**Example:** An isosceles triangle has base 10 and sloping sides of 13.
- Half base = 10 ÷ 2 = 5
- Height = √(13² − 5²) = √(169 − 25) = √144 = **12**
"""

# (h, half_base, s) — height, half-base, sloping side; all exact Pythagorean triples
_ISO_SETUPS = [
    ( 4,  3,  5),   # base=6,  sides=5
    (12,  5, 13),   # base=10, sides=13
    (15,  8, 17),   # base=16, sides=17
    ( 8,  6, 10),   # base=12, sides=10
    (12,  9, 15),   # base=18, sides=15
    (24,  7, 25),   # base=14, sides=25
    (24, 10, 26),   # base=20, sides=26
    (16, 12, 20),   # base=24, sides=20
    (20, 15, 25),   # base=30, sides=25
]

_ISO_CONTEXTS = [
    {
        "intro": "The diagram shows the end wall of a shed.",
        "describe": "The triangular section at the top has equal sloping sides of {s} {unit} and a base of {base} {unit}.",
        "ask": "Find the height of the triangular section.",
        "unit": "m",
    },
    {
        "intro": "The diagram shows a triangular road sign.",
        "describe": "Each sloping side is {s} {unit} and the base is {base} {unit}.",
        "ask": "Find the height of the sign.",
        "unit": "cm",
    },
    {
        "intro": "The diagram shows a triangular banner.",
        "describe": "Each sloping side is {s} {unit} and the base is {base} {unit}.",
        "ask": "Find the height of the banner.",
        "unit": "cm",
    },
    {
        "intro": "The diagram shows a triangular garden feature.",
        "describe": "Each sloping side is {s} {unit} and the base is {base} {unit}.",
        "ask": "Find the height of the triangle.",
        "unit": "m",
    },
    {
        "intro": "The diagram shows a triangular roof section.",
        "describe": "Each sloping side is {s} {unit} and the base is {base} {unit}.",
        "ask": "Find the height of the roof.",
        "unit": "m",
    },
]


def generate_isosceles_height_question():
    h, half_base, s = random.choice(_ISO_SETUPS)
    base = 2 * half_base
    ctx = random.choice(_ISO_CONTEXTS)
    unit = ctx["unit"]

    description = ctx["describe"].format(s=s, base=base, unit=unit)
    question_text = f"{ctx['intro']} {description} {ctx['ask']}"

    scaffold_steps = [
        {
            "prompt": "Square the sloping side and subtract the half base squared",
            "answer": float(h ** 2),
        },
        {
            "prompt": "Take the square root to find the height",
            "answer": float(h),
        },
    ]

    worked = [
        "Drop a line from the top to the middle of the base to make a right-angled triangle.",
        f"height² = sloping side² − half base²",
        f"height² = {s}² − {half_base}² = {s**2} − {half_base**2} = {h**2}",
        f"height = √{h**2} = {h} {unit}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(h),
        topic="Geometry and Measure",
        question_type="Pythagoras Theorem",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=ISOSCELES_NOTES,
        metadata={
            "diagram": "isosceles_height",
            "unit": unit,
            "diagram_params": {
                "h": h, "half_base": half_base, "s": s,
            },
        },
    )


# ===========================================================================
# National 5 levels — mirror Pythagoras_Worksheet.docx (N5 Apps/Worksheets/Geometry and Measure):
#   L1 the hypotenuse, L2 a shorter side, L3 the height and area of an isosceles triangle,
#   L4 Pythagoras inside a problem, L5 two right-angled triangles.
# Every value is rounded to 2 d.p. at each step, as the worksheet's working does; number sets where
# that would change the final answer compared with exact arithmetic are re-drawn.
# Distractors are the errors in the course reports and marking instructions (COMMON-ERRORS.md):
# subtracting for a hypotenuse (2025 MI), no square root (2019 MI), 10² = 20 (2018 CR), adding for a
# shorter side (2023 CR, 2024 MI), the sloping side used as the height (2018 MI, 2022 MI/CR), the
# wrong dimensions (2024 CR/MI), the rolls not rounded up (2021 MI), an area instead of the
# perimeter (2025 CR), the diameter used as the radius (2022 MI).
# Diagrams: topics/geometry_measure/pythagoras_diagrams.py (the worksheet's own drawings).
# ===========================================================================
from decimal import Decimal, ROUND_HALF_UP

from core.models.distractors import distractors

TOPIC, QTYPE = "Geometry and Measure", "Pythagoras Theorem"
_DM = "topics.geometry_measure.pythagoras_diagrams"


def _r(x):
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _g(x):
    x = float(x)
    return str(int(x)) if x == int(x) else f"{x:.6f}".rstrip("0").rstrip(".")


def _sq(x):
    return _r(x * x)


def _diagram(kind, *args):
    return {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DM, "kind": kind, "args": list(args)}}


def _hyp(a, b, u, v="c", at=None):
    """(worked lines, steps, c) for c² = a² + b²."""
    A, B = _sq(a), _sq(b); S = _r(A + B); c = _r(math.sqrt(S))
    lines = [f"{v}² = {at or _g(a)}² + {_g(b)}² = {_g(A)} + {_g(B)} = {_g(S)}", f"{v} = √{_g(S)} = {_g(c)} {u}"]
    steps = [{"prompt": f"{v}² = {at or _g(a)}² + {_g(b)}²", "answer": S},
             {"prompt": f"{v} = √{_g(S)} (2 d.p.)", "answer": c}]
    return lines, steps, c


def _leg(c, b, u, v="a", bt=None):
    """(worked lines, steps, a) for a² = c² − b²."""
    C, B = _sq(c), _sq(b); D = _r(C - B); a = _r(math.sqrt(D))
    lines = [f"{v}² = {_g(c)}² − {bt or _g(b)}² = {_g(C)} − {_g(B)} = {_g(D)}", f"{v} = √{_g(D)} = {_g(a)} {u}"]
    steps = [{"prompt": f"{v}² = {_g(c)}² − {bt or _g(b)}²", "answer": D},
             {"prompt": f"{v} = √{_g(D)} (2 d.p.)", "answer": a}]
    return lines, steps, a


def _draw(make):
    """Call make() until its 2 d.p. chain gives the same answer as exact arithmetic."""
    for _ in range(200):
        out = make()
        if out is not None and abs(out["ans"] - _r(out["exact"])) < 1e-9:
            return out
    raise RuntimeError("no number set found")


def _q(out, notes):
    steps = out["steps"]
    if not steps or abs(steps[-1]["answer"] - out["ans"]) > 1e-9:
        steps = steps + [{"prompt": "Answer", "answer": out["ans"]}]
    return Question(question_text=out["text"], correct_answer=out["ans"], topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=out["worked"], notes=notes,
                    metadata=out.get("meta", {}), distractors=distractors(out["ans"], out["wrong"]))


def _one_dp(lo, hi):
    return round(random.uniform(lo, hi), 1)


NOTES_L1 = """
**Finding the hypotenuse**

The hypotenuse is the longest side, opposite the right angle. **c² = a² + b²** — square the two
shorter sides, **ADD**, then **square root**.

**Example (from the worksheet):** A croft field is a rectangle 80 m long and 45 m wide. A path runs
diagonally across it. Calculate the length of the path.
- c² = 80² + 45²
- c² = 6400 + 2025 = 8425
- c = √8425 = **91.79 m**

⚠ Subtracting instead of adding, or forgetting the square root. In 2025 some candidates wrote 9² − 6²
for a hypotenuse, and in 2019 295² + 300² = 177025 with no square root scored only 1 mark out of 4
(marking instructions). In 2018 many wrote 10² = 20 instead of 100 (course report).
"""

NOTES_L2 = """
**Finding a shorter side**

If you know the hypotenuse, **SUBTRACT**: **a² = c² − b²**. Write the hypotenuse squared FIRST.

**Example (from the worksheet):** A ladder 6.5 m long leans against a wall. Its foot is 1.8 m from the
wall. How far up the wall does the ladder reach?
- h² = 6.5² − 1.8²
- h² = 42.25 − 3.24 = 39.01
- h = √39.01 = **6.25 m**

⚠ Adding instead of subtracting, or writing the subtraction backwards. In 2024 many candidates added
600² + 500² (marking instructions), and 500² − 600² loses the mark — the hypotenuse squared comes
first (2019 and 2024 marking instructions).
"""

NOTES_L3 = """
**The height and area of an isosceles triangle**

The height splits an isosceles triangle into two right-angled triangles: the sloping side is the
hypotenuse and **HALF the base** is a shorter side. Area = ½ × base × **height** — not the sloping side.

**Example (from the worksheet):** A lawn is an isosceles triangle with base 12 m and sloping sides 10 m.
Calculate the area of the lawn.
- Half the base = 12 ÷ 2 = 6 m
- h² = 10² − 6² = 100 − 36 = 64
- h = √64 = 8 m
- Area = ½ × base × height = 0.5 × 12 × 8 = **48 m²**

⚠ Not seeing that you need Pythagoras for the height. In 2018 and 2022 most candidates used the
sloping side as the height — ½ × 12 × 10 = 60 scored 0 marks (2018 marking instructions; 2022 course
report). In 2018 many wrote 10² = 20 and 6² = 12. Give units.
"""

NOTES_L4 = """
**Pythagoras inside a problem**

Pythagoras is often only the first step: find the missing side, then use it — a perimeter, the number
of rolls or panels (**round UP**), a cost, an arc or an area.

**Example (from the worksheet):** A paddock on a croft is a right-angled triangle with shorter sides
40 m and 25 m. It is to be fenced all the way round. Fencing comes in 10 m rolls costing £34.50 each.
Calculate the cost of the fencing.
- c² = 40² + 25² = 1600 + 625 = 2225;  c = √2225 = 47.17 m
- Perimeter = 40 + 25 + 47.17 = 112.17 m
- Rolls = 112.17 ÷ 10 = 11.22 → 12 rolls (round up)
- Cost = 12 × £34.50 = **£414.00**

⚠ Stopping after Pythagoras. In 2025 most candidates found the hypotenuse but not the perimeter, and
some worked out an area instead (course report). In 2021 the fence panels had to be rounded UP
(marking instructions).
"""

NOTES_L5 = """
**Two right-angled triangles**

Use the first triangle to find the side they share, then use it in the second. Decide each time:
hypotenuse → **ADD**; shorter side → **SUBTRACT**.

**Example (from the worksheet):** A lighthouse is 450 m due north of a harbour, H. A boat sails due east
from the harbour. At A it is 750 m from the lighthouse. It sails a further 300 m to B. Calculate the
direct distance from B to the lighthouse.
- x² = 750² − 450² = 562500 − 202500 = 360000;  x = √360000 = 600 m
- Distance from H to B = 600 + 300 = 900 m
- d² = 450² + 900² = 202500 + 810000 = 1012500;  d = √1012500 = **1006.23 m**

⚠ Using the wrong sides. In 2024 most candidates did not pick the correct dimensions — 600² + 400² was
common (course report, marking instructions) — and in 2023 some added in the second Pythagoras
calculation when they should have subtracted (course report).
"""


def _hyp_wrong(a, b, c):
    return [(_r(math.sqrt(abs(a * a - b * b))), "you subtracted — to find the HYPOTENUSE, add the squares "
             "(2025 marking instructions: 9² − 6² was common)."),
            (_r(a * a + b * b), "you forgot the square root — that's c², not c (2019 marking instructions)."),
            (_r(math.sqrt(2 * a + 2 * b)), "squaring means × itself: 10² = 100, not 20 (2018 course report)."),
            (_r(a + b), "you added the sides — square them first, add, then square root.")]


def _leg_wrong(c, b):
    return [(_r(math.sqrt(c * c + b * b)), "you added — the hypotenuse is known, so SUBTRACT to find a shorter "
             "side (2024 marking instructions; 2023 course report)."),
            (_r(c * c - b * b), "you forgot the square root."),
            (_r(math.sqrt(abs(2 * c - 2 * b))), "squaring means × itself, not × 2 (2018 course report)."),
            (_r(c - b), "you subtracted the sides — square them first, subtract, then square root.")]


# ── Level 1: hypotenuse ───────────────────────────────────────────────────────────────────────
def generate_pythagoras_l1(calc_mode=False):
    """Find the hypotenuse."""
    def make():
        kind = random.choice(["triangle", "ramp", "field", "boat", "screen", "gate"])
        if kind == "triangle":
            a, b, u = random.randint(4, 15), random.randint(5, 20), "cm"
            text = "Calculate the length of the hypotenuse of this right-angled triangle."
            meta = _diagram("right_tri", a, b, [f"{a} cm", f"{b} cm", "?"])
        elif kind == "ramp":
            a, b, u = _one_dp(0.3, 0.9), _one_dp(3, 8), "m"
            text = (f"A wheelchair ramp rises {_g(a)} m over a horizontal distance of {_g(b)} m, as shown. "
                    f"Calculate the length of the sloping surface of the ramp.")
            meta = _diagram("ramp", a, b, [f"{_g(a)} m", f"{_g(b)} m", "?"])
        elif kind == "field":
            b, a, u = random.choice([50, 60, 70, 80, 90, 100]), random.choice([25, 30, 35, 40, 45]), "m"
            text = (f"A croft field is a rectangle {b} m long and {a} m wide. A path runs diagonally across "
                    f"it, as shown. Calculate the length of the path.")
            meta = _diagram("rect_diag", b, a, [f"{b} m", f"{a} m", "?"])
        elif kind == "boat":
            a, b, u = random.randint(3, 12), random.randint(3, 12), "km"
            port = random.choice(["Leverburgh", "Castlebay", "Lochboisdale", "Tarbert", "Stornoway"])
            text = (f"A boat leaves {port} and sails {b} km due east, then {a} km due north. Calculate its "
                    f"direct distance from {port}.")
            meta = {}
        elif kind == "screen":
            b, a, u = random.choice([80, 100, 110, 120, 140]), random.choice([45, 56, 62, 68, 79]), "cm"
            text = (f"A television screen is {b} cm wide and {a} cm high. Calculate the length of its "
                    f"diagonal.")
            meta = {}
        else:
            b, a, u = _one_dp(2.5, 4), _one_dp(1.1, 1.8), "m"
            text = (f"A field gate is {_g(b)} m wide and {_g(a)} m high. A wooden brace runs diagonally from "
                    f"one corner to the opposite corner. Calculate the length of the brace.")
            meta = {}
        lines, steps, c = _hyp(a, b, u)
        if abs(c - round(c)) < 1e-9:
            return None                                      # keep it a 2 d.p. answer
        return dict(text=text + " Give your answer to 2 decimal places.", ans=c, exact=math.hypot(a, b),
                    steps=steps, worked=lines, meta=meta, wrong=_hyp_wrong(a, b, c))
    return _q(_draw(make), NOTES_L1)


# ── Level 2: a shorter side ───────────────────────────────────────────────────────────────────
def generate_pythagoras_l2(calc_mode=False):
    """Find a shorter side (subtract)."""
    def make():
        kind = random.choice(["ladder", "triangle", "kite", "slipway", "rectangle", "boat"])
        meta = {}
        if kind == "ladder":
            c, b, u, v = _one_dp(4, 8), _one_dp(1, 2.2), "m", "h"
            text = (f"A ladder {_g(c)} m long leans against a wall. Its foot is {_g(b)} m from the wall, as "
                    f"shown. How far up the wall does the ladder reach?")
            meta = _diagram("ladder", math.sqrt(c * c - b * b), b, [f"{_g(c)} m", "?", f"{_g(b)} m"])
        elif kind == "triangle":
            c, u, v = random.randint(10, 25), "cm", "x"
            b = random.randint(4, c - 3)
            text = "Calculate the length of the side marked x."
            meta = _diagram("right_tri", math.sqrt(c * c - b * b), b, ["x", f"{b} cm", f"{c} cm"])
        elif kind == "kite":
            c, u, v = random.choice([30, 35, 40, 45, 50, 60]), "m", "h"
            b = random.randint(12, c - 8)
            text = (f"A kite on Tolsta beach is on a string {c} m long. It is directly above a point {b} m from "
                    f"the person flying it. Calculate the height of the kite.")
        elif kind == "slipway":
            c, b, u, v = _one_dp(4, 7), _one_dp(0.3, 0.8), "m", "d"
            text = (f"The sloping surface of a slipway is {_g(c)} m long. It rises {_g(b)} m. Calculate the "
                    f"horizontal distance it covers.")
        elif kind == "rectangle":
            b, u, v = random.randint(8, 15), "m", "w"
            c = round(b + random.uniform(1, 5), 1)
            text = (f"The diagonal of a rectangular polytunnel floor is {_g(c)} m. The floor is {b} m long. "
                    f"Calculate its width.")
        else:
            c, b, u, v = _one_dp(6, 12), _one_dp(1.5, 4.5), "km", "n"
            text = (f"A fishing boat is {_g(c)} km from Stornoway harbour, in a straight line. It is {_g(b)} km "
                    f"further east than the harbour. Calculate how far north of the harbour it is.")
        if b >= c:
            return None
        lines, steps, a = _leg(c, b, u, v)
        if abs(a - round(a)) < 1e-9:
            return None
        return dict(text=text + " Give your answer to 2 decimal places.", ans=a, exact=math.sqrt(c * c - b * b),
                    steps=steps, worked=lines, meta=meta, wrong=_leg_wrong(c, b))
    return _q(_draw(make), NOTES_L2)


# ── Level 3: isosceles triangle height and area ───────────────────────────────────────────────
_ISO_NICE = [(12, 10), (16, 17), (10, 13), (24, 13), (18, 15), (14, 25), (30, 17), (60, 50), (2.4, 2), (8, 5)]


def generate_pythagoras_l3(calc_mode=False):
    """Height of an isosceles triangle, then its area (or a gable wall)."""
    def make():
        kind = random.choices(["area", "gable", "height"], weights=[3, 2, 1])[0]
        if random.random() < 0.5:
            base, side = random.choice(_ISO_NICE)
        else:
            base = random.choice([6, 8, 10, 12, 14, 16, 20, 24])
            side = random.randint(int(base / 2) + 2, base + 6)
        hb = _r(base / 2)
        u = "cm" if base >= 20 and kind != "gable" else "m"
        S, H = _sq(side), _sq(hb); D = _r(S - H); h = _r(math.sqrt(D)); he = math.sqrt(side ** 2 - base ** 2 / 4)
        lines = [f"Half the base = {_g(base)} ÷ 2 = {_g(hb)} {u}",
                 f"h² = {_g(side)}² − {_g(hb)}² = {_g(S)} − {_g(H)} = {_g(D)}", f"h = √{_g(D)} = {_g(h)} {u}"]
        steps = [{"prompt": "Half the base", "answer": hb}, {"prompt": f"h² = {_g(side)}² − {_g(hb)}²", "answer": D},
                 {"prompt": "Height h (2 d.p.)", "answer": h}]
        no_half = math.sqrt(side * side - base * base) if side > base else None
        if kind == "height":
            what = random.choice(["roof truss", "road sign", "sail", "tent end"])
            text = (f"A {what} is an isosceles triangle with base {_g(base)} {u} and sloping sides {_g(side)} {u}. "
                    f"Calculate its height. Give your answer to 2 decimal places if it isn't a whole number.")
            return dict(text=text, ans=h, exact=he, steps=steps, worked=lines,
                        meta=_diagram("isosceles", base, side, [f"{_g(base)} {u}", f"{_g(side)} {u}"]),
                        wrong=[(_r(math.sqrt(S + H)), "you added — the sloping side is the hypotenuse, so subtract "
                                "(2022 marking instructions: 13² + 5²)."),
                               (_r(no_half) if no_half else None, "use HALF the base in the right-angled triangle."),
                               (D, "you forgot the square root.")])
        A = _r(0.5 * base * h)
        wrong = [(_r(0.5 * base * side), "you used the sloping side as the height — find the height with Pythagoras "
                  "first (2018 and 2022 marking instructions)."),
                 (_r(base * h), "you forgot the ½ in the area of a triangle."),
                 (_r(0.5 * base * math.sqrt(S + H)), "you added — the sloping side is the hypotenuse, so subtract "
                  "(2022 marking instructions: 13² + 5²).")]
        if no_half:
            wrong.append((_r(0.5 * base * no_half), "use HALF the base in the right-angled triangle."))
        if kind == "area":
            what = random.choice(["lawn", "sail", "flag", "road sign", "flower bed"])
            text = (f"A {what} is an isosceles triangle with base {_g(base)} {u} and sloping sides {_g(side)} {u}, "
                    f"as shown. Calculate its area. Give your answer to 2 decimal places if it isn't a whole number.")
            return dict(text=text, ans=A, exact=0.5 * base * he, worked=lines + [
                f"Area = ½ × base × height = 0.5 × {_g(base)} × {_g(h)} = **{_g(A)} {u}²**"],
                steps=steps + [{"prompt": "Area = ½ × base × height", "answer": A}],
                meta=_diagram("isosceles", base, side, [f"{_g(base)} {u}", f"{_g(side)} {u}"]), wrong=wrong)
        hr = random.choice([2, 2.5, 3, 3.5, 4])
        if base > 12:
            return None
        R = _r(base * hr); tot = _r(A + R)
        text = (f"The end wall of a croft house is a rectangle {_g(base)} m wide and {_g(hr)} m high with an isosceles "
                f"triangle on top, as shown. The sloping sides of the triangle are {_g(side)} m. Calculate the area "
                f"of the wall. Give your answer to 2 decimal places if it isn't a whole number.")
        return dict(text=text, ans=tot, exact=0.5 * base * he + base * hr, worked=lines + [
            f"Triangle = 0.5 × {_g(base)} × {_g(h)} = {_g(A)} m²", f"Rectangle = {_g(base)} × {_g(hr)} = {_g(R)} m²",
            f"Total area = {_g(A)} + {_g(R)} = **{_g(tot)} m²**"],
            steps=steps + [{"prompt": "Area of the triangle", "answer": A}, {"prompt": "Area of the rectangle", "answer": R},
                           {"prompt": "Total area", "answer": tot}],
            meta=_diagram("gable", base, hr, side, [f"{_g(base)} m", f"{_g(hr)} m", f"{_g(side)} m"]),
            wrong=[(_r(v + R), m) for v, m in wrong] + [(A, "add the rectangle as well.")])
    return _q(_draw(make), NOTES_L3)


# ── Level 4: Pythagoras inside a problem ──────────────────────────────────────────────────────
def generate_pythagoras_l4(calc_mode=False):
    """Hypotenuse, then a perimeter / rolls / cost / arc / roof area / circle."""
    def make():
        kind = random.choice(["fence", "badge", "rect_fence", "roof", "table"])
        pi = math.pi
        if kind == "fence":
            a, b = random.randint(8, 45), random.randint(6, 35)
            roll, price = random.choice([(2, 21.40), (3, 22), (10, 34.50), (5, 28.75), (2, 18.60)])
            what = "panels" if roll <= 2 else "rolls"
            L, st, c = _hyp(a, b, "m")
            P = _r(a + b + c); q = P / roll; n = math.ceil(q - 1e-9)
            if abs(q - round(q)) < 0.02:
                return None
            cost = _r(n * price)
            text = (f"A garden is a right-angled triangle with shorter sides {a} m and {b} m. It is to be fenced on all "
                    f"three sides. Fencing comes in {roll} m {what} costing £{price:.2f} each. Calculate the cost of "
                    f"the fencing.")
            worked = L + [f"Perimeter = {a} + {b} + {_g(c)} = {_g(P)} m",
                          f"{what.capitalize()} = {_g(P)} ÷ {roll} = {_g(_r(q))} → {n} {what} (round up)",
                          f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
            steps = st + [{"prompt": "Perimeter", "answer": P}, {"prompt": f"Number of {what} (round up)", "answer": float(n)},
                          {"prompt": "Cost (£)", "answer": cost}]
            exact = math.ceil((a + b + math.hypot(a, b)) / roll) * price
            wrong = [(_r(math.floor(q) * price), "round UP — you can't buy part of a roll (2021 marking instructions)."),
                     (_r(math.ceil((a + b) / roll) * price), "the hypotenuse needs fencing too — find it with Pythagoras."),
                     (_r(math.ceil(c / roll) * price), "fence all three sides, not just the hypotenuse.")]
            return dict(text=text, ans=cost, exact=exact, steps=steps, worked=worked, wrong=wrong,
                        meta=_diagram("right_tri", b, a, [f"{b} m", f"{a} m", ""]))
        if kind == "badge":
            a, b = random.randint(3, 9), random.randint(4, 12)
            L, st, c = _hyp(a, b, "cm")
            arc = _r(pi * c / 2); P = _r(a + b + arc)
            text = ("A badge is a right-angled triangle with a semi-circle on its hypotenuse, as shown. Calculate the "
                    "perimeter of the badge. Give your answer to 2 decimal places.")
            worked = L + [f"Semi-circle = π × d ÷ 2 = π × {_g(c)} ÷ 2 = {_g(arc)} cm",
                          f"Perimeter = {a} + {b} + {_g(arc)} = **{_g(P)} cm**"]
            steps = st + [{"prompt": "Curved edge = π × d ÷ 2", "answer": arc}, {"prompt": "Perimeter", "answer": P}]
            exact = a + b + pi * math.hypot(a, b) / 2
            wrong = [(_r(a + b + pi * (c / 2) ** 2 / 2), "that uses the AREA of the semi-circle — the edge is a length "
                      "(2025 course report)."),
                     (_r(a + b + pi * c), "a semi-circle's edge is HALF of πd."),
                     (_r(a + b + c + arc), "the hypotenuse is inside the badge — it isn't part of the edge."),
                     (arc, "add the two straight sides too (2025 course report: most didn't find the perimeter).")]
            return dict(text=text, ans=P, exact=exact, steps=steps, worked=worked, wrong=wrong,
                        meta=_diagram("badge", a, b, [f"{a} cm", f"{b} cm"]))
        if kind == "rect_fence":
            Lg, W = random.choice([40, 50, 60, 70, 80]), random.choice([25, 30, 35, 40, 45])
            price = random.choice([6.50, 7.50, 8.50, 9.50, 12.25])
            L, st, d = _hyp(Lg, W, "m", "d")
            F = _r(2 * Lg + 2 * W + d); cost = _r(F * price)
            if Lg == W:
                return None
            text = (f"A rectangular field is {Lg} m long and {W} m wide. A fence goes all the way round and also "
                    f"along one diagonal. Fencing costs £{price:.2f} per metre. Calculate the cost of the fencing.")
            worked = L + [f"Fencing = 2 × {Lg} + 2 × {W} + {_g(d)} = {_g(F)} m", f"Cost = {_g(F)} × £{price:.2f} = **£{cost:.2f}**"]
            steps = st + [{"prompt": "Total length of fencing", "answer": F}, {"prompt": "Cost (£)", "answer": cost}]
            exact = (2 * Lg + 2 * W + math.hypot(Lg, W)) * price
            wrong = [(_r((2 * Lg + 2 * W) * price), "you left out the diagonal."),
                     (_r((Lg + W + d) * price), "fence ALL FOUR sides and the diagonal."),
                     (_r(d * price), "the fence goes round the field as well as along the diagonal.")]
            return dict(text=text, ans=cost, exact=exact, steps=steps, worked=worked, wrong=wrong,
                        meta=_diagram("rect_diag", Lg, W, [f"{Lg} m", f"{W} m", ""]))
        if kind == "roof":
            w, t, ln = random.choice([5, 6, 7, 8, 9]), _one_dp(1, 2.5), random.choice([6, 8, 9, 10, 12])
            hw = _r(w / 2)
            L, st, r = _hyp(hw, t, "m", "r")
            A = _r(2 * r * ln)
            text = (f"The roof of a shed is {w} m wide and rises {_g(t)} m in the middle, as shown. Both sloping "
                    f"sides of the roof are rectangles {ln} m long. Calculate the total area of the roof. Give your "
                    f"answer to 2 decimal places.")
            worked = [f"Half the width = {w} ÷ 2 = {_g(hw)} m"] + L + [f"Roof area = 2 × {_g(r)} × {ln} = **{_g(A)} m²**"]
            steps = [{"prompt": "Half the width", "answer": hw}] + st + [{"prompt": "Roof area", "answer": A}]
            exact = 2 * math.hypot(w / 2, t) * ln
            wrong = [(_r(r * ln), "there are TWO sloping sides."),
                     (_r(2 * math.hypot(w, t) * ln), "use HALF the width in the right-angled triangle."),
                     (_r(w * ln), "the roof slopes — use the sloping length, found with Pythagoras.")]
            return dict(text=text, ans=A, exact=exact, steps=steps, worked=worked, wrong=wrong,
                        meta=_diagram("isosceles", w, math.hypot(w / 2, t), [f"{w} m", "", f"{_g(t)} m", ""]))
        s = random.choice([20, 24, 30, 36, 40, 50])
        L, st, d = _hyp(s, s, "cm", "d")
        A = _r(pi * s * s / 2)
        text = (f"A square table top has sides {s} cm. It just fits inside a circular stand, so the diagonal of the "
                f"square is the diameter of the circle. Calculate the area of the circle. Give your answer to 2 "
                f"decimal places.")
        worked = L + [f"r² = d² ÷ 4 = {_g(2 * s * s)} ÷ 4 = {_g(s * s / 2)}", f"Area = π × r² = π × {_g(s * s / 2)} = **{_g(A)} cm²**"]
        steps = st + [{"prompt": "Area = π × r²", "answer": A}]
        wrong = [(_r(pi * 2 * s * s), "you used the diameter as the radius — halve it (2022 marking instructions)."),
                 (_r(pi * s * s), "the diameter is the DIAGONAL of the square, not its side (2022 marking instructions)."),
                 (_r(pi * (s / 2) ** 2), "the diameter is the diagonal — find it with Pythagoras (2022 course report)."),
                 (_r(pi * d), "that's the circumference — the question asks for the area.")]
        return dict(text=text, ans=A, exact=pi * s * s / 2, steps=steps, worked=worked, wrong=wrong)
    return _q(_draw(make), NOTES_L4)


# ── Level 5: two right-angled triangles ───────────────────────────────────────────────────────
def generate_pythagoras_l5(calc_mode=False):
    """Pythagoras twice: the 2024 lighthouse, the 2026 golf ball, the 2019 cables, the 2023 fence."""
    def make():
        kind = random.choice(["ext", "ext_h", "cable", "split_base", "fence2"])
        H, hy = math.hypot, (lambda c, b: math.sqrt(c * c - b * b))
        if kind == "ext":
            h = random.choice([300, 350, 400, 450, 500, 600])
            x1 = random.choice([250, 300, 400, 450, 500, 550])
            x2 = random.choice([200, 250, 300, 350, 400])
            s1 = round(H(h, x1))
            if s1 <= h:
                return None
            L1, st1, X1 = _leg(s1, h, "m", "x")
            X = _r(X1 + x2)
            L2, st2, d = _hyp(h, X, "m", "d", None)
            text = (f"A lighthouse is {h} m due north of a harbour, H. A boat sails due east from the harbour. At A it is "
                    f"{s1} m from the lighthouse. It sails a further {x2} m to B, as shown. Calculate the direct "
                    f"distance from B to the lighthouse. Give your answer to 2 decimal places.")
            worked = L1 + [f"Distance from H to B = {_g(X1)} + {x2} = {_g(X)} m"] + L2
            steps = st1 + [{"prompt": "Distance from H to B", "answer": X}] + st2
            exact = H(h, hy(s1, h) + x2)
            wrong = [(_r(H(s1, x2)), f"{s1} m and {x2} m aren't sides of one right-angled triangle (2024 marking "
                      f"instructions: 600² + 400²)."),
                     (_r(H(h, x2)), "use the whole distance from H to B (2024 marking instructions: 400² + 500²)."),
                     (_r(H(h, H(s1, h) + x2)), "you added in the first triangle — the lighthouse-to-A distance is the "
                      "hypotenuse, so subtract (2024 marking instructions)."),
                     (_r(math.sqrt(abs((hy(s1, h) + x2) ** 2 - h * h))),
                      "the distance to the lighthouse is the hypotenuse — ADD in the second triangle.")]
            return dict(text=text, ans=d, exact=exact, steps=steps, worked=worked, wrong=wrong,
                        meta=_diagram("two_tri_ext", h, hy(s1, h), x2,
                                      [f"{h} m", f"{s1} m", f"{x2} m", "", "lighthouse", "H", "A", "B"]))
        if kind == "ext_h":
            x1 = random.choice([60, 70, 80, 90, 100])
            s1 = x1 + random.choice([3, 4, 5, 6, 8, 10])
            x2 = random.choice([30, 40, 45, 50, 60])
            L1, st1, h = _leg(s1, x1, "m", "h")
            X = x1 + x2
            L2, st2, d = _hyp(h, X, "m", "d", at=_g(h))
            text = (f"A drone hovers directly above a point P. Morag stands {x1} m from P and the drone is {s1} m from "
                    f"her. Iain stands a further {x2} m from P, in a straight line with Morag and P, as shown. Calculate "
                    f"the distance from Iain to the drone. Give your answer to 2 decimal places.")
            worked = L1 + [f"Distance from P to Iain = {x1} + {x2} = {X} m"] + L2
            steps = st1 + [{"prompt": "Distance from P to Iain", "answer": float(X)}] + st2
            exact = H(hy(s1, x1), X)
            wrong = [(_r(H(H(s1, x1), X)), "you added in the first triangle — the drone-to-Morag distance is the "
                      "hypotenuse, so subtract (2026 marking instructions: 274² + 270²)."),
                     (_r(H(s1, x2)), f"{s1} m and {x2} m aren't sides of one right-angled triangle (2024 marking instructions)."),
                     (_r(H(hy(s1, x1), x2)), f"use the whole distance from P to Iain: {x1} + {x2}.")]
            return dict(text=text, ans=d, exact=exact, steps=steps, worked=worked, wrong=wrong,
                        meta=_diagram("two_tri_ext", hy(s1, x1), x1, x2,
                                      ["", f"{s1} m", f"{x2} m", "", "drone", "P", "Morag", "Iain", f"{x1} m"]))
        if kind == "cable":
            bl = random.choice([60, 70, 75, 80, 90])
            s1 = bl + random.choice([5, 8, 10, 12, 15])
            br = random.choice([100, 120, 140, 150, 160])
            L1, st1, h = _leg(s1, bl, "m", "h")
            L2, st2, c = _hyp(h, br, "m", "c", at=_g(h))
            T = _r(s1 + c)
            text = (f"Two cables hold up a mast, as shown. One cable is {s1} m long and reaches the ground {bl} m from "
                    f"the foot of the mast. The other reaches the ground {br} m from the foot of the mast on the other "
                    f"side. Calculate the total length of the two cables. Give your answer to 2 decimal places.")
            worked = L1 + L2 + [f"Total = {s1} + {_g(c)} = **{_g(T)} m**"]
            steps = st1 + st2 + [{"prompt": "Total length of cable", "answer": T}]
            exact = s1 + H(hy(s1, bl), br)
            wrong = [(c, f"add the {s1} m cable too."),
                     (_r(s1 + H(H(s1, bl), br)), "you added in the first triangle — the cable is the hypotenuse, so "
                      "subtract to find the height (2019 marking instructions)."),
                     (_r(s1 * s1 - bl * bl), "you forgot the square root (2019 marking instructions: 295² + 300² = 177025).")]
            return dict(text=text, ans=T, exact=exact, steps=steps, worked=worked, wrong=wrong,
                        meta=_diagram("split_tri", bl, br, hy(s1, bl), [f"{s1} m", "?", f"{bl} m", f"{br} m"]))
        if kind == "split_base":
            bl = random.randint(4, 12)
            s1 = bl + random.randint(3, 9)
            s2 = s1 + random.randint(1, 6)
            L1, st1, h = _leg(s1, bl, "m", "h")
            L2, st2, br = _leg(s2, h, "m", "y", bt=_g(h))
            B = _r(bl + br)
            text = (f"A garden is a triangle with a path at right angles to its base, as shown. The sloping sides are "
                    f"{s1} m and {s2} m, and the left part of the base is {bl} m. Calculate the length of the whole "
                    f"base. Give your answer to 2 decimal places if it isn't a whole number.")
            worked = L1 + L2 + [f"Base = {bl} + {_g(br)} = **{_g(B)} m**"]
            steps = st1 + st2 + [{"prompt": "Length of the whole base", "answer": B}]
            exact = bl + hy(s2, hy(s1, bl))
            wrong = [(_r(bl + H(s2, hy(s1, bl))), "you added in the second triangle — the sloping side is the "
                      "hypotenuse, so subtract (2023 course report)."),
                     (br, f"add the {bl} m part of the base."),
                     (_r(bl + hy(s2, bl)), "find the height first, then use it in the second triangle.")]
            return dict(text=text, ans=B, exact=exact, steps=steps, worked=worked, wrong=wrong,
                        meta=_diagram("split_tri", bl, hy(s2, hy(s1, bl)), hy(s1, bl),
                                      [f"{s1} m", f"{s2} m", f"{bl} m", "?"]))
        a, b = _one_dp(5, 9), _one_dp(3, 6)
        ab = random.choice([18, 20, 21, 22, 24, 25])
        roll, price = random.choice([(3, 22), (3, 18.50), (5, 31), (2, 14.75)])
        L1, st1, ac = _hyp(a, b, "m", "AC")
        L2, st2, bc = _leg(ab, ac, "m", "BC", bt=_g(ac))
        F = _r(ab + bc); q = F / roll; n = math.ceil(q - 1e-9)
        if abs(q - round(q)) < 0.02:
            return None
        cost = _r(n * price)
        text = (f"A patio is a right-angled triangle ADC and a lawn is a right-angled triangle ACB, as shown. "
                f"AD = {_g(b)} m, DC = {_g(a)} m and AB = {ab} m. A new fence is to be put from A to B and from B to C. "
                f"Rolls of fencing are {roll} m long and cost £{price:.2f} each. Calculate the cost of the fencing.")
        worked = L1 + L2 + [f"Fence = {ab} + {_g(bc)} = {_g(F)} m",
                            f"Rolls = {_g(F)} ÷ {roll} = {_g(_r(q))} → {n} rolls (round up)",
                            f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
        steps = st1 + st2 + [{"prompt": "Length of fence", "answer": F}, {"prompt": "Rolls (round up)", "answer": float(n)},
                             {"prompt": "Cost (£)", "answer": cost}]
        acx = H(a, b)
        exact = math.ceil((ab + hy(ab, acx)) / roll) * price
        wrong = [(_r(math.ceil((ab + H(ab, acx)) / roll - 1e-9) * price), "you added in the second triangle — AB is the "
                  "hypotenuse, so subtract (2023 course report)."),
                 (_r(math.floor(q) * price), "round UP — you can't buy part of a roll (2023 marking instructions)."),
                 (_r(math.ceil(ab / roll - 1e-9) * price), "fence B to C as well (2023 marking instructions: 21 ÷ 3 only).")]
        return dict(text=text, ans=cost, exact=exact, steps=steps, worked=worked, wrong=wrong,
                    meta=_diagram("patio_lawn", b, a, ab, [f"{_g(b)} m", f"{_g(a)} m", f"{ab} m", "A", "B", "C", "D"]))
    return _q(_draw(make), NOTES_L5)


# ---------------------------------------------------------------------------
# Dispatcher (National 5) — the worksheet's five levels
# ---------------------------------------------------------------------------

def generate_pythagoras_question(calc_mode=False):
    return random.choice([generate_pythagoras_l1, generate_pythagoras_l2, generate_pythagoras_l3,
                          generate_pythagoras_l4, generate_pythagoras_l5])(calc_mode=calc_mode)
