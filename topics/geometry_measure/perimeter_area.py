"""N5 Geometry and Measure — Perimeter and Area (composite shapes, including parts of circles).

Mirrors Perimeter_and_Area_Worksheet.docx (N5 Apps/Worksheets/Geometry and Measure): arc length of
semi-circles and quarter circles, perimeter of composite shapes, area of semi-circles and quarter
circles, area of composite shapes, and "how many do I need?" (round UP, then cost). Each question
draws its shape with core/ui/composite_shapes.py, the same drawings the worksheet uses.

Distractors are the errors in the course reports and marking instructions: πr² used for a length,
the radius used in πd, the circumference not halved / quartered, the diameter used in πr², the
straight top edge missed (2023 P2 Q2), a cut-out added instead of subtracted (2026 P2 Q2), a
triangle not halved (2018, 2022), and the number of bags rounded down (2025 P1 Q7b).

Values are rounded to 2 d.p. at each step, as the worksheet's working does; π = 3.14 on the
non-calculator (Paper 1 style) questions.
"""
import math
import random

from core.models.distractors import distractors
from core.models.question_model import Question

TOPIC, QTYPE = "Geometry and Measure", "Perimeter and Area"


def _r(x):
    return round(x + 1e-9, 2)


def _g(x):
    x = float(x)
    return str(int(x)) if x == int(x) else f"{x:.6f}".rstrip("0").rstrip(".")


def _pi(non_calc):
    return (3.14, "3.14") if non_calc else (math.pi, "π")


def _diagram(kind, *args):
    return {"diagram": "composite_shape", "diagram_params": {"kind": kind, "args": list(args)}}


NOTES_ARC = """
**Arc length of a semi-circle or quarter circle**

C = πd (use the **diameter**). A semi-circle's curved edge is C ÷ 2; a quarter circle's is C ÷ 4.

**Example (from the worksheet):** A garden bed is a semi-circle with diameter 20 cm. Take π = 3.14.
- C = 3.14 × 20 = 62.8 cm
- Arc = 62.8 ÷ 2 = **31.4 cm**

⚠ πr² is an AREA, not a length, and if you're given the radius, double it first (course reports
2023, 2024, 2026).
"""

NOTES_PERIMETER = """
**Perimeter of a composite shape** — the distance around the OUTSIDE

Add the curved edges to the straight edges. Dashed lines inside the shape don't count.

**Example (from the worksheet):** A badge is a rectangle 8 cm by 6 cm with a semi-circle on the 6 cm
side. Take π = 3.14.
- Semi-circle: 3.14 × 6 ÷ 2 = 9.42 cm
- Straight edges: 8 + 6 + 8 = 22 cm
- Perimeter = 9.42 + 22 = **31.42 cm**

⚠ Find any missing straight edge by subtracting the radii (2023 course report), and don't
calculate an area by mistake (2019, 2025).
"""

NOTES_AREA = """
**Area of a semi-circle or quarter circle**

A = πr² (use the **radius**). Halve it for a semi-circle; divide by 4 for a quarter circle.

**Example (from the worksheet):** A play area is a semi-circle with diameter 16 m. Take π = 3.14.
- r = 16 ÷ 2 = 8 m
- A = 3.14 × 8² = 200.96 m²
- Semi-circle: 200.96 ÷ 2 = **100.48 m²**

⚠ Using the diameter in πr² was common in 2023 and 2026; in 2025 some didn't halve.
"""

NOTES_COMPOSITE = """
**Area of a composite shape**

Split it into rectangles, triangles and parts of circles. ADD the parts that make up the shape;
SUBTRACT anything cut out. Triangle = ½ × base × height.

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

Work out the area or length, divide by what one bag / box / panel covers, then **round UP** — you
can't buy part of a bag. Then multiply by the price.

**Example (from the worksheet):** 189.25 m² of bark; one bag covers 6 m² and costs £7.50.
- 189.25 ÷ 6 = 31.54 → **32 bags**
- 32 × £7.50 = **£240.00**

⚠ 81 ÷ 5 = 16 bags (rounded down) was common in 2025.
"""


# ── Level 1: arc length ───────────────────────────────────────────────────────────────────────
_ARC_CONTEXTS = [("garden bed", "m"), ("badge", "cm"), ("stone arch", "m"), ("window", "m"),
                 ("table corner", "cm"), ("flower bed", "m")]


