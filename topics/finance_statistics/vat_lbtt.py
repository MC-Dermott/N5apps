import random
from core.models.question_model import Question

# Scottish LBTT residential bands (fixed real-world values, like income_tax_ni.py's tax/NI
# bands) — not randomised per question, since it's the actual published band table pupils are
# given on the worksheet.
_LBTT_BANDS = [
    ("0%", 0, 145_000, 0),
    ("2%", 145_000, 250_000, 2),
    ("5%", 250_000, 325_000, 5),
    ("10%", 325_000, 750_000, 10),
    ("12%", 750_000, None, 12),
]
_LBTT_MAX_PRICE = 1_000_000

_PLACES = [
    "Stornoway", "Tarbert", "Scalpay", "Leverburgh", "Berneray", "North Uist", "Ness",
    "Carloway", "Eriskay", "Grimsay", "Balivanich", "Bernera", "Uig", "Portree", "Lochmaddy",
]

_STANDARD_ITEMS = [
    "a pair of waterproof boots", "a set of fishing rods", "a weaving loom",
    "an outboard engine", "a set of tyres", "a dining table", "a laptop", "a quad bike",
    "a set of creels", "a set of oars", "a mountain bike", "a chainsaw",
    "a set of solar panels", "a chest freezer", "a set of golf clubs",
]

_REDUCED_ITEMS = [
    "home heating oil", "insulation for a self-build home",
    "wood pellets for a stove", "a domestic heating oil delivery",
]

NOTES_VAT_INCLUSIVE = """
**Adding VAT (VAT-Inclusive Prices):**

VAT is charged at the standard rate of 20% on most goods and services, and at a reduced rate
of 5% on some items, such as domestic heating fuel.

To find the price **including** VAT, multiply the price before VAT by the multiplier:
- Standard rate: multiplier = 1 + 0.20 = **1.20**
- Reduced rate: multiplier = 1 + 0.05 = **1.05**

**Example:** A ferry ticket costs £45.00 before VAT, at the standard rate.
- Multiplier = 1 + 0.20 = 1.20
- Price including VAT = £45.00 × 1.20 = **£54.00**

**Common mistake:** Multiplying by 0.20 only finds the *amount* of VAT, not the full price
including VAT.
"""

NOTES_VAT_EXCLUSIVE = """
**Reverse Percentages: Finding the Price Before VAT:**

A price "including VAT" is 120% (or 105%, for the reduced rate) of the original price — so to
reverse it, **divide** by the multiplier rather than subtracting a percentage of the given price.

**Example:** A jacket costs £72.00 including VAT at the standard rate.
- Multiplier = 1 + 0.20 = 1.20
- Price before VAT = £72.00 ÷ 1.20 = **£60.00**

**Common mistake:** Do NOT find 20% of the VAT-inclusive price and subtract it — that finds
20% of the wrong amount.
"""

NOTES_VAT_PERCENTAGE = """
**VAT as a Percentage of a Shop:**

Some items (e.g. most food and household essentials) are VAT-exempt (zero-rated) — no VAT is
charged on them. Standard-rated items still include VAT at 20%.

1. Find the VAT-inclusive cost of the standard-rated items: total − exempt items
2. Find the price of these items before VAT: divide by 1.20
3. Find the amount of VAT paid: (1) − (2)
4. Express this as a percentage of the **whole** shop total: (VAT ÷ whole total) × 100

**Common mistake:** Compare the VAT amount with the whole shop total, not just the
standard-rated portion — only some of the shop attracts VAT at all.
"""

NOTES_LBTT = """
**Land and Buildings Transaction Tax (LBTT):**

LBTT is paid in Scotland when buying property or land above a certain price, instead of VAT.
It is a progressive tax: each band is taxed at its own rate, and only on the part of the price
that falls within that band — in the same way Income Tax is calculated in bands.

| Band | Price | LBTT rate |
|---|---|---|
| Nil rate | £0 – £145,000 | 0% |
| | £145,001 – £250,000 | 2% |
| | £250,001 – £325,000 | 5% |
| | £325,001 – £750,000 | 10% |
| | Above £750,000 | 12% |

**Common mistake:** The whole price does not get charged at the top rate it reaches — work
through the bands in order, and stop once you reach the band the price falls into.
"""

