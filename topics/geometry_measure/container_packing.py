"""N5 Geometry and Measure — Container Packing.

Mirrors Container_Packing_Worksheet.docx (N5 Apps/Worksheets/Geometry and Measure): packing boxes one
way round; trying both ways round ("this way up"); changing units and choosing a container; tins
(the diameter is the width) and flat packing; and how many containers are needed (round UP), then
the cost. Diagrams: topics/geometry_measure/container_packing_diagrams.py, the same drawings the
worksheet uses.

Method (SQA marking instructions): divide each length of the container by the matching length of
the item, round each DOWN, MULTIPLY; for "this way up" try both ways round on the floor and choose
the bigger. Distractors are the errors in the course reports and marking instructions: volume ÷
volume (2018 P2 Q9c MI, 2019 CR, 2026 CR), one orientation only (2018, 2025, 2026 CR), adding the
counts instead of multiplying (2018, 2019 CR), rounding up / not rounding (2024 P1 Q8, 2026 P2 Q7d
MI), the height matched with the wrong side (2025 P2 Q5b MI), metres converted wrongly (2022 P2 Q4a
MI), and containers rounded down (2018 P2 Q11b MI).
"""
import math
import random

from core.models.distractors import distractors
from core.models.question_model import Question

TOPIC, QTYPE = "Geometry and Measure", "Container Packing"
DIAG = "topics.geometry_measure.container_packing_diagrams"


def _r(x):
    return round(x + 1e-9, 2)


def _g(x):
    x = float(x)
    return str(int(x)) if x == int(x) else f"{x:.6f}".rstrip("0").rstrip(".")


def _fit(a, b):
    """(2 d.p. quotient, whole number) — None if the 2 d.p. value would floor differently."""
    q = _r(a / b)
    n = math.floor(a / b + 1e-9)
    if math.floor(q + 1e-9) != n:
        return None
    return q, n


def _line(a, b, sa=None, sb=None):
    q, n = _fit(a, b)
    return f"{sa or _g(a)} ÷ {sb or _g(b)} = {_g(q)} → {n}"


def _diagram(*specs):
    return {"diagram": "composite_shape",
            "diagram_params": {"module_path": DIAG, "kind": "panels", "args": [list(specs)], "width": 520}}


def _cub(dims, labels, caption, up=False):
    return {"kind": "cuboid", "dims": list(dims), "labels": labels, "caption": caption, "up": up}


def _lab(dims, u):
    return [f"{_g(v)} {u}" for v in dims]


def _ok(C, I):
    return all(_fit(c, i) for c, i in zip(C, I))


NOTES_ONE = """
**Packing boxes:** divide each length of the container by the matching length of the box, round each
answer **DOWN** (part of a box is no use), then **MULTIPLY** the three whole numbers.

**Worksheet example:** boxes 40 cm × 30 cm × 20 cm high in a van 250 cm × 150 cm × 130 cm high, the
40 cm length along the van.
- Along the length: 250 ÷ 40 = 6.25 → 6
- Across the width: 150 ÷ 30 = 5 → 5
- Up the height: 130 ÷ 20 = 6.5 → 6
- Number of boxes = 6 × 5 × 6 = **180 boxes**

⚠ Never divide volume by volume (4 875 000 ÷ 24 000 = 203.13 here — too many, because of the gaps):
in 2018 Paper 2 Q9(c) that scored 0/3. The 2018 and 2019 course reports: many ADDED the numbers
instead of multiplying, or didn't round down.
"""

NOTES_TWO = """
**Both ways round:** "this way up" fixes the height, but the box can still turn round on the floor.
Work out BOTH ways and choose the bigger.

**Worksheet example:** boxes 16 cm × 10 cm × 8 cm high, this way up, in a crate 70 cm × 50 cm × 26 cm high.
- First way: 70 ÷ 16 = 4.38 → 4;  50 ÷ 10 = 5 → 5
- Second way: 70 ÷ 10 = 7 → 7;  50 ÷ 16 = 3.13 → 3
- Height: 26 ÷ 8 = 3.25 → 3
- First way: 4 × 5 × 3 = 60;  second way: 7 × 3 × 3 = 63
- Maximum = **63 boxes**

⚠ Only one way tried (2018, 2025, 2026 course reports). Keep "this way up": in 2025 Paper 2 Q5(b)
dividing the height by the box's length lost marks (marking instructions).
"""

