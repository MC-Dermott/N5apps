import re

import streamlit as st

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


def render_examples(example_text: str):
    if example_text:
        with st.expander("📝 Examples"):
            st.markdown(example_text)
