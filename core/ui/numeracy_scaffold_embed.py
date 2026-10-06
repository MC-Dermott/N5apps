"""Interactive scaffolds ported from N3apps' `numeracy_scaffolds.html` (a single self-contained
page with several independent tools switched between by a JS `showApp('<id>-app')` call).

Each render function embeds that page, jumps to one tool, switches it to its "My own numbers"
mode and fills in the question's own numbers — so the scaffold walks through exactly the sum the
question shows, not an unrelated demo. Dispatched from `core/ui/scaffold_ui.py`'s
`render_simulation()` on `metadata["diagram"]`.
"""
import json
from pathlib import Path

import streamlit.components.v1 as components

_ASSET = Path(__file__).parent / "assets" / "numeracy_scaffolds.html"
_html_cache = {}


def _json(value):
    return json.dumps(value).replace("</", "<\\/")


def _embed(app_id, setup_js, height):
    if "html" not in _html_cache:
        _html_cache["html"] = _ASSET.read_text(encoding="utf-8")
    script = f"""
        <script>
        (function() {{
            showApp('{app_id}');
            {setup_js}
        }})();
        </script>
    </body>"""
    components.html(_html_cache["html"].replace("</body>", script), height=height, scrolling=True)


def _click_matching(container_id, data_attr, value):
    return (f"document.querySelectorAll('#{container_id} .pill').forEach(function(b) "
            f"{{ if (b.dataset.{data_attr} === '{value}') {{ b.click(); }} }});\n")


def _set_value(elem_id, value):
    return f"document.getElementById('{elem_id}').value = {_json(str(value))};\n"


def render_decimal_column_widget(a, b, op):
    """a, b: the numbers as formatted in the question (strings, e.g. '27.58'); op: '+' or '-'."""
    setup = (_click_matching("dcc-modePills", "mode", "custom")
             + _set_value("dcc-aInput", a) + _set_value("dcc-bInput", b)
             + _click_matching("dcc-opPills", "op", op)
             + "document.getElementById('dcc-startBtn').click();")
    _embed("dcc-app", setup, 760)


def render_decimal_mul_div_widget(value, operation, kind, n):
    """operation: 'multiply'/'divide'; kind: 'single_digit' (ignore-the-point method) or
    'shift' (point moves for x/÷ 10/100/1000); n: the digit, or the power of ten."""
    setup = (_click_matching("dms-modePills", "mode", "custom")
             + _click_matching("dms-kindPills", "kind", kind)
             + _set_value("dms-valueInput", value)
             + _click_matching("dms-opPills", "op", operation))
    if kind == "single_digit":
        setup += _set_value("dms-nDigitInput", n)
    else:
        setup += _click_matching("dms-nPowerPills", "n", str(n))
    setup += "document.getElementById('dms-startBtn').click();"
    _embed("dms-app", setup, 680)


def render_scale_stepper_widget(min_value, max_value, major_step, minor_step, marker_value, unit_label=""):
    """Step-by-step reading of a graduated scale: value of one small gap, then the marker's reading."""
    setup = (_click_matching("ss-modePills", "mode", "custom")
             + _set_value("ss-minInput", min_value) + _set_value("ss-maxInput", max_value)
             + _set_value("ss-majorInput", major_step) + _set_value("ss-minorInput", minor_step)
             + _set_value("ss-markerInput", marker_value) + _set_value("ss-unitInput", unit_label)
             + "document.getElementById('ss-startBtn').click();")
    _embed("ss-app", setup, 520)
