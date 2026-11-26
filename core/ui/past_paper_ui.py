"""Past Paper Questions mode: a random real SQA question on a topic, with its marking instructions on request."""
import io
import random
import threading
import urllib.request

import pypdfium2
import streamlit as st
from PIL import ImageOps

from core.data.past_papers import get_past_paper_entries

# The top strip of each page holds the PDF's own navigation buttons, which do nothing in a picture, and the bottom
# strip repeats the question's year and number.
_EDGE_STRIP = 0.062
_PDFIUM_LOCK = threading.Lock()      # PDFium isn't thread-safe and Streamlit runs each session in a thread


def _trim(image):
    """Cut the edge strips, then any blank space left above and below (a short question fills little of its page)."""
    strip = round(image.height * _EDGE_STRIP)
    image = image.crop((0, strip, image.width, image.height - strip)).convert("RGB")
    ink = ImageOps.invert(image.convert("L")).point(lambda v: 255 if v > 12 else 0).getbbox()
    if not ink:
        return image
    return image.crop((0, max(ink[1] - 20, 0), image.width, min(ink[3] + 20, image.height)))


@st.cache_data(show_spinner="Loading the question…", max_entries=40, ttl=3600)
def load_pages(drive_id):
    """Every page of a Drive PDF as a PNG. Raises (so nothing is cached) if the file can't be fetched."""
    url = f"https://drive.google.com/uc?export=download&id={drive_id}"
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    if not data.startswith(b"%PDF"):
        raise ValueError("Google Drive did not return a PDF")
    pages = []
    with _PDFIUM_LOCK:
        document = pypdfium2.PdfDocument(data)
        try:
            for page in document:
                image = _trim(page.render(scale=2).to_pil())
                buffer = io.BytesIO()
                image.save(buffer, format="PNG", optimize=True)
                pages.append(buffer.getvalue())
        finally:
            document.close()
    return pages


def reset_past_paper():
    st.session_state.pop("past_paper_current", None)
    st.session_state.pop("past_paper_revealed", None)


def _pick(entries):
    """A random question, not repeating any until all of this topic's have been seen."""
    seen = st.session_state.setdefault("past_paper_seen", set())
    unseen = [e for e in entries if e["id"] not in seen]
    if not unseen:
        seen.difference_update(e["id"] for e in entries)
        current = st.session_state.get("past_paper_current") or {}
        unseen = [e for e in entries if e["id"] != current.get("id")] or entries
    entry = random.choice(unseen)
    seen.add(entry["id"])
    return entry


def _title(entry):
    year = f"{entry['year']} (not sat)" if entry["year"] == 2021 and entry["paper"] else str(entry["year"])
    if not entry["paper"]:
        return f"{year} — Question {entry['qnum']}"
    calculator = "non-calculator" if entry["paper"] == 1 else "calculator"
    return f"{year} — Paper {entry['paper']} ({calculator}) — Question {entry['qnum']}"


def render_past_papers(qualification, unit, topic):
    entries = get_past_paper_entries(qualification, unit, topic)
    if not entries:
        st.info("No past paper questions added yet for this topic.")
        return

    st.caption(f"{len(entries)} past paper question{'s' if len(entries) != 1 else ''} on this topic.")
    if st.button("Show a Past Paper Question", type="primary"):
        st.session_state.past_paper_current = _pick(entries)
        st.session_state.past_paper_revealed = False
        st.rerun()

    entry = st.session_state.get("past_paper_current")
    if not entry:
        st.caption("Press **Show a Past Paper Question** to begin.")
        return

    st.markdown(f"**{_title(entry)}**")
    if entry["parts"]:
        st.caption(f"Parts on this topic: {entry['parts']}")
    if entry.get("software"):
        st.warning("This question uses a spreadsheet or statistics software, so you need the paper's electronic files.")

    try:
        pages = load_pages(entry["drive_id"])
    except Exception:
        st.error("The question couldn't be loaded here. Open the PDF instead (the marking instructions follow the question).")
        st.link_button("Open the PDF", f"https://drive.google.com/file/d/{entry['drive_id']}/view")
        return

    marking_start = entry["question_pages"]
    extra_start = marking_start + entry["marking_pages"]
    for page in pages[:marking_start]:
        st.image(page, width="stretch")

    if pages[extra_start:]:
        with st.expander("Formulae list" if entry["paper"] else "Data booklet"):
            for page in pages[extra_start:]:
                st.image(page, width="stretch")

    if st.button("Show Marking Instructions"):
        st.session_state.past_paper_revealed = True

    if st.session_state.get("past_paper_revealed"):
        for page in pages[marking_start:extra_start]:
            st.image(page, width="stretch")
