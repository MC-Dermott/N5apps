"""Higher Applications of Maths — Mathematical Modelling.

Mirrors Mathematical_Modelling_Worksheet.docx (Higher Apps/Worksheets/Modelling): rates and variables,
linear / exponential / quadratic models, recurrence relation models in a spreadsheet, graphs that
model a situation (container depth), errors and tolerance, and estimation. Listed the house way for a
topic with spreadsheet questions: one "Calculator Questions" level drawing from _CALCULATOR_MIX
(weighted by past-paper marks, 2022–2026), plus "Spreadsheet: Recurrence Relation Model" (2023 Q8,
2024 Q4) and "Spreadsheet: Profit Function" (2026 Q5).

Distractors are the errors in the course reports and marking instructions: a rate not per one unit,
max ÷ max for a compound measure, the height's error instead of the volume's, a linear projection
for an exponential claim, the long-term level misread, the graph explained in terms of volume.
"""
import io
import math
import random

from openpyxl import Workbook
from openpyxl.chart import Reference, ScatterChart, Series
from openpyxl.styles import Alignment, Font, PatternFill

from core.engine.spreadsheet_solution import solution_metadata, workbook_bytes
from core.models.distractors import distractors
from core.models.question_model import Question

TOPIC, QTYPE = "Modelling", "Mathematical Modelling"
_DIAG = "topics.modelling.modelling_diagrams"


def _g(x, dp=2):
    x = round(x + 0.0, dp)
    s = f"{x:,.{dp}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def _r(x, dp=2):
    return round(x + 1e-9, dp)


def _diagram(kind, *args, width=420):
    return {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DIAG, "kind": kind, "args": list(args), "width": width}}


NOTES = """
**Mathematical modelling** (Higher Apps — worksheet examples)

- **Rate of change** = amount per ONE unit, with units. A 330 ml can filled in 3 s → 330 ÷ 3 =
  **110 ml per second** ("330 ml every 3 seconds" scored 0 in 2024).
- **Variables:** the independent variable is a quantity (time, load m) — not a unit or a number.
- **Types of model:** linear = constant rate of change; exponential = constant percentage change
  (equal ratios); quadratic = x² term, a maximum or minimum. Seals 1200, 1320, 1452 → ratio 1.1 →
  exponential, N = 1200 × 1.1ᵗ.
- **Recurrence relation:** next = (1 − rate) × current + amount; levels out at amount ÷ rate.
  Fish farm: 2400 fish, 15% harvested, 300 added each week → limit 300 ÷ 0.15 = **2000**.
- **Depth graphs:** narrow part → depth rises quickly; wide part → slowly. Explain the DEPTH.
- **Errors:** relative error of one length carries to the volume: 5 × 6 × 8 = 240 cm³, 2.5% → 6 cm³.
  Maximum speed = maximum distance ÷ MINIMUM time: 120.5 ÷ 1.45 = **83.10 km/h**.

⚠ 2023: "continuous" or "numerical" isn't a type of model. 2022: test an exponential claim by
calculating. 2024: compare a long-term level with the figure given (800 ppm).
"""


# ── calculator questions ─────────────────────────────────────────────────────────────────────
def _q_rate():
    what, amount, unit, tunit, t = random.choice([
        ("can of juice", random.choice([330, 440, 500]), "millilitres", "second", random.choice([2, 2.5, 4])),
        ("water butt", random.choice([180, 200, 240]), "litres", "minute", random.choice([8, 10, 12, 16])),
        ("kettle (temperature rise)", random.choice([60, 75, 80]), "°C", "second", random.choice([120, 150, 160]))])
    rate = _r(amount / t)
    tu = tunit + "s"
    text = (f"A {what} model: the graph is a straight line from 0 to {amount} {unit} in {_g(t)} {tu}. "
            f"Determine the rate of change, in {unit} per {tunit}.")
    return Question(
        question_text=text, correct_answer=rate, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": f"Total change ({unit})", "answer": float(amount)},
                        {"prompt": f"Rate = change ÷ time ({unit} per {tunit})", "answer": rate}],
        worked_solution=[f"Rate = {amount} ÷ {_g(t)} = **{_g(rate)} {unit} per {tunit}**",
                         "Give the amount per ONE unit, with units (2024 Q10(b))."],
        notes=NOTES, metadata=_diagram("rate_graph", t, amount, f"time ({tu})", unit),
        distractors=distractors(rate, [(_r(t / amount, 4), "you divided the wrong way: amount ÷ time."),
                                       (float(amount), f"that's the total, not the rate per {tunit} (2024 marking "
                                                       f"instructions: '330 ml every 3 seconds' scores 0).")]))


