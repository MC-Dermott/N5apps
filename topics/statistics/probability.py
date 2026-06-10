import random
import math
from core.models.question_model import Question

NOTES = """
**Probability:**

**P(event)** = number of favourable outcomes ÷ total outcomes

- Always between 0 (impossible) and 1 (certain)
- **Complementary:** P(not A) = 1 − P(A)
- **Independent events:** P(A and B) = P(A) × P(B)

**Example:**
A bag has 3 red and 7 blue balls. P(red) = 3 ÷ 10 = **0.3**

P(not red) = 1 − 0.3 = **0.7**
"""

_COLOURS = ["red", "blue", "green", "yellow", "purple", "orange", "white", "black"]


def _other(colour):
    return random.choice([c for c in _COLOURS if c != colour])


def generate_probability_question():
    kind = random.choice(["single", "complement", "independent"])

    if kind == "single":
        total = random.randint(8, 20)
        fav = random.randint(1, total - 1)
        p = round(fav / total, 4)
        colour = random.choice(_COLOURS)
        other = _other(colour)
        rest = total - fav

        question_text = (
            f"A bag contains {fav} {colour} balls and {rest} {other} balls. "
            f"A ball is chosen at random. "
            f"Calculate the probability of picking a {colour} ball. "
            f"Give your answer as a decimal."
        )
        scaffold_steps = [
            {"prompt": "Count the total number of balls", "answer": total},
            {"prompt": f"Count the {colour} balls", "answer": fav},
            {"prompt": "Divide favourable outcomes by total", "answer": p},
        ]
        g = math.gcd(fav, total)
        worked = [
            f"P({colour}) = {fav} ÷ {total} = {fav // g}/{total // g} = {p}",
        ]
        answer = p

    elif kind == "complement":
        total = random.randint(8, 20)
        fav = random.randint(1, total - 1)
        p_event = round(fav / total, 4)
        p_not = round(1 - p_event, 4)
        colour = random.choice(_COLOURS)
        other = _other(colour)
        rest = total - fav

        question_text = (
            f"A bag contains {fav} {colour} balls and {rest} {other} balls. "
            f"A ball is chosen at random. "
            f"Calculate the probability of NOT picking a {colour} ball. "
            f"Give your answer as a decimal."
        )
        scaffold_steps = [
            {"prompt": f"Find P({colour})", "answer": p_event},
            {"prompt": "Use P(not A) = 1 − P(A)", "answer": p_not},
        ]
        worked = [
            f"P({colour}) = {fav} ÷ {total} = {p_event}",
            f"P(not {colour}) = 1 − {p_event} = {p_not}",
        ]
        answer = p_not

    else:  # independent
        total_a = random.randint(4, 10)
        fav_a = random.randint(1, total_a - 1)
        total_b = random.randint(4, 10)
        fav_b = random.randint(1, total_b - 1)
        pa = round(fav_a / total_a, 4)
        pb = round(fav_b / total_b, 4)
        p_both = round(pa * pb, 4)
        colour_a = random.choice(_COLOURS)
        colour_b = _other(colour_a)

        question_text = (
            f"Bag A contains {fav_a} {colour_a} balls and {total_a - fav_a} others. "
            f"Bag B contains {fav_b} {colour_b} balls and {total_b - fav_b} others. "
            f"One ball is drawn at random from each bag. "
            f"Calculate the probability of picking a {colour_a} from Bag A "
            f"AND a {colour_b} from Bag B. "
            f"Give your answer as a decimal."
        )
        scaffold_steps = [
            {"prompt": f"Find P({colour_a} from A) = {fav_a} ÷ {total_a}", "answer": pa},
            {"prompt": f"Find P({colour_b} from B) = {fav_b} ÷ {total_b}", "answer": pb},
            {"prompt": "Multiply for independent events: P(A) × P(B)", "answer": p_both},
        ]
        worked = [
            f"P({colour_a} from A) = {fav_a} ÷ {total_a} = {pa}",
            f"P({colour_b} from B) = {fav_b} ÷ {total_b} = {pb}",
            f"P(both) = {pa} × {pb} = {p_both}",
        ]
        answer = p_both

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Statistics",
        question_type="Probability",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
