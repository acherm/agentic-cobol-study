# Key Features — game15-cobol-codex

## Preamble

The project was asked, via the replay-prompt pack of the sibling `cobol-tictactoe`, to implement the Game of 15 in GnuCOBOL: a brute-force counter of all playable games, an ASCII optimal-play tree (minimax), "avoid" annotations separating safe moves from losing ones, a cosmetic 0.15 variant, and a parameterised "Game of N" generator. The Game of 15 is isomorphic to tic-tac-toe via the 3x3 magic square, so the algorithms themselves are textbook — the key features here sit at the intersection of (a) **domain modelling** (the magic-square-isomorphic dedup, the 19,683-state retrograde solve, runtime triple generation), (b) **language-level achievement** (doing all tree walks without recursion via hand-managed per-level stacks in COBOL), and (c) **emergent composition** (each program layer only becomes possible once the previous one is correct). Trivial init blocks, usage messages and isolated bug-fixes are excluded; the bar is depth >= 1 and non-purely-infrastructure. Where relevant the rows note how Codex's idiomatic choice differs from the Claude-Code-built sibling.

## Ranked table

| Rank | SB id | Title | Class | Depth | Effort | Score | Evidence | Significance note |
|------|-------|-------|-------|-------|--------|-------|----------|-------------------|
| 1 | SB-12,SB-13,SB-14,SB-15 | Bottom-up retrograde minimax over all 19,683 base-3 states | ALG | 3 | 3 | 7.5 | `game15_tree.cob:10-15,116-124,227-243,267-415` | Textbook retrograde analysis, but Codex chose to fill the *entire* 3^9 state space (not just the reachable 5,478), with a validity predicate that enforces piece-count and "only the winner moved last" invariants. The whole downstream tree printer (SB-16..SB-21) is a query over this table. |
| 2 | SB-10 | Factorial-rank canonical hash into 986,409-byte SEEN bitmap | DOM | 3 | 2 | 6.0 | `game15.cob:55-59,69-70,381-407` | Unusual: Codex maps each canonical move sequence to an integer in `[0, 9! + lower-length offsets)` using falling-factorial weights and a `LENGTH-OFFSET(L)` start-index per length, then uses a single `PIC X OCCURS 986409` array as the uniqueness set. Not an algorithm lookup — it is a custom-built perfect hash for variable-length permutation prefixes of {1..9}. Claude Code's sibling used a simpler min-of-orbit + standard set; Codex built its own indexable structure. |
| 3 | SB-01,SB-16,SB-28 | Iterative DFS with explicit per-level stack (re-used in 3 programs) | LNG | 2 | 3 | 5.0 | `game15.cob:144-215`; `game15_tree.cob:437-486`; `gameN.cob:372-439` | Project's signature language-level move: every tree walk is hand-driven by `SEARCH-DEPTH`/`ACTIVE-LEVEL` + per-depth arrays (`NEXT-CANDIDATE`, `NODE-CHILD-LIST`, `NODE-BAD-LIST`, `NODE-LAST`). No `CALL … RECURSIVE` anywhere. Comment at `game15_tree.cob:436` makes the choice explicit: "Iterative DFS avoids relying on recursive CALL behavior in GnuCOBOL". |
| 4 | SB-08,SB-09 | D4 symmetry canonicalisation via magic-square permutations | DOM | 3 | 2 | 6.0 | `game15.cob:61-64,175-254,323-379` | Not an algorithm lookup — requires understanding that Game-of-15 inherits the *tic-tac-toe* symmetry group through the magic-square isomorphism, then encoding the 8 D4 permutations as number-to-number maps (via explicit `MOVE n TO SYMMETRY-VALUE(sym, k)` rows, not a REDEFINES string). The user said "duplicates"; the agent chose symmetry-equivalence, which is the hard interpretation. |
| 5 | SB-20,SB-21 | Move classification into safe/bad buckets + avoid-line renderer | CMP | 2 | 2 | 4.0 | `game15_tree.cob:32-34,488-523,595-624` | Only meaningful once SB-12..SB-15 exist: at each node, every legal child is looked up in `STATE-OUTCOME`; outcome-preserving moves go to `NODE-CHILD-LIST`, the rest go to `NODE-BAD-LIST`. `DISPLAY-AVOID-LINE` renders `avoid: n1, n2, …` at the child-prefix column. Pure composition on top of the retrograde solver. |
| 6 | SB-18 | ASCII tree renderer with per-level `NODE-LAST` connectors | DOM | 2 | 2 | 4.0 | `game15_tree.cob:36-47,554-593,626-659` | Standard tree-printing problem, but implemented without strings, stacks or recursion. Connectors rebuilt each line from `NODE-LAST(level)`: `|   ` when the ancestor has more siblings, `    ` otherwise; trailing `|-- ` or `+-- `. Output assembled char-by-char into `LINE-TEXT PIC X(120)` via repeated `STRING … WITH POINTER`. |
| 7 | SB-27,SB-28,SB-29 | Parameterised Game of N (dynamic triples + generalised DFS + default rule) | DOM | 2 | 2 | 4.0 | `gameN.cob:27-38,173-195,301-334,188-211,372-439` | Lifts the hard-coded 9-number/8-triple core into a two-argument family: triples generated at runtime by a nested loop (`a<b<c, a+b+c=target, c≤max`), DFS bounds read from `MAX-NUMBER` and `STORED-TRIPLE-COUNT`. Default `max = target-3` is justified on-the-fly in the agent's reasoning ("values above cannot appear in any distinct winning triple"). Domain generalisation, not a new algorithm. |
| 8 | SB-04 | Direct tic-tac-toe-line win detection (no magic-triple encoding) | DOM | 1 | 1 | 1.5 | `game15.cob:419-475` | Eight triples written out as 8 explicit `IF OWNER(a)=CP AND OWNER(b)=CP AND OWNER(c)=CP` blocks. These are the tic-tac-toe cell triples *after* the magic-square mapping (e.g. `{1,5,9}` is the magic-sum-15 triple). Shallow but load-bearing. Choice diverges from the sibling's magic-triple-string+REDEFINES idiom. |
| 9 | SB-03 | Pre-tabulated `PLAYER-AT-DEPTH` schedule | DOM | 1 | 1 | 1.5 | `game15.cob:14-15,143-151` | Player is stored in a `PIC 9 OCCURS 9` array explicitly initialised `1,2,1,2,1,2,1,2,1`, rather than computed from depth-parity. Small but clean domain encoding; trades a multiplicity-of-branches for a flat index lookup (a Codex-idiomatic choice — CC computed parity via `DIVIDE … REMAINDER`). |
| 10 | SB-22,SB-23,SB-24 | 0.15 display-layer variant via `cp` + `MOVE-LABEL(9)` table | DOM | 1 | 1 | 1.5 | `game015tree.cob:40-42,148-156,599,630-632`; `game015.cob:483` | Correctly identifies that 0.15 is mathematically identical to 15; implements it as a duplicated file plus a 9-entry lookup table from digit to label. Internal integer representation preserved so the 986,409 bitmap and 19,683 state table stay byte-for-byte identical. The *decision* is a domain-modelling win. |
| 11 | SB-31 | Number-pool line-wrapping display in `gameN` | DOM | 1 | 1 | 1.5 | `gameN.cob:272-299` | Wraps the pool `1, 2, …, max` into lines of 12 via `FUNCTION MOD(TABLE-IDX, 12) = 0`. Added after a first-pass regression (agent noticed the pool display was missing), so there is also a fix-forward signal in this feature. |
| 12 | F-01,F-02,F-03 | Self-detected bug-fixes during tree + avoid development | LNG | 1 | 1 | 1.5 | `[T:event_164,205,276]`; `game15_tree.cob:53,418-420,601-602` | Three artefacts of the explicit-stack / full-state-table architecture: `FILLED-TARGET PIC 99` underflowing (fix: `PIC S99`), `OWNER` stale after the solver phase (fix: reset before display), avoid-line stealing a stale `PRINT-LEVEL` (fix: recompute per call). Small but diagnostic of what language-level stack simulation actually costs. |

