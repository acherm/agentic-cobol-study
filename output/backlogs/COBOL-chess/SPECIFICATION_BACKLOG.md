# cobochess — Implementation Feature Backlog

This backlog enumerates every distinct feature implemented by the agent, organized chronologically by implementation phase. Each feature is traced to the source code where it resides in the final codebase.

---

## Phase 1: Project Scaffold
*Feb 9, 10:28–10:32 · [T:019c41c7:lines_200–250]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-001 | Directory structure (`src/`, `copybooks/`, `tools/`, `tests/`, `openings/`, `bin/`, `results/`) | repo layout |
| F-002 | Makefile with `cobc` build, `perft`, `uci-smoke`, `clean`, `rebuild` targets | `Makefile:1–105` |
| F-003 | `.gitignore` for binaries, results, caches | `.gitignore` |
| F-004 | `README.md` with build/test/usage docs | `README.md` |

---

## Phase 2: Core Engine — Board & Data Model
*Feb 9, 10:32–10:45 · [T:019c41c7:lines_250–500]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-010 | 0x88 mailbox board representation (128-element array, off-board detection via `MOD(sq,16) <= 7`) | `copybooks/types.cpy:3–4` |
| F-011 | Piece encoding (EMPTY=0, WP=1..BK=12), color constants (WHITE=0, BLACK=1) | `copybooks/constants.cpy:5–17` |
| F-012 | Castling bitmask encoding (WK=1, WQ=2, BK=4, BQ=8) | `copybooks/constants.cpy:19–22` |
| F-013 | Move flag bitmask (CAPTURE=1, EP=2, CASTLE=4, PROMOTION=8, PAWN-DOUBLE=16) | `copybooks/constants.cpy:24–28` |
| F-014 | Move record structure (from, to, promo, flags, score) | `copybooks/types.cpy:26–31` |
| F-015 | Move list (count + 256-entry array) | `copybooks/types.cpy:33–35` |
| F-016 | Game state structure: board, side, castling, EP sq, halfmove, fullmove, king sqs, ply, Zobrist key | `copybooks/types.cpy:1–13` |
| F-017 | Undo stack: 256-entry stack with captured/moved piece, castling, EP, halfmove, fullmove, king sq, key | `copybooks/types.cpy:14–23` |
| F-018 | Movement offset tables: knight (8), king (8), bishop (4), rook (4); runtime-initialized | `copybooks/offsets.cpy:1–6` |
| F-019 | Board initialization: clear all squares to EMPTY, reset state | `src/board.cob:1–30` |

---

## Phase 3: Core Engine — FEN Parsing
*Feb 9, 10:45–10:48*

| ID | Feature | Evidence |
|----|---------|----------|
| F-020 | FEN string parsing via `UNSTRING ... DELIMITED BY SPACE` (6 fields) | `src/fen.cob:49–51` |
| F-021 | Piece placement: rank-by-rank traversal, char-to-piece mapping (12 types) | `src/fen.cob:58–96` |
| F-022 | Side-to-move parsing (`w`/`b`) | `src/fen.cob:98–108` |
| F-023 | Castling rights parsing (`KQkq` → bitmask, `-` for none) | `src/fen.cob:110–127` |
| F-024 | En passant square parsing (algebraic → 0x88 index) | `src/fen.cob:129–156` |
| F-025 | Halfmove/fullmove clock parsing via `NUMVAL` | `src/fen.cob:158–160` |
| F-026 | King square detection during placement | `src/fen.cob:88–93` |
| F-027 | FEN validation with error status return | `src/fen.cob:53–56, 77–84` |

---

## Phase 4: Core Engine — Attack Detection
*Feb 9, 10:48–10:50*

| ID | Feature | Evidence |
|----|---------|----------|
| F-030 | Square-attacked-by-side query | `src/attack.cob:1–164` |
| F-031 | Pawn attack detection (white/black pawn diagonal offsets) | `src/attack.cob:65–95` |
| F-032 | Knight attack detection (8 offsets) | `src/attack.cob:97–110` |
| F-033 | King attack detection (8 offsets) | `src/attack.cob:112–125` |
| F-034 | Bishop/queen diagonal ray attack detection | `src/attack.cob:127–142` |
| F-035 | Rook/queen orthogonal ray attack detection | `src/attack.cob:144–159` |
| F-036 | 0x88 off-board check for ray/step moves | `src/attack.cob:100, 115, 131, 148` |

