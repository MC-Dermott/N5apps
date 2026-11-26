"""Higher Finance — levels filling the gaps found when the prelim learning outcomes were mapped to the app (Nov 2026):
purpose and risks of borrowing, credit cards, savings and insurance; change of loan term; appreciation and
depreciation; payments in another currency; comparing tax systems. All interest rates are effective rates."""
import random

from core.models.further import g, gbp, md_table, mon, part, pmt, question, r2, step

T = "Finance"

NOTES_RISK = """
**Purpose and risks.** Say what the product is *for*, then who could lose out and how. Borrowing has risks for the
**borrower** (repayments become unaffordable, rates rise, a missed payment damages the credit record, the home or goods
can be repossessed) and for the **lender** (the borrower defaults and the money is not recovered). Savings can lose
**purchasing power** if the interest rate is below inflation, may be locked away, and investments can fall in value.
Insurance moves a large, uncertain loss to the insurer in exchange for a certain premium; an **excess** and
**exclusions** limit what is paid.
"""

# Each item: (question, correct option, [wrong options])
_BORROWING = [
    ("What is the main purpose of a loan?", "To pay for something now and repay the money, with interest, over an agreed time",
     ["To earn interest on money you already have", "To protect you against an unexpected loss"]),
    ("In a loan, what is the capital?", "The amount borrowed that is still to be repaid",
     ["The extra charge made for borrowing", "The total of all the repayments"]),
    ("In a loan, what is the interest?", "The charge for borrowing the capital",
     ["The part of each repayment that reduces the debt", "The amount first borrowed"]),
    ("Which is a risk to the **borrower**?", "A rise in interest rates makes the repayments unaffordable",
     ["The customer does not pay the money back, so the lender loses it", "The lender receives interest each month"]),
    ("Which is a risk to the **lender**?", "The borrower defaults and the full amount is not recovered",
     ["The borrower's credit record is damaged", "The borrower's repayments go up"]),
    ("A mortgage is secured on the house. What risk does this create for the borrower?", "The home can be repossessed if repayments are missed",
     ["The house cannot be redecorated", "The interest rate can never change"]),
    ("What is **negative equity**?", "The house is worth less than the mortgage still owed on it",
     ["The borrower has paid more interest than capital", "The interest rate is below inflation"]),
    ("A fixed rate on a mortgage ends after 2 years. What is the main risk?", "The new rate may be higher, so the repayments rise",
     ["The loan must be taken out again from the start", "The capital already repaid is added back on"]),
]
_CARDS = [
    ("What is a main purpose of a credit card?", "To buy things now and pay later, borrowing up to an agreed limit",
     ["To spend only money already in your bank account", "To save regularly for retirement"]),
    ("When is no interest usually charged on purchases?", "When the full balance is paid off by the due date each month",
     ["When at least the minimum payment is made", "When the card is used for cash withdrawals"]),
    ("Why is paying only the minimum risky?", "The debt takes a long time to clear and much more interest is paid",
     ["The credit limit is removed", "The balance can never go down"]),
    ("What is a risk of using the card to withdraw cash?", "There is usually a fee and interest is charged straight away",
     ["The cash cannot be spent in shops", "The withdrawal is not added to the balance"]),
    ("What is a risk with a 0% introductory offer?", "A much higher rate applies to what is still owed when the offer ends",
     ["The balance is doubled when the offer ends", "No repayments are allowed during the offer"]),
    ("Which is a possible result of missing payments?", "A late-payment charge and a damaged credit record",
     ["A lower interest rate", "The debt is automatically cancelled"]),
]
_SAVINGS = [
    ("What is the main advantage of an instant-access account?", "The money can be taken out at any time without a penalty",
     ["It always pays the highest rate", "The government adds a 25% bonus"]),
    ("What is the main drawback of a fixed-rate bond?", "The money is tied up for the term, or a penalty is paid to get it early",
     ["The rate can fall during the term", "Only one payment of interest is ever allowed to be earned"]),
    ("Why might someone use an ISA?", "The interest or returns are free of tax",
     ["The value can never fall", "It pays a bonus on every withdrawal"]),
    ("What is a Lifetime ISA designed for?", "Saving for a first home or for later life, with a government bonus",
     ["Borrowing to buy a car", "Paying everyday bills"]),
    ("What is the purpose of a pension?", "Saving over a working life to give an income in retirement",
     ["Protecting a house against damage", "Borrowing against future wages"]),
    ("Inflation is 4% and a savings account pays 2.5% a year. What is the risk?", "The savings lose purchasing power even though the balance grows",
     ["The balance in the account falls", "The bank keeps the interest"]),
    ("What is a risk of a pension invested in the stock market?", "The investments can fall in value, so the pension may be smaller than planned",
     ["Contributions cannot be made monthly", "The pension is paid before retirement"]),
    ("What is a risk of not saving at all?", "A sudden cost may have to be met by expensive borrowing",
     ["Interest is charged on money not saved", "Income tax is doubled"]),
]
_INSURANCE = [
    ("What is the purpose of insurance?", "To pay a premium so that a large, uncertain loss is covered by the insurer",
     ["To earn interest on regular payments", "To borrow money when something goes wrong"]),
    ("What is an **excess**?", "The part of a claim that the policyholder pays",
     ["The yearly cost of the policy", "The most the insurer will pay"]),
    ("What usually happens to the premium if the excess is increased?", "It goes down, but the policyholder pays more of any claim",
     ["It goes up, and every claim is paid in full", "It stays the same"]),
    ("Which insurance covers the structure of a house?", "Buildings insurance",
     ["Contents insurance", "Life insurance"]),
    ("Which insurance covers furniture and belongings?", "Contents insurance",
     ["Buildings insurance", "Travel insurance"]),
    ("Which insurance pays money to dependants if the policyholder dies?", "Life insurance",
     ["Pet insurance", "Buildings insurance"]),
    ("What is the main risk of **not** having travel insurance?", "A large medical or cancellation cost may have to be paid in full",
     ["The holiday cannot be booked", "The flight price rises"]),
    ("What is a risk even when you are insured?", "An exclusion in the policy means a claim is refused",
     ["The premium is paid back as a loss", "The insurer charges interest on the claim"]),
]

