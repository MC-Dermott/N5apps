import random
from decimal import Decimal

from core.models.question_model import Question

NOTES = """
**Multiplying and Dividing Decimals (no calculator):**

- By a **single-digit whole number**: ignore the decimal point, do the whole-number calculation,
  then put the point back in the same relative position.
- By **10 / 100 / 1000**: multiply moves the point **right** 1 / 2 / 3 places; divide moves it
  **left** 1 / 2 / 3 places.
- **Decimal × decimal**: ignore both points and multiply the whole numbers. Count the decimal
  places in the question (both numbers together) and give the answer that many.
- **Dividing by a decimal**: multiply both numbers by 10 (or 100) until the divisor is a whole
  number, then divide.

**Example:** 16·3 × 6 = **97·8**

**Example:** 57·5 ÷ 100 — move the point 2 places left → **0·575**

**Example:** 0·4 × 3·6 — 4 × 36 = 144; 2 decimal places in total → **1·44**

**Example:** 7·2 ÷ 0·4 — multiply both by 10: 72 ÷ 4 = **18**
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


# Level 3 — decimal × decimal (lattice on the whole numbers, then place the point)
def generate_decimal_multiplication_division_l3():
    dp_a, dp_b = random.choice([(1, 1), (1, 1), (2, 1), (1, 2)])
    a = _dec(1, 9, dp_a) if dp_a == 2 else _dec(2, 40, dp_a)
    b = _dec(1, 9, dp_b)
    ia, ib = int(a * 10 ** dp_a), int(b * 10 ** dp_b)
    total_dp = dp_a + dp_b
    answer = a * b
    scaffold = [
        {"prompt": f"Ignore the decimal points and multiply {ia} × {ib}", "answer": ia * ib},
        {"prompt": "How many decimal places are there in total in the question?", "answer": total_dp},
    ]
    worked = [
        f"Ignore the points: {ia} × {ib} = {ia * ib}",
        f"{dp_a} + {dp_b} = {total_dp} decimal places in the question, so {total_dp} in the answer.",
        f"{_fmt(a)} × {_fmt(b)} = **{_fmt(answer)}**",
    ]
    return _q(f"Calculate {_fmt(a)} × {_fmt(b)}", answer, worked, scaffold,
              "lattice_multiplication", {"a": ia, "b": ib})


# Level 4 — divide by a decimal (multiply both by 10, then bus stop)
def generate_decimal_multiplication_division_l4():
    divisor = Decimal(random.randint(2, 9)) / 10
    answer = Decimal(random.randint(3, 60))
    value = answer * divisor
    iv, idv = int(value * 10), int(divisor * 10)
    scaffold = [
        {"prompt": f"Multiply both numbers by 10 so the divisor is a whole number. "
                   f"What is {_fmt(value)} × 10?", "answer": iv},
    ]
    worked = [
        f"Multiply both numbers by 10: {_fmt(value)} ÷ {_fmt(divisor)} = {iv} ÷ {idv}",
        f"{iv} ÷ {idv} = **{_fmt(answer)}**",
    ]
    return _q(f"Calculate {_fmt(value)} ÷ {_fmt(divisor)}", answer, worked, scaffold,
              "bus_stop_division", {"dividend": iv, "divisor": idv})


def generate_decimal_multiplication_division_question():
    return random.choice([
        generate_decimal_multiplication_division_l1,
        generate_decimal_multiplication_division_l2,
        generate_decimal_multiplication_division_l3,
        generate_decimal_multiplication_division_l4,
    ])()
