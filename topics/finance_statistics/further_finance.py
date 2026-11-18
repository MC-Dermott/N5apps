"""Higher Finance — further question types from the specification examples (Nov 2026): payment patterns, working
backwards, loans in all forms, repayment holidays, saving strategies, inflation indices, overtime/bonus, pension
contributions, stamp duty. Every part carries metadata["marks"]. All rates are effective rates (spec)."""
import random

from core.models.further import (fv_end, g, gbp, md_table, mon, part, pmt, pv_end, question, r2, step)

T = "Finance"
_NAMES = ["Ailsa", "Callum", "Morag", "Iain", "Kirsty", "Fraser", "Isla", "Euan", "Catriona", "Ruaridh"]

NOTES_PATTERNS = """
**Payments in patterns.** Value each payment at the same date, then add. A payment made *k* years before the date grows
by × (1 + r)ᵏ. Rising payments: list them (fixed step, or each × the growth factor). Deferred: the first payment is later,
so there are fewer years of growth.
"""
NOTES_BACK = """
**Working backwards.** Single payment needed: target ÷ (1 + r)ⁿ. Regular payment needed to reach a target:
target × r ÷ ((1 + r)ⁿ − 1). A loan equals the present value of its repayments: P × (1 − (1 + r)⁻ⁿ) ÷ r.
"""
NOTES_RATES = """
**Comparing and changing rates.** Compare products using effective rates over the same period. When the rate changes,
multiply the growth factors year by year: 1.04 × 1.05 × 1.03 …
"""
NOTES_LOANS = """
**Loans in different forms.** Single repayment: borrowed × (1 + r)ⁿ. Interest-only: interest = rate × loan each period,
and the capital is repaid at the end. Level repayments: P × r ÷ (1 − (1 + r)⁻ⁿ). Decreasing repayments: equal capital each
month plus interest on what is still owed. A payday loan's effective yearly rate = (1 + monthly rate)¹² − 1.
"""
NOTES_HOLIDAY = """
**Repayment holiday.** Interest is still added during the holiday, so the balance grows to P × (1 + r)ʰ; the new repayments
are then calculated on that larger balance over the remaining months, so more is paid in total.
"""
NOTES_STRATEGY = """
**Comparing strategies.** Put every option on the same time footing: accumulated value (or total extra cost) at the end.
Saving earlier means the money earns interest for longer, even if less is paid in.
"""
NOTES_PI = """
**Price indices and inflation.** Index ratio = index now ÷ index then. A basket costing £x then costs x × ratio now.
£1 now buys 1 ÷ ratio of what it bought. Average yearly inflation = ratio^(1/years) − 1.
"""
NOTES_PAY = """
**Pay.** Overtime = hours × normal rate × multiplier (time and a half = × 1.5). A bonus is a percentage of the annual basic
pay. Superannuation is a percentage of salary, paid by employee and employer.
"""
NOTES_SDLT = """
**Property taxes in bands.** Each band is charged only on the part of the price inside it. Add the bands.
"""


def _yrs(n):
    return f"{n} year{'s' if n != 1 else ''}"


# ── Present Value ──────────────────────────────────────────────────────────────
def generate_payment_patterns():
    r = random.choice([3, 3.5, 4, 4.5, 5]) / 100
    kind = random.choice(["step", "grow", "defer"])
    if kind == "step":
        p0, d = random.choice(range(100, 301, 20)), random.choice([10, 20, 30, 40])
        pays = [p0 + d * k for k in range(5)]
        val = sum(p * (1 + r) ** (4 - k) for k, p in enumerate(pays))
        text = (f"A saver pays {', '.join(gbp(p) for p in pays[:-1])} and {gbp(pays[-1])} at the ends of years 1 to 5 (each payment is "
                f"£{d} more than the last). The account pays {g(r * 100)}% effective per year. Find the value at the end of year 5.")
        worked = [f"Value = " + " + ".join(f"{g(p)} × {1 + r:g}^{4 - k}" for k, p in enumerate(pays)), f"= **{gbp(r2(val))}**"]
        steps = [step("Value of the first payment at year 5", r2(pays[0] * (1 + r) ** 4)), step("Total value at year 5", r2(val))]
    elif kind == "grow":
        p0, gr = random.choice(range(100, 301, 20)), random.choice([3, 4, 5, 6])
        pays = [p0 * (1 + gr / 100) ** k for k in range(5)]
        val = sum(p * (1 + r) ** (4 - k) for k, p in enumerate(pays))
        text = (f"{gbp(p0)} is paid at the end of year 1, then each year's payment is {gr}% more than the last, for 5 years. The account "
                f"pays {g(r * 100)}% effective per year. Find the value at the end of year 5.")
        worked = [f"Payments: " + ", ".join(gbp(r2(p)) for p in pays), f"Value = Σ payment × {1 + r:g}^(years left) = **{gbp(r2(val))}**"]
        steps = [step("Second payment", r2(pays[1])), step("Total value at year 5", r2(val))]
    else:
        p, m = random.choice(range(150, 401, 50)), random.choice([2, 3])
        n = 5
        val = fv_end(p, r, n) * (1 + r) ** 2
        text = (f"{gbp(p)} is paid at the end of each year for {n} years, starting at the end of year {m + 1}. The account pays "
                f"{g(r * 100)}% effective per year. Find the value of the savings at the end of year {m + n + 2}.")
        worked = [f"Value when the last payment is made = {p} × ({1 + r:g}⁵ − 1) ÷ {r:g} = {gbp(r2(fv_end(p, r, n)))}",
                  f"It then grows for 2 more years: × {1 + r:g}² = **{gbp(r2(val))}**"]
        steps = [step("Value just after the last payment", r2(fv_end(p, r, n))), step("Value two years later", r2(val))]
    return question(T, "Present Value", "", [part("(a)", text, r2(val), worked, steps, marks=4)], NOTES_PATTERNS, "Payment Patterns")


