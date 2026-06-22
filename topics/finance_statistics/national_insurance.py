import random
from core.models.question_model import Question

_PT_OPTIONS       = [10_000, 11_000, 12_000, 13_000]
_UEL_OPTIONS      = list(range(45_000, 56_000, 1_000))
_RATE_MID_OPTIONS = [10, 11, 12, 13]
_RATE_TOP_OPTIONS = [2, 3, 4]
_PENSION_PCTS     = [3, 4, 5, 6, 7, 8]

_NAMES = [
    "David", "Sarah", "Michael", "Emma", "James",
    "Jessica", "Robert", "Laura", "Andrew", "Rachel",
    "Fraser", "Catriona", "Callum", "Eilidh", "Morag", "Alasdair",
]


def _gen_bands():
    return (
        random.choice(_PT_OPTIONS),
        random.choice(_UEL_OPTIONS),
        random.choice(_RATE_MID_OPTIONS),
        random.choice(_RATE_TOP_OPTIONS),
    )


def _ni_mid(pt, uel, rate_mid):
    return rate_mid * (uel - pt) // 100


def _make_table_md(pt, uel, rate_mid, rate_top):
    return (
        "| Annual Income | National Insurance Rate |\n"
        "|:---|:---|\n"
        f"| Up to £{pt:,} | 0% |\n"
        f"| £{pt:,} to £{uel:,} | {rate_mid}% |\n"
        f"| Over £{uel:,} | {rate_top}% (on earnings above £{uel:,} only) |\n"
    )


def _make_notes(pt, uel, rate_mid, rate_top):
    ni_m = _ni_mid(pt, uel, rate_mid)
    return (
        f"**National Insurance (NI):**\n\n"
        f"NI is a tax on earnings above a minimum threshold.\n\n"
        f"**If annual income is between £{pt:,} and £{uel:,} (Level 1):**\n"
        f"- NI = {rate_mid}% × (income − £{pt:,})\n\n"
        f"**If annual income is above £{uel:,} (Levels 2 & 3):**\n"
        f"- NI on middle band = {rate_mid}% × (£{uel:,} − £{pt:,}) = "
        f"{rate_mid}% × £{uel - pt:,} = **£{ni_m:,}**\n"
        f"- NI on upper band = {rate_top}% × (income − £{uel:,})\n"
        f"- **Total NI = £{ni_m:,} + upper band NI**\n\n"
        f"**Level 3 — Net Pay:**\n"
        f"- Annual net pay = Gross pay − NI − Pension − Income Tax\n"
        f"- Monthly net pay = Annual net pay ÷ 12\n"
        f"- Weekly net pay = Annual net pay ÷ 52\n"
    )


def _diagram_params(income, pt, uel, rate_mid, rate_top):
    return {"income": income, "pt": pt, "uel": uel,
            "rate_mid": rate_mid, "rate_top": rate_top}


def _period_label(period):
    return {"annual": "per year", "monthly": "per month", "weekly": "per week"}[period]


def _period_multiplier(period):
    return {"annual": 1, "monthly": 12, "weekly": 52}[period]


def _gen_l1_income(pt, uel):
    """Return (period, income_annual, income_display) with income_annual in (pt, uel)."""
    for _ in range(30):
        period = random.choice(["annual", "monthly", "weekly"])
        if period == "annual":
            k_opts = [k for k in range(2, 50) if pt + k * 1000 < uel]
            if k_opts:
                k_nice = [k for k in k_opts if k % 5 == 0]
                k = random.choice(k_nice or k_opts)
                annual = pt + k * 1000
                return "annual", annual, annual
        elif period == "monthly":
            # monthly = m*100, annual = m*1200; need pt < m*1200 < uel
            lo = pt // 1200 + 1
            hi = (uel - 1) // 1200
            if lo <= hi:
                m = random.choice(range(lo, hi + 1))
                return "monthly", m * 1200, m * 100
        else:
            # weekly = w*50, annual = w*2600; need pt < w*2600 < uel
            lo = pt // 2600 + 1
            hi = (uel - 1) // 2600
            if lo <= hi:
                w = random.choice(range(lo, hi + 1))
                return "weekly", w * 2600, w * 50
    # fallback to annual
    k_opts = [k for k in range(2, 50) if pt + k * 1000 < uel]
    k = random.choice(k_opts)
    return "annual", pt + k * 1000, pt + k * 1000


