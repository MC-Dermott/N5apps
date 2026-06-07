import random
from core.models.question_model import Question

NOTES = """
**Finding a Fraction of an Amount:**

1. Divide the amount by the **denominator** (bottom number) to find the unit fraction
2. Multiply that result by the **numerator** (top number)

**Example:** What is 3/5 of 40?
- 1/5 of 40 = 40 ÷ 5 = 8
- 3/5 of 40 = 3 × 8 = **24**
"""

FRACTION_PAIRS = [
    (2, 3), (3, 4), (2, 5), (3, 5),
    (5, 6), (3, 8), (5, 8), (7, 10),
    (4, 5), (2, 7), (5, 9), (7, 8),
]

_N4_FRACTION_PAIRS = [
    (1, 2), (1, 4), (3, 4), (1, 3), (2, 3), (1, 5), (2, 5),
]


def generate_fraction_question_n4():
    numerator, denominator = random.choice(_N4_FRACTION_PAIRS)
    multiplier = random.randint(2, 6)
    amount = denominator * multiplier

    unit_value = amount // denominator
    answer = unit_value * numerator

    scaffold_steps = [
        {
            "prompt": "Divide the amount by the denominator",
            "answer": round(amount / denominator, 2)
        },
        {
            "prompt": "Multiply your result by the numerator",
            "answer": float(answer)
        }
    ]

    return Question(
        question_text=f"What is {numerator}/{denominator} of {amount}?",
        correct_answer=answer,
        topic="Numeracy",
        question_type="Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=[
            f"1/{denominator} of {amount} = {amount} ÷ {denominator} = {unit_value}",
            f"{numerator}/{denominator} of {amount} = {numerator} × {unit_value} = {answer}",
        ],
        notes=NOTES,
    )


def generate_fraction_question():
    numerator, denominator = random.choice(FRACTION_PAIRS)
    multiplier = random.randint(3, 15)
    amount = denominator * multiplier

    unit_value = amount // denominator
    answer = unit_value * numerator

    scaffold_steps = [
        {
            "prompt": "Divide the amount by the denominator",
            "answer": round(amount / denominator, 2)
        },
        {
            "prompt": "Multiply your result by the numerator",
            "answer": float(answer)
        }
    ]

    return Question(
        question_text=f"What is {numerator}/{denominator} of {amount}?",
        correct_answer=answer,
        topic="Numeracy",
        question_type="Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=[
            f"1/{denominator} of {amount} = {amount} ÷ {denominator} = {unit_value}",
            f"{numerator}/{denominator} of {amount} = {numerator} × {unit_value} = {answer}",
        ],
        notes=NOTES,
    )
