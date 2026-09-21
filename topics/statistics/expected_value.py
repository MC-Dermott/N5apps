import random

from core.models.question_model import Question

NOTES = """
**Risk and Expected Value:**

**Expected cost = P(event) × cost of the event**

- **Complementary probability:** P(event) = 1 − P(not event)
- **Independent risks:** if a delay can only be caused by risk A or risk B, and the two
  are independent, P(no delay) = P(no A) × P(no B)
- **Control measures:** if a measure removes one risk entirely (at a fixed cost), the
  delay can now only be caused by the *other* risk, so

  **Total expected cost = cost of the measure + (probability of the remaining risk × penalty)**

- Compare the total expected cost of each option (including doing nothing) and choose
  the one that minimises it.

**Example:**
A firm faces a £10,000 penalty if a delivery is delayed. P(delay) = 0.2.
Expected cost = 0.2 × £10,000 = **£2,000**
"""

_SCENARIOS = [
    {"subject": "a haulage firm", "event": "delivery", "verb": "delayed", "penalty": "penalty"},
    {"subject": "a construction company", "event": "build", "verb": "delayed", "penalty": "penalty"},
    {"subject": "a ferry operator", "event": "sailing", "verb": "cancelled", "penalty": "loss"},
    {"subject": "an events company", "event": "festival stage build", "verb": "delayed", "penalty": "penalty"},
    {"subject": "a fish farm", "event": "harvest", "verb": "delayed", "penalty": "loss"},
    {"subject": "a distillery", "event": "cask shipment", "verb": "delayed", "penalty": "penalty"},
    {"subject": "a wind farm developer", "event": "grid connection", "verb": "delayed", "penalty": "penalty"},
    {"subject": "a software company", "event": "product launch", "verb": "delayed", "penalty": "penalty"},
]

_RISK_PAIRS = [
    ("a supplier failing to deliver on time", "a key member of staff being unavailable"),
    ("bad weather halting outdoor work", "a piece of equipment failing"),
    ("a permit or licence being delayed", "a contractor missing a deadline"),
    ("a transport breakdown", "a shortage of materials"),
    ("a technical fault being found during testing", "a delay at customs or a border check"),
]


def _r2(x):
    return round(x, 2)


