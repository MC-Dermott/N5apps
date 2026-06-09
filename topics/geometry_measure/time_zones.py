import random
from core.models.question_model import Question

NOTES = """
**Time Zones:**

Time zones are measured relative to **GMT** (Greenwich Mean Time).

- **GMT+3** means local time is **3 hours ahead** of GMT
- **GMT−5** means local time is **5 hours behind** GMT

**Converting between time zones:**
1. Convert the known time to GMT (reverse the offset)
2. Apply the destination time zone's offset

*Example:* It is 14:00 in Dubai (GMT+4). What time is it in London (GMT)?
- Dubai → GMT: 14:00 − 4 = 10:00 GMT
- GMT → London: 10:00 + 0 = **10:00**

**For journey time calculations:**
1. Convert all times to GMT
2. Subtract departure time from arrival time

**For stopovers:**
1. Find arrival time at the stopover city (local time)
2. Find departure time from the stopover city (local time)
3. Stopover = departure time − arrival time (both in the same city, so no conversion needed)
"""

_CITIES = [
    {"name": "Glasgow",      "country": "Scotland",    "offset": 0,   "gmt": "GMT"},
    {"name": "Edinburgh",    "country": "Scotland",    "offset": 0,   "gmt": "GMT"},
    {"name": "London",       "country": "England",     "offset": 0,   "gmt": "GMT"},
    {"name": "Paris",        "country": "France",      "offset": 1,   "gmt": "GMT+1"},
    {"name": "Berlin",       "country": "Germany",     "offset": 1,   "gmt": "GMT+1"},
    {"name": "Rome",         "country": "Italy",       "offset": 1,   "gmt": "GMT+1"},
    {"name": "Athens",       "country": "Greece",      "offset": 2,   "gmt": "GMT+2"},
    {"name": "Cairo",        "country": "Egypt",       "offset": 2,   "gmt": "GMT+2"},
    {"name": "Dubai",        "country": "UAE",         "offset": 4,   "gmt": "GMT+4"},
    {"name": "Singapore",    "country": "Singapore",   "offset": 8,   "gmt": "GMT+8"},
    {"name": "Hong Kong",    "country": "China",       "offset": 8,   "gmt": "GMT+8"},
    {"name": "Tokyo",        "country": "Japan",       "offset": 9,   "gmt": "GMT+9"},
    {"name": "Sydney",       "country": "Australia",   "offset": 10,  "gmt": "GMT+10"},
    {"name": "Auckland",     "country": "New Zealand", "offset": 12,  "gmt": "GMT+12"},
    {"name": "New York",     "country": "USA",         "offset": -5,  "gmt": "GMT−5"},
    {"name": "Chicago",      "country": "USA",         "offset": -6,  "gmt": "GMT−6"},
    {"name": "Los Angeles",  "country": "USA",         "offset": -8,  "gmt": "GMT−8"},
    {"name": "Toronto",      "country": "Canada",      "offset": -5,  "gmt": "GMT−5"},
    {"name": "Vancouver",    "country": "Canada",      "offset": -8,  "gmt": "GMT−8"},
]

_NAMES = [
    "Amy", "Callum", "Catriona", "Connor", "Douglas", "Eilidh",
    "Ewan", "Fiona", "Hamish", "Isla", "Jamie", "Kirsty",
    "Laura", "Liam", "Megan", "Ross",
]

_GMT_CITIES = [c for c in _CITIES if c["offset"] == 0]
_NON_GMT_CITIES = [c for c in _CITIES if c["offset"] != 0]


# ---------------------------------------------------------------------------
# Time arithmetic helpers
# ---------------------------------------------------------------------------

def _fmt(total_minutes):
    """Format total minutes (may be negative or > 1440) as HH:MM, wrapping within a day."""
    t = int(total_minutes) % (24 * 60)
    return f"{t // 60:02d}:{t % 60:02d}"


def _fmt_hhmm(total_minutes):
    """Format total minutes as HHMM (no colon), wrapping within a day."""
    t = int(total_minutes) % (24 * 60)
    return f"{t // 60:02d}{t % 60:02d}"


def _to_min(h, m=0):
    return h * 60 + m


def _duration_str(total_minutes):
    """Express a positive number of minutes as 'X hours Y minutes'."""
    h = total_minutes // 60
    m = total_minutes % 60
    h_word = f"{h} hour{'s' if h != 1 else ''}"
    m_word = f"{m} minute{'s' if m != 1 else ''}"
    if h == 0:
        return m_word
    if m == 0:
        return h_word
    return f"{h_word} {m_word}"


def _crosses_midnight(start_min, delta_min):
    result = start_min + delta_min
    return result >= 24 * 60 or result < 0


def _day_note(total_minutes):
    if total_minutes >= 24 * 60:
        return " (next day)"
    if total_minutes < 0:
        return " (previous day)"
    return ""


