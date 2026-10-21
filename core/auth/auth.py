import hmac
import logging

import bcrypt
import streamlit as st
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


def login_as_admin(key: str) -> dict | None:
    """Bypasses the password check for the configured admin account, given a matching
    ADMIN_KEY secret. Requires both ADMIN_KEY and ADMIN_USERNAME to be set in secrets;
    returns None (and does nothing) if either is missing or the key doesn't match."""
    expected_key = st.secrets.get("ADMIN_KEY", "")
    admin_username = st.secrets.get("ADMIN_USERNAME", "")
    if not expected_key or not admin_username or not key:
        return None
    if not hmac.compare_digest(key, expected_key):
        logger.warning("Admin bypass attempted with an incorrect key")
        return None
    try:
        result = get_supabase().table("users").select("*").eq("username", admin_username).execute()
    except Exception:
        logger.exception("Admin bypass lookup failed for username=%r", admin_username)
        return None
    if not result.data:
        logger.warning("Admin bypass configured for username=%r but no such user exists", admin_username)
        return None
    logger.info("Admin bypass login succeeded for username=%r", admin_username)
    return result.data[0]


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


def valid_username(name: str) -> "str | None":
    """None if acceptable, else why not. Letters and digits only (so a username can't be confused with
    anything else when it is copied between the app and the trackers), 3-20 characters."""
    if not (3 <= len(name) <= 20) or not name.isascii() or not name.isalnum():
        return "Usernames must be 3-20 letters or digits, with no spaces or symbols."
    return None


def change_username(user_id: str, new_username: str) -> "str | None":
    """Teacher tool: rename an account. Everything is keyed on the user id, so the pupil's results,
    assignments and password are unchanged — they just log in with the new name. Returns None on
    success, error string on failure."""
    new_username = new_username.strip()
    problem = valid_username(new_username)
    if problem:
        return problem
    try:
        sb = get_supabase()
        taken = sb.table("users").select("id").eq("username", new_username).execute().data or []
        if any(u["id"] != user_id for u in taken):
            return "That username is already taken."
        sb.table("users").update({"username": new_username}).eq("id", user_id).execute()
        return None
    except Exception as e:
        logger.exception("Username change failed for user_id=%r", user_id)
        return f"Rename failed: {e}"


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