NOTES_UNITS = """
**Units first:** 1 m = 100 cm, 1 cm = 10 mm. Get every length into cm before dividing. With two
containers to choose from, work out each one and compare.

**Worksheet example:** books 240 mm × 160 mm × 25 mm thick, laid flat, in a box 0.5 m × 35 cm × 20 cm high.
- Book in cm: 240 ÷ 10 = 24;  160 ÷ 10 = 16;  25 ÷ 10 = 2.5
- Box in cm: 0.5 × 100 = 50
- First way: 50 ÷ 24 = 2.08 → 2;  35 ÷ 16 = 2.19 → 2
- Second way: 50 ÷ 16 = 3.13 → 3;  35 ÷ 24 = 1.46 → 1
- Height: 20 ÷ 2.5 = 8 → 8
- First way: 2 × 2 × 8 = 32;  second way: 3 × 1 × 8 = 24
- Maximum = **32 books**

⚠ 2022 Paper 2 Q4(a): a wrong metres → cm conversion lost the first mark. 2023 Paper 1 Q7: some
added the two boxes' totals instead of choosing the bigger (marking instructions).
"""

NOTES_TINS = """
**Tins:** a round tin standing up takes up a square as wide as its **diameter** — divide the length and
width by the diameter, the height by the tin's height. **Flat items** (labels, slabs in one layer): try
both ways round and multiply two numbers.

**Worksheet example:** tins with diameter 7.5 cm and height 11 cm in a box 40 cm × 32 cm × 24 cm high.
- Along the length: 40 ÷ 7.5 = 5.33 → 5
- Across the width: 32 ÷ 7.5 = 4.27 → 4
- Up the height: 24 ÷ 11 = 2.18 → 2
- Number of tins = 5 × 4 × 2 = **40 tins**

⚠ Volume ÷ volume is even worse with tins: 30 720 ÷ 485.97 suggests 63, but only 40 fit (2019 course
report: candidates still not considering the gaps).
"""

NOTES_CRATES = """
**How many containers?** Divide the total by how many fit in one container and round **UP** — a part-full
crate still has to be sent. Only round DOWN for how many FULL ones you can fill.

**Worksheet example:** 500 boxes, 48 in each crate, £7.50 to ship each crate.
- Crates = 500 ÷ 48 = 10.42 → 11 crates (round up)
- Cost = 11 × £7.50 = **£82.50**

⚠ 2018 Paper 2 Q11(b): the 20.64 boxes of tiles had to be rounded UP to 21 before the cost
(marking instructions).
"""

_ITEMS_ONE = [("boxes of smoked salmon", "van", "boxes"), ("bales of Harris Tweed", "shipping container", "bales"),
              ("boxes of oatcakes", "crate", "boxes"), ("fish boxes", "refrigerated container", "fish boxes"),
              ("shoeboxes", "cupboard", "shoeboxes"), ("boxes of seaweed soap", "carton", "boxes")]
_ITEMS_UP = [("boxes of tablet", "crate"), ("boxes of black pudding", "shipping container"),
             ("tins of shortbread", "box"), ("egg boxes", "crate"), ("boxes of shinty balls", "crate"),
             ("boxes of fudge", "crate")]


def _small():
    return [random.choice([8, 9, 10, 12, 14, 15, 16, 18, 20, 24, 25, 30, 4.4, 4.6, 8.4, 9.4])]


