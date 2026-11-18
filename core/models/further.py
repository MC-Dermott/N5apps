"""Helpers for the 'further question types' added from the Higher specification examples (Nov 2026): each generator
returns a multipart Question whose parts carry a mark allocation in metadata["marks"] (the homework builder in the
Higher Apps pipeline reuses these same generators with a fixed seed, so app and homework never disagree)."""
import math
from core.models.question_model import Question, make_part, multipart_worked_solution


def g(x, dp=2):
    x = round(x + 0.0, dp)
    s = f"{x:,.{dp}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def r2(x):
    return round(x + 1e-9, 2)


def gbp(x):
    return f"£{x:,}" if isinstance(x, int) else f"£{x:,.2f}"


def fv_end(p, r, n):
    return p * ((1 + r) ** n - 1) / r


def pv_end(p, r, n):
    return p * (1 - (1 + r) ** -n) / r


def pmt(P, r, n):
    return P * r / (1 - (1 + r) ** -n)


def mon(annual):
    return (1 + annual) ** (1 / 12) - 1


def part(label, text, ans, worked, steps=None, marks=1, options=None, explain=False):
    p = make_part(label, text, ans, scaffold_steps=steps or [], worked_solution=worked, options=options, explain=explain)
    p.metadata["marks"] = marks
    return p


def step(prompt, answer):
    return {"prompt": prompt, "answer": answer}


def question(topic, qtype, context, parts, notes, level, extra=None):
    md = {"level": level, "marks": sum(p.metadata.get("marks", 1) for p in parts), "further": True}
    md.update(extra or {})
    return Question(question_text=context, correct_answer=parts[0].correct_answer, topic=topic, question_type=qtype,
                    notes=notes, parts=parts, worked_solution=multipart_worked_solution(parts), metadata=md)


def md_table(headers, rows):
    out = ["| " + " | ".join(str(h) for h in headers) + " |", "|" + "---|" * len(headers)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)
