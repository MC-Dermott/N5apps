"""Higher Mathematical Modelling — further question types from the specification examples (Nov 2026): suggesting a
model from a description, choosing between two formulae, implausible predictions, improving a model, precision and
accuracy, units consistency, good spreadsheet practice."""
import math
import random

from core.models.further import g, part, question, r2, step, md_table

T, QT = "Modelling", "Mathematical Modelling"

NOTES_SUGGEST = """
**Suggesting a model.** Constant rate of change → **linear**; constant percentage change (grows or decays by the same factor)
→ **exponential**; rises then falls (or falls then rises) → **quadratic**; this period's amount from last period's → **recurrence**.
Always say when the model stops being valid (tank empty, food runs out, ball lands …).
"""
NOTES_CHOOSE = """
**Choosing between two formulae.** Evaluate both at the data points and compare. Then use the context: can the quantity be
negative? Does it level off? Does it keep increasing?
"""
NOTES_IMPLAUSIBLE = """
**Implausible predictions.** Evaluate the model. A negative population, a height below the ground, or more users than people
exist means the model is invalid there (extrapolating too far). State the range where it is valid.
"""
NOTES_PRECISION = """
**Precision and accuracy.** *Precise* = quoted to many digits; *accurate* = close to the truth. A final answer should not
have more significant figures than the least precise data.
"""
NOTES_UNITS = """
**Units.** Only quantities with the same units can be added, subtracted or compared. A rate (£ per year) cannot be compared with an
amount (£). Rate × time = amount.
"""
NOTES_IMPROVE = """
**Improving a model.** Unlimited exponential growth needs unlimited food/space. A better model lets growth slow as the supply runs
out, so the quantity levels off at a limiting value.
"""
NOTES_SHEET = """
**Good spreadsheet practice.** Put inputs in labelled cells; use absolute references ($B$1) for fixed inputs; add comments; use clear
names with units; check that comments match the formulae.
"""

_SCEN = [
    ("linear", "A tank holds {a} litres. Water drains at a steady {b} litres every minute.", "the volume V of water (litres)", "the time t (minutes)", "until the tank is empty", range(60, 241, 20), [4, 5, 6, 8, 10]),
    ("linear", "A phone starts at {a}% charge and loses {b}% of charge every hour.", "the charge C (%)", "the time t (hours)", "until it reaches 0%", [80, 90, 100], [6, 8, 10, 12]),
    ("exponential", "A video is seen by {a} people on day 1 and the audience grows by {b}% every day; there is a very large audience online.", "the number of viewers N", "the time t (days)", "when most of the available audience has already seen it", [20, 50, 100, 200], [20, 30, 40, 60]),
    ("exponential", "A mould covers {a} cm² of bread and its area grows by {b}% every day.", "the area A (cm²)", "the time t (days)", "when it covers the whole slice", [2, 3, 4, 5], [20, 30, 40, 50]),
    ("quadratic", "Water leaves a fountain nozzle at ground level, rises to a maximum height and lands {a} m away.", "the height h (m)", "the horizontal distance x (m)", "between the nozzle and where the water lands", [3, 4, 5], [0]),
    ("quadratic", "A cable hangs between two poles {a} m apart at the same height, and sags in the middle.", "the height of the cable h (m)", "the distance along the ground x (m)", "between the two poles", [20, 30, 40, 50], [0]),
    ("recurrence", "A savings balance each month is the previous month's balance plus {b}% interest, plus a £{a} deposit.", "the balance B (£)", "the month number n", "as long as the rate and deposit stay the same", [50, 80, 100, 150], [0.2, 0.3, 0.4, 0.5]),
]


