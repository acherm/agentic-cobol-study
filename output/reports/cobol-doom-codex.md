# `cobol-doom-codex` — Case Study

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/cobol-doom-codex/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-doom-codex` assessment](../assessments/cobol-doom-codex.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-doom-codex/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/cobol-doom-codex/KEY_FEATURES.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-doom-codex`  
**Sessions.** 1 (0 Claude Code + 1 Codex)  
**Activity window.** 2026-04-17 → 2026-04-18 (0 days)  
**Agents & models.** Codex/gpt-5.4

---

## RQ1 — Domain, intent, novelty

**What it is.** Doom-like FPS in COBOL (Codex) — gridwalker + SDL2 bridge + 11 COPY books.

**Why it's interesting.** Codex-built Doom replica with SDL2 graphical rendering (not terminal-only); modular via 11 COPY books.

**Opening prompt that kicked off the project:**

```
Write a COBOL program (GnuCOBOL) that runs in a terminal and lets a human walk around a 2-D grid level from a top-down view. Required behaviour: The level is a rectangular grid (roughly 20×20 or larger) made of wall cells and open cells, with a clearly visible layout of rooms and corridors. The view is a top-down ASCII map: walls, open floor, and the player drawn at the player's current cell with a symbol that indicates facing direction. The player can move with keys W/A/S/D (or the arrow keys) and quit with Q or ESC. Input must be read without requiring the user to press Enter after each key. The player cannot walk through walls. Attempts to do so leave the player in place. The screen is redrawn after every input so the view stays current. Redrawing must not scroll — the map stays anchore…
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- ray casting via integer trig
- SDL2 bridge from COBOL via C glue
- enemies / pickups / multi-level
- modular COPY-book architecture (11 modules)
- BMP sprite assets

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| command exited with non-zero status | 15 |
| C compiler error | 10 |
| Python traceback (tooling) | 4 |
| missing file | 4 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **0** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 0 |
| Git commit subjects | 10 |

**Git commits (10)** — first 8:

- `02f13a1ea6` 2026-04-18  Add demo launcher and SDL polish
- `9fbcff207b` 2026-04-18  Split COBOL core into copybooks
- `76758985db` 2026-04-18  Refactor COBOL game core structure
- `eee50f8318` 2026-04-18  Add multi-level campaign and start menu
- `fd84dc9fbc` 2026-04-18  Add pickups weapons and HUD
- `866fe4d1b7` 2026-04-17  Add enemies and combat systems
- `4219ca2459` 2026-04-17  Move raycasting core back into COBOL
- `6c516b8c5a` 2026-04-17  Add helper-backed visual raycaster

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `demo` (50 KB)
- `gridwalker` (186 KB)

## RQ4 — Size and complexity

**File inventory** (81 files, 122.6 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 12 | 2,096 |
| C | 2 | 1,839 |
| Makefile | 1 | 21 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 12 |
| Total lines | 2,096 |
| Code lines (non-blank, non-comment) | 1,906 |
| Comment lines | 4 |
| Sections | 10 |
| Paragraphs | 169 |
| Data items (level-number declarations) | 626 |
| Max IF/EVALUATE nesting (any file) | 3 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 222 |
| `PERFORM` | 145 |
| `IF` | 125 |
| `COMPUTE` | 107 |
| `CALL` | 31 |
| `ADD` | 17 |
| `SUBTRACT` | 14 |
| `EXIT` | 13 |
| `EVALUATE` | 5 |
| `SET` | 2 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `levels.cpy` | 447 |
| `gridwalker_render.cpy` | 405 |
| `gridwalker_data.cpy` | 245 |
| `gridwalker_raycast.cpy` | 160 |
| `gridwalker_entity.cpy` | 127 |

**Git churn signal.** 10 commits, 6811 insertions / 2852 deletions, first 2026-04-17, last 2026-04-18.

## RQ4b — COBOL language mastery

**Mastery score:** **28** distinct COBOL constructs used across **10/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 535 | `IF`×250, `PERFORM`×172, `PERFORM_UNTIL`×24, `ELSE`×23, `PERFORM_VARYING`×20, `WHEN`×17, `EXIT`×17, `EVALUATE`×12 |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 142 | `COMPUTE`×111, `ADD`×17, `SUBTRACT`×14 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 537 | `PIC_S9`×220, `USAGE_COMP_5`×220, `PIC_X`×69, `OCCURS`×28 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 41 | `START`×35, `SELECT`×4, `READ`×2 |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 2 | `INSPECT`×2 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 68 | `SORT`×43, `INITIALIZE`×15, `SET`×10 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 65 | `CALL`×42, `USING`×21, `BY_VALUE`×2 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 11 | `COPY`×11 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 40 | `FUNCTION`×40 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 3 | `DISPLAY`×3 |

**Notable non-trivial constructs used:** `CALL` (42×), `OCCURS` (28×), `USAGE_COMP_5` (220×), `COPY` (11×), `FUNCTION` (40×).

**Procedural structure.** 169 paragraphs, 10 sections across 12 COBOL file(s). That means roughly **169 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **2h 1m** across 1920 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 1h 10m | 57.7% |
| `feature` | adding new functionality | 31m 54s | 26.2% |
| `build` | compile / makefile / dependency work | 16m 29s | 13.5% |
| `plan` | task tracking, planning | 1m 1s | 0.8% |
| `unknown` | could not classify confidently | 1m 0s | 0.8% |
| `test` | writing or running tests / benchmarks | 0m 48s | 0.7% |
| `bug_fix` | correcting an observed defect | 0m 13s | 0.2% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `build` | 264 |
| `test` | 99 |
| `feature` | 84 |
| `understanding` | 68 |
| `plan` | 63 |
| `unknown` | 37 |
| `bug_fix` | 16 |

## RQ6 — Failures encountered

Out of **631 tool results**, **21** (3.3%) contained an error signature.

## RQ6b — Difficulty assessment

**Auto-label: `Medium`** (difficulty index 0.46; mean rank across 7 signals = 7.9).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 2.0 | 9.0 |
| Calendar span (days first→last event) | 0 | 3.5 |
| User prompts | 32 | 13.0 |
| Redirect / bug-report prompts | 4 | 9.5 |
| Tool-output error rate | 0.033 | 6.5 |
| Fix cycles (error → immediate retry) | 3 | 9.0 |
| Share of active time spent on `bug_fix` | 0.002 | 5.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 32
- **Average prompt length:** 283 chars; **max:** 1,404 chars
- **Total chars written by user:** 9,063
- **Sessions:** 1; **span:** 0 days
- **Long-prompt ratio** (≥500 chars): 6/32

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Codex | `gpt-5.4` | 2026-04-17 16:34 | 20h 14m | 31 | 631 | $11.28 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| other | 15 |
| clarify | 12 |
| redirect | 4 |
| initial-spec | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-04-17]_ Write a COBOL program (GnuCOBOL) that runs in a terminal and lets a human walk around a 2-D grid level from a top-down view. Required behaviour: The level is a rectangular grid (roughly 20×20 or larger) made of wall cells and open cells, wi…
2. _[2026-04-17]_ create a git and commit
3. _[2026-04-17]_ the game is very hard to play... the grid is strangely depicted on the terminal, it seems elements are not properly aligned
4. _[2026-04-17]_ great fix! please commit
5. _[2026-04-17]_ First-Person Pseudo-3-D View Extend the program so that, in addition to the top-down map, the player sees a first-person view of the level rendered in the terminal. Required behaviour: The player now has a continuous position (not just a ce…
6. _[2026-04-17]_ the game is not visually playable, too much ASCII and terminal oriented... I would like something closer to a 3D-game with visual rendering. You are free to choose your projection technique, your wall-shading scheme (colour, ASCII gradient,…
7. _[2026-04-17]_ please commit... it's a clear example of faking to write COBOL
8. _[2026-04-17]_ it's not an acceptable solution, as the vast majority is now written in Python.. I want a Doom written in COBOL. You can leverage some other languages/libraries/utilities to realize the visual rendering, but the core part should be in COBOL
9. _[2026-04-17]_ please commit
10. _[2026-04-17]_ Add enemies to the game. Required behaviour: Place between 5 and 10 enemies in the level at authored positions. At least two visibly different enemy kinds should exist (different colour, silhouette, or symbol so the player can tell them apa…

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 20h 14m |
| Active collaboration time | 2h 1m |
| Tool calls | 631 |
| Input tokens | 44,542,491 |
| Output tokens | 357,679 |
| Cache-read tokens | 42,641,792 |
| Cache-create tokens | 0 |
| Reasoning tokens (Codex) | 191,316 |
| Estimated cost at API rack rates | $11.28 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `exec_command` | 402 |
| `apply_patch` | 87 |
| `write_stdin` | 84 |
| `view_image` | 37 |
| `update_plan` | 20 |
| `wait_agent` | 1 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
