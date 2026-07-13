# Key Features — cobol-tictactoe

## Preamble

The project was asked to implement the Game of 15 in GnuCOBOL: a brute-force counter of all playable games, an ASCII optimal-play tree (minimax), "avoid" annotations that distinguish safe from losing moves, a cosmetic 0.15 variant, and a parameterised "Game of N" generator. The Game of 15 is isomorphic to tic-tac-toe via the 3x3 magic square, so the algorithms themselves are textbook — the key features here sit at the intersection of (a) domain modelling (the magic-square isomorphism, D4 symmetry, dynamic triple generation), (b) language-level achievement (simulating recursion and a call stack in COBOL via `PERFORM` + level-indexed arrays), and (c) emergent composition (each program layer only becomes possible once the previous one is correct). Trivial display tweaks, usage messages and isolated bug-fixes are excluded; the bar is depth >= 1 and non-purely-infrastructure.

## Ranked table

| Rank | SB id | Title | Class | Depth | Effort | Score | Evidence | Significance note |
|------|-------|-------|-------|-------|--------|-------|----------|-------------------|
| 1 | F-10,F-11,F-12 | Minimax tree with base-3 memoization (two-pass) | ALG | 2 | 3 | 5.0 | `game15tree.cob:114-158,187-297` | Textbook minimax, but the two-pass architecture (solve-then-print) plus 19683-entry transposition table on a 9-cell board pushes it past an isolated algorithm — it is the substrate for F-13/F-14/F-17. |
| 2 | F-01,F-25 | Iterative DFS with explicit stack (DEPTH + NEXT-TRY arrays) | LNG | 2 | 3 | 5.0 | `game15.cob:144-215`; `gameN.cob:283-327` | This is the project's signature language-level move: COBOL has no call stack, so recursion is simulated via a DEPTH counter and per-level NEXT-TRY array. Re-used across three of the five programs. |
| 3 | F-07,F-08 | D4 symmetry canonicalisation via magic-square permutations | DOM | 3 | 2 | 6.0 | `game15.cob:80-96,232-251` | Not an algorithm lookup — requires understanding that Game-of-15 inherits the *tic-tac-toe* symmetry group through the magic-square isomorphism, then encoding the 8 D4 permutations as number-to-number maps rather than cell-to-cell. The user said "duplicates"; the agent chose symmetry-equivalence, which is the hard interpretation. |
| 4 | F-14,F-16 | ASCII tree renderer with per-depth IS-LAST connectors | DOM | 2 | 2 | 4.0 | `game15tree.cob:81-88,445-511` | Standard tree-printing problem, but implemented without strings, stacks or recursion: continuation prefixes are recomputed per depth from an IS-LAST boolean array, output assembled char-by-char into `PIC X(200)`. |
| 5 | F-17,F-18 | Move classification + "avoid" annotations | CMP | 2 | 2 | 4.0 | `game15tree.cob:75-79,429-440,513-545` | Only meaningful once minimax values exist: partition available moves into OPT-NUMS vs BAD-NUMS by comparing each child's minimax value to the parent's, then render an `avoid: ...` line aligned with the tree prefix. Pure composition on top of F-1 and F-4. |
| 6 | F-04 | Win detection via hard-coded magic triples | DOM | 1 | 1 | 1.5 | `game15.cob:71-78,217-227` | The eight triples `{1,5,9},{1,6,8},...` are the concrete artefact of the magic-square isomorphism — the domain knowledge that makes this tic-tac-toe. Shallow but load-bearing. |
| 7 | F-24,F-25,F-26 | Parameterised Game of N (dynamic triples + generalised DFS) | DOM | 2 | 2 | 4.0 | `gameN.cob:173-195,42-49,283-327,146-154` | Lifts the hard-coded 9-number/8-triple core into a two-argument family: triples generated at runtime by a nested loop (a<b<c, a+b+c=target, c<=max), DFS bounds taken from data. This is domain generalisation, not a new algorithm. |
| 8 | F-02,F-03 | Ownership model + depth-parity player alternation | DOM | 1 | 1 | 1.5 | `game15.cob:22-23,161-167` | OWNER-TABLE(9) of {0,1,2} doubles as state and win-check input; player is inferred from `DEPTH mod 2` rather than stored. Small but clean domain encoding. |
| 9 | F-21,F-22 | 0.15 display-layer variant (format-only adaptation) | DOM | 1 | 1 | 1.5 | `game015tree.cob:425-441,449-453` | Correctly identifies that 0.15 is mathematically identical to 15 and implements it as a display-only change (prefix `"0.0"` + 5-char tree indent), instead of touching the engine. Cheap, but the *decision* is a domain-modelling win. |
| 10 | F-13 | COLLECT-OPTIMAL partitioning primitive | CMP | 2 | 1 | 2.5 | `game15tree.cob:388-443` | Shared sub-routine that F-14 (optimal children) and F-17 (avoid set) both rely on; reads memoized minimax values to classify moves in one pass. Only meaningful because F-1 exists. |
| 11 | F-27,F-29,F-31 | Input validation + enumeration guard + rules commentary | DOM | 1 | 1 | 1.5 | `gameN.cob:156-171,197-281,83-109` | Guards (MAX-NUM>9 skipped, target>=6, etc.) and qualitative rules commentary ("games tend to end in draws") encode the *playability envelope* of the parameterised family. Defensive domain work. |
| 12 | F-19,F-20 | CUR-NUM aliasing bug-fixes (DISP-DIGIT, CHOSEN(DEPTH)) | LNG | 1 | 1 | 1.5 | `game15tree.cob:91,477-478,310,374` | Both fixes are artefacts of the explicit-stack simulation: two-digit PIC truncating to the wrong digit, and an inner loop clobbering the caller's "current move" slot. Small but diagnostic of what language-level recursion-simulation actually costs. |