def generate_suggest_model():
    kind, text, dep, ind, valid, ac, bc = random.choice(_SCEN)
    scen = text.format(a=random.choice(list(ac)), b=random.choice(bc))
    opts = ["linear", "exponential", "quadratic", "recurrence relation"]
    parts = [part("(a)", "Which type of model is most suitable?", "recurrence relation" if kind == "recurrence" else kind,
                  [{"linear": "Constant rate of change → **linear**", "exponential": "Constant percentage change → **exponential**",
                    "quadratic": "Rises then falls (or sags) → **quadratic**", "recurrence": "This month from last month → **recurrence relation**"}[kind]],
                  options=opts, marks=1),
             part("(b)", "Which is the independent variable?", ind, [f"The independent variable is **{ind}**."], options=[dep, ind], marks=1),
             part("(c)", "When would the model stop being valid? (Reveal the expected answer.)", valid, [f"The model is valid {valid}."], explain=True, marks=1)]
    return question(T, QT, scen, parts, NOTES_SUGGEST, "Suggest a Model")


def generate_choose_formula():
    kind = random.choice(["cooling", "growth"])
    if kind == "cooling":
        room, t0, k = random.choice([18, 20, 22]), random.choice([80, 85, 90]), random.choice([0.90, 0.92, 0.93, 0.95])
        xs = [0, 5, 10, 15, 20, 25]; data = [round(room + (t0 - room) * k ** x) for x in xs]
        slope = (data[0] - data[-1]) / 25 * 0.98
        A = lambda x: t0 - slope * x; B = lambda x: room + (t0 - room) * k ** x
        ctx = (f"The temperature T (°C) of a drink is measured every 5 minutes in a room at {room} °C.\n\n" + md_table(["t (min)"] + xs, [["T (°C)"] + data]) +
               f"\n\nFormula A: T = {t0} − {slope:.2f}t     Formula B: T = {room} + {t0 - room} × {k}ᵗ")
        xq = random.choice([10, 15, 20]); iq = xs.index(xq)
        lab = "T"; floor = f"cannot fall below {room} °C"
    else:
        a0, k = random.choice([2.0, 2.5, 3.0]), random.choice([1.35, 1.4, 1.45, 1.5]); xs = list(range(6))
        data = [round(a0 * k ** x, 1) for x in xs]; d = (data[-1] - data[0]) / 5
        A = lambda x: a0 + d * x; B = lambda x: a0 * k ** x
        ctx = ("The area A (cm²) of mould on bread is measured each day.\n\n" + md_table(["d (days)"] + xs, [["A (cm²)"] + data]) +
               f"\n\nFormula A: A = {a0} + {d:.2f}d     Formula B: A = {a0} × {k}ᵈ")
        xq = random.choice([2, 3, 4]); iq = xs.index(xq); lab = "A"; floor = "grows faster and faster"
    ea, eb = abs(A(xq) - data[iq]), abs(B(xq) - data[iq])
    parts = [part("(a)", f"Evaluate formula A at {xq} (1 d.p.).", round(A(xq), 1), [f"A({xq}) = **{A(xq):.1f}**"], marks=1),
             part("(b)", f"Evaluate formula B at {xq} (1 d.p.).", round(B(xq), 1), [f"B({xq}) = **{B(xq):.1f}**"], marks=1),
             part("(c)", "Which formula is the better model?", "Formula B", [f"The data value is {data[iq]}; B is closer ({eb:.1f} against {ea:.1f}) and fits the context ({floor}) → **Formula B**"],
                  options=["Formula A", "Formula B"], marks=2)]
    return question(T, QT, ctx, parts, NOTES_CHOOSE, "Choose Between Two Formulae")


