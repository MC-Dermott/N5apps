"""Builds core/data/past_papers.json, the app's index of single-question past paper PDFs on Google Drive, from the
booklet scripts in the worksheet library (their topic tags, page positions and Drive links). Run after adding a new
year there (singles built with --apply):

    venv/bin/python tools/build_past_paper_index.py
"""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

APPS = Path.home() / "Library/CloudStorage/OneDrive-GlowScotland/Resources/Apps"
TOOLS = APPS / ".pipeline-tools"
OUT = Path(__file__).resolve().parent.parent / "core" / "data" / "past_papers.json"

# National 5: (unit, topic shown in the app, booklet tag codes). Topics the app has no practice questions for are
# listed too, so that every tagged skill can be practised.
N5_TOPICS = [
    ("Numeracy", "Fractions", "F1 F2 F3 F4"),
    ("Numeracy", "Percentages", "P1 P2 P3"),
    ("Numeracy", "Probability", "PR1 PR2 PR3 PR4 PR5 PR6"),
    ("Numeracy", "Ratio and Proportion", "R1 R2 R3 R4 D1 D2 D3 D4 D5 D6"),
    ("Numeracy", "Speed, Distance and Time", "T1 T2 T3 T4"),
    ("Numeracy", "Currency Exchange", "C1 C2 C3 C4"),
    ("Numeracy", "Pie Charts", "G5 G6"),
    ("Numeracy", "Calculations and Formulae", "CAL"),
    ("Finance and Statistics", "Appreciation and Depreciation", "P4"),
    ("Finance and Statistics", "Wages", "WG"),
    ("Finance and Statistics", "National Insurance and Net Pay", "TX"),
    ("Finance and Statistics", "Budgeting, Saving and Costs", "MS"),
    ("Finance and Statistics", "Comparing Data Sets", "S1 S2 S3 S4 S5 S6 G7"),
    ("Finance and Statistics", "Statistical Graphs", "G1 G2 G3 G4"),
    ("Finance and Statistics", "Probability and Expected Frequency", "PR1 PR2 PR3 PR4 PR5 PR6"),
    ("Geometry and Measure", "Pythagoras Theorem", "PY"),
    ("Geometry and Measure", "Perimeter", "PE1 PE2 PE3 PE4 PE5"),
    ("Geometry and Measure", "Area", "A1 A2 A3 A4"),
    ("Geometry and Measure", "Volume", "V1 V2 V3 V4 V5"),
    ("Geometry and Measure", "Gradient", "GRD"),
    ("Geometry and Measure", "Tolerance", "TOL"),
    ("Geometry and Measure", "Scale Drawings and Bearings", "SDW R5"),
    ("Geometry and Measure", "Container Packing", "PK"),
    ("Geometry and Measure", "Task (Precedence) Diagrams", "PN"),
    ("Geometry and Measure", "Time Zones", "TZ"),
    ("Geometry and Measure", "Reading Scales and Tables", "RSC"),
    ("Rounding", "Significant Figures and Decimal Places", "P5"),
]

# Higher: (unit, topic shown in the app, booklet topic titles in pp_data.TOPICS)
HIGHER_TOPICS = [
    ("Finance", "Effective Interest Rates", ["Effective interest rates and accumulated values"]),
    ("Finance", "Present Value", ["Present value and working backwards"]),
    ("Finance", "Loan Schedules", ["Loan schedules"]),
    ("Finance", "Mortgages", ["Mortgages"]),
    ("Finance", "Credit Cards", ["Credit cards"]),
    ("Finance", "Savings Products and Pensions", ["Savings products and pensions"]),
    ("Finance", "Risks and Choices with Financial Products", ["Risks and choices with financial products"]),
    ("Finance", "Income Tax and National Insurance", ["Income tax, National Insurance and net pay"]),
    ("Finance", "Inflation and Insurance", ["Insurance", "Inflation and the Consumer Price Index"]),
    ("Statistics", "Data and Distributions", ["Types of data, sampling and bias",
                                              "Statistical diagrams, summaries and spreadsheet data"]),
    ("Statistics", "Correlation and Regression", ["Correlation and regression"]),
    ("Statistics", "Hypothesis Testing", ["Hypothesis testing"]),
    ("Statistics", "Probability", ["Probability: Venn and tree diagrams"]),
    ("Planning", "Networks", ["PERT charts, critical path and float", "Gantt charts"]),
    ("Planning", "Risk and Expected Value", ["Risk and expected value"]),
    ("Modelling", "Mathematical Modelling", [
        "Estimation", "Types of model, variables and rates", "Graphs that model a situation",
        "Recurrence relations (spreadsheet)", "Profit functions (spreadsheet)", "Error and tolerance",
        "Evaluating models, claims and predictions"]),
]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def drive_id(url):
    return re.search(r"/d/([^/]+)/", url).group(1)


