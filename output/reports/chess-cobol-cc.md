# `CHESS-COBOL-CLAUDE` — Case Study (repository folder `chess-cobol-cc`)

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/chess-cobol-cc/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`chess-cobol-cc` assessment](../assessments/chess-cobol-cc.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/chess-cobol-cc/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/chess-cobol-cc/KEY_FEATURES.md)

**Project root.** `/Users/mathieuacher/SANDBOX/chess-cobol-cc`  
**Sessions.** 1 (1 Claude Code + 0 Codex)  
**Activity window.** 2026-03-12 → 2026-03-30 (17 days)  
**Agents & models.** Claude Code/claude-opus-4-6

---

## RQ1 — Domain, intent, novelty

**What it is.** Chess engine in COBOL (GnuCOBOL).

**Why it's interesting.** Writing a performance-sensitive UCI-speaking engine in a language nobody writes engines in. Elo is the objective measure.

**From the project's `README.md` (first sections):**

> **# agentic-chessengine-cobol-cc**  
> An **agentic chess engine** in **COBOL**, created and supervised by Mathieu Acher (mathieu.acher@irisa.fr) with the **Claude Code (Opus 4.6/4.7)** coding agent.

> **## Build / play**  
> Each repository contains the engine source, build files, and any gameplay artefacts (PGN records, perft logs) preserved from the authoring sessions. Open the per-folder build instructions in the root files (`Cargo.toml`, `Makefile`, `pom.xml`, `*.cabal`, `lakefile.lean`, etc.) for build commands.

**Opening prompt that kicked off the project:**

