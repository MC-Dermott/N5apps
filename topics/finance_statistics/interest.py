import calendar
import math
import random
from core.models.question_model import Question

NOTES = """
**Changing Interest Rates:**

A savings account can have **different effective interest rates** over
different date ranges, and rates may be quoted **per month** or **per year**.

1. Work out how many months a deposit is held for **within each rate period**
2. If the rate is **per month**, compound it once for every month held:
   balance × (1 + rate)^(months held)
3. If the rate is **per year**:
   - For each **whole year** held, compound once: balance × (1 + rate)^(whole years)
   - For any **part of a year** left over, apply it once, proportionally:
     balance × (1 + rate × months/12)
4. Carry the running balance forward into the next rate period

**Example:** £1000 held for 9 months at 4.7% per year (less than a full year):
- Balance = £1000 × (1 + 0.047 × 9/12) = **£1035.25**

If more than one deposit is made, grow **each deposit separately** from its
own deposit date to the final date, then **add the grown amounts together**.
"""

MIN_DEPOSIT_NOTES = """
**Finding the Minimum Deposit for a Savings Goal:**

This is the reverse of growing a deposit forward: instead of growing a known
deposit to find the balance, you're given the **target balance** and need to
find the **deposit** that would grow to it.

1. Calculate the **growth multiplier** — what £1 would grow to over the
   period, using the effective interest rate(s) that apply
2. **Divide** the savings goal by this multiplier
3. **Round UP** to the nearest penny — rounding down would leave the goal
   just short

**Example:** £1 grows to £1.0532 over the period. Savings goal is £6000.
- Minimum deposit = £6000 ÷ 1.0532 = £5699.9367...
- Round UP to the nearest penny = **£5699.94**
"""

_NAMES = ["Alex", "Jamie", "Sam", "Jordan", "Casey", "Morgan", "Riley", "Taylor"]

_YEAR_RATES = [1.2, 1.5, 1.7, 2.0, 2.3, 2.6, 3.0, 3.2, 3.5, 4.0, 4.2, 4.5, 4.7, 5.0]
_MONTH_RATES = [0.1, 0.11, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.415, 0.45, 0.5]


def _ym_to_mi(year, month):
    return year * 12 + (month - 1)


def _mi_to_ym(mi):
    year, m0 = divmod(mi, 12)
    return year, m0 + 1


def _fmt_rate(pct):
    return f"{pct:g}"


def _fmt_money(x):
    return f"{x:,.2f}"


def _date_str(year, month, day=1):
    return f"{day} {calendar.month_name[month]} {year}"


def _last_day_str(year, month):
    last_day = calendar.monthrange(year, month)[1]
    return _date_str(year, month, last_day)


def _build_rate_periods(start_mi, offsets):
    """Given month offsets marking the start of each rate period (offsets[0] == 0),
    randomly assign a rate/type to each period and build both the internal
    period list (for calculation) and the display rows (for the table)."""
    n_periods = len(offsets)
    periods = []
    rows = []
    for i in range(n_periods):
        rtype = random.choices(["year", "month"], weights=[70, 30])[0]
        rate_pct = random.choice(_YEAR_RATES if rtype == "year" else _MONTH_RATES)
        rate = rate_pct / 100
        p_start = offsets[i]
        p_end = offsets[i + 1] if i < n_periods - 1 else None
        periods.append((p_start, p_end, rate, rtype))

        y1, m1 = _mi_to_ym(start_mi + p_start)
        if p_end is not None:
            y2, m2 = _mi_to_ym(start_mi + p_end - 1)
            date_range = f"{_date_str(y1, m1)} to {_last_day_str(y2, m2)}"
        else:
            date_range = f"From {_date_str(y1, m1)}"
        rate_label = f"{_fmt_rate(rate_pct)}% per **{rtype}**"
        rows.append((date_range, rate_label))
    return periods, rows


def _rate_table_md(rows):
    lines = ["| Dates | Interest rate |", "|---|---|"]
    for date_range, rate_label in rows:
        lines.append(f"| {date_range} | {rate_label} |")
    return "\n".join(lines)


