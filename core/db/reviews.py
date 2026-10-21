"""Saved attempts, so a pupil can look back over a completed test or unit assessment.

An attempt (the questions as generated, the pupil's answers and which were marked right) is stored as JSON
in `test_result_reviews`, one row per test_results row. Questions are plain dataclasses, so they are
converted to JSON and back; bytes (the completed spreadsheet) are base64-encoded, and the blank question
workbook is left out because nothing in a review needs it."""
import base64
from dataclasses import asdict

from core.db.client import get_supabase
from core.models.question_model import Question

_DROP_METADATA = ("spreadsheet_bytes",)
_BYTES, _TUPLE = "__bytes__", "__tuple__"


def _encode(value):
    if isinstance(value, bytes):
        return {_BYTES: base64.b64encode(value).decode("ascii")}
    if isinstance(value, tuple):
        return {_TUPLE: [_encode(v) for v in value]}
    if isinstance(value, dict):
        return {str(k): _encode(v) for k, v in value.items()}
    if isinstance(value, (list, set)):
        return [_encode(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)                       # anything exotic is shown as text rather than lost


def _decode(value):
    if isinstance(value, dict):
        if set(value) == {_BYTES}:
            return base64.b64decode(value[_BYTES])
        if set(value) == {_TUPLE}:
            return tuple(_decode(v) for v in value[_TUPLE])
        return {k: _decode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_decode(v) for v in value]
    return value


def question_to_json(question):
    d = asdict(question)

    def strip(q):
        for k in _DROP_METADATA:
            q["metadata"].pop(k, None)
        for part in q["parts"]:
            strip(part)
    strip(d)
    return _encode(d)


def question_from_json(data):
    data = _decode(data)
    data["parts"] = [question_from_json(_encode(p)) if isinstance(p, dict) else p for p in data.get("parts", [])]
    return Question(**data)


def attempt_to_json(state):
    """state: the test / unit-assessment session dict."""
    return {"questions": [question_to_json(q) for q in state["questions"]],
            "answers": _encode(list(state["answers"])), "results": [bool(r) for r in state["results"]],
            "types": list(state.get("types") or [])}


def attempt_from_json(payload):
    return {"questions": [question_from_json(q) for q in payload["questions"]],
            "answers": _decode(payload["answers"]), "results": payload["results"],
            "types": payload.get("types") or []}


def save_review(result_id, state):
    """Best-effort: a pupil's score is already saved, so a failure here must not break the test."""
    try:
        get_supabase().table("test_result_reviews").insert(
            {"test_result_id": result_id, "payload": attempt_to_json(state)}).execute()
        return True
    except Exception:
        return False


def load_review(result_id):
    rows = (get_supabase().table("test_result_reviews").select("payload")
            .eq("test_result_id", result_id).execute().data or [])
    return attempt_from_json(rows[0]["payload"]) if rows else None