```
I want to build a chess engine in COBOL (using GNU Cobol)… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of “similar” levels.
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- FEN parser
- UCI protocol I/O
- bitboard or mailbox representation
- move generation (pseudo-legal / legal, castling, en-passant)
- search with alpha-beta + move ordering
- evaluation function
- time management for cutechess matches

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| C compiler error | 8 |
| missing file | 6 |
| command not found | 1 |
| test suite reported FAIL | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **51** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 99 |
| Git commit subjects | 1 |

**Backlog (51 F-### entries).** Grouped by phase:

- **_unclassified_** — 51 features  
  EP-bootstrap; EP-bootstrap; EP-P1; EP-P1; EP-P1; EP-P1; EP-P1; EP-P1 _(+43 more)_

**Prompt-extracted sub-requests (99)** — first 8 (sub-bullets inside user messages):

- _[2026-03-12]_ Phase 1: Board + UCI + random moves (~200-400 Elo) ✅ COMPLETE
- _[2026-03-12]_ Phase 2: Material evaluation + 1-ply search (~600-800 Elo) ✅ COMPLETE
- _[2026-03-12]_ Phase 3: Alpha-beta + depth 3-4 + PSTs (~1000-1200 Elo) 🔧 IN PROGRESS
- _[2026-03-12]_ Phase 4: Iterative deepening + time management (~1200+ Elo)
- _[2026-03-12]_ GNU COBOL 3.2.0 (fixed-format source, `>>SOURCE FORMAT IS FIXED`)
- _[2026-03-12]_ UCI (Universal Chess Interface) protocol for engine communication
- _[2026-03-12]_ cutechess-cli for automated engine testing and Elo estimation
- _[2026-03-12]_ Stockfish 18 as opponent (with UCI_LimitStrength/UCI_Elo=1320)

**Git commits (1)** — first 8:

- `95aa4b3c6e` 2026-05-04  Add agentic chess-engine README, LICENSE, .gitignore

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `chess-engine` (105 KB)
- `chess-engine-dbg` (57 KB)
- `chess-engine-fast` (89 KB)
- `chess-engine-new` (57 KB)
- `chess-engine-noopt` (272 KB)
- `chess-engine-o1` (105 KB)
- `chess-engine-o3` (57 KB)
- `chess-engine-os` (61 KB)
- `chess-engine-test2` (105 KB)
- `chess-engine-v1` (89 KB)
- _(+6 more)_

## RQ4 — Size and complexity

**File inventory** (49 files, 3.3 MB).

| Language | Files | LOC |
|---|---:|---:|
| C | 1 | 7,667 |
| COBOL | 1 | 3,460 |
| C/Header | 2 | 451 |
| Markdown | 1 | 17 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 1 |
| Total lines | 3,460 |
| Code lines (non-blank, non-comment) | 2,920 |
| Comment lines | 366 |
| Sections | 2 |
| Paragraphs | 81 |
| Data items (level-number declarations) | 701 |
| Max IF/EVALUATE nesting (any file) | 10 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 535 |
| `IF` | 279 |
| `PERFORM` | 170 |
| `COMPUTE` | 86 |
| `ADD` | 58 |
| `SUBTRACT` | 27 |
| `EXIT` | 18 |
| `EVALUATE` | 14 |
| `DISPLAY` | 9 |
| `DIVIDE` | 6 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `chess-engine.cob` | 2,920 |

**Git churn signal.** 1 commits, 30912 insertions / 0 deletions, first 2026-05-04, last 2026-05-04.

## RQ4b — COBOL language mastery

**Mastery score:** **38** distinct COBOL constructs used across **10/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 1,020 | `IF`×557, `PERFORM`×209, `WHEN`×73, `ELSE`×59, `PERFORM_UNTIL`×38, `EVALUATE`×31, `PERFORM_VARYING`×28, `EXIT`×18 _(+2 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 206 | `ADD`×87, `COMPUTE`×86, `SUBTRACT`×27, `DIVIDE`×6 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 1,107 | `PIC_S9`×468, `FILLER`×416, `PIC_9`×144, `PIC_X`×44, `OCCURS`×23, `REDEFINES`×9, `LEVEL_88`×3 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 7 | `START`×7 |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 27 | `REFERENCE_MOD`×13, `STRING`×6, `INSPECT`×4, `INSPECT_TALLYING`×4 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 82 | `SORT`×69, `SEARCH`×8, `INITIALIZE`×5 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 7 | `GIVING`×6, `RECURSIVE`×1 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 3 | `COPY`×3 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 37 | `FUNCTION`×29, `FUNCTION_NUMVAL`×6, `FUNCTION_TRIM`×1, `FUNCTION_MOD`×1 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 13 | `DISPLAY`×9, `ACCEPT`×4 |

**Notable non-trivial constructs used:** `RECURSIVE` (1×), `OCCURS` (23×), `REDEFINES` (9×), `COPY` (3×), `FUNCTION` (29×).

**Procedural structure.** 81 paragraphs, 2 sections across 1 COBOL file(s). That means roughly **81 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **15h 31m** across 3023 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 7h 58m | 51.4% |
| `build` | compile / makefile / dependency work | 6h 46m | 43.7% |
| `feature` | adding new functionality | 22m 57s | 2.5% |
| `spec` | specifications / architecture writing | 10m 46s | 1.2% |
| `unknown` | could not classify confidently | 4m 47s | 0.5% |
| `test` | writing or running tests / benchmarks | 3m 3s | 0.3% |
| `bug_fix` | correcting an observed defect | 2m 24s | 0.3% |
| `plan` | task tracking, planning | 2m 23s | 0.3% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `understanding` | 614 |
| `build` | 226 |
| `feature` | 182 |
| `plan` | 57 |
| `test` | 42 |
| `bug_fix` | 35 |

## RQ6 — Failures encountered

Out of **1,155 tool results**, **32** (2.8%) contained an error signature.

## RQ6b — Difficulty assessment

**Auto-label: `High`** (difficulty index 0.61; mean rank across 7 signals = 10.1).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 15.5 | 15.0 |
| Calendar span (days first→last event) | 17 | 12.0 |
| User prompts | 47 | 14.0 |
| Redirect / bug-report prompts | 3 | 7.5 |
| Tool-output error rate | 0.028 | 5.0 |
| Fix cycles (error → immediate retry) | 5 | 11.5 |
| Share of active time spent on `bug_fix` | 0.003 | 6.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 47
- **Average prompt length:** 1793 chars; **max:** 16,704 chars
- **Total chars written by user:** 84,275
- **Sessions:** 1; **span:** 17 days
- **Long-prompt ratio** (≥500 chars): 35/47

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2026-03-12 19:37 | 17d 22h 51m | 47 | 1156 | $518.44 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| other | 29 |
| clarify | 8 |
| review-ask | 6 |
| redirect | 3 |
| resume | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-03-12]_ I want to build a chess engine in COBOL (using GNU Cobol)… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of “similar” levels.
2. _[2026-03-12]_ Let's go for Phase 1
3. _[2026-03-12]_ go to Phase 2
4. _[2026-03-12]_ go
5. _[2026-03-12]_ This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation. Summary: 1. Primary Request and Intent: The user wants to build a chess engine in COBOL …
6. _[2026-03-12]_ [Request interrupted by user for tool use]
7. _[2026-03-12]_ continue
8. _[2026-03-13]_ <task-notification> <task-id>b5y7uxkbk</task-id> <tool-use-id>toolu_01G6eFoKtQ2kQf9kiiVEiZ5q</tool-use-id> <output-file>/private/tmp/claude-501/-Users-mathieuacher-SANDBOX-chess-cobol-cc/9d9bb74e-18ea-4bb9-844c-b4e175998988/tasks/b5y7uxkbk.…
9. _[2026-03-13]_ <task-notification> <task-id>b9gc360t3</task-id> <tool-use-id>toolu_01Xgstr3TuVZosfMKkMxxmRs</tool-use-id> <output-file>/private/tmp/claude-501/-Users-mathieuacher-SANDBOX-chess-cobol-cc/9d9bb74e-18ea-4bb9-844c-b4e175998988/tasks/b9gc360t3.…
10. _[2026-03-13]_ continue

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 17d 22h 51m |
| Active collaboration time | 15h 31m |
| Tool calls | 1,156 |
| Input tokens | 1,937 |
| Output tokens | 591,930 |
| Cache-read tokens | 166,713,533 |
| Cache-create tokens | 11,943,652 |
| Reasoning tokens (Codex) | 0 |
| Estimated cost at API rack rates | $518.44 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `Bash` | 712 |
| `Edit` | 178 |
| `Read` | 143 |
| `Grep` | 57 |
| `TaskOutput` | 53 |
| `Write` | 9 |
| `ToolSearch` | 2 |
| `Agent` | 2 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
