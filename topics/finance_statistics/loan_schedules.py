"""Higher Finance — Loan Schedules.

Mirrors Loan_Schedules_Worksheet.docx (Higher Apps/Worksheets/Finance). SQA convention (2023–2025
marking instructions): interest = ROUND(monthly rate × previous loan outstanding, 2), capital =
repayment − interest, loan outstanding = previous − capital; the monthly rate is (1 + annual)^(1/12) − 1.
l1–l5 drill the calculator steps and the traps: dividing by 12, the same interest every month,
forgetting the deposit, and total interest = everything repaid − amount borrowed. l6/l7 are the
worksheet's spreadsheet skills (Goal Seek for the repayment, and for the rate of a finance deal) as
download/fill/upload spreadsheets — see loan_spreadsheet.py.
"""
import random

from core.models.question_model import Question, make_part, multipart_worked_solution
from topics.finance_statistics.loan_spreadsheet import (
    CHANGE_NOTES, FIRST_ROW, LOAN_SHEET, build_loan_spreadsheet, holiday_case, increase_case, level_plan,
    level_repayment, monthly_rate, rate_change_case, schedule,
)

TOPIC = "Finance"
QTYPE = "Loan Schedules"
_NAMES = ["Iain", "Kenny", "Seonag", "Fiona", "Ruaridh", "Morven", "Calum", "Eilidh", "Donald", "Iona"]

NOTES = """
**Completing a loan schedule**

| Time (months) | Repayment (£) | Interest content (£) | Capital content (£) | Loan outstanding (£) |
|---|---|---|---|---|
| 0 | | | | 3000.00 |
| 1 | 200.00 | 43.62 | 156.38 | 2843.62 |
| 2 | 200.00 | 41.35 | 158.65 | 2684.97 |

**Example:** Iain borrows £3000 with an annual effective rate of interest of 18.9%. He makes level monthly
repayments of £200 at the end of each month. Complete the loan schedule to show the loan outstanding at the
end of month 2.

- Monthly effective rate = 1.189^(1/12) − 1 = 1.454% (**not** 18.9 ÷ 12)
- Month 1: interest = 0.01454… × 3000.00 = 43.62; capital = 200.00 − 43.62 = 156.38; outstanding = 2843.62
- Month 2: interest = 0.01454… × 2843.62 = 41.35; capital = 158.65; outstanding = **£2684.97**

⚠ Interest is charged on the loan outstanding at the end of the **previous** month, so it falls every month —
using the same interest twice loses the mark (2024 marking instructions). Round each interest to 2 d.p.

- **Finance deals:** the loan is the price **minus the deposit** — the deposit is not borrowed.
- **Total interest** = total of all repayments − amount borrowed.
"""


def _monthly(annual):
    return (1 + annual) ** (1 / 12) - 1


def _schedule(P, i, R, k):
    bal, rows = round(P, 2), []
    for t in range(1, k + 1):
        it = round(i * bal + 1e-9, 2)
        cap = round(R - it, 2)
        bal = round(bal - cap, 2)
        rows.append((t, it, cap, bal))
    return rows


def _steps(rows, i):
    steps = [{"prompt": "What is the monthly effective rate of interest, as a percentage (3 d.p.)?", "answer": round(i * 100, 3)}]
    for t, it, cap, bal in rows:
        steps.append({"prompt": f"Interest content of repayment {t} (£)", "answer": it})
        steps.append({"prompt": f"Loan outstanding at the end of month {t} (£)", "answer": bal})
    return steps


def _work(rows, P, R, i_text):
    lines = [i_text]
    prev = P
    for t, it, cap, bal in rows:
        lines.append(f"Month {t}: interest = {it:.2f}, capital = {R:.2f} − {it:.2f} = {cap:.2f}, "
                     f"outstanding = {prev:,.2f} − {cap:.2f} = {bal:,.2f}")
        prev = bal
    return lines


