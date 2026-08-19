import math
import random
from fractions import Fraction
from core.models.question_model import Question

NOTES = """
**Finding a Fraction of an Amount:**

1. Divide the amount by the **denominator** (bottom number) to find the unit fraction
2. Multiply that result by the **numerator** (top number)

**Example:** What is 3/5 of 40?
- 1/5 of 40 = 40 ÷ 5 = 8
- 3/5 of 40 = 3 × 8 = **24**
"""

FRACTION_PAIRS = [
    (2, 3), (3, 4), (2, 5), (3, 5),
    (5, 6), (3, 8), (5, 8), (7, 10),
    (4, 5), (2, 7), (5, 9), (7, 8),
]

_N4_FRACTION_PAIRS = [
    (1, 2), (1, 4), (3, 4), (1, 3), (2, 3), (1, 5), (2, 5),
]


def generate_fraction_question_n4():
    numerator, denominator = random.choice(_N4_FRACTION_PAIRS)
    multiplier = random.randint(2, 6)
    amount = denominator * multiplier

    unit_value = amount // denominator
    answer = unit_value * numerator

    scaffold_steps = [
        {
            "prompt": "Divide the amount by the denominator",
            "answer": round(amount / denominator, 2)
        },
        {
            "prompt": "Multiply your result by the numerator",
            "answer": float(answer)
        }
    ]

    return Question(
        question_text=f"What is {numerator}/{denominator} of {amount}?",
        correct_answer=answer,
        topic="Numeracy",
        question_type="Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=[
            f"1/{denominator} of {amount} = {amount} ÷ {denominator} = {unit_value}",
            f"{numerator}/{denominator} of {amount} = {numerator} × {unit_value} = {answer}",
        ],
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Exam Style — adding fractions (2, occasionally 3) then subtracting the
# total from a whole (usually 1, sometimes 2 or 3), set in real-world contexts
# ---------------------------------------------------------------------------

EXAM_NOTES = """
**Adding and Subtracting Fractions (Exam Style):**

1. Find the **lowest common denominator** of the fractions
2. Convert each fraction to an equivalent fraction over that denominator
3. **Add** the numerators to combine the fractions
4. **Subtract** the total from the whole amount to find what's left

**Example:** A recipe is 1/6 butter, 1/3 sugar and 1/4 chocolate chips. What fraction is flour?
- Common denominator of 6, 3, 4 = 12
- 1/6 + 1/3 + 1/4 = 2/12 + 4/12 + 3/12 = 9/12 = 3/4
- Flour = 1 − 3/4 = **1/4**
"""

_EXAM_NAMES = [
    "Amy", "Callum", "Catriona", "Connor", "Douglas", "Eilidh",
    "Ewan", "Freya", "Hamish", "Isla", "Jamie", "Kirsty",
    "Laura", "Liam", "Megan", "Ramani", "Ross", "Stuart",
]

_EXAM_FRACTION_POOL = [
    (1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5),
    (1, 6), (5, 6), (1, 8), (3, 8), (5, 8), (7, 8),
    (1, 10), (3, 10), (7, 10), (9, 10),
    (1, 12), (5, 12), (7, 12), (11, 12),
]

_EXAM_LARGE_FRACTION_POOL = [
    (1, 2), (2, 3), (3, 4), (3, 5), (4, 5), (5, 6), (5, 8), (7, 8), (7, 10), (9, 10),
]


def _fstr(frac):
    return f"{frac.numerator}/{frac.denominator}"


def _sample_distinct_denominators(pool, n):
    for _ in range(30):
        chosen = random.sample(pool, n)
        if len({d for _, d in chosen}) == n:
            return chosen
    return random.sample(pool, n)


def _pick_valid_combo(pool, n_terms, whole, max_den=100):
    fracs = total = remainder = None
    for _ in range(50):
        fracs = _sample_distinct_denominators(pool, n_terms)
        total = sum((Fraction(n, d) for n, d in fracs), Fraction(0))
        remainder = Fraction(whole) - total
        if remainder.numerator > 0 and remainder.denominator > 1 and remainder.denominator <= max_den:
            break
    return fracs, total, remainder


