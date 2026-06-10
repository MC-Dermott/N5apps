import random
import math
from core.models.question_model import Question

NOTES = """
**Mean and Standard Deviation:**

**Mean** x̄ = Σx ÷ n

**Standard deviation:**
$$s = \\sqrt{\\frac{\\Sigma(x - \\bar{x})^2}{n - 1}}$$

**Steps:**
1. Find the mean x̄ = Σx ÷ n
2. Subtract the mean from each value: (x − x̄)
3. Square each difference: (x − x̄)²
4. Add them up: Σ(x − x̄)²
5. Divide by (n − 1)
6. Take the square root

**Example:** 3, 5, 7, 9, 11
- Mean = 35 ÷ 5 = **7**
- Deviations: −4, −2, 0, 2, 4
- Squared: 16, 4, 0, 4, 16 → Sum = 40
- s = √(40 ÷ 4) = √10 ≈ **3.16**
"""


def generate_standard_deviation_question():
    n = random.randint(5, 7)
    centre = random.randint(10, 30)
    data = [centre + random.randint(-10, 10) for _ in range(n)]

    mean = sum(data) / n
    sq_devs = [(x - mean) ** 2 for x in data]
    variance = sum(sq_devs) / (n - 1)
    sd = round(math.sqrt(variance), 2)
    mean_rounded = round(mean, 2)
    sum_sq_rounded = round(sum(sq_devs), 4)
    variance_rounded = round(variance, 4)

    data_str = ", ".join(str(x) for x in data)

    question_text = (
        f"The following values were recorded:\n\n"
        f"**{data_str}**\n\n"
        f"Calculate the standard deviation. Give your answer to 2 decimal places."
    )

    scaffold_steps = [
        {"prompt": f"Calculate the mean of the {n} values", "answer": mean_rounded},
        {"prompt": "Calculate each (x − x̄)² and sum them: Σ(x − x̄)²", "answer": sum_sq_rounded},
        {"prompt": f"Divide by (n − 1) = {n - 1}", "answer": variance_rounded},
        {"prompt": "Take the square root to find s (2 d.p.)", "answer": sd},
    ]

    worked = [
        f"Mean = ({' + '.join(str(x) for x in data)}) ÷ {n} = {mean_rounded}",
        f"Deviations (x − x̄): {', '.join(str(round(x - mean, 2)) for x in data)}",
        f"Squared deviations: {', '.join(str(round((x - mean)**2, 4)) for x in data)}",
        f"Σ(x − x̄)² = {sum_sq_rounded}",
        f"Variance = {sum_sq_rounded} ÷ {n - 1} = {variance_rounded}",
        f"s = √{variance_rounded} ≈ {sd}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=sd,
        topic="Statistics",
        question_type="Standard Deviation",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
