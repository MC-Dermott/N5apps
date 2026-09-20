import random
from decimal import Decimal, ROUND_HALF_UP
from core.models.question_model import Question

NOTES = """
**Rounding:**

1. Find the digit in the place you are rounding to.
2. Look at the **next digit** (one place further right): if it is 5 or more, round up;
   otherwise, leave it as is.
3. Replace every digit after that place with zero (for whole numbers), or remove it
   (for decimal places).

**Example:** Round 4368 to the nearest 100.
- The digit in the hundreds place is 3.
- The next digit is 6, so round up: 3 → 4.
- 4368 rounded to the nearest 100 = **4400**
"""

_WHOLE_LEVELS = {
    1: {"phrase": "the nearest 10", "lo": 15, "hi": 995},
    2: {"phrase": "the nearest 100", "lo": 105, "hi": 9950},
    3: {"phrase": "the nearest 1000", "lo": 1050, "hi": 99500},
}
_DP_LEVELS = {
    1: "1 decimal place",
    2: "2 decimal places",
}


def _round_whole(value, place_e):
    step = 10 ** place_e
    return int((Decimal(value) / step).quantize(Decimal("1"), rounding=ROUND_HALF_UP)) * step


def _round_decimal(value, dp):
    quant = Decimal("1").scaleb(-dp)
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))


def _diagram(value, place_e):
    return {"diagram": "rounding_number_line", "diagram_params": {"value": value, "place_e": place_e}}


# ---------------------------------------------------------------------------
# Level 1 — nearest 10 / 100 / 1000
# ---------------------------------------------------------------------------

def generate_core_skills_rounding_l1(calc_mode=False):
    place_e = random.choice([1, 2, 3])
    level = _WHOLE_LEVELS[place_e]
    step = 10 ** place_e
    while True:
        value = random.randint(level["lo"], level["hi"])
        if value % step != 0:
            break
    answer = _round_whole(value, place_e)

    question_text = f"Round {value} to {level['phrase']}."
    scaffold_steps = [{"prompt": "What is the rounded value?", "answer": answer}]
    worked = [
        f"Look at the digit just past {level['phrase']} to decide whether to round up or down.",
        f"{value} rounded to {level['phrase']} = **{answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Rounding",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(value, place_e),
    )


# ---------------------------------------------------------------------------
# Level 2 — 1 or 2 decimal places
# ---------------------------------------------------------------------------

def generate_core_skills_rounding_l2(calc_mode=False):
    dp = random.choice([1, 2])
    place_e = -dp
    whole = random.randint(1, 99)
    extra_dp = dp + random.randint(1, 2)
    frac = random.randint(1, 10 ** extra_dp - 1)
    value = round(whole + frac / (10 ** extra_dp), extra_dp)
    answer = _round_decimal(value, dp)
    phrase = _DP_LEVELS[dp]

    question_text = f"Round {value} to {phrase}."
    scaffold_steps = [{"prompt": "What is the rounded value?", "answer": answer}]
    worked = [
        f"Look at the digit just past {phrase} to decide whether to round up or down.",
        f"{value} rounded to {phrase} = **{answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Rounding",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(value, place_e),
    )


def generate_core_skills_rounding_question(calc_mode=False):
    return random.choice(
        [generate_core_skills_rounding_l1, generate_core_skills_rounding_l2]
    )(calc_mode=calc_mode)
