from core.db.client import get_supabase

# N5apps shares a Supabase project with N3apps ("maths"). This tags every row so
# per-app dashboards/heatmaps can filter to their own subject without students
# needing a separate login per app.
SUBJECT = "maths"


def save_practice_attempt(user_id: str, qualification: str, topic: str, question_type: str, correct: bool):
    try:
        get_supabase().table("question_attempts").insert({
            "user_id": user_id,
            "subject": SUBJECT,
            "qualification": qualification,
            "topic": topic,
            "question_type": question_type,
            "correct": correct,
        }).execute()
    except Exception:
        pass  # Don't break the app if tracking fails


def save_test_result(user_id: str, qualification: str, topic: str, question_type: str, score: int, total: int,
                     assignment_id: str | None = None, review_state: dict | None = None) -> bool:
    """Returns True if saved. assignment_id is only sent when set, so ordinary tests still save
    on a database that hasn't had the assignments migration run yet. review_state (the finished test's
    session dict) is stored so the pupil can look back over the attempt (core/db/reviews.py)."""
    row = {
        "user_id": user_id,
        "subject": SUBJECT,
        "qualification": qualification,
        "topic": topic,
        "question_type": question_type,
        "score": score,
        "total": total,
    }
    if assignment_id:
        row["assignment_id"] = assignment_id
    try:
        saved = getattr(get_supabase().table("test_results").insert(row).execute(), "data", None)
        if review_state and saved:
            from core.db.reviews import save_review
            save_review(saved[0]["id"], review_state)
        return True
    except Exception:
        return False  # Don't break the app if tracking fails
