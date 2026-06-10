import random
from core.models.question_model import Question

NOTES = """
**Budgeting:**

- **Total expenditure** = sum of all expenses
- **Surplus** = Income − Total expenditure  *(income exceeds spending)*
- **Deficit** = Total expenditure − Income  *(spending exceeds income)*

**Tip:** Add up all expenses first, then subtract from income.
If the result is positive → surplus. If negative → deficit.
"""

_NAMES = ["Alex", "Jamie", "Sam", "Jordan", "Casey", "Morgan", "Riley", "Taylor"]

_EXPENSE_POOL = [
    ("Rent", 400, 900, 50),
    ("Food shopping", 150, 350, 10),
    ("Transport", 50, 200, 10),
    ("Phone bill", 20, 60, 5),
    ("Gym membership", 20, 60, 5),
    ("Electricity and gas", 60, 150, 10),
    ("Streaming subscriptions", 15, 40, 5),
    ("Clothing", 30, 100, 10),
    ("Internet", 25, 60, 5),
]


def generate_budgeting_question():
    name = random.choice(_NAMES)
    income = random.choice(range(1200, 2801, 50))

    num_expenses = random.randint(4, 5)
    selected = random.sample(_EXPENSE_POOL, num_expenses)

    expenses = {}
    for cat, lo, hi, step in selected:
        expenses[cat] = random.choice(range(lo, hi + 1, step))

    total_expenses = sum(expenses.values())
    net = income - total_expenses

    ask = random.choice(["total", "surplus_deficit"])

    expense_lines = "\n".join(f"- {cat}: £{val}" for cat, val in expenses.items())

    if ask == "total":
        question_text = (
            f"{name} earns £{income:,} per month. Their monthly expenses are:\n\n"
            f"{expense_lines}\n\n"
            f"Calculate {name}'s total monthly expenditure."
        )
        answer = total_expenses
        scaffold_steps = [
            {"prompt": "Add up all the listed expenses", "answer": total_expenses},
        ]
        worked = [
            f"Total = £{' + £'.join(str(v) for v in expenses.values())}",
            f"= £{total_expenses}",
        ]
    else:
        descriptor = "surplus" if net >= 0 else "deficit"
        question_text = (
            f"{name} earns £{income:,} per month. Their monthly expenses are:\n\n"
            f"{expense_lines}\n\n"
            f"Calculate {name}'s monthly {descriptor}."
        )
        answer = abs(net)
        scaffold_steps = [
            {"prompt": "Calculate total monthly expenditure", "answer": total_expenses},
            {"prompt": "Subtract expenditure from income (negative = deficit)", "answer": net},
        ]
        worked = [
            f"Total expenditure = £{total_expenses}",
            f"Income − Expenditure = £{income} − £{total_expenses} = £{net}",
            f"Monthly {descriptor} = £{abs(net)}",
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Finance",
        question_type="Budgeting",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
