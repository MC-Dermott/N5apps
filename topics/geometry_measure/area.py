"""N5 Geometry and Measure — Area (split from the old Perimeter and Area, Oct 2026).

Mirrors Area_Worksheet.docx (N5 Apps/Worksheets/Geometry and Measure): rectangles and triangles,
area of semi-circles and quarter circles, area of composite shapes, and "how many do I need?" (an
area, round UP, then cost). Every shape can also be asked the exam way — turf, paving or harling
priced per square metre, "calculate the cost" (2018 P2 Q11, 2025 P1 Q7) — through
`shape_costs.finish`, and the last level is all costed questions.

Distractors are the errors in the course reports and marking instructions: a triangle not halved
(2018, 2022), the perimeter found instead of the area (2018 P2 Q11 MI), the diameter used in πr²
(2023 CR, 2026 MI), the circle not halved (2025 CR), a cut-out added instead of subtracted (2026 P2
Q2 MI), the number of bags rounded down (2025 P1 Q7b MI).

Values are rounded to 2 d.p. at each step, as the worksheet's working does; π = 3.14 on the
non-calculator (Paper 1 style) questions.
"""
import math
import random

from core.models.distractors import distractors
from core.models.question_model import Question
from topics.geometry_measure.shape_costs import (TOPIC, r2, g, pi_for, diagram, not_whole, tail_for,
                                                 finish)

QTYPE = "Area"
COST_SHARE = 0.35          # how often a level 1–3 question is the costed (exam-style) version

NOTES_RECT = """
**Area of rectangles and triangles**

Rectangle: A = length × breadth. Triangle: A = ½ × base × height (the height is measured at right
angles to the base). Area is in square units (m², cm²).

**Example (from the worksheet):** The floor of a classroom is a rectangle 8 m by 6 m. Carpet costs
£14.50 per square metre.
- Area = 8 × 6 = 48 m²
- Cost = 48 × £14.50 = **£696.00**

⚠ Forgetting to halve for a triangle (2018 and 2022 marking instructions). If the price is per
square metre, use the AREA, not the perimeter.
"""

NOTES_CIRCLE_AREA = """
**Area of a circle**

A = πr² (use the **radius**). If you are given the diameter, halve it first: r = d ÷ 2. For a cost,
multiply the area by the price per square metre.

**Example (from the worksheet):** A circular table top has a diameter of 80 cm. Take π = 3.14.
- r = 80 ÷ 2 = 40 cm
- A = 3.14 × 40² = **5024 cm²**

⚠ Using the diameter in πr² was common in 2023 and 2026; πd is the circumference (a length), not the area.
"""

NOTES_AREA = """
**Area of a semi-circle or quarter circle**

A = πr² (use the **radius**). Halve it for a semi-circle; divide by 4 for a quarter circle. For a
cost, multiply the area by the price per square metre.

**Example (from the worksheet):** A play area is a semi-circle with diameter 16 m. Take π = 3.14.
- r = 16 ÷ 2 = 8 m
- A = 3.14 × 8² = 200.96 m²
- Semi-circle: 200.96 ÷ 2 = **100.48 m²**

⚠ Using the diameter in πr² was common in 2023 and 2026; in 2025 some didn't halve.
"""

NOTES_COMPOSITE = """
**Area of a composite shape**

Split it into rectangles, triangles and parts of circles. ADD the parts that make up the shape;
SUBTRACT anything cut out. Triangle = ½ × base × height. For a cost, multiply the area by the price
per square metre.

**Example (from the worksheet):** A playpark is a rectangle 15 m by 10 m with a semi-circle on the
10 m side. Take π = 3.14.
- Rectangle: 15 × 10 = 150 m²
- Semi-circle: r = 5, 3.14 × 5² ÷ 2 = 39.25 m²
- Total = 150 + 39.25 = **189.25 m²**

⚠ In 2026 many added the window to the door instead of subtracting it; in 2018 and 2022 the
triangle wasn't halved.
"""

