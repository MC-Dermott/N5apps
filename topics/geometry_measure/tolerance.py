import random
from core.models.question_model import Question

_NAMES = [
    "Callum", "Eilidh", "Fraser", "Catriona", "Morag", "Alasdair",
    "David", "Sarah", "Michael", "Emma", "James", "Laura", "Andrew", "Rachel",
]

# ---------------------------------------------------------------------------
# Contexts
# ---------------------------------------------------------------------------

# measurement_phrase is a format string using {target} and {unit}
_L1_CONTEXTS = [
    {"items": "metal rods",      "setting": "a factory",
     "measure": "lengths",       "measurement_phrase": "measured {target} {unit}",
     "adj": "acceptable",
     "unit": "cm",
     "targets": [45.0, 48.0, 50.0, 52.0, 55.0, 60.0],
     "tols":   [0.5, 0.8, 1.0, 1.5, 2.0]},

    {"items": "bolts",           "setting": "a machine shop",
     "measure": "diameters",     "measurement_phrase": "had a diameter of {target} {unit}",
     "adj": "within specification",
     "unit": "mm",
     "targets": [8.0, 10.0, 12.0, 14.0, 16.0, 20.0],
     "tols":   [0.2, 0.3, 0.4, 0.5]},

    {"items": "steel pins",      "setting": "an engineering workshop",
     "measure": "lengths",       "measurement_phrase": "measured {target} {unit}",
     "adj": "acceptable",
     "unit": "mm",
     "targets": [30.0, 35.0, 40.0, 45.0, 50.0],
     "tols":   [0.5, 0.8, 1.0, 1.5]},

    {"items": "ceramic tiles",   "setting": "a tile manufacturer",
     "measure": "widths",        "measurement_phrase": "measured {target} {unit}",
     "adj": "acceptable",
     "unit": "mm",
     "targets": [150.0, 200.0, 250.0, 300.0],
     "tols":   [1.0, 1.5, 2.0, 3.0]},

    {"items": "wooden planks",   "setting": "a DIY store",
     "measure": "lengths",       "measurement_phrase": "measured {target} {unit}",
     "adj": "acceptable",
     "unit": "cm",
     "targets": [90.0, 100.0, 120.0, 150.0],
     "tols":   [0.5, 1.0, 1.5, 2.0]},

    {"items": "glass panes",     "setting": "a glazier",
     "measure": "widths",        "measurement_phrase": "measured {target} {unit}",
     "adj": "acceptable",
     "unit": "cm",
     "targets": [40.0, 45.0, 50.0, 60.0, 75.0],
     "tols":   [0.3, 0.5, 0.8, 1.0]},
]

_L2_CONTEXTS = [
    {"items": "wooden planks",   "setting": "a timber yard",
     "measure": "lengths",       "measurement_phrase": "measured {target} {target_unit}",
     "adj": "acceptable",
     "target_unit": "m", "tol_unit": "cm", "factor": 0.01,
     "targets": [1.2, 1.5, 1.8, 2.0, 2.5],
     "tols":   [3, 5, 8, 10]},

    {"items": "steel girders",   "setting": "a warehouse",
     "measure": "lengths",       "measurement_phrase": "measured {target} {target_unit}",
     "adj": "acceptable",
     "target_unit": "m", "tol_unit": "cm", "factor": 0.01,
     "targets": [3.0, 3.5, 4.0, 4.5, 5.0],
     "tols":   [5, 8, 10, 12]},

    {"items": "water bottles",   "setting": "a bottling plant",
     "measure": "volumes",       "measurement_phrase": "held {target} {target_unit}",
     "adj": "within specification",
     "target_unit": "litres", "tol_unit": "ml", "factor": 0.001,
     "targets": [0.50, 0.75, 1.00, 1.50, 2.00],
     "tols":   [15, 20, 25, 30]},

    {"items": "copper pipes",    "setting": "a plumbing supplier",
     "measure": "lengths",       "measurement_phrase": "measured {target} {target_unit}",
     "adj": "acceptable",
     "target_unit": "m", "tol_unit": "mm", "factor": 0.001,
     "targets": [0.5, 0.8, 1.0, 1.2, 1.5],
     "tols":   [5, 8, 10, 15]},

    {"items": "wire cables",     "setting": "an electrical warehouse",
     "measure": "lengths",       "measurement_phrase": "measured {target} {target_unit}",
     "adj": "acceptable",
     "target_unit": "m", "tol_unit": "cm", "factor": 0.01,
     "targets": [2.0, 2.5, 3.0, 3.5, 4.0],
     "tols":   [3, 4, 5, 8]},

    {"items": "fabric rolls",    "setting": "a textile factory",
     "measure": "widths",        "measurement_phrase": "measured {target} {target_unit}",
     "adj": "acceptable",
     "target_unit": "m", "tol_unit": "cm", "factor": 0.01,
     "targets": [0.90, 1.00, 1.20, 1.50],
     "tols":   [2, 3, 4, 5]},
]

