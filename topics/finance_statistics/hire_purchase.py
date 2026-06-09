import random
from core.models.question_model import Question

NOTES = """
**Hire Purchase:**

Hire purchase (HP) lets you buy an item by paying:
1. A **deposit** upfront (a percentage of the cash price, or a fixed amount)
2. Fixed **monthly installments** over a set number of months

**Level 1:**
Total HP price = deposit + (monthly installment × number of months)

Rearrangements:
- Monthly installment = (total HP price − deposit) ÷ number of months
- Deposit = total HP price − (monthly installment × number of months)

**Level 2:**
Total HP price = deposit + (monthly installment × number of months) + final installment

Rearrangements:
- Monthly installment = (total HP price − deposit − final installment) ÷ number of months
- Final installment = total HP price − deposit − (monthly installment × number of months)

HP always costs **more** than the cash price.
"""

# Items with realistic cash price ranges (multiples of 20 keep deposit % as whole £)
_ITEMS = [
    ("A television",              [400, 600, 800, 1000, 1200]),
    ("A laptop",                  [400, 600, 800, 1000, 1200]),
    ("A washing machine",         [400, 600, 800, 1000]),
    ("A fridge-freezer",          [400, 600, 800, 1000]),
    ("A sofa",                    [600, 800, 1000, 1200, 1400]),
    ("A games console",           [200, 400, 600]),
    ("A mobile phone",            [400, 600, 800, 1000]),
    ("A dishwasher",              [400, 600, 800]),
    ("A tumble dryer",            [400, 600, 800]),
    ("A tablet computer",         [200, 400, 600, 800]),
    ("A treadmill",               [600, 800, 1000, 1200]),
    ("A set of garden furniture", [400, 600, 800, 1000]),
]

_DEPOSIT_PCTS = [10, 15, 20, 25, 30]
_MONTHS       = [12, 18, 24, 36, 48]

# Level 2: number of regular monthly installments (final installment is separate)
_L2_REGULAR_MONTHS = [11, 23, 35, 47]


def _pick_item():
    name, prices = random.choice(_ITEMS)
    return name, random.choice(prices)


def _realistic_monthly(deposit, months, cash):
    """Return a monthly installment that makes total HP between 15% and 45% above cash."""
    premium   = random.uniform(0.15, 0.45)
    target_hp = cash * (1 + premium)
    raw       = (target_hp - deposit) / months
    monthly   = max(5, round(raw / 5) * 5)
    if deposit + monthly * months <= cash:
        monthly += 5
    return monthly


def _l2_installments(deposit, reg_months, cash):
    """Return (monthly, final, total_hp) for Level 2 questions. Final differs from monthly."""
    premium   = random.uniform(0.15, 0.45)
    target_hp = cash * (1 + premium)
    remaining = target_hp - deposit
    raw       = remaining / (reg_months + 1)
    monthly   = max(15, round(raw / 5) * 5)

    delta = random.choice([-40, -30, -20, -10, 10, 20, 30, 40, 50])
    final = max(10, round((monthly + delta) / 5) * 5)
    if final == monthly:
        final = monthly + 10

    total_hp = deposit + reg_months * monthly + final
    if total_hp <= cash:
        monthly += 5
        total_hp = deposit + reg_months * monthly + final

    return monthly, final, total_hp


# ===========================================================================
# LEVEL 1
# ===========================================================================

# ---------------------------------------------------------------------------
# L1 Type A — Find monthly installment (deposit as % of cash price)
# ---------------------------------------------------------------------------

