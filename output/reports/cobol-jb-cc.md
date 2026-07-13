# `cobol-jb-cc` — Case Study

> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-jb-cc` assessment](../assessments/cobol-jb-cc.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-jb-cc/SPECIFICATION_BACKLOG.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-jb-cc`  
**Sessions.** 1 (1 Claude Code + 0 Codex)  
**Activity window.** 2026-06-11 → 2026-07-07 (26 days)  
**Agents & models.** Claude Code/claude-sonnet-4-6

---

## RQ1 — Domain, intent, novelty

**Opening prompt that kicked off the project:**

```
<local-command-stdout>Set model to [1mSonnet 4.6 (1M context)[22m and saved as your default for new sessions · Draws from usage credits</local-command-stdout>
```

## RQ2 — Engineering challenges

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| C compiler error | 6 |
| assertion failed | 2 |
| Python traceback (tooling) | 2 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **0** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 143 |
| Git commit subjects | 6 |

**Prompt-extracted sub-requests (143)** — first 8 (sub-bullets inside user messages):

- _[2026-06-11]_ Target lines of code (LOC): 300 lines
- _[2026-06-11]_ Number of files the program must handle: 2
- _[2026-06-11]_ Target compiler: GnuCOBOL (cobc)
- _[2026-06-11]_ Compilation command: cobc -x -free -o program program.cbl
- _[2026-06-11]_ PERFORM (with VARYING or UNTIL loop)
- _[2026-06-11]_ EVALUATE (multi-branch conditional logic)
- _[2026-06-11]_ FILE SECTION with FD entries
- _[2026-06-11]_ COMPUTE (arithmetic expressions)

**Git commits (6)** — first 8:

- `f185429265` 2026-07-07  Refactor PROCEDURE DIVISION into cohesive named paragraphs
- `d5fc9026fc` 2026-07-07  Replace single input file with fulltime/parttime dual input
- `0b3240b5e7` 2026-07-07  Add category-level summary report to report_output.dat
- `9718d9de61` 2026-06-12  Add input validation with reject file (ERR-001 to ERR-004)
- `a645433ecf` 2026-06-12  Add social contribution deductions to payroll calculation
- `583a5aefaf` 2026-06-11  Add GnuCOBOL payroll management system

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `program` (74 KB)

## RQ4 — Size and complexity