def _norm_gmt(dep_gmt_min, *others):
    """Return (normalized_dep, *normalized_others) so dep is in [0, 1440)."""
    base = (dep_gmt_min // (24 * 60)) * (24 * 60)
    return (dep_gmt_min - base,) + tuple(x - base for x in others)


def _fmt_gmt(norm_min):
    """Format a normalized GMT minute (dep=day 0) as 'HH:MM' with optional day note."""
    day = norm_min // (24 * 60)
    t = _fmt(norm_min)
    if day == 0:
        return t
    if day == 1:
        return f"{t} (next day)"
    if day < 0:
        return f"{t} (previous day)"
    return f"{t} (+{day} days)"


# ---------------------------------------------------------------------------
# Level 1 — Simple time zone conversion
# ---------------------------------------------------------------------------

def _level1_gmt_labels():
    """Convert between two cities given as GMT+/- offsets."""
    for _ in range(50):
        city_a, city_b = random.sample(_CITIES, 2)
        if city_a["offset"] == city_b["offset"]:
            continue

        h_a = random.randint(6, 21)
        m_a = random.choice([0, 30])
        start_min = _to_min(h_a, m_a)

        delta = city_b["offset"] - city_a["offset"]
        result_min = start_min + delta * 60
        day_label = _day_note(result_min)
        time_a = _fmt(start_min)
        time_b_hhmm = _fmt_hhmm(result_min)
        time_b_display = _fmt(result_min)

        off_a = city_a["offset"]
        off_b = city_b["offset"]

        if off_a == 0:
            gmt_worked = f"{city_a['name']} is {city_a['gmt']}, so {time_a} is already GMT"
        elif off_a > 0:
            gmt_worked = (
                f"Convert to GMT: {time_a} − {off_a} hour{'s' if off_a != 1 else ''} "
                f"= {_fmt(start_min - off_a * 60)}"
            )
        else:
            gmt_worked = (
                f"Convert to GMT: {time_a} + {abs(off_a)} hour{'s' if abs(off_a) != 1 else ''} "
                f"= {_fmt(start_min - off_a * 60)}"
            )

        scaffold_steps = [
            {
                "prompt": f"What is the time difference between {city_a['name']} and {city_b['name']}? Give your answer in hours (use a negative number if {city_b['name']} is behind {city_a['name']})",
                "answer": delta,
            },
            {
                "prompt": f"What time is it in {city_b['name']}? Give your answer in HHMM format.",
                "answer": time_b_hhmm,
            },
        ]

        worked = [
            f"{city_a['name']} is {city_a['gmt']}, {city_b['name']} is {city_b['gmt']}",
            f"Time difference = {city_b['gmt']} − {city_a['gmt']} = {delta:+d} hours",
            gmt_worked,
            f"Time in {city_b['name']} = {time_a} {'+' if delta >= 0 else '−'} {abs(delta)} "
            f"hour{'s' if abs(delta) != 1 else ''} = {time_b_display}{day_label}",
        ]

        question_text = (
            f"It is {time_a} in {city_a['name']} ({city_a['gmt']}). "
            f"What time is it in {city_b['name']} ({city_b['gmt']})? "
            f"Give your answer in HHMM format (e.g. 0930)."
        )

        return Question(
            question_text=question_text,
            correct_answer=time_b_hhmm,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 1)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
        )

    return _level1_relative()  # fallback


def _level1_relative():
    """Convert between two cities given as 'X hours ahead/behind'."""
    for _ in range(50):
        city_a, city_b = random.sample(_CITIES, 2)
        if city_a["offset"] == city_b["offset"]:
            continue

        h_a = random.randint(6, 21)
        m_a = random.choice([0, 30])
        start_min = _to_min(h_a, m_a)

        delta = city_b["offset"] - city_a["offset"]
        result_min = start_min + delta * 60
        day_label = _day_note(result_min)
        time_a = _fmt(start_min)
        time_b_hhmm = _fmt_hhmm(result_min)
        time_b_display = _fmt(result_min)

        if delta > 0:
            rel = f"{delta} hour{'s' if delta != 1 else ''} ahead of"
        else:
            rel = f"{abs(delta)} hour{'s' if abs(delta) != 1 else ''} behind"

        question_text = (
            f"{city_b['name']} is {rel} {city_a['name']}. "
            f"It is {time_a} in {city_a['name']}. "
            f"What time is it in {city_b['name']}? "
            f"Give your answer in HHMM format (e.g. 0930)."
        )

        scaffold_steps = [
            {
                "prompt": f"What is the time difference between {city_a['name']} and {city_b['name']}? Give your answer in hours (use a negative number if {city_b['name']} is behind {city_a['name']})",
                "answer": delta,
            },
            {
                "prompt": f"What time is it in {city_b['name']}? Give your answer in HHMM format.",
                "answer": time_b_hhmm,
            },
        ]

        worked = [
            f"{city_b['name']} is {rel} {city_a['name']}",
            f"Time difference = {delta:+d} hours",
            f"Time in {city_b['name']} = {time_a} {'+' if delta >= 0 else '−'} {abs(delta)} "
            f"hour{'s' if abs(delta) != 1 else ''} = {time_b_display}{day_label}",
        ]

        return Question(
            question_text=question_text,
            correct_answer=time_b_hhmm,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 1)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
        )