NOTES_HOW_MANY = """
**How many do I need?**

Work out the area, divide by what one bag / box / tin covers, then **round UP** — you can't buy part
of a bag. Then multiply by the price.

**Example (from the worksheet):** A playpark has an area of 189.25 m² of bark; one bag covers 6 m²
and costs £7.50.
- 189.25 ÷ 6 = 31.54 → **32 bags**
- 32 × £7.50 = **£240.00**

⚠ 81 ÷ 5 = 16 bags (rounded down) was common in 2025.
"""


# ── Level 1: rectangles and triangles ─────────────────────────────────────────────────────────
def _spec_rect(cost):
    thing = random.choice(["lawn", "classroom floor", "stage", "vegetable plot", "car park"])
    L = random.choice([8, 9, 12, 15, 18, 20, 24]); w = random.choice([x for x in (5, 6, 7, 8, 9, 10, 12) if x < L])
    A = float(L * w)
    return dict(desc=f"A {thing} is a rectangle {L} m by {w} m, as shown.", instr="Calculate its area.", ans=A,
                u="m", kind="area", final=False, steps=[], lines=[f"Area = l × b = {L} × {w} = **{L * w} m²**"],
                wrong=[], alt=(float(2 * (L + w)), "that's the PERIMETER — area is length × breadth (2018 Paper 2 "
                                                   "Q11 marking instructions: perimeter found instead of area)."),
                diag=diagram("rect", L, w, [f"{L} m", f"{w} m"]))


def _spec_triangle(cost):
    thing = random.choice(["flower bed", "sail", "garden"])
    b = random.choice([6, 8, 10, 12]); h = random.choice([4, 4.5, 5, 6, 7])
    A = r2(0.5 * b * h)
    return dict(desc=f"A triangular {thing} has base {b} m and height {g(h)} m, as shown.",
                instr="Calculate its area.", ans=A, u="m", kind="area", final=False, steps=[],
                lines=[f"Area = ½ × base × height = 0.5 × {b} × {g(h)} = **{g(A)} m²**"],
                wrong=[(r2(b * h), "you didn't halve — the area of a triangle is ½ × base × height (2018 and "
                                   "2022 marking instructions).")],
                diag=diagram("triangle", b, h, [f"{b} m", f"{g(h)} m"]))


def _spec_square(cost):
    s = random.choice([4.5, 5, 6.5, 7.5, 8, 9.5, 12])
    A = r2(s * s)
    return dict(desc=f"A square {random.choice(['patio', 'paddock', 'courtyard'])} has sides of length {g(s)} m.",
                instr="Calculate its area.", ans=A, u="m", kind="area", final=False, steps=[],
                lines=[f"Area = {g(s)} × {g(s)} = **{g(A)} m²**"],
                wrong=[(r2(2 * s), "you doubled the side — area is side × side.")],
                alt=(r2(4 * s), "that's the PERIMETER — area is side × side."), diag={})


