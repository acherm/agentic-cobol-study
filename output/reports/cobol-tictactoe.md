# `TTTGAME15-COBOL-CLAUDE` — Case Study (repository folder `cobol-tictactoe`)

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/cobol-tictactoe/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-tictactoe` assessment](../assessments/cobol-tictactoe.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-tictactoe/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/cobol-tictactoe/KEY_FEATURES.md)
  
> 🔁 **Replay prompts** (step-wise, HOW-agnostic, for reproducing with a different agent): [`REPLAY_PROMPTS.md`](../backlogs/cobol-tictactoe/REPLAY_PROMPTS.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-tictactoe`  
**Sessions.** 2 (2 Claude Code + 0 Codex)  
**Activity window.** 2026-03-12 → 2026-04-16 (6 days)  
**Agents & models.** Claude Code/claude-opus-4-6

---

## RQ1 — Domain, intent, novelty

**What it is.** Game-of-15 / tic-tac-toe variants with minimax tree search in COBOL.

**Why it's interesting.** Numeric game-of-15 is isomorphic to tic-tac-toe; programme multiple size variants + full search tree.

**From the project's `README.md` (first sections):**

> **# Game of 15 in COBOL**  
> Five COBOL programs exploring the **Game of 15**, a combinatorial number-picking game isomorphic to Tic-Tac-Toe via the 3x3 magic square.

> **## The Game of 15**  
> Two players alternate picking a number from {1, 2, ..., 9}. A number may not be repeated. The first player to hold three numbers summing to **15** wins. If all nine numbers are used with no winner, the game is a draw. The 8 winning triples (subsets of {1..9} summing to 15) correspond exactly to the rows, columns, and diagonals of the magic square: ``` 2 7 6 9 5 1 4 3 8 ``` This makes the Game of 15 strategically equivalent to Tic-Tac-Toe.

**Opening prompt that kicked off the project:**

```
The game of 15 is defined as follows: Two players in turn say a number between one and nine. A particular number may not be repeated. The game is won by the player who has said three numbers whose sum is 15. If all the numbers are used and no one gets three numbers that add up to 15 then the game is a draw. Write a COBOL program (using GNUCobol) that computes the number of possible games in the game of 15...
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- game state encoding
- minimax recursion via PERFORM
- alpha-beta (later)
- multi-variant (N boards)
- interactive I/O

_No explicit error signatures were detected in tool outputs — either the project compiled cleanly or error text was in a format the detector missed._

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **31** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 70 |
| Git commit subjects | 5 |

**Backlog (31 F-### entries).** Grouped by phase:

- **Step 1: Game Counter (`game15.cob` v1)** — 5 features  
  **Iterative DFS with backtracking** (non-recursive, stack-free). Uses …; **Ownership model**. OWNER-TABLE array (9 entries, values 0/1/2) track…; **Player alternation via depth parity**. `DIVIDE DEPTH BY 2 GIVING QUO…; **Win detection via hardcoded triples**. All 8 winning triples encoded…; **Formatted result display**. Leading-zero suppression via `PIC Z(7)9`…
- **Step 2: Symmetry Deduplication (`game15.cob` v2)** — 4 features  
  **Command-line flag parsing**. `ACCEPT CMD-ARG FROM COMMAND-LINE`; com…; **D4 symmetry table (magic square permutations)**. 8 rows of 9 digits …; **Canonical form checking**. For each completed game, compares the mov…; **Dual counter system**. Separate U-P1-WINS, U-P2-WINS, U-DRAWS counte…
