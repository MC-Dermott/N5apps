import random
from decimal import Decimal, ROUND_HALF_UP
from core.models.question_model import Question

NOTES_DECIMAL_PLACES = """
**Rounding to Decimal Places:**

1. Find the digit in the decimal place you are rounding to.
2. Look at the **next digit** (one place further right): if it is 5 or more, round up;
   otherwise, leave it as is.
3. Remove all the digits after the decimal place you rounded to.

**Example:** Round 5.4763 to 2 decimal places.
- The digit in the 2nd decimal place is 7.
- The next digit is 6, so round up: 7 → 8.
- 5.4763 rounded to 2 decimal places = **5.48**
"""

NOTES_MONEY = """
**Rounding Money to the Nearest Penny:**

Money is always rounded to **2 decimal places** (the nearest penny).

1. Find the digit in the pence column (2nd decimal place).
2. Look at the **next digit**: if it is 5 or more, round up; otherwise, leave it as is.
3. Remove all digits after the 2nd decimal place.

**Example:** Round £14.5763 to the nearest penny.
- The digit in the 2nd decimal place is 7.
- The next digit is 6, so round up: 7 → 8.
- £14.5763 rounded to the nearest penny = **£14.58**
"""

NOTES_SIG_FIGS = """
**Rounding to Significant Figures:**

1. Find the first significant figure — the first digit that is **not zero**, reading
   from the left.
2. Count that many significant figures.
3. Look at the **next digit**: if it is 5 or more, round up; otherwise, leave it as is.
4. Fill any remaining places before the decimal point with zeros if needed.

**Example:** Round 3456 to 2 significant figures.
- The first 2 significant figures are 3 and 4.
- The next digit is 5, so round up: 4 → 5.
- 3456 rounded to 2 significant figures = **3500**

**Example:** Round 0.0273 to 1 significant figure.
- The first significant figure is 2 (leading zeros don't count).
- The next digit is 7, so round up: 2 → 3.
- 0.0273 rounded to 1 significant figure = **0.03**
"""

_ORDINALS = {1: "1st", 2: "2nd", 3: "3rd"}


def _ordinal(n):
    return _ORDINALS.get(n, f"{n}th")


def _fmt(d):
    return format(d, "f")


# ---------------------------------------------------------------------------
# Decimal Places
# ---------------------------------------------------------------------------

def generate_rounding_decimal_places():
    places = random.choice([1, 2, 3])
    extra = random.choice([1, 2, 3])
    int_part = random.randint(0, 999)
    frac_digits = [random.randint(0, 9) for _ in range(places + extra)]
    frac_str = "".join(str(d) for d in frac_digits)
    value = Decimal(f"{int_part}.{frac_str}")

    quant = Decimal(1).scaleb(-places)
    rounded = value.quantize(quant, rounding=ROUND_HALF_UP)
    answer = float(rounded)

    next_digit = frac_digits[places]
    place_word = _ordinal(places)
    places_label = f"{places} decimal place{'s' if places != 1 else ''}"

    question_text = f"Round {_fmt(value)} to {places_label}."

    scaffold_steps = [
        {"prompt": f"Is the digit after the {place_word} decimal place 5 or more?",
         "answer": "Yes" if next_digit >= 5 else "No"},
        {"prompt": f"Round the value to {places_label}", "answer": answer},
    ]

    worked = [
        f"The digit after the {place_word} decimal place is {next_digit}, so "
        f"{'round up' if next_digit >= 5 else 'round down'}.",
        f"{_fmt(value)} rounded to {places_label} = **{_fmt(rounded)}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Rounding",
        question_type="Decimal Places",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_DECIMAL_PLACES,
    )


# ---------------------------------------------------------------------------
# Rounding Money — always to the nearest penny (2 decimal places)
# ---------------------------------------------------------------------------

