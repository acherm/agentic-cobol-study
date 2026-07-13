# `SAT-COBOL-CODEX` — Case Study (repository folder `SATCobol-codex`)

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/SATCobol-codex/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`SATCobol-codex` assessment](../assessments/SATCobol-codex.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/SATCobol-codex/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/SATCobol-codex/KEY_FEATURES.md)
  
> 🔁 **Replay prompts** (step-wise, HOW-agnostic, for reproducing with a different agent): [`REPLAY_PROMPTS.md`](../backlogs/SATCobol-codex/REPLAY_PROMPTS.md)

**Project root.** `/Users/mathieuacher/SANDBOX/SATCobol-codex`  
**Sessions.** 1 (0 Claude Code + 1 Codex)  
**Activity window.** 2026-04-15 → 2026-04-16 (0 days)  
**Agents & models.** Codex/gpt-5.4

---

## RQ1 — Domain, intent, novelty

**What it is.** SAT solver in COBOL (Codex-built) with modular copybooks (`cnf`, `io`, `parser`, `propagate`, `search`) and SAT4J / MiniSat cross-checks.

**Why it's interesting.** Second-generation COBOL SAT attempt: a small 280-LOC core orchestrating five COPY books, validated against SAT4J + MiniSat on uf/uuf benchmark families at 75/100/125/150 variables.

**Opening prompt that kicked off the project:**

