"""Higher Applications of Maths — Probability: Venn and Tree Diagrams.

Mirrors Venn_and_Tree_Diagrams_Worksheet.docx (Higher Apps/Worksheets/Statistics), one level per section:
two-set Venn diagrams, three-set Venn diagrams (2024 Q2, 2025 Q2 style, multipart), combining events from a
Venn diagram, two-way tables, tree diagrams with independent events (2026 Q9(a)) and tree diagrams without
replacement / conditional events. Expected cost and control measures stay in Planning → Risk and Expected
Value. No spreadsheet questions: the papers never ask probability that way.

Distractors are the errors in the course reports and marking instructions: the 'none' group left out of the
total (2024 Q2(b) CR), the overlaps not reduced by the centre (2025 Q2(a) CR, MI Candidate A 15/148; 2024 MI
Candidate A 60/273), dividing by the circles instead of the total in the question (2026 Q4(b), Candidate A
78/120), a ratio instead of a probability (2026 Q4(b) MI), adding two independent probabilities instead of
multiplying (2026 Q9(a)(ii) CR).

`generate_probability_question` is the name question_factory imports — keep it.
"""
import random
from fractions import Fraction

from core.models.distractors import distractors
from core.models.question_model import Question, make_part, multipart_worked_solution

TOPIC, QTYPE = "Statistics", "Probability"
_DIAG = "topics.statistics.venn_tree_diagrams"


def _g(x, dp=4):
    x = round(x + 0.0, dp)
    s = f"{x:.{dp}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def _p(n, d):
    """A probability as the app's answer: a decimal to 4 d.p."""
    return round(n / d + 1e-12, 4)


def _fr(n, d):
    """'78/140 = 39/70 ≈ 0.5571' for worked solutions."""
    f = Fraction(n, d)
    s = f"{n}/{d}"
    if (f.numerator, f.denominator) != (n, d):
        s += f" = {f.numerator}/{f.denominator}"
    return s + f" ≈ {_g(n / d)}"


def _diagram(kind, *args, width=420):
    return {"diagram": "composite_shape",
            "diagram_params": {"module_path": _DIAG, "kind": kind, "args": list(args), "width": width}}


def _dist(answer, cands):
    """distractors() without impossible values (negative, or over 1 for a probability)."""
    ok = [(v, m) for v, m in cands if v is not None and v >= 0 and not (answer <= 1 < v)]
    return distractors(answer, ok)


# ── notes: each level's worked example from the worksheet, with its ⚠ common error ──────────
NOTES_VENN2 = """
**Two-set Venn diagrams** (worksheet Section 1)

Start in the overlap; "only A" = A's total − both; "neither" = grand total − everything in the circles,
written **inside** the rectangle. Probability = number in the region ÷ the **grand total**.

**Example:** 150 visitors: 96 visited Callanish, 71 Lews Castle, 48 both.
Callanish only = 96 − 48 = **48**; Lews Castle only = 71 − 48 = **23**; neither = 150 − 119 = **31**.
P(only one) = (48 + 23) ÷ 150 = **71/150 ≈ 0.473**.

⚠ 2026 Q4(b): dividing by the numbers in the circles (78/120) instead of the 140 in the question; a ratio
(78 : 62) scores nothing. If your diagram adds to more than the total, you haven't subtracted the overlap.
"""

NOTES_VENN3 = """
**Three-set Venn diagrams** (worksheet Section 2) — work from the centre outwards

1. All three in the middle. 2. Each pair region = pair total − centre. 3. Each "only" region = the set's total
− the three numbers already in its circle. 4. The 'none' number inside the rectangle. Then add all eight.

**Example:** 6 use all of pool, gym, climbing wall; 40 pool & gym; 25 gym & climbing; 18 pool & climbing;
95 pool; 88 gym; 50 climbing; 21 none.
Pairs: 34, 19, 12. Pool only = 95 − 6 − 34 − 12 = **43**; gym only = 88 − 6 − 34 − 19 = **29**;
climbing only = 50 − 6 − 19 − 12 = **13**. Total = **177**. P(gym and climbing, not pool) = **19/177 ≈ 0.107**.

⚠ 2025 Q2(a): pair totals put straight into the overlaps (Candidate A → 15/148). 2024 Q2(b): the "no
languages" group left out of the total.
"""

