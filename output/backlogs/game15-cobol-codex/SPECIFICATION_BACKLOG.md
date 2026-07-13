# Specification Backlog (Agent-Implemented Features) — game15-cobol-codex

This backlog documents what the **Codex** agent actually built, step by step, at the level of individual technical capabilities. It complements the [README feature backlog](README.md#feature-backlog-bl), which is organized by user requests. Here the perspective is: what decisions did the agent make, what sub-features were introduced (including ones not explicitly requested), and in what order.

Features are numbered SB-01 … SB-30 in implementation order. Each notes whether it was **user-driven** (matches a `UI-###` / `PL-###` request), **agent-initiated**, or a **required prerequisite**. Step segmentation follows the 4 git commits on branch `codex/game15` [G] augmented by within-commit session episodes [T].

> **Agent:** Codex CLI v0.119.0-alpha.11, model `gpt-5.4`, single session `019d95b1-8660-75c2-8a6b-44dfbafc0a19` (2026-04-16 09:49 → 13:26 UTC).
> **Project:** `/Users/mathieuacher/SANDBOX/game15-cobol-codex` (read-only for this analysis).
> **Replay pack:** driven by `output/backlogs/cobol-tictactoe/REPLAY_PROMPTS.md` (human prompts match that file verbatim — see `PL-01`..`PL-06`).

## Step segmentation method

Four commits on `codex/game15` bracket the user prompts one-for-one:

| Step | Commit | Message | Triggering prompt |
|---|---|---|---|
| 1 | `29cbcaa` | Add Game of 15 enumerator | PL-01 (Game Counter) |
| 2 | `c41b9b5` | Add unique counts and optimal play tree | PL-02 (--unique) + PL-03 (tree) + PL-04 (avoid) — combined in one commit |
| 3 | `f9c2eb1` | Add Game of 0.15 programs | PL-05 (0.15 variants) |
| 4 | `ce67d51` | Add generalized Game of N program | PL-06 (gameN) |

Within-step ordering is recovered from session events `[T:session 019d95b1:event_###]`.

---

## Step 1 — Game counter `game15.cob` (commit `29cbcaa`)

User request (PL-01): *"Write a COBOL program (GnuCOBOL) for the Game of 15 […] enumerate every possible game […] report P1 wins, P2 wins, draws, total games."*

| ID | Feature | Origin | Code / evidence |
|----|---------|--------|-----------------|
| SB-01 | **Iterative DFS with explicit stack**. Single `PERFORM UNTIL DONE=1` driven by `SEARCH-DEPTH` counter + `NEXT-CANDIDATE(depth)` array. Chosen explicitly "to avoid relying on compiler-specific recursion behavior" `[T:event_022]`. | Agent-initiated (architecture) | `[R:game15.cob:82-98]` main loop; `[R:game15.cob:272-280]` FIND-NEXT-CANDIDATE; `[R:game15.cob:282-305]` APPLY-MOVE; `[R:game15.cob:409-417]` BACKTRACK |
| SB-02 | **Ownership model + move history + per-depth next-candidate**. `OWNER(9)` holds 0/1/2, `MOVE-NUMBER(9)` records chosen moves, `NEXT-CANDIDATE(9)` holds the next value to try per depth. | Agent-initiated (data layout) | `[R:game15.cob:7-15]` SEARCH-TABLES group |
| SB-03 | **Pre-tabulated player schedule**. `PLAYER-AT-DEPTH(1..9)` explicitly set to `1,2,1,2,1,2,1,2,1` rather than derived modulo. | Agent-initiated | `[R:game15.cob:143-151]` |
| SB-04 | **Hard-coded tic-tac-toe lines, not magic triples**. Win check is 8 triples but expressed as direct cell triples `{1,5,9},{1,6,8},{2,4,9},{2,5,8},{2,6,7},{3,4,8},{3,5,7},{4,5,6}`, one `IF` per triple. (These are the 8 tic-tac-toe lines *after* the magic-square mapping is applied, so equivalent to the magic-triple set.) | Agent-initiated | `[R:game15.cob:419-475]` CHECK-WIN |
| SB-05 | **Stop-on-win termination rule**. Once `HAS-WON = 1` the branch is recorded and the chosen number is un-owned, rather than completing the remaining picks. Makes the reported total 255,168. | Agent-initiated (semantics) | `[R:game15.cob:289-305]` |
| SB-06 | **Formatted reporting with `PIC Z,ZZZ,ZZZ,ZZZ,ZZZ,ZZ9`**. Group-separated numeric edit for the three win/draw/total lines. | Agent-initiated (format) | `[R:game15.cob:72-80, 477-486]` |
| V-01 | Validation: `./game15` prints `Player 1 wins: 131,184 / Player 2 wins: 77,904 / Draws: 46,080 / Total games: 255,168` — matches expected oracle. | | `[T:event_036]` |

---

## Step 2a — Symmetry deduplication (same commit `c41b9b5`, first sub-step)

User request (PL-02): *"Add a --unique command-line flag […] numbers 1-9 arrange in a 3x3 magic square […] remove symmetric duplicates. Keep reporting the original totals as well."*

| ID | Feature | Origin | Code / evidence |
|----|---------|--------|-----------------|
| SB-07 | **CLI flag parsing via INSPECT TALLYING**. Reads `COMMAND-LINE-TEXT`, wraps with sentinel spaces, counts occurrences of literal `" --unique "` to set `UNIQUE-MODE`. | Agent-initiated (mechanism) | `[R:game15.cob:256-270]` PARSE-OPTIONS |
| SB-08 | **D4 symmetry table as number permutations (8 x 9)**. Eight rows of `SYMMETRY-VALUE(sym, n)` mapping number `n` under each square symmetry, stored via individual `MOVE` statements (no REDEFINES / no string literal). | Agent-initiated | `[R:game15.cob:61-64, 175-254]` INITIALIZE-SYMMETRY-TABLES |
| SB-09 | **Canonical sequence via min-over-orbit**. Keeps a `BEST-MOVE(9)` array; iterates 7 non-identity symmetries, remaps the move list into `TEST-MOVE`, compares lexicographically, swaps in `TEST-MOVE` whenever it is smaller. | Agent-initiated | `[R:game15.cob:323-379]` BUILD-CANONICAL-SEQUENCE + COMPARE-CANONICAL-SEQUENCES |
| SB-10 | **Factorial-rank canonical hash → 986,409-entry bitmap**. Each canonical sequence of length `L` is ranked to an integer in `[0, 9!)` using falling-factorial weights and `LENGTH-OFFSET(L)` start-indices. A `SEEN-CANONICAL PIC X OCCURS 986409` array marks already-counted equivalence classes (`"Y"` or SPACE). | Agent-initiated (approach) | `[R:game15.cob:55-59]` ranking tables; `[R:game15.cob:69-70]` `SEEN-CANONICAL`; `[R:game15.cob:381-407]` COMPUTE-SEQUENCE-RANK |
| SB-11 | **Dual counter system**. Four additional `UNIQUE-*` counters incremented only when the canonical sequence is seen for the first time. Always computed; the unique section of the report is gated by `UNIQUE-MODE`. | Agent-initiated | `[R:game15.cob:26-30, 323-341, 488-498]` |
| V-02 | Validation: `./game15 --unique` prints Unique P1 16,398 / P2 9,738 / Draws 5,760 / Total 31,896 — matches oracle in `REPLAY_PROMPTS.md`. | | `[T:event_080]` |

---

## Step 2b — Optimal play tree `game15_tree.cob` (same commit `c41b9b5`, second sub-step)

User request (PL-03): *"Write a new COBOL program that displays the Game of 15 optimal play tree as ASCII art […] support `--depth N` flag."*

| ID | Feature | Origin | Code / evidence |
|----|---------|--------|-----------------|
| SB-12 | **Base-3 state encoding over all 19,683 boards**. Each of the 3^9 `OWNER`-triplets is mapped to a unique integer `STATE-ID ∈ [1, 19683]` using `POWER3(1..9) = 1,3,9,…,6561`. `STATE-VALID(19683)` and `STATE-OUTCOME(19683)` are full tables, not a transposition cache. | Agent-initiated (architecture) | `[R:game15_tree.cob:10-15, 116-124, 245-265, 543-547]` |
| SB-13 | **Bottom-up retrograde analysis**. Outer loop `FILLED-TARGET` from 9 down to 0; for each state at that fill level decides validity + outcome by looking up child states (already solved at depth `filled+1`). Guarantees children are ready before the parent. | Agent-initiated | `[R:game15_tree.cob:227-243]` BUILD-OUTCOME-TABLE |
| SB-14 | **State validity filter**. A board is valid iff piece counts are consistent (`p1 ∈ {p2, p2+1}`), not both players have a winning line, and the player who allegedly just moved is the one who won if a win exists. Used to prune ~70% of the 19683 encodings. | Agent-initiated | `[R:game15_tree.cob:267-300]` EVALUATE-STATE |
| SB-15 | **Minimax folded into retrograde solve**. `STORE-STATE-OUTCOME` resolves terminal states directly, else picks best-over-children using `BEST-OUTCOME` with early exit when optimum (`1` for P1, `2` for P2) is reached. | Agent-initiated | `[R:game15_tree.cob:359-415]` |
| SB-16 | **Per-level node stack for iterative tree printing**. Fixed-size (depth 10) stack with `NODE-MOVE / NODE-STATE-ID / NODE-OUTCOME / NODE-CHILD-LIST(depth,9) / NODE-BAD-LIST(depth,9) / NODE-NEXT-CHILD / NODE-LAST`. All tree walking is iterative — no `CALL … RECURSIVE`. | Agent-initiated | `[R:game15_tree.cob:21-34]` TREE-STACK; `[R:game15_tree.cob:437-486]` main DFS loop |
| SB-17 | **Optimal-child filter tied to parent value**. Only children whose `STATE-OUTCOME` equals the parent's `NODE-OUTCOME` are expanded; others are set aside (anticipates SB-20). | Agent-initiated | `[R:game15_tree.cob:488-523]` BUILD-OPTIMAL-CHILDREN |
| SB-18 | **ASCII connectors assembled into `PIC X(120)` line buffer**. `\|-- / +-- ` leader + per-level `\|   ` / `    ` prefix driven by `NODE-LAST`; built via repeated `STRING ... WITH POINTER LINE-PTR` and displayed with `LINE-TEXT(1:DISPLAY-LENGTH)`. | Agent-initiated | `[R:game15_tree.cob:554-593, 647-659]` DISPLAY-CURRENT-NODE + BUILD-CHILD-PREFIX |
| SB-19 | **`--depth N` option with numeric argument validation**. `UNSTRING … DELIMITED BY ALL SPACE` into 8 token slots; rejects non-numeric, caps at 9; `DISPLAY-ELLIPSIS` emits `...` for pruned sub-trees. | Agent-initiated (mechanism); user-requested (behaviour) | `[R:game15_tree.cob:162-225, 626-645]` |
| F-01 | Bug fix: **`FILLED-TARGET` underflow loop**. First attempt declared the counter `PIC 99` (unsigned); the `UNTIL FILLED-TARGET < 0` condition never fired and the solver hung. Agent self-diagnosed from a stalling run, changed to `PIC S99`. | Agent-initiated (self-detected) | `[T:event_164]`; `[R:game15_tree.cob:53]` `FILLED-TARGET PIC S99` |
| F-02 | Bug fix: **OWNER array stale after solver phase**. `BUILD-OUTCOME-TABLE` leaves `OWNER` holding the last decoded board, so the tree-print phase was rendering from a non-empty root. Fix: explicit reset loop at the top of `DISPLAY-OPTIMAL-TREE`. | Agent-initiated (self-detected) | `[T:event_205]`; `[R:game15_tree.cob:418-420]` |

---

## Step 2c — Avoid annotations (same commit `c41b9b5`, third sub-step)

User request (PL-04): *"Enhance the optimal play tree: at each decision point, before listing the optimal (safe) moves, show which available moves would be mistakes."*

| ID | Feature | Origin | Code / evidence |
|----|---------|--------|-----------------|
| SB-20 | **Move classification into safe vs bad buckets**. Same pass as SB-17: children with value == parent go to `NODE-CHILD-MOVE`, others go to `NODE-BAD-MOVE`. Buckets kept per level on the stack. | User-requested (concept); agent-initiated (mechanism) | `[R:game15_tree.cob:504-523]` |
| SB-21 | **`avoid:` line rendered at child-level prefix**. `DISPLAY-AVOID-LINE` builds `avoid: n1, n2, …` at the same prefix depth as the optimal children (`PRINT-LEVEL = ACTIVE-LEVEL + 1`). Emitted before the child branches; skipped when `NODE-BAD-COUNT = 0`. | Agent-initiated (format) | `[R:game15_tree.cob:595-624]` |
| F-03 | Bug fix: **avoid-line indentation reused a stale prefix depth**. Rendered column was one level too shallow. Fix: compute `PRINT-LEVEL` explicitly for each call; run `BUILD-CHILD-PREFIX` with that fresh value. | Agent-initiated (self-detected) | `[T:event_276]`; `[R:game15_tree.cob:601-602, 615]` |

---

## Step 3 — Game of 0.15 variants (commit `f9c2eb1`)

User request (PL-05): *"Create `game015.cob` (counter) and `game015tree.cob` (tree with avoid). Only the display format changes."*

| ID | Feature | Origin | Code / evidence |
|----|---------|--------|-----------------|
| SB-22 | **File duplication then display-only diff** (`cp game15.cob game015.cob; cp game15_tree.cob game015tree.cob`). Explicit agent plan: "the search, symmetry, minimax, and avoid logic will stay byte-for-byte aligned". | Agent-initiated (approach) | `[T:event_362, event_363]` |
| SB-23 | **`MOVE-LABEL(9)` lookup for decimal rendering in the tree variant**. `PIC X(4) OCCURS 9` pre-filled with `"0.01" … "0.09"`. Tree node strings and avoid lines use `MOVE-LABEL(NODE-MOVE(level))` instead of raw digit. | Agent-initiated | `[R:game015tree.cob:40-42, 148-156, 599, 630-632]` |
| SB-24 | **Target-sum banner text `"Target sum: 0.15"`** in both variants. Single-line cosmetic additions in `REPORT-RESULTS` (counter) and `DISPLAY-ROOT` (tree). | Agent-initiated | `[R:game015.cob:483]`; `[R:game015tree.cob:562-566]` |
| SB-25 | **Internal integers preserved**. Owner / symmetry / state-id / minimax logic untouched — 0.15 ≡ 15 by factor-of-100. Both variants use the same 986,409 bitmap and 19,683 state table. | Agent-initiated (decision) | Whole-file diff shows only display-layer edits |
| V-03 | Validation: `./game015 --unique` reproduces the 255,168 / 31,896 counts (with "Target sum: 0.15" banner); `/tmp/game015tree --depth 3` renders `P1:0.05 [Draw]` etc. | | `[T:event_386, 387, 388]` |

---

## Step 4 — Generalised Game of N `gameN.cob` (commit `ce67d51`)

User request (PL-06): *"Usage `./gameN <target-sum> [<max-number>]` […] Find winning triples, display rules and pool, enumerate when max-number is small, provide usage message."*

| ID | Feature | Origin | Code / evidence |
|----|---------|--------|-----------------|
| SB-26 | **Two-argument CLI with strict numeric validation**. `UNSTRING … INTO ARG-TOKEN(1..4)`, extra tokens rejected, per-character digit check, `NUMVAL` conversion. | Agent-initiated | `[R:gameN.cob:148-215]` PARSE-ARGUMENTS + PARSE-POSITIVE-INTEGER |
| SB-27 | **Runtime winning-triple generation**. Nested `a < b < c, a + b + c = target, c ≤ max-number, c > b`; stores up to 84 triples in `TRIPLE-A/B/C`. | Agent-initiated | `[R:gameN.cob:301-334]` GENERATE-WINNING-TRIPLES |
| SB-28 | **Parameterised DFS over `MAX-NUMBER` and `STORED-TRIPLE-COUNT`**. Engine shape identical to SB-01 but with loop bounds read from data; win check iterates stored triples instead of hard-coded lines. | Agent-initiated (generalisation) | `[R:gameN.cob:384-451]` FIND-NEXT-CANDIDATE / APPLY-MOVE / CHECK-WIN / RECORD-GAME |
| SB-29 | **Auto-default `max-number = target-sum - 3`** (clamped to `[3, 999]`). Agent's stated justification: "values above that cannot appear in any distinct winning triple". `(default, capped at 999)` badge shown when capped. | Agent-initiated | `[R:gameN.cob:188-211, 261-270]` |
| SB-30 | **Enumeration guard `MAX-NUMBER <= 9`**. When larger, triples are still listed but the DFS is skipped with an explanatory message, so the program never hangs on combinatorial blow-up. | Agent-initiated | `[R:gameN.cob:94-101, 213-215]` |
| SB-31 | **Number-pool line-wrapping display**. `DISPLAY-NUMBER-POOL` wraps the pool at 12 entries per line using `FUNCTION MOD(TABLE-IDX, 12) = 0`. Post-validation addition noted in the session as "actual pool listing". | Agent-initiated | `[R:gameN.cob:272-299]`; `[T:event_471]` |
| SB-32 | **Usage message + explicit default / cap explanation**. `DISPLAY-USAGE` run when `ARGUMENT-ERROR = 1` (triggered by empty or malformed args). | Agent-initiated | `[R:gameN.cob:240-246]` |
| V-04 | Validation: `./gameN 15 9` → 8 triples, 255,168 games matching the classic oracle; `./gameN 15` → defaults max to 12 and lists triples but skips DFS; `./gameN abc 9` → usage; `./gameN 123456789 9` → rules + skip. | | `[T:event_441, 442, 464, 465, 479, 492-495]` |

---

## Provenance summary

| Provenance class | Count | Example IDs |
|---|---|---|
| User-driven (explicit PL prompt) | 6 | SB-07 (flag), SB-12..SB-18 (tree), SB-19 (depth), SB-20 (safe/bad split), SB-22 (0.15 variants), SB-26..SB-30 (gameN) |
| Agent-initiated (architecture/format) | 26+ | SB-01, SB-04, SB-08, SB-10, SB-13, SB-14, SB-15, SB-16, SB-27, SB-29, SB-31 |
| Bug fixes (self-detected) | 3 | F-01 (FILLED-TARGET underflow), F-02 (stale OWNER), F-03 (avoid-line indent) |

## Mapping to BL / UI / PL

| BL | UI | PL | SB items |
|----|----|----|----------|
| BL-01 Game counter | UI-01 | PL-01 | SB-01 .. SB-06 |
| BL-02 Unique flag | UI-03 | PL-02 | SB-07 .. SB-11 |
| BL-03 Optimal tree | UI-05 | PL-03 | SB-12 .. SB-19, F-01, F-02 |
| BL-04 Avoid annotations | UI-07 | PL-04 | SB-20, SB-21, F-03 |
| BL-05 Game of 0.15 | UI-09 | PL-05 | SB-22 .. SB-25 |
| BL-06 Game of N | UI-11 | PL-06 | SB-26 .. SB-32 |

## Scope notes

- **Cross-cutting architecture** (factorial bitmap, 19,683-state retrograde solve, iterative explicit-stack printing) is entirely agent-initiated — the prompts specify behaviour, not data structures.
- `.gitignore` containing `game15` and `game15_tree` is agent-initiated repo hygiene (OP, not a feature).
- The three bug fixes (F-01..F-03) and the SB-31 "pool listing" regression were all self-detected by running the binary — no user-reported failures.
