import random
from fractions import Fraction

from core.models.question_model import Question

NOTES = """
**Fractions and Percentages of Shapes:**

- Count the **total** number of equal parts in the shape and the number that are **shaded**.
- **Fraction shaded** = shaded parts ÷ total parts — simplify your answer.
- **Percentage shaded** = fraction shaded as a decimal × 100.
- To find the **area shaded**, find the area of one part first (total area ÷ total parts), then
  multiply by the number of shaded parts.

**Example:** 6 out of 20 equal squares are shaded. What fraction is shaded?
- 6/20 = **3/10**

**Example:** 6 out of 20 equal squares are shaded. What percentage is shaded?
- 6 ÷ 20 = 0·3, 0·3 × 100 = **30%**
"""

_DIAG = "topics.numeracy.core_skills_diagrams"
_GRIDS = [(2, 5), (4, 5), (2, 10), (5, 5), (4, 10), (5, 10), (2, 4), (3, 4), (2, 6), (4, 6), (3, 8)]


def _grid():
    rows, cols = random.choice(_GRIDS)
    n = rows * cols
    shaded = random.choice([k for k in range(1, n) if k % 5 and n % 5 == 0] or range(1, n))
    if n % 5 == 0:
        shaded = random.choice([k for k in range(1, n) if k % 5 != 0] + [k for k in range(5, n, 5)])
    meta = {"diagram": "composite_shape", "diagram_params": {
        "module_path": _DIAG, "kind": "shaded_grid", "args": [rows, cols, shaded], "width": 260}}
    return rows, cols, n, shaded, meta


def _fmt(x):
    return format(float(x), "g")


def _q(text, answer, scaffold, worked, meta, qtype="Fractions and Percentages of Shapes"):
    return Question(question_text=text, correct_answer=answer, topic="Numeracy", question_type=qtype,
                    scaffold_steps=scaffold, worked_solution=worked, notes=NOTES, metadata=meta)


# Level 1 — fraction of the shape that is shaded
def generate_shapes_fp_l1():
    rows, cols, n, k, meta = _grid()
    f = Fraction(k, n)
    return _q("What fraction of this shape is shaded? Give your answer in its simplest form.",
              f"{f.numerator}/{f.denominator}",
              [{"prompt": "How many equal parts are there altogether?", "answer": n},
               {"prompt": "How many parts are shaded?", "answer": k}],
              [f"{k} parts shaded out of {n}: {k}/{n}",
               f"Simplest form: **{f.numerator}/{f.denominator}**" if f.denominator != n else f"**{k}/{n}**"],
              meta)


# Level 2 — percentage of the shape that is shaded
def generate_shapes_fp_l2():
    while True:
        rows, cols, n, k, meta = _grid()
        if 100 % n == 0 or (k / n * 100) == round(k / n * 100, 1):
            break
    pct = k / n * 100
    return _q("What percentage of this shape is shaded? (Type the number only, without the % sign.)", pct,
              [{"prompt": "Write the fraction shaded as a decimal (shaded ÷ total)", "answer": k / n},
               {"prompt": "Multiply the decimal by 100 to get the percentage", "answer": pct}],
              [f"{k}/{n} = {_fmt(k / n)}", f"{_fmt(k / n)} × 100 = **{_fmt(pct)}%**"], meta)


# Level 3 — area of the shaded part
def generate_shapes_fp_l3():
    rows, cols, n, k, meta = _grid()
    part = random.choice([2, 3, 4, 5, 10, 25])
    total = part * n
    answer = part * k
    return _q(f"The whole shape has an area of {total} cm². What is the area of the shaded part?",
              answer,
              [{"prompt": f"What is the area of one part? ({total} ÷ {n})", "answer": part},
               {"prompt": f"There are {k} shaded parts. What is the shaded area?", "answer": answer}],
              [f"One part = {total} ÷ {n} = {part} cm²", f"Shaded area = {k} × {part} = **{answer} cm²**"],
              meta)


def generate_shapes_fp_question():
    return random.choice([generate_shapes_fp_l1, generate_shapes_fp_l2, generate_shapes_fp_l3])()
