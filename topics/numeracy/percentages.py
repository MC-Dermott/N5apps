import random
from core.models.question_model import Question

NOTES = """
**Finding a Percentage of an Amount:**

1. Divide the amount by **100** to find 1%
2. Multiply by the **percentage** you need

**Example:** What is 35% of 84?
- 1% of 84 = 84 ÷ 100 = 0.84
- 35% of 84 = 35 × 0.84 = **29.4**
"""


def generate_percentage_question():
    percentage = random.randint(1, 99)
    amount = random.randint(10, 200)
    answer = round((amount * percentage) / 100, 2)
    one_percent = round(amount / 100, 2)

    scaffold_steps = [
        {
            "prompt": "Find 1% of the amount",
            "answer": one_percent
        },
        {
            "prompt": "Multiply 1% by the percentage you need",
            "answer": answer
        }
    ]

    return Question(
        question_text=f"What is {percentage}% of {amount}?",
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=[
            f"1% of {amount} = {amount} ÷ 100 = {one_percent}",
            f"{percentage}% of {amount} = {percentage} × {one_percent} = {answer}",
        ],
        notes=NOTES,
    )
