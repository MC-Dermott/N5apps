"""Interactive banded-rate earnings simulator (income tax / National Insurance style).

Generalises the fixed 3-band prototype (Downloads/tax_bands_widget.py) to any number of
contiguous rate bands, so the same widget can drive N5's randomised National Insurance
questions (2-3 bands) and Higher's real Scottish income tax bands (7 bands) and National
Insurance (2 bands) alike.

Usage:

    from core.ui.tax_bands_widget import render_tax_band_simulator

    render_tax_band_simulator(
        bands=[
            ("Personal Allowance", 0, 12_570, 0),
            ("Starter rate", 12_570, 15_397, 19),
            ("Basic rate", 15_397, 27_491, 20),
            ...
            ("Top rate", 125_140, None, 48),
        ],
        max_income=150_000,
        initial_income=30_000,
    )

`bands` is a list of `(label, lower, upper, rate_pct)` tuples, ascending and contiguous
(each band's `lower` equals the previous band's `upper`), starting at `lower = 0`. The final
band's `upper` may be `None` for an open-ended top band. `max_income` sets the slider's
maximum and the top of the visual bar (should be >= any question value that will be shown
against it, with headroom to explore).
"""
import json
import streamlit.components.v1 as components

_PALETTE = ["#888780", "#378ADD", "#E24B4A", "#F0A63A", "#5FAE55", "#9B6FD1", "#D65DB1", "#4FB8AF"]

_BAR_HEIGHT_PX = 400


def _range_label(lower, upper, currency):
    if lower == 0:
        return f"up to {currency}{upper:,.0f}"
    if upper is None:
        return f"above {currency}{lower:,.0f}"
    return f"{currency}{lower:,.0f} – {currency}{upper:,.0f}"