def _q_model_type():
    kind = random.choice(["linear", "exponential", "quadratic"])
    if kind == "linear":
        a, d = random.randint(2, 20), random.randint(2, 9)
        vals = [a + d * k for k in range(5)]
    elif kind == "exponential":
        a, f = random.choice([200, 500, 800, 1000]), random.choice([1.1, 1.2, 0.8, 0.9, 1.5])
        vals = [_g(a * f ** k) for k in range(5)]
    else:
        b, c = random.choice([10, 12, 14]), random.choice([1, 2])
        vals = [b * k - c * k * k for k in range(5)]
    right = {"linear": "Linear — the values change by the same amount each time (a constant rate of change)",
             "exponential": "Exponential — each value is the previous one multiplied by the same number",
             "quadratic": "Quadratic — the differences change by the same amount each time"}[kind]
    opts = [right] + [v for k, v in {"linear": "Linear — the values change by the same amount each time (a constant rate of change)",
                                     "exponential": "Exponential — each value is the previous one multiplied by the same number",
                                     "quadratic": "Quadratic — the differences change by the same amount each time"}.items()
                      if k != kind] + ["Continuous — the values follow on from each other"]
    random.shuffle(opts)
    return Question(
        question_text=f"x: 0, 1, 2, 3, 4\n\ny: {', '.join(map(str, vals))}\n\nWhich type of model fits the data?",
        correct_answer=right, topic=TOPIC, question_type=QTYPE, worked_solution=[right], notes=NOTES,
        metadata={"options": opts},
        distractors=[{"value": "Continuous — the values follow on from each other",
                      "mistake": "'continuous' isn't a type of model — name it: linear, exponential or quadratic "
                                 "(2023 course report)."}])


def _q_claim():
    a = random.choice([480, 680, 820, 1200]); f = random.choice([1.15, 1.2, 1.27, 1.35])
    b = round(a * f); gap = random.choice([6, 8, 9, 12]); y0 = random.choice([2006, 2008, 2010, 2012])
    pred = _r(b * b / a)
    lin = b + (b - a)
    text = (f"A population was {a} in {y0} and {b} in {y0 + gap}. If it keeps growing exponentially, predict the "
            f"population in {y0 + 2 * gap}, to the nearest whole number.")
    ans = float(round(pred))
    return Question(
        question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": f"Multiplying factor over {gap} years ({b} ÷ {a}), to 4 d.p.", "answer": _r(b / a, 4)},
                        {"prompt": "Predicted population", "answer": ans}],
        worked_solution=[f"Factor = {b} ÷ {a} = {_g(b / a, 4)} every {gap} years",
                         f"{b} × {b} ÷ {a} = {_g(pred, 1)} → **{int(ans)}**",
                         "To test a claim, calculate — in 2022 most just gave an opinion (course report)."],
        notes=NOTES,
        distractors=distractors(ans, [(float(lin), "that's a LINEAR projection (the same increase again) — an "
                                                   "exponential model multiplies by the same factor."),
                                      (float(round(b * (b / a) ** 2)), "the factor applies once for the next "
                                                                       f"{gap} years, not twice.")]))


