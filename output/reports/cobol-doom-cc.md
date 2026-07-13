# `cobol-doom-cc` — Case Study

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/cobol-doom-cc/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-doom-cc` assessment](../assessments/cobol-doom-cc.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-doom-cc/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/cobol-doom-cc/KEY_FEATURES.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-doom-cc`  
**Sessions.** 1 (1 Claude Code + 0 Codex)  
**Activity window.** 2026-04-17 → 2026-04-18 (0 days)  
**Agents & models.** Claude Code/claude-opus-4-7

---

## RQ1 — Domain, intent, novelty

**What it is.** Doom-like FPS in COBOL (Claude Code) — walker + ray-casting + enemies + levels via copybook modules.

**Why it's interesting.** Second-generation clean Doom build with Claude Code; modular via 7 COPY books (render/world/entities/levels/screens).

**Opening prompt that kicked off the project:**

```
Write a COBOL program (GnuCOBOL) that runs in a terminal and lets a human walk around a 2-D grid level from a top-down view. Required behaviour: The level is a rectangular grid (roughly 20×20 or larger) made of wall cells and open cells, with a clearly visible layout of rooms and corridors. The view is a top-down ASCII map: walls, open floor, and the player drawn at the player's current cell with a symbol that indicates facing direction. The player can move with keys W/A/S/D (or the arrow keys) and quit with Q or ESC. Input must be read without requiring the user to press Enter after each key. The player cannot walk through walls. Attempts to do so leave the player in place. The screen is redrawn after every input so the view stays current. Redrawing must not scroll — the map stays anchore…
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- ray casting via integer trig
- raw-mode terminal input
- COBOL ↔ C ABI for per-frame traffic
- enemies / pickups / multi-level progression
- modular COPY-book architecture

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| C compiler error | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **13** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 0 |
| Git commit subjects | 15 |

**Backlog (13 F-### entries).** Grouped by phase:

- **_unclassified_** — 13 features  
  Top-down 2D grid walker (commit 75c27ad); Fix invisible output (commit c0b9bc7); DDA raycaster with minimap (commit 8a47a28); Unicode half-block + truecolor rendering; Arrow key support (commit 9d2d9c4); Enemies and combat (commit 5ed8682); Pickups, HUD, weapons; POSIX read() for input (commit f0418eb) _(+5 more)_

**Git commits (15)** — first 8:

- `e9854b2b2c` 2026-04-18  Refactor walker.cob into cohesive COBOL copybooks
- `69ab81f858` 2026-04-18  Replace crosshair with weapon HUD; give enemies a silhouette + eyes
- `3398a33cd2` 2026-04-18  Polish graphics: wall texture, floor checkerboard, crosshair, HUD panel
- `3c8416aeeb` 2026-04-18  Add scripted demo play-through + Makefile
- `93b93fab46` 2026-04-18  Add startup level-select menu
- `64181fe664` 2026-04-18  Add reusable level format and three playable levels
- `f0418eb135` 2026-04-18  Bypass ncurses: read stdin directly via POSIX read(2)
- `b2ea5fb085` 2026-04-18  Add HUD strip, ammo, pickups, weapon switching

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `walker` (149 KB)

## RQ4 — Size and complexity

**File inventory** (12 files, 0.2 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 8 | 1,869 |
| Shell | 1 | 118 |
| Makefile | 1 | 21 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 8 |
| Total lines | 1,869 |
| Code lines (non-blank, non-comment) | 1,616 |
| Comment lines | 253 |
| Sections | 1 |
| Paragraphs | 71 |
| Data items (level-number declarations) | 339 |
| Max IF/EVALUATE nesting (any file) | 5 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 404 |
| `COMPUTE` | 174 |
| `IF` | 115 |
| `PERFORM` | 91 |
| `DISPLAY` | 19 |
| `CALL` | 15 |
| `WRITE` | 12 |
| `EVALUATE` | 10 |
| `ADD` | 9 |
| `EXIT` | 7 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `cpy/pd-render.cpy` | 717 |
| `cpy/pd-level.cpy` | 205 |
| `cpy/pd-world.cpy` | 197 |
| `cpy/ws-entities.cpy` | 170 |
| `cpy/ws-levels.cpy` | 126 |

**Git churn signal.** 15 commits, 4463 insertions / 2450 deletions, first 2026-04-17, last 2026-04-18.

## RQ4b — COBOL language mastery

**Mastery score:** **34** distinct COBOL constructs used across **9/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 486 | `IF`×230, `PERFORM`×115, `WHEN`×38, `ELSE`×28, `PERFORM_UNTIL`×21, `PERFORM_VARYING`×21, `EVALUATE`×20, `EXIT`×11 _(+2 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 191 | `COMPUTE`×177, `ADD`×9, `SUBTRACT`×5 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 377 | `PIC_X`×131, `FILLER`×101, `USAGE_BINARY`×99, `PIC_9`×26, `USAGE_COMP_5`×12, `OCCURS`×7, `REDEFINES`×1 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 94 | `START`×61, `READ`×14, `WRITE`×12, `SELECT`×7 |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 3 | `REFERENCE_MOD`×3 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | — | 0 |  |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 69 | `BY_VALUE`×26, `CALL`×15, `USING`×15, `BY_REFERENCE`×13 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 7 | `COPY`×7 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 44 | `FUNCTION`×43, `FUNCTION_UPPER`×1 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 21 | `DISPLAY`×19, `ACCEPT`×2 |

**Notable non-trivial constructs used:** `CALL` (15×), `OCCURS` (7×), `REDEFINES` (1×), `USAGE_COMP_5` (12×), `COPY` (7×), `FUNCTION` (43×).

**Procedural structure.** 71 paragraphs, 1 sections across 8 COBOL file(s). That means roughly **71 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **3h 14m** across 506 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 1h 44m | 53.9% |
| `build` | compile / makefile / dependency work | 36m 22s | 18.7% |
| `feature` | adding new functionality | 23m 3s | 11.9% |
| `unknown` | could not classify confidently | 21m 6s | 10.9% |
| `test` | writing or running tests / benchmarks | 2m 18s | 1.2% |
| `plan` | task tracking, planning | 2m 5s | 1.1% |
| `port` | translating across languages | 1m 44s | 0.9% |
| `spec` | specifications / architecture writing | 1m 34s | 0.8% |
| `bug_fix` | correcting an observed defect | 1m 23s | 0.7% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `feature` | 63 |
| `understanding` | 38 |
| `build` | 34 |
| `plan` | 16 |
| `bug_fix` | 1 |

## RQ6 — Failures encountered

Out of **152 tool results**, **1** (0.7%) contained an error signature.

## RQ6b — Difficulty assessment

**Auto-label: `Medium`** (difficulty index 0.41; mean rank across 7 signals = 7.1).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 3.2 | 12.0 |
| Calendar span (days first→last event) | 0 | 3.5 |
| User prompts | 20 | 10.0 |
| Redirect / bug-report prompts | 4 | 9.5 |
| Tool-output error rate | 0.007 | 2.0 |
| Fix cycles (error → immediate retry) | 1 | 4.5 |
| Share of active time spent on `bug_fix` | 0.007 | 8.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 20
- **Average prompt length:** 479 chars; **max:** 2,145 chars
- **Total chars written by user:** 9,588
- **Sessions:** 1; **span:** 0 days
- **Long-prompt ratio** (≥500 chars): 6/20

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Claude Code | `claude-opus-4-7` | 2026-04-17 16:35 | 20h 12m | 20 | 152 | $367.10 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| other | 12 |
| redirect | 4 |
| clarify | 3 |
| initial-spec | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-04-17]_ Write a COBOL program (GnuCOBOL) that runs in a terminal and lets a human walk around a 2-D grid level from a top-down view. Required behaviour: The level is a rectangular grid (roughly 20×20 or larger) made of wall cells and open cells, wi…
2. _[2026-04-17]_ create a git and commit
3. _[2026-04-17]_ the game is very hard to play since the grid is not visible in the first place, keyboards and moves have no apparent effect (since the grid is not showing up)... only when pressing Q the grid appears, but it's quiting the game
4. _[2026-04-17]_ still the same issue... there is nothing appearing at the start. Using W A S D has no effect. Only Q
5. _[2026-04-17]_ the game is very hard to play... the grid is strangely depicted on the terminal, it seems elements are not properly aligned
6. _[2026-04-17]_ please commit
7. _[2026-04-17]_ First-Person Pseudo-3-D View Extend the program from Step 1 so that, in addition to the top-down map, the player sees a first-person view of the level rendered in the terminal. Required behaviour: The player now has a continuous position (n…
8. _[2026-04-17]_ the game is not visually playable, too much ASCII and terminal oriented... I would like something closer to a 3D-game with visual rendering. You are free to choose your projection technique, your wall-shading scheme (colour, ASCII gradient,…
9. _[2026-04-17]_ two workarounds: at the starting execution, nothing is depicted, I need to press Enter... I have difficulties to move forward and progress in general. in general the game is OKish but could be improved graphically. I also would like to use …
10. _[2026-04-17]_ display has changed but still the same issues at startup time, Enter needed. Arrow keys not working

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 20h 12m |
| Active collaboration time | 3h 14m |
| Tool calls | 152 |
| Input tokens | 628 |
| Output tokens | 1,684,363 |
| Cache-read tokens | 130,194,776 |
| Cache-create tokens | 2,425,304 |
| Reasoning tokens (Codex) | 0 |
| Estimated cost at API rack rates | $367.10 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `Bash` | 79 |
| `Edit` | 53 |
| `Write` | 11 |
| `Read` | 9 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
