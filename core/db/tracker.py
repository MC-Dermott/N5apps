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


def save_test_result(user_id: str, qualification: str, topic: str, question_type: str, score: int, total: int):
    try:
        get_supabase().table("test_results").insert({
            "user_id": user_id,
            "subject": SUBJECT,
            "qualification": qualification,
            "topic": topic,
            "question_type": question_type,
            "score": score,
            "total": total,
        }).execute()
    except Exception:
        pass