def _l1_monthly_from_pct():
    item, cash = _pick_item()
    pct        = random.choice(_DEPOSIT_PCTS)
    deposit    = cash * pct // 100
    months     = random.choice(_MONTHS)
    monthly    = _realistic_monthly(deposit, months, cash)
    total_hp   = deposit + monthly * months

    question_text = (
        f"{item} has a cash price of £{cash:,}. "
        f"It can be bought on hire purchase by paying a deposit of {pct}% of the cash price "
        f"and then equal monthly installments over {months} months. "
        f"The total hire purchase price is £{total_hp:,}. "
        f"Calculate the monthly installment."
    )

    scaffold_steps = [
        {"prompt": "Calculate the deposit",
         "answer": float(deposit)},
        {"prompt": "Find the amount left to pay after the deposit",
         "answer": float(total_hp - deposit)},
        {"prompt": "Divide by the number of months to find each installment",
         "answer": float(monthly)},
    ]

    worked = [
        f"Deposit = {pct}% of £{cash:,} = £{deposit:,}",
        f"Amount remaining = £{total_hp:,} − £{deposit:,} = £{total_hp - deposit:,}",
        f"Monthly installment = £{total_hp - deposit:,} ÷ {months} = £{monthly:.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(monthly),
        topic="Finance and Statistics",
        question_type="Hire Purchase",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# L1 Type B — Find monthly installment (deposit as fixed £ amount)
# ---------------------------------------------------------------------------

def _l1_monthly_from_fixed_deposit():
    item, cash = _pick_item()
    dep_pct = random.uniform(0.10, 0.30)
    deposit = round(cash * dep_pct / 5) * 5
    months  = random.choice(_MONTHS)
    monthly = _realistic_monthly(deposit, months, cash)
    total_hp = deposit + monthly * months

    question_text = (
        f"{item} has a cash price of £{cash:,}. "
        f"It can be bought on hire purchase by paying a deposit of £{deposit:,} "
        f"and then equal monthly installments over {months} months. "
        f"The total hire purchase price is £{total_hp:,}. "
        f"Calculate the monthly installment."
    )

    scaffold_steps = [
        {"prompt": "Find the amount left to pay after the deposit",
         "answer": float(total_hp - deposit)},
        {"prompt": "Divide by the number of months to find each installment",
         "answer": float(monthly)},
    ]

    worked = [
        f"Amount remaining = £{total_hp:,} − £{deposit:,} = £{total_hp - deposit:,}",
        f"Monthly installment = £{total_hp - deposit:,} ÷ {months} = £{monthly:.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(monthly),
        topic="Finance and Statistics",
        question_type="Hire Purchase",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# L1 Type C — Find the deposit
# ---------------------------------------------------------------------------

def _l1_find_deposit():
    item, cash = _pick_item()
    months   = random.choice(_MONTHS)
    dep_pct  = random.uniform(0.10, 0.30)
    deposit  = round(cash * dep_pct / 5) * 5
    monthly  = _realistic_monthly(deposit, months, cash)
    total_hp = deposit + monthly * months

    question_text = (
        f"{item} has a cash price of £{cash:,}. "
        f"It can be bought on hire purchase by paying a deposit "
        f"and then {months} monthly installments of £{monthly:.2f}. "
        f"The total hire purchase price is £{total_hp:,}. "
        f"Calculate the deposit."
    )

    scaffold_steps = [
        {"prompt": "Find the total amount paid in monthly installments",
         "answer": float(monthly * months)},
        {"prompt": "Subtract from the total HP price to find the deposit",
         "answer": float(deposit)},
    ]

    worked = [
        f"Total installments = £{monthly:.2f} × {months} = £{monthly * months:.2f}",
        f"Deposit = £{total_hp:,} − £{monthly * months:.2f} = £{deposit:.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(deposit),
        topic="Finance and Statistics",
        question_type="Hire Purchase",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# L1 Type D — Find the total HP price
# ---------------------------------------------------------------------------

def _l1_find_total_hp():
    item, cash = _pick_item()
    use_pct  = random.choice([True, False])
    months   = random.choice(_MONTHS)

    if use_pct:
        pct      = random.choice(_DEPOSIT_PCTS)
        deposit  = cash * pct // 100
        dep_text = f"a deposit of {pct}% of the cash price"
    else:
        dep_pct  = random.uniform(0.10, 0.30)
        deposit  = round(cash * dep_pct / 5) * 5
        dep_text = f"a deposit of £{deposit:,}"

    monthly  = _realistic_monthly(deposit, months, cash)
    total_hp = deposit + monthly * months
    extra    = total_hp - cash

    question_text = (
        f"{item} has a cash price of £{cash:,}. "
        f"It can be bought on hire purchase by paying {dep_text} "
        f"and then {months} monthly installments of £{monthly:.2f}. "
        f"Calculate the total hire purchase price and find how much more "
        f"this costs than the cash price."
    )

    if use_pct:
        scaffold_steps = [
            {"prompt": "Calculate the deposit",
             "answer": float(deposit)},
            {"prompt": "Find the total amount paid in monthly installments",
             "answer": float(monthly * months)},
            {"prompt": "Add the deposit to find the total HP price",
             "answer": float(total_hp)},
            {"prompt": "Find how much more the HP price is than the cash price",
             "answer": float(extra)},
        ]
        worked = [
            f"Deposit = {pct}% of £{cash:,} = £{deposit:,}",
            f"Total installments = £{monthly:.2f} × {months} = £{monthly * months:.2f}",
            f"Total HP price = £{deposit:,} + £{monthly * months:.2f} = £{total_hp:.2f}",
            f"Extra cost = £{total_hp:.2f} − £{cash:,} = £{extra:.2f}",
        ]
    else:
        scaffold_steps = [
            {"prompt": "Find the total amount paid in monthly installments",
             "answer": float(monthly * months)},
            {"prompt": "Add the deposit to find the total HP price",
             "answer": float(total_hp)},
            {"prompt": "Find how much more the HP price is than the cash price",
             "answer": float(extra)},
        ]
        worked = [
            f"Total installments = £{monthly:.2f} × {months} = £{monthly * months:.2f}",
            f"Total HP price = £{deposit:,} + £{monthly * months:.2f} = £{total_hp:.2f}",
            f"Extra cost = £{total_hp:.2f} − £{cash:,} = £{extra:.2f}",
        ]

    return Question(
        question_text=question_text,
        correct_answer=float(total_hp),
        topic="Finance and Statistics",
        question_type="Hire Purchase",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_hire_purchase_l1():
    return random.choice([
        _l1_monthly_from_pct,
        _l1_monthly_from_fixed_deposit,
        _l1_find_deposit,
        _l1_find_total_hp,
    ])()


# ===========================================================================
# LEVEL 2 — includes a final installment different from the monthly amount
# ===========================================================================

# ---------------------------------------------------------------------------
# L2 Type A — Find the total HP price
# ---------------------------------------------------------------------------

def _l2_find_total_hp():
    item, cash  = _pick_item()
    pct         = random.choice(_DEPOSIT_PCTS)
    deposit     = cash * pct // 100
    reg_months  = random.choice(_L2_REGULAR_MONTHS)
    monthly, final, total_hp = _l2_installments(deposit, reg_months, cash)
    extra = total_hp - cash

    question_text = (
        f"{item} has a cash price of £{cash:,}. "
        f"It can be bought on hire purchase by paying a deposit of {pct}% of the cash price, "
        f"then {reg_months} monthly installments of £{monthly:.2f}, "
        f"followed by a final installment of £{final:.2f}. "
        f"Calculate the total hire purchase price and find how much more "
        f"this costs than the cash price."
    )

    scaffold_steps = [
        {"prompt": "Calculate the deposit",
         "answer": float(deposit)},
        {"prompt": "Find the total of the monthly installments",
         "answer": float(monthly * reg_months)},
        {"prompt": "Add the deposit, monthly total, and final installment to get the total HP price",
         "answer": float(total_hp)},
        {"prompt": "Find how much more the HP price is than the cash price",
         "answer": float(extra)},
    ]

    worked = [
        f"Deposit = {pct}% of £{cash:,} = £{deposit:,}",
        f"Monthly total = £{monthly:.2f} × {reg_months} = £{monthly * reg_months:.2f}",
        f"Total HP price = £{deposit:,} + £{monthly * reg_months:.2f} + £{final:.2f} = £{total_hp:.2f}",
        f"Extra cost = £{total_hp:.2f} − £{cash:,} = £{extra:.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(total_hp),
        topic="Finance and Statistics",
        question_type="Hire Purchase",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# L2 Type B — Find the monthly installment
# ---------------------------------------------------------------------------

def _l2_find_monthly():
    item, cash  = _pick_item()
    pct         = random.choice(_DEPOSIT_PCTS)
    deposit     = cash * pct // 100
    reg_months  = random.choice(_L2_REGULAR_MONTHS)
    monthly, final, total_hp = _l2_installments(deposit, reg_months, cash)

    question_text = (
        f"{item} has a cash price of £{cash:,}. "
        f"It can be bought on hire purchase by paying a deposit of {pct}% of the cash price, "
        f"then {reg_months} equal monthly installments, "
        f"followed by a final installment of £{final:.2f}. "
        f"The total hire purchase price is £{total_hp:,}. "
        f"Calculate the monthly installment."
    )

    after_deposit = total_hp - deposit
    after_final   = after_deposit - final

    scaffold_steps = [
        {"prompt": "Calculate the deposit",
         "answer": float(deposit)},
        {"prompt": "Subtract the deposit from the total HP price",
         "answer": float(after_deposit)},
        {"prompt": "Subtract the final installment to find the amount covered by monthly installments",
         "answer": float(after_final)},
        {"prompt": "Divide by the number of monthly installments",
         "answer": float(monthly)},
    ]

    worked = [
        f"Deposit = {pct}% of £{cash:,} = £{deposit:,}",
        f"After deposit: £{total_hp:,} − £{deposit:,} = £{after_deposit:,}",
        f"After final installment: £{after_deposit:,} − £{final:.2f} = £{after_final:.2f}",
        f"Monthly installment = £{after_final:.2f} ÷ {reg_months} = £{monthly:.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(monthly),
        topic="Finance and Statistics",
        question_type="Hire Purchase",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# L2 Type C — Find the final installment
# ---------------------------------------------------------------------------

def _l2_find_final():
    item, cash  = _pick_item()
    pct         = random.choice(_DEPOSIT_PCTS)
    deposit     = cash * pct // 100
    reg_months  = random.choice(_L2_REGULAR_MONTHS)
    monthly, final, total_hp = _l2_installments(deposit, reg_months, cash)

    question_text = (
        f"{item} has a cash price of £{cash:,}. "
        f"It can be bought on hire purchase by paying a deposit of {pct}% of the cash price, "
        f"then {reg_months} monthly installments of £{monthly:.2f}, "
        f"followed by a final installment. "
        f"The total hire purchase price is £{total_hp:,}. "
        f"Calculate the final installment."
    )

    monthly_total = monthly * reg_months

    scaffold_steps = [
        {"prompt": "Calculate the deposit",
         "answer": float(deposit)},
        {"prompt": "Find the total of the monthly installments",
         "answer": float(monthly_total)},
        {"prompt": "Subtract the deposit and monthly total from the HP price to find the final installment",
         "answer": float(final)},
    ]

    worked = [
        f"Deposit = {pct}% of £{cash:,} = £{deposit:,}",
        f"Monthly total = £{monthly:.2f} × {reg_months} = £{monthly_total:.2f}",
        f"Final installment = £{total_hp:,} − £{deposit:,} − £{monthly_total:.2f} = £{final:.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(final),
        topic="Finance and Statistics",
        question_type="Hire Purchase",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_hire_purchase_l2():
    return random.choice([
        _l2_find_total_hp,
        _l2_find_monthly,
        _l2_find_final,
    ])()


# ===========================================================================
# N4 — Find monthly installment (fixed deposit given)
# ===========================================================================

_N4_ITEMS = [
    ("A television",      [200, 400, 600]),
    ("A laptop",          [400, 600, 800]),
    ("A washing machine", [400, 600]),
    ("A games console",   [200, 400]),
    ("A mobile phone",    [400, 600]),
    ("A tablet computer", [200, 400]),
]

_N4_MONTHS = [12, 24]


def generate_hire_purchase_question_n4():
    name, prices = random.choice(_N4_ITEMS)
    cash    = random.choice(prices)
    dep_pct = random.choice([0.10, 0.20, 0.25])
    deposit = round(cash * dep_pct / 5) * 5
    months  = random.choice(_N4_MONTHS)
    monthly = _realistic_monthly(deposit, months, cash)
    total_hp = deposit + monthly * months

    question_text = (
        f"{name} has a cash price of £{cash:,}. "
        f"It can be bought on hire purchase by paying a deposit of £{deposit:,} "
        f"and then equal monthly installments over {months} months. "
        f"The total hire purchase price is £{total_hp:,}. "
        f"Calculate the monthly installment."
    )

    scaffold_steps = [
        {"prompt": "Find the amount left to pay after the deposit",
         "answer": float(total_hp - deposit)},
        {"prompt": "Divide by the number of months to find each installment",
         "answer": float(monthly)},
    ]

    worked = [
        f"Amount remaining = £{total_hp:,} − £{deposit:,} = £{total_hp - deposit:,}",
        f"Monthly installment = £{total_hp - deposit:,} ÷ {months} = £{monthly:.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(monthly),
        topic="Finance and Statistics",
        question_type="Hire Purchase",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ===========================================================================
# Dispatcher (no level selected → Level 1)
# ===========================================================================

def generate_hire_purchase_question():
    return generate_hire_purchase_l1()