---

## Phase 5: Core Engine — Move Generation
*Feb 9, 10:50–10:55*

| ID | Feature | Evidence |
|----|---------|----------|
| F-040 | Full legal move generator (iterates 0x88 board, dispatches by piece) | `src/movegen.cob:42–55` |
| F-041 | White pawn single push (+16 to empty) | `src/movegen.cob:104–105, 123–146` |
| F-042 | Black pawn single push (-16 to empty) | `src/movegen.cob:117–118, 148–171` |
| F-043 | White pawn double push (+32 from rank 1, both squares empty) | `src/movegen.cob:134–141` |
| F-044 | Black pawn double push (-32 from rank 6) | `src/movegen.cob:159–166` |
| F-045 | Pawn captures (diagonal, enemy piece or EP square) | `src/movegen.cob:96–99, 109–112, 173–217` |
| F-046 | En passant capture (detect `TO-SQ = GS-EP-SQ`, flag EP+CAPTURE) | `src/movegen.cob:175–178, 198–201` |
| F-047 | Pawn promotion (all 4 pieces: Q/R/B/N) on push and capture | `src/movegen.cob:415–429` |
| F-048 | Promotion pushes included in captures-only mode (quiescence) | `src/movegen.cob:103, 116` |
| F-049 | Knight moves (8 step offsets) | `src/movegen.cob:219–224, 443–450` |
| F-050 | Bishop moves (4 sliding directions) | `src/movegen.cob:226–231, 461–464` |
| F-051 | Rook moves (4 sliding directions) | `src/movegen.cob:233–238, 466–469` |
| F-052 | Queen moves (union of bishop + rook directions) | `src/movegen.cob:240–249` |
| F-053 | King moves (8 step offsets) | `src/movegen.cob:251–255, 452–459` |
| F-054 | Sliding piece ray traversal (continue until off-board or blocked; capture blocker) | `src/movegen.cob:290–319` |
| F-055 | Castling: White king-side (e1g1), queen-side (e1c1) | `src/movegen.cob:328–365` |
| F-056 | Castling: Black king-side (e8g8), queen-side (e8c8) | `src/movegen.cob:372–409` |
| F-057 | Castling legality: empty path, rook present, no attacked squares | `src/movegen.cob:330–345, 347–365, 374–389, 391–409` |
| F-058 | Castling suppressed in captures-only mode | `src/movegen.cob:257–259` |
| F-059 | Captures-only mode for quiescence search | `src/movegen.cob:267, 296` |

---

## Phase 6: Core Engine — Make/Unmake Move
*Feb 9, 10:50–10:55*

| ID | Feature | Evidence |
|----|---------|----------|
| F-060 | Make move: save full undo state to stack | `src/makemove.cob:73–85` |
| F-061 | Flag decoding (bitmask → EP, CASTLE, PROMOTION, PAWN-DOUBLE) | `src/makemove.cob:335–345` |
| F-062 | En passant execution: remove captured pawn behind target | `src/makemove.cob:119–136` |
| F-063 | Castling rook movement (4 types: h1→f1, a1→d1, h8→f8, a8→d8) | `src/makemove.cob:138–171, 368–397` |
| F-064 | Promotion execution: replace pawn with promoted piece | `src/makemove.cob:173–221, 347–366` |
| F-065 | Castling rights update on king move | `src/makemove.cob:399–406, 445–453` |
| F-066 | Castling rights update on rook move/capture | `src/makemove.cob:408–442` |
| F-067 | Halfmove clock: reset on pawn/capture, increment otherwise | `src/makemove.cob:183–196` |
| F-068 | EP square set on double pawn push | `src/makemove.cob:239–246` |
| F-069 | Fullmove increment after Black's move | `src/makemove.cob:248–251` |
| F-070 | Side toggle + ply increment | `src/makemove.cob:253–255` |
| F-071 | King square tracking | `src/makemove.cob:228–234` |
| F-072 | Legality check: call ATTACK on own king; undo if in check | `src/makemove.cob:280–294` |
| F-073 | Unmake move: full state restore from undo stack | `src/makemove.cob:529–581` |
| F-074 | Unmake: EP capture undo, castling rook undo | `src/makemove.cob:557–613` |

