# N5apps

A Streamlit app that generates randomised practice questions for National 4/5/Higher maths, with
step-by-step scaffolds, worked solutions, and notes.

## Adding a new topic / question type

There is no auto-discovery — everything is a manual dict registry in
`core/engine/question_factory.py`. `n5_app.py` needs no changes; it's entirely driven by that
registry.

1. Write `topics/<package>/<type_snake_case>.py`. Existing packages: `numeracy`,
   `finance_statistics`, `geometry_measure`, `statistics` (Higher only), `rounding`. Follow the
   pattern in e.g. `topics/numeracy/ratio.py`: module-level `NOTES` markdown constant(s),
   module-level scenario/context lists for randomisation (plain `random.choice`/`randint`, never
   seeded), one `generate_<type>_l1()`/`_l2()`/`_l3()` per difficulty tier — each builds
   `question_text`, `scaffold_steps`, `worked_solution` and returns a
   `core.models.question_model.Question` — plus a `generate_<type>_question()` dispatcher that
   does `random.choice([...])()` across the levels (skip the dispatcher for a single-variant type,
   e.g. `finance_statistics/commission.py`).
2. In `core/engine/question_factory.py`:
   - Import the new generator(s) near that package's other imports.
   - Add `_N5_TOPICS["<Topic>"]["<Question Type>"] = generate_<type>_question`.
   - If there's more than one level, add
     `_N5_LEVELS["<Topic>"]["<Question Type>"] = {"Level 1": generate_<type>_l1, ...}` (read by
     `get_levels()` for the UI's per-level selector).
   - National 4 / Higher / N5-Numeracy variants go in `_N4_TOPICS` / `_HIGHER_TOPICS` /
     `_N5_NUMERACY_TOPICS` the same way.
3. **Stress-test with 100+ random iterations** before committing — check for exceptions,
   absurd/negative values where they shouldn't occur, and formatting artifacts (e.g. Python's
   `f"{x:g}"` silently producing `1e+07`-style output). Then sanity-check the registry wiring:
   `venv/bin/python -c "from core.engine.question_factory import generate_question;
   print(generate_question('<Topic>', '<Question Type>', qualification='National 5'))"`.
4. Commit and push automatically — don't ask each time — unless the change is risky (a merge of
   existing question types, anything destructive, anything you're unsure Luke would want pushed
   unreviewed), in which case stop and flag it. Stage only the files this run touched (never
   `git add -A`).

`topics/numeracy_assessment/` is a separate product surface (a fixed one-of-each-type "Practice
Assessment" mode under the `"N5 Numeracy"` qualification key, listed in
`_NUMERACY_ASSESSMENT_GENERATORS`) — same module contract, different registry wiring. Don't add
regular practice topics there.

## `Question` model (`core/models/question_model.py`)

```python
@dataclass
class Question:
    question_text: str
    correct_answer: Any
    topic: str
    question_type: str
    qid: int = field(default_factory=lambda: random.randint(10000, 99999))
    scaffold_steps: list[dict] = field(default_factory=list)   # [{"prompt": str, "answer": value}]
    worked_solution: list[str] = field(default_factory=list)
    notes: str = ""
    metadata: dict = field(default_factory=dict)
```

- `scaffold_steps`: guided step-by-step working, shown in a collapsible expander
  (`core/ui/scaffold_ui.py`) only if non-empty. Add `"answer_type": "duration"` on a step whose
  answer is a time duration (renders an hours/minutes widget instead of text).
- `worked_solution`: full worked-solution lines shown after submission (complete equations, not
  just the final answer).
- `metadata["diagram"]` / `metadata["diagram_params"]`: only for questions needing a custom
  diagram or interactive widget (e.g. pie charts, the banded-rate earnings simulator) — check
  `core/ui/question_ui.py` and `core/ui/scaffold_ui.py` for diagram keys already handled before
  inventing a new one. `"diagram": "tax_bands"` renders `core/ui/tax_bands_widget.py`'s
  interactive simulator (income slider, live tax/take-home/effective-rate readout) inside the
  scaffold expander — `diagram_params` is `{"bands": [(label, lower, upper_or_None, rate_pct),
  ...], "max_income": ..., "initial_income": ...}`. Used by National Insurance (National 5) and
  Income Tax and National Insurance (Higher); reuse it for any other banded-rate topic rather
  than building a new widget. **When you build any new simulation/widget for a question type,
  attach it the same way** — parameterise it from the question's own numbers (never hardcode a
  demo example), dispatch on a new `"diagram"` key in `scaffold_ui.py`, and stress-test that the
  widget actually builds from every generated question's `diagram_params`, not just that the
  question itself is valid.
- `metadata["reference_sheet"]`: a fixed markdown block (tables/rules, no worked example) shown
  directly above the question text, unconditionally — for real-world reference data (e.g. tax
  bands, NI rates) pupils are given alongside the question rather than expected to memorise.
  Rendered by `render_question()` in `core/ui/question_ui.py`. Used by Income Tax and National
  Insurance (Higher) — attached only to the levels that actually need it, not every level of the
  question type (e.g. not Gross Annual Pay, which doesn't touch tax or NI).

## Worksheet/homework library (outside this repo) — the full pipeline

Worksheets and homework for these topics are filed under
`/Users/luke/Library/CloudStorage/OneDrive-GlowScotland/Resources/Maths/Apps/<Level> Apps/`, e.g.
for National 5: `Worksheets/<Unit>/Questions/` + `Worksheets/<Unit>/Solutions/`, and
`HW/<Unit>/Questions/` + `HW/<Unit>/Solutions/` (`<Unit>` = `Numeracy`, `Finance and Statistics`,
`Geometry and Measure`, or `Rounding`; `<Topic>` — e.g. `Ratio` — is the filename stem inside
that unit's folder).

**The full pipeline** — filing a new worksheet, generating a matching homework, and adding new
question types here in one pass — is documented at
`/Users/luke/Library/CloudStorage/OneDrive-GlowScotland/Resources/Maths/Apps/CLAUDE.md` (with a
per-level pointer file in each `<Level> Apps/` folder), mirroring the equivalent Physics pipeline
at `Resources/Physics/CLAUDE.md`. Read that file when Luke attaches a worksheet — this file only
covers this repo's own module contract and registry mechanism.
