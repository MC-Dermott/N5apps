import random
from core.models.question_model import Question

NOTES = """
**Commission:**

A commission is a percentage of sales paid on top of a basic salary.
Commission is often only paid on sales **above** a threshold amount.

**Calculating gross pay with commission:**
1. Excess sales = total sales − threshold
2. Commission = commission rate % × excess sales
3. **Gross pay = basic salary + commission**
"""

_NAMES = [
    "Amy", "Callum", "Catriona", "Connor", "Douglas", "Eilidh",
    "Ewan", "Freya", "Hamish", "Isla", "Jamie", "Kirsty",
    "Laura", "Liam", "Megan", "Ramani", "Ross", "Stuart",
]

_PRONOUNS = {
    "Amy": ("she", "her"), "Callum": ("he", "his"), "Catriona": ("she", "her"),
    "Connor": ("he", "his"), "Douglas": ("he", "his"), "Eilidh": ("she", "her"),
    "Ewan": ("he", "his"), "Freya": ("she", "her"), "Hamish": ("he", "his"),
    "Isla": ("she", "her"), "Jamie": ("they", "their"), "Kirsty": ("she", "her"),
    "Laura": ("she", "her"), "Liam": ("he", "his"), "Megan": ("she", "her"),
    "Ramani": ("she", "her"), "Ross": ("he", "his"), "Stuart": ("he", "his"),
}

_MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

_SCENARIOS = [
    {"job": "sales person",       "business": "a car company",          "thresholds": [40000, 50000, 58000, 60000, 70000], "excess_opts": [10000, 15000, 20000, 25000, 30000, 35000, 38000, 40000]},
    {"job": "sales representative","business": "an estate agency",       "thresholds": [100000, 120000, 150000, 200000],   "excess_opts": [20000, 25000, 30000, 40000, 50000, 60000, 80000]},
    {"job": "sales assistant",    "business": "an electronics company",  "thresholds": [10000, 12000, 15000, 20000],       "excess_opts": [2000, 3000, 4000, 5000, 6000, 8000, 10000]},
    {"job": "sales person",       "business": "a furniture company",     "thresholds": [15000, 20000, 25000, 30000],       "excess_opts": [3000, 4000, 5000, 6000, 8000, 10000, 12000]},
    {"job": "sales representative","business": "a software company",     "thresholds": [20000, 25000, 30000, 40000],       "excess_opts": [5000, 8000, 10000, 12000, 15000, 20000]},
    {"job": "sales person",       "business": "a double glazing company","thresholds": [10000, 12000, 15000, 20000],       "excess_opts": [2000, 3000, 4000, 5000, 6000, 8000]},
]

_BASIC_SALARIES = [1200, 1400, 1500, 1600, 1750, 1870, 2000, 2200, 2400]
_COMMISSION_RATES = [1, 2, 3, 4, 5]


def generate_commission_question():
    name = random.choice(_NAMES)
    pronoun, possessive = _PRONOUNS[name]
    month = random.choice(_MONTHS)
    scenario = random.choice(_SCENARIOS)
    basic_salary = random.choice(_BASIC_SALARIES)
    rate = random.choice(_COMMISSION_RATES)
    threshold = random.choice(scenario["thresholds"])
    excess = random.choice(scenario["excess_opts"])
    total_sales = threshold + excess

    commission = round(rate / 100 * excess, 2)
    gross_pay = round(basic_salary + commission, 2)

    question_text = (
        f"{name} works as a {scenario['job']} for {scenario['business']}.\n\n"
        f"{pronoun.capitalize()} is paid a basic monthly salary of £{basic_salary:,} "
        f"plus commission of {rate}% on {possessive} monthly sales **over** £{threshold:,}.\n\n"
        f"In {month}, {possessive} sales totalled £{total_sales:,}.\n\n"
        f"Calculate {name}'s gross pay in {month}."
    )

    scaffold_steps = [
        {
            "prompt": f"Calculate the sales over the threshold (total sales − £{threshold:,}).",
            "answer": float(excess),
        },
        {
            "prompt": f"Calculate the commission ({rate}% of £{excess:,}).",
            "answer": commission,
        },
        {
            "prompt": f"Calculate gross pay (basic salary + commission).",
            "answer": gross_pay,
        },
    ]

    worked = [
        f"Sales over threshold = £{total_sales:,} − £{threshold:,} = £{excess:,}",
        f"Commission = {rate}% × £{excess:,} = £{commission:,.2f}",
        f"Gross pay = £{basic_salary:,} + £{commission:,.2f} = £{gross_pay:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=gross_pay,
        topic="Finance and Statistics",
        question_type="Commission",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )
