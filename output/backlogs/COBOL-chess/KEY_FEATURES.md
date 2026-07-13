# KEY_FEATURES — cobochess (COBOL-chess)

## Preamble

`cobochess` is a Codex-built GnuCOBOL UCI chess engine delivered via a spec-first workflow that produced a 184-entry F-### backlog across 27 phases. The brief: build a playable UCI engine, perft-validate it, and measure Elo against Stockfish through cutechess-cli. A "key feature" here is a coherent group of F-### entries that, taken together, delivers a load-bearing engineering capability at depth ≥ 1 and is not purely scaffold/infra. Because the backlog is unusually fine-grained (e.g. the 0x88 board, piece encoding, castling bitmask, move flags and move record are each a separate F-###), we consolidate by architectural concern: data model, FEN, attack/movegen, make/unmake, search core, search heuristics, TT, eval, UCI+time, perft+tooling, Elo harness, macOS build hardening.

## Ranked table

| rank | F-range (group) | title | class | depth | effort | score | evidence |
|---:|---|---|---|---:|---:|---:|---|
| 1 | F-100..F-110, F-220..F-222, F-230..F-232, F-240..F-241, F-290..F-299 | Search core + classical heuristic stack (iterative deepening, negamax α-β, quiescence + stand-pat + delta, PVS, aspiration, NMP, LMR, LMP, mate-distance pruning, 50-move + threefold draws) | ALG (+PRF) | 3 | 3 | 7.5 | `src/search.cob:134–1362`, 10-phase Elo ladder ~675→~1635 |
| 2 | F-180..F-187, F-298..F-299 | Move-ordering stack: PST-aware root scoring, MVV-LVA, 2-slot killers/ply, 16 384-entry history with depth² bonus + aging, selection-sort pick-best at every layer | ALG (+PRF) | 3 | 2 | 6.0 | `copybooks/searchstate.cpy:9–19`, `src/search.cob:282–406, 912–1078`; Phase-15 Elo 1129→1589 |
| 3 | F-200..F-212 | Zobrist hashing + 1 M-entry transposition table: LCG-seeded keys across `EXTERNAL` singleton copybook, incremental update in MAKEMOVE, exact/lower/upper probe, mate-score ply normalization, depth-preferred replacement (F-290/F-291), TT move re-inserted into ordering | ALG+LNG | 3 | 2 | 6.0 | `copybooks/hash.cpy`, `src/fen.cob:199–244`, `src/makemove.cob:91–278`, `src/search.cob:624–665, 1080–1104`; Phase-16 Elo 1511→1635 |
| 4 | F-040..F-059, F-060..F-074 | Pseudo-legal movegen + make/unmake engine: 0x88 ray/step dispatch, en-passant, 4-way promotions, full castling legality (rights + path empty + rook present + no attacked transit + not in check), undo-stack make/unmake with legality filtering via ATTACK | DOM (+ALG) | 3 | 2 | 6.0 | `src/movegen.cob:42–472`, `src/makemove.cob:73–615`, `src/attack.cob:1–164` |
| 5 | F-250..F-255, F-260..F-264, F-270..F-276, F-280..F-281, F-090..F-092 | Classical static evaluation (material + PSTs + doubled/isolated/passed pawns + rook 7th / open-file / semi-open / knight-bishop centralization + NPM-gated middlegame vs endgame king terms + pawn shield + bishop pair + tempo) | DOM | 2 | 3 | 5.0 | `src/eval.cob:64–385` (387 LOC total) |
| 6 | F-120..F-134, F-140..F-141, F-300..F-308, F-170 | UCI protocol surface + time management: full command loop, `position startpos/fen moves …`, `go depth/movetime/wtime+btime+winc+binc+movestogo`, CLI perft modes, centisecond timer, side-aware clock, movestogo estimation [10,60], 50 ms overhead, 20% cap, 20 ms floor; the 512→4096 input buffer fix alone moved Elo 675→1129 | PRO (+DOM) | 2 | 2 | 4.0 | `src/main.cob:85–379`, `src/time.cob:1–49`, `src/uci.cob:1–62` |
| 7 | F-010..F-019 | Board & data model (0x88 mailbox, piece/color constants, castling bitmask, move-flag bitmask, explicit MOVE-REC / MOVE-LIST / GAME-STATE / 256-entry undo stack, offset tables) | DOM (+LNG) | 2 | 2 | 4.0 | `copybooks/constants.cpy`, `copybooks/types.cpy`, `copybooks/offsets.cpy`, `src/board.cob` |
| 8 | F-020..F-027 | FEN parser (`UNSTRING … DELIMITED BY SPACE` 6-field decode, rank-by-rank piece placement, castling mask, EP square, NUMVAL clocks, king-square detection, error status) with Zobrist key computation on load | DOM | 2 | 1 | 3.0 | `src/fen.cob:49–244` |
| 9 | F-080..F-081, F-109..F-110 | Perft + recursive subprograms in COBOL: `PROGRAM-ID. PERFT/ALPHABETA/QUIESCE RECURSIVE` with `LOCAL-STORAGE SECTION` per-frame move-list — the language hack that makes the whole search tree possible | LNG (+VER) | 3 | 1 | 4.5 | `src/perft.cob:1–66`, `src/search.cob:410ff, 1108ff` |
| 10 | F-150..F-155, F-160..F-161, F-310 | Measurement & verification harness: 4-position / depth-5 perft-case JSON + Python checker, UCI smoke, 100-game PGN opening book, `cutechess-cli` runner with Stockfish Elo/Skill modes, PGN-parsing Elo calculator with 95% Wilson CI, W/D/L-perspective bugfix | VER (+SYS+PRO) | 3 | 2 | 6.0 | `tools/perft_check.py`, `tools/uci_smoke.sh`, `tools/elo_run.py`, `tools/elo_calc.py`, `tests/perft_cases.json`, `openings/book.pgn` |
| 11 | F-320..F-328, F-001..F-004 | macOS build hardening + scaffold: Makefile with `cobc` targets, ad-hoc codesigning, xattr de-quarantine, Apple-toolchain PATH prefix to keep GNU `strip` from corrupting Mach-O, `-target arm64-apple-macosx`+SDK flags, `.NOTPARALLEL`, `engine_check.py` diagnostic, 5-attempt build-retry loop | INF (+SYS) | 2 | 2 | 4.0 | `Makefile:17–94`, `tools/engine_check.py:1–132` |