---

## Phase 7: Core Engine — Perft
*Feb 9, 10:50–10:55*

| ID | Feature | Evidence |
|----|---------|----------|
| F-080 | Recursive perft node counter (`PROGRAM-ID. PERFT RECURSIVE`) | `src/perft.cob:1–66` |
| F-081 | `LOCAL-STORAGE SECTION` for per-frame move data (recursion-safe) | `src/perft.cob:24–41` |

---

## Phase 8: Core Engine — Initial Evaluation
*Feb 9, 10:50–10:55 (material-only baseline)*

| ID | Feature | Evidence |
|----|---------|----------|
| F-090 | Material values: P=100, N=320, B=330, R=500, Q=900 | `src/eval.cob:115–122` |
| F-091 | Side-relative scoring (negate for Black) | `src/eval.cob:379–383` |
| F-092 | 0x88 board traversal with off-board skip | `src/eval.cob:72–73, 103–104` |

---

## Phase 9: Core Engine — Initial Search
*Feb 9, 10:50–10:55*

| ID | Feature | Evidence |
|----|---------|----------|
| F-100 | Iterative deepening (depth 1 to max) | `src/search.cob:134` |
| F-101 | Basic alpha-beta (negamax framework) | `src/search.cob:540, 758–764` |
| F-102 | Quiescence search (captures + promotions only, recursive) | `src/search.cob:1108–1362` |
| F-103 | Stand-pat evaluation in quiescence | `src/search.cob:1198–1205` |
| F-104 | Checkmate detection (legal count = 0, in check) | `src/search.cob:837–839` |
| F-105 | Stalemate detection (legal count = 0, not in check) | `src/search.cob:840–842` |
| F-106 | Root move generation + PV output | `src/search.cob:216–217, 192–201` |
| F-107 | UCI `info depth ... nodes ... score cp ... pv ...` output | `src/search.cob:192–201` |
| F-108 | Node counting (`SS-NODES`) | `src/search.cob:113, 546` |
| F-109 | `PROGRAM-ID. ALPHABETA RECURSIVE` + `LOCAL-STORAGE` | `src/search.cob:410 ff.` |
| F-110 | `PROGRAM-ID. QUIESCE RECURSIVE` + `LOCAL-STORAGE` | `src/search.cob:1108 ff.` |

---

## Phase 10: Core Engine — UCI Protocol
*Feb 9, 10:50–10:55*

| ID | Feature | Evidence |
|----|---------|----------|
| F-120 | UCI command loop (`ACCEPT IN-LINE`, dispatch by keyword) | `src/main.cob:119–146` |
| F-121 | `uci` → id + options + `uciok` | `src/main.cob:123–131` |
| F-122 | `isready` → `readyok` | `src/main.cob:132–133` |
| F-123 | `ucinewgame` → reset heuristics | `src/main.cob:134–138` |
| F-124 | `position startpos [moves ...]` | `src/main.cob:139–140, 154–180` |
| F-125 | `position fen <fen> [moves ...]` | `src/main.cob:182–238` |
| F-126 | `go depth <N>` (fixed depth) | `src/main.cob:308–310` |
| F-127 | `go movetime <ms>` (fixed time) | `src/main.cob:311–314` |
| F-128 | `stop`, `quit` | `src/main.cob:143–146` |
| F-129 | `bestmove <uci-move>` output after search | `src/main.cob:339–340` |
| F-130 | Move-to-UCI string conversion (e.g. `e2e4`, `a7a8q`) | `src/uci.cob:1–62` |
| F-131 | Move application from UCI notation (generate all legal, match string, apply) | `src/main.cob:269–289` |
| F-132 | Token parser for input lines (whitespace-delimited, up to 4096 chars) | `src/main.cob:249–267` |
| F-133 | `--perft-startpos <depth>` CLI mode | `src/main.cob:85–97` |
| F-134 | `--perft <fen> <depth>` CLI mode | `src/main.cob:99–111` |

---

## Phase 11: Core Engine — Time Utility
*Feb 9, 10:50–10:55*

| ID | Feature | Evidence |
|----|---------|----------|
| F-140 | Wall-clock time in centiseconds via `ACCEPT FROM DATE/TIME` + `INTEGER-OF-DATE` | `src/time.cob:1–49` |
| F-141 | Date-to-days caching for performance | `src/time.cob:19–24` |