# (lead, loan lo, hi, step, annual % lo, hi, repayment as a fraction of the loan lo, hi)
_LOANS = [
    ("borrows £{P} to buy a van", 4000, 12000, 500, 6.9, 14.9),
    ("takes out a personal loan of £{P}", 1500, 8000, 250, 7.9, 19.9),
    ("borrows £{P} on a credit union loan", 1000, 5000, 100, 9.9, 26.9),
    ("borrows £{P} for a new loom", 3000, 9000, 250, 5.9, 11.9),
]


def _pick_loan():
    lead, lo, hi, st, rlo, rhi = random.choice(_LOANS)
    P = random.randrange(lo, hi + 1, st)
    a = round(random.uniform(rlo, rhi), 1)
    months = random.choice([24, 36, 48])
    i = _monthly(a / 100)
    R = round(P * i / (1 - (1 + i) ** -months) / 5) * 5 + 5     # a round repayment, a little above level
    return lead, P, a, i, R


def generate_loan_schedules_l1():
    """Annual rate given: monthly rate, then the schedule to the end of month 2 (styled on 2024 Q1)."""
    name = random.choice(_NAMES)
    lead, P, a, i, R = _pick_loan()
    rows = _schedule(P, i, R, 2)
    q = (f"{name} {lead.format(P=f'{P:,}')}. The annual effective rate of interest is {a}%. Level repayments of "
         f"£{R:,} are made at the end of each month.\n\nCalculate the loan outstanding at the end of month 2.")
    return Question(question_text=q, correct_answer=rows[-1][3], topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=_steps(rows, i),
                    worked_solution=_work(rows, P, R, f"Monthly effective rate = {1 + a / 100:.3f}^(1/12) − 1 = {i * 100:.3f}%"),
                    notes=NOTES)


def generate_loan_schedules_l2():
    """Monthly rate given: schedule to the end of month 3."""
    name = random.choice(_NAMES)
    P = random.randrange(1200, 6001, 100)
    mp = random.choice([0.6, 0.7, 0.8, 0.9, 1.1, 1.2, 1.4, 1.6, 1.9])
    R = random.randrange(int(P * 0.04 / 10) * 10 + 20, int(P * 0.08 / 10) * 10 + 30, 10)
    rows = _schedule(P, mp / 100, R, 3)
    q = (f"{name} borrows £{P:,}. The loan is charged an effective rate of {mp:g}% per month, and repayments of £{R} are "
         f"made at the end of each month.\n\nCalculate the loan outstanding at the end of month 3.")
    steps = _steps(rows, mp / 100)[1:]
    return Question(question_text=q, correct_answer=rows[-1][3], topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=_work(rows, P, R, f"Monthly rate = {mp:g}% = {mp / 100:g}"),
                    notes=NOTES)


_DEALS = [("a car", 6000, 14000, 100, [0.10, 0.15, 0.20]), ("a motorbike", 3000, 8000, 100, [0.15, 0.20, 0.25]),
          ("a boat engine", 2400, 6000, 100, [0.20, 0.25]), ("a sofa upholstered in Harris Tweed", 900, 2500, 50, [0.10, 0.15, 0.20])]


def generate_loan_schedules_l3():
    """Finance deal with a deposit: loan outstanding after the first repayment."""
    name = random.choice(_NAMES)
    what, lo, hi, st, deps = random.choice(_DEALS)
    price = random.randrange(lo, hi + 1, st); d = random.choice(deps)
    P = round(price * (1 - d), 2)
    a = round(random.uniform(6.9, 19.9), 1); i = _monthly(a / 100)
    R = round(P * i / (1 - (1 + i) ** -36), 2)
    rows = _schedule(P, i, R, 1)
    q = (f"{name} buys {what} for £{price:,} with a {d:.0%} deposit. The rest is paid by level monthly repayments of "
         f"£{R:,.2f} at the end of each month, at an annual effective rate of interest of {a}%.\n\n"
         f"Calculate the loan outstanding after the first repayment.")
    steps = [{"prompt": "What is the amount borrowed (price − deposit) (£)?", "answer": P}] + _steps(rows, i)
    work = [f"Loan = {price:,} × {1 - d:.2f} = £{P:,.2f} (the deposit is not borrowed)"] + \
        _work(rows, P, R, f"Monthly effective rate = {1 + a / 100:.3f}^(1/12) − 1 = {i * 100:.3f}%")
    return Question(question_text=q, correct_answer=rows[-1][3], topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps, worked_solution=work, notes=NOTES)


