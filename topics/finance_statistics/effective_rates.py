"""Higher Finance — Effective Interest Rates.

Mirrors Effective_Interest_Rates_Worksheet.docx (Higher Apps/Worksheets/Finance): converting between
annual, monthly and quarterly effective rates, growing an amount for part of a year, and a loan's
balance through changing rates before repayments start. Varying-rate SAVINGS (single/multiple
deposits, minimum deposit) are the existing "Interest" type, not repeated here.

Common errors built into the notes (2024 course report / marking instructions): dividing the
annual rate by 12, a % sign on the decimal (0.022%), missing brackets round 1/12, whole-number
powers for part-years, the rate used instead of the multiplier, wrong month counts.
"""
import calendar
import random

from core.models.question_model import Question

TOPIC = "Finance"
QTYPE = "Effective Interest Rates"

_NAMES = ["Eilidh", "Calum", "Morag", "Ruaridh", "Seonag", "Iain", "Kirsty", "Donald", "Mairi", "Ewan"]

ANNUAL_TO_MONTHLY_NOTES = """
**Annual → monthly effective rate**

Monthly multiplier = (annual multiplier)^(1/12), then subtract 1.

**Example:** A credit card has an annual effective rate of interest of 22.9%. Calculate the monthly
effective rate of interest.

- Annual multiplier = 1 + 0.229 = 1.229
- Monthly multiplier = 1.229^(1/12) = 1.01733… (type (1.229)^(1÷12) — brackets round the 1÷12)
- Monthly effective rate = 1.01733… − 1 = 0.01733… = **1.73% per month**

⚠ **Don't divide by 12** — 22.9 ÷ 12 = 1.91% is wrong (the most common error in the 2024 course
report). And 0.0173 is 1.73%, **not** 0.0173%.
"""

MONTHLY_TO_ANNUAL_NOTES = """
**Monthly → annual effective rate**

Annual multiplier = (monthly multiplier)^12, then subtract 1.

**Example:** A savings account pays an effective rate of 0.25% per month. Calculate the annual
effective rate of interest.

- Monthly multiplier = 1.0025
- Annual multiplier = 1.0025^12 = 1.03041…
- Annual effective rate = 1.03041… − 1 = **3.04% per year**

⚠ **Don't multiply by 12** (0.25 × 12 = 3.00%) — that ignores the interest earned on interest.
"""

QUARTERLY_NOTES = """
**Other frequencies (e.g. quarterly)**

A year has 4 quarters, so use the power 4 (quarterly → annual) or 1/4 (annual → quarterly), exactly
as you use 12 and 1/12 for months.

- 1.2% per quarter → 1.012^4 − 1 = **4.89% per year**
- 5.5% per year → 1.055^(1/4) − 1 = **1.35% per quarter**
"""

PART_YEAR_NOTES = """
**Growing an amount for part of a year**

For an **annual** rate held for n months, the multiplier is (1 + rate)^(n/12).
For a **monthly** rate held for n months, the multiplier is (1 + rate)^n.

**Example:** Eilidh puts £2400 into a savings account with an annual effective rate of interest of
3.6%. Calculate the balance after 7 months.

- 7 months = 7/12 of a year, so the annual multiplier is raised to the power 7/12
- Balance = 2400 × 1.036^(7/12) = **£2450.03**

⚠ Don't use the power 7 (that is seven **years** of interest), and always use the multiplier
1.036, not the rate 0.036.
"""

LOAN_BEFORE_REPAYMENTS_NOTES = """
**Interest rates that change over time**

1. Count the months in each rate period (first day to first day)
2. Monthly rate → power = number of months. Annual rate → power = months ÷ 12
3. Multiply the amount by all of the multipliers in one go

**Example:** Kirsty deposits £3000 in a variable rate savings account on 1 January 2024. The effective
rates of interest are:

| Dates | Interest rate |
|---|---|
| 1 January 2024 to 31 March 2024 | 0.35% per **month** |
| 1 April 2024 to 31 December 2024 | 4.2% per **year** |
| From 1 January 2025 | 3.0% per **year** |

Calculate her balance on 1 July 2026.

- Months in each period: 3, 9 and 18
- Balance = 3000 × 1.0035^3 × 1.042^(9/12) × 1.03^(18/12) = **£3268.36**

⚠ The most common error (2024 course report) is the **wrong number of months** in a period. A loan's
balance before repayments start grows in exactly the same way — SQA only gives the mark for an annual
rate if a **fractional power** is used.
"""


def _pct(x, dp=2):
    return f"{x * 100:.{dp}f}"


def _mult(rate):
    """1 + rate written as the marking instructions write it (1.042, 1.0035, 1.299)."""
    return f"{1 + rate:.6f}".rstrip("0").rstrip(".")


def _money(x):
    return f"{x:,.2f}"


def _rate_str(pct):
    return f"{pct:g}"


# (context, lead phrase, annual rate % lo, hi, step)
_ANNUAL_CONTEXTS = [
    ("savings account", "A savings account has", 1.2, 5.5, 0.1),
    ("personal loan", "A personal loan has", 5.9, 14.9, 0.1),
    ("car finance deal", "A car finance deal has", 6.9, 19.9, 0.1),
    ("credit card", "A credit card has", 18.9, 34.9, 0.1),
    ("store card", "A store card has", 24.9, 39.9, 0.1),
]