def _pick_one():
    """Fixed orientation: item dims and container dims with every quotient safe and some rounding."""
    while True:
        cm = random.random() < 0.5
        if cm:
            I = [random.choice([20, 24, 25, 30, 33, 35, 40, 45, 50, 60]), random.choice([10, 12, 15, 20, 25, 30, 40]),
                 random.choice([8, 10, 12, 15, 20, 25])]
            C = [random.randint(60, 300), random.randint(40, 200), random.randint(30, 160)]
        else:
            I = [random.choice([40, 45, 50, 60]), random.choice([25, 30, 35, 40]), random.choice([20, 25, 30])]
            C = [random.randint(250, 600), random.randint(150, 240), random.randint(130, 250)]
        if I[1] > I[0] or not _ok(C, I):
            continue
        counts = [math.floor(c / i + 1e-9) for c, i in zip(C, I)]
        if min(counts) < 2 or all(c % i == 0 for c, i in zip(C, I)):
            continue
        return C, I, counts


def _common_distractors(C, I, counts, ans, extra=()):
    V, v = C[0] * C[1] * C[2], I[0] * I[1] * I[2]
    ceil = [math.ceil(c / i - 1e-9) for c, i in zip(C, I)]
    near = [round(c / i) for c, i in zip(C, I)]
    raw = _r(C[0] / I[0]) * _r(C[1] / I[1]) * _r(C[2] / I[2])
    return distractors(ans, list(extra) + [
        (math.floor(V / v + 1e-9), "you divided volume by volume — that ignores the gaps between boxes "
                                   "(2018 Paper 2 Q9(c): 0 marks)."),
        (_r(V / v), "you divided volume by volume — that ignores the gaps (2018 Paper 2 Q9(c): 0 marks)."),
        (sum(counts), "you ADDED the three numbers — multiply them (2018 and 2019 course reports)."),
        (ceil[0] * ceil[1] * ceil[2], "you rounded UP — part of a box won't fit, so round DOWN "
                                      "(2026 Paper 2 Q7(d) marking instructions)."),
        (near[0] * near[1] * near[2], "you rounded to the nearest whole number — always round DOWN "
                                      "(2024 Paper 1 Q8 marking instructions)."),
        (_r(raw), "you didn't round each number down before multiplying (2026 Paper 2 Q7(d))."),
    ])


# ── Level 1 ────────────────────────────────────────────────────────────────────────────────────
def generate_container_packing_l1():
    """Packing boxes one way round (orientation given)."""
    item, cont, word = random.choice(_ITEMS_ONE)
    C, I, (a, b, c) = _pick_one()
    N = a * b * c
    text = (f"The {item} are {_g(I[0])} cm long, {_g(I[1])} cm wide and {_g(I[2])} cm high. They are packed into a "
            f"{cont} {_g(C[0])} cm long, {_g(C[1])} cm wide and {_g(C[2])} cm high, with the {_g(I[0])} cm length "
            f"along the length of the {cont}. Calculate the maximum number of {word} that fit.")
    worked = [f"Along the length: {_line(C[0], I[0])} (round down)", f"Across the width: {_line(C[1], I[1])} (round down)",
              f"Up the height: {_line(C[2], I[2])} (round down)", f"Number of {word} = {a} × {b} × {c} = **{N} {word}**"]
    steps = [{"prompt": f"How many fit along the length? ({_g(C[0])} ÷ {_g(I[0])}, rounded down)", "answer": a},
             {"prompt": f"How many fit across the width? ({_g(C[1])} ÷ {_g(I[1])}, rounded down)", "answer": b},
             {"prompt": f"How many fit up the height? ({_g(C[2])} ÷ {_g(I[2])}, rounded down)", "answer": c},
             {"prompt": "Multiply to find the maximum number", "answer": N}]
    return Question(question_text=text, correct_answer=N, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=worked, notes=NOTES_ONE,
                    distractors=_common_distractors(C, I, [a, b, c], N),
                    metadata=_diagram(_cub(I, _lab(I, "cm"), "box"), _cub(C, _lab(C, "cm"), cont)))