def generate_loan_schedules_l4():
    """Total interest from a repayment plan (optionally after a deposit)."""
    name = random.choice(_NAMES)
    what, lo, hi, st, deps = random.choice(_DEALS)
    price = random.randrange(lo, hi + 1, st); d = random.choice(deps)
    P = round(price * (1 - d), 2)
    a = round(random.uniform(6.9, 24.9), 1); i = _monthly(a / 100); n = random.choice([24, 36, 48])
    R = round(P * i / (1 - (1 + i) ** -n), 2)
    F = round(R + random.choice([-0.4, -0.2, 0.1, 0.3]), 2)
    total = round((n - 1) * R + F, 2); interest = round(total - P, 2)
    q = (f"{name} buys {what} for £{price:,}. The finance package is a {d:.0%} deposit, {n - 1} level monthly repayments "
         f"of £{R:,.2f} and a final repayment of £{F:,.2f}.\n\nCalculate the total interest paid.")
    return Question(question_text=q, correct_answer=interest, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Amount borrowed (£)", "answer": P},
                                    {"prompt": "Total of all the monthly repayments (£)", "answer": total}],
                    worked_solution=[f"Borrowed = {price:,} × {1 - d:.2f} = £{P:,.2f}",
                                     f"Repaid = {n - 1} × {R:.2f} + {F:.2f} = £{total:,.2f}",
                                     f"Total interest = {total:,.2f} − {P:,.2f} = £{interest:,.2f}"],
                    notes=NOTES)


def generate_loan_schedules_l5():
    """Bank vs loan company: difference in total interest (styled on 2023 Q11(c)(ii))."""
    name = random.choice(_NAMES)
    P = random.randrange(3000, 12001, 500); n = random.choice([24, 36, 48])
    ab = round(random.uniform(5.9, 8.9), 1); ib = _monthly(ab / 100)
    Rb = round(P * ib / (1 - (1 + ib) ** -n), 2); Fb = round(Rb + random.choice([-0.3, 0.2, 0.4]), 2)
    ic = _monthly(round(random.uniform(22, 35), 1) / 100)       # loan companies: much higher rates
    Rc = round(P * ic / (1 - (1 + ic) ** -n) / 5) * 5
    bank = round((n - 1) * Rb + Fb - P, 2); comp = round(n * Rc - P, 2)
    q = (f"{name} wants to borrow £{P:,} over {n // 12} years. A bank offers {n - 1} repayments of £{Rb:,.2f} and a final "
         f"repayment of £{Fb:,.2f}. A loan company offers {n} repayments of £{Rc:,}.\n\n"
         f"Calculate the difference in the total interest paid on the two loans.")
    return Question(question_text=q, correct_answer=round(comp - bank, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Total interest on the bank loan (£)", "answer": bank},
                                    {"prompt": "Total interest on the loan company loan (£)", "answer": comp}],
                    worked_solution=[f"Bank: {n - 1} × {Rb:.2f} + {Fb:.2f} − {P:,} = £{bank:,.2f}",
                                     f"Loan company: {n} × {Rc} − {P:,} = £{comp:,.2f}",
                                     f"Difference = £{comp - bank:,.2f}"],
                    notes=NOTES)


SPREADSHEET_NOTES = """
**Loan schedules in a spreadsheet (Goal Seek)**

The downloadable sheet uses the same layout as the worksheet's spreadsheet questions:

- Monthly rate: **C6 = (1+C5)^(1/12)−1** (brackets round 1/12)
- Month 1, then fill down: interest **D13 = ROUND($C$6\\*F12,2)**, capital **E13 = C13−D13**,
  outstanding **F13 = F12−E13**
- **Finding the repayment:** Goal Seek — set the last 'Loan outstanding' to 0 by changing C7,
  then round C7 to 2 d.p. The final repayment clears what is left:
  **C8 = F(last−1)+ROUND($C$6\\*F(last−1),2)**
- **Finding the rate:** enter any dummy monthly rate in C6, build the schedule with the repayments
  given, Goal Seek the last 'Loan outstanding' to 0 by changing C6, then **C5 = (1+C6)^12−1**
- For a finance deal the loan is the price **minus the deposit**.
""" + CHANGE_NOTES + """
⚠ Leaving out ROUND lets the pennies drift; giving the monthly rate when the annual rate is asked
for loses the final mark (2023–2025 marking instructions). Save the file before uploading.
"""

_TERM_LOANS = [
    ("The Croft Tractor Loan", "{name} borrows £{P:,} over {y} years to buy a tractor for the croft.", 6000, 15000, 500),
    ("The Harris Tweed Loom Loan", "{name}, a weaver, borrows £{P:,} over {y} years to buy a new loom.", 4000, 9000, 200),
    ("The Van Loan", "{name} borrows £{P:,} over {y} years to buy a van for the business.", 5000, 14000, 500),
    ("The Home Improvement Loan", "{name} borrows £{P:,} over {y} years for a new kitchen.", 3000, 10000, 250),
]


def generate_loan_schedules_l6():
    """Spreadsheet: Goal Seek the level repayment and the final repayment (worksheet Section 2)."""
    name = random.choice(_NAMES)
    title, lead, lo, hi, st = random.choice(_TERM_LOANS)
    P = random.randrange(lo, hi + 1, st)
    y = random.choice([2, 3, 4])
    n = 12 * y
    a = round(random.uniform(4.9, 12.9), 1)
    i = monthly_rate(a / 100)
    R = round(level_repayment(P, i, n), 2)
    rows = schedule(P, i, R, n)
    final = round(rows[-1][1], 2)
    total_interest = round((n - 1) * R + final - P, 2)
    q = (f"{lead.format(name=name, P=P, y=y)} The annual effective rate of interest is {a}%. Level monthly "
         f"repayments are made at the end of each month, with the final repayment adjusted so the loan ends at "
         f"exactly £0.00.\n\nDownload the spreadsheet below. Complete the loan schedule to determine the level "
         f"monthly repayment (cell C7) and the final repayment (cell C8), then save it and upload it here.")
    meta = build_loan_spreadsheet(
        title=title, sheet_name="Loan Schedule", filename=f"loan_schedule_{name.lower()}.xlsx",
        mode="repayment", P=P, i=i, n=n, rows=rows, R=R, final=final, annual=a / 100)
    return Question(
        question_text=q, correct_answer=R, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[
            {"prompt": "What is the monthly effective rate of interest, as a percentage (3 d.p.)?", "answer": round(i * 100, 3)},
            {"prompt": "Interest content of the first repayment (£)", "answer": rows[0][2]},
            {"prompt": "Level monthly repayment, to 2 d.p. (£)", "answer": R},
            {"prompt": "Final repayment (£)", "answer": final},
        ],
        worked_solution=[
            f"C6: monthly rate = (1 + {a / 100:g})^(1/12) − 1 = {i * 100:.3f}%",
            f"D13 = ROUND($C$6*F12,2) = {rows[0][2]:.2f}; fill D, E and F down to month {n}",
            f"Goal Seek: last 'Loan outstanding' = 0 by changing C7 → level repayment = £{R:,.2f}",
            f"Final repayment = F{FIRST_ROW + n - 2} + ROUND($C$6*F{FIRST_ROW + n - 2},2) = £{final:,.2f}",
            f"(Total interest = {n - 1} × {R:,.2f} + {final:,.2f} − {P:,} = £{total_interest:,.2f})",
        ],
        notes=SPREADSHEET_NOTES, metadata=meta)


