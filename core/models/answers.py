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