Significance notes:

1. **Search core** — Textbook negamax α-β would be depth 2, but the group includes NMP-with-zugzwang-hedge, LMR with re-search, PVS, aspiration with fail re-search, mate-distance pruning and draw detection; each tuned on a measured Elo ladder. This is performance engineering in a language where `PERFORM THRU` recursion is non-trivial.
2. **Move ordering** — Not just "sort by captures". The stack is the canonical modern set (TT/PV/promo/MVV-LVA/killers/history) with aging and per-layer selection sort. Empirically worth ~460 Elo in one phase.
3. **Zobrist + TT** — Significance comes from crossing the COBOL boundary: the `EXTERNAL` copybook turns Zobrist tables into a shared singleton across separately-compiled programs, the incremental update threads through every branch of MAKEMOVE, and mate-score normalization + depth-preferred replacement are implemented correctly.
4. **Movegen + make/unmake** — This is domain, not algorithm: the chess rules (castling-through-check, EP, promotion on push *and* capture, halfmove/fullmove bookkeeping, king-square caching) are faithfully encoded and legality is the make/unmake/ATTACK composition rather than pin logic in the generator.
5. **Evaluation** — Deliberately classical; depth stays at 2 because no mobility / SEE / pawn hash, but the effort budget is high (four phases, 387 LOC) and each term is individually justified.
6. **UCI + time** — Standard-compliance work. The depth-2 label is for the wtime/btime/winc/binc/movestogo allocation formula and the retrospectively obvious but empirically huge `PIC X(512)→X(4096)` fix (+454 Elo on its own).
7. **Board & data model** — Not an algorithm but the shape everything else hangs on; the explicit-record move encoding is a deliberate readability-vs-speed tradeoff for COBOL.
8. **FEN** — A standard format parser; significance is that it also seeds the incremental Zobrist key, so downstream TT probing actually works from any position.
9. **Recursive subprograms** — Small LOC, disproportionate language significance: GnuCOBOL requires `RECURSIVE` + `LOCAL-STORAGE` to make perft, α-β and quiescence re-entrant, and getting this right is the enabling trick for every deeper feature.
10. **Measurement harness** — The reason this project can claim an Elo at all. It is pure composition: perft validates movegen → UCI smoke validates protocol → cutechess-cli runner + Elo calculator validate playing strength. Wilson CI + W/D/L-perspective bugfix show statistical care.
11. **macOS hardening** — Confirms this is not a toy: a full phase was spent diagnosing SIGKILL on stripped Mach-O binaries and defending the build against it with retries and diagnostics. Pure infrastructure, but non-trivial.

