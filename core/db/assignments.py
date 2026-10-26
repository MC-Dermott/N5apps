"""Assignments: teacher-set work that is checked from stored test results.

An assignment is a list of items (a qualification/unit/topic test each), a pass mark and a due
date, aimed at whole classes (class_code) and/or individual pupils. An item counts as done once
the pupil has taken that test *through the assignment* (test_results.assignment_id) and scored
at least the pass mark; the best attempt counts."""
from datetime import date

from core.db.client import get_supabase
from core.db.tracker import SUBJECT

NOT_STARTED, IN_PROGRESS, DONE = "Not started", "In progress", "Done"


# ── Pure logic (no database) ──────────────────────────────────────────────────

def _key(row):
    return row["qualification"], row["topic"], row["question_type"]


def item_status(item, results, pass_pct):
    """results: the pupil's test_results rows for this assignment. Returns
    {"state", "best", "attempts"}; best is the highest percentage (None if no attempts)."""
    rows = [r for r in results if _key(r) == _key(item) and r.get("total")]
    if not rows:
        return {"state": NOT_STARTED, "best": None, "attempts": 0}
    best = max(100 * r["score"] / r["total"] for r in rows)
    return {"state": DONE if best >= pass_pct else IN_PROGRESS, "best": best, "attempts": len(rows)}


MIXED = "mixed"
MIXED_KEY = {"qualification": "Mixed", "topic": "Mixed assignment", "question_type": "Mixed"}


def is_mixed(assignment):
    return assignment.get("format") == MIXED


def mixed_status(results, pass_pct):
    """A mixed assignment is one attempt covering every topic: the best attempt decides. The result has the
    same shape as assignment_status, with the whole assignment as its single item."""
    rows = [r for r in results if r.get("total")]
    if not rows:
        item = {"state": NOT_STARTED, "best": None, "attempts": 0}
    else:
        best = max(100 * r["score"] / r["total"] for r in rows)
        item = {"state": DONE if best >= pass_pct else IN_PROGRESS, "best": best, "attempts": len(rows)}
    return {"state": item["state"], "done": int(item["state"] == DONE), "total": 1, "items": [item]}


def assignment_status(items, results, pass_pct, fmt="tests"):
    """Overall state of one pupil's assignment, plus the per-item statuses."""
    if fmt == MIXED:
        return mixed_status(results, pass_pct)
    per_item = [item_status(i, results, pass_pct) for i in items]
    done = sum(s["state"] == DONE for s in per_item)
    if items and done == len(items):
        state = DONE
    elif any(s["attempts"] for s in per_item):
        state = IN_PROGRESS
    else:
        state = NOT_STARTED
    return {"state": state, "done": done, "total": len(items), "items": per_item}


def is_overdue(assignment, status_state, today=None):
    due = assignment.get("due_date")
    if not due or status_state == DONE:
        return False
    return date.fromisoformat(due) < (today or date.today())


def item_label(item):
    return f"{item['topic']} — {item['question_type']}"


# ── Teacher: create / list / delete ───────────────────────────────────────────

def create_assignment(teacher_id, title, due, pass_pct, items, class_codes, user_ids, fmt="tests"):
    """Returns None on success, or an error string. items: [{qualification, topic, question_type}]."""
    if not title.strip():
        return "Give the assignment a title."
    if not items:
        return "Add at least one topic."
    if not class_codes and not user_ids:
        return "Choose at least one class or pupil."
    sb = get_supabase()
    try:
        row = {"title": title.strip(), "created_by": teacher_id, "subject": SUBJECT,
               "due_date": due.isoformat() if due else None, "pass_pct": int(pass_pct)}
        if fmt == MIXED:          # only sent when needed, so ordinary assignments work before the migration
            row["format"] = MIXED
        created = sb.table("assignments").insert(row).execute().data[0]
    except Exception as e:
        return f"Could not create the assignment (has the assignments migration been run?): {e}"
    aid = created["id"]
    try:
        sb.table("assignment_items").insert([
            {"assignment_id": aid, "position": n, "qualification": i["qualification"],
             "topic": i["topic"], "question_type": i["question_type"]}
            for n, i in enumerate(items)]).execute()
        sb.table("assignment_targets").insert(
            [{"assignment_id": aid, "class_code": c.strip().upper()} for c in class_codes]
            + [{"assignment_id": aid, "user_id": u} for u in user_ids]).execute()
    except Exception as e:
        sb.table("assignments").delete().eq("id", aid).execute()   # cascade removes the partial rows
        return f"Could not create the assignment: {e}"
    return None


def delete_assignment(assignment_id):
    """Removes the assignment; tests already taken through it stay as ordinary test results."""
    try:
        get_supabase().table("assignments").delete().eq("id", assignment_id).execute()
        return None
    except Exception as e:
        return f"Delete failed: {e}"


def teacher_assignments():
    """Every assignment, newest first, each with 'items' and 'targets'."""
    sb = get_supabase()
    assignments = (sb.table("assignments").select("*").eq("subject", SUBJECT)
                   .order("created_at", desc=True).execute().data or [])
    if not assignments:
        return []
    ids = [a["id"] for a in assignments]
    items = sb.table("assignment_items").select("*").in_("assignment_id", ids).order("position").execute().data or []
    targets = sb.table("assignment_targets").select("*").in_("assignment_id", ids).execute().data or []
    for a in assignments:
        a["items"] = [i for i in items if i["assignment_id"] == a["id"]]
        a["targets"] = [t for t in targets if t["assignment_id"] == a["id"]]
    return assignments


def assignment_results(assignment_id):
    return (get_supabase().table("test_results").select("*")
            .eq("assignment_id", assignment_id).execute().data or [])


def recipients(assignment, students):
    """The students an assignment is set for (targets by class code or by pupil)."""
    classes = {t["class_code"] for t in assignment["targets"] if t.get("class_code")}
    people = {t["user_id"] for t in assignment["targets"] if t.get("user_id")}
    return [s for s in students if s["id"] in people or (s.get("class_code") or "").upper() in classes]


# ── Pupil ─────────────────────────────────────────────────────────────────────

def pupil_assignments(user):
    """The pupil's assignments (newest first), each with 'items', 'results' and 'status'."""
    sb = get_supabase()
    clause = f"user_id.eq.{user['id']}"
    if user.get("class_code"):
        clause += f",class_code.eq.{user['class_code'].upper()}"
    targets = sb.table("assignment_targets").select("assignment_id").or_(clause).execute().data or []
    ids = sorted({t["assignment_id"] for t in targets})
    if not ids:
        return []
    assignments = (sb.table("assignments").select("*").in_("id", ids).eq("subject", SUBJECT)
                   .order("created_at", desc=True).execute().data or [])
    items = sb.table("assignment_items").select("*").in_("assignment_id", ids).order("position").execute().data or []
    results = (sb.table("test_results").select("*").eq("user_id", user["id"])
               .in_("assignment_id", ids).execute().data or [])
    for a in assignments:
        a["items"] = [i for i in items if i["assignment_id"] == a["id"]]
        a["results"] = [r for r in results if r["assignment_id"] == a["id"]]
        a["status"] = assignment_status(a["items"], a["results"], a["pass_pct"], a.get("format", "tests"))
    return assignments


def outstanding_count(user):
    try:
        return sum(a["status"]["state"] != DONE for a in pupil_assignments(user))
    except Exception:
        return 0
