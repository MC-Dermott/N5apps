import random
from core.models.question_model import Question
from core.models.distractors import distractors

# Thresholds are in the income's own period. All values are multiples of £100
# so that NI = rate * (income - PT) / 100 is always a whole number for any
# integer rate (including 11% and 13% where gcd(100, rate) = 1, which requires
# the taxable amount to be divisible by 100).
_PT = {
    "annual":  [10_000, 11_000, 12_000, 13_000],
    "monthly": [800, 900, 1_000, 1_100],
    "weekly":  [200],               # £200/wk ≈ £10,400/yr
}
_UEL = {
    "annual":  list(range(45_000, 56_000, 1_000)),
    "monthly": [3_600, 3_800, 4_000, 4_200, 4_400, 4_600],
    "weekly":  [800, 900, 1_000],   # diffs vs PT: 600, 700, 800 — all ÷ 100 ✓
}
_RATE_MID_OPTIONS = [10, 11, 12, 13]
_RATE_MID_OPTIONS_CALC = [10]   # single-digit-or-10 only, so rate × taxable ÷ 100 is non-calc-safe
_RATE_TOP_OPTIONS = [2, 3, 4]
_PENSION_PCTS     = [3, 4, 5, 6, 7, 8]

_NAMES = [
    "David", "Sarah", "Michael", "Emma", "James",
    "Jessica", "Robert", "Laura", "Andrew", "Rachel",
    "Fraser", "Catriona", "Callum", "Eilidh", "Morag", "Alasdair",
]

_PERIOD_LABEL = {"annual": "per year", "monthly": "per month", "weekly": "per week"}
_PERIOD_WORD  = {"annual": "annual",   "monthly": "monthly",   "weekly": "weekly"}
_INCOME_WORD  = {"annual": "Annual",   "monthly": "Monthly",   "weekly": "Weekly"}


def _gen_params(period, calc_mode=False):
    return (
        random.choice(_PT[period]),
        random.choice(_UEL[period]),
        random.choice(_RATE_MID_OPTIONS_CALC if calc_mode else _RATE_MID_OPTIONS),
        random.choice(_RATE_TOP_OPTIONS),
    )


def _ni_mid(pt, uel, rate_mid):
    """NI on the middle band (always a whole number given the threshold constraints)."""
    return rate_mid * (uel - pt) // 100


def _make_table_md(pt, uel, rate_mid, rate_top, period):
    hdr = _INCOME_WORD[period]
    return (
        f"| {hdr} Income | National Insurance Rate |\n"
        "|:---|:---|\n"
        f"| Up to £{pt:,} | 0% |\n"
        f"| £{pt:,} to £{uel:,} | {rate_mid}% |\n"
        f"| Over £{uel:,} | {rate_top}% (on earnings above £{uel:,} only) |\n"
    )


def _make_notes(pt, uel, rate_mid, rate_top, period):
    return _make_notes_core(pt, uel, rate_mid, rate_top, period) + "\n" + WORKSHEET_EXAMPLES


def _make_notes_core(pt, uel, rate_mid, rate_top, period):
    ni_m = _ni_mid(pt, uel, rate_mid)
    pw   = _PERIOD_WORD[period]
    return (
        f"**National Insurance (NI):**\n\n"
        f"NI is calculated on {pw} earnings above a lower threshold.\n\n"
        f"**If {pw} income is between £{pt:,} and £{uel:,} (Level 1):**\n"
        f"- NI = {rate_mid}% × (income − £{pt:,})\n\n"
        f"**If {pw} income is above £{uel:,} (Levels 2 & 3):**\n"
        f"- NI on middle band = {rate_mid}% × (£{uel:,} − £{pt:,}) = "
        f"{rate_mid}% × £{uel - pt:,} = **£{ni_m:,}**\n"
        f"- NI on upper band = {rate_top}% × (income − £{uel:,})\n"
        f"- **Total NI = £{ni_m:,} + upper band NI**\n\n"
        f"**Level 3 — Net Pay:**\n"
        f"- Net pay = Gross pay − NI − Pension − Income Tax\n"
        + ("- Monthly net pay = Annual net pay ÷ 12\n"
           "- Weekly net pay = Annual net pay ÷ 52\n"
           if period == "annual" else "")
        + (
            "\n**Example:** Monthly income £5,000. PT = £1,000, UEL = £4,000, "
            "mid rate 10%, upper rate 2%.\n"
            "- NI on middle band = 10% × (£4,000 − £1,000) = £300\n"
            "- NI on upper band = 2% × (£5,000 − £4,000) = £20\n"
            "- Total NI = £300 + £20 = **£320**\n"
        )
    )


