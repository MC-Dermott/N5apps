import random
from core.models.question_model import Question

NOTES_L1 = """
**Indirect Proportion (Inverse Proportion):**

Two quantities are in indirect (inverse) proportion when one **decreases** as the other
**increases** — for example, a task takes less time as more people work on it, at the same rate
each.

**Method — value for 1:**
If **A** people take **B** hours to do a job, and you want the time for **C** people:

**Value for 1 person = A × B**
**Answer = (A × B) ÷ C**

**Example:** It takes 3 people 8 hours to paint a fence. How long would 4 people take, working at
the same rate?
- Value for 1 person = 3 × 8 = 24
- Answer = 24 ÷ 4 = **6 hours**
"""

NOTES_L2 = """
**Indirect Proportion in Other Contexts:**

The same value-for-1 method works whenever one quantity increases as another decreases at a
steady rate — food lasting fewer or more animals, a faster speed giving a shorter journey time,
or more machines finishing a job sooner.

**Value for 1 = (first quantity) × (first amount)**
**Answer = value for 1 ÷ (second quantity)**

**Example:** A tub of feed lasts 6 hens 8 days, eating at the same rate. How long would it last 4
hens?
- Value for 1 = 6 × 8 = 48
- Answer = 48 ÷ 4 = **12 days**
"""


def _find_inverse_triple(hi, time_hi):
    """Finds (q1, q2, a1, a2) with q1 people/units taking a1 to do a job, q2 taking a2,
    such that q1 * a1 (the constant "value for 1") divides cleanly by q2. Returns None if no
    clean combination is found within the attempt budget."""
    for _ in range(50):
        q1 = random.randint(2, hi)
        q2 = random.choice([q for q in range(2, hi) if q != q1])
        a1 = random.randint(2, time_hi)
        product = q1 * a1
        if product % q2 == 0:
            return q1, q2, a1, product // q2
    return None


# ---------------------------------------------------------------------------
# Level 1 — people and time (how long a task takes as the number of people changes)
# ---------------------------------------------------------------------------

_L1_CONTEXTS = [
    {"plural": "crofters", "singular": "crofter", "task": "gather in the sheep from the hill", "unit": "hours"},
    {"plural": "volunteers", "singular": "volunteer", "task": "clear the litter from a stretch of machair", "unit": "hours"},
    {"plural": "fishermen", "singular": "fisherman", "task": "mend the nets", "unit": "hours"},
    {"plural": "workers", "singular": "worker", "task": "lay a new stretch of pier", "unit": "hours"},
    {"plural": "joiners", "singular": "joiner", "task": "build a byre extension", "unit": "hours"},
    {"plural": "weavers", "singular": "weaver", "task": "complete an order of Harris Tweed", "unit": "days"},
    {"plural": "gardeners", "singular": "gardener", "task": "dig over the community allotment", "unit": "hours"},
    {"plural": "thatchers", "singular": "thatcher", "task": "thatch a blackhouse roof", "unit": "hours"},
]


def generate_indirect_proportion_l1(calc_mode=False):
    ctx = random.choice(_L1_CONTEXTS)
    hi = 9 if calc_mode else 14
    time_hi = 12 if calc_mode else 24
    triple = _find_inverse_triple(hi, time_hi)
    q1, q2, a1, a2 = triple if triple else (4, 6, 12, 8)

    question_text = (
        f"It takes {q1} {ctx['plural']} {a1} {ctx['unit']} to {ctx['task']}, working at the "
        f"same rate.\n\nHow long would it take {q2} {ctx['plural']}?"
    )

    value_of_one = q1 * a1
    scaffold_steps = [
        {"prompt": f"Find the value for 1 {ctx['singular']} (multiply)", "answer": value_of_one},
        {"prompt": f"Divide by {q2} to find the time for {q2} {ctx['plural']}", "answer": a2},
    ]

    worked = [
        f"1 {ctx['singular']} = {q1} × {a1} = {value_of_one} {ctx['unit']}",
        f"{q2} {ctx['plural']} = {value_of_one} ÷ {q2} = {a2} {ctx['unit']}",
        f"**{q2} {ctx['plural']} would take {a2} {ctx['unit']}.**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=a2,
        topic="Numeracy",
        question_type="Indirect Proportion",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L1,
    )


# ---------------------------------------------------------------------------
# Level 2 — other real-world indirect proportion (animals/food, speed/time, work-rate)
# ---------------------------------------------------------------------------

_L2_ANIMAL_CONTEXTS = [
    {"plural": "hens", "singular": "hen", "food": "A bag of feed", "unit": "days"},
    {"plural": "sheep", "singular": "sheep", "food": "A sack of concentrate feed", "unit": "days"},
    {"plural": "seals", "singular": "seal", "food": "A creel of herring", "unit": "days"},
    {"plural": "cows", "singular": "cow", "food": "A bale of silage", "unit": "days"},
]


