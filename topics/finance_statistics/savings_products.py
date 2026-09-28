"""Higher Finance — Savings Products and Pensions.

Mirrors Savings_Products_and_Pensions_Worksheet.docx (Higher Apps/Worksheets/Finance). Lifetime ISA rule as in
the 2025 pre-release: 25% bonus (max £1000 on £4000 a year) paid on the first day of the following month.
Traps (2025 Q6 marking instructions): growing the bonus for 12 months; bonus on the balance after interest.
Regular savings through rate changes are the existing "Savings Schedule" type.
"""
import math
import random

from core.models.question_model import Question

TOPIC = "Finance"
QTYPE = "Savings Products and Pensions"
_NAMES = ["Morgan", "Kirsty", "Seonag", "Ailsa", "Natasha", "Iain", "Donald", "Fiona", "Mairi", "Calum"]
_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November"]

NOTES = """
**Savings products and pensions**

**Lifetime ISA:** the government adds a **25% bonus** (up to £1000 a year, on up to £4000 paid in), paid on the **first day
of the following month** — so the bonus earns interest for one month less than the deposit.

**Example:** Kirsty opens a Lifetime ISA with an annual effective rate of 3.4%. She deposits £3000 on 1 January. The bonus
is paid on the first day of the following month. Calculate the accumulated value on 31 December.

- Bonus = 25% of £3000 = £750, paid on 1 February
- Deposit: 3000 × 1.034^(12/12) = £3102.00
- Bonus: 750 × 1.034^(11/12) = £773.20
- Accumulated value = **£3875.20**

⚠ Don't grow the bonus for 12 months, and work out the bonus on the **deposit**, not the balance after interest
(2025 marking instructions).

- **Contributions over several years:** each payment grows for its own number of years — add them up.
- **Deposit needed for a goal:** D × (sum of the multipliers) = goal, so D = goal ÷ (sum); round **up**.
"""


def generate_savings_products_l1():
    """Lifetime ISA value on 31 December (styled on 2025 Q6)."""
    name = random.choice(_NAMES); r = round(random.uniform(2.5, 4.5), 2)
    mo = random.randint(1, 6); D = random.randrange(1000, 5001, 100)
    b = min(0.25 * min(D, 4000), 1000)
    v = D * (1 + r / 100) ** ((13 - mo) / 12) + b * (1 + r / 100) ** ((12 - mo) / 12)
    q = (f"{name} opens a Lifetime ISA with an annual effective rate of interest of {r:g}%. They deposit £{D:,} on 1 "
         f"{_MONTHS[mo - 1]}. The 25% government bonus (up to £1000 a year) is paid on the first day of the following month. "
         f"No further deposits are made.\n\nCalculate the accumulated value on 31 December.")
    return Question(question_text=q, correct_answer=round(v, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Bonus (£)", "answer": b},
                                    {"prompt": "Value of the deposit on 31 December (£)", "answer": round(D * (1 + r / 100) ** ((13 - mo) / 12), 2)}],
                    worked_solution=[f"Bonus = £{b:,.2f}" + (" (capped: only £4000 counts)" if D > 4000 else ""),
                                     f"{D:,} × {1 + r / 100:g}^({13 - mo}/12) + {b:,.2f} × {1 + r / 100:g}^({12 - mo}/12) = £{v:,.2f}"],
                    notes=NOTES)


def generate_savings_products_l2():
    """Savings schedule by hand to the second regular deposit (styled on 2026 Q6)."""
    a = round(random.uniform(1.2, 3.5), 1); D0 = random.randrange(500, 3001, 100); R = random.randrange(50, 301, 25)
    i = (1 + a / 100) ** (1 / 12) - 1; bal = float(D0); steps = []
    for k in range(2):
        bal = round(round(bal * (1 + i), 2) + R, 2); steps.append({"prompt": f"Balance after deposit {k + 1} of £{R} (£)", "answer": bal})
    q = (f"A savings account has an annual effective rate of {a}%, with interest paid at the end of each month. £{D0:,} is "
         f"deposited on the first day of a month, then £{R} on the first day of each month after that.\n\n"
         f"Calculate the balance immediately after the second £{R} deposit.")
    return Question(question_text=q, correct_answer=bal, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Monthly effective rate, as a percentage (3 d.p.)", "answer": round(i * 100, 3)}] + steps[:1],
                    worked_solution=[f"Monthly rate = {i * 100:.3f}%", f"After deposit 1: £{steps[0]['answer']:,.2f}",
                                     f"After deposit 2: £{bal:,.2f}"], notes=NOTES)


def generate_savings_products_l3():
    """Pension contributions at the start of each year — level or rising."""
    r = round(random.uniform(3.0, 6.0), 1); n = random.randint(3, 5); first = random.randrange(1000, 4001, 100)
    kind = random.choice(["level", "amount", "percent"])
    if kind == "level":
        pays = [first] * n; how = f"£{first:,} at the start of each year"
    elif kind == "amount":
        st = random.choice([100, 200, 250]); pays = [first + st * k for k in range(n)]; how = f"£{first:,} at the start of year 1, rising by £{st} each year"
    else:
        g = random.choice([2, 3, 4]); pays = [round(first * (1 + g / 100) ** k, 2) for k in range(n)]; how = f"£{first:,} at the start of year 1, rising by {g}% each year"
    v = sum(p * (1 + r / 100) ** (n - k) for k, p in enumerate(pays))
    q = (f"Pension contributions of {how} are paid for {n} years. The pension grows at an annual effective rate of {r}%.\n\n"
         f"Calculate the value of the pension at the end of year {n}.")
    return Question(question_text=q, correct_answer=round(v, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": f"Value at the end of year {n} of the first contribution (£)", "answer": round(pays[0] * (1 + r / 100) ** n, 2)}],
                    worked_solution=[" + ".join(f"{p:,.2f} × {1 + r / 100:g}^{n - k}" for k, p in enumerate(pays)) + f" = £{v:,.2f}"],
                    notes=NOTES)


def generate_savings_products_l4():
    """Equal deposit at the start of each year needed for a goal."""
    goal = random.randrange(4000, 20001, 500); r = round(random.uniform(2.0, 5.0), 1); n = random.randint(2, 5)
    f = sum((1 + r / 100) ** k for k in range(1, n + 1)); d = math.ceil(round(goal / f * 100, 6)) / 100
    q = (f"£{goal:,} is needed at the end of year {n}. Equal deposits are made at the start of each year into an account with "
         f"an annual effective rate of {r}%.\n\nCalculate the deposit needed each year.")
    return Question(question_text=q, correct_answer=d, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Sum of the growth multipliers (5 d.p.)", "answer": round(f, 5)}],
                    worked_solution=[f"D × ({' + '.join(f'{1 + r / 100:g}^{k}' for k in range(n, 0, -1))}) = {goal:,}",
                                     f"D = {goal:,} ÷ {f:.5f} = £{d:,.2f} (rounded up)"], notes=NOTES)


def generate_savings_products_question():
    return random.choice([generate_savings_products_l1, generate_savings_products_l2, generate_savings_products_l3,
                          generate_savings_products_l4])()
