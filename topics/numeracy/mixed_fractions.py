import random
from math import gcd

from core.models.question_model import Question

NOTES = """
**Mixed Fractions:**

- A **mixed fraction** has a whole number and a fraction, e.g. 3½.
- To find how many fractional parts are in a mixed number, **multiply the whole number by the
  denominator** and **add the numerator**.
- To write a mixed number as an **improper fraction**, put that total over the denominator.
- To change an improper fraction back, **divide the numerator by the denominator**: the answer is
  the whole number and the remainder is the new numerator.

**Example:** How many halves are in 2½?
- 2 × 2 = 4 halves, plus 1 half = **5 halves**

**Example:** Write 3¼ as an improper fraction.
- 3 × 4 = 12, 12 + 1 = 13
- 3¼ = **13/4**

**Example:** Write 17/5 as a mixed number.
- 17 ÷ 5 = 3 remainder 2
- 17/5 = **3 2/5**
"""

_SUP = str.maketrans("0123456789", "0123456789")


def _mixed(w, n, d):
    return f"{w} {n}/{d}"


def _pick(denoms=(2, 3, 4, 5, 6, 8, 10)):
    d = random.choice(denoms)
    n = random.choice([x for x in range(1, d) if gcd(x, d) == 1])
    return random.randint(1, 9), n, d


def _q(text, answer, scaffold, worked):
    return Question(
        question_text=text, correct_answer=answer, topic="Numeracy",
        question_type="Mixed Fractions", scaffold_steps=scaffold,
        worked_solution=worked, notes=NOTES,
    )


# Level 1 — how many fractional parts are in a mixed number (e.g. 2½ = 5 halves)
def generate_mixed_fractions_l1():
    w, n, d = _pick((2, 3, 4, 5, 8, 10))
    word = {2: "halves", 3: "thirds", 4: "quarters", 5: "fifths", 6: "sixths",
            8: "eighths", 10: "tenths"}[d]
    total = w * d + n
    return _q(
        f"How many {word} are in {_mixed(w, n, d)}?", total,
        [{"prompt": f"How many {word} are in the whole number {w}? ({w} × {d})", "answer": w * d},
         {"prompt": f"Add the extra {n} {word}", "answer": total}],
        [f"{w} whole{'s' if w > 1 else ''} = {w} × {d} = {w * d} {word}",
         f"{w * d} + {n} = **{total} {word}**"],
    )


# Level 2 — mixed number to improper fraction
def generate_mixed_fractions_l2():
    w, n, d = _pick()
    top = w * d + n
    return _q(
        f"Write {_mixed(w, n, d)} as an improper fraction.", f"{top}/{d}",
        [{"prompt": f"Multiply the whole number by the denominator, then add the numerator "
                    f"({w} × {d} + {n})", "answer": top}],
        [f"{w} × {d} = {w * d}, {w * d} + {n} = {top}", f"{_mixed(w, n, d)} = **{top}/{d}**"],
    )


# Level 3 — improper fraction to mixed number
def generate_mixed_fractions_l3():
    w, n, d = _pick()
    top = w * d + n
    return _q(
        f"Write {top}/{d} as a mixed number.", _mixed(w, n, d),
        [{"prompt": f"How many whole numbers are there in {top}/{d}? ({top} ÷ {d}, ignoring the remainder)",
          "answer": w},
         {"prompt": "What is the remainder (the new numerator)?", "answer": n}],
        [f"{top} ÷ {d} = {w} remainder {n}", f"{top}/{d} = **{_mixed(w, n, d)}**"],
    )


def generate_mixed_fractions_question():
    return random.choice([generate_mixed_fractions_l1, generate_mixed_fractions_l2,
                          generate_mixed_fractions_l3])()
