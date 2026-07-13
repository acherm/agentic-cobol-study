# STORY — cobol-tictactoe

## The trick is the isomorphism

The Game of 15 is secretly tic-tac-toe. Solving it in COBOL took less than 3 hours of active collaboration.

Two players alternate picking numbers from {1..9}; first to own three that sum to 15 wins. Arrange 1..9 in the Loh-Shu magic square

    2 7 6
    9 5 1
    4 3 8

and every row, column, and diagonal sums to 15. Picking a number *is* claiming a square; winning triples *are* tic-tac-toe lines. Once you see the isomorphism the game theory is textbook — it is a forced draw, there are exactly 8 winning triples, and the symmetry group is D4. The interesting engineering therefore sits one level down: how do you run minimax, DFS with backtracking, and an ASCII tree printer in a language that has no call stack?

## Minimax in COBOL beats the game theory

The shipped answer is an explicit-stack simulation. A `DEPTH` counter plus a per-level `NEXT-TRY` array act as a frame pointer and a local iterator, `PERFORM`-d in a loop rather than recursed. Player-to-move is inferred from `DEPTH mod 2`, so no turn variable is stored. The win check is a 24-character literal `"159168249258267348357456"` with REDEFINES overlaying eight (T1, T2, T3) triples — the magic-square encoding, flattened into `PIC X`. The minimax solver adds a base-3 transposition table keyed by `sum(OWNER(i) * 3^(i-1))` into a 19 683-entry `MEMO-TABLE`, and a two-pass architecture: pass 1 solves every reachable position, pass 2 walks the solved graph to render the tree. The ASCII renderer itself is written without strings or recursion — an `IS-LAST` boolean array per depth drives the `|  ` vs. `    ` continuation prefixes, assembled char-by-char into a `PIC X(200)` line buffer. The same explicit-stack pattern is reused in `gameN.cob`, generalized to a runtime-computed `NUM-TRIPLES` table.

## Two sessions, 31 features, one clean chain

Two Claude Code sessions. The first, opened 2026-03-12, took the initial request ("write a COBOL program that computes the number of possible games") through symmetry deduplication, the optimal-play tree, and the avoid annotations. The second, 2026-04-07, produced the parameterized `gameN`. Between them, 31 F-### entries in `SPECIFICATION_BACKLOG.md` trace a tight chain: **counter -> tree -> avoid -> 0.15 variant -> gameN**. Only 5 of the 31 came directly from the user; the other 26 were agent-decided — the D4 permutation table, the base-3 memo, the IS-LAST rendering trick, the CHOSEN(DEPTH)-based undo, the `--depth N` flag, the classic-Game-of-15 detection in `gameN`, the enumeration guard for MAX-NUM > 9. Two bug fixes (F-19, F-20) were both self-detected during testing: a two-digit `PIC 99` was truncating to the wrong digit on display, and an inner `COLLECT-OPTIMAL` loop was clobbering the caller's `CUR-NUM` slot. Both were diagnosed and patched in the same session they were introduced.

One user phrasing is worth flagging. When asked to add a flag "to compute numbers without duplicates", the agent chose to interpret "duplicates" as *board-symmetry equivalence* via the magic-square isomorphism, not mere move-order collisions. That is the harder reading and the correct one.

## Five programs, numbers that externally check out

The build delivers five playable binaries: `game15` (counter, with `--unique`), `game15tree` (optimal-play tree with avoid annotations and `--depth N`), `game015` and `game015tree` (the cosmetic 0.15 variant — display-only adaptation, same engine), and `gameN` (parameterized target sum and max number, with dynamic triple generation). The counter prints

    Player 1 wins:   131184
    Player 2 wins:    77904
    Draws:            46080
    Total games:     255168

and the full optimal-play tree closes with 3 584 terminal draw positions and zero forced wins — numbers that match independent brute enumeration of the state space, so the verification story is not self-reference. `./gameN 15 9` reproduces the 255 168 total; `./gameN 12 8` gives 34 704; `./gameN 10 7` gives 4 752. External checkability is the nice property here: the game counts are ground truth, not a rubric judgment.

## Compute budget was never the constraint

408 turns across the two sessions, 2 h 53 m of active collaboration time, 5 git commits. Peak context 140 k of 1 M (14 %), two compactions, and a tool-output error rate of 1.4 % — the lowest in the whole corpus. Zero bug-report-style user prompts, three redirects, 1.2 % of active time spent on `bug_fix`. On every axis the session felt comfortable: the agent had headroom to explore, the user did not have to firefight, and nothing was cut for budget reasons.

## Why this project became the reference exemplar

"Clean, smooth success" is how the assessment tags it, and the tag earned a second life: `REPLAY_PROMPTS.md` was written directly off this project and then used to drive subsequent replica runs across the corpus. That file specifies each step in behavior-only language — inputs, outputs, verification numbers — with no algorithm names, no data-structure prescriptions, no COBOL idioms. It only exists because the original build was coherent enough to be retroactively decomposed into six free-standing prompts without cheating on the dependencies. A project that had stumbled on symmetry, or left the avoid logic half-finished, or conflated the 0.15 variant with the engine, could not have been abstracted that way. The replay pack is therefore a downstream quality signal in its own right: the smoothness that registers as 1.4 % error and 14 % context at the metric level also registers as reusability at the prompt level — a project tidy enough to become a template for the others.