def generate_area_l1(calc_mode=False, cost=None):
    """Area of a rectangle, triangle or square (and the cost of covering it)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    spec = random.choice([_spec_rect, _spec_triangle, _spec_square])(cost)
    return finish(spec, cost, QTYPE, NOTES_RECT, "Area")


# ── Level 2: area of a semi-circle / quarter circle ───────────────────────────────────────────
_ARC_CONTEXTS = [("garden bed", "m"), ("badge", "cm"), ("stone arch", "m"), ("window", "m"),
                 ("table corner", "cm"), ("flower bed", "m")]


_CIRCLE_CONTEXTS = [("round trampoline", "m"), ("circular pond", "m"), ("circular paddling pool", "m"),
                    ("circular table top", "cm"), ("clock face", "cm")]
_CIRCLE_COST_CONTEXTS = [("circular pond", "m"), ("circular paddling pool", "m"), ("circular flower bed", "m"),
                         ("circular lawn", "m")]
_RADII = [2, 3, 4, 5, 6, 8, 10, 12, 14, 15, 20]


def _spec_circle_area(cost):
    """A whole circle. A costed question gives the RADIUS only (as on the worksheet)."""
    what, u = random.choice(_CIRCLE_COST_CONTEXTS if cost else _CIRCLE_CONTEXTS)
    non_calc = random.random() < 0.5
    pv, ps = pi_for(non_calc)
    radius_given = True if cost else random.random() < 0.5
    r = random.choice(_RADII); d = 2 * r
    A = r2(pv * r * r)
    given = f"a radius of {r} {u}" if radius_given else f"a diameter of {d} {u}"
    steps = ([] if radius_given else [{"prompt": "Radius (halve the diameter)", "answer": float(r)}])
    steps += [{"prompt": f"Area, {ps} × r²", "answer": A}]
    lines = ([f"r = {r} {u}"] if radius_given else [f"r = {d} ÷ 2 = {r} {u}"]) + [
        f"A = π × r² = {ps} × {r}² = **{g(A)} {u}²**"]
    diag = diagram("circle_r", r, f"{r} {u}") if radius_given else diagram("circle", d, f"{d} {u}")
    return dict(desc=f"A {what} has {given}.", instr="Calculate its area.", ans=A, u=u, kind="area", final=False,
                steps=steps, lines=lines, tail=tail_for(non_calc), diag=diag,
                wrong=[(r2(pv * d * d), "you used the diameter in πr² — halve it first (2023 course report; 2026 "
                                        "marking instructions)."),
                       (r2(pv * d), "πd is the circumference (a length), not the area (2023, 2025 course reports)."),
                       (r2(pv * 2 * r), "2r isn't r² — square the radius.")])


def _spec_sector(cost, frac):
    """A semi-circle (frac 2) or quarter circle (frac 4). A costed question gives the RADIUS only."""
    what, u = random.choice([c for c in _ARC_CONTEXTS if c[1] == "m"] if cost else _ARC_CONTEXTS)
    non_calc = random.random() < 0.5
    pv, ps = pi_for(non_calc)
    radius_given = True if cost else random.random() < 0.5
    r = random.choice(_RADII); d = 2 * r
    name = "semi-circle" if frac == 2 else "quarter circle"
    given = f"radius {r} {u}" if radius_given else f"diameter {d} {u}"
    A = r2(pv * r * r); ans = r2(A / frac)
    steps = ([] if radius_given else [{"prompt": "Radius (halve the diameter)", "answer": float(r)}])
    steps += [{"prompt": f"Area of the full circle, {ps} × r²", "answer": A}, {"prompt": f"Divide by {frac}", "answer": ans}]
    lines = ([f"r = {r} {u}"] if radius_given else [f"r = {d} ÷ 2 = {r} {u}"]) + [
        f"A = π × r² = {ps} × {r}² = {g(A)} {u}²", f"{name.capitalize()}: A = {g(A)} ÷ {frac} = **{g(ans)} {u}²**"]
    if frac == 2:
        diag = diagram("semi_r", r, f"{r} {u}") if radius_given else diagram("semi", d, f"{d} {u}")
    else:
        diag = diagram("quarter", r, f"{r} {u}")
    return dict(desc=f"A {what} is a {name} with {given}.", instr="Calculate its area.", ans=ans, u=u, kind="area",
                final=False, steps=steps, lines=lines, tail=tail_for(non_calc), diag=diag,
                wrong=[(r2(r2(pv * d * d) / frac), "you used the diameter in πr² — halve it first (2023 course "
                                                   "report; 2026 marking instructions)."),
                       (A, f"that's the whole circle — divide by {frac} for a {name} (2025 course report)."),
                       (r2(r2(pv * d) / frac), "πd is the circumference (a length), not the area (2023, 2025 "
                                               "course reports)."),
                       (r2(r2(pv * 2 * r) / frac), "2r isn't r² — square the radius.")])


def generate_area_circles(calc_mode=False, cost=None):
    """Area of a circle (and the cost of covering it)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    return finish(_spec_circle_area(cost), cost, QTYPE, NOTES_CIRCLE_AREA, "Area")


