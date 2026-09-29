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
from core.models.question_model import Question, make_part, multipart_worked_solution

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


# ---------------------------------------------------------------------------
# Spreadsheet: a fixed monthly payment, and a change part-way through — the payment goes up, a payment
# holiday, or a change of interest rate. One sheet in the same column layout as the Minimum/Fixed
# sheets (row 11 = month 1), with the change's details in H3:I5 and the results in H6:I8.
# ---------------------------------------------------------------------------

CHANGE_NOTES = """
**A fixed payment, and a change part-way through**

- Payment: **F11 = MIN(E11, $C$6)** — never more than is owed; fill down until the balance reaches £0
- Months to clear = the last month with a payment; total interest = **SUM** of the interest column
- **Payment goes up:** from the month of the change the payment uses the new amount (**MIN(E…, $I$4)**).
  Interest saved = total interest before − total interest now
- **Payment holiday:** the payment is **0** in the holiday months, but interest is still added, so the
  balance grows. Extra interest = total interest now − total interest before
- **Change of rate:** from the month the new rate starts, the interest uses the new monthly rate
  (**ROUND($I$5\\*C…,2)**)
"""

_CHANGE_GRID = 60


def _fixed_run(bal, terms):
    """(start, interest, end, payment, after) per month until cleared, where terms(t) gives month t's
    (monthly rate, payment); the payment is never more than is owed. Same arithmetic as _card_schedule()."""
    rows = []
    for t in range(1, _ROWS + 1):
        i, pay_t = terms(t)
        interest = excel_round(i * bal)
        end = bal + interest
        pay = min(end, pay_t)
        rows.append((bal, interest, end, pay, end - pay))
        bal = end - pay
        if bal <= 0:
            break
    return rows


def _fixed_sheet(title, bal, annual, fixed, rows, *, extras=(), fills, pay_ref, rate_ref, answer):
    """Question bytes, graded cell and solution metadata for a one-sheet fixed-payment card schedule.
    `extras` — (row, label, value, format) given in H/I; `fills` — (row, label, formula_or_value, value,
    format) pupils complete in H/I; pay_ref(t) / rate_ref(t) — month t's payment cell (or 0) and rate cell."""
    last = _FIRST + len(rows) - 1

    def base(months, solution):
        wb = Workbook()
        ws = wb.active
        ws.title = "Card"
        ws.column_dimensions["A"].width = 3
        ws.column_dimensions["B"].width = 30
        for col in "CDEFG":
            ws.column_dimensions[col].width = 16
        ws.column_dimensions["H"].width = 38
        ws.column_dimensions["I"].width = 16
        ws["A1"] = title
        ws["A1"].font = Font(bold=True, size=13)
        ws["A2"] = ("Completed solution: the yellow cells show the formulas used." if solution
                    else "Fill in the yellow cells, save the file, then upload it.")
        ws["A2"].font = Font(italic=True)
        for r, label in [(3, "Starting balance (£)"), (4, "Annual effective rate"), (5, "Monthly effective rate"),
                         (6, "Monthly payment (£)")]:
            ws[f"B{r}"] = label
        ws["C3"], ws["C4"], ws["C6"] = bal, annual, fixed
        ws["C3"].number_format = ws["C6"].number_format = "#,##0.00"
        ws["C4"].number_format = ws["C5"].number_format = "0.000%"
        for row, label, value, fmt in extras:
            ws[f"H{row}"], ws[f"I{row}"] = label, value
            ws[f"I{row}"].number_format = fmt
        for row, label, _, _, fmt in fills:
            ws[f"H{row}"] = label
            ws[f"I{row}"].number_format = fmt
        for col, text in zip("BCDEFG", ["Month", "Balance at start (£)", "Interest (£)", "Balance at end of month (£)",
                                        "Payment on the 1st (£)", "Balance after payment (£)"]):
            cell = ws[f"{col}10"]
            cell.value, cell.fill, cell.font = text, _SS_HEADER_FILL, Font(color="FFFFFF", bold=True)
            cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
        ws.row_dimensions[10].height = 45
        for k in range(months):
            r = _FIRST + k
            ws[f"B{r}"] = k + 1
            for c in "CDEFG":
                ws[f"{c}{r}"].number_format = "#,##0.00"
        return wb, ws

    head = ["C5"] + [f"I{row}" for row, *_ in fills]
    wb, ws = base(_CHANGE_GRID, False)
    for ref in head + [f"{c}{r}" for r in range(_FIRST, _FIRST + _CHANGE_GRID) for c in "CDEFG"]:
        ws[ref].fill = _SS_ANSWER_FILL
    question_bytes = workbook_bytes(wb)

    wb, ws = base(len(rows), True)
    ws["C5"] = "=(1+C4)^(1/12)-1"
    values = {"C5": (1 + annual) ** (1 / 12) - 1}
    for row, _, content, value, _ in fills:
        ws[f"I{row}"] = content
        values[f"I{row}"] = value
    for t, (start, interest, end, pay, after) in enumerate(rows, 1):
        r = _FIRST + t - 1
        ws[f"C{r}"] = "=C3" if t == 1 else f"=G{r - 1}"
        ws[f"D{r}"] = f"=ROUND({rate_ref(t)}*C{r},2)"
        ws[f"E{r}"] = f"=C{r}+D{r}"
        ref = pay_ref(t)
        ws[f"F{r}"] = f"=MIN(E{r},{ref})" if ref else 0
        ws[f"G{r}"] = f"=E{r}-F{r}"
        values.update({f"{c}{r}": v for c, v in zip("CDEFG", (start, interest, end, pay, after))})
    filled = head + [f"{c}{r}" for r in range(_FIRST, last + 1) for c in "CDEFG"]
    for ref in filled:
        ws[ref].fill = _SS_ANSWER_FILL
    view = solution_view(ws, values, filled, 3, last, 2, 9)
    return {"spreadsheet_bytes": question_bytes, "spreadsheet_filename": "credit_card_schedule.xlsx",
            "spreadsheet_answer_cell": ("Card", answer),
            **multi_sheet_solution_metadata(wb, [view], "credit_card_schedule_solution.xlsx")}