def _grow_amount_with_steps(amount, start_month, end_month, periods):
    """Grow `amount`, held from month offset `start_month` to `end_month`,
    through the given rate periods. Returns (final_balance, worked_lines,
    running_balance_after_each_applied_step)."""
    balance = amount
    lines = []
    step_answers = []
    for p_start, p_end, rate, rtype in periods:
        seg_start = max(start_month, p_start)
        seg_end = end_month if p_end is None else min(end_month, p_end)
        n_months = seg_end - seg_start
        if n_months <= 0:
            continue

        if rtype == "month":
            before = balance
            balance = balance * (1 + rate) ** n_months
            lines.append(
                f"£{_fmt_money(before)} × (1 + {_fmt_rate(rate * 100)}%)^{n_months} "
                f"= £{_fmt_money(balance)}"
            )
            step_answers.append(round(balance, 2))
        else:
            whole_years, rem_months = divmod(n_months, 12)
            if whole_years:
                before = balance
                balance = balance * (1 + rate) ** whole_years
                lines.append(
                    f"£{_fmt_money(before)} × (1 + {_fmt_rate(rate * 100)}%)^{whole_years} "
                    f"= £{_fmt_money(balance)}"
                )
            if rem_months:
                before = balance
                balance = balance * (1 + rate * (rem_months / 12))
                lines.append(
                    f"£{_fmt_money(before)} × (1 + {_fmt_rate(rate * 100)}% × {rem_months}/12) "
                    f"= £{_fmt_money(balance)}"
                )
            step_answers.append(round(balance, 2))

    return balance, lines, step_answers


def _random_start():
    start_year = random.randint(2021, 2023)
    start_month = random.randint(1, 12)
    return start_year, start_month, _ym_to_mi(start_year, start_month)


def _random_period_offsets():
    n_periods = random.choices([2, 3], weights=[30, 70])[0]
    durations = [random.choice(range(2, 12)) for _ in range(n_periods - 1)]
    offsets = [0]
    for dur in durations:
        offsets.append(offsets[-1] + dur)
    return offsets


# ---------------------------------------------------------------------------
# Level 1 — a single deposit
# ---------------------------------------------------------------------------