def generate_area_semicircles(calc_mode=False, cost=None):
    """Area of a semi-circle (and the cost of covering it)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    return finish(_spec_sector(cost, 2), cost, QTYPE, NOTES_AREA, "Area")


def generate_area_quarters(calc_mode=False, cost=None):
    """Area of a quarter circle (and the cost of covering it)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    return finish(_spec_sector(cost, 4), cost, QTYPE, NOTES_AREA, "Area")


def generate_area_l2(calc_mode=False, cost=None):
    """Kept for older references: a semi-circle or quarter circle."""
    return random.choice([generate_area_semicircles, generate_area_quarters])(calc_mode, cost)


# ── Level 3: area of a composite shape ────────────────────────────────────────────────────────
def _area_rect_semi(pv, ps):
    w = random.choice([6, 8, 10, 12, 14, 16, 20]); L = random.choice([10, 12, 15, 18, 20, 24, 30])
    R = L * w; S = r2(pv * (w / 2) ** 2 / 2); T = r2(R + S)
    lines = [f"Rectangle: {L} × {w} = {R} m²", f"Semi-circle: r = {g(w / 2)}, {ps} × {g(w / 2)}² ÷ 2 = {g(S)} m²",
             f"Total = {R} + {g(S)} = **{g(T)} m²**"]
    steps = [{"prompt": "Area of the rectangle", "answer": float(R)}, {"prompt": "Area of the semi-circle", "answer": S}]
    wrong = [(r2(R + r2(pv * (w / 2) ** 2)), "you didn't halve the circle — it's a semi-circle (2025 course "
                                            "report)."),
             (r2(R + r2(pv * w * w / 2)), "you used the diameter in πr² (2023 course report)."),
             (r2(R + r2(pv * w / 2)), "πd ÷ 2 is the curved edge's length, not the semi-circle's area (2025 "
                                      "marking instructions).")]
    return dict(desc="A playpark is a rectangle and a semi-circle, as shown.", instr="Calculate its area.", ans=T,
                lines=lines, steps=steps, wrong=wrong, diag=diagram("rect_semi", L, w, [f"{L} m", f"{w} m"]))


def _area_door(pv, ps):
    w = random.choice([0.76, 0.8, 0.85, 0.9]); h = random.choice([1.98, 2, 2.03, 2.1]); d = random.choice([0.4, 0.5, 0.54, 0.6])
    R = r2(w * h); S = r2(pv * (d / 2) ** 2 / 2); T = r2(R - S)
    lines = [f"Rectangle: {g(h)} × {g(w)} = {g(R)} m²", f"Window: r = {g(d / 2)}, {ps} × {g(d / 2)}² ÷ 2 = {g(S)} m²",
             f"Area to paint = {g(R)} − {g(S)} = **{g(T)} m²**"]
    steps = [{"prompt": "Area of the rectangle", "answer": R}, {"prompt": "Area of the semi-circular window", "answer": S}]
    wrong = [(r2(R + S), "you added the window — it isn't painted, so SUBTRACT it (2026 Paper 2 Q2 marking "
                         "instructions)."),
             (r2(R - r2(pv * d * d / 2)), "you used the diameter in πr² (2026 marking instructions: "
                                          "π × 0.54² ÷ 2)."),
             (r2(R - r2(pv * (d / 2) ** 2)), "the window is a SEMI-circle — halve the circle's area.")]
    return dict(desc="A front door is a rectangle with a semi-circular window, as shown.",
                instr="Calculate the area of the door to be painted (not the window).", ans=T, lines=lines,
                steps=steps, wrong=wrong, item=("paint", "Paint"),
                diag=diagram("door", w, h, d, [f"{g(w)} m", f"{g(h)} m", f"{g(d)} m"]))


