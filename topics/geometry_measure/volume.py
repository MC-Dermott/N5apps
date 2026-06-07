import random
import math
from core.models.question_model import Question

SPHERE_NOTES = """
**Volume of a Sphere:**

**V = (4/3) × π × r³**

- **r** is the radius
- If you are given the diameter: r = diameter ÷ 2

Give your answer to 2 decimal places.
"""

CONE_NOTES = """
**Volume of a Cone:**

**V = (1/3) × π × r² × h**

- **r** is the radius of the circular base
- **h** is the perpendicular height
- If you are given the diameter: r = diameter ÷ 2

Give your answer to 2 decimal places.
"""

CYLINDER_NOTES = """
**Volume of a Cylinder:**

**V = π × r² × h**

- **r** is the radius of the circular end
- **h** is the height (or length)
- If you are given the diameter: r = diameter ÷ 2

Give your answer to 2 decimal places.
"""

# ---------------------------------------------------------------------------
# Context tables  (template_d = diameter given, template_r = radius given)
# ---------------------------------------------------------------------------

_SPHERE_CONTEXTS = [
    {"shape": "spherical ball",        "unit": "cm", "diams": [6, 8, 10, 12, 14, 16, 18, 20]},
    {"shape": "spherical storage tank","unit": "m",  "diams": [2, 4, 6, 8, 10]},
    {"shape": "spherical marble",      "unit": "mm", "diams": [10, 12, 14, 16, 18, 20]},
    {"shape": "spherical buoy",        "unit": "m",  "diams": [1, 2, 3, 4]},
    {"shape": "spherical chocolate truffle", "unit": "cm", "diams": [2, 3, 4, 5, 6]},
]

_CONE_CONTEXTS = [
    {"shape": "traffic cone",        "unit": "cm", "diams": [14, 16, 18, 20, 24, 28, 30], "heights": [40, 45, 50, 60, 70, 75]},
    {"shape": "conical tent",        "unit": "m",  "diams": [4, 5, 6, 7, 8, 10],          "heights": [2, 3, 4, 5, 6]},
    {"shape": "cone-shaped paper cup","unit": "cm", "diams": [6, 7, 8, 9, 10],             "heights": [8, 9, 10, 11, 12, 14, 15]},
    {"shape": "conical pile of sand", "unit": "m",  "diams": [2, 3, 4, 5, 6],              "heights": [1, 2, 3, 4]},
    {"shape": "ice cream cone",       "unit": "cm", "diams": [4, 5, 6, 7, 8],              "heights": [8, 9, 10, 11, 12]},
]

_CYLINDER_CONTEXTS = [
    {"shape": "cylindrical tin can",   "unit": "cm", "diams": [6, 8, 10, 12, 14],    "heights": [8, 10, 12, 15, 18, 20]},
    {"shape": "cylindrical water tank","unit": "m",  "diams": [2, 3, 4, 6, 8],       "heights": [2, 3, 4, 5, 6, 8]},
    {"shape": "cylindrical pipe",      "unit": "mm", "diams": [20, 30, 40, 50, 60],  "heights": [100, 150, 200, 250, 300]},
    {"shape": "cylindrical drum",      "unit": "cm", "diams": [30, 40, 50, 60],      "heights": [40, 50, 60, 70, 80, 90]},
    {"shape": "cylindrical glass",     "unit": "cm", "diams": [6, 7, 8, 9, 10],      "heights": [8, 9, 10, 11, 12, 14]},
]


def _give_diameter():
    """True ~75 % of the time (mostly diameter, sometimes radius)."""
    return random.random() < 0.75


# ---------------------------------------------------------------------------
# Sphere
# ---------------------------------------------------------------------------

def generate_sphere_question():
    ctx = random.choice(_SPHERE_CONTEXTS)
    unit = ctx["unit"]
    use_diam = _give_diameter()

    d = None
    if use_diam:
        d = random.choice(ctx["diams"])
        r = d / 2
    else:
        r = random.choice(ctx["diams"]) // 2  # pick from same pool, halve

    volume = round((4 / 3) * math.pi * r ** 3, 2)

    question_text = f"Calculate the volume of the {ctx['shape']}. Give your answer to 2 decimal places."

    if use_diam:
        scaffold_steps = [
            {"prompt": "Find the radius from the diameter", "answer": r},
            {"prompt": "Cube the radius", "answer": r ** 3},
            {"prompt": "Calculate the volume using V = (4/3)πr³", "answer": volume},
        ]
        worked = [
            f"r = {d} ÷ 2 = {r} {unit}",
            f"V = (4/3) × π × {r}³",
            f"V = (4/3) × π × {r**3}",
            f"V = {volume} {unit}³",
        ]
    else:
        scaffold_steps = [
            {"prompt": "Cube the radius", "answer": r ** 3},
            {"prompt": "Calculate the volume using V = (4/3)πr³", "answer": volume},
        ]
        worked = [
            f"V = (4/3) × π × {r}³",
            f"V = (4/3) × π × {r**3}",
            f"V = {volume} {unit}³",
        ]

    return Question(
        question_text=question_text,
        correct_answer=volume,
        topic="Geometry and Measure",
        question_type="Volume of a Sphere",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=SPHERE_NOTES,
        metadata={
            "diagram": "sphere",
            "unit": unit,
            "diagram_params": {"r": r, "d": d, "use_diam": use_diam},
        },
    )


