import random
from core.models.question_model import Question

NOTES = """
**Simple Interest:**

**Formula:** I = P × R × T ÷ 100

- **P** = Principal (starting amount)
- **R** = Rate (% per year)
- **T** = Time (years)

**Example:** £500 at 3% for 4 years
- I = 500 × 3 × 4 ÷ 100 = **£60**
- Total = 500 + 60 = **£560**
"""


def generate_simple_interest_question_n4():
    principal = random.choice(range(100, 501, 50))
    rate = random.choice([2, 3, 5, 10])
    years = random.randint(1, 3)

    yearly_interest = round(principal * rate / 100, 2)
    total_interest = round(yearly_interest * years, 2)

    question_text = (
        f"Calculate the simple interest on £{principal:,} at {rate}% per year for {years} year{'s' if years > 1 else ''}."
    )

    worked = [
        f"I = P × R × T ÷ 100",
        f"I = {principal} × {rate} × {years} ÷ 100 = £{total_interest}",
    ]

    scaffold_steps = [
        {"prompt": "Find 1% of the principal", "answer": round(principal / 100, 2)},
        {"prompt": "Find the annual interest", "answer": yearly_interest},
        {"prompt": "Find the total interest over all years", "answer": total_interest},
    ]

    return Question(
        question_text=question_text,
        correct_answer=total_interest,
        topic="Finance and Statistics",
        question_type="Simple Interest",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_simple_interest_question():
    principal = random.choice(range(200, 2001, 50))
    rate = random.choice([2, 3, 4, 5, 6, 7, 8, 10])
    years = random.randint(2, 6)

    yearly_interest = round(principal * rate / 100, 2)
    total_interest = round(yearly_interest * years, 2)
    total = round(principal + total_interest, 2)

    ask_total = random.choice([True, False])

    if ask_total:
        question_text = (
            f"£{principal:,} is invested at {rate}% per year simple interest for {years} years. "
            f"What is the total amount after {years} years?"
        )
        answer = total
        worked = [
            f"I = P × R × T ÷ 100",
            f"I = {principal} × {rate} × {years} ÷ 100 = £{total_interest}",
            f"Total = £{principal} + £{total_interest} = £{total}",
        ]
        scaffold_steps = [
            {"prompt": "Find 1% of the principal", "answer": round(principal / 100, 2)},
            {"prompt": "Find the annual interest", "answer": yearly_interest},
            {"prompt": "Find the total interest over all years", "answer": total_interest},
            {"prompt": "Add the total interest to the principal", "answer": total},
        ]
    else:
        question_text = (
            f"Calculate the simple interest on £{principal:,} at {rate}% per year for {years} years."
        )
        answer = total_interest
        worked = [
            f"I = P × R × T ÷ 100",
            f"I = {principal} × {rate} × {years} ÷ 100 = £{total_interest}",
        ]
        scaffold_steps = [
            {"prompt": "Find 1% of the principal", "answer": round(principal / 100, 2)},
            {"prompt": "Find the annual interest", "answer": yearly_interest},
            {"prompt": "Find the total interest over all years", "answer": total_interest},
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Finance and Statistics",
        question_type="Simple Interest",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