---

## Phase 12: Test Suite & Tooling (initial)
*Feb 9, 10:32 (same batch as scaffold)*

| ID | Feature | Evidence |
|----|---------|----------|
| F-150 | Perft test cases: 4 positions (startpos, kiwipete, EP-edge, promotions), depths 1–5 | `tests/perft_cases.json` |
| F-151 | Perft checker script: runs `cobochess --perft`, compares node counts | `tools/perft_check.py` |
| F-152 | UCI smoke test: sends `uci/isready/position/go depth 3/quit`, verifies responses | `tools/uci_smoke.sh` |
| F-153 | Elo match runner: orchestrates cutechess-cli with Stockfish strength configs, TC, books | `tools/elo_run.py` |
| F-154 | Elo calculator: PGN parser, Elo estimate with 95% Wilson CI | `tools/elo_calc.py` |
| F-155 | Opening book (EPD format, 4 entries from startpos) | `openings/book.epd` |

---

## Phase 13: Elo Calc Bug Fixes
*Feb 9, 12:42–18:47 · [T:019c41c7:lines_865–987]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-160 | Fix regex character range in PGN result parsing | `tools/elo_calc.py` |
| F-161 | Per-game White/Black perspective tracking for correct W/D/L attribution | `tools/elo_calc.py` |

---

## Phase 14: UCI Buffer Fix
*Feb 9, 19:08–19:30 · [T:019c41c7:lines_~1100–1400]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-170 | UCI input line buffer enlarged from `PIC X(512)` to `PIC X(4096)` | `src/main.cob:25` |

*Impact: eliminated "illegal move" forfeits caused by truncated long `position ... moves ...` strings. Elo jumped from ~675 to ~1129.*

---

## Phase 15: Search Improvements — Move Ordering & Extensions
*Feb 9, 20:02–20:14 · [T:019c41c7:lines_~1700–2050]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-180 | Piece-square tables in eval (knight/bishop centralization, pawn advancement with file preference, queen mild centralization) | `src/eval.cob:161–166, 207–211, 234–236` |
| F-181 | MVV-LVA capture ordering: `100000 + victim×10 − attacker` | `src/search.cob:282–371, 912–1009` |
| F-182 | Killer moves: 2 slots per ply (256 plies), +90000/+80000 ordering bonus | `copybooks/searchstate.cpy:9–18`, `src/search.cob:993–999, 1046–1070` |
| F-183 | History heuristic: 16384-entry table (from×128+to), depth² bonus on cutoff, halving on overflow | `copybooks/searchstate.cpy:19`, `src/search.cob:1001–1002, 1072–1078` |
| F-184 | In-check extensions: +1 ply when side-to-move king is in check | `src/search.cob:608–611` |
| F-185 | Root promotion bonus (+80000 + piece value) | `src/search.cob:305–316` |
| F-186 | Root castling bonus (+500) | `src/search.cob:318–321` |
| F-187 | Selection sort (pick-best) for move ordering at root, inner nodes, and quiescence | `src/search.cob:373–406, 1011–1024, 1327–1360` |

*Impact: Elo rose from ~1129 to ~1589 (vs SF@1320).*

---

## Phase 16: Zobrist Hashing & Transposition Table
*Feb 10, 10:22–10:39 · [T:019c41c7:lines_~2100–3500]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-200 | Zobrist hash tables (EXTERNAL shared singleton across compilation units) | `copybooks/hash.cpy:6` |
| F-201 | LCG PRNG for hash key generation (multiplier=1103515245, increment=12345, modulus=2³¹−1) | `copybooks/hash.cpy:2–4`, `src/fen.cob:199–205` |
| F-202 | Piece-square keys: 12 pieces × 128 squares | `copybooks/hash.cpy:9–10` |
| F-203 | Side-to-move key | `copybooks/hash.cpy:11` |
| F-204 | Castling combination keys (16 values) | `copybooks/hash.cpy:12` |
| F-205 | En passant file keys (8 values) | `copybooks/hash.cpy:13` |
| F-206 | Full Zobrist hash computation from position (in FEN parser) | `src/fen.cob:207–244` |
| F-207 | Incremental Zobrist update in MAKEMOVE (pieces, side, castling, EP) | `src/makemove.cob:91–278` |
| F-208 | Transposition table: 1,048,576 entries (key, depth, flag, score, best move) | `copybooks/searchstate.cpy:20–29`, `copybooks/constants.cpy:42` |
| F-209 | TT probing: indexed by `MOD(GS-KEY, TT-SIZE) + 1` | `src/search.cob:624–665` |
| F-210 | TT cutoff: exact match returns immediately; lower bound ≥ beta; upper bound ≤ alpha | `src/search.cob:645–663` |
| F-211 | TT move extraction for ordering (priority +95000) | `src/search.cob:625–632, 925–930` |
| F-212 | TT mate score normalization (adjust relative to current ply on probe/store) | `src/search.cob:636–643, 1089–1097` |

