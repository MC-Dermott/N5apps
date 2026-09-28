"""Higher Finance — Credit Cards.

Mirrors Credit_Cards_Worksheet.docx (Higher Apps/Worksheets/Finance). Convention from 2025 Q11: interest is
added at the end of the month (balance × (1 + annual)^(1/12)), THEN the minimum payment — 5% of the balance
or £5, whichever is higher — is made on the 1st. Traps: paying before adding interest (Candidate B), dividing
the annual rate by 12, ignoring the £5 floor, forgetting a balance-transfer fee.
"""
import random

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

from core.engine.spreadsheet_solution import (
    excel_round, multi_sheet_solution_metadata, solution_view, workbook_bytes,
)
from core.models.question_model import Question

TOPIC = "Finance"
QTYPE = "Credit Cards"
_NAMES = ["Freddie", "Eilidh", "Callum", "Mhairi", "Fiona", "Iona", "Ruaridh", "Kenny", "Seonag", "Donald"]

NOTES = """
**Credit cards**

1. **Interest first:** balance at the end of the month = balance × (1 + annual rate)^(1/12)
2. **Then the payment** on the 1st: minimum payment = 5% of that balance **or £5, whichever is higher**
3. Balance after the payment = end-of-month balance − payment

**Example:** Freddie's card has an annual effective rate of 29.9%. After his payment on 1 March his balance was £823.19
and he does not use the card in March. Calculate his balance on 1 April after the minimum payment.

- Monthly rate = 1.299^(1/12) − 1 = 2.205%
- Balance on 31 March = 823.19 × 1.299^(1/12) = £841.33
- Minimum payment = 5% of £841.33 = £42.07 (more than £5)
- Balance on 1 April = 841.33 − 42.07 = **£799.26**

⚠ Don't take off the payment before adding the interest (2025 marking instructions). A reason to pay the full
balance: to avoid interest / building up debt — "avoids going into debt" is **not** accepted.
"""


def _m(a):
    return (1 + a) ** (1 / 12) - 1


def _month(bal, i):
    it = round(bal * i + 1e-9, 2); b = round(bal + it, 2)
    pay = min(b, max(round(0.05 * b + 1e-9, 2), 5.0))
    return it, b, pay, round(b - pay, 2)


def generate_credit_cards_l1():
    """One month: interest, then the minimum payment (styled on 2025 Q11(a))."""
    name = random.choice(_NAMES); a = round(random.uniform(18.9, 34.9), 1)
    bal = round(random.uniform(150, 2500), 2); i = _m(a / 100)
    it, b, pay, after = _month(bal, i)
    q = (f"{name}'s credit card has an annual effective rate of interest of {a}%. Interest is added at the end of each month, "
         f"and the minimum payment (5% of the balance or £5, whichever is higher) is made on the 1st.\n\nAfter the last payment "
         f"the balance was £{bal:,.2f}, and the card is not used this month. Calculate the balance after the next minimum payment.")
    return Question(question_text=q, correct_answer=after, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Monthly effective rate, as a percentage (3 d.p.)", "answer": round(i * 100, 3)},
                                    {"prompt": "Balance at the end of the month, after interest (£)", "answer": b},
                                    {"prompt": "Minimum payment (£)", "answer": pay}],
                    worked_solution=[f"Monthly rate = {1 + a / 100:.3f}^(1/12) − 1 = {i * 100:.3f}%",
                                     f"End of month: {bal:,.2f} × {1 + a / 100:.3f}^(1/12) = £{b:,.2f}",
                                     f"Minimum payment = 5% of £{b:,.2f} = £{pay:,.2f}", f"Balance = £{after:,.2f}"],
                    notes=NOTES)