def _gen_l2_income(uel):
    """Return (period, income_annual, income_display) with income_annual > uel."""
    for _ in range(30):
        period = random.choice(["annual", "monthly", "weekly"])
        if period == "annual":
            j = random.choice(range(5, 36, 5))
            return "annual", uel + j * 1000, uel + j * 1000
        elif period == "monthly":
            lo = uel // 1200 + 1
            hi = lo + 15
            m = random.choice(range(lo, hi + 1))
            return "monthly", m * 1200, m * 100
        else:
            lo = uel // 2600 + 1
            hi = lo + 10
            w = random.choice(range(lo, hi + 1))
            return "weekly", w * 2600, w * 50
    return "annual", uel + 10_000, uel + 10_000


# ===========================================================================
# Level 1 — income in the middle band only
# ===========================================================================

def generate_ni_l1():
    pt, uel, rate_mid, rate_top = _gen_bands()
    period, income, display = _gen_l1_income(pt, uel)
    taxable = income - pt
    ni = rate_mid * taxable // 100
    name = random.choice(_NAMES)
    mult = _period_multiplier(period)
    plbl = _period_label(period)

    question_text = (
        f"Use the table above to calculate {name}'s annual National Insurance contributions. "
        f"{name} earns £{display:,} {plbl}."
    )

    scaffold_steps = []
    if period != "annual":
        scaffold_steps.append({
            "prompt": f"Convert {name}'s {period} income to an annual figure (multiply by {mult})",
            "answer": float(income),
        })
    scaffold_steps += [
        {"prompt": f"Find how much of {name}'s annual income falls in the {rate_mid}% band "
                   f"(earnings above £{pt:,})",
         "answer": float(taxable)},
        {"prompt": f"Calculate {rate_mid}% of that amount to find the total annual NI",
         "answer": float(ni)},
    ]

    worked = []
    if period != "annual":
        worked.append(f"Annual income = £{display:,} × {mult} = £{income:,}")
    worked += [
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
        notes=_make_notes(pt, uel, rate_mid, rate_top),
        metadata={
            "table": _make_table_md(pt, uel, rate_mid, rate_top),
            "diagram": "ni_bands",
            "diagram_params": _diagram_params(income, pt, uel, rate_mid, rate_top),
        },
    )


# ===========================================================================
# Level 2 — income above the UEL
# ===========================================================================

def generate_ni_l2():
    pt, uel, rate_mid, rate_top = _gen_bands()
    period, income, display = _gen_l2_income(uel)
    ni_m = _ni_mid(pt, uel, rate_mid)
    ni_top = rate_top * (income - uel) // 100
    ni = ni_m + ni_top
    name = random.choice(_NAMES)
    mult = _period_multiplier(period)
    plbl = _period_label(period)

    question_text = (
        f"Use the table above to calculate {name}'s annual National Insurance contributions. "
        f"{name} earns £{display:,} {plbl}."
    )

    scaffold_steps = []
    if period != "annual":
        scaffold_steps.append({
            "prompt": f"Convert {name}'s {period} income to an annual figure (multiply by {mult})",
            "answer": float(income),
        })
    scaffold_steps += [
        {"prompt": f"Calculate the NI on the middle band: "
                   f"{rate_mid}% on earnings from £{pt:,} to £{uel:,}",
         "answer": float(ni_m)},
        {"prompt": f"Calculate the NI on the upper band: "
                   f"{rate_top}% on earnings above £{uel:,}",
         "answer": float(ni_top)},
        {"prompt": "Add both amounts to find the total annual NI",
         "answer": float(ni)},
    ]

    worked = []
    if period != "annual":
        worked.append(f"Annual income = £{display:,} × {mult} = £{income:,}")
    worked += [
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
        notes=_make_notes(pt, uel, rate_mid, rate_top),
        metadata={
            "table": _make_table_md(pt, uel, rate_mid, rate_top),
            "diagram": "ni_bands",
            "diagram_params": _diagram_params(income, pt, uel, rate_mid, rate_top),
        },
    )


# ===========================================================================
# Level 3 — monthly or weekly net pay
# ===========================================================================