*Impact: Elo rose from ~1511 to ~1635 (vs SF@1600).*

---

## Phase 17: Late Move Reductions & Null-Move Pruning
*Feb 10, 12:37–13:18 · [T:019c41c7:lines_~5500–5800]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-220 | Late Move Reductions (LMR): reduce by 1 for quiet moves at depth ≥ 3, legal count ≥ 4; reduce by 2 at depth ≥ 6, legal count ≥ 10; re-search at full depth on fail-high | `src/search.cob:767–796` |
| F-221 | Null-move pruning (NMP): R=3 reduction, requires depth ≥ 4, not in check, non-pawn material present; beta cutoff if null-move score ≥ beta | `src/search.cob:667–705` |
| F-222 | Null-move Zobrist update: toggle side, clear EP, adjust hash key | `src/search.cob:866–910` |

*Impact: Elo reached ~1628 (vs SF@1600, 50 games).*

---

## Phase 18: Aspiration Windows & PVS
*Feb 10, 17:39–18:07 · [T:019c41c7:lines_~5408–6306]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-230 | Aspiration windows: for depth ≥ 3, initial ±50 around previous score; re-search with full window on fail | `src/search.cob:142–161` |
| F-231 | Principal Variation Search (PVS): first move full window, rest null window, re-search on fail-high (root + inner) | `src/search.cob:241–260, 758–805` |
| F-232 | PV move from previous iteration seeded into next iteration | `src/search.cob:135–139` |

---

## Phase 19: Late Move Pruning & Mate Distance Pruning
*Feb 10, 17:39–18:07*

| ID | Feature | Evidence |
|----|---------|----------|
| F-240 | Late Move Pruning (LMP): skip quiet moves at depth ≤ 2 when legal count ≥ 12 (depth 1) or ≥ 20 (depth 2) | `src/search.cob:739–750` |
| F-241 | Mate distance pruning: tighten alpha/beta bounds based on `MATE-SCORE ± GS-PLY` | `src/search.cob:582–594` |

---

## Phase 20: Evaluation Rewrite — Pawn Structure
*Feb 10, 18:38–20:55 · [T:019c41c7:lines_~6400–9500]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-250 | Pawn file count precomputation (`WPC`/`BPC` arrays per file) | `src/eval.cob:64–89` |
| F-251 | Pawn rank tracking (`WPMIN`/`BPMAX` per file) for passed pawn detection | `src/eval.cob:68–69, 82–85` |
| F-252 | Doubled pawn penalty: −8 cp per extra pawn on same file | `src/eval.cob:91–101` |
| F-253 | Isolated pawn penalty: −10 cp if no friendly pawn on adjacent files | `src/eval.cob:168–187` |
| F-254 | Passed pawn bonus: +10 + `rank × 8` if no enemy pawn ahead on same/adjacent files | `src/eval.cob:189–205` |
| F-255 | Pawn piece-square heuristic: advancement reward + central file bonus | `src/eval.cob:161–166` |

---

## Phase 21: Evaluation Rewrite — Piece Placement
*Feb 10, 18:38–20:55*

| ID | Feature | Evidence |
|----|---------|----------|
| F-260 | Knight centralization: `24 − (manhattan_dist × 6)` | `src/eval.cob:207–208` |
| F-261 | Bishop centralization: `16 − (manhattan_dist × 4)` | `src/eval.cob:209–211` |
| F-262 | Queen mild centralization: `5 − (manhattan_dist × 2)` | `src/eval.cob:234–236` |
| F-263 | Rook on 7th rank bonus: +20 cp | `src/eval.cob:213–215` |
| F-264 | Rook on open file: +12 cp (no pawns), semi-open file: +6 cp (no friendly pawn) | `src/eval.cob:216–233` |

