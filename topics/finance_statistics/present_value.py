"""Higher Finance — Present Value.

Mirrors Present_Value_Worksheet.docx (Higher Apps/Worksheets/Finance). Minimum deposits through changing
rates are the existing "Interest" type (Minimum Deposit for a Goal). Traps from the marking instructions:
taking the rate off each year (× 0.929^3, 2026 Q10 Candidate A), forgetting the power (Candidate B),
subtracting instead of discounting (2023 course report), rounding a goal deposit down.
"""
import math
import random

from core.models.question_model import Question

TOPIC = "Finance"
QTYPE = "Present Value"
_NAMES = ["Anna", "Deirdre", "Iain", "Mairi", "Donald", "Katie", "Ruaridh", "Seonag", "Ewan", "Kirsty"]

NOTES = """
**Present value**

The present value is the amount needed **now** to reach a future amount. Divide by the multiplier:

**PV = future amount ÷ (1 + r)^n**   (n in years for an annual rate; months ÷ 12 for part-years)

**Example:** Anna must pay £8200 in 3 years' time. She will make a single deposit now into an account with an annual
effective rate of 6.8%. Calculate the minimum amount she must deposit.

- deposit × 1.068^3 = 8200
- Present value = 8200 ÷ 1.068^3 = 6731.3237…
- Round **UP** (rounding down would leave her just short): **£6731.33**

⚠ Don't multiply by 0.932^3 (taking 6.8% off each year) and don't forget the power (2026 marking instructions).

- **A series of payments:** discount each payment from its own date and add them.
- **Finding the rate:** (1 + r)^n = later ÷ earlier, so r = (later ÷ earlier)^(1/n) − 1 — not total growth ÷ years.
"""


def _up(x):
    return math.ceil(round(x * 100, 6)) / 100


_GOALS = [("a van's final lump-sum payment", 5000, 12000), ("a wedding", 6000, 20000), ("a boat engine", 3000, 9000),
          ("university costs", 8000, 25000), ("a new roof", 7000, 18000)]


def generate_present_value_l1():
    name = random.choice(_NAMES); what, lo, hi = random.choice(_GOALS)
    FV = random.randrange(lo, hi + 1, 25); r = round(random.uniform(2.5, 7.5), 1); n = random.randint(2, 6)
    pv = FV / (1 + r / 100) ** n; ans = _up(pv)
    q = (f"{name} needs £{FV:,} for {what} in {n} years' time. They will make a single deposit now into an account with an "
         f"annual effective rate of interest of {r}%.\n\nCalculate the minimum amount they must deposit.")
    return Question(question_text=q, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": f"What is the multiplier for {n} years, (1 + r)^{n}? (5 d.p.)",
                                     "answer": round((1 + r / 100) ** n, 5)}],
                    worked_solution=[f"PV = {FV:,} ÷ {1 + r / 100:g}^{n} = {pv:.4f}…", f"Round up: £{ans:,.2f}",
                                     f"(Not {FV:,} × {1 - r / 100:g}^{n} — that takes {r}% off each year.)"],
                    notes=NOTES)


def generate_present_value_l2():
    """Level payments at the end of each year, possibly deferred."""
    P = random.randrange(800, 3001, 100); r = round(random.uniform(2.5, 5.5), 1)
    start = random.choice([1, 1, 2, 3]); k = random.randint(3, 4)
    years = list(range(start, start + k))
    pv = sum(P / (1 + r / 100) ** y for y in years)
    defer = "" if start == 1 else f" (nothing is paid in years 1{'–' + str(start - 1) if start > 2 else ''})"
    q = (f"A fund must pay £{P:,} at the end of years {', '.join(map(str, years[:-1]))} and {years[-1]}{defer}. The fund earns an "
         f"annual effective rate of {r}%.\n\nCalculate the amount needed in the fund now.")
    return Question(question_text=q, correct_answer=round(pv, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": f"Present value of the payment at the end of year {years[0]} (£)",
                                     "answer": round(P / (1 + r / 100) ** years[0], 2)}],
                    worked_solution=[" + ".join(f"{P:,} ÷ {1 + r / 100:g}^{y}" for y in years) + f" = £{pv:,.2f}"],
                    notes=NOTES)


def generate_present_value_l3():
    """Payments growing by a fixed amount or a fixed percentage."""
    r = round(random.uniform(3.0, 6.0), 1); first = random.randrange(1000, 3001, 100)
    if random.random() < 0.5:
        step = random.choice([100, 150, 200, 250]); pays = [first + step * j for j in range(3)]
        how = f"rising by £{step} each year"
    else:
        g = random.choice([2, 3, 4, 5]); pays = [round(first * (1 + g / 100) ** j, 2) for j in range(3)]
        how = f"rising by {g}% each year"
    pv = sum(p / (1 + r / 100) ** (j + 1) for j, p in enumerate(pays))
    q = (f"A fund must make payments at the end of each of the next 3 years, starting at £{first:,} and {how}. The fund earns an "
         f"annual effective rate of {r}%.\n\nCalculate the amount needed in the fund now.")
    return Question(question_text=q, correct_answer=round(pv, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Payment at the end of year 3 (£)", "answer": round(pays[2], 2)}],
                    worked_solution=[" + ".join(f"{p:,.2f} ÷ {1 + r / 100:g}^{j + 1}" for j, p in enumerate(pays)) + f" = £{pv:,.2f}"],
                    notes=NOTES)


def generate_present_value_l4():
    """Finding the rate from an earlier and a later value."""
    a0 = random.randrange(1000, 8001, 100); r = round(random.uniform(1.5, 6.5), 2)
    if random.random() < 0.6:
        n = random.randint(2, 6); a1 = round(a0 * (1 + r / 100) ** n); per = "year"; unit = f"{n} years"
    else:
        n = random.randint(6, 18); rm = r / 12; a1 = round(a0 * (1 + rm / 100) ** n); per = "month"; unit = f"{n} months"
    rate = ((a1 / a0) ** (1 / n) - 1) * 100
    q = (f"£{a0:,} grew to £{a1:,} in {unit} in an account with a fixed effective rate of interest.\n\n"
         f"Calculate the {per}ly effective rate of interest, as a percentage to 2 decimal places.")
    return Question(question_text=q, correct_answer=round(rate, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "later ÷ earlier (5 d.p.)", "answer": round(a1 / a0, 5)}],
                    worked_solution=[f"(1 + r)^{n} = {a1:,} ÷ {a0:,} = {a1 / a0:.5f}",
                                     f"r = {a1 / a0:.5f}^(1/{n}) − 1 = {rate:.2f}% per {per}"],
                    notes=NOTES)


def generate_present_value_question():
    return random.choice([generate_present_value_l1, generate_present_value_l2, generate_present_value_l3,
                          generate_present_value_l4])()