def generate_credit_cards_l2():
    """Three months of minimum payments."""
    name = random.choice(_NAMES); a = round(random.uniform(18.9, 29.9), 1)
    start = float(random.randrange(300, 2001, 10)); i = _m(a / 100)
    bal, lines, steps = start, [], []
    for k in range(3):
        it, b, pay, bal = _month(bal, i)
        lines.append(f"Month {k + 1}: interest £{it:.2f}, payment £{pay:.2f}, balance £{bal:,.2f}")
        steps.append({"prompt": f"Balance after payment {k + 1} (£)", "answer": bal})
    q = (f"{name} owes £{start:,.2f} on a credit card with an annual effective rate of interest of {a}%. Interest is added at "
         f"the end of each month, then {name} pays only the minimum (5% of the balance or £5, whichever is higher). The card "
         f"is not used.\n\nCalculate the balance after the third payment.")
    return Question(question_text=q, correct_answer=bal, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=steps[:2], worked_solution=[f"Monthly rate = {i * 100:.3f}%"] + lines, notes=NOTES)


def generate_credit_cards_l3():
    """The minimum payment, including the £5 floor."""
    bal = random.choice([round(random.uniform(20, 99.99), 2), round(random.uniform(100, 3000), 2)])
    pay = max(round(0.05 * bal + 1e-9, 2), 5.0)
    q = (f"A credit card's minimum payment is 5% of the balance or £5, whichever is higher.\n\n"
         f"Calculate the minimum payment on a balance of £{bal:,.2f}.")
    return Question(question_text=q, correct_answer=pay, topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "5% of the balance (£)", "answer": round(0.05 * bal, 2)}],
                    worked_solution=[f"5% of £{bal:,.2f} = £{0.05 * bal:,.2f}",
                                     f"Minimum payment = £{pay:,.2f}" + (" (5% is less than £5, so £5)" if pay == 5 else "")],
                    notes=NOTES)