- **Step 3: Optimal Play Tree (`game15tree.cob`)** — 7 features  
  **Two-pass program architecture**. Pass 1 computes minimax values for …; **Iterative minimax algorithm**. P1 (odd depth) maximizes, P2 (even de…; **Position memoization via base-3 hashing**. Each board state maps to …; **Optimal move filtering (COLLECT-OPTIMAL)**. At each node, tries all …; **ASCII tree rendering with proper connectors**. `\; **Depth-limited display**. `--depth N` flag parsed via UNSTRING into t…; **Node value annotations**. Each node labeled `[Draw]`, `[P1 wins]`, o…
- **Step 4: Avoid Annotations (`game15tree.cob` enhancement)** — 2 features  
  **Move classification (optimal vs. bad)**. COLLECT-OPTIMAL extended to…; **Avoid line rendering**. PRINT-AVOID paragraph builds `avoid: 1, 3, 7…
- **Step 5: Bug Fixes (during Steps 3 and 4)** — 2 features  
  **DISP-DIGIT intermediary for safe numeric display**. CUR-NUM (PIC 99,…; **CHOSEN(DEPTH)-based undo instead of CUR-NUM**. COLLECT-OPTIMAL's inn…
- **Step 6: Game of 0.15 Adaptation (`game015.cob`, `game015tree.cob`)** — 2 features  
  **Display-layer adaptation without logic change**. Internal representa…; **Wider tree indentation for longer labels**. Tree connectors use 5-ch…
- **Step 7: Variant Generator (`gameN.cob`)** — 9 features  
  **Two-argument CLI with UNSTRING parsing**. First argument = target su…; **Dynamic winning triple generation**. Nested loops over all pairs (a,…; **Parameterized DFS engine**. OWNER-TABLE, NEXT-TRY-TABLE, and MOVE-TA…; **Auto-derivation of max-number**. When second argument is omitted, co…; **Input validation with error messages**. Three checks: max-number > 1…; **Usage message**. Displayed when no arguments given. Shows syntax, pa…; **Rules display with game character commentary**. After listing winnin…; **Classic Game of 15 detection**. When TARGET-SUM=15 and MAX-NUM=9, pr… _(+1 more)_

**Prompt-extracted sub-requests (70)** — first 8 (sub-bullets inside user messages):

- _[2026-03-19]_ PASS 1 (Extraction): reconstruct an ex-post backlog and replay package for reproducibility.
- _[2026-03-19]_ PASS 2 (Interpretation): characterize coding strategies + outcomes/quality, including interaction-demand analysis and (if present) COBOL capability indicators.
- _[2026-03-19]_ I will NOT provide transcripts proactively.
- _[2026-03-19]_ You must analyze the repo as-is (git history may be minimal or absent).
- _[2026-03-19]_ Claude session histories are typically available under: ~/.claude/
- _[2026-03-19]_ Your analysis must be evidence-based and reproducible.
- _[2026-03-19]_ Do NOT invent features, decisions, commands, or outcomes.
- _[2026-03-19]_ Every claim must have evidence pointers from: repo files, git commits (if any), ~/.claude session logs, and any commands/logs you executed.

**Git commits (5)** — first 8:

- `e4968ec570` 2026-04-09  Add algorithm-agnostic replay prompts for step-by-step reproduction
- `4ae3129ad1` 2026-03-19  removal history
- `e37dfc24cb` 2026-03-19  backlog feature
- `e351c4bc5c` 2026-03-19  analysis
- `dc71e86cc0` 2026-03-19  Add Game of 15 COBOL programs: counter, optimal play tree, and variant generator

## RQ3 — What was delivered

**Executables present in the root of the project** (evidence that something builds):

- `game015` (53 KB)
- `game015tree` (86 KB)
- `game15` (52 KB)
- `game15tree` (86 KB)
- `gameN` (71 KB)

## RQ4 — Size and complexity

**File inventory** (15 files, 0.5 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 5 | 1,919 |
| Markdown | 3 | 430 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 5 |
| Total lines | 1,919 |
| Code lines (non-blank, non-comment) | 1,537 |
| Comment lines | 382 |
| Sections | 5 |
| Paragraphs | 34 |
| Data items (level-number declarations) | 254 |
| Max IF/EVALUATE nesting (any file) | 6 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 314 |
| `IF` | 150 |
| `ADD` | 107 |
| `DISPLAY` | 86 |
| `PERFORM` | 83 |
| `DIVIDE` | 13 |
| `COMPUTE` | 9 |
| `STOP` | 9 |
| `SUBTRACT` | 9 |
| `ACCEPT` | 5 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `game015tree.cob` | 436 |
| `game15tree.cob` | 434 |
| `gameN.cob` | 289 |
| `game15.cob` | 189 |
| `game015.cob` | 189 |

**Git churn signal.** 5 commits, 4896 insertions / 2542 deletions, first 2026-03-19, last 2026-04-09.

## RQ4b — COBOL language mastery

**Mastery score:** **28** distinct COBOL constructs used across **8/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 565 | `IF`×299, `PERFORM`×105, `ELSE`×90, `PERFORM_UNTIL`×29, `PERFORM_VARYING`×22, `STOP_RUN`×9, `WHEN`×7, `EVALUATE`×4 |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 156 | `ADD`×107, `COMPUTE`×25, `DIVIDE`×13, `SUBTRACT`×9, `MULTIPLY`×2 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 258 | `PIC_9`×164, `OCCURS`×38, `PIC_X`×34, `FILLER`×16, `REDEFINES`×6 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | — | 0 |  |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 17 | `REFERENCE_MOD`×8, `UNSTRING`×6, `DELIMITED_BY`×3 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 9 | `INITIALIZE`×9 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 18 | `GIVING`×18 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | — | 0 |  |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 40 | `FUNCTION`×20, `FUNCTION_TRIM`×16, `FUNCTION_NUMVAL`×4 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 137 | `DISPLAY`×132, `ACCEPT`×5 |

**Notable non-trivial constructs used:** `OCCURS` (38×), `REDEFINES` (6×), `UNSTRING` (6×), `FUNCTION` (20×).

**Procedural structure.** 34 paragraphs, 5 sections across 5 COBOL file(s). That means roughly **34 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **2h 4m** across 206 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 1h 27m | 70.6% |
| `build` | compile / makefile / dependency work | 14m 48s | 11.9% |
| `unknown` | could not classify confidently | 12m 53s | 10.4% |
| `feature` | adding new functionality | 5m 51s | 4.7% |
| `performance` | making it faster | 2m 15s | 1.8% |
| `plan` | task tracking, planning | 0m 25s | 0.3% |
| `test` | writing or running tests / benchmarks | 0m 16s | 0.2% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `test` | 24 |
| `build` | 15 |
| `feature` | 14 |
| `understanding` | 8 |
| `plan` | 5 |
| `bug_fix` | 1 |

## RQ6 — Failures encountered

Out of **67 tool results**, **1** (1.5%) contained an error signature.

## RQ6b — Difficulty assessment

**Auto-label: `Medium`** (difficulty index 0.29; mean rank across 7 signals = 5.3).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 2.1 | 10.0 |
| Calendar span (days first→last event) | 6 | 10.0 |
| User prompts | 12 | 6.0 |
| Redirect / bug-report prompts | 1 | 5.0 |
| Tool-output error rate | 0.015 | 3.0 |
| Fix cycles (error → immediate retry) | 0 | 1.5 |
| Share of active time spent on `bug_fix` | 0.000 | 1.5 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 12
- **Average prompt length:** 953 chars; **max:** 9,729 chars
- **Total chars written by user:** 11,434
- **Sessions:** 2; **span:** 6 days
- **Long-prompt ratio** (≥500 chars): 1/12

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2026-03-12 19:46 | 6d 19h 51m | 14 | 67 | $52.79 |
| 2 | Claude Code | `claude-opus-4-6` | 2026-03-19 10:11 | 27d 23h 36m | 21 | 75 | $35.00 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| other | 6 |
| clarify | 4 |
| initial-spec | 1 |
| redirect | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-03-12]_ The game of 15 is defined as follows: Two players in turn say a number between one and nine. A particular number may not be repeated. The game is won by the player who has said three numbers whose sum is 15. If all the numbers are used and …
2. _[2026-03-12]_ add a flag to compute numbers without duplicates
3. _[2026-03-12]_ I am interested to depict a tree (in ASCII format) of all possible moves and the outcome (under optimal play)... Such a tree would help to know what to play after a certain sequence of "moves" (numbers' choices in the game 15)
4. _[2026-03-12]_ nice! to "simplify" a bit, I suggest that given a sequence of moves/choices, there are (1) follow-up choice to NOT perform (otherwise you lose); (2) follow-up choice you can make (among many possibly)
5. _[2026-03-13]_ The game of 0.15 is defined as follows: Two players in turn say a number among 0.01, 0.02,..., 0.09. A particular number may not be repeated. The game is won by the player who has said three numbers whose sum is 0.15. If all the numbers are…
6. _[2026-03-13]_ Provide a generator that "invents" a variant of the game of N=15 by changing N (eg 0.15) and thus the possible numbers users can choose. Please recap the rules of the game of N after
7. _[2026-03-13]_ This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation. Summary: 1. Primary Request and Intent: The user requested a series of COBOL programs (G…
8. _[2026-03-13]_ continue
9. _[2026-03-13]_ continue
10. _[2026-03-19]_ create a git and commit

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 6d 19h 51m |
| Active collaboration time | 2h 4m |
| Tool calls | 67 |
| Input tokens | 188 |
| Output tokens | 318,409 |
| Cache-read tokens | 7,877,782 |
| Cache-create tokens | 911,207 |
| Reasoning tokens (Codex) | 0 |
| Estimated cost at API rack rates | $52.79 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `Bash` | 46 |
| `Edit` | 8 |
| `Write` | 6 |
| `Read` | 5 |
| `Agent` | 1 |
| `Grep` | 1 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