# ── Level 2 ────────────────────────────────────────────────────────────────────────────────────
def _pick_two(decimal_ok=True):
    while True:
        if decimal_ok and random.random() < 0.3:
            s = random.choice([4.2, 4.4, 4.6, 4.3]); I = [random.choice([8.4, 8.6, 9, 9.4]), s, s]
            C = [random.choice([90, 100, 105, 110, 120]), random.choice([60, 70, 75, 80]), random.choice([40, 45, 50])]
        else:
            I = [random.choice([12, 14, 15, 16, 18, 20, 24, 30, 50]), random.choice([8, 9, 10, 12, 15, 30]),
                 random.choice([5, 6, 7, 8, 9, 10, 20])]
            k = 6 if I[0] < 30 else 12
            C = [random.randint(3 * I[0], k * I[0]), random.randint(3 * I[1], k * I[1]), random.randint(2 * I[2], 8 * I[2])]
        if I[1] >= I[0] or C[1] > C[0] or I[2] > I[1] * 1.5 and I[2] != I[1]:
            continue
        pairs = [(C[0], I[0]), (C[1], I[1]), (C[0], I[1]), (C[1], I[0]), (C[2], I[2]), (C[2], I[0])]
        if not all(_fit(c, i) for c, i in pairs) or C[1] < I[0]:
            continue
        f = lambda c, i: math.floor(c / i + 1e-9)  # noqa: E731
        h = f(C[2], I[2])
        N1, N2 = f(C[0], I[0]) * f(C[1], I[1]) * h, f(C[0], I[1]) * f(C[1], I[0]) * h
        if N1 == N2 or h < 1 or min(N1, N2) < 4:
            continue
        return C, I


def _two_way(C, I, Cs=None, Is=None, word="boxes"):
    Cs = Cs or [_g(v) for v in C]; Is = Is or [_g(v) for v in I]
    f = lambda c, i: math.floor(c / i + 1e-9)  # noqa: E731
    a1, b1, a2, b2, h = f(C[0], I[0]), f(C[1], I[1]), f(C[0], I[1]), f(C[1], I[0]), f(C[2], I[2])
    N1, N2 = a1 * b1 * h, a2 * b2 * h
    N = max(N1, N2)
    worked = [f"First way: {_line(C[0], I[0], Cs[0], Is[0])};  {_line(C[1], I[1], Cs[1], Is[1])} (round down)",
              f"Second way: {_line(C[0], I[1], Cs[0], Is[1])};  {_line(C[1], I[0], Cs[1], Is[0])} (round down)",
              f"Height: {_line(C[2], I[2], Cs[2], Is[2])} (round down)",
              f"First way: {a1} × {b1} × {h} = {N1};  second way: {a2} × {b2} × {h} = {N2}",
              f"Maximum = **{N} {word}**"]
    steps = [{"prompt": f"First way ({Is[0]} along the {Cs[0]} length): how many along?", "answer": a1},
             {"prompt": f"First way: how many across ({Cs[1]} ÷ {Is[1]})?", "answer": b1},
             {"prompt": f"How many layers up the height ({Cs[2]} ÷ {Is[2]})?", "answer": h},
             {"prompt": "Total the first way", "answer": N1},
             {"prompt": "Total the second way (box turned round)", "answer": N2},
             {"prompt": f"Maximum number of {word}", "answer": N}]
    wrong_h = f(C[2], I[0]) * f(C[0], I[2]) * f(C[1], I[1])
    extra = [(min(N1, N2), "you only tried one way round — the other way fits more (2018, 2025 and 2026 course reports)."),
             (N1 + N2, "you added the two ways together — choose the BIGGER of the two (2023 Paper 1 Q7 marking instructions)."),
             (wrong_h, "'this way up' fixes the height — you matched the height with the wrong side of the box "
                       "(2025 Paper 2 Q5(b) marking instructions).")]
    return N, worked, steps, extra, [a1, b1, h]