def generate_perimeter_area_l1(calc_mode=False):
    """Arc length of a semi-circle or quarter circle."""
    what, u = random.choice(_ARC_CONTEXTS)
    frac = random.choice([2, 4])
    non_calc = random.random() < 0.6
    pv, ps = _pi(non_calc)
    radius_given = random.random() < 0.5
    r = random.choice([3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30])
    d = 2 * r
    name = "semi-circle" if frac == 2 else "quarter circle"
    given = f"radius {r} {u}" if radius_given else f"diameter {d} {u}"
    tail = "Take π = 3.14." if non_calc else "Give your answer to 2 decimal places."
    text = f"A {what} is a {name} with {given}. Calculate the length of its curved edge. {tail}"
    C = _r(pv * d); arc = _r(C / frac)
    steps = ([{"prompt": "Diameter (double the radius)", "answer": float(d)}] if radius_given else [])
    steps += [{"prompt": f"Circumference of the full circle, {ps} × d", "answer": C},
              {"prompt": f"Divide by {frac}", "answer": arc}]
    worked = ([f"d = 2 × {r} = {d} {u}"] if radius_given else [f"d = {d} {u}"]) + [
        f"C = π × d = {ps} × {d} = {_g(C)} {u}", f"Arc = {_g(C)} ÷ {frac} = **{_g(arc)} {u}**"]
    diag = _diagram("semi", d, f"{d} {u}") if frac == 2 else _diagram("quarter", r, f"{r} {u}")
    if radius_given and frac == 2:
        diag = {}
    return Question(
        question_text=text, correct_answer=arc, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=steps, worked_solution=worked, notes=NOTES_ARC, metadata=diag,
        distractors=distractors(arc, [
            (_r(_r(pv * r * r) / frac), "that's πr² — an AREA. Arc length uses πd (2024 and 2026 "
                                        "marking instructions: πr² scores 0)."),
            (_r(_r(pv * r) / frac), "you used the radius as the diameter — double it first (2023, "
                                    "2024 course reports; 2026 marking instructions)."),
            (C, f"that's the whole circle — divide by {frac} for a {name} (2022 marking instructions)."),
            (_r(_r(pv * d) / (6 - frac)), f"a {name} is ÷ {frac}, not ÷ {6 - frac}."),
        ]))


# ── Level 2: perimeter of a composite shape ───────────────────────────────────────────────────
def _perim_rect_semi(non_calc):
    pv, ps = _pi(non_calc)
    u, what = random.choice([("cm", "badge"), ("cm", "sign"), ("m", "flower bed"), ("cm", "table top")])
    w = random.choice([6, 8, 10, 12, 14, 20, 30, 40, 50])
    L = random.choice([x for x in (8, 10, 12, 15, 18, 20, 24, 30, 40, 50, 60, 90) if x > w * 0.8])
    arc = _r(pv * w / 2); st = 2 * L + w; tot = _r(arc + st)
    text = f"A {what} is a rectangle with a semi-circle on one end, as shown. Calculate its perimeter."
    lines = [f"Semi-circle: arc = {ps} × {w} ÷ 2 = {_g(arc)} {u}", f"Straight edges = {L} + {w} + {L} = {st} {u}",
             f"Perimeter = {_g(arc)} + {st} = **{_g(tot)} {u}**"]
    steps = [{"prompt": "Length of the curved edge (semi-circle)", "answer": arc},
             {"prompt": "Total of the straight edges", "answer": float(st)}]
    wrong = [(_r(pv * w + st), "you didn't halve the circumference — it's a SEMI-circle (2022 marking "
                               "instructions)."),
             (_r(_r(pv * (w / 2) ** 2 / 2) + st), "you used πr² (an area) for the curved edge (2019, "
                                                  "2025 course reports)."),
             (_r(arc + st + w), "the dashed line inside the shape isn't part of the perimeter.")]
    return text, tot, u, lines, steps, wrong, _diagram("rect_semi", L, w, [f"{L} {u}", f"{w} {u}"])


