import random
from core.models.question_model import Question

NOTES = """
**Percentage of an Amount — Multiplier Method:**

1. Write the percentage as a decimal **multiplier** (percentage ÷ 100)
2. **Multiply** the amount by the multiplier

**Example:** What is 35% of 84?
- Multiplier = 35 ÷ 100 = 0.35
- 35% of 84 = 0.35 × 84 = **29.4**
"""

NOTES_L2 = """
**One Percentage of Another — Multiplier Method:**

1. Divide the part by the whole to find the decimal **multiplier** (part ÷ whole)
2. **Multiply** the multiplier by 100 to convert it to a percentage

**Example:** A pupil scores 34 out of 40 in a test.
- Multiplier = 34 ÷ 40 = 0.85
- Percentage = 0.85 × 100 = **85%**
"""

NOTES_MULTIPLIER = """
**Calculating the Multiplier:**

A multiplier lets you calculate a new amount after a percentage increase or decrease in a
single step.

- **Increase** of r%: multiplier = 1 + (r ÷ 100)
- **Decrease** of r%: multiplier = 1 − (r ÷ 100)

**Example:** A shop increases all prices by 8%.
- 8% = 0.08
- Multiplier = 1 + 0.08 = **1.08**

**Example:** A car depreciates in value by 15%.
- 15% = 0.15
- Multiplier = 1 − 0.15 = **0.85**
"""

NOTES_SINGLE_CHANGE = """
**Calculating a Single Percentage Change — Multiplier Method:**

1. Write the percentage as a decimal
2. Add it to (increase) or subtract it from (decrease) 1 to find the **multiplier**
3. **Multiply** the original amount by the multiplier

**Example:** A laptop costs £650. It is reduced by 20% in a sale.
- 20% = 0.20
- Multiplier = 1 − 0.20 = 0.80
- New price = £650 × 0.80 = **£520**
"""

_NAMES = [
    "Amy", "Callum", "Catriona", "Connor", "Douglas", "Eilidh",
    "Ewan", "Freya", "Hamish", "Isla", "Jamie", "Kirsty",
    "Laura", "Liam", "Megan", "Ramani", "Ross", "Stuart",
]

_N4_PERCENTAGES = [10, 20, 25, 50, 75]


