import random
from core.models.question_model import Question

NOTES = """
**Foreign Currency Exchange:**

1. Calculate total spent: daily spend × number of days
2. Find remaining foreign currency: starting amount − total spent
3. Round **down** to the nearest multiple the bank accepts
4. Convert back to pounds: remaining ÷ exchange rate

**Example:** £1 = 1.21 Euros, 220 Euros remaining:
- 220 ÷ 1.21 = 181.818... = **£181.82** (nearest penny)

*Note: always round DOWN when the bank requires multiples — they won't change leftover coins.*
"""

_DESTINATIONS = [
    ("Spain", "Euros", "€", True),
    ("France", "Euros", "€", True),
    ("Italy", "Euros", "€", True),
    ("Germany", "Euros", "€", True),
    ("Portugal", "Euros", "€", True),
]

_RATES = [1.12, 1.15, 1.18, 1.20, 1.21, 1.25, 1.28, 1.30, 1.35]

_NAMES = ["Mr Smith", "Mrs Jones", "Ms Brown", "Mr Patel", "Mrs Taylor",
          "Mr Wilson", "Ms Davis", "Mr Miltonio"]


def generate_foreign_currency():
    country, currency, symbol, _ = random.choice(_DESTINATIONS)
    rate = random.choice(_RATES)
    multiple = 10

    # Ensure spending leaves a meaningful remainder (> 20)
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
        f"{person} went on holiday to {country}.\n\n"
        f"They took {start} {currency} to spend.\n\n"
        f"They spent on average {daily} {currency} each day for {days} days.\n\n"
        f"When they came home, they changed the remaining {currency} back to Pounds Sterling.\n\n"
        f"The bank would only change multiples of {multiple} {currency}.\n\n"
        f"£1 = {rate} {currency}\n\n"
        f"How much in Pounds Sterling will {surname} get back? Give your answer to the nearest penny."
    )

    scaffold_steps = [
        {"prompt": f"Total {currency} spent ({daily} × {days})", "answer": spent},
        {"prompt": f"{currency} remaining ({start} − {spent})", "answer": remaining},
        {"prompt": f"Rounded down to nearest multiple of {multiple}", "answer": rounded},
        {"prompt": f"Convert to £ ({rounded} ÷ {rate})", "answer": answer},
    ]

    worked = [
        f"Total spent = {daily} × {days} = {spent} {currency}",
        f"Remaining = {start} − {spent} = {remaining} {currency}",
        f"Rounded down to nearest {multiple}: {rounded} {currency}",
        f"£1 = {rate} {currency}  →  1 {currency} = £(1 ÷ {rate})",
        f"{rounded} {currency} = (1 ÷ {rate}) × {rounded} = **£{answer:.2f}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numbers and Money",
        question_type="Foreign Currency",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
