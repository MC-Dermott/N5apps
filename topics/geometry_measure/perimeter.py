"""N5 Geometry and Measure — Perimeter (split from the old Perimeter and Area, Oct 2026).

Mirrors Perimeter_Worksheet.docx (N5 Apps/Worksheets/Geometry and Measure): rectangles and squares,
L-shapes with missing sides, circumference of circles, arc length of semi-circles and of quarter circles
(a costed one gives the radius only; some ask for the whole edge, curved plus straight), perimeter of composite
shapes, and "how many do I need?" (a perimeter, round UP, then cost). Every shape can also be asked
the exam way — a fence, edging or rail priced per metre, "calculate the cost" (2019 P2 Q5, 2021 P2 Q2)
— through `shape_costs.finish`, and the last level is all costed questions.

Distractors are the errors in the course reports and marking instructions: only the length and width
added (half way round), the area found instead of the perimeter (2019, 2025 CR), πr² used for a length,
the radius used in πd, the circumference not halved / quartered, the straight top edge missed
(2023 P2 Q2), the number of panels rounded down (2019 P2 Q5 CR, 2025 P1 Q7b MI).

Values are rounded to 2 d.p. at each step, as the worksheet's working does; π = 3.14 on the
non-calculator (Paper 1 style) questions.
"""
import math
import random

from core.models.distractors import distractors
from core.models.question_model import Question
from topics.geometry_measure.shape_costs import (TOPIC, r2, g, pi_for, diagram, not_whole, tail_for,
                                                 finish)

QTYPE = "Perimeter"
COST_SHARE = 0.35          # how often a level 1–4 question is the costed (exam-style) version

NOTES_RECT = """
**Perimeter of a rectangle or square**

The perimeter is the total distance all the way round the outside edge. A rectangle has two pairs of
equal sides, so add all four. Write the units in your answer.

**Example (from the worksheet):** A sheep pen on a croft is a rectangle 12 m long and 7 m wide.
- Perimeter = 12 + 7 + 12 + 7 = **38 m**

**Costs:** a fence or edging is priced per metre, so cost = perimeter × price per metre. Fencing
costing £4.50 per metre round a 9 m by 6 m plot: 30 × £4.50 = **£135.00**.

⚠ Adding only the length and the width is half way round. Go round the whole outside, writing down
all four sides, and give the units. Find the perimeter (not the area) when the price is per metre.
"""

NOTES_LSHAPE = """
**Perimeter of an L-shape with missing sides**

Some sides are not labelled. Work them out from the sides you know: the sides going across add up to
the full width, and the sides going up and down add up to the full height. Then add up ALL six sides.

**Example (from the worksheet):** The floor of a croft house extension is an L-shape, 10 m wide and
8 m high, with the notch 4 m across and 3 m down.
- a = 8 − 3 = 5 m
- b = 10 − 4 = 6 m
- Perimeter = 10 + 5 + 4 + 3 + 6 + 8 = **36 m**
- Check: 2 × (10 + 8) = 36 m

⚠ Adding only the sides that are labelled, or working out a missing side but then leaving it out of
the perimeter. An L-shape has six sides: tick each one as you add it.
"""

NOTES_CIRCLE = """
**Circumference of a circle**

C = πd (use the **diameter**). If you are given the radius, double it first: d = 2 × r.

**Example (from the worksheet):** A circular pond has a radius of 4 m. Take π = 3.14.
- d = 2 × 4 = 8 m
- C = 3.14 × 8 = **25.12 m**

⚠ πr² is an AREA, not a length, and the radius is not the diameter (course reports 2023, 2024, 2026).
For a cost, multiply the circumference by the price per metre.
"""

NOTES_ARC = """
**Arc length of a semi-circle or quarter circle**

C = πd (use the **diameter**). A semi-circle's curved edge is C ÷ 2; a quarter circle's is C ÷ 4.
If the whole edge is needed, add the straight edge(s): the diameter of a semi-circle, the two radii of a
quarter circle.

**Example (from the worksheet):** A garden bed is a semi-circle with diameter 20 cm. Take π = 3.14.
- C = 3.14 × 20 = 62.8 cm
- Arc = 62.8 ÷ 2 = **31.4 cm**

⚠ πr² is an AREA, not a length, and if you're given the radius, double it first (course reports
2023, 2024, 2026). For a cost, multiply the length of the curved edge by the price per metre.
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
calculate an area by mistake (2019, 2025). For a fence or rail, multiply the perimeter by the price
per metre.
"""