def generate_percentage_question_n4():
    percentage = random.choice(_N4_PERCENTAGES)
    amount = random.choice(range(20, 201, 20))
    answer = round((amount * percentage) / 100, 2)
    one_percent = round(amount / 100, 2)

    scaffold_steps = [
        {
            "prompt": "Find 1% of the amount",
            "answer": one_percent
        },
        {
            "prompt": "Multiply 1% by the percentage you need",
            "answer": answer
        }
    ]

    return Question(
        question_text=f"What is {percentage}% of {amount}?",
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=[
            f"1% of {amount} = {amount} ÷ 100 = {one_percent}",
            f"{percentage}% of {amount} = {percentage} × {one_percent} = {answer}",
        ],
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 1 — percentage of an amount
# ---------------------------------------------------------------------------

def generate_percentage_l1():
    percentage = random.randint(1, 99)
    amount = random.randint(10, 200)
    multiplier = round(percentage / 100, 2)
    answer = round(amount * multiplier, 2)

    scaffold_steps = [
        {
            "prompt": "Write the percentage as a decimal multiplier (percentage ÷ 100)",
            "answer": multiplier
        },
        {
            "prompt": "Multiply the amount by the multiplier",
            "answer": answer
        }
    ]

    return Question(
        question_text=f"What is {percentage}% of {amount}?",
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=[
            f"Multiplier = {percentage} ÷ 100 = {multiplier}",
            f"{percentage}% of {amount} = {multiplier} × {amount} = {answer}",
        ],
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 2 — one amount as a percentage of another (real-world contexts)
# ---------------------------------------------------------------------------

_PL_ITEMS = [
    "bike", "laptop", "sofa", "guitar", "smartphone", "watch",
    "games console", "mountain bike", "television", "washing machine",
]


def _profit_loss_question():
    name = random.choice(_NAMES)
    item = random.choice(_PL_ITEMS)
    cost = random.choice(range(40, 601, 10))
    is_profit = random.choice([True, False])
    max_change = min(cost - 2, 250)
    change = random.choice(range(4, max_change, 2))

    if is_profit:
        sale = cost + change
        verb = "profit"
    else:
        sale = cost - change
        verb = "loss"

    multiplier = round(change / cost, 4)
    answer = round(multiplier * 100, 1)

    question_text = (
        f"{name} bought a {item} for £{cost} and sold it for £{sale}.\n\n"
        f"Calculate the {verb} as a percentage of the cost price.\n\n"
        f"Give your answer to 1 decimal place."
    )

    scaffold_steps = [
        {
            "prompt": f"Calculate the {verb} (difference between the cost price and the selling price)",
            "answer": float(change),
        },
        {
            "prompt": f"Divide the {verb} by the cost price to find the multiplier",
            "answer": multiplier,
        },
        {
            "prompt": "Multiply the multiplier by 100 to convert to a percentage",
            "answer": answer,
        },
    ]

    worked = [
        f"{verb.capitalize()} = £{max(sale, cost)} − £{min(sale, cost)} = £{change}",
        f"Multiplier = {change} ÷ {cost} = {multiplier}",
        f"{verb.capitalize()} % = {multiplier} × 100 = {answer}%",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


_QC_CONTEXTS = [
    {"items": "light bulbs", "setting": "a factory", "adj": "faulty"},
    {"items": "circuit boards", "setting": "an electronics plant", "adj": "defective"},
    {"items": "glass bottles", "setting": "a bottling plant", "adj": "cracked"},
    {"items": "phone screens", "setting": "a manufacturing plant", "adj": "damaged"},
    {"items": "tyres", "setting": "a tyre factory", "adj": "substandard"},
    {"items": "ceramic mugs", "setting": "a pottery factory", "adj": "chipped"},
]


def _quality_control_question():
    ctx = random.choice(_QC_CONTEXTS)
    batch = random.choice(range(200, 2001, 50))
    faulty = random.choice(range(4, max(6, batch // 10), 2))
    multiplier = round(faulty / batch, 4)
    answer = round(multiplier * 100, 1)

    question_text = (
        f"A quality control inspector at {ctx['setting']} checked a batch of {batch} {ctx['items']}.\n\n"
        f"{faulty} of the {ctx['items']} were found to be {ctx['adj']}.\n\n"
        f"Calculate the percentage of the batch that was {ctx['adj']}.\n\n"
        f"Give your answer to 1 decimal place."
    )

    scaffold_steps = [
        {
            "prompt": f"Divide the number {ctx['adj']} by the batch size to find the multiplier",
            "answer": multiplier,
        },
        {
            "prompt": "Multiply the multiplier by 100 to convert to a percentage",
            "answer": answer,
        },
    ]

    worked = [
        f"Multiplier = {faulty} ÷ {batch} = {multiplier}",
        f"Percentage = {multiplier} × 100 = {answer}%",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


_SUBJECTS = [
    "Maths", "English", "Physics", "Chemistry", "Biology",
    "History", "Geography", "French", "Computing", "Art",
]


def _test_score_question():
    name = random.choice(_NAMES)
    subject = random.choice(_SUBJECTS)
    total = random.choice([20, 25, 30, 40, 50, 60, 75, 80])
    score = random.randint(int(total * 0.3), total)
    multiplier = round(score / total, 4)
    answer = round(multiplier * 100, 1)

    question_text = (
        f"{name} scored {score} marks out of {total} in a {subject} test.\n\n"
        f"Calculate {name}'s score as a percentage.\n\n"
        f"Give your answer to 1 decimal place."
    )

    scaffold_steps = [
        {
            "prompt": "Divide the score by the total marks to find the multiplier",
            "answer": multiplier,
        },
        {
            "prompt": "Multiply the multiplier by 100 to convert to a percentage",
            "answer": answer,
        },
    ]

    worked = [
        f"Multiplier = {score} ÷ {total} = {multiplier}",
        f"Percentage = {multiplier} × 100 = {answer}%",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


_SPORTS_CONTEXTS = [
    {"sport": "basketball", "action": "free throws", "attempt_word": "attempts"},
    {"sport": "football", "action": "penalty kicks", "attempt_word": "attempts"},
    {"sport": "darts", "action": "throws", "attempt_word": "throws"},
    {"sport": "netball", "action": "shots", "attempt_word": "attempts"},
    {"sport": "archery", "action": "arrows", "attempt_word": "shots"},
]


def _sports_question():
    name = random.choice(_NAMES)
    ctx = random.choice(_SPORTS_CONTEXTS)
    attempts = random.choice(range(20, 121, 5))
    success = random.randint(int(attempts * 0.3), attempts)
    multiplier = round(success / attempts, 4)
    answer = round(multiplier * 100, 1)

    question_text = (
        f"During a {ctx['sport']} match, {name} attempted {attempts} {ctx['action']} "
        f"and successfully scored with {success} of them.\n\n"
        f"Calculate {name}'s success rate as a percentage.\n\n"
        f"Give your answer to 1 decimal place."
    )

    scaffold_steps = [
        {
            "prompt": f"Divide the successful {ctx['action']} by the total {ctx['attempt_word']} to find the multiplier",
            "answer": multiplier,
        },
        {
            "prompt": "Multiply the multiplier by 100 to convert to a percentage",
            "answer": answer,
        },
    ]

    worked = [
        f"Multiplier = {success} ÷ {attempts} = {multiplier}",
        f"Percentage = {multiplier} × 100 = {answer}%",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


_SHOP_ITEMS = [
    "jacket", "pair of trainers", "television", "laptop",
    "bicycle", "sofa", "dining table", "smartphone",
]


def _discount_question():
    item = random.choice(_SHOP_ITEMS)
    original = random.choice(range(40, 601, 10))
    discount = random.choice(range(4, min(original - 2, 200), 2))
    sale = original - discount
    multiplier = round(discount / original, 4)
    answer = round(multiplier * 100, 1)

    question_text = (
        f"A {item} has an original price of £{original}. In a sale, it is reduced to £{sale}.\n\n"
        f"Calculate the discount as a percentage of the original price.\n\n"
        f"Give your answer to 1 decimal place."
    )

    scaffold_steps = [
        {
            "prompt": "Calculate the discount amount (original price − sale price)",
            "answer": float(discount),
        },
        {
            "prompt": "Divide the discount by the original price to find the multiplier",
            "answer": multiplier,
        },
        {
            "prompt": "Multiply the multiplier by 100 to convert to a percentage",
            "answer": answer,
        },
    ]

    worked = [
        f"Discount = £{original} − £{sale} = £{discount}",
        f"Multiplier = {discount} ÷ {original} = {multiplier}",
        f"Discount % = {multiplier} × 100 = {answer}%",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


_SURVEY_CONTEXTS = [
    {"population": "pupils in a school", "group": "walk to school", "total_word": "pupils surveyed"},
    {"population": "people at a cinema", "group": "bought popcorn", "total_word": "people surveyed"},
    {"population": "commuters at a train station", "group": "were delayed", "total_word": "commuters surveyed"},
    {"population": "customers at a cafe", "group": "ordered a hot drink", "total_word": "customers surveyed"},
]


def _survey_question():
    ctx = random.choice(_SURVEY_CONTEXTS)
    total = random.choice(range(80, 601, 20))
    part = random.randint(int(total * 0.1), int(total * 0.9))
    multiplier = round(part / total, 4)
    answer = round(multiplier * 100, 1)

    question_text = (
        f"A survey was carried out on {total} {ctx['population']}.\n\n"
        f"{part} of the {ctx['total_word']} {ctx['group']}.\n\n"
        f"Calculate this as a percentage of those surveyed.\n\n"
        f"Give your answer to 1 decimal place."
    )

    scaffold_steps = [
        {
            "prompt": f"Divide the number who {ctx['group']} by the total surveyed to find the multiplier",
            "answer": multiplier,
        },
        {
            "prompt": "Multiply the multiplier by 100 to convert to a percentage",
            "answer": answer,
        },
    ]

    worked = [
        f"Multiplier = {part} ÷ {total} = {multiplier}",
        f"Percentage = {multiplier} × 100 = {answer}%",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


def generate_percentage_l2():
    return random.choice([
        _profit_loss_question,
        _quality_control_question,
        _test_score_question,
        _sports_question,
        _discount_question,
        _survey_question,
    ])()


# ---------------------------------------------------------------------------
# Calculating the Multiplier
# ---------------------------------------------------------------------------

_CHANGE_CONTEXTS = [
    {"subject": "A shop", "increase_verb": "increases all prices by", "decrease_verb": "reduces all prices by", "noun": "price"},
    {"subject": "A company", "increase_verb": "gives all staff a pay rise of", "decrease_verb": "cuts all staff pay by", "noun": "salary"},
    {"subject": "A car", "increase_verb": "appreciates in value by", "decrease_verb": "depreciates in value by", "noun": "value"},
    {"subject": "A town's population", "increase_verb": "grows by", "decrease_verb": "shrinks by", "noun": "population"},
    {"subject": "A phone company", "increase_verb": "increases its subscription price by", "decrease_verb": "decreases its subscription price by", "noun": "subscription price"},
    {"subject": "A gym", "increase_verb": "puts membership fees up by", "decrease_verb": "reduces membership fees by", "noun": "membership fee"},
]


def generate_percentage_multiplier():
    ctx = random.choice(_CHANGE_CONTEXTS)
    is_increase = random.choice([True, False])
    rate = random.randint(1, 50)
    decimal = round(rate / 100, 2)
    multiplier = round(1 + decimal, 2) if is_increase else round(1 - decimal, 2)
    verb = ctx["increase_verb"] if is_increase else ctx["decrease_verb"]
    sign = "+" if is_increase else "−"

    question_text = (
        f"{ctx['subject']} {verb} {rate}%.\n\n"
        f"Write down the multiplier that would be used to calculate the new {ctx['noun']}."
    )

    scaffold_steps = [
        {"prompt": f"Write {rate}% as a decimal", "answer": decimal},
        {"prompt": f"{'Add' if is_increase else 'Subtract'} this {'to' if is_increase else 'from'} 1 to find the multiplier",
         "answer": multiplier},
    ]

    worked = [
        f"{rate}% = {decimal}",
        f"Multiplier = 1 {sign} {decimal} = {multiplier}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=multiplier,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_MULTIPLIER,
    )


# ---------------------------------------------------------------------------
# Calculating Single Changes
# ---------------------------------------------------------------------------

_SINGLE_CHANGE_CONTEXTS = [
    {"subject": "A laptop", "verb_stem": "costs", "noun": "price"},
    {"subject": "A games console", "verb_stem": "costs", "noun": "price"},
    {"subject": "A car", "verb_stem": "is valued at", "noun": "value"},
    {"subject": "A flat", "verb_stem": "is valued at", "noun": "value"},
    {"subject": "A monthly salary", "verb_stem": "is", "noun": "salary"},
    {"subject": "A small business's annual profit", "verb_stem": "is", "noun": "profit"},
]


def generate_percentage_single_change():
    ctx = random.choice(_SINGLE_CHANGE_CONTEXTS)
    is_increase = random.choice([True, False])
    rate = random.randint(2, 40)
    amount = random.choice(range(200, 20001, 100))
    decimal = round(rate / 100, 2)
    multiplier = round(1 + decimal, 2) if is_increase else round(1 - decimal, 2)
    answer = round(amount * multiplier, 2)
    verb = "increased" if is_increase else "reduced"
    sign = "+" if is_increase else "−"

    question_text = (
        f"{ctx['subject']} {ctx['verb_stem']} £{amount:,}.\n\n"
        f"It is {verb} by {rate}%.\n\n"
        f"Calculate the new {ctx['noun']}."
    )

    scaffold_steps = [
        {"prompt": f"Write {rate}% as a decimal", "answer": decimal},
        {"prompt": f"{'Add' if is_increase else 'Subtract'} this {'to' if is_increase else 'from'} 1 to find the multiplier",
         "answer": multiplier},
        {"prompt": "Multiply the original amount by the multiplier", "answer": answer},
    ]

    worked = [
        f"{rate}% = {decimal}",
        f"Multiplier = 1 {sign} {decimal} = {multiplier}",
        f"New {ctx['noun']} = £{amount:,} × {multiplier} = £{answer:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_SINGLE_CHANGE,
    )


# ---------------------------------------------------------------------------
# Default dispatcher
# ---------------------------------------------------------------------------

def generate_percentage_question():
    return random.choice([
        generate_percentage_l1,
        generate_percentage_l2,
        generate_percentage_multiplier,
        generate_percentage_single_change,
    ])()