def _build_html(bands, max_income, initial_income, currency, height):
    if not bands:
        raise ValueError("bands must be non-empty")
    if bands[0][1] != 0:
        raise ValueError("first band must start at lower=0")
    for (_, lo, up, _r), (_, next_lo, _, _) in zip(bands, bands[1:]):
        if up != next_lo:
            raise ValueError(f"bands must be contiguous: band ending {up} does not meet next band starting {next_lo}")

    colors = _PALETTE[: len(bands)] if len(bands) <= len(_PALETTE) else _PALETTE * (len(bands) // len(_PALETTE) + 1)

    segments = []
    bottom = 0.0
    for i, (label, lower, upper, rate) in enumerate(bands):
        capped_upper = max_income if upper is None else min(upper, max_income)
        width = max(0.0, capped_upper - lower)
        seg_height = width / max_income * _BAR_HEIGHT_PX if max_income else 0
        segments.append({
            "label": label, "lower": lower, "upper": upper, "rate": rate,
            "color": colors[i], "bottom": bottom, "height": seg_height, "width": width,
        })
        bottom += seg_height

    if initial_income is None:
        mid_band = bands[min(1, len(bands) - 1)]
        initial_income = mid_band[1] + (mid_band[2] or max_income - mid_band[1]) / 2
    initial_income = min(initial_income, max_income)

    bar_divs = "\n".join(
        f'<div id="fillbg{i}" style="position:absolute;bottom:{s["bottom"]:.2f}px;left:0;width:100%;'
        f'height:{s["height"]:.2f}px;background:{s["color"]}22;"></div>'
        f'<div id="fill{i}" style="position:absolute;bottom:{s["bottom"]:.2f}px;left:0;width:100%;'
        f'height:0;background:{s["color"]};"></div>'
        + (f'<div style="position:absolute;left:0;right:0;bottom:{s["bottom"] + s["height"]:.2f}px;'
           f'border-top:2px dashed #222;"></div>' if i < len(segments) - 1 else "")
        for i, s in enumerate(segments)
    )

    legend_rows = "\n".join(
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">'
        f'<span style="width:10px;height:10px;border-radius:2px;background:{s["color"]};flex-shrink:0;"></span>'
        f'<div><p style="margin:0;font-size:14px;font-weight:600;color:#111;">{s["rate"]}%</p>'
        f'<p style="margin:0;font-size:12px;color:#666;">{_range_label(s["lower"], s["upper"], currency)}</p></div>'
        f'</div>'
        for s in reversed(segments)
    )

    bands_json = json.dumps([
        {"lower": s["lower"], "upper": s["upper"], "rate": s["rate"],
         "bottom": s["bottom"], "height": s["height"], "width": s["width"]}
        for s in segments
    ])

    return f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
      <div style="display:flex;gap:28px;align-items:flex-start;padding:0.5rem 0 0;">
        <div style="position:relative;width:90px;height:{_BAR_HEIGHT_PX}px;flex-shrink:0;border-radius:8px;border:1px solid #ddd;background:#f5f5f5;overflow:hidden;">
          {bar_divs}
        </div>
        <div style="display:flex;flex-direction:column;justify-content:flex-end;min-width:190px;">
          {legend_rows}
        </div>
      </div>

      <div style="margin:1.5rem 0 0;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem;">
          <label style="font-size:14px;color:#666;white-space:nowrap;">Income</label>
          <input type="range" id="earnings" min="0" max="{max_income}" step="{max(1, round(max_income / 200))}" value="{initial_income}" style="flex:1;">
          <span id="earnings-out" style="font-size:14px;font-weight:600;min-width:90px;text-align:right;color:#111;"></span>
        </div>

        <div style="display:grid;grid-template-columns:repeat(3, minmax(0,1fr));gap:12px;">
          <div style="background:#f5f5f5;border-radius:8px;padding:1rem;">
            <p style="margin:0 0 4px;font-size:13px;color:#666;">Amount charged</p>
            <p id="tax-out" style="margin:0;font-size:22px;font-weight:600;color:#111;"></p>
          </div>
          <div style="background:#f5f5f5;border-radius:8px;padding:1rem;">
            <p style="margin:0 0 4px;font-size:13px;color:#666;">Remaining</p>
            <p id="takehome-out" style="margin:0;font-size:22px;font-weight:600;color:#111;"></p>
          </div>
          <div style="background:#f5f5f5;border-radius:8px;padding:1rem;">
            <p style="margin:0 0 4px;font-size:13px;color:#666;">Effective rate</p>
            <p id="rate-out" style="margin:0;font-size:22px;font-weight:600;color:#111;"></p>
          </div>
        </div>
      </div>
    </div>

    <script>
      const BANDS = {bands_json};
      const MAX = {max_income};
      const CUR = {json.dumps(currency)};

      const earningsSlider = document.getElementById('earnings');
      const earningsOut = document.getElementById('earnings-out');
      const taxOut = document.getElementById('tax-out');
      const takehomeOut = document.getElementById('takehome-out');
      const rateOut = document.getElementById('rate-out');

      function money(n) {{
        return CUR + Math.round(n).toLocaleString('en-GB');
      }}

      function update() {{
        const earnings = Number(earningsSlider.value);
        let tax = 0;

        BANDS.forEach((b, i) => {{
          const upper = b.upper === null ? MAX : b.upper;
          const taxable = Math.max(0, Math.min(earnings, upper) - b.lower);
          const fillHeight = b.width > 0 ? (taxable / b.width) * b.height : 0;
          document.getElementById('fill' + i).style.height = fillHeight + 'px';
          tax += taxable * (b.rate / 100);
        }});

        const remaining = earnings - tax;
        const effRate = earnings > 0 ? (tax / earnings) * 100 : 0;

        earningsOut.textContent = money(earnings);
        taxOut.textContent = money(tax);
        takehomeOut.textContent = money(remaining);
        rateOut.textContent = effRate.toFixed(1) + '%';
      }}

      earningsSlider.addEventListener('input', update);
      update();
    </script>
    """


def render_tax_band_simulator(bands, max_income, initial_income=None, currency="£", height=620):
    """Render the interactive banded-rate earnings simulator in the current Streamlit app.

    See the module docstring for the `bands`/`max_income`/`initial_income` contract.
    """
    html_code = _build_html(bands, max_income, initial_income, currency, height)
    components.html(html_code, height=height, scrolling=False)
