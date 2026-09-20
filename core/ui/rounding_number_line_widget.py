"""Interactive guided rounding number-line widget.

Adapted from the standalone prototype at
`/Users/luke/Library/CloudStorage/OneDrive-GlowScotland/Resources/Maths/scaffolds/maths_scaffolds.html`
(the "Rounding number line — guided" tool) — trimmed to drop that page's own number/rounding-
target setup panel, since here the value and place always come from the question that's already
been generated, following the same pattern as bus_stop_division_widget.py.

Walks the pupil through three stages: estimate where the number sits on the line between the
two round values, reveal its exact position and choose which end it's closer to, then complete
the "... rounded to ... is ___" sentence.

Usage:

    from core.ui.rounding_number_line_widget import render_rounding_number_line_widget

    render_rounding_number_line_widget(value=7.9831, place_e=-2)   # round to 2 d.p.
    render_rounding_number_line_widget(value=4368, place_e=2)      # round to nearest 100
"""
import streamlit.components.v1 as components

_PHRASES = {
    3: "the nearest 1000",
    2: "the nearest 100",
    1: "the nearest 10",
    0: "the nearest whole number",
    -1: "1 decimal place",
    -2: "2 decimal places",
    -3: "3 decimal places",
}


def _build_html(value, place_e, height):
    if place_e not in _PHRASES:
        raise ValueError("place_e must be one of 3, 2, 1, 0, -1, -2, -3")
    phrase = _PHRASES[place_e]

    return f"""
    <style>
      #rn-root{{
        --ink: #22282f; --ink-soft: #5b6470; --line: #d8d2c4;
        --down: #2f6f6b; --down-tint: #e3efee; --up: #c25b2e; --up-tint: #fbeae0;
        --mark: #d9a62c; --mark-deep: #a97a13; --guess: #8a8fa3;
        --good: #2f6f4a; --good-tint: #eaf3ec; --bad: #b3402b; --bad-tint: #fbeae6;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--ink);
      }}
      #rn-root *{{ box-sizing: border-box; }}
      #rn-root .stageLabel{{ font-size: 12.5px; font-weight:600; letter-spacing:.02em; color: var(--mark-deep); margin-bottom: 6px; }}
      #rn-root .prompt{{ font-size: 18px; font-weight:600; margin: 0 0 16px; line-height:1.4; }}
      #rn-root svg{{ width:100%; height:auto; display:block; touch-action: none; }}
      #rn-root .estimateHint{{ text-align:center; font-size: 13px; color: var(--ink-soft); margin: 6px 0 18px; }}
      #rn-root .legend{{ display:flex; gap: 18px; font-size: 12.5px; color: var(--ink-soft); margin: 4px 0 20px; }}
      #rn-root .legend span{{ display:inline-flex; align-items:center; gap:6px; }}
      #rn-root .dot{{ width:10px; height:10px; border-radius:50%; display:inline-block; }}
      #rn-root .choiceRow{{ display:flex; gap: 12px; margin: 4px 0 20px; flex-wrap:wrap; }}
      #rn-root .choiceBtn{{ flex:1 1 120px; font-family:'Courier New', monospace; font-size: 18px; font-weight:600; padding: 14px 10px; border-radius: 9px; border: 2px solid var(--line); background: #fff; cursor: pointer; text-align:center; transition: border-color .12s, background .12s; }}
      #rn-root .choiceBtn:hover:not(:disabled){{ border-color: var(--mark-deep); }}
      #rn-root .choiceBtn:disabled{{ cursor:default; }}
      #rn-root .choiceBtn.correct{{ border-color: var(--good); background: var(--good-tint); color: var(--good); }}
      #rn-root .choiceBtn.wrong{{ border-color: var(--bad); background: var(--bad-tint); color: var(--bad); }}
      #rn-root .feedback{{ font-size: 14px; font-weight:600; margin: -8px 0 18px; }}
      #rn-root .feedback.good{{ color: var(--good); }}
      #rn-root .feedback.bad{{ color: var(--bad); }}
      #rn-root .sentenceBox{{ font-size: 19px; font-weight: 600; line-height:1.7; margin: 6px 0 18px; }}
      #rn-root .sentenceBox .num{{ font-family:'Courier New', monospace; font-weight:600; }}
      #rn-root .sentenceBox .phrase{{ color: var(--mark-deep); }}
      #rn-root .blankInput{{ font-family:'Courier New', monospace; font-size: 19px; font-weight:600; width: 110px; text-align:center; padding: 6px 8px; border: none; border-bottom: 2.5px solid var(--ink); background: transparent; color: var(--ink); outline: none; margin: 0 2px; }}
      #rn-root .blankInput:focus{{ border-bottom-color: var(--mark-deep); }}
      #rn-root .blankInput.correct{{ border-bottom-color: var(--good); color: var(--good); background: var(--good-tint); }}
      #rn-root .blankInput.wrong{{ border-bottom-color: var(--bad); color: var(--bad); background: var(--bad-tint); }}
      #rn-root .blankInput:disabled{{ opacity:1; }}
      #rn-root .checkRow{{ display:flex; align-items:center; gap: 14px; margin-bottom: 6px; }}
      #rn-root .checkFeedback{{ font-size: 14px; font-weight:600; margin: 10px 0 4px; }}
      #rn-root .checkFeedback.good{{ color: var(--good); }}
      #rn-root .checkFeedback.bad{{ color: var(--bad); }}
      #rn-root .verdict{{ font-size: 17px; font-weight: 500; line-height:1.4; margin: 14px 0 4px; color: var(--ink-soft); }}
      #rn-root .verdict .num{{ font-family:'Courier New', monospace; font-weight:600; color: var(--ink); }}
      #rn-root .verdict .down{{ color: var(--down); }}
      #rn-root .verdict .up{{ color: var(--up); }}
      #rn-root .controls{{ display:flex; gap: 10px; margin-top: 20px; flex-wrap:wrap; }}
      #rn-root .btn{{ font-size: 14px; font-weight:600; padding: 12px 20px; border-radius: 8px; border: none; cursor: pointer; color: #fff; background: var(--ink); transition: opacity .12s; }}
      #rn-root .btn:hover{{ opacity:.9; }}
      #rn-root .btn:disabled{{ opacity:.4; cursor:not-allowed; }}
    </style>

    <div id="rn-root">
      <div class="stageLabel" id="rn-stageLabel"></div>
      <p class="prompt" id="rn-promptText"></p>
      <div id="rn-svgHost"></div>
      <div class="estimateHint" id="rn-estimateHint"></div>
      <div class="legend" id="rn-legendRow" style="display:none">
        <span><span class="dot" style="background:var(--guess)"></span>your estimate</span>
        <span><span class="dot" style="background:var(--mark)"></span>actual position</span>
      </div>
      <div class="choiceRow" id="rn-choiceRow" style="display:none"></div>
      <div class="feedback" id="rn-feedbackText"></div>
      <div id="rn-blankHost"></div>
      <div id="rn-verdictHost"></div>
      <div class="controls"><button class="btn" id="rn-advanceBtn"></button></div>
    </div>

    <script>
    (function(){{
      const LAYOUT = {{ W: 680, H: 200, padL: 60, padR: 60, y: 104 }};
      LAYOUT.xLower = LAYOUT.padL;
      LAYOUT.xUpper = LAYOUT.W - LAYOUT.padR;
      LAYOUT.xMid = (LAYOUT.xLower + LAYOUT.xUpper) / 2;

      const currentE = {place_e};
      const phrase = {phrase!r};
      const num = {value};
      let r = null;
      let stage = 'estimate';
      let guessT = null;
      let chosen = null;
      let checked = false;
      let isCorrect = false;

      function fmt(value, decimals){{
        const d = Math.max(decimals, 0);
        return Number(value).toFixed(d);
      }}
      function decimalsFor(e){{ return e < 0 ? -e : 0; }}

      function computeRounding(n, e){{
        const step = Math.pow(10, e);
        let scaled = n / step;
        scaled = Math.round(scaled * 1e9) / 1e9;
        const lowerScaled = Math.floor(scaled);
        const upperScaled = lowerScaled + 1;
        const frac = scaled - lowerScaled;
        const goesUp = frac >= 0.5;
        return {{
          lower: lowerScaled * step,
          upper: upperScaled * step,
          midpoint: (lowerScaled + 0.5) * step,
          rounded: (goesUp ? upperScaled : lowerScaled) * step,
          frac, goesUp,
          exactlyHalf: Math.abs(frac - 0.5) < 1e-9
        }};
      }}

      r = computeRounding(num, currentE);

      function buildSVG(){{
        const {{ W, H, y, xLower, xUpper, xMid }} = LAYOUT;
        const e = currentE;
        const decLower = decimalsFor(e);
        const decMid = e <= 0 ? decimalsFor(e) + 1 : 0;

        const showMid = stage !== 'estimate';
        const showActual = stage !== 'estimate';
        const showGuess = guessT !== null;
        const colorize = stage === 'answered' && checked;
        const lowerIsAnswer = colorize ? !r.goesUp : null;

        const t = (r.upper === r.lower) ? 0.5 : (num - r.lower) / (r.upper - r.lower);
        const clampT = Math.min(Math.max(t, 0), 1);
        const xActual = xLower + clampT * (xUpper - xLower);
        const xGuess = showGuess ? xLower + guessT * (xUpper - xLower) : null;

        let bandLower = '#eef0ee', bandUpper = '#eef0ee';
        let lowerColor = '#9aa0a8', upperColor = '#9aa0a8';
        let lowerWidth = 2, upperWidth = 2;
        if (colorize){{
          bandLower = lowerIsAnswer ? 'var(--down-tint)' : '#f2efe8';
          bandUpper = !lowerIsAnswer ? 'var(--up-tint)' : '#f2efe8';
          lowerColor = lowerIsAnswer ? 'var(--down)' : '#9aa0a8';
          upperColor = !lowerIsAnswer ? 'var(--up)' : '#9aa0a8';
          lowerWidth = lowerIsAnswer ? 3 : 2;
          upperWidth = !lowerIsAnswer ? 3 : 2;
        }}

        let svg = `<svg viewBox="0 0 ${{W}} ${{H}}" xmlns="http://www.w3.org/2000/svg">`;
        svg += `<rect id="rn-clickTarget" x="${{xLower}}" y="${{y-24}}" width="${{xUpper-xLower}}" height="48" fill="transparent"/>`;
        svg += `<rect x="${{xLower}}" y="${{y-3}}" width="${{(xUpper-xLower)/2}}" height="6" fill="${{bandLower}}"/>`;
        svg += `<rect x="${{xMid}}" y="${{y-3}}" width="${{(xUpper-xLower)/2}}" height="6" fill="${{bandUpper}}"/>`;
        svg += `<line x1="${{xLower}}" y1="${{y}}" x2="${{xUpper}}" y2="${{y}}" stroke="var(--line)" stroke-width="2"/>`;
        svg += `<line x1="${{xLower}}" y1="${{y-12}}" x2="${{xLower}}" y2="${{y+12}}" stroke="${{lowerColor}}" stroke-width="${{lowerWidth}}"/>`;
        svg += `<line x1="${{xUpper}}" y1="${{y-12}}" x2="${{xUpper}}" y2="${{y+12}}" stroke="${{upperColor}}" stroke-width="${{upperWidth}}"/>`;
        svg += `<line x1="${{xMid}}" y1="${{y-9}}" x2="${{xMid}}" y2="${{y+9}}" stroke="#b9b2a0" stroke-width="1.5" stroke-dasharray="3,3"/>`;
        svg += `<text x="${{xLower}}" y="${{y+36}}" text-anchor="middle" font-family="Courier New, monospace" font-size="18" font-weight="600" fill="${{lowerColor}}">${{fmt(r.lower, decLower)}}</text>`;
        svg += `<text x="${{xUpper}}" y="${{y+36}}" text-anchor="middle" font-family="Courier New, monospace" font-size="18" font-weight="600" fill="${{upperColor}}">${{fmt(r.upper, decLower)}}</text>`;
        if (showMid){{
          svg += `<text x="${{xMid}}" y="${{y-20}}" text-anchor="middle" font-family="Courier New, monospace" font-size="12.5" fill="#9a927e">midpoint ${{fmt(r.midpoint, decMid)}}</text>`;
        }}
        if (showGuess){{
          svg += `<line x1="${{xGuess}}" y1="${{y+14}}" x2="${{xGuess}}" y2="${{y+34}}" stroke="var(--guess)" stroke-width="2" stroke-dasharray="2,3"/>`;
          svg += `<polygon points="${{xGuess-7}},${{y+34}} ${{xGuess+7}},${{y+34}} ${{xGuess}},${{y+46}}" fill="var(--guess)"/>`;
        }}
        if (showActual){{
          svg += `<line x1="${{xActual}}" y1="${{y-38}}" x2="${{xActual}}" y2="${{y-8}}" stroke="var(--mark-deep)" stroke-width="2"/>`;
          svg += `<circle cx="${{xActual}}" cy="${{y}}" r="7.5" fill="var(--mark)" stroke="var(--mark-deep)" stroke-width="2"/>`;
          svg += `<rect x="${{xActual-46}}" y="${{y-64}}" width="92" height="26" rx="6" fill="var(--mark)" stroke="var(--mark-deep)" stroke-width="1.5"/>`;
          svg += `<text x="${{xActual}}" y="${{y-46}}" text-anchor="middle" font-family="Courier New, monospace" font-size="14" font-weight="600" fill="#3a2c05">${{num}}</text>`;
        }}
        svg += `</svg>`;
        return svg;
      }}

      function attachClickHandler(){{
        if (stage !== 'estimate') return;
        const svgEl = document.querySelector('#rn-svgHost svg');
        if (!svgEl) return;
        svgEl.style.cursor = 'pointer';
        svgEl.addEventListener('pointerdown', (evt) => {{
          const pt = svgEl.createSVGPoint();
          pt.x = evt.clientX; pt.y = evt.clientY;
          const ctm = svgEl.getScreenCTM();
          if (!ctm) return;
          const loc = pt.matrixTransform(ctm.inverse());
          let t = (loc.x - LAYOUT.xLower) / (LAYOUT.xUpper - LAYOUT.xLower);
          t = Math.min(Math.max(t, 0), 1);
          guessT = t;
          renderStage();
        }});
      }}

      function doCheck(){{
        const input = document.getElementById('rn-blankInput');
        const decLower = decimalsFor(currentE);
        const val = parseFloat((input.value || '').trim());
        checked = true;
        if (isNaN(val)){{
          isCorrect = false;
        }} else {{
          isCorrect = Math.abs(val - r.rounded) < 1e-9;
        }}
        renderStage();
        const reInput = document.getElementById('rn-blankInput');
        if (reInput && !isCorrect) reInput.focus();
      }}

      function renderStage(){{
        const stageLabel = document.getElementById('rn-stageLabel');
        const promptText = document.getElementById('rn-promptText');
        const svgHost = document.getElementById('rn-svgHost');
        const estimateHint = document.getElementById('rn-estimateHint');
        const legendRow = document.getElementById('rn-legendRow');
        const choiceRow = document.getElementById('rn-choiceRow');
        const feedbackText = document.getElementById('rn-feedbackText');
        const blankHost = document.getElementById('rn-blankHost');
        const verdictHost = document.getElementById('rn-verdictHost');
        const advanceBtn = document.getElementById('rn-advanceBtn');

        const decLower = decimalsFor(currentE);
        const lowerStr = fmt(r.lower, decLower);
        const upperStr = fmt(r.upper, decLower);

        svgHost.innerHTML = buildSVG();
        attachClickHandler();

        if (stage === 'estimate'){{
          stageLabel.textContent = 'Step 1 of 3 — Estimate';
          promptText.textContent = `Where does ${{num}} sit between ${{lowerStr}} and ${{upperStr}}?`;
          estimateHint.textContent = 'Click or tap the line to drop your estimate — then reveal the exact position.';
          legendRow.style.display = guessT !== null ? 'flex' : 'none';
          choiceRow.style.display = 'none';
          feedbackText.textContent = '';
          blankHost.innerHTML = '';
          verdictHost.innerHTML = '';
          advanceBtn.textContent = 'Reveal exact position';
          advanceBtn.disabled = false;
          advanceBtn.onclick = () => {{ stage = 'revealed'; renderStage(); }};
        }}
        else if (stage === 'revealed'){{
          stageLabel.textContent = 'Step 2 of 3 — Which is it closer to?';
          promptText.textContent = `${{num}} is placed exactly. Which value is it closer to?`;
          estimateHint.textContent = '';
          legendRow.style.display = guessT !== null ? 'flex' : 'none';

          choiceRow.style.display = 'flex';
          choiceRow.innerHTML = '';
          ['lower','upper'].forEach(side => {{
            const val = side === 'lower' ? lowerStr : upperStr;
            const btn = document.createElement('button');
            btn.className = 'choiceBtn';
            btn.textContent = val;
            btn.disabled = chosen !== null;
            if (chosen !== null){{
              const correctSide = r.goesUp ? 'upper' : 'lower';
              if (side === correctSide) btn.classList.add('correct');
              if (side === chosen && side !== correctSide) btn.classList.add('wrong');
            }}
            btn.addEventListener('click', () => {{
              chosen = side;
              renderStage();
            }});
            choiceRow.appendChild(btn);
          }});

          if (chosen === null){{
            feedbackText.textContent = '';
          }} else {{
            const correctSide = r.goesUp ? 'upper' : 'lower';
            if (chosen === correctSide){{
              feedbackText.className = 'feedback good';
              feedbackText.textContent = 'Correct!';
            }} else {{
              feedbackText.className = 'feedback bad';
              feedbackText.textContent = 'Not quite — have another look at the line.';
            }}
          }}

          blankHost.innerHTML = '';
          verdictHost.innerHTML = '';
          advanceBtn.textContent = 'Continue to answer';
          advanceBtn.disabled = false;
          advanceBtn.onclick = () => {{
            stage = 'answered';
            checked = false;
            isCorrect = false;
            renderStage();
            const inp = document.getElementById('rn-blankInput');
            if (inp) inp.focus();
          }};
        }}
        else if (stage === 'answered'){{
          stageLabel.textContent = 'Step 3 of 3 — Complete the sentence';
          promptText.textContent = 'Fill in the final blank.';
          estimateHint.textContent = '';
          legendRow.style.display = guessT !== null ? 'flex' : 'none';
          choiceRow.style.display = 'none';
          feedbackText.textContent = '';

          const inputClass = checked ? (isCorrect ? 'correct' : 'wrong') : '';
          blankHost.innerHTML = `
            <div class="sentenceBox">
              <span class="num">${{num}}</span> rounded to <span class="phrase">${{phrase}}</span> is
              <input id="rn-blankInput" class="blankInput ${{inputClass}}" type="text" inputmode="decimal" autocomplete="off" placeholder="?" value="${{checked && isCorrect ? fmt(r.rounded, decLower) : ''}}" ${{checked && isCorrect ? 'disabled' : ''}}>
            </div>
            <div class="checkRow">
              <button class="btn" id="rn-checkBtn">Check answer</button>
            </div>
            <div class="checkFeedback ${{checked ? (isCorrect ? 'good' : 'bad') : ''}}" id="rn-checkFeedback">
              ${{checked ? (isCorrect ? 'Correct — well done!' : `Not quite — try again.`) : ''}}
            </div>
          `;

          document.getElementById('rn-checkBtn').addEventListener('click', doCheck);
          const blankInput = document.getElementById('rn-blankInput');
          blankInput.addEventListener('keydown', (evt) => {{
            if (evt.key === 'Enter') doCheck();
          }});

          if (checked && isCorrect){{
            const dirClass = r.goesUp ? 'up' : 'down';
            const halfNote = r.exactlyHalf
              ? `<div style="font-size:12.5px;color:var(--ink-soft);margin-top:2px;">Exactly halfway between ${{lowerStr}} and ${{upperStr}} — rounds up by convention.</div>`
              : '';
            verdictHost.innerHTML = `
              <p class="verdict">
                <span class="num">${{num}}</span> is closer to
                <span class="num ${{dirClass}}">${{r.goesUp ? upperStr : lowerStr}}</span>.
              </p>
              ${{halfNote}}
            `;
          }} else {{
            verdictHost.innerHTML = '';
          }}

          advanceBtn.textContent = 'Done';
          advanceBtn.disabled = !(checked && isCorrect);
          advanceBtn.onclick = () => {{}};
        }}
      }}

      renderStage();
    }})();
    </script>
    """


def render_rounding_number_line_widget(value, place_e, height=520):
    """Render the guided rounding number-line walkthrough for `value` rounded to the place
    named by `place_e` (3=nearest 1000, 2=nearest 100, 1=nearest 10, 0=nearest whole number,
    -1/-2/-3 = 1/2/3 decimal places).

    Walks the pupil through estimating where the number sits on the line, revealing its exact
    position and choosing which end it's closer to, then completing the rounding sentence.
    """
    html_code = _build_html(value, place_e, height)
    components.html(html_code, height=height, scrolling=True)
