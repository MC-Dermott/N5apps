import math
import random

from core.models.question_model import Question

_HEADLINE = "### **The fraction of a pie chart covered by a segment = the fraction of the total**"

NOTES_L1 = f"""
{_HEADLINE}

**Reading Pie Charts**

There are 360° in a full circle — a sector's angle is always a fraction of 360°.

**Fraction represented by a sector:**
Fraction = sector angle ÷ 360

**Example:** A sector has an angle of 90°.
- Fraction = 90 ÷ 360
- = 1/4 (dividing both numbers by 90)
"""

NOTES_L2 = f"""
{_HEADLINE}

**Finding a Missing Angle**

The angles in a pie chart always add up to 360°.

Missing angle = 360 − (sum of the angles you already know)

**Example:** A pie chart shows: Tea: 110°, Coffee: 100°, Juice: **?**.
- Missing angle = 360 − 110 − 100 = 150°
- Fraction = 150 ÷ 360 = 5/12
"""

NOTES_L3 = f"""
{_HEADLINE}

**Finding an Amount from an Angle and a Total**

1. Find the segment's fraction: Fraction = sector angle ÷ 360
2. Multiply by the total: Amount = fraction × total

**Example:** A pie chart shows a 90° segment. The total represented by the whole chart is
200 people.
- Fraction = 90 ÷ 360 = 1/4
- Amount = 1/4 × 200 = 50 people
"""

NOTES_L4 = f"""
{_HEADLINE}

**Working from One Known Segment**

If you know one segment's angle AND its value, you can work out the value of any other
segment — or the total — without knowing the overall total in advance.

Value per degree = known value ÷ known angle
Other segment's value = other angle × value per degree
Total = 360 × value per degree

**Example:** A 60° segment represents 120 people.
- Value per degree = 120 ÷ 60 = 2 people per degree
- A 90° segment = 90 × 2 = 180 people
- Total = 360 × 2 = 720 people
"""

NOTES_L5 = f"""
{_HEADLINE}

**Calculating Angles from a Frequency Table**

1. Add up the frequencies to find the **total**.
2. For each category, find its **fraction** of the total: fraction = frequency ÷ total.
3. Multiply the fraction by 360° to find that category's **angle**.

**Example:** A survey of 18 people asked which country they'd like to visit.

| Country | Frequency |
|:---|:---|
| France | 3 |
| Wales | 4 |
| England | 11 |

- France: fraction = 3 ÷ 18 = 1/6 → angle = 1/6 × 360 = 60°
- Wales: fraction = 4 ÷ 18 = 2/9 → angle = 2/9 × 360 = 80°
- England: fraction = 11 ÷ 18 → angle = 11/18 × 360 = 220°
- Check: 60 + 80 + 220 = 360° ✓
"""

_PALETTE = ["#5b9bd5", "#ed7d31", "#70ad47", "#ffc000", "#7030a0", "#c00000", "#4472c4", "#548235"]


def _freq_table_md(categories, frequencies, category_label="Category", value_label="Frequency"):
    header = f"| {category_label} | {value_label} |\n|:---|:---|\n"
    rows = "".join(f"| {c} | {f} |\n" for c, f in zip(categories, frequencies))
    return header + rows


def _split_degrees(total, n):
    """Split `total` degrees into exactly `n` positive-integer pieces (random cut points)."""
    if n <= 1:
        return [total]
    cuts = sorted(random.sample(range(1, total), n - 1))
    bounds = [0] + cuts + [total]
    return [bounds[i + 1] - bounds[i] for i in range(len(bounds) - 1)]


# ---------------------------------------------------------------------------
# Level 1 — Fraction from the Angle
# ---------------------------------------------------------------------------

_L1_ANGLES = [24, 30, 36, 40, 45, 60, 72, 90, 120, 135, 144, 150, 160, 180, 200, 210, 225, 240, 270, 300]

_L1_SCENARIOS = [
    ("A survey of S1 pupils at Sir E Scott School asked how they travel to school",
     ["By minibus", "By car", "On foot", "By bicycle"]),
    ("A survey of Tarbert fishermen recorded which species they landed most last week",
     ["Langoustine", "Crab", "Mackerel", "Other species"]),
    ("A survey of Harris Tweed mill workers asked their favourite pattern",
     ["Herringbone", "Houndstooth", "Plain twill", "Check"]),
    ("A survey of Scalpay crofters recorded which animals they keep",
     ["Sheep", "Cattle", "Hens", "Goats"]),
    ("A survey of Leverburgh ceilidh-goers asked their favourite dance",
     ["Strip the Willow", "Eightsome Reel", "Dashing White Sergeant", "Waltz"]),
    ("A survey of CalMac passengers on the Uig crossing asked how they were travelling",
     ["On foot", "By car", "By coach", "By bicycle"]),
    ("A survey of Ness households recorded how they heat their home",
     ["Peat", "Oil", "Electric", "Wood"]),
    ("A survey of Stornoway pupils asked their favourite subject",
     ["Art", "Maths", "PE", "English"]),
    ("A survey of Berneray pupils asked their favourite ceilidh dance",
     ["Eightsome Reel", "Strip the Willow", "Waltz", "Polka"]),
    ("A survey of Uig crofters recorded their main occupation",
     ["Fishing", "Crofting", "Weaving", "Tourism"]),
]


def generate_pie_charts_l1():
    context, categories = random.choice(_L1_SCENARIOS)
    category = categories[0]
    angle = random.choice(_L1_ANGLES)
    other_angles = _split_degrees(360 - angle, len(categories) - 1)
    colors = random.sample(_PALETTE, len(categories))

    g = math.gcd(angle, 360)
    n, d = angle // g, 360 // g
    answer_str = f"{n}/{d}"

    question_text = (
        f"{context}. The pie chart above shows the results.\n\n"
        f"Write the **{category}** segment as a fraction of the whole pie chart, in its "
        f"simplest form."
    )

    worked = [
        f"Fraction = {angle} ÷ 360",
        f"= {answer_str} (dividing both numbers by {g})",
    ]

    angles = [angle] + other_angles

    return Question(
        question_text=question_text,
        correct_answer=answer_str,
        topic="Numeracy",
        question_type="Pie Charts",
        worked_solution=worked,
        notes=NOTES_L1,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": categories,
                "angles": angles,
                "colors": colors,
                "wedge_labels": [f"{a}°" for a in angles],
                "show_legend": True,
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — Finding the Missing Angle
# ---------------------------------------------------------------------------

_L2_CONTEXTS = [
    ("A Leverburgh crofter's day is split between feeding livestock, mending fences, and paperwork",
     ["Feeding livestock", "Mending fences", "Paperwork"]),
    ("Passengers on the Berneray causeway bus travelled by car, on foot, or by bicycle",
     ["Car", "On foot", "Bicycle"]),
    ("A weekly shop at the Tarbert co-op is split between groceries, fuel, and other spending",
     ["Groceries", "Fuel", "Other"]),
    ("A Stornoway S3 class spend their lunchtime on sport, homework club, or the library",
     ["Sport", "Homework club", "Library"]),
    ("Visitors to the Callanish Stones travelled by coach, car, or bicycle",
     ["Coach", "Car", "Bicycle"]),
    ("A Scalpay fishing boat's catch is split between prawns, crab, and other species",
     ["Prawns", "Crab", "Other species"]),
]

_L2_PAIRS = [(150, 120), (130, 170), (45, 270), (36, 144), (300, 30), (20, 160), (135, 105), (200, 100)]


def generate_pie_charts_l2():
    context, labels = random.choice(_L2_CONTEXTS)
    a1, a2 = random.choice(_L2_PAIRS)
    missing = 360 - a1 - a2
    g = math.gcd(missing, 360)
    n, d = missing // g, 360 // g
    fraction_str = f"{n}/{d}"
    cat1, cat2, cat3 = labels
    colors = random.sample(_PALETTE, 3)

    question_text = (
        f"{context}. The pie chart above shows: **{cat1}**: {a1}°, **{cat2}**: {a2}°, "
        f"and **{cat3}**: **?**.\n\n"
        f"(a) Work out the missing angle marked '?'.\n\n"
        f"(b) Write **{cat3}** as a fraction of the whole pie chart, in its simplest form."
    )

    scaffold_steps = [
        {"prompt": "Missing angle = 360 − (the two known angles)", "answer": missing},
        {"prompt": "Fraction = missing angle ÷ 360, simplified", "answer": fraction_str},
    ]

    worked = [
        f"Missing angle = 360 − {a1} − {a2} = {missing}°",
        f"Fraction = {missing} ÷ 360 = {fraction_str}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=fraction_str,
        topic="Numeracy",
        question_type="Pie Charts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L2,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": [cat1, cat2, cat3],
                "angles": [a1, a2, missing],
                "colors": colors,
                "wedge_labels": [f"{a1}°", f"{a2}°", "?"],
                "show_legend": True,
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 3 — Calculating the Amount
# ---------------------------------------------------------------------------

_L3_SCENARIOS = [
    {
        "context": "A weekly household budget of £{total} on Scalpay, split by spending type.",
        "categories": ["Petrol", "Groceries", "Heating", "Other"],
        "unit": "£", "angle": 72,
        "totals": [100, 150, 200, 250, 300],
    },
    {
        "context": "The {total}-minute school day at Sir E Scott School, by activity.",
        "categories": ["PE", "Registration", "Lessons", "Lunch"],
        "unit": "minutes", "angle": 60,
        "totals": [360, 420, 480, 540, 600],
    },
    {
        "context": "{total} passengers on a CalMac sailing to Tarbert, by type.",
        "categories": ["Foot passengers", "Car passengers", "Coach passengers", "Freight"],
        "unit": "people", "angle": 90,
        "totals": [120, 160, 200, 240, 280],
    },
    {
        "context": "£{total} raised at the Leverburgh hall fundraiser, by activity.",
        "categories": ["The raffle", "Tombola", "Cake stall", "Entry donations"],
        "unit": "£", "angle": 45,
        "totals": [160, 240, 320, 400, 480],
    },
    {
        "context": "{total} people on Harris surveyed about their main occupation.",
        "categories": ["Crofting", "Fishing", "Tourism", "Weaving"],
        "unit": "people", "angle": 40,
        "totals": [90, 180, 270, 360, 450],
    },
    {
        "context": "A {total}-hour working week for a Scalpay fisherman, by task.",
        "categories": ["Hauling creels", "Sailing", "Mending nets", "Selling the catch"],
        "unit": "hours", "angle": 120,
        "totals": [36, 45, 54, 63, 72],
    },
]


def generate_pie_charts_l3():
    sc = random.choice(_L3_SCENARIOS)
    total = random.choice(sc["totals"])
    angle = sc["angle"]
    categories = sc["categories"]
    other_angles = _split_degrees(360 - angle, len(categories) - 1)
    colors = random.sample(_PALETTE, len(categories))
    amount = angle * total // 360
    g = math.gcd(angle, 360)
    n, d = angle // g, 360 // g
    fraction_str = f"{n}/{d}"
    unit = sc["unit"]
    context = sc["context"].format(total=total)
    caption = f"Total: £{total}" if unit == "£" else f"Total: {total} {unit}"
    category = categories[0]

    question_text = (
        f"{context}\n\n"
        f"Use the angle of the **{category}** segment, together with the total given, to "
        f"calculate the amount it represents."
    )

    scaffold_steps = [
        {"prompt": "Fraction = segment's angle ÷ 360, simplified", "answer": fraction_str},
        {"prompt": "Amount = fraction (from the previous step) × total", "answer": amount},
    ]

    amount_str = f"£{amount}" if unit == "£" else f"{amount} {unit}"
    worked = [
        f"Fraction = {angle} ÷ 360 = {fraction_str}",
        f"Amount = {fraction_str} × {total} = {amount_str}",
    ]

    angles = [angle] + other_angles

    return Question(
        question_text=question_text,
        correct_answer=amount,
        topic="Numeracy",
        question_type="Pie Charts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L3,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": categories,
                "angles": angles,
                "colors": colors,
                "wedge_labels": [f"{a}°" for a in angles],
                "show_legend": True,
                "caption": caption,
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 4 — Working from One Segment
# ---------------------------------------------------------------------------

_L4_SCENARIOS = [
    {
        "context": "Favourite Harris Tweed colour among mill workers at Tarbert.",
        "known": "Herringbone Grey", "known_angle": 45,
        "target": "Moorland Green", "target_angle": 90,
        "others": ["Peat Brown", "Machair Blue"],
        "unit": "votes",
    },
    {
        "context": "A Scalpay fisherman's day, split by task.",
        "known": "Baiting creels", "known_angle": 80,
        "target": "Sailing", "target_angle": 40,
        "others": ["Hauling creels", "Mending nets"],
        "unit": "minutes",
    },
    {
        "context": "CalMac ferry passengers on the Uig–Lochmaddy crossing, by type.",
        "known": "Car passengers", "known_angle": 150,
        "target": "Foot passengers", "target_angle": 90,
        "others": ["Bicycle passengers", "Freight"],
        "unit": "people",
    },
    {
        "context": "Favourite subjects among S3 pupils at Sir E Scott School.",
        "known": "PE", "known_angle": 60,
        "target": "Maths", "target_angle": 120,
        "others": ["Art", "English"],
        "unit": "pupils",
    },
    {
        "context": "Croft chores on Scalpay over the course of a month.",
        "known": "Feeding sheep", "known_angle": 100,
        "target": "Repairing fences", "target_angle": 50,
        "others": ["Milking", "Peat cutting"],
        "unit": "hours",
    },
]

_L4_PER_DEGREE = [1, 2, 3, 4, 5]


def generate_pie_charts_l4():
    sc = random.choice(_L4_SCENARIOS)
    k = random.choice(_L4_PER_DEGREE)
    known_value = k * sc["known_angle"]
    target_value = k * sc["target_angle"]
    total = k * 360
    unit = sc["unit"]

    question_text = (
        f"{sc['context']} The pie chart above shows: **{sc['known']}**: {sc['known_angle']}°, "
        f"{known_value} {unit}. **{sc['target']}**: {sc['target_angle']}°, **?**.\n\n"
        f"(a) Find the value of the segment marked '?'.\n\n"
        f"(b) Find the total represented by the whole pie chart.\n\n"
        f"**Enter your answer for part (b).**"
    )

    scaffold_steps = [
        {"prompt": "Value per degree = known segment's value ÷ known segment's angle", "answer": k},
        {"prompt": "(a) Value of ? = target segment's angle × value per degree (from the previous step)", "answer": target_value},
        {"prompt": "(b) Total = 360 × value per degree", "answer": total},
    ]

    worked = [
        f"Value per degree = {known_value} ÷ {sc['known_angle']} = {k}",
        f"(a) {sc['target']} = {sc['target_angle']} × {k} = {target_value} {unit}",
        f"(b) Total = 360 × {k} = {total} {unit}",
    ]

    rest_angle = 360 - sc["known_angle"] - sc["target_angle"]
    other_angles = _split_degrees(rest_angle, len(sc["others"]))
    categories = [sc["known"], sc["target"]] + sc["others"]
    colors = random.sample(_PALETTE, len(categories))
    angles = [sc["known_angle"], sc["target_angle"]] + other_angles
    wedge_labels = (
        [f"{sc['known_angle']}°\n({known_value})", f"{sc['target_angle']}°\n?"]
        + [f"{a}°" for a in other_angles]
    )

    return Question(
        question_text=question_text,
        correct_answer=total,
        topic="Numeracy",
        question_type="Pie Charts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L4,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": categories,
                "angles": angles,
                "colors": colors,
                "wedge_labels": wedge_labels,
                "show_legend": True,
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 5 — Calculating Angles from a Frequency Table
# ---------------------------------------------------------------------------

_L5_TOTALS = [12, 15, 18, 20, 24, 30, 36, 40, 45, 60]


def generate_pie_charts_l5():
    context, all_categories = random.choice(_L1_SCENARIOS)
    n = random.choice([3, 4])
    categories = random.sample(all_categories, n)
    total = random.choice(_L5_TOTALS)
    per_unit = 360 // total
    frequencies = _split_degrees(total, n)
    angles = [f * per_unit for f in frequencies]

    target_idx = random.randrange(n)
    target_category = categories[target_idx]
    target_angle = angles[target_idx]

    question_text = (
        f"{context}. The table above shows the results.\n\n"
        f"Calculate the angle needed to represent each category in a pie chart.\n\n"
        f"**Enter your answer for {target_category} in the box below.**"
    )

    scaffold_steps = []
    for cat, freq, ang in zip(categories, frequencies, angles):
        g = math.gcd(freq, total)
        n_, d_ = freq // g, total // g
        frac_str = f"{n_}/{d_}"
        scaffold_steps.append({
            "prompt": f"{cat}: what fraction of the total is this ({freq} ÷ {total}, simplified)?",
            "answer": frac_str,
        })
        scaffold_steps.append({
            "prompt": f"{cat}: what angle represents this fraction (fraction × 360)?",
            "answer": ang,
        })

    worked = [f"Total = {' + '.join(str(f) for f in frequencies)} = {total}"]
    for cat, freq, ang in zip(categories, frequencies, angles):
        worked.append(f"{cat}: {freq} ÷ {total} × 360 = {ang}°")
    worked.append(f"Check: {' + '.join(str(a) for a in angles)} = {sum(angles)}° ✓")

    return Question(
        question_text=question_text,
        correct_answer=target_angle,
        topic="Numeracy",
        question_type="Pie Charts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_L5,
        metadata={
            "table": _freq_table_md(categories, frequencies),
            "diagram": "frequency_table_angles",
            "diagram_params": {
                "categories": categories,
                "frequencies": frequencies,
                "angles": angles,
            },
        },
    )


def generate_pie_charts_question():
    return random.choice([
        generate_pie_charts_l1,
        generate_pie_charts_l2,
        generate_pie_charts_l3,
        generate_pie_charts_l4,
        generate_pie_charts_l5,
    ])()