---

## Phase 22: Evaluation Rewrite — King Safety
*Feb 10, 18:38–20:55*

| ID | Feature | Evidence |
|----|---------|----------|
| F-270 | Non-pawn material (NPM) tracking for game phase detection | `src/eval.cob:124–127` |
| F-271 | Endgame detection: `NPM-TOTAL ≤ 2600` | `src/eval.cob:252–254` |
| F-272 | King piece-square (middlegame): encourages edge placement `(dist × 5) − 20` | `src/eval.cob:274–276, 297–298` |
| F-273 | King piece-square (endgame): encourages centralization `20 − (dist × 5)` | `src/eval.cob:272–273, 295–296` |
| F-274 | White king pawn shield: +6 per friendly pawn on 3 forward squares, −6 per missing | `src/eval.cob:303–334` |
| F-275 | Black king pawn shield | `src/eval.cob:336–365` |
| F-276 | Pawn shield disabled in endgame | `src/eval.cob:304` |

---

## Phase 23: Evaluation Rewrite — Misc Terms
*Feb 10, 18:38–20:55*

| ID | Feature | Evidence |
|----|---------|----------|
| F-280 | Bishop pair bonus: +30 cp for having 2+ bishops | `src/eval.cob:368–370` |
| F-281 | Tempo bonus: +10 cp for the side to move | `src/eval.cob:372–377` |

---

## Phase 24: Search Refinements
*Feb 10, 21:00–21:32 · [T:019c41c7:lines_~9500–10000]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-290 | TT replacement policy: depth-preferred (replace only if new depth ≥ stored depth or different key) | `src/search.cob:1080–1104` |
| F-291 | TT flag determination: EXACT (alpha improved, < beta), LOWER (beta cutoff), UPPER (no improvement) | `src/search.cob:850–860` |
| F-292 | Threefold repetition detection: scan undo stack keys within reversible window, draw on 2 hits | `src/search.cob:566–580` |
| F-293 | 50-move rule draw: return 0 if `GS-HALFMOVE ≥ 100` | `src/search.cob:561–564` |
| F-294 | Delta pruning in quiescence: prune if `standpat + 950 < alpha` | `src/search.cob:1207–1211` |
| F-295 | Quiescence MVV-LVA + promotion scoring | `src/search.cob:1257–1325` |
| F-296 | Time check with countdown: every 2048 nodes, call TIMEUTIL, compare elapsed vs limit | `src/search.cob:547–558, 1183–1196` |
| F-297 | Time abort at root: retain previous iteration's best move/score | `src/search.cob:163–171` |
| F-298 | Killer move update on beta cutoff: promote to slot 1, demote old to slot 2 | `src/search.cob:1046–1070` |
| F-299 | History heuristic update on cutoff: depth² bonus, halved on overflow (aging) | `src/search.cob:1072–1078` |

---

## Phase 25: Time Management (advanced)
*Feb 10, 21:00–21:32*

| ID | Feature | Evidence |
|----|---------|----------|
| F-300 | `go wtime/btime/winc/binc/movestogo` support | `src/main.cob:315–327` |
| F-301 | Side-aware clock selection (pick wtime/winc or btime/binc based on side-to-move) | `src/main.cob:344–350` |
| F-302 | Moves-to-go estimation: default 22, clamped [10, 60] | `src/main.cob:352–355` |
| F-303 | Overhead subtraction: 50ms safety margin | `src/main.cob:358–360` |
| F-304 | Time allocation formula: `(safe_remaining / movestogo) + (increment × 0.8)` | `src/main.cob:362` |
| F-305 | Time cap: think time ≤ 20% of remaining | `src/main.cob:363–364` |
| F-306 | Minimum think time: floor of 20ms | `src/main.cob:366–372` |
| F-307 | Final safety clamp: think ≤ remaining | `src/main.cob:374` |
| F-308 | Centisecond conversion with minimum 1 cs | `src/main.cob:376–379` |

---

## Phase 26: Opening Book (PGN format)
*Feb 10 · [T:019c41c7]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-310 | PGN-format opening book for cutechess-cli diversification (100 games from standard openings) | `openings/book.pgn` |

---

