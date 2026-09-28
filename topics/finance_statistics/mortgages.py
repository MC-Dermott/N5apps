"""Higher Finance — Mortgages.

Mirrors Mortgages_Worksheet.docx (Higher Apps/Worksheets/Finance). Replaces the old flat-rate version:
the Higher Apps course uses effective (compound) rates only. SQA convention (2024 Q9, 2026 Q8 marking
instructions): monthly rate (1 + annual)^(1/12) − 1, interest = ROUND(rate × previous outstanding, 2);
paying the lender's maximum shortens the term and the saving is the difference in the TOTAL repaid;
affordability = repayments no more than 28% of monthly taxable income (after pension contributions);
loan-to-value = mortgage ÷ property value.
"""
import random

from core.models.question_model import Question

TOPIC = "Finance"
QTYPE = "Mortgages"
_NAMES = ["Morag", "Ceit", "Domhnall", "Janet", "Fraser", "Kirsty", "Calum", "Iona", "Ewan", "Niall"]

NOTES = """
**Mortgages**

- **Monthly rate** = (1 + annual rate)^(1/12) − 1 — never annual ÷ 12, and never type a rounded rate into a spreadsheet
- **Each month:** interest = rate × mortgage outstanding (to 2 d.p.); capital = repayment − interest;
  outstanding = previous outstanding − capital
- **Paying the lender's maximum** shortens the term; the **saving** = total repaid on the original plan −
  total repaid on the new plan (not the difference in the monthly repayments)
- **Target balance** at the end of a fixed rate: Goal Seek the outstanding at the end of the fixed period to the
  **target** (not to 0), then round the repayment **up**
- **Affordability:** repayments should be no more than **28% of monthly taxable income** (salary after pension
  contributions). Always give the figure as your reason.
- **Loan-to-value** = mortgage ÷ property value (not deposit ÷ value)

**Example:** Lenders recommend that mortgage repayments are no more than 28% of monthly taxable income. Iona earns
£34,800 a year and pays 5% into her pension. Her repayment would be £720. Is it affordable?

- Taxable income = 34,800 × 0.95 = £33,060 a year = £2,755.00 a month
- 28% of £2,755.00 = £771.40
- £720 < £771.40, so **yes — affordable**
"""


def _monthly(a):
    return (1 + a) ** (1 / 12) - 1


def _clear(P, i, R):
    bal, rows = round(P, 2), []
    while bal > 0 and len(rows) < 600:
        it = round(i * bal + 1e-9, 2)
        pay = min(R, round(bal + it, 2))
        bal = round(bal - (pay - it), 2)
        rows.append((pay, it, bal))
    return rows


def _level(P, i, n):
    R = round(P * i / (1 - (1 + i) ** -n), 2)
    bal = round(P, 2)
    for _ in range(n - 1):
        bal = round(bal - (R - round(i * bal + 1e-9, 2)), 2)
    F = round(bal + round(i * bal + 1e-9, 2), 2)
    return R, F


# (context, amount lo, hi, step, annual % lo, hi, years options)
_MORTGAGES = [("a house", 90000, 240000, 5000, 3.9, 5.9, [20, 25, 30]),
              ("an extension to their croft house", 15000, 35000, 1000, 3.0, 4.5, [4, 5, 6]),
              ("a flat in Stornoway", 70000, 140000, 5000, 4.1, 5.6, [20, 25])]


def generate_mortgages_l1():
    """Mortgage outstanding at the end of month 2, by hand."""
    name = random.choice(_NAMES); ctx, lo, hi, st, rlo, rhi, yrs = random.choice(_MORTGAGES)
    P = random.randrange(lo, hi + 1, st); a = round(random.uniform(rlo, rhi), 1); i = _monthly(a / 100)
    R = round(P * i / (1 - (1 + i) ** -(12 * random.choice(yrs))) / 5) * 5 + 5
    it1 = round(i * P + 1e-9, 2); b1 = round(P - (R - it1), 2)
    it2 = round(i * b1 + 1e-9, 2); b2 = round(b1 - (R - it2), 2)
    q = (f"{name} takes out a £{P:,} mortgage for {ctx}. The annual effective rate of interest is {a}%, and repayments of "
         f"£{R:,} are made at the end of each month.\n\nCalculate the mortgage outstanding at the end of month 2.")
    return Question(question_text=q, correct_answer=b2, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Monthly effective rate, as a percentage (3 d.p.)", "answer": round(i * 100, 3)},
                                    {"prompt": "Mortgage outstanding at the end of month 1 (£)", "answer": b1},
                                    {"prompt": "Interest content of repayment 2 (£)", "answer": it2}],
                    worked_solution=[f"Monthly rate = {1 + a / 100:.3f}^(1/12) − 1 = {i * 100:.3f}%",
                                     f"Month 1: interest {it1:,.2f}, outstanding {b1:,.2f}",
                                     f"Month 2: interest {it2:,.2f}, outstanding £{b2:,.2f}"],
                    notes=NOTES)