_L3_CONTEXTS = [
    {"items": "fire extinguishers", "setting": "a local business",
     "measure": "weights",          "measurement_phrase": "weighed {target} {unit}",
     "adj": "safe",
     "unit": "kg",
     "targets": [8.0, 9.0, 10.0, 10.4, 12.0, 15.0],
     "pcts":   [5, 8, 10, 12, 15]},

    {"items": "batteries",       "setting": "an electronics factory",
     "measure": "voltages",      "measurement_phrase": "had a voltage of {target} {unit}",
     "adj": "acceptable",
     "unit": "V",
     "targets": [9.0, 12.0, 14.4, 24.0],
     "pcts":   [3, 5, 8, 10]},

    {"items": "ball bearings",   "setting": "an engineering company",
     "measure": "diameters",     "measurement_phrase": "had a diameter of {target} {unit}",
     "adj": "within specification",
     "unit": "mm",
     "targets": [5.0, 6.0, 8.0, 10.0, 12.0, 15.0],
     "pcts":   [2, 3, 5, 8, 10]},

    {"items": "metal springs",   "setting": "a manufacturing plant",
     "measure": "lengths",       "measurement_phrase": "measured {target} {unit}",
     "adj": "acceptable",
     "unit": "mm",
     "targets": [20.0, 25.0, 30.0, 35.0, 40.0],
     "pcts":   [5, 8, 10, 12]},

    {"items": "resistors",       "setting": "an electronics factory",
     "measure": "resistances",   "measurement_phrase": "had a resistance of {target} {unit}",
     "adj": "within specification",
     "unit": "Ω",
     "targets": [100.0, 150.0, 220.0, 330.0, 470.0],
     "pcts":   [5, 10, 15, 20]},

    {"items": "medicine capsules", "setting": "a pharmaceutical company",
     "measure": "weights",        "measurement_phrase": "weighed {target} {unit}",
     "adj": "within specification",
     "unit": "mg",
     "targets": [100.0, 200.0, 250.0, 500.0],
     "pcts":   [3, 5, 8, 10]},
]

