import random
import math
from core.models.distractors import distractors
from core.models.question_model import Question

SPHERE_NOTES = """
**Volume of a Sphere:**

**V = (4/3) × π × r³**

- **r** is the radius
- If you are given the diameter: r = diameter ÷ 2

Give your answer to 2 decimal places.

**Example:** A sphere has radius 6 cm.
- V = (4/3) × π × 6³ = (4/3) × π × 216 ≈ **904.78 cm³**

**Worksheet example:** A bowl is a hemisphere with diameter 16 cm.
- r = 16 ÷ 2 = 8 cm;  V = (4 ÷ 3) × π × 8³ = 2144.66 cm³;  hemisphere = 2144.66 ÷ 2 = **1072.33 cm³**

⚠ Use the radius, CUBE it, and use 4/3 (not 3/4) — all common in 2024 (marking instructions). A
hemisphere is half a sphere (2023). Give units (2023–2025 course reports).
"""

CONE_NOTES = """
**Volume of a Cone:**

**V = (1/3) × π × r² × h**

- **r** is the radius of the circular base
- **h** is the perpendicular height
- If you are given the diameter: r = diameter ÷ 2

Give your answer to 2 decimal places.

**Example:** A cone has radius 4 cm and height 9 cm.
- V = (1/3) × π × 4² × 9 = (1/3) × π × 144 ≈ **150.80 cm³**

**Worksheet example:** An ice-cream cone has diameter 8 cm and height 12 cm.
- r = 4;  V = (1 ÷ 3) × π × 4² × 12 = **201.06 cm³**

⚠ Use the radius, and don't forget the ⅓.
"""

CYLINDER_NOTES = """
**Volume of a Cylinder:**

**V = π × r² × h**

- **r** is the radius of the circular end
- **h** is the height (or length)
- If you are given the diameter: r = diameter ÷ 2

Give your answer to 2 decimal places.

**Example:** A cylinder has radius 5 cm and height 10 cm.
- V = π × 5² × 10 = π × 250 ≈ **785.40 cm³**

**Worksheet example:** A shortbread tin has diameter 20 cm and height 8 cm.
- r = 10;  V = π × 10² × 8 = 2513.27 cm³ = **2.51 litres** (÷ 1000)

⚠ π × 3.8² × 9.7 — the diameter instead of the radius — was common in 2018 (marking instructions).
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
        r = random.choice(ctx["diams"]) / 2  # pick from same pool, halve (/ not //: a 1 m buoy has r = 0.5)

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
        distractors=distractors(volume, [
            (round(4 / 3 * math.pi * (2 * r) ** 3, 2), "you used the diameter — halve it first (2024 marking instructions)."),
            (round(4 / 3 * math.pi * r ** 2, 2), "you squared the radius — the sphere formula CUBES it (2024 marking instructions)."),
            (round(3 / 4 * math.pi * r ** 3, 2), "it's 4/3, not 3/4 (2024 marking instructions)."),
            (round(4 / 3 * math.pi * r ** 3 / 2, 2), "that's a hemisphere — this is a whole sphere."),
        ]),
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
        distractors=distractors(volume, [
            (round(math.pi * (2 * r) ** 2 * h / 3, 2), "you used the diameter — halve it first."),
            (round(math.pi * r ** 2 * h, 2), "you forgot the ⅓ — that's the volume of a cylinder."),
            (round(math.pi * r * h / 3, 2), "square the radius."),
        ]),
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
        distractors=distractors(volume, [
            (round(math.pi * (2 * r) ** 2 * h, 2), "you used the diameter — halve it first (2018 marking "
                                                   "instructions: π × 3.8² × 9.7)."),
            (round(math.pi * r * h, 2), "square the radius (2018 marking instructions: π × 1.9 × 9.7)."),
            (round(math.pi * 2 * r * h, 2), "πd × h isn't a volume — use πr²h (2018 marking instructions)."),
        ]),
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


# ---------------------------------------------------------------------------
# Prisms, composite solids and litres — mirror Volume_Worksheet.docx Sections 1, 4 and 5
# (N5 Apps/Worksheets/Geometry and Measure). Distractors are the course-report errors: the ½ missed
# for a triangle, cm³ not converted, m³ ÷ 1000, a hemisphere taken as a whole sphere, a part added
# instead of subtracted, the gap at the top of a container ignored, bottles rounded down.
# ---------------------------------------------------------------------------

def _r2(x):
    return round(x + 1e-9, 2)


def _g(x):
    x = float(x)
    return str(int(x)) if x == int(x) else f"{x:.6f}".rstrip("0").rstrip(".")


def _solid(kind, *args):
    return {"diagram": "composite_shape", "diagram_params": {"module": "solids", "kind": kind, "args": list(args)}}


PRISM_NOTES = """
**Volume of a prism:** V = area of the cross-section × length (V = Ah, on the formulae list).
A cuboid's cross-section is a rectangle; a triangular prism's is a triangle (½ × base × height).

