"""Interactive step-by-step column addition/subtraction widget ("chimney sum") — carrying for
addition, borrowing for subtraction, column by column, right to left.

Adapted from the `runChimneySum()` helper in
`/Users/luke/Library/CloudStorage/OneDrive-GlowScotland/Resources/Maths/scaffolds/numeracy_scaffolds.html`
(the "Decimal column calculator" tool) — trimmed to drop that page's own setup panel and
"type your own numbers" mode, since here the two numbers always come from the question that's
already been generated, following the same pattern as bus_stop_division_widget.py.

Usage:

    from core.ui.column_calculation_widget import render_column_calculation_widget

    render_column_calculation_widget(a=247, b=138, op="+")
    render_column_calculation_widget(a=27.58, b=13.27, op="-")
"""
import streamlit.components.v1 as components


def _build_html(a, b, op, dp, height):
    if op not in ("+", "-"):
        raise ValueError("op must be '+' or '-'")

    return f"""
    <style>
      #colc-root{{
        --ink: #22282f; --ink-soft: #5b6470; --line: #d8d2c4;
        --mark-deep: #a97a13; --good: #2f6f4a; --good-tint: #eaf3ec;
        --bad: #b3402b; --bad-tint: #fbeae6; --exchange: #a9455f;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--ink);
      }}
      #colc-root *{{ box-sizing: border-box; }}
      #colc-root .stageLabel{{ font-size: 12.5px; font-weight:600; letter-spacing:.02em; color: var(--mark-deep); margin-bottom: 6px; }}
      #colc-root .prompt{{ font-size: 18px; font-weight:600; margin: 0 0 16px; line-height:1.4; }}
      #colc-root .dccRow{{ display:flex; align-items:flex-end; gap:2px; }}
      #colc-root .dccGutter{{ width:32px; flex:0 0 32px; font-family:'Courier New', monospace; font-weight:700; font-size:26px; text-align:center; color: var(--ink-soft); }}
      #colc-root .subDigitCell{{ width:38px; flex:0 0 38px; font-family:'Courier New', monospace; font-weight:700; font-size:26px; text-align:center; height:32px; line-height:32px; }}
      #colc-root .subDigitCell.pointCol{{ width:14px; flex:0 0 14px; }}
      #colc-root .carryCell{{ width:38px; flex:0 0 38px; font-family:'Courier New', monospace; font-size:16px; font-weight:700; text-align:center; height:22px; line-height:22px; color: var(--exchange); }}
      #colc-root .carryCell.pointCol{{ width:14px; flex:0 0 14px; }}
      #colc-root .subBottomRow{{ border-bottom:3px solid var(--ink); padding-bottom:4px; margin-bottom:2px; }}
      #colc-root .subAnswerCell{{ width:38px; flex:0 0 38px; font-family:'Courier New', monospace; font-size:26px; font-weight:700; text-align:center; height:32px; line-height:32px; color: var(--good); }}
      #colc-root .subAnswerCell.pointCol{{ width:14px; flex:0 0 14px; color: var(--ink); }}
      #colc-root .subAnswerCell.placeholder{{ color: transparent; border-bottom: 3px dashed var(--line); }}
      #colc-root .subAnswerCell.active{{ background:#fdf6e3; border-radius:6px; color: var(--ink); border-bottom: 3px solid var(--mark-deep); }}
      #colc-root .dccOverflowGap{{ width:38px; flex:0 0 38px; }}
      #colc-root .carryInputBox{{ width:24px; font-family:'Courier New', monospace; font-size:14px; font-weight:700; text-align:center; padding:1px 0; border:1.5px solid var(--line); border-radius:5px; background:#fff; color: var(--ink); outline:none; }}
      #colc-root .carryInputBox:focus{{ border-color: var(--mark-deep); }}
      #colc-root .quotHint{{ font-size: 12.5px; color: var(--ink-soft); margin: -6px 0 12px; }}
      #colc-root .checkRow{{ display:flex; align-items:center; gap: 12px; margin-bottom: 6px; flex-wrap:wrap; }}
      #colc-root .blankInput{{ font-family:'Courier New', monospace; font-size: 19px; font-weight:600; width: 60px; text-align:center; padding: 7px 8px; border: 1.5px solid var(--line); border-radius:7px; background: #fff; color: var(--ink); outline: none; }}
      #colc-root .blankInput:focus{{ border-color: var(--mark-deep); }}
      #colc-root .checkFeedback{{ font-size: 13.5px; font-weight:600; margin: 2px 0 14px; min-height: 18px; }}
      #colc-root .checkFeedback.good{{ color: var(--good); }}
      #colc-root .checkFeedback.bad{{ color: var(--bad); }}
      #colc-root .btn{{ font-size: 14px; font-weight:600; padding: 10px 18px; border-radius: 8px; border: none; cursor: pointer; color: #fff; background: var(--ink); transition: opacity .12s; }}
      #colc-root .btn:hover{{ opacity:.9; }}
      #colc-root .finishBox{{ background: var(--good-tint); border: 1.5px solid var(--good); border-radius: 8px; padding: 14px 16px; margin: 10px 0 4px; }}
      #colc-root .finishBox .headline{{ font-weight:700; font-size:17px; color: var(--good); margin-bottom:6px; }}
      #colc-root .finishBox p{{ margin: 2px 0; font-size: 14px; color: var(--ink); line-height:1.5; }}
      #colc-root .finishBox .ans{{ font-family:'Courier New', monospace; font-weight:700; }}
    </style>

    <div id="colc-root">
      <div class="stageLabel" id="colc-stageLabel"></div>
      <p class="prompt" id="colc-promptText"></p>
      <div id="colc-gridHost"></div>
      <div class="quotHint" id="colc-quotHint"></div>
      <div class="checkRow" id="colc-checkRow">
        <input id="colc-answerInput" class="blankInput" type="text" inputmode="numeric">
        <button class="btn" id="colc-checkBtn">Check</button>
      </div>
      <div class="checkFeedback" id="colc-checkFeedback"></div>
      <div id="colc-finishHost"></div>
    </div>

    <script>
    (function(){{
      const A = {a};
      const B = {b};
      const OP = {op!r};
      const DP = {dp};

      function el(tag, cls, text){{
        var e = document.createElement(tag);
        if (cls) e.className = cls;
        if (text !== undefined && text !== null) e.textContent = text;
        return e;
      }}
      function padLeft(s, len){{ while (s.length < len) s = '0' + s; return s; }}
      function digitsOf(str){{
        var parts = str.split('.');
        var ip = parts[0].replace(/^0+(?=\\d)/, '') || '0';
        return {{ ip: ip, dp: parts[1] || '' }};
      }}

      var aStr = A.toFixed(DP), bStr = B.toFixed(DP);
      var a = digitsOf(aStr), b = digitsOf(bStr);
      var intLen = Math.max(a.ip.length, b.ip.length);
      var aIp = padLeft(a.ip, intLen), bIp = padLeft(b.ip, intLen);
      var aDp = a.dp, bDp = b.dp;
      var op = OP;
      if (op === '-' && parseFloat(bStr) > parseFloat(aStr)){{
        var t = aIp; aIp = bIp; bIp = t; var t2 = aDp; aDp = bDp; bDp = t2;
        var ts = aStr; aStr = bStr; bStr = ts;
      }}

      var columns = [];
      for (var i = 0; i < intLen; i++) columns.push({{ type: 'digit', top: +aIp[i], bottom: +bIp[i] }});
      if (DP > 0) columns.push({{ type: 'point' }});
      for (var j = 0; j < DP; j++) columns.push({{ type: 'digit', top: +aDp[j], bottom: +bDp[j] }});

      var order = [];
      for (var k = columns.length - 1; k >= 0; k--) if (columns[k].type === 'digit') order.push(k);

      var carry = 0, borrow = 0;
      order.forEach(function(idx){{
        var col = columns[idx];
        if (op === '+'){{
          var sum = col.top + col.bottom + carry;
          col.carryIn = carry; col.ansDigit = sum % 10; col.carryOut = Math.floor(sum / 10);
          carry = col.carryOut;
        }} else {{
          var t3 = col.top - borrow;
          col.borrowIn = borrow;
          if (t3 < col.bottom){{ t3 += 10; col.borrowOut = 1; }} else {{ col.borrowOut = 0; }}
          col.ansDigit = t3 - col.bottom;
          borrow = col.borrowOut;
        }}
      }});
      var overflow = (op === '+') ? carry : 0;

      var pos = 0;
      var carryConfirmed = columns.map(function(){{ return false; }});
      var finalCarryDigit = 0, finalCarryConfirmed = false;

      function activeIdx(){{ return pos < order.length ? order[pos] : null; }}
      function isSolved(idx){{ return order.indexOf(idx) !== -1 && order.indexOf(idx) < pos; }}
      function placeName(idx){{
        var pIdx = -1;
        for (var i2 = 0; i2 < columns.length; i2++) if (columns[i2].type === 'point') pIdx = i2;
        var lastIntIdx = pIdx === -1 ? columns.length - 1 : pIdx - 1;
        if (idx <= lastIntIdx){{
          var fromRight = lastIntIdx - idx;
          return ['units', 'tens', 'hundreds', 'thousands'][fromRight] || (fromRight + 1) + '-thousands';
        }}
        var decPos = idx - pIdx;
        return ['tenths', 'hundredths', 'thousandths'][decPos - 1] || decPos + '-decimal place';
      }}

      function mkCarryInput(wrapCls, id){{
        var wrap = el('div', wrapCls);
        var inp = document.createElement('input');
        inp.type = 'text'; inp.inputMode = 'numeric'; inp.maxLength = 1; inp.autocomplete = 'off';
        inp.className = 'carryInputBox'; inp.id = id;
        wrap.appendChild(inp);
        return wrap;
      }}
      function carryCellFor(idx, known, act){{
        var col = columns[idx];
        if (op !== '+') return el('div', 'carryCell', (known && col.borrowIn) ? '\u22121' : '');
        if (idx === order[0]) return el('div', 'carryCell');
        if (carryConfirmed[idx]) return el('div', 'carryCell', col.carryIn ? '+' + col.carryIn : '');
        if (act !== null) return mkCarryInput('carryCell', 'colc-carryInput' + idx);
        return el('div', 'carryCell');
      }}
      function overflowAnswerCell(act){{
        if (finalCarryConfirmed) return el('div', 'subAnswerCell', finalCarryDigit ? String(finalCarryDigit) : '');
        if (act !== null) return mkCarryInput('subAnswerCell', 'colc-finalCarryInput');
        return el('div', 'dccOverflowGap');
      }}

      function renderGrid(){{
        var gridHost = document.getElementById('colc-gridHost');
        gridHost.innerHTML = '';
        var act = activeIdx();
        var addMode = (op === '+');
        function makeRow(cls){{ return el('div', 'dccRow' + (cls ? ' ' + cls : '')); }}
        var carryRow = makeRow(), topRow = makeRow(), bottomRow = makeRow('subBottomRow'), ansRow = makeRow();
        if (addMode){{
          carryRow.appendChild(el('div', 'dccOverflowGap'));
          topRow.appendChild(el('div', 'dccOverflowGap'));
          bottomRow.appendChild(el('div', 'dccOverflowGap'));
          ansRow.appendChild(overflowAnswerCell(act));
        }}
        carryRow.appendChild(el('div', 'dccGutter'));
        topRow.appendChild(el('div', 'dccGutter'));
        bottomRow.appendChild(el('div', 'dccGutter', op === '+' ? '+' : '\u2212'));
        ansRow.appendChild(el('div', 'dccGutter'));

        columns.forEach(function(col, idx){{
          if (col.type === 'point'){{
            carryRow.appendChild(el('div', 'carryCell pointCol'));
            topRow.appendChild(el('div', 'subDigitCell pointCol', '.'));
            bottomRow.appendChild(el('div', 'subDigitCell pointCol', '.'));
            ansRow.appendChild(el('div', 'subAnswerCell pointCol', '.'));
            return;
          }}
          var known = isSolved(idx) || idx === act;
          carryRow.appendChild(carryCellFor(idx, known, act));
          topRow.appendChild(el('div', 'subDigitCell', String(col.top)));
          bottomRow.appendChild(el('div', 'subDigitCell', String(col.bottom)));
          if (isSolved(idx)) ansRow.appendChild(el('div', 'subAnswerCell', String(col.ansDigit)));
          else if (idx === act) ansRow.appendChild(el('div', 'subAnswerCell placeholder active', '?'));
          else ansRow.appendChild(el('div', 'subAnswerCell placeholder', ''));
        }});

        gridHost.appendChild(carryRow); gridHost.appendChild(topRow); gridHost.appendChild(bottomRow); gridHost.appendChild(ansRow);

        if (addMode && act !== null){{
          gridHost.querySelectorAll('.carryInputBox').forEach(function(inp){{
            inp.addEventListener('input', function(){{ inp.value = inp.value.replace(/[^0-9]/g, '').slice(0, 1); }});
            inp.addEventListener('keydown', function(e){{ if (e.key === 'Enter') document.getElementById('colc-checkBtn').click(); }});
          }});
        }}
      }}

      function finalAnswerStr(){{
        var s = columns.map(function(c){{ return c.type === 'point' ? '.' : String(c.ansDigit); }}).join('');
        if (overflow > 0) s = overflow + s;
        return s;
      }}

      function updateStage(){{
        renderGrid();
        var act = activeIdx();
        var promptEl = document.getElementById('colc-promptText'), hintEl = document.getElementById('colc-quotHint'),
            checkRow = document.getElementById('colc-checkRow'), finishHost = document.getElementById('colc-finishHost'),
            fb = document.getElementById('colc-checkFeedback'), stageLbl = document.getElementById('colc-stageLabel');
        finishHost.innerHTML = ''; fb.textContent = ''; fb.className = 'checkFeedback';
        var answerInput = document.getElementById('colc-answerInput');
        answerInput.value = ''; answerInput.disabled = false;
        document.getElementById('colc-checkBtn').disabled = false;

        if (act !== null){{
          stageLbl.textContent = 'Step ' + (pos + 1) + ' of ' + (order.length + 1);
          var col = columns[act];
          var extra = '';
          if (op === '+' && col.carryIn) extra = ', plus the ' + col.carryIn + ' carried in';
          if (op === '-' && col.borrowIn) extra = ' (remember you borrowed a ten from this column)';
          promptEl.textContent = 'Work out the ' + placeName(act) + ' column: ' + col.top + ' ' + op + ' ' + col.bottom + extra + '.';
          checkRow.style.display = 'flex';
          if (op === '+'){{
            hintEl.textContent = (order.indexOf(act) === order.length - 1)
              ? 'Type your answer below the line. If it carries, write that digit in the box on the far left too \u2014 then check them together.'
              : 'Type your answer below the line. If this column totals 10 or more, write the carried ten in the small box above the next column too \u2014 then check them together.';
          }} else {{ hintEl.textContent = ''; }}
          setTimeout(function(){{ answerInput.focus(); }}, 30);
        }} else {{
          checkRow.style.display = 'none';
          hintEl.textContent = '';
          stageLbl.textContent = 'Finished';
          var aTop = columns.map(function(c){{ return c.type === 'point' ? '.' : c.top; }}).join('');
          var bBottom = columns.map(function(c){{ return c.type === 'point' ? '.' : c.bottom; }}).join('');
          promptEl.textContent = 'Every column is solved.';
          finishHost.innerHTML = '<div class="finishBox"><div class="headline">' + (op === '+' ? 'Added!' : 'Subtracted!') + '</div>' +
            '<p>' + aTop + ' ' + op + ' ' + bBottom + ' = <span class="ans">' + finalAnswerStr() + '</span></p></div>';
        }}
      }}

      function doCheck(){{
        var act = activeIdx();
        if (act === null) return;
        var answerInput = document.getElementById('colc-answerInput');
        var val = parseInt(answerInput.value, 10);
        var col = columns[act];
        var fb = document.getElementById('colc-checkFeedback');
        if (isNaN(val)){{ fb.textContent = 'Type a number in the box first.'; fb.className = 'checkFeedback bad'; return; }}

        if (op !== '+'){{
          if (val === col.ansDigit){{
            fb.textContent = '\u2713 Correct!'; fb.className = 'checkFeedback good';
            pos++; answerInput.disabled = true; document.getElementById('colc-checkBtn').disabled = true;
            setTimeout(updateStage, 350);
          }} else {{
            fb.textContent = '\u2717 Not quite \u2014 try again.'; fb.className = 'checkFeedback bad';
          }}
          return;
        }}

        var posIdx = order.indexOf(act);
        var isLast = posIdx === order.length - 1;
        var carryEl = isLast ? document.getElementById('colc-finalCarryInput') : document.getElementById('colc-carryInput' + order[posIdx + 1]);
        var rawCarry = carryEl ? carryEl.value.trim() : '';
        var carryVal = rawCarry === '' ? 0 : parseInt(rawCarry, 10);
        var answerOk = val === col.ansDigit;
        var carryOk = carryVal === col.carryOut;

        if (answerOk && carryOk){{
          fb.textContent = '\u2713 Correct!'; fb.className = 'checkFeedback good';
          if (isLast){{ finalCarryDigit = col.carryOut === 1 ? 1 : 0; finalCarryConfirmed = true; }}
          else {{ carryConfirmed[order[posIdx + 1]] = true; }}
          pos++; answerInput.disabled = true; document.getElementById('colc-checkBtn').disabled = true;
          setTimeout(updateStage, 350);
          return;
        }}
        if (!answerOk && col.carryOut === 1 && val === col.top + col.bottom + (col.carryIn || 0)){{
          fb.textContent = "That's the full total for this column. Write just the last digit here, and carry the other digit into the box above the next column.";
        }} else if (!answerOk){{
          fb.textContent = '\u2717 Not quite \u2014 check the answer digit and try again.';
        }} else if (col.carryOut === 1){{
          fb.textContent = "The answer digit is right, but this column totals 10 or more \u2014 don't forget to carry the ten.";
        }} else {{
          fb.textContent = "The answer digit is right, but check the carry box \u2014 this column doesn't need one.";
        }}
        fb.className = 'checkFeedback bad';
        if (!answerOk){{ answerInput.value = ''; answerInput.focus(); }}
        if (!carryOk && carryEl){{ carryEl.value = ''; if (answerOk) carryEl.focus(); }}
      }}

      document.getElementById('colc-checkBtn').addEventListener('click', doCheck);
      document.getElementById('colc-answerInput').addEventListener('keydown', function(e){{ if (e.key === 'Enter'){{ e.preventDefault(); doCheck(); }} }});
      updateStage();
    }})();
    </script>
    """


def render_column_calculation_widget(a, b, op, dp=0, height=420):
    """Render the interactive column addition/subtraction ("chimney sum") walkthrough for
    `a op b`, carrying (addition) or borrowing (subtraction) column by column, right to left.

    a, b: numbers. op: '+' or '-'. dp: decimal places to align both numbers to (0 for whole
    numbers).
    """
    html_code = _build_html(a, b, op, dp, height)
    components.html(html_code, height=height, scrolling=True)
