import random
from core.models.question_model import Question

NOTES = """
**Bus-Stop (Long) Division:**

1. Divide the divisor into the first digit(s) of the number, working left to right.
2. Write the whole number of times it divides in above the line, and carry the
   **remainder** down to join the next digit.
3. Keep going, digit by digit — if you reach the end of the whole number and there's
   still a remainder, add a decimal point and bring down a 0 to keep dividing.

**Example:** Calculate 583 ÷ 7.
- 5 ÷ 7 = 0 remainder 5 → carry the 5 to make 58
- 58 ÷ 7 = 8 remainder 2 → carry the 2 to make 23
- 23 ÷ 7 = 3 remainder 2 → carry the 2 to make 20 (bring down a 0, add the decimal point)
- 20 ÷ 7 = 2 remainder 6 → carry the 6 to make 60
- 583 ÷ 7 = **83.2...** (continue for more decimal places if needed)
"""

NOTES_RECURRING = NOTES + """
**Recurring Decimals:**

If a remainder repeats one you've already seen, the decimal digits will repeat forever
too — that's a **recurring decimal**. Round to the number of decimal places asked for.

**Example:** 10 ÷ 3 = 3.333... — the 3s repeat forever, so to 2 decimal places that's **3.33**.
"""

_DIVISOR_POOL = [3, 4, 6, 7, 8, 9, 11, 12]


def _compute_division(dividend, divisor, max_decimals=10):
    """Bus-stop division, column by column — mirrors the interactive widget's own
    engine so the scaffold's step-by-step working matches what pupils see there."""
    running = 0
    for digit in str(dividend):
        combined = running * 10 + int(digit)
        running = combined % divisor

    decimals = []
    seen = {}
    terminates = False
    repeat_start = None
    for i in range(max_decimals):
        if running == 0:
            terminates = True
            break
        if running in seen:
            repeat_start = seen[running]
            break
        seen[running] = i
        combined = running * 10
        q, rem = divmod(combined, divisor)
        decimals.append(q)
        running = rem

    return {
        "whole_value": dividend // divisor,
        "decimals": decimals,
        "terminates": terminates,
        "repeat_start": repeat_start,
    }


def _generate(digit_count, want_type, max_decimals=10):
    lo, hi = (10, 99) if digit_count == 2 else (100, 999)
    for _ in range(4000):
        divisor = random.choice(_DIVISOR_POOL)
        dividend = random.randint(lo, hi)
        if dividend <= divisor:
            continue
        exact = dividend % divisor == 0
        if want_type == "exact" and not exact:
            continue
        if want_type != "exact" and exact:
            continue

        res = _compute_division(dividend, divisor, max_decimals)
        if want_type == "exact" and res["terminates"] and not res["decimals"]:
            return dividend, divisor, res
        if want_type == "terminating" and res["terminates"] and 1 <= len(res["decimals"]) <= 2:
            return dividend, divisor, res
        if want_type == "recurring" and not res["terminates"] and res["repeat_start"] is not None:
            return dividend, divisor, res
    raise RuntimeError(f"could not generate a {digit_count}-digit '{want_type}' division question")


def _diagram(dividend, divisor):
    return {"diagram": "bus_stop_division", "diagram_params": {"dividend": dividend, "divisor": divisor}}


# ---------------------------------------------------------------------------
# Level 1 — divides exactly, whole number answer
# ---------------------------------------------------------------------------

def generate_division_l1(calc_mode=False):
    digit_count = random.choice([2, 3])
    dividend, divisor, res = _generate(digit_count, "exact")
    answer = res["whole_value"]

    question_text = f"Calculate {dividend} ÷ {divisor}."

    scaffold_steps = [
        {"prompt": "What is the answer?", "answer": answer},
    ]

    worked = [
        f"Divide {divisor} into {dividend} using bus-stop division, column by column.",
        f"{dividend} ÷ {divisor} = **{answer}** exactly (remainder 0).",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Division",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(dividend, divisor),
    )


# ---------------------------------------------------------------------------
# Level 2 — terminates after 1-2 decimal places
# ---------------------------------------------------------------------------

def generate_division_l2(calc_mode=False):
    digit_count = random.choice([2, 3])
    dividend, divisor, res = _generate(digit_count, "terminating")
    answer = round(dividend / divisor, 2)

    question_text = f"Calculate {dividend} ÷ {divisor}. Give your answer correct to 2 decimal places."

    scaffold_steps = [
        {"prompt": "What is the whole number part of the answer (before the decimal point)?",
         "answer": res["whole_value"]},
        {"prompt": "What is the full answer, correct to 2 decimal places?", "answer": answer},
    ]

    decimals_str = "".join(str(d) for d in res["decimals"])
    worked = [
        f"Divide {divisor} into {dividend} using bus-stop division, continuing into the decimal places.",
        f"Whole number part: {dividend} ÷ {divisor} = {res['whole_value']} remainder, then carry on past the decimal point.",
        f"{dividend} ÷ {divisor} = {res['whole_value']}.{decimals_str} = **{answer}** (to 2 d.p.)",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Division",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(dividend, divisor),
    )


# ---------------------------------------------------------------------------
# Level 3 — recurring decimal, rounded to 2 decimal places
# ---------------------------------------------------------------------------

def generate_division_l3(calc_mode=False):
    digit_count = random.choice([2, 3])
    dividend, divisor, res = _generate(digit_count, "recurring")
    answer = round(dividend / divisor, 2)

    question_text = f"Calculate {dividend} ÷ {divisor}. Give your answer correct to 2 decimal places."

    scaffold_steps = [
        {"prompt": "What is the whole number part of the answer (before the decimal point)?",
         "answer": res["whole_value"]},
        {"prompt": "What is the full answer, correct to 2 decimal places?", "answer": answer},
    ]

    repeat_start = res["repeat_start"]
    non_repeating = "".join(str(d) for d in res["decimals"][:repeat_start])
    repeating = "".join(str(d) for d in res["decimals"][repeat_start:])
    worked = [
        f"Divide {divisor} into {dividend} using bus-stop division, continuing into the decimal places.",
        f"The remainder starts repeating, so the digits {repeating} recur forever: "
        f"{dividend} ÷ {divisor} = {res['whole_value']}.{non_repeating}{repeating}... (recurring)",
        f"Rounded to 2 decimal places: **{answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Division",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_RECURRING,
        metadata=_diagram(dividend, divisor),
    )


def generate_division_question(calc_mode=False):
    return random.choice([generate_division_l1, generate_division_l2, generate_division_l3])(calc_mode=calc_mode)
