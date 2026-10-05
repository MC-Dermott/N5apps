"""Higher Applications of Maths — Hypothesis Testing (unit "Statistics").

Mirrors Hypothesis_Testing_Worksheet.docx (Higher Apps/Worksheets/Statistics): research questions and choosing a
test (two-sample t-test, paired t-test, z-test for two proportions), null and alternative hypotheses in context,
interpreting p-values and stating conclusions, performing a test (the test statistic from summary statistics),
confidence intervals, and errors in testing (type I/II, confounding, a worthwhile difference). The exam's tests are
done with R or Excel on .csv data, not in a spreadsheet grid, so the levels follow the worksheet's sections.

Distractors are the errors in the course reports and marking instructions: 't-test' for two proportions and 'the
sample size must be the same' (2022 Q3(c)(d)); 'paired t-test' for two separate groups (2025 Q9(b)(i), 2024 Q6
Candidate A); hypotheses not about the MEAN, or 'average' (2025 Q9(b)(ii), 2026 Q7(a)(ii)); 0.5 or 0.005 instead of
0.05, and no conclusion in context (2025 Q9(b)(iii), 2024 Q6(c)(iii)); 'accept the null hypothesis' and 'there is
no difference' (2022 course report, 2024 marking instructions). Statistics in pure Python (no scipy): the t tail by
the regularized incomplete beta function, the normal by math.erf.
"""
import math
import random

from core.models.distractors import distractors
from core.models.question_model import Question

TOPIC, QTYPE = "Statistics", "Hypothesis Testing"
_DIAG = "topics.statistics.hypothesis_testing_diagrams"


def _g(x, dp=3):
    x = round(x + 0.0, dp)
    s = f"{x:,.{dp}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def _r(x, dp=3):
    return round(x + 0.0, dp)


def _diagram(kind, *args, width=460):
    return {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DIAG, "kind": kind, "args": list(args), "width": width}}


def _options(question_text, right, wrong, notes, solution):
    """An options question: the right answer plus [(wrong option, mistake)], shuffled."""
    opts = [right] + [w for w, _ in wrong]
    random.shuffle(opts)
    return Question(question_text=question_text, correct_answer=right, topic=TOPIC, question_type=QTYPE,
                    worked_solution=solution, notes=notes, metadata={"options": opts},
                    distractors=[{"value": w, "mistake": m} for w, m in wrong])


# ── pure-Python distributions ───────────────────────────────────────────────────────────────────
def _betacf(a, b, x):
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 1000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c; c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c; c = c if abs(c) > tiny else tiny
        de = d * c; h *= de
        if abs(de - 1) < 1e-15:
            break
    return h


def _betainc(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbt = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lbt) * _betacf(a, b, x) / a
    return 1 - math.exp(lbt) * _betacf(b, a, 1 - x) / b


def t_two_tail(t, df):
    """P(|T| ≥ |t|) for Student's t (df may be non-integer, as in R's Welch test)."""
    return _betainc(df / 2, 0.5, df / (df + t * t))


def norm_two_tail(z):
    return math.erfc(abs(z) / math.sqrt(2))


def _p_text(p):
    """A p-value as R prints it (4 significant figures, e-notation when small)."""
    s = f"{p:.4g}"
    if "e" in s:
        mant, ex = s.split("e")
        s = f"{mant}e-{abs(int(ex)):02d}"
    return s


