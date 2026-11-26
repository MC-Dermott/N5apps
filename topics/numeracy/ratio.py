import math
import random
from core.models.question_model import Question
from core.models.distractors import distractors

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

NOTES_L3 = """
**Using the Difference Between Two Parts of a Ratio:**

When you are told how many **more** of one thing there are than another, that number matches
the **difference** between their ratio numbers — not one part, and not the total.

1. Subtract the ratio numbers to find the difference in shares.
2. Divide the difference you are given by this to find the value of **one share**.
3. Multiply the value of one share by the number of shares you need.

**Example:** Sheep and cows are in the ratio 5:3. There are 48 more sheep than cows.
- Difference in shares = 5 − 3 = 2
- One share = 48 ÷ 2 = 24
- Total animals = (5 + 3) × 24 = 8 × 24 = 192
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

NOTES += """
⚠ **Common error:** dividing the total by just one number in the ratio instead of the total
number of shares. Check: the shares must add back up to the total.
"""
NOTES_L2 += """
⚠ **Common error:** dividing the amount you're given by the **total** number of shares. The amount
you're given is only that category's shares — divide by its own ratio number. This was the most
common mistake in 2018, 2019 and 2026 (marking instructions).
"""
NOTES_L3 += """
⚠ **Common error:** dividing the difference by one of the ratio numbers. The difference is
(larger − smaller) shares — most candidates got no marks for this in 2025 (course report).
"""

_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


_CALC_SAFE_RATIOS = [(1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 2, 6), (1, 3, 4), (1, 3, 5), (2, 3, 4)]


def _random_ratio(calc_mode=False):
    if calc_mode:
        # Sum of parts must itself be single-digit (it's the divisor for "one share"
        # and a multiplier for "total") — only sums ≤ 9 qualify.
        return random.choice(_CALC_SAFE_RATIOS)
    parts = random.sample(range(1, 10), 3)
    return tuple(parts)


# ---------------------------------------------------------------------------
# Level 1 — split an amount into unequal quantities
# ---------------------------------------------------------------------------

def generate_ratio_l1(calc_mode=False):
    ctx = random.choice(_CONTEXTS)
    month = random.choice(_MONTHS)
    parts = _random_ratio(calc_mode)
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
        distractors=distractors(ask_amount, [
            (round(total / parts[ask_idx], 2), f"you divided the total by {parts[ask_idx]} — divide by the "
                                               f"total number of shares ({total_shares}) first."),
            (share_value, f"that's one share — multiply it by {parts[ask_idx]} for the {ask_category} "
                          f"{ctx['item_plural']}."),
        ]),
    )


# ---------------------------------------------------------------------------
# Level 2 — calculate a total when given one of the ratio amounts
# ---------------------------------------------------------------------------

def generate_ratio_l2(calc_mode=False):
    ctx = random.choice(_CONTEXTS)
    month = random.choice(_MONTHS)
    parts = _random_ratio(calc_mode)
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
        distractors=distractors(total, [
            (round(given_amount + given_amount / total_shares * (total_shares - parts[given_idx]), 2),
             f"you divided {given_amount:,} by the total number of shares — {given_amount:,} is the "
             f"{given_category} {ctx['item_plural']}' {parts[given_idx]} shares, so divide by "
             f"{parts[given_idx]} (2018, 2019 and 2026 marking instructions)."),
            (round(given_amount / total_shares, 2),
             f"you divided by the total number of shares — divide {given_amount:,} by "
             f"{parts[given_idx]}, its own ratio number."),
        ] + [
            (round(given_amount / parts[j] * total_shares, 2),
             f"you divided by the wrong ratio number — the {given_category} {ctx['item_plural']} "
             f"are {parts[given_idx]} shares (2023 marking instructions).")
            for j in range(3) if parts[j] != parts[given_idx]
        ][:1]),
    )


# ---------------------------------------------------------------------------
# Level 3 — use the difference between two parts (2025 Paper 1 Q9 style)
# ---------------------------------------------------------------------------

# (larger, smaller) pairs in their simplest form. Non-calculator pairs keep both the difference
# and the total number of shares small enough to divide and multiply by in your head.
_DIFF_RATIOS = [(3, 1), (3, 2), (4, 1), (4, 3), (5, 1), (5, 2), (5, 3), (5, 4), (7, 2), (7, 3),
                (7, 4), (7, 5), (8, 3), (8, 5), (9, 2), (9, 4), (9, 5), (9, 7)]
_CALC_SAFE_DIFF_RATIOS = [(3, 1), (3, 2), (4, 1), (4, 3), (5, 2), (5, 3), (7, 3), (7, 4), (7, 5)]


def generate_ratio_l3(calc_mode=False):
    ctx = random.choice(_CONTEXTS)
    month = random.choice(_MONTHS)
    big, small = random.choice(_CALC_SAFE_DIFF_RATIOS if calc_mode else _DIFF_RATIOS)
    share_value = random.choice(range(4, 21, 2) if calc_mode else range(4, 41, 2))
    diff_shares = big - small
    difference = diff_shares * share_value
    cat_big, cat_small = random.sample(ctx["categories"], 2)
    items = ctx["item_plural"]

    ask = random.choice(["total", "total", "big", "small"])
    if ask == "total":
        target_shares, target_label = big + small, f"{cat_big} and {cat_small} {items} altogether"
        target_working = f"Total = ({big} + {small}) × {share_value} = {big + small} × {share_value}"
        ask_text = f"Calculate the **total** number of {cat_big} and {cat_small} {items} {ctx['verb']} in {month}."
    else:
        cat = cat_big if ask == "big" else cat_small
        target_shares = big if ask == "big" else small
        target_label = f"{cat} {items}"
        target_working = f"{cat.capitalize()} = {target_shares} × {share_value}"
        ask_text = f"Calculate the number of **{cat}** {items} {ctx['verb']} in {month}."
    answer = target_shares * share_value

    question_text = (
        f"In {month} {ctx['subject']} {ctx['verb']} {cat_big} and {cat_small} {items} "
        f"in the ratio {big}:{small}.\n\n"
        f"{ctx['subject']} {ctx['verb']} {difference:,} more {cat_big} {items} than {cat_small} {items}.\n\n"
        f"{ask_text}"
    )

    scaffold_steps = [
        {"prompt": "Difference in ratio shares (larger ratio number − smaller ratio number)", "answer": diff_shares},
        {"prompt": "Value of one share (difference given ÷ difference in shares)", "answer": share_value},
        {"prompt": f"Number of {target_label} (shares needed × value of one share)", "answer": answer},
    ]

    worked = [
        f"Difference in shares = {big} − {small} = {diff_shares}",
        f"One share = {difference:,} ÷ {diff_shares} = {share_value}",
        f"{target_working} = {answer:,}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Ratio",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L3,
        distractors=distractors(answer, [
            (round(difference / small * target_shares, 2),
             f"you divided the difference by {small} — the difference is {big} − {small} = "
             f"{diff_shares} shares (2025 course report)."),
            (round(difference / big * target_shares, 2),
             f"you divided the difference by {big} — the difference is {big} − {small} = "
             f"{diff_shares} shares (2025 course report)."),
            (round(difference / (big + small) * target_shares, 2),
             f"you divided the difference by the total shares — the difference is {diff_shares} shares."),
        ]),
    )


# ---------------------------------------------------------------------------
# Writing and simplifying a ratio
# ---------------------------------------------------------------------------

NOTES_SIMPLIFY = """
**Writing and Simplifying a Ratio:**