def _card_plan():
    name = random.choice(_NAMES)
    bal = float(random.randrange(600, 3001, 10))
    a = round(random.uniform(18.9, 32.9), 1)
    i = _m(a / 100)
    fixed = max(25, int(round(bal * random.uniform(0.05, 0.1) / 5) * 5))
    base = _fixed_run(bal, lambda t: (i, fixed))
    return dict(name=name, bal=bal, a=a, i=i, fixed=fixed, base=base, months=len(base),
                interest=round(sum(r[1] for r in base), 2))


def _card_title(p, subtitle):
    return f"{p['name']}'s Credit Card — {subtitle}"


def _results(rows):
    last = _FIRST + len(rows) - 1
    total = round(sum(r[1] for r in rows), 2)
    return last, total, [(6, "Months to clear the balance", len(rows), len(rows), "0"),
                         (7, "Total interest (£)", f"=SUM(D{_FIRST}:D{last})", sum(r[1] for r in rows), "#,##0.00")]


def _fixed_case(p):
    """No change: months to clear and total interest paying a fixed amount (graded: total interest)."""
    rows = p["base"]
    last, total, fills = _results(rows)
    text = (f"Download the spreadsheet below. Complete the schedule for a fixed payment of £{p['fixed']} a month to "
            f"find how many months it takes to clear the balance (I6) and the total interest paid (I7). Save the "
            f"file and upload it.")
    steps = [{"prompt": "Monthly effective rate, as a percentage (3 d.p.)", "answer": round(p["i"] * 100, 3)},
             {"prompt": "Interest added in month 1 (£)", "answer": rows[0][1]},
             {"prompt": "Months to clear the balance", "answer": len(rows)},
             {"prompt": "Total interest (£)", "answer": total}]
    worked = [f"C5 = (1 + {p['a'] / 100:g})^(1/12) − 1 = {p['i'] * 100:.3f}%",
              f"D11 = ROUND($C$5*C11,2) = {rows[0][1]:,.2f}; F11 = MIN(E11,$C$6); fill down",
              f"The balance reaches £0 in month {len(rows)} (last payment £{rows[-1][3]:,.2f})",
              f"Total interest = SUM(D11:D{last}) = £{total:,.2f}"]
    meta = _fixed_sheet(_card_title(p, f"paying £{p['fixed']} a month"), p["bal"], p["a"] / 100, p["fixed"], rows,
                        fills=fills, pay_ref=lambda t: "$C$6", rate_ref=lambda t: "$C$5", answer="I7")
    return dict(text=text, answer=total, steps=steps, worked=worked, meta=meta)


