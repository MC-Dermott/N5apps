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
