import random
import math
from core.models.question_model import Question

NOTES = """
**Area of a Circle:**

**Formula:** A = πr²  (where **r** is the radius)

If you are given the **diameter**: r = d ÷ 2

**Example:** Circle with radius 5 cm
- A = π × 5² = π × 25 = **78.54 cm²** (2 d.p.)
"""


def generate_circle_area_question():
    given_radius = random.choice([True, False])

    if given_radius:
        radius = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 15])
        question_text = (
            f"Calculate the area of a circle with radius {radius} cm. "
            f"Give your answer to 2 decimal places."
        )
        answer = round(math.pi * radius ** 2, 2)
        scaffold_steps = [
            {"prompt": "Square the radius", "answer": float(radius ** 2)},
            {"prompt": "Multiply by π to find the area", "answer": answer},
        ]
        worked = [
            "A = πr²",
            f"A = π × {radius}²",
            f"A = π × {radius**2}",
            f"A = {answer} cm²",
        ]
    else:
        diameter = random.choice([6, 8, 10, 12, 14, 16, 18, 20, 24, 30])
        radius = diameter // 2
        question_text = (
            f"Calculate the area of a circle with diameter {diameter} cm. "
            f"Give your answer to 2 decimal places."
        )
        answer = round(math.pi * radius ** 2, 2)
        scaffold_steps = [
            {"prompt": "Find the radius from the diameter", "answer": float(radius)},
            {"prompt": "Square the radius", "answer": float(radius ** 2)},
            {"prompt": "Multiply by π to find the area", "answer": answer},
        ]
        worked = [
            f"r = d ÷ 2 = {diameter} ÷ 2 = {radius} cm",
            f"A = πr² = π × {radius}² = π × {radius**2} = {answer} cm²",
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Geometry and Measure",
        question_type="Area of a Circle",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