def generate_interest_l1():
    name = random.choice(_NAMES)
    start_year, start_month, start_mi = _random_start()
    offsets = _random_period_offsets()
    target_offset = offsets[-1] + random.randint(6, 30)

    periods, rows = _build_rate_periods(start_mi, offsets)
    table_md = _rate_table_md(rows)

    start_str = _date_str(start_year, start_month)
    ty, tm = _mi_to_ym(start_mi + target_offset)
    target_str = _date_str(ty, tm)

    deposit = random.choice(range(1000, 9001, 250))

    question_text = (
        f"{name} deposited £{deposit:,} in a savings account on {start_str}.\n\n"
        f"The effective rates of interest for the savings account are as follows:\n\n"
        f"{table_md}\n\n"
        f"Calculate {name}'s balance on {target_str}."
    )

    balance, lines, step_answers = _grow_amount_with_steps(deposit, 0, target_offset, periods)
    answer = round(balance, 2)

    scaffold_steps = [
        {
            "prompt": f"Apply the interest for stage {i + 1} of the calculation (carry your balance forward)",
            "answer": val,
        }
        for i, val in enumerate(step_answers)
    ]

    worked = lines + [f"Balance on {target_str} = £{_fmt_money(answer)}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Finance",
        question_type="Interest",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 2 — an initial deposit plus one or more additional deposits
# ---------------------------------------------------------------------------

def generate_interest_l2():
    name = random.choice(_NAMES)
    start_year, start_month, start_mi = _random_start()
    offsets = _random_period_offsets()
    target_offset = offsets[-1] + random.randint(8, 30)

    periods, rows = _build_rate_periods(start_mi, offsets)
    table_md = _rate_table_md(rows)

    start_str = _date_str(start_year, start_month)
    ty, tm = _mi_to_ym(start_mi + target_offset)
    target_str = _date_str(ty, tm)

    initial_deposit = random.choice(range(200, 2001, 50))

    n_extra = random.choices([1, 2], weights=[50, 50])[0]
    available = list(range(2, max(3, target_offset - 1)))
    n_extra = min(n_extra, len(available)) or 1
    extra_offsets = sorted(random.sample(available, n_extra))
    extra_amounts = [random.choice(range(100, 501, 50)) for _ in extra_offsets]

    deposits = [(0, initial_deposit)] + list(zip(extra_offsets, extra_amounts))

    deposit_lines = []
    for off, amt in deposits[1:]:
        dy, dm = _mi_to_ym(start_mi + off)
        deposit_lines.append(f"£{amt:,} on {_date_str(dy, dm)}")

    if len(deposit_lines) == 1:
        deposits_sentence = f"{name} makes a further deposit of {deposit_lines[0]}."
    else:
        deposits_sentence = (
            f"{name} makes further deposits of "
            + ", ".join(deposit_lines[:-1])
            + f" and {deposit_lines[-1]}."
        )

    question_text = (
        f"{name} opens a savings account on {start_str} with an initial deposit of £{initial_deposit:,}.\n\n"
        f"The effective rates of interest for the savings account are as follows:\n\n"
        f"{table_md}\n\n"
        f"{deposits_sentence}\n\n"
        f"Calculate the balance in {name}'s savings account on {target_str}."
    )

    scaffold_steps = []
    worked = []
    total = 0.0
    for idx, (off, amt) in enumerate(deposits):
        grown, lines, _ = _grow_amount_with_steps(amt, off, target_offset, periods)
        total += grown
        if idx == 0:
            deposit_label = f"initial deposit of £{amt:,}"
        else:
            dy, dm = _mi_to_ym(start_mi + off)
            deposit_label = f"deposit of £{amt:,} made on {_date_str(dy, dm)}"

        scaffold_steps.append({
            "prompt": f"Calculate how much the {deposit_label} grows to by {target_str}",
            "answer": round(grown, 2),
        })
        worked.append(f"Growth of the {deposit_label}:")
        worked.extend(f"  {line}" for line in lines)
        worked.append(f"  → grows to £{_fmt_money(grown)}")

    answer = round(total, 2)
    scaffold_steps.append({
        "prompt": "Add the grown amounts together to find the total balance",
        "answer": answer,
    })
    worked.append(f"Total balance on {target_str} = £{_fmt_money(answer)}")

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Finance",
        question_type="Interest",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 3 — minimum deposit required to reach a savings goal
# ---------------------------------------------------------------------------

def generate_interest_l3():
    name = random.choice(_NAMES)
    start_year, start_month, start_mi = _random_start()
    offsets = _random_period_offsets()
    periods, rows = _build_rate_periods(start_mi, offsets)
    table_md = _rate_table_md(rows)

    open_offset = offsets[-1]
    target_offset = open_offset + random.randint(12, 36)

    oy, om = _mi_to_ym(start_mi + open_offset)
    open_str = _date_str(oy, om)
    ty, tm = _mi_to_ym(start_mi + target_offset)
    target_str = _date_str(ty, tm)

    goal = random.choice(range(2000, 15001, 500))

    multiplier, lines, _ = _grow_amount_with_steps(1, open_offset, target_offset, periods)
    exact_deposit = goal / multiplier
    min_deposit = math.ceil(exact_deposit * 100 - 1e-9) / 100

    question_text = (
        f"{name} opened a savings account on {open_str}.\n\n"
        f"The effective rates of interest for the savings account are as follows:\n\n"
        f"{table_md}\n\n"
        f"{name} has a savings goal of £{goal:,} by {target_str}.\n\n"
        f"Calculate the minimum deposit {name} should have made on {open_str} "
        f"to achieve this savings goal."
    )

    scaffold_steps = [
        {
            "prompt": f"Calculate the growth multiplier for £1 held from {open_str} to {target_str}",
            "answer": round(multiplier, 4),
        },
        {
            "prompt": "Divide the savings goal by this multiplier, then round UP to the nearest penny",
            "answer": min_deposit,
        },
    ]

    worked = lines + [
        f"£1 grows to £{_fmt_money(multiplier)} by {target_str}",
        f"£{goal:,} ÷ {_fmt_money(multiplier)} = £{_fmt_money(exact_deposit)}",
        f"Minimum deposit (rounded up to the nearest penny) = £{_fmt_money(min_deposit)}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=min_deposit,
        topic="Finance",
        question_type="Interest",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=MIN_DEPOSIT_NOTES,
    )


def generate_interest_question():
    return random.choice([generate_interest_l1, generate_interest_l2, generate_interest_l3])()
