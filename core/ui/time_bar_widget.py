"""Interactive guided time bar for time-interval questions.

Draws the time between a start and finish as a bar split at the next o'clock and the last
o'clock before the finish (the same diagram as the Speed, Distance and Time worksheet's
Section 4 examples), then walks the pupil through `core.models.time_bar.time_bar_steps()` one
step at a time — each correct answer uncovers that piece of the bar. The steps are the same
ones the question's own scaffold uses, so the two always agree.

Usage (via metadata {"diagram": "time_bar", "diagram_params": {...}}):

    render_time_bar_widget(start=455, end=740, mode="interval",
                           start_label="Leaves Oban", end_label="Arrives Castlebay")
    # ask_total=True hides the time to add/take away until the pupil works it out — for
    # questions where it comes from T = D ÷ S rather than being given.
    render_time_bar_widget(start=648, end=845, mode="forward")    # find the finish time
    render_time_bar_widget(start=705, end=850, mode="backward")   # find the start time

Times are minutes after midnight (`end` may pass 1440 for an overnight journey).
"""
import json

import streamlit.components.v1 as components

from core.models.time_bar import clock, hm, time_bar_segments, time_bar_steps, time_bar_ticks


def _build_html(start, end, mode="interval", start_label="", end_label="", ask_total=False,
                static=False):
    ticks = time_bar_ticks(start, end)
    segs = time_bar_segments(start, end)
    steps = time_bar_steps(start, end, mode)
    verb = "add on" if mode == "forward" else "take away"
    given = "" if mode == "interval" else f"Time to {verb}: <b>{hm(end - start)}</b>"
    if ask_total and mode != "interval":
        # The time to add comes from the question's own working (e.g. T = D ÷ S, plus any
        # delay) — make the pupil find it rather than giving it away.
        steps = [{"prompt": f"First work out the total time to {verb}, in hours and minutes.",
                  "answer": hm(end - start), "kind": "duration", "reveal_segs": [],
                  "reveal_ticks": [], "reveal_given": True}] + steps
    known = {"interval": list(range(len(ticks))), "forward": [0], "backward": [len(ticks) - 1]}[mode]
    data = {
        "ticks": [clock(t) for t in ticks],
        "segs": [{"label": hm(b - a).replace("minutes", "min").replace("minute", "min"),
                  "hours": kind == "hours"} for a, b, kind in segs],
        "steps": steps,
        "known": known,
        "backward": mode == "backward",
        "startLabel": start_label,
        "endLabel": end_label,
        "given": given,
        "hideGiven": bool(ask_total and mode != "interval"),
        "givenHidden": "" if mode == "interval" else f"Time to {verb}: <b>?</b>",
        # static: a fully labelled worked-example diagram (no steps), with the pieces added up
        # underneath and the time being found highlighted — matches the worksheet's diagrams.
        "static": static,
        "found": {"forward": len(ticks) - 1, "backward": 0}.get(mode, -1),
        "total": " + ".join(hm(b - a).replace("minutes", "min").replace("minute", "min") for a, b, _ in segs)
                 + f" = {hm(end - start)}",
    }
    payload = json.dumps(data)

    return """
    <style>
      #tb-root{ --ink:#22282f; --soft:#5b6470; --line:#d8d2c4; --min:#dcefed; --hr:#fbe9c6;
        --accent:#c25b2e; --good:#2f6f4a; --good-tint:#eaf3ec; --bad:#b3402b; --bad-tint:#fbeae6;
        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; color:var(--ink); }
      #tb-root *{ box-sizing:border-box; }
      #tb-root svg{ width:100%; height:auto; display:block; }
      #tb-root .given{ font-size:15px; margin:0 0 6px; }
      #tb-root .done{ font-size:14px; color:var(--soft); margin:2px 0; }
      #tb-root .done b{ color:var(--good); }
      #tb-root .prompt{ font-size:16px; font-weight:600; margin:14px 0 8px; }
      #tb-root .row{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
      #tb-root input{ font-size:16px; padding:7px 9px; border:1.5px solid var(--line); border-radius:7px; width:90px; }
      #tb-root input.wide{ width:110px; }
      #tb-root .unit{ font-size:14px; color:var(--soft); }
      #tb-root button{ font-size:14px; font-weight:600; padding:8px 16px; border-radius:7px; border:none;
        cursor:pointer; color:#fff; background:var(--ink); }
      #tb-root button.ghost{ background:#fff; color:var(--ink); border:1.5px solid var(--line); }
      #tb-root .fb{ font-size:14px; font-weight:600; margin-top:8px; min-height:18px; }
      #tb-root .fb.good{ color:var(--good); } #tb-root .fb.bad{ color:var(--bad); }
      #tb-root .finish{ margin-top:14px; padding:10px 12px; border-radius:8px; background:var(--good-tint);
        color:var(--good); font-weight:600; font-size:15px; }
    </style>
    <div id="tb-root">
      <div class="given" id="tb-given"></div>
      <div id="tb-svg"></div>
      <div id="tb-done"></div>
      <div id="tb-step"></div>
    </div>
    <script>
    (function(){
      const D = """ + payload + """;
      const revealedSegs = new Set(), revealedTicks = new Set(D.known);
      let cur = 0;
      const givenEl = document.getElementById('tb-given');
      givenEl.innerHTML = D.hideGiven ? D.givenHidden : D.given;

      const W = 680, padL = 60, padR = 60, barY = 78, barH = 40;
      const weights = D.segs.map(s => s.hours ? 2.3 : 1.35);
      const wsum = weights.reduce((a, b) => a + b, 0);
      const xs = [padL];
      weights.forEach(w => xs.push(xs[xs.length - 1] + w / wsum * (W - padL - padR)));

      function stepNumbers(){
        // Order in which the pieces are counted: left to right, or right to left going backwards.
        const n = D.segs.length, order = [];
        for (let i = 0; i < n; i++) order.push(D.backward ? n - i : i + 1);
        return order;
      }

      function draw(){
        const nums = stepNumbers();
        let s = `<svg viewBox="0 0 ${W} 190" xmlns="http://www.w3.org/2000/svg">`;
        D.segs.forEach((seg, i) => {
          const x0 = xs[i], x1 = xs[i + 1], cx = (x0 + x1) / 2;
          const shown = revealedSegs.has(i);
          s += `<rect x="${x0}" y="${barY}" width="${x1 - x0}" height="${barH}" fill="${seg.hours ? 'var(--hr)' : 'var(--min)'}" stroke="var(--ink)" stroke-width="2"/>`;
          s += `<text x="${cx}" y="${barY + barH / 2 + 6}" text-anchor="middle" font-size="17" font-weight="700" fill="${shown ? 'var(--ink)' : '#9aa0a8'}">${shown ? seg.label : '?'}</text>`;
          const ay = barY - 20, a0 = D.backward ? x1 - 12 : x0 + 12, a1 = D.backward ? x0 + 12 : x1 - 12;
          const dir = D.backward ? -1 : 1;
          s += `<line x1="${a0}" y1="${ay}" x2="${a1 - dir * 8}" y2="${ay}" stroke="var(--accent)" stroke-width="2"/>`;
          s += `<polygon points="${a1},${ay} ${a1 - dir * 10},${ay - 5} ${a1 - dir * 10},${ay + 5}" fill="var(--accent)"/>`;
          s += `<text x="${cx}" y="${ay - 10}" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent)">Step ${nums[i]}</text>`;
        });
        D.ticks.forEach((t, j) => {
          const x = xs[j], shown = revealedTicks.has(j);
          s += `<line x1="${x}" y1="${barY - 6}" x2="${x}" y2="${barY + barH + 8}" stroke="var(--ink)" stroke-width="2"/>`;
          if (D.static && j === D.found) s += `<rect x="${x - 34}" y="${barY + barH + 11}" width="68" height="26" rx="6" fill="#fff" stroke="var(--accent)" stroke-width="2"/>`;
          s += `<text x="${x}" y="${barY + barH + 30}" text-anchor="middle" font-size="18" font-weight="700" fill="${D.static && j === D.found ? 'var(--accent)' : shown ? 'var(--ink)' : '#9aa0a8'}">${shown ? t : '?'}</text>`;
        });
        if (D.startLabel) s += `<text x="${xs[0]}" y="${barY + barH + 52}" text-anchor="middle" font-size="13" font-style="italic" fill="var(--soft)">${D.startLabel}</text>`;
        if (D.endLabel) s += `<text x="${xs[xs.length - 1]}" y="${barY + barH + 52}" text-anchor="middle" font-size="13" font-style="italic" fill="var(--soft)">${D.endLabel}</text>`;
        s += `</svg>`;
        document.getElementById('tb-svg').innerHTML = s;
      }

      function toMinutes(str){
        const m = String(str).match(/(\\d+)\\s*hours?/), n = String(str).match(/(\\d+)\\s*minutes?/);
        return (m ? +m[1] * 60 : 0) + (n ? +n[1] : 0);
      }
      function normClock(v){
        const d = String(v).replace(/\\D/g, '');
        return (d.length === 3 || d.length === 4) ? d.padStart(4, '0') : null;
      }
      function check(step){
        if (step.kind === 'duration'){
          const h = +document.getElementById('tb-h').value || 0, m = +document.getElementById('tb-m').value || 0;
          return h * 60 + m === toMinutes(step.answer);
        }
        const v = document.getElementById('tb-in').value.trim();
        if (step.kind === 'clock') return normClock(v) === step.answer.replace(':', '');
        return v !== '' && Number(v) === Number(step.answer);
      }
      function shownAnswer(step){
        if (step.kind === 'minutes') return step.answer + ' min';
        if (step.kind === 'hours') return step.answer + ' hour' + (step.answer == 1 ? '' : 's');
        return step.answer;
      }

      function complete(){
        const step = D.steps[cur];
        step.reveal_segs.forEach(i => revealedSegs.add(i));
        step.reveal_ticks.forEach(i => revealedTicks.add(i));
        if (step.reveal_given) givenEl.innerHTML = D.given;
        const p = document.createElement('div');
        p.className = 'done';
        p.innerHTML = `✓ ${step.prompt} <b>${shownAnswer(step)}</b>`;
        document.getElementById('tb-done').appendChild(p);
        cur++;
        draw(); renderStep();
      }

      function renderStep(){
        const host = document.getElementById('tb-step');
        if (cur >= D.steps.length){
          D.segs.forEach((_, i) => revealedSegs.add(i));
          D.ticks.forEach((_, j) => revealedTicks.add(j));
          draw();
          const last = D.steps[D.steps.length - 1];
          host.innerHTML = `<div class="finish">Done — ${shownAnswer(last)}</div>`;
          return;
        }
        const step = D.steps[cur];
        let inputs;
        if (step.kind === 'duration'){
          inputs = `<input id="tb-h" type="number" min="0"><span class="unit">hours</span>
                    <input id="tb-m" type="number" min="0" max="59"><span class="unit">minutes</span>`;
        } else if (step.kind === 'clock'){
          inputs = `<input id="tb-in" class="wide" placeholder="hh:mm">`;
        } else {
          inputs = `<input id="tb-in" type="number" min="0"><span class="unit">${step.kind === 'hours' ? 'hours' : 'minutes'}</span>`;
        }
        host.innerHTML = `<div class="prompt">Step ${cur + 1}: ${step.prompt}</div>
          <div class="row">${inputs}<button id="tb-check">Check</button>
          <button id="tb-show" class="ghost" style="display:none">Show me</button></div>
          <div class="fb" id="tb-fb"></div>`;
        const fb = document.getElementById('tb-fb');
        document.getElementById('tb-check').onclick = () => {
          if (check(step)){ complete(); }
          else {
            fb.className = 'fb bad';
            fb.textContent = 'Not quite — look at the time bar and try again.';
            document.getElementById('tb-show').style.display = '';
          }
        };
        document.getElementById('tb-show').onclick = complete;
        host.querySelectorAll('input').forEach(el => el.addEventListener('keydown', e => {
          if (e.key === 'Enter') document.getElementById('tb-check').click();
        }));
      }

      if (D.static){
        D.segs.forEach((_, i) => revealedSegs.add(i));
        D.ticks.forEach((_, j) => revealedTicks.add(j));
        givenEl.innerHTML = '';
        draw();
        document.getElementById('tb-step').innerHTML =
          `<div style="text-align:center;margin-top:4px"><span style="display:inline-block;padding:6px 14px;border-radius:8px;background:#f4f1ea;border:1px solid var(--line);font-weight:700;font-size:15px">${D.total}</span></div>`;
      } else {
        draw(); renderStep();
      }
    })();
    </script>
    """


def render_time_bar_widget(start, end, mode="interval", start_label="", end_label="", ask_total=False,
                           height=None):
    steps = len(time_bar_steps(start, end, mode)) + (1 if ask_total else 0)
    components.html(_build_html(start, end, mode, start_label, end_label, ask_total),
                    height=height or 330 + 26 * steps, scrolling=False)


def render_time_bar_diagram(start, end, mode="interval", start_label="", end_label=""):
    """Static, fully labelled time bar for a worked example (see core/ui/notes_ui.py)."""
    components.html(_build_html(start, end, mode, start_label, end_label, static=True),
                    height=240, scrolling=False)
