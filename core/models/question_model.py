from dataclasses import dataclass, field
from typing import Any
import random


@dataclass
class Question:
    question_text: str
    correct_answer: Any
    topic: str
    question_type: str
    qid: int = field(default_factory=lambda: random.randint(10000, 99999))
    scaffold_steps: list[dict] = field(default_factory=list)
    worked_solution: list[str] = field(default_factory=list)
    notes: str = ""
    metadata: dict = field(default_factory=dict)
    # Multipart questions: `question_text` is the shared context shown above every part,
    # and each part is its own Question (own text, answer, scaffold, worked solution).
    parts: list = field(default_factory=list)
    # Recognised wrong answers, each {"value": ..., "mistake": str} — the real common errors
    # from the SQA course reports / marking instructions. A pupil whose wrong answer matches
    # one is told what went wrong ("Common mistake: ...").
    distractors: list = field(default_factory=list)


def make_part(label, question_text, correct_answer, scaffold_steps=None, worked_solution=None,
              options=None, explain=False, distractors=None):
    """One part of a multipart question. `label` is shown as "Part <label>" — e.g. "(a)",
    "(b)(i)". `options` renders a radio choice instead of a text box. `explain=True` marks an
    unmarked written-answer part (e.g. "Explain your answer"): practice mode shows a reveal
    button for `correct_answer` (the expected answer), and tests skip it."""
    metadata = {"label": label}
    if options:
        metadata["options"] = list(options)
    if explain:
        metadata["type"] = "explain"
    return Question(
        question_text=question_text,
        correct_answer=correct_answer,
        topic="", question_type="",
        scaffold_steps=scaffold_steps or [],
        worked_solution=worked_solution or [],
        metadata=metadata,
        distractors=distractors or [],
    )


def multipart_worked_solution(parts):
    """Every part's worked solution, each block headed by its part label."""
    lines = []
    for part in parts:
        lines.append(f"**{part.metadata['label']}**")
        lines.extend(part.worked_solution or [str(part.correct_answer)])
    return lines
