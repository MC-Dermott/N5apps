import random
from math import gcd
from core.models.question_model import Question

NOTES = """
**Adding Fractions with Different Denominators:**

1. Find the **Lowest Common Denominator (LCD)** — the smallest number both denominators divide into
2. Convert each fraction so it has the LCD as its denominator
3. Add the fractions
4. Subtract from 1 to find the remainder fraction

**Example:** 2/5 chose pizza, 1/4 chose chips. What fraction chose curry?
- LCD of 5 and 4 = **20**
- 2/5 = 8/20,   1/4 = 5/20
- Pizza & chips = 8/20 + 5/20 = **13/20**
- Curry = 1 − 13/20 = 20/20 − 13/20 = **7/20**

*Tip: S&K (Smile and Kiss) — Same denominator → Keep it, add the tops.*
"""

# (a, b, c, d): fractions a/b and c/d; their sum must be < 1
_FRACTION_PARAMS = [
    (2, 5, 1, 4),
    (1, 3, 2, 5),
    (3, 8, 1, 4),
    (2, 5, 1, 3),
    (1, 4, 3, 8),
    (2, 7, 1, 3),
    (3, 5, 1, 6),
    (1, 3, 1, 4),
    (2, 9, 1, 3),
    (3, 7, 2, 7),
    (1, 5, 2, 7),
    (3, 8, 1, 5),
    (1, 4, 2, 9),
    (2, 11, 1, 4),
]

_CONTEXTS = [
    ("In a school canteen", "chose pizza", "chose chips", "chose curry"),
    ("In a survey of students", "chose football", "chose tennis", "chose another sport"),
    ("In a class", "walked to school", "cycled", "came by other transport"),
    ("In a year group", "chose art", "chose music", "chose drama"),
    ("In a school survey", "preferred science", "preferred maths", "preferred another subject"),
    ("In a leisure centre", "used the pool", "used the gym", "used other facilities"),
]


def generate_fractions():
    a, b, c, d = random.choice(_FRACTION_PARAMS)

    lcd = b * d // gcd(b, d)
    a_new = a * (lcd // b)
    c_new = c * (lcd // d)
    sum_num = a_new + c_new

    # Ensure sum < lcd (remainder is positive)
    if sum_num >= lcd:
        a, b, c, d = (2, 5, 1, 4)
        lcd = 20
        a_new, c_new, sum_num = 8, 5, 13

    raw_rest = lcd - sum_num
    common = gcd(raw_rest, lcd)
    rest_num = raw_rest // common
    rest_den = lcd // common
    answer = f"{rest_num}/{rest_den}"

    setting, opt1, opt2, opt3 = random.choice(_CONTEXTS)

    question_text = (
        f"{setting}, {a}/{b} of people {opt1} and {c}/{d} {opt2}. "
        f"The rest {opt3}. "
        f"What fraction {opt3}? Give your answer as a fraction in its simplest form."
    )

    scaffold_steps = [
        {"prompt": f"Find the LCD of {b} and {d}", "answer": lcd},
        {"prompt": f"Convert {a}/{b} to a fraction with denominator {lcd}", "answer": f"{a_new}/{lcd}"},
        {"prompt": f"Convert {c}/{d} to a fraction with denominator {lcd}", "answer": f"{c_new}/{lcd}"},
        {"prompt": "Add the two fractions", "answer": f"{sum_num}/{lcd}"},
        {"prompt": f"Remainder = 1 − {sum_num}/{lcd}", "answer": answer},
    ]

    simplify_note = f" = {answer}" if common > 1 else ""
    worked = [
        f"LCD of {b} and {d} = {lcd}",
        f"{a}/{b} = {a_new}/{lcd}",
        f"{c}/{d} = {c_new}/{lcd}",
        f"Total choosing {opt1} and {opt2} = {a_new}/{lcd} + {c_new}/{lcd} = {sum_num}/{lcd}",
        f"Fraction that {opt3} = 1 − {sum_num}/{lcd} = {lcd}/{lcd} − {sum_num}/{lcd} = {raw_rest}/{lcd}{simplify_note}",
        f"**Answer: {answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numbers and Money",
        question_type="Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