def page_count(pdf):
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", info).group(1))


def national_5(questions):
    folder = TOOLS / "n5_pp_booklet"
    tags = load(folder / "tags.py")
    segments = json.loads((folder / "segments.json").read_text())
    links = json.loads((folder / "question_links.json").read_text())
    topics, used = {}, set()
    for year in tags.YEARS:
        for paper in (1, 2):
            seg = segments[f"{year}-{paper}"]
            for n in sorted(int(k) for k in seg["qp"]):
                qid = f"N5-{year}-{paper}-{n}"
                q_pages, mi_pages = len(seg["qp"][str(n)]), len(seg["mi"][str(n)])
                pdf = APPS / "N5 Apps/Past exam papers/Single questions" / str(year) / f"N5_Apps_{year}_P{paper}_Q{n:02d}.pdf"
                # question pages, marking instructions, then the one-page formulae list
                assert page_count(pdf) == q_pages + mi_pages + 1, pdf
                questions[qid] = {"year": year, "paper": paper, "qnum": n, "drive_id": drive_id(links[f"{year}-{paper}-{n}"]),
                                  "question_pages": q_pages, "marking_pages": mi_pages}
                found = tags.tags(f"{year}-{paper}", n)
                for unit, topic, codes in N5_TOPICS:
                    hit = [found[c] for c in codes.split() if c in found]
                    if not hit:
                        continue
                    used.update(c for c in codes.split() if c in found)
                    # name the parts only if every matching tag does
                    parts = sorted({p for h in hit for p in h}) if all(hit) else []
                    topics.setdefault(unit, {}).setdefault(topic, []).append({"id": qid, "parts": ", ".join(parts)})
    every = {c for _, rows in tags.ROWS for _, codes in rows for c in codes}
    assert every <= {c for _, _, codes in N5_TOPICS for c in codes.split()}, "a tag code has no app topic"
    return topics


def higher(questions):
    folder = TOOLS / "haom_pp_booklet"
    data = load(folder / "pp_data.py")
    links = json.loads((folder / "question_links.json").read_text())
    for year in data.YEARS:
        for n in sorted(data.QP[year]):
            q_pages, mi_pages = len(data.QP[year][n]), len(data.MI[year][n])
            pdf = APPS / "Higher Apps/Past exam papers/Single questions" / str(year) / f"Higher_AoM_{year}_Q{n:02d}.pdf"
            booklet = n in data.BOOKLET[year]
            pages = page_count(pdf)      # question, marking instructions, then the data booklet if it's needed
            assert pages > q_pages + mi_pages if booklet else pages == q_pages + mi_pages, pdf
            questions[f"H-{year}-{n}"] = {"year": year, "paper": None, "qnum": n,
                                          "drive_id": drive_id(links[f"{year}-{n}"]),
                                          "question_pages": q_pages, "marking_pages": mi_pages,
                                          "software": n in data.SOFTWARE[year]}
    booklet_topics = {title: by_year for _, rows in data.TOPICS for title, by_year in rows}
    assert set(booklet_topics) == {t for _, _, titles in HIGHER_TOPICS for t in titles}, "booklet topics have changed"
    topics = {}
    for unit, topic, titles in HIGHER_TOPICS:
        for year in data.YEARS:
            found = {}      # question number -> parts ("" means the whole question)
            for title in titles:
                for label in booklet_topics[title][year]:
                    n, part = re.fullmatch(r"(\d+)(.*)", label).groups()
                    found.setdefault(int(n), []).append(part)
            for n in sorted(found):
                parts = sorted(set(found[n])) if all(found[n]) else []
                topics.setdefault(unit, {}).setdefault(topic, []).append({"id": f"H-{year}-{n}", "parts": ", ".join(parts)})
    return topics


if __name__ == "__main__":
    questions = {}
    topics = {"National 5": national_5(questions), "Higher": higher(questions)}
    OUT.write_text(json.dumps({"topics": topics, "questions": questions}, indent=1) + "\n")
    print(len(questions), "questions indexed")
    for qual, units in topics.items():
        for unit, by_topic in units.items():
            print(qual, "|", unit, {t: len(e) for t, e in by_topic.items()})