_REFERENCE_SHEET_LBTT = """
**Scottish residential LBTT bands**

| Price | LBTT rate |
|---|---|
| £0 – £145,000 | 0% |
| £145,001 – £250,000 | 2% |
| £250,001 – £325,000 | 5% |
| £325,001 – £750,000 | 10% |
| Above £750,000 | 12% |

LBTT is charged instead of VAT when buying property or land; it is a separate tax.
"""


def _r2(v):
    return round(float(v), 2)


def _banded_calc(amount, bands):
    """Total charge over a set of contiguous bands, plus a breakdown of each band actually
    reached: list of (label, lower, portion_upper, taxable, rate, amount_charged)."""
    breakdown = []
    total = 0.0
    for label, lower, upper, rate in bands:
        if amount <= lower:
            break
        portion_upper = amount if upper is None else min(amount, upper)
        taxable = portion_upper - lower
        amt = taxable * rate / 100
        breakdown.append((label, lower, portion_upper, taxable, rate, amt))
        total += amt
        if upper is not None and amount <= upper:
            break
    return _r2(total), breakdown


# ── Section A: VAT-Inclusive Price ───────────────────────────────────────────

def generate_vat_inclusive_price(level="Higher"):
    place = random.choice(_PLACES)
    if random.random() < 0.75:
        item = random.choice(_STANDARD_ITEMS)
        rate = 20
        price_before = random.choice(range(30, 1200, 5))
    else:
        item = random.choice(_REDUCED_ITEMS)
        rate = 5
        price_before = random.choice(range(140, 620, 20))

    multiplier = _r2(1 + rate / 100)
    price_after = _r2(price_before * multiplier)
    rate_word = "standard" if rate == 20 else "reduced"

    question_text = (
        f"{item[0].upper()}{item[1:]} from a supplier in {place} costs £{price_before:,.2f} "
        f"before VAT. VAT is charged at the {rate_word} rate of {rate}%. "
        f"Calculate the price including VAT."
    )
    scaffold_steps = [
        {"prompt": f"Find the multiplier (1 + {rate}/100)", "answer": multiplier},
        {"prompt": "Price including VAT = price before VAT × multiplier", "answer": price_after},
    ]
    worked = [
        f"Multiplier = 1 + {rate}/100 = {multiplier}",
        f"Price including VAT = £{price_before:,.2f} × {multiplier} = £{price_after:,.2f}",
    ]
    return Question(
        question_text=question_text,
        correct_answer=price_after,
        topic="Finance",
        question_type="VAT and LBTT",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_VAT_INCLUSIVE,
    )


# ── Section B: Reverse Percentages — Price Before VAT ────────────────────────

def generate_vat_exclusive_price(level="Higher"):
    place = random.choice(_PLACES)
    if random.random() < 0.75:
        item = random.choice(_STANDARD_ITEMS)
        rate = 20
        price_before = random.choice(range(30, 1200, 5))
    else:
        item = random.choice(_REDUCED_ITEMS)
        rate = 5
        price_before = random.choice(range(140, 620, 20))

    multiplier = _r2(1 + rate / 100)
    price_after = _r2(price_before * multiplier)
    rate_word = "standard" if rate == 20 else "reduced"

    question_text = (
        f"{item[0].upper()}{item[1:]} from a supplier in {place} costs £{price_after:,.2f} "
        f"including VAT at the {rate_word} rate of {rate}%. Calculate the price before VAT."
    )
    scaffold_steps = [
        {"prompt": f"Find the multiplier (1 + {rate}/100)", "answer": multiplier},
        {"prompt": "Price before VAT = price including VAT ÷ multiplier", "answer": price_before},
    ]
    worked = [
        f"Multiplier = 1 + {rate}/100 = {multiplier}",
        f"Price before VAT = £{price_after:,.2f} ÷ {multiplier} = £{price_before:,.2f}",
    ]
    return Question(
        question_text=question_text,
        correct_answer=_r2(price_before),
        topic="Finance",
        question_type="VAT and LBTT",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_VAT_EXCLUSIVE,
    )


# ── Section C: VAT as a Percentage of a Shop ─────────────────────────────────

_SHOP_TEMPLATES = [
    "A shop at the village shop in {place} comes to a total of £{total:,.2f}.",
    "A shop at the Co-op in {place} comes to a total of £{total:,.2f}.",
    "An online supermarket order delivered to {place} comes to a total of £{total:,.2f}.",
    "A family shop delivered to a house in {place} totals £{total:,.2f}.",
]


