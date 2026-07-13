# Assessment — `cobol-jb` — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> **A self-contained GnuCOBOL payroll program** with three FDs (employees / payslips / rejects), 88-level condition names for job categories, `PERFORM UNTIL`, `EVALUATE TRUE`, `COMPUTE` with rounding, input validation with a reject file, and a formatted summary report. Verified against a 28-criterion grid in the `VERIFICATION_REPORT.md` (26 PASS, 1 PARTIAL, 1 FAIL on LOC overshoot 705 vs 300).

> **Textbook / case-study grade**: the COBOL idioms deployed (FDs, 88-levels, `PERFORM UNTIL`, `EVALUATE TRUE`, `COMPUTE ROUNDED`, formatted `DISPLAY`) are exactly what a mainframe payroll program looks like. This is a clean, idiomatic COBOL exercise at a believable size for its scope.

**Difficulty (auto-labelled):** Medium (idx 0.39). **Active collaboration time:** 0 h 40 m. **Sessions:** 2. **Backlog entries discovered:** 38. **Git commits:** 10.

## 1. Contract — what was asked

Industrial-idiom exercise: a payroll management system in GnuCOBOL that reads employee records, computes salaries with overtime + social-contribution rules, and emits payslips + a summary report. Verify against a 28-criterion grid.

Opening user prompt (verbatim, truncated):

```
You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program. ## Business Context Domain: Payroll management system ## Technical Constraints - Target lines of code (LOC): 300 lines - Number of files the program must handle: 2 (employees_input.dat as input, payslips_output.dat as output) - Target compiler: GnuCOBOL (cobc) - Compilation command: cobc -x -free -o program program.cbl ## Required COBOL Patterns The program MUST contain the following constructs: - PERFORM (with VARYING or UNTIL loop) - EVALUATE (multi-branch conditional logic) - FILE SECTION with FD entries - COMPUTE (arithmetic expressions) - 88-level condition names ## Requirements - The program must be complete and self-contained (no external dependencies) - All data is declared in the WORKING-STORAGE S
```

## 2. Delivered — externally-observable evidence

**A self-contained GnuCOBOL payroll program** with three FDs (employees / payslips / rejects), 88-level condition names for job categories, `PERFORM UNTIL`, `EVALUATE TRUE`, `COMPUTE` with rounding, input validation with a reject file, and a formatted summary report. Verified against a 28-criterion grid in the `VERIFICATION_REPORT.md` (26 PASS, 1 PARTIAL, 1 FAIL on LOC overshoot 705 vs 300).

**Executables present in `SANDBOX/cobol-jb/`** (at least *something* built):

- `program` (74 KB)

**COBOL surface exercised.** 2 COBOL file(s), 906 code lines, 32 paragraphs (≈ function-like units), 7 sections, mastery score **35** distinct constructs across **8/10** capability categories.

**Backlog (auto-mined).** 38 `F-###` / `SB-###` / `S#-##` entries in the harvested / subagent-generated `SPECIFICATION_BACKLOG.md`. Prompts also produced 34 sub-request bullets; git history carries 10 commits.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

**Mean score across 4 BLs and 6 criteria: 1.57/2** (Q1 corr. 2, Q2 build 2, Q3 tests 1.25, Q4 robust 1.25, Q5 maintain 1.25, Q6 repro 1.75).

| BL | Q1 corr. | Q2 build/run | Q3 tests | Q4 robust | Q5 maintain | Q6 repro | Conf |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BL-001` | 2 | 2 | 1 | 1 | 1 | 2 | High |
| `BL-002` | 2 | 2 | 1 | 1 | 1 | 2 | High |
| `BL-003` | 2 | 2 | 1 | 2 | 1 | 1 | High |
| `BL-004` | 2 | NA | 2 | 1 | 2 | 2 | High |

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** A production mainframe payroll: GL integration, multi-currency, time-series history, audit trails, batch scheduling, CICS online screens. Industrial systems run tens to hundreds of kLOC.

**Where this result sits.** **Textbook / case-study grade**: the COBOL idioms deployed (FDs, 88-levels, `PERFORM UNTIL`, `EVALUATE TRUE`, `COMPUTE ROUNDED`, formatted `DISPLAY`) are exactly what a mainframe payroll program looks like. This is a clean, idiomatic COBOL exercise at a believable size for its scope.

**Why the ceiling is out of reach here — honest constraints (not failures):**

- Scope was a **single self-contained program**, not an enterprise system — by design.
- No GL / ledger integration; no time-series; no batch scheduling layer — those live outside the contract.

## 5. What's genuinely impressive (evidence-anchored)

- **Compiles cleanly** on first `cobc -x -free` attempt after the first session's `WS-FILE-STATUS` / PROCEDURE DIVISION header mishap was fixed — and the 2nd / 3rd features compiled first-try.
- Uses **idiomatic COBOL**: three FDs with proper SELECT/ASSIGN, condition names (`88 CATEGORY-WHITE-COLLAR VALUE 'W'`), `EVALUATE TRUE` rather than nested IF, `COMPUTE var ROUNDED` for payroll arithmetic.
- Grid-based verification: 28 explicit acceptance criteria, 26 PASS, transparent grid disclosure of the LOC overshoot and README drift.
- Low user-intervention rate: 11 user prompts, 6 of them git/push ops — actual coding required only 5 user turns for 4 BLs.

## 6. Honest gaps

- **LOC overshoot**: 705 actual vs 300 target — noted in the grid (criterion #3 FAIL).
- **README drift**: BL-003 README update never landed (DoD = Partial).
- No CICS / batch-scheduler integration (out of scope).

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 4.0% (4 errors / 100 tool outputs).
- Bug-report-style user prompts: 2.
- Redirect-style user prompts: 0.
- Share of active time spent on `bug_fix`: 1.5% (0 min of 40 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/cobol-jb`
- Sessions: 2 (primary agent: Claude Code claude-opus-4-6)
- Git history: 10 commits available in `/Users/mathieuacher/SANDBOX/cobol-jb/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/cobol-jb/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/cobol-jb__*.jsonl`.

## 8. Final take

****Textbook / case-study grade**: the COBOL idioms deployed (FDs, 88-levels, `PERFORM UNTIL`, `EVALUATE TRUE`, `COMPUTE ROUNDED`, formatted `DISPLAY`) are exactly what a mainframe payroll program looks like.** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/cobol-jb.json`, `output/backlogs/cobol-jb/appendix.json` (when present), `output/complexity/cobol-jb.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