## Phase 27: macOS Build System Hardening
*Feb 10, 22:16 – Feb 11, 10:59 · [T:019c41c7:lines_10013–13400]*

| ID | Feature | Evidence |
|----|---------|----------|
| F-320 | macOS ad-hoc code signing (`codesign -s - -f`) via `make sign` target | `Makefile:75–78` |
| F-321 | macOS quarantine xattr clearing (`xattr -dr com.apple.quarantine/provenance`) via `make unquarantine` | `Makefile:80–94` |
| F-322 | Engine health check: `tools/engine_check.py` — runs `--perft-startpos 1`, checks for SIGKILL, prints macOS diagnostics (Mach-O magic, otool, codesign, xattr, strip version) | `tools/engine_check.py:1–132` |
| F-323 | Build retry loop: up to 5 attempts with `engine_check.py` validation between rebuilds | `Makefile:57–66` |
| F-324 | Force Apple toolchain PATH prefix: `PATH="/usr/bin:/bin:/usr/sbin:/sbin:$$PATH"` before `cobc` invocation (prevents GNU `strip` from corrupting Mach-O) | `Makefile:73` |
| F-325 | macOS-specific compiler flags: `-target arm64-apple-macosx`, `-isysroot $(MACOS_SDK)`, `-Wl,-adhoc_codesign` | `Makefile:17–24` |
| F-326 | `.NOTPARALLEL:` + explicit `clean → build` ordering to prevent build races | `Makefile:29–37` |
| F-327 | Quarantine/codesign workarounds in tool scripts (`perft_check.py`, `uci_smoke.sh`, `elo_run.py`) | `tools/perft_check.py`, `tools/uci_smoke.sh`, `tools/elo_run.py` |
| F-328 | Hash UCI option declaration (`option name Hash type spin default 16 min 1 max 1024`) | `src/main.cob:126` |

---

## Summary Statistics

| Phase | Feature Count | Key Outcome |
|-------|--------------|-------------|
| 1–4: Scaffold + data model | 23 (F-001–F-019) | Project structure + 0x88 board |
| 5: FEN parsing | 8 (F-020–F-027) | Load any chess position |
| 6: Attack detection | 7 (F-030–F-036) | Square-attacked queries |
| 7: Move generation | 20 (F-040–F-059) | Full legal move gen + castling + EP + promotions |
| 8: Make/unmake | 15 (F-060–F-074) | Reversible move application |
| 9: Perft | 2 (F-080–F-081) | Recursive node counter |
| 10: Initial eval | 3 (F-090–F-092) | Material-only baseline |
| 11: Initial search | 11 (F-100–F-110) | Alpha-beta + quiescence |
| 12: UCI protocol | 15 (F-120–F-134) | Full UCI interface + CLI perft |
| 13: Time utility | 2 (F-140–F-141) | Wall-clock centiseconds |
| 14: Test suite + tooling | 6 (F-150–F-155) | Perft suite, Elo harness, opening book |
| 15: Elo calc bugfixes | 2 (F-160–F-161) | Correct W/D/L tracking |
| 16: UCI buffer fix | 1 (F-170) | ~675 → ~1129 Elo |
| 17: Move ordering + extensions | 8 (F-180–F-187) | ~1129 → ~1589 Elo |
| 18: Zobrist + TT | 13 (F-200–F-212) | ~1511 → ~1635 Elo |
| 19: LMR + NMP | 3 (F-220–F-222) | ~1628 Elo |
| 20: Aspiration + PVS | 3 (F-230–F-232) | Tighter search windows |
| 21: LMP + mate distance | 2 (F-240–F-241) | Forward pruning |
| 22: Pawn structure | 6 (F-250–F-255) | Eval depth: pawns |
| 23: Piece placement | 5 (F-260–F-264) | Eval depth: pieces |
| 24: King safety | 7 (F-270–F-276) | Eval depth: king |
| 25: Misc eval terms | 2 (F-280–F-281) | Bishop pair + tempo |
| 26: Search refinements | 10 (F-290–F-299) | TT policy, draws, pruning |
| 27: Time management | 9 (F-300–F-308) | Clock-based thinking |
| 28: Opening book PGN | 1 (F-310) | Match diversification |
| 29: macOS build hardening | 9 (F-320–F-328) | SIGKILL workarounds |
| **Total** | **162 features** | **~1600–1700 Elo** |
