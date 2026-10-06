import random
from decimal import Decimal

from core.models.question_model import Question

NOTES = """
**Adding and Subtracting Decimals (no calculator):**

- Line up the **decimal points** underneath each other before you add or subtract.
- Fill in any empty spaces with a zero so both numbers have the same number of decimal places.
- Add/subtract as normal, then bring the decimal point straight down into the answer.

**Example:** Calculate 4·31 + 4·58
- 4·31
- + 4·58
- = **8·89**

**Example:** Calculate 27·5 − 13·27 (write 27·5 as 27·50)
- 27·50
- − 13·27
- = **14·23**
"""

_CONTEXTS = [
    ("two planks of length {a} m and {b} m are joined end to end", "How long are they altogether?", "+", "m"),
    ("a bag of flour weighs {a} kg and a bag of sugar weighs {b} kg", "What is their total weight?", "+", "kg"),
    ("a ribbon {a} m long has {b} m cut off", "How much ribbon is left?", "-", "m"),
    ("a jug holds {a} litres and {b} litres are poured out", "How much is left in the jug?", "-", "litres"),
]


def _fmt(d, dp):
    return f"{d:.{dp}f}"


def _dec(lo, hi, dp):
    scale = 10 ** dp
    return Decimal(random.randint(lo * scale, hi * scale)) / scale


def _build(a, b, op, dp, question_text, unit=""):
    answer = a + b if op == "+" else a - b
    dp_out = max(dp[0], dp[1])
    a_s, b_s, ans_s = _fmt(a, dp[0]), _fmt(b, dp[1]), _fmt(answer, dp_out)
    padded_a, padded_b = _fmt(a, dp_out), _fmt(b, dp_out)
    sym = "+" if op == "+" else "−"
    worked = [
        "Line up the decimal points" + (", adding zeros so both numbers have the same number of "
                                        "decimal places:" if dp[0] != dp[1] else ":"),
        f"{padded_a} {sym} {padded_b} = **{ans_s}**{(' ' + unit) if unit else ''}",
    ]
    return Question(
        question_text=question_text,
        correct_answer=float(answer),
        topic="Numeracy",
        question_type="Decimal Addition and Subtraction",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "decimal_column",
            "diagram_params": {"a": a_s, "b": b_s, "op": op},
        },
    )


def _ordered(a, b, op):
    return (a, b) if (op == "+" or a >= b) else (b, a)


# Level 1 — two decimals with the same number of decimal places
def generate_decimal_addition_subtraction_l1():
    dp = random.choice([1, 2])
    op = random.choice(["+", "-"])
    a, b = _ordered(_dec(1, 90, dp), _dec(1, 90, dp), op)
    sym = "+" if op == "+" else "−"
    return _build(a, b, op, (dp, dp), f"Calculate {_fmt(a, dp)} {sym} {_fmt(b, dp)}")


# Level 2 — different numbers of decimal places (pad with zeros)
def generate_decimal_addition_subtraction_l2():
    op = random.choice(["+", "-"])
    dp_a, dp_b = random.choice([(1, 2), (2, 1), (1, 3), (2, 0)])
    a, b = _dec(1, 90, dp_a), _dec(1, 90, dp_b)
    if op == "-" and a < b:
        a, b, dp_a, dp_b = b, a, dp_b, dp_a
    sym = "+" if op == "+" else "−"
    return _build(a, b, op, (dp_a, dp_b), f"Calculate {_fmt(a, dp_a)} {sym} {_fmt(b, dp_b)}")


# Level 3 — worded measurement problems
def generate_decimal_addition_subtraction_l3():
    text, ask, op, unit = random.choice(_CONTEXTS)
    dp = random.choice([1, 2])
    a, b = _ordered(_dec(2, 40, dp), _dec(2, 40, dp), op)
    if op == "-" and a == b:
        a += 1
    story = text.format(a=_fmt(a, dp), b=_fmt(b, dp))
    return _build(a, b, op, (dp, dp), f"{story[0].upper()}{story[1:]}. {ask}", unit)


def generate_decimal_addition_subtraction_question():
    return random.choice([
        generate_decimal_addition_subtraction_l1,
        generate_decimal_addition_subtraction_l2,
        generate_decimal_addition_subtraction_l3,
    ])()