def _q_profit():
    s, c = random.choice([(9, 3), (12, 4), (10, 2), (15, 5)])
    k = random.choice([0.01, 0.015, 0.02, 0.025])
    best = (s - c) / (2 * k)
    if best != int(best):
        k = 0.02; best = (s - c) / (2 * k)
    pmax = _r((s - c) * best - k * best * best)
    text = (f"Profit = (s − c)x − {k}x², with s = £{s} (selling price), c = £{c} (cost per item), x items made and sold. "
            f"The maximum profit is when x = {int(best)}. Calculate the maximum profit.")
    return Question(
        question_text=text, correct_answer=pmax, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": f"(s − c) × {int(best)}", "answer": float((s - c) * best)},
                        {"prompt": f"{k} × {int(best)}²", "answer": _r(k * best * best)},
                        {"prompt": "Maximum profit (£)", "answer": pmax}],
        worked_solution=[f"({s} − {c}) × {int(best)} − {k} × {int(best)}² = {_g((s - c) * best)} − {_g(k * best * best)} "
                         f"= **£{pmax:,.2f}**", "This is a quadratic model: the profit rises to a maximum, then falls "
                                                "(a loss beyond twice this number)."],
        notes=NOTES,
        distractors=distractors(pmax, [(_r((s - c) * best - k ** 2), f"you squared {k} instead of x — the 2026 marking "
                                                                     f"instructions' Candidate A typed −0.015^2."),
                                       (_r((s - c) * best), "you left out the − kx² term.")]))


def _q_recurrence_limit():
    start, pct, add, what = random.choice([(2000, 12, 150, "ppm of CO2"), (2400, 15, 300, "fish"),
                                           (200, 30, 80, "mg of medicine"), (5, 40, 1.5, "tonnes of pollutant"),
                                           (2.5, 20, 0.4, "mg per litre of chlorine")])
    L = _r(add / (pct / 100))
    text = (f"A model starts at {_g(start)} {what}. Each step {pct}% is removed and then {_g(add)} is added. Calculate the "
            f"long-term level the model settles at.")
    k = 1 - pct / 100
    u1 = _r(k * start + add)
    return Question(
        question_text=text, correct_answer=L, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "Value after the first step: (1 − rate) × start + amount", "answer": u1},
                        {"prompt": "Long-term level: amount ÷ rate", "answer": L}],
        worked_solution=[f"next = {_g(k)} × current + {_g(add)}", f"Step 1: {_g(k)} × {_g(start)} + {_g(add)} = {_g(u1)}",
                         f"Levels out at {_g(add)} ÷ {_g(pct / 100)} = **{_g(L)}**",
                         "Compare a long-term level with any figure you're given (2024 course report)."],
        notes=NOTES,
        distractors=distractors(L, [(u1, "that's the value after one step, not the long-term level."),
                                    (_r(add / k), f"divide by the rate removed ({_g(pct / 100)}), not the rate "
                                                  f"remaining ({_g(k)})."),
                                    (_r(start * k), "the amount added each step matters too.")]))


def _q_error():
    a, b = random.choice([(5, 6), (3, 4), (40, 30), (50, 40)]); h = random.choice([7, 8, 10, 25, 30])
    pc = random.choice([2, 2.5, 4, 5])
    V = a * b * h; ans = _r(V * pc / 100)
    text = (f"A mould has a base exactly {a} cm by {b} cm. It is filled to a height of {h} cm with a relative error of "
            f"{_g(pc)}%. Calculate the absolute error of the volume, in cm³.")
    return Question(
        question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "Volume (cm³)", "answer": float(V)}, {"prompt": f"{_g(pc)}% of the volume", "answer": ans}],
        worked_solution=[f"V = {a} × {b} × {h} = {V} cm³", f"Absolute error = {_g(pc)}% of {V} = **{_g(ans)} cm³**"],
        notes=NOTES,
        distractors=distractors(ans, [(_r(h * pc / 100), f"that's the HEIGHT's absolute error, not the volume's (2026 "
                                                         f"marking instructions: 2% of 7)."),
                                      (float(V), "that's the volume — the question asks for its absolute error.")]))