# The worked examples on Income_Tax_and_National_Insurance_Worksheet.docx (N5 Apps/Worksheets/
# Finance and Statistics), word for word, with the course-report common errors under each.
WORKSHEET_EXAMPLES = """
**Worked examples (from the worksheet)** — rates: 0% up to £12,584; 8% from £12,584 to £50,284;
2% over £50,284.

**Example:** Isla earns £38,500 per year. Calculate her annual National Insurance.
- Pay above £12,584 = 38,500 − 12,584 = 25,916
- NI = 8% × 25,916 = **£2,073.28**

⚠ Don't ignore the 0% band — 8% of the whole pay lost marks in 2024, 2025 and 2026.

**Example:** Donald earns £56,400 per year. Calculate his annual National Insurance.
- 8% band: 50,284 − 12,584 = 37,700;  8% × 37,700 = £3,016.00
- 2% band: 56,400 − 50,284 = 6,116;  2% × 6,116 = £122.32
- Total NI = £3,016.00 + £122.32 = **£3,138.32**

⚠ Pay that goes over the upper limit caused problems in 2023 — split it into bands first.

**Example:** Akira earns £33,800 per year. She pays 6.5% of her gross salary into her pension. Her
annual income tax is £4,246.00. She is paid weekly. Calculate her weekly net pay.
- NI = 8% × (33,800 − 12,584) = 8% × 21,216 = £1,697.28
- Pension = 6.5% × 33,800 = £2,197.00
- Net pay = 33,800 − £1,697.28 − £2,197.00 − £4,246.00 = £25,659.72
- Weekly net pay = £25,659.72 ÷ 52 = **£493.46**

⚠ The pension is a percentage of the **gross** pay — working it out after taking off the NI cost
marks in 2023, 2024, 2025 and 2026 (course reports).
"""


def _diagram_params(income, pt, uel, rate_mid, rate_top):
    bands = [
        ("0%", 0, pt, 0),
        (f"{rate_mid}%", pt, uel, rate_mid),
        (f"{rate_top}%", uel, None, rate_top),
    ]
    return {
        "diagram": "tax_bands",
        "diagram_params": {
            "bands": bands,
            "max_income": max(income * 1.12, uel * 1.35),
            "initial_income": income,
        },
    }


def _gen_l1_income(period, pt, uel):
    """Income (in period units) strictly between pt and uel, multiples of £100 (or £1000 annual)."""
    step = 1_000 if period == "annual" else 100
    lo = pt // step + 1
    hi = (uel - 1) // step
    valid = list(range(lo, hi + 1))
    if period == "annual":
        nice = [k for k in valid if k % 5 == 0]
        valid = nice or valid
    k = random.choice(valid)
    return k * step


def _gen_l2_income(period, uel):
    """Income (in period units) strictly above uel, multiples of £100 (or £1000 annual)."""
    step = 1_000 if period == "annual" else 100
    if period == "annual":
        j = random.choice(range(5, 36, 5))
    else:
        j = random.choice(range(1, 11))
    return uel + j * step


# ===========================================================================
# Level 1 — income in the middle (rate_mid%) band only
# ===========================================================================