def generate_credit_cards_l4():
    """Comparing a monthly rate with an annual rate: annual rate of the monthly card."""
    mp = random.choice([1.4, 1.6, 1.8, 1.9, 2.1, 2.3, 2.5]); a = round(random.uniform(18.9, 32.9), 1)
    ann = ((1 + mp / 100) ** 12 - 1) * 100
    q = (f"Card A charges an annual effective rate of {a}%. Card B charges {mp}% per month.\n\n"
         f"Calculate the annual effective rate of Card B, as a percentage to 2 decimal places.")
    return Question(question_text=q, correct_answer=round(ann, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": "Annual multiplier for Card B, (1 + monthly rate)^12 (5 d.p.)", "answer": round((1 + mp / 100) ** 12, 5)}],
                    worked_solution=[f"{1 + mp / 100:g}^12 − 1 = {ann:.2f}% per year",
                                     f"Card {'A' if a < ann else 'B'} is cheaper ({min(a, ann):.2f}% < {max(a, ann):.2f}%)"],
                    notes=NOTES)


def generate_credit_cards_l5():
    """Balance transfer: saving over the offer period (ignoring payments)."""
    bal = random.randrange(1000, 5001, 100); a = round(random.uniform(19.9, 29.9), 1)
    months = random.choice([12, 15, 18, 24]); fee = random.choice([2.5, 2.9, 3.0, 3.5])
    interest = bal * (1 + a / 100) ** (months / 12) - bal; f = bal * fee / 100
    q = (f"£{bal:,} is owed on a card with an annual effective rate of {a}%. Another card offers 0% interest for {months} months "
         f"on a balance transfer, with a {fee}% transfer fee.\n\nCalculate the saving over the {months} months (ignoring payments).")
    return Question(question_text=q, correct_answer=round(interest - f, 2), topic=TOPIC, question_type=QTYPE,
                    scaffold_steps=[{"prompt": f"Interest on the original card over {months} months (£)", "answer": round(interest, 2)},
                                    {"prompt": "Transfer fee (£)", "answer": round(f, 2)}],
                    worked_solution=[f"Interest = {bal:,} × {1 + a / 100:.3f}^({months}/12) − {bal:,} = £{interest:,.2f}",
                                     f"Fee = {fee}% of {bal:,} = £{f:,.2f}", f"Saving = £{interest - f:,.2f}"],
                    notes=NOTES)


# ---------------------------------------------------------------------------
# Spreadsheet: minimum payments vs a fixed payment (worksheet Section 3). Same sheet layout and
# formulas as Credit_Cards_Worksheet.xlsx's 'Q5 Minimum' / 'Q5 Minimum Fixed' sheets, plus a
# Summary sheet holding the graded cell.
# ---------------------------------------------------------------------------

SPREADSHEET_NOTES = """
**Credit card schedule in a spreadsheet**

Same layout as the worksheet's spreadsheet questions. Row 11 is month 1; fill each formula down:

- Monthly rate: **C5 = (1+C4)^(1/12)−1**
- Balance at start: **C11 = C3**, then **C12 = G11** (last month's balance after payment)
- Interest: **D11 = ROUND($C$5\\*C11,2)**; end of month: **E11 = C11+D11**
- Minimum payment: **F11 = MIN(E11, MAX(ROUND($C$6\\*E11,2), $C$7))** — the MIN stops a payment bigger
  than what is owed; the MAX applies the £5 floor. Fixed payment: **F11 = MIN(E11, $C$8)**
- Balance after payment: **G11 = E11−F11**
- Summary: months to clear = **COUNTIF(F11:F410,">0")**; total interest = **SUM(D11:D410)**

⚠ Forgetting the £5 floor means the balance never reaches zero. Compare the **total interest**, not the
payments. Save the file before uploading.
"""

_ROWS = 400
_FIRST = 11
_LAST = _FIRST + _ROWS - 1
_SS_HEADER_FILL = PatternFill("solid", fgColor="1F3864")
_SS_ANSWER_FILL = PatternFill("solid", fgColor="FFFF00")


def _card_schedule(bal, i, fixed=None):
    """(start, interest, end, payment, after) per month until the card is cleared.

    Mirrors the sheet's arithmetic exactly: E = C+D and G = E−F are never rounded, so the same
    float drift a pupil's spreadsheet accumulates (198.699999999999 rather than 198.70) is here
    too — it occasionally decides which way ROUND(5% of E) goes."""
    rows = []
    while bal > 0 and len(rows) < _ROWS:
        interest = excel_round(i * bal)
        end = bal + interest
        pay = min(end, fixed) if fixed else min(end, max(excel_round(0.05 * end), 5.0))
        after = end - pay
        rows.append((bal, interest, end, pay, after))
        bal = after
    return rows


def _card_sheet(ws, title, bal, annual, fixed, rows, solution):
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 32
    for col in "CDEFG":
        ws.column_dimensions[col].width = 16
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=13)
    for r, label in [(3, "Starting balance (£)"), (4, "Annual effective rate"), (5, "Monthly effective rate"),
                     (6, "Minimum payment: % of balance"), (7, "Minimum payment: at least (£)"), (8, "Fixed payment (£)")]:
        ws[f"B{r}"] = label
    ws["C3"], ws["C4"], ws["C6"], ws["C7"] = bal, annual, 0.05, 5
    ws["C3"].number_format = ws["C7"].number_format = "#,##0.00"
    ws["C4"].number_format = ws["C5"].number_format = "0.000%"
    ws["C6"].number_format = "0%"
    if fixed:
        ws["C8"] = fixed
        ws["C8"].number_format = "#,##0.00"
    for col, text in zip("BCDEFG", ["Month", "Balance at start (£)", "Interest (£)", "Balance at end of month (£)",
                                    "Payment on the 1st (£)", "Balance after payment (£)"]):
        cell = ws[f"{col}10"]
        cell.value, cell.fill, cell.font = text, _SS_HEADER_FILL, Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    ws.row_dimensions[10].height = 45

    filled = ["C5"] + [f"{c}{r}" for r in range(_FIRST, _LAST + 1) for c in "CDEFG"]
    values = {}
    if solution:
        ws["C5"] = "=(1+C4)^(1/12)-1"
        values["C5"] = (1 + annual) ** (1 / 12) - 1
    pay_formula = "MIN(E{r},$C$8)" if fixed else "MIN(E{r},MAX(ROUND($C$6*E{r},2),$C$7))"
    for k in range(_ROWS):
        r = _FIRST + k
        ws[f"B{r}"] = k + 1
        for c in "CDEFG":
            ws[f"{c}{r}"].number_format = "#,##0.00"
        if solution:
            ws[f"C{r}"] = "=C3" if k == 0 else f"=G{r - 1}"
            ws[f"D{r}"] = f"=ROUND($C$5*C{r},2)"
            ws[f"E{r}"] = f"=C{r}+D{r}"
            ws[f"F{r}"] = "=" + pay_formula.format(r=r)
            ws[f"G{r}"] = f"=E{r}-F{r}"
            vals = rows[k] if k < len(rows) else (0.0, 0.0, 0.0, 0.0, 0.0)
            values.update({f"{c}{r}": v for c, v in zip("CDEFG", vals)})
    for ref in filled:
        ws[ref].fill = _SS_ANSWER_FILL
    return values, filled