NOTES_HOW_MANY = """
**How many do I need?**

Find the perimeter first, divide by the length of one panel / rail, then **round UP** — you can't
buy part of a panel. Then multiply by the price.

**Example (from the worksheet):** A fence 38.5 m long; panels are 1.8 m long and cost £24.50 each.
- 38.5 ÷ 1.8 = 21.39 → **22 panels**
- 22 × £24.50 = **£539.00**

⚠ Rounding down was common: in 2019 many didn't round the number of 3 m lengths of rail up before
the cost, and in 2025 81 ÷ 5 = 16 bags (it should be 17).
"""


# ── Level 1: rectangles and squares ───────────────────────────────────────────────────────────
_RECT_THINGS = [("m", "vegetable plot"), ("m", "football pitch"), ("m", "paddock"), ("m", "school garden"),
                ("cm", "noticeboard"), ("cm", "picture frame")]


def _spec_rect(cost):
    u, thing = random.choice([t for t in _RECT_THINGS if t[0] == "m"] if cost else _RECT_THINGS)
    big = u == "m"
    L = random.choice([8, 9, 12, 15, 18, 20, 24, 30, 45, 90] if big else [60, 80, 90, 120, 150])
    w = random.choice([x for x in ([5, 6, 7, 8, 9, 10, 12, 14, 20, 40] if big else [30, 45, 50, 75, 90]) if x < L])
    tot = 2 * (L + w)
    return dict(desc=f"A {thing} is a rectangle {L} {u} by {w} {u}, as shown.", instr="Calculate its perimeter.",
                ans=float(tot), u=u, kind="length", final=False, steps=[],
                lines=[f"Perimeter = {L} + {w} + {L} + {w} = **{tot} {u}**"],
                wrong=[(float(L + w), "you only added the length and the width — that's half way round; add "
                                      "all four sides."),
                       (float(L * w), "that's the AREA (length × width) — the perimeter is the distance "
                                      "round the edge (2019, 2025 course reports).")],
                diag=diagram("rect", L, w, [f"{L} {u}", f"{w} {u}"]), item=("fencing", "Fencing"))


def _spec_square(cost):
    u = "m"
    s = random.choice([4.5, 5, 6.5, 7.5, 8, 9.5, 12, 15.5])
    tot = r2(4 * s)
    return dict(desc=f"A square {random.choice(['patio', 'paddock', 'vegetable plot'])} has sides of length "
                     f"{g(s)} {u}.", instr="Calculate its perimeter.", ans=tot, u=u, kind="length",
                final=False, steps=[], lines=[f"Perimeter = 4 × {g(s)} = **{g(tot)} {u}**"],
                wrong=[(r2(2 * s), "a square has FOUR equal sides — you only found half way round."),
                       (r2(s * s), "that's the AREA — the perimeter is the distance round the edge.")],
                diag={}, item=("fencing", "Fencing"))


def _spec_rect_back():
    P = random.choice([40, 50, 60, 64, 80, 90, 120]); L = random.choice([x for x in (12, 15, 18, 20, 24, 30) if x < P / 2 - 3])
    half = P // 2; w = half - L
    return dict(desc=f"A rectangular field has a perimeter of {P} m. It is {L} m long.",
                instr="Calculate its width.", ans=float(w), u="m", kind="length", final=False,
                steps=[{"prompt": "Length + width (half the perimeter)", "answer": float(half)},
                       {"prompt": "Width", "answer": float(w)}],
                lines=[f"Length + width = {P} ÷ 2 = {half} m", f"Width = {half} − {L} = **{w} m**"],
                wrong=[(float(P - L), "you took the length off the whole perimeter — halve it first, "
                                      "since two lengths and two widths make the perimeter."),
                       (float(P / 2 - 2 * L), "the length appears once in length + width, not twice.")],
                diag={})