def generate_loan_schedules_l7():
    """Spreadsheet: Goal Seek the effective rate of a finance deal with a deposit (worksheet Section 3)."""
    name = random.choice(_NAMES)
    what, lo, hi, st, deps = random.choice(_DEALS)
    price = random.randrange(lo, hi + 1, st)
    d = random.choice(deps)
    P = round(price * (1 - d), 2)
    n = random.choice([24, 36, 48])
    a = round(random.uniform(6.9, 19.9), 1)
    i = monthly_rate(a / 100)
    R = round(level_repayment(P, i, n), 2)
    final = round(schedule(P, i, R, n)[-1][1], 2)       # the printed final repayment, to the penny
    rows = schedule(P, i, R, n, final)
    q = (f"{name} buys {what} for £{price:,}. The finance package is:\n"
         f"- {d:.0%} deposit\n- {n - 1} level monthly repayments of £{R:,.2f}\n"
         f"- final monthly repayment £{final:,.2f}\n\n"
         f"Download the spreadsheet below. Complete the loan schedule to determine the annual effective rate of "
         f"interest being charged (cell C5), then save it and upload it here.")
    meta = build_loan_spreadsheet(
        title=f"Finance Deal — {what[0].upper() + what[1:]}", sheet_name="Loan Schedule",
        filename=f"finance_deal_{name.lower()}.xlsx", mode="rate", P=P, i=i, n=n, rows=rows, R=R,
        final=final, annual=a / 100, price=price, deposit=d)
    return Question(
        question_text=q, correct_answer=a, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[
            {"prompt": "Amount borrowed (price − deposit) (£)", "answer": P},
            {"prompt": "Monthly effective rate found by Goal Seek, as a percentage (3 d.p.)", "answer": round(i * 100, 3)},
            {"prompt": "Annual effective rate of interest (%)", "answer": a},
        ],
        worked_solution=[
            f"C4: loan = {price:,} × (1 − {d:g}) = £{P:,.2f} (the deposit is not borrowed)",
            f"Build the schedule with repayments of £{R:,.2f} and a final repayment of £{final:,.2f}",
            f"Goal Seek: last 'Loan outstanding' = 0 by changing C6 → monthly rate = {i * 100:.3f}%",
            f"C5 = (1 + C6)^12 − 1 = {a:.1f}%",
        ],
        notes=SPREADSHEET_NOTES, metadata=meta)


# ---------------------------------------------------------------------------
# Spreadsheet questions on a change to the plan part-way through (an increased repayment, a payment
# holiday, a change of interest rate) — built by loan_spreadsheet.py's *_case() helpers.
# ---------------------------------------------------------------------------

def _term_plan():
    name = random.choice(_NAMES)
    title, lead, lo, hi, st = random.choice(_TERM_LOANS)
    P = random.randrange(lo, hi + 1, st)
    y = random.choice([2, 3, 4])
    a = round(random.uniform(4.9, 12.9), 1)
    return level_plan(name, P, a, 12 * y, LOAN_SHEET, title, lead=lead.format(name=name, P=P, y=y))


def _plan_intro(p):
    return (f"{p['lead']} The annual effective rate of interest is {p['a']}%, with {p['n'] - 1} level monthly "
            f"repayments of £{p['R']:,.2f} and a final repayment of £{p['F']:,.2f}.")


def _rate_change_intro(p):
    return (f"{p['lead']} The loan has a fixed annual effective rate of {p['a']}% to begin with, and level monthly "
            f"repayments of £{p['R']:,.2f}.")


def _single(case, intro):
    p = _term_plan()
    c = case(p)
    return Question(question_text=f"{intro(p)} {c['text']}", correct_answer=c["answer"], topic=TOPIC,
                    question_type=QTYPE, scaffold_steps=c["steps"], worked_solution=c["worked"],
                    notes=SPREADSHEET_NOTES, metadata=c["meta"])


def generate_loan_schedules_l8():
    """Spreadsheet: increase the repayment part-way through — saving over the term."""
    return _single(increase_case, _plan_intro)


def generate_loan_schedules_l9():
    """Spreadsheet: a payment holiday part-way through — extra cost."""
    return _single(holiday_case, _plan_intro)


def generate_loan_schedules_l10():
    """Spreadsheet: the rate rises after a fixed period — Goal Seek the new level repayment."""
    return _single(rate_change_case, _rate_change_intro)


