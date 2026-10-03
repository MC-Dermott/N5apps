import random
from core.models.question_model import Question
from core.models.distractors import distractors


def _hm_string(total_minutes):
    h, m = divmod(total_minutes, 60)
    h_word = f"{h} hour{'s' if h != 1 else ''}"
    m_word = f"{m} minute{'s' if m != 1 else ''}"
    if h == 0:
        return m_word
    if m == 0:
        return h_word
    return f"{h_word} {m_word}"


NOTES_MIN_TO_HOURS = """
**Minutes to Hours:**

Write the minutes as a fraction of 60, then divide to get a decimal.

**Decimal number of hours = minutes ÷ 60**

**Example:** Convert 45 minutes to hours.
- 45 minutes = 45/60 of an hour
- 45 ÷ 60 = **0.75 hours**

If the number of minutes is 60 or more, the answer is simply more than 1 hour — the method is
exactly the same.
"""

NOTES_HOURS_TO_MIN = """
**Hours to Hours and Minutes:**

Split the decimal into a whole number of hours and a decimal part, then multiply the decimal
part by 60 to find the minutes.

**Minutes = decimal part × 60**

**Example:** Convert 2.75 hours to hours and minutes.
- Whole hours = 2
- Decimal part = 0.75
- 0.75 × 60 = 45
- 2.75 hours = **2 hours 45 minutes**
"""

NOTES_INDIRECT_HM = """
**Indirect Proportion — Answers in Hours and Minutes:**

Use the value-for-1 method to find the answer as a decimal number of hours, then convert that
decimal into hours and minutes the same way as above.

**Value for 1 = (first quantity) × (first amount)**
**Answer (hours) = value for 1 ÷ (second quantity)**

**Example:** It takes 3 crofters 10 hours to repair a drystane dyke, working at the same rate.
How long would it take 4 crofters?
- Value for 1 crofter = 3 × 10 = 30
- 4 crofters = 30 ÷ 4 = 7.5 hours
- 0.5 × 60 = 30, so 7.5 hours = **7 hours 30 minutes**
"""


# ---------------------------------------------------------------------------
# Question type 1 — Minutes to Hours (write as a decimal)
# ---------------------------------------------------------------------------

_MIN_CONTEXTS = [
    "A phone call lasts", "A music lesson lasts", "A dance class lasts", "A ceilidh lasts",
    "A ferry crossing takes", "A bus journey takes", "A hill walk takes", "A dog walk takes",
    "A shinty match lasts", "A cookery class lasts",
]


def _misread_hours(hours):
    """The reported error of reading the digits after the point as minutes (2.8 h → '2 hours 8
    minutes'), as a duration string — None if those digits couldn't be minutes."""
    whole, _, frac = f"{round(hours, 2):.2f}".rstrip("0").rstrip(".").partition(".")
    if not frac or int(frac) > 59:
        return None
    return _hm_string(int(whole) * 60 + int(frac))


_MISREAD = ("you read the decimal part as minutes — multiply it by 60 (2026 course report: 2.8 hours "
            "is 2 hours 48 minutes).")
_AS_DECIMAL = ("you wrote the minutes after the decimal point — divide the minutes by 60 (2025 marking "
               "instructions: 33 minutes is 0.55 hours, not 0.33).")

NOTES_COMMON_TC = """
⚠ **Common errors:** writing the minutes after the decimal point (33 minutes is **not** 0.33
hours; 1 hour 45 minutes is **not** 1.45 hours) and reading the decimal part as minutes (2.8 hours
is 2 hours **48** minutes) — 2022, 2025 and 2026 course reports and marking instructions.
"""


def _minutes_multiple_of_three(lo, hi):
    choices = [n for n in range(lo, hi + 1) if n % 3 == 0]
    return random.choice(choices)


def generate_minutes_to_hours_l1(calc_mode=False):
    """Under 60 minutes."""
    minutes = _minutes_multiple_of_three(3, 57)
    context = random.choice(_MIN_CONTEXTS)
    decimal = minutes / 60

    question_text = f"{context} {minutes} minutes.\n\nWrite this as a decimal number of hours."

    scaffold_steps = [
        {"prompt": "Write the minutes as a fraction of 60", "answer": f"{minutes}/60"},
        {"prompt": "Divide to find the decimal number of hours", "answer": decimal},
    ]
    worked = [
        f"{minutes} minutes = {minutes}/60 of an hour",
        f"{minutes} ÷ 60 = {decimal}",
        f"**{minutes} minutes = {decimal} hours.**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=decimal,
        topic="Numeracy",
        question_type="Minutes to Hours",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_MIN_TO_HOURS + NOTES_COMMON_TC,
        distractors=distractors(decimal, [(minutes / 100, _AS_DECIMAL)]),
    )


