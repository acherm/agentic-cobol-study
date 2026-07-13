# `PYGAME-COBOL-CODEX` — Case Study (repository folder `COBOL-pygame`)

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/COBOL-pygame/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`COBOL-pygame` assessment](../assessments/COBOL-pygame.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/COBOL-pygame/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/COBOL-pygame/KEY_FEATURES.md)
  
> 🔁 **Replay prompts** (step-wise, HOW-agnostic, for reproducing with a different agent): [`REPLAY_PROMPTS.md`](../backlogs/COBOL-pygame/REPLAY_PROMPTS.md)

**Project root.** `/Users/mathieuacher/SANDBOX/COBOL-pygame`  
**Sessions.** 2 (1 Claude Code + 1 Codex)  
**Activity window.** 2026-02-09 → 2026-03-19 (0 days)  
**Agents & models.** Claude Code/claude-opus-4-6, Codex/gpt-5.2

---

## RQ1 — Domain, intent, novelty

**What it is.** A pygame-like framework callable from COBOL (GnuCOBOL).

**Why it's interesting.** C glue + COPY books exposing pygame-style primitives to COBOL programs.

**From the project's `README.md` (first sections):**

> **# COBOL PyGame (SDL2) for GnuCOBOL**  
> This is a tiny "pygame-like" framework for **COBOL** built on **SDL2**, meant to be used with **GnuCOBOL (`cobc`)**. Created in a single Codex (GPT-5.2) session on 2026-02-09. It is **not** full pygame. It provides a minimal subset: - init / quit - create a window + renderer - clear / present - draw primitives (line, rect, filled rect) - event polling (quit, keyboard, mouse) - timing (delay, ticks) - load and render **BMP** textures (SDL2 built-in `SDL_LoadBMP`)

> **## Prerequisites**  
> - GnuCOBOL (`cobc`) >= 3.2 - SDL2 development headers and libraries (`sdl2-config` must be on PATH)

**Opening prompt that kicked off the project:**

