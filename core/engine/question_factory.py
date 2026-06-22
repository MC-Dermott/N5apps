from topics.numeracy.fractions import generate_fraction_question, generate_fraction_question_n4
from topics.numeracy.percentages import generate_percentage_question, generate_percentage_question_n4
from topics.numeracy.probability import (
    generate_probability_question as generate_numeracy_probability_question,
    generate_probability_l1 as generate_numeracy_probability_l1,
    generate_probability_l2 as generate_numeracy_probability_l2,
)
from topics.finance_statistics.simple_interest import generate_simple_interest_question, generate_simple_interest_question_n4
from topics.finance_statistics.appreciation import generate_appreciation_question, generate_appreciation_question_n4
from topics.finance_statistics.hire_purchase import (
    generate_hire_purchase_question,
    generate_hire_purchase_question_n4,
    generate_hire_purchase_l1,
    generate_hire_purchase_l2,
)
from topics.finance_statistics.national_insurance import (
    generate_ni_question,
    generate_ni_l1,
    generate_ni_l2,
    generate_ni_l3,
)
from topics.finance_statistics.wages import generate_wages_question, generate_wages_l1, generate_wages_l2
from topics.finance_statistics.commission import generate_commission_question
from topics.finance_statistics.loans import generate_loans_question
from topics.finance_statistics.mortgages import generate_mortgages_question
from topics.finance_statistics.budgeting import generate_budgeting_question
from topics.finance_statistics.reverse_percentage import generate_reverse_percentage_question
from topics.geometry_measure.pythagoras import generate_pythagoras_question, generate_pythagoras_question_n4
from topics.geometry_measure.circle_area import generate_circle_area_question, generate_circle_area_question_n4
from topics.geometry_measure.gradient import generate_gradient_question, generate_gradient_question_n4
from topics.geometry_measure.volume import generate_volume_question, generate_volume_question_n4
from topics.geometry_measure.time_zones import (
    generate_time_zone_question,
    generate_time_zone_question_n4,
    generate_time_zone_l1,
    generate_time_zone_l2,
    generate_time_zone_l3,
)
from topics.geometry_measure.tolerance import (
    generate_tolerance_question,
    generate_tolerance_l1,
    generate_tolerance_l2,
    generate_tolerance_l3,
)
from topics.statistics.standard_deviation import generate_standard_deviation_question
from topics.statistics.probability import generate_probability_question
from topics.numeracy_assessment.compound_percentages import generate_compound_percentages
from topics.numeracy_assessment.fractions import generate_fractions as generate_num_fractions
from topics.numeracy_assessment.liquid_volume import generate_liquid_volume
from topics.numeracy_assessment.foreign_currency import generate_foreign_currency
from topics.numeracy_assessment.time_zones_reading_tables import generate_time_zones_reading_tables
from topics.numeracy_assessment.reading_scale import generate_reading_scale
from topics.numeracy_assessment.ratio import generate_ratio
from topics.numeracy_assessment.probability import generate_probability as generate_num_probability
from topics.numeracy_assessment.stem_and_leaf import generate_stem_and_leaf
from topics.numeracy_assessment.reading_bar_charts import generate_reading_bar_charts
from topics.numeracy_assessment.pie_charts import generate_pie_charts

_N5_TOPICS = {
    "Numeracy": {
        "Fractions": generate_fraction_question,
        "Percentages": generate_percentage_question,
        "Probability": generate_numeracy_probability_question,
    },
    "Finance and Statistics": {
        "Simple Interest": generate_simple_interest_question,
        "Appreciation and Depreciation": generate_appreciation_question,
        "Hire Purchase": generate_hire_purchase_question,
        "National Insurance": generate_ni_question,
        "Wages": generate_wages_question,
        "Commission": generate_commission_question,
    },
    "Geometry and Measure": {
        "Pythagoras Theorem": generate_pythagoras_question,
        "Area of a Circle": generate_circle_area_question,
        "Gradient": generate_gradient_question,
        "Volume": generate_volume_question,
        "Time Zones": generate_time_zone_question,
        "Tolerance": generate_tolerance_question,
    },
}

