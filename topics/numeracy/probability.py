import random
import math
from core.models.question_model import Question

NOTES = """
**Probability:**

**P(event)** = number of favourable outcomes ÷ total outcomes

- Probability is always between 0 (impossible) and 1 (certain)
- Give answers as **fractions in their simplest form**
- **Combined events (AND):** P(A and B) = P(A) × P(B) when events are independent
- For two-dice problems, count all possible totals systematically

**Example:** Landing on a prime from a spinner numbered 1–10:
- Primes: 2, 3, 5, 7 → 4 outcomes
- P(prime) = 4/10 = **2/5**
"""


def _frac(num, den):
    g = math.gcd(abs(num), abs(den))
    return f"{num // g}/{den // g}"


def _primes_up_to(n):
    return [x for x in range(2, n + 1) if all(x % i != 0 for i in range(2, x))]


def _squares_up_to(n):
    result, i = [], 1
    while i * i <= n:
        result.append(i * i)
        i += 1
    return result


def _two_dice_count(sides, threshold, direction):
    count = 0
    for i in range(1, sides + 1):
        for j in range(1, sides + 1):
            t = i + j
            if direction == ">" and t > threshold:
                count += 1
            elif direction == "<" and t < threshold:
                count += 1
    return count


def _digit_sum_count(max_ticket, threshold):
    return sum(1 for n in range(1, max_ticket + 1) if sum(int(d) for d in str(n)) >= threshold)


def _tombola_breakdown(threshold):
    lines = []
    singles = [n for n in range(1, 10) if n >= threshold]
    if singles:
        lines.append(f"Single digits: {{{', '.join(str(n) for n in singles)}}} → {len(singles)}")
    for tens in range(1, 10):
        group = [n for n in range(tens * 10, min(tens * 10 + 10, 101))
                 if sum(int(d) for d in str(n)) >= threshold]
        if group:
            if len(group) <= 5:
                s = ", ".join(str(n) for n in group)
            else:
                s = f"{group[0]}, {group[1]}, ..., {group[-1]}"
            lines.append(f"{tens}0s: {{{s}}} → {len(group)}")
    return lines


# ─────────────────────────────────────────────────────────────────
# Level 1 sub-generators
# ─────────────────────────────────────────────────────────────────

_CARD_SCENARIOS = [
    {
        "text": "picking a red Queen from a standard deck of 52 cards",
        "fav": 2, "total": 52,
        "solution": [
            "Red suits (hearts, diamonds) each have one Queen → 2 red Queens",
            "P(red Queen) = 2/52 = 1/26",
        ],
    },
    {
        "text": "picking a red card from a standard deck of 52 cards",
        "fav": 26, "total": 52,
        "solution": [
            "Hearts (13) + Diamonds (13) = 26 red cards",
            "P(red card) = 26/52 = 1/2",
        ],
    },
    {
        "text": "picking an Ace from a standard deck of 52 cards",
        "fav": 4, "total": 52,
        "solution": [
            "One Ace per suit × 4 suits = 4 Aces",
            "P(Ace) = 4/52 = 1/13",
        ],
    },
    {
        "text": "picking a diamond card from a standard deck of 52 cards",
        "fav": 13, "total": 52,
        "solution": [
            "The diamond suit has 13 cards",
            "P(diamond) = 13/52 = 1/4",
        ],
    },
    {
        "text": "picking a face card (Jack, Queen or King) from a standard deck of 52 cards",
        "fav": 12, "total": 52,
        "solution": [
            "Face cards: Jacks (4) + Queens (4) + Kings (4) = 12",
            "P(face card) = 12/52 = 3/13",
        ],
    },
    {
        "text": "picking the King of Hearts from a standard deck of 52 cards",
        "fav": 1, "total": 52,
        "solution": [
            "There is only 1 King of Hearts in a standard deck",
            "P(King of Hearts) = 1/52",
        ],
    },
]


def _cards_question():
    sc = random.choice(_CARD_SCENARIOS)
    fav, total = sc["fav"], sc["total"]
    answer = _frac(fav, total)
    scaffold = [
        {"prompt": "How many favourable outcomes are there?", "answer": fav},
        {"prompt": "How many total outcomes are there?", "answer": total},
        {"prompt": "Write the probability as a simplified fraction (e.g. 3/13)", "answer": answer},
    ]
    return Question(
        question_text=(
            f"Calculate the probability of {sc['text']}.\n\n"
            f"Give your answer as a fraction in its simplest form."
        ),
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=scaffold,
        worked_solution=sc["solution"],
        notes=NOTES,
    )