1. Write the quantities **in the order the question names them**, in the **same units**.
2. Divide every number by the highest common factor.

**Example:** A mix uses 2 litres of juice and 500 ml of water. Write juice : water in its simplest form.
- 2000 : 500
- = **4 : 1** (dividing both by 500)
"""

_PAIRS_SIMPLIFY = [("adults", "children", "At a swimming pool there are {a} adults and {b} children."),
                   ("red", "blue", "A bag holds {a} red counters and {b} blue counters."),
                   ("wins", "losses", "A netball team had {a} wins and {b} losses."),
                   ("cars", "vans", "A car park holds {a} cars and {b} vans.")]


def generate_ratio_simplify(calc_mode=False):
    first, second, sentence = random.choice(_PAIRS_SIMPLIFY)
    while True:
        p, q = random.randint(1, 9), random.randint(1, 9)
        if p != q and math.gcd(p, q) == 1:
            break
    k = random.choice([3, 4, 5, 6, 8, 12])
    a, b = p * k, q * k
    swap = random.random() < 0.5
    x, y = (b, a) if swap else (a, b)
    n1, n2 = (second, first) if swap else (first, second)
    rp, rq = (q, p) if swap else (p, q)
    right = f"{rp} : {rq}"
    wrong = [(f"{rq} : {rp}", f"the order matters — the question asks for {n1} first."),
             (f"{rp} : {rp + rq}", f"that compares {n1} with the total, not with {n2}."),
             (f"{x} : {y}", "that isn't in its simplest form.")]
    opts = list(dict.fromkeys([right] + [v for v, _ in wrong]))
    random.shuffle(opts)
    return Question(
        question_text=sentence.format(a=a, b=b) + f"\n\nWrite the ratio of **{n1} to {n2}** in its simplest form.",
        correct_answer=right,
        topic="Numeracy",
        question_type="Ratio",
        scaffold_steps=[{"prompt": "Highest common factor of the two numbers", "answer": k}],
        worked_solution=[f"{n1} : {n2} = {x} : {y}", f"= {right} (dividing both by {k})"],
        notes=NOTES_SIMPLIFY,
        metadata={"options": opts},
        distractors=[{"value": v, "mistake": m} for v, m in wrong if v != right],
    )


# ---------------------------------------------------------------------------
# Scale drawings
# ---------------------------------------------------------------------------

NOTES_SCALE = """
**Scale Drawings:** a scale of 1 : 50 means 1 cm on the drawing is 50 cm in real life.