**File inventory** (10 files, 0.2 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 1 | 598 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 1 |
| Total lines | 598 |
| Code lines (non-blank, non-comment) | 535 |
| Comment lines | 7 |
| Sections | 4 |
| Paragraphs | 23 |
| Data items (level-number declarations) | 192 |
| Max IF/EVALUATE nesting (any file) | 2 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 80 |
| `DISPLAY` | 33 |
| `PERFORM` | 19 |
| `COMPUTE` | 13 |
| `IF` | 12 |
| `WRITE` | 12 |
| `ADD` | 11 |
| `OPEN` | 10 |
| `EVALUATE` | 6 |
| `STOP` | 6 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `program.cbl` | 535 |

**Git churn signal.** 6 commits, 783 insertions / 163 deletions, first 2026-06-11, last 2026-07-07.

## RQ4b — COBOL language mastery

**Mastery score:** **30** distinct COBOL constructs used across **5/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 86 | `IF`×24, `PERFORM`×19, `WHEN`×18, `EVALUATE`×12, `STOP_RUN`×6, `ELSE`×3, `PERFORM_VARYING`×2, `PERFORM_UNTIL`×1 _(+1 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 31 | `COMPUTE`×17, `ADD`×11, `ROUNDED`×3 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 189 | `PIC_X`×79, `FILLER`×52, `PIC_9`×37, `LEVEL_88`×16, `PIC_V`×3, `OCCURS`×1, `REDEFINES`×1 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 60 | `WRITE`×22, `READ`×7, `FD`×5, `SELECT`×5, `ASSIGN`×5, `CLOSE`×5, `LINE_SEQUENTIAL`×5, `OPEN_OUTPUT`×3 _(+2 more)_ |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | — | 0 |  |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | — | 0 |  |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | — | 0 |  |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | — | 0 |  |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | — | 0 |  |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 36 | `DISPLAY`×36 |

**Notable non-trivial constructs used:** `OCCURS` (1×), `REDEFINES` (1×), `FD` (5×).

**Procedural structure.** 23 paragraphs, 4 sections across 1 COBOL file(s). That means roughly **23 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **1h 57m** across 415 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 38m 29s | 32.8% |
| `build` | compile / makefile / dependency work | 36m 29s | 31.1% |
| `doc` | README / comments / final reports | 16m 11s | 13.8% |
| `bug_fix` | correcting an observed defect | 8m 11s | 7.0% |
| `spec` | specifications / architecture writing | 8m 7s | 6.9% |
| `feature` | adding new functionality | 7m 1s | 6.0% |
| `test` | writing or running tests / benchmarks | 1m 47s | 1.5% |
| `plan` | task tracking, planning | 0m 40s | 0.6% |
| `unknown` | could not classify confidently | 0m 20s | 0.3% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `feature` | 63 |
| `build` | 26 |
| `understanding` | 19 |
| `plan` | 12 |
| `test` | 9 |
| `bug_fix` | 7 |

## RQ6 — Failures encountered

Out of **136 tool results**, **7** (5.1%) contained an error signature.

The user filed **7 bug-report-style prompt(s)** (prompts containing words like 'error', 'crash', 'broken', 'wrong').

## RQ6b — Difficulty assessment

**Auto-label: `High`** (difficulty index 0.63; mean rank across 7 signals = 10.5).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 1.9 | 8.0 |
| Calendar span (days first→last event) | 26 | 13.5 |
| User prompts | 21 | 11.0 |
| Redirect / bug-report prompts | 7 | 13.0 |
| Tool-output error rate | 0.051 | 10.0 |
| Fix cycles (error → immediate retry) | 1 | 4.5 |
| Share of active time spent on `bug_fix` | 0.070 | 13.5 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 21
- **Average prompt length:** 1153 chars; **max:** 3,299 chars
- **Total chars written by user:** 24,206
- **Sessions:** 1; **span:** 26 days
- **Long-prompt ratio** (≥500 chars): 14/21

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Claude Code | `claude-sonnet-4-6` | 2026-06-11 10:10 | 26d 1h 34m | 29 | 136 | $13.35 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| bug-report | 7 |
| review-ask | 7 |
| clarify | 4 |
| other | 3 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-06-11]_ <local-command-stdout>Set model to [1mSonnet 4.6 (1M context)[22m and saved as your default for new sessions · Draws from usage credits</local-command-stdout>
2. _[2026-06-11]_ <local-command-stdout>Set model to [1mSonnet 4.6 (1M context)[22m and saved as your default for new sessions with [1mhigh[22m effort · Draws from usage credits</local-command-stdout>
3. _[2026-06-11]_ You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program. ## Business Context Domain: Payroll management system ## Technical Constraints - Target lines of code (LOC): 300 lines - Number of files the program must h…
4. _[2026-06-11]_ create a git and commit mathieuacher@Mathieus-MacBook-Pro cobol-jb-cc % cobc -x -free -o program program.cbl mathieuacher@Mathieus-MacBook-Pro cobol-jb-cc % ./program ------------------------------------------------------------ PAYROLL PROC…
5. _[2026-06-11]_ You are a mainframe COBOL expert. You must modify an existing COBOL program. ## Feature to Add Add social contribution deductions to the payroll calculation. The following deductions must be applied to the gross salary to compute the net sa…
6. _[2026-06-12]_ mathieuacher@Mathieus-MacBook-Pro cobol-jb-cc % cobc -x -free -o program program.cbl mathieuacher@Mathieus-MacBook-Pro cobol-jb-cc % ./program ------------------------------------------------------------ PAYROLL PROCESSING REPORT ----------…
7. _[2026-06-12]_ You are a mainframe COBOL expert. You must modify an existing COBOL program. ## Feature to Add Add social contribution deductions to the payroll calculation. The following deductions must be applied to the gross salary to compute the net sa…
8. _[2026-06-12]_ correct! You are a mainframe COBOL expert. You must modify an existing COBOL program. ## Feature to Add Add input data validation with a dedicated reject file for invalid records. The following validation rules must be applied to each emplo…
9. _[2026-07-07]_ mathieuacher@Mathieus-MacBook-Pro cobol-jb-cc % cobc -x -free -o program program.cbl mathieuacher@Mathieus-MacBook-Pro cobol-jb-cc % ./program ------------------------------------------------------------ PAYROLL PROCESSING REPORT ----------…
10. _[2026-07-07]_ <local-command-stdout>Set model to [1mOpus 4.8 (1M context) (default)[22m and saved as your default for new sessions</local-command-stdout>

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 26d 1h 34m |
| Active collaboration time | 1h 57m |
| Tool calls | 136 |
| Input tokens | 1,171 |
| Output tokens | 222,078 |
| Cache-read tokens | 19,457,587 |
| Cache-create tokens | 1,113,176 |
| Reasoning tokens (Codex) | 0 |
| Estimated cost at API rack rates | $13.35 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `Bash` | 62 |
| `Edit` | 61 |
| `Read` | 10 |
| `Write` | 3 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