def generate_container_packing_l2():
    """Trying both ways round, this way up."""
    item, cont = random.choice(_ITEMS_UP)
    C, I = _pick_two()
    N, worked, steps, extra, counts = _two_way(C, I)
    text = (f"The {item} are {_g(I[0])} cm long, {_g(I[1])} cm wide and {_g(I[2])} cm high. They must be packed "
            f"this way up, all facing the same direction, into a {cont} {_g(C[0])} cm long, {_g(C[1])} cm wide and "
            f"{_g(C[2])} cm high. Calculate the maximum number that can be packed.")
    return Question(question_text=text, correct_answer=N, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=worked, notes=NOTES_TWO,
                    distractors=_common_distractors(C, I, counts, N, extra),
                    metadata=_diagram(_cub(I, _lab(I, "cm"), "box", True), _cub(C, _lab(C, "cm"), cont, True)))


# ── Level 3 ────────────────────────────────────────────────────────────────────────────────────
def _units_question():
    while True:
        C, I = _pick_two(decimal_ok=False)
        if all(c % 5 == 0 for c in C) or random.random() < 0.3:
            break
    C = [5 * round(c / 5) or 5 for c in C]
    if not all(_fit(c, i) for c, i in [(C[0], I[0]), (C[1], I[1]), (C[0], I[1]), (C[1], I[0]), (C[2], I[2])]):
        return None
    f = lambda c, i: math.floor(c / i + 1e-9)  # noqa: E731
    if f(C[0], I[0]) * f(C[1], I[1]) == f(C[0], I[1]) * f(C[1], I[0]) or C[1] < I[0]:
        return None
    if f(C[2], I[2]) < 1:
        return None
    Cm = [c / 100 for c in C]
    Cs = [_g(c) for c in C]
    N, worked, steps, extra, counts = _two_way(C, I, Cs, None)
    worked.insert(0, f"Crate in cm: {_g(Cm[0])} × 100 = {_g(C[0])};  {_g(Cm[1])} × 100 = {_g(C[1])};  "
                     f"{_g(Cm[2])} × 100 = {_g(C[2])}")
    steps.insert(0, {"prompt": f"Change the crate's length to cm ({_g(Cm[0])} m × 100)", "answer": C[0]})
    wrongC = [c / 10 for c in C]
    wrong = 0
    if all(w >= i for w, i in zip(wrongC, I)):
        wrong = max(f(wrongC[0], I[0]) * f(wrongC[1], I[1]), f(wrongC[0], I[1]) * f(wrongC[1], I[0])) * f(wrongC[2], I[2])
    extra.append((wrong or None, "1 m = 100 cm, not 10 cm (2022 Paper 2 Q4(a) marking instructions)."))
    text = (f"Boxes {_g(I[0])} cm long, {_g(I[1])} cm wide and {_g(I[2])} cm high must be packed this way up, all "
            f"facing the same direction, into a crate {_g(Cm[0])} m long, {_g(Cm[1])} m wide and {_g(Cm[2])} m high. "
            f"Calculate the maximum number of boxes that fit in the crate.")
    diag = _diagram(_cub(I, _lab(I, "cm"), "box", True), _cub(C, _lab(Cm, "m"), "crate", True))
    return Question(question_text=text, correct_answer=N, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=worked, notes=NOTES_UNITS,
                    distractors=_common_distractors(C, I, counts, N, extra), metadata=diag)