def generate_working_backwards():
    kind = random.choice(["single", "series", "loan"])
    if kind == "single":
        tgt, n, r = random.choice(range(5000, 20001, 2500)), random.randint(3, 8), random.choice([2.5, 3, 3.5, 4]) / 100
        ans = tgt / (1 + r) ** n
        text = (f"A deposit of {gbp(tgt)} is needed in {_yrs(n)}. How much must be paid into an account now to have exactly this amount, "
                f"at {g(r * 100)}% effective per year?")
        worked = [f"{tgt:,} ÷ {1 + r:g}^{n} = **{gbp(r2(ans))}**"]
        steps = [step(f"{1 + r:g}^{n}", round((1 + r) ** n, 4))]
    elif kind == "series":
        tgt, n, rm = random.choice(range(6000, 20001, 2000)), random.randint(2, 5), random.choice([0.2, 0.25, 0.3]) / 100
        ans = tgt * rm / ((1 + rm) ** (12 * n) - 1)
        text = (f"A saver wants {gbp(tgt)} in {_yrs(n)}. Equal payments go into an account at the end of each month, which pays "
                f"{g(rm * 100)}% effective per month. Find the monthly payment.")
        worked = [f"Payment = {tgt:,} × {rm:g} ÷ ({1 + rm:g}^{12 * n} − 1) = **{gbp(r2(ans))}**"]
        steps = [step(f"({1 + rm:g}^{12 * n} − 1)", round((1 + rm) ** (12 * n) - 1, 5))]
    else:
        pay, n, rm = random.choice(range(150, 401, 50)), random.choice([36, 48, 60]), random.choice([0.5, 0.6, 0.7, 0.8]) / 100
        ans = pv_end(pay, rm, n)
        text = (f"A lender will receive {gbp(pay)} at the end of each month for {n} months. The loan carries {g(rm * 100)}% effective "
                f"per month. What loan amount do these repayments clear?")
        worked = [f"Loan = repayments' present value = {pay} × (1 − {1 + rm:g}^−{n}) ÷ {rm:g} = **{gbp(r2(ans))}**"]
        steps = [step(f"1 − {1 + rm:g}^−{n}", round(1 - (1 + rm) ** -n, 5))]
    return question(T, "Present Value", "", [part("(a)", text, r2(ans), worked, steps, marks=3)], NOTES_BACK, "Working Backwards")


def generate_payments_several_times():
    r = random.choice([3, 4, 5]) / 100
    pays = [random.choice(range(200, 801, 50)) for _ in range(5)]
    pv = sum(p / (1 + r) ** (k + 1) for k, p in enumerate(pays))
    text = (f"A buyer will pay " + ", ".join(gbp(p) for p in pays[:-1]) + f" and {gbp(pays[-1])} at the ends of years 1, 2, 3, 4 and 5. "
            f"At {g(r * 100)}% effective per year, find the single payment now that is equivalent (the present value).")
    worked = [" + ".join(f"{p}/{1 + r:g}^{k + 1}" for k, p in enumerate(pays)), f"= **{gbp(r2(pv))}**"]
    steps = [step("Present value of the first payment", r2(pays[0] / (1 + r))), step("Present value of all five", r2(pv))]
    return question(T, "Present Value", "", [part("(a)", text, r2(pv), worked, steps, marks=4)], NOTES_BACK, "Payments at Several Times")