def _q_limits():
    d = random.choice([60, 84, 120, 150]); t = random.choice([0.8, 1.2, 1.5, 2.5])
    vmax = _r((d + 0.5) / (t - 0.05))
    text = (f"A journey is {d} km, to the nearest km, and takes {_g(t)} hours, to the nearest 0.1 hour. Calculate the "
            f"maximum possible average speed, in km/h.")
    return Question(
        question_text=text, correct_answer=vmax, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "Maximum distance (km)", "answer": d + 0.5},
                        {"prompt": "Minimum time (hours)", "answer": _r(t - 0.05)},
                        {"prompt": "Maximum speed (km/h)", "answer": vmax}],
        worked_solution=[f"Max distance {d + 0.5} km; min time {_g(t - 0.05)} h",
                         f"{d + 0.5} ÷ {_g(t - 0.05)} = **{_g(vmax)} km/h**"],
        notes=NOTES,
        distractors=distractors(vmax, [(_r((d + 0.5) / (t + 0.05)), "max ÷ max — the MAXIMUM speed needs the MINIMUM "
                                                                     "time."),
                                       (_r(d / t), "that's the speed from the rounded values — find the limits first.")]))


_GRAPH_RULES = {
    "cone_down": ("fast_slow", "narrow at the bottom, so the depth rises quickly at first, then more slowly"),
    "cone_up": ("slow_fast", "wide at the bottom, so the depth rises slowly at first, then faster"),
    "bowl": ("fast_slow", "narrow at the bottom, so the depth rises quickly at first, then more slowly"),
    "sphere": ("s_shape", "narrow at the bottom and top and wide in the middle: quick, slow, then quick"),
    "cylinder": ("linear", "the same width all the way up, so the depth rises at a constant rate"),
}


def _q_depth_graph():
    kind = random.choice(list(_GRAPH_RULES))
    right, why = _GRAPH_RULES[kind]
    others = random.sample([k for k in ("linear", "fast_slow", "slow_fast", "s_shape") if k != right], 2)
    kinds = [right] + others
    random.shuffle(kinds)
    letter = "ABC"[kinds.index(right)]
    answer = f"Graph {letter}: the container is {why}."
    vol = f"Graph {letter}: the volume of the container gets bigger as it fills."
    opts = [answer, vol] + [f"Graph {'ABC'[kinds.index(o)]}: the container is {_reason(o)}." for o in others]
    random.shuffle(opts)
    md = {"options": opts, "diagram": "composite_shape",
          "diagram_params": {"module_path": _DIAG, "kind": "container_and_graphs", "args": [kind, kinds], "width": 560}}
    return Question(
        question_text="Water is poured into the container at a constant rate. Which graph, and why, models the depth of water "
                      "against time?",
        correct_answer=answer, topic=TOPIC, question_type=QTYPE, worked_solution=[answer], notes=NOTES, metadata=md,
        distractors=[{"value": vol, "mistake": "explain how the DEPTH changes, not the volume (2023 and 2025 course "
                                               "reports)."}])


def _reason(shape):
    return {"linear": "the same width all the way up, so the depth rises at a constant rate",
            "fast_slow": "narrow at the bottom, so the depth rises quickly at first, then more slowly",
            "slow_fast": "wide at the bottom, so the depth rises slowly at first, then faster",
            "s_shape": "narrow at the bottom and top and wide in the middle: quick, slow, then quick"}[shape]


