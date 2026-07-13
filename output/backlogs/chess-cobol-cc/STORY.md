# STORY — `chess-cobol-cc`

## 1. What was asked, and why COBOL makes it strange

On the evening of 12 March 2026, the user typed a single paragraph into Claude Code: *"I want to build a chess engine in COBOL (using GNU Cobol)… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of 'similar' levels."* That one sentence (prompt `PL-ROOT`, event `#4`) kicked off a seventeen-day session that would end with a UCI-compliant engine playing at roughly **1630 Elo** — a solid club-player level — written in a language designed for 1960s batch payroll jobs.

The strangeness is the whole point. Modern chess engines assume bitboards (64-bit integers as sets of squares), pointer-chased move stacks, SIMD evaluation, multi-threaded search, and — in the Stockfish era — a neural network evaluator (NNUE). COBOL gives you none of these natively. It has no pointers; recursion exists (`PROGRAM-ID … IS RECURSIVE`) but is rarely trusted; bit manipulation has to go through `USAGE COMP-5` plus `FUNCTION MOD`; there is no SMP, no SIMD, no linear-algebra runtime. Asking an LLM agent to deliver a playable UCI engine in that language is closer to a systems-engineering challenge than a textbook algorithm exercise.

## 2. Why this is hard in the specific

A chess engine is the composition of four tightly-coupled subsystems: move generation (pseudo-legal generation + castling + en-passant + a king-safety filter), search (alpha-beta with a pile of pruning heuristics), evaluation (material + piece-square tables + pawn structure + king safety), and protocol (UCI over stdin/stdout, clock-aware with `wtime/btime/movestogo`). Any one of them silently broken invalidates the Elo measurement at the end. On top of that, you need a three-process harness — `cutechess-cli` orchestrating the COBOL child and a `UCI_LimitStrength`-capped Stockfish child — to generate PGN oracles you can actually score against.

In COBOL specifically: the negamax stack has to be hand-rolled because recursion is unreliable, so the agent allocated `WS-PLY-DATA(12)` — twelve per-ply state slots — and wrote its own `SEARCH-MAKE-MOVE` / `SEARCH-UNMAKE-MOVE` wrappers (SB-011, SB-012). Piece-square tables live as `REDEFINES` over `OCCURS` arrays. The UCI command loop is an `ACCEPT … FROM CONSOLE` dispatcher, not a line-buffered reader, and had to be made byte-compatible with cutechess-cli's parser.

## 3. How the build actually went

The chronology falls into nine agent-named phases across seventeen days, bounded by five auto-compaction events (at session events `#263`, `#865`, `#1661`, `#2648`, `#3088` — dated 2026-03-12, 03-16, 03-20, 03-21, and 03-23 respectively). Each compaction produced an agent-authored summary that is the richest surviving record of what happened in the preceding segment.

**Phase 1 (EP-P1, 2026-03-12).** The skeleton: FEN parser, 8×8 board, pseudo-legal move generation for every piece type, castling legality, a king-safety filter (`FILTER-LEGAL-MOVES`), and random-legal-move output. Two immediate defects surfaced from the PGN oracle: the input buffer overflowed on long `position` lines (SB-007: widen `WS-INPUT-LINE` to `PIC X(8192)`), and FEN column parsing wrapped at 9 (SB-008: `PIC 9` → `PIC 9(2)`). After the fixes, twenty straight stress games were clean.

**Phases 2 and 3 (EP-P2, EP-P3).** Material (P=100, N=320, B=330, R=500, Q=900, K=20000), piece-square tables, then the explicit-stack negamax — the language-level achievement. First match vs Stockfish 1320 recorded in `phase3_test.pgn`.

**Phases 4 through 4d (EP-P4 … EP-P4d, up to 2026-03-20).** Iterative deepening, UCI `wtime/btime/movestogo` parsing, MVV-LVA ordering, quiescence search (captures-only + stand-pat), two killer moves per ply, 512-node time-check granularity, delta pruning, history heuristic (4096 entries, depth² increments), and aspiration windows (±50 cp). Also: the GNU COBOL toolchain bug. With `-O2` alone, the compiled binary hung before entering `MAIN-PROGRAM`; after empirical bisection the agent pinned `COB_CFLAGS="-O2 -fwrapv …"` (SB-026). That single flag is the reason any of this runs at all. The first binary snapshot `chess-engine-v1` dates to 2026-03-20 and calibrated at ~1517 Elo (85 % vs SF 1320, 52.5 % vs SF 1500).

**Phases v2, v3, v3b (through 2026-03-23).** Bishop-pair bonus, rook-on-open/semi-open file, pawn structure (doubled -15, isolated -20, passed +10..+90 tapered), Late Move Reductions with a 0/1/2 re-search state machine. v2 reached ~1608 Elo; v3b reached ~1627.

**Phases 6 through 9 (EP-P6 … EP-v4b, through 2026-03-30).** More experiments, more reverts, and the single largest measured gain: v4 added PV-move ordering at the root (previous-iteration best move gets score 20 000) and made the killer + history tables persistent across iterative-deepening iterations. That change alone pushed the engine to 14/20 (70 %) against SF 1500 — ~1647 Elo in one run. v4b tightened LMR to R=2 for move-index ≥ 7 and trimmed 17 % of nodes at depth 5 while holding ~1627 Elo.