def _area_house(pv, ps):
    w = random.choice([6, 8, 9, 10, 12]); h = random.choice([4, 4.5, 5, 6]); t = random.choice([2, 3, 4])
    R = r2(w * h); Tr = r2(0.5 * w * t); T = r2(R + Tr)
    lines = [f"Rectangle: {w} × {g(h)} = {g(R)} m²", f"Triangle: 0.5 × {w} × {t} = {g(Tr)} m²",
             f"Total = {g(R)} + {g(Tr)} = **{g(T)} m²**"]
    steps = [{"prompt": "Area of the rectangle", "answer": R}, {"prompt": "Area of the triangle", "answer": Tr}]
    wrong = [(r2(R + w * t), "you didn't halve for the triangle — ½ × base × height (2018 and 2022 marking "
                             "instructions).")]
    return dict(desc="The end wall of a house is a rectangle with an isosceles triangle on top, as shown.",
                instr="Calculate the area of the wall.", ans=T, lines=lines, steps=steps, wrong=wrong,
                item=("harling", "Harling"), no_tail=True,
                diag=diagram("house", w, h, t, [f"{w} m", f"{g(h)} m", f"{t} m"]))


def _area_patio(pv, ps):
    L = random.choice([10, 12, 14, 15]); w = random.choice([8, 9, 10]); r = random.choice([1.5, 2, 2.5, 3])
    R = L * w; C = r2(pv * r * r); T = r2(R - C)
    lines = [f"Rectangle: {L} × {w} = {R} m²", f"Pond: {ps} × {g(r)}² = {g(C)} m²", f"Patio = {R} − {g(C)} = **{g(T)} m²**"]
    steps = [{"prompt": "Area of the rectangle", "answer": float(R)}, {"prompt": "Area of the pond", "answer": C}]
    wrong = [(r2(R + C), "the pond is cut out of the patio — SUBTRACT it."),
             (r2(R - r2(pv * 2 * r)), "πd is the circumference, not the area (2024 course report)."),
             (r2(R - r2(pv * 4 * r * r)), "you used the diameter in πr².")]
    return dict(desc="A patio is a rectangle with a circular pond in the middle, as shown.",
                instr="Calculate the area of the patio (shaded).", ans=T, lines=lines, steps=steps, wrong=wrong,
                item=("paving", "Paving"), diag=diagram("patio", L, w, r, [f"{L} m", f"{w} m", f"{g(r)} m"]))


def _area_square_semis(pv, ps):
    s = random.choice([1, 1.2, 1.4, 1.5]); d = random.choice([x for x in (0.5, 0.6, 0.7, 0.8) if x < s])
    Q = r2(s * s); C = r2(2 * pv * (d / 2) ** 2); T = r2(Q + C)
    lines = [f"Square: {g(s)} × {g(s)} = {g(Q)} m²", f"Four semi-circles = two circles: 2 × {ps} × {g(d / 2)}² = {g(C)} m²",
             f"Total = {g(Q)} + {g(C)} = **{g(T)} m²**"]
    steps = [{"prompt": "Area of the square", "answer": Q}, {"prompt": "Area of the four semi-circles", "answer": C}]
    wrong = [(r2(Q + r2(pv * (d / 2) ** 2)), "there are FOUR semi-circles (2023 marking instructions: "
                                            "π × 0.35² + 1.44)."),
             (r2(Q + r2(4 * pv * (d / 2) ** 2)), "four SEMI-circles make two circles, not four (2023 marking "
                                                "instructions)."),
             (r2(Q + r2(2 * pv * d * d)), "you used the diameter in πr² (2023 course report).")]
    return dict(desc="A mirror is a square with an identical semi-circle on each side, as shown.",
                instr="Calculate its area.", ans=T, lines=lines, steps=steps, wrong=wrong,
                item=("glass", "Glass"), diag=diagram("square_semis", s, d, [f"{g(s)} m", f"{g(d)} m"]))


