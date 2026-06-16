import random
from core.models.question_model import Question

NOTES = """
**Reading a Blood Pressure Chart:**

Blood pressure is measured as two numbers:
- **Systolic** (top): pressure when the heart beats (y-axis)
- **Diastolic** (bottom): pressure when the heart rests (x-axis)

**Categories (approximate boundaries):**

| Category | Systolic | Diastolic |
|---|---|---|
| Low | below 90 | below 60 |
| Ideal | 90–120 | 60–80 |
| Pre-high | 120–140 | 80–90 |
| High | above 140 **or** above 90 | (either reading) |

**Note:** If *either* reading is in the High zone, the overall category is High.

Type your answer as: **low** / **ideal** / **pre-high** / **high**
"""

# Each zone: name, systolic range (lo, hi), diastolic range (lo, hi)
# Ranges are chosen so readings clearly fall in one zone
_ZONES = [
    ("low",      (70, 89),   (40, 55)),
    ("ideal",    (90, 120),  (60, 80)),
    ("pre-high", (121, 139), (81, 90)),
    ("high",     (141, 185), (91, 100)),
]

_PEOPLE = ["Alex", "Sam", "Morgan", "Jordan", "Taylor", "Rupert", "Diana", "Chris"]
_ROLES  = ["teacher", "nurse", "bus driver", "office worker", "firefighter", "doctor"]


def generate_reading_scale():
    zone_name, (sys_lo, sys_hi), (dia_lo, dia_hi) = random.choice(_ZONES)

    # Round to nearest 5 for readability; clamp to zone bounds
    sys_candidates = [s for s in range(sys_lo, sys_hi + 1, 5)]
    dia_candidates = [d for d in range(dia_lo, dia_hi + 1, 5)]
    if not sys_candidates:
        sys_candidates = [sys_lo]
    if not dia_candidates:
        dia_candidates = [dia_lo]

    systolic = random.choice(sys_candidates)
    diastolic = random.choice(dia_candidates)

    person = random.choice(_PEOPLE)
    role = random.choice(_ROLES)
    answer = zone_name

    question_text = (
        f"{person} is a {role} and has their blood pressure taken.\n\n"
        f"The reading is:\n\n"
        f"**Systolic = {systolic},  Diastolic = {diastolic}**\n\n"
        f"Using the blood pressure chart above, what does this tell us about {person}'s blood pressure?\n\n"
        f"Type one of: **low** / **ideal** / **pre-high** / **high**"
    )

    def _classify_single(val, lo, hi):
        return "in range" if lo <= val <= hi else "out of range"

    scaffold_steps = [
        {"prompt": f"Locate Systolic = {systolic} on the vertical axis. Which zone?",
         "answer": f"{zone_name} ({sys_lo}–{sys_hi})"},
        {"prompt": f"Locate Diastolic = {diastolic} on the horizontal axis. Which zone?",
         "answer": f"{zone_name} ({dia_lo}–{dia_hi})"},
        {"prompt": "Overall blood pressure category (low / ideal / pre-high / high)", "answer": answer},
    ]

    worked = [
        f"Systolic = {systolic}: falls in the **{zone_name}** range ({sys_lo}–{sys_hi})",
        f"Diastolic = {diastolic}: falls in the **{zone_name}** range ({dia_lo}–{dia_hi})",
        f"Both readings place {person}'s blood pressure in the **{zone_name}** zone.",
        f"**Answer: {answer}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Time and Measurement",
        question_type="Reading Scale",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "blood_pressure",
            "diagram_params": {
                "systolic": systolic,
                "diastolic": diastolic,
                "zone": zone_name,
            },
        },
    )