def generate_mortgages_l2():
    """Loan-to-value ratio."""
    name = random.choice(_NAMES)
    V = random.randrange(120000, 320001, 5000)
    dep = random.choice([0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
    D = round(V * dep)
    ltv = round((V - D) / V * 100, 2)
    q = (f"{name} buys a house valued at £{V:,}, paying a deposit of £{D:,} and taking a mortgage for the rest.\n\n"
         f"Calculate the loan-to-value ratio, as a percentage.")
    return Question(question_text=q, correct_answer=ltv, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Mortgage amount (£)", "answer": V - D}],
                    worked_solution=[f"Mortgage = {V:,} − {D:,} = £{V - D:,}",
                                     f"Loan-to-value = {V - D:,} ÷ {V:,} = {ltv:g}%  (not deposit ÷ value)"],
                    notes=NOTES)


def generate_mortgages_l3():
    """Maximum affordable repayment under the 28% guideline (styled on 2026 Q8(c))."""
    name = random.choice(_NAMES)
    sal = random.randrange(22000, 52001, 100); pen = random.choice([0.03, 0.04, 0.05, 0.06, 0.08])
    tax_m = sal * (1 - pen) / 12; lim = round(0.28 * tax_m, 2)
    q = (f"Lenders recommend that mortgage repayments are no more than 28% of monthly taxable income (salary after "
         f"pension contributions). {name} earns £{sal:,} a year and pays {pen:.0%} of it into a pension.\n\n"
         f"Calculate the maximum monthly repayment the lender would consider affordable.")
    return Question(question_text=q, correct_answer=lim, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Annual taxable income (£)", "answer": round(sal * (1 - pen), 2)},
                                    {"prompt": "Monthly taxable income (£)", "answer": round(tax_m, 2)}],
                    worked_solution=[f"Taxable income = {sal:,} × {1 - pen:.2f} = £{sal * (1 - pen):,.2f} a year",
                                     f"Monthly = £{tax_m:,.2f};  28% = £{lim:,.2f}"],
                    notes=NOTES)


def generate_mortgages_l4():
    """Saving from paying the lender's maximum repayment (styled on 2024 Q9(c))."""
    name = random.choice(_NAMES)
    P = random.randrange(15000, 40001, 1000); a = round(random.uniform(3.0, 4.8), 1); yrs = random.choice([4, 5, 6])
    i = _monthly(a / 100); R, F = _level(P, i, yrs * 12)
    mx = int(R // 50 + 2) * 50
    inc = _clear(P, i, mx)
    orig = round((yrs * 12 - 1) * R + F, 2); new = round(sum(r[0] for r in inc), 2)
    q = (f"{name}'s £{P:,} mortgage over {yrs} years has {yrs * 12 - 1} level repayments of £{R:,.2f} and a final repayment "
         f"of £{F:,.2f}. By paying the lender's maximum of £{mx} a month instead, the mortgage is cleared with "
         f"{len(inc) - 1} repayments of £{mx} and a final repayment of £{inc[-1][0]:,.2f}.\n\n"
         f"Calculate how much {name} saves over the term of the mortgage.")
    return Question(question_text=q, correct_answer=round(orig - new, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Total repaid on the original plan (£)", "answer": orig},
                                    {"prompt": "Total repaid paying the maximum (£)", "answer": new}],
                    worked_solution=[f"Original: {yrs * 12 - 1} × {R:,.2f} + {F:,.2f} = £{orig:,.2f}",
                                     f"Maximum: {len(inc) - 1} × {mx} + {inc[-1][0]:,.2f} = £{new:,.2f}",
                                     f"Saving = £{orig - new:,.2f}  (not {mx} − {R:,.2f})"],
                    notes=NOTES)


def generate_mortgages_l5():
    """Total interest on a mortgage plan."""
    name = random.choice(_NAMES); ctx, lo, hi, st, rlo, rhi, yrs = random.choice(_MORTGAGES)
    P = random.randrange(lo, hi + 1, st); a = round(random.uniform(rlo, rhi), 1); y = random.choice(yrs)
    R, F = _level(P, _monthly(a / 100), y * 12)
    total = round((y * 12 - 1) * R + F, 2)
    q = (f"{name}'s £{P:,} mortgage for {ctx} is repaid with {y * 12 - 1} level monthly repayments of £{R:,.2f} and a "
         f"final repayment of £{F:,.2f}.\n\nCalculate the total interest paid.")
    return Question(question_text=q, correct_answer=round(total - P, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Total repaid (£)", "answer": total}],
                    worked_solution=[f"Total repaid = {y * 12 - 1} × {R:,.2f} + {F:,.2f} = £{total:,.2f}",
                                     f"Total interest = {total:,.2f} − {P:,} = £{total - P:,.2f}"],
                    notes=NOTES)


def generate_mortgages_question():
    return random.choice([generate_mortgages_l1, generate_mortgages_l2, generate_mortgages_l3,
                          generate_mortgages_l4, generate_mortgages_l5])()