# ── scenarios ───────────────────────────────────────────────────────────────────────────────────
# kind: two (two-sample t-test), paired, prop (z-test for two proportions)
_SCEN = [
    dict(kind="two", study="A crofter weighs a random sample of lambs raised on feed A and a separate random sample "
                           "raised on feed B, at 8 weeks old.",
         core="the mean mass of lambs raised on feed A and lambs raised on feed B",
         effect="the type of feed does not affect the lambs", unit="kg", m=(24.5, 2.4)),
    dict(kind="two", study="A community energy scheme on North Uist tests a random sample of Type A solar panels and "
                           "a random sample of Type B panels, recording each panel's daily output.",
         core="the mean daily output of Type A and Type B solar panels",
         effect="the type of panel does not affect the output", unit="kWh", m=(14.0, 1.8)),
    dict(kind="two", study="A sports scientist compares the distance a shinty ball travels when hit with a carbon stick "
                           "and with a wooden stick, using a random sample of hits with each.",
         core="the mean distance travelled by the ball hit with a carbon stick and with a wooden stick",
         effect="the stick does not affect the distance", unit="m", m=(62.0, 6.5)),
    dict(kind="two", study="A PE teacher times a random sample of S2 pupils and a random sample of S5 pupils running "
                           "1500 metres.",
         core="the mean time taken to run 1500 metres between S2 pupils and S5 pupils",
         effect="age does not affect running", unit="s", m=(410.0, 35.0)),
    dict(kind="paired", study="The resting heart rate of a group of runners is measured before and after a six-week "
                              "running programme.",
         core="the mean resting heart rate of the runners before and after the programme",
         effect="the programme does not affect the runners", unit="bpm", m=(4.0, 4.5)),
    dict(kind="paired", study="Swimmers at the Stornoway pool record their 400 m time before and after a block of "
                              "coaching.",
         core="the mean 400 m time of the swimmers before and after the coaching",
         effect="coaching does not affect the swimmers", unit="s", m=(6.0, 7.0)),
    dict(kind="paired", study="The blood pressure of a group of patients is measured before and after they take a new "
                              "medicine for four weeks.",
         core="the mean blood pressure of the patients before and after taking the medicine",
         effect="the medicine does not affect the patients", unit="mmHg", m=(5.0, 8.0)),
    dict(kind="prop", study="Random samples of pupils at a school in Stornoway and a school in Castlebay are asked "
                            "whether they walk to school.",
         core="the proportion of pupils who walk to school in Stornoway and in Castlebay",
         effect="where pupils live does not affect walking", p=(0.35, 0.45)),
    dict(kind="prop", study="A council surveys random samples of households in Lewis and in Skye to find out whether "
                            "they have a heat pump.",
         core="the proportion of households with a heat pump in Lewis and in Skye",
         effect="the island does not affect heat pumps", p=(0.25, 0.32)),
    dict(kind="prop", study="Random samples of sailings from Ullapool and from Oban are checked to see whether they "
                            "were delayed.",
         core="the proportion of sailings delayed from Ullapool and from Oban",
         effect="the port does not affect delays", p=(0.15, 0.22)),
]
_TEST = {"two": "Two-sample t-test", "paired": "Paired t-test", "prop": "z-test for two proportions"}
_REASON = {"two": "two separate (independent) groups of numerical data",
           "paired": "the same individuals are measured twice, so the data are paired",
           "prop": "the data are categorical — counts out of totals — so we compare two proportions"}
_REL = ["A tourist office records the hours of sunshine and the number of visitors to Luskentyre beach on 30 days.",
        "A coach records the back squat weight and the vertical jump height of 20 athletes.",
        "A garage records the tread depth and the stopping distance of 25 tyres."]

