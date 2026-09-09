import random
from core.models.question_model import Question

# Scottish income tax bands, 2025/26 (annual). Fixed real-world values — unlike National
# Insurance below (and N5's own National Insurance topic), this isn't randomised per question,
# since it's the actual published band table pupils are given on the worksheet.
_TAX_BANDS_ANNUAL = [
    ("Personal Allowance", 0, 12_570, 0),
    ("Starter rate", 12_570, 15_397, 19),
    ("Basic rate", 15_397, 27_491, 20),
    ("Intermediate rate", 27_491, 43_662, 21),
    ("Higher rate", 43_662, 75_000, 42),
    ("Advanced rate", 75_000, 125_140, 45),
    ("Top rate", 125_140, None, 48),
]
_TAX_MAX_INCOME = 160_000

# National Insurance, 2025/26 (monthly, employee Class 1).
_NI_BANDS_MONTHLY = [
    ("0%", 0, 1_048, 0),
    ("8%", 1_048, 4_189, 8),
    ("2%", 4_189, None, 2),
]
_NI_MAX_INCOME = 6_500

_NAMES = [
    "Ailsa", "Iain", "Ceit", "Anna", "Dòmhnall", "Ishbel", "Ruaridh", "Catrìona",
    "Aonghas", "Màiri", "Tormod", "Alasdair", "Fionnlagh", "Seonaid", "Mòrag",
    "Eilidh", "Callum", "Fraser", "Rhona", "Coinneach",
]

_NOTES_GROSS_PAY = """
**Calculating Gross Annual Pay:**

Assume 52 weeks in a year. When you're only given a rate for a short period (an hour or a
day), work up one step at a time — day, then week, then year. Skipping a step is the easiest
way to lose marks.

**Example:** Paid £13.60 per hour, 7.5 hours per day, 5 days per week.
- Daily pay = £13.60 × 7.5 = £102.00
- Weekly pay = £102.00 × 5 = £510.00
- Gross annual salary = £510.00 × 52 = **£26,520.00**
"""

_NOTES_INCOME_TAX = """
**Calculating Income Tax (Scottish bands, 2025/26):**

| Band | Taxable income | Rate |
|---|---|---|
| Personal Allowance | Up to £12,570 | 0% |
| Starter rate | £12,570 – £15,397 | 19% |
| Basic rate | £15,397 – £27,491 | 20% |
| Intermediate rate | £27,491 – £43,662 | 21% |
| Higher rate | £43,662 – £75,000 | 42% |
| Advanced rate | £75,000 – £125,140 | 45% |
| Top rate | Over £125,140 | 48% |

Keep subtracting each band's lower limit from its upper limit to find how much falls in that
band — the same pattern continues for as many bands as the salary reaches. Only the final,
highest band uses the person's actual salary instead of the band's own upper limit.

**Example:** Gross annual salary £48,000.
- Personal Allowance: £12,570 taxed at 0% = £0
- Starter rate: £15,397 − £12,570 = £2,827 taxed at 19% = £537.13
- Basic rate: £27,491 − £15,397 = £12,094 taxed at 20% = £2,418.80
- Intermediate rate: £43,662 − £27,491 = £16,171 taxed at 21% = £3,395.91
- Higher rate: £48,000 − £43,662 = £4,338 taxed at 42% = £1,821.96
- **Total tax = £537.13 + £2,418.80 + £3,395.91 + £1,821.96 = £8,173.80**
"""

_NOTES_NI = """
**Calculating National Insurance (2025/26):**

You begin paying National Insurance once you earn more than £1,048 a month. Between £1,048
and £4,189 a month, you pay 8%; above £4,189, you pay 2% on the amount above £4,189.
National Insurance is calculated on gross salary, before deductions such as pension
contributions.

Always check whether the monthly salary goes above £4,189. If it doesn't, only the 8% rate
applies — but if it does, only the amount above £4,189 is charged at 2%, not the full amount.

**Example:** Gross monthly salary £4,800.
- 8% band: £4,189 − £1,048 = £3,141 at 8% = £251.28
- 2% band: £4,800 − £4,189 = £611 at 2% = £12.22
- **Total National Insurance = £251.28 + £12.22 = £263.50**
"""

