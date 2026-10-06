import random
from decimal import Decimal

from core.models.question_model import Question

NOTES = """
**Multiplying and Dividing Decimals (no calculator):**

- By a **single-digit whole number**: ignore the decimal point, do the whole-number calculation,
  then put the point back in the same relative position.
- By **10 / 100 / 1000**: multiply moves the point **right** 1 / 2 / 3 places; divide moves it
  **left** 1 / 2 / 3 places.
- - By a **multiple of 10, 100 or 1000** (e.g. 30, 200, 4000): split it, e.g. 200 = 2 × 100 —
  multiply or divide by the single digit, then by the 10 / 100 / 1000.

**Example:** 16·3 × 6 = **97·8**

**Example:** 57·5 ÷ 100 — move the point 2 places left → **0·575**

**Example:** 3·4 × 200 — 3·4 × 2 = 6·8, then × 100 → **680**
"""


def _fmt(d):
    s = format(d.normalize(), "f")
    return s


def _dec(lo, hi, dp):
    scale = 10 ** dp
    return Decimal(random.randint(lo * scale, hi * scale)) / scale


def _q(text, answer, worked, scaffold, diagram, params):
    meta = {"diagram": diagram, "diagram_params": params} if diagram else {}
    return Question(
        question_text=text,
        correct_answer=float(answer),
        topic="Numeracy",
        question_type="Decimal Multiplication and Division",
        scaffold_steps=scaffold,
        worked_solution=worked,
        notes=NOTES,
        metadata=meta,
    )


# Level 1 — decimal by a single-digit whole number
def generate_decimal_multiplication_division_l1():
    dp = random.choice([1, 2])
    n = random.randint(2, 9)
    if random.random() < 0.5:
        value = _dec(1, 40, dp)
        answer = value * n
        return _q(f"Calculate {_fmt(value)} × {n}", answer,
                  [f"Ignore the point: {int(value * 10 ** dp)} × {n} = {int(value * 10 ** dp) * n}",
                   f"Put the point back ({dp} decimal place{'s' if dp > 1 else ''}): "
                   f"{_fmt(value)} × {n} = **{_fmt(answer)}**"],
                  [], "decimal_mul_div",
                  {"value": _fmt(value), "operation": "multiply", "kind": "single_digit", "n": n})
    answer = _dec(1, 40, dp)
    value = answer * n
    return _q(f"Calculate {_fmt(value)} ÷ {n}", answer,
              [f"Ignore the point: {int(value * 10 ** dp)} ÷ {n} = {int(answer * 10 ** dp)}",
               f"Put the point back: {_fmt(value)} ÷ {n} = **{_fmt(answer)}**"],
              [], "decimal_mul_div",
              {"value": _fmt(value), "operation": "divide", "kind": "single_digit", "n": n})


# Level 2 — multiply/divide by 10, 100, 1000
def generate_decimal_multiplication_division_l2():
    power = random.choice([10, 100, 1000])
    places = {10: 1, 100: 2, 1000: 3}[power]
    dp = random.choice([1, 2])
    value = _dec(1, 90, dp)
    if random.random() < 0.5:
        answer = value * power
        return _q(f"Calculate {_fmt(value)} × {power}", answer,
                  [f"Multiplying by {power} moves the decimal point {places} place"
                   f"{'s' if places > 1 else ''} to the right.",
                   f"{_fmt(value)} × {power} = **{_fmt(answer)}**"],
                  [], "decimal_mul_div",
                  {"value": _fmt(value), "operation": "multiply", "kind": "shift", "n": power})
    answer = value / power
    return _q(f"Calculate {_fmt(value)} ÷ {power}", answer,
              [f"Dividing by {power} moves the decimal point {places} place"
               f"{'s' if places > 1 else ''} to the left.",
               f"{_fmt(value)} ÷ {power} = **{_fmt(answer)}**"],
              [], "decimal_mul_div",
              {"value": _fmt(value), "operation": "divide", "kind": "shift", "n": power})


# Level 3 — multiples of 10, 100 and 1000 (e.g. 30, 200, 4000)
def generate_decimal_multiplication_division_l3():
    k = random.randint(2, 9)
    power = random.choice([10, 100, 1000])
    m = k * power
    dp = random.choice([1, 2])
    if random.random() < 0.5:
        value = _dec(1, 40, dp)
        answer = value * m
        iv = int(value * 10 ** dp)
        scaffold = [
            {"prompt": f"Ignore the decimal point and multiply {iv} × {k}", "answer": iv * k},
            {"prompt": f"Now multiply {_fmt(value * k)} by {power}", "answer": float(answer)},
        ]
        worked = [
            f"{m} = {k} × {power}, so multiply by {k} then by {power}.",
            f"{_fmt(value)} × {k} = {_fmt(value * k)}",
            f"{_fmt(value * k)} × {power} = **{_fmt(answer)}**",
        ]
        return _q(f"Calculate {_fmt(value)} × {m}", answer, worked, scaffold,
                  "lattice_multiplication", {"a": iv, "b": k})
    answer = _dec(1, 40, dp)
    value = answer * m
    shifted = value / power
    d = max(-shifted.normalize().as_tuple().exponent, -answer.normalize().as_tuple().exponent, 0)
    n = int(shifted * 10 ** d)
    scaffold = [
        {"prompt": f"Divide {_fmt(value)} by {power}", "answer": float(shifted)},
        {"prompt": f"Now divide {_fmt(shifted)} by {k}", "answer": float(answer)},
    ]
    worked = [
        f"{m} = {k} × {power}, so divide by {power} then by {k}.",
        f"{_fmt(value)} ÷ {power} = {_fmt(shifted)}",
        f"{_fmt(shifted)} ÷ {k} = **{_fmt(answer)}**",
    ]
    return _q(f"Calculate {_fmt(value)} ÷ {m}", answer, worked, scaffold,
              "bus_stop_division", {"dividend": n, "divisor": k})


def generate_decimal_multiplication_division_question():
    return random.choice([
        generate_decimal_multiplication_division_l1,
        generate_decimal_multiplication_division_l2,
        generate_decimal_multiplication_division_l3,
    ])()
