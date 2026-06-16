import random
import math
from core.models.question_model import Question

NOTES = """
**Compound Percentages (Appreciation / Depreciation):**

Use the **multiplier method**:
- Appreciation at r%: multiply by **(1 + r/100)** each year
- Depreciation at r%: multiply by **(1 − r/100)** each year
- Apply the multiplier once per year (or raise it to the power of the number of years)

**Example:** Item worth £6800 appreciates at 4.8% for 3 years:
- Multiplier = (100 + 4.8) ÷ 100 = **1.048**
- Value = £6800 × 1.048³ = £7826.95

**2 Significant Figures (2 SF):** Keep only the first 2 non-zero digits, rounding the rest.
- £7826.95 → **£7800** (2 SF)
- £1243 → **£1200** (2 SF)
- £23,600 → **£24,000** (2 SF)
"""

_ITEMS_APPRECIATION = [
    ("A house", "appreciated"),
    ("A flat", "appreciated"),
    ("A property", "appreciated"),
    ("A piece of artwork", "appreciated"),
    ("A classic car", "appreciated"),
    ("A vintage motorbike", "appreciated"),
    ("A rare painting", "appreciated"),
]

_ITEMS_DEPRECIATION = [
    ("A car", "depreciated"),
    ("A motorbike", "depreciated"),
    ("A van", "depreciated"),
    ("A piece of machinery", "depreciated"),
    ("A laptop", "depreciated"),
    ("A boat", "depreciated"),
    ("A forklift", "depreciated"),
]

_RATES = [3, 4, 4.8, 5, 6, 7, 8, 10, 12, 15]


def _to_2sf(x):
    if x == 0:
        return 0
    mag = 10 ** (math.floor(math.log10(abs(x))) - 1)
    return int(round(x / mag) * mag)


def generate_compound_percentages():
    kind = random.choice(["appreciation", "depreciation"])
    rate = random.choice(_RATES)
    years = random.randint(3, 4)
    start = random.choice(range(2000, 15001, 500))

    if kind == "appreciation":
        multiplier = round(1 + rate / 100, 4)
        subject, verb = random.choice(_ITEMS_APPRECIATION)
    else:
        multiplier = round(1 - rate / 100, 4)
        subject, verb = random.choice(_ITEMS_DEPRECIATION)

    exact = round(start * (multiplier ** years), 2)
    answer = _to_2sf(exact)

    sign = "+" if kind == "appreciation" else "−"
    question_text = (
        f"{subject} is worth £{start:,}. "
        f"It {verb} in value by {rate}% for each of the next {years} years. "
        f"How much is it worth now? Give your answer to 2 significant figures."
    )

    scaffold_steps = [
        {"prompt": f"Write down the multiplier ((100 {sign} {rate}) ÷ 100)", "answer": round(multiplier, 4)},
        {"prompt": f"Calculate the value after {years} years (before rounding)", "answer": exact},
        {"prompt": "Round to 2 significant figures", "answer": answer},
    ]

    power_val = round(multiplier ** years, 6)
    worked = [
        f"Multiplier = (100 {sign} {rate}) ÷ 100 = {round(multiplier, 4)}",
        f"Value = £{start:,} × {round(multiplier, 4)}^{years}",
        f"     = £{start:,} × {power_val}",
        f"     = £{exact:,.2f}",
        f"Rounded to 2 significant figures: **£{answer:,}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numbers and Money",
        question_type="Compound Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
