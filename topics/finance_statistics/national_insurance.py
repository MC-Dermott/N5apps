import random
from core.models.question_model import Question

_PT  = 12570   # Primary Threshold (below → 0%, above → 12%)
_UEL = 50270   # Upper Earnings Limit (above → 2%)

_NI_TABLE_MD = """\
| Annual Income | National Insurance Rate |
|:---|:---|
| Up to £12,570 | 0% |
| £12,571 to £50,270 | 12% |
| Over £50,270 | 2% (on earnings above £50,270 only) |
"""

NOTES = """
**National Insurance (NI):**

NI is a tax on earnings above a minimum threshold.

**If annual income is between £12,570 and £50,270 (Level 1):**
- NI = 12% × (income − £12,570)

**If annual income is above £50,270 (Levels 2 & 3):**
- NI on middle band = 12% × (£50,270 − £12,570) = 12% × £37,700 = **£4,524**
- NI on upper band = 2% × (income − £50,270)
- **Total NI = £4,524 + upper band NI**

**Level 3 — Net Pay:**
- Annual net pay = Gross pay − NI − Pension − Income Tax
- Monthly net pay = Annual net pay ÷ 12
- Weekly net pay = Annual net pay ÷ 52
"""

_NAMES = [
    "David", "Sarah", "Michael", "Emma", "James",
    "Jessica", "Robert", "Laura", "Andrew", "Rachel",
    "Fraser", "Catriona", "Callum", "Eilidh", "Morag", "Alasdair",
]

# L1: income = PT + k*1000; NI = 12% × k*1000 = 120k → always whole pounds
_L1_K = [5, 10, 15, 20, 25, 30, 35]

# L2/L3: income = UEL + j*1000; upper-band NI = 2% × j*1000 = 20j → always whole pounds
_L2_J = [5, 10, 15, 20, 25, 30]

_PENSION_PCTS = [3, 4, 5, 6, 7, 8]

_NI_MID = int(round(0.12 * (_UEL - _PT)))   # 4524, fixed for any L2/L3 question


def _ni_l2(income):
    return _NI_MID + int(round(0.02 * (income - _UEL)))


# ===========================================================================
# Level 1 — income in the 12% band only
# ===========================================================================

def generate_ni_l1():
    k       = random.choice(_L1_K)
    income  = _PT + k * 1000
    taxable = k * 1000
    ni      = 12 * k * 10        # = 120k, always integer
    name    = random.choice(_NAMES)

    question_text = (
        f"Use the table above to calculate {name}'s annual National Insurance contributions. "
        f"{name} earns £{income:,} per year."
    )

    scaffold_steps = [
        {"prompt": f"Find how much of {name}'s income falls in the 12% band "
                   f"(earnings above £{_PT:,})",
         "answer": float(taxable)},
        {"prompt": "Calculate 12% of that amount to find the total NI",
         "answer": float(ni)},
    ]

    worked = [
        f"Income above £{_PT:,} = £{income:,} − £{_PT:,} = £{taxable:,}",
        f"NI = 12% × £{taxable:,} = £{ni:,}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(ni),
        topic="Finance and Statistics",
        question_type="National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={"table": _NI_TABLE_MD},
    )


# ===========================================================================
# Level 2 — income above the UEL (two-band calculation)
# ===========================================================================

def generate_ni_l2():
    j      = random.choice(_L2_J)
    income = _UEL + j * 1000
    ni_top = 20 * j              # 2% × j*1000, always integer
    ni     = _NI_MID + ni_top
    name   = random.choice(_NAMES)

    question_text = (
        f"Use the table above to calculate {name}'s annual National Insurance contributions. "
        f"{name} earns £{income:,} per year."
    )

    scaffold_steps = [
        {"prompt": f"Calculate the NI on the middle band: "
                   f"12% on earnings from £{_PT:,} to £{_UEL:,}",
         "answer": float(_NI_MID)},
        {"prompt": f"Calculate the NI on the upper band: "
                   f"2% on earnings above £{_UEL:,}",
         "answer": float(ni_top)},
        {"prompt": "Add both amounts to find the total annual NI",
         "answer": float(ni)},
    ]

    worked = [
        f"Middle band (12%): £{_UEL:,} − £{_PT:,} = £{_UEL - _PT:,}",
        f"NI on middle band = 12% × £{_UEL - _PT:,} = £{_NI_MID:,}",
        f"Upper band (2%): £{income:,} − £{_UEL:,} = £{income - _UEL:,}",
        f"NI on upper band = 2% × £{income - _UEL:,} = £{ni_top:,}",
        f"Total NI = £{_NI_MID:,} + £{ni_top:,} = £{ni:,}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(ni),
        topic="Finance and Statistics",
        question_type="National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={"table": _NI_TABLE_MD},
    )


