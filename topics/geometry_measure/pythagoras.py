import random
import math
from core.models.question_model import Question

NOTES = """
**Pythagoras' Theorem:**

In a right-angled triangle: **a² + b² = c²**  (where **c** is the hypotenuse)

- **Finding the hypotenuse:** c = √(a² + b²)
- **Finding a shorter side:** a = √(c² − b²)

**Common Pythagorean triples:** 3-4-5 · 5-12-13 · 8-15-17
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


def generate_pythagoras_question():
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


# ---------------------------------------------------------------------------
# Dispatcher — randomly picks between the two question types
# ---------------------------------------------------------------------------

def generate_pythagoras_question():
    if random.choice([True, False]):
        return generate_two_triangle_question()
    return generate_isosceles_height_question()
