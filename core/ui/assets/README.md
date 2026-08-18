# Geometry Dash Clone

A self-contained HTML5 canvas Geometry Dash game: one continuous level, "The
Full Run", that tours every mechanic in turn - normal running past
mushroom/lighthouse obstacles, a gravity-flip section that flips the world
upside down, a sheep-block staircase (jump your way up four rising steps,
then back down four falling ones), and a flying gauntlet where the sprite
becomes a car weaving between obstacles from above and below - joined by
glowing portal-style transitions between sections. Uses a custom face sprite
as the player icon. Progress and best times are saved in the browser's local
storage.

`geometry_dash.html` is the real asset: it's what `core/ui/test_ui.py`
reads and embeds as the reward game students unlock after a perfect test
score in the main N5apps app. It's fully self-contained (no external image
files, everything including the cameo images is base64-inlined), so it also
runs standalone - double-click it to open directly in a browser, no
Streamlit or N5apps required.

`app.py` is a standalone playtest harness for iterating on the game outside
the full N5apps flow, so you don't have to complete a test to see it.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

This opens the game in your browser via Streamlit.

## Files

- `app.py` - standalone Streamlit wrapper that embeds the game, for
  playtesting in isolation.
- `geometry_dash.html` - the self-contained game itself, and the file the
  main N5apps app actually loads.
- `requirements.txt` - Python dependencies for `app.py`.
