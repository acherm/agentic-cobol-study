# `cobol-jb` — Case Study

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/cobol-jb/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-jb` assessment](../assessments/cobol-jb.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-jb/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/cobol-jb/KEY_FEATURES.md)
  
> 🔁 **Replay prompts** (step-wise, HOW-agnostic, for reproducing with a different agent): [`REPLAY_PROMPTS.md`](../backlogs/cobol-jb/REPLAY_PROMPTS.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-jb`  
**Sessions.** 2 (2 Claude Code + 0 Codex)  
**Activity window.** 2026-04-03 → 2026-04-04 (0 days)  
**Agents & models.** Claude Code/claude-opus-4-6

---

## RQ1 — Domain, intent, novelty

**What it is.** Payroll processing case-study in GnuCOBOL.

**Why it's interesting.** Industrial-style domain exercise (employee records → payslips + summary) used as a replay/verification grid.

**From the project's `README.md` (first sections):**

> **# COBOL Payroll Management System**  
> A complete GnuCOBOL payroll processing program that reads employee records, calculates gross salaries with overtime bonuses based on job categories, applies social contribution deductions, generates formatted payslips with net salary, and produces a summary report.

> **## Files**  
> | File | Description | |------|-------------| | `program.cbl` | Main COBOL source program | | `employees_input.dat` | Input file with employee records | | `payslips_output.dat` | Output file with generated payslips |

**Opening prompt that kicked off the project:**