def _perim_track(non_calc):
    pv, ps = _pi(non_calc)
    w = random.choice([40, 50, 60, 64, 70, 80]); L = random.choice([80, 85, 90, 100, 110])
    arc = _r(pv * w); st = 2 * L; tot = _r(arc + st)
    text = "A running track is a rectangle with a semi-circle at each end, as shown. Calculate its perimeter."
    lines = [f"Two semi-circles make one circle: C = {ps} × {w} = {_g(arc)} m", f"Straight edges = {L} + {L} = {st} m",
             f"Perimeter = {_g(arc)} + {st} = **{_g(tot)} m**"]
    steps = [{"prompt": "Two semi-circles = one full circle: its circumference", "answer": arc},
             {"prompt": "Total of the straight edges", "answer": float(st)}]
    wrong = [(_r(_r(pv * w / 2) + st), "there are TWO semi-circles — together they make a whole circle."),
             (_r(_r(pv * (w / 2) ** 2) + st), "you used πr² (an area) for the curved edges."),
             (_r(arc + st + 2 * w), "the dashed lines inside the track aren't part of the perimeter.")]
    return text, tot, "m", lines, steps, wrong, _diagram("track", L, w, [f"{L} m", f"{w} m"])


def _perim_square_quarter(non_calc):
    pv, ps = _pi(non_calc)
    s = random.choice([8, 10, 12, 14, 15, 20]); gap = random.choice([0, 1, 1.5, 2])
    arc = _r(pv * 2 * s / 4); st = 4 * s - gap; tot = _r(arc + st)
    gate = f", leaving a {_g(gap)} m gap for a gate" if gap else ""
    text = (f"A garden is the shape of a square and a quarter circle, as shown. A fence is built around "
            f"the garden{gate}. Calculate the length of the fence.")
    minus = f" − {_g(gap)}" if gap else ""
    lines = [f"Quarter circle: arc = {ps} × {2 * s} ÷ 4 = {_g(arc)} m",
             f"Straight edges = {s} + {s} + {s} + {s}{minus} = {_g(st)} m", f"Fence = {_g(arc)} + {_g(st)} = **{_g(tot)} m**"]
    steps = [{"prompt": "Length of the curved edge (quarter circle, d = 2 × radius)", "answer": arc},
             {"prompt": "Total of the straight edges" + (" (take off the gap)" if gap else ""), "answer": float(st)}]
    wrong = [(_r(_r(pv * s / 4) + st), "you used the radius as the diameter (2026 Paper 1 Q12 marking "
                                       "instructions: 3.14 × 10 ÷ 4)."),
             (_r(_r(pv * s * s / 4) + st), "you used πr² (an area) for the curved edge (2026 marking "
                                           "instructions)."),
             (_r(_r(pv * 2 * s) + st), "that's the whole circle — a quarter circle is ÷ 4 (2026 marking "
                                       "instructions)."),
             (_r(arc + 4 * s), "you forgot to take off the gap for the gate.") if gap else (None, "")]
    return text, tot, "m", lines, steps, wrong, _diagram("square_quarter", s, gap, [f"{s} m", f"{_g(gap)} m"])


def _perim_arch(non_calc):
    pv, ps = _pi(False)
    r = random.choice([400, 500, 600, 700]); W = random.choice([x for x in (1600, 1800, 2000, 2300, 2400) if x > 2 * r + 200])
    H = random.choice([800, 900, 1000, 1200])
    arc = _r(pv * r); top = W - 2 * r; st = W + 2 * H + top; tot = _r(arc + st)
    text = ("A window is made from two rectangles and two identical quarter circles, as shown. Calculate "
            "the length of edging needed for its perimeter, to 2 decimal places.")
    lines = [f"Two quarter circles make a semi-circle: arc = π × {2 * r} ÷ 2 = {_g(arc)} mm",
             f"Top edge = {W} − {r} − {r} = {top} mm", f"Straight edges = {W} + {H} + {H} + {top} = {st} mm",
             f"Perimeter = {_g(arc)} + {st} = **{_g(tot)} mm**"]
    steps = [{"prompt": "Two quarter circles: length of the curved edges", "answer": arc},
             {"prompt": "Straight edge at the top, between the quarter circles", "answer": float(top)},
             {"prompt": "Total of the straight edges", "answer": float(st)}]
    wrong = [(_r(arc + W + 2 * H), "you missed the straight edge at the top — subtract the two radii "
                                   "(2023 course report: most candidates missed this)."),
             (_r(_r(pv * r / 2) + st), "you used the radius as the diameter (2023 course report)."),
             (_r(_r(pv * 2 * r) + st), "two quarter circles make HALF a circle, not a whole one.")]
    return text, tot, "mm", lines, steps, wrong, _diagram("arch", W, H, r, [f"{W} mm", f"{H} mm", f"{r} mm"])