# (generator, weight) — weighted toward the past papers' marks, 2022–2026:
# rates/variables 2024 Q10, 2025 Q10(b), 2023 Q10(b) ≈ 7; model types 2023 Q8(b), 2024 Q10(a), 2026 Q5(b) ≈ 5;
# exponential claim 2022 Q10(a) = 2; depth graphs 2023 Q10(c), 2025 Q10(a)(c) = 7; errors 2026 Q5(c) = 2;
# recurrence long-term level 2023 Q8(c), 2024 Q4(c) = 2; profit 2026 Q5(b) = 2.
_CALCULATOR_MIX = [(_q_rate, 4), (_q_model_type, 3), (_q_claim, 2), (_q_depth_graph, 4), (_q_error, 2),
                   (_q_limits, 2), (_q_recurrence_limit, 2), (_q_profit, 2)]


def generate_modelling_calculator(calc_mode=False):
    gens, weights = zip(*_CALCULATOR_MIX)
    return random.choices(gens, weights=weights)[0]()


# ── spreadsheet questions ────────────────────────────────────────────────────────────────────
_YELLOW = PatternFill("solid", fgColor="FFF2CC")
_HEAD = PatternFill("solid", fgColor="1F3864")
_SCENARIOS = [
    dict(title="Air quality in a showroom", step="Day", qty="CO2 concentration (ppm)", short="CO2 concentration",
         unit="ppm", start=(1800, 2400, 100), pct=(10, 15), add=(120, 200, 10), n=(30, 40), whole=False),
    dict(title="Fish farm cage", step="Week", qty="Number of fish", short="number of fish", unit="fish",
         start=(2000, 3000, 50), pct=(10, 20), add=(200, 400, 25), n=(12, 26), whole=True),
    dict(title="Warehouse stock", step="Week", qty="Units of stock", short="units of stock", unit="units",
         start=(1500, 2000, 50), pct=(15, 25), add=(250, 350, 25), n=(20, 30), whole=True),
    dict(title="Medicine in the bloodstream", step="Dose", qty="Medicine (mg)", short="amount of medicine", unit="mg",
         start=(150, 250, 10), pct=(25, 35), add=(60, 100, 5), n=(10, 20), whole=False),
]


def _recurrence_values(start, keep, add, n, whole):
    u = [start]
    for _ in range(n):
        v = keep * u[-1] + add
        u.append(math.floor(v + 1e-9) if whole else v)
    return u


def _recurrence_workbook(sc, solved):
    wb = Workbook(); ws = wb.active; ws.title = "Model"
    ws.column_dimensions["A"].width = 40; ws.column_dimensions["B"].width = 22
    ws["A1"] = sc["title"]; ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Completed solution: the yellow cells contain the formulas used." if solved else
                "Complete the yellow cells. Use $ so you can fill down" + (", and INT for whole numbers." if sc["whole"] else "."))
    ws["A2"].font = Font(italic=True)
    ws["A4"] = f"Starting {sc['short']} ({sc['unit']})"; ws["B4"] = sc["start"]
    ws["A5"] = f"Percentage removed each {sc['step'].lower()}"; ws["B5"] = sc["pct"] / 100; ws["B5"].number_format = "0%"
    ws["A6"] = f"Percentage remaining each {sc['step'].lower()}"; ws["B6"].fill = _YELLOW; ws["B6"].number_format = "0%"
    ws["A7"] = f"Amount added each {sc['step'].lower()} ({sc['unit']})"; ws["B7"] = sc["add"]
    for c, h in zip("AB", [sc["step"], sc["qty"]]):
        ws[f"{c}10"] = h; ws[f"{c}10"].fill = _HEAD; ws[f"{c}10"].font = Font(bold=True, color="FFFFFF")
        ws[f"{c}10"].alignment = Alignment(wrap_text=True, horizontal="center")
    fmt = "0" if sc["whole"] else "0.00"
    ws["A11"] = 0; ws["B11"] = sc["start"]; ws["B11"].number_format = fmt
    values, filled = {}, []
    if solved:
        ws["B6"] = "=1-B5"; values["B6"] = 1 - sc["pct"] / 100; filled.append("B6")
    u = _recurrence_values(sc["start"], 1 - sc["pct"] / 100, sc["add"], sc["n"], sc["whole"])
    for k in range(1, sc["n"] + 1):
        r = 11 + k
        ws[f"A{r}"] = k; ws[f"B{r}"].fill = _YELLOW; ws[f"B{r}"].number_format = fmt
        if solved:
            core = f"$B$6*B{r - 1}+$B$7"
            ws[f"B{r}"] = f"=INT({core})" if sc["whole"] else f"={core}"
            values[f"B{r}"] = u[k]; filled.append(f"B{r}")
    if solved:
        ch = ScatterChart(); ch.title = sc["title"]; ch.x_axis.title = sc["step"]; ch.y_axis.title = sc["qty"]
        se = Series(Reference(ws, min_col=2, min_row=10, max_row=11 + sc["n"]),
                    Reference(ws, min_col=1, min_row=11, max_row=11 + sc["n"]), title_from_data=True)
        se.marker.symbol = "circle"; ch.series.append(se); ch.legend = None
        ws.add_chart(ch, "D10")
    return wb, ws, values, filled, u


