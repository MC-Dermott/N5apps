import random
from core.models.question_model import Question

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


def _gen_params(period):
    return (
        random.choice(_PT[period]),
        random.choice(_UEL[period]),
        random.choice(_RATE_MID_OPTIONS),
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
    )


def _diagram_params(income, pt, uel, rate_mid, rate_top):
    return {"income": income, "pt": pt, "uel": uel,
            "rate_mid": rate_mid, "rate_top": rate_top}


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

def generate_ni_l1():
    period = random.choice(["annual", "monthly", "weekly"])
    pt, uel, rate_mid, rate_top = _gen_params(period)
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
        {"prompt": f"Find how much of {name}'s {pw} income falls in the {rate_mid}% band "
                   f"(earnings above £{pt:,})",
         "answer": float(taxable)},
        {"prompt": f"Calculate {rate_mid}% of that amount to find {pw} NI",
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
            "diagram": "ni_bands",
            "diagram_params": _diagram_params(income, pt, uel, rate_mid, rate_top),
        },
    )


# ===========================================================================
# Level 2 — income above the UEL (two-band calculation)
# ===========================================================================

def generate_ni_l2():
    period = random.choice(["annual", "monthly", "weekly"])
    pt, uel, rate_mid, rate_top = _gen_params(period)
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
        {"prompt": f"Calculate the NI on the middle band: "
                   f"{rate_mid}% on earnings from £{pt:,} to £{uel:,}",
         "answer": float(ni_m)},
        {"prompt": f"Calculate the NI on the upper band: "
                   f"{rate_top}% on earnings above £{uel:,}",
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
            "diagram": "ni_bands",
            "diagram_params": _diagram_params(income, pt, uel, rate_mid, rate_top),
        },
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


def generate_ni_l3():
    period = random.choice(["annual", "monthly", "weekly"])
    pt, uel, rate_mid, rate_top = _gen_params(period)
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
        {"prompt": f"Calculate the NI on the middle band: "
                   f"{rate_mid}% on earnings from £{pt:,} to £{uel:,}",
         "answer": float(ni_m)},
        {"prompt": f"Calculate the NI on the upper band: "
                   f"{rate_top}% on earnings above £{uel:,}",
         "answer": float(ni_top)},
        {"prompt": f"Add both NI amounts to find total {pw} NI",
         "answer": float(ni)},
        {"prompt": f"Calculate {pw} pension: {pension_pct}% of £{income:,}",
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

    return Question(
        question_text=question_text,
        correct_answer=float(result),
        topic="Finance and Statistics",
        question_type="National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_make_notes(pt, uel, rate_mid, rate_top, period),
        metadata={
            "table": _make_table_md(pt, uel, rate_mid, rate_top, period),
            "diagram": "ni_bands",
            "diagram_params": _diagram_params(income, pt, uel, rate_mid, rate_top),
        },
    )


# ===========================================================================
# Default dispatcher
# ===========================================================================

def generate_ni_question():
    return generate_ni_l1()