_NOTES_NET_PAY = """
**Calculating Net Monthly Income:**

Net monthly income = gross monthly salary − pension − income tax − National Insurance.

Pension comes off **before** tax is worked out (it reduces the taxable income), but National
Insurance is worked out on the salary **before** the pension is deducted. Mixing up which
figure to use for which deduction is the most common mistake.
"""

# The reference sheet pupils are given alongside these questions (tax bands + NI rules, with
# no worked example) — shown directly above the question itself for any level that involves
# income tax and/or National Insurance, i.e. every level here except Gross Annual Pay.
_REFERENCE_SHEET = """
**Scottish tax bands 2025/26**

| Band | Taxable income | Scottish tax rate |
|---|---|---|
| Personal Allowance | Up to £12,570 | 0% |
| Starter rate | £12,570 – £15,397 | 19% |
| Basic rate | £15,397 – £27,491 | 20% |
| Intermediate rate | £27,491 – £43,662 | 21% |
| Higher rate | £43,662 – £75,000 | 42% |
| Advanced rate | £75,000 – £125,140 | 45% |
| Top rate | Over £125,140 | 48% |

**National Insurance contributions**

You begin paying National Insurance once you earn more than £1,048 a month (this is the amount
for the 2025/26 tax year).

For payslips dated between 6 April 2025 and 5 April 2026, you pay 8% of your monthly earnings
between £1,048 and £4,189; 2% of your monthly earnings above £4,189.

National Insurance is calculated on a person's salary **before deductions** such as pension
contributions.
"""


def _r2(v):
    return round(float(v), 2)


def _banded_calc(amount, bands):
    """Total charge over a set of contiguous bands, plus a breakdown of each band actually
    reached: list of (label, lower, portion_upper, taxable, rate, amount_charged)."""
    breakdown = []
    total = 0.0
    for label, lower, upper, rate in bands:
        if amount <= lower:
            break
        portion_upper = amount if upper is None else min(amount, upper)
        taxable = portion_upper - lower
        amt = taxable * rate / 100
        breakdown.append((label, lower, portion_upper, taxable, rate, amt))
        total += amt
        if upper is not None and amount <= upper:
            break
    return _r2(total), breakdown


def _bands_metadata(bands, max_income, initial_income):
    return {
        "diagram": "tax_bands",
        "diagram_params": {
            "bands": bands,
            "max_income": max_income,
            "initial_income": initial_income,
        },
    }


# ── Gross Annual Pay ─────────────────────────────────────────────────────────

def _gap_hourly_weekly():
    name = random.choice(_NAMES)
    rate = round(random.uniform(9.5, 22.0), 2)
    hours = random.choice(range(15, 41))
    weekly = _r2(rate * hours)
    annual = _r2(weekly * 52)

    question_text = f"{name} is paid £{rate:.2f} per hour. {name} works {hours} hours per week. Calculate {name}'s gross annual salary."
    scaffold_steps = [
        {"prompt": "Weekly pay = hourly rate × hours worked per week", "answer": weekly},
        {"prompt": "Gross annual salary = weekly pay × 52", "answer": annual},
    ]
    worked = [
        f"Weekly pay: £{rate:.2f} × {hours} = £{weekly:.2f}",
        f"Gross annual salary = £{weekly:.2f} × 52 = £{annual:.2f}",
    ]
    return question_text, annual, scaffold_steps, worked


def _gap_weekly_wage():
    name = random.choice(_NAMES)
    weekly = random.choice(range(280, 900, 4))
    annual = _r2(weekly * 52)

    question_text = f"{name} is paid a weekly wage of £{weekly}. Calculate {name}'s gross annual salary."
    worked = [f"Gross annual salary = £{weekly} × 52 = £{annual:.2f}"]
    return question_text, annual, [], worked