def _area_path(pv, ps):
    L = random.choice([8, 10, 12]); w = random.choice([5, 6, 8]); p = random.choice([1, 1.5])
    O = r2((L + 2 * p) * (w + 2 * p)); I = L * w; T = r2(O - I)
    lines = [f"Outside rectangle: ({L} + 2 × {g(p)}) × ({w} + 2 × {g(p)}) = {g(O)} m²", f"Lawn: {L} × {w} = {I} m²",
             f"Path = {g(O)} − {I} = **{g(T)} m²**"]
    steps = [{"prompt": "Area of the outside rectangle (lawn and path)", "answer": O},
             {"prompt": "Area of the lawn", "answer": float(I)}]
    wrong = [(r2((L + p) * (w + p) - I), "the path goes all the way round, so add the width on BOTH sides "
                                         "(2 × the path width)."),
             (r2(O + I), "the lawn isn't part of the path — SUBTRACT it.")]
    return dict(desc=f"A lawn {L} m by {w} m has a path {g(p)} m wide all the way round it, as shown.",
                instr="Calculate the area of the path (shaded).", ans=T, lines=lines, steps=steps, wrong=wrong,
                item=("gravel", "Gravel"), diag=diagram("path_round", L, w, p, [f"{L} m", f"{w} m", f"{g(p)} m"]))