def _compare_question():
    f = lambda c, i: math.floor(c / i + 1e-9)  # noqa: E731
    while True:
        s, h = random.choice([7, 8, 9, 10]), random.choice([11, 12, 14, 15])
        I = [s, s, h]
        A = [random.randint(3 * s, 7 * s), random.randint(3 * s, 6 * s), random.randint(2 * h, 4 * h)]
        B = [random.randint(3 * s, 7 * s), random.randint(3 * s, 6 * s), random.randint(2 * h, 4 * h)]
        if not (_ok(A, I) and _ok(B, I)):
            continue
        cA = [f(c, i) for c, i in zip(A, I)]; cB = [f(c, i) for c, i in zip(B, I)]
        NA, NB = math.prod(cA), math.prod(cB)
        if NA != NB:
            break
    best, N = ("A", NA) if NA > NB else ("B", NB)
    what = random.choice(["honey jars", "candles", "biscuit tins"])
    text = (f"Boxes of {what} have a square base {s} cm by {s} cm and a height of {h} cm, and must stand upright. "
            f"They can be packed into Box A, {A[0]} cm long, {A[1]} cm wide and {A[2]} cm high, or Box B, {B[0]} cm "
            f"long, {B[1]} cm wide and {B[2]} cm high. What is the maximum number of boxes that can be packed into "
            f"one of these boxes?")
    worked = [f"Box A: {_line(A[0], s)};  {_line(A[1], s)};  {_line(A[2], h)} (round down)",
              f"Box A holds {cA[0]} × {cA[1]} × {cA[2]} = {NA}",
              f"Box B: {_line(B[0], s)};  {_line(B[1], s)};  {_line(B[2], h)} (round down)",
              f"Box B holds {cB[0]} × {cB[1]} × {cB[2]} = {NB}",
              f"Maximum = **{N} (box {best})**"]
    steps = [{"prompt": "How many fit in Box A?", "answer": NA}, {"prompt": "How many fit in Box B?", "answer": NB},
             {"prompt": "Maximum number", "answer": N}]
    extra = [(NA + NB, "don't add the two boxes — choose the one that holds more (2023 Paper 1 Q7 marking instructions)."),
             (min(NA, NB), "that's the box that holds FEWER — choose the bigger.")]
    diag = _diagram(_cub(I, _lab(I, "cm"), "item", True), _cub(A, _lab(A, "cm"), "Box A", True),
                    _cub(B, _lab(B, "cm"), "Box B", True))
    best_C = A if best == "A" else B
    return Question(question_text=text, correct_answer=N, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=worked, notes=NOTES_UNITS,
                    distractors=_common_distractors(best_C, I, cA if best == "A" else cB, N, extra), metadata=diag)


def generate_container_packing_l3():
    """Changing units (crate in metres), or choosing between two boxes."""
    if random.random() < 0.6:
        q = None
        while q is None:
            q = _units_question()
        return q
    return _compare_question()


# ── Level 4 ────────────────────────────────────────────────────────────────────────────────────
def _tins_question():
    while True:
        d, h = random.choice([6, 7, 7.5, 8, 9, 10]), random.choice([9, 10, 11, 12, 14])
        C = [random.randint(4 * 6, 8 * 10), random.randint(3 * 6, 6 * 10), random.randint(h + 5, 3 * h + 5)]
        I = [d, d, h]
        if C[1] > C[0] or not _ok(C, I):
            continue
        counts = [math.floor(c / i + 1e-9) for c, i in zip(C, I)]
        if min(counts) >= 2 and any(c % i for c, i in zip(C, I)):
            break
    a, b, c = counts; N = a * b * c
    r = d / 2
    text = (f"Tins are cylinders with diameter {_g(d)} cm and height {h} cm. They stand upright in a box {C[0]} cm long, "
            f"{C[1]} cm wide and {C[2]} cm high. Calculate the maximum number of tins that fit in the box.")
    worked = [f"Along the length: {_line(C[0], d)} (round down)", f"Across the width: {_line(C[1], d)} (round down)",
              f"Up the height: {_line(C[2], h)} (round down)", f"Number of tins = {a} × {b} × {c} = **{N} tins**"]
    steps = [{"prompt": "How many tins fit along the length? (use the diameter)", "answer": a},
             {"prompt": "How many across the width?", "answer": b},
             {"prompt": "How many layers up the height?", "answer": c},
             {"prompt": "Maximum number of tins", "answer": N}]
    V, v = C[0] * C[1] * C[2], math.pi * r * r * h
    rr = [math.floor(C[0] / r + 1e-9), math.floor(C[1] / r + 1e-9)]
    wrong = [(math.floor(V / v + 1e-9), "you divided the box's volume by the tin's volume — the round tins leave "
                                         "gaps (2019 course report)."),
             (rr[0] * rr[1] * c, "you used the radius — each tin takes up its whole DIAMETER."),
             (a + b + c, "you ADDED the three numbers — multiply them (2018 and 2019 course reports)."),
             (math.ceil(C[0] / d - 1e-9) * math.ceil(C[1] / d - 1e-9) * math.ceil(C[2] / h - 1e-9),
              "you rounded UP — part of a tin won't fit, so round DOWN (2026 Paper 2 Q7(d)).")]
    diag = _diagram({"kind": "cylinder", "dims": [d, h], "labels": [f"{_g(d)} cm", f"{h} cm"], "caption": "tin"},
                    _cub(C, _lab(C, "cm"), "box"))
    return Question(question_text=text, correct_answer=N, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                    worked_solution=worked, notes=NOTES_TINS, distractors=distractors(N, wrong), metadata=diag)


