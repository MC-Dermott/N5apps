"""Higher Mathematical Modelling — levels filling the gaps found when the prelim learning outcomes were mapped to the
app (Nov 2026): tolerance (absolute and relative error, within tolerance, tolerance needed in an input), reading a
model's graph, and the specification's spreadsheet functions and data skills."""
import random
import statistics

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Font, PatternFill

from core.engine.spreadsheet_solution import solution_metadata, workbook_bytes
from core.models.further import g, md_table, part, question, r2, step
from core.models.question_model import Question

T, QT = "Modelling", "Mathematical Modelling"
_DIAG = "topics.modelling.modelling_diagrams"

NOTES_TOLERANCE = """
**Error and tolerance.** Absolute error = size of the error, in the units of the quantity. Relative error = absolute
error ÷ value (often as a percentage). A **tolerance** is the largest permitted error: a process is within tolerance only
if **every** result lies from target − tolerance to target + tolerance. To find the tolerance needed in an input, find
the limits allowed for the output and **work backwards** to the input.
"""


def generate_tolerance():
    target, tol_pc = random.choice([(500, 2), (250, 2), (1000, 1.5), (750, 2), (330, 3)])
    tol = r2(target * tol_pc / 100)
    inside = random.choice([True, False])
    vals = [round(target + random.uniform(-0.8, 0.8) * tol) for _ in range(5)]
    if not inside:
        vals[random.randrange(5)] = int(target + random.choice([-1, 1]) * (int(tol) + random.randint(1, 4)))
    ok = all(abs(v - target) <= tol for v in vals)
    k = random.choice([6, 8, 12, 15])
    C = random.choice([60, 90, 120, 150])
    pc = random.choice([2, 4, 5])
    xmax_err = r2(C * pc / 100 / k)
    ctx = (f"A machine fills bottles with a target of {target} ml and a tolerance of {tol_pc}%. A sample contains "
           f"(ml): {', '.join(map(str, vals))}.")
    ans = "Yes, every bottle is within tolerance" if ok else "No, at least one bottle is outside tolerance"
    parts = [
        part("(a)", "What is the largest absolute error allowed, in ml?", tol, [f"{tol_pc}% of {target} = **{g(tol)} ml**"], marks=1),
        part("(b)", "Is the sample within tolerance?", ans,
             [f"Allowed: {g(target - tol)} ml to {g(target + tol)} ml → **{ans}**"],
             options=["Yes, every bottle is within tolerance", "No, at least one bottle is outside tolerance"], marks=2),
        part("(c)", f"A cost is given by C = {k}x. C must be £{C} with a relative error of no more than {pc}%. "
                    f"What is the largest absolute error allowed in x? (2 d.p.)", xmax_err,
             [f"Error allowed in C = {pc}% of {C} = {g(C * pc / 100)}", f"Error in x = {g(C * pc / 100)} ÷ {k} = **{g(xmax_err)}**"],
             [step("Largest absolute error in C", r2(C * pc / 100))], marks=3),
    ]
    return question(T, QT, ctx, parts, NOTES_TOLERANCE, "Tolerance")


NOTES_GRAPH = """
**Reading a model's graph.** Read values from the axes, saying the units. **Linear** growth has a constant rate (equal
steps). **Exponential** growth gets steadily faster; exponential decay gets steadily slower, getting closer to zero
without reaching it. The average rate of change over an interval = change in y ÷ change in x. Beyond the plotted
range is **extrapolation**, which may not be reliable.
"""

_GRAPHS = [
    ("The number of users of an app", "month", "users", [200, 300, 400], [1.3, 1.4, 1.5]),
    ("The value of a machine", "year", "value (£ hundreds)", [200, 240, 300], [0.7, 0.75, 0.8]),
    ("The mass of a drug in the body", "hour", "mass (mg)", [160, 200, 240], [0.65, 0.7, 0.75]),
    ("The area of pondweed", "week", "area (m²)", [10, 20, 30], [1.4, 1.5, 1.6]),
]