# ── notes: the worksheet's worked examples and their ⚠ errors ──────────────────────────────────────
NOTES_TEST = """
**Choosing a test (worksheet, Section 1).** Research questions take one of three forms: *I am going to
investigate if there is a difference in means between… / a relationship between… / a difference between two
proportions…*

| Research question | Data | Analysis (R) |
|---|---|---|
| difference in means — two separate groups | numerical | two-sample t-test `t.test(X, Y)` |
| difference in means — same individuals twice | numerical, paired | paired t-test `t.test(X, Y, paired = TRUE)` |
| difference between two proportions | categorical (counts) | z-test for two proportions `prop.test(…)` |
| relationship between two variables | numerical pairs | correlation and regression `cor.test`, `lm` |

**Example.** Shell lengths of 40 mussels from Loch Roag and 40 from Loch Erisort → two-sample t-test. Twelve divers'
breath-hold times before and after a course → paired t-test. 27 of 180 sailings from Ullapool delayed, 33 of 150
from Oban → z-test for two proportions. Assumptions: random (independent) samples; for a t-test, data
approximately normal. The samples do NOT need to be the same size.

⚠ 2022 Q3(c): many answered 't-test' for two proportions. 2022 Q3(d): 'the sample size must be the same' scored 0.
2025 Q9(b)(i): 'paired t-test' was not accepted for two separate groups.
"""
NOTES_HYP = """
**Hypotheses (worksheet, Section 2).** *'Is there a significant difference in the mean time taken to swim 50
metres between S2 pupils and S4 pupils?'*

- **Null hypothesis:** there is no difference in the mean time taken to swim 50 metres between S2 pupils and S4 pupils.
- **Alternative hypothesis:** there is a difference in the mean time taken to swim 50 metres between S2 pupils and
  S4 pupils.

For two proportions: *there is no difference in the proportion of … between … and …*.

⚠ 2025 Q9(b)(ii): most scored 0 — not about the difference in the MEAN mass, or not in context. 2026 Q7(a)(ii):
'average' not accepted for 'mean'; both groups must be named.
"""
NOTES_P = """
**Interpreting a p-value (worksheet, Section 3).** The p-value is the probability of getting data as extreme as
those observed if the null hypothesis were true. Compare it with **0.05**.

**Example.** Lambs on two feeds, p = 0.0213: *since 0.0213 < 0.05, reject the null hypothesis. There is evidence
that suggests there is a significant difference in the mean mass of lambs raised on the two feeds.*
A second study, p = 0.072: *since 0.072 > 0.05, fail to reject the null hypothesis. There is insufficient evidence to
suggest a significant difference in the mean mass of lambs raised on the two feeds.*
`3.215e-05` means 0.00003215.

⚠ 2025 Q9(b)(iii): 0.5 or 0.005 used instead of 0.05; most didn't state a significant difference in the MEAN mass.
2024 Q6(c)(iii): 'there is no difference in the distances' lost the second mark (too definite). Say 'fail to
reject', not 'accept' (2022 course report).
"""
NOTES_CALC = """
**Performing a test (worksheet, Section 4).** R: `t.test(X, Y)` (Welch two-sample), `t.test(X, Y, paired = TRUE)`,
`prop.test(x = c(a, b), n = c(n1, n2))`. Excel: `T.TEST(range1, range2, 2, 3)` (two-sample), type 1 for paired.

- two-sample: t = (x̄₁ − x̄₂) ÷ √(s₁²/n₁ + s₂²/n₂)
- paired: t = d̄ ÷ (s_d ÷ √n)
- two proportions: z = (p̂₁ − p̂₂) ÷ √(p̂(1 − p̂)(1/n₁ + 1/n₂)), with pooled p̂ = (a + b) ÷ (n₁ + n₂)

**Example.** Solar panels, 12 of each type: Type A mean 14.84167, sd 1.27953; Type B mean 12.86667, sd 2.30072.
t = 1.9750 ÷ √(1.27953²/12 + 2.30072²/12) = 1.9750 ÷ 0.7600 = **2.599**; R: t = 2.5988, df = 17.21,
p-value = 0.0186 < 0.05 → a significant difference in the mean daily output.

⚠ 2024 Q6(c)(ii): two-sample p = 0.188; Candidate A ran a paired t-test (0.2092), Candidate B a correlation
test (0.6118). The p-value must come from the test you stated.
"""
NOTES_CI = """
**Confidence intervals (worksheet, Section 5).** A 95% confidence interval is a range of uncertainty for an
estimate. Wider = more uncertainty; larger samples give narrower intervals. For a DIFFERENCE: contains 0 → no
significant difference; doesn't contain 0 → significant difference.

**Example.** Solar panels: 95% CI 0.373 to 3.577 kWh (Type A − Type B). It doesn't contain 0, so there is a
significant difference in mean output (agrees with p = 0.0186); Type A is higher, by between about 0.37 and 3.58 kWh.
If the study were repeated 100 times, 95 of these times the estimated difference in the population mean output would
lie within the interval.

⚠ A 95% interval is about the population mean, not where 95% of the data lie (course specification); an interval
containing 0 doesn't PROVE there is no difference (2024 Q6(c)(iii): conclusions not too definite).
"""
NOTES_ERR = """
**Errors and confounding (worksheet, Section 6).** Type I: rejecting the null hypothesis when it is true. Type II:
failing to reject the null hypothesis when it is false. At the 5% level, if H₀ is true there is a 5% chance of a
type I error.

**Example.** Urban clinic 26 of 198 dogs need flea treatment (July–September); rural clinic 41 of 162
(October–December); p = 0.004843. The data come from different seasons, so season is confounded with area — the
difference may be due to the time of year. A type I error would be concluding there's a difference between urban and
rural areas when there isn't. A type II error is impossible here: the null hypothesis was rejected.

⚠ 2022 Q3(e): compare the two clinics' time periods. 2022 Q7(d): correlation is not causation.
"""


# ── Level 1: research questions and choosing a test ─────────────────────────────────────────────
def generate_hypothesis_testing_l1(calc_mode=False):
    v = random.choice(["test", "test", "test", "design", "form"])
    if v == "design":
        sc = random.choice([s for s in _SCEN if s["kind"] == "prop"])
        right = "The samples must be chosen randomly (and independently)."
        wrong = [("The sample sizes must be the same.", "equal sample sizes are not needed — this scored 0 in the 2022 "
                                                        "marking instructions (Q3(d))."),
                 ("The data must be numerical.", "this study compares proportions — categorical data."),
                 ("The two proportions must be equal.", "that's the null hypothesis, not a design condition.")]
        return _options(f"{sc['study']} A z-test for two proportions will be used. State one part of the design of the "
                        f"study that is needed for the test to be valid.", right, wrong, NOTES_TEST,
                        [right, "Not 'the sample size must be the same' (2022 Q3(d))."])
    if v == "form":
        if random.random() < 0.5:
            study = random.choice(_REL)
            right = "…if there is a relationship between… — correlation and regression"
        else:
            sc = random.choice(_SCEN); study = sc["study"]
            right = ("…if there is a difference between two proportions… — z-test for two proportions" if sc["kind"] == "prop"
                     else f"…if there is a difference in means between… — {_TEST[sc['kind']].lower()}")
        all_opts = ["…if there is a relationship between… — correlation and regression",
                    "…if there is a difference between two proportions… — z-test for two proportions",
                    "…if there is a difference in means between… — two-sample t-test",
                    "…if there is a difference in means between… — paired t-test"]
        wrong = [(o, "match the research question to the data: relationship → correlation/regression; difference in "
                     "means → t-test (paired if the same individuals); proportions → z-test.") for o in all_opts
                 if o != right]
        return _options(f"{study} Which form of research question, and which analysis, fits this study?", right, wrong,
                        NOTES_TEST, [right])
    sc = random.choice(_SCEN)
    right = _TEST[sc["kind"]]
    mistakes = {"Two-sample t-test": "two-sample t-test is for the MEANS of two separate groups.",
                "Paired t-test": "a paired t-test needs the same individuals measured twice — 'paired t-test' was not "
                                 "accepted for two separate groups in 2025 (Q9(b)(i)).",
                "z-test for two proportions": "a z-test compares PROPORTIONS (counts out of totals), not means.",
                "Correlation test": "a correlation test looks for a relationship — 2024 Q6 Candidate B lost marks for "
                                    "it."}
    if sc["kind"] == "prop":
        mistakes["Two-sample t-test"] = ("these are proportions, not means — 'many candidates answered t-test' (2022 "
                                         "course report, Q3(c)).")
    wrong = [(o, m) for o, m in mistakes.items() if o != right]
    return _options(f"{sc['study']} State an appropriate hypothesis test.", right, wrong, NOTES_TEST,
                    [f"**{right}** — {_REASON[sc['kind']]}."])