# ── Effective interest rates ───────────────────────────────────────────────────
def generate_comparing_products():
    a, b = random.sample([2.4, 2.6, 2.9, 3.1, 3.4, 3.7], 2)
    loan, card = random.choice([6.9, 7.4, 8.2, 9.5]), random.choice([17.9, 19.5, 21.9, 24.9])
    P, n = random.choice(range(1000, 3001, 500)), random.choice([2, 3])
    best = max(a, b); inta = P * (1 + best / 100) ** n - P
    intl, intc = P * (1 + loan / 100) ** n - P, P * (1 + card / 100) ** n - P
    ctx = (f"Effective yearly rates: savings account A {a}%, savings account B {b}%, personal loan {loan}%, credit card {card}%.")
    parts = [part("(a)", "Which savings account is better for a saver?", f"Account {'A' if a > b else 'B'}",
                  [f"The higher effective rate: {best}% → **Account {'A' if a > b else 'B'}**"], options=["Account A", "Account B"], marks=1),
             part("(b)", f"Find the interest earned on {gbp(P)} in the better account over {_yrs(n)}.", r2(inta),
                  [f"{P} × {1 + best / 100:g}^{n} − {P} = **{gbp(r2(inta))}**"], [step("Amount after the period", r2(P + inta))], marks=2),
             part("(c)", f"If {gbp(P)} were borrowed on the credit card and nothing repaid for {_yrs(n)}, find the interest owed.", r2(intc),
                  [f"{P} × {1 + card / 100:g}^{n} − {P} = **{gbp(r2(intc))}**"], [step("Amount owed", r2(P + intc))], marks=2),
             part("(d)", f"How much more interest is owed on the card than on the loan over the same {_yrs(n)}?", r2(intc - intl),
                  [f"Loan interest = {gbp(r2(intl))}; difference = {gbp(r2(intc))} − {gbp(r2(intl))} = **{gbp(r2(intc - intl))}**"], marks=2)]
    return question(T, "Effective Interest Rates", ctx, parts, NOTES_RATES, "Comparing Products")


def generate_rates_change():
    P = random.choice(range(2000, 12001, 1000)); rs = random.sample([3.5, 4.0, 4.5, 5.0, 5.5, 6.0], 3)
    fin = P * (1 + rs[0] / 100) * (1 + rs[1] / 100) * (1 + rs[2] / 100)
    ctx = f"A variable-rate loan of {gbp(P)} is repaid in one payment after 3 years. The effective rates in the three years are {rs[0]}%, {rs[1]}% and {rs[2]}%."
    parts = [part("(a)", "Find the amount to be repaid.", r2(fin), [f"{P} × {1 + rs[0] / 100:g} × {1 + rs[1] / 100:g} × {1 + rs[2] / 100:g} = **{gbp(r2(fin))}**"],
                  [step("Balance after year 1", r2(P * (1 + rs[0] / 100)))], marks=3),
             part("(b)", "Find the total interest.", r2(fin - P), [f"{gbp(r2(fin))} − {gbp(P)} = **{gbp(r2(fin - P))}**"], marks=1)]
    return question(T, "Effective Interest Rates", ctx, parts, NOTES_RATES, "Rates That Change")


# ── Credit cards ───────────────────────────────────────────────────────────────
def generate_loans_all_forms():
    kind = random.choice(["payday", "card", "personal"])
    if kind == "payday":
        B = random.choice(range(200, 501, 50)); fee = random.choice([15, 20, 25])
        pay = B * (1 + fee / 100)
        ans = round(((1 + fee / 100) ** 12 - 1) * 100, 1)
        text = (f"A payday loan of {gbp(B)} is repaid as {gbp(pay)} after one month. Find the equivalent effective yearly rate of interest, as a percentage "
                f"to 1 decimal place.")
        worked = [f"Monthly rate = ({pay:g} − {B}) ÷ {B} = {fee}%", f"Yearly = {1 + fee / 100:g}¹² − 1 = **{ans}%**"]
        steps = [step("Monthly interest rate (%)", float(fee))]
        marks = 3
    elif kind == "card":
        B = random.choice(range(500, 2001, 250)); rm = random.choice([1.2, 1.5, 1.8, 2.0]); n = random.choice([3, 4, 6])
        ans = r2(B * (1 + rm / 100) ** n)
        text = f"A credit-card balance of {gbp(B)} is left unpaid for {n} months at {rm}% effective per month. Find the balance."
        worked = [f"{B} × {1 + rm / 100:g}^{n} = **{gbp(ans)}**"]; steps = [step("Monthly multiplier", round(1 + rm / 100, 4))]; marks = 2
    else:
        L = random.choice(range(2000, 10001, 1000)); ry = random.choice([7, 8, 9, 10]); n = random.choice([2, 3, 4])
        ans = r2(L * (1 + ry / 100) ** n)
        text = f"A personal loan of {gbp(L)} at {ry}% effective per year is repaid in a single payment after {_yrs(n)}. Find the payment."
        worked = [f"{L} × {1 + ry / 100:g}^{n} = **{gbp(ans)}**"]; steps = [step("Yearly multiplier", round(1 + ry / 100, 3))]; marks = 2
    return question(T, "Credit Cards", "", [part("(a)", text, ans, worked, steps, marks=marks)], NOTES_LOANS, "Loans in All Forms")


