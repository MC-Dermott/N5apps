"""Higher Applications of Maths — Correlation and Regression (unit "Statistics").

Mirrors Correlation_and_Regression_Worksheet.docx (Higher Apps/Worksheets/Statistics): scatter plots of Y on X
and describing a relationship, the correlation coefficient r (from cor.test / summary(lm) output), calculating r
and the regression line from data, interpreting the slope and intercept, making predictions (interpolation vs
extrapolation), and trends and seasonality (4-point moving averages). No spreadsheet-formula questions — the
exam's software questions use .csv data with R or Excel — so the levels follow the worksheet's sections.

Distractors are the errors in the 2022 Q7, 2023 Q5 and 2026 Q3 course reports and marking instructions: X
plotted on Y, R² given for r, r interpreted without 'positive'/'linear' or without context, the equation not in
context, the regression of X on Y, the intercept read as the slope, x and y used the wrong way round in a
prediction, and extrapolation trusted. Pure Python statistics (no scipy): the t-distribution for cor.test's
p-value comes from the regularized incomplete beta function.
"""
import math
import random

from core.models.distractors import distractors
from core.models.question_model import Question, make_part, multipart_worked_solution

TOPIC, QTYPE = "Statistics", "Correlation and Regression"
_DIAG = "topics.statistics.correlation_regression_diagrams"


def _g(x, dp=2):
    x = round(x + 0.0, dp)
    s = f"{x:,.{dp}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def _r(x, dp=3):
    return round(x + 0.0, dp)


def _diagram(kind, *args, width=460):
    return {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DIAG, "kind": kind, "args": list(args), "width": width}}


# ── worksheet examples (Notes) ──────────────────────────────────────────────────────────────────
_EX_SCATTER = """
**Example (worksheet, Section 1).** A seafront café in Oban records the midday temperature (°C) and the
number of iced drinks sold on 14 days. Iced drinks sold DEPENDS on temperature, so it goes on the vertical
axis: a scatter plot of *number of iced drinks sold ON temperature* —
`plot(Temperature, Drinks, main="Scatterplot of iced drinks sold on temperature", xlab=..., ylab=...)`.
Comment: *a strong positive linear relationship: as the temperature increases, the number of iced drinks sold
increases.*

⚠ Plotting X on Y (carbohydrate on calories) — MOST candidates in 2023 (Q5(a)); in 2022 (Q7(a)(i)) it made the
regression line impossible to find. "Y on X" = Y up the side, X along the bottom.
"""
_EX_R = """
**Example (worksheet, Section 2).** `cor.test(Temperature, Drinks)` gives `cor 0.9639095`.
**r = 0.964** — stated on its own, separate from the output. *There is a strong positive linear correlation
between temperature and the number of iced drinks sold.* (Excel: `=CORREL(B2:B15, A2:A15)`.)
r measures a LINEAR relationship only; an outlier reduces it; correlation does not imply causation.

⚠ Giving R² (0.9291) instead of r — 2022 Q7(b)(i). From R², r = ±√R² with the SIGN of the slope.
Not stating r (2023 Q5(b)(i), 2026 Q3(b)); no 'positive' and 'linear' (2023 Q5(b)(ii)); no context
(2026 Q3(b)(ii) — no context, no mark).
"""
_EX_LINE = """
**Example (worksheet, Section 3).** `lm(Drinks ~ Temperature)` gives Intercept −24.155, slope 6.014:
**number of iced drinks sold = −24.155 + 6.014 × temperature.**
Slope: *for each increase of 1 °C in the temperature, the number of iced drinks sold increases by about 6.01.*
Intercept: *at 0 °C the model gives −24.15 drinks — impossible; 0 °C is outside the data (9–24 °C), so it has
no practical meaning.*
By hand: slope b = Sxy ÷ Sxx, intercept a = ȳ − b x̄, r = Sxy ÷ √(Sxx Syy), where Sxx = Σ(x − x̄)²,
Syy = Σ(y − ȳ)², Sxy = Σ(x − x̄)(y − ȳ).

⚠ Equation not in context — 2023 Q5(c)(i) (most candidates); 2026 Q3(c): "y = 43.944 − 2.376x" lost the mark.
lm(X ~ Y) is the wrong way round (2023 and 2026 marking instructions, Candidate A).
"""
_EX_PRED = """
**Example (worksheet, Section 4).** For 18.5 °C:
`predict(lm(Drinks ~ Temperature), newdata=data.frame(Temperature=18.5), interval="pred")` → fit 87.09,
lwr 69.69, upr 104.49. By substitution −24.155 + 6.014 × 18.5 = **87.1 — about 87 iced drinks.**
18.5 °C is inside the data (9–24 °C, interpolation) and r = 0.964 is a strong linear model, so it is reliable.
32 °C is outside the data (extrapolation): the trend may not continue — unreliable.

⚠ Not using the predict function or not commenting on accuracy (2022 Q7(c)); putting the value in for the
WRONG variable (2026 Q3(d), MI Candidate C; 2022 MI: 165 put in for jump height). The given value is X; the
estimate is Y.
"""
_EX_TREND = """
**Example (worksheet, Section 5).** Island visitors (thousands) each quarter, 2023–2025:
4.2, 9.8, 15.6, 6.1, 4.6, 10.5, 16.8, 6.5, 5.1, 11.2, 17.9, 7.0.
Seasonal pattern: highest every Q3 (July–September), lowest every Q1.
4-point moving averages: (4.2 + 9.8 + 15.6 + 6.1) ÷ 4 = **8.925**, then (9.8 + 15.6 + 6.1 + 4.6) ÷ 4 = 9.025, …
— rising, so the trend is upward. Compare a quarter with the SAME quarter a year earlier.

⚠ Not yet examined (course spec: 'exploring trends in data, for example seasonality'); in 2022 Q5(b) a comment
on change over TIME was needed. Describe both the seasonal pattern and the trend, in context.
"""
NOTES = ("**Correlation and regression** (Higher Apps — worksheet examples)\n" + _EX_SCATTER + _EX_R + _EX_LINE
         + _EX_PRED + _EX_TREND)


