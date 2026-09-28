"""Downloadable loan-schedule spreadsheets (download, fill in, upload) — shared by the
Higher Finance topics whose worksheets build a loan schedule in Excel (Loan Schedules,
Mortgages …).

The layout matches the sheets in Higher Apps/Worksheets/Finance/Questions/
Loan_Schedules_Worksheet.xlsx cell for cell, so the worksheet's cell references (C6, D13 …)
work here too:

    B3 Price   B4 Loan amount   B5 Annual effective rate   B6 Monthly effective rate
    B7 Level monthly repayment  B8 Final repayment         B9 Term (months)
    row 11 headers; row 12 = month 0; rows 13… = months 1…n

    D13 = ROUND($C$6*F12,2)   E13 = C13-D13   F13 = F12-E13   (the last month repays $C$8)

Two modes, matching the worksheet's two Goal Seek skills:
- "repayment": rate given; pupils Goal Seek the level repayment (graded cell C7).
- "rate": repayments given; pupils Goal Seek the monthly rate, then convert it to the
  annual effective rate (graded cell C5, as a percentage).
"""
import io

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

from core.engine.spreadsheet_solution import solution_metadata

HEADER_FILL = PatternFill("solid", fgColor="1F3864")
ANSWER_FILL = PatternFill("solid", fgColor="FFFF00")
HEADER_FONT = Font(color="FFFFFF", bold=True)
MONEY = "#,##0.00"
RATE = "0.000%"
FIRST_ROW = 13


def monthly_rate(annual):
    return (1 + annual) ** (1 / 12) - 1


def level_repayment(P, i, n):
    return P * i / (1 - (1 + i) ** -n)


def schedule(P, i, R, n, final=None):
    """Rows (month, repayment, interest, capital, outstanding) with the SQA rounding: interest
    to the penny on the previous outstanding. If `final` is None the last repayment is
    whatever clears the loan (outstanding + that month's interest)."""
    bal, rows = round(P, 2), []
    for t in range(1, n + 1):
        interest = round(i * bal + 1e-9, 2)
        if t == n:
            pay = round(bal + interest, 2) if final is None else final
        else:
            pay = R
        capital = round(pay - interest, 2)
        bal = round(bal - capital, 2)
        rows.append((t, pay, interest, capital, bal))
    return rows


def _sheet(title, sheet_name, n):
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 30
    for col in "CDEF":
        ws.column_dimensions[col].width = 18
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=13)
    for row, label in [(3, "Price (£)"), (4, "Loan amount (£)"), (5, "Annual effective rate"),
                       (6, "Monthly effective rate"), (7, "Level monthly repayment (£)"),
                       (8, "Final repayment (£)"), (9, "Term (months)")]:
        ws[f"B{row}"] = label
    for ref, fmt in [("C3", MONEY), ("C4", MONEY), ("C5", RATE), ("C6", RATE), ("C7", MONEY), ("C8", MONEY)]:
        ws[ref].number_format = fmt
    ws["C9"] = n
    for col, text in zip("BCDEF", ["Time (months)", "Repayment (£)", "Interest content of repayment (£)",
                                   "Capital content of repayment (£)", "Loan outstanding (£)"]):
        cell = ws[f"{col}11"]
        cell.value = text
        cell.fill, cell.font = HEADER_FILL, HEADER_FONT
        cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    ws.row_dimensions[11].height = 45
    ws["B12"] = 0
    ws["F12"].number_format = MONEY
    for t in range(1, n + 1):
        r = FIRST_ROW + t - 1
        ws[f"B{r}"] = t
        for col in "CDEF":
            ws[f"{col}{r}"].number_format = MONEY
    return wb, ws


def _bytes(wb):
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def build_loan_spreadsheet(*, title, sheet_name, filename, mode, P, i, n, rows, R, final,
                           annual=None, price=None, deposit=None):
    """Question workbook bytes, graded cell, and the completed-solution metadata.

    `rows` is `schedule(P, i, R, n, final)`; `annual` is the annual effective rate (a
    fraction); `price`/`deposit` (a fraction) for a finance deal, where the loan is the
    price minus the deposit."""
    last = FIRST_ROW + n - 1
    deal = price is not None

    # ---------------- question ----------------
    wb, ws = _sheet(title, sheet_name, n)
    to_fill = []
    if deal:
        ws["C3"] = price
        ws["D3"] = f"Deposit: {deposit:.0%}"
        to_fill.append("C4")
    else:
        ws["C3"] = "—"
        ws["C4"] = P
        ws["F12"] = P
    if mode == "repayment":
        ws["C5"] = annual
        to_fill += ["C6", "C7", "C8"]
    else:
        ws["C7"], ws["C8"] = R, final
        to_fill += ["C5", "C6"]
    if deal:
        to_fill.append("F12")
    to_fill += [f"{col}{r}" for r in range(FIRST_ROW, last + 1) for col in "CDEF"]
    for ref in to_fill:
        ws[ref].fill = ANSWER_FILL
    ws["A2"] = "Fill in the yellow cells, save the file, then upload it."
    ws["A2"].font = Font(italic=True)
    answer_cell = "C7" if mode == "repayment" else "C5"
    question_bytes = _bytes(wb)

    # ---------------- completed solution ----------------
    wb, ws = _sheet(title, sheet_name, n)
    ws["A2"] = "Completed solution: the yellow cells show the formulas used."
    ws["A2"].font = Font(italic=True)
    values = {}
    if deal:
        ws["C3"] = price
        ws["D3"] = f"Deposit: {deposit:.0%}"
        ws["C4"] = f"=C3*(1-{deposit:g})"
        values["C4"] = P
    else:
        ws["C3"] = "—"
        ws["C4"] = P
    if mode == "repayment":
        ws["C5"] = annual
        ws["C6"] = "=(1+C5)^(1/12)-1"
        ws["C7"] = R
        ws["D7"] = "← Goal Seek: last 'Loan outstanding' = 0 by changing C7, then round to 2 d.p."
        ws["C8"] = f"=F{last - 1}+ROUND($C$6*F{last - 1},2)"
        values.update({"C6": i, "C8": final})
    else:
        ws["C5"] = "=(1+C6)^12-1"
        ws["C6"] = i
        ws["D6"] = "← Goal Seek: set the last 'Loan outstanding' to 0 by changing C6"
        ws["C7"], ws["C8"] = R, final
        values["C5"] = annual
    ws["F12"] = "=C4"
    values["F12"] = P
    for t, pay, interest, capital, bal in rows:
        r = FIRST_ROW + t - 1
        ws[f"C{r}"] = "=$C$8" if t == n else "=$C$7"
        ws[f"D{r}"] = f"=ROUND($C$6*F{r - 1},2)"
        ws[f"E{r}"] = f"=C{r}-D{r}"
        ws[f"F{r}"] = f"=F{r - 1}-E{r}"
        values.update({f"C{r}": pay, f"D{r}": interest, f"E{r}": capital, f"F{r}": bal})
    for ref in to_fill:
        ws[ref].fill = ANSWER_FILL
    solution = solution_metadata(wb, ws, values, to_fill, min_row=3, max_row=last, min_col=2, max_col=6,
                                 filename=filename.replace(".xlsx", "_solution.xlsx"))

    metadata = {
        "spreadsheet_bytes": question_bytes,
        "spreadsheet_filename": filename,
        "spreadsheet_answer_cell": (sheet_name, answer_cell),
        **solution,
    }
    if mode == "rate":
        metadata["spreadsheet_answer_percent"] = True
    return metadata
