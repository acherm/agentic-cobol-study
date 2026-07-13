# `TTTGAME15-COBOL-CODEX` — Case Study (repository folder `game15-cobol-codex`)

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/game15-cobol-codex/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`game15-cobol-codex` assessment](../assessments/game15-cobol-codex.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/game15-cobol-codex/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/game15-cobol-codex/KEY_FEATURES.md)

**Project root.** `/Users/mathieuacher/SANDBOX/game15-cobol-codex`  
**Sessions.** 1 (0 Claude Code + 1 Codex)  
**Activity window.** 2026-04-16 → 2026-04-16 (0 days)  
**Agents & models.** Codex/gpt-5.4

---

## RQ1 — Domain, intent, novelty

**What it is.** Game of 15 / tic-tac-toe in COBOL (Codex-built) — the Codex replica of the small-game domain, paired with the Claude-Code-built `cobol-tictactoe`.

**Why it's interesting.** Cross-agent replication: same game-of-15 / minimax tree contract, different agent. Specifically exercises the `REPLAY_PROMPTS.md` produced for `cobol-tictactoe`.

**Opening prompt that kicked off the project:**

```
Write a COBOL program (GnuCOBOL) for the "Game of 15". Rules: Two players alternate picking a number from {1, 2, ..., 9}. A number cannot be picked twice. A player wins when any three of their chosen numbers sum to exactly 15. If all nine numbers are picked and no player has won, the game is a draw. The program should enumerate every possible game (every legal sequence of moves to completion) and report: Player 1 wins (player who picks first) Player 2 wins Draws Total games
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- game counting via enumeration
- symmetry deduplication via magic square
- optimal-play tree with avoid annotations
- parameterized gameN variant
- multi-variant interactive I/O

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| command exited with non-zero status | 6 |
| C compiler error | 2 |
| GnuCOBOL compiler error (incl. syntax) | 1 |
| missing file | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **35** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 0 |
| Git commit subjects | 4 |

**Backlog (35 F-### entries).** Grouped by phase:

- **Step 1 — Game counter `game15.cob` (commit `29cbcaa`)** — 6 features  
  **Iterative DFS with explicit stack**. Single `PERFORM UNTIL DONE=1` d…; **Ownership model + move history + per-depth next-candidate**. `OWNER(…; **Pre-tabulated player schedule**. `PLAYER-AT-DEPTH(1..9)` explicitly …; **Hard-coded tic-tac-toe lines, not magic triples**. Win check is 8 tr…; **Stop-on-win termination rule**. Once `HAS-WON = 1` the branch is rec…; **Formatted reporting with `PIC Z,ZZZ,ZZZ,ZZZ,ZZZ,ZZ9`**. Group-separa…
- **Step 2a — Symmetry deduplication (same commit `c41b9b5`, first sub-step)** — 5 features  
  **CLI flag parsing via INSPECT TALLYING**. Reads `COMMAND-LINE-TEXT`, …; **D4 symmetry table as number permutations (8 x 9)**. Eight rows of `S…; **Canonical sequence via min-over-orbit**. Keeps a `BEST-MOVE(9)` arra…; **Factorial-rank canonical hash → 986,409-entry bitmap**. Each canonic…; **Dual counter system**. Four additional `UNIQUE-*` counters increment…
- **Step 2b — Optimal play tree `game15_tree.cob` (same commit `c41b9b5`, second sub-step)** — 10 features  
  **Base-3 state encoding over all 19,683 boards**. Each of the 3^9 `OWN…; **Bottom-up retrograde analysis**. Outer loop `FILLED-TARGET` from 9 d…; **State validity filter**. A board is valid iff piece counts are consi…; **Minimax folded into retrograde solve**. `STORE-STATE-OUTCOME` resolv…; **Per-level node stack for iterative tree printing**. Fixed-size (dept…; **Optimal-child filter tied to parent value**. Only children whose `ST…; **ASCII connectors assembled into `PIC X(120)` line buffer**. `\; **`--depth N` option with numeric argument validation**. `UNSTRING … D… _(+2 more)_
- **Step 2c — Avoid annotations (same commit `c41b9b5`, third sub-step)** — 3 features  
  **Move classification into safe vs bad buckets**. Same pass as SB-17: …; **`avoid:` line rendered at child-level prefix**. `DISPLAY-AVOID-LINE`…; Bug fix: **avoid-line indentation reused a stale prefix depth**. Rende…
- **Step 3 — Game of 0.15 variants (commit `f9c2eb1`)** — 4 features  
  **File duplication then display-only diff** (`cp game15.cob game015.co…; **`MOVE-LABEL(9)` lookup for decimal rendering in the tree variant**. …; **Target-sum banner text `"Target sum: 0.15"`** in both variants. Sing…; **Internal integers preserved**. Owner / symmetry / state-id / minimax…
- **Step 4 — Generalised Game of N `gameN.cob` (commit `ce67d51`)** — 7 features  
  **Two-argument CLI with strict numeric validation**. `UNSTRING … INTO …; **Runtime winning-triple generation**. Nested `a < b < c, a + b + c = …; **Parameterised DFS over `MAX-NUMBER` and `STORED-TRIPLE-COUNT`**. Eng…; **Auto-default `max-number = target-sum - 3`** (clamped to `[3, 999]`)…; **Enumeration guard `MAX-NUMBER <= 9`**. When larger, triples are stil…; **Number-pool line-wrapping display**. `DISPLAY-NUMBER-POOL` wraps the…; **Usage message + explicit default / cap explanation**. `DISPLAY-USAGE…

**Git commits (4)** — first 8:

- `ce67d51325` 2026-04-16  Add generalized Game of N program
- `f9c2eb18f0` 2026-04-16  Add Game of 0.15 programs
- `c41b9b5e54` 2026-04-16  Add unique counts and optimal play tree
- `29cbcaa73a` 2026-04-16  Add Game of 15 enumerator

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `game15` (69 KB)
- `game15_tree` (86 KB)

## RQ4 — Size and complexity

**File inventory** (8 files, 0.2 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 5 | 2,822 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 5 |
| Total lines | 2,822 |
| Code lines (non-blank, non-comment) | 2,264 |
| Comment lines | 211 |
| Sections | 5 |
| Paragraphs | 88 |
| Data items (level-number declarations) | 259 |
| Max IF/EVALUATE nesting (any file) | 38 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 585 |
| `IF` | 193 |
| `PERFORM` | 170 |
| `DISPLAY` | 56 |
| `ADD` | 48 |
| `COMPUTE` | 33 |
| `EXIT` | 32 |
| `STRING` | 30 |
| `EVALUATE` | 11 |
| `SUBTRACT` | 7 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `game015tree.cob` | 551 |
| `game15_tree.cob` | 538 |
| `game015.cob` | 402 |
| `game15.cob` | 401 |
| `gameN.cob` | 372 |

**Git churn signal.** 4 commits, 2834 insertions / 10 deletions, first 2026-04-16, last 2026-04-16.

## RQ4b — COBOL language mastery

**Mastery score:** **35** distinct COBOL constructs used across **9/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 734 | `IF`×269, `PERFORM`×191, `PERFORM_UNTIL`×71, `PERFORM_VARYING`×65, `ELSE`×49, `EXIT`×32, `WHEN`×30, `EVALUATE`×21 _(+1 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 96 | `ADD`×48, `COMPUTE`×37, `SUBTRACT`×7, `DIVIDE`×4 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 299 | `PIC_9`×181, `OCCURS`×69, `USAGE_POINTER`×28, `PIC_X`×18, `PIC_S9`×3 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 2 | `START`×2 |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 90 | `DELIMITED_BY`×47, `STRING`×36, `UNSTRING`×3, `INSPECT`×2, `INSPECT_TALLYING`×2 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 91 | `SEARCH`×65, `INITIALIZE`×20, `SET`×6 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 4 | `GIVING`×4 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | — | 0 |  |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 68 | `FUNCTION`×34, `FUNCTION_TRIM`×27, `FUNCTION_NUMVAL`×3, `FUNCTION_LENGTH`×3, `FUNCTION_MOD`×1 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 121 | `DISPLAY`×116, `ACCEPT`×5 |

**Notable non-trivial constructs used:** `OCCURS` (69×), `UNSTRING` (3×), `FUNCTION` (34×).

**Procedural structure.** 88 paragraphs, 5 sections across 5 COBOL file(s). That means roughly **88 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **33m 4s** across 533 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 23m 21s | 70.6% |
| `feature` | adding new functionality | 7m 55s | 23.9% |
| `build` | compile / makefile / dependency work | 1m 38s | 4.9% |
| `plan` | task tracking, planning | 0m 7s | 0.4% |
| `test` | writing or running tests / benchmarks | 0m 2s | 0.1% |
| `bug_fix` | correcting an observed defect | 0m 1s | 0.1% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `build` | 106 |
| `plan` | 23 |
| `feature` | 17 |
| `understanding` | 12 |
| `test` | 12 |
| `bug_fix` | 3 |

## RQ6 — Failures encountered

Out of **173 tool results**, **6** (3.5%) contained an error signature.

## RQ6b — Difficulty assessment

**Auto-label: `Medium`** (difficulty index 0.26; mean rank across 7 signals = 4.9).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 0.6 | 4.0 |
| Calendar span (days first→last event) | 0 | 3.5 |
| User prompts | 11 | 5.0 |
| Redirect / bug-report prompts | 1 | 5.0 |
| Tool-output error rate | 0.035 | 9.0 |
| Fix cycles (error → immediate retry) | 1 | 4.5 |
| Share of active time spent on `bug_fix` | 0.001 | 3.5 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 11
- **Average prompt length:** 396 chars; **max:** 828 chars
- **Total chars written by user:** 4,354
- **Sessions:** 1; **span:** 0 days
- **Long-prompt ratio** (≥500 chars): 5/11

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Codex | `gpt-5.4` | 2026-04-16 09:49 | 3h 37m | 11 | 173 | $2.77 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| clarify | 5 |
| review-ask | 2 |
| other | 2 |
| initial-spec | 1 |
| redirect | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-04-16]_ Write a COBOL program (GnuCOBOL) for the "Game of 15". Rules: Two players alternate picking a number from {1, 2, ..., 9}. A number cannot be picked twice. A player wins when any three of their chosen numbers sum to exactly 15. If all nine n…
2. _[2026-04-16]_ create a git and commit
3. _[2026-04-16]_ Add a --unique command-line flag to the game counter. The Game of 15 is isomorphic to Tic-Tac-Toe. The numbers 1-9 can be arranged in a 3x3 magic square where rows, columns, and diagonals each sum to 15: 2 7 6 9 5 1 4 3 8 This means the Gam…
4. _[2026-04-16]_ commit
5. _[2026-04-16]_ Write a new COBOL program that displays the Game of 15 optimal play tree as ASCII art. "Optimal play" means both players play to maximize their own outcome: Player 1 tries to win (or at least draw), Player 2 tries to win (or at least draw).…
6. _[2026-04-16]_ Enhance the optimal play tree: at each decision point, before listing the optimal (safe) moves, show which available moves would be mistakes. For each position, classify every available move as either: Safe/optimal: playing it does not wors…
7. _[2026-04-16]_ commit
8. _[2026-04-16]_ The "Game of 0.15" is defined as follows: two players alternate picking a number among {0.01, 0.02, ..., 0.09}. A number cannot be repeated. A player wins when three of their numbers sum to 0.15. If all numbers are used with no winner, the …
9. _[2026-04-16]_ commit
10. _[2026-04-16]_ Write a COBOL program that generalizes the game to any target sum and number range. Usage: ./gameN <target-sum> [<max-number>] The "Game of N" is played with numbers {1, 2, ..., max-number}. Two players alternate picking; a player wins when…

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 3h 37m |
| Active collaboration time | 33m 4s |
| Tool calls | 173 |
| Input tokens | 465,028 |
| Output tokens | 113,459 |
| Cache-read tokens | 8,434,688 |
| Cache-create tokens | 0 |
| Reasoning tokens (Codex) | 68,774 |
| Estimated cost at API rack rates | $2.77 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `exec_command` | 145 |
| `apply_patch` | 18 |
| `write_stdin` | 9 |
| `wait_agent` | 1 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