def generate_perimeter_l1(calc_mode=False, cost=None):
    """Perimeter of a rectangle or square (and the cost of fencing it)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    pick = random.choice(["rect", "rect", "square", "back"] if not cost else ["rect", "square"])
    spec = {"rect": _spec_rect, "square": _spec_square}.get(pick, lambda c: _spec_rect_back())(cost)
    return finish(spec, cost, QTYPE, NOTES_RECT, "Perimeter")


# ── Level 2: L-shapes with missing sides ──────────────────────────────────────────────────────
_HIDDEN = [[1], [4], [1, 4], [1, 2], [3, 4], [2, 3]]
_PARTNER = {1: 3, 3: 1, 2: 4, 4: 2}


def _spec_lshape(cost):
    W = random.randint(9, 18); H = random.randint(7, 13)
    a = random.randint(3, W - 4); b = random.randint(2, H - 3)
    e = [W, H - b, a, b, W - a, H]
    hidden = sorted(random.choice(_HIDDEN))
    name = {i: "ab"[n] for n, i in enumerate(hidden)}
    labels = [name[i] if i in name else f"{e[i]} m" for i in range(6)]
    lines, steps = [], []
    for i in hidden:
        whole = H if i in (1, 3) else W
        lines.append(f"{name[i]} = {whole} − {e[_PARTNER[i]]} = {e[i]} m")
        steps.append({"prompt": f"Missing side {name[i]}", "answer": float(e[i])})
    tot = sum(e)
    lines.append(f"Perimeter = {' + '.join(str(x) for x in e)} = **{tot} m**")
    names = " and ".join(name[i] for i in hidden)
    mark = f"(marked {names})"
    desc = (f"A {random.choice(['garden', 'school hall', 'croft house extension', 'weaving shed'])} is an "
            f"L-shape, as shown. Some sides are not labelled: work out the missing sides {mark} first.")
    known = sum(e[i] for i in range(6) if i not in name)
    return dict(desc=desc, instr="Calculate its perimeter.", ans=float(tot), u="m", kind="length", steps=steps,
                lines=lines, wrong=[(float(known), "you added only the sides that are labelled — an L-shape "
                                                   "has six sides, so work out the missing ones too."),
                                    (float(tot - sum(e[i] for i in hidden) + 0), "you left the missing sides "
                                                                                 "out of the perimeter.")],
                diag=diagram("lshape_r", W, H, a, b, labels, random.randint(0, 3), random.randint(0, 1)),
                item=("fencing", "Fencing"))


def generate_perimeter_l2(calc_mode=False, cost=None):
    """Perimeter of an L-shape with missing sides (and the cost of fencing it)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    return finish(_spec_lshape(cost), cost, QTYPE, NOTES_LSHAPE, "Perimeter")


# ── Level 3: circles, semi-circles and quarter circles ────────────────────────────────────────
_CIRCLE_CONTEXTS = [("round trampoline", "m"), ("circular pond", "m"), ("circular paddling pool", "m"),
                    ("circular table top", "cm"), ("clock face", "cm")]
_CIRCLE_COST_CONTEXTS = [("circular pond", "m"), ("circular paddling pool", "m"), ("circular flower bed", "m"),
                         ("circular sheep pen", "m")]
_ARC_CONTEXTS = [("garden bed", "m"), ("badge", "cm"), ("stone arch", "m"), ("window", "m"),
                 ("table corner", "cm"), ("flower bed", "m")]
_RADII = [3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]


def _spec_circle(cost):
    """A whole circle. A costed question gives the RADIUS only (the worksheet's rule)."""
    what, u = random.choice(_CIRCLE_COST_CONTEXTS if cost else _CIRCLE_CONTEXTS)
    non_calc = random.random() < 0.6
    pv, ps = pi_for(non_calc)
    radius_given = True if cost else random.random() < 0.5
    r = random.choice(_RADII); d = 2 * r
    C = r2(pv * d)
    given = f"a radius of {r} {u}" if radius_given else f"a diameter of {d} {u}"
    steps = ([{"prompt": "Diameter (double the radius)", "answer": float(d)}] if radius_given else [])
    steps += [{"prompt": f"Circumference, {ps} × d", "answer": C}]
    lines = ([f"d = 2 × {r} = {d} {u}"] if radius_given else [f"d = {d} {u}"]) + [
        f"C = π × d = {ps} × {d} = **{g(C)} {u}**"]
    diag = diagram("circle_r", r, f"{r} {u}") if radius_given else diagram("circle", d, f"{d} {u}")
    return dict(desc=f"A {what} has {given}.", instr="Calculate its circumference.",
                ans=C, u=u, kind="length", final=False, steps=steps, lines=lines, tail=tail_for(non_calc),
                item=("fencing", "Fencing"), diag=diag,
                wrong=[(r2(pv * r * r), "that's πr² — an AREA. Circumference uses πd (2024 and 2026 marking "
                                        "instructions: πr² scores 0)."),
                       (r2(pv * r), "you used the radius as the diameter — double it first (2023, 2024 course "
                                    "reports; 2026 marking instructions)."),
                       (r2(pv * d * d), "you multiplied by the diameter twice — C = π × d.")])