def generate_modelling_spreadsheet_recurrence(calc_mode=False):
    base = random.choice(_SCENARIOS)
    sc = dict(base)
    sc["start"] = random.randrange(base["start"][0], base["start"][1] + 1, base["start"][2])
    sc["pct"] = random.randint(*base["pct"])
    sc["add"] = random.randrange(base["add"][0], base["add"][1] + 1, base["add"][2])
    sc["n"] = random.randint(*base["n"])
    wbq, _, _, _, u = _recurrence_workbook(sc, False)
    wbs, wss, values, filled, _ = _recurrence_workbook(sc, True)
    ans = float(u[-1]) if sc["whole"] else _r(u[-1])
    keep = 1 - sc["pct"] / 100
    cell = f"B{11 + sc['n']}"
    text = (f"**{sc['title']}.** The {sc['short']} starts at {sc['start']} {sc['unit']}. Each {sc['step'].lower()} "
            f"{sc['pct']}% is removed, and then {sc['add']} {sc['unit']} is added"
            f"{' (whole numbers only — use INT)' if sc['whole'] else ''}. Download the spreadsheet, complete it, and give the "
            f"{sc['short']} after {sc['n']} {sc['step'].lower()}s (cell {cell})" + ("." if sc["whole"] else ", to 2 decimal places."))
    limit = sc["add"] / (1 - keep)
    return Question(
        question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "Percentage remaining, as a decimal (cell B6)", "answer": _r(keep)},
                        {"prompt": f"Value after {sc['step'].lower()} 1", "answer": float(u[1]) if sc["whole"] else _r(u[1])},
                        {"prompt": f"Value after {sc['n']} {sc['step'].lower()}s", "answer": ans}],
        worked_solution=[f"B6: =1-B5 → {_g(keep)}",
                         f"B12: ={'INT(' if sc['whole'] else ''}$B$6*B11+$B$7{')' if sc['whole'] else ''}, filled down",
                         f"{cell} = **{_g(ans)}**",
                         f"It levels out at {sc['add']} ÷ {_g(sc['pct'] / 100)} = {_g(limit)} — a recurrence relation model."],
        notes=NOTES,
        metadata={"spreadsheet_bytes": workbook_bytes(wbq),
                  "spreadsheet_filename": f"{sc['title'].lower().replace(' ', '_')}.xlsx",
                  "spreadsheet_answer_cell": ("Model", cell),
                  **solution_metadata(wbs, wss, values, filled, min_row=4, max_row=11 + sc["n"], max_col=2,
                                      filename=f"{sc['title'].lower().replace(' ', '_')}_solution.xlsx")},
        distractors=distractors(ans, [(_r(sc["start"] * keep ** sc["n"]), "you left out the amount added each step."),
                                      (_r(limit), "that's the long-term level — the question asks for the value at "
                                                  f"{sc['step'].lower()} {sc['n']}.")]))