def _level1_find_arrival():
    """Given departure time and journey duration, find local arrival time in destination."""
    for _ in range(50):
        city_a, city_b = random.sample(_CITIES, 2)
        if city_a["offset"] == city_b["offset"]:
            continue

        dep_h = random.randint(6, 18)
        dep_m = random.choice([0, 30])
        dep_local_min = _to_min(dep_h, dep_m)
        journey_h = random.randint(1, 5)
        journey_min = journey_h * 60

        # Arrival in origin local time (intermediate step)
        arr_origin_min = dep_local_min + journey_min
        dep_gmt_min = dep_local_min - city_a["offset"] * 60
        arr_gmt_min = dep_gmt_min + journey_min
        arr_dest_min = arr_gmt_min + city_b["offset"] * 60

        dep_time = _fmt(dep_local_min)
        arr_origin_hhmm = _fmt_hhmm(arr_origin_min)
        arr_dest_hhmm = _fmt_hhmm(arr_dest_min)
        arr_dest_display = _fmt(arr_dest_min)
        arr_origin_display = _fmt(arr_origin_min)
        arr_dest_day = _day_note(arr_dest_min)

        delta = city_b["offset"] - city_a["offset"]
        if delta > 0:
            offset_desc = f"Apply time zone offset: {arr_origin_display} + {delta}h = {arr_dest_display}{arr_dest_day}"
        else:
            offset_desc = f"Apply time zone offset: {arr_origin_display} − {abs(delta)}h = {arr_dest_display}{arr_dest_day}"

        question_text = (
            f"A flight from {city_a['name']} ({city_a['gmt']}) to {city_b['name']} ({city_b['gmt']}) "
            f"takes {journey_h} hour{'s' if journey_h != 1 else ''}. "
            f"The flight departs {city_a['name']} at {dep_time}. "
            f"What time does it arrive in {city_b['name']} (local time)? "
            f"Give your answer in HHMM format (e.g. 0930)."
        )

        scaffold_steps = [
            {
                "prompt": f"Add the journey time to find the arrival time in {city_a['name']} time. Give your answer in HHMM format.",
                "answer": arr_origin_hhmm,
            },
            {
                "prompt": f"Apply the time zone offset to find the arrival time in {city_b['name']}. Give your answer in HHMM format.",
                "answer": arr_dest_hhmm,
            },
        ]

        worked = [
            f"Arrival in {city_a['name']} time: {dep_time} + {journey_h}h = {arr_origin_display}",
            offset_desc,
        ]

        return Question(
            question_text=question_text,
            correct_answer=arr_dest_hhmm,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 1)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
        )

    return _level1_gmt_labels()


def _level1_find_departure():
    """Given arrival time and journey duration, find local departure time in origin."""
    for _ in range(50):
        city_a, city_b = random.sample(_CITIES, 2)
        if city_a["offset"] == city_b["offset"]:
            continue

        # Build from a known departure so all values are consistent
        dep_h = random.randint(6, 18)
        dep_m = random.choice([0, 30])
        dep_local_min = _to_min(dep_h, dep_m)
        journey_h = random.randint(1, 5)
        journey_min = journey_h * 60

        dep_gmt_min = dep_local_min - city_a["offset"] * 60
        arr_gmt_min = dep_gmt_min + journey_min
        arr_dest_min = arr_gmt_min + city_b["offset"] * 60

        # Intermediate: arrival time expressed in origin timezone
        arr_in_origin_min = dep_local_min + journey_min

        dep_time = _fmt(dep_local_min)
        dep_hhmm = _fmt_hhmm(dep_local_min)
        arr_dest_time = _fmt(arr_dest_min)
        arr_in_origin_hhmm = _fmt_hhmm(arr_in_origin_min)
        arr_in_origin_display = _fmt(arr_in_origin_min)
        arr_dest_day = _day_note(arr_dest_min)

        delta = city_b["offset"] - city_a["offset"]
        if delta > 0:
            conv_desc = f"Convert arrival to {city_a['name']} time: {arr_dest_time}{arr_dest_day} − {delta}h = {arr_in_origin_display}"
        else:
            conv_desc = f"Convert arrival to {city_a['name']} time: {arr_dest_time}{arr_dest_day} + {abs(delta)}h = {arr_in_origin_display}"

        question_text = (
            f"A flight from {city_a['name']} ({city_a['gmt']}) to {city_b['name']} ({city_b['gmt']}) "
            f"takes {journey_h} hour{'s' if journey_h != 1 else ''}. "
            f"The flight arrives in {city_b['name']} at {arr_dest_time}{arr_dest_day} local time. "
            f"What time did the flight depart from {city_a['name']}? "
            f"Give your answer in HHMM format (e.g. 0930)."
        )

        scaffold_steps = [
            {
                "prompt": f"Convert the arrival time from {city_b['name']} time to {city_a['name']} time. Give your answer in HHMM format.",
                "answer": arr_in_origin_hhmm,
            },
            {
                "prompt": f"Subtract the journey time to find the departure time. Give your answer in HHMM format.",
                "answer": dep_hhmm,
            },
        ]

        worked = [
            conv_desc,
            f"Departure from {city_a['name']}: {arr_in_origin_display} − {journey_h}h = {dep_time}",
        ]

        return Question(
            question_text=question_text,
            correct_answer=dep_hhmm,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 1)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
        )

    return _level1_relative()


def generate_level1_question():
    return random.choice([_level1_gmt_labels, _level1_relative, _level1_find_arrival, _level1_find_departure])()


# ---------------------------------------------------------------------------
# Level 2 — Journey time involving a time zone conversion
# ---------------------------------------------------------------------------