NOTES_COMBINE = """
**Combining events: and, or, not** (worksheet Section 3)

A and B = the overlap (include the centre); A or B = everything in either circle, overlap counted once;
not A = everything outside A, **including none**; exactly one = the "only" regions; at least two = the
overlaps and the centre. Divide by the **grand total**.

**Example:** festival days — Friday only 22, Saturday only 35, Sunday only 18, Fri & Sat 14, Sat & Sun 20,
Fri & Sun 6, all three 10, none 5. Total = 130.
P(Saturday) = 79/130 ≈ 0.608; P(Friday or Sunday) = 90/130 ≈ 0.692; P(not Saturday) = 51/130 ≈ 0.392;
P(at least two days) = 50/130 ≈ 0.385.

⚠ 2024 Q2(b): "some candidates did not include the number … that did not study any language within their
total"; 2025 Q2(b): the total wasn't calculated.
"""

NOTES_TABLE = """
**Two-way (contingency) tables** (worksheet Section 4)

Fill gaps from the row and column totals. P(row and column) = cell ÷ grand total. "Or": row total + column
total − the cell counted twice. "A resident is chosen…" — divide by the residents' total only.

**Example:** Tarbert ferry — residents 46 by car, 18 on foot; visitors 84 by car, 52 on foot (200).
P(visitor on foot) = 52/200 = 0.26; P(resident) = 64/200 = 0.32;
P(resident or on foot) = (64 + 70 − 18)/200 = 116/200 = 0.58.

⚠ The wrong total: 2026 Q4(b) — "did not identify the total number of candidates from the question".
"""

NOTES_TREE = """
**Tree diagrams: independent events** (worksheet Section 5)

Branches from one point add to 1. **Multiply** along a path (and); **add** the end results (or).
P(at least one) = 1 − P(neither). Don't round; check the end results add to 1.

**Example:** weather delay 0.2, breakdown 0.05, independent. Missing branches 0.8 and 0.95.
End results 0.01, 0.19, 0.04, 0.76 (add to 1). P(one or both) = 1 − 0.76 = **0.24**.

⚠ 2026 Q9(a)(ii): many candidates added 0.2 + 0.05 instead of using the tree; others rounded part-way
(2026 MI: "Do not accept any rounding"), and a probability over 1 gains no mark.
"""

NOTES_DEPENDENT = """
**Tree diagrams: without replacement and conditional events** (worksheet Section 6)

Without replacement the second stage changes: one fewer in total, one fewer of the kind already taken.
Conditional: read each second-stage probability for THAT branch.

**Example:** 4 winning tickets out of 10, two drawn without replacement.
P(both win) = 4/10 × 3/9 = 12/90 = 2/15 ≈ 0.133;
P(exactly one) = 4/10 × 6/9 + 6/10 × 4/9 = 48/90 = 8/15 ≈ 0.533.

**Example:** ferry late 0.3; if late P(miss bus) = 0.6, if on time 0.05.
P(miss) = 0.3 × 0.6 + 0.7 × 0.05 = 0.18 + 0.035 = **0.215**.

⚠ Rounding part-way (3/9 → 0.33) so the end results don't add to 1 — 2026 Q9(a)(i), marking instructions
and course report.
"""

# ── contexts: (who, verb, base verb for 'did not …', name A, name B, short label A, short label B) ──
_TWO = [("visitors to Stornoway", "had visited", "visit", "the Callanish Stones", "Lews Castle",
         "Callanish Stones", "Lews Castle"),
        ("S5 pupils", "study", "study", "Applications of Maths", "Biology", "Applications", "Biology"),
        ("ferry passengers", "had", "have", "a car", "a cabin booked", "car", "cabin"),
        ("firefighter candidates", "passed", "pass", "the verbal test", "the numerical test", "verbal", "numerical"),
        ("members of a triathlon club", "do", "do", "sea swimming", "road cycling", "swimming", "cycling"),
        ("households in a Lewis village", "own", "own", "a dog", "a cat", "dog", "cat")]

_THREE = [("gym members", "use", "use", ["the treadmill", "the rowing machine", "the cross trainer"],
           ["treadmill", "rowing machine", "cross trainer"]),
          ("adults at evening classes", "take", "take", ["Gaelic", "French", "Spanish"], ["Gaelic", "French", "Spanish"]),
          ("walkers on the West Highland Way", "used", "use", ["a campsite", "a hostel", "a B&B"],
           ["campsite", "hostel", "B&B"]),
          ("visitors to the Outer Hebrides", "visited", "visit", ["Lewis", "Harris", "Uist"], ["Lewis", "Harris", "Uist"]),
          ("S6 pupils", "took", "take", ["Maths", "Physics", "Chemistry"], ["Maths", "Physics", "Chemistry"]),
          ("islanders", "used", "use", ["the Ullapool ferry", "the Uig ferry", "the Oban ferry"],
           ["Ullapool", "Uig", "Oban"])]