# ── Level 2: hypotheses ─────────────────────────────────────────────────────────────────────────
def generate_hypothesis_testing_l2(calc_mode=False):
    sc = random.choice(_SCEN)
    core = sc["core"]
    right = f"H₀: there is no difference in {core}. H₁: there is a difference in {core}."
    avg = core.replace("the mean", "the average")
    wrong = [(f"H₀: {sc['effect']}. H₁: {sc['effect'].replace('does not affect', 'affects')}.",
              "not about the difference in the MEAN (or proportion) — most candidates scored 0 for this in 2025 "
              "(Q9(b)(ii))."),
             (f"H₀: there is a difference in {core}. H₁: there is no difference in {core}.",
              "the wrong way round: the null hypothesis is 'no difference'.")]
    if avg != core:
        wrong.append((f"H₀: there is no difference in {avg}. H₁: there is a difference in {avg}.",
                      "'average' is not accepted in place of 'mean' (2026 marking instructions, Q7(a)(ii))."))
    else:
        wrong.append(("H₀: there is no difference in the proportions. H₁: there is a difference in the proportions.",
                      "not in context — name what is being compared and both groups (2025 course report)."))
    return _options(f"{sc['study']} A {_TEST[sc['kind']].lower()} is performed. Which "
                    f"are appropriate null and alternative hypotheses?", right, wrong, NOTES_HYP,
                    [f"Null hypothesis: there is no difference in {core}.",
                     f"Alternative hypothesis: there is a difference in {core}."])


# ── Level 3: p-values and conclusions ───────────────────────────────────────────────────────────
_PVALS = [0.0004, 0.0021, 0.0094, 0.0213, 0.031, 0.0317, 0.0432, 0.0498, 3.215e-05, 7.48e-11,
          0.0517, 0.072, 0.188, 0.2092, 0.3469, 0.3812, 0.62, 0.0802]


def generate_hypothesis_testing_l3(calc_mode=False):
    sc = random.choice(_SCEN)
    p = random.choice(_PVALS)
    ptxt = _p_text(p)
    core = sc["core"]
    sig = p < 0.05
    if sig:
        right = (f"Since the p-value ({ptxt}) < 0.05, reject the null hypothesis: there is evidence of a significant "
                 f"difference in {core}.")
        wrong = [(f"Since the p-value ({ptxt}) < 0.05, reject the null hypothesis.",
                  "no conclusion in context — state whether there is a significant difference in the mean (or "
                  "proportion), naming the groups (2024 course report, Q6(c)(iii); 2025 Q9(b)(iii))."),
                 (f"Since the p-value ({ptxt}) < 0.05, fail to reject the null hypothesis: there is insufficient "
                  f"evidence of a significant difference in {core}.",
                  "a p-value below 0.05 means REJECT the null hypothesis."),
                 (f"Since the p-value ({ptxt}) < 0.005, reject the null hypothesis: there is a significant difference "
                  f"in {core}." if p < 0.005 else
                  f"Since the p-value ({ptxt}) > 0.005, fail to reject the null hypothesis: there is no significant "
                  f"difference in {core}.",
                  "the significance level is 0.05 (5%), not 0.005 — a value candidates used in 2025 (course report, "
                  "Q9(b)(iii)).")]
    else:
        right = (f"Since the p-value ({ptxt}) > 0.05, fail to reject the null hypothesis: there is insufficient evidence "
                 f"of a significant difference in {core}.")
        wrong = [(f"Since the p-value ({ptxt}) > 0.05, accept the null hypothesis: there is no difference in {core}.",
                  "say 'fail to reject', not 'accept' (2022 course report), and 'there is no difference' is too "
                  "definite — it lost the second mark in 2024 (Q6(c)(iii))."),
                 (f"Since the p-value ({ptxt}) > 0.05, reject the null hypothesis: there is a significant difference "
                  f"in {core}.", "a p-value above 0.05 means FAIL TO REJECT the null hypothesis."),
                 (f"Since the p-value ({ptxt}) < 0.5, reject the null hypothesis: there is a significant difference in "
                  f"{core}." if p < 0.5 else
                  f"Since the p-value ({ptxt}) > 0.05, fail to reject the null hypothesis.",
                  "compare with 0.05, not 0.5 (2025 course report, Q9(b)(iii))." if p < 0.5 else
                  "no conclusion in context (2024 course report, Q6(c)(iii)).")]
    extra = f" = {p:.{3 - math.floor(math.log10(p))}f}" if "e" in ptxt else ""
    return _options(f"{sc['study']} A {_TEST[sc['kind']].lower()} gives  p-value = {ptxt}. Which interprets the "
                    f"p-value, and the result of the test, in context?", right, wrong, NOTES_P,
                    [f"p-value = {ptxt}{extra}; compare with 0.05.", right])