_EXPLAIN = {
    "borrow": ("Give one risk of borrowing for the borrower and one for the lender. (Reveal the expected answer.)",
               "Borrower: repayments become unaffordable / rates rise / credit record damaged / repossession. Lender: the borrower defaults and the money is lost."),
    "card": ("Explain why paying the balance in full each month is sensible. (Reveal the expected answer.)",
             "No interest is charged, so nothing extra is paid and the debt cannot build up."),
    "save": ("Give one reason to choose an account with a lower interest rate. (Reveal the expected answer.)",
             "e.g. instant access to the money, no penalty for withdrawals, or lower risk."),
    "insure": ("Explain why someone might buy insurance even though the premium is more than the expected cost. (Reveal the expected answer.)",
               "They could not afford the full loss; insurance removes that risk."),
}


def _mcq(bank, explain_key, qtype, level):
    picked = random.sample(bank, 3)
    parts = []
    for label, (q, right, wrong) in zip(["(a)", "(b)", "(c)"], picked):
        opts = [right] + wrong
        random.shuffle(opts)
        parts.append(part(label, q, right, [f"**{right}**"], marks=1, options=opts))
    q, a = _EXPLAIN[explain_key]
    parts.append(part("(d)", q, a, [a], marks=2, explain=True))
    return question(T, qtype, "", parts, NOTES_RISK, level)


def generate_borrowing_risks():
    return _mcq(_BORROWING, "borrow", "Loan Schedules", "Purpose and Risks of Borrowing")


def generate_card_risks():
    return _mcq(_CARDS, "card", "Credit Cards", "Purpose and Risks of Credit Cards")


def generate_savings_risks():
    return _mcq(_SAVINGS, "save", "Savings Products and Pensions", "Purpose and Risks of Savings")


def generate_insurance_risks():
    return _mcq(_INSURANCE, "insure", "Inflation and Insurance", "Purpose and Risks of Insurance")


# ── change of loan term ────────────────────────────────────────────────────────
NOTES_TERM = """
**Changing the term.** Find the loan still outstanding on the date of the change (it is the present value of the
repayments still to be made), then work out a new level repayment for the new number of months. A longer term gives a
smaller repayment but **more interest in total**.
"""


