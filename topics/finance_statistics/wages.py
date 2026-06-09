import random
from core.models.question_model import Question

NOTES = """
**Wages — Overtime Pay:**

Workers are often paid a **basic hourly rate** for their contracted hours.
Any hours worked **above** the contracted hours are **overtime**.

**Overtime rates:**
- **Time and a half** = basic rate × 1.5
- **Double time** = basic rate × 2

**Calculating gross pay:**
1. Basic pay = basic rate × contracted hours
2. Overtime hours = hours worked − contracted hours
3. Overtime pay = overtime rate × overtime hours
4. **Gross pay = basic pay + overtime pay**

**Level 2 — Net Pay:**

Net pay = Gross pay − Income Tax − National Insurance − Pension
"""

_NAMES = [
    "Amy", "Callum", "Catriona", "Connor", "Douglas", "Eilidh",
    "Ewan", "Freya", "Hamish", "Isla", "Jamie", "Kirsty",
    "Laura", "Liam", "Megan", "Ross", "Stuart", "Siobhan",
]

_COMPANIES = [
    "McKay Marketplace", "Tesco", "Scotmid", "Morrison's", "Asda",
    "B&Q", "Argos", "Next", "Sports Direct", "Primark",
    "Greggs", "Costa Coffee", "McDonald's", "Subway", "Boots",
]

_WORKPLACES = [
    "a shop", "a supermarket", "a hotel", "a restaurant", "a café",
    "a factory", "a warehouse", "a call centre", "a bakery", "a garage",
]

_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

_CONTRACTED_HOURS = [35, 37, 37.5, 40]
_BASIC_RATES = [10.60, 11.00, 11.44, 12.00, 12.50, 13.00, 14.00, 15.00]
_OVERTIME_HOURS_L1 = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
_OVERTIME_TYPES = ["time and a half", "double time"]

_L2_BASIC_HOURS = [80, 100, 120, 140, 160]
_L2_OT_HOURS = [10, 15, 20, 25, 30]


def _fmt_hrs(h):
    return int(h) if h == int(h) else h


def _round_to_half(x):
    return round(round(x * 2) / 2, 2)


# ---------------------------------------------------------------------------
# Level 1 — gross pay with overtime
# ---------------------------------------------------------------------------

