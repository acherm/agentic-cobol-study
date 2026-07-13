# `cobol-pygame-cc` — Case Study

> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-pygame-cc` assessment](../assessments/cobol-pygame-cc.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-pygame-cc/SPECIFICATION_BACKLOG.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-pygame-cc`  
**Sessions.** 1 (1 Claude Code + 0 Codex)  
**Activity window.** 2026-07-08 → 2026-07-08 (0 days)  
**Agents & models.** Claude Code/claude-opus-4-6

---

## RQ1 — Domain, intent, novelty

**From the project's `README.md` (first sections):**

> **# COBOL-Pygame: a pygame-style graphics framework for GnuCOBOL**  
> A thin C/SDL2 library that lets GnuCOBOL programs open a window, draw coloured primitives, load images, and handle keyboard/mouse input. Game logic, physics, and rendering live entirely in COBOL — no handwritten C glue required in the COBOL source. Includes four ready-to-run examples: an interactive demo, a bouncing rectangle, an image-loading test, and a complete Flappy Bird clone written in pure COBOL.

> **## Prerequisites**  
> | Tool | Tested version | Notes | |------|----------------|-------| | GnuCOBOL (`cobc`) | 3.2.0 | must support `-fstatic-call` and `-free` | | SDL2 (`sdl2-config`) | 2.32.x | only the core library; no SDL2_image/mixer | | C compiler (cc/gcc/clang) | Apple Clang 16 | any C11 compiler should work | | GNU Make | 3.81+ | | **macOS (Homebrew):** ```sh brew install gnucobol sdl2 ``` **Debian / Ubuntu:** ```sh sudo apt install gnucobol4 libsdl2-dev ``` > The framework targets **macOS** and **Linux**. > Windows should work under MSYS2/MinGW with the same packages but is untested.

**Opening prompt that kicked off the project:**

```
Create a small "pygame-like" graphical framework that can be called from COBOL programs compiled with GnuCOBOL (cobc). The framework itself may be written in any host language you think appropriate (e.g., a thin C layer over an existing cross-platform graphics/windowing library), as long as the result is a library that a COBOL program can link against and call. The framework must let a COBOL program do the following, through whatever calling convention you design: Initialize and later shut down the graphics subsystem. Open a single resizable window of a requested width and height with a caller-supplied title, and obtain whatever handle(s) are needed to draw into it. Set a current drawing color (RGBA or equivalent). Clear the window to the current color, and present/flip the frame so drawin…
```

## RQ2 — Engineering challenges

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| C compiler error | 2 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **0** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 41 |
| Git commit subjects | 2 |

**Prompt-extracted sub-requests (41)** — first 8 (sub-bullets inside user messages):

- _[2026-07-08]_ **Step 2**: Write an animated bouncing rectangle demo (`bounce.cob`) proving the framework works end-to-end at ~60fps with clean exit.
- _[2026-07-08]_ GnuCOBOL 3.2.0 (`cobc`) compiling free-format COBOL with `-fstatic-call` flag
- _[2026-07-08]_ SDL2 2.32.x as the graphics backend (built-in `SDL_LoadBMP` for BMP support, no extra deps)
- _[2026-07-08]_ Singleton window/renderer pattern (COBOL never handles pointers)
- _[2026-07-08]_ COBOL-to-C interop: `CALL "func" USING BY VALUE / BY REFERENCE ... RETURNING var`
- _[2026-07-08]_ BINARY-LONG maps to C `int32_t` with no alignment padding
- _[2026-07-08]_ COBOL strings are space-padded PIC X(n), C side trims trailing spaces
- _[2026-07-08]_ GnuCOBOL's `-fstatic-call` flag generates direct C function calls instead of runtime dlsym lookups

**Git commits (2)** — first 8:

- `b9482aa7f3` 2026-07-08  Add Flappy Bird clone and rewrite README for fresh users
- `95e7034e50` 2026-07-08  Add pygame-style graphics framework for GnuCOBOL

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `bounce` (55 KB)
- `demo` (55 KB)
- `flappy` (74 KB)
- `gen_test_bmp` (33 KB)
- `imgtest` (56 KB)

## RQ4 — Size and complexity

