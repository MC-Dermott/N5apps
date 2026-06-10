import random
from core.models.question_model import Question

NOTES = """
**Mortgages:**

A mortgage is a loan used to buy property.

1. **Deposit** = House price × deposit %
2. **Mortgage** = House price − Deposit
3. **Total interest** = Mortgage × R × T ÷ 100
4. **Total repaid** = Mortgage + Total interest
5. **Monthly repayment** = Total repaid ÷ number of months

**Example:** House costs £180,000. 10% deposit. Mortgage at 4% for 25 years.
- Deposit = £180,000 × 10% = **£18,000**
- Mortgage = £180,000 − £18,000 = **£162,000**
- Total interest = £162,000 × 4 × 25 ÷ 100 = **£162,000**
- Total repaid = £162,000 + £162,000 = **£324,000**
- Monthly repayment = £324,000 ÷ 300 = **£1,080**
"""

_NAMES = ["Alex", "Jamie", "Sam", "Jordan", "Casey", "Morgan", "Riley", "Taylor"]


def generate_mortgages_question():
    name = random.choice(_NAMES)
    house_price = random.choice(range(100_000, 350_001, 5_000))
    deposit_pct = random.choice([5, 10, 15, 20])
    rate = random.choice([2, 3, 4, 5])
    years = random.choice([20, 25, 30])
    months = years * 12

    deposit = round(house_price * deposit_pct / 100, 2)
    mortgage = house_price - deposit
    total_interest = round(mortgage * rate * years / 100, 2)
    total_repaid = round(mortgage + total_interest, 2)
    monthly = round(total_repaid / months, 2)

    ask = random.choice(["deposit", "monthly", "total_interest"])

    base = (
        f"{name} buys a house for £{house_price:,}. "
        f"They put down a {deposit_pct}% deposit and take out a mortgage at a flat rate of "
        f"{rate}% per year over {years} years."
    )

    if ask == "deposit":
        question_text = f"{base} Calculate the deposit {name} must pay."
        answer = deposit
        scaffold_steps = [
            {"prompt": f"Find {deposit_pct}% of £{house_price:,}", "answer": deposit},
        ]
        worked = [
            f"Deposit = £{house_price:,} × {deposit_pct} ÷ 100 = £{deposit:,.2f}",
        ]
    elif ask == "monthly":
        question_text = f"{base} Calculate {name}'s monthly repayment."
        answer = monthly
        scaffold_steps = [
            {"prompt": f"Calculate the deposit ({deposit_pct}% of £{house_price:,})", "answer": deposit},
            {"prompt": "Calculate the mortgage (house price − deposit)", "answer": mortgage},
            {"prompt": "Calculate the total interest (mortgage × R × T ÷ 100)", "answer": total_interest},
            {"prompt": "Calculate the total amount repaid", "answer": total_repaid},
            {"prompt": f"Divide by {months} months", "answer": monthly},
        ]
        worked = [
            f"Deposit = £{house_price:,} × {deposit_pct} ÷ 100 = £{deposit:,.2f}",
            f"Mortgage = £{house_price:,} − £{deposit:,.2f} = £{mortgage:,.2f}",
            f"Total interest = £{mortgage:,.2f} × {rate} × {years} ÷ 100 = £{total_interest:,.2f}",
            f"Total repaid = £{mortgage:,.2f} + £{total_interest:,.2f} = £{total_repaid:,.2f}",
            f"Monthly repayment = £{total_repaid:,.2f} ÷ {months} = £{monthly:,.2f}",
        ]
    else:
        question_text = f"{base} Calculate the total interest {name} will pay."
        answer = total_interest
        scaffold_steps = [
            {"prompt": f"Calculate the deposit ({deposit_pct}% of £{house_price:,})", "answer": deposit},
            {"prompt": "Calculate the mortgage (house price − deposit)", "answer": mortgage},
            {"prompt": "Calculate the total interest (mortgage × R × T ÷ 100)", "answer": total_interest},
        ]
        worked = [
            f"Deposit = £{house_price:,} × {deposit_pct} ÷ 100 = £{deposit:,.2f}",
            f"Mortgage = £{house_price:,} − £{deposit:,.2f} = £{mortgage:,.2f}",
            f"Total interest = £{mortgage:,.2f} × {rate} × {years} ÷ 100 = £{total_interest:,.2f}",
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Finance",
        question_type="Mortgages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