_NOTES = """\
**Tolerance:**

A tolerance defines the acceptable range around a target measurement.

**Absolute tolerance (± value):**
- Minimum = target − tolerance
- Maximum = target + tolerance

**Percentage tolerance (± %):**
- Minimum = target × (1 − rate/100)
- Maximum = target × (1 + rate/100)

**Level 2 — mixed units:**
Convert the tolerance to the same unit as the measurements before calculating min/max.

**Finding the fraction:**
Count how many measurements fall within [minimum, maximum], then write as a fraction:
  fraction = (number within range) ÷ (total measurements)
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _gen_measurements(target, lo, hi, n_total, n_pass, decimals=2):
    """Return a shuffled list of n_total measurements: n_pass inside (lo, hi), rest outside."""
    tol = (hi - lo) / 2
    inside, outside = [], []

    attempts = 0
    while len(inside) < n_pass and attempts < 500:
        attempts += 1
        frac = random.uniform(0.05, 0.85)
        sign = random.choice([-1, 1])
        v = round(target + sign * frac * tol, decimals)
        if lo < v < hi and v not in inside:
            inside.append(v)

    attempts = 0
    while len(outside) < n_total - n_pass and attempts < 500:
        attempts += 1
        frac = random.uniform(1.1, 2.2)
        sign = random.choice([-1, 1])
        v = round(target + sign * frac * tol, decimals)
        if (v < lo or v > hi) and v > 0 and v not in outside and v not in inside:
            outside.append(v)

    result = inside + outside
    random.shuffle(result)
    return result


def _ask_acceptable():
    """Randomly decide whether to ask for fraction acceptable or not acceptable."""
    return random.choice([True, False])


def _fraction_text(acceptable, adj):
    if acceptable:
        return f"were considered {adj}"
    else:
        return f"were not considered {adj}"


def _format_measurements(meas):
    return ", ".join(f"{m:g}" if m == int(m) else str(m) for m in meas)


# ---------------------------------------------------------------------------
# Level 1 — absolute tolerance, same units
# ---------------------------------------------------------------------------

def generate_tolerance_l1():
    ctx    = random.choice(_L1_CONTEXTS)
    target = random.choice(ctx["targets"])
    tol    = random.choice(ctx["tols"])
    lo     = round(target - tol, 2)
    hi     = round(target + tol, 2)
    name   = random.choice(_NAMES)
    unit   = ctx["unit"]
    adj    = ctx["adj"]

    n_total = random.randint(5, 8)
    n_pass  = random.randint(1, n_total - 1)
    meas    = _gen_measurements(target, lo, hi, n_total, n_pass)

    ask_acc = _ask_acceptable()
    frac_count = n_pass if ask_acc else n_total - n_pass
    correct    = frac_count / n_total
    frac_text  = _fraction_text(ask_acc, adj)

    meas_phrase = ctx["measurement_phrase"].format(target=target, unit=unit)
    meas_list   = _format_measurements(meas)

    question_text = (
        f"{name} inspected the {ctx['items']} at {ctx['setting']}.\n\n"
        f"The {ctx['items']} were considered {adj} if they {meas_phrase} ± {tol} {unit}.\n\n"
        f"The {ctx['measure']}, in {unit}, of the {ctx['items']} inspected are shown.\n\n"
        f"{meas_list}\n\n"
        f"Calculate the maximum and minimum {adj} {ctx['measure']} and determine "
        f"the fraction that {frac_text}."
    )

    scaffold_steps = [
        {"prompt": f"Calculate the minimum {adj} {ctx['measure'][:-1] if ctx['measure'].endswith('s') else ctx['measure']} "
                   f"(target − tolerance)",
         "answer": float(lo)},
        {"prompt": f"Calculate the maximum {adj} {ctx['measure'][:-1] if ctx['measure'].endswith('s') else ctx['measure']} "
                   f"(target + tolerance)",
         "answer": float(hi)},
        {"prompt": f"Count how many measurements {frac_text} (i.e. fall {'within' if ask_acc else 'outside'} "
                   f"the range £{lo} to £{hi})".replace("£", ""),
         "answer": float(frac_count)},
        {"prompt": f"Write the fraction that {frac_text} (count ÷ total)",
         "answer": float(correct)},
    ]

    worked = [
        f"Minimum = {target} − {tol} = {lo} {unit}",
        f"Maximum = {target} + {tol} = {hi} {unit}",
        f"Measurements within range: " +
        ", ".join(str(m) for m in sorted(meas) if lo <= m <= hi) +
        f" → {n_pass} out of {n_total}",
        f"Fraction {frac_text} = {frac_count}/{n_total}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(correct),
        topic="Geometry and Measure",
        question_type="Tolerance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_NOTES,
        metadata={},
    )


# ---------------------------------------------------------------------------
# Level 2 — absolute tolerance, different units
# ---------------------------------------------------------------------------

def generate_tolerance_l2():
    ctx         = random.choice(_L2_CONTEXTS)
    target      = random.choice(ctx["targets"])
    tol_raw     = random.choice(ctx["tols"])          # tolerance in tol_unit
    tol_conv    = round(tol_raw * ctx["factor"], 4)   # converted to target_unit
    lo          = round(target - tol_conv, 3)
    hi          = round(target + tol_conv, 3)
    name        = random.choice(_NAMES)
    target_unit = ctx["target_unit"]
    tol_unit    = ctx["tol_unit"]
    adj         = ctx["adj"]

    n_total = random.randint(5, 8)
    n_pass  = random.randint(1, n_total - 1)
    meas    = _gen_measurements(target, lo, hi, n_total, n_pass, decimals=2)

    ask_acc = _ask_acceptable()
    frac_count = n_pass if ask_acc else n_total - n_pass
    correct    = frac_count / n_total
    frac_text  = _fraction_text(ask_acc, adj)

    meas_phrase = ctx["measurement_phrase"].format(target=target, target_unit=target_unit)
    meas_list   = _format_measurements(meas)

    question_text = (
        f"{name} inspected the {ctx['items']} at {ctx['setting']}.\n\n"
        f"The {ctx['items']} were considered {adj} if they {meas_phrase} ± {tol_raw} {tol_unit}.\n\n"
        f"The {ctx['measure']}, in {target_unit}, of the {ctx['items']} inspected are shown.\n\n"
        f"{meas_list}\n\n"
        f"Calculate the maximum and minimum {adj} {ctx['measure']} and determine "
        f"the fraction that {frac_text}."
    )

    # Singular form for step prompts
    measure_singular = ctx["measure"].rstrip("s") if ctx["measure"].endswith("s") else ctx["measure"]

    scaffold_steps = [
        {"prompt": f"Convert the tolerance from {tol_unit} to {target_unit} "
                   f"({tol_raw} {tol_unit} = ? {target_unit})",
         "answer": float(tol_conv)},
        {"prompt": f"Calculate the minimum {adj} {measure_singular} "
                   f"(target − tolerance in {target_unit})",
         "answer": float(lo)},
        {"prompt": f"Calculate the maximum {adj} {measure_singular} "
                   f"(target + tolerance in {target_unit})",
         "answer": float(hi)},
        {"prompt": f"Count how many measurements {frac_text} "
                   f"(fall {'within' if ask_acc else 'outside'} {lo} to {hi} {target_unit})",
         "answer": float(frac_count)},
        {"prompt": f"Write the fraction that {frac_text} (count ÷ total)",
         "answer": float(correct)},
    ]

    worked = [
        f"Convert tolerance: {tol_raw} {tol_unit} = {tol_conv} {target_unit}",
        f"Minimum = {target} − {tol_conv} = {lo} {target_unit}",
        f"Maximum = {target} + {tol_conv} = {hi} {target_unit}",
        f"Measurements within range: " +
        ", ".join(str(m) for m in sorted(meas) if lo <= m <= hi) +
        f" → {n_pass} out of {n_total}",
        f"Fraction {frac_text} = {frac_count}/{n_total}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(correct),
        topic="Geometry and Measure",
        question_type="Tolerance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_NOTES,
        metadata={},
    )


# ---------------------------------------------------------------------------
# Level 3 — percentage tolerance
# ---------------------------------------------------------------------------

def generate_tolerance_l3():
    ctx    = random.choice(_L3_CONTEXTS)
    target = random.choice(ctx["targets"])
    pct    = random.choice(ctx["pcts"])
    rate   = pct / 100
    lo     = round(target * (1 - rate), 2)
    hi     = round(target * (1 + rate), 2)
    name   = random.choice(_NAMES)
    unit   = ctx["unit"]
    adj    = ctx["adj"]

    n_total = random.randint(5, 8)
    n_pass  = random.randint(1, n_total - 1)
    meas    = _gen_measurements(target, lo, hi, n_total, n_pass)

    ask_acc = _ask_acceptable()
    frac_count = n_pass if ask_acc else n_total - n_pass
    correct    = frac_count / n_total
    frac_text  = _fraction_text(ask_acc, adj)

    meas_phrase = ctx["measurement_phrase"].format(target=target, unit=unit)
    meas_list   = _format_measurements(meas)

    question_text = (
        f"{name} inspected the {ctx['items']} at {ctx['setting']}.\n\n"
        f"The {ctx['items']} were considered {adj} if they {meas_phrase} ± {pct}%.\n\n"
        f"The {ctx['measure']}, in {unit}, of the {ctx['items']} inspected are shown.\n\n"
        f"{meas_list}\n\n"
        f"Calculate the maximum and minimum {adj} {ctx['measure']} and determine "
        f"the fraction that {frac_text}."
    )

    measure_singular = ctx["measure"].rstrip("s") if ctx["measure"].endswith("s") else ctx["measure"]

    scaffold_steps = [
        {"prompt": f"Calculate the minimum {adj} {measure_singular}: "
                   f"{target} × (1 − {pct}%)",
         "answer": float(lo)},
        {"prompt": f"Calculate the maximum {adj} {measure_singular}: "
                   f"{target} × (1 + {pct}%)",
         "answer": float(hi)},
        {"prompt": f"Count how many measurements {frac_text} "
                   f"(fall {'within' if ask_acc else 'outside'} {lo} to {hi} {unit})",
         "answer": float(frac_count)},
        {"prompt": f"Write the fraction that {frac_text} (count ÷ total)",
         "answer": float(correct)},
    ]

    worked = [
        f"Minimum = {target} × (1 − {pct}/100) = {target} × {1 - rate} = {lo} {unit}",
        f"Maximum = {target} × (1 + {pct}/100) = {target} × {1 + rate} = {hi} {unit}",
        f"Measurements within range: " +
        ", ".join(str(m) for m in sorted(meas) if lo <= m <= hi) +
        f" → {n_pass} out of {n_total}",
        f"Fraction {frac_text} = {frac_count}/{n_total}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=float(correct),
        topic="Geometry and Measure",
        question_type="Tolerance",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=_NOTES,
        metadata={},
    )


# ---------------------------------------------------------------------------
# Default dispatcher
# ---------------------------------------------------------------------------

def generate_tolerance_question():
    return generate_tolerance_l1()
