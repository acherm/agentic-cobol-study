# `SAT-COBOL-CLAUDE` — Case Study (repository folder `SATCobol-cc`)

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/SATCobol-cc/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`SATCobol-cc` assessment](../assessments/SATCobol-cc.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/SATCobol-cc/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/SATCobol-cc/KEY_FEATURES.md)

**Project root.** `/Users/mathieuacher/SANDBOX/SATCobol-cc`  
**Sessions.** 1 (1 Claude Code + 0 Codex)  
**Activity window.** 2026-04-15 → 2026-04-17 (1 days)  
**Agents & models.** Claude Code/claude-opus-4-6

---

## RQ1 — Domain, intent, novelty

**What it is.** SAT solver in COBOL (Claude-Code-built) — the Claude-Code replica of the SAT domain, paired with the Codex-built `SATCobol-codex`.

**Why it's interesting.** Cross-agent replication: same SAT-solving contract, same `uf`/`uuf` benchmarks, different coding agent — lets us compare how two agents approach CDCL-style solving in COBOL side-by-side.

**Opening prompt that kicked off the project:**

```
Implement a robust DIMACS CNF parser in COBOL: supports c comments, p cnf <vars> <clauses>, arbitrary whitespace, multiple lines per clause, and 0 clause terminators. Add a parser-only mode: ./cobsat --parse file.cnf prints a normalized representation (vars, clauses, literals). Add unit tests under tests/ that cover: empty lines, CRLF line endings, trailing spaces, many spaces, comment lines between tokens.
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- DIMACS CNF parser
- clause/literal representation without pointers
- unit propagation
- decision heuristic
- cross-check against MiniSat / SAT4J
- performance parity vs the Codex sibling

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| C compiler error | 2 |
| GnuCOBOL compiler error (incl. syntax) | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **87** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 0 |
| Git commit subjects | 10 |

**Backlog (87 F-### entries).** Grouped by phase:

- **_unclassified_** — 87 features  
  `049f4b5`; `049f4b5`; `049f4b5`; `049f4b5`; `049f4b5`; `3fc5cdd`; `3fc5cdd`; `3fc5cdd` _(+79 more)_

**Git commits (10)** — first 8:

- `6404f111ff` 2026-04-17  Conflict-driven clause learning (CDCL) with first-UIP + backjump
- `c3b2a7c527` 2026-04-16  Phase saving, VSIDS-lite, JW branching, Luby restarts
- `57de05d273` 2026-04-16  Pass SAT4J's acceptance test suite
- `a121b45cae` 2026-04-16  Add scripts/crosscheck_minisat.sh to cross-verify against minisat
- `de35d40e71` 2026-04-15  Two-watched literals + occurrence branching; perf script; larger benchmarks
- `b2d8324121` 2026-04-15  Refactor cobsat into per-module copybooks (io, parser, cnf, propagate, search)
- `bdea674016` 2026-04-15  Add baseline DPLL solver (--solve) with unit propagation
- `88e8e997ab` 2026-04-15  Treat SATLIB '%' line as end-of-data; ship uf75/uuf75 benchmarks

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `cobsat` (68 KB)

## RQ4 — Size and complexity

**File inventory** (2832 files, 28.2 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 13 | 1,675 |
| Shell | 4 | 719 |
| Makefile | 1 | 18 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 13 |
| Total lines | 1,675 |
| Code lines (non-blank, non-comment) | 1,347 |
| Comment lines | 232 |
| Sections | 3 |
| Paragraphs | 94 |
| Data items (level-number declarations) | 159 |
| Max IF/EVALUATE nesting (any file) | 3 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 306 |
| `IF` | 123 |
| `PERFORM` | 121 |
| `ADD` | 47 |
| `EXIT` | 45 |
| `DISPLAY` | 39 |
| `COMPUTE` | 32 |
| `EVALUATE` | 10 |
| `SUBTRACT` | 6 |
| `OPEN` | 4 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `src/copy/parser.cpy` | 371 |
| `src/copy/propagate.cpy` | 325 |
| `src/copy/cnf.cpy` | 150 |
| `src/copy/io.cpy` | 143 |
| `src/copy/search.cpy` | 104 |

**Git churn signal.** 10 commits, 795633 insertions / 1141 deletions, first 2026-04-15, last 2026-04-17.

## RQ4b — COBOL language mastery

**Mastery score:** **41** distinct COBOL constructs used across **9/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 638 | `IF`×246, `PERFORM`×155, `EXIT`×75, `ELSE`×52, `PERFORM_UNTIL`×35, `WHEN`×32, `EVALUATE`×20, `PERFORM_VARYING`×17 _(+2 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 99 | `ADD`×54, `COMPUTE`×36, `SUBTRACT`×6, `DIVIDE`×2, `MULTIPLY`×1 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 222 | `PIC_9`×90, `USAGE_COMP_5`×67, `PIC_X`×34, `OCCURS`×19, `PIC_S9`×12 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 63 | `ASSIGN`×18, `READ`×17, `START`×12, `CLOSE`×6, `SELECT`×2, `LINE_SEQUENTIAL`×2, `FD`×2, `OPEN_INPUT`×2 _(+1 more)_ |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 13 | `REFERENCE_MOD`×5, `STRING`×4, `DELIMITED_BY`×4 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 5 | `SEARCH`×2, `SET`×2, `INITIALIZE`×1 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | — | 0 |  |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 12 | `COPY`×12 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 42 | `FUNCTION`×23, `FUNCTION_TRIM`×17, `FUNCTION_MOD`×2 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 42 | `DISPLAY`×39, `ACCEPT`×3 |

**Notable non-trivial constructs used:** `OCCURS` (19×), `USAGE_COMP_5` (67×), `COPY` (12×), `FD` (2×), `FUNCTION` (23×).

**Procedural structure.** 94 paragraphs, 3 sections across 13 COBOL file(s). That means roughly **94 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **1h 14m** across 316 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `build` | compile / makefile / dependency work | 44m 2s | 59.4% |
| `understanding` | reading / searching to build a mental model | 15m 43s | 21.2% |
| `feature` | adding new functionality | 8m 13s | 11.1% |
| `unknown` | could not classify confidently | 3m 25s | 4.6% |
| `test` | writing or running tests / benchmarks | 1m 48s | 2.4% |
| `plan` | task tracking, planning | 0m 50s | 1.1% |
| `bug_fix` | correcting an observed defect | 0m 5s | 0.1% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `feature` | 56 |
| `build` | 22 |
| `understanding` | 20 |
| `plan` | 10 |
| `test` | 6 |
| `bug_fix` | 1 |

## RQ6 — Failures encountered

Out of **115 tool results**, **2** (1.7%) contained an error signature.

## RQ6b — Difficulty assessment

**Auto-label: `Low`** (difficulty index 0.23; mean rank across 7 signals = 4.5).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 1.2 | 7.0 |
| Calendar span (days first→last event) | 1 | 7.5 |
| User prompts | 8 | 3.0 |
| Redirect / bug-report prompts | 0 | 2.0 |
| Tool-output error rate | 0.017 | 4.0 |
| Fix cycles (error → immediate retry) | 1 | 4.5 |
| Share of active time spent on `bug_fix` | 0.001 | 3.5 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 8
- **Average prompt length:** 170 chars; **max:** 410 chars
- **Total chars written by user:** 1,358
- **Sessions:** 1; **span:** 1 days
- **Long-prompt ratio** (≥500 chars): 0/8

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2026-04-15 12:20 | 1d 22h 41m | 31 | 360 | $473.78 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| review-ask | 4 |
| clarify | 3 |
| initial-spec | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-04-15]_ Implement a robust DIMACS CNF parser in COBOL: supports c comments, p cnf <vars> <clauses>, arbitrary whitespace, multiple lines per clause, and 0 clause terminators. Add a parser-only mode: ./cobsat --parse file.cnf prints a normalized rep…
2. _[2026-04-15]_ create a git and commit
3. _[2026-04-15]_ Implement: given a CNF instance and a proposed assignment, evaluate whether every clause is satisfied. Add a mode ./cobsat --check-model file.cnf model.txt that returns 0 if model satisfies, non-zero otherwise. Add tests: feed known satisfy…
4. _[2026-04-15]_ in tests/ folder I have put two archives in tar gz... uf75-325 / uuf75-325: 75 variables, 325 clauses - 100 instances, all sat/unsat please check it's working
5. _[2026-04-15]_ in tests/ folder I have put two archives in tar gz... uf75-325 / uuf75-325: 75 variables, 325 clauses - 100 instances, all sat/unsat please check it's working
6. _[2026-04-15]_ Implement a baseline DPLL solver: unit propagation + backtracking. Keep it simple but correct. If SAT, output: s SATISFIABLE and a v ... 0 model line If UNSAT, output s UNSATISFIABLE. Add small SAT/UNSAT tests (including “pigeonhole small”,…
7. _[2026-04-15]_ retry/continue
8. _[2026-04-15]_ please commit

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 1d 22h 41m |
| Active collaboration time | 1h 14m |
| Tool calls | 360 |
| Input tokens | 977 |
| Output tokens | 984,752 |
| Cache-read tokens | 168,569,731 |
| Cache-create tokens | 7,843,062 |
| Reasoning tokens (Codex) | 0 |
| Estimated cost at API rack rates | $473.78 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `Bash` | 54 |
| `Write` | 29 |
| `Edit` | 28 |
| `Read` | 4 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