# ── Loan schedules / mortgages ─────────────────────────────────────────────────
def generate_loan_forms():
    L = random.choice(range(2000, 8001, 500)); ry = random.choice([5.5, 6.5, 7.5]); ny = random.choice([2, 3, 4])
    M = random.choice(range(60000, 120001, 10000)); ri = random.choice([3.5, 4, 4.5, 5]); ni = random.choice([20, 25])
    Lp, rm, nm = random.choice(range(4000, 9001, 1000)), random.choice([0.4, 0.5, 0.6]) / 100, random.choice([36, 48])
    a = L * (1 + ry / 100) ** ny; ia = M * ri / 100; pm = pmt(Lp, rm, nm)
    parts = [part("(a)", f"A {gbp(L)} loan at {ry}% effective per year is repaid in a single payment after {_yrs(ny)}. How much is repaid?", r2(a),
                  [f"{L} × {1 + ry / 100:g}^{ny} = **{gbp(r2(a))}**"], marks=2),
             part("(b)", f"A {gbp(M)} loan at {ri}% per year is interest-only: interest is paid each year and the capital is repaid after {ni} years. "
                         f"Find the yearly interest.", r2(ia), [f"{M} × {ri / 100:g} = **{gbp(r2(ia))}**"], marks=1),
             part("(c)", f"Find the total paid over the {ni} years in (b).", r2(ni * ia + M), [f"{ni} × {gbp(r2(ia))} + {gbp(M)} = **{gbp(r2(ni * ia + M))}**"], marks=2),
             part("(d)", f"A {gbp(Lp)} loan at {g(rm * 100)}% effective per month is repaid by {nm} level monthly repayments. Find the repayment.", r2(pm),
                  [f"{Lp} × {rm:g} ÷ (1 − {1 + rm:g}^−{nm}) = **{gbp(r2(pm))}**"], [step("1 − multiplier^−n", round(1 - (1 + rm) ** -nm, 5))], marks=3)]
    return question(T, "Loan Schedules", "", parts, NOTES_LOANS, "Single, Interest-only and Level Repayments")


def generate_decreasing_repayments():
    L = random.choice([1200, 1500, 1800, 2400]); n = 6; rm = random.choice([1.0, 1.2, 1.5]) / 100
    cap = L / n; bal = L; pays = []
    for _ in range(n):
        pays.append(cap + bal * rm); bal -= cap
    ti = sum(pays) - L; lv = pmt(L, rm, n); til = lv * n - L
    ctx = (f"A {gbp(L)} loan has interest of {g(rm * 100)}% per month on the outstanding balance, repaid over {n} months. Option A: repay {gbp(cap)} of capital each "
           f"month plus that month's interest. Option B: {n} level monthly repayments.")
    parts = [part("(a)", "Find the first repayment in option A.", r2(pays[0]), [f"{cap:g} + {L} × {rm:g} = **{gbp(r2(pays[0]))}**"], marks=1),
             part("(b)", "Find the total interest paid in option A.", r2(ti), ["Repayments: " + ", ".join(gbp(r2(p)) for p in pays), f"Total interest = {gbp(r2(sum(pays)))} − {gbp(L)} = **{gbp(r2(ti))}**"],
                  [step("Last repayment", r2(pays[-1]))], marks=3),
             part("(c)", "Find the level monthly repayment in option B.", r2(lv), [f"{L} × {rm:g} ÷ (1 − {1 + rm:g}^−{n}) = **{gbp(r2(lv))}**"], marks=2),
             part("(d)", "Which option has less total interest?", "Option A" if ti < til else "Option B",
                  [f"A: {gbp(r2(ti))}; B: {gbp(r2(til))} → **{'Option A' if ti < til else 'Option B'}**: capital is repaid faster at the start, so the balance falls quicker"],
                  options=["Option A", "Option B"], marks=1)]
    return question(T, "Loan Schedules", ctx, parts, NOTES_LOANS, "Decreasing Repayments")