# ── Level 4: confidence intervals ───────────────────────────────────────────────────────────────
def generate_hypothesis_testing_l4(calc_mode=False):
    v = random.choice(["diff", "diff", "claim", "width", "meaning"])
    if v == "diff":
        sc = random.choice([s for s in _SCEN if s["kind"] != "prop"])
        unit = sc["unit"]; s0 = sc["m"][1]
        mid = _r(random.uniform(-1.4, 1.4) * s0, 2); half = _r(random.uniform(0.35, 1.0) * s0, 2)
        lo, hi = _r(mid - half, 2), _r(mid + half, 2)
        if abs(lo) < 0.01 or abs(hi) < 0.01:
            lo, hi = _r(lo - 0.05, 2), _r(hi - 0.05, 2)
        contains = lo < 0 < hi
        if contains:
            right = (f"It contains 0, so there is no significant difference in {sc['core']} at the 5% level.")
            wrong = [(f"It contains 0, so it proves there is no difference in {sc['core']}.",
                      "an interval containing 0 shows no SIGNIFICANT difference — it doesn't prove there is none "
                      "(2024 Q6(c)(iii): conclusions not too definite)."),
                     (f"It doesn't contain 0, so there is a significant difference in {sc['core']}.",
                      f"check the ends: {_g(lo, 2)} is negative and {_g(hi, 2)} is positive, so 0 is inside."),
                     ("95% of the measurements lie inside the interval, so there is no difference.",
                      "the interval is about the population mean difference, not where the data lie (course "
                      "specification).")]
        else:
            right = f"It doesn't contain 0, so there is a significant difference in {sc['core']} at the 5% level."
            wrong = [(f"It contains 0, so there is no significant difference in {sc['core']}.",
                      f"both ends ({_g(lo, 2)} and {_g(hi, 2)}) have the same sign, so 0 is not inside."),
                     ("95% of the measurements lie inside the interval, so there is a significant difference.",
                      "the interval is about the population mean difference, not where the data lie (course "
                      "specification)."),
                     (f"The interval is wide, so there is no significant difference in {sc['core']}.",
                      "the width shows the uncertainty; significance depends on whether 0 is inside.")]
        q = _options(f"{sc['study']} The 95% confidence interval for the difference in means is {_g(lo, 2)} {unit} to "
                     f"{_g(hi, 2)} {unit}. What does it tell you?", right, wrong, NOTES_CI,
                     [f"0 is {'inside' if contains else 'outside'} {_g(lo, 2)} to {_g(hi, 2)}.", right])
        q.metadata.update(_diagram("ci_plot", [[lo, hi]], ["difference"], f"difference in means ({unit})"))
        return q
    if v == "claim":
        m = random.choice([31.4, 32.2, 24.6, 14.1, 62.3])
        half = random.choice([1.2, 1.3, 0.9, 1.6])
        lo, hi = _r(m - half, 2), _r(m + half, 2)
        claim = _r(random.choice([m + half + random.choice([0.4, 0.8, 1.5]), m - half - random.choice([0.3, 0.7]),
                                  m + random.choice([-0.5, 0.3, 0.6])]), 1)
        inside = lo <= claim <= hi
        right = (f"{_g(claim, 1)} is inside the interval, so the claim is plausible." if inside else
                 f"{_g(claim, 1)} is outside the interval, so the sample does not support the claim.")
        wrong = [((f"{_g(claim, 1)} is outside the interval, so the sample does not support the claim." if inside else
                   f"{_g(claim, 1)} is inside the interval, so the claim is plausible."),
                  f"compare {_g(claim, 1)} with the ends {_g(lo, 2)} and {_g(hi, 2)}."),
                 ("95% of the sample values lie in the interval, so the claim is correct.",
                  "the interval is a range for the population MEAN, not where the data lie (course specification)."),
                 ("The claim is proved correct by the interval.", "a confidence interval can't prove a claim.")]
        return _options(f"From a random sample, t.test gives a 95% confidence interval for the mean of {_g(lo, 2)} to "
                        f"{_g(hi, 2)}. A report claims the mean is {_g(claim, 1)}. Comment on the claim.", right, wrong,
                        NOTES_CI, [right])
    if v == "width":
        n1, n2 = random.choice([(20, 80), (15, 60), (25, 100)])
        c = random.choice([250, 64, 410]); w1 = random.choice([18, 20, 24]) * c / 250; w2 = w1 / 2
        order = random.random() < 0.5
        a = (n1, _r(c - w1 * 0.9, 1), _r(c + w1 * 1.1, 1)); b = (n2, _r(c - w2, 1), _r(c + w2, 1))
        s1, s2 = (a, b) if order else (b, a)
        right = f"The sample of {n1} — its interval is wider, because it has a smaller sample."
        wrong = [(f"The sample of {n2} — its interval is narrower, so it is more uncertain.",
                  "a NARROWER interval means LESS uncertainty (course specification)."),
                 (f"The sample of {n2} — a larger sample is always more uncertain.",
                  "larger samples give narrower intervals and less uncertainty."),
                 ("Both are equally uncertain — they are both 95% intervals.",
                  "the confidence level is the same, but the widths show different uncertainty.")]
        return _options(f"Two studies estimate the same mean. A random sample of {s1[0]} gives a 95% confidence interval "
                        f"{_g(s1[1], 1)} to {_g(s1[2], 1)}; a random sample of {s2[0]} gives {_g(s2[1], 1)} to {_g(s2[2], 1)}. "
                        f"Which estimate is more uncertain?", right, wrong, NOTES_CI, [right])
    right = ("If the study were repeated 100 times, 95 of these times the estimated population mean would lie within the "
             "interval.")
    wrong = [("95% of the data values lie within the interval.",
              "the interval is about the population mean, not the data (course specification)."),
             ("There is a 95% chance that the sample mean is wrong.", "that isn't what the confidence level means."),
             ("The population mean is exactly in the middle of the interval.",
              "the SAMPLE mean is in the middle; the population mean is uncertain.")]
    return _options("A study gives a 95% confidence interval for a mean. Which is the literal interpretation of a 95% "
                    "confidence interval given in the course specification?", right, wrong, NOTES_CI, [right])


