import random
from core.models.question_model import Question

NOTES = """
**Reading Bar Charts:**

- Read the height of each bar from the y-axis scale
- To find a total: add up all the bar heights for that group
- To compare groups: identify which bars are taller for each category
- When bars fall between grid lines, **estimate** to the nearest value shown

*Tip: Label each bar value as you read it, then add them up.*
"""

_SCENARIOS = [
    {
        "title": "Mobile Phone Ownership",
        "x_label": "No. of phones owned",
        "y_label": "No. of people",
        "group1": "Girls",
        "group2": "Boys",
        "categories": ["0–4", "5–9", "10–14", "15–19", "20–24"],
    },
    {
        "title": "Weekly Sports Participation",
        "x_label": "Sport",
        "y_label": "No. of students",
        "group1": "Girls",
        "group2": "Boys",
        "categories": ["Football", "Tennis", "Swimming", "Athletics", "Cycling"],
    },
    {
        "title": "Favourite School Subjects",
        "x_label": "Subject",
        "y_label": "No. of pupils",
        "group1": "S1",
        "group2": "S2",
        "categories": ["Maths", "English", "Science", "History", "Art"],
    },
    {
        "title": "Library Book Borrowing",
        "x_label": "Book Genre",
        "y_label": "No. of books borrowed",
        "group1": "Adults",
        "group2": "Teenagers",
        "categories": ["Fiction", "Non-fiction", "Crime", "Science Fiction", "Biography"],
    },
]


def _bar_vals(n, lo=2, hi=35, step=2):
    return [random.choice(range(lo, hi + 1, step)) for _ in range(n)]


def generate_reading_bar_charts():
    sc = random.choice(_SCENARIOS)
    n = len(sc["categories"])

    g1 = _bar_vals(n)
    g2 = _bar_vals(n)

    # Ensure at least 2 categories where each group leads
    for _ in range(30):
        g1_leads = sum(1 for a, b in zip(g1, g2) if a > b)
        g2_leads = sum(1 for a, b in zip(g1, g2) if b > a)
        if g1_leads >= 2 and g2_leads >= 2:
            break
        g1 = _bar_vals(n)
        g2 = _bar_vals(n)

    g1_wins = [sc["categories"][i] for i in range(n) if g1[i] > g2[i]]
    total_g2 = sum(g2)

    question_text = (
        f"The bar chart above shows **{sc['title'].lower()}**.\n\n"
        f"**(a)** In which categories did **{sc['group1']}** outnumber **{sc['group2']}**?\n\n"
        f"**(b)** Estimate how many **{sc['group2']}** in total are shown in the chart.\n\n"
        f"**(c)** What does the chart tell you about the difference between "
        f"{sc['group1']} and {sc['group2']}?\n\n"
        f"**Enter your answer for part (b) — the total for {sc['group2']}.**"
    )

    scaffold_steps = [
        {"prompt": f"Read each {sc['group2']} bar value", "answer": str(g2)},
        {"prompt": f"Total for {sc['group2']}", "answer": total_g2},
    ]

    worked = [
        f"**(a)** {sc['group1']} outnumber {sc['group2']} in: **{', '.join(g1_wins)}**",
        "",
        f"**(b)** {sc['group2']} bar values: {g2}",
        f"Total = {' + '.join(str(v) for v in g2)} = **{total_g2}**",
        "",
        f"**(c)** The chart shows the relative patterns of {sc['group1']} vs {sc['group2']} "
        f"across the different categories.",
    ]

    return Question(
        question_text=question_text,
        correct_answer=total_g2,
        topic="Data and Analysis",
        question_type="Reading Bar Charts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "bar_chart",
            "diagram_params": {
                "categories": sc["categories"],
                "group1_data": g1,
                "group2_data": g2,
                "group1_name": sc["group1"],
                "group2_name": sc["group2"],
                "x_label": sc["x_label"],
                "y_label": sc["y_label"],
                "title": sc["title"],
            },
        },
    )
