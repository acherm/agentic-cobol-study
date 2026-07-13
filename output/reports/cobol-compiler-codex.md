# `COMPILER-COBOL-CODEX` — Case Study (repository folder `cobol-compiler-codex`)

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/cobol-compiler-codex/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-compiler-codex` assessment](../assessments/cobol-compiler-codex.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-compiler-codex/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/cobol-compiler-codex/KEY_FEATURES.md)
  
> 🔁 **Replay prompts** (step-wise, HOW-agnostic, for reproducing with a different agent): [`REPLAY_PROMPTS.md`](../backlogs/cobol-compiler-codex/REPLAY_PROMPTS.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-compiler-codex`  
**Sessions.** 4 (0 Claude Code + 4 Codex)  
**Activity window.** 2026-03-29 → 2026-04-03 (4 days)  
**Agents & models.** Codex/gpt-5.4

---

## RQ1 — Domain, intent, novelty

**What it is.** Alternative minicobc COBOL-to-C compiler, driven by Codex.

**Why it's interesting.** Second compiler implementation as a controlled replication with a different agent, same ambition (compile non-trivial COBOL).

**From the project's `README.md` (first sections):**

> **# MiniCOBC**  
> `MiniCOBC` is a small COBOL compiler written in COBOL. It compiles a practical COBOL subset into C, then `gcc` turns that generated C into native executables. The project is validated not only on small sample programs, but also on non-trivial COBOL codebases including Game of 15 from [`acherm/agentic-cobol-game15tictactoe`](https://github.com/acherm/agentic-cobol-game15tictactoe) at [commit `4ae3129`](https://github.com/acherm/agentic-cobol-game15tictactoe/commit/4ae3129ad1f5b6a81cb28c075864781891c0e7a1), the chess engine from [`acherm/agentic-chessengine-cobol-codex`](https://github.com/acher…

> **## Current Status**  
> As of 2026-04-02, `MiniCOBC` is a working subset COBOL compiler with correctness tests, performance harnesses, an optimization mode, a bootstrap check, and multiple larger external programs now handled through the generic front end. - Generic compiler path: the shared `core` and `opt` corpus currently passes `11/11` benchmark cases, the full benchmark passes `19/19` including the mixed Game-of-15 suite, and additional regression tests now cover paragraph `PERFORM`, paragraph `PERFORM UNTIL`, `PERFORM VARYING`, restricted external `CALL`, multiline procedure statements, `EVALUATE`, `PIC X`, `PI…

**Opening prompt that kicked off the project:**

```
Write a COBOL compiler in COBOL. Demonstrate that you can run some (non-trivial) COBOL programs thanks to the written compiler.
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- subset of lexer/parser
- code-gen
- scripts/benchmarks
- run known non-trivial programs (doom, game15tictactoe)
- compare output/perf vs GnuCOBOL

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| test suite reported FAIL | 607 |
| command exited with non-zero status | 426 |
| C compiler error | 168 |
| missing file | 48 |
| GnuCOBOL compiler error (incl. syntax) | 32 |
| Python traceback (tooling) | 5 |
| permission denied | 5 |
| process aborted | 2 |
| segmentation fault at runtime | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **61** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 0 |
| Git commit subjects | 13 |

**Backlog (61 F-### entries).** Grouped by phase:

- **_unclassified_** — 61 features  
  COBOL-in-COBOL compiler skeleton `src/minicobc.cob`; Subset lexer/parser for `IDENTIFICATION`, `DATA`, `WORKING-STORAGE`, `…; Core statements: `DISPLAY`, `ACCEPT`, `MOVE`, `INITIALIZE`, `ADD`/`SUB…; Three local sample programs `primes.cob`, `collatz.cob`, `gcd.cob`; Build+demo+test scripts (`scripts/demo.sh`, `scripts/test.sh`); Compatibility path for `agentic-cobol-game15tictactoe@4ae3129`; External submodule pinning of `acherm/agentic-cobol-game15tictactoe`; Benchmark manifest `benchmark/cases.json` with core + compatibility su… _(+53 more)_

**Git commits (13)** — first 8:

- `1b72b9c9fa` 2026-04-03  Fix else-if chain closure handling
- `a05a8a47d0` 2026-04-03  Add cutechess Elo match tooling
- `1b0ca6f91f` 2026-04-03  Add chess tournament benchmarking
- `ab7f7d052e` 2026-04-02  Fix chess search equivalence and document validation
- `a8aeb459d1` 2026-04-02  Advance generic chess engine support
- `3147785e79` 2026-03-31  Advance generic chess support and validation
- `bdff7bb413` 2026-03-30  Target gameN with the generic front end
- `b9b2c6ef63` 2026-03-30  Refine README attribution and links

## RQ3 — What was delivered

## RQ4 — Size and complexity

**File inventory** (252 files, 3.2 MB).

| Language | Files | LOC |
|---|---:|---:|
| C | 25 | 63,074 |
| COBOL | 69 | 13,173 |
| Python | 13 | 5,940 |
| C/Header | 31 | 3,467 |
| JSON | 2 | 1,945 |
| Shell | 39 | 1,589 |
| Markdown | 5 | 1,405 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 69 |
| Total lines | 13,173 |
| Code lines (non-blank, non-comment) | 11,680 |
| Comment lines | 731 |
| Sections | 70 |
| Paragraphs | 246 |
| Data items (level-number declarations) | 189 |
| Max IF/EVALUATE nesting (any file) | 396 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 2,448 |
| `PERFORM` | 1,377 |
| `STRING` | 1,018 |
| `IF` | 924 |
| `EXIT` | 198 |
| `DISPLAY` | 147 |
| `COMPUTE` | 143 |
| `ADD` | 111 |
| `STOP` | 73 |
| `CALL` | 67 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `src/minicobc.cob` | 10,535 |
| `tests/chess/phase3_direct_ref.cob` | 123 |
| `tests/chess/phase3_search_ref.cob` | 53 |
| `tests/chess/phase1_fen_ref.cob` | 42 |
| `examples/primes.cob` | 25 |

**Git churn signal.** 13 commits, 162592 insertions / 74567 deletions, first 2026-03-29, last 2026-04-03.

## RQ4b — COBOL language mastery

**Mastery score:** **60** distinct COBOL constructs used across **10/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 4,265 | `IF`×1472, `PERFORM`×1451, `WHEN`×356, `ELSE`×266, `EXIT`×200, `EVALUATE`×160, `PERFORM_UNTIL`×140, `PERFORM_VARYING`×108 _(+3 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 330 | `COMPUTE`×146, `ADD`×116, `SUBTRACT`×50, `DIVIDE`×13, `MULTIPLY`×5 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 1,958 | `USAGE_POINTER`×997, `PIC_9`×260, `PIC_X`×250, `OCCURS`×217, `USAGE_COMP_5`×149, `REDEFINES`×60, `PIC_S9`×24, `FILLER`×1 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 402 | `START`×267, `CLOSE`×51, `WRITE`×21, `READ`×16, `AT_END`×14, `ASSIGN`×11, `OPEN_INPUT`×8, `OPEN_OUTPUT`×5 _(+3 more)_ |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 2,894 | `STRING`×1803, `DELIMITED_BY`×1035, `REFERENCE_MOD`×29, `UNSTRING`×13, `INSPECT`×7, `INSPECT_REPLACING`×7 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 60 | `SEARCH`×44, `SET`×9, `INITIALIZE`×7 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 416 | `CALL`×277, `USING`×95, `RECURSIVE`×14, `BY_VALUE`×12, `GIVING`×11, `BY_REFERENCE`×7 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 51 | `COPY`×44, `REPLACING`×7 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 1,124 | `FUNCTION`×571, `FUNCTION_TRIM`×521, `FUNCTION_NUMVAL`×11, `FUNCTION_LENGTH`×9, `FUNCTION_MOD`×8, `FUNCTION_UPPER`×4 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 283 | `DISPLAY`×252, `ACCEPT`×31 |

**Notable non-trivial constructs used:** `CALL` (277×), `RECURSIVE` (14×), `OCCURS` (217×), `REDEFINES` (60×), `USAGE_COMP_5` (149×), `COPY` (44×), `FD` (3×), `UNSTRING` (13×), `FUNCTION` (571×).

**Procedural structure.** 246 paragraphs, 70 sections across 69 COBOL file(s). That means roughly **246 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **10h 58m** across 15631 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 7h 13m | 65.8% |
| `feature` | adding new functionality | 1h 48m | 16.5% |
| `build` | compile / makefile / dependency work | 1h 21m | 12.4% |
| `bug_fix` | correcting an observed defect | 25m 36s | 3.9% |
| `test` | writing or running tests / benchmarks | 7m 23s | 1.1% |
| `plan` | task tracking, planning | 1m 33s | 0.2% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `build` | 2,572 |
| `test` | 1,054 |
| `bug_fix` | 808 |
| `feature` | 611 |
| `plan` | 173 |
| `understanding` | 151 |
| `unknown` | 1 |

## RQ6 — Failures encountered

Out of **5,370 tool results**, **1,072** (20.0%) contained an error signature.

The user filed **1 bug-report-style prompt(s)** (prompts containing words like 'error', 'crash', 'broken', 'wrong').

## RQ6b — Difficulty assessment

**Auto-label: `Very-High`** (difficulty index 0.81; mean rank across 7 signals = 13.1).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 11.0 | 14.0 |
| Calendar span (days first→last event) | 4 | 9.0 |
| User prompts | 97 | 15.0 |
| Redirect / bug-report prompts | 5 | 11.0 |
| Tool-output error rate | 0.200 | 16.0 |
| Fix cycles (error → immediate retry) | 152 | 16.0 |
| Share of active time spent on `bug_fix` | 0.039 | 11.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 97
- **Average prompt length:** 83 chars; **max:** 410 chars
- **Total chars written by user:** 8,041
- **Sessions:** 4; **span:** 4 days
- **Long-prompt ratio** (≥500 chars): 0/97

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Codex | `gpt-5.4` | 2026-03-29 15:54 | 4d 20h 5m | 89 | 5070 | $102.97 |
| 2 | Codex | `gpt-5.4` | 2026-04-03 12:25 | 58m 13s | 4 | 130 | $3.10 |
| 3 | Codex | `gpt-5.4` | 2026-04-03 13:41 | 5m 9s | 1 | 55 | $0.56 |
| 4 | Codex | `gpt-5.4` | 2026-04-03 13:54 | 44m 38s | 2 | 115 | $1.47 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| other | 53 |
| clarify | 33 |
| review-ask | 6 |
| redirect | 4 |
| bug-report | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-03-29]_ Write a COBOL compiler in COBOL. Demonstrate that you can run some (non-trivial) COBOL programs thanks to the written compiler.
2. _[2026-03-29]_ could you compile/run all COBOL programs available here https://github.com/acherm/agentic-cobol-game15tictactoe/ (commit: 4ae3129ad1f5b6a81cb28c075864781891c0e7a1) with the new compiler
3. _[2026-03-29]_ please create a git and commit
4. _[2026-03-29]_ please design a benchmark based on COBOL programs you have tested so far
5. _[2026-03-29]_ three terminals are running; please stop them... I'd like to compare performance of the compiler compared to traditional compiler like the GNUCobol one
6. _[2026-03-29]_ I don't get why primes, collatz, gcd are not accepted by GnuCOBOL
7. _[2026-03-29]_ yes please... minicobc should support valid COBOL programs
8. _[2026-03-29]_ is minicobc able to compile/build minicobc? and thus bootstrap?
9. _[2026-03-29]_ please extend minicobx until it can compile the current src/minicobc.cob
10. _[2026-03-29]_ sure! please benchmark minicobc when compiled using minicobc

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 4d 21h 53m |
| Active collaboration time | 10h 58m |
| Tool calls | 5,370 |
| Input tokens | 19,706,259 |
| Output tokens | 2,350,772 |
| Cache-read tokens | 479,668,736 |
| Cache-create tokens | 0 |
| Reasoning tokens (Codex) | 1,187,284 |
| Estimated cost at API rack rates | $108.10 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `exec_command` | 4,113 |
| `apply_patch` | 763 |
| `write_stdin` | 443 |
| `update_plan` | 48 |
| `wait_agent` | 2 |
| `read_thread_terminal` | 1 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
