"""Shared helpers for the Perimeter and Area question types (split from the old Perimeter and Area).

Every shape maker returns a *spec* (a dict, see `finish`). `finish` turns a spec into either the plain
"calculate the perimeter / area" question or the exam-style costed version (price per metre for a
perimeter, per square metre for an area), the way the worksheets ask them — the cost line is added to
the text, the scaffold, the worked solution and the distractors, so each shape type can be asked both
ways without a second set of makers.

Spec keys:
  desc    the shape described, no instruction ("A paddock is a rectangle with a semi-circle ...")
  instr   the plain instruction ("Calculate its perimeter.")
  ans     the perimeter (m, cm, mm) or area (m², ...)
  u       the unit of ans's length (a costed question needs "m")
  lines   worked-solution lines; the last is the quantity, in **bold**
  steps   scaffold steps for the quantity (not including the final one)
  wrong   [(value, mistake)] wrong quantities; costed questions multiply each by the price
  diag    metadata for the diagram
  kind    "length" or "area"
  item    optional (what, What) overriding the random material, e.g. ("fencing", "Fencing")
  final   False for a one-step plain question (no scaffold)
  tail    "Take π = 3.14." / "Give your answer to 2 decimal places."
  alt     optional (value, mistake): the other quantity (area for a perimeter), also priced
"""
import math
import random

from core.models.distractors import distractors
from core.models.question_model import Question

TOPIC = "Geometry and Measure"

LENGTH_ITEMS = [("fencing", "Fencing"), ("edging strip", "Edging strip"), ("railing", "Railing"),
                ("hedging", "Hedging")]
AREA_ITEMS = [("turf", "Turf"), ("paving", "Paving"), ("topsoil", "Topsoil"), ("gravel", "Gravel"),
              ("harling", "Harling")]
LENGTH_PRICES = [1.85, 2.5, 2.75, 3.2, 3.8, 4.5, 5.4, 6.2, 7.1]
AREA_PRICES = [4.2, 4.8, 9.8, 12.5, 16.5, 18, 26.5, 28, 35]


def r2(x):
    return round(x + 1e-9, 2)


def g(x):
    x = float(x)
    return str(int(x)) if x == int(x) else f"{x:.6f}".rstrip("0").rstrip(".")


def pi_for(non_calc):
    return (3.14, "3.14") if non_calc else (math.pi, "π")


def diagram(kind, *args):
    return {"diagram": "composite_shape", "diagram_params": {"kind": kind, "args": list(args)}}


def not_whole(A, per):
    """Nudge A so that A ÷ per isn't a whole number (there must be something to round up)."""
    while abs(A / per - round(A / per)) < 0.02:
        A = round(A + 0.37, 2)
    return A


def tail_for(non_calc):
    return "Take π = 3.14." if non_calc else "Give your answer to 2 decimal places."


def finish(spec, cost, qtype, notes, final_prompt):
    """A Question from a shape spec, plain or costed (see the module docstring)."""
    ans, length = spec["ans"], spec["kind"] == "length"
    wrong = [(v, m) for v, m in spec["wrong"]]
    if spec.get("alt"):
        wrong.append(spec["alt"])
    wrong = [(v, m) for v, m in wrong if v is not None and v > 0]        # no negative "lengths"
    tail = spec.get("tail", "")
    if not cost:
        text = " ".join(x for x in (spec["desc"], spec["instr"], tail) if x)
        steps = list(spec["steps"])
        if spec.get("final", True):
            steps.append({"prompt": final_prompt, "answer": ans})
        return Question(question_text=text, correct_answer=ans, topic=TOPIC, question_type=qtype,
                        scaffold_steps=steps, worked_solution=spec["lines"], notes=notes,
                        metadata=spec["diag"], distractors=distractors(ans, wrong))
    price = random.choice(LENGTH_PRICES if length else AREA_PRICES)
    what, What = spec.get("item") or random.choice(LENGTH_ITEMS if length else AREA_ITEMS)
    per = "metre" if length else "square metre"
    answer = r2(ans * price)
    text = " ".join(x for x in (spec["desc"], f"{What} costs £{price:.2f} per {per}.",
                                f"Calculate the cost of the {what}.", tail) if x)
    lines = list(spec["lines"])
    lines[-1] = lines[-1].replace("**", "")
    lines.append(f"Cost = {g(ans)} × £{price:.2f} = **£{answer:.2f}**")
    steps = list(spec["steps"])
    if spec.get("final", True):
        steps.append({"prompt": final_prompt, "answer": ans})
    steps.append({"prompt": f"Cost, {'perimeter' if length else 'area'} × price per {per}", "answer": answer})
    cwrong = [(r2(v * price), m) for v, m in wrong if v is not None]
    cwrong.append((ans, f"that's the {'perimeter' if length else 'area'} — now multiply by the price "
                        f"per {per}."))
    return Question(question_text=text, correct_answer=answer, topic=TOPIC, question_type=qtype,
                    scaffold_steps=steps, worked_solution=lines, notes=notes, metadata=spec["diag"],
                    distractors=distractors(answer, cwrong))