def generate_change_of_term():
    loan = random.choice(range(6000, 20001, 1000))
    rate = random.choice([6.4, 7.2, 8.5, 9.9, 11.3])
    n = random.choice([36, 48])
    done = random.choice([12, 18])
    new_left = (n - done) + random.choice([12, 18, 24])
    i = mon(rate / 100)
    old = r2(pmt(loan, i, n))
    out = r2(old * (1 - (1 + i) ** -(n - done)) / i)
    new = r2(pmt(out, i, new_left))
    extra = r2(new * new_left - old * (n - done))
    ctx = (f"A loan of {gbp(loan)} at an annual effective rate of {rate}% is being repaid by {n} level monthly repayments of "
           f"{gbp(old)}. Just after repayment {done}, the borrower asks to spread what is left over **{new_left}** more months "
           f"instead of {n - done}. (Ignore the small adjustment to the final repayment.)")
    parts = [
        part("(a)", "Calculate the loan outstanding just after repayment " + str(done) + " (the present value of the repayments left).", out,
             [f"Monthly rate = {1 + rate / 100:g}^(1/12) − 1 = {i:.6f}",
              f"{old} × (1 − (1 + i)^−{n - done}) ÷ i = **{gbp(out)}**"], [step("Monthly rate, as a decimal", round(i, 6))], marks=3),
        part("(b)", "Calculate the new monthly repayment.", new, [f"{out} × i ÷ (1 − (1 + i)^−{new_left}) = **{gbp(new)}**"], marks=2),
        part("(c)", "How much more is paid in total from this point because of the change?", extra,
             [f"{new_left} × {new} − {n - done} × {old} = **{gbp(extra)}**"],
             [step("Total still to pay under the old term", r2(old * (n - done))), step("Total to pay under the new term", r2(new * new_left))], marks=2),
    ]
    return question(T, "Loan Schedules", ctx, parts, NOTES_TERM, "Change of Term")


# ── appreciation and depreciation ──────────────────────────────────────────────
NOTES_APP = """
**Appreciation and depreciation** are compound changes: multiply by (1 + r) for a rise and (1 − r) for a fall, once for
every year. Different rates in different years are multiplied one after another. To work backwards, **divide**.
"""


def generate_appreciation():
    start = random.choice(range(12000, 32001, 1000))
    d1 = random.choice([15, 18, 20, 25])
    d2 = random.choice([8, 10, 12])
    n = random.choice([2, 3, 4])
    val = r2(start * (1 - d1 / 100) * (1 - d2 / 100) ** n)
    house = random.choice(range(150000, 300001, 5000))
    up = random.choice([2.5, 3, 3.5, 4.2])
    yrs = random.choice([3, 4, 5])
    now = round(house * (1 + up / 100) ** yrs)
    ctx = (f"A van costing {gbp(start)} loses {d1}% of its value in the first year and {d2}% a year after that. A flat has "
           f"risen in value by {up}% a year for {yrs} years and is now worth {gbp(now)}.")
    parts = [
        part("(a)", f"Find the value of the van after {n + 1} years.", val,
             [f"{start} × {1 - d1 / 100:g} × {1 - d2 / 100:g}^{n} = **{gbp(val)}**"],
             [step("Value after 1 year", r2(start * (1 - d1 / 100)))], marks=3),
        part("(b)", f"Find the flat's value {yrs} years ago, to the nearest £100.", round(now / (1 + up / 100) ** yrs, -2),
             [f"{now} ÷ {1 + up / 100:g}^{yrs} = **{gbp(int(round(now / (1 + up / 100) ** yrs, -2)))}**"], marks=2),
    ]
    return question(T, "Interest", ctx, parts, NOTES_APP, "Appreciation and Depreciation")


# ── payments in another currency ───────────────────────────────────────────────
NOTES_FX = """
**Payments in another currency.** Change every amount into the **same currency** before adding or comparing, then use
the interest rate of the account the money is in. Pounds → foreign: multiply by the rate. Foreign → pounds: divide.
"""


def generate_other_currency():
    cur, sym, fx = random.choice([("euros", "€", 1.16), ("euros", "€", 1.18), ("US dollars", "$", 1.27), ("US dollars", "$", 1.32)])
    amount = random.choice(range(6000, 24001, 2000))
    yrs = random.choice([2, 3, 4])
    r = random.choice([2.8, 3.1, 3.6, 4.2])
    gbp_needed = amount / fx
    dep = r2(gbp_needed / (1 + r / 100) ** yrs)
    new_fx = r2(fx - random.choice([0.06, 0.08, 0.1]))
    short = r2(amount / new_fx - gbp_needed)
    ctx = (f"A student will have to pay a fee of {sym}{amount:,} in {yrs} years. The savings account is in pounds and pays "
           f"{r}% effective per year. The exchange rate is £1 = {sym}{fx:.2f}.")
    parts = [
        part("(a)", "Using today's exchange rate, find the fee in pounds.", r2(gbp_needed), [f"{amount} ÷ {fx} = **{gbp(r2(gbp_needed))}**"], marks=1),
        part("(b)", "Find the single deposit needed now to have this amount when the fee is due.", dep,
             [f"{r2(gbp_needed)} ÷ {1 + r / 100:g}^{yrs} = **{gbp(dep)}**"], marks=2),
        part("(c)", f"When the fee is paid, £1 = {sym}{new_fx:.2f}. How much extra, in pounds, must the student find?", short,
             [f"{amount} ÷ {new_fx} − {r2(gbp_needed)} = **{gbp(short)}**"], [step("Fee in pounds at the new rate", r2(amount / new_fx))], marks=2),
    ]
    return question(T, "Present Value", ctx, parts, NOTES_FX, "Payments in Another Currency")