def _regions3():
    """Random three-set region counts (all positive)."""
    return {"ABC": random.randint(3, 12), "AB": random.randint(5, 35), "AC": random.randint(4, 30),
            "BC": random.randint(4, 30), "A": random.randint(10, 45), "B": random.randint(8, 45),
            "C": random.randint(5, 40), "none": random.randint(5, 25)}


# ── Level 1: two-set Venn diagrams ───────────────────────────────────────────────────────────
def generate_probability_l1(calc_mode=False):
    who, verb, _, a, b, la, lb = random.choice(_TWO)
    both = random.randint(12, 50)
    a_only, b_only, none = random.randint(10, 60), random.randint(8, 50), random.randint(6, 40)
    nA, nB, total = a_only + both, b_only + both, a_only + both + b_only + none
    inside = a_only + both + b_only
    ask = random.choice(["only_one", "neither", "a_not_b", "a_or_b"])
    if ask == "only_one":
        num, what, line = a_only + b_only, "exactly one of them", f"Only one = {a_only} + {b_only} = {a_only + b_only}"
    elif ask == "neither":
        num, what, line = none, "neither of them", f"Neither = {none}"
    elif ask == "a_not_b":
        num, what, line = a_only, f"{a} but not {b}", f"{a} only = {a_only}"
    else:
        num, what, line = inside, f"{a} or {b} (or both)", f"In either circle = {a_only} + {both} + {b_only} = {inside}"
    ans = _p(num, total)
    text = (f"{total} {who} were surveyed: {nA} {verb} {a}, {nB} {verb} {b} and {both} {verb} both. "
            f"Complete the Venn diagram, then calculate the probability that one of them, chosen at random, "
            f"{verb} {what}. Give your answer as a fraction or a decimal.")
    if ask == "neither":
        cands = [(_p(total - nA - nB, total) if total - nA - nB > 0 else None,
                  "you didn't subtract the overlap — the 'both' group is inside both totals (2026 MI: the diagram "
                  "can't add to more than the total)."),
                 (_p(none, inside), "divide by the grand total in the question, not the numbers in the circles "
                                    "(2026 Q4(b), Candidate A)."),
                 (_p(inside, total), "that's P(at least one) — 'neither' is the number outside both circles.")]
    else:
        cands = [(_p(num, inside), "you divided by the numbers in the circles — divide by the total in the question, "
                                   "including 'neither' (2026 Q4(b), Candidate A: 78/120).")]
        if ask == "only_one":
            cands.append((_p(nA + nB, total), "you didn't take the overlap off each total first."))
        elif ask == "a_not_b":
            cands.append((_p(nA, total), f"that's everyone who {verb} {a} — 'but not {b}' means {a} only."))
        else:
            cands.append((_p(nA + nB, total), "you counted the overlap twice."))
    return Question(
        question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": f"{la} only ({nA} − {both})", "answer": a_only},
                        {"prompt": f"{lb} only ({nB} − {both})", "answer": b_only},
                        {"prompt": "Neither (the total − everyone in the circles)", "answer": none},
                        {"prompt": "The probability", "answer": ans}],
        worked_solution=[f"Both: {both}. {la} only = {nA} − {both} = {a_only}; {lb} only = {nB} − {both} = {b_only}",
                         f"Neither = {total} − ({a_only} + {both} + {b_only}) = {none} — inside the rectangle",
                         line, f"P = {num} ÷ {total} = **{_fr(num, total)}**"],
        notes=NOTES_VENN2,
        metadata=_diagram("venn2", [la, lb], {"A": None, "B": None, "AB": None, "none": None}, width=380),
        distractors=_dist(ans, cands))


