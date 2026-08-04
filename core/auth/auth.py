import logging

import bcrypt
from core.db.client import get_supabase

logger = logging.getLogger(__name__)


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def login(username: str, password: str) -> dict | None:
    """Returns user dict on success, None on bad credentials."""
    try:
        result = get_supabase().table("users").select("*").eq("username", username).execute()
    except Exception:
        logger.exception(
            "Login lookup failed for username=%r (Supabase/config error, not a bad password)",
            username,
        )
        return None
    if not result.data:
        logger.info("Login failed: no user found for username=%r", username)
        return None
    user = result.data[0]
    if not _verify(password, user["password_hash"]):
        logger.info("Login failed: password mismatch for username=%r", username)
        return None
    return user


def reset_password(user_id: str, new_password: str) -> "str | None":
    """Returns None on success, error string on failure."""
    try:
        get_supabase().table("users").update({
            "password_hash": _hash(new_password),
        }).eq("id", user_id).execute()
        return None
    except Exception as e:
        logger.exception("Password reset failed for user_id=%r", user_id)
        return f"Reset failed: {e}"


def signup(username: str, password: str, role: str = "student", class_code: str = "") -> "dict | str":
    """Returns user dict on success, error string on failure."""
    try:
        sb = get_supabase()
        if sb.table("users").select("id").eq("username", username).execute().data:
            return "That username is already taken."
        row = {
            "username": username,
            "password_hash": _hash(password),
            "role": role,
        }
        if class_code:
            row["class_code"] = class_code.strip().upper()
        result = sb.table("users").insert(row).execute()
        return result.data[0] if result.data else "Signup failed — please try again."
    except Exception as e:
        logger.exception("Signup failed for username=%r", username)
        return f"Signup failed: {e}"
