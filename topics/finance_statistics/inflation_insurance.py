"""Higher Finance — Inflation and Insurance.

Mirrors Inflation_and_Insurance_Worksheet.docx (Higher Apps/Worksheets/Finance). Traps from the 2023/2024 course
reports and marking instructions: taking the CPI % off a later price instead of dividing (2023 Q9(b)), subtracting
index values instead of comparing ratios (2023 Q9(c)), purchasing-power answers that don't mention buying less for
the same money, and treating the insurance excess as money the insurer pays.
"""
import random

from core.models.question_model import Question

TOPIC = "Finance"
QTYPE = "Inflation and Insurance"

NOTES = """
**Inflation (CPI)**

- A CPI of 133.0 (base 100) means £133 now buys what £100 bought in the base year — **the same money buys less**
  (purchasing power has fallen). "Prices have risen" alone is not enough.
- **Adjusting a price:** new price = old price × new CPI ÷ old CPI (and old = new × old CPI ÷ new CPI).
- **Rate of inflation** between two years = new CPI ÷ old CPI (e.g. 119.0 ÷ 110.4 = 1.0779 → 7.79%) — **not** new − old.
- **Kept up with inflation?** Compare ratios: salary (or savings) new ÷ old against CPI new ÷ old, and state a conclusion.

**Example:** The price of a new car rose in line with CPI between April 2015 (CPI 100) and April 2021 (CPI 110.4). In
2021 it cost £14,108. Calculate its price in April 2015.

- Price in 2015 = 14,108 × 100 ÷ 110.4 = **£12,778.99**  (not 14,108 − 10.4%)

**Insurance**

- The **premium** is what you pay for the policy; the **excess** is the part of any claim **you** pay.
- A higher excess → a **lower premium**. Small claims close to the excess are often not worth making: future premiums
  can rise and a no-claims discount can be lost.
"""


def generate_inflation_l1():
    """Adjusting a price with the CPI (forward or back)."""
    c0 = round(random.uniform(100, 118), 1); c1 = round(c0 * random.uniform(1.04, 1.25), 1)
    item, lo, hi = random.choice([("car", 9000, 25000), ("bike", 300, 1500), ("Harris Tweed jacket", 180, 420), ("kitchen", 4000, 15000)])
    P = random.randrange(lo, hi + 1, 1 if hi < 1000 else 10)
    if random.random() < 0.5:
        ans = P * c0 / c1
        q = (f"A {item} costs £{P:,} now, when the CPI is {c1}. Its price has risen in line with the CPI.\n\n"
             f"Calculate its price when the CPI was {c0}.")
        work = f"£{P:,} × {c0} ÷ {c1} = £{ans:,.2f}  (not {P:,} minus a percentage)"
    else:
        ans = P * c1 / c0
        q = f"A {item} cost £{P:,} when the CPI was {c0}. Its price rises in line with the CPI to {c1}.\n\nCalculate its new price."
        work = f"£{P:,} × {c1} ÷ {c0} = £{ans:,.2f}"
    return Question(question_text=q, correct_answer=round(ans, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "CPI ratio, new ÷ old (4 d.p.)", "answer": round(c1 / c0, 4)}],
                    worked_solution=[work], notes=NOTES)


def generate_inflation_l2():
    """Value needed to keep up with inflation."""
    c0 = round(random.uniform(105, 125), 1); c1 = round(c0 * random.uniform(1.03, 1.12), 1)
    what, lo, hi, dp = random.choice([("hourly wage", 9, 16, 2), ("monthly salary", 1800, 5000, 0), ("savings balance", 2000, 12000, 0)])
    v = round(random.uniform(lo, hi), dp)
    need = v * c1 / c0
    q = (f"A {what} was £{v:,.2f} when the CPI was {c0}. The CPI is now {c1}.\n\n"
         f"Calculate the {what} needed now for it to have kept up with inflation.")
    return Question(question_text=q, correct_answer=round(need, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "CPI ratio, new ÷ old (4 d.p.)", "answer": round(c1 / c0, 4)}],
                    worked_solution=[f"£{v:,.2f} × {c1} ÷ {c0} = £{need:,.2f}"], notes=NOTES)


def generate_inflation_l3():
    """Rate of inflation between two CPI values."""
    c0 = round(random.uniform(100, 125), 1); c1 = round(c0 * random.uniform(1.02, 1.15), 1)
    r = (c1 / c0 - 1) * 100
    q = f"The CPI rose from {c0} to {c1}.\n\nCalculate the rate of inflation over this period, as a percentage to 2 decimal places."
    return Question(question_text=q, correct_answer=round(r, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "CPI ratio, new ÷ old (4 d.p.)", "answer": round(c1 / c0, 4)}],
                    worked_solution=[f"{c1} ÷ {c0} = {c1 / c0:.4f}, so inflation = {r:.2f}%  (not {c1} − {c0} = {c1 - c0:.1f})"],
                    notes=NOTES)


def generate_insurance_l4():
    """What the insurer pays after the excess."""
    ex = random.choice([100, 150, 195, 250, 350, 400]); dmg = random.randrange(ex + 10, ex + 1500, 5)
    q = (f"An insurance policy has a £{ex} excess. Damage costing £{dmg:,} is claimed for.\n\n"
         f"Calculate how much the insurer pays.")
    return Question(question_text=q, correct_answer=float(dmg - ex), topic=TOPIC, question_type=QTYPE,
                    worked_solution=[f"The policyholder pays the first £{ex} (the excess); the insurer pays £{dmg:,} − £{ex} = £{dmg - ex:,}"],
                    notes=NOTES)


def generate_insurance_l5():
    """Total cost in a year with one claim: premium + excess."""
    p = random.randrange(180, 600, 1); ex = random.choice([100, 150, 200, 250, 300, 350, 400, 500])
    q = (f"A car insurance policy costs £{p} a year and has a £{ex} excess. One claim for £1,500 of damage is made during the year.\n\n"
         f"Calculate the total cost to the policyholder for the year.")
    return Question(question_text=q, correct_answer=float(p + ex), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Amount the policyholder pays towards the claim (£)", "answer": float(ex)}],
                    worked_solution=[f"Premium £{p} + excess £{ex} = £{p + ex}"], notes=NOTES)


def generate_inflation_insurance_question():
    return random.choice([generate_inflation_l1, generate_inflation_l2, generate_inflation_l3,
                          generate_insurance_l4, generate_insurance_l5])()