def _flat_question():
    f = lambda c, i: math.floor(c / i + 1e-9)  # noqa: E731
    what, unit_l = random.choice([("labels", "sheet"), ("photos", "noticeboard"), ("tiles", "tray")])
    while True:
        I = [random.choice([5, 6, 7, 8, 9, 10, 12]), random.choice([3, 4, 5, 6])]
        C = [random.randint(25, 60), random.randint(18, 40)]
        if I[1] >= I[0] or C[1] > C[0] or C[1] < I[0]:
            continue
        if not all(_fit(c, i) for c, i in [(C[0], I[0]), (C[1], I[1]), (C[0], I[1]), (C[1], I[0])]):
            continue
        N1, N2 = f(C[0], I[0]) * f(C[1], I[1]), f(C[0], I[1]) * f(C[1], I[0])
        if N1 != N2:
            break
    a1, b1, a2, b2 = f(C[0], I[0]), f(C[1], I[1]), f(C[0], I[1]), f(C[1], I[0])
    N = max(N1, N2)
    text = (f"Rectangular {what} {I[0]} cm by {I[1]} cm are placed flat, in one layer and all facing the same way, on a "
            f"{unit_l} {C[0]} cm by {C[1]} cm. Calculate the maximum number of {what} that fit.")
    worked = [f"First way: {_line(C[0], I[0])};  {_line(C[1], I[1])} (round down)",
              f"Second way: {_line(C[0], I[1])};  {_line(C[1], I[0])} (round down)",
              f"First way: {a1} × {b1} = {N1};  second way: {a2} × {b2} = {N2}", f"Maximum = **{N} {what}**"]
    steps = [{"prompt": "Total the first way", "answer": N1}, {"prompt": "Total the second way", "answer": N2},
             {"prompt": f"Maximum number of {what}", "answer": N}]
    wrong = [(min(N1, N2), "you only tried one way round (2025 and 2026 course reports)."),
             (math.floor(C[0] * C[1] / (I[0] * I[1]) + 1e-9), "you divided area by area — that ignores the gaps."),
             (a1 + b1 if N1 > N2 else a2 + b2, "you ADDED instead of multiplying (2018 and 2019 course reports).")]
    diag = _diagram({"kind": "rect", "dims": I, "labels": _lab(I, "cm"), "caption": what[:-1]},
                    {"kind": "rect", "dims": C, "labels": _lab(C, "cm"), "caption": unit_l})
    return Question(question_text=text, correct_answer=N, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                    worked_solution=worked, notes=NOTES_TINS, distractors=distractors(N, wrong), metadata=diag)


def generate_container_packing_l4():
    """Tins (diameter as the width) or flat packing in one layer."""
    return _tins_question() if random.random() < 0.6 else _flat_question()


