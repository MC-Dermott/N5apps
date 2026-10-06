import random
from fractions import Fraction

from core.models.question_model import Question

NOTES = """
**Fractions, Decimals and Percentages:**

- **Fraction → decimal:** divide the numerator by the denominator.
- **Decimal → percentage:** multiply by 100 (move the point 2 places right).
- **Percentage → decimal:** divide by 100 (move the point 2 places left).
- **Percentage → fraction:** write it over 100, then simplify.
- **Fraction → percentage:** change to a decimal first, then × 100.

**Example:** Write 3/8 as a decimal.
- 3 ÷ 8 = **0·375**

**Example:** Write 0·35 as a percentage.
- 0·35 × 100 = **35%**

**Example:** Write 60% as a fraction in its simplest form.
- 60/100 = **3/5**

**Example:** Write 0·35 as a fraction in its simplest form.
- 0·35 = 35/100 = **7/20**
"""

# fractions with terminating decimals: (n, d)
_FRACS = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 8), (3, 8), (5, 8), (7, 8),
          (1, 10), (3, 10), (7, 10), (9, 10), (1, 20), (3, 20), (7, 20), (9, 20), (1, 25), (3, 25),
          (7, 25), (11, 20), (13, 20)]


def _num(x):
    return format(float(x), "g")


def _q(text, answer, scaffold, worked):
    return Question(question_text=text, correct_answer=answer, topic="Numeracy",
                    question_type="Fractions, Decimals and Percentages",
                    scaffold_steps=scaffold, worked_solution=worked, notes=NOTES)


def _simplest_pct(n, d):
    return float(Fraction(n, d) * 100)


# Level 1 — fraction to decimal and decimal to percentage
def generate_equivalences_l1():
    n, d = random.choice(_FRACS)
    dec = n / d
    if random.random() < 0.5:
        return _q(f"Write {n}/{d} as a decimal.", dec,
                  [{"prompt": f"Divide the numerator by the denominator ({n} ÷ {d})", "answer": dec}],
                  [f"{n} ÷ {d} = **{_num(dec)}**"])
    pct = round(dec * 100, 4)
    return _q(f"Write {_num(dec)} as a percentage. (Type the number only, without the % sign.)", pct,
              [{"prompt": f"Multiply {_num(dec)} by 100", "answer": pct}],
              [f"{_num(dec)} × 100 = **{_num(pct)}%**"])


# Level 2 — fraction to percentage, percentage to fraction
def generate_equivalences_l2():
    n, d = random.choice(_FRACS)
    pct = _simplest_pct(n, d)
    if random.random() < 0.5:
        return _q(f"Write {n}/{d} as a percentage. (Type the number only, without the % sign.)", pct,
                  [{"prompt": f"Write {n}/{d} as a decimal", "answer": n / d},
                   {"prompt": "Multiply the decimal by 100", "answer": pct}],
                  [f"{n} ÷ {d} = {_num(n / d)}", f"{_num(n / d)} × 100 = **{_num(pct)}%**"])
    f = Fraction(n, d)
    return _q(f"Write {_num(pct)}% as a fraction in its simplest form.", f"{f.numerator}/{f.denominator}",
              [{"prompt": f"Write {_num(pct)}% as a fraction out of 100: what is the numerator "
                          f"when the denominator is 100?", "answer": pct}],
              [f"{_num(pct)}% = {_num(pct)}/100", f"Simplify: **{f.numerator}/{f.denominator}**"]
              if pct == int(pct) else
              [f"{_num(pct)}% = {_num(pct / 100)}",
               f"{_num(pct / 100)} = **{f.numerator}/{f.denominator}** in its simplest form"])


# Level 3 — decimal to fraction in simplest form
def generate_equivalences_l3():
    n, d = random.choice([f for f in _FRACS if f[1] in (4, 5, 8, 10, 20, 25)])
    dec = n / d
    dp = len(_num(dec).split(".")[1])
    top = round(dec * 10 ** dp)
    return _q(f"Write {_num(dec)} as a fraction in its simplest form.", f"{n}/{d}",
              [{"prompt": f"Write {_num(dec)} as a fraction out of {10 ** dp}: what is the numerator?",
                "answer": top}],
              [f"{_num(dec)} = {top}/{10 ** dp}", f"Simplify: **{n}/{d}**"])


def generate_equivalences_question():
    return random.choice([generate_equivalences_l1, generate_equivalences_l2, generate_equivalences_l3])()