def generate_reading_graph():
    what, xu, yu, starts, factors = random.choice(_GRAPHS)
    a, f, n = random.choice(starts), random.choice(factors), 6
    ys = [a * f ** k for k in range(n + 1)]
    i = random.choice([2, 3, 4])
    reading = int(round(ys[i]))
    first = (ys[2] - ys[0]) / 2
    last = (ys[6] - ys[4]) / 2
    shape = ("Growth that gets faster and faster" if f > 1 else "Decay that gets slower and slower")
    opts = ["Growth that gets faster and faster", "Growth at a constant rate", "Decay that gets slower and slower",
            "Decay at a constant rate"]
    ctx = f"{what} is modelled by the graph below."
    step_ = max(15, round(max(ys) * 0.15))
    choices = [str(reading), str(reading + step_), str(reading + 2 * step_), str(reading - step_ if reading > step_ else reading + 3 * step_)]
    random.shuffle(choices)
    p1 = part("(a)", f"Which is the best estimate of the {yu} at {xu} {i}, from the graph?", str(reading),
              [f"Read up from {i}: about **{reading}**"], marks=1, options=choices)
    parts = [
        p1,
        part("(b)", "Which describes the graph?", shape, [f"**{shape}** (an exponential model)"], options=opts, marks=1),
        part("(c)", f"How does the size of the average rate of change from {xu} 4 to 6 compare with that from {xu} 0 to 2?",
             "It is larger" if abs(last) > abs(first) else "It is smaller",
             [f"First: about {abs(first):.0f} per {xu}; last: about {abs(last):.0f} per {xu}"],
             options=["It is larger", "It is smaller", "It is the same"], marks=2),
        part("(d)", f"Why might the graph not be reliable for {xu} 30? (Reveal the expected answer.)",
             "It is far beyond the plotted data (extrapolation); the conditions that produced the pattern are unlikely to continue.",
             ["Extrapolation: the model may not remain valid."], explain=True, marks=1),
    ]
    q = question(T, QT, ctx, parts, NOTES_GRAPH, "Reading a Model's Graph",
                 extra={"diagram": "composite_shape",
                        "diagram_params": {"module_path": _DIAG, "kind": "exp_graph", "args": [a, f, n, xu, yu], "width": 460}})
    return q


NOTES_FUNCTIONS = """
**Spreadsheet functions** (specification list): SUM, PRODUCT, AVERAGE, MEDIAN, MIN, MAX, STDEV, PEARSON, COUNTIF, IF,
AND, OR, ROUND, ABS, INT and Goal Seek. Give columns clear headings, sort data before reading off the biggest or smallest,
put key values in their own labelled cells and use $ to fix them when filling down. Label chart axes (with units).
"""
_HEAD = PatternFill("solid", fgColor="1F3864")
_YELLOW = PatternFill("solid", fgColor="FFF2CC")


def _functions_workbook(names, hours, rate, limit, solved):
    wb = Workbook(); ws = wb.active; ws.title = "Data"
    for col, w in zip("ABCDEFG", (22, 16, 14, 16, 3, 40, 16)):
        ws.column_dimensions[col].width = w
    ws["A1"] = "Weekly timesheet"; ws["A1"].font = Font(bold=True, size=13)
    ws["A3"] = "Hourly rate (£)"; ws["B3"] = rate; ws["B3"].number_format = "£#,##0.00"
    ws["A4"] = "Hours before overtime"; ws["B4"] = limit
    for col, h in zip("ABCD", ["Worker", "Hours worked", "Overtime?", "Pay (£)"]):
        c = ws[f"{col}6"]; c.value = h; c.fill = _HEAD; c.font = Font(bold=True, color="FFFFFF")
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    values, filled = {}, []
    first, last = 7, 6 + len(names)

    def put(ref, formula, value, fmt=None):
        ws[ref].fill = _YELLOW
        if fmt:
            ws[ref].number_format = fmt
        if solved:
            ws[ref] = formula; values[ref] = value; filled.append(ref)

    pays = []
    for k, (nm, h) in enumerate(zip(names, hours)):
        r = first + k
        ws[f"A{r}"] = nm; ws[f"B{r}"] = h
        over = h > limit
        pay = h * rate + (max(h - limit, 0) * rate * 0.5)
        pays.append(pay)
        put(f"C{r}", f'=IF(B{r}>$B$4,"Yes","No")', "Yes" if over else "No")
        put(f"D{r}", f"=ROUND(B{r}*$B$3+IF(B{r}>$B$4,(B{r}-$B$4)*$B$3*0.5,0),2)", round(pay + 1e-9, 2), "£#,##0.00")
    pays = [round(p + 1e-9, 2) for p in pays]
    rng_b, rng_c, rng_d = f"B{first}:B{last}", f"C{first}:C{last}", f"D{first}:D{last}"
    summary = [("Total pay (£)", f"=SUM({rng_d})", sum(pays), "£#,##0.00"),
               ("Mean pay (£)", f"=AVERAGE({rng_d})", sum(pays) / len(pays), "£#,##0.00"),
               ("Median hours", f"=MEDIAN({rng_b})", statistics.median(hours), "0.0"),
               ("Standard deviation of hours", f"=STDEV({rng_b})", statistics.stdev(hours), "0.00"),
               ("Largest pay (£)", f"=MAX({rng_d})", max(pays), "£#,##0.00"),
               ("Smallest pay (£)", f"=MIN({rng_d})", min(pays), "£#,##0.00"),
               ("Number working overtime", f'=COUNTIF({rng_c},"Yes")', sum(h > limit for h in hours), "0")]
    for k, (lab, f, v, fmt) in enumerate(summary):
        r = 7 + k
        ws[f"F{r}"] = lab; put(f"G{r}", f, v, fmt)
    if solved:
        ch = BarChart(); ch.title = "Pay for each worker"; ch.x_axis.title = "Worker"; ch.y_axis.title = "Pay (£)"
        ch.add_data(Reference(ws, min_col=4, min_row=6, max_row=last), titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=1, min_row=first, max_row=last)); ch.legend = None
        ws.add_chart(ch, "F16")
    return wb, ws, values, filled, summary, pays