def generate_loan_schedules_l11():
    """Exam style, in parts as 2023 Q11: (a) spreadsheet level repayment, (b) total interest, (c) a
    spreadsheet change to the plan — an increased repayment, a payment holiday or a rate rise."""
    p = _term_plan()
    name, P, a, i, n, R, F = p["name"], p["P"], p["a"], p["i"], p["n"], p["R"], p["F"]
    case = random.choice([increase_case, holiday_case, rate_change_case])
    rate_note = " (fixed for the first part of the term — see part (c))" if case is rate_change_case else ""
    context = (f"{p['lead']} The annual effective rate of interest is {a}%{rate_note}. Level monthly repayments "
               f"are made at the end of each month, with the final repayment adjusted so the loan ends at exactly "
               f"£0.00.")

    rows = schedule(P, i, R, n)
    part_a = make_part(
        "(a)", "Download the spreadsheet below. Complete the loan schedule to determine the level monthly "
               "repayment (cell C7) and the final repayment (cell C8), then save it and upload it here.", R,
        scaffold_steps=[{"prompt": "Monthly effective rate, as a percentage (3 d.p.)", "answer": round(i * 100, 3)},
                        {"prompt": "Interest content of the first repayment (£)", "answer": rows[0][2]},
                        {"prompt": "Level monthly repayment, to 2 d.p. (£)", "answer": R}],
        worked_solution=[f"C6 = (1 + {a / 100:g})^(1/12) − 1 = {i * 100:.3f}%",
                         f"Goal Seek: last 'Loan outstanding' = 0 by changing C7 → £{R:,.2f}",
                         f"Final repayment = what is left in month {n} = £{F:,.2f}"])
    part_a.metadata.update(build_loan_spreadsheet(
        title=p["title"], sheet_name="Loan Schedule", filename=f"loan_schedule_{name.lower()}.xlsx",
        mode="repayment", P=P, i=i, n=n, rows=rows, R=R, final=F, annual=a / 100))

    interest = round(p["orig"] - P, 2)
    part_b = make_part(
        "(b)", "Calculate the total interest paid on the loan.", interest,
        scaffold_steps=[{"prompt": "Total of all the repayments (£)", "answer": p["orig"]}],
        worked_solution=[f"Total repaid = {n - 1} × {R:,.2f} + {F:,.2f} = £{p['orig']:,.2f}",
                         f"Total interest = {p['orig']:,.2f} − {P:,} = £{interest:,.2f}"])

    c = case(p)
    part_c = make_part("(c)", c["text"], c["answer"], scaffold_steps=c["steps"], worked_solution=c["worked"])
    part_c.metadata.update(c["meta"])

    parts = [part_a, part_b, part_c]
    return Question(question_text=context, correct_answer=c["answer"], topic=TOPIC, question_type=QTYPE,
                    parts=parts, worked_solution=multipart_worked_solution(parts), notes=SPREADSHEET_NOTES)


# The non-spreadsheet question types, grouped as one "Calculator Questions" entry in the app and
# weighted toward what the 2023–2026 past papers actually ask (see the comments).
_CALCULATOR_MIX = [
    (generate_loan_schedules_l1, 5),        # schedule by hand to month 2 — 2024 Q1
    (generate_loan_schedules_l3, 2),        # finance deal: the loan is price − deposit — 2025 Q8
    (generate_loan_schedules_l4, 2),        # total interest — 2023 Q11(b)
    (generate_loan_schedules_l5, 2),        # difference in total interest — 2023 Q11(c)
    (generate_loan_schedules_l2, 1),        # monthly rate given — not yet examined
]


def generate_loan_schedules_calculator():
    generator = random.choices([g for g, _ in _CALCULATOR_MIX], weights=[w for _, w in _CALCULATOR_MIX])[0]
    return generator()


def generate_loan_schedules_question():
    return random.choice([generate_loan_schedules_calculator, generate_loan_schedules_l6, generate_loan_schedules_l7,
                          generate_loan_schedules_l8, generate_loan_schedules_l9, generate_loan_schedules_l10,
                          generate_loan_schedules_l11])()
