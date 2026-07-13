# Key Features — `chess-cobol-cc`

## Preamble

The project was asked to build a UCI-compliant chess engine in GNU COBOL 3.2
from scratch, then assess its playing strength by running automated
`cutechess-cli` matches against strength-capped Stockfish opponents. A "key
feature" here is a delivered capability of depth ≥ 1 that is not purely
infrastructure: the ranking below consolidates the 51 SB entries into the
dozen capabilities that actually moved the needle on correctness, Elo, or
toolchain viability. Significance is scored per the taxonomy
(`score = depth × (1 + effort × 0.5)`) and each row carries a note saying
whether the capability is textbook-algorithmic or whether it required
domain, system, or language-level engineering in COBOL specifically.

## Ranked table

| rank | SB/F id | title | class | depth | effort | score | significance note | evidence pointer |
|---:|---|---|---|---:|---:|---:|---|---|
| 1 | SB-011, SB-012 (BL-004) | Explicit-stack negamax alpha-beta with per-ply `WS-PLY-DATA(12)` + `SEARCH-MAKE/UNMAKE-MOVE` | **LNG** (sec. ALG) | 3 | 3 | 7.5 | Not "just minimax": COBOL's `PROGRAM-ID … IS RECURSIVE` was declared but deemed unreliable, so the agent hand-rolled an explicit search stack with OCCURS-based per-ply state arrays — this is the language-level achievement the taxonomy explicitly names. | `[R:chess-engine.cob:320]` `WS-PLY-DATA`; `[T:#263]` §3; `[T:#865]` |
| 2 | BL-006 (SB-015…SB-049) | Iterative Elo-improvement loop: quiescence + MVV-LVA + killers + delta pruning + history + aspiration + LMR + PV-ordering + persistent killer/history + 7 measured reverts | **PRF** (sec. ALG) | 3 | 3 | 7.5 | This is not a checklist of textbook pruning techniques added in one go — it is 14 match-driven INCR→TEST→RETR cycles across 9 phases, with each change kept only if the 20-game match improved vs the previous binary, producing a documented 1517 → 1608 → 1627 → 1647 Elo ladder. The negative-result reverts (SB-027/033/037/038/042/043/047) are the signal. | `[M:project_elo_progress.md]`, `[M:feedback_overhead_sensitivity.md]`, `[R:phase4d_vs1500.pgn]` … `[R:phase9_vs1500.pgn]` |
| 3 | SB-050, SB-051 (BL-007) | Multi-level Elo triangulation: 100 games vs SF 1400/1500/1600/1700 → weighted ~1621 / realistic ~1630 Elo | **CMP** (sec. VER) | 3 | 2 | 6.0 | Emergent composition: this report is only possible because the UCI loop (SB-003), the legal-move filter (SB-005), the search (SB-011), the time manager (SB-016), and a surviving v4b binary all exist and interoperate with `cutechess-cli` + Stockfish. Removing any one upstream piece makes the measurement meaningless. | `[R:elo_vs1400.pgn]`, `[R:elo_vs1600.pgn]`, `[R:elo_vs1700.pgn]`; `[T:#3713]` |
| 4 | SB-003 (BL-002) | UCI protocol implementation: `ACCEPT FROM CONSOLE` dispatcher for `uci / isready / position [startpos/fen] [moves …] / go [depth N / wtime / btime / movestogo] / quit` | **PRO** (sec. DOM) | 2 | 2 | 4.0 | Implementing a published external specification (UCI) inside a language whose native I/O primitive is record-oriented — not line-oriented — is protocol-compliance work, not algorithm work. Must interoperate byte-for-byte with cutechess-cli's parser. | `[T:#263]` §3; `[R:chess-engine.cob]` UCI-CMD-* paragraphs |
| 5 | SB-004, SB-005 (BL-002) | FEN parser + pseudo-legal move generator for all piece types + castling legality + king-safety legal-move filter | **DOM** | 2 | 2 | 4.0 | Pure domain modelling: chess rules — 8×8 board, castling rights, en-passant, legality filter — encoded into COBOL `OCCURS` tables, `EVALUATE` per-piece dispatch, and inline attack detection. No textbook "algorithm" involved; it is the rule set. | `[T:#263]` §3 `GENERATE-*`, `FILTER-LEGAL-MOVES` |
| 6 | SB-015, SB-016 (BL-005) | Iterative deepening loop + UCI `wtime/btime/movestogo` clock-aware time management with 512-node granularity and soft-time (4× last iter) guard | **DOM** (sec. PRO) | 2 | 2 | 4.0 | Binds the UCI clock protocol to the search: the revert in SB-038 (7 forfeits under `time/movestogo` without a safety buffer) shows this is non-trivial domain logic, not a library call. | `[T:#865]` §3; `[T:#3088]` §4; `[M:feedback_time_management.md]` |
| 7 | SB-050 harness + `cutechess-cli` + `UCI_LimitStrength` integration | Cross-process match harness: engine binary ↔ cutechess-cli ↔ Stockfish, with PGN capture per phase | **SYS** | 2 | 2 | 4.0 | Three-process integration (agent-launched cutechess-cli orchestrating a COBOL child and a Stockfish child over UCI pipes, parsing PGN back) is the "engineering lives at the boundary" tell-tale from the taxonomy. | `[R:phase*.pgn]` (25 files); `[R:.claude/settings.local.json]` PC-001 pre-approved cmd list |
| 8 | SB-009, SB-031, SB-032, SB-035 (BL-003, BL-006) | Layered classical evaluation: material + PST + bishop pair + rook on open/semi-open file + doubled/isolated/passed pawns | **DOM** (sec. ALG) | 2 | 2 | 4.0 | Textbook-classical eval, but the layering order matters: each term was kept only because it improved the 20-game match. Encoded via REDEFINES for PST tables. | `[T:#263]` §3 `EVALUATE-POSITION`; `[T:#2648]` §3; `[T:#3088]` §3 |
| 9 | SB-026 | `-fwrapv` toolchain fix for the GNU COBOL `-O2` hang before `MAIN-PROGRAM` | **INF** (sec. LNG) | 2 | 1 | 3.0 | A compiler bug found by empirical bisection (noopt/o1/os/o3 binaries still on disk). Low LOC but high blast radius: without it, no build runs. Pure toolchain-level engineering. | `[T:#1661]` §4; `[R:COB_CFLAGS]` pinned in README §3 |
| 10 | SB-007, SB-008, SB-018, SB-028 | Correctness hardening: input-buffer overflow (256→8192), FEN column `PIC 9`→`PIC 9(2)`, root-move corruption across ID iterations, time-formula regression | **VER** | 2 | 1 | 3.0 | Four defect-fixes driven by observed match failures (illegal moves in PGN; time forfeits). The PGN harness acted as the test oracle — no unit tests exist. | `[T:#263]` §4; `[T:#865]` §4; `[T:#3088]` §4 |
| 11 | SB-036, SB-048 | Late Move Reductions with re-search state machine (0/1/2) + aggressive R=2 branch for move-index ≥ 7 | **ALG** | 2 | 2 | 4.0 | Standard search-tree pruning algorithm, non-trivial but textbook. Interaction with MAX-PLY arrays forced SB-037's futility-pruning revert, which is why the score isn't higher. | `[T:#3088]` §3; `[T:#3606]` |
| 12 | SB-044, SB-045 | PV-move root ordering (prev-iter best gets score 20 000) + **persistent** killer/history tables across ID iterations | **ALG** (sec. PRF) | 2 | 1 | 3.0 | Single largest measured Elo win (+30, v3b→v4), driven by the `feedback_overhead_sensitivity.md` insight that only zero-per-node-cost changes survive. Textbook idea, informed placement. | `[T:#3420]`, `[T:#3427]`; `[R:phase7_vs1500.pgn]` |