def generate_perimeter_area_l2(calc_mode=False):
    """Perimeter of a composite shape."""
    non_calc = random.random() < 0.5
    make = random.choice([_perim_rect_semi, _perim_track, _perim_square_quarter, _perim_arch])
    text, ans, u, lines, steps, wrong, diag = make(non_calc)
    if make is not _perim_arch:
        text += " Take π = 3.14." if non_calc else " Give your answer to 2 decimal places."
    steps = steps + [{"prompt": "Perimeter", "answer": ans}]
    return Question(question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=lines, notes=NOTES_PERIMETER, metadata=diag,
                    distractors=distractors(ans, wrong))


# ── Level 3: area of a semi-circle / quarter circle ───────────────────────────────────────────
def generate_perimeter_area_l3(calc_mode=False):
    """Area of a semi-circle or quarter circle."""
    what, u = random.choice(_ARC_CONTEXTS)
    frac = random.choice([2, 4])
    non_calc = random.random() < 0.5
    pv, ps = _pi(non_calc)
    radius_given = random.random() < 0.5
    r = random.choice([2, 3, 4, 5, 6, 8, 10, 12, 14, 15, 20])
    d = 2 * r
    name = "semi-circle" if frac == 2 else "quarter circle"
    given = f"radius {r} {u}" if radius_given else f"diameter {d} {u}"
    tail = "Take π = 3.14." if non_calc else "Give your answer to 2 decimal places."
    A = _r(pv * r * r); ans = _r(A / frac)
    steps = ([] if radius_given else [{"prompt": "Radius (halve the diameter)", "answer": float(r)}])
    steps += [{"prompt": f"Area of the full circle, {ps} × r²", "answer": A}, {"prompt": f"Divide by {frac}", "answer": ans}]
    worked = ([f"r = {r} {u}"] if radius_given else [f"r = {d} ÷ 2 = {r} {u}"]) + [
        f"A = π × r² = {ps} × {r}² = {_g(A)} {u}²", f"{name.capitalize()}: A = {_g(A)} ÷ {frac} = **{_g(ans)} {u}²**"]
    diag = _diagram("semi", d, f"{d} {u}") if (frac == 2 and not radius_given) else (
        _diagram("quarter", r, f"{r} {u}") if frac == 4 and radius_given else {})
    return Question(
        question_text=f"A {what} is a {name} with {given}. Calculate its area. {tail}", correct_answer=ans,
        topic=TOPIC, question_type=QTYPE, scaffold_steps=steps, worked_solution=worked, notes=NOTES_AREA,
        metadata=diag,
        distractors=distractors(ans, [
            (_r(_r(pv * d * d) / frac), "you used the diameter in πr² — halve it first (2023 course "
                                        "report; 2026 marking instructions)."),
            (A, f"that's the whole circle — divide by {frac} for a {name} (2025 course report)."),
            (_r(_r(pv * d) / frac), "πd is the circumference (a length), not the area (2023, 2025 course "
                                    "reports)."),
            (_r(_r(pv * 2 * r) / frac), "2r isn't r² — square the radius."),
        ]))


# ── Level 4: area of a composite shape ────────────────────────────────────────────────────────
def _area_rect_semi(pv, ps):
    w = random.choice([6, 8, 10, 12, 14, 16, 20]); L = random.choice([10, 12, 15, 18, 20, 24, 30])
    R = L * w; S = _r(pv * (w / 2) ** 2 / 2); T = _r(R + S)
    lines = [f"Rectangle: {L} × {w} = {R} m²", f"Semi-circle: r = {_g(w / 2)}, {ps} × {_g(w / 2)}² ÷ 2 = {_g(S)} m²",
             f"Total = {R} + {_g(S)} = **{_g(T)} m²**"]
    steps = [{"prompt": "Area of the rectangle", "answer": float(R)}, {"prompt": "Area of the semi-circle", "answer": S}]
    wrong = [(_r(R + _r(pv * (w / 2) ** 2)), "you didn't halve the circle — it's a semi-circle (2025 course "
                                            "report)."),
             (_r(R + _r(pv * w * w / 2)), "you used the diameter in πr² (2023 course report)."),
             (_r(R + _r(pv * w / 2)), "πd ÷ 2 is the curved edge's length, not the semi-circle's area (2025 "
                                      "marking instructions).")]
    return ("A playpark is a rectangle and a semi-circle, as shown. Calculate its area.", T, lines, steps, wrong,
            _diagram("rect_semi", L, w, [f"{L} m", f"{w} m"]))