def _level2_find_duration():
    """Given departure and arrival times in different time zones, find flight duration."""
    name = random.choice(_NAMES)

    for _ in range(50):
        city_a, city_b = random.sample(_CITIES, 2)
        if city_a["offset"] == city_b["offset"]:
            continue

        # Pick departure time (whole or half hour, 05:00–14:00 for outbound flights)
        dep_h = random.randint(5, 14)
        dep_m = random.choice([0, 15, 30, 45])
        dep_local_min = _to_min(dep_h, dep_m)

        # Pick duration: 1h to 13h in 15-min increments
        duration_min = random.choice(range(60, 13 * 60 + 1, 15))

        # Arrival in city_b local time
        dep_gmt_min = dep_local_min - city_a["offset"] * 60
        arr_gmt_min = dep_gmt_min + duration_min
        arr_local_min = arr_gmt_min + city_b["offset"] * 60

        # Keep arrival in a "plausible" time range (06:00 – 30:00 local)
        arr_display_min = arr_local_min % (24 * 60)
        if arr_display_min < 0:
            arr_display_min += 24 * 60

        dep_time = _fmt(dep_local_min)
        arr_time = _fmt(arr_local_min)

        dur_str = _duration_str(duration_min)

        # Normalise so dep_gmt is "day 0" for correct day annotations
        dep_g, arr_g = _norm_gmt(dep_gmt_min, arr_gmt_min)
        arr_gmt_hhmm = _fmt_hhmm(arr_gmt_min)   # for scaffold answer
        dep_gmt_display = _fmt(dep_gmt_min)

        off_a = city_a["offset"]
        off_b = city_b["offset"]

        if off_a == 0:
            dep_gmt_desc = f"Departure: {dep_time} (already GMT)"
        elif off_a > 0:
            dep_gmt_desc = (
                f"Departure in GMT: {dep_time} − {off_a} "
                f"hour{'s' if off_a != 1 else ''} = {_fmt_gmt(dep_g)}"
            )
        else:
            dep_gmt_desc = (
                f"Departure in GMT: {dep_time} + {abs(off_a)} "
                f"hour{'s' if abs(off_a) != 1 else ''} = {_fmt_gmt(dep_g)}"
            )

        day_note_arr = _day_note(arr_local_min)

        if off_b > 0:
            conv_desc = (
                f"Convert arrival time to GMT: {arr_time}{day_note_arr} − {off_b} "
                f"hour{'s' if off_b != 1 else ''} = {_fmt_gmt(arr_g)}"
            )
        elif off_b < 0:
            conv_desc = (
                f"Convert arrival time to GMT: {arr_time}{day_note_arr} + {abs(off_b)} "
                f"hour{'s' if abs(off_b) != 1 else ''} = {_fmt_gmt(arr_g)}"
            )
        else:
            conv_desc = f"Arrival in {city_b['name']} is already GMT: {arr_time}{day_note_arr}"

        question_text = (
            f"{name} flies from {city_a['name']} ({city_a['gmt']}) to "
            f"{city_b['name']} ({city_b['gmt']}). "
            f"The flight departs {city_a['name']} at {dep_time}. "
            f"The flight arrives in {city_b['name']} at {arr_time} local time"
            f"{day_note_arr}. "
            f"Calculate the flight time. "
            f"Give your answer in the form 'X hours Y minutes'."
        )

        scaffold_steps = [
            {
                "prompt": f"Convert the {city_b['name']} arrival time to GMT. Give your answer in HHMM format.",
                "answer": arr_gmt_hhmm,
            },
            {
                "prompt": "Calculate the flight time (arrival GMT − departure GMT)",
                "answer": dur_str,
                "answer_type": "duration",
            },
        ]

        worked = [
            dep_gmt_desc,
            conv_desc,
            f"Flight time = {_fmt_gmt(arr_g)} − {_fmt_gmt(dep_g)}",
            f"Flight time = {dur_str}",
        ]

        # Avoid very short flights (< 1 h) or same-GMT-time oddities
        if duration_min < 60:
            continue

        return Question(
            question_text=question_text,
            correct_answer=dur_str,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 2)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
            metadata={"answer_type": "duration"},
        )