## Composition chains

1. **FEN parser (SB-004) → pseudo-legal + legal move generator (SB-005) → explicit-stack negamax (SB-011/012) → iterative deepening + time mgmt (SB-015/016) → UCI loop (SB-003) → cutechess-cli harness (SYS) → multi-level Elo triangulation (SB-050/051).** The final 1630-Elo number is only meaningful because every upstream link is correct — an illegal move at link 2, a stack-frame bug at link 3, or a clock miscount at link 4 would invalidate the oracle.
2. **Match harness (SYS) → PGN artefact → agent-authored memory note (`feedback_overhead_sensitivity.md`) → zero-per-node-cost constraint → SB-044/045 persistent-table redesign.** The engine's best single improvement emerged only because the failed experiments (SB-033/042/043/047) were captured as persistent agent memory and *constrained the next change*.
3. **`-O2` hang (SB-026) → `-fwrapv` toolchain fix → v1/v2/v3b/v4/v4b binary snapshots → checkpoint-based Elo ladder.** Without the compiler workaround there is no engine at all; the versioned binaries still on disk are the substrate the whole Elo ladder is measured against.
4. **UCI command dispatcher (SB-003) → `go depth N` parameter parsing (SB-013) → `wtime/btime/movestogo` parsing (SB-016) → soft-time guard (SB-038-fix).** The emergent capability is "plays a real tournament-legal 40/60 game without forfeiting," a property that requires *all four* pieces to coexist and that regressed visibly (3.5/20 → 13.5/20) when the last link was broken in phase 5.

## Significance profile

| Class | Count in top 12 | Notes |
|---|---:|---|
| ALG | 2 | LMR and PV/persistent-table idea — classical. |
| DOM | 3 | Move gen, eval, time-mgmt-as-protocol-binding. |
| SYS | 1 | cutechess-cli three-process harness. |
| INF | 1 | `-fwrapv` toolchain fix. |
| PRO | 1 | UCI command protocol compliance. |
| LNG | 1 | Explicit-stack negamax in COBOL (rank 1). |
| VER | 1 | Four correctness defect-fixes clustered. |
| PRF | 1 | The 14-cycle measured-improvement loop (rank 2). |
| CMP | 1 | Multi-level Elo triangulation (rank 3). |
| **Total** | **12** | (Secondary tags: ALG ×3, PRO ×1, DOM ×1, LNG ×1, VER ×1, PRF ×1, not counted above.) |

## Verdict

**Hybrid, centre-of-gravity LNG + PRF + SYS, not "just minimax":** the top three ranks are a language-level achievement (explicit-stack search in COBOL), a performance-engineering loop (14 measured INCR→TEST→RETR cycles with 7 reverts), and an emergent composition (the Elo triangulation), each of which dominates any individual textbook-algorithm component.