def generate_wages_l1():
    name = random.choice(_NAMES)
    company = random.choice(_COMPANIES)
    contracted = random.choice(_CONTRACTED_HOURS)
    basic_rate = random.choice(_BASIC_RATES)
    ot_hours = random.choice(_OVERTIME_HOURS_L1)
    total_hours = contracted + ot_hours
    ot_type = random.choice(_OVERTIME_TYPES)

    if ot_type == "time and a half":
        ot_rate = round(basic_rate * 1.5, 2)
        ot_multiplier = "1.5"
    else:
        ot_rate = round(basic_rate * 2, 2)
        ot_multiplier = "2"

    basic_pay = round(basic_rate * contracted, 2)
    ot_pay = round(ot_rate * ot_hours, 2)
    gross_pay = round(basic_pay + ot_pay, 2)

    question_text = (
        f"{name} works for {company}.\n\n"
        f"- {name} is contracted to work {_fmt_hrs(contracted)} hours each week.\n"
        f"- {name}'s basic hourly rate of pay is £{basic_rate:.2f}.\n"
        f"- {name} is paid **{ot_type}** for any overtime.\n"
        f"- Last week {name} worked {_fmt_hrs(total_hours)} hours.\n\n"
        f"Calculate {name}'s gross pay for last week."
    )

    scaffold_steps = [
        {
            "prompt": f"Calculate {name}'s basic pay ({_fmt_hrs(contracted)} hours at £{basic_rate:.2f} per hour).",
            "answer": basic_pay,
        },
        {
            "prompt": f"How many overtime hours did {name} work?",
            "answer": float(ot_hours),
        },
        {
            "prompt": f"Calculate the overtime rate of pay ({ot_type} = basic rate × {ot_multiplier}).",
            "answer": ot_rate,
        },
        {
            "prompt": f"Calculate {name}'s overtime pay ({_fmt_hrs(ot_hours)} hours at £{ot_rate:.2f} per hour).",
            "answer": ot_pay,
        },
        {
            "prompt": "Calculate gross pay (basic pay + overtime pay).",
            "answer": gross_pay,
        },
    ]

    worked = [
        f"Basic pay = £{basic_rate:.2f} × {_fmt_hrs(contracted)} = £{basic_pay:.2f}",
        f"Overtime hours = {_fmt_hrs(total_hours)} − {_fmt_hrs(contracted)} = {_fmt_hrs(ot_hours)} hours",
        f"Overtime rate = £{basic_rate:.2f} × {ot_multiplier} = £{ot_rate:.2f} per hour",
        f"Overtime pay = £{ot_rate:.2f} × {_fmt_hrs(ot_hours)} = £{ot_pay:.2f}",
        f"Gross pay = £{basic_pay:.2f} + £{ot_pay:.2f} = £{gross_pay:.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=gross_pay,
        topic="Finance and Statistics",
        question_type="Wages (Level 1)",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 2 — net pay after deductions
# ---------------------------------------------------------------------------

def generate_wages_l2():
    name = random.choice(_NAMES)
    workplace = random.choice(_WORKPLACES)
    month = random.choice(_MONTHS)
    basic_rate = random.choice(_BASIC_RATES)
    basic_hours = random.choice(_L2_BASIC_HOURS)
    ot_hours = random.choice(_L2_OT_HOURS)
    ot_type = random.choice(_OVERTIME_TYPES)

    if ot_type == "time and a half":
        ot_rate = round(basic_rate * 1.5, 2)
        ot_multiplier = "1.5"
    else:
        ot_rate = round(basic_rate * 2, 2)
        ot_multiplier = "2"

    basic_pay = round(basic_rate * basic_hours, 2)
    ot_pay = round(ot_rate * ot_hours, 2)
    gross_pay = round(basic_pay + ot_pay, 2)

    # Generate deductions as rounded-to-nearest-£0.50 amounts
    tax = _round_to_half(gross_pay * random.uniform(0.12, 0.18))
    ni = _round_to_half(gross_pay * random.uniform(0.06, 0.10))
    pension = _round_to_half(gross_pay * random.uniform(0.03, 0.06))

    total_deductions = round(tax + ni + pension, 2)
    net_pay = round(gross_pay - total_deductions, 2)

    question_text = (
        f"{name} works in {workplace}.\n\n"
        f"- {name} earns £{basic_rate:.2f} per hour.\n"
        f"- {name} gets paid overtime at {ot_type}.\n"
        f"- In {month} {name} worked {_fmt_hrs(basic_hours)} hours basic "
        f"plus {_fmt_hrs(ot_hours)} hours overtime.\n"
        f"- In {month} {name} paid £{tax:.2f} in income tax, "
        f"£{ni:.2f} in National Insurance "
        f"and £{pension:.2f} towards their pension.\n\n"
        f"Calculate {name}'s net pay for {month}."
    )

    scaffold_steps = [
        {
            "prompt": f"Calculate {name}'s basic pay ({_fmt_hrs(basic_hours)} hours at £{basic_rate:.2f} per hour).",
            "answer": basic_pay,
        },
        {
            "prompt": f"Calculate the overtime rate of pay ({ot_type} = basic rate × {ot_multiplier}).",
            "answer": ot_rate,
        },
        {
            "prompt": f"Calculate {name}'s overtime pay ({_fmt_hrs(ot_hours)} hours at £{ot_rate:.2f} per hour).",
            "answer": ot_pay,
        },
        {
            "prompt": "Calculate gross pay (basic pay + overtime pay).",
            "answer": gross_pay,
        },
        {
            "prompt": "Calculate total deductions (income tax + National Insurance + pension).",
            "answer": total_deductions,
        },
        {
            "prompt": "Calculate net pay (gross pay − total deductions).",
            "answer": net_pay,
        },
    ]

    worked = [
        f"Basic pay = £{basic_rate:.2f} × {_fmt_hrs(basic_hours)} = £{basic_pay:.2f}",
        f"Overtime rate = £{basic_rate:.2f} × {ot_multiplier} = £{ot_rate:.2f} per hour",
        f"Overtime pay = £{ot_rate:.2f} × {_fmt_hrs(ot_hours)} = £{ot_pay:.2f}",
        f"Gross pay = £{basic_pay:.2f} + £{ot_pay:.2f} = £{gross_pay:.2f}",
        f"Total deductions = £{tax:.2f} + £{ni:.2f} + £{pension:.2f} = £{total_deductions:.2f}",
        f"Net pay = £{gross_pay:.2f} − £{total_deductions:.2f} = £{net_pay:.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=net_pay,
        topic="Finance and Statistics",
        question_type="Wages (Level 2)",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Dispatchers
# ---------------------------------------------------------------------------

def generate_wages_question():
    return random.choice([generate_wages_l1, generate_wages_l2])()
