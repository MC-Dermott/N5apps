"""Part-finished assignment tests, so a pupil can leave and Continue later (or Start over).

The test / unit-assessment session dict is stored as JSON in `assignment_progress`, one row per pupil per
assignment item (migration 2026-10-26). Unlike a review, the blank question workbook is kept: a pupil who
carries on needs it. Everything is best-effort: if the table is missing the test still works, it just can't
be resumed."""
from datetime import datetime, timezone

from core.db.client import get_supabase
from core.db.reviews import _decode, _encode, question_from_json, question_to_json

TABLE = "assignment_progress"


def progress_to_json(state, calc_mode=False):
    """results keeps None for unanswered questions (an attempt's results are all booleans)."""
    return {"questions": [question_to_json(q, keep_bytes=True) for q in state["questions"]],
            "answers": _encode(list(state["answers"])),
            "results": [None if r is None else bool(r) for r in state["results"]],
            "types": list(state.get("types") or []), "index": state["index"], "calc_mode": bool(calc_mode)}


def progress_from_json(payload):
    """Returns (state dict ready for st.session_state, calc_mode)."""
    n = len(payload["questions"])
    answers = _decode(payload["answers"]) + [None] * n
    results = list(payload["results"]) + [None] * n
    return ({"questions": [question_from_json(q) for q in payload["questions"]], "types": payload.get("types") or [],
             "index": min(payload.get("index", 0), n - 1), "answers": answers[:n], "results": results[:n],
             "complete": False, "saved": False}, bool(payload.get("calc_mode")))


def answered_count(state):
    return sum(r is not None for r in state["results"])


def save_progress(user_id, item_id, state, calc_mode=False):
    try:
        get_supabase().table(TABLE).upsert(
            {"user_id": user_id, "assignment_item_id": item_id, "q_index": state["index"],
             "q_total": len(state["questions"]), "payload": progress_to_json(state, calc_mode),
             "updated_at": datetime.now(timezone.utc).isoformat()}, on_conflict="user_id,assignment_item_id").execute()
        return True
    except Exception:
        return False


def load_progress(user_id, item_id):
    """(state, calc_mode) or None."""
    try:
        rows = (get_supabase().table(TABLE).select("payload").eq("user_id", user_id)
                .eq("assignment_item_id", item_id).execute().data or [])
        return progress_from_json(rows[0]["payload"]) if rows else None
    except Exception:
        return None


def delete_progress(user_id, item_id):
    try:
        get_supabase().table(TABLE).delete().eq("user_id", user_id).eq("assignment_item_id", item_id).execute()
    except Exception:
        pass


def progress_summaries(user_id):
    """{assignment_item_id: {"index", "total"}} for the pupil's My Assignments page."""
    try:
        rows = (get_supabase().table(TABLE).select("assignment_item_id,q_index,q_total")
                .eq("user_id", user_id).execute().data or [])
    except Exception:
        return {}
    return {r["assignment_item_id"]: {"index": r["q_index"], "total": r["q_total"]} for r in rows}