def _lcm_lines(fracs):
    dens = [d for _, d in fracs]
    lcd = math.lcm(*dens)
    equiv_lines = []
    numerators = []
    for n, d in fracs:
        factor = lcd // d
        en = n * factor
        equiv_lines.append(f"{n}/{d} = {en}/{lcd}")
        numerators.append(en)
    add_line = " + ".join(f"{en}/{lcd}" for en in numerators) + f" = {sum(numerators)}/{lcd}"
    return lcd, equiv_lines, add_line


_ITEM_CONTEXTS = [
    {"item": "cake", "plural": "cakes"},
    {"item": "pizza", "plural": "pizzas"},
    {"item": "chocolate bar", "plural": "chocolate bars"},
    {"item": "loaf of bread", "plural": "loaves of bread"},
    {"item": "carton of juice", "plural": "cartons of juice"},
    {"item": "cheesecake", "plural": "cheesecakes"},
]

_ITEM_GROUPS = [
    "the guests", "the family", "the classmates", "the neighbours",
    "the team", "the visitors", "the pupils", "the staff",
]

_OCCASIONS = [
    "a birthday party", "a family gathering", "the school fair",
    "a bake sale", "a picnic", "a celebration",
]

_ORDINALS = ["first", "second", "third"]
_NUMBER_WORDS = {2: "two", 3: "three"}


def _cake_leftover_question():
    n_terms = random.choices([2, 3], weights=[70, 30])[0]
    ctx = random.choice(_ITEM_CONTEXTS)
    name = random.choice(_EXAM_NAMES)
    occasion = random.choice(_OCCASIONS)
    groups = random.sample(_ITEM_GROUPS, n_terms)
    fracs, total, remainder = _pick_valid_combo(_EXAM_LARGE_FRACTION_POOL, n_terms, n_terms)

    lines = [f"{name} bought {_NUMBER_WORDS[n_terms]} identical {ctx['plural']} for {occasion}."]
    for i, (grp, (num, den)) in enumerate(zip(groups, fracs)):
        lines.append(f"{grp.capitalize()} ate {num}/{den} of the {_ORDINALS[i]} {ctx['item']}.")
    lines.append(f"Calculate the **total** amount of {ctx['item']} left over.")
    lines.append(f"Give your answer as a fraction of a {ctx['item']}.")
    question_text = "\n\n".join(lines)

    lcd, equiv_lines, add_line = _lcm_lines(fracs)
    eaten_str = _fstr(total)
    answer_str = _fstr(remainder)
    eaten_list_str = ", ".join(f"{num}/{den}" for num, den in fracs)

    scaffold_steps = [
        {"prompt": f"Find the lowest common denominator of {eaten_list_str}", "answer": float(lcd)},
        {"prompt": "Add the fractions eaten, using equivalent fractions over the common denominator", "answer": eaten_str},
        {"prompt": f"Subtract the total eaten from {n_terms} to find the amount left over", "answer": answer_str},
    ]

    worked = equiv_lines + [
        add_line,
        f"Total eaten = {eaten_str}",
        f"Amount left over = {n_terms} − {eaten_str} = {answer_str}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer_str,
        topic="Numeracy",
        question_type="Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=EXAM_NOTES,
    )


_DISHES = [
    "cookie dough", "bread", "cake", "pancake batter", "granola bar",
    "trail mix", "flapjack", "muffin",
]

_INGREDIENTS = [
    "butter", "sugar", "flour", "chocolate chips", "oats", "raisins",
    "honey", "cocoa powder", "milk powder", "desiccated coconut",
]


