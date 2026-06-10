import bcrypt
from core.db.client import get_supabase


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def login(username: str, password: str) -> dict | None:
    """Returns user dict on success, None on bad credentials."""
    try:
        result = get_supabase().table("users").select("*").eq("username", username).execute()
    except Exception:
        return None
    if not result.data:
        return None
    user = result.data[0]
    return user if _verify(password, user["password_hash"]) else None


def reset_password(user_id: str, new_password: str) -> "str | None":
    """Returns None on success, error string on failure."""
    try:
        get_supabase().table("users").update({
            "password_hash": _hash(new_password),
        }).eq("id", user_id).execute()
        return None
    except Exception as e:
        return f"Reset failed: {e}"


def signup(username: str, password: str, role: str = "student") -> "dict | str":
    """Returns user dict on success, error string on failure."""
    try:
        sb = get_supabase()
        if sb.table("users").select("id").eq("username", username).execute().data:
            return "That username is already taken."
        result = sb.table("users").insert({
            "username": username,
            "password_hash": _hash(password),
            "role": role,
        }).execute()
        return result.data[0] if result.data else "Signup failed — please try again."
    except Exception as e:
        return f"Signup failed: {e}"
