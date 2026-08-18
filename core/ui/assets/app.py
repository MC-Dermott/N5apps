"""Standalone playtest harness for geometry_dash.html - lets you play the
game directly without going through a full N5apps test. The real embed
lives in core/ui/test_ui.py, which loads the same file as a post-test
reward."""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(page_title="Geometry Dash Playtest", layout="wide")
st.title("Geometry Dash Clone")
st.caption("Space / click / tap to jump (and hold to fly, in the flying section). Dodge the spikes and blocks.")

game_html = Path(__file__).parent.joinpath("geometry_dash.html").read_text(encoding="utf-8")

# height is the pixel height of the iframe; the canvas inside scales to
# fill the available width while keeping its aspect ratio.
components.html(game_html, height=420, scrolling=False)

st.markdown(
    "One continuous, fixed (not random) level that tours every mechanic in "
    "turn, joined by glowing portal transitions: normal running, a "
    "gravity-flip section, a sheep-block staircase you jump up and back down, "
    "and a flying gauntlet. Progress and best times are saved in your "
    "browser's local storage, so they persist between visits but are "
    "specific to this browser/device."
)
