"""Time-bar method for time intervals: split the time between a start and finish at the next
o'clock and the last o'clock before the finish, then count each piece.

Pure logic (no Streamlit) shared by the question generators — which turn `time_bar_steps()` into
`scaffold_steps` — and `core/ui/time_bar_widget.py`, which renders the same steps as a guided
interactive bar, so the scaffold and the widget always agree.

Times are minutes after midnight; `end` may run past 1440 for an overnight journey.
"""


def clock(t):
    t %= 1440
    return f"{t // 60:02d}:{t % 60:02d}"


def hm(total_minutes):
    h, m = divmod(total_minutes, 60)
    h_word = f"{h} hour{'s' if h != 1 else ''}"
    m_word = f"{m} minute{'s' if m != 1 else ''}"
    if h == 0:
        return m_word
    if m == 0:
        return h_word
    return f"{h_word} {m_word}"


def time_bar_ticks(start, end):
    """Start, next o'clock, last o'clock before the finish, finish — de-duplicated, so a
    journey with no whole hours (or starting/finishing on the hour) gets fewer pieces."""
    if end <= start:
        raise ValueError("end must be after start")
    h1 = -(-start // 60) * 60      # next o'clock (the start itself if on the hour)
    h2 = (end // 60) * 60
    return sorted({p for p in (start, h1, h2, end) if start <= p <= end})


def time_bar_segments(start, end):
    """[(from, to, kind)] where kind is 'lead' (up to an o'clock), 'hours' (o'clock to
    o'clock) or 'tail' (o'clock to a finish that isn't on the hour)."""
    ticks = time_bar_ticks(start, end)
    segs = []
    for a, b in zip(ticks, ticks[1:]):
        if a % 60 == 0 and b % 60 == 0:
            kind = "hours"
        elif a % 60 == 0:
            kind = "tail"
        else:
            kind = "lead"
        segs.append((a, b, kind))
    return segs


def time_bar_steps(start, end, mode="interval"):
    """Guided steps for the time bar.

    mode: 'interval' — both clock times known, find the time between them;
          'forward'  — start and the time to add known, find the finish time;
          'backward' — finish and the time to take away known, find the start time.

    Each step: {"prompt", "answer", "kind" ('minutes' | 'hours' | 'duration' | 'clock'),
    "reveal_segs": [segment indices], "reveal_ticks": [tick indices]} — the reveal lists say
    which parts of the bar the widget uncovers once the step is answered.
    """
    segs = time_bar_segments(start, end)
    ticks = time_bar_ticks(start, end)
    total = end - start
    steps = []

    def seg_step(i, a, b, kind, prompt_time):
        n = b - a
        if kind == "hours":
            return {"prompt": f"How many whole hours from {clock(a)} to {clock(b)}?",
                    "answer": n // 60, "kind": "hours", "reveal_segs": [i], "reveal_ticks": []}
        return {"prompt": prompt_time, "answer": n, "kind": "minutes",
                "reveal_segs": [i], "reveal_ticks": []}

    if mode == "interval":
        for i, (a, b, kind) in enumerate(segs):
            steps.append(seg_step(i, a, b, kind, f"How many minutes from {clock(a)} to {clock(b)}?"))
        steps.append({"prompt": "Add the pieces together. How long is it altogether?",
                      "answer": hm(total), "kind": "duration", "reveal_segs": [], "reveal_ticks": []})
        return steps

    order = list(range(len(segs)))
    if mode == "backward":
        order.reverse()
    elif mode != "forward":
        raise ValueError("mode must be 'interval', 'forward' or 'backward'")

    left = total
    verb_add, verb_left = ("Add on", "add") if mode == "forward" else ("Take away", "take away")
    what = "finish" if mode == "forward" else "start"
    for pos, i in enumerate(order):
        a, b, kind = segs[i]
        n = b - a
        reached_idx = i + 1 if mode == "forward" else i
        last = pos == len(order) - 1
        if pos == 0 and kind != "hours" and not last:
            # First piece: count the minutes to (or back from) the o'clock, then see how much
            # of the time is still left.
            if mode == "forward":
                prompt = f"How many minutes from {clock(a)} up to {clock(b)}?"
            else:
                prompt = f"How many minutes from {clock(b)} back to {clock(a)}?"
            steps.append({"prompt": prompt, "answer": n, "kind": "minutes",
                          "reveal_segs": [i], "reveal_ticks": [reached_idx]})
            left -= n
            steps.append({"prompt": f"How much time is still left to {verb_left}?",
                          "answer": hm(left), "kind": "duration", "reveal_segs": [], "reveal_ticks": []})
            continue
        if last:
            piece = f"the last {hm(n)}" if pos else hm(n)
            prompt = f"{verb_add} {piece}. What is the {what} time?"
        else:
            prompt = f"{verb_add} the {n // 60} whole hour{'s' if n != 60 else ''}. What time do you reach?"
        steps.append({"prompt": prompt, "answer": clock(ticks[reached_idx]), "kind": "clock",
                      "reveal_segs": [i], "reveal_ticks": [reached_idx]})
        left -= n
    return steps