def generate_ni_l1(calc_mode=False):
    period = random.choice(["annual", "monthly", "weekly"])
    pt, uel, rate_mid, rate_top = _gen_params(period, calc_mode)
    income  = _gen_l1_income(period, pt, uel)
    taxable = income - pt
    ni      = rate_mid * taxable // 100
    name    = random.choice(_NAMES)
    pw      = _PERIOD_WORD[period]
    plbl    = _PERIOD_LABEL[period]

    question_text = (
        f"Use the table above to calculate {name}'s {pw} National Insurance contributions. "
        f"{name} earns £{income:,} {plbl}."
    )

    scaffold_steps = [
        {"prompt": f"Find how much of {name}'s {pw} income is above the lower threshold in the table",
         "answer": float(taxable)},
        {"prompt": f"Apply the band's NI rate from the table to that amount to find {pw} NI",
         "answer": float(ni)},
    ]

    worked = [
        f"Income above £{pt:,} = £{income:,} − £{pt:,} = £{taxable:,}",
        f"NI = {rate_mid}% × £{taxable:,} = £{ni:,}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(ni),
        topic="Finance and Statistics",
        question_type="National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_make_notes(pt, uel, rate_mid, rate_top, period),
        metadata={
            "table": _make_table_md(pt, uel, rate_mid, rate_top, period),
            **_diagram_params(income, pt, uel, rate_mid, rate_top),
        },
        distractors=distractors(float(ni), [
            (round(rate_mid * income / 100, 2), f"you ignored the 0% band — only the pay above £{pt:,} is "
                                                f"charged (2024, 2025 and 2026 course reports)."),
        ]),
    )


# ===========================================================================
# Level 2 — income above the UEL (two-band calculation)
# ===========================================================================

def generate_ni_l2(calc_mode=False):
    period = random.choice(["annual", "monthly", "weekly"])
    pt, uel, rate_mid, rate_top = _gen_params(period, calc_mode)
    income  = _gen_l2_income(period, uel)
    ni_m    = _ni_mid(pt, uel, rate_mid)
    ni_top  = rate_top * (income - uel) // 100
    ni      = ni_m + ni_top
    name    = random.choice(_NAMES)
    pw      = _PERIOD_WORD[period]
    plbl    = _PERIOD_LABEL[period]

    question_text = (
        f"Use the table above to calculate {name}'s {pw} National Insurance contributions. "
        f"{name} earns £{income:,} {plbl}."
    )

    scaffold_steps = [
        {"prompt": "Calculate the NI on the middle band, using the middle band rate on earnings "
                   "between the lower threshold and the upper limit in the table",
         "answer": float(ni_m)},
        {"prompt": "Calculate the NI on the upper band, using the upper band rate on earnings "
                   "above the upper limit in the table",
         "answer": float(ni_top)},
        {"prompt": f"Add both amounts to find total {pw} NI",
         "answer": float(ni)},
    ]

    worked = [
        f"Middle band ({rate_mid}%): £{uel:,} − £{pt:,} = £{uel - pt:,}",
        f"NI on middle band = {rate_mid}% × £{uel - pt:,} = £{ni_m:,}",
        f"Upper band ({rate_top}%): £{income:,} − £{uel:,} = £{income - uel:,}",
        f"NI on upper band = {rate_top}% × £{income - uel:,} = £{ni_top:,}",
        f"Total NI = £{ni_m:,} + £{ni_top:,} = £{ni:,}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(ni),
        topic="Finance and Statistics",
        question_type="National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_make_notes(pt, uel, rate_mid, rate_top, period),
        metadata={
            "table": _make_table_md(pt, uel, rate_mid, rate_top, period),
            **_diagram_params(income, pt, uel, rate_mid, rate_top),
        },
        distractors=distractors(float(ni), [
            (round(rate_mid * (income - pt) / 100, 2),
             f"you charged {rate_mid}% on everything above £{pt:,} — the pay above £{uel:,} is charged at "
             f"{rate_top}% (2023 course report)."),
            (float(ni_m), f"that's only the {rate_mid}% band — add the {rate_top}% on the pay above £{uel:,}."),
            (round(rate_mid * income / 100, 2), f"you ignored the 0% band and the upper band."),
        ]),
    )