# ===========================================================================
# Level 3 — monthly or weekly net pay (NI + pension % + income tax £)
# ===========================================================================

def _l3_params():
    """Return parameters for a valid L3 question with a whole-pound net pay per period."""
    for _ in range(500):
        j           = random.choice(_L2_J)
        income      = _UEL + j * 1000
        pension_pct = random.choice(_PENSION_PCTS)
        pension     = round(pension_pct / 100 * income)   # whole pounds
        ni_top      = 20 * j
        ni          = _NI_MID + ni_top
        subtotal    = income - ni - pension               # whole pounds

        ask_monthly = random.choice([True, False])
        divisor     = 12 if ask_monthly else 52
        step        = 50 if ask_monthly else 10
        lo          = 1500 if ask_monthly else 350
        hi          = 4500 if ask_monthly else 1050

        # Income tax should be roughly 8–28% of gross
        min_tax = int(0.08 * income)
        max_tax = int(0.28 * income)

        # net_period = target; tax = subtotal - divisor*target
        # → divisor*target = subtotal - tax → target in [(subtotal-max_tax)/div, (subtotal-min_tax)/div]
        k_min = max(lo, (subtotal - max_tax + divisor - 1) // divisor)
        k_max = min(hi, (subtotal - min_tax) // divisor)
        if k_min > k_max:
            continue

        # Snap to step multiples within range
        k_snap_min = ((k_min + step - 1) // step) * step
        k_snap_max = (k_max // step) * step
        if k_snap_min > k_snap_max:
            continue

        target = random.choice(range(k_snap_min, k_snap_max + 1, step))
        tax    = subtotal - divisor * target
        if not (min_tax <= tax <= max_tax):
            continue

        return {
            "income":      income,
            "ni_top":      ni_top,
            "ni":          ni,
            "pension_pct": pension_pct,
            "pension":     pension,
            "tax":         tax,
            "net_annual":  divisor * target,
            "net_period":  target,
            "ask_monthly": ask_monthly,
            "divisor":     divisor,
        }

    return None


def generate_ni_l3():
    p = _l3_params()
    if p is None:
        raise RuntimeError("Could not generate valid Level 3 NI question parameters")

    name        = random.choice(_NAMES)
    income      = p["income"]
    ni_top      = p["ni_top"]
    ni          = p["ni"]
    pension_pct = p["pension_pct"]
    pension     = p["pension"]
    tax         = p["tax"]
    net_annual  = p["net_annual"]
    net_period  = p["net_period"]
    divisor     = p["divisor"]
    period_name = "monthly" if p["ask_monthly"] else "weekly"

    question_text = (
        f"{name} has a gross annual salary of £{income:,}. "
        f"They pay National Insurance (as shown in the table above), "
        f"a pension contribution of {pension_pct}% of their gross salary, "
        f"and income tax of £{tax:,} per year. "
        f"Calculate {name}'s {period_name} net pay."
    )

    scaffold_steps = [
        {"prompt": f"Calculate the NI on the middle band: "
                   f"12% on earnings from £{_PT:,} to £{_UEL:,}",
         "answer": float(_NI_MID)},
        {"prompt": f"Calculate the NI on the upper band: "
                   f"2% on earnings above £{_UEL:,}",
         "answer": float(ni_top)},
        {"prompt": "Add both NI amounts to find total annual NI",
         "answer": float(ni)},
        {"prompt": f"Calculate annual pension: {pension_pct}% of £{income:,}",
         "answer": float(pension)},
        {"prompt": "Calculate annual net pay (gross − NI − pension − income tax)",
         "answer": float(net_annual)},
        {"prompt": f"Divide by {divisor} to find {period_name} net pay",
         "answer": float(net_period)},
    ]

    worked = [
        f"Middle band (12%): £{_UEL:,} − £{_PT:,} = £{_UEL - _PT:,}",
        f"NI on middle band = 12% × £{_UEL - _PT:,} = £{_NI_MID:,}",
        f"Upper band (2%): £{income:,} − £{_UEL:,} = £{income - _UEL:,}",
        f"NI on upper band = 2% × £{income - _UEL:,} = £{ni_top:,}",
        f"Total NI = £{_NI_MID:,} + £{ni_top:,} = £{ni:,}",
        f"Pension = {pension_pct}% × £{income:,} = £{pension:,}",
        f"Annual net pay = £{income:,} − £{ni:,} − £{pension:,} − £{tax:,} = £{net_annual:,}",
        f"{period_name.capitalize()} net pay = £{net_annual:,} ÷ {divisor} = £{net_period:,}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(net_period),
        topic="Finance and Statistics",
        question_type="National Insurance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={"table": _NI_TABLE_MD},
    )


# ===========================================================================
# Default dispatcher (no level selected → Level 1)
# ===========================================================================

def generate_ni_question():
    return generate_ni_l1()