def _profit_workbook(s, c, k, xmax, step, solved):
    wb = Workbook(); ws = wb.active; ws.title = "Profit"
    ws.column_dimensions["A"].width = 34; ws.column_dimensions["B"].width = 16
    ws["A1"] = "Profit model:  Profit = (s − c)x − k x²"; ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Completed solution: the yellow cells contain the formulas used." if solved else
                "Enter s, c and k, then complete the Profit column and fill down.")
    values, filled = {}, []
    for r, (lab, val) in enumerate([("Selling price per item, s (£)", s), ("Cost to make each item, c (£)", c),
                                    ("Coefficient k", k)], start=4):
        ws[f"A{r}"] = lab; ws[f"B{r}"].fill = _YELLOW
        if solved:
            ws[f"B{r}"] = val
    for col, h in zip("AB", ["Number made and sold, x", "Profit (£)"]):
        ws[f"{col}9"] = h; ws[f"{col}9"].fill = _HEAD; ws[f"{col}9"].font = Font(bold=True, color="FFFFFF")
    xs = list(range(0, xmax + 1, step))
    for i, x in enumerate(xs):
        r = 10 + i
        ws[f"A{r}"] = x; ws[f"B{r}"].fill = _YELLOW; ws[f"B{r}"].number_format = "£#,##0.00"
        if solved:
            ws[f"B{r}"] = f"=($B$4-$B$5)*A{r}-$B$6*A{r}^2"
            values[f"B{r}"] = (s - c) * x - k * x * x; filled.append(f"B{r}")
    return wb, ws, values, filled, xs


def generate_modelling_spreadsheet_profit(calc_mode=False):
    s, c = random.choice([(9, 3), (12, 4), (10, 2), (14, 6), (11, 5)])
    k = random.choice([0.01, 0.015, 0.02, 0.025])
    best = (s - c) / (2 * k)
    xmax = int(round(2 * best / 100.0)) * 100 + 100
    xmax = max(xmax, 300)
    step = 20 if xmax <= 600 else 50
    wbq, _, _, _, xs = _profit_workbook(s, c, k, xmax, step, False)
    wbs, wss, values, filled, _ = _profit_workbook(s, c, k, xmax, step, True)
    last = f"B{9 + len(xs)}"
    ans = _r((s - c) * xmax - k * xmax * xmax)
    text = (f"A business models its profit as Profit = (s − c)x − {k}x², with s = £{s}, c = £{c}. Download the spreadsheet, "
            f"enter s, c and k, and complete the profit column from 0 to {xmax} items. Give the profit for {xmax} items "
            f"(cell {last}).")
    return Question(
        question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": f"Profit for {xmax} items (£)", "answer": ans}],
        worked_solution=[f"B10: =($B$4-$B$5)*A10-$B$6*A10^2, filled down", f"{last} = **£{ans:,.2f}**",
                         f"Quadratic model: maximum profit at x = {_g(best)}; beyond {_g(2 * best)} items the business "
                         f"makes a loss (2026 Q5(b))."],
        notes=NOTES,
        metadata={"spreadsheet_bytes": workbook_bytes(wbq), "spreadsheet_filename": "profit_model.xlsx",
                  "spreadsheet_answer_cell": ("Profit", last),
                  **solution_metadata(wbs, wss, values, filled, min_row=4, max_row=9 + len(xs), max_col=2,
                                      filename="profit_model_solution.xlsx")},
        distractors=distractors(ans, [(_r((s - c) * xmax - k ** 2), f"you squared k instead of x (2026 marking "
                                                                     f"instructions, Candidate A: −0.015^2)."),
                                      (_r((s - c) * xmax), "you left out the − kx² term.")]))


def generate_modelling_question(calc_mode=False):
    return random.choice([generate_modelling_calculator, generate_modelling_calculator,
                          generate_modelling_spreadsheet_recurrence, generate_modelling_spreadsheet_profit])()