def generate_implausible():
    kind = random.choice(["linear", "exponential", "ball"])
    if kind == "linear":
        a, b = random.choice([600, 900, 1200]), random.choice([60, 75, 100]); t = a // b + random.randint(2, 5)
        val = a - b * t
        ctx = f"A model for the number of fish N in a bay after t years is N = {a} − {b}t."
        parts = [part("(a)", f"Evaluate N when t = {t}.", val, [f"{a} − {b} × {t} = **{val}**"], marks=1),
                 part("(b)", "Is this prediction plausible?", "No: the number of fish cannot be negative", [f"A negative number of fish is impossible → **No**"], options=["Yes", "No: the number of fish cannot be negative"], marks=1),
                 part("(c)", "For how many whole years t is the model valid (N ≥ 0)?", a // b, [f"{a} ÷ {b} = {a / b:.2f}, so up to t = **{a // b}**"], marks=1)]
    elif kind == "exponential":
        a, b = random.choice([500, 1000, 1200, 2000]), random.choice([1.6, 1.7, 1.8, 2.0]); t = math.ceil(math.log(9e9 / a) / math.log(b)) + random.randint(0, 3)
        val = a * b ** t
        ctx = f"An app had {a} users at launch. A model says the number after t months is N = {a} × {b}ᵗ. The world's population is about 8 billion."
        parts = [part("(a)", f"Find N when t = {t} in billions (1 d.p.).", round(val / 1e9, 1), [f"{a} × {b}^{t} = **{val / 1e9:.1f} billion**"], marks=2),
                 part("(b)", "Is this plausible?", "No: more than the world's population", ["It exceeds the world's population → **No**"], options=["Yes", "No: more than the world's population"], marks=1)]
    else:
        h0, v = random.choice([2, 3]), random.choice([15, 20, 25]); t = random.choice([6, 7, 8])
        val = -5 * t * t + v * t + h0
        ctx = f"The height of a ball thrown from a roof is modelled by h = −5t² + {v}t + {h0} (h in metres, t in seconds)."
        land = (v + math.sqrt(v * v + 20 * h0)) / 10
        parts = [part("(a)", f"Find h when t = {t}.", val, [f"−5 × {t}² + {v} × {t} + {h0} = **{val}**"], marks=2),
                 part("(b)", "What does this tell you about the model?", "It is not valid after the ball lands", ["A negative height means below the ground, so the model stops being valid when the ball lands."], options=["It is valid for all t", "It is not valid after the ball lands"], marks=1),
                 part("(c)", "At what time does the ball land (2 d.p.)?", round(land, 2), [f"Solve h = 0: t = ({v} + √({v}² + 20 × {h0})) ÷ 10 = **{land:.2f} s**"], marks=2)]
    return question(T, QT, ctx, parts, NOTES_IMPLAUSIBLE, "Implausible Predictions")


def generate_precision_accuracy():
    true = random.choice([42000, 48000, 52000, 56000]); precise_wrong = true + random.choice([-4913, -3721, 4087, 5129])
    l, b = round(random.uniform(3, 9), 1), round(random.uniform(3, 9), 1); area = l * b; v_d, v_t = random.choice([80, 95, 120, 140]), round(random.uniform(7, 12), 1)
    sp = v_d / v_t
    stmts = {f"The crowd was {precise_wrong:,}.": "Precise but not accurate", f"The crowd was between {true - 12000:,} and {true + 12000:,}.": "Accurate but not precise",
             f"The crowd was between {true // 5:,} and {true // 3:,}.": "Neither"}
    s, ans = random.choice(list(stmts.items()))
    ctx = f"A stadium crowd was really about {true:,}."
    opts = ["Precise but not accurate", "Accurate but not precise", "Both", "Neither"]
    parts = [part("(a)", f"Describe the statement “{s}”", ans, [f"→ **{ans}**"], options=opts, marks=1),
             part("(b)", f"A garden is {l} m by {b} m. The calculator gives the area as {area:.2f} m². Give the area to 2 significant figures.", float(f"{area:.2g}"),
                  [f"The data have 2 significant figures, so **{float(f'{area:.2g}'):g} m²**"], marks=1),
             part("(c)", f"A runner covers {v_d} m (2 s.f.) in {v_t} s. Give the speed in m/s to a sensible precision.", float(f"{sp:.2g}"),
                  [f"{v_d} ÷ {v_t} = {sp:.3f}; to 2 s.f. = **{float(f'{sp:.2g}'):g} m/s**"], marks=1)]
    return question(T, QT, ctx, parts, NOTES_PRECISION, "Precision and Accuracy")


_UNITS = [
    ("“The perimeter of the rectangle is {p} cm and its area is {a} cm², so its perimeter is greater.”", False),
    ("“Zoe earns £{p} a year and owes £{a}, so she earns more than she owes.”", False),
    ("“The total cost is £{p} per tile × {a} tiles = £{c}.”", True),
    ("“Fuel used (litres) = distance (km) + driver’s age (years).”", False),
    ("“Distance = speed × time, with speed in km/h and time in hours, gives distance in km.”", True),
    ("“A firm earns £{p} million a year and owes £{a} million, so the debt is worth more than the whole firm's earnings.”", False),
]


def generate_units_consistency():
    t, ok = random.choice(_UNITS); p, a = random.choice(range(20, 60, 2)), random.choice(range(12, 40, 2)); c = p * a
    stmt = t.format(p=p, a=a, c=c)
    ans = "Valid: the units are consistent" if ok else "Invalid: the units are inconsistent"
    parts = [part("(a)", f"Is this statement valid?  {stmt}", ans, ["The units " + ("are consistent" if ok else "are inconsistent (different quantities compared or combined)") + f" → **{ans.split(':')[0]}**"],
                  options=["Valid: the units are consistent", "Invalid: the units are inconsistent"], marks=2)]
    return question(T, QT, "", parts, NOTES_UNITS, "Units Consistency")


def generate_improve_model():
    a, b, cap = random.choice([5, 8, 10]), random.choice([2, 3]), random.choice([300, 400, 500]); w = random.choice([8, 9, 10])
    val = a * b ** w
    ctx = f"Algae cover {a} m² of a pond at week 0 and the area is multiplied by {b} each week: A = {a} × {b}ʷ. The pond's area is {cap} m²."
    parts = [part("(a)", f"What area does the model predict at w = {w}?", val, [f"{a} × {b}^{w} = **{val} m²**"], marks=2),
             part("(b)", "Which assumption is at fault?", "Unlimited space and nutrients", [f"{val} m² is larger than the pond → the model assumes **unlimited space and nutrients**"],
                  options=["Unlimited space and nutrients", "A constant rate of change"], marks=1),
             part("(c)", "Suggest an improvement to the model. (Reveal the expected answer.)", f"Make the growth slow as the pond fills so the area levels off at {cap} m².",
                  [f"Make growth depend on the space left, so the area approaches a limit of {cap} m²."], explain=True, marks=1)]
    return question(T, QT, ctx, parts, NOTES_IMPROVE, "Improving a Model")


def generate_spreadsheet_practice():
    rate = random.choice([2, 3, 4]); dep = random.choice([100, 150, 200])
    ctx = (f"Sheet A holds `=B2*{1 + rate / 100:g}+{dep}` in every row. Sheet B has labelled cells: Rate (B1) = {rate}%, Deposit (B2) = £{dep}, "
           f"and its formula is `=B5*(1+$B$1)+$B$2`.")
    parts = [part("(a)", "Which sheet is easier for someone else to check?", "Sheet B", ["Inputs are labelled and visible in their own cells → **Sheet B**"], options=["Sheet A", "Sheet B"], marks=1),
             part("(b)", "The rate changes. How many cells must be edited in sheet B?", 1, ["Only B1 (the formulas use $B$1) → **1**"], marks=1),
             part("(c)", "Why does the formula use $B$1 and not B1?", "So the reference does not move when the formula is filled down",
                  ["The $ signs fix the reference as the formula is filled down."], options=["So the reference does not move when the formula is filled down", "To round the answer"], marks=1)]
    return question(T, QT, ctx, parts, NOTES_SHEET, "Good Spreadsheet Practice")


FURTHER = {("Modelling", "Mathematical Modelling"): {
    "Suggest a Model": generate_suggest_model, "Choose Between Two Formulae": generate_choose_formula, "Implausible Predictions": generate_implausible,
    "Precision and Accuracy": generate_precision_accuracy, "Units Consistency": generate_units_consistency, "Improving a Model": generate_improve_model,
    "Good Spreadsheet Practice": generate_spreadsheet_practice}}