def _build_card_workbooks(title, bal, annual, fixed, min_rows, fix_rows):
    summary = [
        (3, "Months to clear — minimum payments", "=COUNTIF(Minimum!F11:F{L},\">0\")", len(min_rows), "0"),
        (4, "Total interest — minimum payments (£)", "=SUM(Minimum!D11:D{L})", round(sum(r[1] for r in min_rows), 2), "#,##0.00"),
        (5, "Months to clear — fixed payments", "=COUNTIF(Fixed!F11:F{L},\">0\")", len(fix_rows), "0"),
        (6, "Total interest — fixed payments (£)", "=SUM(Fixed!D11:D{L})", round(sum(r[1] for r in fix_rows), 2), "#,##0.00"),
        (7, "Interest saved by paying the fixed amount (£)", "=C4-C6",
         round(sum(r[1] for r in min_rows) - sum(r[1] for r in fix_rows), 2), "#,##0.00"),
    ]
    out = []
    for solution in (False, True):
        wb = Workbook()
        ws_min = wb.active
        ws_min.title = "Minimum"
        ws_fix = wb.create_sheet("Fixed")
        ws_sum = wb.create_sheet("Summary")
        v_min, f_min = _card_sheet(ws_min, f"{title} — minimum payments", bal, annual, None, min_rows, solution)
        v_fix, f_fix = _card_sheet(ws_fix, f"{title} — fixed payments of £{fixed}", bal, annual, fixed, fix_rows, solution)
        ws_sum.column_dimensions["B"].width = 46
        ws_sum.column_dimensions["C"].width = 16
        ws_sum["A1"] = f"{title} — summary"
        ws_sum["A1"].font = Font(bold=True, size=13)
        v_sum, f_sum = {}, []
        for r, label, formula, value, fmt in summary:
            ws_sum[f"B{r}"] = label
            ref = f"C{r}"
            ws_sum[ref].number_format = fmt
            ws_sum[ref].fill = _SS_ANSWER_FILL
            f_sum.append(ref)
            if solution:
                ws_sum[ref] = formula.format(L=_LAST)
                v_sum[ref] = value
        ws_sum["B9"] = ("Completed solution: the yellow cells show the formulas used." if solution
                        else "Fill in the yellow cells on all three sheets, save the file, then upload it.")
        ws_sum["B9"].font = Font(italic=True)
        out.append((wb, (ws_sum, v_sum, f_sum), (ws_min, v_min, f_min), (ws_fix, v_fix, f_fix)))
    return out, summary[-1][3]