- Drawing → real: **multiply** by the scale, then change units.
- Real → drawing: change to cm, then **divide** by the scale.

**Example:** On a plan with scale 1 : 50, a wall is 8.4 cm long.
- 8.4 × 50 = 420 cm = **4.2 m**
"""

_SCALE_THINGS = ["a wall", "a classroom", "a garden", "a stage", "a car park", "a kitchen"]


def generate_ratio_scale(calc_mode=False):
    thing = random.choice(_SCALE_THINGS)
    scale = random.choice([20, 50, 100, 200])
    drawing = random.choice([x / 2 for x in range(5, 31)]) if calc_mode else round(random.randint(25, 180) / 10, 1)
    real_cm = round(drawing * scale, 1)
    real_m = round(real_cm / 100, 3)
    if random.random() < 0.5:
        text = (f"A plan is drawn with a scale of **1 : {scale}**.\n\nOn the plan, {thing} is {drawing:g} cm long.\n\n"
                f"Calculate its real length in **metres**.")
        answer = real_m
        steps = [{"prompt": "Real length in cm (drawing length × scale)", "answer": real_cm},
                 {"prompt": "Real length in metres", "answer": real_m}]
        worked = [f"{drawing:g} × {scale} = {real_cm:g} cm", f"{real_cm:g} ÷ 100 = {real_m:g} m"]
        wrong = [(real_cm, "that's in centimetres — change to metres."),
                 (round(drawing / scale, 4), "drawing → real means multiply by the scale.")]
    else:
        text = (f"A plan is drawn with a scale of **1 : {scale}**.\n\nIn real life, {thing} is {real_m:g} m long.\n\n"
                f"Calculate its length on the plan in **centimetres**.")
        answer = drawing
        steps = [{"prompt": "Real length in cm", "answer": real_cm},
                 {"prompt": "Length on the plan (real length in cm ÷ scale)", "answer": drawing}]
        worked = [f"{real_m:g} m = {real_cm:g} cm", f"{real_cm:g} ÷ {scale} = {drawing:g} cm"]
        wrong = [(round(real_m / scale, 4), "change the real length to centimetres first."),
                 (round(real_m * scale, 3), "real → drawing means divide by the scale.")]
    return Question(question_text=text, correct_answer=answer, topic="Numeracy", question_type="Ratio",
                    scaffold_steps=steps, worked_solution=worked, notes=NOTES_SCALE,
                    distractors=distractors(answer, wrong))


# ---------------------------------------------------------------------------
# Default dispatcher
# ---------------------------------------------------------------------------

def generate_ratio_question(calc_mode=False):
    return random.choice([generate_ratio_simplify, generate_ratio_l1, generate_ratio_l2, generate_ratio_l3,
                          generate_ratio_scale])(calc_mode=calc_mode)
