from topics.numeracy.fractions import generate_fraction_question, generate_fraction_question_n4
from topics.numeracy.percentages import generate_percentage_question, generate_percentage_question_n4
from topics.finance_statistics.simple_interest import generate_simple_interest_question, generate_simple_interest_question_n4
from topics.finance_statistics.appreciation import generate_appreciation_question, generate_appreciation_question_n4
from topics.finance_statistics.hire_purchase import (
    generate_hire_purchase_question,
    generate_hire_purchase_question_n4,
    generate_hire_purchase_l1,
    generate_hire_purchase_l2,
)
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

_N5_TOPICS = {
    "Numeracy": {
        "Fractions": generate_fraction_question,
        "Percentages": generate_percentage_question,
    },
    "Finance and Statistics": {
        "Simple Interest": generate_simple_interest_question,
        "Appreciation and Depreciation": generate_appreciation_question,
        "Hire Purchase": generate_hire_purchase_question,
    },
    "Geometry and Measure": {
        "Pythagoras Theorem": generate_pythagoras_question,
        "Area of a Circle": generate_circle_area_question,
        "Gradient": generate_gradient_question,
        "Volume": generate_volume_question,
        "Time Zones": generate_time_zone_question,
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

QUAL_REGISTRY = {
    "National 5": _N5_TOPICS,
    "National 4": _N4_TOPICS,
}

# Kept for any code that referenced TOPIC_REGISTRY directly
TOPIC_REGISTRY = _N5_TOPICS

_N5_LEVELS = {
    "Finance and Statistics": {
        "Hire Purchase": {
            "Level 1": generate_hire_purchase_l1,
            "Level 2": generate_hire_purchase_l2,
        }
    },
    "Geometry and Measure": {
        "Time Zones": {
            "Level 1": generate_time_zone_l1,
            "Level 2": generate_time_zone_l2,
            "Level 3": generate_time_zone_l3,
        }
    },
}

_N4_LEVELS = {}

_QUAL_LEVELS = {
    "National 5": _N5_LEVELS,
    "National 4": _N4_LEVELS,
}


def get_levels(topic, question_type, qualification="National 5"):
    return _QUAL_LEVELS.get(qualification, {}).get(topic, {}).get(question_type, {})


def generate_question(topic, question_type, level=None, qualification="National 5"):
    if level:
        levels = get_levels(topic, question_type, qualification)
        if level in levels:
            return levels[level]()
    return QUAL_REGISTRY[qualification][topic][question_type]()
