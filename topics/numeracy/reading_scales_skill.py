import random
from decimal import Decimal

from core.models.question_model import Question

NOTES = """
**Reading a Scale:**

1. Look at two **numbered** marks next to each other and find the difference between them.
2. Count the **number of gaps** between those two marks.
3. **Divide** the difference by the number of gaps — that is what **one small gap** is worth.
4. Start at the nearest numbered mark and count on (or back) in small gaps to the arrow.
   If the arrow is between marks, give the **nearest marked division**.

**Example:** The scale is numbered 0, 10, 20 … with 5 gaps between each number.
- One small gap = 10 ÷ 5 = 2
- The arrow is 3 gaps past 20, so the reading is 20 + 3 × 2 = **26**
"""

_DIAG = "topics.numeracy.core_skills_diagrams"

# (major step, gaps between numbers, unit)
_SCALES = [
    (10, 5, ""), (10, 10, ""), (20, 4, ""), (50, 5, "ml"), (100, 5, "ml"), (100, 10, "g"),
    (0.5, 5, "litres"), (1, 10, "kg"), (1, 5, "cm"), (10, 5, "°C"), (5, 5, "mm"), (20, 5, "g"),
]


def _fmt(x):
    return format(float(x), "g")


def _build(level_gaps=None):
    major, gaps, unit = random.choice([s for s in _SCALES if level_gaps is None or s[1] in level_gaps])
    minor = Decimal(str(major)) / gaps
    n_major = random.randint(3, 6)
    lo = 0
    hi = Decimal(str(major)) * n_major
    marker_idx = random.choice([i for i in range(1, n_major * gaps) if i % gaps])
    marker = minor * marker_idx
    below = (marker_idx // gaps)
    past = marker_idx % gaps
    return major, gaps, unit, minor, lo, hi, marker, below, past


def _question(level_gaps, ask_gap):
    major, gaps, unit, minor, lo, hi, marker, below, past = _build(level_gaps)
    u = f" {unit}" if unit else ""
    base = Decimal(str(major)) * below
    diagram = {"diagram": "composite_shape", "diagram_params": {
        "module_path": _DIAG, "kind": "scale", "width": 560,
        "args": [lo, float(hi), float(major), float(minor), float(marker), unit]}}
    sim = {"simulation": "scale_stepper", "simulation_params": {
        "min_value": lo, "max_value": float(hi), "major_step": float(major),
        "minor_step": float(minor), "marker_value": float(marker), "unit_label": unit}}
    scaffold = [
        {"prompt": f"How many small gaps are there between two numbered marks (e.g. between "
                   f"{_fmt(base)} and {_fmt(base + Decimal(str(major)))})?", "answer": gaps},
        {"prompt": f"What is the value of one small gap? ({_fmt(major)} ÷ {gaps})", "answer": float(minor)},
        {"prompt": f"The arrow is {past} gap{'s' if past > 1 else ''} past {_fmt(base)}. "
                   f"What is the reading?", "answer": float(marker)},
    ]
    worked = [
        f"{gaps} small gaps between {_fmt(base)} and {_fmt(base + Decimal(str(major)))}, "
        f"so one gap = {_fmt(major)} ÷ {gaps} = {_fmt(minor)}{u}",
        f"The arrow is {past} gap{'s' if past > 1 else ''} past {_fmt(base)}: "
        f"{_fmt(base)} + {past} × {_fmt(minor)} = **{_fmt(marker)}{u}**",
    ]
    meta = {**diagram, **sim}
    if ask_gap:
        return Question(
            question_text=f"What is the value of **one small gap** on this scale{(' (in ' + unit + ')') if unit else ''}?",
            correct_answer=float(minor), topic="Numeracy", question_type="Reading Scales",
            scaffold_steps=scaffold[:2], worked_solution=worked[:1] + [f"One small gap = **{_fmt(minor)}{u}**"],
            notes=NOTES, metadata=meta)
    return Question(
        question_text=f"What reading does the arrow point to?{(' Give your answer in ' + unit + '.') if unit else ''}",
        correct_answer=float(marker), topic="Numeracy", question_type="Reading Scales",
        scaffold_steps=scaffold, worked_solution=worked, notes=NOTES, metadata=meta)


def generate_reading_scales_l1():
    return _question((5, 10), ask_gap=True)


def generate_reading_scales_l2():
    return _question(None, ask_gap=False)


def generate_reading_scales_question():
    return random.choice([generate_reading_scales_l1, generate_reading_scales_l2])()