# ── Level 5: calculating a test from data ───────────────────────────────────────────────────────
def _q_welch():
    sc = random.choice([s for s in _SCEN if s["kind"] == "two"])
    mu, s0 = sc["m"]
    n1, n2 = random.randint(10, 40), random.randint(10, 40)
    m1 = _r(mu + random.uniform(-0.6, 0.6) * s0, 2); m2 = _r(m1 + random.choice([-1, 1]) * random.uniform(0.15, 1.2) * s0, 2)
    s1 = _r(s0 * random.uniform(0.7, 1.3), 2); s2 = _r(s0 * random.uniform(0.7, 1.3), 2)
    se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    t = _r((m1 - m2) / se)
    df = (s1 ** 2 / n1 + s2 ** 2 / n2) ** 2 / ((s1 ** 2 / n1) ** 2 / (n1 - 1) + (s2 ** 2 / n2) ** 2 / (n2 - 1))
    p = t_two_tail((m1 - m2) / se, df)
    unit = sc["unit"]
    text = (f"{sc['study']}\n\nGroup 1: n = {n1}, mean = {_g(m1, 2)} {unit}, standard deviation = {_g(s1, 2)} {unit}.  \n"
            f"Group 2: n = {n2}, mean = {_g(m2, 2)} {unit}, standard deviation = {_g(s2, 2)} {unit}.\n\n"
            f"Calculate the two-sample test statistic t = (x̄₁ − x̄₂) ÷ √(s₁²/n₁ + s₂²/n₂), to 3 decimal places.")
    return Question(
        question_text=text, correct_answer=t, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "x̄₁ − x̄₂", "answer": _r(m1 - m2, 2)},
                        {"prompt": "Standard error √(s₁²/n₁ + s₂²/n₂), to 4 d.p.", "answer": _r(se, 4)},
                        {"prompt": "t, to 3 d.p.", "answer": t}],
        worked_solution=[f"x̄₁ − x̄₂ = {_g(m1, 2)} − {_g(m2, 2)} = {_g(m1 - m2, 2)}",
                         f"SE = √({_g(s1, 2)}²/{n1} + {_g(s2, 2)}²/{n2}) = {_g(se, 4)}",
                         f"t = {_g(m1 - m2, 2)} ÷ {_g(se, 4)} = **{_g(t)}**",
                         f"R's t.test (Welch) would give df = {_g(df, 2)}, p-value = {_p_text(p)} — "
                         f"{'less' if p < 0.05 else 'more'} than 0.05, so {'a' if p < 0.05 else 'no'} significant "
                         f"difference in {sc['core']}."],
        notes=NOTES_CALC,
        distractors=distractors(t, [(_r((m1 - m2) / math.sqrt(s1 / n1 + s2 / n2)), "square the standard deviations: "
                                                                                    "s², not s."),
                                    (_r((m1 - m2) / (s1 ** 2 / n1 + s2 ** 2 / n2)), "take the square root of the "
                                                                                    "bottom line."),
                                    (_r((m1 - m2) / math.sqrt(s1 ** 2 + s2 ** 2)), "divide each variance by its "
                                                                                    "sample size."),
                                    (_r(-t), "subtract in the order given: group 1 − group 2.")]))