The discipline is in the **seven reverts**. Reverse-futility pruning (SB-027), check extensions at the first qsearch ply (SB-033), futility pruning in v3 (SB-037), the aggressive time formula that cost seven forfeits (SB-038), tapered king evaluation (SB-042), horizon check extensions (SB-043), and endgame king correction via phase-switch (SB-047) were all implemented, measured against a 20-game match, observed to regress, and rolled back. Six of the seven produced persistent agent memory notes (`feedback_time_management.md`, `feedback_overhead_sensitivity.md`) that constrained later experiments — notably the v4 redesign which deliberately targeted *zero per-node cost* changes.

Across the arc, roughly fourteen INCR→TEST→RETR cycles produced a documented ladder: **1517 → 1608 → 1627 → 1647**.

## 4. What was actually delivered

The project root at `/Users/mathieuacher/SANDBOX/chess-cobol-cc` contains a single 3 460-line source file (`chess-engine.cob`, 2 920 code lines, 81 paragraphs), sixteen engine binaries (`chess-engine`, `chess-engine-v1` … `chess-engine-v4b`, plus `-dbg/-fast/-noopt/-o1/-os/-o3` variants used for the toolchain bisection), and twenty-five PGN artefacts. The final Elo triangulation (BL-007, prompted `"no refine the Elo assessment"` at event `#3659`) produced `elo_vs1400.pgn`, `elo_vs1600.pgn`, and `elo_vs1700.pgn`, with the 1500-level evidence sitting in `phase9_vs1500.pgn`. Weighted score: SF 1400 at 80 %, SF 1500 at 70 %, SF 1600 at 55 %, SF 1700 at 30 %. Reported central figure: **~1630 Elo over 100 games** (session event `#3713`).

## 5. Validation and the two classes of difficulty

Validation rested on two oracles: perft for move generation (depths 1–4 on startpos, kiwipete, en-passant edge, promotion positions) and `cutechess-cli` PGN matches for playing strength. There are no unit tests in the repo; the PGNs are the test harness.

Two difficulty classes dominated. The first is the GNU COBOL `-O2` hang already mentioned — pure toolchain archaeology, solved by a compiler-flag change with high blast radius. The second is **time-management regressions**, which bit the engine twice. The first (SB-018) was root-move corruption across iterative-deepening iterations, fixed by regenerating the legal moves each iteration. The second and more dramatic (SB-038) was an aggressive `time/movestogo` formula that caused *seven forfeits* in a 20-game match (`phase5_vs1500.pgn`: 3.5/20). The fix was a restored safety buffer and a soft-time check (4× the last iteration's elapsed time). The next match (`phase5b_vs1500.pgn`) scored 13.5/20. The delta — 3.5 to 13.5 out of 20 — is exactly the signal-to-noise the 20-game match harness was built to catch.

## 6. Compute and context footprint

Across a 17-day calendar span the agent spent **~15 h 31 m** of active collaboration time across **3 023 turns**, one session. Peak context was **167 327 tokens** against the 1 M Opus window — 16.7 % utilisation — with median **101 k** and p90 **154 k**. The window never came close to saturating; the five `isCompactSummary` events (2026-03-12, 03-16, 03-20, 03-21, 03-23) reset working memory and preserved the phase-by-phase narrative. Grand total tokens (input + output + cache read + cache create) for the single Claude Code session: **179 251 052** — roughly **$518** at rack rates. Output tokens alone: **591 930** (203 output tokens per COBOL LOC, 11 606 per backlog entry — numbers from `output/cost_metrics.md`).

## 7. Where this sits on the Elo map

~1630 Elo is a solid intermediate club player. It beats casual opponents reliably and loses to strong ones. The engine plays legal, tactically-aware chess with correct castling, en-passant, promotions, stalemate, threefold-repetition, and fifty-move handling; it uses its clock sensibly. It contains techniques standard in engines up to ~2400 Elo: LMR, null-move-style pruning, PVS, aspiration windows, Zobrist-hashed transposition tables, MVV-LVA, killers, history, pawn-structure and king-safety terms. The ceiling above ~1700 is set by the language, not the engineering: no NNUE (needs a linear-algebra runtime), no SMP (GnuCOBOL exposes no threading primitives), no tablebases, no bitboards-without-pointers fast enough to matter. Calling that a failure would be wrong — it is the envelope the tool imposes.

## 8. The surprising part

Two things stand out. First, the fourteen-cycle measured-improvement loop with **seven verified reverts** is rare discipline for an agent working without git history — each change was kept only if a fresh 20-game PGN match outscored the previous binary. Second, the engine caught its own regressions through its own oracle: the tapered king-evaluation experiment (SB-042) was abandoned when `phase6_vs1500.pgn` scored 8/20; the horizon check extension (SB-043) was abandoned at 9/20 in `phase6b_vs1500.pgn`. The agent wrote `feedback_overhead_sensitivity.md` to encode the lesson ("per-node cost dominates textbook gains at this depth") and then deliberately chose the next improvement — PV ordering plus persistent tables — *because* it cost nothing per node. That is not bullet-point capability; that is the shape of a feedback loop.

Honest gaps remain: no git history, no CI, no separate test directory, no NNUE, no SMP, no pondering, and — because this meta-analysis is read-only — no re-executed match to independently confirm the 1630 figure beyond the PGNs on disk. But the claim is checkable: the binary is there, the PGNs are there, the flags are pinned. That is more than most 17-day projects ship.