```
Write a pygame framework for COBOL (using GNUcobol)
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- Python/C integration
- COBOL → C FFI via CALL
- input/event loop
- sample games

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| command exited with non-zero status | 3 |
| C compiler error | 2 |
| GnuCOBOL compiler error (incl. syntax) | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **11** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 31 |
| Git commit subjects | 1 |

**Backlog (11 F-### entries).** Grouped by phase:

- **_unclassified_** — 11 features  
  Environment Discovery & Toolchain Validation; API Design (pygame-like C API); Scaffold Project (all source files); First Build & COBOL Data Type Fix; Fix Runtime Module Lookup (Bug Fix); Makefile Hardening (Prerequisite Tracking); README Update (Static Call Note); Flappy Bird Game Implementation _(+3 more)_

**Prompt-extracted sub-requests (31)** — first 8 (sub-bullets inside user messages):

- _[2026-03-19]_ PASS 1 (Extraction): reconstruct (i) a USER-DRIVEN Feature Backlog, (ii) an AGENT-CENTRIC Specification Backlog (step-wise), plus Prompt Ledger + Replay Package…
- _[2026-03-19]_ SPECIFICATION_BACKLOG.md
- _[2026-03-19]_ README.md (must reference SPECIFICATION_BACKLOG.md)
- _[2026-03-19]_ PASS 2 (Interpretation): characterize strategies, outcomes/quality, interaction demand; correlate with lightweight metrics.
- _[2026-03-19]_ I will NOT provide transcripts proactively.
- _[2026-03-19]_ You must analyze the repo as-is (git history may be minimal/absent).
- _[2026-03-19]_ Codex stores local state under CODEX_HOME (defaults to ~/.codex).
- _[2026-03-19]_ $CODEX_HOME/sessions/**.jsonl (session event streams)

**Git commits (1)** — first 8:

- `b2095a1ce0` 2026-03-19  Initial commit: pygame-like SDL2 framework for COBOL + Flappy Bird

## RQ3 — What was delivered

**From `REPORT.md`:**

> **# Post-Session Backlog & Strategy Report**  
> 

> **## Session: "Add pygame framework for COBOL"**  
> - **Session ID**: `019c41c6-066e-7fc2-80fc-df9d9c702a1e` - **Date**: 2026-02-09, 09:40–10:41 UTC (~61 minutes) - **Agent**: GPT-5.2 via Codex Desktop 0.98.0 - **Model provider**: OpenAI - **Reasoning effort**: xhigh - **Tokens**: ~1.15M total (input: ~1.1M, output: ~48K, reasoning: ~34K) ---

## RQ4 — Size and complexity

**File inventory** (12 files, 0.1 MB).

| Language | Files | LOC |
|---|---:|---:|
| Markdown | 3 | 775 |
| COBOL | 3 | 492 |
| JSON | 1 | 472 |
| C | 1 | 367 |
| C/Header | 1 | 55 |
| Makefile | 1 | 47 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 3 |
| Total lines | 492 |
| Code lines (non-blank, non-comment) | 398 |
| Comment lines | 11 |
| Sections | 2 |
| Paragraphs | 11 |
| Data items (level-number declarations) | 90 |
| Max IF/EVALUATE nesting (any file) | 2 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `CALL` | 39 |
| `IF` | 33 |
| `PERFORM` | 30 |
| `MOVE` | 26 |
| `COMPUTE` | 21 |
| `SET` | 13 |
| `STOP` | 6 |
| `ADD` | 5 |
| `DISPLAY` | 4 |
| `MULTIPLY` | 4 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `examples/flappy.cob` | 282 |
| `examples/hello.cob` | 88 |
| `cobol/cpg.cpy` | 28 |

**Git churn signal.** 1 commits, 2222 insertions / 0 deletions, first 2026-03-19, last 2026-03-19.

## RQ4b — COBOL language mastery

**Mastery score:** **31** distinct COBOL constructs used across **10/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 134 | `IF`×66, `PERFORM`×41, `PERFORM_UNTIL`×9, `PERFORM_VARYING`×7, `STOP_RUN`×6, `EXIT`×3, `ELSE`×2 |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 31 | `COMPUTE`×21, `ADD`×5, `MULTIPLY`×4, `SUBTRACT`×1 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 125 | `USAGE_COMP_5`×55, `PIC_S9`×54, `PIC_X`×8, `USAGE_POINTER`×3, `PIC_9`×2, `LEVEL_88`×2, `OCCURS`×1 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 3 | `START`×3 |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 7 | `DELIMITED_BY`×5, `STRING`×2 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 6 | `SET`×6 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 159 | `BY_VALUE`×57, `CALL`×39, `BY_REFERENCE`×33, `USING`×30 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 2 | `COPY`×2 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 7 | `FUNCTION`×4, `FUNCTION_RANDOM`×2, `FUNCTION_TRIM`×1 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 4 | `DISPLAY`×4 |

**Notable non-trivial constructs used:** `CALL` (39×), `OCCURS` (1×), `USAGE_COMP_5` (55×), `COPY` (2×), `FUNCTION` (4×).

**Procedural structure.** 11 paragraphs, 2 sections across 3 COBOL file(s). That means roughly **11 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **4m 16s** across 97 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `feature` | adding new functionality | 3m 17s | 77.0% |
| `understanding` | reading / searching to build a mental model | 0m 39s | 15.2% |
| `bug_fix` | correcting an observed defect | 0m 13s | 5.1% |
| `plan` | task tracking, planning | 0m 5s | 2.0% |
| `build` | compile / makefile / dependency work | 0m 2s | 0.8% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `build` | 11 |
| `plan` | 9 |
| `feature` | 7 |
| `bug_fix` | 3 |
| `understanding` | 1 |

## RQ6 — Failures encountered

Out of **31 tool results**, **3** (9.7%) contained an error signature.

The user filed **1 bug-report-style prompt(s)** (prompts containing words like 'error', 'crash', 'broken', 'wrong').

## RQ6b — Difficulty assessment

**Auto-label: `Medium`** (difficulty index 0.37; mean rank across 7 signals = 6.5).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 0.1 | 2.0 |
| Calendar span (days first→last event) | 0 | 3.5 |
| User prompts | 3 | 2.0 |
| Redirect / bug-report prompts | 1 | 5.0 |
| Tool-output error rate | 0.097 | 12.0 |
| Fix cycles (error → immediate retry) | 3 | 9.0 |
| Share of active time spent on `bug_fix` | 0.051 | 12.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 3
- **Average prompt length:** 115 chars; **max:** 229 chars
- **Total chars written by user:** 345
- **Sessions:** 2; **span:** 0 days
- **Long-prompt ratio** (≥500 chars): 1/3

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Codex | `gpt-5.2` | 2026-02-09 09:40 | 1h 1m | 3 | 31 | $0.70 |
| 2 | Claude Code | `claude-opus-4-6` | 2026-03-19 15:47 | 34m 29s | 5 | 51 | $15.90 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| other | 2 |
| bug-report | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-02-09]_ Write a pygame framework for COBOL (using GNUcobol)
2. _[2026-02-09]_ mathieuacher@Mathieus-MacBook-Pro COBOL-pygame % make make: Nothing to be done for `all'. mathieuacher@Mathieus-MacBook-Pro COBOL-pygame % make run ./build/hello libcob: error: module 'cpg_init' not found make: *** [run] Error 1
3. _[2026-02-09]_ write a Flappy bird in COBOL now, thanks to the new framework.

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 1h 1m |
| Active collaboration time | 4m 16s |
| Tool calls | 31 |
| Input tokens | 76,222 |
| Output tokens | 47,872 |
| Cache-read tokens | 1,025,920 |
| Cache-create tokens | 0 |
| Reasoning tokens (Codex) | 34,000 |
| Estimated cost at API rack rates | $0.70 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `exec_command` | 12 |
| `apply_patch` | 10 |
| `update_plan` | 9 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