def _gap_hourly_daily_weekly():
    name = random.choice(_NAMES)
    rate = round(random.uniform(9.5, 22.0), 2)
    hours_per_day = random.choice([4, 5, 6, 7, 7.5, 8])
    days_per_week = random.choice([3, 4, 5])
    daily = _r2(rate * hours_per_day)
    weekly = _r2(daily * days_per_week)
    annual = _r2(weekly * 52)

    question_text = (
        f"{name} is paid £{rate:.2f} per hour. {name} works {hours_per_day} hours per day, "
        f"{days_per_week} days per week. Calculate {name}'s gross annual salary."
    )
    scaffold_steps = [
        {"prompt": "Daily pay = hourly rate × hours worked per day", "answer": daily},
        {"prompt": "Weekly pay = daily pay × days worked per week", "answer": weekly},
        {"prompt": "Gross annual salary = weekly pay × 52", "answer": annual},
    ]
    worked = [
        f"Daily pay: £{rate:.2f} × {hours_per_day} = £{daily:.2f}",
        f"Weekly pay: £{daily:.2f} × {days_per_week} = £{weekly:.2f}",
        f"Gross annual salary = £{weekly:.2f} × 52 = £{annual:.2f}",
    ]
    return question_text, annual, scaffold_steps, worked


def generate_gross_annual_pay(level="Higher"):
    question_text, annual, scaffold_steps, worked = random.choice([
        _gap_hourly_weekly, _gap_weekly_wage, _gap_hourly_daily_weekly,
    ])()
    return Question(
        question_text=question_text,
        correct_answer=annual,
        topic="Finance",
        question_type="Income Tax and National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_NOTES_GROSS_PAY,
    )


# ── Income Tax ────────────────────────────────────────────────────────────────

def generate_income_tax(level="Higher"):
    name = random.choice(_NAMES)
    salary = random.choice(range(13_000, 145_000, 250))
    tax, breakdown = _banded_calc(salary, _TAX_BANDS_ANNUAL)

    question_text = f"{name}'s gross annual salary is £{salary:,}. Calculate the total income tax {name} pays in a year."

    scaffold_steps = []
    worked = []
    for label, lower, upper, taxable, rate, amt in breakdown:
        scaffold_steps.append({
            "prompt": f"{label}: tax on the amount of salary in this band at {rate}%",
            "answer": _r2(amt),
        })
        if rate == 0:
            worked.append(f"{label}: £{taxable:,.2f} taxed at 0% = £0.00")
        else:
            worked.append(f"{label}: £{upper:,.2f} − £{lower:,.2f} = £{taxable:,.2f} taxed at {rate}% = £{amt:,.2f}")
    scaffold_steps.append({"prompt": "Total tax = sum of all bands above", "answer": tax})
    worked.append("Total tax = " + " + ".join(f"£{b[5]:,.2f}" for b in breakdown) + f" = £{tax:,.2f}")

    return Question(
        question_text=question_text,
        correct_answer=tax,
        topic="Finance",
        question_type="Income Tax and National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_NOTES_INCOME_TAX,
        metadata={**_bands_metadata(_TAX_BANDS_ANNUAL, _TAX_MAX_INCOME, salary), "reference_sheet": _REFERENCE_SHEET},
    )


# ── National Insurance ────────────────────────────────────────────────────────

def generate_higher_ni(level="Higher"):
    name = random.choice(_NAMES)
    salary = random.choice(range(1_100, 6_200, 20))
    ni, breakdown = _banded_calc(salary, _NI_BANDS_MONTHLY)

    question_text = f"{name} earns £{salary:,} per month. Calculate how much National Insurance {name} pays in a month."

    scaffold_steps = []
    worked = []
    for label, lower, upper, taxable, rate, amt in breakdown:
        if rate == 0:
            continue
        scaffold_steps.append({
            "prompt": f"{label} band: the amount of salary in this band at {rate}%",
            "answer": _r2(amt),
        })
        worked.append(f"{rate}% band: £{upper:,.2f} − £{lower:,.2f} = £{taxable:,.2f} at {rate}% = £{amt:,.2f}")
    if len(scaffold_steps) > 1:
        scaffold_steps.append({"prompt": "Total National Insurance = sum of both bands above", "answer": ni})
    worked.append("Total National Insurance = " + " + ".join(f"£{b[5]:,.2f}" for b in breakdown if b[4] > 0) + f" = £{ni:,.2f}")

    return Question(
        question_text=question_text,
        correct_answer=ni,
        topic="Finance",
        question_type="Income Tax and National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_NOTES_NI,
        metadata={**_bands_metadata(_NI_BANDS_MONTHLY, _NI_MAX_INCOME, salary), "reference_sheet": _REFERENCE_SHEET},
    )


