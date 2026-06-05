from topics.numeracy.fractions import generate_fraction_question
from topics.numeracy.percentages import generate_percentage_question
from topics.finance_statistics.simple_interest import generate_simple_interest_question
from topics.finance_statistics.appreciation import generate_appreciation_question
from topics.finance_statistics.hire_purchase import generate_hire_purchase_question
from topics.geometry_measure.pythagoras import generate_pythagoras_question
from topics.geometry_measure.circle_area import generate_circle_area_question
from topics.geometry_measure.gradient import generate_gradient_question
from topics.geometry_measure.volume import generate_volume_question
from topics.geometry_measure.time_zones import (
    generate_time_zone_question,
    generate_time_zone_l1,
    generate_time_zone_l2,
    generate_time_zone_l3,
)

TOPIC_REGISTRY = {
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

# Maps topic → question_type → {level_name: generator} for types that have levels.
# Any question type listed here will show level-selection buttons in the UI.
LEVEL_REGISTRY = {
    "Geometry and Measure": {
        "Time Zones": {
            "Level 1": generate_time_zone_l1,
            "Level 2": generate_time_zone_l2,
            "Level 3": generate_time_zone_l3,
        }
    }
}


def get_levels(topic, question_type):
    """Return {level_name: generator} for this question type, or {} if none."""
    return LEVEL_REGISTRY.get(topic, {}).get(question_type, {})


def generate_question(topic, question_type, level=None):
    if level:
        levels = get_levels(topic, question_type)
        if level in levels:
            return levels[level]()
    return TOPIC_REGISTRY[topic][question_type]()