# ── Level 2: three-set Venn diagrams (exam style, multipart) ────────────────────────────────
def generate_probability_l2(calc_mode=False):
    who, verb, _, names, labels = random.choice(_THREE)
    r = _regions3()
    pt = {k: r[k] + r["ABC"] for k in ("AB", "AC", "BC")}
    st = {s: r[s] + sum(r[k] for k in ("AB", "AC", "BC") if s in k) + r["ABC"] for s in "ABC"}
    total = sum(r.values()); inside = total - r["none"]
    nm = dict(zip("ABC", names))
    facts = (f"• {r['ABC']} {verb} {nm['A']}, {nm['B']} and {nm['C']}\n"
             f"• {pt['AB']} {verb} {nm['A']} and {nm['B']}\n• {pt['BC']} {verb} {nm['B']} and {nm['C']}\n"
             f"• {pt['AC']} {verb} {nm['A']} and {nm['C']}\n"
             f"• {st['A']} {verb} {nm['A']}\n• {st['B']} {verb} {nm['B']}\n• {st['C']} {verb} {nm['C']}\n"
             f"• {r['none']} {verb} none of these")
    text = f"A group of {who} were asked about three options. The results were:\n\n{facts}"
    s = random.choice("ABC")
    p1, p2 = [k for k in ("AB", "AC", "BC") if s in k]
    part_a = make_part(
        "(a)", f"Complete the Venn diagram. How many {verb} {nm[s]} only?", r[s],
        scaffold_steps=[{"prompt": "The centre (all three)", "answer": r["ABC"]},
                        {"prompt": f"First pair region with {labels['ABC'.index(s)]}: pair total − centre", "answer": r[p1]},
                        {"prompt": "Second pair region: pair total − centre", "answer": r[p2]},
                        {"prompt": f"{labels['ABC'.index(s)]} only", "answer": r[s]}],
        worked_solution=[f"Centre {r['ABC']}; pairs {pt['AB']} − {r['ABC']} = {r['AB']}, {pt['BC']} − {r['ABC']} = "
                         f"{r['BC']}, {pt['AC']} − {r['ABC']} = {r['AC']}",
                         f"{nm[s]} only = {st[s]} − {r['ABC']} − {r[p1]} − {r[p2]} = **{r[s]}**"],
        distractors=_dist(r[s], [(st[s] - r["ABC"] - pt[p1] - pt[p2],
                                  "you used the pair totals without taking off the centre — 2025 Q2(a): candidates "
                                  "'did not consider … at least one other machine' (course report)."),
                                 (st[s] - r["ABC"], "take off the two pair regions as well as the centre.")]))
    part_b = make_part(
        "(b)", "How many were asked altogether?", total,
        scaffold_steps=[{"prompt": "Add the seven numbers in the circles", "answer": inside},
                        {"prompt": "Add 'none'", "answer": total}],
        worked_solution=[f"{' + '.join(str(r[k]) for k in ('A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC', 'none'))} = **{total}**"],
        distractors=_dist(total, [(inside, "include the 'none' group in the total (2024 Q2(b) course report)."),
                                  (st["A"] + st["B"] + st["C"] + r["none"],
                                   "adding the set totals counts the overlaps more than once.")]))
    pair = random.choice(["AB", "AC", "BC"])
    out = [n for n in "ABC" if n not in pair][0]
    ans = _p(r[pair], total)
    part_c = make_part(
        "(c)", f"One is selected at random. Determine the probability that they {verb} {nm[pair[0]]} and "
               f"{nm[pair[1]]}, but not {nm[out]}.", ans,
        scaffold_steps=[{"prompt": f"The '{labels['ABC'.index(pair[0])]} and {labels['ABC'.index(pair[1])]} only' "
                                   f"region", "answer": r[pair]},
                        {"prompt": "The probability", "answer": ans}],
        worked_solution=[f"P = {r[pair]} ÷ {total} = **{_fr(r[pair], total)}**"],
        distractors=_dist(ans, [(_p(pt[pair], total), f"the {pt[pair]} includes those in all three — 2025 Q2 marking "
                                                      "instructions, Candidate A."),
                                (_p(r[pair], inside), "include the 'none' group in the total (2024 Q2(b))."),
                                (_p(pt[pair], total + 3 * r["ABC"]),
                                 "the pair totals went straight into the overlaps, so the centre was counted "
                                 "again in each (2024 Q2 marking instructions, Candidate A: 60/273).")]))
    parts = [part_a, part_b, part_c]
    return Question(
        question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE, parts=parts,
        worked_solution=multipart_worked_solution(parts), notes=NOTES_VENN3,
        metadata=_diagram("venn3", labels, {k: None for k in r}, width=380))