def _level2_find_arrival():
    """Given departure time and flight duration, find local arrival time."""
    name = random.choice(_NAMES)

    for _ in range(50):
        city_a, city_b = random.sample(_CITIES, 2)
        if city_a["offset"] == city_b["offset"]:
            continue

        dep_h = random.randint(5, 15)
        dep_m = random.choice([0, 15, 30, 45])
        dep_local_min = _to_min(dep_h, dep_m)

        duration_min = random.choice(range(60, 14 * 60 + 1, 15))
        if duration_min < 60:
            continue

        dep_gmt_min = dep_local_min - city_a["offset"] * 60
        arr_gmt_min = dep_gmt_min + duration_min
        arr_local_min = arr_gmt_min + city_b["offset"] * 60

        dep_time = _fmt(dep_local_min)
        arr_time = _fmt(arr_local_min)
        dep_gmt_hhmm = _fmt_hhmm(dep_gmt_min)   # scaffold answer
        arr_gmt_hhmm = _fmt_hhmm(arr_gmt_min)   # scaffold answer
        arr_time_hhmm = _fmt_hhmm(arr_local_min)
        dur_str = _duration_str(duration_min)
        day_note_arr = _day_note(arr_local_min)

        # Normalise GMT times for annotated worked solution
        dep_g, arr_g = _norm_gmt(dep_gmt_min, arr_gmt_min)

        off_a = city_a["offset"]
        if off_a == 0:
            step1_desc = f"Departure is already in GMT: {dep_time}"
            step1_ans = dep_gmt_display
        elif off_a > 0:
            step1_desc = (
                f"Convert departure to GMT: {dep_time} − {off_a} "
                f"hour{'s' if off_a != 1 else ''} = {_fmt_gmt(dep_g)}"
            )
            step1_ans = dep_gmt_display
        else:
            step1_desc = (
                f"Convert departure to GMT: {dep_time} + {abs(off_a)} "
                f"hour{'s' if abs(off_a) != 1 else ''} = {_fmt_gmt(dep_g)}"
            )
            step1_ans = dep_gmt_display

        off_b = city_b["offset"]
        if off_b > 0:
            step3_desc = (
                f"Convert arrival GMT to {city_b['name']} local time: "
                f"{_fmt_gmt(arr_g)} + {off_b} hour{'s' if off_b != 1 else ''} = {arr_time}{day_note_arr}"
            )
        elif off_b < 0:
            step3_desc = (
                f"Convert arrival GMT to {city_b['name']} local time: "
                f"{_fmt_gmt(arr_g)} − {abs(off_b)} hour{'s' if abs(off_b) != 1 else ''} = {arr_time}{day_note_arr}"
            )
        else:
            step3_desc = (
                f"Arrival in GMT = {_fmt_gmt(arr_g)}, which is also local time in {city_b['name']}"
            )

        question_text = (
            f"{name}'s flight departs {city_a['name']} ({city_a['gmt']}) at {dep_time}. "
            f"The flight to {city_b['name']} ({city_b['gmt']}) takes {dur_str}. "
            f"What is the local time in {city_b['name']} when the flight lands? "
            f"Give your answer in HHMM format (e.g. 0930)."
        )

        scaffold_steps = [
            {
                "prompt": f"Convert the {city_a['name']} departure time to GMT. Give your answer in HHMM format.",
                "answer": dep_gmt_hhmm,
            },
            {
                "prompt": "Add the flight time to find the arrival time in GMT. Give your answer in HHMM format.",
                "answer": arr_gmt_hhmm,
            },
            {
                "prompt": f"Convert the GMT arrival time to {city_b['name']} local time. Give your answer in HHMM format.",
                "answer": arr_time_hhmm,
            },
        ]

        worked = [
            step1_desc,
            f"Arrival in GMT: {_fmt_gmt(dep_g)} + {dur_str} = {_fmt_gmt(arr_g)}",
            step3_desc,
        ]

        return Question(
            question_text=question_text,
            correct_answer=arr_time_hhmm,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 2)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
        )


def _level2_find_departure():
    """Given arrival time and flight duration, find local departure time in origin."""
    name = random.choice(_NAMES)

    for _ in range(50):
        city_a, city_b = random.sample(_CITIES, 2)
        if city_a["offset"] == city_b["offset"]:
            continue

        dep_h = random.randint(5, 15)
        dep_m = random.choice([0, 15, 30, 45])
        dep_local_min = _to_min(dep_h, dep_m)

        duration_min = random.choice(range(60, 13 * 60 + 1, 15))

        dep_gmt_min = dep_local_min - city_a["offset"] * 60
        arr_gmt_min = dep_gmt_min + duration_min
        arr_dest_min = arr_gmt_min + city_b["offset"] * 60

        dep_time = _fmt(dep_local_min)
        arr_dest_time = _fmt(arr_dest_min)
        dep_hhmm = _fmt_hhmm(dep_local_min)
        arr_gmt_hhmm = _fmt_hhmm(arr_gmt_min)
        dep_gmt_hhmm = _fmt_hhmm(dep_gmt_min)
        arr_gmt_display = _fmt(arr_gmt_min)
        dep_gmt_display = _fmt(dep_gmt_min)
        arr_dest_day = _day_note(arr_dest_min)
        dur_str = _duration_str(duration_min)

        dep_g, arr_g = _norm_gmt(dep_gmt_min, arr_gmt_min)

        off_b = city_b["offset"]
        if off_b == 0:
            step1_desc = f"Arrival in {city_b['name']} is already GMT: {arr_dest_time}{arr_dest_day}"
        elif off_b > 0:
            step1_desc = (
                f"Convert arrival to GMT: {arr_dest_time}{arr_dest_day} − {off_b} "
                f"hour{'s' if off_b != 1 else ''} = {_fmt_gmt(arr_g)}"
            )
        else:
            step1_desc = (
                f"Convert arrival to GMT: {arr_dest_time}{arr_dest_day} + {abs(off_b)} "
                f"hour{'s' if abs(off_b) != 1 else ''} = {_fmt_gmt(arr_g)}"
            )

        off_a = city_a["offset"]
        if off_a == 0:
            step3_desc = f"Departure is already in GMT: {dep_time}"
        elif off_a > 0:
            step3_desc = (
                f"Convert departure GMT to {city_a['name']} local time: "
                f"{_fmt_gmt(dep_g)} + {off_a} hour{'s' if off_a != 1 else ''} = {dep_time}"
            )
        else:
            step3_desc = (
                f"Convert departure GMT to {city_a['name']} local time: "
                f"{_fmt_gmt(dep_g)} − {abs(off_a)} hour{'s' if abs(off_a) != 1 else ''} = {dep_time}"
            )

        question_text = (
            f"{name}'s flight arrives in {city_b['name']} ({city_b['gmt']}) at "
            f"{arr_dest_time}{arr_dest_day} local time. "
            f"The flight from {city_a['name']} ({city_a['gmt']}) takes {dur_str}. "
            f"What time did the flight depart from {city_a['name']}? "
            f"Give your answer in HHMM format (e.g. 0930)."
        )

        scaffold_steps = [
            {
                "prompt": f"Convert the {city_b['name']} arrival time to GMT. Give your answer in HHMM format.",
                "answer": arr_gmt_hhmm,
            },
            {
                "prompt": "Subtract the flight time to find the departure time in GMT. Give your answer in HHMM format.",
                "answer": dep_gmt_hhmm,
            },
            {
                "prompt": f"Convert the GMT departure time to {city_a['name']} local time. Give your answer in HHMM format.",
                "answer": dep_hhmm,
            },
        ]

        worked = [
            step1_desc,
            f"Departure in GMT: {_fmt_gmt(arr_g)} − {dur_str} = {_fmt_gmt(dep_g)}",
            step3_desc,
        ]

        return Question(
            question_text=question_text,
            correct_answer=dep_hhmm,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 2)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
        )