def _pick_rate(lo, hi, step):
    n = int(round((hi - lo) / step))
    return round(lo + step * random.randint(0, n), 2)


def generate_effective_rates_l1():
    """Annual → monthly effective rate."""
    ctx, lead, lo, hi, step = random.choice(_ANNUAL_CONTEXTS)
    a = _pick_rate(lo, hi, step)
    mm = (1 + a / 100) ** (1 / 12)
    ans = round((mm - 1) * 100, 3)
    q = (f"{lead} an annual effective rate of interest of {_rate_str(a)}%.\n\n"
         f"Calculate the monthly effective rate of interest. Give your answer as a percentage to 3 significant "
         f"figures.")
    return Question(
        question_text=q, correct_answer=float(f"{(mm - 1) * 100:.3g}"), topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "What is the annual multiplier (1 + rate)?", "answer": round(1 + a / 100, 6)},
                        {"prompt": "What is the monthly multiplier, (annual multiplier)^(1/12)? (5 d.p.)",
                         "answer": round(mm, 5)}],
        worked_solution=[f"Annual multiplier = {_mult(a / 100)}",
                         f"Monthly multiplier = {_mult(a / 100)}^(1/12) = {mm:.5f}…",
                         f"Monthly effective rate = {mm:.5f}… − 1 = {(mm - 1):.5f}… = {(mm - 1) * 100:.3g}% per month",
                         f"(Not {_rate_str(a)} ÷ 12 = {a / 12:.3g}% — dividing by 12 is the most common error.)"],
        notes=ANNUAL_TO_MONTHLY_NOTES)


def generate_effective_rates_l2():
    """Monthly → annual effective rate."""
    kind = random.choice(["savings", "loan"])
    if kind == "savings":
        mpct = random.choice([0.1, 0.12, 0.15, 0.18, 0.2, 0.25, 0.28, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6])
        lead = random.choice(["A regular saver account pays", "A savings account pays", "A credit union account pays"])
    else:
        mpct = random.choice([0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.4, 2.7, 2.9, 3.1])
        lead = random.choice(["A store card charges", "A short-term loan charges", "A credit card charges"])
    am = (1 + mpct / 100) ** 12
    q = (f"{lead} an effective rate of {_rate_str(mpct)}% per month.\n\n"
         f"Calculate the annual effective rate of interest. Give your answer as a percentage to 2 decimal places.")
    return Question(
        question_text=q, correct_answer=round((am - 1) * 100, 2), topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "What is the monthly multiplier (1 + rate)?", "answer": round(1 + mpct / 100, 6)},
                        {"prompt": "What is the annual multiplier, (monthly multiplier)^12? (5 d.p.)",
                         "answer": round(am, 5)}],
        worked_solution=[f"Monthly multiplier = {_mult(mpct / 100)}",
                         f"Annual multiplier = {_mult(mpct / 100)}^12 = {am:.5f}…",
                         f"Annual effective rate = {am:.5f}… − 1 = {_pct(am - 1)}% per year",
                         f"(Not {_rate_str(mpct)} × 12 = {mpct * 12:g}% — that ignores interest on interest.)"],
        notes=MONTHLY_TO_ANNUAL_NOTES)


def generate_effective_rates_l3():
    """Quarterly ↔ annual."""
    if random.random() < 0.5:
        qpct = random.choice([0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.5, 1.8, 2.0])
        am = (1 + qpct / 100) ** 4
        q = (f"A credit union savings account pays an effective rate of {_rate_str(qpct)}% per quarter "
             f"(every 3 months).\n\nCalculate the annual effective rate of interest, as a percentage to 2 decimal places.")
        return Question(
            question_text=q, correct_answer=round((am - 1) * 100, 2), topic=TOPIC, question_type=QTYPE,
            scaffold_steps=[{"prompt": "How many quarters are there in a year?", "answer": 4},
                            {"prompt": "What is the annual multiplier, (quarterly multiplier)^4? (5 d.p.)",
                             "answer": round(am, 5)}],
            worked_solution=[f"Annual multiplier = {_mult(qpct / 100)}^4 = {am:.5f}…",
                             f"Annual effective rate = {_pct(am - 1)}% per year"],
            notes=QUARTERLY_NOTES)
    a = _pick_rate(3.0, 12.0, 0.5)
    qm = (1 + a / 100) ** 0.25
    q = (f"A loan has an annual effective rate of interest of {_rate_str(a)}%.\n\n"
         f"Calculate the quarterly effective rate of interest, as a percentage to 2 decimal places.")
    return Question(
        question_text=q, correct_answer=round((qm - 1) * 100, 2), topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "What power turns an annual multiplier into a quarterly one? (as a decimal)",
                         "answer": 0.25},
                        {"prompt": "What is the quarterly multiplier? (5 d.p.)", "answer": round(qm, 5)}],
        worked_solution=[f"Quarterly multiplier = {_mult(a / 100)}^(1/4) = {qm:.5f}…",
                         f"Quarterly effective rate = {_pct(qm - 1)}% per quarter"],
        notes=QUARTERLY_NOTES)