# ── Level 3: combining events from a completed Venn diagram ─────────────────────────────────
def _q_ratio_or_fraction():
    """Which written answer gains the mark? (2026 Q4(b) marking instructions and CORs.)"""
    total = random.choice([120, 140, 150, 160, 180, 200])
    inside = total - random.randint(12, 30)
    n = random.randint(25, inside - 20)
    right, ratio, circles, count = f"{n}/{total}", f"{n} : {total - n}", f"{n}/{inside}", f"{n} people"
    opts = [right, ratio, circles, count]
    random.shuffle(opts)
    return Question(
        question_text=(f"{total} people were surveyed. In a Venn diagram of the results, {inside} are inside the "
                       f"circles and {n} are in exactly one circle. One person is chosen at random. Which answer to "
                       f"'calculate the probability that they are in exactly one circle' gains the mark?"),
        correct_answer=right, topic=TOPIC, question_type=QTYPE,
        worked_solution=[f"P = {n} ÷ {total} = **{right}** (≈ {_g(n / total)}) — a fraction, decimal or percentage, "
                         f"over the grand total."],
        notes=NOTES_VENN2, metadata={"options": opts},
        distractors=[{"value": ratio, "mistake": "a ratio is not a probability — 'not available for an answer "
                                                 "expressed as a ratio' (2026 Q4(b) marking instructions)."},
                     {"value": circles, "mistake": f"the total is the {total} in the question, not the {inside} in the "
                                                   f"circles (2026 Q4(b), Candidate A: 78/120)."},
                     {"value": count, "mistake": "that's a count, not a probability."}])


def generate_probability_l3(calc_mode=False):
    if random.random() < 0.2:
        return _q_ratio_or_fraction()
    three = random.random() < 0.6
    if three:
        who, verb, base, names, labels = random.choice(_THREE)
        r = _regions3()
        keys = ["A", "B", "C", "AB", "AC", "BC", "ABC", "none"]
    else:
        who, verb, base, a, b, la, lb = random.choice(_TWO)
        names, labels = [a, b], [la, lb]
        r = {"A": random.randint(8, 40), "AB": random.randint(5, 25), "B": random.randint(6, 35),
             "none": random.randint(5, 30)}
        keys = ["A", "B", "AB", "none"]
    nm = dict(zip("ABC", names))
    total = sum(r.values()); inside = total - r["none"]
    s = random.choice("AB")
    ask = random.choice(["and", "or", "not", "exactly1"] + (["atleast2"] if three else []))
    if ask == "and":
        ks = [k for k in keys if "A" in k and "B" in k]
        what = f"{verb} {nm['A']} and {nm['B']}"
        wrong = [(_p(r["AB"], total) if three else None, "include the centre — those in all three are in both too.")]
    elif ask == "or":
        ks = [k for k in keys if "A" in k or "B" in k]
        what = f"{verb} {nm['A']} or {nm['B']} (or both)"
        wrong = [(_p(sum(r[k] for k in keys if "A" in k) + sum(r[k] for k in keys if "B" in k), total),
                  "you counted the overlap twice — count each region once.")]
    elif ask == "not":
        ks = [k for k in keys if s not in k]
        what = f"did not {base} {nm[s]}"
        wrong = [(_p(sum(r[k] for k in ks if k != "none"), total), "'not' includes the 'none' group as well.")]
    elif ask == "exactly1":
        ks = [k for k in ("A", "B", "C") if k in keys]
        what = f"{verb} exactly one of the {len(ks)} shown"
        wrong = []
    else:
        ks = ["AB", "AC", "BC", "ABC"]
        what = f"{verb} at least two of the three"
        wrong = [(_p(r["AB"] + r["AC"] + r["BC"], total), "'at least two' includes those in all three.")]
    n = sum(r[k] for k in ks)
    ans = _p(n, total)
    wrong.append((_p(n, inside), "divide by the grand total, including 'none' — 2024 Q2(b): 'did not include the "
                                 "number … that did not study any language within their total' (course report)."))
    text = (f"The Venn diagram shows the results of a survey of {who}. One is chosen at random. Calculate the "
            f"probability that they {what}.")
    return Question(
        question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "The grand total (every number, including 'none')", "answer": total},
                        {"prompt": "The number in the region(s) wanted", "answer": n},
                        {"prompt": "The probability", "answer": ans}],
        worked_solution=[f"Total = {' + '.join(str(r[k]) for k in keys)} = {total}",
                         f"Regions wanted: {' + '.join(str(r[k]) for k in ks)} = {n}",
                         f"P = **{_fr(n, total)}**"],
        notes=NOTES_COMBINE,
        metadata=_diagram("venn3" if three else "venn2", list(labels), {k: r[k] for k in keys}, width=380),
        distractors=_dist(ans, wrong))


