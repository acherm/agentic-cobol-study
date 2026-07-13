# `COMPILER-COBOL-CLAUDE` — Case Study (repository folder `cobol-compiler-cc`)

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/cobol-compiler-cc/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-compiler-cc` assessment](../assessments/cobol-compiler-cc.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-compiler-cc/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/cobol-compiler-cc/KEY_FEATURES.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-compiler-cc`  
**Sessions.** 3 (3 Claude Code + 0 Codex)  
**Activity window.** 2026-03-29 → 2026-04-05 (11 days)  
**Agents & models.** Claude Code/None, Claude Code/claude-opus-4-6

---

## RQ1 — Domain, intent, novelty

**What it is.** COBOL compiler (and interpreter) written in COBOL.

**Why it's interesting.** Self-hosting-ish: a COBOL→C compiler and a tree-walking interpreter, both authored in COBOL. The compiler's own source is ~11k COBOL LOC.

**From the project's `README.md` (first sections):**

> **# A COBOL Compiler (and Interpreter) Written in COBOL**  
> Two COBOL programs that process other COBOL programs: - **`cobolcc.cob`** (11,044 lines) — A **COBOL-to-C compiler**. Translates COBOL source into C code that compiles to native binaries with gcc. Supports both fixed and free format, COMP-5 binary types, CALL to external C functions, multi-program compilation with LINKAGE SECTION, RECURSIVE programs with paragraph functions, cross-file group struct wrapping, and many COBOL intrinsics. - **`cobolint.cob`** (4,462 lines) — A **COBOL interpreter**. Directly executes COBOL programs through a table-driven interpreter. Slower but fully self-containe…

> **## Quick Start**  
> ```bash

**Opening prompt that kicked off the project:**

```
Write a COBOL compiler in COBOL. Demonstrate that you can run some (non-trivial) COBOL programs thanks to the written compiler.
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- lexer + preprocessor
- parser for COBOL 74/85 subset (fixed+free format)
- PIC/USAGE decoding
- DATA DIVISION → C struct generation
- PROCEDURE DIVISION → C functions
- COMP-5 binary types
- PERFORM THRU paragraph ranges
- RECURSIVE programs
- CALL to external C
- multi-program linking
- COBOL intrinsics library
- benchmark harness vs GnuCOBOL

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| C compiler error | 195 |
| missing file | 24 |
| GnuCOBOL compiler error (incl. syntax) | 13 |
| test suite reported FAIL | 6 |
| segmentation fault at runtime | 2 |
| bus error at runtime | 1 |
| process aborted | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **32** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 80 |
| Git commit subjects | 74 |

