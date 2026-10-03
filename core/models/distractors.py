"""Build a question's recognised wrong answers (see `Question.distractors`)."""


def distractors(answer, candidates):
    """[(value, mistake)] -> [{"value", "mistake"}], dropping None values, anything within 0.01
    of the answer (numbers) or equal to it (text), and repeats. Values are the pupil's likely
    wrong final answers from the SQA course reports / marking instructions."""
    out = []

    def same(a, b):
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return abs(a - b) < 0.01
        return str(a).strip().lower() == str(b).strip().lower()

    for value, mistake in candidates:
        if value is None or same(value, answer) or any(same(value, d["value"]) for d in out):
            continue
        if isinstance(value, (int, float)) and abs(value) < 0.001:
            continue                       # nobody types 0.000014 — not worth matching
        out.append({"value": value, "mistake": mistake})
    return out