# (lead, amount lo, hi, step, annual rate lo, hi, is_loan)
_GROWTH_CONTEXTS = [
    ("puts £{A} into a savings account with an annual effective rate of interest of {R}%", 500, 8000, 50, 1.5, 5.5, False),
    ("borrows £{A} on a loan with an annual effective rate of interest of {R}%. No repayments are made", 800, 6000, 100, 6.9, 29.9, True),
]


def generate_effective_rates_l4():
    """Growing an amount for part of a year (annual rate, fractional power; or monthly rate)."""
    name = random.choice(_NAMES)
    if random.random() < 0.7:
        lead, alo, ahi, ast, rlo, rhi, loan = random.choice(_GROWTH_CONTEXTS)
        A = random.randrange(alo, ahi + 1, ast)
        r = _pick_rate(rlo, rhi, 0.1)
        n = random.choice([k for k in range(2, 35) if k % 12])
        val = A * (1 + r / 100) ** (n / 12)
        what = "how much is owed" if loan else "the balance"
        q = (f"{name} {lead.format(A=f'{A:,}', R=_rate_str(r))}.\n\nCalculate {what} after {n} months.")
        power = f"({n}/12)"
        work = f"£{A:,} × {_mult(r / 100)}^{power}"
        steps = [{"prompt": "What power should the annual multiplier be raised to? (as a decimal, 4 d.p.)",
                  "answer": round(n / 12, 4)}]
    else:
        A = random.randrange(300, 5001, 50)
        mp = random.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])
        n = random.randint(5, 30)
        val = A * (1 + mp / 100) ** n
        q = (f"{name} saves £{A:,} in an account paying an effective rate of {_rate_str(mp)}% per month.\n\n"
             f"Calculate the balance after {n} months.")
        work = f"£{A:,} × {_mult(mp / 100)}^{n}"
        steps = [{"prompt": "What is the monthly multiplier?", "answer": round(1 + mp / 100, 6)}]
    ans = round(val, 2)
    return Question(
        question_text=q, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=steps + [{"prompt": "Calculate the amount (£)", "answer": ans}],
        worked_solution=[f"{work} = £{_money(ans)}"], notes=PART_YEAR_NOTES)


_MONTHS = list(calendar.month_name)


def _date(mi):
    y, m = divmod(mi, 12)
    return f"1 {_MONTHS[m + 1]} {y}"


def _last_day(mi):
    y, m = divmod(mi, 12)
    return f"{calendar.monthrange(y, m + 1)[1]} {_MONTHS[m + 1]} {y}"


def generate_effective_rates_l5():
    """A loan's balance through changing rates before repayments start (styled on 2026 Q1)."""
    name = random.choice(_NAMES)
    start = random.randint(2024, 2025) * 12 + random.randint(0, 11)
    lens = [random.randint(2, 6), random.randint(3, 7)]
    lens.append(12 - sum(lens)) if sum(lens) < 11 else lens.append(random.randint(2, 4))
    kinds = random.sample(["year", "year", "month"], 3)
    A = random.randrange(1500, 8001, 250)
    rows, factors, val, mi = [], [], float(A), start
    steps = []
    for L, k in zip(lens, kinds):
        if k == "year":
            r = _pick_rate(5.9, 9.9, 0.1)
            label = f"{_rate_str(r)}% per **year**"
            val *= (1 + r / 100) ** (L / 12)
            factors.append(f"{_mult(r / 100)}^({L}/12)")
        else:
            r = random.choice([0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75])
            label = f"{_rate_str(r)}% per **month**"
            val *= (1 + r / 100) ** L
            factors.append(f"{_mult(r / 100)}^{L}")
        rows.append((f"{_date(mi)} to {_last_day(mi + L - 1)}", label))
        steps.append({"prompt": f"How many months are in the period {_date(mi)} to {_last_day(mi + L - 1)}?", "answer": L})
        mi += L
    end_mi = mi
    table = "| Dates | Interest rate |\n|---|---|\n" + "\n".join(f"| {d} | {r} |" for d, r in rows)
    ans = round(val, 2)
    q = (f"{name} took out a personal loan for £{A:,} on {_date(start)}. They will start making repayments on "
         f"{_date(end_mi)}.\n\nThe effective rates of interest for the loan are as follows:\n\n{table}\n\n"
         f"Calculate the accumulated balance of {name}'s loan on {_last_day(end_mi - 1)}.")
    return Question(
        question_text=q, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=steps + [{"prompt": "Multiply the loan by all of the multipliers (£)", "answer": ans}],
        worked_solution=[f"Months in each period: {', '.join(str(L) for L in lens)}",
                         f"£{A:,} × " + " × ".join(factors) + f" = £{_money(ans)}"],
        notes=LOAN_BEFORE_REPAYMENTS_NOTES)


def generate_effective_rates_question():
    return random.choice([generate_effective_rates_l1, generate_effective_rates_l2, generate_effective_rates_l3,
                          generate_effective_rates_l4, generate_effective_rates_l5])()
