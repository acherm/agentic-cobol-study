# `COBOL-chess` — Case Study

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/COBOL-chess/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`COBOL-chess` assessment](../assessments/COBOL-chess.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/COBOL-chess/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/COBOL-chess/KEY_FEATURES.md)
  
> 🔁 **Replay prompts** (step-wise, HOW-agnostic, for reproducing with a different agent): [`REPLAY_PROMPTS.md`](../backlogs/COBOL-chess/REPLAY_PROMPTS.md)

**Project root.** `/Users/mathieuacher/SANDBOX/COBOL-chess`  
**Sessions.** 3 (1 Claude Code + 2 Codex)  
**Activity window.** 2026-02-09 → 2026-03-19 (38 days)  
**Agents & models.** Claude Code/claude-opus-4-6, Codex/gpt-5.2, Codex/gpt-5.4

---

## RQ1 — Domain, intent, novelty

**What it is.** Chess engine in COBOL with formal architecture + spec backlog.

**Why it's interesting.** Second chess-engine attempt — this time led by Codex (GPT-5) instead of Claude, with explicit architecture / specification artefacts.

**From the project's `README.md` (first sections):**

> **# COBOL Chess Engine (`cobochess`)**  
> `cobochess` is a small but real chess engine written in GNUCobol. It speaks UCI, enforces full chess move legality, exposes command-line perft modes, and ships with a benchmarking harness built around `cutechess-cli` and Stockfish. This repository now has two documentation layers: - `README.md`: quick project overview, feature list, build/run workflow, and a compact architecture summary. - [`ARCHITECTURE.md`](ARCHITECTURE.md): the longer technical report covering data structures, control flow, search, evaluation, tooling, and current limitations.

> **## Architecture at a glance**  
> - Multi-program GNUCobol engine: `COBOCHESS`, `SEARCH`, `ALPHABETA`, `QUIESCE`, `MOVEGEN`, `MAKEMOVE`, `UNMAKEMOVE`, `ATTACK`, `EVAL`, `FEN`, `TIMEUTIL`, and `MOVE2UCI`. - Board representation: a shared 0x88 mailbox board stored in `GAME-STATE`. - Move legality model: pseudo-legal generation plus legality filtering through `MAKEMOVE`/`UNMAKEMOVE`. - Search: iterative deepening negamax with alpha-beta pruning, aspiration windows, principal variation search, quiescence search, transposition table, killer/history heuristics, null-move pruning, late-move reductions, late-move pruning, check extens…

**Opening prompt that kicked off the project:**

```
I want to build a chess engine in COBOL (GNUCobol)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- FEN/UCI I/O
- move gen
- search
- opening book
- openings + results directories
- reproducible cutechess matches

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| command exited with non-zero status | 38 |
| C compiler error | 35 |
| test suite reported FAIL | 13 |
| GnuCOBOL compiler error (incl. syntax) | 10 |
| Python traceback (tooling) | 6 |
| missing file | 3 |
| process aborted | 2 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **184** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 8 |
| Bullet / numbered sub-requests inside user prompts | 92 |
| Git commit subjects | 2 |

**Backlog (184 F-### entries).** Grouped by phase:

- **Phase 1: Project Scaffold** — 4 features  
  Directory structure (`src/`, `copybooks/`, `tools/`, `tests/`, `openin…; Makefile with `cobc` build, `perft`, `uci-smoke`, `clean`, `rebuild` t…; `.gitignore` for binaries, results, caches; `README.md` with build/test/usage docs