def _l2_animal_question(calc_mode=False):
    ctx = random.choice(_L2_ANIMAL_CONTEXTS)
    hi = 9 if calc_mode else 14
    time_hi = 12 if calc_mode else 24
    triple = _find_inverse_triple(hi, time_hi)
    q1, q2, a1, a2 = triple if triple else (8, 6, 3, 4)

    question_text = (
        f"{ctx['food']} lasts {q1} {ctx['plural']} {a1} {ctx['unit']}, eating at the same "
        f"rate.\n\nHow long would it last {q2} {ctx['plural']}?"
    )

    value_of_one = q1 * a1
    scaffold_steps = [
        {"prompt": f"Find the value for 1 {ctx['singular']} (multiply)", "answer": value_of_one},
        {"prompt": f"Divide by {q2} to find how long it lasts {q2} {ctx['plural']}", "answer": a2},
    ]

    worked = [
        f"1 {ctx['singular']} = {q1} × {a1} = {value_of_one} {ctx['unit']}",
        f"{q2} {ctx['plural']} = {value_of_one} ÷ {q2} = {a2} {ctx['unit']}",
        f"**It would last {q2} {ctx['plural']} {a2} {ctx['unit']}.**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=a2,
        topic="Numeracy",
        question_type="Indirect Proportion",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


_L2_SPEED_CONTEXTS = [
    {"journey": "the ferry crossing to the mainland", "unit": "knots"},
    {"journey": "the tour bus journey to Stornoway", "unit": "mph"},
    {"journey": "the fishing boat's trip out to the grounds", "unit": "knots"},
    {"journey": "the ambulance's journey along the single-track road", "unit": "mph"},
]


def _l2_speed_question(calc_mode=False):
    ctx = random.choice(_L2_SPEED_CONTEXTS)
    hi = 9 if calc_mode else 14
    time_hi = 8 if calc_mode else 12
    triple = _find_inverse_triple(hi, time_hi)
    speed1, speed2, time1, time2 = triple if triple else (12, 20, 5, 3)

    question_text = (
        f"At a speed of {speed1} {ctx['unit']}, {ctx['journey']} takes {time1} hours.\n\n"
        f"How long would {ctx['journey']} take at a speed of {speed2} {ctx['unit']}?"
    )

    distance = speed1 * time1
    scaffold_steps = [
        {"prompt": "Find the distance (multiply speed × time)", "answer": distance},
        {"prompt": f"Divide by {speed2} to find the time at the new speed", "answer": time2},
    ]

    worked = [
        f"Distance = {speed1} × {time1} = {distance}",
        f"Time = {distance} ÷ {speed2} = {time2} hours",
        f"**At {speed2} {ctx['unit']}, the journey would take {time2} hours.**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=time2,
        topic="Numeracy",
        question_type="Indirect Proportion",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


_L2_WORKRATE_CONTEXTS = [
    {"plural": "water pumps", "singular": "water pump", "task": "empty the flooded field", "unit": "hours"},
    {"plural": "buckets", "singular": "bucket", "task": "bail out the rowing boat", "unit": "minutes"},
    {"plural": "hoses", "singular": "hose", "task": "fill the water tank", "unit": "minutes"},
    {"plural": "diggers", "singular": "digger", "task": "clear the storm-damaged track", "unit": "hours"},
]


def _l2_workrate_question(calc_mode=False):
    ctx = random.choice(_L2_WORKRATE_CONTEXTS)
    hi = 8 if calc_mode else 12
    time_hi = 12 if calc_mode else 24
    triple = _find_inverse_triple(hi, time_hi)
    q1, q2, a1, a2 = triple if triple else (3, 2, 4, 6)

    question_text = (
        f"{q1} {ctx['plural']} can {ctx['task']} in {a1} {ctx['unit']}, working at the same "
        f"rate.\n\nHow long would it take {q2} {ctx['plural']}?"
    )

    value_of_one = q1 * a1
    scaffold_steps = [
        {"prompt": f"Find the value for 1 {ctx['singular']} (multiply)", "answer": value_of_one},
        {"prompt": f"Divide by {q2} to find the time for {q2} {ctx['plural']}", "answer": a2},
    ]

    worked = [
        f"1 {ctx['singular']} = {q1} × {a1} = {value_of_one} {ctx['unit']}",
        f"{q2} {ctx['plural']} = {value_of_one} ÷ {q2} = {a2} {ctx['unit']}",
        f"**{q2} {ctx['plural']} would take {a2} {ctx['unit']}.**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=a2,
        topic="Numeracy",
        question_type="Indirect Proportion",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
    )


def generate_indirect_proportion_l2(calc_mode=False):
    return random.choice([
        _l2_animal_question,
        _l2_speed_question,
        _l2_workrate_question,
    ])(calc_mode=calc_mode)


# ---------------------------------------------------------------------------
# Default dispatcher
# ---------------------------------------------------------------------------

def generate_indirect_proportion_question(calc_mode=False):
    return random.choice([
        generate_indirect_proportion_l1,
        generate_indirect_proportion_l2,
    ])(calc_mode=calc_mode)
