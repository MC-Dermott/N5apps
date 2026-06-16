import random
from core.models.question_model import Question

NOTES = """
**Time Zones:**

When a destination is **ahead** of the UK:
1. Convert the arrival time to UK time by *subtracting* the hour difference
2. Calculate the journey duration in UK time

**Example:** Depart 2156 UK, arrive 0314 France time (France = UK + 1 hour)
- 0314 France → 0214 UK
- Journey: 2156 → 0214 (next day) = 4 hours 18 minutes

**Reading Fare Tables:**
- Identify the correct ticket type and price
- Children's discount: usually 80% of adult fare
- Add insurance, credit card fee where stated
"""

# Pre-verified journey scenarios (dep and arr_local in (h, m) tuples)
# duration_str is pre-computed and correct
_JOURNEYS = [
    {
        "from": "Dover (UK)", "to": "France",
        "dep": (21, 56), "arr_local": (3, 14), "tz_ahead": 1,
        "dur_h": 4, "dur_m": 18,
    },
    {
        "from": "Edinburgh (UK)", "to": "Spain",
        "dep": (20, 30), "arr_local": (1, 45), "tz_ahead": 1,
        "dur_h": 4, "dur_m": 15,
    },
    {
        "from": "London (UK)", "to": "Germany",
        "dep": (22, 10), "arr_local": (2, 20), "tz_ahead": 1,
        "dur_h": 3, "dur_m": 10,
    },
    {
        "from": "Glasgow (UK)", "to": "Sweden",
        "dep": (19, 45), "arr_local": (23, 30), "tz_ahead": 1,
        "dur_h": 2, "dur_m": 45,
    },
]

# Fixed fare table (same structure as the original assessment)
_FARE_TABLE = {
    "Standard Non-flexible":           150,
    "Standard Semi-flexible":          160,
    "Standard Premier Non-flexible":   180,
    "Standard Premier Semi-flexible":  190,
    "Business Premier":                250,
}
_CHILD_PCT    = 80    # children pay 80% of adult fare
_INS_ADULT    = 40   # travel insurance per adult
_INS_CHILD    = 20   # travel insurance per child (50% of adult)
_CARD_FEE     = 5    # credit card surcharge (flat, one-off)


def _fmt_time(h, m):
    return f"{h:02d}{m:02d}"


def _dur_str(h, m):
    parts = []
    if h:
        parts.append(f"{h} hour{'s' if h != 1 else ''}")
    if m:
        parts.append(f"{m} minute{'s' if m != 1 else ''}")
    return " ".join(parts) if parts else "0 minutes"