def _level2_find_duration_relative():
    """Find flight duration; time difference given as 'X hours ahead/behind'."""
    name = random.choice(_NAMES)

    for _ in range(50):
        city_a, city_b = random.sample(_CITIES, 2)
        delta = city_b["offset"] - city_a["offset"]
        if delta == 0:
            continue

        dep_h = random.randint(5, 14)
        dep_m = random.choice([0, 15, 30, 45])
        dep_local_min = _to_min(dep_h, dep_m)
        dep_in_b_min = dep_local_min + delta * 60

        # Avoid day-crossing in the dep-to-city-b conversion to keep worked solution clean
        if not (0 <= dep_in_b_min < 24 * 60):
            continue

        duration_min = random.choice(range(60, 13 * 60 + 1, 15))

        dep_gmt_min = dep_local_min - city_a["offset"] * 60
        arr_gmt_min = dep_gmt_min + duration_min
        arr_local_min = arr_gmt_min + city_b["offset"] * 60

        dep_time = _fmt(dep_local_min)
        arr_time = _fmt(arr_local_min)
        dur_str = _duration_str(duration_min)
        day_note_arr = _day_note(arr_local_min)
        dep_in_b_display = _fmt(dep_in_b_min)
        dep_in_b_hhmm = _fmt_hhmm(dep_in_b_min)

        if delta > 0:
            rel = f"{delta} hour{'s' if delta != 1 else ''} ahead of"
            conv_desc = f"Convert departure to {city_b['name']} time: {dep_time} + {delta}h = {dep_in_b_display}"
        else:
            rel = f"{abs(delta)} hour{'s' if abs(delta) != 1 else ''} behind"
            conv_desc = f"Convert departure to {city_b['name']} time: {dep_time} − {abs(delta)}h = {dep_in_b_display}"

        question_text = (
            f"{name} flies from {city_a['name']} to {city_b['name']}. "
            f"{city_b['name']} is {rel} {city_a['name']}. "
            f"The flight departs {city_a['name']} at {dep_time}. "
            f"The flight arrives in {city_b['name']} at {arr_time} local time{day_note_arr}. "
            f"Calculate the flight time. "
            f"Give your answer in the form 'X hours Y minutes'."
        )

        scaffold_steps = [
            {
                "prompt": f"Convert the departure time to {city_b['name']} time. Give your answer in HHMM format.",
                "answer": dep_in_b_hhmm,
            },
            {
                "prompt": f"Calculate the flight time (arrival time in {city_b['name']} − departure time in {city_b['name']} time)",
                "answer": dur_str,
                "answer_type": "duration",
            },
        ]

        worked = [
            f"{city_b['name']} is {rel} {city_a['name']}",
            conv_desc,
            f"Flight time = {arr_time}{day_note_arr} − {dep_in_b_display} = {dur_str}",
        ]

        return Question(
            question_text=question_text,
            correct_answer=dur_str,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 2)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
            metadata={"answer_type": "duration"},
        )