## Composition chains

1. **Correctness chain** — Board & data model (F-010..F-019) → FEN parser (F-020..F-027) → attack detection (F-030..F-036) → movegen + make/unmake (F-040..F-074) → perft + recursive subprograms (F-080..F-081) → perft JSON cases + checker (F-150..F-151). Emergent capability: every later move-generator change is regression-checked against Kiwipete/EP/promotion positions to depth 5, and no further engineering is valid until this chain passes.
2. **Search chain** — Material-only eval (F-090..F-092) → α-β + quiescence + ID (F-100..F-110) → move ordering + PST (F-180..F-187) → Zobrist + TT (F-200..F-212) → LMR / NMP / PVS / aspiration / LMP / mate-distance (F-220..F-241) → TT replacement + draws + delta + time-check (F-290..F-299). Emergent capability: each new technique is worth only ~50–200 Elo individually, but composed on top of a correct TT they stack to take the engine from ~675 to ~1635 Elo.
3. **Playable-engine chain** — Search chain → UCI loop + `position`/`go` (F-120..F-134) → 4 K input buffer fix (F-170) → time management formula (F-300..F-308) → move-to-UCI string (F-130). Emergent capability: the engine becomes something `cutechess-cli` can actually talk to under real clock controls — without F-170 alone the engine forfeited on long opening lines.
4. **Measurement chain** — Playable-engine chain → PGN opening book (F-310) → `elo_run.py` cutechess driver (F-153) → Stockfish Elo/Skill introspection → PGN parser + Elo/Wilson calculator (F-154, F-160/161) → macOS build hardening (F-320..F-328) so the binary survives launch from Python. Emergent capability: reproducible Elo claims of ~1600–1700 against a calibrated opponent, not a vibe-check.

## Significance profile

| Class | Count in top 11 (primary) | Secondary tags |
|---|---:|---:|
| ALG | 2 | +1 |
| DOM | 3 | +1 |
| SYS | 0 | +2 |
| INF | 1 | 0 |
| PRO | 1 | +1 |
| LNG | 1 | +2 |
| VER | 1 | +1 |
| PRF | 0 | +2 |
| CMP | 0 | 0 |

Centre of gravity: ALG + DOM dominate the primaries (5/11), with a strong LNG/VER/PRF secondary cloud and a real INF presence from the macOS build phase. No primary SYS or CMP — the engine stays in-process, and the Elo harness is the closest thing to an emergent-composition feature (tagged VER+SYS).

## Verdict

**Hybrid: algorithm-centric with serious domain-modelling and verification backbone, plus a LNG accent from COBOL-specific recursion tricks** — a thorough, by-the-book chess engine where the sophistication lives in composing a 1 000-line search module on top of correctly-encoded chess rules and a reproducible Elo measurement harness, rather than in any single novel algorithm.
