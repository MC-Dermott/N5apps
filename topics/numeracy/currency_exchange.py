import random
from core.models.question_model import Question

# Currency pool shared across all three levels — deliberately mixed so a run of questions
# doesn't default/cluster on euros the way the source worksheet's restricted-exchange section
# did. (name, symbol, rate_lo, rate_hi, decimal places for a rate/amount in this currency,
# smallest common banknote in that currency — used by Level 3's exchange restriction, since a
# real bureau de change restricts to whole notes of that currency's own denominations, not a
# blanket "nearest 10" regardless of currency: euros/dollars have 10-unit notes, but Norway's
# smallest note is 50 kroner and Japan's is 1000 yen).
_CURRENCIES = [
    ("euros", "€", 1.10, 1.30, 2, 10),
    ("US dollars", "$", 1.20, 1.35, 2, 10),
    ("Norwegian kroner", "kr", 12.00, 15.00, 2, 50),
    ("Japanese yen", "¥", 175, 200, 0, 1000),
    ("Polish złoty", "zł", 4.70, 5.20, 2, 10),
]

_PLACES = {
    "€": ["Ireland", "Spain", "France", "Portugal", "Italy", "Greece"],
    "$": ["the USA", "Canada", "New York", "Florida"],
    "kr": ["Norway", "Bergen", "Oslo"],
    "¥": ["Japan", "Tokyo", "Kyoto"],
    "zł": ["Poland", "Warsaw", "Kraków", "Gdańsk"],
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


def _pick_two_currencies():
    return random.sample(_CURRENCIES, 2)


def _rate_table_md(rateA, nameA, dpA, rateB, nameB, dpB):
    return (
        "| Pounds Sterling (£) | Other Currencies |\n"
        "|:---|:---|\n"
        f"| 1 | {_fmt(rateA, dpA)} {nameA} |\n"
        f"| 1 | {_fmt(rateB, dpB)} {nameB} |\n"
    )


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

NOTES_L4 = """
**Converting Between Two Currencies:**

You can't convert directly between two foreign currencies — exchange rates are always quoted
against £1. Convert back through pounds as the "middle step":

1. Convert the starting pounds into the first currency (× first rate).
2. Subtract however much was spent.
3. Convert what's left back into pounds (÷ first rate).
4. Convert those pounds into the second currency (× second rate).

**Example:** £640 → zlotys at £1 = 4.94 zł. Lorna spends 340 zł a day for 4 days, then changes
what's left into euros at £1 = €1.15.
- £640 × 4.94 = 3161.60 zł
- Spent = 340 × 4 = 1360 zł
- Remaining = 3161.60 − 1360 = 1801.60 zł
- Back to pounds: 1801.60 ÷ 4.94 = £364.70
- To euros: £364.70 × 1.15 = **€419.40**
"""

NOTES_L5 = """
**Calculating the Exchange Rate:**

If you know how much of a foreign currency a given number of pounds converts to, find the rate
by dividing the foreign amount by the pound amount — this gives the amount of foreign currency
equivalent to £1.

**Example:** £50 converts to €57.50. Calculate the exchange rate.
- Rate = €57.50 ÷ £50 = **£1 = €1.15**
"""


# ── Level 1: basic exchange, either direction ────────────────────────────────

def generate_currency_l1():
    name, symbol, lo, hi, dp, note = _pick_currency()
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
    name, symbol, lo, hi, dp, note = _pick_currency()
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
    name, symbol, lo, hi, dp, note = _pick_currency()
    rate = _rate(lo, hi, dp)
    place = random.choice(_PLACES[symbol])
    person = random.choice(_NAMES)

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


# ── Level 4: change, spend, then convert what's left into a THIRD currency ──

def generate_currency_l4():
    (nameA, symbolA, loA, hiA, dpA, _noteA), (nameB, symbolB, loB, hiB, dpB, _noteB) = _pick_two_currencies()
    rateA = _rate(loA, hiA, dpA)
    rateB = _rate(loB, hiB, dpB)
    place = random.choice(_PLACES[symbolA])
    person = random.choice(_NAMES)
    days = random.randint(3, 10)

    for _ in range(50):
        gbp = random.choice(range(150, 700, 10))
        foreignA = round(gbp * rateA, 2) if dpA else round(gbp * rateA)
        spend_frac = random.uniform(0.3, 0.6)
        daily = round((foreignA * spend_frac) / days, 2) if dpA else round((foreignA * spend_frac) / days)
        spent = round(daily * days, 2) if dpA else daily * days
        remainingA = round(foreignA - spent, 2) if dpA else foreignA - spent
        if remainingA > (10 if dpA else 100):
            break

    gbp_back = round(remainingA / rateA, 2)
    foreignB = round(gbp_back * rateB, 2) if dpB else round(gbp_back * rateB)

    question_text = (
        f"{person} is travelling around Europe.\n\n"
        f"Use the table above to help you.\n\n"
        f"{person} converted £{gbp} into {nameA}.\n\n"
        f"They were in {place} for {days} days.\n\n"
        f"They spent {symbolA}{_fmt(daily, dpA)} each day they were in {place}.\n\n"
        f"They converted their remaining {nameA} into {nameB}.\n\n"
        f"Calculate how many {nameB} they received."
    )

    scaffold_steps = [
        {"prompt": f"£{gbp} × {_fmt(rateA, dpA)}", "answer": foreignA},
        {"prompt": f"Total {nameA} spent ({_fmt(daily, dpA)} × {days})", "answer": spent},
        {"prompt": f"{nameA} remaining ({_fmt(foreignA, dpA)} − {_fmt(spent, dpA)})", "answer": remainingA},
        {"prompt": f"Remaining {nameA} converted to £ ({_fmt(remainingA, dpA)} ÷ {_fmt(rateA, dpA)})",
         "answer": gbp_back},
        {"prompt": f"£{gbp_back:.2f} × {_fmt(rateB, dpB)}", "answer": foreignB},
    ]
    worked = [
        f"£{gbp} × {_fmt(rateA, dpA)} = {symbolA}{_fmt(foreignA, dpA)}",
        f"Spent = {_fmt(daily, dpA)} × {days} = {symbolA}{_fmt(spent, dpA)}",
        f"Remaining = {symbolA}{_fmt(foreignA, dpA)} − {symbolA}{_fmt(spent, dpA)} = {symbolA}{_fmt(remainingA, dpA)}",
        f"Back to pounds: {symbolA}{_fmt(remainingA, dpA)} ÷ {_fmt(rateA, dpA)} = £{gbp_back:.2f}",
        f"To {nameB}: £{gbp_back:.2f} × {_fmt(rateB, dpB)} = {symbolB}{_fmt(foreignB, dpB)}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=foreignB,
        topic="Numeracy",
        question_type="Currency Exchange",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L4,
        metadata={"table": _rate_table_md(rateA, nameA, dpA, rateB, nameB, dpB)},
    )


# ── Level 5: calculate the exchange rate itself ─────────────────────────────

def generate_currency_l5():
    name, symbol, lo, hi, dp, note = _pick_currency()
    rate = _rate(lo, hi, dp)
    place = random.choice(_PLACES[symbol])
    person = random.choice(_NAMES)
    forward = random.choice([True, False])
    gbp = random.choice(range(20, 500, 5))
    foreign = round(gbp * rate, 2) if dp else round(gbp * rate)

    if forward:
        question_text = (
            f"{person} changes £{gbp} into {name} before a trip to {place}, and receives "
            f"{symbol}{_fmt(foreign, dp)}. How many {name} are equivalent to £1?"
        )
    else:
        question_text = (
            f"{person} changes {symbol}{_fmt(foreign, dp)} into pounds at the end of a trip to "
            f"{place}, and receives £{gbp}. How many {name} are equivalent to £1?"
        )

    scaffold_steps = [
        {"prompt": f"{symbol}{_fmt(foreign, dp)} ÷ £{gbp}", "answer": rate},
    ]
    worked = [
        f"{symbol}{_fmt(foreign, dp)} ÷ {gbp} = {_fmt(rate, dp)}",
        f"£1 = {symbol}{_fmt(rate, dp)}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=rate,
        topic="Numeracy",
        question_type="Currency Exchange",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L5,
    )


def generate_currency_question():
    return random.choice([generate_currency_l1, generate_currency_l2, generate_currency_l3,
                           generate_currency_l4, generate_currency_l5])()