def _area_door(pv, ps):
    w = random.choice([0.76, 0.8, 0.85, 0.9]); h = random.choice([1.98, 2, 2.03, 2.1]); d = random.choice([0.4, 0.5, 0.54, 0.6])
    R = _r(w * h); S = _r(pv * (d / 2) ** 2 / 2); T = _r(R - S)
    lines = [f"Rectangle: {_g(h)} × {_g(w)} = {_g(R)} m²", f"Window: r = {_g(d / 2)}, {ps} × {_g(d / 2)}² ÷ 2 = {_g(S)} m²",
             f"Area to paint = {_g(R)} − {_g(S)} = **{_g(T)} m²**"]
    steps = [{"prompt": "Area of the rectangle", "answer": R}, {"prompt": "Area of the semi-circular window", "answer": S}]
    wrong = [(_r(R + S), "you added the window — it isn't painted, so SUBTRACT it (2026 Paper 2 Q2 marking "
                         "instructions)."),
             (_r(R - _r(pv * d * d / 2)), "you used the diameter in πr² (2026 marking instructions: "
                                          "π × 0.54² ÷ 2)."),
             (_r(R - _r(pv * (d / 2) ** 2)), "the window is a SEMI-circle — halve the circle's area.")]
    return ("A front door is a rectangle with a semi-circular window, as shown. Calculate the area of the door "
            "to be painted (not the window).", T, lines, steps, wrong,
            _diagram("door", w, h, d, [f"{_g(w)} m", f"{_g(h)} m", f"{_g(d)} m"]))


def _area_house(pv, ps):
    w = random.choice([6, 8, 10, 12]); h = random.choice([4, 5, 6]); t = random.choice([2, 3, 4])
    R = w * h; Tr = _r(0.5 * w * t); T = _r(R + Tr)
    lines = [f"Rectangle: {w} × {h} = {R} m²", f"Triangle: 0.5 × {w} × {t} = {_g(Tr)} m²", f"Total = {R} + {_g(Tr)} = **{_g(T)} m²**"]
    steps = [{"prompt": "Area of the rectangle", "answer": float(R)}, {"prompt": "Area of the triangle", "answer": Tr}]
    wrong = [(R + w * t, "you didn't halve for the triangle — ½ × base × height (2018 and 2022 marking "
                         "instructions).")]
    return ("The end wall of a house is a rectangle with an isosceles triangle on top, as shown. Calculate the "
            "area of the wall.", T, lines, steps, wrong, _diagram("house", w, h, t, [f"{w} m", f"{h} m", f"{t} m"]))


def _area_patio(pv, ps):
    L = random.choice([10, 12, 14, 15]); w = random.choice([8, 9, 10]); r = random.choice([1.5, 2, 2.5, 3])
    R = L * w; C = _r(pv * r * r); T = _r(R - C)
    lines = [f"Rectangle: {L} × {w} = {R} m²", f"Pond: {ps} × {_g(r)}² = {_g(C)} m²", f"Patio = {R} − {_g(C)} = **{_g(T)} m²**"]
    steps = [{"prompt": "Area of the rectangle", "answer": float(R)}, {"prompt": "Area of the pond", "answer": C}]
    wrong = [(_r(R + C), "the pond is cut out of the patio — SUBTRACT it."),
             (_r(R - _r(pv * 2 * r)), "πd is the circumference, not the area (2024 course report)."),
             (_r(R - _r(pv * 4 * r * r)), "you used the diameter in πr².")]
    return ("A patio is a rectangle with a circular pond in the middle, as shown. Calculate the area of the "
            "patio (shaded).", T, lines, steps, wrong, _diagram("patio", L, w, r, [f"{L} m", f"{w} m", f"{_g(r)} m"]))


def _area_square_semis(pv, ps):
    s = random.choice([1, 1.2, 1.4, 1.5]); d = random.choice([x for x in (0.5, 0.6, 0.7, 0.8) if x < s])
    Q = _r(s * s); C = _r(2 * pv * (d / 2) ** 2); T = _r(Q + C)
    lines = [f"Square: {_g(s)} × {_g(s)} = {_g(Q)} m²", f"Four semi-circles = two circles: 2 × {ps} × {_g(d / 2)}² = {_g(C)} m²",
             f"Total = {_g(Q)} + {_g(C)} = **{_g(T)} m²**"]
    steps = [{"prompt": "Area of the square", "answer": Q}, {"prompt": "Area of the four semi-circles", "answer": C}]
    wrong = [(_r(Q + _r(pv * (d / 2) ** 2)), "there are FOUR semi-circles (2023 marking instructions: "
                                            "π × 0.35² + 1.44)."),
             (_r(Q + _r(4 * pv * (d / 2) ** 2)), "four SEMI-circles make two circles, not four (2023 marking "
                                                "instructions)."),
             (_r(Q + _r(2 * pv * d * d)), "you used the diameter in πr² (2023 course report).")]
    return ("A mirror is a square with an identical semi-circle on each side, as shown. Calculate its area.", T,
            lines, steps, wrong, _diagram("square_semis", s, d, [f"{_g(s)} m", f"{_g(d)} m"]))