## Composition chains

1. **Counter -> symmetry -> canonical enumeration** — F-01 (iterative DFS) -> F-04 (magic triples) -> F-07 (D4 permutation table) -> F-08 (canonical-form check). Emergent capability: the 255,168 -> 31,896 symmetry-quotient count, which requires the full enumerator *and* a correctly encoded symmetry group.
2. **Solver -> tree -> avoid** — F-10/F-11 (two-pass minimax) -> F-12 (base-3 memoization) -> F-13 (optimal/bad partition) -> F-14 (ASCII render) -> F-17/F-18 (avoid annotations). The avoid lines only have meaning because the solver already assigns a game-theoretic value to every reachable position; F-17 is textbook *composition*, not a new algorithm.
3. **Game-of-15 engine -> Game-of-N engine** — F-01/F-02/F-03/F-04 (hard-coded 9/8-triple engine) -> F-24 (dynamic triple generation) -> F-25 (generalised DFS over MAX-NUM and NUM-TRIPLES) -> F-26/F-27/F-31 (auto-defaults, validation, guard). Emergent capability: a whole family of games derived by parameter sweep from the same correctness core.
4. **Core logic -> 0.15 variant** — F-01..F-18 -> F-21/F-22. The variant is meaningful *exactly because* the engine already works; the agent's decision to adapt display only (not logic) is the composition-aware move.

## Significance profile

| Class | Count in top 12 |
|-------|-----------------|
| ALG   | 1 |
| DOM   | 6 |
| SYS   | 0 |
| INF   | 0 |
| PRO   | 0 |
| LNG   | 2 |
| VER   | 0 |
| PRF   | 0 |
| CMP   | 2 |

Centre of gravity: **DOM + LNG + CMP**, with a single but load-bearing ALG entry. No SYS/PRO/VER/PRF work, which matches a self-contained GnuCOBOL project with no external protocols, no FFI and no performance iteration.

## Verdict

Hybrid **domain-modelling + language-achievement** project with strong emergent composition: the algorithm content is textbook (one minimax, one DFS), but the magic-square/D4 encoding, the COBOL-recursion-via-explicit-stack, and the counter -> tree -> avoid -> variant -> parameterised chain are where the real engineering lives.