def _q_paired():
    sc = random.choice([s for s in _SCEN if s["kind"] == "paired"])
    mu, s0 = sc["m"]
    n = random.randint(8, 25)
    d = _r(mu * random.uniform(0.5, 1.5), 2); sd = _r(s0 * random.uniform(0.7, 1.3), 2)
    se = sd / math.sqrt(n); t = _r(d / se)
    p = t_two_tail(d / se, n - 1)
    unit = sc["unit"]
    text = (f"{sc['study']}\n\nFor the n = {n} differences (before − after): mean difference d̄ = {_g(d, 2)} {unit}, "
            f"standard deviation of the differences s_d = {_g(sd, 2)} {unit}.\n\n"
            f"Calculate the paired test statistic t = d̄ ÷ (s_d ÷ √n), to 3 decimal places.")
    return Question(
        question_text=text, correct_answer=t, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "Standard error s_d ÷ √n, to 4 d.p.", "answer": _r(se, 4)},
                        {"prompt": "t, to 3 d.p.", "answer": t}],
        worked_solution=[f"SE = {_g(sd, 2)} ÷ √{n} = {_g(se, 4)}", f"t = {_g(d, 2)} ÷ {_g(se, 4)} = **{_g(t)}**",
                         f"df = {n - 1}; p-value = {_p_text(p)} → {'reject' if p < 0.05 else 'fail to reject'} the "
                         f"null hypothesis."],
        notes=NOTES_CALC,
        distractors=distractors(t, [(_r(d / (sd / n)), "divide s_d by √n, not by n."),
                                    (_r(d / sd), "divide s_d by √n first — the standard error."),
                                    (_r(d * math.sqrt(n) * sd), "t = d̄ ÷ (s_d ÷ √n).")]))


def _q_ztest():
    sc = random.choice([s for s in _SCEN if s["kind"] == "prop"])
    lo, hi = sc["p"]
    n1, n2 = random.randint(60, 260), random.randint(60, 260)
    a = round(n1 * random.uniform(lo - 0.1, hi + 0.1)); b = round(n2 * random.uniform(lo - 0.1, hi + 0.1))
    if a * n2 == b * n1:
        b += 1
    p1, p2 = a / n1, b / n2; pool = (a + b) / (n1 + n2)
    se = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2)); z = _r((p1 - p2) / se)
    pv = norm_two_tail((p1 - p2) / se)
    text = (f"{sc['study']}\n\nGroup 1: {a} out of {n1}.  Group 2: {b} out of {n2}.\n\n"
            f"Calculate z = (p̂₁ − p̂₂) ÷ √(p̂(1 − p̂)(1/n₁ + 1/n₂)), where p̂ = (a + b) ÷ (n₁ + n₂) is the pooled "
            f"proportion, to 3 decimal places.")
    unpooled = (p1 - p2) / math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return Question(
        question_text=text, correct_answer=z, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "p̂₁, to 4 d.p.", "answer": _r(p1, 4)}, {"prompt": "p̂₂, to 4 d.p.", "answer": _r(p2, 4)},
                        {"prompt": "Pooled proportion p̂, to 4 d.p.", "answer": _r(pool, 4)},
                        {"prompt": "Standard error, to 4 d.p.", "answer": _r(se, 4)},
                        {"prompt": "z, to 3 d.p.", "answer": z}],
        worked_solution=[f"p̂₁ = {a} ÷ {n1} = {_g(p1, 4)}; p̂₂ = {b} ÷ {n2} = {_g(p2, 4)}",
                         f"p̂ = {a + b} ÷ {n1 + n2} = {_g(pool, 4)}",
                         f"SE = √({_g(pool, 4)} × {_g(1 - pool, 4)} × (1/{n1} + 1/{n2})) = {_g(se, 4)}",
                         f"z = {_g(p1 - p2, 4)} ÷ {_g(se, 4)} = **{_g(z)}**",
                         f"Two-tailed p-value = {_p_text(pv)} (R's prop.test applies a continuity correction, so its "
                         f"p-value is a little larger)."],
        notes=NOTES_CALC,
        distractors=distractors(z, [(_r(unpooled), "use the POOLED proportion in the standard error."),
                                    (_r(-z), "subtract in the order given: group 1 − group 2."),
                                    (_r((p1 - p2) / (pool * (1 - pool) * (1 / n1 + 1 / n2))),
                                     "take the square root for the standard error.")]))


def generate_hypothesis_testing_l5(calc_mode=False):
    return random.choice([_q_welch, _q_welch, _q_paired, _q_ztest])()