def generate_perimeter_area_l4(calc_mode=False):
    """Area of a composite shape (add or subtract)."""
    non_calc = random.random() < 0.3
    pv, ps = _pi(non_calc)
    make = random.choice([_area_rect_semi, _area_door, _area_house, _area_patio, _area_square_semis])
    text, ans, lines, steps, wrong, diag = make(pv, ps)
    if make is not _area_house:
        text += " Take π = 3.14." if non_calc else " Give your answer to 2 decimal places."
    steps = steps + [{"prompt": "Total area", "answer": ans}]
    wrong = [(v, m) for v, m in wrong if v is not None and v > 0]     # no negative "areas"
    return Question(question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=lines, notes=NOTES_COMPOSITE, metadata=diag,
                    distractors=distractors(ans, wrong))


def _not_whole(A, per):
    """Nudge A so that A ÷ per isn't a whole number (there must be something to round up)."""
    while abs(A / per - round(A / per)) < 0.02:
        A = round(A + 0.37, 2)
    return A


# ── Level 5: how many do I need? ──────────────────────────────────────────────────────────────
def generate_perimeter_area_l5(calc_mode=False):
    """Area / length → number of bags, boxes or panels (rounded UP) → cost."""
    kind = random.choice(["bark", "panels", "paint"])
    if kind == "bark":
        A = round(random.uniform(40, 300), 2); per = random.choice([4, 5, 6, 8]); A = _not_whole(A, per); price = random.choice([6.5, 7.5, 8, 9.25])
        text = (f"A playpark has an area of {_g(A)} m². It is covered with bark. One bag covers {per} m² and costs "
                f"£{price:.2f}. Calculate the cost of the bark.")
        q, unit = A / per, "bags"
    elif kind == "panels":
        A = round(random.uniform(30, 90), 2); per = random.choice([1.8, 2, 2.5, 3]); A = _not_whole(A, per); price = random.choice([21.4, 23.6, 24.5, 29.99])
        text = (f"A fence round a garden is {_g(A)} m long. Fence panels are {_g(per)} m long and cost £{price:.2f} each. "
                f"Calculate the cost of the panels.")
        q, unit = A / per, "panels"
    else:
        A = round(random.uniform(2, 12), 2); per = random.choice([2.5, 4, 5]); A = _not_whole(A, per); price = random.choice([12.99, 14.99, 18.5])
        text = (f"A wall has {_g(A)} m² to paint. One tin of paint covers {_g(per)} m² and costs £{price:.2f}. "
                f"Calculate the cost of the paint.")
        q, unit = A / per, "tins"
    n = math.ceil(q - 1e-9); cost = _r(n * price)
    return Question(
        question_text=text, correct_answer=cost, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": f"Number of {unit} needed (round UP)", "answer": float(n)},
                        {"prompt": "Cost", "answer": cost}],
        worked_solution=[f"{_g(A)} ÷ {_g(per)} = {_g(_r(q))} → {n} {unit} (round up)",
                         f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"],
        notes=NOTES_HOW_MANY,
        distractors=distractors(cost, [
            (_r(math.floor(q) * price), f"you rounded DOWN — {math.floor(q)} {unit} isn't enough (2025 Paper 1 "
                                        f"Q7 marking instructions: 81 ÷ 5 = 16 bags)."),
            (_r(q * price), f"you can't buy part of a {unit[:-1]} — round up to {n} first (2019 course "
                            f"report)."),
            (_r(A * price), f"divide by what one {unit[:-1]} covers first (2025 marking instructions: "
                            f"81 × 8)."),
        ]))


def generate_perimeter_area_question(calc_mode=False):
    return random.choice([generate_perimeter_area_l1, generate_perimeter_area_l2, generate_perimeter_area_l3,
                          generate_perimeter_area_l4, generate_perimeter_area_l5])(calc_mode=calc_mode)