def _level2_find_arrival_relative():
    """Find arrival time; time difference given as 'X hours ahead/behind'."""
    name = random.choice(_NAMES)

    for _ in range(50):
        city_a, city_b = random.sample(_CITIES, 2)
        delta = city_b["offset"] - city_a["offset"]
        if delta == 0:
            continue

        dep_h = random.randint(5, 15)
        dep_m = random.choice([0, 15, 30, 45])
        dep_local_min = _to_min(dep_h, dep_m)

        duration_min = random.choice(range(60, 14 * 60 + 1, 15))
        if duration_min < 60:
            continue

        dep_gmt_min = dep_local_min - city_a["offset"] * 60
        arr_gmt_min = dep_gmt_min + duration_min
        arr_local_min = arr_gmt_min + city_b["offset"] * 60

        dep_time = _fmt(dep_local_min)
        arr_time = _fmt(arr_local_min)
        arr_time_hhmm = _fmt_hhmm(arr_local_min)
        dur_str = _duration_str(duration_min)
        day_note_arr = _day_note(arr_local_min)

        # Intermediate: add duration in city_a's timezone, then adjust
        naive_arr_min = dep_local_min + duration_min
        naive_arr_display = _fmt(naive_arr_min)
        naive_arr_hhmm = _fmt_hhmm(naive_arr_min)
        naive_arr_day = _day_note(naive_arr_min)

        if delta > 0:
            rel = f"{delta} hour{'s' if delta != 1 else ''} ahead of"
            step2_desc = (
                f"Apply time zone: {naive_arr_display}{naive_arr_day} + {delta}h = {arr_time}{day_note_arr}"
            )
        else:
            rel = f"{abs(delta)} hour{'s' if abs(delta) != 1 else ''} behind"
            step2_desc = (
                f"Apply time zone: {naive_arr_display}{naive_arr_day} − {abs(delta)}h = {arr_time}{day_note_arr}"
            )

        question_text = (
            f"{name}'s flight departs {city_a['name']} at {dep_time}. "
            f"The flight to {city_b['name']} takes {dur_str}. "
            f"{city_b['name']} is {rel} {city_a['name']}. "
            f"What is the local time in {city_b['name']} when the flight lands? "
            f"Give your answer in HHMM format (e.g. 0930)."
        )

        scaffold_steps = [
            {
                "prompt": f"Add the flight time to find the arrival time in {city_a['name']} time. Give your answer in HHMM format.",
                "answer": naive_arr_hhmm,
            },
            {
                "prompt": f"Apply the time zone difference to find the arrival time in {city_b['name']}. Give your answer in HHMM format.",
                "answer": arr_time_hhmm,
            },
        ]

        worked = [
            f"{city_b['name']} is {rel} {city_a['name']}",
            f"Add flight time: {dep_time} + {dur_str} = {naive_arr_display}{naive_arr_day}",
            step2_desc,
        ]

        return Question(
            question_text=question_text,
            correct_answer=arr_time_hhmm,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 2)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
        )


def _level2_find_departure_relative():
    """Find departure time; time difference given as 'X hours ahead/behind'."""
    name = random.choice(_NAMES)

    for _ in range(50):
        city_a, city_b = random.sample(_CITIES, 2)
        delta = city_b["offset"] - city_a["offset"]
        if delta == 0:
            continue

        dep_h = random.randint(5, 15)
        dep_m = random.choice([0, 15, 30, 45])
        dep_local_min = _to_min(dep_h, dep_m)

        duration_min = random.choice(range(60, 13 * 60 + 1, 15))
        if duration_min < 60:
            continue

        dep_gmt_min = dep_local_min - city_a["offset"] * 60
        arr_gmt_min = dep_gmt_min + duration_min
        arr_dest_min = arr_gmt_min + city_b["offset"] * 60

        dep_time = _fmt(dep_local_min)
        dep_hhmm = _fmt_hhmm(dep_local_min)
        arr_dest_time = _fmt(arr_dest_min)
        dur_str = _duration_str(duration_min)
        arr_dest_day = _day_note(arr_dest_min)

        # Convert arrival back to city_a time by reversing the offset
        arr_in_a_min = arr_dest_min - delta * 60
        arr_in_a_display = _fmt(arr_in_a_min)
        arr_in_a_hhmm = _fmt_hhmm(arr_in_a_min)
        arr_in_a_day = _day_note(arr_in_a_min)

        if delta > 0:
            rel = f"{delta} hour{'s' if delta != 1 else ''} ahead of"
            step1_desc = (
                f"Convert arrival to {city_a['name']} time: "
                f"{arr_dest_time}{arr_dest_day} − {delta}h = {arr_in_a_display}{arr_in_a_day}"
            )
        else:
            rel = f"{abs(delta)} hour{'s' if abs(delta) != 1 else ''} behind"
            step1_desc = (
                f"Convert arrival to {city_a['name']} time: "
                f"{arr_dest_time}{arr_dest_day} + {abs(delta)}h = {arr_in_a_display}{arr_in_a_day}"
            )

        question_text = (
            f"{name}'s flight arrives in {city_b['name']} at {arr_dest_time}{arr_dest_day} local time. "
            f"The flight from {city_a['name']} takes {dur_str}. "
            f"{city_b['name']} is {rel} {city_a['name']}. "
            f"What time did the flight depart from {city_a['name']}? "
            f"Give your answer in HHMM format (e.g. 0930)."
        )

        scaffold_steps = [
            {
                "prompt": f"Convert the {city_b['name']} arrival time to {city_a['name']} time. Give your answer in HHMM format.",
                "answer": arr_in_a_hhmm,
            },
            {
                "prompt": f"Subtract the flight time to find the departure time from {city_a['name']}. Give your answer in HHMM format.",
                "answer": dep_hhmm,
            },
        ]

        worked = [
            f"{city_b['name']} is {rel} {city_a['name']}",
            step1_desc,
            f"Departure from {city_a['name']}: {arr_in_a_display}{arr_in_a_day} − {dur_str} = {dep_time}",
        ]

        return Question(
            question_text=question_text,
            correct_answer=dep_hhmm,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 2)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
        )


def generate_level2_question():
    return random.choice([
        _level2_find_duration,
        _level2_find_arrival,
        _level2_find_departure,
        _level2_find_duration_relative,
        _level2_find_arrival_relative,
        _level2_find_departure_relative,
    ])()


