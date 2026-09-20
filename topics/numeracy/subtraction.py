import random
from core.models.question_model import Question

NOTES = """
**Column Subtraction:**

1. Line up the numbers by place value, units under units, tens under tens, and so on, with
   the larger number on top.
2. Start with the column furthest to the right (the units).
3. Subtract the bottom digit from the top digit in each column. If the top digit is smaller,
   **borrow** a ten from the next column to the left first.
4. Repeat for every column.

**Example:** Calculate 523 − 187.
- Units: 3 − 7 → borrow a ten, 13 − 7 = 6
- Tens: 1 (after lending) − 8 → borrow a hundred, 11 − 8 = 3
- Hundreds: 4 (after lending) − 1 = 3
- 523 − 187 = **336**
"""

_DIGIT_RANGES = {
    2: (10, 99),
    3: (100, 999),
}


def _random_pair(digit_count):
    lo, hi = _DIGIT_RANGES[digit_count]
    a = random.randint(lo, hi)
    b = random.randint(lo, a - 1) if a > lo else lo
    return a, b


def _diagram(a, b):
    return {"diagram": "column_calculation", "diagram_params": {"a": a, "b": b, "op": "-", "dp": 0}}


# ---------------------------------------------------------------------------
# Level 1 — two 2-digit numbers, no negative result
# ---------------------------------------------------------------------------

def generate_subtraction_l1(calc_mode=False):
    a, b = _random_pair(2)
    answer = a - b

    question_text = f"Calculate {a} − {b}."
    scaffold_steps = [{"prompt": "What is the answer?", "answer": answer}]
    worked = [
        f"Subtract {a} − {b} using column subtraction, right to left, borrowing where needed.",
        f"{a} − {b} = **{answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Subtraction",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(a, b),
    )


# ---------------------------------------------------------------------------
# Level 2 — two 3-digit numbers, no negative result
# ---------------------------------------------------------------------------

def generate_subtraction_l2(calc_mode=False):
    a, b = _random_pair(3)
    answer = a - b

    question_text = f"Calculate {a} − {b}."
    scaffold_steps = [{"prompt": "What is the answer?", "answer": answer}]
    worked = [
        f"Subtract {a} − {b} using column subtraction, right to left, borrowing where needed.",
        f"{a} − {b} = **{answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Subtraction",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(a, b),
    )


def generate_subtraction_question(calc_mode=False):
    return random.choice([generate_subtraction_l1, generate_subtraction_l2])(calc_mode=calc_mode)
