import random
from core.models.question_model import Question

NOTES = """
**Reverse Percentages:**

To find the **original** price before a percentage change:

1. Find the **multiplier**:
   - Decrease of X%: multiplier = 1 − X/100
   - Increase of X%:  multiplier = 1 + X/100

2. **Divide** the given (new) price by the multiplier

**Example:** A dress is reduced by 20%. Sale price is £720.
- Multiplier = 1 − 0.20 = **0.80**
- Original = £720 ÷ 0.80 = **£900**

**Common mistake:** Do NOT add/subtract the percentage of the sale price —
the percentage was taken off the *original*, not the new price.
"""

_DECREASE_TEMPLATES = [
    ("{item} is reduced by {pct}% in a sale. The sale price is £{new_price:,}. "
     "Calculate the original price of the {item_lower}."),
    ("A {item_lower} has been reduced by {pct}% to £{new_price:,}. "
     "What was the price before the reduction?"),
    ("In a sale, a {item_lower} is discounted by {pct}%. "
     "The sale price is £{new_price:,}. "
     "Calculate the price before the sale."),
    ("A {item_lower} costs £{new_price:,} after a {pct}% reduction. "
     "Find the original price."),
]

_INCREASE_TEMPLATES = [
    ("The price of a {item_lower} increases by {pct}%. "
     "The new price is £{new_price:,}. "
     "Calculate the price before the increase."),
    ("After a {pct}% price rise, a {item_lower} costs £{new_price:,}. "
     "What was the original price?"),
    ("VAT of {pct}% is added to the price of a {item_lower}. "
     "The price including VAT is £{new_price:,}. "
     "Calculate the price before VAT."),
    ("A {item_lower} costs £{new_price:,} after a {pct}% increase. "
     "Find the price before the increase."),
]

_ITEMS = [
    "Wedding dress", "Laptop", "Sofa", "Television", "Bicycle",
    "Camera", "Coat", "Washing machine", "Fridge", "Dining table",
    "Smartphone", "Handbag", "Suit", "Microwave", "Armchair",
]


def generate_reverse_percentage_question():
    item = random.choice(_ITEMS)
    item_lower = item.lower()

    # Pick original price as a round number, then derive new price
    original = random.choice(range(200, 2001, 50))
    pct = random.choice([5, 10, 15, 20, 25, 30, 40])
    direction = random.choice(["decrease", "increase"])

    if direction == "decrease":
        multiplier = round(1 - pct / 100, 2)
        new_price = round(original * multiplier, 2)
        template = random.choice(_DECREASE_TEMPLATES)
    else:
        multiplier = round(1 + pct / 100, 2)
        new_price = round(original * multiplier, 2)
        template = random.choice(_INCREASE_TEMPLATES)

    # Ensure new_price is a whole number (looks cleaner in questions)
    if new_price != int(new_price):
        # Regenerate with a compatible original
        for candidate in range(200, 3001, 10):
            trial = round(candidate * multiplier, 2)
            if trial == int(trial):
                original = candidate
                new_price = int(trial)
                break

    new_price = int(new_price)
    original_display = round(original, 2)

    question_text = template.format(
        item=item,
        item_lower=item_lower,
        pct=pct,
        new_price=new_price,
    )

    scaffold_steps = [
        {
            "prompt": (
                f"Find the multiplier "
                f"({'1 − ' if direction == 'decrease' else '1 + '}{pct}/100)"
            ),
            "answer": multiplier,
        },
        {
            "prompt": f"Divide £{new_price:,} by the multiplier to find the original price",
            "answer": original_display,
        },
    ]

    worked = [
        f"Multiplier = {'1 − ' if direction == 'decrease' else '1 + '}{pct}/100 = {multiplier}",
        f"Original price = £{new_price:,} ÷ {multiplier} = £{original_display:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=original_display,
        topic="Finance",
        question_type="Reverse Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