**Litres:** 1 litre = 1000 cm³ (so cm³ ÷ 1000), and 1 m³ = 1000 litres (so m³ × 1000).

**Worksheet example:** A chocolate box is a triangular prism: triangle base 12 cm, height 9 cm,
length 40 cm.
- A = 0.5 × 12 × 9 = 54 cm²;  V = 54 × 40 = 2160 cm³;  2160 ÷ 1000 = **2.16 litres**

⚠ In 2024 most candidates didn't find the prism or cuboid volume and didn't convert to litres; in
2018 many divided m³ by 1000 instead of multiplying (course reports).
"""

COMPOSITE_NOTES = """
**Composite solids:** split into shapes you know. ADD the parts that make it up; SUBTRACT anything
taken out or left empty. Give units.

**Worksheet example:** A bottle is a cuboid 12 × 5 × 9 cm with a cylinder (diameter 4 cm, height 5 cm)
on top.
- Cuboid = 540 cm³;  cylinder = π × 2² × 5 = 62.83 cm³;  total = **602.83 cm³**

⚠ 2023: many couldn't find the cube, or used a whole sphere for a hemisphere. 2025: empty space =
box − balls. 2022: the 2 cm gap at the top of the tank.
"""

LITRES_NOTES = """
**Litres and filling:** convert to litres, then work out how many. Round UP when you need enough
(bottles, bags); round DOWN for how many FULL ones you get.

**Worksheet example:** 26 cups each hold 346.36 cm³. Juice comes in 1.5 litre bottles.
- 26 × 346.36 = 9005.36 cm³ = 9.01 litres;  9.01 ÷ 1.5 = 6.01 → **7 bottles**