def generate_area_l3(calc_mode=False, cost=None):
    """Area of a composite shape, add or subtract (and the cost of covering it)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    non_calc = random.random() < 0.3
    pv, ps = pi_for(non_calc)
    make = random.choice([_area_rect_semi, _area_door, _area_house, _area_patio, _area_square_semis, _area_path])
    spec = make(pv, ps)
    spec.update(kind="area", u="m")
    if not spec.pop("no_tail", False) and make is not _area_path:
        spec["tail"] = tail_for(non_calc)
    spec["wrong"] = [(v, m) for v, m in spec["wrong"] if v is not None and v > 0]      # no negative "areas"
    return finish(spec, cost, QTYPE, NOTES_COMPOSITE, "Total area")


# ── Level 4: how many do I need? ──────────────────────────────────────────────────────────────
def generate_area_l4(calc_mode=False):
    """An area → number of bags, boxes or tins (rounded UP) → cost."""
    kind = random.choice(["bark", "tiles", "paint", "lawn", "circle", "wall"])
    meta = {}
    if kind == "bark":
        A = round(random.uniform(40, 300), 2); per = random.choice([4, 5, 6, 8]); A = not_whole(A, per)
        price = random.choice([6.5, 7.5, 8, 9.25]); unit = "bags"
        text = (f"A playpark has an area of {g(A)} m². It is covered with bark. One bag covers {per} m² and costs "
                f"£{price:.2f}. Calculate the cost of the bark.")
        q = A / per; n = math.ceil(q - 1e-9); cost = r2(n * price)
        steps = [{"prompt": "Number of bags needed (round UP)", "answer": float(n)}, {"prompt": "Cost", "answer": cost}]
        worked = [f"{g(A)} ÷ {per} = {g(r2(q))} → {n} bags (round up)", f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
        wrong = [(r2(math.floor(q) * price), f"you rounded DOWN — {math.floor(q)} bags isn't enough (2025 Paper 1 "
                                              f"Q7 marking instructions: 81 ÷ 5 = 16 bags)."),
                 (r2(q * price), f"you can't buy part of a bag — round up to {n} first (2019 course report)."),
                 (r2(A * price), "divide by what one bag covers first (2025 marking instructions: 81 × 8).")]
    elif kind == "tiles":
        A = float(random.choice([18, 24, 30, 36, 42])); perm = random.choice([16, 20, 25])
        box = random.choice([b for b in (20, 30, 40) if b != perm])      # equal sizes would always divide exactly
        price = random.choice([14.5, 18.95, 22.5])
        tiles = A * perm
        while abs(tiles / box - round(tiles / box)) < 0.02:
            A += 1; tiles = A * perm
        q = tiles / box; n = math.ceil(q - 1e-9); cost = r2(n * price)
        text = (f"A path has an area of {g(A)} m². It is covered with tiles: {perm} tiles cover 1 m². Tiles are "
                f"sold in boxes of {box}, costing £{price:.2f} a box. Calculate the cost of the tiles.")
        steps = [{"prompt": "Number of tiles", "answer": float(tiles)}, {"prompt": "Number of boxes (round UP)", "answer": float(n)},
                 {"prompt": "Cost", "answer": cost}]
        worked = [f"Tiles = {g(A)} × {perm} = {g(tiles)} tiles", f"Boxes = {g(tiles)} ÷ {box} = {g(r2(q))} → {n} boxes (round up)",
                  f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
        wrong = [(r2(math.floor(q) * price), f"you rounded DOWN — {math.floor(q)} boxes isn't enough."),
                 (r2(q * price), f"you can't buy part of a box — round up to {n} first."),
                 (r2(math.ceil(A / box) * price), f"{perm} tiles cover 1 m² — find the number of tiles first.")]
    elif kind == "paint":
        A = round(random.uniform(2, 12), 2); per = random.choice([2.5, 4, 5]); A = not_whole(A, per)
        price = random.choice([12.99, 14.99, 18.5]); coats = random.choice([1, 2])
        X = r2(A * coats)
        q = X / per; n = math.ceil(q - 1e-9); cost = r2(n * price)
        cw = "needs 2 coats" if coats == 2 else "needs 1 coat"
        text = (f"A wall has {g(A)} m² to paint, and it {cw}. One tin of paint covers {g(per)} m² and costs "
                f"£{price:.2f}. Calculate the cost of the paint.")
        steps = ([{"prompt": "Total area to cover (all the coats)", "answer": X}] if coats == 2 else []) + [
            {"prompt": "Number of tins needed (round UP)", "answer": float(n)}, {"prompt": "Cost", "answer": cost}]
        worked = ([f"Area to cover = {g(A)} × 2 coats = {g(X)} m²"] if coats == 2 else []) + [
            f"{g(X)} ÷ {g(per)} = {g(r2(q))} → {n} tins (round up)", f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
        wrong = [(r2(math.floor(q) * price), f"you rounded DOWN — {math.floor(q)} tins isn't enough (2025 Paper 1 "
                                              f"Q7 marking instructions)."),
                 (r2(q * price), f"you can't buy part of a tin — round up to {n} first."),
                 (r2(math.ceil(A / per) * price), "the wall needs 2 coats — double the area first.") if coats == 2
                 else (r2(A * price), "divide by what one tin covers first.")]
    elif kind == "circle":
        r = random.choice([3, 4, 5, 6]); A = r2(math.pi * r * r)
        per = random.choice([3, 4, 5, 6, 7]); price = random.choice([6.75, 7.5, 9.25])
        while abs(A / per - round(A / per)) < 0.02:
            per += 1
        q = A / per; n = math.ceil(q - 1e-9); cost = r2(n * price)
        text = (f"A circular lawn has a radius of {r} m, as shown. It is covered with topsoil. One bag covers "
                f"{per} m² and costs £{price:.2f}. Calculate the cost of the topsoil.")
        steps = [{"prompt": "Area of the lawn (to 2 decimal places)", "answer": A},
                 {"prompt": "Number of bags needed (round UP)", "answer": float(n)}, {"prompt": "Cost", "answer": cost}]
        worked = [f"Area = π × r² = π × {r}² = {g(A)} m²", f"{g(A)} ÷ {per} = {g(r2(q))} → {n} bags (round up)",
                  f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
        wrong = [(r2(math.floor(q) * price), f"you rounded DOWN — {math.floor(q)} bags isn't enough."),
                 (r2(q * price), f"you can't buy part of a bag — round up to {n} first."),
                 (r2(math.ceil(r2(math.pi * 2 * r) / per) * price), "πd is the circumference (a length), not the area."),
                 (r2(math.ceil(r2(math.pi * 4 * r * r) / per) * price), "you used the diameter in πr² — halve it first.")]
        meta = diagram("circle_r", r, f"{r} m")
    elif kind == "wall":
        coats = 2; price = random.choice([14.99, 18.5, 21.5])
        while True:                                  # something to round up: resample until X ÷ per isn't whole
            L = random.choice([6, 7, 8, 9, 10]); H = random.choice([2.5, 3, 4.5, 6.5]); A = r2(L * H)
            per = random.choice([2.5, 4, 5, 9]); X = r2(A * coats)
            if abs(X / per - round(X / per)) >= 0.02:
                break
        q = X / per; n = math.ceil(q - 1e-9); cost = r2(n * price)
        text = (f"A wall is a rectangle {g(L)} m long and {g(H)} m high, as shown. It is painted with 2 coats. One tin "
                f"of paint covers {g(per)} m² and costs £{price:.2f}. Calculate the cost of the paint.")
        steps = [{"prompt": "Area of the wall", "answer": A}, {"prompt": "Total area to cover (2 coats)", "answer": X},
                 {"prompt": "Number of tins needed (round UP)", "answer": float(n)}, {"prompt": "Cost", "answer": cost}]
        worked = [f"Area = {g(L)} × {g(H)} = {g(A)} m²", f"Area to cover = {g(A)} × 2 coats = {g(X)} m²",
                  f"{g(X)} ÷ {g(per)} = {g(r2(q))} → {n} tins (round up)", f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
        wrong = [(r2(math.floor(q) * price), f"you rounded DOWN — {math.floor(q)} tins isn't enough."),
                 (r2(q * price), f"you can't buy part of a tin — round up to {n} first."),
                 (r2(math.ceil(A / per) * price), "the wall needs 2 coats — double the area first."),
                 (r2(math.ceil(2 * (L + H) * 2 / per) * price), "you used the PERIMETER — paint covers an area.")]
        meta = diagram("rect", L, H, [f"{g(L)} m", f"{g(H)} m"])
    else:
        L = random.choice([10, 12, 15, 18]); w = random.choice([6, 8, 9, 10]); A = float(L * w)
        per = random.choice([x for x in (3, 3.5, 4, 7) if w % x != 0]); price = random.choice([6.75, 7.5, 9.25])   # w % per == 0 would always divide exactly
        while abs(A / per - round(A / per)) < 0.02:
            L += 1; A = float(L * w)
        q = A / per; n = math.ceil(q - 1e-9); cost = r2(n * price)
        text = (f"A lawn is a rectangle {L} m by {w} m, as shown. It is covered with topsoil. One bag covers "
                f"{g(per)} m² and costs £{price:.2f}. Calculate the cost of the topsoil.")
        steps = [{"prompt": "Area of the lawn", "answer": A}, {"prompt": "Number of bags needed (round UP)", "answer": float(n)},
                 {"prompt": "Cost", "answer": cost}]
        worked = [f"Area = {L} × {w} = {g(A)} m²", f"{g(A)} ÷ {g(per)} = {g(r2(q))} → {n} bags (round up)",
                  f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
        wrong = [(r2(math.floor(q) * price), f"you rounded DOWN — {math.floor(q)} bags isn't enough."),
                 (r2(q * price), f"you can't buy part of a bag — round up to {n} first."),
                 (r2(math.ceil(2 * (L + w) / per) * price), "you used the PERIMETER — topsoil covers an area "
                                                             "(2018 Paper 2 Q11 marking instructions).")]
        meta = diagram("rect", L, w, [f"{L} m", f"{w} m"])
    return Question(question_text=text, correct_answer=cost, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                    worked_solution=worked, notes=NOTES_HOW_MANY, metadata=meta,
                    distractors=distractors(cost, wrong))


# ── Level 5: exam style — the cost of an area ─────────────────────────────────────────────────
def generate_area_costs(calc_mode=False):
    """Any area question, asked the exam way: priced per square metre, calculate the cost."""
    return random.choice([generate_area_l1, generate_area_circles, generate_area_semicircles, generate_area_quarters,
                          generate_area_l3])(calc_mode=calc_mode, cost=True)


def generate_area_question(calc_mode=False):
    return random.choice([generate_area_l1, generate_area_circles, generate_area_semicircles, generate_area_quarters,
                          generate_area_l3, generate_area_l4, generate_area_costs])(calc_mode=calc_mode)