def _single_die_question():
    sides_options = [4, 6, 8, 10, 12]
    for _ in range(20):
        sides = random.choice(sides_options)
        direction = random.choice(["lower than", "higher than"])
        if direction == "lower than":
            threshold = random.randint(3, max(3, sides // 2 + 2))
            fav = threshold - 1
        else:
            threshold = random.randint(max(2, sides // 2), sides - 1)
            fav = sides - threshold
        if 0 < fav < sides:
            break

    total = sides
    answer = _frac(fav, total)
    outcomes = (list(range(1, threshold)) if direction == "lower than"
                else list(range(threshold + 1, sides + 1)))
    if len(outcomes) <= 6:
        out_str = "{" + ", ".join(str(x) for x in outcomes) + "}"
    else:
        out_str = f"{{{outcomes[0]}, {outcomes[1]}, ..., {outcomes[-1]}}}"

    scaffold = [
        {"prompt": f"List the outcomes {direction} {threshold} on a {sides}-sided die", "answer": fav},
        {"prompt": "How many total outcomes are there?", "answer": total},
        {"prompt": "Write the probability as a simplified fraction", "answer": answer},
    ]
    worked = [
        f"Outcomes {direction} {threshold}: {out_str} → {fav} outcome{'s' if fav != 1 else ''}",
        f"Total outcomes: {sides}",
        f"P(rolling {direction} {threshold}) = {fav}/{total} = {answer}",
    ]
    return Question(
        question_text=(
            f"Calculate the probability of rolling {direction} {threshold} "
            f"on a standard {sides}-sided die.\n\n"
            f"Give your answer as a fraction in its simplest form."
        ),
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=scaffold,
        worked_solution=worked,
        notes=NOTES,
    )


_SPINNER_RANGES = [10, 12, 15, 20]


def _spinner_question():
    if random.random() < 0.2:
        n = 37
        outcomes = _squares_up_to(n)
        cat_name = "square number"
        hint = "List square numbers (1²=1, 2²=4, 3²=9, ...) up to 37"
        prefix = f"A roulette wheel has {n} numbers (1–{n})."
    else:
        n = random.choice(_SPINNER_RANGES)
        primes = _primes_up_to(n)
        squares = _squares_up_to(n)
        mult3 = list(range(3, n + 1, 3))
        cats = [
            ("prime number", primes, "List prime numbers (divisible only by 1 and themselves)"),
            ("square number", squares, "List square numbers (1, 4, 9, 16, ...)"),
            ("odd number", list(range(1, n + 1, 2)), "Count odd numbers"),
            ("even number", list(range(2, n + 1, 2)), "Count even numbers"),
        ]
        if 1 < len(mult3) < n - 1:
            cats.append(("multiple of 3", mult3, "List multiples of 3"))
        cat_name, outcomes, hint = random.choice(cats)
        prefix = f"A spinner is numbered 1 to {n}."

    fav, total = len(outcomes), n
    answer = _frac(fav, total)
    if len(outcomes) <= 8:
        out_str = "{" + ", ".join(str(x) for x in outcomes) + "}"
    else:
        out_str = f"{{{outcomes[0]}, {outcomes[1]}, ..., {outcomes[-1]}}}"

    scaffold = [
        {"prompt": f"{hint} — how many are there?", "answer": fav},
        {"prompt": "How many sections are there in total?", "answer": total},
        {"prompt": "Write the probability as a simplified fraction", "answer": answer},
    ]
    worked = [
        f"{cat_name.capitalize()}s from 1 to {n}: {out_str} → {fav} outcome{'s' if fav != 1 else ''}",
        f"Total sections: {n}",
        f"P({cat_name}) = {fav}/{n} = {answer}",
    ]
    return Question(
        question_text=(
            f"{prefix} Calculate the probability of landing on a {cat_name}.\n\n"
            f"Give your answer as a fraction in its simplest form."
        ),
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=scaffold,
        worked_solution=worked,
        notes=NOTES,
    )


_DICE_CONFIGS = [
    (6, 7, ">"),   # 15/36 = 5/12
    (6, 6, ">"),   # 21/36 = 7/12
    (6, 8, ">"),   # 10/36 = 5/18
    (6, 5, ">"),   # 26/36 = 13/18
    (6, 6, "<"),   # 10/36 = 5/18
    (6, 7, "<"),   # 15/36 = 5/12
    (8, 9, ">"),   # 28/64 = 7/16
    (8, 8, ">"),   # 36/64 = 9/16
    (8, 9, "<"),   # 28/64 = 7/16
    (9, 10, "<"),  # 36/81 = 4/9
    (9, 9, ">"),   # 45/81 = 5/9
    (10, 10, ">"), # 55/100 = 11/20
    (10, 10, "<"), # 36/100 = 9/25
]


def _two_dice_question():
    sides, threshold, direction = random.choice(_DICE_CONFIGS)
    total = sides * sides
    fav = _two_dice_count(sides, threshold, direction)
    answer = _frac(fav, total)
    dir_word = "greater than" if direction == ">" else "less than"

    favorable = [
        (i, j) for i in range(1, sides + 1) for j in range(1, sides + 1)
        if (direction == ">" and i + j > threshold) or (direction == "<" and i + j < threshold)
    ]
    if len(favorable) <= 12:
        pairs_str = ", ".join(f"({a},{b})" for a, b in favorable)
    else:
        pairs_str = ", ".join(f"({a},{b})" for a, b in favorable[:10]) + ", ..."

    scaffold = [
        {"prompt": f"How many total outcomes are there for two {sides}-sided dice?", "answer": total},
        {"prompt": f"Count outcomes where the total is {dir_word} {threshold}", "answer": fav},
        {"prompt": "Write the probability as a simplified fraction", "answer": answer},
    ]
    worked = [
        f"Total outcomes = {sides} × {sides} = {total}",
        f"Outcomes where total is {dir_word} {threshold}: {{{pairs_str}}} → {fav}",
        f"P(total {dir_word} {threshold}) = {fav}/{total} = {answer}",
    ]
    return Question(
        question_text=(
            f"Two {sides}-sided dice are rolled. "
            f"Calculate the probability of landing on a total {dir_word} {threshold}.\n\n"
            f"Give your answer as a fraction in its simplest form."
        ),
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=scaffold,
        worked_solution=worked,
        notes=NOTES,
    )


_SPINNER_COMBOS = [
    {
        "desc": "an odd number and a vowel",
        "letter_set": ["A", "E"],
        "letter_desc": "vowels (A, E)",
        "number_set": [1, 3, 5],
        "number_desc": "odd numbers (1, 3, 5)",
    },
    {
        "desc": "an even number and a consonant",
        "letter_set": ["B", "C", "D"],
        "letter_desc": "consonants (B, C, D)",
        "number_set": [2, 4],
        "number_desc": "even numbers (2, 4)",
    },
    {
        "desc": "A or B and 4 or less",
        "letter_set": ["A", "B"],
        "letter_desc": "A or B",
        "number_set": [1, 2, 3, 4],
        "number_desc": "4 or less (1, 2, 3, 4)",
    },
    {
        "desc": "a consonant and an odd number",
        "letter_set": ["B", "C", "D"],
        "letter_desc": "consonants (B, C, D)",
        "number_set": [1, 3, 5],
        "number_desc": "odd numbers (1, 3, 5)",
    },
    {
        "desc": "a vowel and a number greater than 3",
        "letter_set": ["A", "E"],
        "letter_desc": "vowels (A, E)",
        "number_set": [4, 5],
        "number_desc": "greater than 3 (4, 5)",
    },
    {
        "desc": "C, D or E and an even number",
        "letter_set": ["C", "D", "E"],
        "letter_desc": "C, D or E",
        "number_set": [2, 4],
        "number_desc": "even numbers (2, 4)",
    },
]


def _two_spinners_question():
    c = random.choice(_SPINNER_COMBOS)
    fl = len(c["letter_set"])
    fn = len(c["number_set"])
    total = 25
    fav = fl * fn
    answer = _frac(fav, total)

    scaffold = [
        {"prompt": f"How many letters from A–E satisfy '{c['letter_desc']}'?", "answer": fl},
        {"prompt": f"How many numbers from 1–5 satisfy '{c['number_desc']}'?", "answer": fn},
        {"prompt": "How many total outcomes are there (5 × 5)?", "answer": total},
        {"prompt": "Calculate the probability as a simplified fraction", "answer": answer},
    ]
    worked = [
        f"Favourable letters ({c['letter_desc']}): {fl}",
        f"Favourable numbers ({c['number_desc']}): {fn}",
        f"Total outcomes = 5 × 5 = 25",
        f"Favourable outcomes = {fl} × {fn} = {fav}",
        f"P({c['desc']}) = {fav}/25 = {answer}",
    ]
    return Question(
        question_text=(
            f"Two 5-sided spinners are spun together.\n\n"
            f"- Spinner 1 is labelled **A, B, C, D, E** (one letter per section).\n"
            f"- Spinner 2 is labelled **1, 2, 3, 4, 5** (one number per section).\n\n"
            f"Calculate the probability of landing on **{c['desc']}**.\n\n"
            f"Give your answer as a fraction in its simplest form."
        ),
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=scaffold,
        worked_solution=worked,
        notes=NOTES,
    )


# ─────────────────────────────────────────────────────────────────
# Level 2 sub-generators (Apply questions)
# ─────────────────────────────────────────────────────────────────

_TOMBOLA_SCENARIOS = [
    {"tombola_threshold": 9,  "dice_threshold": 7},  # dice wins:    21/36 > 55/100
    {"tombola_threshold": 8,  "dice_threshold": 8},  # tombola wins: 64/100 > 15/36
    {"tombola_threshold": 9,  "dice_threshold": 8},  # tombola wins: 55/100 > 15/36
    {"tombola_threshold": 10, "dice_threshold": 7},  # dice wins:    21/36 > 45/100
    {"tombola_threshold": 8,  "dice_threshold": 7},  # tombola wins: 64/100 > 21/36
]


def _tombola_vs_dice_question():
    sc = random.choice(_TOMBOLA_SCENARIOS)
    t_thresh = sc["tombola_threshold"]
    d_thresh = sc["dice_threshold"]

    tombola_fav = _digit_sum_count(100, t_thresh)
    tombola_frac = _frac(tombola_fav, 100)
    tombola_prob = tombola_fav / 100

    # "total >= d_thresh" is the same as "total > d_thresh - 1"
    dice_fav = _two_dice_count(6, d_thresh - 1, ">")
    dice_frac = _frac(dice_fav, 36)
    dice_prob = dice_fav / 36

    winner = "tombola" if tombola_prob > dice_prob else "dice game"
    breakdown = _tombola_breakdown(t_thresh)

    scaffold = [
        {
            "prompt": (
                f"Count tickets 1–100 with digit sum ≥ {t_thresh} "
                f"(work by group: singles, 10s, 20s, ... 90s)"
            ),
            "answer": tombola_fav,
        },
        {"prompt": "Write the tombola probability as a simplified fraction", "answer": tombola_frac},
        {
            "prompt": f"Count two-dice outcomes (out of 36) with total ≥ {d_thresh}",
            "answer": dice_fav,
        },
        {"prompt": "Write the dice game probability as a simplified fraction", "answer": dice_frac},
        {
            "prompt": "Which game has the greater probability? Type tombola or dice game",
            "answer": winner,
        },
    ]
    worked = (
        [f"Tombola — tickets with digit sum ≥ {t_thresh}:"]
        + [f"  {line}" for line in breakdown]
        + [
            f"  Total: {tombola_fav} tickets",
            f"P(tombola win) = {tombola_fav}/100 = {tombola_frac} ≈ {tombola_prob:.3f}",
            f"Dice game — totals ≥ {d_thresh} out of 36: {dice_fav} outcomes",
            f"P(dice win) = {dice_fav}/36 = {dice_frac} ≈ {dice_prob:.3f}",
            f"Since {tombola_frac if winner == 'tombola' else dice_frac} > "
            f"{dice_frac if winner == 'tombola' else tombola_frac}, "
            f"the **{winner}** gives the greater chance of winning.",
        ]
    )
    return Question(
        question_text=(
            f"A prize tombola has 100 tickets numbered 1–100.\n"
            f"To win, the digit sum of your ticket number must total **{t_thresh} or more**.\n\n"
            f"There is also a dice game with two standard 6-sided dice.\n"
            f"To win you must roll a combined total of **{d_thresh} or more**.\n\n"
            f"Show your working to decide which game gives the greater chance of winning.\n\n"
            f"Type **tombola** or **dice game**."
        ),
        correct_answer=winner,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=scaffold,
        worked_solution=worked,
        notes=NOTES,
    )


_ALL_COLOURS = ["Blue", "White", "Green", "Yellow", "Red", "Black"]
_COLOUR_SPINNER_SCENARIOS = [
    # 2 colours (2/6), odd on 1–6 (3/6): P = 6/36 = 1/6
    {"colour_group": ["Green", "White"],  "cond_desc": "an odd number",        "cond_nums": [1, 3, 5]},
    # 2 colours (2/6), even on 1–6 (3/6): P = 6/36 = 1/6
    {"colour_group": ["Red", "Black"],    "cond_desc": "an even number",       "cond_nums": [2, 4, 6]},
    # 2 colours (2/6), >4 on 1–6 (2/6): P = 4/36 = 1/9
    {"colour_group": ["Blue", "Yellow"],  "cond_desc": "a number greater than 4", "cond_nums": [5, 6]},
    # 1 colour (1/6), prime on 1–6 (3/6): P = 3/36 = 1/12
    {"colour_group": ["Blue"],            "cond_desc": "a prime number",       "cond_nums": [2, 3, 5]},
    # 3 colours (3/6), prime on 1–6 (3/6): P = 9/36 = 1/4
    {"colour_group": ["Blue", "White", "Green"], "cond_desc": "a prime number", "cond_nums": [2, 3, 5]},
    # 2 colours (2/6), <3 on 1–6 (2/6): P = 4/36 = 1/9
    {"colour_group": ["Yellow", "Red"],   "cond_desc": "a number less than 3", "cond_nums": [1, 2]},
    # 3 colours (3/6), >4 on 1–6 (2/6): P = 6/36 = 1/6
    {"colour_group": ["Red", "Blue", "Black"], "cond_desc": "a number greater than 4", "cond_nums": [5, 6]},
    # 1 colour (1/6), <3 on 1–6 (2/6): P = 2/36 = 1/18
    {"colour_group": ["White"],           "cond_desc": "a number less than 3", "cond_nums": [1, 2]},
]


def _colour_spinner_question():
    sc = random.choice(_COLOUR_SPINNER_SCENARIOS)
    colour_group = sc["colour_group"]
    cond_desc = sc["cond_desc"]
    cond_nums = sc["cond_nums"]
    sides = 6
    numbers = list(range(1, sides + 1))

    fav_c = len(colour_group)
    fav_n = len(cond_nums)
    total = sides * sides
    fav = fav_c * fav_n
    answer = _frac(fav, total)

    colour_str = " or ".join(colour_group)
    nums_str = ", ".join(str(n) for n in cond_nums)

    scaffold = [
        {"prompt": f"How many sections on the colour spinner show {colour_str}?", "answer": fav_c},
        {"prompt": f"How many sections on the number spinner show {cond_desc}?", "answer": fav_n},
        {"prompt": f"How many total outcomes are there ({sides} × {sides})?", "answer": total},
        {"prompt": "Calculate the probability as a simplified fraction", "answer": answer},
    ]
    worked = [
        f"Colour spinner ({colour_str}): {fav_c} out of {sides} sections",
        f"Number spinner ({cond_desc}): {{{nums_str}}} → {fav_n} out of {sides} sections",
        f"Total outcomes = {sides} × {sides} = {total}",
        f"Favourable outcomes = {fav_c} × {fav_n} = {fav}",
        f"P({colour_str} and {cond_desc}) = {fav}/{total} = {answer}",
    ]
    return Question(
        question_text=(
            f"Two 6-sided spinners are spun together.\n\n"
            f"- **Colour spinner** has one section each of: {', '.join(_ALL_COLOURS)}.\n"
            f"- **Number spinner** has one section each of: {', '.join(str(n) for n in numbers)}.\n\n"
            f"Calculate the probability of landing on **{colour_str}** and **{cond_desc}**.\n\n"
            f"Give your answer as a fraction in its simplest form."
        ),
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=scaffold,
        worked_solution=worked,
        notes=NOTES,
    )


# ─────────────────────────────────────────────────────────────────
# Public dispatchers
# ─────────────────────────────────────────────────────────────────

def generate_probability_l1():
    return random.choice([
        _cards_question,
        _single_die_question,
        _spinner_question,
        _two_dice_question,
        _two_spinners_question,
    ])()


def generate_probability_l2():
    return random.choice([
        _tombola_vs_dice_question,
        _colour_spinner_question,
    ])()


def generate_probability_question():
    return random.choice([generate_probability_l1, generate_probability_l2])()