# ── Level 4: two-way tables ─────────────────────────────────────────────────────────────────
_TABLES = [("ferry passengers arriving at Tarbert", ["Resident", "Visitor"], ["By car", "On foot"], "passenger"),
           ("sailings recorded by a ferry company", ["Summer", "Winter"], ["On time", "Late"], "sailing"),
           ("pupils at a secondary school", ["S1–S3", "S4–S6"], ["School lunch", "Packed lunch"], "pupil"),
           ("passengers on a puffin-watching trip", ["Adult", "Child"], ["Seen before", "Not seen before"], "passenger"),
           ("driving-test candidates in Inverness", ["Automatic", "Manual"], ["Passed", "Failed"], "candidate")]


def _table_md(rows, cols, cells):
    rt = [sum(c) for c in cells]
    ct = [cells[0][j] + cells[1][j] for j in range(2)]
    md = f"| | {cols[0]} | {cols[1]} | Total |\n|---|---|---|---|\n"
    for i in range(2):
        md += f"| {rows[i]} | {cells[i][0]} | {cells[i][1]} | {rt[i]} |\n"
    return md + f"| Total | {ct[0]} | {ct[1]} | {sum(rt)} |"


def generate_probability_l4(calc_mode=False):
    who, rows, cols, one = random.choice(_TABLES)
    cells = [[random.randint(15, 140), random.randint(10, 120)] for _ in range(2)]
    rt = [sum(c) for c in cells]; ct = [cells[0][j] + cells[1][j] for j in range(2)]; T = sum(rt)
    i, j = random.randint(0, 1), random.randint(0, 1)
    ask = random.choice(["and", "or", "given"])
    if ask == "and":
        n, d = cells[i][j], T
        what = f"a {one} chosen at random is '{rows[i]}' and '{cols[j]}'"
        steps = [{"prompt": "Grand total", "answer": T}]
        line = f"P = {cells[i][j]} ÷ {T}"
        wrong = [(_p(cells[i][j], rt[i]), f"divide by the grand total {T}, not the row total."),
                 (_p(cells[i][j], ct[j]), f"divide by the grand total {T}, not the column total.")]
    elif ask == "or":
        n, d = rt[i] + ct[j] - cells[i][j], T
        what = f"a {one} chosen at random is '{rows[i]}' or '{cols[j]}' (or both)"
        steps = [{"prompt": f"Row total + column total − the cell counted twice ({rt[i]} + {ct[j]} − {cells[i][j]})",
                  "answer": n}]
        line = f"{rt[i]} + {ct[j]} − {cells[i][j]} = {n};  P = {n} ÷ {T}"
        wrong = [(_p(rt[i] + ct[j], T), f"the {cells[i][j]} is in both totals — take it off once."),
                 (_p(cells[i][j], T), "that's 'and' (the one cell) — 'or' is everything in the row or the column.")]
    else:
        n, d = cells[i][j], rt[i]
        what = f"a {one} chosen at random from the '{rows[i]}' row is '{cols[j]}'"
        steps = [{"prompt": f"The '{rows[i]}' total (only these count)", "answer": rt[i]}]
        line = f"Only the {rt[i]} in '{rows[i]}' count: P = {cells[i][j]} ÷ {rt[i]}"
        wrong = [(_p(cells[i][j], T), f"the {one} is chosen from '{rows[i]}' only — divide by {rt[i]}."),
                 (_p(cells[i][j], ct[j]), f"divide by the '{rows[i]}' row total, not the '{cols[j]}' column total.")]
    ans = _p(n, d)
    steps.append({"prompt": "The probability", "answer": ans})
    text = f"The table shows {who}.\n\n{_table_md(rows, cols, cells)}\n\nCalculate the probability that {what}."
    return Question(
        question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE, scaffold_steps=steps,
        worked_solution=[line, f"P = **{_fr(n, d)}**"], notes=NOTES_TABLE, distractors=_dist(ans, wrong))