# ---------------------------------------------------------------------------
# Level 3 — Stopover journey
# ---------------------------------------------------------------------------

def _level3_find_stopover():
    name = random.choice(_NAMES)

    for _ in range(100):
        cities = random.sample(_CITIES, 3)
        origin, stop, dest = cities

        if origin["offset"] == dest["offset"]:
            continue

        dep_h = random.randint(6, 12)
        dep_m = random.choice([0, 30])
        dep_local_min = _to_min(dep_h, dep_m)
        dep_gmt_min = dep_local_min - origin["offset"] * 60

        flight1_h = random.randint(1, 7)
        flight1_min = flight1_h * 60

        stopover_h = random.randint(1, 4)
        stopover_min = stopover_h * 60

        flight2_h = random.randint(1, 7)
        flight2_min = flight2_h * 60

        total_journey_min = flight1_min + stopover_min + flight2_min
        total_flight_min = flight1_min + flight2_min

        arr_dest_gmt_min = dep_gmt_min + total_journey_min
        arr_dest_local_min = arr_dest_gmt_min + dest["offset"] * 60

        # Departure time converted into the destination timezone
        dep_in_dest_min = dep_local_min + (dest["offset"] - origin["offset"]) * 60

        # Keep dep_in_dest as a clean same-day time so the arithmetic is clear
        if not (0 <= dep_in_dest_min < 24 * 60):
            continue

        dep_time = _fmt(dep_local_min)
        arr_dest_time = _fmt(arr_dest_local_min)
        arr_dest_day = _day_note(arr_dest_local_min)
        dep_in_dest = _fmt_hhmm(dep_in_dest_min)
        dep_in_dest_display = _fmt(dep_in_dest_min)

        total_journey_str = _duration_str(total_journey_min)
        total_flight_str = _duration_str(total_flight_min)
        stopover_str = _duration_str(stopover_min)

        off_diff = dest["offset"] - origin["offset"]
        if off_diff > 0:
            conv_desc = (
                f"Convert departure to {dest['name']} time: "
                f"{dep_time} + {off_diff}h = {dep_in_dest_display}"
            )
        else:
            conv_desc = (
                f"Convert departure to {dest['name']} time: "
                f"{dep_time} − {abs(off_diff)}h = {dep_in_dest_display}"
            )

        question_text = (
            f"{name} flies from {origin['name']} to {dest['name']} with a stopover in {stop['name']}.\n\n"
            f"- {name} departs {origin['name']} ({origin['gmt']}) at {dep_time}.\n"
            f"- The flight from {origin['name']} to {stop['name']} takes "
            f"{flight1_h} hour{'s' if flight1_h != 1 else ''}.\n"
            f"- The flight from {stop['name']} to {dest['name']} takes "
            f"{flight2_h} hour{'s' if flight2_h != 1 else ''}.\n"
            f"- {name} arrives in {dest['name']} ({dest['gmt']}) at {arr_dest_time} local time{arr_dest_day}.\n\n"
            f"Calculate how long {name} waited in {stop['name']}. "
            f"Give your answer in the form 'X hours Y minutes'."
        )

        scaffold_steps = [
            {
                "prompt": (
                    f"Convert the departure time from {origin['name']} ({origin['gmt']}) to "
                    f"{dest['name']} ({dest['gmt']}) time. Give your answer in HHMM format (e.g. 0930)."
                ),
                "answer": dep_in_dest,
            },
            {
                "prompt": (
                    f"Calculate the total journey time using the departure time in {dest['name']} time "
                    f"({dep_in_dest_display}) and the arrival time in {dest['name']} "
                    f"({arr_dest_time}{arr_dest_day})."
                ),
                "answer": total_journey_str,
                "answer_type": "duration",
            },
            {
                "prompt": (
                    f"Calculate the total flight time "
                    f"({flight1_h} hour{'s' if flight1_h != 1 else ''} + "
                    f"{flight2_h} hour{'s' if flight2_h != 1 else ''})."
                ),
                "answer": total_flight_str,
                "answer_type": "duration",
            },
            {
                "prompt": "Calculate the stopover time (total journey time − total flight time).",
                "answer": stopover_str,
                "answer_type": "duration",
            },
        ]

        worked = [
            conv_desc,
            f"Total journey time = {arr_dest_time}{arr_dest_day} − {dep_in_dest_display} = {total_journey_str}",
            f"Total flight time = {flight1_h}h + {flight2_h}h = {total_flight_str}",
            f"Stopover = {total_journey_str} − {total_flight_str} = {stopover_str}",
        ]

        return Question(
            question_text=question_text,
            correct_answer=stopover_str,
            topic="Geometry and Measure",
            question_type="Time Zones (Level 3)",
            scaffold_steps=scaffold_steps,
            worked_solution=worked,
            notes=NOTES,
            metadata={"answer_type": "duration"},
        )


def generate_level3_question():
    return _level3_find_stopover()


# ---------------------------------------------------------------------------
# Dispatchers
# ---------------------------------------------------------------------------

def generate_time_zone_question_n4():
    return generate_level1_question()


def generate_time_zone_l1():
    return generate_level1_question()


def generate_time_zone_l2():
    return generate_level2_question()


def generate_time_zone_l3():
    return generate_level3_question()


def generate_time_zone_question():
    return random.choice([
        generate_level1_question,
        generate_level2_question,
        generate_level3_question,
    ])()