⚠ m³ × 1000 = litres, not ÷ (2018 course report). Round the bottles up (2021 marking instructions).
"""


def generate_volume_prism(calc_mode=False):
    """Cuboid or triangular prism, often in litres."""
    tri = random.random() < 0.55
    if tri:
        what, u = random.choice([("chocolate box", "cm"), ("tent", "m"), ("gift box", "cm"), ("feeding trough", "cm")])
        if u == "m":
            b, h, L = random.choice([1.6, 1.8, 2, 2.4]), random.choice([1.2, 1.5, 1.8]), random.choice([2, 2.5, 3])
        else:
            b, h, L = random.choice([4, 6, 8, 10, 12, 20]), random.choice([3, 4, 5, 9, 15]), random.choice([20, 25, 30, 40, 50])
        A = _r2(0.5 * b * h); text = f"A {what} is a triangular prism, as shown. Calculate its volume"
        diag = _solid("tri_prism", b, h, L, [f"{_g(b)} {u}", f"{_g(h)} {u}", f"{_g(L)} {u}"])
        a_line = f"A = ½ × base × height = 0.5 × {_g(b)} × {_g(h)} = {_g(A)} {u}²"
        no_half = b * h * L
    else:
        what, u = random.choice([("fish tank", "cm"), ("milk carton", "cm"), ("swimming pool", "m"), ("storage box", "cm")])
        if u == "m":
            b, h, L = random.choice([20, 25, 30]), random.choice([1.2, 1.5, 2]), random.choice([8, 10, 12])
        else:
            b, h, L = random.choice([20, 30, 40, 50, 60]), random.choice([20, 25, 30, 40]), random.choice([15, 20, 25, 30])
        A = _r2(b * h); text = f"A {what} is a cuboid {_g(b)} {u} long, {_g(L)} {u} wide and {_g(h)} {u} high. Calculate its volume"
        diag = _solid("cuboid", b, L, h, [f"{_g(b)} {u}", f"{_g(L)} {u}", f"{_g(h)} {u}"])
        a_line = f"A = {_g(b)} × {_g(h)} = {_g(A)} {u}²"
        no_half = None
    V = _r2(A * L)
    litres = random.random() < 0.7
    if litres:
        ans = _r2(V * 1000) if u == "m" else _r2(V / 1000)
        conv = f"{_g(V)} × 1000 = **{_g(ans)} litres**" if u == "m" else f"{_g(V)} ÷ 1000 = **{_g(ans)} litres**"
        text += " in litres."
        wrong = [(V, "you didn't convert to litres (2024 course report)."),
                 (_r2(V / 1000) if u == "m" else _r2(V * 1000),
                  "wrong way round: cm³ ÷ 1000 = litres, but m³ × 1000 = litres (2018 course report).")]
        if no_half:
            wrong.append((_r2(no_half * 1000) if u == "m" else _r2(no_half / 1000),
                          "you forgot the ½ for the triangle (2024 course report)."))
        steps = [{"prompt": "Area of the cross-section", "answer": A}, {"prompt": f"Volume in {u}³", "answer": V},
                 {"prompt": "Volume in litres", "answer": ans}]
        worked = [a_line, f"V = A × length = {_g(A)} × {_g(L)} = {_g(V)} {u}³", conv]
    else:
        ans = V
        text += f". Give units."
        wrong = [(no_half, "you forgot the ½ for the triangle (2024 course report).")] if no_half else []
        steps = [{"prompt": "Area of the cross-section", "answer": A}, {"prompt": "Volume", "answer": V}]
        worked = [a_line, f"V = A × length = {_g(A)} × {_g(L)} = **{_g(V)} {u}³**"]
    return Question(question_text=text, correct_answer=ans, topic="Geometry and Measure",
                    question_type="Volume of a Prism", scaffold_steps=steps, worked_solution=worked,
                    notes=PRISM_NOTES, metadata=diag, distractors=distractors(ans, wrong))


def generate_volume_composite(calc_mode=False):
    """Composite solids: add parts, or subtract what's empty."""
    kind = random.choice(["bottle", "cube_hemi", "house", "box_balls", "silo", "tank_gap"])
    pi = math.pi
    if kind == "bottle":
        l, b, h = random.choice([8, 10, 12]), random.choice([4, 5, 6]), random.choice([8, 9, 10, 12])
        d, hc = random.choice([2, 3, 4]), random.choice([3, 4, 5])
        C = l * b * h; Y = _r2(pi * (d / 2) ** 2 * hc); ans = _r2(C + Y)
        text = "A bottle is made from a cuboid and a cylinder, as shown. Calculate the volume of the bottle, to 2 decimal places."
        diag = _solid("cuboid_cylinder", l, b, h, d, hc, [f"{l} cm", f"{b} cm", f"{h} cm", f"{d} cm", f"{hc} cm"])
        steps = [{"prompt": "Volume of the cuboid", "answer": float(C)}, {"prompt": "Volume of the cylinder", "answer": Y}]
        worked = [f"Cuboid = {l} × {b} × {h} = {C} cm³", f"Cylinder = π × {_g(d / 2)}² × {hc} = {_g(Y)} cm³",
                  f"Total = {C} + {_g(Y)} = **{_g(ans)} cm³**"]
        wrong = [(_r2(C + pi * d * d * hc), "you used the diameter in the cylinder formula (2019 marking instructions).")]
    elif kind == "cube_hemi":
        s_ = random.choice([4, 6, 8, 10])
        C = s_ ** 3; H = _r2(4 / 3 * pi * (s_ / 2) ** 3 / 2); ans = _r2(C + H)
        text = (f"An ornament is a cube of side {s_} cm with a hemisphere on top, as shown. The hemisphere's diameter "
                f"is {s_} cm. Calculate the volume of the ornament, to 2 decimal places.")
        diag = _solid("cube_hemisphere", s_, [f"{s_} cm"])
        steps = [{"prompt": "Volume of the cube", "answer": float(C)}, {"prompt": "Volume of the hemisphere", "answer": H}]
        worked = [f"Cube = {s_} × {s_} × {s_} = {C} cm³", f"Hemisphere = (4 ÷ 3) × π × {_g(s_ / 2)}³ ÷ 2 = {_g(H)} cm³",
                  f"Total = {C} + {_g(H)} = **{_g(ans)} cm³**"]
        wrong = [(_r2(C + 2 * H), "you used a whole sphere — it's a HEMISPHERE (2023 marking instructions)."),
                 (_r2(C + 4 / 3 * pi * s_ ** 3 / 2), "you used the diameter in the sphere formula (2023 marking instructions)."),
                 (_r2(s_ * s_ + H), "a cube's volume is side × side × side (2023 course report).")]
    elif kind == "house":
        b, h, t, L = random.choice([10, 20, 30]), random.choice([10, 15, 20]), random.choice([10, 15]), random.choice([40, 50, 60])
        R = b * h; T = 0.5 * b * t; V = (R + T) * L; ans = _r2(V / 1000)
        text = "A container is a cuboid with a triangular prism on top, as shown. Calculate its volume in litres."
        diag = _solid("house_prism", b, h, t, L, [f"{b} cm", f"{h} cm", f"{t} cm", f"{L} cm"])
        steps = [{"prompt": "Area of the cross-section (rectangle + triangle)", "answer": float(R + T)},
                 {"prompt": "Volume in cm³", "answer": float(V)}, {"prompt": "Volume in litres", "answer": ans}]
        worked = [f"Cross-section = {b} × {h} + 0.5 × {b} × {t} = {_g(R + T)} cm²", f"V = {_g(R + T)} × {L} = {_g(V)} cm³",
                  f"{_g(V)} ÷ 1000 = **{_g(ans)} litres**"]
        wrong = [(V, "you didn't convert to litres (2024 course report)."),
                 (_r2((R + 2 * T) * L / 1000), "you forgot the ½ for the triangle."),
                 (_r2(R * L / 1000), "you left out the triangular prism (2024 course report).")]
    elif kind == "box_balls":
        dball = random.choice([4, 5, 6]); n = 2; side = dball + 0.2; long = 2 * dball + 0.4
        B = _r2(long * side * side); S = _r2(n * 4 / 3 * pi * (dball / 2) ** 3); ans = _r2(B - S)
        text = (f"A box is a cuboid {_g(long)} cm by {_g(side)} cm by {_g(side)} cm. It holds two balls, each a sphere "
                f"with diameter {dball} cm. Calculate the volume of empty space in the box, to 2 decimal places.")
        diag = _solid("cuboid", long, side, side, [f"{_g(long)} cm", f"{_g(side)} cm", f"{_g(side)} cm"])
        steps = [{"prompt": "Volume of the box", "answer": B}, {"prompt": "Volume of the two balls", "answer": S}]
        worked = [f"Box = {_g(long)} × {_g(side)} × {_g(side)} = {_g(B)} cm³",
                  f"Balls = 2 × (4 ÷ 3) × π × {_g(dball / 2)}³ = {_g(S)} cm³", f"Empty space = {_g(B)} − {_g(S)} = **{_g(ans)} cm³**"]
        wrong = [(_r2(B - S / 2), "there are TWO balls (2025 marking instructions)."),
                 (_r2(B + S), "the empty space is the box MINUS the balls (2025 marking instructions).")]
    elif kind == "silo":
        d, h = random.choice([3, 4, 5, 6]), random.choice([6, 8, 10, 12])
        r = d / 2; C = _r2(pi * r * r * h); H = _r2(4 / 3 * pi * r ** 3 / 2); ans = _r2(C + H)
        text = f"A grain silo is a cylinder with a hemisphere on top, as shown. Calculate its volume, to 2 decimal places."
        diag = _solid("cylinder_hemisphere", d, h, [f"{d} m", f"{h} m"])
        steps = [{"prompt": "Volume of the cylinder", "answer": C}, {"prompt": "Volume of the hemisphere", "answer": H}]
        worked = [f"Cylinder = π × {_g(r)}² × {h} = {_g(C)} m³", f"Hemisphere = (4 ÷ 3) × π × {_g(r)}³ ÷ 2 = {_g(H)} m³",
                  f"Total = {_g(C)} + {_g(H)} = **{_g(ans)} m³**"]
        wrong = [(_r2(C + 2 * H), "you used a whole sphere — it's a HEMISPHERE (2023 marking instructions).")]
    else:
        l, b, H, gap = random.choice([40, 50, 60]), random.choice([25, 30, 35]), random.choice([30, 35, 40, 45]), random.choice([2, 3, 5])
        V = l * b * (H - gap); ans = _r2(V / 1000)
        text = (f"A fish tank is a cuboid {l} cm long, {b} cm wide and {H} cm high. It is filled with water to {gap} cm "
                f"from the top. Calculate the volume of water in litres.")
        diag = _solid("cuboid", l, b, H, [f"{l} cm", f"{b} cm", f"{H} cm"])
        steps = [{"prompt": "Depth of the water", "answer": float(H - gap)}, {"prompt": "Volume of water in cm³", "answer": float(V)},
                 {"prompt": "Volume in litres", "answer": ans}]
        worked = [f"Depth = {H} − {gap} = {H - gap} cm", f"V = {l} × {b} × {H - gap} = {V} cm³", f"{V} ÷ 1000 = **{_g(ans)} litres**"]
        wrong = [(_r2(l * b * H / 1000), f"the water is {gap} cm below the top — use a depth of {H - gap} cm (2022 course report)."),
                 (float(V), "you didn't convert to litres.")]
    steps = steps + [{"prompt": "Answer", "answer": ans}]
    return Question(question_text=text, correct_answer=ans, topic="Geometry and Measure",
                    question_type="Composite Volume", scaffold_steps=steps, worked_solution=worked,
                    notes=COMPOSITE_NOTES, metadata=diag, distractors=distractors(ans, wrong))