# ── Level 5: tree diagrams, independent events ──────────────────────────────────────────────
_DELAYS = [("A boatbuilder", "a manufacturing delay", "a delivery delay", "manufacturing delay", "delivery delay"),
           ("A lorry taking salmon to the mainland", "bad weather on the Minch", "a breakdown", "bad weather",
            "breakdown"),
           ("A festival stage builder", "a weather delay", "staff failing to arrive", "weather delay", "staff delay"),
           ("A housing contractor", "a supplier delay", "a planning delay", "supplier delay", "planning delay")]


def generate_probability_l5(calc_mode=False):
    who, e1, e2, h1, h2 = random.choice(_DELAYS)
    p1 = random.choice([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])
    p2 = random.choice([0.05, 0.1, 0.12, 0.15, 0.2, 0.25, 0.3])
    q1, q2 = round(1 - p1, 4), round(1 - p2, 4)
    ends = [round(p1 * p2, 6), round(p1 * q2, 6), round(q1 * p2, 6), round(q1 * q2, 6)]
    ask = random.choice(["one_or_both", "one_or_both", "exactly_one", "neither"])
    if ask == "one_or_both":
        ans = round(1 - ends[3], 6); what = "one or both of these delays will happen"
        line = f"1 − P(no delay) = 1 − {_g(ends[3], 6)} = **{_g(ans, 6)}**"
        other = (ends[3], "that's P(no delay) — 'one or both' is 1 minus it.")
    elif ask == "exactly_one":
        ans = round(ends[1] + ends[2], 6); what = "exactly one of these delays will happen"
        line = f"{_g(ends[1], 6)} + {_g(ends[2], 6)} = **{_g(ans, 6)}**"
        other = (round(1 - ends[3], 6), "that's 'one or both' — exactly one leaves out the both-delays path.")
    else:
        ans = ends[3]; what = "neither delay happens"
        line = f"{_g(q1)} × {_g(q2)} = **{_g(ans, 6)}**"
        other = (round(1 - ends[3], 6), "that's P(one or both) — neither is the no-delay, no-delay path.")
    text = (f"{who} can be delayed by {e1} (probability {_g(p1)}) or by {e2} (probability {_g(p2)}). The two are "
            f"independent. Complete the tree diagram, then determine the probability that {what}.")
    return Question(
        question_text=text, correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": f"P(no {h1})", "answer": q1}, {"prompt": f"P(no {h2})", "answer": q2},
                        {"prompt": "P(no delay at all) — multiply along the path", "answer": ends[3]},
                        {"prompt": "The probability asked for", "answer": ans}],
        worked_solution=[f"Missing branches: 1 − {_g(p1)} = {_g(q1)}, 1 − {_g(p2)} = {_g(q2)}",
                         f"End results: {', '.join(_g(e, 6) for e in ends)} (they add to 1 — no rounding)", line],
        notes=NOTES_TREE,
        metadata=_diagram("tree_q", [h1, h2], [["delay", _g(p1)], ["no delay", None]],
                          [[["delay", _g(p2)], ["no delay", None]], [["delay", None], ["no delay", None]]],
                          [None, None, None, None], width=520),
        distractors=_dist(ans, [(round(p1 + p2, 6), "you added the two probabilities — multiply along the tree "
                                                    "(2026 Q9(a)(ii) course report)."),
                                (ends[0], "that's P(both delays) only."), other,
                                (ends[1] if ask == "exactly_one" else None,
                                 "there are two paths with exactly one delay — add both.")]))


# ── Level 6: tree diagrams, without replacement and conditional ─────────────────────────────
_BAGS = [("raffle tickets in a hat at a ceilidh", "winning", "losing"),
         ("chocolates in a box", "caramel", "truffle"),
         ("names in a hat for a quiz team", "S5", "S6"),
         ("counters in a bag", "red", "blue")]
_COND = [("the Oban ferry arrives late", "a passenger misses the connecting bus"),
         ("it rains on the day of a shinty match", "the match is cancelled"),
         ("a supplier is late", "the building work is delayed"),
         ("the plane from Glasgow to Barra is delayed", "a visitor misses their connecting ferry")]