def generate_repayment_holiday():
    P = random.choice(range(5000, 12001, 1000)); rm = random.choice([0.6, 0.7, 0.8, 0.9]) / 100; n = random.choice([24, 30, 36]); h = random.choice([2, 3])
    norm = pmt(P, rm, n); bal = P * (1 + rm) ** h; new = pmt(bal, rm, n - h); extra = new * (n - h) - norm * n
    ctx = f"A {gbp(P)} loan is repaid over {n} months at {g(rm * 100)}% effective per month."
    parts = [part("(a)", "Find the normal monthly repayment.", r2(norm), [f"{P} × {rm:g} ÷ (1 − {1 + rm:g}^−{n}) = **{gbp(r2(norm))}**"], marks=2),
             part("(b)", f"The borrower takes a {h}-month repayment holiday at the start (no payments; interest still added). Find the balance after the holiday.", r2(bal),
                  [f"{P} × {1 + rm:g}^{h} = **{gbp(r2(bal))}**"], marks=1),
             part("(c)", f"The rest is repaid over the remaining {n - h} months. Find the new monthly repayment.", r2(new),
                  [f"{r2(bal)} × {rm:g} ÷ (1 − {1 + rm:g}^−{n - h}) = **{gbp(r2(new))}**"], marks=2),
             part("(d)", "How much more is paid in total than without the holiday?", r2(extra),
                  [f"{n - h} × {gbp(r2(new))} − {n} × {gbp(r2(norm))} = **{gbp(r2(extra))}**"], marks=2)]
    return question(T, "Loan Schedules", ctx, parts, NOTES_HOLIDAY, "Repayment Holiday")


def generate_rate_rise():
    M = random.choice(range(100000, 200001, 25000)); yrs = random.choice([20, 25, 30]); r1, r2_ = random.choice([(3.5, 5.5), (4, 6), (3, 5)])
    inc = random.choice(range(2200, 3201, 200))
    p1, p2 = pmt(M, mon(r1 / 100), 12 * yrs), pmt(M, mon(r2_ / 100), 12 * yrs)
    ctx = (f"A {gbp(M)} variable-rate mortgage is repaid over {yrs} years in monthly repayments (use the effective monthly rate equivalent to the yearly rate). "
           f"A household's take-home income is {gbp(inc)} a month.")
    parts = [part("(a)", f"Find the monthly repayment when the effective yearly rate is {r1}%.", r2(p1), [f"Monthly rate = {1 + r1 / 100:g}^(1/12) − 1 = {mon(r1 / 100) * 100:.4f}%", f"Repayment = **{gbp(r2(p1))}**"],
                  [step("Effective monthly rate (%)", round(mon(r1 / 100) * 100, 4))], marks=3),
             part("(b)", f"Find the monthly repayment when the rate rises to {r2_}%.", r2(p2), [f"Repayment = **{gbp(r2(p2))}**"], marks=2),
             part("(c)", f"What percentage of take-home income does the higher repayment take (1 d.p.)?", round(p2 / inc * 100, 1),
                  [f"{gbp(r2(p2))} ÷ {inc} × 100 = **{p2 / inc * 100:.1f}%**"], marks=1)]
    return question(T, "Mortgages", ctx, parts, NOTES_HOLIDAY + "\nA rate rise raises repayments and can make them unaffordable for the borrower.", "Rate Rise and Affordability")


# ── Savings ────────────────────────────────────────────────────────────────────
def generate_time_to_goal():
    goal = random.choice(range(5000, 15001, 2500)); rm = random.choice([0.15, 0.2, 0.25]) / 100
    p1 = random.choice(range(150, 301, 50)); p2 = p1 + random.choice([50, 100])

    def months(p):
        b = 0; k = 0
        while b < goal:
            b = b * (1 + rm) + p; k += 1
        return k
    k1, k2 = months(p1), months(p2)
    ctx = f"A saver wants {gbp(goal)}. Payments are made at the end of each month into an account earning {g(rm * 100)}% effective per month."
    parts = [part("(a)", f"How many months does it take saving {gbp(p1)} a month?", k1, [f"Use the balance rule Bₙ₊₁ = {1 + rm:g}Bₙ + {p1}, or the formula, until the balance reaches {gbp(goal)}: **{k1} months**"], marks=3),
             part("(b)", f"How many months if she saves {gbp(p2)} a month?", k2, [f"**{k2} months**"], marks=2),
             part("(c)", "How many months does the extra saving cut off?", k1 - k2, [f"{k1} − {k2} = **{k1 - k2} months**"], marks=1)]
    return question(T, "Savings Products and Pensions", ctx, parts, NOTES_STRATEGY, "Time to Reach a Goal")