# ── statistics, pure Python ─────────────────────────────────────────────────────────────────────
def _betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-300 else 1e-300); h = d
    for m in range(1, 400):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c; c = c if abs(c) > 1e-300 else 1e-300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c; c = c if abs(c) > 1e-300 else 1e-300
        de = d * c; h *= de
        if abs(de - 1) < 1e-15:
            break
    return h


def _ibeta(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return bt * _betacf(a, b, x) / a
    return 1 - bt * _betacf(b, a, 1 - x) / b


def _p_t(t, df):
    return _ibeta(df / 2, 0.5, df / (df + t * t))


def _t975(df):
    lo, hi = 0.0, 50.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _p_t(mid, df) > 0.05 else (lo, mid)
    return (lo + hi) / 2


def _fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    r = sxy / math.sqrt(sxx * syy)
    b = sxy / sxx
    a = my - b * mx
    df = n - 2
    sse = sum((y - a - b * x) ** 2 for x, y in zip(xs, ys))
    t = r * math.sqrt(df / (1 - r * r))
    z, se = math.atanh(r), 1 / math.sqrt(n - 3)
    return dict(n=n, mx=mx, my=my, sxx=sxx, syy=syy, sxy=sxy, r=r, a=a, b=b, df=df, s=math.sqrt(sse / df), t=t,
                p=_p_t(t, df), ci=(math.tanh(z - 1.959963984540054 * se), math.tanh(z + 1.959963984540054 * se)))


def _predict(f, x0):
    y = f["a"] + f["b"] * x0
    h = _t975(f["df"]) * f["s"] * math.sqrt(1 + 1 / f["n"] + (x0 - f["mx"]) ** 2 / f["sxx"])
    return y, y - h, y + h


def _dec(x, sig):
    if x == 0:
        return 0
    d = max(0, sig - 1 - math.floor(math.log10(abs(x))))
    s = f"{abs(x):.{d}f}"
    if "." not in s:
        return 0
    s = s.rstrip("0")
    return 0 if s.endswith(".") else len(s.split(".")[1])


def _rvec(xs, sig=7):
    d = max(_dec(x, sig) for x in xs)
    return [f"{x:.{d}f}" for x in xs]


def _rp(p):
    if p < 2.220446e-16:
        return "< 2.2e-16"
    m, e = f"{p:.3e}".split("e")
    sci = f"{m.rstrip('0').rstrip('.')}e{int(e):+03d}"
    fixed = _rvec([p], 4)[0]
    return "= " + (fixed if len(fixed) <= len(sci) else sci)


def _cor_output(c, f):
    lo, hi = _rvec(list(f["ci"]))
    cor = _rvec([f["r"]])[0]
    return "\n".join([f"> cor.test({c['xn']}, {c['yn']})", "", "        Pearson's product-moment correlation", "",
                      f"data:  {c['xn']} and {c['yn']}",
                      f"t = {f['t']:.5g}, df = {f['df']}, p-value {_rp(f['p'])}",
                      "alternative hypothesis: true correlation is not equal to 0",
                      "95 percent confidence interval:", f" {lo} {hi}", "sample estimates:", "cor".rjust(len(cor)), cor])


def _lm_output(xn, yn, a, b):
    sa, sb = _rvec([a, b], 4)
    w1, w2 = max(11, len(sa)), max(len(xn), len(sb))
    return "\n".join([f"> lm({yn} ~ {xn})", "", "Coefficients:", "(Intercept)".rjust(w1) + "  " + xn.rjust(w2),
                      sa.rjust(w1) + "  " + sb.rjust(w2)])


def _dist(answer, cands):
    """distractors(), also dropping any value the app's 2% answer check would mark as correct."""
    keep = [(v, m) for v, m in cands if v is None or abs(answer) < 1e-9 or abs(v - answer) / abs(answer) > 0.025]
    return distractors(answer, keep)


def _code(text):
    return "```\n" + text + "\n```"


# ── contexts (Y on X) ──────────────────────────────────────────────────────────────────────────
# xn/yn: R variable names; xd/yd: descriptions; xu/yu: units; x: (lo, hi, dp); y = c + m x + noise (dp)
_CONTEXTS = [
    dict(xn="Temperature", yn="Drinks", xd="temperature", yd="number of iced drinks sold", xu="°C", yu="drinks",
         x=(8, 25, 0), c=-25, m=6.0, noise=9, ydp=0, who="A café in Oban records the midday temperature and the "
                                                         "number of iced drinks sold"),
    dict(xn="Age", yn="Weight", xd="age", yd="weight of a lamb", xu="weeks", yu="kg", x=(4, 22, 0), c=6.5, m=1.45,
         noise=1.6, ydp=1, who="A crofter in Lewis records the age and weight of lambs"),
    dict(xn="Engine", yn="CO2", xd="engine size", yd="CO2 emissions", xu="litres", yu="g/km", x=(1.0, 4.0, 1),
         c=60, m=50, noise=12, ydp=0, who="A garage records the engine size and CO2 emissions of cars"),
    dict(xn="Rainfall", yn="Visitors", xd="rainfall", yd="number of visitors", xu="mm", yu="visitors",
         x=(0, 16, 1), c=800, m=-22, noise=55, ydp=0, who="A visitor centre on Skye records the rainfall and the "
                                                          "number of visitors each day"),
    dict(xn="Distance", yn="Time", xd="distance", yd="winning time", xu="km", yu="minutes", x=(4, 24, 1), c=-1,
         m=5.8, noise=6, ydp=0, who="The distances and winning times of Scottish hill races are recorded"),
    dict(xn="Depth", yn="Distance", xd="tread depth", yd="stopping distance", xu="mm", yu="metres", x=(1.5, 8, 1),
         c=44, m=-2.4, noise=1.2, ydp=1, who="A tyre maker records the tread depth and the stopping distance of cars"),
    dict(xn="Wind", yn="Crossing", xd="wind speed", yd="crossing time", xu="mph", yu="minutes", x=(5, 35, 0),
         c=160, m=1.1, noise=4.5, ydp=0, who="A ferry company records the wind speed and the time of crossings "
                                             "between Ullapool and Stornoway"),
    dict(xn="Age", yn="Price", xd="age", yd="price of a used car", xu="years", yu="pounds", x=(1, 10, 0), c=18000,
         m=-1400, noise=1300, ydp=-2, who="A dealer in Inverness records the age and price of used cars"),
]


def _round(v, dp):
    v = round(v, dp)
    return int(v) if dp <= 0 else v


def _data(c, n, rmin=0.6, rmax=0.975, noise_mult=None):
    """Random data for a context, with |r| between rmin and rmax (the noise is varied until it fits)."""
    lo, hi, xdp = c["x"]
    for _ in range(2000):
        xs = sorted(_round(random.uniform(lo, hi), xdp) for _ in range(n))
        if len(set(xs)) < min(0.6 * n, 0.7 * ((hi - lo) * 10 ** xdp + 1)):
            continue
        k = math.exp(random.uniform(math.log(0.15), math.log(4)))
        ys = [_round(c["c"] + c["m"] * x + random.gauss(0, c["noise"] * k), c["ydp"]) for x in xs]
        if min(ys) <= 0:
            continue
        f = _fit(xs, ys)
        if rmin <= abs(f["r"]) <= rmax and not 0.78 <= abs(f["r"]) <= 0.82:
            return xs, ys, f
    return _data(c, max(7, n - 2), rmin, rmax)


def _one(u):
    """'1 week', '1 minute', '1 kg' — the unit after the number 1."""
    return u[:-1] if u.endswith("s") else u


def _strength(r):
    return "strong" if abs(r) > 0.8 else "moderate"


def _dirn(r):
    return "positive" if r > 0 else "negative"


def _incdec(v):
    return "increases" if v > 0 else "decreases"


def _describe(c, r):
    return (f"A {_strength(r)} {_dirn(r)} linear relationship: as the {c['xd']} increases, the {c['yd']} "
            f"{_incdec(r)}.")


def _table(c, xs, ys):
    head = f"| {c['xd'].capitalize()} ({c['xu']}) | " + " | ".join(_g(x, 3) for x in xs) + " |"
    sep = "|---" * (len(xs) + 1) + "|"
    row = f"| {c['yd'].capitalize()} ({c['yu']}) | " + " | ".join(_g(y, 3) for y in ys) + " |"
    return "\n".join([head, sep, row])


def _eq(c, a, b, dp=3):
    sign = "+" if b >= 0 else "−"
    return f"{c['yd']} = {_g(a, dp)} {sign} {_g(abs(b), dp)} × {c['xd']}"


# ── Level 1: scatter plots ─────────────────────────────────────────────────────────────────────
def generate_correlation_regression_l1(calc_mode=False):
    c = random.choice(_CONTEXTS)
    if random.random() < 0.35:
        right = f"The {c['yd']} on the vertical (y) axis — it depends on the {c['xd']}."
        wrong = f"The {c['xd']} on the vertical (y) axis — it is the first variable."
        opts = [right, wrong, "Either variable — it makes no difference to the regression line.",
                f"The {c['yd']} on the horizontal (x) axis — it is the one being predicted."]
        random.shuffle(opts)
        return Question(
            question_text=f"{c['who']}. The {c['yd']} depends on the {c['xd']}. A scatter plot of {c['yd']} ON "
                          f"{c['xd']} is to be constructed. Which variable goes on the vertical axis?",
            correct_answer=right, topic=TOPIC, question_type=QTYPE, notes=_EX_SCATTER,
            worked_solution=[right, f"'{c['yd']} on {c['xd']}' = Y on X: Y up the side, X along the bottom."],
            metadata={"options": opts},
            distractors=[{"value": wrong, "mistake": "that's X on Y — most candidates did this in 2023 (Q5(a)) and "
                                                     "lost the mark (course report)."},
                         {"value": "Either variable — it makes no difference to the regression line.",
                          "mistake": "it does: in 2022 (Q7) plotting X on Y made the regression line of Y on X "
                                     "impossible to find (course report)."}])
    n = random.randint(12, 16)
    if random.random() < 0.2:
        lo, hi, xdp = c["x"]
        while True:
            xs = sorted(_round(random.uniform(lo, hi), xdp) for _ in range(n))
            ymid = c["c"] + c["m"] * (lo + hi) / 2
            ys = [_round(abs(ymid) * random.uniform(0.6, 1.4), c["ydp"]) for _ in xs]
            if abs(_fit(xs, ys)["r"]) < 0.3 and min(ys) > 0:
                break
        right = f"There is no linear relationship between the {c['xd']} and the {c['yd']}."
        r = 0.0
    else:
        strong = random.random() < 0.6
        xs, ys, f = _data(c, n, *((0.9, 0.985) if strong else (0.62, 0.76)), noise_mult=0.5 if strong else 2.2)
        r = f["r"]
        right = _describe(c, r)
    opts = {right}
    for s in ("strong", "moderate"):
        for d in ("positive", "negative"):
            opts.add(f"A {s} {d} linear relationship: as the {c['xd']} increases, the {c['yd']} "
                     f"{'increases' if d == 'positive' else 'decreases'}.")
    opts.add(f"There is no linear relationship between the {c['xd']} and the {c['yd']}.")
    vague = "There is a strong correlation."
    opts = sorted(opts)
    keep = [right] + random.sample([o for o in opts if o != right], 3) + [vague]
    random.shuffle(keep)
    wrong_dir = (f"A {_strength(r)} {'negative' if r > 0 else 'positive'} linear relationship: as the {c['xd']} "
                 f"increases, the {c['yd']} {'decreases' if r > 0 else 'increases'}.")
    md = {"options": keep, **_diagram("app_scatter", xs, ys, f"{c['xd']} ({c['xu']})", f"{c['yd']} ({c['yu']})",
                                      f"Scatterplot of {c['yd']} on {c['xd']}", False, None)}
    return Question(
        question_text=f"{c['who']}. Make an appropriate comment about the relationship shown in the scatter plot.",
        correct_answer=right, topic=TOPIC, question_type=QTYPE, notes=_EX_SCATTER, metadata=md,
        worked_solution=[right, "Give the direction (positive/negative), the form (linear) and the strength — in "
                                "context (2022 MI: 'positive' must appear)."],
        distractors=[{"value": vague, "mistake": "no direction, no 'linear' and no context — 'positive' must appear "
                                                 "(2022 marking instructions) and context is needed (2026 Q3(b)(ii))."},
                     {"value": wrong_dir, "mistake": "check the direction: going up from left to right is positive."}])


# ── Level 2: the correlation coefficient from software output ──────────────────────────────────
def generate_correlation_regression_l2(calc_mode=False):
    c = random.choice(_CONTEXTS)
    xs, ys, f = _data(c, random.randint(10, 18), 0.62, 0.975)
    r = _r(f["r"])
    r2 = _r(f["r"] ** 2, 4)
    if random.random() < 0.5:
        shown = _code(_cor_output(c, f))
        lead = "This output was produced with statistical software."
        sc = [{"prompt": "The number under 'cor' (to 3 d.p.)", "answer": r}]
        how = [f"The number under 'cor' is {_rvec([f['r']])[0]}", f"**r = {_g(r, 3)}** — stated separately"]
    else:
        sa, sb = _rvec([f["a"], f["b"]], 5)
        shown = _code(f"> summary(lm({c['yn']} ~ {c['xn']}))\n...\nCoefficients:\n            Estimate\n"
                      f"(Intercept) {sa}\n{c['xn']:<11} {sb}\n...\nMultiple R-squared:  {f['r']**2:.4f}")
        lead = "Part of the summary output of a regression is shown."
        sc = [{"prompt": "√R² (to 3 d.p.)", "answer": _r(math.sqrt(round(f['r'] ** 2, 4)))},
              {"prompt": "r, with the sign of the slope", "answer": r}]
        how = [f"R² = {f['r']**2:.4f}, so √R² = {_g(math.sqrt(round(f['r']**2, 4)), 3)}",
               f"The slope is {_dirn(f['b'])}, so **r = {_g(r, 3)}** (2022 MI: R² must be square-rooted)."]
    pa = make_part("(a)", "State the correlation coefficient, r, to 3 decimal places.", r, scaffold_steps=sc,
                   worked_solution=how,
                   distractors=_dist(r, [(r2, "that's R², the coefficient of determination — not r (2022 Q7(b)(i), "
                                                    "course report)."),
                                               (_r(-r), "check the sign: r has the same sign as the slope."),
                                               (_r(f["t"]), "that's the t statistic, not r."),
                                               (_r(f["ci"][0]), "that's the lower end of the confidence interval, "
                                                                "not r.")]))
    right = (f"There is a {_strength(r)} {_dirn(r)} linear correlation between the {c['xd']} and the {c['yd']}: as the "
             f"{c['xd']} increases, the {c['yd']} tends to {'increase' if r > 0 else 'decrease'}.")
    noctx = f"There is a {_strength(r)} {_dirn(r)} linear correlation."
    vague = "There is a strong correlation between the variables."
    wrongd = (f"There is a {_strength(r)} {'negative' if r > 0 else 'positive'} linear correlation between the "
              f"{c['xd']} and the {c['yd']}.")
    opts = [right, noctx, vague, wrongd]
    random.shuffle(opts)
    pb = make_part("(b)", "Interpret the correlation coefficient.", right, options=opts, worked_solution=[right],
                   distractors=[{"value": noctx, "mistake": "no context — the 2026 marking instructions (Q3(b)(ii)) only "
                                                            "give the mark where context is included."},
                                {"value": vague, "mistake": "say 'positive'/'negative' and 'linear' (2023 Q5(b)(ii), "
                                                            "course report), in context."},
                                {"value": wrongd, "mistake": "a negative r means one variable decreases as the other "
                                                             "increases — check the sign."}])
    return Question(question_text=f"{c['who']}. {lead}\n\n{shown}", correct_answer=r, topic=TOPIC,
                    question_type=QTYPE, parts=[pa, pb], worked_solution=multipart_worked_solution([pa, pb]),
                    notes=_EX_R)


# ── Level 3: r and the regression line from the data ───────────────────────────────────────────
def generate_correlation_regression_l3(calc_mode=False):
    c = random.choice(_CONTEXTS)
    xs, ys, f = _data(c, random.randint(7, 9), 0.7, 0.975)
    r, b, a = _r(f["r"]), _r(f["b"], 3), _r(f["a"], 3)
    bxy = f["sxy"] / f["syy"]                    # slope of the regression of X on Y
    axy = f["mx"] - bxy * f["my"]
    sc_common = [{"prompt": "Mean of x (x̄)", "answer": _r(f["mx"], 4)}, {"prompt": "Mean of y (ȳ)", "answer": _r(f["my"], 4)},
                 {"prompt": "Sxx = Σ(x − x̄)²", "answer": _r(f["sxx"], 4)}, {"prompt": "Sxy = Σ(x − x̄)(y − ȳ)",
                                                                             "answer": _r(f["sxy"], 4)}]
    pa = make_part("(a)", f"Find the correlation coefficient between the {c['yd']} and the {c['xd']}, to 3 d.p.", r,
                   scaffold_steps=sc_common + [{"prompt": "Syy = Σ(y − ȳ)²", "answer": _r(f["syy"], 4)},
                                               {"prompt": "r = Sxy ÷ √(Sxx × Syy)", "answer": r}],
                   worked_solution=[f"cor.test({c['xn']}, {c['yn']}) or =CORREL(): **r = {_g(r, 3)}**",
                                    f"(Sxy = {_g(f['sxy'], 3)}, Sxx = {_g(f['sxx'], 3)}, Syy = {_g(f['syy'], 3)})"],
                   distractors=_dist(r, [(_r(f["r"] ** 2), "that's R², not r (2022 Q7(b)(i)).")]))
    pb = make_part("(b)", f"Find the slope of the regression line of {c['yd']} on {c['xd']}, to 3 d.p.", b,
                   scaffold_steps=sc_common + [{"prompt": "slope b = Sxy ÷ Sxx", "answer": b}],
                   worked_solution=[f"lm({c['yn']} ~ {c['xn']}) or =SLOPE(): b = {_g(f['sxy'], 3)} ÷ {_g(f['sxx'], 3)} "
                                    f"= **{_g(b, 3)}**"],
                   distractors=_dist(b, [(_r(bxy, 3), f"that's the slope of {c['xd']} ON {c['yd']} — lm(X ~ Y), "
                                                            f"the wrong way round (2023/2026 MI, Candidate A)."),
                                               (r, "that's r, not the slope.")]))
    pc = make_part("(c)", "Find the intercept, to 3 d.p., and state the equation of the regression line in context.", a,
                   scaffold_steps=[{"prompt": "slope b", "answer": b}, {"prompt": "intercept a = ȳ − b x̄", "answer": a}],
                   worked_solution=[f"a = {_g(f['my'], 4)} − {_g(f['b'], 4)} × {_g(f['mx'], 4)} = **{_g(a, 3)}**",
                                    f"**{_eq(c, f['a'], f['b'])}** — with the variables' names (2023 Q5(c)(i))."],
                   distractors=_dist(a, [(_r(axy, 3), "that's the intercept of lm(X ~ Y) — the wrong way round."),
                                               (_r(f["my"], 3), "that's ȳ — subtract b × x̄."),
                                               (_r(f["my"] + f["b"] * f["mx"], 3), "a = ȳ − b x̄, not ȳ + b x̄.")]))
    md = {"table": _table(c, xs, ys)}
    return Question(question_text=f"{c['who']}. Use statistical software (cor.test and lm in R, or CORREL, SLOPE and "
                                  f"INTERCEPT in Excel) or a calculator with the data below.",
                    correct_answer=r, topic=TOPIC, question_type=QTYPE, parts=[pa, pb, pc],
                    worked_solution=multipart_worked_solution([pa, pb, pc]), notes=_EX_LINE, metadata=md)


# ── Level 4: interpreting slope and intercept ──────────────────────────────────────────────────
def generate_correlation_regression_l4(calc_mode=False):
    c = random.choice(_CONTEXTS)
    xs, ys, f = _data(c, random.randint(10, 15), 0.85, 0.985)
    lo, hi = min(xs), max(xs)
    a, b = f["a"], f["b"]
    adp = 0 if abs(a) >= 100 else 2
    bdp = 0 if abs(b) >= 100 else 2
    lm = _lm_output(c["xn"], c["yn"], a, b)
    slope_ok = (f"For each increase of 1 {_one(c['xu'])} in the {c['xd']}, the {c['yd']} {_incdec(b)} by about "
                f"{_g(abs(b), bdp)} {c['yu']}.")
    slope_int = f"When the {c['xd']} is 0 {c['xu']}, the {c['yd']} is {_g(b, bdp)} {c['yu']}."
    slope_swap = (f"For each increase of 1 {_one(c['yu'])} in the {c['yd']}, the {c['xd']} {_incdec(b)} by about "
                  f"{_g(abs(b), bdp)} {c['xu']}.")
    slope_a = (f"For each increase of 1 {_one(c['xu'])} in the {c['xd']}, the {c['yd']} changes by {_g(a, adp)} {c['yu']}.")
    o1 = [slope_ok, slope_int, slope_swap, slope_a]
    random.shuffle(o1)
    pa = make_part("(a)", "Interpret the slope.", slope_ok, options=o1, worked_solution=[slope_ok],
                   distractors=[{"value": slope_int, "mistake": "that's how you describe an INTERCEPT — the slope is the "
                                                                "change in Y for each 1 unit increase in X (2023 Q5(c)(ii))."},
                                {"value": slope_swap, "mistake": "the wrong way round: the slope of Y on X is the change "
                                                                 "in Y per unit of X."},
                                {"value": slope_a, "mistake": "that's the intercept's value, not the slope."}])
    meaningful = a > 0 and lo / (hi - lo) <= 0.3          # 0 is at (or just below) the edge of the data
    int_val = f"When the {c['xd']} is 0 {c['xu']}, the model gives a {c['yd']} of {_g(a, adp)} {c['yu']}"
    if meaningful:
        int_ok = int_val + "."
        int_alt = (f"The intercept has no meaning, because a {c['xd']} of 0 {c['xu']} is impossible.")
        mistake_alt = "0 is close to the data here, and the value is sensible — interpret it in context."
    else:
        int_ok = (int_val + f" — but 0 {c['xu']} is outside the data ({_g(lo)} to {_g(hi)} {c['xu']}), so it has no "
                            f"practical meaning.")
        int_alt = int_val + ", and this is a reliable estimate."
        mistake_alt = "0 is outside the range of the data — the intercept is an extrapolation."
    int_slope = f"For each increase of 1 {_one(c['xu'])} in the {c['xd']}, the {c['yd']} changes by {_g(a, adp)} {c['yu']}."
    o2 = [int_ok, int_alt, int_slope]
    random.shuffle(o2)
    pb = make_part("(b)", "Interpret the intercept.", int_ok, options=o2, worked_solution=[int_ok],
                   distractors=[{"value": int_alt, "mistake": mistake_alt},
                                {"value": int_slope, "mistake": "that's how you describe a SLOPE — the intercept is the "
                                                                "value of Y when X = 0."}])
    eq_ok = _eq(c, a, b, 3)
    eq_xy = f"y = {_g(a, 3)} {'+' if b >= 0 else '−'} {_g(abs(b), 3)}x"
    eq_rev = f"{c['xd']} = {_g(a, 3)} {'+' if b >= 0 else '−'} {_g(abs(b), 3)} × {c['yd']}"
    o0 = [eq_ok, eq_xy, eq_rev]
    random.shuffle(o0)
    p0 = make_part("(a)", f"State the equation of the regression line of {c['yd']} on {c['xd']}.", eq_ok, options=o0,
                   worked_solution=[eq_ok],
                   distractors=[{"value": eq_xy, "mistake": "not in context — 2026 marking instructions (Candidate B): "
                                                            "'y = 43.944 − 2.376x' lost the mark."},
                                {"value": eq_rev, "mistake": "the variables are the wrong way round."}])
    pa.metadata["label"], pb.metadata["label"] = "(b)", "(c)"
    parts = [p0, pa, pb]
    md = _diagram("app_scatter", xs, ys, f"{c['xd']} ({c['xu']})", f"{c['yd']} ({c['yu']})",
                  f"Scatterplot of {c['yd']} on {c['xd']}", True, None)
    return Question(question_text=f"{c['who']} ({_g(lo)} to {_g(hi)} {c['xu']}).\n\n{_code(lm)}", correct_answer=eq_ok,
                    topic=TOPIC, question_type=QTYPE, parts=parts, worked_solution=multipart_worked_solution(parts),
                    notes=_EX_LINE, metadata=md)


# ── Level 5: making predictions ────────────────────────────────────────────────────────────────
def generate_correlation_regression_l5(calc_mode=False):
    c = random.choice(_CONTEXTS)
    xs, ys, f = _data(c, random.randint(10, 15), 0.85, 0.985)
    lo, hi, xdp = min(xs), max(xs), c["x"][2]
    a, b = float(_rvec([f["a"]], 4)[0]), float(_rvec([f["b"]], 4)[0])
    x0 = _round(random.uniform(lo + 0.15 * (hi - lo), hi - 0.15 * (hi - lo)), max(xdp, 1) if hi - lo < 10 else 0)
    y0 = a + b * x0
    dp = 0 if abs(y0) >= 1000 else 1 if abs(y0) >= 10 else 2
    ans = _r(y0, dp)
    fit_, plo, phi = _predict(f, x0)
    lm = _lm_output(c["xn"], c["yn"], a, b)
    swap = (x0 - a) / b
    pa = make_part("(a)", f"Estimate the {c['yd']} when the {c['xd']} is {_g(x0, 2)} {c['xu']}"
                          f"{' (to the nearest whole number)' if dp == 0 else f' (to {dp} d.p.)'}.", ans,
                   scaffold_steps=[{"prompt": f"slope × {_g(x0, 2)}", "answer": _r(b * x0, 3)},
                                   {"prompt": f"intercept + slope × {_g(x0, 2)}", "answer": ans}],
                   worked_solution=[f"{_g(a, 4)} {'+' if b >= 0 else '−'} {_g(abs(b), 4)} × {_g(x0, 2)} = **{_g(ans, dp)} "
                                    f"{c['yu']}**",
                                    f"predict(lm({c['yn']} ~ {c['xn']}), newdata=data.frame({c['xn']}={_g(x0, 2)}), "
                                    f"interval=\"pred\") gives {_g(fit_, 2)} ({_g(plo, 2)} to {_g(phi, 2)})."],
                   distractors=_dist(ans, [(_r(swap, dp), f"you put {_g(x0, 2)} in for the {c['yd']} — x and y the "
                                                               f"wrong way (2026 Q3(d), MI Candidate C)."),
                                                 (_r(b * x0, dp), "you left out the intercept."),
                                                 (_r(a + x0, dp), "multiply the slope by x — don't add.")]))
    outside = random.random() < 0.5
    span = hi - lo
    x1 = _round(hi + random.uniform(0.6, 1.5) * span if outside else random.uniform(lo + 0.1 * span, hi - 0.1 * span),
                xdp if xdp > 0 else 0)
    good = (f"Reliable: {_g(x1, 2)} {c['xu']} is within the data ({_g(lo)} to {_g(hi)}) and r = {_g(f['r'], 3)} shows a "
            f"strong linear model.")
    bad = (f"Not reliable: {_g(x1, 2)} {c['xu']} is outside the data ({_g(lo)} to {_g(hi)}) — extrapolation; the trend "
           f"may not continue.")
    trust = f"Reliable: r = {_g(f['r'], 3)} is strong, so the model can be used for any {c['xd']}."
    right = bad if outside else good
    opts = [good, bad, trust]
    random.shuffle(opts)
    dist = [{"value": trust, "mistake": "a strong r is not enough — the value must also be within the range of the data "
                                        "(course spec; 2022 Q7(c) marking instructions)."}]
    if outside:
        dist.append({"value": good, "mistake": f"{_g(x1, 2)} is outside the data — that's extrapolation."})
    else:
        dist.append({"value": bad, "mistake": f"{_g(x1, 2)} is inside the data ({_g(lo)} to {_g(hi)}) — interpolation."})
    pb = make_part("(b)", f"Comment on the reliability of using the model to estimate the {c['yd']} when the {c['xd']} is "
                          f"{_g(x1, 2)} {c['xu']}.", right, options=opts, worked_solution=[right], distractors=dist)
    md = _diagram("app_scatter", xs, ys, f"{c['xd']} ({c['xu']})", f"{c['yd']} ({c['yu']})",
                  f"Scatterplot of {c['yd']} on {c['xd']}", True, [x0, y0])
    return Question(question_text=f"{c['who']} ({len(xs)} observations, {c['xd']} from {_g(lo)} to {_g(hi)} {c['xu']}; "
                                  f"r = {_g(f['r'], 3)}).\n\n{_code(lm)}",
                    correct_answer=ans, topic=TOPIC, question_type=QTYPE, parts=[pa, pb],
                    worked_solution=multipart_worked_solution([pa, pb]), notes=_EX_PRED, metadata=md)


# ── Level 6: trends and seasonality ────────────────────────────────────────────────────────────
_SERIES = [
    dict(what="visitors (thousands) to an island in the Inner Hebrides", peak=3, base=[4.5, 10, 16, 6.3], dp=1,
         why="summer"),
    dict(what="heating oil delivered (thousand litres) on Harris", peak=1, base=[38, 21, 12, 30], dp=0, why="winter"),
    dict(what="electricity used (kWh) by a house in Shetland", peak=1, base=[1450, 980, 720, 1210], dp=0, why="winter"),
    dict(what="ice creams sold (hundreds) by a shop in Pitlochry", peak=3, base=[12, 30, 46, 16], dp=0, why="summer"),
]


def generate_correlation_regression_l6(calc_mode=False):
    s = random.choice(_SERIES)
    years = random.choice([2, 3])
    trend = random.choice([1, -1]) * random.uniform(0.02, 0.05)
    vals = []
    for k in range(4 * years):
        v = s["base"][k % 4] * (1 + trend * k / 4) * random.uniform(0.97, 1.03)
        vals.append(_round(v, s["dp"]))
    y0 = random.choice([2023, 2024])
    labels = [f"Q{q} {y0 + y}" for y in range(years) for q in (1, 2, 3, 4)]
    mas = [sum(vals[i:i + 4]) / 4 for i in range(len(vals) - 3)]
    k = random.randint(1, min(3, len(mas)))
    ans = _r(mas[k - 1], 3)
    direction = "upward" if mas[-1] > mas[0] else "downward"
    pa = make_part("(a)", f"Calculate 4-point moving average number {k} (the mean of quarters {k} to {k + 3}).", ans,
                   scaffold_steps=[{"prompt": f"Sum of quarters {k} to {k + 3}", "answer": _r(sum(vals[k - 1:k + 3]), 3)},
                                   {"prompt": "Divide by 4", "answer": ans}],
                   worked_solution=[f"({' + '.join(_g(v, 2) for v in vals[k - 1:k + 3])}) ÷ 4 = **{_g(ans, 3)}**"],
                   distractors=_dist(ans, [(_r(sum(vals[k - 1:k + 3]), 3), "divide the total by 4."),
                                                 (_r(sum(vals[k - 1:k + 2]) / 3, 3), "a 4-point moving average uses FOUR "
                                                                                     "quarters."),
                                                 (_r(sum(vals[k:k + 4]) / 4, 3) if k + 4 <= len(vals) else None,
                                                  "start at quarter number " + str(k) + ".")]))
    low = {3: 1, 1: 3}[s["peak"]]
    right = (f"Seasonal: highest every Q{s['peak']} ({s['why']}) and lowest every Q{low}; the moving averages show a "
             f"gradual {direction} trend.")
    wrong_trend = (f"Seasonal: highest every Q{s['peak']} ({s['why']}) and lowest every Q{low}; the moving averages show "
                   f"a gradual {'downward' if direction == 'upward' else 'upward'} trend.")
    no_season = f"There is no pattern: the values go up and down at random, and the trend is {direction}."
    fall = f"The values fall sharply after every Q{s['peak']}, so the figures are collapsing."
    opts = [right, wrong_trend, no_season, fall]
    random.shuffle(opts)
    pb = make_part("(b)", "Describe the seasonal pattern and the trend.", right, options=opts, worked_solution=[right],
                   distractors=[{"value": wrong_trend, "mistake": "look at the moving averages, not the last quarter."},
                                {"value": no_season, "mistake": "the same quarter is high every year — that is "
                                                                "seasonality."},
                                {"value": fall, "mistake": "that's the seasonal pattern, not the trend — compare with the "
                                                           "same quarter a year earlier."}])
    ylabel = s["what"].split(" by ")[0].split(" to ")[0].split(" on ")[0]
    md = _diagram("app_time_series", labels, vals, "quarter", ylabel, "Quarterly figures", None, width=560)
    data = "; ".join(f"{y0 + y}: " + ", ".join(_g(v, 2) for v in vals[4 * y:4 * y + 4]) for y in range(years))
    return Question(question_text=f"The {s['what']} each quarter (Q1 = January–March) were: {data}.",
                    correct_answer=ans, topic=TOPIC, question_type=QTYPE, parts=[pa, pb],
                    worked_solution=multipart_worked_solution([pa, pb]), notes=_EX_TREND, metadata=md)


def generate_correlation_regression_question(calc_mode=False):
    return random.choice([generate_correlation_regression_l1, generate_correlation_regression_l2,
                          generate_correlation_regression_l3, generate_correlation_regression_l4,
                          generate_correlation_regression_l5, generate_correlation_regression_l6])()