def _l3_params(pt, uel, rate_mid, rate_top):
    ni_m = _ni_mid(pt, uel, rate_mid)

    for _ in range(500):
        j           = random.choice(range(5, 36, 5))
        income      = uel + j * 1000
        ni_top      = rate_top * j * 10
        ni          = ni_m + ni_top
        pension_pct = random.choice(_PENSION_PCTS)
        pension     = round(pension_pct / 100 * income)
        subtotal    = income - ni - pension

        ask_monthly = random.choice([True, False])
        divisor     = 12 if ask_monthly else 52
        step        = 50 if ask_monthly else 10
        lo          = 1500 if ask_monthly else 350
        hi          = 4500 if ask_monthly else 1050

        min_tax = int(0.08 * income)
        max_tax = int(0.28 * income)

        k_min = max(lo, (subtotal - max_tax + divisor - 1) // divisor)
        k_max = min(hi, (subtotal - min_tax) // divisor)
        if k_min > k_max:
            continue

        k_snap_min = ((k_min + step - 1) // step) * step
        k_snap_max = (k_max // step) * step
        if k_snap_min > k_snap_max:
            continue

        target = random.choice(range(k_snap_min, k_snap_max + 1, step))
        tax    = subtotal - divisor * target
        if not (min_tax <= tax <= max_tax):
            continue

        return {
            "income": income, "ni_top": ni_top, "ni": ni, "ni_m": ni_m,
            "pension_pct": pension_pct, "pension": pension, "tax": tax,
            "net_annual": divisor * target, "net_period": target,
            "ask_monthly": ask_monthly, "divisor": divisor,
        }
    return None


def generate_ni_l3():
    pt, uel, rate_mid, rate_top = _gen_bands()
    p = _l3_params(pt, uel, rate_mid, rate_top)
    if p is None:
        raise RuntimeError("Could not generate valid Level 3 NI question parameters")

    # Choose how income is stated
    period = random.choice(["annual", "monthly", "weekly"])
    income      = p["income"]
    mult        = _period_multiplier(period)
    plbl        = _period_label(period)
    display     = income if period == "annual" else income // mult

    name        = random.choice(_NAMES)
    ni_m        = p["ni_m"]
    ni_top      = p["ni_top"]
    ni          = p["ni"]
    pension_pct = p["pension_pct"]
    pension     = p["pension"]
    tax         = p["tax"]
    net_annual  = p["net_annual"]
    net_period  = p["net_period"]
    divisor     = p["divisor"]
    pay_period  = "monthly" if p["ask_monthly"] else "weekly"

    if period == "annual":
        income_phrase = f"a gross annual salary of £{income:,}"
    else:
        income_phrase = f"a gross {period} salary of £{display:,}"

    question_text = (
        f"{name} has {income_phrase}. "
        f"They pay National Insurance (as shown in the table above), "
        f"a pension contribution of {pension_pct}% of their gross annual salary, "
        f"and income tax of £{tax:,} per year. "
        f"Calculate {name}'s {pay_period} net pay."
    )

    scaffold_steps = []
    if period != "annual":
        scaffold_steps.append({
            "prompt": f"Convert {name}'s {period} salary to an annual figure (multiply by {mult})",
            "answer": float(income),
        })
    scaffold_steps += [
        {"prompt": f"Calculate the NI on the middle band: "
                   f"{rate_mid}% on earnings from £{pt:,} to £{uel:,}",
         "answer": float(ni_m)},
        {"prompt": f"Calculate the NI on the upper band: "
                   f"{rate_top}% on earnings above £{uel:,}",
         "answer": float(ni_top)},
        {"prompt": "Add both NI amounts to find total annual NI",
         "answer": float(ni)},
        {"prompt": f"Calculate annual pension: {pension_pct}% of £{income:,}",
         "answer": float(pension)},
        {"prompt": "Calculate annual net pay (gross − NI − pension − income tax)",
         "answer": float(net_annual)},
        {"prompt": f"Divide by {divisor} to find {pay_period} net pay",
         "answer": float(net_period)},
    ]

    worked = []
    if period != "annual":
        worked.append(f"Annual salary = £{display:,} × {mult} = £{income:,}")
    worked += [
        f"Middle band ({rate_mid}%): £{uel:,} − £{pt:,} = £{uel - pt:,}",
        f"NI on middle band = {rate_mid}% × £{uel - pt:,} = £{ni_m:,}",
        f"Upper band ({rate_top}%): £{income:,} − £{uel:,} = £{income - uel:,}",
        f"NI on upper band = {rate_top}% × £{income - uel:,} = £{ni_top:,}",
        f"Total NI = £{ni_m:,} + £{ni_top:,} = £{ni:,}",
        f"Pension = {pension_pct}% × £{income:,} = £{pension:,}",
        f"Annual net pay = £{income:,} − £{ni:,} − £{pension:,} − £{tax:,} = £{net_annual:,}",
        f"{pay_period.capitalize()} net pay = £{net_annual:,} ÷ {divisor} = £{net_period:,}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(net_period),
        topic="Finance and Statistics",
        question_type="National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_make_notes(pt, uel, rate_mid, rate_top),
        metadata={
            "table": _make_table_md(pt, uel, rate_mid, rate_top),
            "diagram": "ni_bands",
            "diagram_params": _diagram_params(income, pt, uel, rate_mid, rate_top),
        },
    )


# ===========================================================================
# Default dispatcher
# ===========================================================================

def generate_ni_question():
    return generate_ni_l1()
