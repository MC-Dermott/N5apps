"""Interactive step-by-step lattice multiplication widget.

Adapted from the standalone prototype at
`/Users/luke/Library/CloudStorage/OneDrive-GlowScotland/Resources/Maths/scaffolds/numeracy_scaffolds.html`
(the "Lattice multiplication" tool) — trimmed to drop that page's own setup panel and
"type your own numbers"/"random question" modes, since here the two numbers always come from
the question that's already been generated, following the same pattern as
bus_stop_division_widget.py.

Walks the pupil through the lattice method in three stages: fill in the grid's digits around
the edge, multiply cell by cell (with a per-cell times-table hint toggle), then add down each
diagonal band with carry boxes — the same mechanic as column_calculation_widget.py's addition
mode.

Usage:

    from core.ui.lattice_multiplication_widget import render_lattice_multiplication_widget

    render_lattice_multiplication_widget(a=236, b=47)
"""
import streamlit.components.v1 as components


def _build_html(a_str, b_str, height):
    if not a_str.isdigit() or not b_str.isdigit():
        raise ValueError("a and b must be whole numbers")

    return f"""
    <style>
      #lat-root{{
        --ink: #22282f; --ink-soft: #5b6470; --line: #d8d2c4;
        --mark-deep: #a97a13; --good: #2f6f4a; --good-tint: #eaf3ec;
        --bad: #b3402b; --bad-tint: #fbeae6; --exchange: #a9455f;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--ink);
      }}
      #lat-root *{{ box-sizing: border-box; }}
      #lat-root .stageLabel{{ font-size: 12.5px; font-weight:600; letter-spacing:.02em; color: var(--mark-deep); margin-bottom: 6px; }}
      #lat-root .prompt{{ font-size: 18px; font-weight:600; margin: 0 0 16px; line-height:1.4; }}
      #lat-root .stagePrompt{{ font-size: 17px; font-weight:600; margin: 6px 0 12px; line-height:1.4; }}
      #lat-root .checkRow{{ display:flex; align-items:center; gap: 12px; margin-bottom: 6px; flex-wrap:wrap; }}
      #lat-root .blankInput{{ font-family:'Courier New', monospace; font-size: 19px; font-weight:600; width: 44px; text-align:center; padding: 7px 8px; border: 1.5px solid var(--line); border-radius:7px; background: #fff; color: var(--ink); outline: none; margin: 0 2px; }}
      #lat-root .blankInput:focus{{ border-color: var(--mark-deep); }}
      #lat-root .checkFeedback{{ font-size: 13.5px; font-weight:600; margin: 2px 0 14px; min-height: 18px; }}
      #lat-root .checkFeedback.good{{ color: var(--good); }}
      #lat-root .checkFeedback.bad{{ color: var(--bad); }}
      #lat-root .btn{{ font-size: 14px; font-weight:600; padding: 10px 18px; border-radius: 8px; border: none; cursor: pointer; color: #fff; background: var(--ink); transition: opacity .12s; }}
      #lat-root .btn:hover{{ opacity:.9; }}
      #lat-root .btn:disabled{{ opacity:.4; cursor:not-allowed; }}
      #lat-root .btn.secondary{{ background:#fff; color:var(--ink); border:1.5px solid var(--line); }}
      #lat-root .btn.small{{ font-size:13px; padding:8px 14px; }}
      #lat-root .quotHint{{ font-size: 12.5px; color: var(--ink-soft); margin: -6px 0 12px; }}
      #lat-root .finishBox{{ background: var(--good-tint); border: 1.5px solid var(--good); border-radius: 8px; padding: 14px 16px; margin: 10px 0 4px; }}
      #lat-root .finishBox .headline{{ font-weight:700; font-size:17px; color: var(--good); margin-bottom:6px; }}
      #lat-root .finishBox p{{ margin: 2px 0; font-size: 14px; color: var(--ink); line-height:1.5; }}
      #lat-root .finishBox .ans{{ font-family:'Courier New', monospace; font-weight:700; }}

      #lat-root .answerRow{{ display:flex; gap:10px; align-items:center; margin-bottom: 8px; flex-wrap:wrap; }}
      #lat-root .timesTable{{ display:none; background:#fff; border:1px solid var(--line); border-radius:8px; padding:12px 14px; font-family:'Courier New', monospace; font-size:14px; line-height:1.9; margin-bottom:10px; }}
      #lat-root .timesTable.show{{ display:block; }}
      #lat-root .timesTable .ttHead{{ font-weight:600; font-size:12.5px; color:var(--ink-soft); margin-bottom:6px; }}

      #lat-root .latticeGrid{{ display:inline-grid; margin: 10px 0; }}
      #lat-root .latticeCornerCell{{ width:54px; height:54px; }}
      #lat-root .latticeHeaderCell{{ width:54px; height:54px; display:flex; align-items:center; justify-content:center; font-family:'Courier New', monospace; font-weight:700; font-size:22px; border:2px solid var(--ink); background:#fff; }}
      #lat-root .latticeHeaderCell.solved{{ background:#fdf6e3; color: var(--mark-deep); }}
      #lat-root .latticeHeaderCell input{{ width:32px; text-align:center; font-family:'Courier New', monospace; font-weight:700; font-size:20px; border:1.5px solid var(--line); border-radius:6px; padding:4px 2px; outline:none; background:#fff; color:var(--ink); }}
      #lat-root .latticeHeaderCell input:focus{{ border-color: var(--mark-deep); }}
      #lat-root .latticeHeaderCell input.correct{{ border-color: var(--good); color: var(--good); }}
      #lat-root .latticeHeaderCell input.wrong{{ border-color: var(--bad); color: var(--bad); }}
      #lat-root .latticeCell{{
        position:relative; width:54px; height:54px; border:1px solid var(--ink); background:#fff;
        background-image: linear-gradient(135deg, transparent calc(50% - 1px), var(--line) calc(50% - 1px), var(--line) calc(50% + 1px), transparent calc(50% + 1px));
      }}
      #lat-root .latticeCell.active{{ background-color:#fdf6e3; }}
      #lat-root .latticeTens, #lat-root .latticeUnits{{ position:absolute; font-family:'Courier New', monospace; font-weight:700; font-size:15px; color: var(--good); }}
      #lat-root .latticeTens{{ top:3px; left:5px; }}
      #lat-root .latticeUnits{{ bottom:3px; right:5px; }}
      #lat-root .latticeTensInput, #lat-root .latticeUnitsInput{{ position:absolute; width:20px; height:18px; text-align:center; font-family:'Courier New', monospace; font-weight:700; font-size:13px; border:1px solid var(--line); border-radius:4px; padding:0; outline:none; background:#fff; color:var(--ink); }}
      #lat-root .latticeTensInput{{ top:2px; left:3px; }}
      #lat-root .latticeUnitsInput{{ bottom:2px; right:3px; }}
      #lat-root .latticeTensInput:focus, #lat-root .latticeUnitsInput:focus{{ border-color: var(--mark-deep); }}
      #lat-root .latticeBandHost{{ margin: 10px 0 16px; }}

      #lat-root .dccRow{{ display:flex; align-items:flex-end; gap:2px; }}
      #lat-root .carryCell{{ width:38px; flex:0 0 38px; font-family:'Courier New', monospace; font-size:16px; font-weight:700; text-align:center; height:22px; line-height:22px; color: var(--exchange); }}
      #lat-root .carryInputBox{{ width:24px; font-family:'Courier New', monospace; font-size:14px; font-weight:700; text-align:center; padding:1px 0; border:1.5px solid var(--line); border-radius:5px; background:#fff; color: var(--ink); outline:none; }}
      #lat-root .carryInputBox:focus{{ border-color: var(--mark-deep); }}
      #lat-root .subAnswerCell{{ width:38px; flex:0 0 38px; font-family:'Courier New', monospace; font-size:26px; font-weight:700; text-align:center; height:32px; line-height:32px; color: var(--good); }}
      #lat-root .subAnswerCell.placeholder{{ color: transparent; border-bottom: 3px dashed var(--line); }}
      #lat-root .subAnswerCell.active{{ background:#fdf6e3; border-radius:6px; color: var(--ink); border-bottom: 3px solid var(--mark-deep); }}

      @media (max-width:480px){{
        #lat-root .latticeCornerCell, #lat-root .latticeHeaderCell, #lat-root .latticeCell{{ width:42px; height:42px; }}
        #lat-root .latticeHeaderCell{{ font-size:18px; }}
        #lat-root .latticeHeaderCell input{{ width:26px; font-size:16px; }}
      }}
    </style>

    <div id="lat-root">
      <div class="stageLabel" id="lat-stageLabel"></div>
      <p class="prompt" id="lat-promptText"></p>
      <div id="lat-mainHost"></div>
    </div>

    <script>
    (function(){{
      const A_STR = {a_str!r};
      const B_STR = {b_str!r};

      function el(tag, cls, text){{
        var e = document.createElement(tag);
        if (cls) e.className = cls;
        if (text !== undefined && text !== null) e.textContent = text;
        return e;
      }}
      function finishBox(headline, lines){{
        var box = el('div', 'finishBox');
        box.appendChild(el('div', 'headline', headline));
        lines.forEach(function(l){{ var p = el('p'); p.innerHTML = l; box.appendChild(p); }});
        return box;
      }}

      var A_DIGITS = A_STR.split('').map(Number);
      var B_DIGITS = B_STR.split('').map(Number);
      var nA = A_DIGITS.length, nB = B_DIGITS.length;
      var cells = [];
      for (var r = 0; r < nB; r++){{
        var row = [];
        for (var c = 0; c < nA; c++){{
          var product = A_DIGITS[c] * B_DIGITS[r];
          row.push({{ top: A_DIGITS[c], side: B_DIGITS[r], product: product, tens: Math.floor(product / 10), units: product % 10, solved: false }});
        }}
        cells.push(row);
      }}
      var cellOrder = [];
      for (var r2 = 0; r2 < nB; r2++) for (var c2 = 0; c2 < nA; c2++) cellOrder.push([r2, c2]);
      var cellPos = 0;
      var bands = [], bandPos = 0;
      var stage = 'headers';

      function prepareBands(){{
        var maxBand = (nA - 1) + (nB - 1) + 1;
        var raw = [];
        for (var b = 0; b <= maxBand; b++) raw.push([]);
        for (var r3 = 0; r3 < nB; r3++){{
          for (var c3 = 0; c3 < nA; c3++){{
            var cell = cells[r3][c3];
            var unitsBand = (nB - 1 - r3) + (nA - 1 - c3);
            raw[unitsBand].push(cell.units);
            raw[unitsBand + 1].push(cell.tens);
          }}
        }}
        bands = raw.map(function(contributors, idx){{ return {{ index: idx, contributors: contributors, carryIn: 0, sum: 0, digit: 0, carryOut: 0 }}; }});
        var carry = 0;
        bands.forEach(function(band){{
          band.carryIn = carry;
          band.sum = band.contributors.reduce(function(s, v){{ return s + v; }}, 0) + carry;
          band.digit = band.sum % 10;
          band.carryOut = Math.floor(band.sum / 10);
          carry = band.carryOut;
        }});
        if (carry > 0){{
          bands.push({{ index: bands.length, contributors: [], carryIn: carry, sum: carry, digit: carry % 10, carryOut: Math.floor(carry / 10) }});
        }}
        bandPos = 0;
      }}

      function finalAnswerStr(){{
        return bands.slice().reverse().map(function(b){{ return b.digit; }}).join('').replace(/^0+(?=\\d)/, '');
      }}

      function buildGrid(opts){{
        opts = opts || {{}};
        var grid = el('div', 'latticeGrid');
        grid.style.gridTemplateColumns = 'repeat(' + (nA + 1) + ', 54px)';
        grid.style.gridTemplateRows = 'repeat(' + (nB + 1) + ', 54px)';
        grid.appendChild(el('div', 'latticeCornerCell'));

        for (var c = 0; c < nA; c++){{
          if (opts.headerInputs){{
            var hc = el('div', 'latticeHeaderCell');
            var hi = document.createElement('input');
            hi.type = 'text'; hi.inputMode = 'numeric'; hi.maxLength = 1; hi.autocomplete = 'off';
            hi.id = 'lat-headA' + c;
            hc.appendChild(hi);
            grid.appendChild(hc);
          }} else {{
            grid.appendChild(el('div', 'latticeHeaderCell solved', String(A_DIGITS[c])));
          }}
        }}

        for (var r4 = 0; r4 < nB; r4++){{
          if (opts.headerInputs){{
            var hc2 = el('div', 'latticeHeaderCell');
            var hi2 = document.createElement('input');
            hi2.type = 'text'; hi2.inputMode = 'numeric'; hi2.maxLength = 1; hi2.autocomplete = 'off';
            hi2.id = 'lat-headB' + r4;
            hc2.appendChild(hi2);
            grid.appendChild(hc2);
          }} else {{
            grid.appendChild(el('div', 'latticeHeaderCell solved', String(B_DIGITS[r4])));
          }}
          for (var c2 = 0; c2 < nA; c2++){{
            var cellData = cells[r4][c2];
            var isActive = opts.activeRC && opts.activeRC[0] === r4 && opts.activeRC[1] === c2;
            var cellDiv = el('div', 'latticeCell' + (isActive ? ' active' : ''));
            if (opts.headerInputs){{
              // blank placeholder \u2014 nothing filled in yet at this stage
            }} else if (cellData.solved){{
              cellDiv.appendChild(el('div', 'latticeTens', String(cellData.tens)));
              cellDiv.appendChild(el('div', 'latticeUnits', String(cellData.units)));
            }} else if (isActive){{
              var tensInp = document.createElement('input');
              tensInp.type = 'text'; tensInp.inputMode = 'numeric'; tensInp.maxLength = 1; tensInp.autocomplete = 'off';
              tensInp.className = 'latticeTensInput'; tensInp.id = 'lat-tensInput';
              var unitsInp = document.createElement('input');
              unitsInp.type = 'text'; unitsInp.inputMode = 'numeric'; unitsInp.maxLength = 1; unitsInp.autocomplete = 'off';
              unitsInp.className = 'latticeUnitsInput'; unitsInp.id = 'lat-unitsInput';
              cellDiv.appendChild(tensInp); cellDiv.appendChild(unitsInp);
            }}
            grid.appendChild(cellDiv);
          }}
        }}
        return grid;
      }}

      function render(){{
        var host = document.getElementById('lat-mainHost');
        var stageLbl = document.getElementById('lat-stageLabel');
        var promptEl = document.getElementById('lat-promptText');
        stageLbl.textContent =
          stage === 'headers' ? 'Step 1 of 3: fill in the grid' :
          stage === 'cells' ? 'Step 2 of 3: multiply cell by cell' :
          stage === 'diagonals' ? 'Step 3 of 3: add along the diagonals' : 'Finished';
        promptEl.textContent = '';
        host.innerHTML = '';
        if (stage === 'headers') renderHeaders(host);
        else if (stage === 'cells') renderCells(host);
        else if (stage === 'diagonals') renderDiagonals(host);
        else renderFinished(host);
      }}

      function renderHeaders(host){{
        host.appendChild(el('p', 'prompt',
          'Type each digit of ' + A_DIGITS.join('') + ' along the top, and each digit of ' + B_DIGITS.join('') + ' down the side.'));
        host.appendChild(buildGrid({{ headerInputs: true }}));

        var checkRow = el('div', 'checkRow');
        var checkBtn = el('button', 'btn', 'Check numbers');
        checkRow.appendChild(checkBtn);
        host.appendChild(checkRow);
        var fb = el('div', 'checkFeedback');
        host.appendChild(fb);

        checkBtn.onclick = function(){{
          var ok = true;
          for (var c = 0; c < nA; c++){{
            var inp = document.getElementById('lat-headA' + c);
            if (parseInt(inp.value, 10) === A_DIGITS[c]){{ inp.classList.remove('wrong'); inp.classList.add('correct'); inp.disabled = true; }}
            else {{ inp.classList.add('wrong'); ok = false; }}
          }}
          for (var r5 = 0; r5 < nB; r5++){{
            var inp2 = document.getElementById('lat-headB' + r5);
            if (parseInt(inp2.value, 10) === B_DIGITS[r5]){{ inp2.classList.remove('wrong'); inp2.classList.add('correct'); inp2.disabled = true; }}
            else {{ inp2.classList.add('wrong'); ok = false; }}
          }}
          if (ok){{
            fb.textContent = '\u2713 Correct! Now multiply cell by cell.'; fb.className = 'checkFeedback good';
            checkBtn.disabled = true;
            setTimeout(function(){{ stage = 'cells'; render(); }}, 500);
          }} else {{
            fb.textContent = '\u2717 Check the highlighted boxes and try again.'; fb.className = 'checkFeedback bad';
          }}
        }};
      }}

      function renderCells(host){{
        var act = cellPos < cellOrder.length ? cellOrder[cellPos] : null;
        if (!act){{
          host.appendChild(el('p', 'prompt', 'Every cell is filled in.'));
          setTimeout(function(){{ stage = 'diagonals'; prepareBands(); render(); }}, 600);
          return;
        }}
        var r6 = act[0], c6 = act[1];
        var cellData = cells[r6][c6];
        host.appendChild(el('p', 'prompt',
          'Multiply the top digit by the side digit: ' + cellData.top + ' \u00d7 ' + cellData.side + '. Write the tens digit above the line, the units digit below.'));
        host.appendChild(buildGrid({{ activeRC: act }}));

        var hintRow = el('div', 'answerRow');
        var hintBtn = el('button', 'btn secondary small', 'Show \u00d7' + cellData.side + ' table');
        hintRow.appendChild(hintBtn);
        host.appendChild(hintRow);
        var hintHost = el('div', 'timesTable');
        host.appendChild(hintHost);
        hintBtn.onclick = function(){{
          if (!hintHost.classList.contains('show')){{
            var lines = '<div class="ttHead">\u00d7' + cellData.side + ' table</div>';
            for (var i = 1; i <= 12; i++) lines += i + ' \u00d7 ' + cellData.side + ' = ' + (i * cellData.side) + '<br>';
            hintHost.innerHTML = lines;
            hintHost.classList.add('show');
            hintBtn.textContent = 'Hide table';
          }} else {{
            hintHost.classList.remove('show');
            hintBtn.textContent = 'Show \u00d7' + cellData.side + ' table';
          }}
        }};

        var checkRow = el('div', 'checkRow');
        var tensLabel = el('span', null, 'Tens:');
        var tensAns = document.createElement('input');
        tensAns.type = 'text'; tensAns.inputMode = 'numeric'; tensAns.maxLength = 1; tensAns.className = 'blankInput'; tensAns.id = 'lat-tensAnswer';
        var unitsLabel = el('span', null, 'Units:');
        var unitsAns = document.createElement('input');
        unitsAns.type = 'text'; unitsAns.inputMode = 'numeric'; unitsAns.maxLength = 1; unitsAns.className = 'blankInput'; unitsAns.id = 'lat-unitsAnswer';
        var checkBtn = el('button', 'btn', 'Check');
        checkRow.appendChild(tensLabel); checkRow.appendChild(tensAns);
        checkRow.appendChild(unitsLabel); checkRow.appendChild(unitsAns);
        checkRow.appendChild(checkBtn);
        host.appendChild(checkRow);
        var fb = el('div', 'checkFeedback');
        host.appendChild(fb);

        function doCheck(){{
          var tv = tensAns.value.trim() === '' ? 0 : parseInt(tensAns.value, 10);
          var uv = parseInt(unitsAns.value, 10);
          if (isNaN(uv)){{ fb.textContent = 'Type at least the units digit.'; fb.className = 'checkFeedback bad'; return; }}
          if (tv === cellData.tens && uv === cellData.units){{
            fb.textContent = '\u2713 Correct!'; fb.className = 'checkFeedback good';
            cellData.solved = true;
            cellPos++;
            tensAns.disabled = true; unitsAns.disabled = true; checkBtn.disabled = true;
            setTimeout(render, 350);
          }} else {{
            fb.textContent = '\u2717 Not quite \u2014 check ' + cellData.top + ' \u00d7 ' + cellData.side + ' and try again.'; fb.className = 'checkFeedback bad';
            tensAns.value = ''; unitsAns.value = ''; unitsAns.focus();
          }}
        }}
        checkBtn.onclick = doCheck;
        unitsAns.addEventListener('keydown', function(e){{ if (e.key === 'Enter') doCheck(); }});
        tensAns.addEventListener('keydown', function(e){{ if (e.key === 'Enter') doCheck(); }});
        setTimeout(function(){{ unitsAns.focus(); }}, 30);
      }}

      function renderBandStrip(bandHost){{
        bandHost.innerHTML = '';
        var n = bands.length;
        var carryRow = el('div', 'dccRow');
        var ansRow = el('div', 'dccRow');
        for (var i = n - 1; i >= 0; i--){{
          var band = bands[i];
          var solvedHere = i < bandPos;
          var isActive = i === bandPos;
          if (i === 0){{
            carryRow.appendChild(el('div', 'carryCell'));
          }} else if (solvedHere){{
            carryRow.appendChild(el('div', 'carryCell', band.carryIn ? '+' + band.carryIn : ''));
          }} else {{
            var wrap = el('div', 'carryCell');
            var inp = document.createElement('input');
            inp.type = 'text'; inp.inputMode = 'numeric'; inp.maxLength = 1; inp.autocomplete = 'off';
            inp.className = 'carryInputBox'; inp.id = 'lat-carryInput' + i;
            wrap.appendChild(inp);
            carryRow.appendChild(wrap);
          }}
          if (solvedHere) ansRow.appendChild(el('div', 'subAnswerCell', String(band.digit)));
          else if (isActive) ansRow.appendChild(el('div', 'subAnswerCell placeholder active', '?'));
          else ansRow.appendChild(el('div', 'subAnswerCell placeholder', ''));
        }}
        bandHost.appendChild(carryRow);
        bandHost.appendChild(ansRow);
        if (bandPos > 0){{
          bandHost.querySelectorAll('.carryInputBox').forEach(function(inp){{
            inp.addEventListener('input', function(){{ inp.value = inp.value.replace(/[^0-9]/g, '').slice(0, 1); }});
            inp.addEventListener('keydown', function(e){{ if (e.key === 'Enter'){{ var b = document.getElementById('lat-bandAnswerInput'); if (b) document.querySelector('#lat-mainHost .checkRow .btn').click(); }} }});
          }});
        }}
      }}

      function renderDiagonals(host){{
        host.appendChild(el('p', 'prompt', 'Every cell is multiplied out. Now add down each diagonal strip, starting from the right.'));
        host.appendChild(buildGrid({{}}));

        var n = bands.length;
        var act = bandPos < n ? bands[bandPos] : null;

        var bandHost = el('div', 'latticeBandHost');
        host.appendChild(bandHost);
        renderBandStrip(bandHost);

        if (!act){{
          setTimeout(function(){{ stage = 'finished'; render(); }}, 700);
          return;
        }}

        var exprParts = act.contributors.slice();
        var exprStr = exprParts.length ? exprParts.join(' + ') : '0';
        if (act.carryIn) exprStr += (exprParts.length ? ' + ' : '') + act.carryIn + ' carried in';
        host.appendChild(el('p', 'stagePrompt', 'Add this diagonal: ' + exprStr + '.'));
        if (bandPos < n - 1){{
          host.appendChild(el('div', 'quotHint', 'Type the digit below the line. If the total is 10 or more, write the carried ten in the small box above the next diagonal too \u2014 then check them together.'));
        }} else {{
          host.appendChild(el('div', 'quotHint', 'This is the last diagonal \u2014 just type the digit below the line.'));
        }}

        var checkRow = el('div', 'checkRow');
        var answerInput = document.createElement('input');
        answerInput.type = 'text'; answerInput.inputMode = 'numeric'; answerInput.className = 'blankInput'; answerInput.id = 'lat-bandAnswerInput'; answerInput.style.width = '60px';
        var checkBtn = el('button', 'btn', 'Check');
        checkRow.appendChild(answerInput); checkRow.appendChild(checkBtn);
        host.appendChild(checkRow);
        var fb = el('div', 'checkFeedback');
        host.appendChild(fb);

        function doCheck(){{
          var val = parseInt(answerInput.value, 10);
          if (isNaN(val)){{ fb.textContent = 'Type a number in the box first.'; fb.className = 'checkFeedback bad'; return; }}
          var isLast = bandPos === n - 1;
          var carryEl = isLast ? null : document.getElementById('lat-carryInput' + (bandPos + 1));
          var rawCarry = carryEl ? carryEl.value.trim() : '';
          var carryVal = rawCarry === '' ? 0 : parseInt(rawCarry, 10);
          var answerOk = val === act.digit;
          var carryOk = isLast ? true : (carryVal === act.carryOut);

          if (answerOk && carryOk){{
            fb.textContent = '\u2713 Correct!'; fb.className = 'checkFeedback good';
            bandPos++;
            answerInput.disabled = true; checkBtn.disabled = true;
            setTimeout(render, 350);
            return;
          }}
          var rawSum = exprParts.reduce(function(s, v){{ return s + v; }}, 0) + act.carryIn;
          if (!answerOk && act.carryOut === 1 && val === rawSum){{
            fb.textContent = "That's the full total for this diagonal. Write just the last digit here, and carry the other digit into the box above the next diagonal.";
          }} else if (!answerOk){{
            fb.textContent = '\u2717 Not quite \u2014 check the digit and try again.';
          }} else if (act.carryOut >= 1){{
            fb.textContent = "The digit is right, but this diagonal totals 10 or more \u2014 don't forget to carry.";
          }} else {{
            fb.textContent = "The digit is right, but check the carry box \u2014 this diagonal doesn't need one.";
          }}
          fb.className = 'checkFeedback bad';
          if (!answerOk){{ answerInput.value = ''; answerInput.focus(); }}
          if (!carryOk && carryEl){{ carryEl.value = ''; if (answerOk) carryEl.focus(); }}
        }}
        checkBtn.onclick = doCheck;
        answerInput.addEventListener('keydown', function(e){{ if (e.key === 'Enter') doCheck(); }});
        setTimeout(function(){{ answerInput.focus(); }}, 30);
      }}

      function renderFinished(host){{
        var aVal = A_DIGITS.join(''), bVal = B_DIGITS.join('');
        host.appendChild(buildGrid({{}}));
        var bandHost = el('div', 'latticeBandHost');
        host.appendChild(bandHost);
        renderBandStrip(bandHost);
        host.appendChild(finishBox('Finished!', [aVal + ' \u00d7 ' + bVal + ' = <span class="ans">' + finalAnswerStr() + '</span>']));
      }}

      render();
    }})();
    </script>
    """


def render_lattice_multiplication_widget(a, b, height=780):
    """Render the interactive lattice multiplication walkthrough for `a \u00d7 b`.

    a, b: whole numbers (int or numeric string, no decimal points). Walks the pupil through
    filling in the grid, multiplying cell by cell (with a per-cell times-table hint), then
    adding down each diagonal band with carrying — reveals the final product once every band
    is solved.
    """
    html_code = _build_html(str(a), str(b), height)
    components.html(html_code, height=height, scrolling=True)
