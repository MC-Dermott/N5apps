import random
from core.models.question_model import Question

NOTES_L1 = """
**Direct Proportion:**

Two quantities are in direct proportion when one increases at the same rate as the other
(e.g. more items need proportionally more material).

**Method — cross multiplication:**
If **A** corresponds to **B**, and you want the amount that corresponds to **C**:

**Answer = (A × C) ÷ B**

**Example:** 5 tins of paint are needed to paint 3 rooms. How many tins are needed to paint 5 rooms?
- Answer = (5 × 5) ÷ 3 = 25 ÷ 3 ≈ **8.3 tins**
"""

NOTES_L2 = """
**Comparing Value for Money:**

To compare two deals, find the **price per unit** (per item, per gram, per kilogram, etc.)
for each option. The option with the **lower price per unit** is the better value.

**price per unit = total price ÷ quantity**

**Example:** Option 1: 35 kiwi fruit for £5.95. Option 2: 45 kiwi fruit for £8.10.
- Option 1: 595p ÷ 35 = 17p per kiwi fruit
- Option 2: 810p ÷ 45 = 18p per kiwi fruit
- Option 1 has the lower price per item, so it is **better value**.
"""

NOTES_L3 = """
**Direct Proportion with Unit Conversion:**

Before comparing or scaling quantities, make sure they are in the **same units**.

**Common conversions:**
- 1 litre = 1000 ml
- 1 kg = 1000 g
- 1 m = 100 cm
- 1 km = 1000 m

**Example:** 5 ml of conditioner is needed for every 20,000 ml of tap water.
Calculate the conditioner required for 14 litres of tap water.
- Convert: 14 litres = 14,000 ml
- Conditioner = (5 × 14,000) ÷ 20,000 = 70,000 ÷ 20,000 = **3.5 ml**
"""

# ---------------------------------------------------------------------------
# Level 1 — basic direct proportion (scaling)
# ---------------------------------------------------------------------------

_L1_CONTEXTS = [
    {"item_plural": "tins of paint", "unit_plural": "rooms", "verb": "are needed to paint"},
    {"item_plural": "litres of juice", "unit_plural": "guests", "verb": "are needed for"},
    {"item_plural": "bags of cement", "unit_plural": "metres of path", "verb": "are needed to lay"},
    {"item_plural": "packets of seeds", "unit_plural": "flower beds", "verb": "are needed to plant"},
    {"item_plural": "sheets of paper", "unit_plural": "posters", "verb": "are needed to print"},
    {"item_plural": "boxes of tiles", "unit_plural": "bathrooms", "verb": "are needed to tile"},
    {"item_plural": "bottles of water", "unit_plural": "runners", "verb": "are needed for"},
]


def generate_direct_proportion_l1(calc_mode=False):
    ctx = random.choice(_L1_CONTEXTS)

    quantity1 = quantity2 = amount1 = amount2 = None
    q2_hi = 10 if calc_mode else 16   # calc_mode: q2 stays single-digit (a clean multiplier)
    for _ in range(50):
        q1 = random.randint(2, 9)
        q2 = random.choice([q for q in range(2, q2_hi) if q != q1])
        a1 = random.randint(2, 40)
        if (a1 * q2) % q1 == 0:
            quantity1, quantity2, amount1 = q1, q2, a1
            amount2 = a1 * q2 // q1
            break
    if quantity1 is None:
        quantity1, quantity2, amount1, amount2 = 3, 5, 5, 8  # fallback (rounds to whole below)
        amount2 = round(amount1 * quantity2 / quantity1)

    question_text = (
        f"{amount1} {ctx['item_plural']} {ctx['verb']} {quantity1} {ctx['unit_plural']}.\n\n"
        f"How many {ctx['item_plural']} {ctx['verb']} {quantity2} {ctx['unit_plural']}?"
    )

    scaffold_steps = [
        {"prompt": "Multiply the given amount by the new quantity", "answer": amount1 * quantity2},
        {"prompt": f"Divide by the original quantity to find the amount needed for the new number of {ctx['unit_plural']}",
         "answer": amount2},
    ]

    worked = [
        f"{amount1} {ctx['item_plural']} ÷ {quantity1} {ctx['unit_plural']} × {quantity2} {ctx['unit_plural']}",
        f"= ({amount1} × {quantity2}) ÷ {quantity1}",
        f"= {amount1 * quantity2} ÷ {quantity1}",
        f"= **{amount2} {ctx['item_plural']}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=amount2,
        topic="Numeracy",
        question_type="Direct Proportion",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L1,
    )