def generate_minutes_to_hours_l2(calc_mode=False):
    """60 minutes or more."""
    hi = 240 if calc_mode else 300
    minutes = _minutes_multiple_of_three(63, hi)
    context = random.choice(_MIN_CONTEXTS)
    decimal = minutes / 60

    question_text = f"{context} {minutes} minutes.\n\nWrite this as a decimal number of hours."

    scaffold_steps = [
        {"prompt": "Write the minutes as a fraction of 60", "answer": f"{minutes}/60"},
        {"prompt": "Divide to find the decimal number of hours", "answer": decimal},
    ]
    worked = [
        f"{minutes} minutes = {minutes}/60 of an hour",
        f"{minutes} ÷ 60 = {decimal}",
        f"**{minutes} minutes = {decimal} hours.**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=decimal,
        topic="Numeracy",
        question_type="Minutes to Hours",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_MIN_TO_HOURS + NOTES_COMMON_TC,
        distractors=distractors(decimal, [
            (minutes // 60 + (minutes % 60) / 100, _AS_DECIMAL) if minutes % 60 else (None, ""),
            (minutes / 100, "divide by 60, not 100 — there are 60 minutes in an hour."),
        ]),
    )


def generate_minutes_to_hours_question(calc_mode=False):
    return random.choice([
        generate_minutes_to_hours_l1,
        generate_minutes_to_hours_l2,
    ])(calc_mode=calc_mode)


# ---------------------------------------------------------------------------
# Question type 2 — Hours to Hours and Minutes (decimal × 60)
# ---------------------------------------------------------------------------

_HOUR_CONTEXTS = [
    "A recipe takes", "A dog walk takes", "Cutting the peat takes", "A bus journey takes",
    "Knitting a jumper sleeve takes", "A hill walk takes", "A ferry crossing takes",
    "A driving lesson takes", "A tour of the broch takes", "Repairing the fence takes",
]

_CLEAN_DECIMAL_PARTS = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
                         0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]


def generate_hours_to_minutes_l1(calc_mode=False):
    """Under 1 hour."""
    part = random.choice(_CLEAN_DECIMAL_PARTS)
    context = random.choice(_HOUR_CONTEXTS)
    minutes = round(part * 60)
    answer = _hm_string(minutes)

    question_text = f"{context} {part} hours.\n\nWrite this as minutes."

    scaffold_steps = [
        {"prompt": "Multiply the decimal by 60 to find the minutes", "answer": minutes},
    ]
    worked = [
        f"{part} × 60 = {minutes}",
        f"**{part} hours = {minutes} minutes.**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Hours to Hours and Minutes",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_HOURS_TO_MIN + NOTES_COMMON_TC,
        metadata={"answer_type": "duration"},
        distractors=distractors(answer, [(_misread_hours(part), _MISREAD)]),
    )


def generate_hours_to_minutes_l2(calc_mode=False):
    """1 hour or more."""
    whole = random.randint(1, 6 if calc_mode else 9)
    part = random.choice(_CLEAN_DECIMAL_PARTS)
    context = random.choice(_HOUR_CONTEXTS)
    decimal_hours = round(whole + part, 2)
    minutes = round(part * 60)
    answer = _hm_string(whole * 60 + minutes)

    question_text = f"{context} {decimal_hours} hours.\n\nWrite this as hours and minutes."

    scaffold_steps = [
        {"prompt": "Write down the whole number of hours", "answer": whole},
        {"prompt": "Multiply the decimal part by 60 to find the minutes", "answer": minutes},
    ]
    worked = [
        f"Whole hours = {whole}",
        f"Decimal part = {round(decimal_hours - whole, 2)}",
        f"{round(decimal_hours - whole, 2)} × 60 = {minutes}",
        f"**{decimal_hours} hours = {answer}.**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Hours to Hours and Minutes",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_HOURS_TO_MIN + NOTES_COMMON_TC,
        metadata={"answer_type": "duration"},
        distractors=distractors(answer, [(_misread_hours(decimal_hours), _MISREAD)]),
    )


def generate_hours_to_minutes_question(calc_mode=False):
    return random.choice([
        generate_hours_to_minutes_l1,
        generate_hours_to_minutes_l2,
    ])(calc_mode=calc_mode)


# ---------------------------------------------------------------------------
# Question type 3 — Indirect Proportion: Answers in Hours and Minutes
# ---------------------------------------------------------------------------

_WORKRATE_CONTEXTS = [
    {"plural": "weavers", "singular": "weaver", "task": "finish a length of Harris Tweed"},
    {"plural": "shearers", "singular": "shearer", "task": "clear a fold of sheep"},
    {"plural": "joiners", "singular": "joiner", "task": "build a bothy porch"},
    {"plural": "fishermen", "singular": "fisherman", "task": "haul in the catch"},
    {"plural": "thatchers", "singular": "thatcher", "task": "thatch a blackhouse roof"},
    {"plural": "gardeners", "singular": "gardener", "task": "dig over the community allotment"},
]