- **Phase 2: Core Engine — Board & Data Model** — 10 features  
  0x88 mailbox board representation (128-element array, off-board detect…; Piece encoding (EMPTY=0, WP=1..BK=12), color constants (WHITE=0, BLACK…; Castling bitmask encoding (WK=1, WQ=2, BK=4, BQ=8); Move flag bitmask (CAPTURE=1, EP=2, CASTLE=4, PROMOTION=8, PAWN-DOUBLE…; Move record structure (from, to, promo, flags, score); Move list (count + 256-entry array); Game state structure: board, side, castling, EP sq, halfmove, fullmove…; Undo stack: 256-entry stack with captured/moved piece, castling, EP, h… _(+2 more)_
- **Phase 3: Core Engine — FEN Parsing** — 8 features  
  FEN string parsing via `UNSTRING ... DELIMITED BY SPACE` (6 fields); Piece placement: rank-by-rank traversal, char-to-piece mapping (12 typ…; Side-to-move parsing (`w`/`b`); Castling rights parsing (`KQkq` → bitmask, `-` for none); En passant square parsing (algebraic → 0x88 index); Halfmove/fullmove clock parsing via `NUMVAL`; King square detection during placement; FEN validation with error status return
- **Phase 4: Core Engine — Attack Detection** — 7 features  
  Square-attacked-by-side query; Pawn attack detection (white/black pawn diagonal offsets); Knight attack detection (8 offsets); King attack detection (8 offsets); Bishop/queen diagonal ray attack detection; Rook/queen orthogonal ray attack detection; 0x88 off-board check for ray/step moves
- **Phase 5: Core Engine — Move Generation** — 20 features  
  Full legal move generator (iterates 0x88 board, dispatches by piece); White pawn single push (+16 to empty); Black pawn single push (-16 to empty); White pawn double push (+32 from rank 1, both squares empty); Black pawn double push (-32 from rank 6); Pawn captures (diagonal, enemy piece or EP square); En passant capture (detect `TO-SQ = GS-EP-SQ`, flag EP+CAPTURE); Pawn promotion (all 4 pieces: Q/R/B/N) on push and capture _(+12 more)_
- **Phase 6: Core Engine — Make/Unmake Move** — 15 features  
  Make move: save full undo state to stack; Flag decoding (bitmask → EP, CASTLE, PROMOTION, PAWN-DOUBLE); En passant execution: remove captured pawn behind target; Castling rook movement (4 types: h1→f1, a1→d1, h8→f8, a8→d8); Promotion execution: replace pawn with promoted piece; Castling rights update on king move; Castling rights update on rook move/capture; Halfmove clock: reset on pawn/capture, increment otherwise _(+7 more)_
- **Phase 7: Core Engine — Perft** — 2 features  
  Recursive perft node counter (`PROGRAM-ID. PERFT RECURSIVE`); `LOCAL-STORAGE SECTION` for per-frame move data (recursion-safe)
- **Phase 8: Core Engine — Initial Evaluation** — 3 features  
  Material values: P=100, N=320, B=330, R=500, Q=900; Side-relative scoring (negate for Black); 0x88 board traversal with off-board skip
- **Phase 9: Core Engine — Initial Search** — 11 features  
  Iterative deepening (depth 1 to max); Basic alpha-beta (negamax framework); Quiescence search (captures + promotions only, recursive); Stand-pat evaluation in quiescence; Checkmate detection (legal count = 0, in check); Stalemate detection (legal count = 0, not in check); Root move generation + PV output; UCI `info depth ... nodes ... score cp ... pv ...` output _(+3 more)_
- **Phase 10: Core Engine — UCI Protocol** — 15 features  
  UCI command loop (`ACCEPT IN-LINE`, dispatch by keyword); `uci` → id + options + `uciok`; `isready` → `readyok`; `ucinewgame` → reset heuristics; `position startpos [moves ...]`; `position fen <fen> [moves ...]`; `go depth <N>` (fixed depth); `go movetime <ms>` (fixed time) _(+7 more)_
- **Phase 11: Core Engine — Time Utility** — 2 features  
  Wall-clock time in centiseconds via `ACCEPT FROM DATE/TIME` + `INTEGER…; Date-to-days caching for performance
- **Phase 12: Test Suite & Tooling (initial)** — 6 features  
  Perft test cases: 4 positions (startpos, kiwipete, EP-edge, promotions…; Perft checker script: runs `cobochess --perft`, compares node counts; UCI smoke test: sends `uci/isready/position/go depth 3/quit`, verifies…; Elo match runner: orchestrates cutechess-cli with Stockfish strength c…; Elo calculator: PGN parser, Elo estimate with 95% Wilson CI; Opening book (EPD format, 4 entries from startpos)
- **Phase 13: Elo Calc Bug Fixes** — 2 features  
  Fix regex character range in PGN result parsing; Per-game White/Black perspective tracking for correct W/D/L attributio…
- **Phase 14: UCI Buffer Fix** — 1 features  
  UCI input line buffer enlarged from `PIC X(512)` to `PIC X(4096)`
- **Phase 15: Search Improvements — Move Ordering & Extensions** — 8 features  
  Piece-square tables in eval (knight/bishop centralization, pawn advanc…; MVV-LVA capture ordering: `100000 + victim×10 − attacker`; Killer moves: 2 slots per ply (256 plies), +90000/+80000 ordering bonu…; History heuristic: 16384-entry table (from×128+to), depth² bonus on cu…; In-check extensions: +1 ply when side-to-move king is in check; Root promotion bonus (+80000 + piece value); Root castling bonus (+500); Selection sort (pick-best) for move ordering at root, inner nodes, and…
- **Phase 16: Zobrist Hashing & Transposition Table** — 13 features  
  Zobrist hash tables (EXTERNAL shared singleton across compilation unit…; LCG PRNG for hash key generation (multiplier=1103515245, increment=123…; Piece-square keys: 12 pieces × 128 squares; Side-to-move key; Castling combination keys (16 values); En passant file keys (8 values); Full Zobrist hash computation from position (in FEN parser); Incremental Zobrist update in MAKEMOVE (pieces, side, castling, EP) _(+5 more)_
- **Phase 17: Late Move Reductions & Null-Move Pruning** — 3 features  
  Late Move Reductions (LMR): reduce by 1 for quiet moves at depth ≥ 3, …; Null-move pruning (NMP): R=3 reduction, requires depth ≥ 4, not in che…; Null-move Zobrist update: toggle side, clear EP, adjust hash key
- **Phase 18: Aspiration Windows & PVS** — 3 features  
  Aspiration windows: for depth ≥ 3, initial ±50 around previous score; …; Principal Variation Search (PVS): first move full window, rest null wi…; PV move from previous iteration seeded into next iteration
- **Phase 19: Late Move Pruning & Mate Distance Pruning** — 2 features  
  Late Move Pruning (LMP): skip quiet moves at depth ≤ 2 when legal coun…; Mate distance pruning: tighten alpha/beta bounds based on `MATE-SCORE …
- **Phase 20: Evaluation Rewrite — Pawn Structure** — 6 features  
  Pawn file count precomputation (`WPC`/`BPC` arrays per file); Pawn rank tracking (`WPMIN`/`BPMAX` per file) for passed pawn detectio…; Doubled pawn penalty: −8 cp per extra pawn on same file; Isolated pawn penalty: −10 cp if no friendly pawn on adjacent files; Passed pawn bonus: +10 + `rank × 8` if no enemy pawn ahead on same/adj…; Pawn piece-square heuristic: advancement reward + central file bonus
- **Phase 21: Evaluation Rewrite — Piece Placement** — 5 features  
  Knight centralization: `24 − (manhattan_dist × 6)`; Bishop centralization: `16 − (manhattan_dist × 4)`; Queen mild centralization: `5 − (manhattan_dist × 2)`; Rook on 7th rank bonus: +20 cp; Rook on open file: +12 cp (no pawns), semi-open file: +6 cp (no friend…
- **Phase 22: Evaluation Rewrite — King Safety** — 7 features  
  Non-pawn material (NPM) tracking for game phase detection; Endgame detection: `NPM-TOTAL ≤ 2600`; King piece-square (middlegame): encourages edge placement `(dist × 5) …; King piece-square (endgame): encourages centralization `20 − (dist × 5…; White king pawn shield: +6 per friendly pawn on 3 forward squares, −6 …; Black king pawn shield; Pawn shield disabled in endgame
- **Phase 23: Evaluation Rewrite — Misc Terms** — 2 features  
  Bishop pair bonus: +30 cp for having 2+ bishops; Tempo bonus: +10 cp for the side to move
- **Phase 24: Search Refinements** — 10 features  
  TT replacement policy: depth-preferred (replace only if new depth ≥ st…; TT flag determination: EXACT (alpha improved, < beta), LOWER (beta cut…; Threefold repetition detection: scan undo stack keys within reversible…; 50-move rule draw: return 0 if `GS-HALFMOVE ≥ 100`; Delta pruning in quiescence: prune if `standpat + 950 < alpha`; Quiescence MVV-LVA + promotion scoring; Time check with countdown: every 2048 nodes, call TIMEUTIL, compare el…; Time abort at root: retain previous iteration's best move/score _(+2 more)_
- **Phase 25: Time Management (advanced)** — 9 features  
  `go wtime/btime/winc/binc/movestogo` support; Side-aware clock selection (pick wtime/winc or btime/binc based on sid…; Moves-to-go estimation: default 22, clamped [10, 60]; Overhead subtraction: 50ms safety margin; Time allocation formula: `(safe_remaining / movestogo) + (increment × …; Time cap: think time ≤ 20% of remaining; Minimum think time: floor of 20ms; Final safety clamp: think ≤ remaining _(+1 more)_
- **Phase 26: Opening Book (PGN format)** — 1 features  
  PGN-format opening book for cutechess-cli diversification (100 games f…
- **Phase 27: macOS Build System Hardening** — 9 features  
  macOS ad-hoc code signing (`codesign -s - -f`) via `make sign` target; macOS quarantine xattr clearing (`xattr -dr com.apple.quarantine/prove…; Engine health check: `tools/engine_check.py` — runs `--perft-startpos …; Build retry loop: up to 5 attempts with `engine_check.py` validation b…; Force Apple toolchain PATH prefix: `PATH="/usr/bin:/bin:/usr/sbin:/sbi…; macOS-specific compiler flags: `-target arm64-apple-macosx`, `-isysroo…; `.NOTPARALLEL:` + explicit `clean → build` ordering to prevent build r…; Quarantine/codesign workarounds in tool scripts (`perft_check.py`, `uc… _(+1 more)_

**README/REPORT features (8)** — first 8:

- Full rule handling: castling, en passant, promotions, checkmate/stalemate detection, repetition detection, and the 50-move rule inside search.
- UCI support for the common engine loop: `uci`, `isready`, `ucinewgame`, `position startpos|fen`, `go depth`, `go movetime`, and clock-driven `go`.
- CLI perft modes for correctness testing:
- `--perft-startpos <depth>`
- `--perft "<fen>" <depth>`
- Root search info output in UCI format.
- Deterministic opening suites in [`openings/book.pgn`](openings/book.pgn) and [`openings/book.epd`](openings/book.epd) for tournament runs.
- Historical tournament artifacts under [`results/`](results/).

**Prompt-extracted sub-requests (92)** — first 8 (sub-bullets inside user messages):

- _[2026-03-19]_ PASS 1 (Extraction): reconstruct the feature backlog + prompt ledger + replay package (repro-first, factual).
- _[2026-03-19]_ PASS 2 (Interpretation): characterize agent strategies, outcomes/quality, interaction demand; correlate with lightweight repo metrics.
- _[2026-03-19]_ I will NOT provide transcripts proactively.
- _[2026-03-19]_ You must analyze the repo as-is (git history may be minimal/absent).
- _[2026-03-19]_ Codex stores local state under CODEX_HOME (default ~/.codex). Session artifacts are typically under:
- _[2026-03-19]_ $CODEX_HOME/sessions/ (often JSONL files, session-id named)
- _[2026-03-19]_ $CODEX_HOME/history.jsonl (if history persistence is enabled)
- _[2026-03-19]_ $CODEX_HOME/log/ (diagnostic logs; location may vary via config)

**Git commits (2)** — first 8:

- `0e2ab146f3` 2026-05-04  Add agentic chess-engine README, LICENSE, .gitignore
- `faf0f163e9` 2026-03-19  Initial commit: cobochess — COBOL (GnuCOBOL) UCI chess engine (~1600-1700 Elo)

## RQ3 — What was delivered

## RQ4 — Size and complexity

**File inventory** (145 files, 4.3 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 16 | 3,988 |
| Markdown | 4 | 1,149 |
| JSON | 55 | 983 |
| Python | 4 | 681 |
| Makefile | 1 | 105 |
| Shell | 1 | 42 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 16 |
| Total lines | 3,988 |
| Code lines (non-blank, non-comment) | 3,359 |
| Comment lines | 117 |
| Sections | 30 |
| Paragraphs | 70 |
| Data items (level-number declarations) | 610 |
| Max IF/EVALUATE nesting (any file) | 6 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 859 |
| `IF` | 439 |
| `COMPUTE` | 209 |
| `PERFORM` | 182 |
| `EXIT` | 82 |
| `ADD` | 79 |
| `CALL` | 56 |
| `SUBTRACT` | 52 |
| `DIVIDE` | 35 |
| `EVALUATE` | 22 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `src/search.cob` | 1,147 |
| `src/makemove.cob` | 501 |
| `src/movegen.cob` | 418 |
| `src/eval.cob` | 328 |
| `src/main.cob` | 321 |

**Git churn signal.** 2 commits, 8554 insertions / 0 deletions, first 2026-03-19, last 2026-05-04.

## RQ4b — COBOL language mastery

**Mastery score:** **40** distinct COBOL constructs used across **10/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 1,640 | `IF`×878, `PERFORM`×237, `WHEN`×141, `ELSE`×98, `EXIT`×82, `PERFORM_UNTIL`×53, `GOBACK`×50, `EVALUATE`×44 _(+3 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 460 | `COMPUTE`×215, `ADD`×158, `SUBTRACT`×52, `DIVIDE`×35 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 1,040 | `USAGE_COMP_5`×489, `PIC_S9`×487, `PIC_X`×31, `OCCURS`×25, `PIC_9`×8 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 24 | `READ`×13, `START`×11 |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 45 | `REFERENCE_MOD`×26, `DELIMITED_BY`×13, `UNSTRING`×4, `STRING`×2 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 17 | `SEARCH`×9, `SET`×8 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 197 | `CALL`×77, `USING`×69, `GIVING`×35, `LINKAGE_SECTION`×13, `RECURSIVE`×3 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 34 | `COPY`×34 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 205 | `FUNCTION`×109, `FUNCTION_MOD`×60, `FUNCTION_TRIM`×23, `FUNCTION_NUMVAL`×13 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 16 | `DISPLAY`×9, `ACCEPT`×7 |

**Notable non-trivial constructs used:** `CALL` (77×), `RECURSIVE` (3×), `OCCURS` (25×), `USAGE_COMP_5` (489×), `COPY` (34×), `UNSTRING` (4×), `FUNCTION` (109×).

**Procedural structure.** 70 paragraphs, 30 sections across 16 COBOL file(s). That means roughly **70 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **4h 58m** across 5640 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `build` | compile / makefile / dependency work | 2h 38m | 53.0% |
| `understanding` | reading / searching to build a mental model | 45m 29s | 15.2% |
| `feature` | adding new functionality | 39m 29s | 13.2% |
| `spec` | specifications / architecture writing | 18m 22s | 6.1% |
| `unknown` | could not classify confidently | 17m 21s | 5.8% |
| `test` | writing or running tests / benchmarks | 12m 22s | 4.1% |
| `bug_fix` | correcting an observed defect | 7m 14s | 2.4% |
| `plan` | task tracking, planning | 0m 15s | 0.1% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `test` | 981 |
| `build` | 618 |
| `feature` | 185 |
| `understanding` | 77 |
| `bug_fix` | 61 |
| `plan` | 13 |

## RQ6 — Failures encountered

Out of **1,935 tool results**, **66** (3.4%) contained an error signature.

The user filed **10 bug-report-style prompt(s)** (prompts containing words like 'error', 'crash', 'broken', 'wrong').

## RQ6b — Difficulty assessment

**Auto-label: `High`** (difficulty index 0.74; mean rank across 7 signals = 12.1).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 5.0 | 13.0 |
| Calendar span (days first→last event) | 38 | 16.0 |
| User prompts | 26 | 12.0 |
| Redirect / bug-report prompts | 10 | 14.0 |
| Tool-output error rate | 0.034 | 8.0 |
| Fix cycles (error → immediate retry) | 6 | 13.0 |
| Share of active time spent on `bug_fix` | 0.024 | 9.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 26
- **Average prompt length:** 1554 chars; **max:** 10,014 chars
- **Total chars written by user:** 40,418
- **Sessions:** 3; **span:** 38 days
- **Long-prompt ratio** (≥500 chars): 14/26

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Codex | `gpt-5.2` | 2026-02-09 09:42 | 2d 1h 16m | 24 | 1872 | $44.48 |
| 2 | Claude Code | `claude-opus-4-6` | 2026-03-19 12:54 | 27d 20h 46m | 10 | 55 | $20.74 |
| 3 | Codex | `gpt-5.4` | 2026-03-19 14:00 | 6m 50s | 1 | 63 | $0.69 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| other | 11 |
| bug-report | 10 |
| review-ask | 4 |
| clarify | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-02-09]_ I want to build a chess engine in COBOL (GNUCobol)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels
2. _[2026-02-09]_ PLEASE IMPLEMENT THIS PLAN: # COBOL (GnuCOBOL) UCI Chess Engine + Elo Harness ## Summary Build a playable chess engine in **GNUCobol 3.2.x** that speaks **UCI**, using a **0x88 mailbox board**, with correctness validated via **perft** and p…
3. _[2026-02-09]_ mathieuacher@Mathieus-MacBook-Pro COBOL-chess % make build make: Nothing to be done for `build'.
4. _[2026-02-09]_ mathieuacher@Mathieus-MacBook-Pro COBOL-chess % python3 tools/elo_calc.py /Users/mathieuacher/SANDBOX/COBOL-chess/results/match_20260209_131301.pgn --baseline-elo 1320 Traceback (most recent call last): File "/Users/mathieuacher/SANDBOX/COB…
5. _[2026-02-09]_ it's working but it's not accurate: there is a mix of games with white and black side, and it seems to assume that the engine under study always have white or black pieces... please correct
6. _[2026-02-09]_ Elo rating of cobochess is not good at all... before trying to improve it, is it possible to investigate whether there is a misconfiguration about reasoning depth or time to think or whatever?
7. _[2026-02-09]_ depth 4: is it for cobochess? such a depth is very low
8. _[2026-02-09]_ I basically want to see games of the best "variant" of cobochess
9. _[2026-02-09]_ OK... the current implementation is very weak. Try to significantly improve the engine
10. _[2026-02-10]_ good... let's try to beat Stockfish @1600 now

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 2d 1h 23m |
| Active collaboration time | 4h 58m |
| Tool calls | 1,935 |
| Input tokens | 236,150,053 |
| Output tokens | 1,146,954 |
| Cache-read tokens | 232,432,640 |
| Cache-create tokens | 0 |
| Reasoning tokens (Codex) | 897,503 |
| Estimated cost at API rack rates | $45.17 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `exec_command` | 900 |
| `write_stdin` | 836 |
| `apply_patch` | 191 |
| `update_plan` | 6 |
| `request_user_input` | 2 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