def generate_spreadsheet_functions(calc_mode=False):
    names = random.sample(["Ahmed", "Beth", "Chloe", "Dev", "Erin", "Finn", "Grace", "Hamish", "Isla", "Jack",
                           "Kai", "Lena", "Mia", "Noah"], 10)
    rate = random.choice([11.5, 12.2, 12.6, 13.4, 14.0])
    limit = random.choice([35, 36, 37])
    while True:
        hours = [random.randint(28, 46) for _ in names]
        n_over = sum(h > limit for h in hours)
        if 2 <= n_over <= 7:
            break
    wbq, _, _, _, _, _ = _functions_workbook(names, hours, rate, limit, False)
    wbs, wss, values, filled, summary, pays = _functions_workbook(names, hours, rate, limit, True)
    ans = r2(sum(pays))
    text = (f"**Weekly timesheet.** Hours above {limit} are paid at time and a half. Download the spreadsheet. Use IF to "
            f"show who worked overtime, then calculate each worker's pay, rounded to the nearest penny with ROUND. "
            f"Complete the summary cells using SUM, AVERAGE, MEDIAN, STDEV, MAX, MIN and COUNTIF. Upload your file; the answer checked is the **total pay "
            f"(cell G7)**.")
    return Question(
        question_text=text, correct_answer=ans, topic=T, question_type=QT,
        scaffold_steps=[{"prompt": f"Pay for {names[0]} (£)", "answer": pays[0]},
                        {"prompt": "Number working overtime", "answer": n_over},
                        {"prompt": "Total pay (£)", "answer": ans}],
        worked_solution=["C7: =IF(B7>$B$4,\"Yes\",\"No\"), filled down",
                         "D7: =ROUND(B7*$B$3+IF(B7>$B$4,(B7-$B$4)*$B$3*0.5,0),2), filled down",
                         f"G7: =SUM(D7:D16) → **£{ans:,.2f}**; COUNTIF(C7:C16,\"Yes\") → {n_over}"],
        notes=NOTES_FUNCTIONS,
        metadata={"spreadsheet_bytes": workbook_bytes(wbq), "spreadsheet_filename": "timesheet.xlsx",
                  "spreadsheet_answer_cell": ("Data", "G7"),
                  **solution_metadata(wbs, wss, values, filled, min_row=6, max_row=16, max_col=7,
                                      filename="timesheet_solution.xlsx")})


GAPS = {(T, QT): {"Tolerance": generate_tolerance, "Reading a Model's Graph": generate_reading_graph,
                  "Spreadsheet: Data and Functions": generate_spreadsheet_functions}}