```
You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program. ## Business Context Domain: Payroll management system ## Technical Constraints - Target lines of code (LOC): 300 lines - Number of files the program must handle: 2 (employees_input.dat as input, payslips_output.dat as output) - Target compiler: GnuCOBOL (cobc) - Compilation command: cobc -x -free -o program program.cbl ## Required COBOL Patterns The program MUST contain the following constructs: - PERFORM (with VARYING or UNTIL loop) - EVALUATE (multi-branch conditional logic) - FILE SECTION with FD entries - COMPUTE (arithmetic expressions) - 88-level condition names ## Requirements - The program must be complete and self-contained (no external dependencies) - All data is declared in the WORKING-STORAGE S…
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- fixed-format input file
- overtime rules per category
- social-contribution rules
- formatted output
- verification report

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| C compiler error | 2 |
| process aborted | 1 |
| GnuCOBOL compiler error (incl. syntax) | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **38** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 34 |
| Git commit subjects | 10 |

**Backlog (38 F-### entries).** Grouped by phase:

- **_unclassified_** — 38 features  
  STEP-0; STEP-0; STEP-0; STEP-0; STEP-0; STEP-0; STEP-0; STEP-0 _(+30 more)_

**Prompt-extracted sub-requests (34)** — first 8 (sub-bullets inside user messages):

- _[2026-04-03]_ Target lines of code (LOC): 300 lines
- _[2026-04-03]_ Number of files the program must handle: 2
- _[2026-04-03]_ Target compiler: GnuCOBOL (cobc)
- _[2026-04-03]_ Compilation command: cobc -x -free -o program program.cbl
- _[2026-04-03]_ PERFORM (with VARYING or UNTIL loop)
- _[2026-04-03]_ EVALUATE (multi-branch conditional logic)
- _[2026-04-03]_ FILE SECTION with FD entries
- _[2026-04-03]_ COMPUTE (arithmetic expressions)

**Git commits (10)** — first 8:

- `4b148bc1a9` 2026-04-03  Add verification report scoring 25/27 on case study reproduction
- `ca7cf7a768` 2026-04-03  Add input validation with reject file for invalid records
- `ad841ed6f2` 2026-04-03  Add social contribution deductions to payroll calculation
- `cf26a128e7` 2026-04-03  Add COBOL payroll management system
- `71d46f1052` 2026-04-03  Add verification report scoring 25/27 on case study reproduction
- `704baa87c3` 2026-04-03  Add input validation with reject file for invalid records
- `a566a9ec77` 2026-04-03  Add social contribution deductions to payroll calculation
- `b4c6c665fe` 2026-04-03  Add COBOL payroll management system

## RQ3 — What was delivered

**From `VERIFICATION_REPORT.md`:**

> **# Case Study Verification Report**  
> **Date:** 2026-04-03 **Score:** 25/27 — Near-identical reproduction (minor acceptable differences)

> **## Step 0 — Generation**  
> | # | Criterion | Result | Notes | |---|-----------|--------|-------| | 1 | File created | PASS | `program.cbl` exists | | 2 | Compilation OK | PASS | `cobc -x -free` exits 0, no errors | | 3 | Approximate LOC (250–350) | FAIL | 705 lines — well above the 350 upper bound | | 4 | PERFORM pattern | PASS | Multiple `PERFORM` statements | | 5 | EVALUATE pattern | PASS | Multiple `EVALUATE TRUE` blocks | | 6 | FILE SECTION FDs | PASS | `FD EMPLOYEE-FILE` + `FD PAYSLIP-FILE` present, `ASSIGN TO` claus…

**Executables present in the root of the project** (evidence that something builds):

- `program` (74 KB)

## RQ4 — Size and complexity

**File inventory** (15 files, 0.4 MB).

| Language | Files | LOC |
|---|---:|---:|
| Markdown | 5 | 5,343 |
| COBOL | 2 | 1,100 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 2 |
| Total lines | 1,100 |
| Code lines (non-blank, non-comment) | 906 |
| Comment lines | 35 |
| Sections | 7 |
| Paragraphs | 32 |
| Data items (level-number declarations) | 246 |
| Max IF/EVALUATE nesting (any file) | 12 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 164 |
| `DISPLAY` | 45 |
| `WRITE` | 43 |
| `PERFORM` | 37 |
| `COMPUTE` | 29 |
| `IF` | 20 |
| `SET` | 15 |
| `EVALUATE` | 9 |
| `OPEN` | 9 |
| `ADD` | 9 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `program.cbl` | 568 |
| `case-study-1/program.cbl` | 338 |

**Git churn signal.** 10 commits, 7494 insertions / 16 deletions, first 2026-04-02, last 2026-04-03.

## RQ4b — COBOL language mastery

**Mastery score:** **35** distinct COBOL constructs used across **8/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 138 | `WHEN`×37, `PERFORM`×37, `IF`×24, `EVALUATE`×12, `ELSE`×8, `CONTINUE`×6, `PERFORM_UNTIL`×5, `EXIT`×4 _(+2 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 40 | `COMPUTE`×31, `ADD`×9 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 310 | `PIC_X`×110, `PIC_9`×89, `FILLER`×67, `LEVEL_88`×35, `PIC_V`×7, `PIC_S9`×1, `OCCURS`×1 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 106 | `WRITE`×56, `READ`×8, `CLOSE`×8, `FD`×6, `SELECT`×6, `ASSIGN`×6, `LINE_SEQUENTIAL`×6, `OPEN_OUTPUT`×4 _(+2 more)_ |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 10 | `DELIMITED_BY`×7, `STRING`×3 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 18 | `SET`×15, `INITIALIZE`×3 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | — | 0 |  |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | — | 0 |  |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 1 | `FUNCTION`×1 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 54 | `DISPLAY`×54 |

**Notable non-trivial constructs used:** `OCCURS` (1×), `FD` (6×), `FUNCTION` (1×).

**Procedural structure.** 32 paragraphs, 7 sections across 2 COBOL file(s). That means roughly **32 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **40m 11s** across 281 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 17m 27s | 43.4% |
| `doc` | README / comments / final reports | 9m 22s | 23.3% |
| `build` | compile / makefile / dependency work | 4m 13s | 10.5% |
| `unknown` | could not classify confidently | 3m 55s | 9.7% |
| `feature` | adding new functionality | 3m 43s | 9.2% |
| `plan` | task tracking, planning | 0m 47s | 1.9% |
| `bug_fix` | correcting an observed defect | 0m 37s | 1.5% |
| `test` | writing or running tests / benchmarks | 0m 7s | 0.3% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `feature` | 32 |
| `understanding` | 22 |
| `plan` | 20 |
| `build` | 18 |
| `bug_fix` | 5 |
| `test` | 3 |

## RQ6 — Failures encountered

Out of **100 tool results**, **4** (4.0%) contained an error signature.

The user filed **2 bug-report-style prompt(s)** (prompts containing words like 'error', 'crash', 'broken', 'wrong').

## RQ6b — Difficulty assessment

**Auto-label: `Medium`** (difficulty index 0.39; mean rank across 7 signals = 6.0).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 0.7 | 4.0 |
| Calendar span (days first→last event) | 0 | 3.0 |
| User prompts | 11 | 4.5 |
| Redirect / bug-report prompts | 2 | 5.5 |
| Tool-output error rate | 0.040 | 9.0 |
| Fix cycles (error → immediate retry) | 2 | 6.0 |
| Share of active time spent on `bug_fix` | 0.015 | 10.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 11
- **Average prompt length:** 588 chars; **max:** 2,484 chars
- **Total chars written by user:** 6,473
- **Sessions:** 2; **span:** 0 days
- **Long-prompt ratio** (≥500 chars): 4/11

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2026-04-03 14:45 | 1h 13m | 6 | 74 | $13.79 |
| 2 | Claude Code | `claude-opus-4-6` | 2026-04-03 15:46 | 19h 17m | 5 | 26 | $4.35 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| clarify | 4 |
| other | 4 |
| bug-report | 2 |
| initial-spec | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-04-03]_ You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program. ## Business Context Domain: Payroll management system ## Technical Constraints - Target lines of code (LOC): 300 lines - Number of files the program must h…
2. _[2026-04-03]_ create a git and commit
3. _[2026-04-03]_ You are a mainframe COBOL expert. You must modify an existing COBOL program. ## Feature to Add Add social contribution deductions to the payroll calculation. The following deductions must be applied to the gross salary to compute the net sa…
4. _[2026-04-03]_ please commit (incl. update of README)
5. _[2026-04-03]_ Add input data validation with a dedicated reject file for invalid records. The following validation rules must be applied to each employee record before processing: Rule 1 (ERR-001): Employee ID must not be spaces or zeros Rule 2 (ERR-002)…
6. _[2026-04-03]_ please commit
7. _[2026-04-03]_ look at the current repo Use this grid to objectively verify whether the agent produced equivalent results when replaying the case study. ### Step 0 — Generation | # | Criterion | Verification | |---|-----------|--------------| | 1 | File c…
8. _[2026-04-03]_ please commit this report
9. _[2026-04-03]_ please push on Github in this fork repo: https://github.com/acherm/cobol-agentic-dev-case-studies
10. _[2026-04-03]_ push in the main, not master

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 20h 30m |
| Active collaboration time | 40m 11s |
| Tool calls | 100 |
| Input tokens | 227 |
| Output tokens | 39,543 |
| Cache-read tokens | 7,238,447 |
| Cache-create tokens | 230,048 |
| Reasoning tokens (Codex) | 0 |
| Estimated cost at API rack rates | $18.14 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `Bash` | 49 |
| `Edit` | 25 |
| `Read` | 10 |
| `Write` | 9 |
| `Grep` | 6 |
| `Glob` | 1 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
