import random
from core.models.question_model import Question

NOTES = """
**Liquid Volume and Weight:**

Key conversions:
- 1 litre = 1000 ml
- 1 litre of water / soft drink weighs 1 kilogram (1 kg = 1000 g)
- So: volume in ml = weight in grams  (e.g. 200 ml of drink = 200 g)
- 1 tonne = 1000 kg

**Steps:**
1. Weight of liquid in one bottle = bottle volume in ml → same number in grams
2. Add the empty bottle weight → total weight per full bottle
3. Multiply by bottles per tray, then by number of trays → total weight (g)
4. Convert to kg (÷ 1000) and compare to van capacity
"""

_PRODUCTS = [
    ("soft drink", "bottle", "bottles"),
    ("fruit juice", "bottle", "bottles"),
    ("water", "bottle", "bottles"),
    ("energy drink", "can", "cans"),
]


def generate_liquid_volume():
    product, container_sg, container_pl = random.choice(_PRODUCTS)
    bottle_ml = random.choice([200, 250, 330, 500])
    bottle_weight_g = random.choice([20, 25, 30, 40, 50])
    bottles_per_tray = random.choice([12, 24, 48, 60, 100, 120, 124])
    num_trays = random.randint(20, 50)
    van_kg = 1000

    liquid_g = bottle_ml          # 1 litre = 1 kg = 1000 g, so X ml = X g
    total_per_bottle_g = liquid_g + bottle_weight_g
    total_bottles = bottles_per_tray * num_trays
    total_g = total_bottles * total_per_bottle_g
    total_kg = round(total_g / 1000, 3)

    can_deliver = total_kg <= van_kg
    answer = "Yes" if can_deliver else "No"

    question_text = (
        f"A company sells {product} in {bottle_ml} ml {container_pl}. "
        f"Each empty {container_sg} weighs {bottle_weight_g} g.\n\n"
        f"To transport the full {container_pl}, they are packaged in trays of {bottles_per_tray} {container_pl}.\n\n"
        f"A shop orders {num_trays} trays. "
        f"The delivery van can take a maximum load of 1 tonne (1000 kg = 1 tonne).\n\n"
        f"1 litre of {product} weighs 1 kilogram.\n\n"
        f"Can the shop's order be delivered in one van load? "
        f"Use your calculations to justify your answer. Type **Yes** or **No**."
    )

    scaffold_steps = [
        {"prompt": f"Weight of {product} in one {container_sg} (in grams)", "answer": liquid_g},
        {"prompt": f"Total weight of one full {container_sg} (liquid + {container_sg})", "answer": total_per_bottle_g},
        {"prompt": f"Total number of {container_pl} ordered", "answer": total_bottles},
        {"prompt": f"Total weight of all {container_pl} in grams", "answer": total_g},
        {"prompt": "Total weight in kg (÷ 1000)", "answer": total_kg},
        {"prompt": "Is this ≤ 1000 kg? (Yes or No)", "answer": answer},
    ]

    op = "≤" if can_deliver else ">"
    verdict = "can" if can_deliver else "cannot"
    worked = [
        f"Conversions: 1 litre = 1 kg = 1000 g, so {bottle_ml} ml = {liquid_g} g",
        f"Weight per full {container_sg} = {liquid_g} g + {bottle_weight_g} g = {total_per_bottle_g} g",
        f"Total {container_pl} = {bottles_per_tray} × {num_trays} = {total_bottles}",
        f"Total weight = {total_bottles} × {total_per_bottle_g} = {total_g:,} g = {total_kg} kg",
        f"Since {total_kg} kg {op} 1000 kg, the order **{verdict}** be delivered in one van load.",
        f"**Answer: {answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numbers and Money",
        question_type="Liquid Volume",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