def _recipe_mix_question():
    n_terms = random.choices([2, 3], weights=[70, 30])[0]
    dish = random.choice(_DISHES)
    ingredients = random.sample(_INGREDIENTS, n_terms + 1)
    given_ingredients = ingredients[:n_terms]
    remainder_ingredient = ingredients[n_terms]
    fracs, total, remainder = _pick_valid_combo(_EXAM_FRACTION_POOL, n_terms, 1)

    lines = [f"A basic {dish} mix requires {', '.join(given_ingredients)} and {remainder_ingredient}."]
    for (num, den), ingredient in zip(fracs, given_ingredients):
        lines.append(f"- {num}/{den} of the mix is {ingredient}")
    lines.append(f"- The rest of the mix is {remainder_ingredient}")
    lines.append(f"Calculate the fraction of the mix that is {remainder_ingredient}.")
    question_text = "\n\n".join(lines)

    lcd, equiv_lines, add_line = _lcm_lines(fracs)
    total_str = _fstr(total)
    answer_str = _fstr(remainder)
    given_list_str = ", ".join(f"{num}/{den}" for num, den in fracs)

    scaffold_steps = [
        {"prompt": f"Find the lowest common denominator of {given_list_str}", "answer": float(lcd)},
        {"prompt": "Add the given fractions together", "answer": total_str},
        {"prompt": f"Subtract the total from 1 to find the fraction that is {remainder_ingredient}", "answer": answer_str},
    ]

    worked = equiv_lines + [
        add_line,
        f"Total of given ingredients = {total_str}",
        f"{remainder_ingredient.capitalize()} = 1 − {total_str} = {answer_str}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer_str,
        topic="Numeracy",
        question_type="Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=EXAM_NOTES,
    )


_ROLES = [
    "head prefect", "class president", "form captain", "sports captain",
    "charity representative", "eco committee leader",
]


def _election_votes_question():
    n_terms = random.choices([2, 3], weights=[75, 25])[0]
    role = random.choice(_ROLES)
    candidates = random.sample(_EXAM_NAMES, n_terms + 1)
    given_candidates = candidates[:n_terms]
    remainder_candidate = candidates[n_terms]
    fracs, total, remainder = _pick_valid_combo(_EXAM_FRACTION_POOL, n_terms, 1)

    lines = [f"At a school, pupils voted to elect a {role}."]
    for (num, den), candidate in zip(fracs, given_candidates):
        lines.append(f"- {candidate} received {num}/{den} of the votes.")
    lines.append(f"- {remainder_candidate} received the rest of the votes.")
    lines.append(f"Calculate the fraction of the votes that {remainder_candidate} received.")
    question_text = "\n\n".join(lines)

    lcd, equiv_lines, add_line = _lcm_lines(fracs)
    total_str = _fstr(total)
    answer_str = _fstr(remainder)
    given_list_str = ", ".join(f"{num}/{den}" for num, den in fracs)

    scaffold_steps = [
        {"prompt": f"Find the lowest common denominator of {given_list_str}", "answer": float(lcd)},
        {"prompt": "Add the given fractions of the votes together", "answer": total_str},
        {"prompt": f"Subtract the total from 1 to find {remainder_candidate}'s fraction of the votes", "answer": answer_str},
    ]

    worked = equiv_lines + [
        add_line,
        f"Total of the other candidates = {total_str}",
        f"{remainder_candidate}'s share = 1 − {total_str} = {answer_str}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer_str,
        topic="Numeracy",
        question_type="Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=EXAM_NOTES,
    )


_CROPS = [
    "wheat", "barley", "potatoes", "carrots", "peas", "oats", "beans", "cabbages",
]


