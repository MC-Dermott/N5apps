import math
import random
from core.models.question_model import Question
from topics.numeracy.fractions import SIMPLIFY_NOTES, _SIMPLIFY_BASE_PAIRS


def _diagram(numerator, denominator):
    return {
        "diagram": "fraction_simplifier",
        "diagram_params": {"numerator": numerator, "denominator": denominator},
    }


def _build(reduced_n, reduced_d, factor):
    n, d = reduced_n * factor, reduced_d * factor
    hcf = math.gcd(n, d)
    answer_str = f"{reduced_n}/{reduced_d}"

    question_text = f"Simplify {n}/{d} to its simplest form."
    scaffold_steps = [
        {"prompt": "Find the highest common factor of the numerator and denominator", "answer": float(hcf)},
        {"prompt": "Divide both the numerator and denominator by the highest common factor", "answer": answer_str},
    ]
    worked = [
        f"HCF of {n} and {d} = {hcf}",
        f"{n} ÷ {hcf} = {reduced_n}, {d} ÷ {hcf} = {reduced_d}",
        f"{n}/{d} = **{answer_str}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer_str,
        topic="Numeracy",
        question_type="Simplifying Fractions",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=SIMPLIFY_NOTES,
        metadata=_diagram(n, d),
    )


# ---------------------------------------------------------------------------
# Level 1 — small factor (2-4)
# ---------------------------------------------------------------------------

def generate_simplifying_fractions_l1(calc_mode=False):
    reduced_n, reduced_d = random.choice(_SIMPLIFY_BASE_PAIRS)
    factor = random.randint(2, 4)
    return _build(reduced_n, reduced_d, factor)


# ---------------------------------------------------------------------------
# Level 2 — larger factor (5-9)
# ---------------------------------------------------------------------------

def generate_simplifying_fractions_l2(calc_mode=False):
    reduced_n, reduced_d = random.choice(_SIMPLIFY_BASE_PAIRS)
    factor = random.randint(5, 9)
    return _build(reduced_n, reduced_d, factor)


def generate_simplifying_fractions_question(calc_mode=False):
    return random.choice(
        [generate_simplifying_fractions_l1, generate_simplifying_fractions_l2]
    )(calc_mode=calc_mode)