def _spec_arc(cost, frac=None):
    """A semi-circle (frac 2) or quarter circle (frac 4). A costed question gives the RADIUS only, and half
    of them ask for the WHOLE edge: the curved edge plus the straight edge(s)."""
    frac = frac or random.choice([2, 4])
    what, u = random.choice([c for c in _ARC_CONTEXTS if c[1] == "m"] if cost else _ARC_CONTEXTS)
    non_calc = random.random() < 0.6
    pv, ps = pi_for(non_calc)
    radius_given = True if cost else random.random() < 0.5
    edge = bool(cost) and random.random() < 0.5
    r = random.choice(_RADII); d = 2 * r
    name = "semi-circle" if frac == 2 else "quarter circle"
    given = f"radius {r} {u}" if radius_given else f"diameter {d} {u}"
    C = r2(pv * d); arc = r2(C / frac)
    straight = d if frac == 2 else 2 * r
    steps = ([{"prompt": "Diameter (double the radius)", "answer": float(d)}] if radius_given else [])
    steps += [{"prompt": f"Circumference of the full circle, {ps} × d", "answer": C},
              {"prompt": f"Divide by {frac}", "answer": arc}]
    lines = ([f"d = 2 × {r} = {d} {u}"] if radius_given else [f"d = {d} {u}"]) + [
        f"C = π × d = {ps} × {d} = {g(C)} {u}", f"Arc = {g(C)} ÷ {frac} = **{g(arc)} {u}**"]
    if radius_given:
        diag = diagram("semi_r", r, f"{r} {u}") if frac == 2 else diagram("quarter", r, f"{r} {u}")
    else:
        diag = diagram("semi", d, f"{d} {u}") if frac == 2 else diagram("quarter", r, f"{r} {u}")
    wrong = [(r2(r2(pv * r * r) / frac), "that's πr² — an AREA. Arc length uses πd (2024 and 2026 "
                                         "marking instructions: πr² scores 0)."),
             (r2(r2(pv * r) / frac), "you used the radius as the diameter — double it first (2023, "
                                     "2024 course reports; 2026 marking instructions)."),
             (C, f"that's the whole circle — divide by {frac} for a {name} (2022 marking "
                 f"instructions)."),
             (r2(r2(pv * d) / (6 - frac)), f"a {name} is ÷ {frac}, not ÷ {6 - frac}.")]
    spec = dict(desc=f"A {what} is a {name} with {given}.", instr="Calculate the length of its curved edge.",
                ans=arc, u=u, kind="length", final=False, steps=steps, lines=lines, tail=tail_for(non_calc),
                item=("edging", "Edging"), diag=diag, wrong=wrong)
    if edge:
        whole = r2(arc + straight)
        straight_word = "straight edge" if frac == 2 else "two straight edges"
        spec.update(
            desc=(f"A {what} is a {name} with {given}. It is edged all the way round, along the curved edge "
                  f"and the {straight_word}."),
            instr="Calculate the length of the whole edge.", ans=whole, item=("edging", "Edging"),
            steps=steps + [{"prompt": f"Whole edge: curved edge + {straight_word} "
                                      f"({g(straight)} {u})", "answer": whole}],
            lines=lines[:-1] + [f"Arc = {g(C)} ÷ {frac} = {g(arc)} {u}",
                                f"Whole edge = {g(arc)} + {g(straight)} = **{g(whole)} {u}**"],
            wrong=[(arc, f"that's only the curved edge — add the {straight_word} too (2023 course report: "
                         f"straight edges missed)."),
                   (r2(arc + r), f"the {straight_word} {'is the diameter' if frac == 2 else 'are TWO radii'}, "
                                 f"{'not the radius' if frac == 2 else 'not one'}."),
                   (r2(wrong[0][0] + straight), "you used πr² (an AREA) for the curve."),
                   (r2(C + straight), f"you didn't divide the circumference by {frac}.")])
    return spec


def generate_perimeter_circles(calc_mode=False, cost=None):
    """Circumference of a circle (and the cost of fencing it)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    return finish(_spec_circle(cost), cost, QTYPE, NOTES_CIRCLE, "Circumference")


def generate_perimeter_semicircles(calc_mode=False, cost=None):
    """Arc length of a semi-circle (and the cost of edging it, curved edge only or the whole edge)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    return finish(_spec_arc(cost, 2), cost, QTYPE, NOTES_ARC, "Length of the edge")