_N4_TOPICS = {
    "Numeracy": {
        "Fractions": generate_fraction_question_n4,
        "Percentages": generate_percentage_question_n4,
    },
    "Finance and Statistics": {
        "Simple Interest": generate_simple_interest_question_n4,
        "Appreciation and Depreciation": generate_appreciation_question_n4,
        "Hire Purchase": generate_hire_purchase_question_n4,
    },
    "Geometry and Measure": {
        "Pythagoras Theorem": generate_pythagoras_question_n4,
        "Area of a Circle": generate_circle_area_question_n4,
        "Gradient": generate_gradient_question_n4,
        "Volume": generate_volume_question_n4,
        "Time Zones": generate_time_zone_question_n4,
    },
}

_N5_NUMERACY_TOPICS = {
    "Numbers and Money": {
        "Compound Percentages": generate_compound_percentages,
        "Fractions": generate_num_fractions,
        "Ratio": generate_ratio,
        "Foreign Currency": generate_foreign_currency,
        "Liquid Volume": generate_liquid_volume,
    },
    "Data and Analysis": {
        "Stem and Leaf": generate_stem_and_leaf,
        "Pie Charts": generate_pie_charts,
        "Reading Bar Charts": generate_reading_bar_charts,
        "Probability": generate_num_probability,
    },
    "Time and Measurement": {
        "Reading Scale": generate_reading_scale,
        "Time Zones and Reading Tables": generate_time_zones_reading_tables,
    },
}

_HIGHER_TOPICS = {
    "Finance": {
        "Loans": generate_loans_question,
        "Mortgages": generate_mortgages_question,
        "Budgeting": generate_budgeting_question,
        "Reverse Percentages": generate_reverse_percentage_question,
    },
    "Statistics": {
        "Standard Deviation": generate_standard_deviation_question,
        "Probability": generate_probability_question,
    },
}

QUAL_REGISTRY = {
    "National 4": _N4_TOPICS,
    "National 5": _N5_TOPICS,
    "Higher": _HIGHER_TOPICS,
    "N5 Numeracy": _N5_NUMERACY_TOPICS,
}

# Kept for any code that referenced TOPIC_REGISTRY directly
TOPIC_REGISTRY = _N5_TOPICS

_N5_LEVELS = {
    "Numeracy": {
        "Probability": {
            "Level 1": generate_numeracy_probability_l1,
            "Level 2": generate_numeracy_probability_l2,
        },
    },
    "Finance and Statistics": {
        "Hire Purchase": {
            "Level 1": generate_hire_purchase_l1,
            "Level 2": generate_hire_purchase_l2,
        },
        "National Insurance": {
            "Level 1": generate_ni_l1,
            "Level 2": generate_ni_l2,
            "Level 3": generate_ni_l3,
        },
        "Wages": {
            "Level 1": generate_wages_l1,
            "Level 2": generate_wages_l2,
        },
    },
    "Geometry and Measure": {
        "Time Zones": {
            "Level 1": generate_time_zone_l1,
            "Level 2": generate_time_zone_l2,
            "Level 3": generate_time_zone_l3,
        },
        "Tolerance": {
            "Level 1": generate_tolerance_l1,
            "Level 2": generate_tolerance_l2,
            "Level 3": generate_tolerance_l3,
        },
    },
}

_N4_LEVELS = {}

_HIGHER_LEVELS = {}

_N5_NUMERACY_LEVELS = {}

_QUAL_LEVELS = {
    "National 4": _N4_LEVELS,
    "National 5": _N5_LEVELS,
    "Higher": _HIGHER_LEVELS,
    "N5 Numeracy": _N5_NUMERACY_LEVELS,
}

# Assessment sequence: one of each type in canonical order
_NUMERACY_ASSESSMENT_GENERATORS = [
    generate_compound_percentages,
    generate_liquid_volume,
    generate_foreign_currency,
    generate_time_zones_reading_tables,
    generate_reading_scale,
    generate_num_fractions,
    generate_ratio,
    generate_num_probability,
    generate_stem_and_leaf,
    generate_reading_bar_charts,
    generate_pie_charts,
]


def generate_numeracy_assessment():
    return [gen() for gen in _NUMERACY_ASSESSMENT_GENERATORS]


def get_levels(topic, question_type, qualification="National 5"):
    return _QUAL_LEVELS.get(qualification, {}).get(topic, {}).get(question_type, {})


def generate_question(topic, question_type, level=None, qualification="National 5"):
    if level:
        levels = get_levels(topic, question_type, qualification)
        if level in levels:
            return levels[level]()
    return QUAL_REGISTRY[qualification][topic][question_type]()
