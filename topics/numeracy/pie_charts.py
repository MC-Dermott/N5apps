import math
import random

from core.models.question_model import Question

NOTES = """
**Reading Pie Charts**

There are 360° in a full circle — a sector's angle is always a fraction of 360°.

**Fraction represented by a sector:**
Fraction = sector angle ÷ 360

**Finding a missing angle:**
Missing angle = 360 − (sum of the angles you already know)

**Finding an amount from an angle and a total:**
Amount = (sector angle ÷ 360) × total

**Finding another segment (or the total) from one known segment:**
Value per degree = known value ÷ known angle
Other segment's value = other angle × value per degree
Total = 360 × value per degree
"""

_WEDGE_BLUE = "#5b9bd5"
_WEDGE_ORANGE = "#ed7d31"
_WEDGE_GREEN = "#70ad47"
_WEDGE_GREY = "#d9d9d9"

# ---------------------------------------------------------------------------
# Level 1 — Fraction from the Angle
# ---------------------------------------------------------------------------

_L1_ANGLES = [24, 30, 36, 40, 45, 60, 72, 90, 120, 135, 144, 150, 160, 180, 200, 210, 225, 240, 270, 300]

_L1_CONTEXTS = [
    ("A survey of S1 pupils at Sir E Scott School asked how they travel to school", "By minibus"),
    ("A survey of Tarbert fishermen recorded which species they landed most last week", "Langoustine"),
    ("A survey of Harris Tweed mill workers asked their favourite pattern", "Herringbone"),
    ("A survey of Scalpay crofters recorded which animals they keep", "Sheep"),
    ("A survey of Leverburgh ceilidh-goers asked their favourite dance", "Strip the Willow"),
    ("A survey of CalMac passengers on the Uig crossing asked how they were travelling", "On foot"),
    ("A survey of Ness households recorded how they heat their home", "Peat"),
    ("A survey of Stornoway pupils asked their favourite subject", "Art"),
    ("A survey of Berneray pupils asked their favourite ceilidh dance", "Eightsome Reel"),
    ("A survey of Uig crofters recorded their main occupation", "Fishing"),
]