def generate_spend_or_save():
    kind = random.choice(["spend", "use", "loan"])
    if kind == "spend":
        A, n, r = random.choice(range(1000, 4001, 500)), random.choice([3, 4, 5]), random.choice([2.5, 3, 3.5]) / 100
        v = A * (1 + r) ** n
        ctx = f"{random.choice(_NAMES)} can spend {gbp(A)} on a holiday now, or save it for {_yrs(n)} at {g(r * 100)}% effective per year."
        parts = [part("(a)", "Find the amount after saving.", r2(v), [f"{A} × {1 + r:g}^{n} = **{gbp(r2(v))}**"], marks=2),
                 part("(b)", "How much extra does saving give?", r2(v - A), [f"{gbp(r2(v))} − {gbp(A)} = **{gbp(r2(v - A))}**"], marks=1)]
    elif kind == "use":
        A, n = random.choice(range(3000, 9001, 1000)), 2; rs, rl = random.choice([2.5, 3, 3.5]) / 100, random.choice([7, 8, 9]) / 100
        s, l = A * (1 + rs) ** n - A, A * (1 + rl) ** n - A
        ctx = (f"{random.choice(_NAMES)} has {gbp(A)}. Option A: keep it in a {n}-year fixed account at {g(rs * 100)}% effective per year. Option B: use it to repay a "
               f"{gbp(A)} loan costing {g(rl * 100)}% effective per year.")
        parts = [part("(a)", "Find the interest earned in option A.", r2(s), [f"{A} × {1 + rs:g}^{n} − {A} = **{gbp(r2(s))}**"], marks=2),
                 part("(b)", "Find the interest avoided in option B.", r2(l), [f"{A} × {1 + rl:g}^{n} − {A} = **{gbp(r2(l))}**"], marks=2),
                 part("(c)", "Which is better financially?", "Option B", [f"B saves {gbp(r2(l - s))} more → **Option B**"], options=["Option A", "Option B"], marks=1)]
    else:
        A, rs, rl = random.choice(range(7000, 14001, 1000)), random.choice([2.5, 3, 3.5]) / 100, random.choice([6, 7, 8]) / 100
        lost = A * (1 + rs) ** 3 - A; pm_ = pmt(A, mon(rl), 36); extra = 36 * pm_ - A
        ctx = (f"A car costs {gbp(A)}. Option A: pay from savings that earn {g(rs * 100)}% effective per year (3 years' lost interest). Option B: borrow {gbp(A)} at "
               f"{g(rl * 100)}% effective per year over 36 level monthly repayments (use the equivalent monthly rate).")
        parts = [part("(a)", "Find the lost interest in option A.", r2(lost), [f"{A} × {1 + rs:g}³ − {A} = **{gbp(r2(lost))}**"], marks=2),
                 part("(b)", "Find the extra cost (total repaid − amount borrowed) in option B.", r2(extra),
                      [f"Monthly repayment = {gbp(r2(pm_))}; 36 × {gbp(r2(pm_))} − {gbp(A)} = **{gbp(r2(extra))}**"], marks=3),
                 part("(c)", "Which option costs less?", "Option A" if lost < extra else "Option B", [f"**{'Option A' if lost < extra else 'Option B'}**"],
                      options=["Option A", "Option B"], marks=1)]
    return question(T, "Savings Products and Pensions", ctx, parts, NOTES_STRATEGY, "Spend or Save, Loan or Savings")


def generate_earlier_or_later():
    r = random.choice([5, 6, 7]) / 100; pay = random.choice([500, 1000, 1500]); a, b = random.choice([(10, 20), (8, 22), (12, 18)])
    A = fv_end(pay, r, a) * (1 + r) ** b; B = fv_end(pay, r, b)
    ctx = (f"Ailsa saves {gbp(pay)} at the end of each year for {a} years, then stops but leaves the money invested for another {b} years. Bea saves nothing for {a} years, "
           f"then saves {gbp(pay)} at the end of each year for {b} years. The rate is {g(r * 100)}% effective per year.")
    parts = [part("(a)", f"Find Ailsa's balance at the end of {a + b} years.", r2(A), [f"{pay} × ({1 + r:g}^{a} − 1) ÷ {r:g} × {1 + r:g}^{b} = **{gbp(r2(A))}**"], [step(f"Value after {a} years", r2(fv_end(pay, r, a)))], marks=3),
             part("(b)", f"Find Bea's balance at the end of {a + b} years.", r2(B), [f"{pay} × ({1 + r:g}^{b} − 1) ÷ {r:g} = **{gbp(r2(B))}**"], marks=2),
             part("(c)", "Who paid in more, and who ends with more?", "Bea paid in more; Ailsa ends with more" if A > B else "Bea paid in more and ends with more",
                  [f"Paid in: Ailsa {gbp(pay * a)}, Bea {gbp(pay * b)}", "Saving earlier gives the money longer to earn interest."],
                  options=["Bea paid in more; Ailsa ends with more", "Bea paid in more and ends with more"], marks=1)]
    return question(T, "Savings Products and Pensions", ctx, parts, NOTES_STRATEGY, "Saving Earlier or Later")