def generate_vat_percentage_of_shop(level="Higher"):
    place = random.choice(_PLACES)
    total = random.choice(range(48, 312, 6))
    exempt = random.choice(range(18, total - 18, 6))
    standard_incl = total - exempt

    before = _r2(standard_incl / 1.20)
    vat = _r2(standard_incl - before)
    pct = _r2((vat / total) * 100)

    template = random.choice(_SHOP_TEMPLATES)
    question_text = (
        template.format(place=place, total=total) +
        f" Of this, £{exempt:,.2f} is spent on VAT-exempt items. The rest is spent on "
        f"standard-rated items, which include VAT at 20%. Calculate what percentage of the "
        f"total £{total:,.2f} shop is made up of VAT."
    )
    scaffold_steps = [
        {"prompt": "Find the VAT-inclusive cost of the standard-rated items (total − exempt items)", "answer": standard_incl},
        {"prompt": "Find the price of these items before VAT (÷ 1.20)", "answer": before},
        {"prompt": "Find the amount of VAT paid", "answer": vat},
        {"prompt": "Express this as a percentage of the whole shop total", "answer": pct},
    ]
    worked = [
        f"Standard-rated (incl. VAT) = £{total:,.2f} − £{exempt:,.2f} = £{standard_incl:,.2f}",
        f"Before VAT = £{standard_incl:,.2f} ÷ 1.20 = £{before:,.2f}",
        f"VAT = £{standard_incl:,.2f} − £{before:,.2f} = £{vat:,.2f}",
        f"Percentage of shop = (£{vat:,.2f} ÷ £{total:,.2f}) × 100 = {pct}%",
    ]
    return Question(
        question_text=question_text,
        correct_answer=pct,
        topic="Finance",
        question_type="VAT and LBTT",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_VAT_PERCENTAGE,
    )


# ── Section D: LBTT ───────────────────────────────────────────────────────────

def generate_lbtt(level="Higher"):
    place = random.choice(_PLACES)
    price = random.choice(range(50_000, 900_000, 5_000))
    lbtt, breakdown = _banded_calc(price, _LBTT_BANDS)

    property_type = random.choice([
        "house", "croft house", "plot of croft land", "guesthouse", "cottage", "estate",
    ])
    question_text = f"A {property_type} in {place} is bought for £{price:,}. Calculate the LBTT payable."

    if lbtt == 0.0:
        scaffold_steps = [
            {"prompt": "Which band does the price fall entirely within?", "answer": 0.0},
        ]
        worked = [
            f"£{price:,} falls entirely within the £0 – £145,000 band, which is charged at 0%.",
            "Total LBTT = £0.00 — no LBTT is payable because the price is below the nil-rate threshold.",
        ]
    else:
        scaffold_steps = []
        worked = []
        for label, lower, upper, taxable, rate, amt in breakdown:
            if rate == 0:
                worked.append(f"Band ({label}): £{taxable:,.2f} taxed at 0% = £0.00")
                continue
            scaffold_steps.append({
                "prompt": f"{label} band: the amount of the price in this band, taxed at {rate}%",
                "answer": _r2(amt),
            })
            worked.append(f"Band ({label}): £{upper:,.2f} − £{lower:,.2f} = £{taxable:,.2f} × {rate}% = £{amt:,.2f}")
        scaffold_steps.append({"prompt": "Total LBTT = sum of all bands above", "answer": lbtt})
        worked.append("Total LBTT = " + " + ".join(f"£{b[5]:,.2f}" for b in breakdown) + f" = £{lbtt:,.2f}")

    return Question(
        question_text=question_text,
        correct_answer=lbtt,
        topic="Finance",
        question_type="VAT and LBTT",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_LBTT,
        metadata={
            "diagram": "tax_bands",
            "diagram_params": {
                "bands": _LBTT_BANDS,
                "max_income": _LBTT_MAX_PRICE,
                "initial_income": price,
                "amount_label": "Purchase price",
            },
            "reference_sheet": _REFERENCE_SHEET_LBTT,
        },
    )


# ── Default dispatcher ────────────────────────────────────────────────────────

def generate_vat_lbtt_question(level="Higher"):
    return random.choice([
        generate_vat_inclusive_price, generate_vat_exclusive_price,
        generate_vat_percentage_of_shop, generate_lbtt,
    ])(level=level)
