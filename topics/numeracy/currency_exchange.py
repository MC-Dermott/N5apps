import random
from core.models.question_model import Question

# Currency pool shared across all three levels — deliberately mixed so a run of questions
# doesn't default/cluster on euros the way the source worksheet's restricted-exchange section
# did. (name, symbol, rate_lo, rate_hi, decimal places for a rate/amount in this currency)
_CURRENCIES = [
    ("euros", "€", 1.10, 1.30, 2),
    ("US dollars", "$", 1.20, 1.35, 2),
    ("Norwegian kroner", "kr", 12.00, 15.00, 2),
    ("Japanese yen", "¥", 175, 200, 0),
]

_PLACES = {
    "€": ["Ireland", "Spain", "France", "Portugal", "Italy", "Greece"],
    "$": ["the USA", "Canada", "New York", "Florida"],
    "kr": ["Norway", "Bergen", "Oslo"],
    "¥": ["Japan", "Tokyo", "Kyoto"],
}

_NAMES = [
    "Iain", "Ishbel", "Ceit", "Ailsa", "Mòrag", "Aonghas", "Fiona", "Ruaridh",
    "Dòmhnall", "Anna", "Euan", "Rhona", "Coinneach", "Seonaid", "Tormod", "Catrìona",
]


def _rate(lo, hi, dp):
    r = random.uniform(lo, hi)
    return round(r, dp) if dp else round(r)


def _fmt(val, dp):
    return f"{val:,.2f}" if dp else f"{val:,.0f}"


def _pick_currency():
    return random.choice(_CURRENCIES)


NOTES_L1 = """
**Currency Exchange:**

An exchange rate tells you how many units of a foreign currency you get for £1.

- **Pounds → foreign currency:** multiply by the rate.
- **Foreign currency → pounds:** divide by the rate.

**Example:** £1 = €1.15. Convert £60 into euros.
- €amount = £60 × 1.15 = **€69.00**

**Example:** £1 = €1.15. Convert €69 into pounds.
- £amount = €69 ÷ 1.15 = **£60.00**
"""

NOTES_L2 = """
**Changing, Spending, and Changing Back:**

1. Convert the starting pounds into the foreign currency (× rate).
2. Subtract however much was spent.
3. Convert what's left back into pounds (÷ rate).
"""

NOTES_L3 = """
**Currency Exchange with Restrictions:**

Some exchanges will only change back whole notes of a certain value (e.g. whole €10 notes) —
any smaller leftover amount can't be exchanged.

1. Convert the starting pounds into the foreign currency (× rate).
2. Subtract however much was spent.
3. Round **down** to the nearest whole multiple the exchange accepts — the amount lost this way
   is the amount "left over".
4. Convert the roundable amount back into pounds (÷ rate).
"""


# ── Level 1: basic exchange, either direction ────────────────────────────────

def generate_currency_l1():
    name, symbol, lo, hi, dp = _pick_currency()
    rate = _rate(lo, hi, dp)
    place = random.choice(_PLACES[symbol])
    person = random.choice(_NAMES)
    forward = random.choice([True, False])

    if forward:
        gbp = random.choice(range(20, 500, 5))
        foreign = round(gbp * rate, 2) if dp else round(gbp * rate)
        question_text = (
            f"{person} changes £{gbp} into {name} before a trip to {place}, at a rate of "
            f"£1 = {symbol}{_fmt(rate, dp)}. How many {name} do they receive?"
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
        topic="Numeracy",
        question_type="Currency Exchange",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L1,
    )


# ── Level 2: change, spend, change back ──────────────────────────────────────

def generate_currency_l2():
    name, symbol, lo, hi, dp = _pick_currency()
    rate = _rate(lo, hi, dp)
    place = random.choice(_PLACES[symbol])
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
        f"Before a trip to {place}, {person} changes £{gbp} into {name} at a rate of "
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
        topic="Numeracy",
        question_type="Currency Exchange",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


# ── Level 3: change, spend, change back — restricted to whole notes ─────────

def generate_currency_l3():
    name, symbol, lo, hi, dp = _pick_currency()
    rate = _rate(lo, hi, dp)
    place = random.choice(_PLACES[symbol])
    person = random.choice(_NAMES)
    note = 10

    for _ in range(50):
        gbp = random.choice(range(100, 600, 10))
        foreign = round(gbp * rate, 2) if dp else round(gbp * rate)
        spend_frac = random.uniform(0.35, 0.75)
        spent = round(foreign * spend_frac, 2) if dp else round(foreign * spend_frac)
        remaining = round(foreign - spent, 2) if dp else foreign - spent
        roundable = (remaining // note) * note
        leftover = round(remaining - roundable, 2) if dp else remaining - roundable
        if roundable >= note and leftover > 0:
            break

    back = round(roundable / rate, 2)

    question_text = (
        f"{person} changes £{gbp} into {name} at a rate of £1 = {symbol}{_fmt(rate, dp)} before a "
        f"trip to {place}. They spend {symbol}{_fmt(spent, dp)} while they are away. Only whole "
        f"{symbol}{note} notes can be exchanged back. How many pounds do they receive, and how "
        f"many {name} are left over?"
    )
    scaffold_steps = [
        {"prompt": f"£{gbp} × {_fmt(rate, dp)}", "answer": foreign},
        {"prompt": f"{symbol}{_fmt(foreign, dp)} − {symbol}{_fmt(spent, dp)}", "answer": remaining},
        {"prompt": f"Largest multiple of {symbol}{note} in {symbol}{_fmt(remaining, dp)}", "answer": roundable},
        {"prompt": f"{symbol}{_fmt(roundable, dp)} ÷ {_fmt(rate, dp)}", "answer": back},
    ]
    worked = [
        f"£{gbp} × {_fmt(rate, dp)} = {symbol}{_fmt(foreign, dp)}",
        f"Remaining = {symbol}{_fmt(foreign, dp)} − {symbol}{_fmt(spent, dp)} = {symbol}{_fmt(remaining, dp)}",
        f"Largest multiple of {symbol}{note} in {symbol}{_fmt(remaining, dp)} is {symbol}{_fmt(roundable, dp)} "
        f"({symbol}{_fmt(leftover, dp)} cannot be exchanged)",
        f"{symbol}{_fmt(roundable, dp)} ÷ {_fmt(rate, dp)} = £{back:.2f}",
        f"{person} receives £{back:.2f}, with {symbol}{_fmt(leftover, dp)} left over.",
    ]

    return Question(
        question_text=question_text,
        correct_answer=back,
        topic="Numeracy",
        question_type="Currency Exchange",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L3,
        metadata={"leftover": leftover, "leftover_symbol": symbol},
    )


def generate_currency_question():
    return random.choice([generate_currency_l1, generate_currency_l2, generate_currency_l3])()