def _field_crops_question():
    n_terms = random.choices([2, 3], weights=[70, 30])[0]
    crops = random.sample(_CROPS, n_terms + 1)
    given_crops = crops[:n_terms]
    remainder_crop = crops[n_terms]
    fracs, total, remainder = _pick_valid_combo(_EXAM_FRACTION_POOL, n_terms, 1)

    lines = ["A farmer divides a field between different crops."]
    for (num, den), crop in zip(fracs, given_crops):
        lines.append(f"- {num}/{den} of the field is used for {crop}")
    lines.append(f"- The rest of the field is used for {remainder_crop}")
    lines.append(f"Calculate the fraction of the field used for {remainder_crop}.")
    question_text = "\n\n".join(lines)

    lcd, equiv_lines, add_line = _lcm_lines(fracs)
    total_str = _fstr(total)
    answer_str = _fstr(remainder)
    given_list_str = ", ".join(f"{num}/{den}" for num, den in fracs)

    scaffold_steps = [
        {"prompt": f"Find the lowest common denominator of {given_list_str}", "answer": float(lcd)},
        {"prompt": "Add the given fractions of the field together", "answer": total_str},
        {"prompt": f"Subtract the total from 1 to find the fraction used for {remainder_crop}", "answer": answer_str},
    ]

    worked = equiv_lines + [
        add_line,
        f"Total of the other crops = {total_str}",
        f"Fraction for {remainder_crop} = 1 − {total_str} = {answer_str}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer_str,
        topic="Numeracy",
        question_type="Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=EXAM_NOTES,
    )


_ACTIVITIES = [
    "sleeping", "at school", "doing homework", "playing sport",
    "watching TV", "eating meals", "travelling", "relaxing",
]


def _daily_routine_question():
    n_terms = random.choices([2, 3], weights=[70, 30])[0]
    name = random.choice(_EXAM_NAMES)
    activities = random.sample(_ACTIVITIES, n_terms + 1)
    given_activities = activities[:n_terms]
    remainder_activity = activities[n_terms]
    fracs, total, remainder = _pick_valid_combo(_EXAM_FRACTION_POOL, n_terms, 1)

    lines = [f"{name} kept a record of a typical day."]
    for (num, den), activity in zip(fracs, given_activities):
        lines.append(f"- {num}/{den} of the day is spent {activity}")
    lines.append(f"- The rest of the day is spent {remainder_activity}")
    lines.append(f"Calculate the fraction of the day {name} spends {remainder_activity}.")
    question_text = "\n\n".join(lines)

    lcd, equiv_lines, add_line = _lcm_lines(fracs)
    total_str = _fstr(total)
    answer_str = _fstr(remainder)
    given_list_str = ", ".join(f"{num}/{den}" for num, den in fracs)

    scaffold_steps = [
        {"prompt": f"Find the lowest common denominator of {given_list_str}", "answer": float(lcd)},
        {"prompt": "Add the given fractions of the day together", "answer": total_str},
        {"prompt": f"Subtract the total from 1 to find the fraction spent {remainder_activity}", "answer": answer_str},
    ]

    worked = equiv_lines + [
        add_line,
        f"Total of the other activities = {total_str}",
        f"Fraction spent {remainder_activity} = 1 − {total_str} = {answer_str}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer_str,
        topic="Numeracy",
        question_type="Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=EXAM_NOTES,
    )


def generate_fraction_exam_style():
    return random.choice([
        _cake_leftover_question,
        _recipe_mix_question,
        _election_votes_question,
        _field_crops_question,
        _daily_routine_question,
    ])()


def generate_fraction_question():
    numerator, denominator = random.choice(FRACTION_PAIRS)
    multiplier = random.randint(3, 15)
    amount = denominator * multiplier

    unit_value = amount // denominator
    answer = unit_value * numerator

    scaffold_steps = [
        {
            "prompt": "Divide the amount by the denominator",
            "answer": round(amount / denominator, 2)
        },
        {
            "prompt": "Multiply your result by the numerator",
            "answer": float(answer)
        }
    ]

    return Question(
        question_text=f"What is {numerator}/{denominator} of {amount}?",
        correct_answer=answer,
        topic="Numeracy",
        question_type="Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=[
            f"1/{denominator} of {amount} = {amount} ÷ {denominator} = {unit_value}",
            f"{numerator}/{denominator} of {amount} = {numerator} × {unit_value} = {answer}",
        ],
        notes=NOTES,
    )
