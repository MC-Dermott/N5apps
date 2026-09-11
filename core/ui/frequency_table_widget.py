"""Interactive frequency-table-to-pie-chart-angle checker.

Shows a Category / Frequency / Angle table — exactly like a pupil's own working —
with the Angle column left blank for pupils to fill in, one cell per category, then
checks every cell at once against the correct angles.

Usage:

    from core.ui.frequency_table_widget import render_frequency_table_widget

    render_frequency_table_widget(
        categories=["France", "Wales", "England"],
        frequencies=[3, 4, 11],
        angles=[60, 80, 220],
    )
"""
import json
import html
import streamlit.components.v1 as components


def _build_html(categories, frequencies, angles, category_label, value_label, height):
    n = len(categories)
    if n != len(frequencies) or n != len(angles):
        raise ValueError("categories, frequencies and angles must be the same length")

    rows_html = "\n".join(
        f'<tr>'
        f'<td class="ftw-catCell">{html.escape(str(cat))}</td>'
        f'<td class="ftw-freqCell">{freq}</td>'
        f'<td class="ftw-angleCell">'
        f'<input type="number" inputmode="numeric" class="ftw-angleInput" id="ftw-input-{i}">'
        f'<span class="ftw-degSign">°</span>'
        f'<span class="ftw-mark" id="ftw-mark-{i}"></span>'
        f'</td>'
        f'</tr>'
        for i, (cat, freq) in enumerate(zip(categories, frequencies))
    )

    return f"""
    <style>
      #ftw-root{{
        --ink: #22282f; --ink-soft: #5b6470; --line: #d8d2c4;
        --mark-deep: #a97a13; --good: #2f6f4a; --good-tint: #eaf3ec;
        --bad: #b3402b; --bad-tint: #fbeae6;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--ink);
      }}
      #ftw-root *{{ box-sizing: border-box; }}
      #ftw-root table{{ border-collapse: collapse; width: 100%; max-width: 480px; }}
      #ftw-root th, #ftw-root td{{
        border: 1.5px solid var(--line); padding: 10px 14px; text-align: left; font-size: 15px;
      }}
      #ftw-root th{{ background: #faf7f0; font-weight: 700; color: var(--ink); }}
      #ftw-root .ftw-catCell{{ font-weight: 600; }}
      #ftw-root .ftw-freqCell{{ font-family:'Courier New', monospace; }}
      #ftw-root .ftw-angleCell{{ display:flex; align-items:center; gap: 4px; white-space:nowrap; }}
      #ftw-root .ftw-angleInput{{
        width: 64px; font-family:'Courier New', monospace; font-size: 15px; font-weight:600;
        padding: 6px 8px; border: 1.5px solid var(--line); border-radius: 6px;
        background: #fff; color: var(--ink); outline: none;
      }}
      #ftw-root .ftw-angleInput:focus{{ border-color: var(--mark-deep); }}
      #ftw-root .ftw-angleInput.ftw-correct{{ border-color: var(--good); background: var(--good-tint); color: var(--good); }}
      #ftw-root .ftw-angleInput.ftw-wrong{{ border-color: var(--bad); background: var(--bad-tint); color: var(--bad); }}
      #ftw-root .ftw-angleInput::-webkit-outer-spin-button, #ftw-root .ftw-angleInput::-webkit-inner-spin-button{{ -webkit-appearance:none; margin:0; }}
      #ftw-root .ftw-degSign{{ font-size: 15px; }}
      #ftw-root .ftw-mark{{ font-weight:700; font-size: 15px; min-width: 16px; }}
      #ftw-root .ftw-mark.good{{ color: var(--good); }}
      #ftw-root .ftw-mark.bad{{ color: var(--bad); }}
      #ftw-root .ftw-btn{{
        margin-top: 16px; font-size: 14px; font-weight:600; padding: 10px 18px; border-radius: 8px;
        border: none; cursor: pointer; color: #fff; background: var(--ink); transition: opacity .12s;
      }}
      #ftw-root .ftw-btn:hover{{ opacity:.9; }}
      #ftw-root .ftw-feedback{{ margin-top: 12px; font-size: 14px; font-weight:600; min-height: 20px; }}
      #ftw-root .ftw-feedback.good{{ color: var(--good); }}
      #ftw-root .ftw-feedback.bad{{ color: var(--bad); }}
    </style>

    <div id="ftw-root">
      <table>
        <thead>
          <tr><th>{html.escape(category_label)}</th><th>{html.escape(value_label)}</th><th>Angle</th></tr>
        </thead>
        <tbody>
          {rows_html}
        </tbody>
      </table>
      <button class="ftw-btn" id="ftw-checkBtn">Check my angles</button>
      <div class="ftw-feedback" id="ftw-feedback"></div>
    </div>

    <script>
    (function(){{
      const ANGLES = {json.dumps(angles)};
      const N = ANGLES.length;

      document.getElementById('ftw-checkBtn').addEventListener('click', () => {{
        let numCorrect = 0;
        for (let i = 0; i < N; i++){{
          const input = document.getElementById('ftw-input-' + i);
          const mark = document.getElementById('ftw-mark-' + i);
          const val = parseFloat(input.value);
          const isCorrect = !isNaN(val) && Math.abs(val - ANGLES[i]) < 0.01;
          input.classList.remove('ftw-correct', 'ftw-wrong');
          input.classList.add(isCorrect ? 'ftw-correct' : 'ftw-wrong');
          mark.textContent = isCorrect ? '✓' : '✗';
          mark.className = 'ftw-mark ' + (isCorrect ? 'good' : 'bad');
          if (isCorrect) numCorrect++;
        }}
        const feedback = document.getElementById('ftw-feedback');
        if (numCorrect === N){{
          feedback.textContent = `All ${{N}} correct — and they add up to 360°, just like they should!`;
          feedback.className = 'ftw-feedback good';
        }} else {{
          feedback.textContent = `${{numCorrect}} out of ${{N}} correct — check the red boxes and try again.`;
          feedback.className = 'ftw-feedback bad';
        }}
      }});
    }})();
    </script>
    """


def render_frequency_table_widget(categories, frequencies, angles, category_label="Category",
                                   value_label="Frequency", height=340):
    """Render the fillable Category/Frequency/Angle table for a pie-chart-angles question.

    Pupils type an angle into each row, then check all of them at once.
    """
    height = max(height, 90 + 46 * len(categories))
    html_code = _build_html(categories, frequencies, angles, category_label, value_label, height)
    components.html(html_code, height=height, scrolling=True)
