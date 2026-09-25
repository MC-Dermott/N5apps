import re

import streamlit as st

from core.ui.time_bar_widget import render_time_bar_diagram

# Every topic's NOTES markdown constant embeds its worked example as a
# "**Example:**" (or "**Example (Level 2):**", "*Example:*", etc.) heading
# partway through the same string. This splits on the first such heading so
# the concept explanation and the worked example can be shown in separate
# expanders without editing every topic module.
_EXAMPLE_HEADING_RE = re.compile(r"(?m)^\s*\*{1,2}Example\b", re.IGNORECASE)


def split_notes_and_example(notes: str) -> tuple[str, str]:
    if not notes:
        return "", ""
    match = _EXAMPLE_HEADING_RE.search(notes)
    if not match:
        return notes.strip(), ""
    return notes[:match.start()].strip(), notes[match.start():].strip()


def render_notes(notes_text: str):
    if notes_text:
        with st.expander("📚 Notes"):
            st.markdown(notes_text)


# A worked example can show a time-bar diagram (the same one as the worksheet) by putting a
# line like  [[time_bar 07:35-12:20 interval | Leaves Oban | Arrives Castlebay]]  in its
# markdown — mode is interval / forward / backward, and the finish may be earlier than the
# start for an overnight journey.
_TIME_BAR_RE = re.compile(
    r"^\[\[time_bar (\d{2}):(\d{2})-(\d{2}):(\d{2}) (interval|forward|backward)"
    r"(?: \| ([^|\]]*))?(?: \| ([^|\]]*))?\]\]$", re.MULTILINE)


def render_examples(example_text: str):
    if example_text:
        with st.expander("📝 Examples"):
            pos = 0
            for m in _TIME_BAR_RE.finditer(example_text):
                if example_text[pos:m.start()].strip():
                    st.markdown(example_text[pos:m.start()])
                start = int(m[1]) * 60 + int(m[2])
                end = int(m[3]) * 60 + int(m[4])
                if end <= start:
                    end += 1440
                render_time_bar_diagram(start, end, m[5], (m[6] or "").strip(), (m[7] or "").strip())
                pos = m.end()
            if example_text[pos:].strip():
                st.markdown(example_text[pos:])
