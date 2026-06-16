import random
from core.models.question_model import Question

NOTES = """
**Back-to-Back Stem and Leaf Diagrams:**

- The **stem** (middle column) is the tens digit
- **Left side** (read right → left from the stem): first dataset
- **Right side** (read left → right from the stem): second dataset
- Key: e.g. 6 | 3 = 63

**To find the mean:** add all values in the group, then divide by the count.

**Highest value:** scan both sides for the largest number.

**Comparing means:** state both means and describe whether the measure increased or decreased.
"""

_CONTEXTS = [
    {
        "measure": "resting heart rate (bpm)",
        "group1": "Before Training",
        "group2": "After Training",
        "unit": "bpm",
        "stems": [5, 6, 7, 8],
    },
    {
        "measure": "test score",
        "group1": "Class A",
        "group2": "Class B",
        "unit": "marks",
        "stems": [4, 5, 6, 7, 8],
    },
    {
        "measure": "daily step count (hundreds)",
        "group1": "Week 1",
        "group2": "Week 2",
        "unit": "hundred steps",
        "stems": [6, 7, 8, 9],
    },
]


def _gen_data(stems, n):
    vals = []
    for _ in range(n):
        s = random.choice(stems)
        leaf = random.randint(1, 9)
        vals.append(s * 10 + leaf)
    return sorted(vals)


def generate_stem_and_leaf():
    ctx = random.choice(_CONTEXTS)
    stems = ctx["stems"]
    n = 10

    group1 = _gen_data(stems, n)
    group2 = _gen_data(stems, n)

    # Ensure means differ by at least 3
    for _ in range(40):
        m1 = sum(group1) / n
        m2 = sum(group2) / n
        if abs(m1 - m2) >= 3:
            break
        group2 = _gen_data(stems, n)

    mean1 = round(sum(group1) / n, 1)
    mean2 = round(sum(group2) / n, 1)
    highest = max(group1 + group2)

    # Build stem-leaf by stem
    g1s = {s: [] for s in stems}
    g2s = {s: [] for s in stems}
    for v in group1:
        g1s[v // 10].append(v % 10)
    for v in group2:
        g2s[v // 10].append(v % 10)
    for s in stems:
        g1s[s].sort(reverse=True)
        g2s[s].sort()

    lines = [
        f"**{ctx['group1']}** | Stem | **{ctx['group2']}**",
        "---:|:---:|:---",
    ]
    for s in stems:
        left = " ".join(str(l) for l in g1s[s]) if g1s[s] else " "
        right = " ".join(str(l) for l in g2s[s]) if g2s[s] else " "
        lines.append(f"{left} | {s} | {right}")
    lines.append(f"n = {n} |  | n = {n}")
    lines.append(f" | *Key: 6 \\| 3 = 63 {ctx['unit']}* | ")

    display = "\n".join(lines)

    question_text = (
        f"The {ctx['measure']} for two groups is shown in the back-to-back stem and leaf diagram.\n\n"
        f"**(a)** What was the highest recorded value?\n\n"
        f"**(b)** Find the mean {ctx['measure']} for **{ctx['group1']}**.\n\n"
        f"The mean for **{ctx['group2']}** was {mean2} {ctx['unit']}.\n\n"
        f"**(c)** Has the {ctx['measure']} changed between the two groups? Explain your answer.\n\n"
        f"**Enter your answer for part (b) — the mean for {ctx['group1']}.**"
    )

    direction = "decreased" if mean1 > mean2 else "increased"
    diff = round(abs(mean1 - mean2), 1)

    scaffold_steps = [
        {"prompt": f"Highest value in the whole diagram", "answer": highest},
        {"prompt": f"Sum of all {ctx['group1']} values", "answer": sum(group1)},
        {"prompt": f"Mean = {sum(group1)} ÷ {n}", "answer": mean1},
    ]

    worked = [
        f"**(a) Highest value:** {highest} {ctx['unit']}",
        "",
        f"**(b) Mean for {ctx['group1']}:**",
        f"Values (reading left side): {group1}",
        f"Sum = {sum(group1)}",
        f"Mean = {sum(group1)} ÷ {n} = **{mean1} {ctx['unit']}**",
        "",
        f"**(c) Comparison:**",
        f"Mean for {ctx['group1']} = {mean1} {ctx['unit']}",
        f"Mean for {ctx['group2']} = {mean2} {ctx['unit']} (given)",
        f"The {ctx['measure']} has **{direction}** by {diff} {ctx['unit']} between the two groups.",
    ]

    return Question(
        question_text=question_text,
        correct_answer=mean1,
        topic="Data and Analysis",
        question_type="Stem and Leaf",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={"table": display},
    )