# ── Net Monthly Income ────────────────────────────────────────────────────────

def generate_net_monthly_income(level="Higher"):
    name = random.choice(_NAMES)
    annual_salary = random.choice(range(20_000, 70_000, 200))
    pension_pct = random.choice([2, 3, 4, 5, 6])
    give_ni = random.choice([True, False])

    annual_pension = _r2(annual_salary * pension_pct / 100)
    monthly_pension = _r2(annual_pension / 12)
    taxable_income = _r2(annual_salary - annual_pension)
    annual_tax, tax_breakdown = _banded_calc(taxable_income, _TAX_BANDS_ANNUAL)
    monthly_tax = _r2(annual_tax / 12)

    monthly_gross = _r2(annual_salary / 12)
    ni, ni_breakdown = _banded_calc(monthly_gross, _NI_BANDS_MONTHLY)

    net_monthly = _r2(monthly_gross - monthly_pension - monthly_tax - ni)

    if give_ni:
        question_text = (
            f"{name}'s gross annual salary is £{annual_salary:,}.\n\n"
            f"{name} contributes {pension_pct}% of their salary before tax into their pension fund.\n\n"
            f"{name} pays £{ni:,.2f} in National Insurance each month.\n\n"
            f"Calculate {name}'s net monthly income."
        )
    else:
        question_text = (
            f"{name}'s gross annual salary is £{annual_salary:,}.\n\n"
            f"{name} contributes {pension_pct}% of their salary before tax into their pension fund.\n\n"
            f"Calculate {name}'s net monthly income."
        )

    scaffold_steps = [
        {"prompt": "Monthly pension = pension percentage of annual salary ÷ 12", "answer": monthly_pension},
        {"prompt": "Taxable income = annual salary − annual pension", "answer": taxable_income},
        {"prompt": "Total income tax for the year (using the tax bands)", "answer": annual_tax},
        {"prompt": "Monthly income tax = annual tax ÷ 12", "answer": monthly_tax},
    ]
    if not give_ni:
        scaffold_steps.append(
            {"prompt": "Monthly National Insurance (on gross monthly salary, before pension)",
             "answer": ni}
        )
    scaffold_steps.append({
        "prompt": "Net monthly income = gross monthly salary − pension − tax − National Insurance",
        "answer": net_monthly,
    })

    worked = [
        f"Pension: {pension_pct}% of £{annual_salary:,} = £{annual_pension:,.2f} a year = £{monthly_pension:,.2f} a month",
        f"Taxable income: £{annual_salary:,} − £{annual_pension:,.2f} = £{taxable_income:,.2f}",
    ]
    for label, lower, upper, taxable, rate, amt in tax_breakdown:
        worked.append(f"{label}: £{taxable:,.2f} at {rate}% = £{amt:,.2f}")
    worked.append(f"Total tax = £{annual_tax:,.2f} a year = £{monthly_tax:,.2f} a month")
    if not give_ni:
        worked.append(
            f"National Insurance (on gross monthly salary of £{monthly_gross:,.2f}, before pension): £{ni:,.2f}"
        )
    worked.append(
        f"Net monthly income = £{monthly_gross:,.2f} − £{monthly_pension:,.2f} − £{monthly_tax:,.2f} "
        f"− £{ni:,.2f} = £{net_monthly:,.2f}"
    )

    return Question(
        question_text=question_text,
        correct_answer=net_monthly,
        topic="Finance",
        question_type="Income Tax and National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_NOTES_NET_PAY,
        metadata={**_bands_metadata(_TAX_BANDS_ANNUAL, _TAX_MAX_INCOME, taxable_income), "reference_sheet": _REFERENCE_SHEET},
    )


# ── Default dispatcher ────────────────────────────────────────────────────────

def generate_tax_ni_question(level="Higher"):
    return random.choice([
        generate_gross_annual_pay, generate_income_tax, generate_higher_ni, generate_net_monthly_income,
    ])(level=level)