```
Implement a robust DIMACS CNF parser in COBOL: supports c comments, p cnf <vars> <clauses>, arbitrary whitespace, multiple lines per clause, and 0 clause terminators. Add a parser-only mode: ./cobsat --parse file.cnf prints a normalized representation (vars, clauses, literals). Add unit tests under tests/ that cover: empty lines, CRLF line endings, trailing spaces, many spaces, comment lines between tokens.
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- DIMACS CNF parser in its own COPY
- clause / literal representation in free-format COBOL
- unit propagation module
- decision heuristic module
- SAT4J / MiniSat cross-check harness
- perf runner over uf/uuf benchmark sets
- result comparison + failure capture

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| C compiler error | 18 |
| command exited with non-zero status | 6 |
| test suite reported FAIL | 3 |
| missing file | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **63** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 0 |
| Git commit subjects | 10 |

**Backlog (63 F-### entries).** Grouped by phase:

- **_unclassified_** — 63 features  
  `6e49eb7`; `6e49eb7`; `6e49eb7`; `6e49eb7`; `6e49eb7` (same); `6e49eb7` (same); `6e49eb7`; `59d47ff` _(+55 more)_

**Git commits (10)** — first 8:

- `e7b5156eb1` 2026-04-16  Improve learned clauses and document benchmarks
- `edb0942bdc` 2026-04-16  Add clause learning and backjumping
- `8c6ebcf114` 2026-04-16  Add Minisat comparison benchmark script
- `c8cc713f30` 2026-04-15  Add restarts and activity-based branching
- `bad44e0a4f` 2026-04-15  Add translated SAT4J regression suite
- `ca9a67a790` 2026-04-15  Add Minisat cross-check script
- `1ebd388fdb` 2026-04-15  Optimize solver propagation and branching
- `14555932a0` 2026-04-15  Refactor solver into modules

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `cobsat` (0 KB)

## RQ4 — Size and complexity

**File inventory** (191 files, 6.8 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 6 | 1,934 |
| Shell | 5 | 936 |
| Markdown | 2 | 271 |
| Makefile | 1 | 28 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 6 |
| Total lines | 1,934 |
| Code lines (non-blank, non-comment) | 1,706 |
| Comment lines | 5 |
| Sections | 3 |
| Paragraphs | 70 |
| Data items (level-number declarations) | 22 |
| Max IF/EVALUATE nesting (any file) | 4 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 352 |
| `IF` | 147 |
| `PERFORM` | 146 |
| `EXIT` | 78 |
| `DISPLAY` | 49 |
| `COMPUTE` | 27 |
| `ADD` | 23 |
| `EVALUATE` | 10 |
| `ACCEPT` | 7 |
| `SUBTRACT` | 7 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `src/modules/parser.cpy` | 469 |
| `src/modules/search.cpy` | 377 |
| `src/modules/cnf.cpy` | 300 |
| `src/cobsat.cob` | 263 |
| `src/modules/propagate.cpy` | 193 |

**Git churn signal.** 10 commits, 72281 insertions / 1260 deletions, first 2026-04-15, last 2026-04-16.

## RQ4b — COBOL language mastery

**Mastery score:** **42** distinct COBOL constructs used across **9/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 695 | `IF`×294, `PERFORM`×178, `EXIT`×78, `WHEN`×38, `EVALUATE`×29, `PERFORM_UNTIL`×29, `ELSE`×26, `PERFORM_VARYING`×17 _(+2 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 60 | `COMPUTE`×27, `ADD`×23, `SUBTRACT`×7, `DIVIDE`×2, `MULTIPLY`×1 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 236 | `USAGE_COMP_5`×81, `PIC_9`×80, `PIC_X`×38, `OCCURS`×22, `PIC_S9`×15 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 85 | `START`×37, `ASSIGN`×27, `SELECT`×4, `READ`×4, `AT_END`×4, `OPEN_INPUT`×3, `FD`×2, `LINE_SEQUENTIAL`×2 _(+1 more)_ |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 7 | `STRING`×2, `DELIMITED_BY`×2, `INSPECT`×2, `REFERENCE_MOD`×1 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 29 | `INITIALIZE`×21, `SEARCH`×8 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | — | 0 |  |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 5 | `COPY`×5 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 121 | `FUNCTION`×67, `FUNCTION_TRIM`×52, `FUNCTION_NUMVAL`×1, `FUNCTION_LENGTH`×1 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 64 | `DISPLAY`×57, `ACCEPT`×7 |

**Notable non-trivial constructs used:** `OCCURS` (22×), `USAGE_COMP_5` (81×), `COPY` (5×), `FD` (2×), `FUNCTION` (67×).

**Procedural structure.** 70 paragraphs, 3 sections across 6 COBOL file(s). That means roughly **70 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **45m 49s** across 620 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 27m 53s | 60.9% |
| `feature` | adding new functionality | 11m 14s | 24.5% |
| `bug_fix` | correcting an observed defect | 3m 13s | 7.0% |
| `build` | compile / makefile / dependency work | 2m 27s | 5.3% |
| `test` | writing or running tests / benchmarks | 0m 33s | 1.2% |
| `plan` | task tracking, planning | 0m 29s | 1.1% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `build` | 85 |
| `test` | 29 |
| `plan` | 28 |
| `feature` | 21 |
| `bug_fix` | 14 |
| `understanding` | 10 |

## RQ6 — Failures encountered

Out of **187 tool results**, **26** (13.9%) contained an error signature.

## RQ6b — Difficulty assessment

**Auto-label: `Medium`** (difficulty index 0.44; mean rank across 7 signals = 7.6).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 0.8 | 5.0 |
| Calendar span (days first→last event) | 0 | 3.5 |
| User prompts | 15 | 7.0 |
| Redirect / bug-report prompts | 0 | 2.0 |
| Tool-output error rate | 0.139 | 13.0 |
| Fix cycles (error → immediate retry) | 3 | 9.0 |
| Share of active time spent on `bug_fix` | 0.070 | 13.5 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 15
- **Average prompt length:** 138 chars; **max:** 411 chars
- **Total chars written by user:** 2,075
- **Sessions:** 1; **span:** 0 days
- **Long-prompt ratio** (≥500 chars): 0/15

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Codex | `gpt-5.4` | 2026-04-15 12:19 | 17h 24m | 29 | 508 | $10.71 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| clarify | 6 |
| other | 4 |
| review-ask | 4 |
| initial-spec | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-04-15]_ Implement a robust DIMACS CNF parser in COBOL: supports c comments, p cnf <vars> <clauses>, arbitrary whitespace, multiple lines per clause, and 0 clause terminators. Add a parser-only mode: ./cobsat --parse file.cnf prints a normalized rep…
2. _[2026-04-15]_ consider large DIMACS formula, coming from https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html for instance
3. _[2026-04-15]_ create a git and commit
4. _[2026-04-15]_ Implement: given a CNF instance and a proposed assignment, evaluate whether every clause is satisfied. Add a mode ./cobsat --check-model file.cnf model.txt that returns 0 if model satisfies, non-zero otherwise. Add tests: feed known satisfy…
5. _[2026-04-15]_ in tests/ folder I have put two archives in tar gz... uf75-325 / uuf75-325: 75 variables, 325 clauses - 100 instances, all sat/unsat please check it's working
6. _[2026-04-15]_ what about --check-model ?
7. _[2026-04-15]_ Implement a baseline DPLL solver: unit propagation + backtracking. Keep it simple but correct. If SAT, output: s SATISFIABLE and a v ... 0 model line If UNSAT, output s UNSATISFIABLE. Add small SAT/UNSAT tests (including “pigeonhole small”,…
8. _[2026-04-15]_ does it work with uf75-325 and uuf75-325?
9. _[2026-04-15]_ please commit
10. _[2026-04-15]_ Refactor solver code into modules (parser, cnf, propagate, search, io) without breaking tests

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 17h 24m |
| Active collaboration time | 45m 49s |
| Tool calls | 508 |
| Input tokens | 2,096,697 |
| Output tokens | 290,821 |
| Cache-read tokens | 41,474,048 |
| Cache-create tokens | 0 |
| Reasoning tokens (Codex) | 146,500 |
| Estimated cost at API rack rates | $10.71 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `exec_command` | 136 |
| `apply_patch` | 24 |
| `write_stdin` | 22 |
| `update_plan` | 5 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