# ---------------------------------------------------------------------------
# Level 2 — best value comparisons (price per unit)
# ---------------------------------------------------------------------------

_L2_COUNT_CONTEXTS = [
    {"subject": "Laura", "verb": "buy", "item_plural": "kiwi fruit"},
    {"subject": "Amir", "verb": "buy", "item_plural": "oranges"},
    {"subject": "A corner shop", "verb": "stock", "item_plural": "notebooks"},
    {"subject": "Priya", "verb": "buy", "item_plural": "pencils"},
    {"subject": "A bakery", "verb": "buy", "item_plural": "bread rolls"},
    {"subject": "A café", "verb": "buy", "item_plural": "eggs"},
]

_L2_WEIGHT_CONTEXTS = [
    {"subject": "A supermarket", "item": "rice"},
    {"subject": "A supermarket", "item": "granola"},
    {"subject": "A café", "item": "coffee beans"},
    {"subject": "A shop", "item": "cheese"},
    {"subject": "A shop", "item": "washing powder"},
    {"subject": "A market stall", "item": "flour"},
]

_L2_QTYS = [20, 24, 25, 30, 35, 40, 45, 50, 60, 70, 75, 80]
_L2_QTYS_CALC = [20, 30, 40, 50, 60, 70, 80]   # single-digit × 10 only — clean divisors