_MONEY_TEMPLATES = [
    "A supermarket receipt comes to £{amount}.",
    "Amir's electricity bill this month is £{amount}.",
    "A taxi fare works out at £{amount}.",
    "The total cost of fuel for the trip is £{amount}.",
    "After converting currency, Priya has £{amount}.",
    "A restaurant bill, before service charge, comes to £{amount}.",
    "The cost of the shopping trolley is £{amount}.",
    "A phone bill this month comes to £{amount}.",
]


def generate_rounding_money():
    extra = random.choice([1, 2, 3])
    int_part = random.randint(0, 500)
    frac_digits = [random.randint(0, 9) for _ in range(2 + extra)]
    frac_str = "".join(str(d) for d in frac_digits)
    value = Decimal(f"{int_part}.{frac_str}")

    rounded = value.quantize(Decimal("1.00"), rounding=ROUND_HALF_UP)
    answer = float(rounded)

    next_digit = frac_digits[2]
    template = random.choice(_MONEY_TEMPLATES)

    question_text = (
        f"{template.format(amount=_fmt(value))}\n\n"
        f"Round this to the nearest penny (2 decimal places)."
    )

    scaffold_steps = [
        {"prompt": "Is the digit after the 2nd decimal place 5 or more?",
         "answer": "Yes" if next_digit >= 5 else "No"},
        {"prompt": "Round the amount to the nearest penny", "answer": answer},
    ]

    worked = [
        f"The digit after the 2nd decimal place is {next_digit}, so "
        f"{'round up' if next_digit >= 5 else 'round down'}.",
        f"£{_fmt(value)} rounded to the nearest penny = **£{_fmt(rounded)}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Rounding",
        question_type="Rounding Money",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_MONEY,
    )


# ---------------------------------------------------------------------------
# Significant Figures — excludes cases needing a trailing zero after the
# decimal point to show the correct number of significant figures.
# ---------------------------------------------------------------------------

def _round_sig_figs(value, sig_figs):
    exponent = value.adjusted() - sig_figs + 1
    quant = Decimal(1).scaleb(exponent)
    return value.quantize(quant, rounding=ROUND_HALF_UP)


def _has_decimal_trailing_zero(rounded):
    tup = rounded.as_tuple()
    return tup.exponent < 0 and tup.digits[-1] == 0


def _random_decimal_candidate(sig_figs):
    int_digits = random.randint(0, 3)
    int_part = random.randint(1, 10 ** int_digits - 1) if int_digits else 0
    frac_digits = [random.randint(0, 9) for _ in range(sig_figs + random.randint(1, 3))]
    if int_part == 0:
        frac_digits[0] = random.randint(1, 9)
    frac_str = "".join(str(d) for d in frac_digits)
    return Decimal(f"{int_part}.{frac_str}")


def generate_rounding_significant_figures():
    sig_figs = random.choice([1, 2, 3])

    if random.random() < 0.35:
        digit_count = sig_figs + random.randint(1, 3)
        low = 10 ** (digit_count - 1)
        high = 10 ** digit_count - 1
        value = Decimal(random.randint(low, high))
    else:
        for _ in range(30):
            value = _random_decimal_candidate(sig_figs)
            if not _has_decimal_trailing_zero(_round_sig_figs(value, sig_figs)):
                break

    rounded = _round_sig_figs(value, sig_figs)
    answer = float(rounded)

    digits = value.as_tuple().digits
    next_digit = digits[sig_figs] if len(digits) > sig_figs else 0
    figs_label = f"{sig_figs} significant figure{'s' if sig_figs != 1 else ''}"

    question_text = f"Round {_fmt(value)} to {figs_label}."

    scaffold_steps = [
        {"prompt": f"Is the digit after the {figs_label} you are keeping 5 or more?",
         "answer": "Yes" if next_digit >= 5 else "No"},
        {"prompt": f"Round the value to {figs_label}", "answer": answer},
    ]

    worked = [
        f"The digit after the {figs_label} you keep is {next_digit}, so "
        f"{'round up' if next_digit >= 5 else 'round down'}.",
        f"{_fmt(value)} rounded to {figs_label} = **{_fmt(rounded)}**",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Rounding",
        question_type="Significant Figures",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES_SIG_FIGS,
    )