_SPEED_CONTEXTS = [
    {"journey": "the ferry crossing to the mainland", "unit": "knots"},
    {"journey": "the puffin-watching boat trip to the Shiants", "unit": "knots"},
    {"journey": "the tour bus journey to Stornoway", "unit": "mph"},
    {"journey": "the minibus journey along the coast road", "unit": "mph"},
]


def _find_inverse_hm(hi, time_hi):
    """Finds q1, q2, a1, result_minutes such that q1 units take a1 hours, and q2 units take
    an exact whole number of minutes (result_minutes), with a genuine hours+minutes remainder
    (not a whole number of hours)."""
    candidates = list(range(2, hi + 1))
    for _ in range(300):
        q1 = random.choice(candidates)
        q2 = random.choice([q for q in candidates if q != q1])
        a1 = random.randint(2, time_hi)
        total_minutes = q1 * a1 * 60
        if total_minutes % q2 == 0:
            result_minutes = total_minutes // q2
            if result_minutes % 60 != 0:
                return q1, q2, a1, result_minutes
    return None


def _hm_distractors(answer, hours, direct_hours):
    direct_mins = direct_hours * 60
    return distractors(answer, [
        (_misread_hours(hours), _MISREAD),
        (_hm_string(round(hours) * 60), "don't round — change the decimal part of the hours into minutes "
                                        "(2025 marking instructions)."),
        (_hm_string(round(direct_mins)) if abs(direct_mins - round(direct_mins)) < 1e-9 else None,
         "that's direct proportion — the time should go the other way (2023, 2024 and 2026 course "
         "reports)."),
    ])


def generate_indirect_proportion_hm_l1(calc_mode=False):
    """People/work-rate contexts."""
    ctx = random.choice(_WORKRATE_CONTEXTS)
    hi = 8 if calc_mode else 12
    time_hi = 10 if calc_mode else 16
    triple = _find_inverse_hm(hi, time_hi)
    q1, q2, a1, result_minutes = triple if triple else (6, 5, 8, 576)
    value_of_one = q1 * a1
    answer = _hm_string(result_minutes)

    question_text = (
        f"{q1} {ctx['plural']} can {ctx['task']} in {a1} hours, working at the same rate.\n\n"
        f"How long would it take {q2} {ctx['plural']}? Give your answer in hours and minutes."
    )

    scaffold_steps = [
        {"prompt": f"Find the value for 1 {ctx['singular']} (multiply)", "answer": value_of_one},
        {"prompt": f"Divide by {q2} to find the decimal number of hours",
         "answer": round(value_of_one / q2, 4)},
        {"prompt": "Convert the decimal hours into hours and minutes",
         "answer": answer, "answer_type": "duration"},
    ]
    worked = [
        f"1 {ctx['singular']} = {q1} × {a1} = {value_of_one} hours",
        f"{q2} {ctx['plural']} = {value_of_one} ÷ {q2} = {round(value_of_one / q2, 4)} hours",
        f"**{q2} {ctx['plural']} would take {answer}.**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Indirect Proportion (Hours and Minutes)",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_INDIRECT_HM + NOTES_COMMON_TC,
        metadata={"answer_type": "duration"},
        distractors=_hm_distractors(answer, value_of_one / q2, a1 * q2 / q1),
    )


def generate_indirect_proportion_hm_l2(calc_mode=False):
    """Speed/distance/time contexts."""
    ctx = random.choice(_SPEED_CONTEXTS)
    hi = 9 if calc_mode else 14
    time_hi = 8 if calc_mode else 10
    triple = _find_inverse_hm(hi, time_hi)
    speed1, speed2, time1, result_minutes = triple if triple else (9, 8, 4, 270)
    distance = speed1 * time1
    answer = _hm_string(result_minutes)

    question_text = (
        f"At a speed of {speed1} {ctx['unit']}, {ctx['journey']} takes {time1} hours.\n\n"
        f"How long would {ctx['journey']} take at a speed of {speed2} {ctx['unit']}? "
        f"Give your answer in hours and minutes."
    )

    scaffold_steps = [
        {"prompt": "Find the distance (multiply speed × time)", "answer": distance},
        {"prompt": f"Divide by {speed2} to find the decimal number of hours",
         "answer": round(distance / speed2, 4)},
        {"prompt": "Convert the decimal hours into hours and minutes",
         "answer": answer, "answer_type": "duration"},
    ]
    worked = [
        f"Distance = {speed1} × {time1} = {distance}",
        f"Time = {distance} ÷ {speed2} = {round(distance / speed2, 4)} hours",
        f"**At {speed2} {ctx['unit']}, the journey would take {answer}.**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Indirect Proportion (Hours and Minutes)",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_INDIRECT_HM + NOTES_COMMON_TC,
        metadata={"answer_type": "duration"},
        distractors=_hm_distractors(answer, distance / speed2, time1 * speed2 / speed1),
    )


def generate_indirect_proportion_hm_question(calc_mode=False):
    return random.choice([
        generate_indirect_proportion_hm_l1,
        generate_indirect_proportion_hm_l2,
    ])(calc_mode=calc_mode)
