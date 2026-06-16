import random
from core.models.question_model import Question

NOTES = """
**Experimental Probability:**

**Expected count** = Probability × Total

To compare actual results to what was expected:
1. Calculate the expected count: P × N
2. Compare to the actual count (or compare the actual probability to the expected probability)
3. Actual probability = actual count ÷ total

**Example:** P(faulty) = 0.014, 700 boxes delivered, 12 were faulty:
- Actual P = 12 ÷ 700 = 0.01714
- Since 0.01714 > 0.014, this is **more** than expected

Type your answer as: **more** or **less**
"""

_SCENARIOS = [
    {
        "item": "balloons", "unit": "boxes", "defect": "faulty balloon",
        "intro": "A shop orders balloons in boxes of seven.",
    },
    {
        "item": "light bulbs", "unit": "packs", "defect": "defective bulb",
        "intro": "A factory produces light bulbs packed in boxes.",
    },
    {
        "item": "eggs", "unit": "boxes", "defect": "cracked egg",
        "intro": "A farm packages eggs in boxes of twelve.",
    },
    {
        "item": "circuit boards", "unit": "batches", "defect": "faulty board",
        "intro": "A electronics firm produces circuit boards in batches.",
    },
]

_PROBS = [0.01, 0.012, 0.015, 0.02, 0.025, 0.03, 0.05]
_TOTALS = [200, 300, 400, 500, 600, 700, 800, 1000]


def generate_probability():
    sc = random.choice(_SCENARIOS)
    prob = random.choice(_PROBS)
    n = random.choice(_TOTALS)
    expected = prob * n

    is_more = random.choice([True, False])
    if is_more:
        actual = max(1, round(expected * random.uniform(1.3, 1.9)))
    else:
        actual = max(1, round(expected * random.uniform(0.2, 0.6)))

    actual_prob = round(actual / n, 5)
    answer = "more" if actual_prob > prob else "less"

    question_text = (
        f"{sc['intro']}\n\n"
        f"The probability of a {sc['unit'][:-1]} containing at least one {sc['defect']} is {prob}.\n\n"
        f"In a delivery of {n} {sc['unit']}, {actual} {sc['unit']} contained at least one {sc['defect']}.\n\n"
        f"Is this **more** or **less** than expected?\n\n"
        f"Use your working to explain your answer. Type **more** or **less**."
    )

    cmp = ">" if actual_prob > prob else "<"
    scaffold_steps = [
        {"prompt": f"Expected count = {prob} × {n}", "answer": round(expected, 2)},
        {"prompt": f"Actual probability = {actual} ÷ {n}", "answer": actual_prob},
        {"prompt": f"Is {actual_prob} {cmp} {prob}? Type more or less", "answer": answer},
    ]

    worked = [
        f"Expected count = {prob} × {n} = {expected:.2f} {sc['unit']}",
        f"Actual probability = {actual} ÷ {n} = {actual_prob}",
        f"Since {actual_prob} {cmp} {prob}, the actual number was **{answer}** than expected.",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Data and Analysis",
        question_type="Probability",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