# ── Inflation and insurance ────────────────────────────────────────────────────
def generate_price_index():
    y0 = random.choice([2016, 2018, 2019]); y1 = y0 + random.choice([4, 5, 6]); I1 = random.choice([118, 124, 130, 136]); basket = random.choice([60, 80, 90, 120])
    sav = random.choice([300, 400, 500, 600]); ratio = I1 / 100
    ctx = f"A price index for everyday goods was 100 in {y0} and {I1} in {y1}."
    parts = [part("(a)", f"A basket costing {gbp(basket)} in {y0} costs how much in {y1}?", r2(basket * ratio), [f"{basket} × {I1} ÷ 100 = **{gbp(r2(basket * ratio))}**"], marks=1),
             part("(b)", f"{gbp(sav)} in {y0} would buy goods worth how much in {y0} prices, if it had to be spent in {y1}?", r2(sav / ratio),
                  [f"{sav} ÷ {ratio:g} = **{gbp(r2(sav / ratio))}** of {y0} goods: purchasing power has fallen"], marks=2),
             part("(c)", f"Find the average yearly inflation rate (as a percentage, 2 d.p.).", round(((ratio) ** (1 / (y1 - y0)) - 1) * 100, 2),
                  [f"{ratio:g}^(1/{y1 - y0}) − 1 = **{((ratio) ** (1 / (y1 - y0)) - 1) * 100:.2f}%**"], marks=3)]
    return question(T, "Inflation and Insurance", ctx, parts, NOTES_PI, "Price Index and Purchasing Power")


def generate_insurance_expected():
    loss = random.choice([4000, 6000, 8000, 12000]); p = random.choice([1, 2, 3, 4]); prem = random.choice([60, 90, 140, 200])
    exp = loss * p / 100
    ctx = f"Contents insurance covers {gbp(loss)} of belongings and costs {gbp(prem)} a year. There is a {p}% chance of a claim-worthy burglary in a year."
    ans = "No: the premium is more than the expected cost" if prem > exp else "Yes: the premium is less than the expected cost"
    parts = [part("(a)", "Find the expected cost of a burglary in a year.", r2(exp), [f"{p / 100:g} × {loss} = **{gbp(r2(exp))}**"], marks=1),
             part("(b)", "On expected value alone, is the insurance worth buying?", ans,
                  [f"Premium {gbp(prem)} compared with expected cost {gbp(r2(exp))} → **{ans}**"],
                  options=["Yes: the premium is less than the expected cost", "No: the premium is more than the expected cost"], marks=1),
             part("(c)", "Give a reason a household might still buy it.", "It protects against a loss the household could not afford; insurance transfers the risk.",
                  ["Insurance protects against a loss that could not be afforded (risk transfer)."], explain=True, marks=1)]
    return question(T, "Inflation and Insurance", ctx, parts, "**Insurance.** Expected cost = probability × loss. Insurance can cost more than the expected loss and still be sensible, because it removes the risk of an unaffordable loss.", "Expected Cost of Insurance")


# ── Income tax / NI / property tax ─────────────────────────────────────────────
def generate_overtime_bonus():
    rate = random.choice([9.5, 10.25, 11.0, 12.5, 14.0]); hrs = random.choice([35, 37.5, 40]); mult = random.choice([1.5, 2.0]); ot = random.choice([4, 5, 6, 8])
    pct = random.choice([3, 4, 5, 6])
    basic = rate * hrs; over = mult * rate * ot; annual = basic * 52
    ctx = f"{random.choice(_NAMES)} earns £{rate:.2f} an hour for a {g(hrs)}-hour week. Overtime is paid at {'time and a half' if mult == 1.5 else 'double time'}."
    parts = [part("(a)", f"One week {ot} hours of overtime are worked. Find that week's gross pay.", r2(basic + over),
                  [f"Basic = {rate} × {hrs:g} = {gbp(r2(basic))}", f"Overtime = {mult:g} × {rate} × {ot} = {gbp(r2(over))}", f"Gross = **{gbp(r2(basic + over))}**"],
                  [step("Basic pay", r2(basic)), step("Overtime pay", r2(over))], marks=3),
             part("(b)", f"A bonus of {pct}% of annual basic pay (52 weeks, no overtime) is paid at the end of the year. Find the bonus.", r2(annual * pct / 100),
                  [f"Annual basic = {gbp(r2(annual))}; bonus = {pct}% × {gbp(r2(annual))} = **{gbp(r2(annual * pct / 100))}**"], [step("Annual basic pay", r2(annual))], marks=2)]
    return question(T, "Income Tax and National Insurance", ctx, parts, NOTES_PAY, "Overtime and Bonus")