def _l2_count_question(calc_mode=False):
    ctx = random.choice(_L2_COUNT_CONTEXTS)

    for _ in range(50):
        qty1, qty2 = random.sample(_L2_QTYS_CALC if calc_mode else _L2_QTYS, 2)
        price1_p = random.randint(150, 1500)
        price2_p = random.randint(150, 1500)
        unit1 = round(price1_p / qty1, 2)
        unit2 = round(price2_p / qty2, 2)
        if abs(unit1 - unit2) >= 0.5:
            break

    price1, price2 = price1_p / 100, price2_p / 100
    better = "Option 1" if unit1 < unit2 else "Option 2"

    question_text = (
        f"{ctx['subject']} wants to {ctx['verb']} {ctx['item_plural']} in bulk.\n\n"
        f"{ctx['subject']} is comparing two deals:\n\n"
        f"- **Option 1:** {qty1} {ctx['item_plural']} for £{price1:.2f}\n"
        f"- **Option 2:** {qty2} {ctx['item_plural']} for £{price2:.2f}\n\n"
        f"Determine which option offers the best value for money.\n\n"
        f"Type **Option 1** or **Option 2**."
    )

    scaffold_steps = [
        {"prompt": "Price per item for Option 1, in pence (price ÷ quantity)", "answer": unit1},
        {"prompt": "Price per item for Option 2, in pence (price ÷ quantity)", "answer": unit2},
        {"prompt": "Which option is better value? (Option 1 or Option 2)", "answer": better},
    ]

    worked = [
        f"Option 1: {price1_p}p ÷ {qty1} = {unit1}p per item",
        f"Option 2: {price2_p}p ÷ {qty2} = {unit2}p per item",
        f"{better} has the lower price per item, so it is **better value**.",
    ]

    return Question(
        question_text=question_text,
        correct_answer=better,
        topic="Numeracy",
        question_type="Direct Proportion",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


_L2_WEIGHTS_G = [200, 250, 300, 400, 500, 600, 750, 800, 900, 1000, 1200, 1500]
_L2_WEIGHTS_G_CALC = [200, 300, 400, 500, 600, 800, 900, 1000]   # single-digit × 100 only


def _l2_weight_question(calc_mode=False):
    ctx = random.choice(_L2_WEIGHT_CONTEXTS)

    for _ in range(50):
        w1, w2 = random.sample(_L2_WEIGHTS_G_CALC if calc_mode else _L2_WEIGHTS_G, 2)
        price1_p = random.randint(100, 800)
        price2_p = random.randint(100, 800)
        unit1 = round(price1_p * 1000 / w1, 1)
        unit2 = round(price2_p * 1000 / w2, 1)
        if abs(unit1 - unit2) >= 2:
            break

    price1, price2 = price1_p / 100, price2_p / 100
    better = "Option 1" if unit1 < unit2 else "Option 2"

    question_text = (
        f"{ctx['subject']} sells {ctx['item']} in two sizes:\n\n"
        f"- **Option 1:** {w1} g for £{price1:.2f}\n"
        f"- **Option 2:** {w2} g for £{price2:.2f}\n\n"
        f"Determine which option offers the best value for money.\n\n"
        f"Type **Option 1** or **Option 2**."
    )

    scaffold_steps = [
        {"prompt": "Price per kilogram for Option 1, in pence (price ÷ weight in grams × 1000)", "answer": unit1},
        {"prompt": "Price per kilogram for Option 2, in pence (price ÷ weight in grams × 1000)", "answer": unit2},
        {"prompt": "Which option is better value? (Option 1 or Option 2)", "answer": better},
    ]

    worked = [
        f"Option 1: {price1_p}p ÷ {w1} g × 1000 = {unit1}p per kg",
        f"Option 2: {price2_p}p ÷ {w2} g × 1000 = {unit2}p per kg",
        f"{better} has the lower price per kilogram, so it is **better value**.",
    ]

    return Question(
        question_text=question_text,
        correct_answer=better,
        topic="Numeracy",
        question_type="Direct Proportion",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


def generate_direct_proportion_l2(calc_mode=False):
    return random.choice([_l2_count_question, _l2_weight_question])(calc_mode=calc_mode)


# ---------------------------------------------------------------------------
# Level 3 — direct proportion or best value, requiring a unit conversion
# ---------------------------------------------------------------------------

_L3_SCALING_CONTEXTS = [
    {"subject": "Jamel", "activity": "keeps fish", "detail": "To make tap water safe for fish, a conditioner is added.",
     "dependent": "conditioner", "independent": "tap water"},
    {"subject": "A gardener", "activity": "waters a lawn", "detail": "A fertiliser is diluted in water before watering.",
     "dependent": "fertiliser", "independent": "water"},
    {"subject": "A swimming pool company", "activity": "treats pool water", "detail": "Chlorine is added to keep the pool water clean.",
     "dependent": "chlorine", "independent": "pool water"},
    {"subject": "A farmer", "activity": "sprays crops", "detail": "A pesticide is mixed with water before spraying.",
     "dependent": "pesticide", "independent": "water"},
]

_L3_TARGET_LITRES = [2, 3, 5, 7, 10, 12, 14, 15, 18, 20, 25]
_L3_INDEP_ML = [10000, 20000, 25000, 40000, 50000]
_L3_INDEP_ML_CALC = [10000, 20000, 40000, 50000]   # drop 25000 — not single-digit × 1000
_L3_DEP_ML = [2, 3, 4, 5, 6, 8, 10]


def _l3_conversion_scaling(calc_mode=False):
    ctx = random.choice(_L3_SCALING_CONTEXTS)
    indep_ml = random.choice(_L3_INDEP_ML_CALC if calc_mode else _L3_INDEP_ML)
    dep_ml = random.choice(_L3_DEP_ML)
    target_litres = random.choice(_L3_TARGET_LITRES)
    target_ml = target_litres * 1000
    answer = round(dep_ml * target_ml / indep_ml, 2)
    if answer == int(answer):
        answer = int(answer)

    question_text = (
        f"{ctx['subject']} {ctx['activity']}.\n\n"
        f"{ctx['detail']}\n\n"
        f"The volume of {ctx['dependent']} required is directly proportional to the volume of {ctx['independent']}.\n\n"
        f"{dep_ml} ml of {ctx['dependent']} must be used for every {indep_ml:,} ml of {ctx['independent']}.\n\n"
        f"Calculate the volume of {ctx['dependent']} required for {target_litres} litres of {ctx['independent']}."
    )

    scaffold_steps = [
        {"prompt": "Convert the target volume to ml (× 1000)", "answer": target_ml},
        {"prompt": "Multiply the given dependent-quantity rate by the converted target volume", "answer": dep_ml * target_ml},
        {"prompt": f"Divide by the given independent-quantity rate to find the volume of {ctx['dependent']} needed", "answer": answer},
    ]

    worked = [
        f"Convert {target_litres} litres = {target_litres} × 1000 = {target_ml:,} ml",
        f"{ctx['dependent'].capitalize()} required = ({dep_ml} × {target_ml:,}) ÷ {indep_ml:,}",
        f"= {dep_ml * target_ml:,} ÷ {indep_ml:,}",
        f"= **{answer} ml**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Direct Proportion",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L3,
    )


def _l3_conversion_value():
    ctx = random.choice(_L2_WEIGHT_CONTEXTS)

    for _ in range(50):
        w1_g = random.choice(_L2_WEIGHTS_G)
        w2_kg = random.choice([1, 1.2, 1.5, 2, 2.5, 3])
        price1_p = random.randint(100, 800)
        price2_p = random.randint(150, 1200)
        unit1 = round(price1_p * 1000 / w1_g, 1)
        unit2 = round(price2_p / w2_kg, 1)
        if abs(unit1 - unit2) >= 2:
            break

    price1, price2 = price1_p / 100, price2_p / 100
    w2_g = w2_kg * 1000
    better = "Option 1" if unit1 < unit2 else "Option 2"

    question_text = (
        f"{ctx['subject']} sells {ctx['item']} in two sizes:\n\n"
        f"- **Option 1:** {w1_g} g for £{price1:.2f}\n"
        f"- **Option 2:** {w2_kg} kg for £{price2:.2f}\n\n"
        f"Determine which option offers the best value for money.\n\n"
        f"Type **Option 1** or **Option 2**."
    )

    scaffold_steps = [
        {"prompt": "Convert Option 1's weight to kg", "answer": round(w1_g / 1000, 3)},
        {"prompt": "Price per kilogram for Option 1, in pence (price ÷ weight in kg × 100)", "answer": unit1},
        {"prompt": "Price per kilogram for Option 2, in pence (price ÷ weight in kg × 100)", "answer": unit2},
        {"prompt": "Which option is better value? (Option 1 or Option 2)", "answer": better},
    ]

    worked = [
        f"Convert {w1_g} g = {w1_g / 1000} kg",
        f"Option 1: £{price1:.2f} ÷ {w1_g / 1000} kg = {unit1}p per kg",
        f"Option 2: £{price2:.2f} ÷ {w2_kg} kg = {unit2}p per kg",
        f"{better} has the lower price per kilogram, so it is **better value**.",
    ]

    return Question(
        question_text=question_text,
        correct_answer=better,
        topic="Numeracy",
        question_type="Direct Proportion",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L3,
    )


def generate_direct_proportion_l3(calc_mode=False):
    # _l3_conversion_value divides by an arbitrary weight/kg figure with no clean-divisor
    # variant available, so calc_mode always takes the scaling sub-type instead.
    if calc_mode:
        return _l3_conversion_scaling(calc_mode=True)
    return random.choice([_l3_conversion_scaling, _l3_conversion_value])()


# ---------------------------------------------------------------------------
# Default dispatcher
# ---------------------------------------------------------------------------

def generate_direct_proportion_question(calc_mode=False):
    return random.choice([
        generate_direct_proportion_l1,
        generate_direct_proportion_l2,
        generate_direct_proportion_l3,
    ])(calc_mode=calc_mode)
