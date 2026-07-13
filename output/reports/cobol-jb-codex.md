# `cobol-jb-codex` — Case Study

> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-jb-codex` assessment](../assessments/cobol-jb-codex.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-jb-codex/SPECIFICATION_BACKLOG.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-jb-codex`  
**Sessions.** 2 (0 Claude Code + 2 Codex)  
**Activity window.** 2026-06-11 → 2026-07-07 (26 days)  
**Agents & models.** Codex/gpt-5.4, Codex/gpt-5.5

---

## RQ1 — Domain, intent, novelty

**From the project's `README.md` (first sections):**

> **# Payroll COBOL Program**  
> This workspace contains a self-contained GnuCOBOL payroll program in `program.cbl`. A ready-to-run sample input file is included in `employees_input.dat`.

> **## Build**  
> ```sh cobc -x -free -o program program.cbl ```

**Opening prompt that kicked off the project:**

```
You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program. ## Business Context Domain: Payroll management system ## Technical Constraints - Target lines of code (LOC): 300 lines - Number of files the program must handle: 2 (employees_input.dat as input, payslips_output.dat as output) - Target compiler: GnuCOBOL (cobc) - Compilation command: cobc -x -free -o program program.cbl ## Required COBOL Patterns The program MUST contain the following constructs: - PERFORM (with VARYING or UNTIL loop) - EVALUATE (multi-branch conditional logic) - FILE SECTION with FD entries - COMPUTE (arithmetic expressions) - 88-level condition names ## Requirements - The program must be complete and self-contained (no external dependencies) - All data is declared in the WORKING-STORAGE S…
```

## RQ2 — Engineering challenges

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| test suite reported FAIL | 25 |
| command exited with non-zero status | 6 |
| missing file | 1 |
| C compiler error | 1 |
| command not found | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **0** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 128 |
| Git commit subjects | 6 |

**Prompt-extracted sub-requests (128)** — first 8 (sub-bullets inside user messages):

- _[2026-06-11]_ Target lines of code (LOC): 300 lines
- _[2026-06-11]_ Number of files the program must handle: 2
- _[2026-06-11]_ Target compiler: GnuCOBOL (cobc)
- _[2026-06-11]_ Compilation command: cobc -x -free -o program program.cbl
- _[2026-06-11]_ PERFORM (with VARYING or UNTIL loop)
- _[2026-06-11]_ EVALUATE (multi-branch conditional logic)
- _[2026-06-11]_ FILE SECTION with FD entries
- _[2026-06-11]_ COMPUTE (arithmetic expressions)

**Git commits (6)** — first 8:

- `03c677aec8` 2026-07-07  Refactor COBOL procedure division structure
- `65a755c7aa` 2026-07-07  Split payroll processing across two input files
- `c39c28184d` 2026-07-07  Add category summary payroll report
- `17a479f405` 2026-06-11  Add payroll reject file validation
- `cdd737b85c` 2026-06-11  Add payroll social contribution deductions
- `f39ee0aca6` 2026-06-11  Initial payroll COBOL program

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `program` (73 KB)

## RQ4 — Size and complexity