def generate_expected_value_l1():
    """Expected cost of a single risk — includes the complementary-probability step about
    half the time, matching worksheet Sections 1-2."""
    scenario = random.choice(_SCENARIOS)
    penalty = random.choice(range(2000, 40000, 500))
    give_complement = random.choice([True, False])
    p_event = _r2(random.randint(5, 35) / 100)

    if give_complement:
        p_no_event = _r2(1 - p_event)
        question_text = (
            f"{scenario['subject'].capitalize()} faces a £{penalty:,} {scenario['penalty']} if "
            f"a {scenario['event']} is {scenario['verb']}. The probability that it is NOT "
            f"{scenario['verb']} is {p_no_event}. Calculate the expected cost of a "
            f"{scenario['verb']} {scenario['event']}."
        )
        scaffold_steps = [
            {"prompt": f"P({scenario['verb']}) = 1 − P(not {scenario['verb']})", "answer": p_event},
            {"prompt": "Expected cost = P(event) × cost", "answer": _r2(p_event * penalty)},
        ]
        worked = [
            f"P({scenario['verb']}) = 1 − {p_no_event} = {p_event}",
            f"Expected cost = {p_event} × £{penalty:,} = £{_r2(p_event * penalty):,.2f}",
        ]
    else:
        question_text = (
            f"{scenario['subject'].capitalize()} faces a £{penalty:,} {scenario['penalty']} if "
            f"a {scenario['event']} is {scenario['verb']}. The probability of this happening is "
            f"{p_event}. Calculate the expected cost."
        )
        scaffold_steps = [
            {"prompt": "Expected cost = P(event) × cost", "answer": _r2(p_event * penalty)},
        ]
        worked = [
            f"Expected cost = {p_event} × £{penalty:,} = £{_r2(p_event * penalty):,.2f}",
        ]

    return Question(
        question_text=question_text,
        correct_answer=_r2(p_event * penalty),
        topic="Planning",
        question_type="Risk and Expected Value",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_expected_value_l2():
    """Combining two independent risks, then finding the expected cost — matches worksheet
    Section 3."""
    scenario = random.choice(_SCENARIOS)
    risk_a, risk_b = random.choice(_RISK_PAIRS)
    penalty = random.choice(range(3000, 60000, 500))
    p_no_a = _r2(random.randint(80, 97) / 100)
    p_no_b = _r2(random.randint(80, 97) / 100)
    p_no_event = _r2(p_no_a * p_no_b)
    p_event = _r2(1 - p_no_event)
    expected_cost = _r2(p_event * penalty)

    question_text = (
        f"{scenario['subject'].capitalize()} faces a £{penalty:,} {scenario['penalty']} if a "
        f"{scenario['event']} is {scenario['verb']}. The {scenario['event']} can only be "
        f"{scenario['verb']} by {risk_a}, or by {risk_b} — these two risks are independent.\n\n"
        f"The probability of no delay from the first risk ({risk_a}) is {p_no_a}. The "
        f"probability of no delay from the second risk ({risk_b}) is {p_no_b}.\n\n"
        f"Calculate the expected cost of a {scenario['verb']} {scenario['event']}."
    )

    scaffold_steps = [
        {"prompt": "P(no delay) = P(no risk A) × P(no risk B)", "answer": p_no_event},
        {"prompt": "P(delay) = 1 − P(no delay)", "answer": p_event},
        {"prompt": "Expected cost = P(delay) × cost", "answer": expected_cost},
    ]
    event_noun = "cancellation" if scenario["verb"] == "cancelled" else "delay"
    worked = [
        f"P(no {event_noun}) = {p_no_a} × {p_no_b} = {p_no_event}",
        f"P({event_noun}) = 1 − {p_no_event} = {p_event}",
        f"Expected cost = {p_event} × £{penalty:,} = £{expected_cost:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=expected_cost,
        topic="Planning",
        question_type="Risk and Expected Value",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_expected_value_l3():
    """Full cost-benefit capstone: expected cost before any control measure, the total
    expected cost under each of two control measures (each eliminating one risk), and which
    to choose — matches worksheet Section 5 / the target exam-style question."""
    scenario = random.choice(_SCENARIOS)
    risk_a, risk_b = random.choice(_RISK_PAIRS)
    penalty = random.choice(range(8000, 100000, 1000))
    p_a = _r2(random.randint(5, 25) / 100)  # P(risk A causes the event)
    p_b = _r2(random.randint(5, 25) / 100)  # P(risk B causes the event)
    p_no_event = _r2((1 - p_a) * (1 - p_b))
    p_event = _r2(1 - p_no_event)

    cost1 = random.choice(range(500, 5000, 100))  # eliminates risk A
    cost2 = random.choice(range(500, 5000, 100))  # eliminates risk B

    base_cost = _r2(p_event * penalty)
    cm1_total = _r2(cost1 + p_b * penalty)
    cm2_total = _r2(cost2 + p_a * penalty)

    if cm1_total <= cm2_total:
        chosen, chosen_cost = "Control Measure 1", cm1_total
    else:
        chosen, chosen_cost = "Control Measure 2", cm2_total

    question_text = (
        f"{scenario['subject'].capitalize()} faces a £{penalty:,} {scenario['penalty']} if a "
        f"{scenario['event']} is {scenario['verb']}. For the purposes of a cost-benefit "
        f"analysis, only two events are assumed to cause a {scenario['verb']} {scenario['event']}: "
        f"{risk_a}, or {risk_b}.\n\n"
        f"The probability of no {scenario['verb']} {scenario['event']} is {p_no_event}.\n\n"
        f"(a) Calculate the expected cost of a {scenario['verb']} {scenario['event']} before any "
        f"control measures are applied.\n\n"
        f"Two control measures are being considered:\n"
        f"Control Measure 1 — at a cost of £{cost1:,}, eliminates the risk of {risk_a} entirely.\n"
        f"Control Measure 2 — at a cost of £{cost2:,}, eliminates the risk of {risk_b} entirely.\n"
        f"The probability of {risk_a} is {p_a}. The probability of {risk_b} is {p_b}.\n\n"
        f"(b) Calculate the total expected cost (control measure cost plus remaining expected "
        f"penalty) if the company uses: (i) Control Measure 1, (ii) Control Measure 2.\n\n"
        f"The company will only use one control measure.\n\n"
        f"(c) State which control measure minimises the total expected cost."
    )

    scaffold_steps = [
        {"prompt": "(a) P(delay) = 1 − P(no delay)", "answer": p_event},
        {"prompt": "(a) Expected cost before any control measure = P(delay) × penalty",
         "answer": base_cost},
        {"prompt": "(b)(i) Control Measure 1 eliminates risk A — the remaining risk is B. "
                    "Total expected cost = cost of measure + (P(risk B) × penalty)",
         "answer": cm1_total},
        {"prompt": "(b)(ii) Control Measure 2 eliminates risk B — the remaining risk is A. "
                    "Total expected cost = cost of measure + (P(risk A) × penalty)",
         "answer": cm2_total},
        {"prompt": "(c) Which control measure gives the lower total expected cost?",
         "answer": chosen},
    ]
    worked = [
        f"(a) P(delay) = 1 − {p_no_event} = {p_event}. "
        f"Expected cost = {p_event} × £{penalty:,} = £{base_cost:,.2f}",
        f"(b)(i) Control Measure 1: £{cost1:,} + ({p_b} × £{penalty:,}) "
        f"= £{cost1:,} + £{_r2(p_b * penalty):,.2f} = £{cm1_total:,.2f}",
        f"(b)(ii) Control Measure 2: £{cost2:,} + ({p_a} × £{penalty:,}) "
        f"= £{cost2:,} + £{_r2(p_a * penalty):,.2f} = £{cm2_total:,.2f}",
        f"(c) {chosen} should be used, since its total expected cost (£{chosen_cost:,.2f}) is "
        f"the lower of the two.",
    ]

    return Question(
        question_text=question_text,
        correct_answer=chosen_cost,
        topic="Planning",
        question_type="Risk and Expected Value",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_expected_value_question():
    return random.choice([
        generate_expected_value_l1,
        generate_expected_value_l2,
        generate_expected_value_l3,
    ])()
