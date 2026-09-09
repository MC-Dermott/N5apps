import random
from core.models.question_model import Question

NOTES = """
**Sharing an Amount in a Given Ratio:**

1. Add up the parts of the ratio to find the total number of shares.
2. Divide the total amount by the total number of shares to find the value of **one share**.
3. Multiply the value of one share by the number of shares for the part you need.

**Example:** Share £360 in the ratio 2:3:4.
- Total shares = 2 + 3 + 4 = 9
- One share = £360 ÷ 9 = £40
- Largest share = 4 × £40 = £160
"""

NOTES_L2 = """
**Finding a Total from One Part of a Ratio:**

1. Use the amount you are given and its ratio number to find the value of **one share**.
2. Add up all the parts of the ratio to find the total number of shares.
3. Multiply the value of one share by the total number of shares.

**Example:** A:B:C = 6:2:7. If C = 56:
- One share = 56 ÷ 7 = 8
- Total shares = 6 + 2 + 7 = 15
- Total = 8 × 15 = 120
"""

_CONTEXTS = [
    {"subject": "Pepe", "verb": "sold", "item_plural": "fire extinguishers",
     "categories": ["water", "foam", "powder"]},
    {"subject": "Greenfield Garden Centre", "verb": "sold", "item_plural": "plants",
     "categories": ["shrubs", "bedding plants", "trees"]},
    {"subject": "The Riverside Cinema", "verb": "sold", "item_plural": "tickets",
     "categories": ["standard", "premium", "VIP"]},
    {"subject": "Highland Bakery", "verb": "baked", "item_plural": "loaves",
     "categories": ["white", "wholemeal", "seeded"]},
    {"subject": "Northside Sports", "verb": "sold", "item_plural": "football shirts",
     "categories": ["home", "away", "third"]},
    {"subject": "Coastal Ice Cream Co.", "verb": "sold", "item_plural": "ice creams",
     "categories": ["vanilla", "chocolate", "strawberry"]},
    {"subject": "Bright Books", "verb": "sold", "item_plural": "books",
     "categories": ["fiction", "non-fiction", "children's"]},
    {"subject": "Summit Outdoor Store", "verb": "sold", "item_plural": "tents",
     "categories": ["2-person", "4-person", "6-person"]},
]

_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def _random_ratio():
    parts = random.sample(range(1, 10), 3)
    return tuple(parts)


# ---------------------------------------------------------------------------
# Level 1 — split an amount into unequal quantities
# ---------------------------------------------------------------------------

def generate_ratio_l1():
    ctx = random.choice(_CONTEXTS)
    month = random.choice(_MONTHS)
    parts = _random_ratio()
    total_shares = sum(parts)
    share_value = random.choice(range(4, 41, 2))
    total = share_value * total_shares
    ask_idx = random.randrange(3)
    cats = ctx["categories"]
    ask_category = cats[ask_idx]
    ask_amount = parts[ask_idx] * share_value
    ratio_str = ":".join(str(p) for p in parts)

    question_text = (
        f"{ctx['subject']} {ctx['verb']} {total:,} {ctx['item_plural']} in {month}.\n\n"
        f"They were {ctx['verb']} in the ratio "
        f"{cats[0]} : {cats[1]} : {cats[2]} = {ratio_str} respectively.\n\n"
        f"Calculate the number of **{ask_category}** {ctx['item_plural']} sold."
    )

    scaffold_steps = [
        {"prompt": "Total number of ratio shares (add up the ratio parts)", "answer": total_shares},
        {"prompt": "Value of one share (total ÷ total number of shares)", "answer": share_value},
        {"prompt": f"Number of {ask_category} {ctx['item_plural']} (its ratio number × value of one share)", "answer": ask_amount},
    ]

    worked = [
        f"Total shares = {' + '.join(str(p) for p in parts)} = {total_shares}",
        f"One share = {total:,} ÷ {total_shares} = {share_value}",
        f"{ask_category.capitalize()} = {parts[ask_idx]} × {share_value} = {ask_amount}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=ask_amount,
        topic="Numeracy",
        question_type="Ratio",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 2 — calculate a total when given one of the ratio amounts
# ---------------------------------------------------------------------------

def generate_ratio_l2():
    ctx = random.choice(_CONTEXTS)
    month = random.choice(_MONTHS)
    parts = _random_ratio()
    total_shares = sum(parts)
    share_value = random.choice(range(4, 41, 2))
    given_idx = random.randrange(3)
    given_amount = parts[given_idx] * share_value
    total = share_value * total_shares
    cats = ctx["categories"]
    given_category = cats[given_idx]
    ratio_str = ":".join(str(p) for p in parts)

    question_text = (
        f"{ctx['subject']} {ctx['verb']} three different types of {ctx['item_plural']}.\n\n"
        f"In {month} {ctx['subject']} {ctx['verb']} {cats[0]}, {cats[1]} and {cats[2]} "
        f"{ctx['item_plural']} in the ratio {ratio_str} respectively.\n\n"
        f"{ctx['subject']} {ctx['verb']} {given_amount:,} {given_category} {ctx['item_plural']} in {month}.\n\n"
        f"Calculate the **total** number of {ctx['item_plural']} sold in {month}."
    )

    scaffold_steps = [
        {"prompt": "Value of one ratio share (given amount ÷ its ratio number)", "answer": share_value},
        {"prompt": "Total number of ratio shares (add up the ratio parts)", "answer": total_shares},
        {"prompt": f"Total number of {ctx['item_plural']} (value of one share × total number of shares)", "answer": total},
    ]

    worked = [
        f"One share = {given_amount:,} ÷ {parts[given_idx]} = {share_value}",
        f"Total shares = {' + '.join(str(p) for p in parts)} = {total_shares}",
        f"Total {ctx['item_plural']} = {share_value} × {total_shares} = {total:,}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=total,
        topic="Numeracy",
        question_type="Ratio",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


# ---------------------------------------------------------------------------
# Default dispatcher
# ---------------------------------------------------------------------------

def generate_ratio_question():
    return random.choice([generate_ratio_l1, generate_ratio_l2])()
