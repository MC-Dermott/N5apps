import random
from core.models.question_model import Question

NOTES = """
**Lattice Multiplication:**

1. Draw a grid with one column per digit of the first number, and one row per digit of the
   second number. Split each cell diagonally.
2. Write the first number's digits along the top, and the second number's digits down the
   side.
3. Multiply each pair of digits (one from the top, one from the side) and write the answer
   in that cell — tens digit above the diagonal, units digit below.
4. Add the digits along each diagonal band, starting from the bottom-right, carrying into the
   next band whenever a diagonal totals 10 or more.
5. Read the answer down the left side and along the bottom.

**Example:** Calculate 236 × 47.
- Multiply every digit of 236 by every digit of 47 into the grid's cells.
- Add along the diagonals, carrying as needed.
- 236 × 47 = **11092**
"""

_A_DIGIT_CHOICES = [2, 3]
_B_DIGIT_CHOICES = [1, 2]


def _random_digits(n):
    digits = [random.randint(1, 9)]
    digits += [random.randint(0, 9) for _ in range(n - 1)]
    return "".join(str(d) for d in digits)


def _diagram(a, b):
    return {"diagram": "lattice_multiplication", "diagram_params": {"a": a, "b": b}}


# ---------------------------------------------------------------------------
# Level 1 — 2-digit x 1-digit
# ---------------------------------------------------------------------------

def generate_multiplication_l1(calc_mode=False):
    a_str = _random_digits(2)
    b = random.randint(2, 9)
    a = int(a_str)
    answer = a * b

    question_text = f"Calculate {a} × {b}."
    scaffold_steps = [{"prompt": "What is the answer?", "answer": answer}]
    worked = [
        f"Multiply {a} × {b} using the lattice method, cell by cell.",
        f"{a} × {b} = **{answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Multiplication",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(a, b),
    )


# ---------------------------------------------------------------------------
# Level 2 — 2-digit x 2-digit
# ---------------------------------------------------------------------------

def generate_multiplication_l2(calc_mode=False):
    a_str = _random_digits(2)
    b_str = _random_digits(2)
    a, b = int(a_str), int(b_str)
    answer = a * b

    question_text = f"Calculate {a} × {b}."
    scaffold_steps = [{"prompt": "What is the answer?", "answer": answer}]
    worked = [
        f"Multiply {a} × {b} using the lattice method, cell by cell.",
        f"{a} × {b} = **{answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Multiplication",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(a, b),
    )


# ---------------------------------------------------------------------------
# Level 3 — 3-digit x 2-digit
# ---------------------------------------------------------------------------

def generate_multiplication_l3(calc_mode=False):
    a_str = _random_digits(3)
    b_str = _random_digits(2)
    a, b = int(a_str), int(b_str)
    answer = a * b

    question_text = f"Calculate {a} × {b}."
    scaffold_steps = [{"prompt": "What is the answer?", "answer": answer}]
    worked = [
        f"Multiply {a} × {b} using the lattice method, cell by cell.",
        f"{a} × {b} = **{answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Multiplication",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(a, b),
    )


def generate_multiplication_question(calc_mode=False):
    return random.choice(
        [generate_multiplication_l1, generate_multiplication_l2, generate_multiplication_l3]
    )(calc_mode=calc_mode)