def _baseline(p, baseline):
    if baseline:
        return (f"Paying £{p['fixed']} every month, the balance would be cleared in {p['months']} months with total "
                f"interest of £{p['interest']:,.2f}. ")
    return ""


def _card_increase_case(p, baseline=True):
    i, fixed = p["i"], p["fixed"]
    k = random.choice([m for m in (3, 4, 6, 9, 12) if m <= p["months"] // 2])
    inc = random.choice([10, 20, 25, 30, 50]) if fixed < 100 else random.choice([25, 50, 75, 100])
    new = fixed + inc
    rows = _fixed_run(p["bal"], lambda t: (i, fixed if t <= k else new))
    last, total, fills = _results(rows)
    saved = round(p["interest"] - total, 2)
    text = (f"{_baseline(p, baseline)}Instead, after {k} payments of £{fixed}, {p['name']} increases the payment to "
            f"£{new} a month from month {k + 1}.\n\nDownload the spreadsheet below. Complete the schedule to find how "
            f"many months it now takes to clear the balance (I6), the total interest (I7), and the interest saved "
            f"(I8){'' if baseline else ' compared with part (b)'}. Save the file and upload it.")
    steps = [{"prompt": f"Balance after the payment in month {k} (£)", "answer": round(rows[k - 1][4], 2)},
             {"prompt": "Months to clear the balance now", "answer": len(rows)},
             {"prompt": "Total interest now (£)", "answer": total},
             {"prompt": "Interest saved (£)", "answer": saved}]
    worked = [f"Months 1–{k}: F = MIN(E…,$C$6) (£{fixed}); from month {k + 1}: F = MIN(E…,$I$4) (£{new})",
              f"Balance after month {k}: £{rows[k - 1][4]:,.2f}",
              f"Cleared in month {len(rows)} (was {p['months']}); total interest = SUM(D11:D{last}) = £{total:,.2f}",
              f"Interest saved = {p['interest']:,.2f} − {total:,.2f} = £{saved:,.2f}"]
    meta = _fixed_sheet(
        _card_title(p, "payment goes up"), p["bal"], p["a"] / 100, fixed, rows,
        extras=[(3, "Payment goes up from month", k + 1, "0"), (4, "New monthly payment (£)", new, "#,##0.00")],
        fills=fills + [(8, "Interest saved (£)", f"={p['interest']:.2f}-I7", p["interest"] - sum(r[1] for r in rows),
                        "#,##0.00")],
        pay_ref=lambda t: "$C$6" if t <= k else "$I$4", rate_ref=lambda t: "$C$5", answer="I8")
    return dict(text=text, answer=saved, steps=steps, worked=worked, meta=meta)


def _card_holiday_case(p, baseline=True):
    i, fixed = p["i"], p["fixed"]
    k = random.choice([m for m in (2, 3, 4, 6, 9) if m <= p["months"] // 2])
    h = random.choice([1, 2, 3])
    s = k + 1
    rows = _fixed_run(p["bal"], lambda t: (i, 0 if s <= t < s + h else fixed))
    last, total, fills = _results(rows)
    extra = round(total - p["interest"], 2)
    span = f"month {s}" if h == 1 else f"months {s}–{s + h - 1}"
    text = (f"{_baseline(p, baseline)}Instead, after {k} payments the card provider offers {p['name']} a {h}-month "
            f"payment holiday: no payment is made in {span}, but interest is still added. Payments of £{fixed} then "
            f"resume.\n\nDownload the spreadsheet below. Complete the schedule to find how many months it now takes to "
            f"clear the balance (I6), the total interest (I7), and the extra interest the holiday costs (I8)"
            f"{'' if baseline else ', compared with part (b)'}. Save the file and upload it.")
    steps = [{"prompt": f"Balance after the payment in month {k} (£)", "answer": round(rows[k - 1][4], 2)},
             {"prompt": f"Balance at the end of the holiday, month {s + h - 1} (£)", "answer": round(rows[s + h - 2][4], 2)},
             {"prompt": "Months to clear the balance now", "answer": len(rows)},
             {"prompt": "Total interest now (£)", "answer": total},
             {"prompt": "Extra interest from the payment holiday (£)", "answer": extra}]
    worked = [f"{span.capitalize()}: payment = 0, so the balance grows by the interest added",
              f"Balance: £{rows[k - 1][4]:,.2f} after month {k}, £{rows[s + h - 2][4]:,.2f} at the end of the holiday",
              f"Cleared in month {len(rows)} (was {p['months']}); total interest = SUM(D11:D{last}) = £{total:,.2f}",
              f"Extra interest = {total:,.2f} − {p['interest']:,.2f} = £{extra:,.2f}"]
    meta = _fixed_sheet(
        _card_title(p, "payment holiday"), p["bal"], p["a"] / 100, fixed, rows,
        extras=[(3, "Payment holiday starts in month", s, "0"), (4, "Length of payment holiday (months)", h, "0")],
        fills=fills + [(8, "Extra interest from the holiday (£)", f"=I7-{p['interest']:.2f}",
                        sum(r[1] for r in rows) - p["interest"], "#,##0.00")],
        pay_ref=lambda t: None if s <= t < s + h else "$C$6", rate_ref=lambda t: "$C$5", answer="I8")
    return dict(text=text, answer=extra, steps=steps, worked=worked, meta=meta)


def _card_rate_case(p, baseline=True, intro=False):
    """The rate changes from month k+1: an introductory rate ending (intro=True — the plan's rate is the
    introductory one) or the provider raising the rate. Graded: total interest."""
    i, fixed = p["i"], p["fixed"]
    k = random.choice([m for m in (3, 6, 9, 12) if m <= p["months"] // 2])
    a2 = round(random.uniform(21.9, 34.9), 1) if intro else round(p["a"] + random.uniform(2, 6), 1)
    i2 = _m(a2 / 100)
    rows = _fixed_run(p["bal"], lambda t: (i if t <= k else i2, fixed))
    last, total, fills = _results(rows)
    fills = [(5, "New monthly effective rate", "=(1+I4)^(1/12)-1", i2, "0.000%")] + fills
    if intro:
        change = (f"The rate of {p['a']:g}% is an introductory rate for the first {k} months only; from month {k + 1} "
                  f"the standard rate of {a2}% applies.")
    else:
        change = f"Instead, after {k} months the card provider raises the annual effective rate to {a2}%."
    text = (f"{_baseline(p, baseline) if not intro else ''}{change}\n\nDownload the spreadsheet below. Complete the "
            f"schedule, paying £{fixed} a month, to find how many months it takes to clear the balance (I6) and the "
            f"total interest paid (I7). Save the file and upload it.")
    steps = [{"prompt": "New monthly effective rate, as a percentage (3 d.p.)", "answer": round(i2 * 100, 3)},
             {"prompt": f"Balance after the payment in month {k} (£)", "answer": round(rows[k - 1][4], 2)},
             {"prompt": "Months to clear the balance", "answer": len(rows)},
             {"prompt": "Total interest (£)", "answer": total}]
    worked = [f"Months 1–{k}: D = ROUND($C$5*C…,2); from month {k + 1}: D = ROUND($I$5*C…,2), where "
              f"I5 = (1 + {a2 / 100:g})^(1/12) − 1 = {i2 * 100:.3f}%",
              f"Balance after month {k}: £{rows[k - 1][4]:,.2f}",
              f"Cleared in month {len(rows)}; total interest = SUM(D11:D{last}) = £{total:,.2f}"]
    if not intro:
        worked.append(f"(£{total - p['interest']:,.2f} more interest than at {p['a']}%)")
    meta = _fixed_sheet(
        _card_title(p, "change of interest rate"), p["bal"], p["a"] / 100, fixed, rows,
        extras=[(3, "New rate applies from month", k + 1, "0"), (4, "New annual effective rate", a2 / 100, "0.000%")],
        fills=fills, pay_ref=lambda t: "$C$6", rate_ref=lambda t: "$C$5" if t <= k else "$I$5", answer="I7")
    return dict(text=text, answer=total, steps=steps, worked=worked, meta=meta)


def _card_intro(p):
    return (f"{p['name']} owes £{p['bal']:,.2f} on a credit card with an annual effective rate of interest of {p['a']:g}%. "
            f"Interest is added at the end of each month and {p['name']} pays a fixed £{p['fixed']} on the 1st of each "
            f"month (or the whole balance, if that is less). The card is not used again.\n\n")


def _card_single(case):
    p = _card_plan()
    c = case(p)
    return Question(question_text=_card_intro(p) + c["text"], correct_answer=c["answer"], topic=TOPIC,
                    question_type=QTYPE, scaffold_steps=c["steps"], worked_solution=c["worked"],
                    notes=SPREADSHEET_NOTES + CHANGE_NOTES, metadata=c["meta"])


def generate_credit_cards_l7():
    """Spreadsheet: the fixed payment goes up part-way through — interest saved."""
    return _card_single(_card_increase_case)


def generate_credit_cards_l8():
    """Spreadsheet: a payment holiday part-way through — extra interest."""
    return _card_single(_card_holiday_case)


def generate_credit_cards_l9():
    """Spreadsheet: an introductory rate ends — months to clear and total interest."""
    def case(p):
        p["a"] = random.choice([0.0, 2.9, 4.9, 6.9, 9.9])
        p["i"] = _m(p["a"] / 100)
        return _card_rate_case(p, intro=True)
    return _card_single(case)


def generate_credit_cards_l10():
    """Exam style, in parts as 2025 Q11: (a) one month by hand, (b) spreadsheet with a fixed payment,
    (c) a spreadsheet change — the payment goes up, a payment holiday or a rate rise, (d) a reason."""
    p = _card_plan()
    name, bal, a, i, fixed = p["name"], p["bal"], p["a"], p["i"], p["fixed"]
    context = (f"{name} owes £{bal:,.2f} on a credit card with an annual effective rate of interest of {a}%. Interest "
               f"is added at the end of each month, then a payment is made on the 1st. The card is not used again.")

    it, b, pay, after = _month(bal, i)
    part_a = make_part(
        "(a)", "If only the minimum payment (5% of the balance or £5, whichever is higher) is made, calculate the "
               "balance after the first payment.", after,
        scaffold_steps=[{"prompt": "Monthly effective rate, as a percentage (3 d.p.)", "answer": round(i * 100, 3)},
                        {"prompt": "Balance at the end of the month, after interest (£)", "answer": b},
                        {"prompt": "Minimum payment (£)", "answer": pay}],
        worked_solution=[f"End of month: {bal:,.2f} × {1 + a / 100:.3f}^(1/12) = £{b:,.2f}",
                         f"Minimum payment = 5% of £{b:,.2f} = £{pay:,.2f}",
                         f"Balance = {b:,.2f} − {pay:,.2f} = £{after:,.2f}  (interest first, then the payment)"])

    c = _fixed_case(p)
    part_b = make_part("(b)", f"{name} decides to pay a fixed £{fixed} a month instead (or the whole balance, if that "
                              f"is less). " + c["text"], c["answer"], scaffold_steps=c["steps"], worked_solution=c["worked"])
    part_b.metadata.update(c["meta"])

    c = random.choice([_card_increase_case, _card_holiday_case, _card_rate_case])(p, baseline=False)
    part_c = make_part("(c)", c["text"], c["answer"], scaffold_steps=c["steps"], worked_solution=c["worked"])
    part_c.metadata.update(c["meta"])

    part_d = make_part(
        "(d)", "Give one reason why it is better to clear a credit card balance as quickly as possible.",
        "Less interest is paid overall — the interest on the outstanding balance keeps adding to the debt. "
        "(\"It avoids going into debt\" is not accepted.)", explain=True)

    parts = [part_a, part_b, part_c, part_d]
    return Question(question_text=context, correct_answer=c["answer"], topic=TOPIC, question_type=QTYPE,
                    parts=parts, worked_solution=multipart_worked_solution(parts), notes=NOTES + CHANGE_NOTES)


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
    return random.choice([generate_credit_cards_calculator, generate_credit_cards_l6, generate_credit_cards_l7,
                          generate_credit_cards_l8, generate_credit_cards_l9, generate_credit_cards_l10])()
