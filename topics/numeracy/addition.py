import random
from core.models.question_model import Question

NOTES = """
**Column Addition:**

1. Line up the numbers by place value, units under units, tens under tens, and so on.
2. Start with the column furthest to the right (the units).
3. Add the digits in each column. If the total is 10 or more, write down the units digit and
   **carry** the tens digit into the next column to the left.
4. Repeat for every column, including any carried digit.

**Example:** Calculate 247 + 186.
- Units: 7 + 6 = 13 → write 3, carry 1
- Tens: 4 + 8 + 1 (carried) = 13 → write 3, carry 1
- Hundreds: 2 + 1 + 1 (carried) = 4
- 247 + 186 = **433**
"""

_DIGIT_RANGES = {
    2: (10, 99),
    3: (100, 999),
}


def _random_number(digit_count):
    lo, hi = _DIGIT_RANGES[digit_count]
    return random.randint(lo, hi)


def _diagram(a, b):
    return {"diagram": "column_calculation", "diagram_params": {"a": a, "b": b, "op": "+", "dp": 0}}


# ---------------------------------------------------------------------------
# Level 1 — two 2-digit numbers
# ---------------------------------------------------------------------------

def generate_addition_l1(calc_mode=False):
    a = _random_number(2)
    b = _random_number(2)
    answer = a + b

    question_text = f"Calculate {a} + {b}."
    scaffold_steps = [{"prompt": "What is the answer?", "answer": answer}]
    worked = [
        f"Add {a} + {b} using column addition, right to left, carrying where needed.",
        f"{a} + {b} = **{answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Addition",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(a, b),
    )


# ---------------------------------------------------------------------------
# Level 2 — two 3-digit numbers
# ---------------------------------------------------------------------------

def generate_addition_l2(calc_mode=False):
    a = _random_number(3)
    b = _random_number(3)
    answer = a + b

    question_text = f"Calculate {a} + {b}."
    scaffold_steps = [{"prompt": "What is the answer?", "answer": answer}]
    worked = [
        f"Add {a} + {b} using column addition, right to left, carrying where needed.",
        f"{a} + {b} = **{answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Addition",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(a, b),
    )


def generate_addition_question(calc_mode=False):
    return random.choice([generate_addition_l1, generate_addition_l2])(calc_mode=calc_mode)
