import random
from core.models.question_model import Question

NOTES = """
**Loans — Flat Rate Interest:**

**Total interest** = P × R × T ÷ 100
- **P** = Principal (amount borrowed)
- **R** = Annual interest rate (%)
- **T** = Time (years)

**Total repaid** = Principal + Total interest

**Monthly repayment** = Total repaid ÷ number of months

**Example:** Borrow £2,400 at 8% per year for 2 years
- Total interest = 2400 × 8 × 2 ÷ 100 = **£384**
- Total repaid = £2,400 + £384 = **£2,784**
- Monthly repayment = £2,784 ÷ 24 = **£116**
"""


def generate_loans_question():
    principal = random.choice(range(500, 5001, 100))
    rate = random.choice([4, 5, 6, 8, 10, 12])
    years = random.randint(1, 4)
    months = years * 12

    total_interest = round(principal * rate * years / 100, 2)
    total_repaid = round(principal + total_interest, 2)
    monthly = round(total_repaid / months, 2)

    ask = random.choice(["monthly", "total_interest", "total_repaid"])

    if ask == "monthly":
        question_text = (
            f"A loan of £{principal:,} is taken out at a flat rate of {rate}% per year for "
            f"{years} year{'s' if years > 1 else ''}. "
            f"Calculate the monthly repayment."
        )
        answer = monthly
        scaffold_steps = [
            {"prompt": "Calculate the total interest (P × R × T ÷ 100)", "answer": total_interest},
            {"prompt": "Calculate the total amount repaid", "answer": total_repaid},
            {"prompt": f"Divide by {months} months to get the monthly repayment", "answer": monthly},
        ]
        worked = [
            "Total interest = P × R × T ÷ 100",
            f"= £{principal} × {rate} × {years} ÷ 100 = £{total_interest}",
            f"Total repaid = £{principal} + £{total_interest} = £{total_repaid}",
            f"Monthly repayment = £{total_repaid} ÷ {months} = £{monthly}",
        ]
    elif ask == "total_interest":
        question_text = (
            f"A loan of £{principal:,} is taken out at a flat rate of {rate}% per year for "
            f"{years} year{'s' if years > 1 else ''}. "
            f"Calculate the total interest charged."
        )
        answer = total_interest
        scaffold_steps = [
            {"prompt": "Calculate 1% of the principal", "answer": round(principal / 100, 2)},
            {"prompt": f"Multiply by {rate}% to get the annual interest", "answer": round(principal * rate / 100, 2)},
            {"prompt": f"Multiply by {years} year{'s' if years > 1 else ''} for total interest", "answer": total_interest},
        ]
        worked = [
            "Total interest = P × R × T ÷ 100",
            f"= £{principal} × {rate} × {years} ÷ 100 = £{total_interest}",
        ]
    else:
        question_text = (
            f"A loan of £{principal:,} is taken out at a flat rate of {rate}% per year for "
            f"{years} year{'s' if years > 1 else ''}. "
            f"Calculate the total amount repaid."
        )
        answer = total_repaid
        scaffold_steps = [
            {"prompt": "Calculate the total interest (P × R × T ÷ 100)", "answer": total_interest},
            {"prompt": "Add to the principal to find total repaid", "answer": total_repaid},
        ]
        worked = [
            "Total interest = P × R × T ÷ 100",
            f"= £{principal} × {rate} × {years} ÷ 100 = £{total_interest}",
            f"Total repaid = £{principal} + £{total_interest} = £{total_repaid}",
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Finance",
        question_type="Loans",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