# ---------------------------------------------------------------------------
# Cone
# ---------------------------------------------------------------------------

def generate_cone_question():
    ctx = random.choice(_CONE_CONTEXTS)
    unit = ctx["unit"]
    h = random.choice(ctx["heights"])
    use_diam = _give_diameter()

    d = None
    if use_diam:
        d = random.choice(ctx["diams"])
        r = d / 2
    else:
        r = random.choice(ctx["diams"]) / 2

    volume = round((1 / 3) * math.pi * r ** 2 * h, 2)

    question_text = f"Calculate the volume of the {ctx['shape']}. Give your answer to 2 decimal places."

    if use_diam:
        scaffold_steps = [
            {"prompt": "Find the radius from the diameter", "answer": r},
            {"prompt": "Square the radius", "answer": r ** 2},
            {"prompt": "Calculate the volume using V = (1/3)πr²h", "answer": volume},
        ]
        worked = [
            f"r = {d} ÷ 2 = {r} {unit}",
            f"V = (1/3) × π × {r}² × {h}",
            f"V = (1/3) × π × {r**2} × {h}",
            f"V = {volume} {unit}³",
        ]
    else:
        scaffold_steps = [
            {"prompt": "Square the radius", "answer": r ** 2},
            {"prompt": "Calculate the volume using V = (1/3)πr²h", "answer": volume},
        ]
        worked = [
            f"V = (1/3) × π × {r}² × {h}",
            f"V = (1/3) × π × {r**2} × {h}",
            f"V = {volume} {unit}³",
        ]

    return Question(
        question_text=question_text,
        correct_answer=volume,
        topic="Geometry and Measure",
        question_type="Volume of a Cone",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=CONE_NOTES,
        metadata={
            "diagram": "cone",
            "unit": unit,
            "diagram_params": {"r": r, "h": h, "d": d, "use_diam": use_diam},
        },
    )


# ---------------------------------------------------------------------------
# Cylinder
# ---------------------------------------------------------------------------

def generate_cylinder_question():
    ctx = random.choice(_CYLINDER_CONTEXTS)
    unit = ctx["unit"]
    h = random.choice(ctx["heights"])
    use_diam = _give_diameter()

    d = None
    if use_diam:
        d = random.choice(ctx["diams"])
        r = d / 2
    else:
        r = random.choice(ctx["diams"]) / 2

    volume = round(math.pi * r ** 2 * h, 2)

    question_text = f"Calculate the volume of the {ctx['shape']}. Give your answer to 2 decimal places."

    if use_diam:
        scaffold_steps = [
            {"prompt": "Find the radius from the diameter", "answer": r},
            {"prompt": "Square the radius", "answer": r ** 2},
            {"prompt": "Calculate the volume using V = πr²h", "answer": volume},
        ]
        worked = [
            f"r = {d} ÷ 2 = {r} {unit}",
            f"V = π × {r}² × {h}",
            f"V = π × {r**2} × {h}",
            f"V = {volume} {unit}³",
        ]
    else:
        scaffold_steps = [
            {"prompt": "Square the radius", "answer": r ** 2},
            {"prompt": "Calculate the volume using V = πr²h", "answer": volume},
        ]
        worked = [
            f"V = π × {r}² × {h}",
            f"V = π × {r**2} × {h}",
            f"V = {volume} {unit}³",
        ]

    return Question(
        question_text=question_text,
        correct_answer=volume,
        topic="Geometry and Measure",
        question_type="Volume of a Cylinder",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=CYLINDER_NOTES,
        metadata={
            "diagram": "cylinder",
            "unit": unit,
            "diagram_params": {"r": r, "h": h, "d": d, "use_diam": use_diam},
        },
    )


_N4_CYLINDER_CONTEXTS = [
    {"shape": "cylindrical tin can",    "unit": "cm", "radii": [3, 4, 5, 6, 7],    "heights": [8, 10, 12, 15]},
    {"shape": "cylindrical water tank", "unit": "m",  "radii": [1, 2, 3],           "heights": [2, 3, 4, 5]},
    {"shape": "cylindrical glass",      "unit": "cm", "radii": [3, 4, 5],           "heights": [8, 9, 10, 12]},
]


def generate_volume_question_n4():
    ctx = random.choice(_N4_CYLINDER_CONTEXTS)
    unit = ctx["unit"]
    r = random.choice(ctx["radii"])
    h = random.choice(ctx["heights"])
    volume = round(math.pi * r ** 2 * h, 2)

    question_text = f"Calculate the volume of the {ctx['shape']}. Give your answer to 2 decimal places."

    scaffold_steps = [
        {"prompt": "Square the radius", "answer": float(r ** 2)},
        {"prompt": "Calculate the volume using V = πr²h", "answer": volume},
    ]

    worked = [
        f"V = π × {r}² × {h}",
        f"V = π × {r**2} × {h}",
        f"V = {volume} {unit}³",
    ]

    return Question(
        question_text=question_text,
        correct_answer=volume,
        topic="Geometry and Measure",
        question_type="Volume of a Cylinder",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=CYLINDER_NOTES,
        metadata={
            "diagram": "cylinder",
            "unit": unit,
            "diagram_params": {"r": r, "h": h, "d": None, "use_diam": False},
        },
    )


def generate_volume_question():
    return random.choice([
        generate_sphere_question,
        generate_cone_question,
        generate_cylinder_question,
    ])()
