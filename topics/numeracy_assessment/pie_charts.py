import random
from core.models.question_model import Question

NOTES = """
**Reading Pie Charts:**

Each sector's angle is proportional to its count.

**To find the total from a known sector:**
- Total = known_count × (360 ÷ known_angle)

**To find another sector's count:**
- Count = (sector_angle ÷ 360) × Total

**Shortcut:** Count_B = known_count × (angle_B ÷ angle_known)
"""

# Each scenario has categories with fixed angles (summing to 360),
# a reference sector whose count will be given, and a target sector to find.
# counts_for_ref: valid counts for the reference sector that produce integer answers.
_SCENARIOS = [
    {
        "context": "how pupils travel to school",
        "survey": "S1–S6 pupils at a local school",
        "categories": [("Walk", 140), ("Bus", 120), ("Car", 60), ("Cycle", 40)],
        "ref_idx": 2,   # Car = 60°
        "ask_idx": 0,   # Walk = 140° → integer when ref is multiple of 3
        "ref_counts": [60, 90, 120, 180, 240, 300],
    },
    {
        "context": "favourite sports",
        "survey": "students in a year group",
        "categories": [("Football", 120), ("Swimming", 80), ("Tennis", 60), ("Athletics", 100)],
        "ref_idx": 2,   # Tennis = 60°
        "ask_idx": 0,   # Football = 120°
        "ref_counts": [60, 120, 180, 240],
    },
    {
        "context": "types of pet owned",
        "survey": "pet owners in a local survey",
        "categories": [("Dogs", 150), ("Cats", 120), ("Fish", 60), ("Other", 30)],
        "ref_idx": 2,   # Fish = 60°
        "ask_idx": 0,   # Dogs = 150°
        "ref_counts": [60, 120, 180, 240],
    },
    {
        "context": "how people spend their leisure time",
        "survey": "adults in a town",
        "categories": [("TV", 120), ("Sport", 80), ("Reading", 40), ("Gaming", 120)],
        "ref_idx": 2,   # Reading = 40°
        "ask_idx": 0,   # TV = 120°
        "ref_counts": [40, 80, 120, 160, 200],
    },
    {
        "context": "favourite school subjects",
        "survey": "S3 pupils",
        "categories": [("Science", 90), ("English", 120), ("Maths", 90), ("PE", 60)],
        "ref_idx": 3,   # PE = 60°
        "ask_idx": 1,   # English = 120°
        "ref_counts": [60, 120, 180, 240],
    },
]


def generate_pie_charts():
    sc = random.choice(_SCENARIOS)
    ref_count = random.choice(sc["ref_counts"])
    ref_cat, ref_angle = sc["categories"][sc["ref_idx"]]
    ask_cat, ask_angle = sc["categories"][sc["ask_idx"]]

    total = ref_count * 360 // ref_angle
    ask_count = ask_angle * total // 360

    question_text = (
        f"A survey of {sc['survey']} was carried out to find out {sc['context']}.\n\n"
        f"The pie chart above shows the results.\n\n"
        f"**{ref_count}** people said **{ref_cat}**.\n\n"
        f"How many people said **{ask_cat}**?"
    )

    scaffold_steps = [
        {"prompt": f"Total surveyed = {ref_count} × (360 ÷ {ref_angle})", "answer": total},
        {"prompt": f"Number choosing {ask_cat} = ({ask_angle} ÷ 360) × {total}", "answer": ask_count},
    ]

    worked = [
        f"The {ref_cat} sector has angle {ref_angle}° and represents {ref_count} people.",
        f"Total = {ref_count} × (360 ÷ {ref_angle}) = {ref_count} × {360 // ref_angle} = {total}",
        f"The {ask_cat} sector has angle {ask_angle}°",
        f"Number choosing {ask_cat} = ({ask_angle} ÷ 360) × {total} = **{ask_count}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=ask_count,
        topic="Data and Analysis",
        question_type="Pie Charts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": [c[0] for c in sc["categories"]],
                "angles": [c[1] for c in sc["categories"]],
                "ref_cat": ref_cat,
                "ref_count": ref_count,
                "ask_cat": ask_cat,
            },
        },
    )