def generate_pie_charts_l1():
    angle = random.choice(_L1_ANGLES)
    context, category = random.choice(_L1_CONTEXTS)
    g = math.gcd(angle, 360)
    n, d = angle // g, 360 // g
    answer_str = f"{n}/{d}"

    question_text = (
        f"{context}. The pie chart above shows the results.\n\n"
        f"The **{category}** segment has an angle of **{angle}°**.\n\n"
        f"Write the **{category}** segment as a fraction of the whole pie chart, in its "
        f"simplest form."
    )

    worked = [
        f"Fraction = {angle} ÷ 360",
        f"= {answer_str} (dividing both numbers by {g})",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer_str,
        topic="Numeracy",
        question_type="Pie Charts",
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": [category, "Rest"],
                "angles": [angle, 360 - angle],
                "colors": [_WEDGE_BLUE, _WEDGE_GREY],
                "wedge_labels": [f"{angle}°", ""],
                "show_labels": False,
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

    question_text = (
        f"{context}. The pie chart above shows: **{cat1}**: {a1}°, **{cat2}**: {a2}°, "
        f"and **{cat3}**: **?**.\n\n"
        f"(a) Work out the missing angle marked '?'.\n\n"
        f"(b) Write **{cat3}** as a fraction of the whole pie chart, in its simplest form."
    )

    scaffold_steps = [
        {"prompt": f"Missing angle = 360 − {a1} − {a2}", "answer": missing},
        {"prompt": f"Fraction = {missing} ÷ 360, simplified", "answer": fraction_str},
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
        notes=NOTES,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": [cat1, cat2, cat3],
                "angles": [a1, a2, missing],
                "colors": [_WEDGE_BLUE, _WEDGE_ORANGE, _WEDGE_GREY],
                "wedge_labels": [f"{a1}°", f"{a2}°", "?"],
                "show_labels": False,
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 3 — Calculating the Amount
# ---------------------------------------------------------------------------

_L3_SCENARIOS = [
    {
        "context": "A weekly household budget of £{total} on Scalpay. This segment shows spending on petrol.",
        "category": "petrol", "unit": "£", "angle": 72,
        "totals": [100, 150, 200, 250, 300],
    },
    {
        "context": "The {total}-minute school day at Sir E Scott School, by activity. This segment shows PE.",
        "category": "PE", "unit": "minutes", "angle": 60,
        "totals": [360, 420, 480, 540, 600],
    },
    {
        "context": "{total} passengers on a CalMac sailing to Tarbert, by type. This segment shows foot passengers.",
        "category": "foot passengers", "unit": "people", "angle": 90,
        "totals": [120, 160, 200, 240, 280],
    },
    {
        "context": "£{total} raised at the Leverburgh hall fundraiser. This segment shows the raffle.",
        "category": "the raffle", "unit": "£", "angle": 45,
        "totals": [160, 240, 320, 400, 480],
    },
    {
        "context": "{total} people on Harris surveyed about their main occupation. This segment shows crofting.",
        "category": "crofting", "unit": "people", "angle": 40,
        "totals": [90, 180, 270, 360, 450],
    },
    {
        "context": "A {total}-hour working week for a Scalpay fisherman, by task. This segment shows hauling creels.",
        "category": "hauling creels", "unit": "hours", "angle": 120,
        "totals": [36, 45, 54, 63, 72],
    },
]


def generate_pie_charts_l3():
    sc = random.choice(_L3_SCENARIOS)
    total = random.choice(sc["totals"])
    angle = sc["angle"]
    amount = angle * total // 360
    g = math.gcd(angle, 360)
    n, d = angle // g, 360 // g
    fraction_str = f"{n}/{d}"
    unit = sc["unit"]
    context = sc["context"].format(total=total)
    caption = f"Total: £{total}" if unit == "£" else f"Total: {total} {unit}"

    question_text = (
        f"{context}\n\n"
        f"Use the angle of the shaded segment, together with the total given, to calculate the "
        f"amount it represents."
    )

    scaffold_steps = [
        {"prompt": f"Fraction = {angle} ÷ 360, simplified", "answer": fraction_str},
        {"prompt": f"Amount = {fraction_str} × {total}", "answer": amount},
    ]

    amount_str = f"£{amount}" if unit == "£" else f"{amount} {unit}"
    worked = [
        f"Fraction = {angle} ÷ 360 = {fraction_str}",
        f"Amount = {fraction_str} × {total} = {amount_str}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=amount,
        topic="Numeracy",
        question_type="Pie Charts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": [sc["category"], "Rest"],
                "angles": [angle, 360 - angle],
                "colors": [_WEDGE_BLUE, _WEDGE_GREY],
                "wedge_labels": [f"{angle}°", ""],
                "show_labels": False,
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
        "unit": "votes",
    },
    {
        "context": "A Scalpay fisherman's day, split by task.",
        "known": "Baiting creels", "known_angle": 80,
        "target": "Sailing", "target_angle": 40,
        "unit": "minutes",
    },
    {
        "context": "CalMac ferry passengers on the Uig–Lochmaddy crossing, by type.",
        "known": "Car passengers", "known_angle": 150,
        "target": "Foot passengers", "target_angle": 90,
        "unit": "people",
    },
    {
        "context": "Favourite subjects among S3 pupils at Sir E Scott School.",
        "known": "PE", "known_angle": 60,
        "target": "Maths", "target_angle": 120,
        "unit": "pupils",
    },
    {
        "context": "Croft chores on Scalpay over the course of a month.",
        "known": "Feeding sheep", "known_angle": 100,
        "target": "Repairing fences", "target_angle": 50,
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
        f"(b) Find the total represented by the whole pie chart."
    )

    scaffold_steps = [
        {"prompt": f"Value per degree = {known_value} ÷ {sc['known_angle']}", "answer": k},
        {"prompt": f"(a) Value of ? = {sc['target_angle']} × {k}", "answer": target_value},
        {"prompt": f"(b) Total = 360 × {k}", "answer": total},
    ]

    worked = [
        f"Value per degree = {known_value} ÷ {sc['known_angle']} = {k}",
        f"(a) {sc['target']} = {sc['target_angle']} × {k} = {target_value} {unit}",
        f"(b) Total = 360 × {k} = {total} {unit}",
    ]

    rest_angle = 360 - sc["known_angle"] - sc["target_angle"]

    return Question(
        question_text=question_text,
        correct_answer=target_value,
        topic="Numeracy",
        question_type="Pie Charts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": [sc["known"], sc["target"], "Rest"],
                "angles": [sc["known_angle"], sc["target_angle"], rest_angle],
                "colors": [_WEDGE_GREEN, _WEDGE_ORANGE, _WEDGE_GREY],
                "wedge_labels": [f"{sc['known_angle']}°\n({known_value})", f"{sc['target_angle']}°\n?", ""],
                "show_labels": False,
            },
        },
    )


def generate_pie_charts_question():
    return random.choice([
        generate_pie_charts_l1,
        generate_pie_charts_l2,
        generate_pie_charts_l3,
        generate_pie_charts_l4,
    ])()