def generate_time_zones_reading_tables():
    journey = random.choice(_JOURNEYS)
    dep_h, dep_m = journey["dep"]
    arr_h, arr_m = journey["arr_local"]
    tz = journey["tz_ahead"]
    dur_h, dur_m = journey["dur_h"], journey["dur_m"]

    # Compute UK arrival time for the worked solution
    uk_arr_h = arr_h - tz
    if uk_arr_h < 0:
        uk_arr_h += 24

    # Part (ii): random family scenario
    n_adults   = random.choice([1, 2])
    n_children = random.choice([1, 2])

    ticket_name, adult_price = random.choice(list(_FARE_TABLE.items())[:-1])  # skip Business Premier
    child_price = round(adult_price * _CHILD_PCT / 100)

    include_ins  = random.choice([True, False])
    use_card     = random.choice([True, False])

    train_cost = n_adults * adult_price + n_children * child_price
    ins_cost   = (n_adults * _INS_ADULT + n_children * _INS_CHILD) if include_ins else 0
    card_cost  = _CARD_FEE if use_card else 0
    total_cost = train_cost + ins_cost + card_cost

    # Build fare table markdown (shown above question)
    table_lines = [
        "| Ticket Type | Adult Price |",
        "|---|---|",
    ]
    for t, p in _FARE_TABLE.items():
        table_lines.append(f"| {t} | £{p} |")
    table_lines.append("")
    table_lines.append(f"*Children (under 16) pay {_CHILD_PCT}% of the adult fare*")
    if include_ins:
        table_lines.append("")
        table_lines.append("| Travel Insurance | |")
        table_lines.append("|---|---|")
        table_lines.append(f"| Adults | £{_INS_ADULT} per person |")
        table_lines.append(f"| Children (under 16) | £{_INS_CHILD} per person |")
    if use_card:
        table_lines.append("")
        table_lines.append(f"*A £{_CARD_FEE} fee is added if paying by credit card.*")

    table_md = "\n".join(table_lines)

    # Build choices list for question text
    choices = [f"To buy **{ticket_name}** tickets"]
    if include_ins:
        choices.append(f"To buy travel insurance for all {n_adults + n_children} people")
    if use_card:
        choices.append("To pay by credit card")

    question_text = (
        f"**(i)** A train leaves {journey['from']} at {_fmt_time(dep_h, dep_m)} local time "
        f"and arrives in {journey['to']} at {_fmt_time(arr_h, arr_m)} local time. "
        f"{journey['to']} is {tz} hour ahead of {journey['from'].split('(')[0].strip()}. "
        f"How long did the journey take?\n\n"
        f"**(ii)** Using the fare table above, a family of "
        f"{n_adults} adult{'s' if n_adults > 1 else ''} and "
        f"{n_children} child{'ren' if n_children > 1 else ''} decide:\n\n"
        + "\n".join(f"- {c}" for c in choices)
        + f"\n\n**What is the total cost?** Enter the amount in pounds."
    )

    scaffold_steps = [
        {
            "prompt": (f"Convert arrival to UK time "
                       f"({_fmt_time(arr_h, arr_m)} − {tz} hour)"),
            "answer": _fmt_time(uk_arr_h, arr_m),
        },
        {
            "prompt": f"Journey duration ({_fmt_time(dep_h, dep_m)} → {_fmt_time(uk_arr_h, arr_m)})",
            "answer": _dur_str(dur_h, dur_m),
        },
        {
            "prompt": (f"Train cost: {n_adults} × £{adult_price} + "
                       f"{n_children} × £{child_price}"),
            "answer": train_cost,
        },
    ]
    if include_ins:
        scaffold_steps.append({
            "prompt": (f"Insurance: {n_adults} × £{_INS_ADULT} + "
                       f"{n_children} × £{_INS_CHILD}"),
            "answer": ins_cost,
        })
    if use_card:
        scaffold_steps.append({"prompt": "Credit card fee", "answer": card_cost})
    scaffold_steps.append({"prompt": "Total cost", "answer": total_cost})

    worked = [
        f"**(i) Journey time:**",
        (f"{journey['to']} time {_fmt_time(arr_h, arr_m)} → "
         f"UK time {_fmt_time(uk_arr_h, arr_m)} (subtract {tz} hour)"),
        (f"Journey: {_fmt_time(dep_h, dep_m)} → {_fmt_time(uk_arr_h, arr_m)} "
         f"= **{_dur_str(dur_h, dur_m)}**"),
        "",
        f"**(ii) Total cost:**",
        (f"Child price = {_CHILD_PCT}% × £{adult_price} = £{child_price}"),
        (f"Train: {n_adults} × £{adult_price} + {n_children} × £{child_price} "
         f"= £{n_adults * adult_price} + £{n_children * child_price} = £{train_cost}"),
    ]
    if include_ins:
        worked.append(
            f"Insurance: {n_adults} × £{_INS_ADULT} + {n_children} × £{_INS_CHILD} "
            f"= £{n_adults * _INS_ADULT} + £{n_children * _INS_CHILD} = £{ins_cost}"
        )
    if use_card:
        worked.append(f"Credit card fee: £{card_cost}")
    worked.append(
        f"Total = £{train_cost}"
        + (f" + £{ins_cost}" if include_ins else "")
        + (f" + £{card_cost}" if use_card else "")
        + f" = **£{total_cost}**"
    )

    return Question(
        question_text=question_text,
        correct_answer=total_cost,
        topic="Time and Measurement",
        question_type="Time Zones and Reading Tables",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={"table": table_md},
    )
