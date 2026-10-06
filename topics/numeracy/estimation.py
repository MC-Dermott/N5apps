import random
from decimal import Decimal, ROUND_HALF_UP

from core.models.question_model import Question

NOTES = """
**Estimating (no calculator):**

- To **estimate**, round every number first, then calculate with the rounded numbers. An
  estimate is quick, not exact.
- Round to the **nearest 10 or 100** for adding/subtracting, or to **1 significant figure**
  (keep the first non-zero digit, round on the next one) for multiplying/dividing.
- Rounding rule: **5 or more rounds up**, 4 or less stays.

**Example:** Estimate 68 + 41 by rounding each number to the nearest 10.
- 68 → 70 and 41 → 40
- 70 + 40 = **110**

**Example:** Estimate 4·87 × 19·6 by rounding each number to 1 significant figure.
- 4·87 → 5 and 19·6 → 20
- 5 × 20 = **100**
"""


def _round_to(value, place):
    d = (Decimal(str(value)) / Decimal(place)).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return int(d * Decimal(place)) if Decimal(place) >= 1 else float(d * Decimal(str(place)))


def _fmt(x):
    return f"{x:g}" if abs(x) < 1e6 else str(int(x))


def _one_sf(value):
    d = Decimal(str(value))
    exp = d.adjusted()
    return _round_to(value, Decimal(10) ** exp)


def _result(question_text, answer, scaffold, worked, metadata):
    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Estimation",
        scaffold_steps=scaffold,
        worked_solution=worked,
        notes=NOTES,
        metadata=metadata,
    )


# Level 1 — add/subtract, round to nearest 10
def generate_estimation_l1():
    return _add_sub(10, 11, 98)


# Level 2 — add/subtract, round to nearest 100
def generate_estimation_l2():
    return _add_sub(100, 105, 9850)


def _add_sub(place, lo, hi):
    while True:
        a, b = random.randint(lo, hi), random.randint(lo, hi)
        op = random.choice(["+", "-"])
        if op == "-" and a < b:
            a, b = b, a
        ra, rb = _round_to(a, place), _round_to(b, place)
        if a != ra and b != rb and ra != rb:
            break
    answer = ra + rb if op == "+" else ra - rb
    sym = "+" if op == "+" else "−"
    return _result(
        f"**Estimate** the answer to {a} {sym} {b} by rounding each number to the nearest {place} first.",
        answer,
        [{"prompt": f"Round {a} to the nearest {place}", "answer": ra},
         {"prompt": f"Round {b} to the nearest {place}", "answer": rb}],
        [f"{a} rounds to {ra}, {b} rounds to {rb}", f"Estimate = {ra} {sym} {rb} = **{answer}**"],
        {"diagram": "estimation", "diagram_params": {"a": a, "b": b, "op": op, "place": place}},
    )


# Level 3 — multiply/divide, round to 1 significant figure
def generate_estimation_l3():
    op = random.choice(["×", "×", "÷"])
    while True:
        if op == "×":
            a = round(random.uniform(1.1, 99), random.choice([0, 1, 2]))
            b = round(random.uniform(1.1, 99), random.choice([0, 1, 2]))
        else:
            b = random.randint(11, 79)
            a = random.randint(110, 990) * random.choice([1, 10])
        ra, rb = _one_sf(a), _one_sf(b)
        if a != ra and b != rb and ra > 0 and rb > 0 and (op == "×" or ra % rb == 0):
            break
    answer = ra * rb if op == "×" else ra // rb
    return _result(
        f"**Estimate** the answer to {_fmt(a)} {op} {_fmt(b)} by rounding each number to "
        f"1 significant figure first.",
        answer,
        [{"prompt": f"Round {_fmt(a)} to 1 significant figure", "answer": ra},
         {"prompt": f"Round {_fmt(b)} to 1 significant figure", "answer": rb}],
        [f"{_fmt(a)} rounds to {_fmt(ra)}, {_fmt(b)} rounds to {_fmt(rb)}",
         f"Estimate = {_fmt(ra)} {op} {_fmt(rb)} = **{_fmt(answer)}**"],
        {},
    )


def generate_estimation_question():
    return random.choice([generate_estimation_l1, generate_estimation_l2, generate_estimation_l3])()