# ===========================================================================
# Level 3 — net pay
#
# Annual income: final step divides annual net by 12 or 52 (tests an extra skill).
# Monthly/weekly income: everything stays in that period — no final division.
# ===========================================================================

def _l3_params(pt, uel, rate_mid, rate_top, period):
    ni_m = _ni_mid(pt, uel, rate_mid)

    # For annual: result is monthly or weekly net (divide at end).
    # For monthly/weekly: result is already the period net (no divide).
    if period == "annual":
        ask_monthly  = random.choice([True, False])
        result_per   = "monthly" if ask_monthly else "weekly"
        divisor      = 12 if ask_monthly else 52
        result_step  = 50 if ask_monthly else 10
        result_lo    = 1_500 if ask_monthly else 350
        result_hi    = 4_500 if ask_monthly else 1_050
    else:
        result_per   = period
        divisor      = 1
        result_step  = 50
        result_lo    = 1_500 if period == "monthly" else 350
        result_hi    = 4_500 if period == "monthly" else 1_000

    for _ in range(500):
        if period == "annual":
            j      = random.choice(range(5, 36, 5))
            income = uel + j * 1_000
        else:
            j      = random.choice(range(1, 11))
            income = uel + j * 100

        ni_top      = rate_top * (income - uel) // 100
        ni          = ni_m + ni_top
        pension_pct = random.choice(_PENSION_PCTS)
        pension     = round(pension_pct / 100 * income)
        subtotal    = income - ni - pension

        min_tax = int(0.08 * income)
        max_tax = int(0.28 * income)

        if divisor > 1:
            k_min = max(result_lo, (subtotal - max_tax + divisor - 1) // divisor)
            k_max = min(result_hi, (subtotal - min_tax) // divisor)
            if k_min > k_max:
                continue
            k_snap_min = ((k_min + result_step - 1) // result_step) * result_step
            k_snap_max = (k_max // result_step) * result_step
            if k_snap_min > k_snap_max:
                continue
            result = random.choice(range(k_snap_min, k_snap_max + 1, result_step))
            tax    = subtotal - divisor * result
            net_in_period_units = subtotal - tax   # = divisor * result (annual net)
        else:
            net_min = max(result_lo, subtotal - max_tax)
            net_max = min(result_hi, subtotal - min_tax)
            if net_min > net_max:
                continue
            n_snap_min = ((net_min + result_step - 1) // result_step) * result_step
            n_snap_max = (net_max // result_step) * result_step
            if n_snap_min > n_snap_max:
                continue
            result = random.choice(range(n_snap_min, n_snap_max + 1, result_step))
            tax    = subtotal - result
            net_in_period_units = result

        if not (min_tax <= tax <= max_tax):
            continue

        return {
            "income": income, "ni_top": ni_top, "ni": ni, "ni_m": ni_m,
            "pension_pct": pension_pct, "pension": pension, "tax": tax,
            "net_in_period_units": net_in_period_units,
            "result": result,
            "result_per": result_per,
            "divisor": divisor,
        }
    return None


def generate_ni_l3(calc_mode=False):
    # "annual" forces a final ÷12 or ÷52 step to reach monthly/weekly net pay — not
    # non-calc-safe, so calc_mode restricts to periods needing no such division.
    period = random.choice(["monthly", "weekly"]) if calc_mode else random.choice(["annual", "monthly", "weekly"])
    pt, uel, rate_mid, rate_top = _gen_params(period, calc_mode)
    p = _l3_params(pt, uel, rate_mid, rate_top, period)
    if p is None:
        raise RuntimeError("Could not generate valid Level 3 NI question parameters")

    name        = random.choice(_NAMES)
    income      = p["income"]
    ni_m        = p["ni_m"]
    ni_top      = p["ni_top"]
    ni          = p["ni"]
    pension_pct = p["pension_pct"]
    pension     = p["pension"]
    tax         = p["tax"]
    net_units   = p["net_in_period_units"]
    result      = p["result"]
    result_per  = p["result_per"]
    divisor     = p["divisor"]
    pw          = _PERIOD_WORD[period]
    plbl        = _PERIOD_LABEL[period]

    if period == "annual":
        salary_phrase = f"a gross annual salary of £{income:,}"
        tax_phrase    = f"income tax of £{tax:,} per year"
    else:
        salary_phrase = f"a gross {pw} salary of £{income:,}"
        tax_phrase    = f"income tax of £{tax:,} {plbl}"

    question_text = (
        f"{name} has {salary_phrase}. "
        f"They pay National Insurance (as shown in the table above), "
        f"a pension contribution of {pension_pct}% of their gross {pw} salary, "
        f"and {tax_phrase}. "
        f"Calculate {name}'s {result_per} net pay."
    )

    scaffold_steps = [
        {"prompt": "Calculate the NI on the middle band, using the middle band rate on earnings "
                   "between the lower threshold and the upper limit in the table",
         "answer": float(ni_m)},
        {"prompt": "Calculate the NI on the upper band, using the upper band rate on earnings "
                   "above the upper limit in the table",
         "answer": float(ni_top)},
        {"prompt": f"Add both NI amounts to find total {pw} NI",
         "answer": float(ni)},
        {"prompt": f"Calculate {pw} pension (pension percentage of gross {pw} salary)",
         "answer": float(pension)},
        {"prompt": f"Calculate {pw} net pay (gross − NI − pension − income tax)",
         "answer": float(net_units)},
    ]

    if divisor > 1:
        scaffold_steps.append({
            "prompt": f"Divide by {divisor} to find {result_per} net pay",
            "answer": float(result),
        })

    worked = [
        f"Middle band ({rate_mid}%): £{uel:,} − £{pt:,} = £{uel - pt:,}",
        f"NI on middle band = {rate_mid}% × £{uel - pt:,} = £{ni_m:,}",
        f"Upper band ({rate_top}%): £{income:,} − £{uel:,} = £{income - uel:,}",
        f"NI on upper band = {rate_top}% × £{income - uel:,} = £{ni_top:,}",
        f"Total NI = £{ni_m:,} + £{ni_top:,} = £{ni:,}",
        f"Pension = {pension_pct}% × £{income:,} = £{pension:,}",
        f"{pw.capitalize()} net pay = £{income:,} − £{ni:,} − £{pension:,} − £{tax:,} = £{net_units:,}",
    ]
    if divisor > 1:
        worked.append(
            f"{result_per.capitalize()} net pay = £{net_units:,} ÷ {divisor} = £{result:,}"
        )

    wrong = []
    pen_after = round(pension_pct / 100 * (income - ni))
    net_after = income - ni - pen_after - tax
    wrong.append((round(net_after / divisor, 2),
                  "you worked out the pension AFTER taking off the National Insurance — it's a percentage "
                  "of the gross pay (2023–2026 course reports)."))
    if divisor > 1:
        other = 52 if divisor == 12 else 12
        wrong.append((round(net_units / other, 2), f"you divided by {other} — {result_per} pay means "
                                                   f"÷ {divisor}."))
        wrong.append((float(net_units), f"that's the annual net pay — divide by {divisor} for {result_per} "
                                        f"pay."))
    return Question(
        distractors=distractors(float(result), wrong),
        question_text=question_text,
        correct_answer=float(result),
        topic="Finance and Statistics",
        question_type="National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_make_notes(pt, uel, rate_mid, rate_top, period),
        metadata={
            "table": _make_table_md(pt, uel, rate_mid, rate_top, period),
            **_diagram_params(income, pt, uel, rate_mid, rate_top),
        },
    )


# ===========================================================================
# Default dispatcher
# ===========================================================================

# ===========================================================================
# Level 4 — income tax from given bands (worksheet Section 3)
# ===========================================================================

_TAX_PA, _TAX_TOP, _TAX_BASIC, _TAX_HIGHER = 12_570, 50_270, 20, 40


def _tax_table_md():
    return (
        "| Annual taxable income | Income tax rate |\n|:---|:---|\n"
        f"| Up to £{_TAX_PA:,} (personal allowance) | 0% |\n"
        f"| £{_TAX_PA + 1:,} to £{_TAX_TOP:,} | {_TAX_BASIC}% |\n"
        f"| Over £{_TAX_TOP:,} | {_TAX_HIGHER}% |\n"
    )


TAX_NOTES = """
**Income tax from given bands:** take off the personal allowance (taxed at 0%), then charge each band.

**Example (from the worksheet):** Mairi earns £34,200 per year. Use the income tax bands to calculate
her annual income tax.
- Taxable income = 34,200 − 12,570 = 21,630
- Income tax = 20% × 21,630 = **£4,326.00**

⚠ Don't tax the whole salary — the personal allowance is tax-free (the same slip as ignoring the 0%
band for National Insurance).
"""


def generate_ni_l4(calc_mode=False):
    name = random.choice(_NAMES)
    two_bands = random.random() < 0.35
    if calc_mode:
        salary = random.choice(range(22_570, 48_571, 1_000))     # taxable = whole thousands
        two_bands = False
    elif two_bands:
        salary = random.choice(range(52_000, 90_001, 100))
    else:
        salary = random.choice(range(16_000, 50_001, 10))
    if salary <= _TAX_TOP:
        taxable = salary - _TAX_PA
        tax = round(taxable * _TAX_BASIC / 100, 2)
        worked = [f"Taxable income = £{salary:,} − £{_TAX_PA:,} = £{taxable:,}",
                  f"Income tax = {_TAX_BASIC}% × £{taxable:,} = £{tax:,.2f}"]
        steps = [{"prompt": "Taxable income (salary − personal allowance)", "answer": float(taxable)},
                 {"prompt": f"Income tax ({_TAX_BASIC}% of the taxable income)", "answer": tax}]
        wrong = [(round(salary * _TAX_BASIC / 100, 2), "you taxed the whole salary — the personal allowance "
                                                       "is tax-free.")]
    else:
        basic = _TAX_TOP - _TAX_PA
        t1 = round(basic * _TAX_BASIC / 100, 2)
        higher = salary - _TAX_TOP
        t2 = round(higher * _TAX_HIGHER / 100, 2)
        tax = round(t1 + t2, 2)
        worked = [f"{_TAX_BASIC}% band: £{_TAX_TOP:,} − £{_TAX_PA:,} = £{basic:,};  {_TAX_BASIC}% × £{basic:,} = £{t1:,.2f}",
                  f"{_TAX_HIGHER}% band: £{salary:,} − £{_TAX_TOP:,} = £{higher:,};  {_TAX_HIGHER}% × £{higher:,} = £{t2:,.2f}",
                  f"Income tax = £{t1:,.2f} + £{t2:,.2f} = £{tax:,.2f}"]
        steps = [{"prompt": f"Tax in the {_TAX_BASIC}% band", "answer": t1},
                 {"prompt": f"Tax in the {_TAX_HIGHER}% band", "answer": t2},
                 {"prompt": "Total income tax", "answer": tax}]
        wrong = [(round((salary - _TAX_PA) * _TAX_BASIC / 100, 2),
                  f"you charged {_TAX_BASIC}% on everything — the pay over £{_TAX_TOP:,} is taxed at {_TAX_HIGHER}%."),
                 (round((salary - _TAX_PA) * _TAX_HIGHER / 100, 2),
                  f"you charged {_TAX_HIGHER}% on everything — only the pay over £{_TAX_TOP:,} is taxed at "
                  f"{_TAX_HIGHER}%.")]
    return Question(
        question_text=f"{name} earns £{salary:,} per year. Use the income tax bands above to calculate "
                      f"{name}'s annual income tax.",
        correct_answer=tax,
        topic="Finance and Statistics",
        question_type="National Insurance",
        scaffold_steps=steps,
        worked_solution=worked,
        notes=TAX_NOTES,
        metadata={"table": _tax_table_md()},
        distractors=distractors(tax, wrong),
    )


def generate_ni_question(calc_mode=False):
    return random.choice([generate_ni_l1, generate_ni_l2, generate_ni_l3, generate_ni_l4])(calc_mode=calc_mode)
