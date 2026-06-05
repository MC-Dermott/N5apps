import random
from core.models.question_model import Question

NOTES = """
**Appreciation and Depreciation:**

- **Appreciation** — value **increases** (e.g. property)
- **Depreciation** — value **decreases** (e.g. cars)

**Multiplier method:**
- Appreciation at r%: multiply by **(1 + r/100)** each year
- Depreciation at r%: multiply by **(1 − r/100)** each year

**Example:** Car worth £8,000 depreciates at 20% per year. Value after 2 years:
- Multiplier = 1 − 0.20 = **0.80**
- After year 1: £8,000 × 0.80 = £6,400
- After year 2: £6,400 × 0.80 = **£5,120**
"""


def generate_appreciation_question():
    kind = random.choice(["depreciation", "appreciation"])
    rate = random.choice([5, 8, 10, 12, 15, 20, 25])
    years = random.randint(2, 4)

    if kind == "depreciation":
        start = random.choice(range(2000, 15001, 500))
        multiplier = round(1 - rate / 100, 2)
        subject = random.choice(["A car", "A motorbike", "A piece of equipment"])
        verb = "depreciates"
    else:
        start = random.choice(range(50000, 250001, 5000))
        multiplier = round(1 + rate / 100, 2)
        subject = random.choice(["A house", "A flat", "A property"])
        verb = "appreciates"

    year_values = []
    value = start
    for _ in range(years):
        value = round(value * multiplier, 2)
        year_values.append(value)

    answer = year_values[-1]

    question_text = (
        f"{subject} is worth £{start:,}. "
        f"It {verb} at {rate}% per year. "
        f"What is it worth after {years} year{'s' if years > 1 else ''}?"
    )

    scaffold_steps = [
        {
            "prompt": "Calculate the multiplier",
            "answer": multiplier,
        }
    ]
    for y in range(years):
        scaffold_steps.append({
            "prompt": f"Find the value after year {y + 1}",
            "answer": year_values[y],
        })

    worked = [f"Multiplier = {multiplier}"]
    for y in range(years):
        prev = start if y == 0 else year_values[y - 1]
        worked.append(f"After year {y + 1}: £{prev:,.2f} × {multiplier} = £{year_values[y]:,.2f}")

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Finance and Statistics",
        question_type="Appreciation and Depreciation",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