# ── Level 5 ────────────────────────────────────────────────────────────────────────────────────
def generate_container_packing_l5():
    """How many containers (round UP), then the cost — or how many FULL ones (round DOWN)."""
    kind = random.choice(["crates", "crates", "tiles", "full"])
    if kind == "tiles":
        while True:
            A = _r(random.choice([8.4, 9.6, 10.5, 12.6, 14.7, 15.4, 18.2, 20.8]))
            per, box = random.choice([9, 11, 16, 25]), random.choice([10, 20, 25, 50])
            t = _r(A * per); q = _r(t / box)
            n = math.ceil(A * per / box - 1e-9)
            if math.ceil(q - 1e-9) == n and abs(A * per / box - round(A * per / box)) > 0.02:
                break
        price = random.choice([18.95, 22.50, 24.99, 31.40])
        T = _r(n * price)
        text = (f"A floor has an area of {_g(A)} m². {per} tiles are needed to cover 1 square metre. The tiles are "
                f"sold in boxes of {box}, and each box costs £{price:.2f}. Calculate the cost of the tiles needed.")
        worked = [f"Tiles = {_g(A)} × {per} = {_g(t)}", f"Boxes = {_g(t)} ÷ {box} = {_g(q)} → {n} boxes (round up)",
                  f"Cost = {n} × £{price:.2f} = **£{T:.2f}**"]
        steps = [{"prompt": "Number of tiles", "answer": t}, {"prompt": "Number of boxes (round up)", "answer": n},
                 {"prompt": "Cost (£)", "answer": T}]
        wrong = [(_r((n - 1) * price), "you rounded the boxes DOWN — you'd run out of tiles; round UP "
                                       "(2018 Paper 2 Q11(b) marking instructions)."),
                 (_r(q * price), "you didn't round the number of boxes — you can only buy whole boxes.")]
        return Question(question_text=text, correct_answer=T, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                        worked_solution=worked, notes=NOTES_CRATES, distractors=distractors(T, wrong))
    while True:
        per = random.randint(12, 64)
        total = random.randint(150, 1500)
        q = total / per
        if total % per and _r(q) != round(q) and abs(q - round(q)) > 0.01:
            break
    if kind == "full":
        n = total // per
        text = (f"A shop has {total} tins. It fills boxes that each hold {per} tins. How many FULL boxes can it fill?")
        worked = [f"Boxes = {total} ÷ {per} = {_g(_r(q))} → **{n} full boxes** (round down)"]
        steps = [{"prompt": f"{total} ÷ {per}, then round down", "answer": n}]
        wrong = [(n + 1, "the question asks for FULL boxes — the last box isn't full, so round DOWN.")]
        return Question(question_text=text, correct_answer=n, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                        worked_solution=worked, notes=NOTES_CRATES, distractors=distractors(n, wrong))
    item, cont = random.choice([("boxes of oatcakes", "crate"), ("fleeces", "wool sack"), ("boxes of salmon", "pallet"),
                                ("bales of tweed", "container")])
    n = math.ceil(q)
    cost = random.choice([3.80, 7.50, 12.40, 18.75, 35.00, 42.60])
    T = _r(n * cost)
    text = (f"{total} {item} must be sent to Glasgow. Each {cont} holds {per}. It costs £{cost:.2f} to send each "
            f"{cont}. Calculate the cost of sending all the {item}.")
    worked = [f"{cont.capitalize()}s = {total} ÷ {per} = {_g(_r(q))} → {n} (round up)",
              f"Cost = {n} × £{cost:.2f} = **£{T:.2f}**"]
    steps = [{"prompt": f"How many {cont}s are needed? (round up)", "answer": n}, {"prompt": "Cost (£)", "answer": T}]
    wrong = [(_r((n - 1) * cost), f"you rounded DOWN — {n - 1} {cont}s only hold {(n - 1) * per}; round UP "
                                  f"(2018 Paper 2 Q11(b) marking instructions)."),
             (_r(q * cost), f"you didn't round — you can only send whole {cont}s.")]
    return Question(question_text=text, correct_answer=T, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
                    worked_solution=worked, notes=NOTES_CRATES, distractors=distractors(T, wrong))


def generate_container_packing_question():
    return random.choice([generate_container_packing_l1, generate_container_packing_l2, generate_container_packing_l3,
                          generate_container_packing_l4, generate_container_packing_l5])()