def generate_pension_contributions():
    sal = random.choice(range(24000, 52001, 2000)); e = random.choice([5, 5.5, 6, 6.5, 7]); em = random.choice([15, 18, 20, 23])
    ctx = f"{random.choice(_NAMES)} earns {gbp(sal)} a year. Their superannuation scheme takes {e}% from the employee and the employer adds {em}%."
    parts = [part("(a)", "Find the employee's yearly contribution.", r2(sal * e / 100), [f"{e}% × {sal} = **{gbp(r2(sal * e / 100))}**"], marks=1),
             part("(b)", "Find the employer's yearly contribution.", r2(sal * em / 100), [f"{em}% × {sal} = **{gbp(r2(sal * em / 100))}**"], marks=1),
             part("(c)", "Find the total going into the pension each year.", r2(sal * (e + em) / 100), [f"**{gbp(r2(sal * (e + em) / 100))}**"], marks=1)]
    return question(T, "Income Tax and National Insurance", ctx, parts, NOTES_PAY, "Pension Contributions")


_LBTT = [(0, 145000, 0), (145000, 250000, 2), (250000, 325000, 5), (325000, 750000, 10), (750000, None, 12)]
_SDLT = [(0, 125000, 0), (125000, 250000, 2), (250000, 925000, 5), (925000, 1500000, 10), (1500000, None, 12)]


def _bands(price, bands):
    return sum(((min(price, hi) if hi is not None else price) - lo) * r / 100 for lo, hi, r in bands if price > lo)


def generate_stamp_duty():
    price = random.choice(range(180000, 320001, 10000))
    a, b = _bands(price, _LBTT), _bands(price, _SDLT)
    tbl = md_table(["Band", "LBTT (Scotland)", "Stamp duty (other system)"],
                   [["£0 – £125 000", "0%", "0%"], ["£125 000 – £145 000", "0%", "2%"], ["£145 000 – £250 000", "2%", "2%"], ["£250 000 – £325 000", "5%", "5%"],
                    ["Over £325 000 (not needed here)", "10%", "5%"]])
    ctx = f"A house costs {gbp(price)}. The tax is charged by band, only on the part of the price inside each band.\n\n{tbl}"
    parts = [part("(a)", "Find the LBTT payable.", r2(a), [f"LBTT = **{gbp(r2(a))}**"], marks=3),
             part("(b)", "Find the stamp duty payable in the other system.", r2(b), [f"Stamp duty = **{gbp(r2(b))}**"], marks=3),
             part("(c)", "How much more is the stamp duty than the LBTT?", r2(b - a), [f"{gbp(r2(b))} − {gbp(r2(a))} = **{gbp(r2(b - a))}**"], marks=1)]
    return question(T, "VAT and LBTT", ctx, parts, NOTES_SDLT, "Stamp Duty and LBTT")


FURTHER = {
    ("Finance", "Present Value"): {"Payment Patterns": generate_payment_patterns, "Working Backwards": generate_working_backwards,
                                   "Payments at Several Times": generate_payments_several_times},
    ("Finance", "Effective Interest Rates"): {"Comparing Products": generate_comparing_products, "Rates That Change": generate_rates_change},
    ("Finance", "Credit Cards"): {"Loans in All Forms": generate_loans_all_forms},
    ("Finance", "Loan Schedules"): {"Single, Interest-only and Level Repayments": generate_loan_forms, "Decreasing Repayments": generate_decreasing_repayments,
                                    "Repayment Holiday": generate_repayment_holiday},
    ("Finance", "Mortgages"): {"Repayment Holiday": generate_repayment_holiday, "Rate Rise and Affordability": generate_rate_rise},
    ("Finance", "Savings Products and Pensions"): {"Time to Reach a Goal": generate_time_to_goal, "Spend or Save, Loan or Savings": generate_spend_or_save,
                                                   "Saving Earlier or Later": generate_earlier_or_later},
    ("Finance", "Inflation and Insurance"): {"Price Index and Purchasing Power": generate_price_index, "Expected Cost of Insurance": generate_insurance_expected},
    ("Finance", "Income Tax and National Insurance"): {"Overtime and Bonus": generate_overtime_bonus, "Pension Contributions": generate_pension_contributions},
    ("Finance", "VAT and LBTT"): {"Stamp Duty and LBTT": generate_stamp_duty},
}