# ── comparing tax systems ──────────────────────────────────────────────────────
NOTES_TAXCOMPARE = """
**Comparing tax systems.** Work out each system separately from the **taxable** income, band by band: each rate applies
only to the part of the income inside its band. Then compare the totals, or the percentage of gross pay taken
(total tax ÷ gross pay).
"""


def _tax(taxable, bands):
    total, low = 0.0, 0
    for top, rate in bands:
        hi = taxable if top is None else min(taxable, top)
        if hi > low:
            total += (hi - low) * rate / 100
        if top is None or taxable <= top:
            break
        low = top
    return total


def _band_rows(bands):
    rows, low = [], 0
    for top, rate in bands:
        rows.append([f"over £{low:,}" if top is None else (f"first £{top:,}" if not low else f"£{low:,} to £{top:,}"), f"{rate}%"])
        low = top
    return rows


def generate_compare_tax_systems():
    pa_a, pa_b = 12000, 10000
    a = [(3000, 19), (15000, 20), (31000, 21), (None, 42)]
    b = [(35000, random.choice([22, 23, 24])), (None, 40)]
    gross = random.choice(range(24000, 60001, 2000))
    ta, tb = gross - pa_a, gross - pa_b
    xa, xb = r2(_tax(ta, a)), r2(_tax(tb, b))
    ctx = (f"Two countries tax a salary of {gbp(gross)}.\n\n**Country A** has a tax-free allowance of {gbp(pa_a)}. Rates on taxable income:\n\n"
           + md_table(["Taxable income", "Rate"], _band_rows(a))
           + f"\n\n**Country B** has a tax-free allowance of {gbp(pa_b)}. Rates on taxable income:\n\n"
           + md_table(["Taxable income", "Rate"], _band_rows(b)))
    higher = "Country A" if xa > xb else "Country B"
    parts = [
        part("(a)", "Find the yearly income tax in Country A.", xa, [f"Taxable = {gbp(ta)}; tax = **{gbp(xa)}**"], [step("Taxable income", ta)], marks=3),
        part("(b)", "Find the yearly income tax in Country B.", xb, [f"Taxable = {gbp(tb)}; tax = **{gbp(xb)}**"], [step("Taxable income", tb)], marks=2),
        part("(c)", "Which country takes more tax from this salary?", higher, [f"**{higher}** by {gbp(r2(abs(xa - xb)))}"], options=["Country A", "Country B"], marks=1),
        part("(d)", "In the higher-tax country, what percentage of the gross salary is taken in tax? (1 d.p.)",
             round(max(xa, xb) / gross * 100, 1), [f"{max(xa, xb)} ÷ {gross} × 100 = **{max(xa, xb) / gross * 100:.1f}%**"], marks=1),
    ]
    return question(T, "Income Tax and National Insurance", ctx, parts, NOTES_TAXCOMPARE, "Comparing Tax Systems")


GAPS = {
    ("Finance", "Loan Schedules"): {"Purpose and Risks of Borrowing": generate_borrowing_risks, "Change of Term": generate_change_of_term},
    ("Finance", "Credit Cards"): {"Purpose and Risks of Credit Cards": generate_card_risks},
    ("Finance", "Savings Products and Pensions"): {"Purpose and Risks of Savings": generate_savings_risks},
    ("Finance", "Inflation and Insurance"): {"Purpose and Risks of Insurance": generate_insurance_risks},
    ("Finance", "Interest"): {"Appreciation and Depreciation": generate_appreciation},
    ("Finance", "Present Value"): {"Payments in Another Currency": generate_other_currency},
    ("Finance", "Income Tax and National Insurance"): {"Comparing Tax Systems": generate_compare_tax_systems},
}