**File inventory** (19 files, 0.4 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 5 | 915 |
| Markdown | 1 | 407 |
| C | 2 | 349 |
| Makefile | 1 | 50 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 5 |
| Total lines | 915 |
| Code lines (non-blank, non-comment) | 764 |
| Comment lines | 62 |
| Sections | 4 |
| Paragraphs | 48 |
| Data items (level-number declarations) | 159 |
| Max IF/EVALUATE nesting (any file) | 3 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `CALL` | 94 |
| `MOVE` | 48 |
| `IF` | 40 |
| `PERFORM` | 37 |
| `COMPUTE` | 33 |
| `SET` | 22 |
| `DISPLAY` | 16 |
| `ADD` | 14 |
| `STOP` | 13 |
| `MULTIPLY` | 9 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `flappy.cob` | 307 |
| `imgtest.cob` | 156 |
| `demo.cob` | 114 |
| `bounce.cob` | 111 |
| `pygame_cobol.cpy` | 76 |

**Git churn signal.** 2 commits, 1888 insertions / 153 deletions, first 2026-07-08, last 2026-07-08.

## RQ4b — COBOL language mastery

**Mastery score:** **28** distinct COBOL constructs used across **10/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 199 | `IF`×80, `PERFORM`×45, `WHEN`×25, `EVALUATE`×14, `STOP_RUN`×13, `PERFORM_UNTIL`×12, `ELSE`×6, `PERFORM_VARYING`×4 |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 61 | `COMPUTE`×33, `ADD`×14, `MULTIPLY`×9, `SUBTRACT`×5 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 9 | `PIC_X`×6, `PIC_9`×2, `OCCURS`×1 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 7 | `START`×6, `DELETE`×1 |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 8 | `STRING`×4, `DELIMITED_BY`×4 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 2 | `SET`×2 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 357 | `BY_VALUE`×181, `CALL`×94, `USING`×64, `BY_REFERENCE`×18 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 4 | `COPY`×4 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 4 | `FUNCTION`×2, `FUNCTION_TRIM`×2 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 16 | `DISPLAY`×16 |

**Notable non-trivial constructs used:** `CALL` (94×), `OCCURS` (1×), `COPY` (4×), `FUNCTION` (2×).

**Procedural structure.** 48 paragraphs, 4 sections across 5 COBOL file(s). That means roughly **48 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **2h 6m** across 434 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 53m 54s | 42.6% |
| `build` | compile / makefile / dependency work | 53m 37s | 42.4% |
| `feature` | adding new functionality | 11m 52s | 9.4% |
| `bug_fix` | correcting an observed defect | 9m 55s | 7.8% |
| `plan` | task tracking, planning | 0m 28s | 0.4% |
| `performance` | making it faster | 0m 19s | 0.3% |
| `unknown` | could not classify confidently | 0m 3s | 0.0% |
| `spec` | specifications / architecture writing | -1d 23h 56m | -3.0% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `understanding` | 58 |
| `feature` | 54 |
| `build` | 32 |
| `bug_fix` | 5 |
| `plan` | 4 |

## RQ6 — Failures encountered

Out of **153 tool results**, **5** (3.3%) contained an error signature.

The user filed **14 bug-report-style prompt(s)** (prompts containing words like 'error', 'crash', 'broken', 'wrong').

## RQ6b — Difficulty assessment

**Auto-label: `High`** (difficulty index 0.57; mean rank across 7 signals = 9.5).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 2.1 | 11.0 |
| Calendar span (days first→last event) | 0 | 3.5 |
| User prompts | 17 | 8.0 |
| Redirect / bug-report prompts | 14 | 15.5 |
| Tool-output error rate | 0.033 | 6.5 |
| Fix cycles (error → immediate retry) | 2 | 7.0 |
| Share of active time spent on `bug_fix` | 0.078 | 15.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 17
- **Average prompt length:** 2086 chars; **max:** 12,312 chars
- **Total chars written by user:** 35,457
- **Sessions:** 1; **span:** 0 days
- **Long-prompt ratio** (≥500 chars): 8/17

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2026-07-08 09:40 | 5h 30m | 17 | 153 | $90.04 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| bug-report | 14 |
| clarify | 2 |
| initial-spec | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-07-08]_ Create a small "pygame-like" graphical framework that can be called from COBOL programs compiled with GnuCOBOL (cobc). The framework itself may be written in any host language you think appropriate (e.g., a thin C layer over an existing cro…
2. _[2026-07-08]_ mathieuacher@mathieus-macbook-pro cobol-pygame-cc % ./demo libcob: error: module 'pg_init' not found mathieuacher@mathieus-macbook-pro cobol-pygame-cc %
3. _[2026-07-08]_ Using the framework from Step 1, write an example COBOL program that proves the framework actually works end to end. The program must: Open a window of roughly 640 x 480 with a descriptive title. Run a main loop that, on each iteration: pol…
4. _[2026-07-08]_ Extend the framework from Step 1 so that a COBOL program can load an image from disk and draw it into the window. Requirements: Support at least one common image file format that can be loaded without pulling in a heavyweight third-party de…
5. _[2026-07-08]_ mathieuacher@mathieus-macbook-pro cobol-pygame-cc % make run-imgtest ./imgtest --- Testing error handling --- Load correctly failed (rc=-1) Error: Cannot load 'nonexistent.bmp': Parameter 'src' is invalid --- Error handling OK --- Loaded te…
6. _[2026-07-08]_ still an error: mathieuacher@mathieus-macbook-pro cobol-pygame-cc % make run-imgtest ./imgtest --- Testing error handling --- Load correctly failed (rc=-1) Error: Cannot open 'nonexistent.bmp': No such file or directory --- Error handling O…
7. _[2026-07-08]_ mathieuacher@mathieus-macbook-pro cobol-pygame-cc % make run-imgtest ./imgtest --- Testing error handling --- Load correctly failed (rc=-1) Error: Cannot open 'nonexistent.bmp': No such file or directory --- Error handling OK --- Loaded tes…
8. _[2026-07-08]_ This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation. Summary: 1. Primary Request and Intent: The user requested a multi-step project to creat…
9. _[2026-07-08]_ mathieuacher@mathieus-macbook-pro cobol-pygame-cc % make run-imgtest ./imgtest --- Testing error handling --- Load correctly failed (rc=-1) Error: Cannot open 'nonexistent.bmp': No such file or directory --- Error handling OK --- Loaded tes…
10. _[2026-07-08]_ almost perfect... mathieuacher@mathieus-macbook-pro cobol-pygame-cc % make run-imgtest ./imgtest --- Testing error handling --- Load correctly failed (rc=-1) Error: Cannot open 'nonexistent.bmp': No such file or directory --- Error handling…

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 5h 30m |
| Active collaboration time | 2h 6m |
| Tool calls | 153 |
| Input tokens | 345 |
| Output tokens | 489,521 |
| Cache-read tokens | 25,086,132 |
| Cache-create tokens | 837,119 |
| Reasoning tokens (Codex) | 0 |
| Estimated cost at API rack rates | $90.04 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `Bash` | 59 |
| `Edit` | 42 |
| `Read` | 38 |
| `Write` | 14 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
