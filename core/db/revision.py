"""Pupil revision guide rows (table revision_guide, filled by
Resources/Apps/.pipeline-tools/assessment_tracker/sync_revision_guide.py)."""
from core.db.client import get_supabase


def fetch_guide(user_id: str):
    """This pupil's rows, weakest first, or None if the table doesn't exist yet."""
    try:
        rows = (get_supabase().table("revision_guide").select("*").eq("user_id", user_id).execute().data or [])
    except Exception:
        return None
    rows.sort(key=lambda r: (r["qualification"], r["rank"]))
    return rows
