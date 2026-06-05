import random
import math
from core.models.question_model import Question

NOTES = """
**Gradient:**

Gradient measures how steep a slope is.

**gradient = vertical rise ÷ horizontal distance**

⚠️ **Units must match** before you divide — convert rise and run to the same unit first.

**Useful conversions:**
- 1 m = 100 cm → divide cm by 100 to get m
- 1 km = 1000 m → multiply km by 1000 to get m
"""

# ---------------------------------------------------------------------------
# Predefined number pairs that give clean gradient answers after unit conversion
# ---------------------------------------------------------------------------

# (rise_cm, run_m) → gradient = rise_cm / (100 × run_m)
_CM_M_PAIRS = [
    (30,  6), (25,  5), (40,  8), (50,  4), (20,  8),
    (15,  6), (10,  4), (60,  4), (75,  5), (50, 10),
    (80,  5), (45,  9), (36,  9), (24,  6), (48,  8),
]

# (rise_m, run_km) → gradient = rise_m / (run_km × 1000)
_M_KM_PAIRS = [
    ( 50, 2), ( 80, 4), (100, 2), (150, 3), ( 60, 3),
    ( 75, 3), (120, 4), (200, 5), ( 40, 2), ( 90, 3),
    (100, 5), (160, 4), (120, 6), (180, 6), (250, 5),
]

_CM_M_CONTEXTS = [
    ("ramp",     "A ramp"),
    ("path",     "A path"),
    ("driveway", "A driveway"),
    ("slope",    "A slope"),
]

_M_KM_CONTEXTS = [
    ("road",          "A road"),
    ("hillside path", "A hillside path"),
    ("railway line",  "A railway line"),
    ("hill track",    "A hill track"),
]

_PLACES = [
    "Aviemore",    "Pitlochry",    "Callander",   "Dunkeld",     "Braemar",
    "Aberfeldy",   "Killin",       "Crianlarich", "Tyndrum",     "Glencoe",
    "Kinlochleven","Spean Bridge", "Newtonmore",  "Kingussie",   "Carrbridge",
    "Tomintoul",   "Blairgowrie",  "Comrie",      "Balquhidder", "Strathyre",
    "Ardlui",      "Lochearnhead", "Thornhill",   "Aberfoyle",   "Killearn",
]

# 2dp decimal parts added to heights for realism
_DECIMALS = [0.12, 0.23, 0.34, 0.45, 0.47, 0.56, 0.67, 0.68, 0.78, 0.89]


def _gcd(a, b):
    return math.gcd(int(abs(a)), int(abs(b)))


def _frac_str(num, den):
    g = _gcd(num, den)
    n, d = num // g, den // g
    return str(n) if d == 1 else f"{n}/{d}"


def generate_gradient_question():
    qtype = random.choice(["cm_m_slope", "m_km_slope", "sea_level"])
    return {
        "cm_m_slope": _gradient_cm_m,
        "m_km_slope": _gradient_m_km,
        "sea_level":  _gradient_sea_level,
    }[qtype]()


# ---------------------------------------------------------------------------
# Type 1 — Simple slope: rise in cm, run in m
# ---------------------------------------------------------------------------

def _gradient_cm_m():
    rise_cm, run_m = random.choice(_CM_M_PAIRS)
    rise_m_float = rise_cm / 100
    gradient = rise_cm / (run_m * 100)   # integer division avoids float rounding
    g_frac = _frac_str(rise_cm, run_m * 100)

    noun, subject = random.choice(_CM_M_CONTEXTS)

    question_text = (
        f"{subject} rises {rise_cm} cm over a horizontal distance of {run_m} m. "
        f"Calculate the gradient of the {noun}."
    )

    scaffold_steps = [
        {
            "prompt": "Convert the rise to metres",
            "answer": rise_m_float,
        },
        {
            "prompt": "Calculate the gradient (rise ÷ run)",
            "answer": gradient,
        },
    ]

    worked = [
        f"Convert rise: {rise_cm} cm ÷ 100 = {rise_m_float:g} m",
        "gradient = vertical rise ÷ horizontal distance",
        f"gradient = {rise_m_float:g} ÷ {run_m}",
        f"gradient = {g_frac} = {gradient:g}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=gradient,
        topic="Geometry and Measure",
        question_type="Gradient",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Type 2 — Simple slope: rise in m, run in km
# ---------------------------------------------------------------------------

def _gradient_m_km():
    rise_m, run_km = random.choice(_M_KM_PAIRS)
    run_m = run_km * 1000
    gradient = rise_m / run_m
    g_frac = _frac_str(rise_m, run_m)

    noun, subject = random.choice(_M_KM_CONTEXTS)

    question_text = (
        f"{subject} rises {rise_m} m over a horizontal distance of {run_km} km. "
        f"Calculate the gradient of the {noun}."
    )

    scaffold_steps = [
        {
            "prompt": "Convert the horizontal distance to metres",
            "answer": float(run_m),
        },
        {
            "prompt": "Calculate the gradient (rise ÷ run)",
            "answer": gradient,
        },
    ]

    worked = [
        f"Convert run: {run_km} km × 1000 = {run_m} m",
        "gradient = vertical rise ÷ horizontal distance",
        f"gradient = {rise_m} ÷ {run_m}",
        f"gradient = {g_frac} = {gradient:g}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=gradient,
        topic="Geometry and Measure",
        question_type="Gradient",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Type 3 — Height above sea level word problem
# ---------------------------------------------------------------------------

def _gradient_sea_level():
    rise_m, run_km = random.choice(_M_KM_PAIRS)
    run_m = run_km * 1000
    gradient = rise_m / run_m
    g_frac = _frac_str(rise_m, run_m)

    place_a, place_b = random.sample(_PLACES, 2)

    base_a = random.randint(80, 350)
    decimal = random.choice(_DECIMALS)
    height_a = round(base_a + decimal, 2)
    height_b = round(height_a + rise_m, 2)

    question_text = (
        f"{place_a} is {height_a:.2f} m above sea level. "
        f"{place_b} is {height_b:.2f} m above sea level. "
        f"The horizontal distance between them is {run_km} km. "
        f"Calculate the gradient of the road between {place_a} and {place_b}."
    )

    scaffold_steps = [
        {
            "prompt": "Find the difference in height",
            "answer": float(rise_m),
        },
        {
            "prompt": "Convert the horizontal distance to metres",
            "answer": float(run_m),
        },
        {
            "prompt": "Calculate the gradient (rise ÷ run)",
            "answer": gradient,
        },
    ]

    worked = [
        f"Rise = {height_b:.2f} − {height_a:.2f} = {rise_m} m",
        f"Horizontal distance = {run_km} km × 1000 = {run_m} m",
        "gradient = vertical rise ÷ horizontal distance",
        f"gradient = {rise_m} ÷ {run_m}",
        f"gradient = {g_frac} = {gradient:g}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=gradient,
        topic="Geometry and Measure",
        question_type="Gradient",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
