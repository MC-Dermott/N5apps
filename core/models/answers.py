import re

_CLOCK_RE = re.compile(r"^\d{2}:\d{2}$")


def clock_answers_match(user, expected):
    """For a 24-hour clock-time answer ("08:18"), accept "8:18", "0818", "08.18" or "8 18".
    Returns None when `expected` isn't a clock time, so callers fall through to their own
    numeric/string checks."""
    expected = str(expected).strip()
    if not _CLOCK_RE.match(expected):
        return None
    digits = re.sub(r"\D", "", str(user))
    if len(digits) not in (3, 4):
        return False
    return digits.zfill(4) == expected.replace(":", "")


def _number(s):
    s = str(s).strip().replace(",", "").replace("£", "").replace("%", "")
    try:
        return float(s)
    except ValueError:
        if "/" in s:
            try:
                num, den = s.split("/", 1)
                return float(num) / float(den)
            except (ValueError, ZeroDivisionError):
                pass
    return None


def common_mistake(question, user):
    """The `mistake` message of the first distractor the pupil's (wrong) answer matches, else
    None. Numbers match to within 0.01, like the answer checkers; anything else must match as
    text, ignoring case."""
    u = _number(user)
    for d in getattr(question, "distractors", None) or []:
        v = _number(d["value"])
        if u is not None and v is not None:
            if abs(u - v) < 0.01:
                return d["mistake"]
        elif str(user).strip().lower() == str(d["value"]).strip().lower():
            return d["mistake"]
    return None