**Backlog (32 F-### entries).** Grouped by phase:

- **_unclassified_** — 32 features  
  Bootstrap project skeleton and decide on interpreter-first design; Interpreter correctness on 9 test programs + game15 subsets; Attempt full game15.cob via interpreter (timeout) — motivation for com…; Initial git commit (`0eae806`): interpreter + tests + first README; Interpreter documentation (initial README); New `cobolcc.cob` — COBOL-to-C compiler v1 (5 game tests pass); `cobolcc` verified on game15 / game015 (0.01 s, 20× speedup vs GnuCOBO…; Free-format support, COMP-5, CALL to external C — extend cobolcc for D… _(+24 more)_

**Prompt-extracted sub-requests (80)** — first 8 (sub-bullets inside user messages):

- _[2026-04-03]_ Initial request: Compile and run all COBOL programs from the acherm/agentic-cobol-game15tictactoe repository (specifically commits 4ae3129) using an existing CO…
- _[2026-04-03]_ Final intent: Build a COBOL-to-C compiler that produces native-speed binaries while reusing the existing parser front-end
- _[2026-04-03]_ Self-hosted COBOL tools: Both interpreter and compiler written in COBOL itself, compiled with GnuCOBOL
- _[2026-04-03]_ Three-phase architecture: Load/Preprocess → Parse → Execute (interpreter) or Compile to C (compiler)
- _[2026-04-03]_ Symbol table: Stores 200 variables with type, value, array info
- _[2026-04-03]_ Instruction table: Stores 2000 compiled instructions with opcodes and arguments
- _[2026-04-03]_ Paragraph table: Tracks function definitions and line ranges
- _[2026-04-03]_ Array storage: Uses packed character strings with calculated offsets for 1D, 2D, and nested subscripts

**Git commits (74)** — first 8:

- `a578b0a1ec` 2026-04-10  Update README: chess engine fully working, document EXTERNAL limitation
- `f289f1c911` 2026-04-10  Fix CU-GRP struct wrapping for cross-file CALL USING groups
- `610bd6ddb0` 2026-04-09  Fix LINKAGE group passthrough and self-copy guard for copy-out
- `4ac6bd201c` 2026-04-08  Runtime self-copy guard for LINKAGE group copy-in/copy-out
- `cc1932b80d` 2026-04-08  RECURSIVE frame pointer (Approach E): ALPHABETA/QUIESCE search working
- `da3da4f9e0` 2026-04-07  Fix cob_trim variable comparison, ACCEPT FROM DATE/TIME, FIX-STRING trigger
- `8bcf4e4f26` 2026-04-07  Fix ALPHABETA/QUIESCE: RECURSIVE locals only for programs without paragraphs
- `13163f5472` 2026-04-07  Fix MAKEMOVE legality check: remove _saved_p redirect, perft now 100% correct

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `cobolcc` (701 KB)
- `cobolint` (138 KB)
- `fizzbuzz_cc` (33 KB)
- `game015_cc` (33 KB)
- `game15_8_cc` (33 KB)
- `game15_8_ref` (51 KB)
- `game15_cc` (33 KB)
- `game15_ref` (51 KB)
- `game15l_ref` (51 KB)
- `game15m_ref` (51 KB)
- _(+18 more)_

## RQ4 — Size and complexity

**File inventory** (107 files, 4.1 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 36 | 18,908 |
| C | 16 | 3,068 |
| Markdown | 3 | 742 |
| Shell | 1 | 332 |
| C/Header | 2 | 67 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 36 |
| Total lines | 18,908 |
| Code lines (non-blank, non-comment) | 15,912 |
| Comment lines | 2,201 |
| Sections | 40 |
| Paragraphs | 266 |
| Data items (level-number declarations) | 980 |
| Max IF/EVALUATE nesting (any file) | 20 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 3,127 |
| `IF` | 1,523 |
| `PERFORM` | 1,212 |
| `ADD` | 713 |
| `EXIT` | 299 |
| `DISPLAY` | 245 |
| `STRING` | 245 |
| `COMPUTE` | 150 |
| `SUBTRACT` | 103 |
| `STOP` | 63 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `cobolcc.cob` | 9,436 |
| `cobolint.cob` | 3,568 |
| `agentic-cobol-game15tictactoe/game015tree.cob` | 436 |
| `agentic-cobol-game15tictactoe/game15tree.cob` | 434 |
| `agentic-cobol-game15tictactoe/gameN.cob` | 289 |

**Git churn signal.** 74 commits, 17929 insertions / 954 deletions, first 2026-03-31, last 2026-04-10.

## RQ4b — COBOL language mastery

**Mastery score:** **57** distinct COBOL constructs used across **10/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 6,333 | `IF`×3052, `PERFORM`×1619, `ELSE`×479, `PERFORM_UNTIL`×366, `EXIT`×303, `PERFORM_VARYING`×255, `WHEN`×121, `STOP_RUN`×51 _(+4 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 1,075 | `ADD`×721, `COMPUTE`×183, `SUBTRACT`×111, `DIVIDE`×44, `MULTIPLY`×16 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 1,009 | `PIC_9`×595, `PIC_X`×183, `OCCURS`×161, `PIC_S9`×22, `REDEFINES`×21, `FILLER`×18, `USAGE_POINTER`×4, `LEVEL_88`×3 _(+1 more)_ |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 308 | `WRITE`×194, `START`×68, `READ`×8, `CLOSE`×8, `AT_END`×8, `OPEN_INPUT`×5, `FD`×4, `SELECT`×4 _(+3 more)_ |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 670 | `STRING`×530, `REFERENCE_MOD`×119, `UNSTRING`×16, `DELIMITED_BY`×3, `INSPECT`×1, `INSPECT_TALLYING`×1 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 56 | `INITIALIZE`×36, `SET`×20 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 172 | `CALL`×55, `GIVING`×50, `USING`×44, `RECURSIVE`×23 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 45 | `COPY`×45 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 2,488 | `FUNCTION`×1248, `FUNCTION_TRIM`×1066, `FUNCTION_LENGTH`×146, `FUNCTION_NUMVAL`×17, `FUNCTION_UPPER`×11 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 421 | `DISPLAY`×386, `ACCEPT`×35 |

**Notable non-trivial constructs used:** `CALL` (55×), `RECURSIVE` (23×), `OCCURS` (161×), `REDEFINES` (21×), `USAGE_COMP_5` (2×), `COPY` (45×), `FD` (4×), `UNSTRING` (16×), `FUNCTION` (1248×).

**Procedural structure.** 266 paragraphs, 40 sections across 36 COBOL file(s). That means roughly **266 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **1d 8h 30m** across 10225 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `build` | compile / makefile / dependency work | 19h 12m | 59.1% |
| `understanding` | reading / searching to build a mental model | 9h 42m | 29.9% |
| `feature` | adding new functionality | 1h 11m | 3.7% |
| `bug_fix` | correcting an observed defect | 1h 2m | 3.2% |
| `unknown` | could not classify confidently | 41m 9s | 2.1% |
| `plan` | task tracking, planning | 17m 12s | 0.9% |
| `spec` | specifications / architecture writing | 13m 16s | 0.7% |
| `test` | writing or running tests / benchmarks | 7m 10s | 0.4% |
| `doc` | README / comments / final reports | 2m 37s | 0.1% |
| `performance` | making it faster | 0m 52s | 0.0% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `understanding` | 1,610 |
| `build` | 964 |
| `feature` | 629 |
| `bug_fix` | 309 |
| `plan` | 171 |
| `test` | 57 |

## RQ6 — Failures encountered

Out of **3,740 tool results**, **325** (8.7%) contained an error signature.

The user filed **9 bug-report-style prompt(s)** (prompts containing words like 'error', 'crash', 'broken', 'wrong').

## RQ6b — Difficulty assessment

**Auto-label: `Very-High`** (difficulty index 0.83; mean rank across 7 signals = 13.5).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 32.5 | 16.0 |
| Calendar span (days first→last event) | 11 | 11.0 |
| User prompts | 98 | 16.0 |
| Redirect / bug-report prompts | 14 | 15.5 |
| Tool-output error rate | 0.087 | 11.0 |
| Fix cycles (error → immediate retry) | 42 | 15.0 |
| Share of active time spent on `bug_fix` | 0.032 | 10.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 98
- **Average prompt length:** 512 chars; **max:** 13,502 chars
- **Total chars written by user:** 50,178
- **Sessions:** 3; **span:** 11 days
- **Long-prompt ratio** (≥500 chars): 3/98

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2026-03-29 15:55 | 11d 13h 49m | 97 | 3734 | $5183.70 |
| 2 | Claude Code | `None` | 2026-03-30 08:54 | 0m 2s | 6 | 0 | $0.00 |
| 3 | Claude Code | `claude-opus-4-6` | 2026-04-05 21:30 | 30m 58s | 3 | 6 | $1.27 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| other | 50 |
| clarify | 32 |
| bug-report | 9 |
| redirect | 5 |
| review-ask | 2 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-03-29]_ Write a COBOL compiler in COBOL. Demonstrate that you can run some (non-trivial) COBOL programs thanks to the written compiler.
2. _[2026-03-30]_ could you compile/run all COBOL programs available here https://github.com/acherm/agentic-cobol-game15tictactoe/ (commit: 4ae3129ad1f5b6a81cb28c075864781891c0e7a1) with the new compiler
3. _[2026-03-30]_ <task-notification> <task-id>b3mv77ax4</task-id> <tool-use-id>toolu_01JHNTr1kLnQZDrDvvoxuKVp</tool-use-id> <output-file>/private/tmp/claude-501/-Users-mathieuacher-SANDBOX-cobol-compiler-cc/625f1b9f-c4c4-41ca-ad54-354184c6cf34/tasks/b3mv77a…
4. _[2026-03-30]_ <task-notification> <task-id>bsy9icr96</task-id> <tool-use-id>toolu_016XSooUeXYjVRCyUTVp5fbG</tool-use-id> <output-file>/private/tmp/claude-501/-Users-mathieuacher-SANDBOX-cobol-compiler-cc/625f1b9f-c4c4-41ca-ad54-354184c6cf34/tasks/bsy9icr…
5. _[2026-03-30]_ <task-notification> <task-id>btglq5070</task-id> <tool-use-id>toolu_01CwtwQ1YmBwbbroBP6tW1Lq</tool-use-id> <output-file>/private/tmp/claude-501/-Users-mathieuacher-SANDBOX-cobol-compiler-cc/625f1b9f-c4c4-41ca-ad54-354184c6cf34/tasks/btglq50…
6. _[2026-03-30]_ <task-notification> <task-id>b9up2yzrh</task-id> <tool-use-id>toolu_013kf5D8GHCNv8f5hiPrhvCc</tool-use-id> <output-file>/private/tmp/claude-501/-Users-mathieuacher-SANDBOX-cobol-compiler-cc/625f1b9f-c4c4-41ca-ad54-354184c6cf34/tasks/b9up2yz…
7. _[2026-03-30]_ <task-notification> <task-id>bg3hxcyq5</task-id> <tool-use-id>toolu_019GarHugtg46yRmcskMC5yX</tool-use-id> <output-file>/private/tmp/claude-501/-Users-mathieuacher-SANDBOX-cobol-compiler-cc/625f1b9f-c4c4-41ca-ad54-354184c6cf34/tasks/bg3hxcy…
8. _[2026-03-30]_ <task-notification> <task-id>bkr82a10t</task-id> <tool-use-id>toolu_01H9gTgKGMz1oXtuNmKDh9Tk</tool-use-id> <output-file>/private/tmp/claude-501/-Users-mathieuacher-SANDBOX-cobol-compiler-cc/625f1b9f-c4c4-41ca-ad54-354184c6cf34/tasks/bkr82a1…
9. _[2026-03-30]_ <task-notification> <task-id>b4b91l9uu</task-id> <tool-use-id>toolu_01JHXqHpUygTLCKQQRRjeJoF</tool-use-id> <output-file>/private/tmp/claude-501/-Users-mathieuacher-SANDBOX-cobol-compiler-cc/625f1b9f-c4c4-41ca-ad54-354184c6cf34/tasks/b4b91l9…
10. _[2026-03-30]_ <task-notification> <task-id>bmhbchi4v</task-id> <tool-use-id>toolu_011ZA4uBbL8z7XVG14mMCRZJ</tool-use-id> <output-file>/private/tmp/claude-501/-Users-mathieuacher-SANDBOX-cobol-compiler-cc/625f1b9f-c4c4-41ca-ad54-354184c6cf34/tasks/bmhbchi…

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 11d 14h 20m |
| Active collaboration time | 1d 8h 30m |
| Tool calls | 3,740 |
| Input tokens | 7,243 |
| Output tokens | 1,567,526 |
| Cache-read tokens | 2,933,801,019 |
| Cache-create tokens | 35,551,366 |
| Reasoning tokens (Codex) | 0 |
| Estimated cost at API rack rates | $5184.96 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `Bash` | 1,932 |
| `Edit` | 656 |
| `Read` | 649 |
| `Grep` | 402 |
| `TaskUpdate` | 39 |
| `TaskCreate` | 23 |
| `Agent` | 19 |
| `Write` | 15 |
| `ToolSearch` | 5 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