def generate_credit_cards_l6():
    """Spreadsheet: minimum payments vs a fixed payment — months to clear, total interest, interest saved."""
    name = random.choice(_NAMES)
    title = random.choice(["Only the Minimum?", "The Store Card", "Clearing the Card", "A Holiday on Credit"])
    bal = float(random.randrange(500, 3001, 10))
    a = round(random.uniform(18.9, 34.9), 1)
    i = _m(a / 100)
    fixed = int(round(bal * random.uniform(0.045, 0.08) / 5) * 5)
    fixed = max(fixed, int(-(-(excel_round(0.05 * bal * (1 + i)) + 1) // 5) * 5))   # above the first minimum payment
    min_rows = _card_schedule(bal, i)
    fix_rows = _card_schedule(bal, i, fixed)
    (q_book, s_book), saved = _build_card_workbooks(title, bal, a / 100, fixed, min_rows, fix_rows)

    q_wb = q_book[0]
    wb, *sheets = s_book
    views = [solution_view(ws, v, f, 3, 7, 2, 3) if ws.title == "Summary" else
             solution_view(ws, v, f, 3, _FIRST + len(rows), 2, 7)
             for (ws, v, f), rows in zip(sheets, [None, min_rows, fix_rows])]
    int_min = round(sum(r[1] for r in min_rows), 2)
    int_fix = round(sum(r[1] for r in fix_rows), 2)

    q = (f"{name} owes £{bal:,.2f} on a credit card with an annual effective rate of interest of {a}%. Interest is added at "
         f"the end of each month and a payment is made on the 1st. The card is not used again.\n\n"
         f"Download the spreadsheet below.\n"
         f"- On the **Minimum** sheet, find how many months it takes to clear the debt paying only the minimum "
         f"(5% of the balance or £5, whichever is higher), and the total interest.\n"
         f"- On the **Fixed** sheet, repeat with a fixed payment of £{fixed} a month.\n"
         f"- On the **Summary** sheet, record your results and calculate how much interest is saved by paying the "
         f"fixed amount (cell C7).\n\nSave the file and upload it here.")
    return Question(
        question_text=q, correct_answer=saved, topic=TOPIC, question_type=QTYPE,
        scaffold_steps=[
            {"prompt": "Monthly effective rate, as a percentage (3 d.p.)", "answer": round(i * 100, 3)},
            {"prompt": "Minimum payment made in month 1 (£)", "answer": min_rows[0][3]},
            {"prompt": "Months to clear the debt paying only the minimum", "answer": len(min_rows)},
            {"prompt": "Total interest paying only the minimum (£)", "answer": int_min},
            {"prompt": f"Months to clear the debt paying £{fixed} a month", "answer": len(fix_rows)},
            {"prompt": f"Total interest paying £{fixed} a month (£)", "answer": int_fix},
        ],
        worked_solution=[
            f"Monthly rate = {1 + a / 100:.3f}^(1/12) − 1 = {i * 100:.3f}%",
            f"Minimum payments: F11 = MIN(E11, MAX(ROUND($C$6*E11,2), $C$7)), filled down → cleared in "
            f"{len(min_rows)} months ({len(min_rows) // 12} years {len(min_rows) % 12} months), total interest £{int_min:,.2f}",
            f"Fixed £{fixed}: F11 = MIN(E11, $C$8), filled down → cleared in {len(fix_rows)} months, "
            f"total interest £{int_fix:,.2f}",
            f"Interest saved = {int_min:,.2f} − {int_fix:,.2f} = £{saved:,.2f}, and the debt is cleared "
            f"{len(min_rows) - len(fix_rows)} months sooner",
        ],
        notes=SPREADSHEET_NOTES,
        metadata={
            "spreadsheet_bytes": workbook_bytes(q_wb),
            "spreadsheet_filename": f"credit_card_{name.lower()}.xlsx",
            "spreadsheet_answer_cell": ("Summary", "C7"),
            **multi_sheet_solution_metadata(wb, views, f"credit_card_{name.lower()}_solution.xlsx"),
        })


# The non-spreadsheet question types, grouped as one "Calculator Questions" entry in the app and
# weighted toward what the 2023–2026 past papers actually ask (see the comments).
_CALCULATOR_MIX = [
    (generate_credit_cards_l1, 5),          # one month: interest, then the minimum payment — 2025 Q11(a)
    (generate_credit_cards_l2, 2),          # three months of minimum payments
    (generate_credit_cards_l3, 2),          # the minimum payment's £5 floor
    (generate_credit_cards_l4, 1),          # comparing a monthly and an annual rate — not yet examined
    (generate_credit_cards_l5, 1),          # balance transfer — not yet examined
]


def generate_credit_cards_calculator():
    generator = random.choices([g for g, _ in _CALCULATOR_MIX], weights=[w for _, w in _CALCULATOR_MIX])[0]
    return generator()


def generate_credit_cards_question():
    return random.choice([generate_credit_cards_calculator, generate_credit_cards_l6])()