def generate_perimeter_quarters(calc_mode=False, cost=None):
    """Arc length of a quarter circle (and the cost of edging it, curved edge only or the whole edge)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    return finish(_spec_arc(cost, 4), cost, QTYPE, NOTES_ARC, "Length of the edge")


def generate_perimeter_l3(calc_mode=False, cost=None):
    """Kept for older references: a semi-circle or quarter circle."""
    return random.choice([generate_perimeter_semicircles, generate_perimeter_quarters])(calc_mode, cost)


# ── Level 4: composite perimeter ──────────────────────────────────────────────────────────────
def _perim_rect_semi(non_calc, cost):
    pv, ps = pi_for(non_calc)
    u, what = random.choice([("m", "paddock"), ("m", "flower bed"), ("m", "pond")] if cost else
                            [("cm", "badge"), ("cm", "sign"), ("m", "flower bed"), ("cm", "table top")])
    w = random.choice([6, 8, 10, 12, 14, 20, 30, 40, 50]) if u == "cm" or what != "paddock" else random.choice([20, 25, 30])
    L = random.choice([x for x in (8, 10, 12, 15, 18, 20, 24, 30, 40, 50, 60, 90) if x > w * 0.8])
    arc = r2(pv * w / 2); st = 2 * L + w; tot = r2(arc + st)
    lines = [f"Semi-circle: arc = {ps} × {w} ÷ 2 = {g(arc)} {u}", f"Straight edges = {L} + {w} + {L} = {st} {u}",
             f"Perimeter = {g(arc)} + {st} = **{g(tot)} {u}**"]
    steps = [{"prompt": "Length of the curved edge (semi-circle)", "answer": arc},
             {"prompt": "Total of the straight edges", "answer": float(st)}]
    wrong = [(r2(pv * w + st), "you didn't halve the circumference — it's a SEMI-circle (2022 marking "
                               "instructions)."),
             (r2(r2(pv * (w / 2) ** 2 / 2) + st), "you used πr² (an area) for the curved edge (2019, "
                                                  "2025 course reports)."),
             (r2(arc + st + w), "the dashed line inside the shape isn't part of the perimeter.")]
    return dict(desc=f"A {what} is a rectangle with a semi-circle on one end, as shown.",
                instr="Calculate its perimeter.", ans=tot, u=u, kind="length", steps=steps, lines=lines, wrong=wrong,
                diag=diagram("rect_semi", L, w, [f"{L} {u}", f"{w} {u}"]), item=("fencing", "Fencing"))


def _perim_track(non_calc, cost):
    pv, ps = pi_for(non_calc)
    w = random.choice([40, 50, 60, 64, 70, 80]); L = random.choice([80, 85, 90, 100, 110])
    arc = r2(pv * w); st = 2 * L; tot = r2(arc + st)
    lines = [f"Two semi-circles make one circle: C = {ps} × {w} = {g(arc)} m", f"Straight edges = {L} + {L} = {st} m",
             f"Perimeter = {g(arc)} + {st} = **{g(tot)} m**"]
    steps = [{"prompt": "Two semi-circles = one full circle: its circumference", "answer": arc},
             {"prompt": "Total of the straight edges", "answer": float(st)}]
    wrong = [(r2(r2(pv * w / 2) + st), "there are TWO semi-circles — together they make a whole circle."),
             (r2(r2(pv * (w / 2) ** 2) + st), "you used πr² (an area) for the curved edges."),
             (r2(arc + st + 2 * w), "the dashed lines inside the track aren't part of the perimeter.")]
    return dict(desc="A running track is a rectangle with a semi-circle at each end, as shown. A rail is put "
                     "all the way round the outside of the track." if cost else
                     "A running track is a rectangle with a semi-circle at each end, as shown.",
                instr="Calculate its perimeter.", ans=tot, u="m", kind="length", steps=steps, lines=lines,
                wrong=wrong, diag=diagram("track", L, w, [f"{L} m", f"{w} m"]), item=("rail", "Railing"))


def _perim_square_quarter(non_calc, cost):
    pv, ps = pi_for(non_calc)
    s = random.choice([8, 10, 12, 14, 15, 20]); gap = random.choice([0, 1, 1.5, 2])
    arc = r2(pv * 2 * s / 4); st = 4 * s - gap; tot = r2(arc + st)
    gate = f", leaving a {g(gap)} m gap for a gate" if gap else ""
    minus = f" − {g(gap)}" if gap else ""
    lines = [f"Quarter circle: arc = {ps} × {2 * s} ÷ 4 = {g(arc)} m",
             f"Straight edges = {s} + {s} + {s} + {s}{minus} = {g(st)} m", f"Fence = {g(arc)} + {g(st)} = **{g(tot)} m**"]
    steps = [{"prompt": "Length of the curved edge (quarter circle, d = 2 × radius)", "answer": arc},
             {"prompt": "Total of the straight edges" + (" (take off the gap)" if gap else ""), "answer": float(st)}]
    wrong = [(r2(r2(pv * s / 4) + st), "you used the radius as the diameter (2026 Paper 1 Q12 marking "
                                       "instructions: 3.14 × 10 ÷ 4)."),
             (r2(r2(pv * s * s / 4) + st), "you used πr² (an area) for the curved edge (2026 marking "
                                           "instructions)."),
             (r2(r2(pv * 2 * s) + st), "that's the whole circle — a quarter circle is ÷ 4 (2026 marking "
                                       "instructions)."),
             (r2(arc + 4 * s), "you forgot to take off the gap for the gate.") if gap else (None, "")]
    return dict(desc=f"A garden is the shape of a square and a quarter circle, as shown. A fence is built "
                     f"around the garden{gate}.", instr="Calculate the length of the fence.", ans=tot, u="m",
                kind="length", steps=steps, lines=lines, wrong=wrong, item=("fencing", "Fencing"),
                diag=diagram("square_quarter", s, gap, [f"{s} m", f"{g(gap)} m"]))


def _perim_arch(non_calc, cost):
    pv, ps = pi_for(False)
    r = random.choice([400, 500, 600, 700]); W = random.choice([x for x in (1600, 1800, 2000, 2300, 2400) if x > 2 * r + 200])
    H = random.choice([800, 900, 1000, 1200])
    arc = r2(pv * r); top = W - 2 * r; st = W + 2 * H + top; tot = r2(arc + st)
    lines = [f"Two quarter circles make a semi-circle: arc = π × {2 * r} ÷ 2 = {g(arc)} mm",
             f"Top edge = {W} − {r} − {r} = {top} mm", f"Straight edges = {W} + {H} + {H} + {top} = {st} mm",
             f"Perimeter = {g(arc)} + {st} = **{g(tot)} mm**"]
    steps = [{"prompt": "Two quarter circles: length of the curved edges", "answer": arc},
             {"prompt": "Straight edge at the top, between the quarter circles", "answer": float(top)},
             {"prompt": "Total of the straight edges", "answer": float(st)}]
    wrong = [(r2(arc + W + 2 * H), "you missed the straight edge at the top — subtract the two radii "
                                   "(2023 course report: most candidates missed this)."),
             (r2(r2(pv * r / 2) + st), "you used the radius as the diameter (2023 course report)."),
             (r2(r2(pv * 2 * r) + st), "two quarter circles make HALF a circle, not a whole one.")]
    return dict(desc="A window is made from two rectangles and two identical quarter circles, as shown.",
                instr="Calculate the length of edging needed for its perimeter.", ans=tot, u="mm", kind="length",
                steps=steps, lines=lines, wrong=wrong, tail="Give your answer to 2 decimal places.",
                diag=diagram("arch", W, H, r, [f"{W} mm", f"{H} mm", f"{r} mm"]))


_TRIPLES = [(5, 12), (6, 8), (8, 6), (12, 5), (9, 12), (15, 20)]


def _perim_tri_semi(non_calc, cost):
    pv, ps = pi_for(non_calc)
    a, b = random.choice(_TRIPLES)
    h = math.hypot(a, b); h = float(round(h))
    arc = r2(pv * h / 2); tot = r2(a + b + arc)
    lines = [f"Hypotenuse: d = √({a}² + {b}²) = {g(h)} m", f"Semi-circle: arc = {ps} × {g(h)} ÷ 2 = {g(arc)} m",
             f"Perimeter = {a} + {b} + {g(arc)} = **{g(tot)} m**"]
    steps = [{"prompt": "Longest side (Pythagoras): the semi-circle's diameter", "answer": h},
             {"prompt": "Length of the curved edge", "answer": arc}]
    wrong = [(r2(a + b + h + arc), "the hypotenuse is inside the shape — the semi-circle's curved edge "
                                   "replaces it (2025 course report)."),
             (r2(a + b + r2(pv * h)), "you didn't halve the circumference — it's a SEMI-circle."),
             (r2(r2(pv * (h / 2) ** 2 / 2) + a + b), "you used πr² (an area) for the curved edge.")]
    return dict(desc="A badge is a right-angled triangle with a semi-circle on its longest side, as shown.",
                instr="Calculate the perimeter of the badge.", ans=tot, u="m", kind="length", steps=steps,
                lines=lines, wrong=wrong, item=("edging strip", "Edging strip"), diag=diagram("tri_semi", a, b, [f"{a} m", f"{b} m"]))


def generate_perimeter_l4(calc_mode=False, cost=None):
    """Perimeter of a composite shape (and the cost of fencing / railing it)."""
    cost = (random.random() < COST_SHARE) if cost is None else cost
    non_calc = random.random() < 0.5
    makers = [_perim_rect_semi, _perim_track, _perim_square_quarter, _perim_tri_semi] + ([] if cost else [_perim_arch])
    make = random.choice(makers)
    spec = make(non_calc, cost)
    if make is not _perim_arch:
        spec["tail"] = tail_for(non_calc)
    spec["wrong"] = [(v, m) for v, m in spec["wrong"] if v is not None]
    return finish(spec, cost, QTYPE, NOTES_PERIMETER, "Perimeter")


# ── Level 5: how many do I need? ──────────────────────────────────────────────────────────────
def generate_perimeter_l5(calc_mode=False):
    """A perimeter → number of panels, rails or rolls (rounded UP) → cost."""
    kind = random.choice(["panels", "rails", "garden", "ribbon", "track"])
    if kind in ("panels", "rails"):
        P = round(random.uniform(30, 90), 2)
        per = random.choice([1.8, 2, 2.4, 2.5]) if kind == "panels" else 3
        what = "panels" if kind == "panels" else "rails"
        P = not_whole(P, per); price = random.choice([21.4, 23.6, 24.5, 19.95, 8.4])
        text = (f"A fence round a garden is {g(P)} m long. Fence panels are {g(per)} m long and cost £{price:.2f} "
                f"each. Calculate the cost of the panels." if kind == "panels" else
                f"A rail is fitted all the way round a decking area. The rail is {g(P)} m long. Rails come in "
                f"{g(per)} m lengths costing £{price:.2f} each. Calculate the cost of the rails.")
        q = P / per; n = math.ceil(q - 1e-9); cost = r2(n * price)
        steps = [{"prompt": f"Number of {what} needed (round UP)", "answer": float(n)}, {"prompt": "Cost", "answer": cost}]
        worked = [f"{g(P)} ÷ {g(per)} = {g(r2(q))} → {n} {what} (round up)", f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
        wrong = [(r2(math.floor(q) * price), f"you rounded DOWN — {math.floor(q)} {what} isn't enough (2019 "
                                              f"Paper 2 Q5 course report; 2025 Paper 1 Q7 marking instructions)."),
                 (r2(q * price), f"you can't buy part of a {what[:-1]} — round up to {n} first."),
                 (r2(P * price), f"divide by the length of one {what[:-1]} first.")]
        meta = {}
    elif kind == "garden":
        L = random.choice([20, 24, 26, 30, 36]); w = random.choice([12, 14, 15, 18]); gap = random.choice([0, 2, 3])
        per = random.choice([2, 2.5, 3]); price = random.choice([21.4, 23.6, 24.5, 29.99])
        P = 2 * (L + w) - gap
        while abs(P / per - round(P / per)) < 0.02:
            gap += 1; P = 2 * (L + w) - gap
        gate = f" The fence has a {gap} m gap for a gate." if gap else ""
        text = (f"A school garden is a rectangle {L} m by {w} m, as shown. A fence is built all the way round it."
                f"{gate} Fence panels are {g(per)} m long and cost £{price:.2f} each. Calculate the cost of "
                f"the panels.")
        q = P / per; n = math.ceil(q - 1e-9); cost = r2(n * price)
        minus = f" − {gap}" if gap else ""
        steps = [{"prompt": "Length of the fence" + (" (take off the gap)" if gap else ""), "answer": float(P)},
                 {"prompt": "Number of panels needed (round UP)", "answer": float(n)}, {"prompt": "Cost", "answer": cost}]
        worked = [f"Length of fence = {L} + {w} + {L} + {w}{minus} = {P} m",
                  f"{P} ÷ {g(per)} = {g(r2(q))} → {n} panels (round up)", f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
        wrong = [(r2(math.floor(q) * price), f"you rounded DOWN — {math.floor(q)} panels isn't enough (2019 "
                                              f"Paper 2 Q5 course report)."),
                 (r2(q * price), f"you can't buy part of a panel — round up to {n} first."),
                 (r2(math.ceil((L * w) / per) * price), "you used the AREA, not the perimeter (2019, 2025 "
                                                         "course reports).")]
        if gap:
            wrong.append((r2(math.ceil((P + gap) / per) * price), "you forgot to take off the gap for the gate."))
        meta = diagram("rect", L, w, [f"{L} m", f"{w} m"])
    elif kind == "track":
        L = random.choice([60, 70, 85, 90, 100]); w = random.choice([40, 50, 64, 70])
        per = random.choice([2, 2.4, 2.5, 3]); price = random.choice([19.95, 21.4, 23.6, 24.5])
        circ = r2(math.pi * w); P = r2(circ + 2 * L)
        while abs(P / per - round(P / per)) < 0.02:
            L += 1; P = r2(circ + 2 * L)
        text = (f"A running track is a rectangle {L} m long with a semi-circle at each end, {w} m wide, as shown. "
                f"A fence is built all the way round the track, using panels {g(per)} m long costing £{price:.2f} "
                f"each. Calculate the cost of the panels. Give the perimeter to 2 decimal places.")
        q = P / per; n = math.ceil(q - 1e-9); cost = r2(n * price)
        steps = [{"prompt": "Perimeter of the track (m)", "answer": P},
                 {"prompt": "Number of panels needed (round UP)", "answer": float(n)}, {"prompt": "Cost", "answer": cost}]
        worked = [f"Two semi-circles make one circle: C = π × d = π × {w} = {g(circ)} m",
                  f"Perimeter = {g(circ)} + {L} + {L} = {g(P)} m",
                  f"Panels = {g(P)} ÷ {g(per)} = {g(r2(q))} → {n} panels (round up)",
                  f"Cost = {n} × £{price:.2f} = **£{cost:.2f}**"]
        wrong = [(r2(math.floor(q) * price), f"you rounded DOWN — {math.floor(q)} panels isn't enough (2019 "
                                              f"Paper 2 Q5 course report)."),
                 (r2(q * price), f"you can't buy part of a panel — round up to {n} first."),
                 (r2(math.ceil(circ / per) * price), "you left out the two straight edges (2018, 2019 course "
                                                      "reports: a straight edge missed)."),
                 (r2(math.ceil(((L * w) + math.pi * w * w / 4) / per) * price), "you used the AREA, not the "
                                                                                  "perimeter (2019, 2025 course reports).")]
        meta = diagram("track", L, w, [f"{L} m", f"{w} m"])
    else:
        k = random.choice([12, 15, 20, 24, 30]); L = random.choice([8, 10, 12, 15]); w = random.choice([4, 6, 8, 10])
        pcm = r2(2 * L + w + 3.14 * w / 2); roll = random.choice([5, 10])

        def ribbon_text(k):
            return (f"Gold ribbon is put round the edge of {k} badges. Each badge is a rectangle {L} cm by {w} cm "
                    f"with a semi-circle on one end, as shown. Ribbon is sold in {roll} m rolls. How many rolls "
                    f"are needed? Take π = 3.14.")
        X = r2(pcm * k); Xm = r2(X / 100); q = Xm / roll
        while abs(q - round(q)) < 0.02:
            k += 1; X = r2(pcm * k); Xm = r2(X / 100); q = Xm / roll
        text = ribbon_text(k)
        arc = r2(3.14 * w / 2); straight = 2 * L + w
        n = math.ceil(q - 1e-9); cost = float(n)
        steps = [{"prompt": "Perimeter of one badge (cm)", "answer": pcm},
                 {"prompt": "Total length of ribbon in cm", "answer": X},
                 {"prompt": "Change to metres (÷ 100)", "answer": Xm},
                 {"prompt": "Number of rolls (round UP)", "answer": float(n)}]
        worked = [f"Semi-circle: arc = π × d ÷ 2 = 3.14 × {w} ÷ 2 = {g(arc)} cm",
                  f"Straight edges = {L} + {w} + {L} = {straight} cm;  Perimeter = {g(arc)} + {straight} = {g(pcm)} cm",
                  f"Ribbon = {g(pcm)} × {k} = {g(X)} cm;  {g(X)} ÷ 100 = {g(Xm)} m",
                  f"Rolls = {g(Xm)} ÷ {roll} = {g(r2(q))} → **{n} rolls** (round up)"]
        wrong = [(float(max(1, math.floor(q))), "you rounded DOWN — that isn't enough ribbon."),
                 (r2(X / roll), "change the centimetres to metres first (÷ 100) — the rolls are in metres."),
                 (r2(q), "you can't buy part of a roll — round up."),
                 (float(math.ceil(r2(r2(straight * k) / 100) / roll)), "you left out the curved edge of the badge.")]
        meta = diagram("rect_semi", L, w, [f"{L} cm", f"{w} cm"])
    return Question(question_text=text, correct_answer=cost, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=worked, notes=NOTES_HOW_MANY, metadata=meta,
                    distractors=distractors(cost, wrong))


# ── Level 6: exam style — the cost of a perimeter ─────────────────────────────────────────────
def generate_perimeter_costs(calc_mode=False):
    """Any perimeter question, asked the exam way: priced per metre, calculate the cost."""
    return random.choice([generate_perimeter_l1, generate_perimeter_l2, generate_perimeter_circles,
                          generate_perimeter_semicircles, generate_perimeter_quarters,
                          generate_perimeter_l4])(calc_mode=calc_mode, cost=True)


def generate_perimeter_question(calc_mode=False):
    return random.choice([generate_perimeter_l1, generate_perimeter_l2, generate_perimeter_circles,
                          generate_perimeter_semicircles, generate_perimeter_quarters,
                          generate_perimeter_l4, generate_perimeter_l5, generate_perimeter_costs])(
        calc_mode=calc_mode)
