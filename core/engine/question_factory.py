import random

from topics.numeracy.fractions import (
    generate_fraction_question,
    generate_fraction_question_n4,
    generate_fraction_exam_style,
    generate_fraction_exam_l1,
    generate_fraction_exam_l2,
    generate_fraction_exam_l3,
    generate_fraction_addition,
    generate_fraction_subtraction,
    generate_fraction_three,
    generate_improper_fraction_conversion,
    generate_fraction_simplification,
)
from topics.numeracy.percentages import (
    generate_percentage_question,
    generate_percentage_question_n4,
    generate_percentage_l1,
    generate_percentage_l2,
    generate_percentage_multiplier,
    generate_percentage_single_change,
    generate_percentage_appreciation,
    generate_percentage_depreciation,
    generate_percentage_mixed_changes,
)
from topics.numeracy.probability import (
    generate_probability_question as generate_numeracy_probability_question,
    generate_probability_l1 as generate_numeracy_probability_l1,
    generate_probability_l2 as generate_numeracy_probability_l2,
)
from topics.numeracy.ratio import (
    generate_ratio_l1 as generate_numeracy_ratio_l1,
    generate_ratio_l2 as generate_numeracy_ratio_l2,
)
from topics.numeracy.direct_proportion import (
    generate_direct_proportion_l1,
    generate_direct_proportion_l2,
    generate_direct_proportion_l3,
)
from topics.numeracy.currency_exchange import (
    generate_currency_question,
    generate_currency_l1,
    generate_currency_l2,
    generate_currency_l3,
    generate_currency_l4,
    generate_currency_l5,
)
from topics.numeracy.pie_charts import (
    generate_pie_charts_question as generate_numeracy_pie_charts_question,
    generate_pie_charts_l1,
    generate_pie_charts_l2,
    generate_pie_charts_l3,
    generate_pie_charts_l4,
)
from topics.rounding.rounding import (
    generate_rounding_decimal_places,
    generate_rounding_money,
    generate_rounding_significant_figures,
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
from topics.finance_statistics.interest import (
    generate_interest_question,
    generate_interest_l1,
    generate_interest_l2,
    generate_interest_l3,
)
from topics.finance_statistics.savings_schedule import generate_savings_schedule_question
from topics.finance_statistics.income_tax_ni import (
    generate_tax_ni_question,
    generate_gross_annual_pay,
    generate_income_tax,
    generate_higher_ni,
    generate_net_monthly_income,
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
from topics.numeracy_assessment.foreign_currency import (
    generate_foreign_currency,
    generate_foreign_currency_l1,
    generate_foreign_currency_l2,
    generate_foreign_currency_l3,
    generate_foreign_currency_l4,
    generate_foreign_currency_l5,
)
from topics.numeracy_assessment.time_zones_reading_tables import generate_time_zones_reading_tables
from topics.numeracy_assessment.reading_scale import generate_reading_scale
from topics.numeracy_assessment.ratio import generate_ratio
from topics.numeracy_assessment.probability import generate_probability as generate_num_probability
from topics.numeracy_assessment.stem_and_leaf import generate_stem_and_leaf
from topics.numeracy_assessment.reading_bar_charts import generate_reading_bar_charts
from topics.numeracy_assessment.pie_charts import generate_pie_charts

def generate_ratio_and_proportion_question(calc_mode=False):
    return random.choice([
        generate_numeracy_ratio_l1,
        generate_numeracy_ratio_l2,
        generate_direct_proportion_l1,
        generate_direct_proportion_l2,
        generate_direct_proportion_l3,
    ])(calc_mode=calc_mode)


_N5_TOPICS = {
    "Numeracy": {
        "Fractions": generate_fraction_question,
        "Fractions (Exam Style)": generate_fraction_exam_style,
        "3 Fractions": generate_fraction_three,
        "Percentages": generate_percentage_question,
        "Probability": generate_numeracy_probability_question,
        "Ratio and Direct Proportion": generate_ratio_and_proportion_question,
        "Currency Exchange": generate_currency_question,
        "Pie Charts": generate_numeracy_pie_charts_question,
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
    "Rounding": {
        "Decimal Places": generate_rounding_decimal_places,
        "Rounding Money": generate_rounding_money,
        "Significant Figures": generate_rounding_significant_figures,
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
        "Fractions (Exam Style)": generate_fraction_exam_style,
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
        "Interest": generate_interest_question,
        "Savings Schedule": generate_savings_schedule_question,
        "Income Tax and National Insurance": generate_tax_ni_question,
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
        "Fractions": {
            "Add Fractions": generate_fraction_addition,
            "Subtract Fractions": generate_fraction_subtraction,
            "Improper Fractions": generate_improper_fraction_conversion,
            "Simplify Fractions": generate_fraction_simplification,
        },
        "Fractions (Exam Style)": {
            "Two Fractions, Subtract from 1": generate_fraction_exam_l1,
            "Two Fractions, Subtract from Several Items": generate_fraction_exam_l2,
            "Three Fractions, Subtract from a Whole": generate_fraction_exam_l3,
        },
        "Percentages": {
            "Percentage of an Amount": generate_percentage_l1,
            "One Percentage of Another": generate_percentage_l2,
            "Calculating the Multiplier": generate_percentage_multiplier,
            "Calculating Single Changes": generate_percentage_single_change,
            "Appreciation": generate_percentage_appreciation,
            "Depreciation": generate_percentage_depreciation,
            "Mixed Changes": generate_percentage_mixed_changes,
        },
        "Probability": {
            "Single Event": generate_numeracy_probability_l1,
            "Combined Events": generate_numeracy_probability_l2,
        },
        "Ratio and Direct Proportion": {
            "Ratio: Find a Share": generate_numeracy_ratio_l1,
            "Ratio: Find the Total": generate_numeracy_ratio_l2,
            "Direct Proportion: Scaling": generate_direct_proportion_l1,
            "Direct Proportion: Best Value": generate_direct_proportion_l2,
            "Direct Proportion: Unit Conversion": generate_direct_proportion_l3,
        },
        "Currency Exchange": {
            "Basic Exchange": generate_currency_l1,
            "Changing, Spending, and Changing Back": generate_currency_l2,
            "Exchange with Restrictions": generate_currency_l3,
            "Converting Between Two Currencies": generate_currency_l4,
            "Calculating the Exchange Rate": generate_currency_l5,
        },
        "Pie Charts": {
            "Fraction from the Angle": generate_pie_charts_l1,
            "Finding the Missing Angle": generate_pie_charts_l2,
            "Calculating the Amount": generate_pie_charts_l3,
            "Working from One Segment": generate_pie_charts_l4,
        },
    },
    "Finance and Statistics": {
        "Hire Purchase": {
            "Standard Instalments": generate_hire_purchase_l1,
            "Different Final Instalment": generate_hire_purchase_l2,
        },
        "National Insurance": {
            "Single Band": generate_ni_l1,
            "Two Bands": generate_ni_l2,
            "Net Pay": generate_ni_l3,
        },
        "Wages": {
            "Gross Pay with Overtime": generate_wages_l1,
            "Net Pay after Deductions": generate_wages_l2,
        },
    },
    "Geometry and Measure": {
        "Time Zones": {
            "Time Zone Conversion": generate_time_zone_l1,
            "Journey Times Across Zones": generate_time_zone_l2,
            "Stopover Journeys": generate_time_zone_l3,
        },
        "Tolerance": {
            "Absolute Tolerance": generate_tolerance_l1,
            "Tolerance with Unit Conversion": generate_tolerance_l2,
            "Percentage Tolerance": generate_tolerance_l3,
        },
    },
}

_N4_LEVELS = {}

_HIGHER_LEVELS = {
    "Finance": {
        "Interest": {
            "Single Deposit": generate_interest_l1,
            "Multiple Deposits": generate_interest_l2,
            "Minimum Deposit for a Goal": generate_interest_l3,
        },
        "Income Tax and National Insurance": {
            "Gross Annual Pay": generate_gross_annual_pay,
            "Income Tax": generate_income_tax,
            "National Insurance": generate_higher_ni,
            "Net Monthly Income": generate_net_monthly_income,
        },
    },
}

_N5_NUMERACY_LEVELS = {
    "Numbers and Money": {
        "Fractions (Exam Style)": {
            "Two Fractions, Subtract from 1": generate_fraction_exam_l1,
            "Two Fractions, Subtract from Several Items": generate_fraction_exam_l2,
            "Three Fractions, Subtract from a Whole": generate_fraction_exam_l3,
        },
        "Foreign Currency": {
            "Basic Exchange": generate_foreign_currency_l1,
            "Changing, Spending, and Changing Back": generate_foreign_currency_l2,
            "Holiday Spending Money": generate_foreign_currency_l3,
            "Converting Between Two Currencies": generate_foreign_currency_l4,
            "Calculating the Exchange Rate": generate_foreign_currency_l5,
        },
    },
}

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


# ---------------------------------------------------------------------------
# Calculator vs Non-calculator mode
#
# _CALC_MODE_AWARE: generator functions that accept a `calc_mode` kwarg and
# restrict their own number generation (single-digit/power-of-ten multipliers
# and divisors, ≤2 d.p. decimals) when it's True.
# _ALWAYS_CALC_SAFE: generator functions whose output already satisfies the
# non-calculator constraint unconditionally — called with no kwarg either way.
#
# Higher is deliberately excluded entirely (no non-calculator mode there), as
# are any topics whose arithmetic can't be made non-calc-safe without
# falsifying the numbers (e.g. real exchange rates, compounding, π).
# ---------------------------------------------------------------------------

_CALC_MODE_AWARE = {
    generate_ni_question, generate_ni_l1, generate_ni_l2, generate_ni_l3,
    generate_ratio_and_proportion_question,
    generate_numeracy_ratio_l1, generate_numeracy_ratio_l2,
    generate_direct_proportion_l1, generate_direct_proportion_l2, generate_direct_proportion_l3,
    generate_percentage_question, generate_percentage_l1, generate_percentage_single_change,
    generate_percentage_appreciation, generate_percentage_depreciation, generate_percentage_mixed_changes,
    generate_gradient_question, generate_gradient_question_n4,
    generate_tolerance_question, generate_tolerance_l1, generate_tolerance_l2, generate_tolerance_l3,
    generate_rounding_significant_figures,
    generate_liquid_volume, generate_num_probability,
}

_ALWAYS_CALC_SAFE = {
    generate_fraction_question, generate_fraction_question_n4,
    generate_fraction_exam_style, generate_fraction_exam_l1, generate_fraction_exam_l2, generate_fraction_exam_l3,
    generate_fraction_addition, generate_fraction_subtraction, generate_fraction_three,
    generate_improper_fraction_conversion, generate_fraction_simplification,
    generate_percentage_question_n4, generate_percentage_multiplier,
    generate_numeracy_probability_question, generate_numeracy_probability_l1, generate_numeracy_probability_l2,
    generate_numeracy_pie_charts_question, generate_pie_charts_l1, generate_pie_charts_l2,
    generate_pie_charts_l3, generate_pie_charts_l4,
    generate_simple_interest_question, generate_simple_interest_question_n4,
    generate_commission_question,
    generate_time_zone_question, generate_time_zone_question_n4,
    generate_time_zone_l1, generate_time_zone_l2, generate_time_zone_l3,
    generate_stem_and_leaf, generate_pie_charts, generate_reading_bar_charts,
    generate_reading_scale, generate_num_fractions, generate_time_zones_reading_tables,
}

_CALC_MODE_SAFE = _CALC_MODE_AWARE | _ALWAYS_CALC_SAFE


def _invoke(func, calc_mode):
    if calc_mode and func in _CALC_MODE_AWARE:
        return func(calc_mode=True)
    return func()


def calc_mode_available(topic, question_type, level=None, qualification="National 5"):
    """Whether a non-calculator variant exists for this exact topic/type/level selection."""
    if level:
        func = get_levels(topic, question_type, qualification).get(level)
    else:
        func = QUAL_REGISTRY.get(qualification, {}).get(topic, {}).get(question_type)
    return func in _CALC_MODE_SAFE if func else False


def generate_question(topic, question_type, level=None, qualification="National 5", calc_mode=False):
    if level:
        levels = get_levels(topic, question_type, qualification)
        if level in levels:
            return _invoke(levels[level], calc_mode)
    return _invoke(QUAL_REGISTRY[qualification][topic][question_type], calc_mode)