**File inventory** (10 files, 0.1 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 1 | 647 |
| Markdown | 1 | 67 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 1 |
| Total lines | 647 |
| Code lines (non-blank, non-comment) | 572 |
| Comment lines | 25 |
| Sections | 3 |
| Paragraphs | 14 |
| Data items (level-number declarations) | 103 |
| Max IF/EVALUATE nesting (any file) | 19 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 92 |
| `CLOSE` | 35 |
| `DISPLAY` | 24 |
| `SET` | 22 |
| `IF` | 21 |
| `COMPUTE` | 17 |
| `PERFORM` | 16 |
| `ADD` | 15 |
| `OPEN` | 10 |
| `STOP` | 9 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `program.cbl` | 572 |

**Git churn signal.** 6 commits, 1016 insertions / 287 deletions, first 2026-06-11, last 2026-07-07.

## RQ4b — COBOL language mastery

**Mastery score:** **34** distinct COBOL constructs used across **7/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 90 | `IF`×27, `WHEN`×18, `PERFORM`×16, `STOP_RUN`×9, `EVALUATE`×6, `ELSE`×5, `CONTINUE`×4, `PERFORM_UNTIL`×3 _(+2 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 39 | `COMPUTE`×21, `ADD`×15, `ROUNDED`×3 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 104 | `PIC_X`×39, `PIC_9`×36, `LEVEL_88`×21, `PIC_V`×7, `OCCURS`×1 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 89 | `CLOSE`×35, `WRITE`×14, `OPEN_OUTPUT`×6, `READ`×6, `FD`×5, `SELECT`×5, `ASSIGN`×5, `LINE_SEQUENTIAL`×5 _(+2 more)_ |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 60 | `DELIMITED_BY`×54, `STRING`×5, `INSPECT`×1 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 23 | `SET`×22, `INITIALIZE`×1 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | — | 0 |  |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | — | 0 |  |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | — | 0 |  |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 103 | `DISPLAY`×103 |

**Notable non-trivial constructs used:** `OCCURS` (1×), `FD` (5×).

**Procedural structure.** 14 paragraphs, 3 sections across 1 COBOL file(s). That means roughly **14 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **30m 41s** across 638 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 18m 15s | 59.5% |
| `build` | compile / makefile / dependency work | 5m 18s | 17.3% |
| `bug_fix` | correcting an observed defect | 3m 39s | 11.9% |
| `feature` | adding new functionality | 3m 3s | 9.9% |
| `plan` | task tracking, planning | 0m 20s | 1.1% |
| `test` | writing or running tests / benchmarks | 0m 5s | 0.3% |
| `unknown` | could not classify confidently | 0m 1s | 0.1% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `build` | 114 |
| `plan` | 36 |
| `bug_fix` | 13 |
| `feature` | 11 |
| `understanding` | 11 |
| `test` | 8 |
| `unknown` | 6 |

## RQ6 — Failures encountered

Out of **199 tool results**, **32** (16.1%) contained an error signature.

The user filed **6 bug-report-style prompt(s)** (prompts containing words like 'error', 'crash', 'broken', 'wrong').

## RQ6b — Difficulty assessment

**Auto-label: `High`** (difficulty index 0.72; mean rank across 7 signals = 11.8).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 0.5 | 3.0 |
| Calendar span (days first→last event) | 26 | 13.5 |
| User prompts | 19 | 9.0 |
| Redirect / bug-report prompts | 6 | 12.0 |
| Tool-output error rate | 0.161 | 15.0 |
| Fix cycles (error → immediate retry) | 7 | 14.0 |
| Share of active time spent on `bug_fix` | 0.119 | 16.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 19
- **Average prompt length:** 698 chars; **max:** 2,072 chars
- **Total chars written by user:** 13,264
- **Sessions:** 2; **span:** 26 days
- **Long-prompt ratio** (≥500 chars): 10/19

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Codex | `gpt-5.4` | 2026-06-11 10:18 | 26d 1h 55m | 18 | 179 | $2.66 |
| 2 | Codex | `gpt-5.5` | 2026-07-07 11:16 | 6m 44s | 1 | 20 | $0.19 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| other | 6 |
| bug-report | 6 |
| clarify | 3 |
| review-ask | 2 |
| initial-spec | 1 |
| resume | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-06-11]_ You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program. ## Business Context Domain: Payroll management system ## Technical Constraints - Target lines of code (LOC): 300 lines - Number of files the program must h…
2. _[2026-06-11]_ mathieuacher@Mathieus-MacBook-Pro cobol-jb-codex % cobc -x -free program.cbl mathieuacher@Mathieus-MacBook-Pro cobol-jb-codex % ls README.md program program.cbl mathieuacher@Mathieus-MacBook-Pro cobol-jb-codex % ./program FAILED TO OPEN INP…
3. _[2026-06-11]_ create a git and commit
4. _[2026-06-11]_ You are a mainframe COBOL expert. You must modify an existing COBOL program. ## Feature to Add Add social contribution deductions to the payroll calculation. The following deductions must be applied to the gross salary to compute the net sa…
5. _[2026-06-11]_ please commit mathieuacher@Mathieus-MacBook-Pro cobol-jb-codex % ./program TOTAL EMPLOYEES PROCESSED : 0000005 TOTAL GROSS PAYROLL : 4,769.50 TOTAL NET PAYROLL : 3,977.73
6. _[2026-06-11]_ You are a mainframe COBOL expert. You must modify an existing COBOL program. ## Feature to Add Add input data validation with a dedicated reject file for invalid records. The following validation rules must be applied to each employee recor…
7. _[2026-06-11]_ ./program EMPLOYEES PROCESSED VALID : 5 EMPLOYEES REJECTED : 0 TOTAL GROSS PAYROLL : 4,769.50 TOTAL NET PAYROLL : 3,977.73 no employees rejected, which is strange mathieuacher@Mathieus-MacBook-Pro cobol-jb-codex % ./program rejects_output.d…
8. _[2026-06-11]_ that works indeed... please commit
9. _[2026-07-07]_ there are existing sessions I'd like to resume in this folder... but they do not appear in the left-hand side. Can you depict it? or tell me how to "restore" it?
10. _[2026-07-07]_ You are a mainframe COBOL expert. You must modify an existing COBOL program. ## Feature to Add Add a category-level summary report generated at the end of the job. A new output file report_output.dat must be created and declared with a prop…

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 26d 2h 2m |
| Active collaboration time | 30m 41s |
| Tool calls | 199 |
| Input tokens | 10,701,852 |
| Output tokens | 94,626 |
| Cache-read tokens | 10,200,576 |
| Cache-create tokens | 0 |
| Reasoning tokens (Codex) | 49,754 |
| Estimated cost at API rack rates | $2.85 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `exec_command` | 175 |
| `apply_patch` | 18 |
| `list_threads` | 3 |
| `read_thread` | 1 |
| `set_thread_archived` | 1 |
| `set_thread_pinned` | 1 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