## Composition chains

1. **Counter -> symmetry -> canonical enumeration** — SB-01 (iterative DFS) -> SB-04 (direct lines) -> SB-08 (D4 permutation table) -> SB-09 (min-of-orbit) -> SB-10 (factorial-rank bitmap). Emergent capability: the 255,168 -> 31,896 symmetry-quotient count, which requires a correct full enumerator *and* the custom factorial-rank hash as the uniqueness set.
2. **Retrograde solve -> tree -> avoid** — SB-12 (base-3 encoding) -> SB-13 (bottom-up fill order) -> SB-14 (validity predicate) -> SB-15 (minimax over children) -> SB-16 (per-level node stack) -> SB-17/SB-18 (optimal-child filter + ASCII connectors) -> SB-20/SB-21 (safe/bad split + avoid line). The avoid lines only have meaning because the state table already assigns an optimal-play outcome to every reachable position; SB-21 is textbook *composition*, not a new algorithm.
3. **Game-of-15 engine -> Game-of-N engine** — SB-01/SB-04 (hard-coded 9/8-triple engine) -> SB-27 (dynamic triple generation) -> SB-28 (generalised DFS over `MAX-NUMBER` and `STORED-TRIPLE-COUNT`) -> SB-29 (auto-default) -> SB-30 (enumeration guard) -> SB-31 (pool listing). Emergent capability: a whole family of games derived by parameter sweep from the same correctness core.
4. **Core logic -> 0.15 variant** — SB-01..SB-21 -> SB-22/SB-23/SB-24/SB-25. The variant is meaningful *exactly because* the engine already works; Codex's decision to duplicate the files and only patch the display layer (via a `MOVE-LABEL(9)` table) is the composition-aware move.

## Significance profile

| Class | Count in top 12 |
|-------|-----------------|
| ALG   | 1 |
| DOM   | 7 |
| SYS   | 0 |
| INF   | 0 |
| PRO   | 0 |
| LNG   | 2 |
| VER   | 0 |
| PRF   | 0 |
| CMP   | 1 |

Centre of gravity: **DOM + LNG**, with a single but very load-bearing ALG entry (the retrograde solver) and one CMP (the avoid annotations). No SYS/PRO/VER/PRF work, which matches a self-contained GnuCOBOL project with no external protocols, no FFI and no performance iteration.

## Verdict

Hybrid **domain-modelling + language-achievement** project with strong emergent composition — same verdict as the Claude-Code sibling, but with Codex leaning a step further into **eager, table-driven domain encodings** (the 986,409-byte factorial-rank bitmap and the 19,683-state retrograde table). The algorithm content is textbook (one minimax, one DFS), but the custom indexable set structure, the retrograde-over-entire-state-space decision, the COBOL-without-recursion idiom, and the counter -> tree -> avoid -> variant -> parameterised chain are where the real engineering lives.
