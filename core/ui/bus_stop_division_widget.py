"""Interactive step-by-step bus-stop (long) division widget.

Adapted from the standalone prototype at
`/Users/luke/Library/CloudStorage/OneDrive-GlowScotland/Resources/Maths/scaffolds/maths_scaffolds.html`
(the "Bus stop division with decimals" tool) — trimmed to drop that page's own
setup panel and "type your own numbers" compose mode, since here the dividend
and divisor always come from the question that's already been generated.

Walks the pupil through the bus-stop method column by column: for each digit,
"how many Ns go into this?" then "how many are left over?", continuing into
decimal places (with a ×divisor reference table toggle) until the division
terminates or a repeating remainder is detected, at which point the repeating
decimal digits are underlined.

Usage:

    from core.ui.bus_stop_division_widget import render_bus_stop_division_widget

    render_bus_stop_division_widget(dividend=428, divisor=7)
"""
import json
import streamlit.components.v1 as components


def _build_html(dividend, divisor, max_decimals, height):
    if divisor < 2:
        raise ValueError("divisor must be at least 2")
    if dividend <= divisor:
        raise ValueError("dividend must be greater than divisor")

    return f"""
    <style>
      #bsw-root{{
        --ink: #22282f; --ink-soft: #5b6470; --line: #d8d2c4;
        --mark-deep: #a97a13; --good: #2f6f4a; --good-tint: #eaf3ec;
        --bad: #b3402b; --bad-tint: #fbeae6; --exchange: #a9455f;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--ink);
      }}
      #bsw-root *{{ box-sizing: border-box; }}
      #bsw-root .topRow{{ display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap; margin-bottom: 6px; }}
      #bsw-root .questionLabel{{ font-size: 13px; font-weight:600; letter-spacing:.02em; color: var(--mark-deep); }}
      #bsw-root .layoutRow{{ display:flex; gap: 26px; align-items:flex-start; flex-wrap:wrap; }}
      #bsw-root .busstopCol{{ flex: 1 1 320px; min-width: 280px; }}
      #bsw-root .tableCol{{ flex: 0 0 150px; }}
      #bsw-root .busstopGrid{{
        display:grid; grid-template-columns: max-content 1fr;
        row-gap: 4px; column-gap: 10px; align-items:end; margin: 18px 0 8px;
      }}
      #bsw-root #bsw-quotientRow{{ grid-row:1; grid-column:2; display:flex; align-items:flex-end; gap:3px; padding: 0 12px; min-height: 32px; }}
      #bsw-root #bsw-divisorLabel{{
        grid-row:2; grid-column:1; font-family:'Courier New', monospace; font-weight:700; font-size:24px; padding-bottom: 10px;
      }}
      #bsw-root #bsw-dividendArea{{
        grid-row:2; grid-column:2; border-left: 3px solid var(--ink); border-top: 3px solid var(--ink);
        border-top-left-radius: 3px; display:flex; gap:3px; padding: 8px 12px 8px 12px;
      }}
      #bsw-root .digitCell{{
        position:relative; font-family:'Courier New', monospace; font-size:22px; font-weight:600; width:36px; text-align:center;
      }}
      #bsw-root .digitCell.active{{ color: var(--mark-deep); }}
      #bsw-root .quotDigit{{
        font-family:'Courier New', monospace; font-size:22px; font-weight:700;
        width:36px; height:32px; line-height:32px; text-align:center; color: var(--ink);
      }}
      #bsw-root .quotDigit.overline{{ text-decoration: overline; text-decoration-thickness: 2.5px; text-underline-offset: 3px; }}
      #bsw-root .quotInputBox{{
        font-family:'Courier New', monospace; font-size:22px; font-weight:700;
        width:36px; height:32px; line-height:normal; text-align:center;
        border: none; border-bottom: 2.5px solid var(--ink);
        background: transparent; color: var(--ink); outline:none; padding:0; margin:0;
      }}
      #bsw-root .quotInputBox:focus{{ border-bottom-color: var(--mark-deep); background: #fffaf0; }}
      #bsw-root .quotInputBox::-webkit-outer-spin-button, #bsw-root .quotInputBox::-webkit-inner-spin-button{{ -webkit-appearance:none; margin:0; }}
      #bsw-root .pointGap{{ width:12px; display:flex; align-items:flex-end; font-weight:700; font-size:22px; }}
      #bsw-root .exchangeBadge{{ position:absolute; top:-16px; left:-2px; font-size:12.5px; font-weight:700; color: var(--exchange); }}
      #bsw-root .exchangeInputBox{{
        position:absolute; top:-19px; left:-5px; width:24px; height:17px;
        font-family:'Courier New', monospace; font-size:12.5px; font-weight:700;
        text-align:center; line-height:normal; border:none; border-bottom:2px solid var(--exchange);
        background:transparent; color:var(--exchange); outline:none; padding:0; margin:0;
      }}
      #bsw-root .exchangeInputBox:focus{{ background:#fdf0f2; }}
      #bsw-root .digitCell.exchangeTarget{{ background:#fdf6e3; border-radius:4px; }}
      #bsw-root .stagePrompt{{ font-size: 17px; font-weight:600; margin: 6px 0 12px; line-height:1.4; }}
      #bsw-root .stagePrompt .n{{ font-family:'Courier New', monospace; font-weight:700; color: var(--mark-deep); }}
      #bsw-root .answerRow{{ display:flex; gap:10px; align-items:center; margin-bottom: 8px; }}
      #bsw-root #bsw-answerInput{{
        width: 100px; font-family:'Courier New', monospace; font-size: 20px; font-weight:600;
        padding: 9px 11px; border: 1.5px solid var(--line); border-radius: 7px;
        background: #fff; color: var(--ink); outline: none;
      }}
      #bsw-root #bsw-answerInput:focus{{ border-color: var(--mark-deep); }}
      #bsw-root .quotHint{{ font-size: 12.5px; color: var(--ink-soft); margin: -6px 0 12px; }}
      #bsw-root .checkFeedback{{ font-size: 13.5px; font-weight:600; margin: 2px 0 14px; min-height: 18px; }}
      #bsw-root .checkFeedback.good{{ color: var(--good); }}
      #bsw-root .checkFeedback.bad{{ color: var(--bad); }}
      #bsw-root .finishBox{{ background: var(--good-tint); border: 1.5px solid var(--good); border-radius: 8px; padding: 14px 16px; margin: 10px 0 4px; }}
      #bsw-root .finishBox .headline{{ font-weight:700; font-size:17px; color: var(--good); margin-bottom:6px; }}
      #bsw-root .finishBox p{{ margin: 2px 0; font-size: 14px; color: var(--ink); line-height:1.5; }}
      #bsw-root .finishBox .ans{{ font-family:'Courier New', monospace; font-weight:700; }}
      #bsw-root .btn{{
        font-size: 14px; font-weight:600; padding: 10px 18px; border-radius: 8px; border: none;
        cursor: pointer; color: #fff; background: var(--ink); transition: opacity .12s;
      }}
      #bsw-root .btn:hover{{ opacity:.9; }}
      #bsw-root .btn.secondary{{ background:#fff; color:var(--ink); border:1.5px solid var(--line); }}
      #bsw-root .btn.small{{ font-size:13px; padding:8px 14px; }}
      #bsw-root .timesTable{{
        display:none; background: #fff; border: 1px solid var(--line); border-radius: 8px;
        padding: 12px 14px; font-family:'Courier New', monospace; font-size: 14px; line-height: 1.9;
      }}
      #bsw-root .timesTable.show{{ display:block; }}
      #bsw-root .timesTable .ttHead{{ font-weight:600; font-size:12.5px; color:var(--ink-soft); margin-bottom:6px; }}
    </style>

    <div id="bsw-root">
      <div class="topRow">
        <div class="questionLabel" id="bsw-questionLabel"></div>
        <button class="btn secondary small" id="bsw-tableToggleBtn"></button>
      </div>
      <div class="layoutRow">
        <div class="busstopCol">
          <div class="busstopGrid">
            <div id="bsw-quotientRow"></div>
            <div id="bsw-divisorLabel"></div>
            <div id="bsw-dividendArea"></div>
          </div>
          <p class="stagePrompt" id="bsw-stagePrompt"></p>
          <div class="quotHint" id="bsw-quotHint"></div>
          <div class="answerRow" id="bsw-answerRow">
            <input type="number" id="bsw-answerInput" inputmode="numeric">
          </div>
          <div class="answerRow">
            <button class="btn" id="bsw-checkBtn">Check</button>
          </div>
          <div class="checkFeedback" id="bsw-checkFeedback"></div>
          <div id="bsw-finishHost"></div>
        </div>
        <div class="tableCol">
          <div class="timesTable" id="bsw-timesTable"></div>
        </div>
      </div>
    </div>

    <script>
    (function(){{
      const DIVIDEND = {dividend};
      const DIVISOR = {divisor};
      const MAX_DECIMALS = {max_decimals};

      function computeSteps(dividend, divisor, maxDecimals){{
        const wholeDigits = String(dividend).split('').map(Number);
        let running = 0;
        const steps = [];
        wholeDigits.forEach(d => {{
          const combined = running*10 + d;
          const q = Math.floor(combined/divisor);
          const rem = combined % divisor;
          steps.push({{ phase:'whole', digit:d, combined, quotient:q, remainder:rem }});
          running = rem;
        }});
        const decimals = [];
        const seen = new Map();
        let repeatStart = null, terminates = false;
        for (let i=0; i<maxDecimals; i++){{
          if (running === 0){{ terminates = true; break; }}
          if (seen.has(running)){{ repeatStart = seen.get(running); break; }}
          seen.set(running, i);
          const combined = running*10;
          const q = Math.floor(combined/divisor);
          const rem = combined % divisor;
          steps.push({{ phase:'decimal', digit:0, combined, quotient:q, remainder:rem, decimalIndex:i }});
          decimals.push(q);
          running = rem;
        }}
        return {{ wholeDigits, steps, decimals, terminates, repeatStart, wholeValue: Math.floor(dividend/divisor) }};
      }}

      const result = computeSteps(DIVIDEND, DIVISOR, MAX_DECIMALS);
      let columns = result.wholeDigits.map(d => ({{ type:'digit', digit:String(d), quotient:null, exchange:null }}));
      let stepIndex = 0;
      let substage = 'quotient';
      let finished = false;
      let pendingNextColIdx = null;

      document.getElementById('bsw-questionLabel').textContent = `${{DIVIDEND}} ÷ ${{DIVISOR}}`;
      document.getElementById('bsw-divisorLabel').textContent = DIVISOR;

      const tableToggleBtn = document.getElementById('bsw-tableToggleBtn');
      function buildTimesTable(){{
        const t = document.getElementById('bsw-timesTable');
        let html = `<div class="ttHead">×${{DIVISOR}} table</div>`;
        for (let i=1; i<=12; i++){{ html += `${{i}} × ${{DIVISOR}} = ${{i*DIVISOR}}<br>`; }}
        t.innerHTML = html;
      }}
      buildTimesTable();
      tableToggleBtn.textContent = `Show ×${{DIVISOR}} table`;
      tableToggleBtn.addEventListener('click', () => {{
        const t = document.getElementById('bsw-timesTable');
        t.classList.toggle('show');
        tableToggleBtn.textContent = t.classList.contains('show') ? 'Hide table' : `Show ×${{DIVISOR}} table`;
      }});

      function activeColumnIndexFor(stepIdx){{
        let count = -1;
        for (let i=0;i<columns.length;i++){{
          if (columns[i].type === 'digit'){{ count++; if (count === stepIdx) return i; }}
        }}
        return -1;
      }}
      function activeColumnIndex(){{ return activeColumnIndexFor(stepIndex); }}

      function render(){{
        const quotientRow = document.getElementById('bsw-quotientRow');
        const dividendArea = document.getElementById('bsw-dividendArea');
        const stagePrompt = document.getElementById('bsw-stagePrompt');
        const answerRow = document.getElementById('bsw-answerRow');
        const checkFeedback = document.getElementById('bsw-checkFeedback');
        const finishHost = document.getElementById('bsw-finishHost');
        const quotHint = document.getElementById('bsw-quotHint');

        quotientRow.innerHTML = '';
        dividendArea.innerHTML = '';
        columns.forEach((col, idx) => {{
          if (col.type === 'point'){{
            quotientRow.innerHTML += `<div class="pointGap">.</div>`;
            dividendArea.innerHTML += `<div class="pointGap">.</div>`;
            return;
          }}
          const isActive = !finished && idx === activeColumnIndex();
          const isQuotientTurn = isActive && substage === 'quotient';
          if (isQuotientTurn){{
            quotientRow.innerHTML += `<input type="number" inputmode="numeric" class="quotInputBox" id="bsw-quotInput">`;
          }} else {{
            quotientRow.innerHTML += `<div class="quotDigit ${{col.overline ? 'overline' : ''}}">${{col.quotient !== null ? col.quotient : ''}}</div>`;
          }}
          const exchangeHtml = col.exchangeInputActive
            ? `<input type="number" inputmode="numeric" class="exchangeInputBox" id="bsw-exchangeInput">`
            : (col.exchange ? `<span class="exchangeBadge">${{col.exchange}}</span>` : '');
          dividendArea.innerHTML += `<div class="digitCell ${{isActive ? 'active' : ''}} ${{col.exchangeInputActive ? 'exchangeTarget' : ''}}">${{exchangeHtml}}${{col.digit}}</div>`;
        }});

        if (finished){{
          stagePrompt.textContent = '';
          answerRow.style.display = 'none';
          checkFeedback.textContent = '';
          return;
        }}

        finishHost.innerHTML = '';
        const step = result.steps[stepIndex];

        if (substage === 'quotient'){{
          stagePrompt.innerHTML = `How many <span class="n">${{DIVISOR}}s</span> go into <span class="n">${{step.combined}}</span>?`;
          quotHint.textContent = 'Type your answer in the box above the line, then check it.';
          answerRow.style.display = 'none';
          const quotInput = document.getElementById('bsw-quotInput');
          if (quotInput){{
            quotInput.addEventListener('keydown', (e) => {{ if (e.key === 'Enter') doCheck(); }});
            setTimeout(() => quotInput.focus(), 30);
          }}
        }} else {{
          stagePrompt.innerHTML = `How many are left over?`;
          if (pendingNextColIdx !== null){{
            quotHint.textContent = 'Type it in the small box above the next number, then check it.';
            answerRow.style.display = 'none';
            const exchangeInput = document.getElementById('bsw-exchangeInput');
            if (exchangeInput){{
              exchangeInput.addEventListener('keydown', (e) => {{ if (e.key === 'Enter') doCheck(); }});
              setTimeout(() => exchangeInput.focus(), 30);
            }}
          }} else {{
            quotHint.textContent = '';
            answerRow.style.display = 'flex';
            const answerInput = document.getElementById('bsw-answerInput');
            answerInput.value = '';
            setTimeout(() => answerInput.focus(), 30);
          }}
        }}
        checkFeedback.textContent = '';
        checkFeedback.className = 'checkFeedback';
      }}

      document.getElementById('bsw-checkBtn').addEventListener('click', doCheck);
      document.getElementById('bsw-answerInput').addEventListener('keydown', (e) => {{ if (e.key === 'Enter') doCheck(); }});

      function doCheck(){{
        const checkFeedback = document.getElementById('bsw-checkFeedback');
        const step = result.steps[stepIndex];
        const colIdx = activeColumnIndex();
        const input = substage === 'quotient'
          ? document.getElementById('bsw-quotInput')
          : (pendingNextColIdx !== null ? document.getElementById('bsw-exchangeInput') : document.getElementById('bsw-answerInput'));
        if (!input) return;
        const val = parseInt(input.value, 10);
        if (isNaN(val)){{
          checkFeedback.textContent = 'Type a number in the box first.';
          checkFeedback.className = 'checkFeedback bad';
          return;
        }}
        if (substage === 'quotient'){{
          if (val === step.quotient){{
            columns[colIdx].quotient = val;
            checkFeedback.textContent = 'Correct!';
            checkFeedback.className = 'checkFeedback good';
            substage = 'remainder';
            revealNextColumnForExchange();
            setTimeout(() => {{ render(); }}, 350);
          }} else {{
            checkFeedback.textContent = 'Not quite — try again.';
            checkFeedback.className = 'checkFeedback bad';
            input.value = '';
            input.focus();
          }}
        }} else {{
          if (val === step.remainder){{
            checkFeedback.textContent = 'Correct!';
            checkFeedback.className = 'checkFeedback good';
            if (pendingNextColIdx !== null){{
              columns[pendingNextColIdx].exchange = val > 0 ? val : null;
              columns[pendingNextColIdx].exchangeInputActive = false;
            }}
            goToNextStepOrFinish();
          }} else {{
            checkFeedback.textContent = 'Not quite — try again.';
            checkFeedback.className = 'checkFeedback bad';
            input.value = '';
            input.focus();
          }}
        }}
      }}

      function revealNextColumnForExchange(){{
        const nextIndex = stepIndex + 1;
        if (nextIndex >= result.steps.length){{ pendingNextColIdx = null; return; }}
        const nextStep = result.steps[nextIndex];
        const curStep = result.steps[stepIndex];
        if (nextStep.phase === 'decimal' && curStep.phase === 'whole'){{
          columns.push({{ type:'point' }});
        }}
        if (nextStep.phase === 'decimal'){{
          columns.push({{ type:'digit', digit:'0', quotient:null, exchange:null, exchangeInputActive:true }});
          pendingNextColIdx = columns.length - 1;
        }} else {{
          const idx = activeColumnIndexFor(nextIndex);
          columns[idx].exchangeInputActive = true;
          pendingNextColIdx = idx;
        }}
      }}

      function goToNextStepOrFinish(){{
        const nextIndex = stepIndex + 1;
        if (nextIndex < result.steps.length){{
          stepIndex = nextIndex;
          substage = 'quotient';
          pendingNextColIdx = null;
          setTimeout(() => {{ render(); }}, 350);
        }} else {{
          setTimeout(() => finish(), 350);
        }}
      }}

      function finish(){{
        finished = true;
        const finishHost = document.getElementById('bsw-finishHost');
        const decLen = result.decimals.length;
        if (result.terminates){{
          if (decLen === 0){{
            finishHost.innerHTML = `
              <div class="finishBox">
                <div class="headline">Remainder 0 — division complete!</div>
                <p><span class="n">${{DIVIDEND}}</span> ÷ <span class="n">${{DIVISOR}}</span> = <span class="ans">${{result.wholeValue}}</span> exactly.</p>
              </div>`;
          }} else {{
            const decStr = result.decimals.join('');
            finishHost.innerHTML = `
              <div class="finishBox">
                <div class="headline">Remainder 0 — division complete!</div>
                <p><span class="n">${{DIVIDEND}}</span> ÷ <span class="n">${{DIVISOR}}</span> = <span class="ans">${{result.wholeValue}}.${{decStr}}</span></p>
              </div>`;
          }}
        }} else {{
          const repeatStart = result.repeatStart;
          const startColIdx = activeColumnIndexFor(result.wholeDigits.length + repeatStart);
          for (let i = startColIdx; i < columns.length; i++){{
            if (columns[i].type === 'digit') columns[i].overline = true;
          }}
          const nonRepeating = result.decimals.slice(0, repeatStart).join('');
          const repeating = result.decimals.slice(repeatStart).join('');
          finishHost.innerHTML = `
            <div class="finishBox">
              <div class="headline">The remainder just repeated — the digits repeat forever!</div>
              <p><span class="n">${{DIVIDEND}}</span> ÷ <span class="n">${{DIVISOR}}</span> = <span class="ans">${{result.wholeValue}}.${{nonRepeating}}<span style="text-decoration:overline">${{repeating}}</span></span> (recurring)</p>
            </div>`;
        }}
        render();
      }}

      render();
    }})();
    </script>
    """


def render_bus_stop_division_widget(dividend, divisor, max_decimals=10, height=560):
    """Render the interactive bus-stop division walkthrough for `dividend ÷ divisor`.

    Walks the pupil through the long-division method column by column, checking
    each quotient digit and remainder as they go, and reveals whether the
    division terminates or recurs once complete.
    """
    html_code = _build_html(dividend, divisor, max_decimals, height)
    components.html(html_code, height=height, scrolling=True)
