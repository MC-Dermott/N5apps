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

# (currency name, symbol, destinations..., rate_lo, rate_hi, decimal places) — deliberately
# mixed so a run of questions doesn't cluster on euros.
# Last field is the smallest common banknote in that currency — Level 3's bank restriction uses
# it instead of a blanket "nearest 10" regardless of currency: euros/dollars have 10-unit notes,
# but Norway's smallest note is 50 kroner and Japan's is 1000 yen.
_CURRENCIES = [
    ("Euros", "€", ["Spain", "France", "Italy", "Germany", "Portugal"], 1.10, 1.30, 2, 10),
    ("US Dollars", "$", ["the USA", "Canada", "Florida", "New York"], 1.20, 1.35, 2, 10),
    ("Norwegian Kroner", "kr", ["Norway", "Bergen", "Oslo"], 12.00, 15.00, 2, 50),
    ("Japanese Yen", "¥", ["Japan", "Tokyo", "Kyoto"], 175, 200, 0, 1000),
    ("Polish Złoty", "zł", ["Poland", "Warsaw", "Kraków", "Gdańsk"], 4.70, 5.20, 2, 10),
]

_NAMES = ["Mr Smith", "Mrs Jones", "Ms Brown", "Mr Patel", "Mrs Taylor",
          "Mr Wilson", "Ms Davis", "Mr Miltonio"]

# Level 3 ("holiday spending money") scenario ranges, keyed by symbol — these have to scale
# with the currency, not just its note size: e.g. "took 600-1200 yen" is meaningless holiday
# money (about £3-6), so yen amounts need to be roughly 170x the euro-scale ones, matching its
# exchange rate. (start_lo, start_hi, start_step, daily_lo, daily_hi, daily_step, remain_lo, remain_hi)
_L3_RANGES = {
    "€": (600, 1200, 50, 60, 120, 5, 20, 400),
    "$": (650, 1300, 50, 65, 130, 5, 20, 400),
    "kr": (7000, 14000, 100, 700, 1400, 50, 100, 2000),
    "¥": (100_000, 200_000, 2000, 10_000, 20_000, 500, 2000, 40_000),
    "zł": (2500, 5000, 100, 250, 500, 25, 100, 1500),
}


def _rate(lo, hi, dp):
    r = random.uniform(lo, hi)
    return round(r, dp) if dp else round(r)


def _fmt(val, dp):
    return f"{val:,.2f}" if dp else f"{val:,.0f}"


# ── Level 1: basic exchange, either direction ────────────────────────────────

def generate_foreign_currency_l1():
    currency, symbol, destinations, lo, hi, dp, note = random.choice(_CURRENCIES)
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
    currency, symbol, destinations, lo, hi, dp, note = random.choice(_CURRENCIES)
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
    currency, symbol, destinations, lo, hi, dp, multiple = random.choice(_CURRENCIES)
    rate = _rate(lo, hi, dp)
    place = random.choice(destinations)
    start_lo, start_hi, start_step, daily_lo, daily_hi, daily_step, remain_lo, remain_hi = _L3_RANGES[symbol]

    for _ in range(30):
        start = random.choice(range(start_lo, start_hi + 1, start_step))
        daily = random.choice(range(daily_lo, daily_hi + 1, daily_step))
        days = random.randint(5, 10)
        spent = daily * days
        remaining = start - spent
        if remain_lo <= remaining <= remain_hi:
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


def _rate_table_md(rateA, nameA, dpA, rateB, nameB, dpB):
    return (
        "| Pounds Sterling (£) | Other Currencies |\n"
        "|:---|:---|\n"
        f"| 1 | {_fmt(rateA, dpA)} {nameA} |\n"
        f"| 1 | {_fmt(rateB, dpB)} {nameB} |\n"
    )


# ── Level 4: change, spend, then convert what's left into a THIRD currency ──

def generate_foreign_currency_l4():
    (nameA, symbolA, destinationsA, loA, hiA, dpA, _noteA), \
        (nameB, symbolB, _destB, loB, hiB, dpB, _noteB) = random.sample(_CURRENCIES, 2)
    rateA = _rate(loA, hiA, dpA)
    rateB = _rate(loB, hiB, dpB)
    place = random.choice(destinationsA)
    person = random.choice(_NAMES)
    surname = person.split()[1]
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
        f"{surname} converted £{gbp} into {nameA}.\n\n"
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
        topic="Numbers and Money",
        question_type="Foreign Currency",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L4,
        metadata={"table": _rate_table_md(rateA, nameA, dpA, rateB, nameB, dpB)},
    )


# ── Level 5: calculate the exchange rate itself ─────────────────────────────

def generate_foreign_currency_l5():
    currency, symbol, destinations, lo, hi, dp, note = random.choice(_CURRENCIES)
    rate = _rate(lo, hi, dp)
    place = random.choice(destinations)
    person = random.choice(_NAMES)
    forward = random.choice([True, False])
    gbp = random.choice(range(20, 500, 5))
    foreign = round(gbp * rate, 2) if dp else round(gbp * rate)

    if forward:
        question_text = (
            f"{person} changes £{gbp} into {currency} before a trip to {place}, and receives "
            f"{symbol}{_fmt(foreign, dp)}. How many {currency} are equivalent to £1?"
        )
    else:
        question_text = (
            f"{person} changes {symbol}{_fmt(foreign, dp)} into pounds at the end of a trip to "
            f"{place}, and receives £{gbp}. How many {currency} are equivalent to £1?"
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
        topic="Numbers and Money",
        question_type="Foreign Currency",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L5,
    )


def generate_foreign_currency():
    return random.choice([generate_foreign_currency_l1, generate_foreign_currency_l2,
                           generate_foreign_currency_l3, generate_foreign_currency_l4,
                           generate_foreign_currency_l5])()
