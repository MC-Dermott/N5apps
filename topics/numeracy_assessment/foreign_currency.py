import random
from core.models.question_model import Question

NOTES_L1 = """
**Currency Exchange:**

An exchange rate tells you how many units of a foreign currency you get for £1.

- **Pounds → foreign currency:** multiply by the rate.
- **Foreign currency → pounds:** divide by the rate.

**Example:** £1 = €1.15. Convert £60 into euros.
- €amount = £60 × 1.15 = **€69.00**
"""

NOTES_L2 = """
**Changing, Spending, and Changing Back:**

1. Convert the starting pounds into the foreign currency (× rate).
2. Subtract however much was spent.
3. Convert what's left back into pounds (÷ rate).
"""

NOTES_L3 = """
**Foreign Currency Exchange (with a bank restriction):**

1. Calculate total spent: daily spend × number of days
2. Find remaining foreign currency: starting amount − total spent
3. Round **down** to the nearest multiple the bank accepts
4. Convert back to pounds: remaining ÷ exchange rate

**Example:** £1 = 1.21 Euros, 220 Euros remaining:
- 220 ÷ 1.21 = 181.818... = **£181.82** (nearest penny)

*Note: always round DOWN when the bank requires multiples — they won't change leftover coins.*
"""

# (currency name, symbol, destinations..., rate_lo, rate_hi, decimal places) — deliberately
# mixed so a run of questions doesn't cluster on euros.
_CURRENCIES = [
    ("Euros", "€", ["Spain", "France", "Italy", "Germany", "Portugal"], 1.10, 1.30, 2),
    ("US Dollars", "$", ["the USA", "Canada", "Florida", "New York"], 1.20, 1.35, 2),
    ("Norwegian Kroner", "kr", ["Norway", "Bergen", "Oslo"], 12.00, 15.00, 2),
    ("Japanese Yen", "¥", ["Japan", "Tokyo", "Kyoto"], 175, 200, 0),
]

_NAMES = ["Mr Smith", "Mrs Jones", "Ms Brown", "Mr Patel", "Mrs Taylor",
          "Mr Wilson", "Ms Davis", "Mr Miltonio"]


def _rate(lo, hi, dp):
    r = random.uniform(lo, hi)
    return round(r, dp) if dp else round(r)


def _fmt(val, dp):
    return f"{val:,.2f}" if dp else f"{val:,.0f}"


# ── Level 1: basic exchange, either direction ────────────────────────────────

def generate_foreign_currency_l1():
    currency, symbol, destinations, lo, hi, dp = random.choice(_CURRENCIES)
    rate = _rate(lo, hi, dp)
    place = random.choice(destinations)
    person = random.choice(_NAMES)
    forward = random.choice([True, False])

    if forward:
        gbp = random.choice(range(20, 500, 5))
        foreign = round(gbp * rate, 2) if dp else round(gbp * rate)
        question_text = (
            f"{person} changes £{gbp} into {currency} before a trip to {place}, at a rate of "
            f"£1 = {symbol}{_fmt(rate, dp)}. How many {currency} do they receive?"
        )
        scaffold_steps = [{"prompt": f"£{gbp} × {_fmt(rate, dp)}", "answer": foreign}]
        worked = [f"£{gbp} × {_fmt(rate, dp)} = {symbol}{_fmt(foreign, dp)}"]
        answer = foreign
    else:
        foreign = random.choice(range(50, 1500, 10))
        gbp = round(foreign / rate, 2)
        question_text = (
            f"{person} changes {symbol}{_fmt(foreign, dp)} back into pounds at the end of a trip "
            f"to {place}, at a rate of £1 = {symbol}{_fmt(rate, dp)}. How many pounds do they receive?"
        )
        scaffold_steps = [{"prompt": f"{symbol}{_fmt(foreign, dp)} ÷ {_fmt(rate, dp)}", "answer": gbp}]
        worked = [f"{symbol}{_fmt(foreign, dp)} ÷ {_fmt(rate, dp)} = £{gbp:.2f}"]
        answer = gbp

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numbers and Money",
        question_type="Foreign Currency",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L1,
    )


# ── Level 2: change, spend, change back (no restriction) ────────────────────