def _q_without_replacement():
    what, x, y = random.choice(_BAGS)
    a, b = random.randint(3, 8), random.randint(4, 9)
    N = a + b; d = N * (N - 1)
    ask = random.choice(["both_x", "different", "same"])
    if ask == "both_x":
        n, q = a * (a - 1), f"both are {x}"
        line = f"{a}/{N} × {a - 1}/{N - 1} = {n}/{d}"
        wrong = [(_p(a * a, N * N), "that's WITH replacement — after one is taken there is one fewer of each count.")]
    elif ask == "different":
        n, q = 2 * a * b, "the two are different"
        line = f"{a}/{N} × {b}/{N - 1} + {b}/{N} × {a}/{N - 1} = {n}/{d}"
        wrong = [(_p(a * b, d), f"there are two paths: {x} then {y}, and {y} then {x}."),
                 (_p(2 * a * b, N * N), "that's WITH replacement — the second draw is out of one fewer.")]
    else:
        n, q = a * (a - 1) + b * (b - 1), "the two are the same"
        line = f"{a}/{N} × {a - 1}/{N - 1} + {b}/{N} × {b - 1}/{N - 1} = {n}/{d}"
        wrong = [(_p(a * a + b * b, N * N), "that's WITH replacement."),
                 (_p(a * (a - 1), d), f"add the {y}–{y} path too.")]
    ans = _p(n, d)
    return Question(
        question_text=(f"There are {N} {what}: {a} {x} and {b} {y}. Two are taken at random, without replacement. "
                       f"Calculate the probability that {q}."),
        correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": f"P(first is {x})", "answer": _p(a, N)},
                        {"prompt": f"P(second is {x}, given the first was {x})", "answer": _p(a - 1, N - 1)},
                        {"prompt": "The probability asked for", "answer": ans}],
        worked_solution=[line, f"P = **{_fr(n, d)}** — keep fractions; don't round part-way."],
        notes=NOTES_DEPENDENT,
        metadata=_diagram("tree_q", ["first", "second"], [[x, f"{a}/{N}"], [y, f"{b}/{N}"]],
                          [[[x, None], [y, None]], [[x, None], [y, None]]], None, width=440),
        distractors=_dist(ans, wrong))


def _q_conditional():
    first, second = random.choice(_COND)
    p1 = random.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.4])
    pa = random.choice([0.5, 0.6, 0.7, 0.75, 0.8])
    pn = random.choice([0.02, 0.05, 0.1])
    ans = round(p1 * pa + (1 - p1) * pn, 6)
    return Question(
        question_text=(f"The probability that {first} is {_g(p1)}. If it does, the probability that {second} is "
                       f"{_g(pa)}; if not, the probability is {_g(pn)}. Calculate the probability that {second}."),
        correct_answer=ans, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[{"prompt": "First path: multiply", "answer": round(p1 * pa, 6)},
                        {"prompt": "Second path: multiply", "answer": round((1 - p1) * pn, 6)},
                        {"prompt": "Add the two paths", "answer": ans}],
        worked_solution=[f"{_g(p1)} × {_g(pa)} + {_g(1 - p1)} × {_g(pn)} = {_g(p1 * pa, 6)} + {_g((1 - p1) * pn, 6)} "
                         f"= **{_g(ans, 6)}**"],
        notes=NOTES_DEPENDENT,
        metadata=_diagram("tree_q", ["first event", "second event"], [["yes", _g(p1)], ["no", _g(1 - p1)]],
                          [[["yes", _g(pa)], ["no", None]], [["yes", _g(pn)], ["no", None]]], None, width=440),
        distractors=_dist(ans, [(round(p1 * pa, 6), "add the second path too — it can also happen when the first "
                                                    "event doesn't."),
                                (round(pa + pn, 6), "multiply along each path before adding (2026 Q9(a)(ii) course "
                                                    "report: added instead of multiplied)."),
                                (round(p1 * pa + pn, 6), f"the second path is {_g(1 - p1)} × {_g(pn)}, not just {_g(pn)}.")]))


def generate_probability_l6(calc_mode=False):
    return _q_without_replacement() if random.random() < 0.55 else _q_conditional()


LEVELS = {"Two-Set Venn Diagrams": generate_probability_l1,
          "Three-Set Venn Diagrams": generate_probability_l2,
          "Combining Events from a Venn Diagram": generate_probability_l3,
          "Two-Way Tables": generate_probability_l4,
          "Tree Diagrams: Independent Events": generate_probability_l5,
          "Tree Diagrams: Without Replacement and Conditional": generate_probability_l6}


def generate_probability_question(calc_mode=False):
    return random.choice(list(LEVELS.values()))()
