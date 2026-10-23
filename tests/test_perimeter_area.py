"""Stress test for the Perimeter and Area question types: venv/bin/python tests/test_perimeter_area.py

600 questions per level: no exceptions, sensible answers, no formatting artefacts, the last scaffold
step equals the answer, no distractor within 0.01 of the answer or of each other, every diagram
renders, and costed questions say how much per metre / square metre.
"""
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.engine.question_factory import generate_question, get_levels  # noqa: E402
from core.ui import composite_shapes  # noqa: E402

BAD = re.compile(r"e\+|nan|None|\{|\}|\.0{3,}|\d\.\d{4,}")


def check(q, level, render=True):
    text = q.question_text + " ".join(q.worked_solution) + " ".join(str(s["prompt"]) for s in q.scaffold_steps)
    assert not BAD.search(text), (level, text)
    ans = q.correct_answer
    assert isinstance(ans, (int, float)) and ans > 0, (level, ans, q.question_text)
    if q.scaffold_steps:
        assert abs(q.scaffold_steps[-1]["answer"] - ans) < 0.011, (level, q.scaffold_steps[-1], ans)
    assert q.worked_solution and "**" in q.worked_solution[-1], (level, q.worked_solution)
    vals = [d["value"] for d in q.distractors]
    for i, v in enumerate(vals):
        assert abs(v - ans) >= 0.01 and v > 0, (level, v, ans)
        assert all(abs(v - w) >= 0.01 for w in vals[:i]), (level, vals)
    if "per metre" in q.question_text or "per square metre" in q.question_text:
        assert "Calculate the cost" in q.question_text, q.question_text
        assert abs(q.scaffold_steps[-1]["answer"] - ans) < 0.011
        assert any("Cost" in w for w in q.worked_solution), q.worked_solution
    p = q.metadata.get("diagram_params")
    if p and render:
        buf = io.BytesIO()
        getattr(composite_shapes, p["kind"])(*p["args"], buf)
        assert buf.getvalue()[:4] == b"\x89PNG", (level, p)


def check_circle_levels():
    """Costed circle / semi-circle / quarter-circle questions give the radius only; whole-edge questions add
    the straight edge(s); every answer is recomputed from the text with the same 2 d.p. rounding."""
    import math
    R = lambda x: round(x + 1e-9, 2)
    levels = get_levels("Geometry and Measure", "Perimeter", "National 5")
    whole = 0
    for name, frac in (("Circumference of Circles", 1), ("Arc Length of Semi-circles", 2),
                       ("Arc Length of Quarter Circles", 4)):
        for _ in range(400):
            q = levels[name](); t = q.question_text
            pi = 3.14 if "3.14" in t else math.pi
            kind, v = re.search(r"(radius|diameter) (?:of )?([\d.]+)", t).groups()
            r = float(v) if kind == "radius" else float(v) / 2
            exp = R(R(pi * 2 * r) / frac)
            if "whole edge" in t or "edged all the way round" in t:
                exp = R(exp + 2 * r); whole += 1        # the diameter, or the two radii
            m = re.search(r"£([\d.]+) per metre", t)
            if m:
                assert kind == "radius", t
                exp = R(exp * float(m.group(1)))
            assert abs(q.correct_answer - exp) < 0.011, (t, q.correct_answer, exp)
    assert whole > 50, whole
    print("ok circle levels: radius-only costs, whole-edge questions", whole)


def check_area_levels():
    """Costed circle / semi-circle / quarter-circle area questions give the radius only; every answer is
    recomputed from the text with the same 2 d.p. rounding."""
    import math
    R = lambda x: round(x + 1e-9, 2)
    levels = get_levels("Geometry and Measure", "Area", "National 5")
    for name, frac in (("Area of Circles", 1), ("Area of Semi-circles", 2), ("Area of Quarter Circles", 4)):
        for _ in range(400):
            q = levels[name](); t = q.question_text
            pi = 3.14 if "3.14" in t else math.pi
            kind, v = re.search(r"(radius|diameter) (?:of )?([\d.]+)", t).groups()
            r = float(v) if kind == "radius" else float(v) / 2
            exp = R(R(pi * r * r) / frac)
            m = re.search(r"£([\d.]+) per square metre", t)
            if m:
                assert kind == "radius", t
                exp = R(exp * float(m.group(1)))
            assert abs(q.correct_answer - exp) < 0.011, (t, q.correct_answer, exp)
    print("ok area circle levels: radius-only costs, answers recomputed")


def main():
    costed = 0
    for qtype in ("Perimeter", "Area"):
        levels = get_levels("Geometry and Measure", qtype, "National 5")
        assert levels, qtype
        for name in list(levels) + [None]:
            for i in range(600):
                q = (levels[name]() if name else generate_question("Geometry and Measure", qtype,
                                                                   qualification="National 5"))
                check(q, f"{qtype}/{name}", render=i % 12 == 0)   # every 12th diagram is drawn
                costed += "per metre" in q.question_text or "per square metre" in q.question_text
            print("ok", qtype, name)
    assert costed > 1000, costed
    try:
        generate_question("Geometry and Measure", "Perimeter and Area", qualification="National 5")
    except Exception:
        pass
    else:
        raise AssertionError("the old combined type should be gone")
    check_circle_levels()
    check_area_levels()
    print("all good —", costed, "costed questions")


if __name__ == "__main__":
    main()
