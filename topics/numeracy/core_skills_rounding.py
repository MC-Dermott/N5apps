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

**Significant figures:** the first significant figure is the first non-zero digit. Count the
number of figures you need from there, then round using the next digit.

**Example:** Round 0·04762 to 2 significant figures.
- The first significant figure is the 4, the second is the 7. The next digit is 6, so round up.
- 0·04762 to 2 significant figures = **0·048**
"""

_WHOLE_LEVELS = {
    1: {"phrase": "the nearest 10", "lo": 15, "hi": 995},
    2: {"phrase": "the nearest 100", "lo": 105, "hi": 9950},
    3: {"phrase": "the nearest 1000", "lo": 1050, "hi": 99500},
}
_DP_LEVELS = {
    1: "1 decimal place",
    2: "2 decimal places",
    3: "3 decimal places",
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
    return _decimal_places(dp)


def _decimal_places(dp):
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


def generate_core_skills_rounding_l3(calc_mode=False):
    return _decimal_places(3)


# ---------------------------------------------------------------------------
# Level 4 — significant figures
# ---------------------------------------------------------------------------

def generate_core_skills_rounding_l4(calc_mode=False):
    sf = random.choice([1, 2, 3])
    while True:
        magnitude = random.choice([-2, -1, 0, 1, 2, 3, 4])
        digits = random.randint(10 ** (sf + 1), 10 ** (sf + 3) - 1)
        value = Decimal(digits).scaleb(magnitude - sf - 1)
        if -3 <= value.adjusted() - sf + 1 <= 3 and value != value.quantize(Decimal(1).scaleb(value.adjusted() - sf + 1), rounding=ROUND_HALF_UP):
            break
    place_e = value.adjusted() - sf + 1
    answer = value.quantize(Decimal(1).scaleb(place_e), rounding=ROUND_HALF_UP)
    value_f, answer_f = float(value), float(answer)
    value_s = format(value.normalize(), "f")
    answer_s = format(answer, "f") if place_e < 0 else str(int(answer))
    phrase = f"{sf} significant figure{'s' if sf > 1 else ''}"
    worked = [
        f"The first significant figure is the first non-zero digit. Count {sf} digit"
        f"{'s' if sf > 1 else ''} from there, then look at the next digit to decide whether to round up or down.",
        f"{value_s} rounded to {phrase} = **{answer_s}**",
    ]
    return Question(
        question_text=f"Round {value_s} to {phrase}.",
        correct_answer=answer_f,
        topic="Numeracy",
        question_type="Rounding",
        scaffold_steps=[{"prompt": "What is the rounded value?", "answer": answer_f}],
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(value_f, place_e),
    )


def generate_core_skills_rounding_question(calc_mode=False):
    return random.choice([
        generate_core_skills_rounding_l1,
        generate_core_skills_rounding_l2,
        generate_core_skills_rounding_l3,
        generate_core_skills_rounding_l4,
    ])(calc_mode=calc_mode)