def generate_foreign_currency_l2():
    currency, symbol, destinations, lo, hi, dp = random.choice(_CURRENCIES)
    rate = _rate(lo, hi, dp)
    place = random.choice(destinations)
    person = random.choice(_NAMES)

    for _ in range(50):
        gbp = random.choice(range(80, 500, 10))
        foreign = round(gbp * rate, 2) if dp else round(gbp * rate)
        spend_frac = random.uniform(0.3, 0.75)
        spent = round(foreign * spend_frac, 2) if dp else round(foreign * spend_frac)
        remaining = round(foreign - spent, 2) if dp else foreign - spent
        if remaining > 5:
            break

    back = round(remaining / rate, 2)

    question_text = (
        f"Before a trip to {place}, {person} changes £{gbp} into {currency} at a rate of "
        f"£1 = {symbol}{_fmt(rate, dp)}. They spend {symbol}{_fmt(spent, dp)} while they are away. "
        f"They change the rest back into pounds at the same rate. How many pounds do they receive?"
    )
    scaffold_steps = [
        {"prompt": f"£{gbp} × {_fmt(rate, dp)}", "answer": foreign},
        {"prompt": f"{symbol}{_fmt(foreign, dp)} − {symbol}{_fmt(spent, dp)}", "answer": remaining},
        {"prompt": f"{symbol}{_fmt(remaining, dp)} ÷ {_fmt(rate, dp)}", "answer": back},
    ]
    worked = [
        f"£{gbp} × {_fmt(rate, dp)} = {symbol}{_fmt(foreign, dp)}",
        f"Remaining = {symbol}{_fmt(foreign, dp)} − {symbol}{_fmt(spent, dp)} = {symbol}{_fmt(remaining, dp)}",
        f"{symbol}{_fmt(remaining, dp)} ÷ {_fmt(rate, dp)} = £{back:.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=back,
        topic="Numbers and Money",
        question_type="Foreign Currency",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


# ── Level 3: holiday spending money, restricted round-down ──────────────────

def generate_foreign_currency_l3():
    currency, symbol, destinations, lo, hi, dp = random.choice(_CURRENCIES)
    rate = _rate(lo, hi, dp)
    place = random.choice(destinations)
    multiple = 10

    for _ in range(20):
        start = random.choice(range(600, 1201, 50))
        daily = random.choice(range(60, 121, 5))
        days = random.randint(5, 10)
        spent = daily * days
        remaining = start - spent
        if 20 <= remaining <= 400:
            break

    rounded = (remaining // multiple) * multiple
    gbp = rounded / rate
    answer = round(gbp, 2)

    person = random.choice(_NAMES)
    surname = person.split()[1]

    question_text = (
        f"{person} went on holiday to {place}.\n\n"
        f"They took {start} {currency} to spend.\n\n"
        f"They spent on average {daily} {currency} each day for {days} days.\n\n"
        f"When they came home, they changed the remaining {currency} back to Pounds Sterling.\n\n"
        f"The bank would only change multiples of {multiple} {currency}.\n\n"
        f"£1 = {_fmt(rate, dp)} {currency}\n\n"
        f"How much in Pounds Sterling will {surname} get back? Give your answer to the nearest penny."
    )

    scaffold_steps = [
        {"prompt": f"Total {currency} spent ({daily} × {days})", "answer": spent},
        {"prompt": f"{currency} remaining ({start} − {spent})", "answer": remaining},
        {"prompt": f"Rounded down to nearest multiple of {multiple}", "answer": rounded},
        {"prompt": f"Convert to £ ({rounded} ÷ {_fmt(rate, dp)})", "answer": answer},
    ]

    worked = [
        f"Total spent = {daily} × {days} = {spent} {currency}",
        f"Remaining = {start} − {spent} = {remaining} {currency}",
        f"Rounded down to nearest {multiple}: {rounded} {currency}",
        f"£1 = {_fmt(rate, dp)} {currency}  →  1 {currency} = £(1 ÷ {_fmt(rate, dp)})",
        f"{rounded} {currency} = (1 ÷ {_fmt(rate, dp)}) × {rounded} = **£{answer:.2f}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numbers and Money",
        question_type="Foreign Currency",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L3,
    )


def generate_foreign_currency():
    return random.choice([generate_foreign_currency_l1, generate_foreign_currency_l2, generate_foreign_currency_l3])()