def generate_volume_litres(calc_mode=False):
    """Converting to litres; how many bottles / bags (round up) or full cans (round down)."""
    kind = random.choice(["pool", "bark", "bottles", "cans"])
    if kind == "pool":
        l, b, h = random.choice([20, 25, 30]), random.choice([8, 10, 12]), random.choice([1.2, 1.5, 2])
        V = _r2(l * b * h); ans = _r2(V * 1000)
        text = f"A swimming pool is a cuboid {l} m long, {b} m wide and {_g(h)} m deep. How many litres of water does it hold?"
        steps = [{"prompt": "Volume in m³", "answer": V}, {"prompt": "Litres (1 m³ = 1000 litres)", "answer": ans}]
        worked = [f"V = {l} × {b} × {_g(h)} = {_g(V)} m³", f"{_g(V)} × 1000 = **{_g(ans)} litres**"]
        wrong = [(_r2(V / 1000), "m³ to litres is × 1000, not ÷ 1000 (2018 course report)."), (V, "convert m³ to litres.")]
    elif kind == "bark":
        A, mm, bag = random.choice([30, 40, 45, 60]), random.choice([50, 60, 75]), random.choice([50, 70, 90])
        L = _r2(A * mm / 1000 * 1000); q = L / bag; ans = float(math.ceil(q - 1e-9))
        if ans == q:
            bag = 70 if bag != 70 else 90; q = L / bag; ans = float(math.ceil(q - 1e-9))
        text = f"Bark is spread {mm} mm deep over {A} m² of a garden. Bark is sold in {bag} litre bags. How many bags are needed?"
        steps = [{"prompt": "Depth in metres", "answer": mm / 1000}, {"prompt": "Volume in litres", "answer": L},
                 {"prompt": "Number of bags (round up)", "answer": ans}]
        worked = [f"Depth = {mm} ÷ 1000 = {_g(mm / 1000)} m", f"V = {A} × {_g(mm / 1000)} = {_g(L / 1000)} m³ = {_g(L)} litres",
                  f"{_g(L)} ÷ {bag} = {_g(_r2(q))} → **{int(ans)} bags**"]
        wrong = [(float(math.floor(q)), "round UP — you need enough bark to cover the garden."),
                 (_r2(q), "you can't buy part of a bag — round up.")]
    elif kind == "bottles":
        d, H, gap, n, bottle = random.choice([6, 7, 8]), random.choice([10, 11, 12]), random.choice([1, 2]), random.choice([20, 24, 26, 30]), random.choice([1.5, 1.75, 2])
        cup = _r2(math.pi * (d / 2) ** 2 * (H - gap)); T = _r2(n * cup); L = _r2(T / 1000); q = L / bottle
        ans = float(math.ceil(q - 1e-9))
        text = (f"Cups are cylinders with diameter {d} cm and height {H} cm. Each is filled with juice to {gap} cm from the top. "
                f"{n} cups are filled. Juice is sold in {_g(bottle)} litre bottles. How many bottles are needed?")
        steps = [{"prompt": "Volume of juice in one cup (cm³)", "answer": cup}, {"prompt": "Total juice in litres", "answer": L},
                 {"prompt": "Number of bottles (round up)", "answer": ans}]
        worked = [f"One cup = π × {_g(d / 2)}² × {H - gap} = {_g(cup)} cm³", f"{n} × {_g(cup)} = {_g(T)} cm³ = {_g(L)} litres",
                  f"{_g(L)} ÷ {_g(bottle)} = {_g(_r2(q))} → **{int(ans)} bottles**"]
        full = _r2(n * math.pi * (d / 2) ** 2 * H / 1000)
        wrong = [(float(math.floor(q)), "round UP — you need enough juice for every cup (2021 marking instructions)."),
                 (float(math.ceil(full / bottle - 1e-9)), f"the cups are only filled to {gap} cm from the top (2021 Paper 2 Q7).")]
    else:
        L, can = round(random.uniform(120, 400), 2), random.choice([5, 8, 9, 10])
        q = L / can; ans = float(math.floor(q + 1e-9))
        if ans == q:
            L = round(L + 0.37, 2); q = L / can; ans = float(math.floor(q))
        text = f"A water butt holds {_g(L)} litres. A watering can holds {can} litres. How many FULL watering cans can be filled?"
        steps = [{"prompt": "Number of full cans (round down)", "answer": ans}]
        worked = [f"{_g(L)} ÷ {can} = {_g(_r2(q))} → **{int(ans)} full cans** (round down: the last one isn't full)"]
        wrong = [(float(math.ceil(q)), "round DOWN — the last can wouldn't be full.")]
    return Question(question_text=text, correct_answer=ans, topic="Geometry and Measure",
                    question_type="Litres and Filling", scaffold_steps=steps, worked_solution=worked,
                    notes=LITRES_NOTES, distractors=distractors(ans, wrong))


def generate_volume_question(calc_mode=False):
    return random.choice([
        generate_volume_prism,
        generate_sphere_question,
        generate_cone_question,
        generate_cylinder_question,
        generate_volume_composite,
        generate_volume_litres,
    ])()
