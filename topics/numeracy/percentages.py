import random
from core.models.question_model import Question

NOTES = """
**Finding a Percentage of an Amount:**

1. Divide the amount by **100** to find 1%
2. Multiply by the **percentage** you need

**Example:** What is 35% of 84?
- 1% of 84 = 84 ÷ 100 = 0.84
- 35% of 84 = 35 × 0.84 = **29.4**
"""

NOTES_L2 = """
**Expressing One Amount as a Percentage of Another:**

1. Write the amount as a fraction of the total: **part ÷ whole**
2. Multiply by **100** to convert to a percentage

**Example:** A pupil scores 34 out of 40 in a test.
- Fraction = 34 ÷ 40 = 0.85
- Percentage = 0.85 × 100 = **85%**
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

    answer = round(change / cost * 100, 1)

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
            "prompt": f"Calculate the {verb} as a percentage of the cost price: ({verb} ÷ cost price) × 100",
            "answer": answer,
        },
    ]

    worked = [
        f"{verb.capitalize()} = £{max(sale, cost)} − £{min(sale, cost)} = £{change}",
        f"{verb.capitalize()} % = ({change} ÷ {cost}) × 100 = {answer}%",
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
    fraction = round(faulty / batch, 4)
    answer = round(faulty / batch * 100, 1)

    question_text = (
        f"A quality control inspector at {ctx['setting']} checked a batch of {batch} {ctx['items']}.\n\n"
        f"{faulty} of the {ctx['items']} were found to be {ctx['adj']}.\n\n"
        f"Calculate the percentage of the batch that was {ctx['adj']}.\n\n"
        f"Give your answer to 1 decimal place."
    )

    scaffold_steps = [
        {
            "prompt": f"Write the number {ctx['adj']} as a fraction of the batch size",
            "answer": fraction,
        },
        {
            "prompt": "Convert the fraction to a percentage (× 100)",
            "answer": answer,
        },
    ]

    worked = [
        f"Fraction {ctx['adj']} = {faulty}/{batch}",
        f"Percentage = ({faulty} ÷ {batch}) × 100 = {answer}%",
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
    fraction = round(score / total, 4)
    answer = round(score / total * 100, 1)

    question_text = (
        f"{name} scored {score} marks out of {total} in a {subject} test.\n\n"
        f"Calculate {name}'s score as a percentage.\n\n"
        f"Give your answer to 1 decimal place."
    )

    scaffold_steps = [
        {
            "prompt": "Write the score as a fraction of the total marks",
            "answer": fraction,
        },
        {
            "prompt": "Convert the fraction to a percentage (× 100)",
            "answer": answer,
        },
    ]

    worked = [
        f"Fraction = {score}/{total}",
        f"Percentage = ({score} ÷ {total}) × 100 = {answer}%",
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
    fraction = round(success / attempts, 4)
    answer = round(success / attempts * 100, 1)

    question_text = (
        f"During a {ctx['sport']} match, {name} attempted {attempts} {ctx['action']} "
        f"and successfully scored with {success} of them.\n\n"
        f"Calculate {name}'s success rate as a percentage.\n\n"
        f"Give your answer to 1 decimal place."
    )

    scaffold_steps = [
        {
            "prompt": f"Write the successful {ctx['action']} as a fraction of the total {ctx['attempt_word']}",
            "answer": fraction,
        },
        {
            "prompt": "Convert the fraction to a percentage (× 100)",
            "answer": answer,
        },
    ]

    worked = [
        f"Fraction successful = {success}/{attempts}",
        f"Percentage = ({success} ÷ {attempts}) × 100 = {answer}%",
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
    answer = round(discount / original * 100, 1)

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
            "prompt": "Calculate the discount as a percentage of the original price: (discount ÷ original price) × 100",
            "answer": answer,
        },
    ]

    worked = [
        f"Discount = £{original} − £{sale} = £{discount}",
        f"Discount % = ({discount} ÷ {original}) × 100 = {answer}%",
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
    fraction = round(part / total, 4)
    answer = round(part / total * 100, 1)

    question_text = (
        f"A survey was carried out on {total} {ctx['population']}.\n\n"
        f"{part} of the {ctx['total_word']} {ctx['group']}.\n\n"
        f"Calculate this as a percentage of those surveyed.\n\n"
        f"Give your answer to 1 decimal place."
    )

    scaffold_steps = [
        {
            "prompt": f"Write the number who {ctx['group']} as a fraction of the total surveyed",
            "answer": fraction,
        },
        {
            "prompt": "Convert the fraction to a percentage (× 100)",
            "answer": answer,
        },
    ]

    worked = [
        f"Fraction = {part}/{total}",
        f"Percentage = ({part} ÷ {total}) × 100 = {answer}%",
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
# Default dispatcher
# ---------------------------------------------------------------------------

def generate_percentage_question():
    return random.choice([generate_percentage_l1, generate_percentage_l2])()