# ── Level 6: errors and confounding ─────────────────────────────────────────────────────────────
def generate_hypothesis_testing_l6(calc_mode=False):
    v = random.choice(["which", "describe", "confound", "worth"])
    sc = random.choice(_SCEN); core = sc["core"]
    if v == "which":
        p = random.choice(_PVALS); ptxt = _p_text(p)
        right = ("Type I — the null hypothesis was rejected, so the error would be rejecting a true null hypothesis."
                 if p < 0.05 else
                 "Type II — the null hypothesis was not rejected, so the error would be failing to reject a false null "
                 "hypothesis.")
        other = ("Type II — the null hypothesis was rejected, so the error would be failing to reject a false null "
                 "hypothesis." if p < 0.05 else
                 "Type I — the null hypothesis was not rejected, so the error would be rejecting a true null hypothesis.")
        wrong = [(other, "type I = rejecting a true H₀; type II = failing to reject a false H₀ — check what the test "
                         "decided."),
                 ("Neither — with a p-value we can't make an error.", "any test can lead to a wrong conclusion."),
                 ("Both types of error could have been made.", "only one decision was made, so only one type of error "
                                                               "is possible.")]
        return _options(f"{sc['study']} The test gives p-value = {ptxt}. Which type of error could have been made?",
                        right, wrong, NOTES_ERR, [f"p = {ptxt} {'<' if p < 0.05 else '>'} 0.05.", right])
    if v == "describe":
        t1 = random.random() < 0.5
        right = (f"Concluding there is a difference in {core} when there really is none." if t1 else
                 f"Concluding there is insufficient evidence of a difference in {core} when there really is a "
                 f"difference.")
        wrong = [((f"Concluding there is insufficient evidence of a difference in {core} when there really is a "
                   f"difference.") if t1 else f"Concluding there is a difference in {core} when there really is none.",
                  "type I: rejecting a TRUE null hypothesis; type II: failing to reject a FALSE one."),
                 ("Using the wrong test.", "that's a mistake in the method, not a type I or II error."),
                 ("Collecting the data in different months.", "that's a confounding variable, not a type I/II error.")]
        return _options(f"{sc['study']} Describe a type {'I' if t1 else 'II'} error in this context.", right, wrong,
                        NOTES_ERR, [right])
    if v == "confound":
        g = random.choice([("an urban clinic", "a rural clinic", "dogs needing flea treatment", "July to September",
                            "October to December"),
                           ("Uig", "Tarbert", "sailings delayed", "January to March", "June to August"),
                           ("a school in Stornoway", "a school in Castlebay", "pupils who walk to school", "May", "December")])
        right = (f"The data were collected at different times of year, so the season is confounded with the place: the "
                 f"difference may be caused by the time of year, not by {g[0]} versus {g[1]}.")
        wrong = [("The sample sizes are different, so the test can't be used.",
                  "equal sample sizes are not needed (2022 marking instructions, Q3(d))."),
                 ("It makes no difference — a z-test allows for the time of year.",
                  "the test can't separate the place from the season (2022 Q3(e))."),
                 ("The data become numerical, so a t-test is needed.", "the data are still counts out of totals.")]
        return _options(f"A study compares the proportion of {g[2]} at {g[0]} (data collected {g[3]}) and {g[1]} (data "
                        f"collected {g[4]}). Explain how this may affect the conclusions.", right, wrong, NOTES_ERR,
                        [right, "2022 Q3(e): compare the two time periods."])
    big = random.random() < 0.5
    if big:
        text = ("A two-sample t-test finds a significant difference of £8.40 in the mean cost of the same weekly shop at "
                "two supermarkets. Is the difference worthwhile?")
        right = "Yes — over a year that is more than £400 for a family, so it matters to shoppers."
        wrong = [("No — every significant difference is too small to matter.", "decide in context: £8.40 a week adds "
                                                                                "up."),
                 ("No — the p-value must be below 0.005 for a difference to be worthwhile.", "the 5% level is 0.05; "
                                                                                             "being worthwhile is a "
                                                                                             "judgement in context."),
                 ("Yes — because the p-value is small, the difference must be large.",
                  "a small p-value shows a significant difference, not a large one.")]
    else:
        text = ("A ferry company's annual fuel bill is £12 million. A t-test shows that changing fuel supplier would "
                "give a significant saving of £40 a year on average. Is the difference worthwhile?")
        right = "No — £40 is negligible compared with £12 million."
        wrong = [("Yes — a significant difference is always worthwhile.", "significant ≠ important: judge it in context "
                                                                          "(course specification)."),
                 ("Yes — because the p-value is small, the saving must be large.",
                  "a small p-value shows a significant difference, not a large one."),
                 ("No — a t-test can't be used for money.", "it can; the question is whether £40 matters.")]
    return _options(text, right, wrong, NOTES_ERR, [right, "Course specification: decide if the difference is "
                                                           "worthwhile in the context of the research."])


def generate_hypothesis_testing_question(calc_mode=False):
    return random.choice([generate_hypothesis_testing_l1, generate_hypothesis_testing_l2,
                          generate_hypothesis_testing_l3, generate_hypothesis_testing_l4,
                          generate_hypothesis_testing_l5, generate_hypothesis_testing_l6])()
