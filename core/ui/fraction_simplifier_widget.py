"""Interactive step-by-step fraction simplifier widget.

N3apps has no single dedicated "simplify a fraction" tool to port — the closest pieces are the
generic two-step check-input flow used throughout
`/Users/luke/Library/CloudStorage/OneDrive-GlowScotland/Resources/Maths/scaffolds/numeracy_scaffolds.html`
(e.g. its probability tool's `buildStepFlowText`, which checks a pupil-typed fraction against a
raw/simplified pair) and the stacked `.fracDisplay` fraction shown above it. This widget
combines those two established patterns into a dedicated tool: show the fraction, ask for the
highest common factor of its numerator and denominator, then ask for the fraction divided
through by that HCF — matching the same visual language (fonts, pill/blank-input styling,
finish box) as the other ported widgets in this package.

Usage:

    from core.ui.fraction_simplifier_widget import render_fraction_simplifier_widget

    render_fraction_simplifier_widget(numerator=18, denominator=24)
"""
from math import gcd

import streamlit.components.v1 as components


def _build_html(numerator, denominator, height):
    if numerator <= 0 or denominator <= 0:
        raise ValueError("numerator and denominator must be positive")
    hcf = gcd(numerator, denominator)
    simplified_num = numerator // hcf
    simplified_den = denominator // hcf

    return f"""
    <style>
      #fsw-root{{
        --ink: #22282f; --ink-soft: #5b6470; --line: #d8d2c4;
        --mark-deep: #a97a13; --good: #2f6f4a; --good-tint: #eaf3ec;
        --bad: #b3402b; --bad-tint: #fbeae6;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--ink);
      }}
      #fsw-root *{{ box-sizing: border-box; }}
      #fsw-root .stageLabel{{ font-size: 12.5px; font-weight:600; letter-spacing:.02em; color: var(--mark-deep); margin-bottom: 6px; }}
      #fsw-root .prompt{{ font-size: 18px; font-weight:600; margin: 0 0 16px; line-height:1.4; }}
      #fsw-root .fracDisplay{{ font-family:'Courier New', monospace; font-weight:700; font-size:30px; text-align:center; margin: 10px 0 22px; line-height:1.15; }}
      #fsw-root .fracDisplay .fline{{ display:inline-block; border-bottom:3px solid var(--ink); padding: 0 10px 4px; }}
      #fsw-root .fracDisplay .fnum, #fsw-root .fracDisplay .fden{{ display:block; }}
      #fsw-root .checkRow{{ display:flex; align-items:center; gap: 12px; margin-bottom: 6px; flex-wrap:wrap; }}
      #fsw-root .blankInput{{ font-family:'Courier New', monospace; font-size: 19px; font-weight:600; width: 120px; text-align:center; padding: 7px 8px; border: 1.5px solid var(--line); border-radius:7px; background: #fff; color: var(--ink); outline: none; margin: 0 2px; }}
      #fsw-root .blankInput:focus{{ border-color: var(--mark-deep); }}
      #fsw-root .checkFeedback{{ font-size: 13.5px; font-weight:600; margin: 2px 0 14px; min-height: 18px; }}
      #fsw-root .checkFeedback.good{{ color: var(--good); }}
      #fsw-root .checkFeedback.bad{{ color: var(--bad); }}
      #fsw-root .btn{{ font-size: 14px; font-weight:600; padding: 10px 18px; border-radius: 8px; border: none; cursor: pointer; color: #fff; background: var(--ink); transition: opacity .12s; }}
      #fsw-root .btn:hover{{ opacity:.9; }}
      #fsw-root .finishBox{{ background: var(--good-tint); border: 1.5px solid var(--good); border-radius: 8px; padding: 14px 16px; margin: 10px 0 4px; }}
      #fsw-root .finishBox .headline{{ font-weight:700; font-size:17px; color: var(--good); margin-bottom:6px; }}
      #fsw-root .finishBox p{{ margin: 2px 0; font-size: 14px; color: var(--ink); line-height:1.5; }}
      #fsw-root .finishBox .ans{{ font-family:'Courier New', monospace; font-weight:700; }}
    </style>

    <div id="fsw-root">
      <div class="stageLabel" id="fsw-stageLabel"></div>
      <p class="prompt" id="fsw-promptText"></p>
      <div class="fracDisplay"><span class="fline"><span class="fnum">{numerator}</span><span class="fden">{denominator}</span></span></div>
      <div id="fsw-stepHost"></div>
      <div id="fsw-finishHost"></div>
    </div>

    <script>
    (function(){{
      const NUM = {numerator};
      const DEN = {denominator};
      const HCF = {hcf};
      const SIMP_NUM = {simplified_num};
      const SIMP_DEN = {simplified_den};

      const steps = [
        {{ prompt: 'What is the highest common factor (HCF) of ' + NUM + ' and ' + DEN + '?', answer: HCF }},
        {{ prompt: 'Divide the numerator and denominator by the HCF. What is ' + NUM + '/' + DEN + ' in its simplest form?', answer: SIMP_NUM + '/' + SIMP_DEN }}
      ];
      let idx = 0;

      function parseAnswer(raw, expected){{
        var v = String(raw).trim().replace(/\\s/g, '');
        if (typeof expected === 'number'){{ return Number(v) === expected; }}
        return v === expected;
      }}

      function renderStep(){{
        const stageLbl = document.getElementById('fsw-stageLabel');
        const host = document.getElementById('fsw-stepHost');
        const finishHost = document.getElementById('fsw-finishHost');
        finishHost.innerHTML = '';
        host.innerHTML = '';

        if (idx >= steps.length){{
          stageLbl.textContent = 'Finished';
          finishHost.innerHTML = '<div class="finishBox"><div class="headline">Simplified!</div>' +
            '<p>' + NUM + '/' + DEN + ' = <span class="ans">' + SIMP_NUM + '/' + SIMP_DEN + '</span></p></div>';
          return;
        }}

        stageLbl.textContent = 'Step ' + (idx + 1) + ' of ' + steps.length;
        const s = steps[idx];
        const row = document.createElement('div');
        row.className = 'checkRow';
        const inp = document.createElement('input');
        inp.className = 'blankInput'; inp.type = 'text';
        inp.placeholder = typeof s.answer === 'number' ? 'e.g. 2' : 'e.g. 3/4';
        const btn = document.createElement('button');
        btn.className = 'btn'; btn.textContent = 'Check';
        row.appendChild(inp); row.appendChild(btn);
        const fb = document.createElement('div');
        fb.className = 'checkFeedback';
        host.appendChild(document.createElement('p')).outerHTML = '<p class="prompt" style="font-size:16px;margin-bottom:10px;">' + s.prompt + '</p>';
        host.appendChild(row);
        host.appendChild(fb);

        function doCheck(){{
          if (parseAnswer(inp.value, s.answer)){{
            fb.textContent = '✓ Correct!'; fb.className = 'checkFeedback good';
            inp.disabled = true; btn.disabled = true;
            idx++;
            setTimeout(renderStep, 400);
          }} else {{
            fb.textContent = '✗ Not quite — try again.'; fb.className = 'checkFeedback bad';
          }}
        }}
        btn.onclick = doCheck;
        inp.addEventListener('keydown', function(e){{ if (e.key === 'Enter'){{ e.preventDefault(); doCheck(); }} }});
        setTimeout(function(){{ inp.focus(); }}, 30);
      }}

      renderStep();
    }})();
    </script>
    """


def render_fraction_simplifier_widget(numerator, denominator, height=380):
    """Render the interactive fraction-simplifying walkthrough for `numerator/denominator`:
    find the HCF of the two numbers, then divide both through by it to reach simplest form.
    """
    html_code = _build_html(numerator, denominator, height)
    components.html(html_code, height=height, scrolling=True)
