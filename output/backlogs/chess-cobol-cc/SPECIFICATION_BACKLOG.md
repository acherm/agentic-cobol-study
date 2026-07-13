# Specification Backlog — `chess-cobol-cc` (agent-centric, step-wise)

**Project:** COBOL chess engine + Elo assessment against Stockfish
**Agent:** Claude Code 2.1.74, `claude-opus-4-6`
**Session:** `9d9bb74e-18ea-4bb9-844c-b4e175998988.jsonl` (17-day span, 2026-03-12 → 2026-03-30)

## Purpose

SB captures **what the agent actually built, incrementally**, as opposed to the
user-driven Feature Backlog (see `README.md`). SB items are each a stable
capability that the engine exhibited at a specific step, with explicit
**provenance** (user-driven / agent-initiated / prerequisite). Step labels are
**session episodes (EP-N)**, each bounded by a named "phase" / "version"
milestone (the agent itself introduced these phase labels, e.g. Phase 1…9, v1…v4b).

## Step segmentation method + limitations

- **No git repository** exists in `/Users/mathieuacher/SANDBOX/chess-cobol-cc`, so commit-based segmentation is unavailable. All `[G:…]` pointers are therefore omitted.
- Steps are derived from (a) session JSONL episodes, (b) the agent's own phase labels, (c) PGN filenames (`phase3_test.pgn`, `phase4b_test.pgn`, …, `phase9_vs1500.pgn`), and (d) the five auto-compaction boundaries in the session. Labels like `EP-P4b` correspond to "Phase 4b" as named by the agent.
- Line-precise file references to `chess-engine.cob` cite the current-tip file; the evolution across steps is captured by the PGN artefacts, the five compaction summaries, and the three memory-note files.
- The five auto-compactions (`#263`, `#865`, `#1661`, `#2648`, `#3088`) are the richest evidence: each contains an agent-authored summary of what was built in the preceding session segment. They are labelled `[T:#<event-idx>]`.

## Evidence sources

- `[T:#<n>]` — event index in `9d9bb74e-18ea-4bb9-844c-b4e175998988.jsonl`.
- `[R:<path>]` — file in the project root `/Users/mathieuacher/SANDBOX/chess-cobol-cc`.
- `[M:<memory-file>]` — persisted agent memory under `~/.claude/projects/-Users-mathieuacher-SANDBOX-chess-cobol-cc/memory/`.
- `[S:stats_run_1]` — repo statistics computed by `_work/repo_stats.py` (47 files, 1 dir excluding root).

---

## SB Table

| ID | Step (EP) | Title | Category | Provenance | Maps to | Key evidence |
|---|---|---|---|---|---|---|
| SB-001 | EP-bootstrap | Environment discovery (GNU COBOL 3.2.0 + cutechess-cli + Stockfish) | Tooling | Prerequisite | BL-001, PL-ROOT | `[T:#10]` `which cutechess-cli` |
| SB-002 | EP-bootstrap | Phased plan proposed (4 phases, Elo targets 200→1200+) | Documentation | Agent-initiated | BL-001 | `[T:#14]` |
| SB-003 | EP-P1 | UCI skeleton: `ACCEPT … FROM CONSOLE` + command dispatch (`uci`, `isready`, `position`, `go`, `quit`) | Capability | User-driven | BL-002, UI-002 | `[T:#263]` compaction §3 |
| SB-004 | EP-P1 | 8×8 board + starting position + FEN parser + UCI move application | Capability | User-driven | BL-002 | `[R:chess-engine.cob]`; `[T:#263]` |
| SB-005 | EP-P1 | Pseudo-legal move generation for all piece types + castling legality + king-safety filter | Capability | User-driven | BL-002 | `[T:#263]` §3 paragraphs `GENERATE-…`, `FILTER-LEGAL-MOVES` |
| SB-006 | EP-P1 | Random-move output (Phase-1 Elo baseline) | Behavior | User-driven | BL-002 | `[R:phase2_games.pgn]`, `[R:stress_test.pgn]` |
| SB-007 | EP-P1 | **Bug fix:** input buffer overflow → widened `WS-INPUT-LINE` to `PIC X(8192)` | Quality/Hardening | Agent-initiated | BL-002 | `[T:#263]` §4; 4/10 illegal-move games → 20/20 clean |
| SB-008 | EP-P1 | **Bug fix:** FEN column overflow (`PIC 9` wrapped) → widened to `PIC 9(2)` | Quality/Hardening | Agent-initiated | BL-002 | `[T:#263]` §4 |
| SB-009 | EP-P2 | Material + piece-square-table evaluation (P=100, N=320, B=330, R=500, Q=900, K=20000) | Capability | User-driven | BL-003, UI-003 | `[T:#263]` §3 `EVALUATE-POSITION` |
| SB-010 | EP-P2 | 1-ply `SEARCH-BEST-MOVE` (pick move with best eval) | Capability | User-driven | BL-003 | `[T:#263]` §3 |
| SB-011 | EP-P3 | Explicit-stack negamax alpha-beta (COBOL lacks convenient recursion) | Capability | User-driven | BL-004, UI-004 | `[T:#263]` §3 Phase-3 search architecture |
| SB-012 | EP-P3 | Per-ply state arrays (`WS-PLY-DATA(12)`) + `SEARCH-MAKE/UNMAKE-MOVE` wrappers | Capability | Prerequisite | BL-004 | `[T:#263]` §3 |
| SB-013 | EP-P3 | `go depth N` UCI parameter parsing + default depth reduced to 3 | Capability | Agent-initiated (fix for time-forfeits) | BL-004 | `[T:#865]` §4 |
| SB-014 | EP-P3 | First Stockfish match `vs SF 1320`, 10-game run | Test/Validation | User-driven | BL-004 | `[R:phase3_test.pgn]`; `[T:#517]` |
| SB-015 | EP-P4 | Iterative deepening loop in `UCI-CMD-GO` | Capability | User-driven | BL-005, UI-007 | `[T:#865]` §3 |
| SB-016 | EP-P4 | Time management: parse `wtime/btime/movestogo`, formula `time/(movestogo+1)/10`, cap 10–500 cs | Capability | User-driven | BL-005 | `[T:#865]` §3 |
| SB-017 | EP-P4 | MVV-LVA capture ordering + selection sort | Capability | Agent-initiated (ordering quality) | BL-005 | `[T:#865]` §3 `ORDER-PLY-MOVES` |
| SB-018 | EP-P4 | **Bug fix:** root-move corruption across iterations (regenerate legal moves each iteration) | Quality/Hardening | Agent-initiated | BL-005 | `[T:#865]` §4 |
| SB-019 | EP-P4b | Quiescence search (captures-only + stand-pat + checkmate guard) | Capability | Agent-initiated | BL-006 | `[T:#865]` §3 |
| SB-020 | EP-P4b | 2 killer moves per ply + `STORE-KILLER-MOVE` on beta cutoff | Capability | Agent-initiated | BL-006 | `[T:#865]` §3 |
| SB-021 | EP-P4b | Node-count telemetry + 512-node time-check granularity | Quality/Hardening | Agent-initiated | BL-006 | `[T:#865]` §3; `[R:phase4b_test.pgn]` |
| SB-022 | EP-P4c | Broadened opponent calibration run vs SF 1600 | Test/Validation | Agent-initiated | BL-006 | `[R:phase4c_test.pgn]`; `[T:#830]` |
| SB-023 | EP-P4d | Delta pruning in quiescence (per-move + big-delta at stand-pat) | Capability | Agent-initiated | BL-006 | `[T:#1661]` §3 |
| SB-024 | EP-P4d | History heuristic (flat 4096-entry table, depth² increments) | Capability | Agent-initiated | BL-006 | `[T:#1661]` §3 |
| SB-025 | EP-P4d | Aspiration windows (±50 cp), full re-search on fail | Capability | Agent-initiated | BL-006 | `[T:#1661]` §3 |
| SB-026 | EP-P4d | **Toolchain fix:** `-O2` hang ⇒ mandatory `COB_CFLAGS=-O2 -fwrapv …` | Tooling | Agent-initiated | BL-006 | `[T:#1661]` §4 ("GNU COBOL compiler bug") |
| SB-027 | EP-P4d | **Revert:** reverse-futility pruning (extra eval cost > savings) | Quality/Hardening (negative result) | Agent-initiated | BL-006 | `[T:#1661]` §4 |
| SB-028 | EP-P4d | **Regression fix:** time-mgmt formula reverted to `time/(movestogo+2)/10` | Bugfix | Agent-initiated | BL-006 | `[T:#1661]` §4; `[M:feedback_time_management.md]` |
| SB-029 | EP-v1 | First named binary snapshot (`chess-engine-v1`) post time-mgmt fix | Tooling | Agent-initiated | BL-006 | `[R:chess-engine-v1]` mtime 2026-03-20 |
| SB-030 | EP-v1 | Multi-level calibration: `vs SF 1320 85%`, `vs SF 1500 52.5%` ⇒ ~1517 Elo | Test/Validation | Agent-initiated | BL-006 | `[R:phase4d_timefix.pgn]`, `[R:phase4d_vs1500.pgn]`; `[M:project_elo_progress.md]` |
| SB-031 | EP-v2 | Bishop-pair bonus (+50 cp both-bishops) | Capability | Agent-initiated | BL-006 | `[T:#2648]` §3 |
| SB-032 | EP-v2 | Rook on open/semi-open file (+25 / +15 cp) with inline pawn-file tracking | Capability | Agent-initiated | BL-006 | `[T:#2648]` §3 |
| SB-033 | EP-v2 | **Revert:** check-extension at first qsearch ply (search explosion) | Quality/Hardening (negative result) | Agent-initiated | BL-006 | `[T:#2648]` §4 |
| SB-034 | EP-v2 | v2 match vs SF 1500 = 65.0% ⇒ ~1608 Elo | Test/Validation | Agent-initiated | BL-006 | `[R:phase4e_vs1500.pgn]`; `[M:project_elo_progress.md]` |
| SB-035 | EP-v3 | Pawn-structure eval: doubled (-15), isolated (-20), passed (tapered +10..+90) | Capability | Agent-initiated | BL-006 | `[T:#3088]` §3 |
| SB-036 | EP-v3 | Late Move Reductions with re-search-on-fail-high (state machine 0/1/2) | Capability | Agent-initiated | BL-006 | `[T:#3088]` §3 |
| SB-037 | EP-v3 | **Revert:** futility pruning (interaction with LMR-modified MAX-PLY) | Quality/Hardening (negative result) | Agent-initiated | BL-006 | `[T:#3088]` §4 |
| SB-038 | EP-v3 | **Regression fix:** aggressive `time/movestogo` → 7 forfeits → restored buffer + soft-time check (4× last-iteration) | Bugfix | Agent-initiated | BL-006 | `[T:#3088]` §4; `[R:phase5_vs1500.pgn]` (3.5/20) vs `[R:phase5b_vs1500.pgn]` (13.5/20) |
| SB-039 | EP-v3 | v3b match vs SF 1500 = 67.5% ⇒ ~1627 Elo | Test/Validation | Agent-initiated | BL-006 | `[R:phase5b_vs1500.pgn]`; `[M:project_elo_progress.md]` |
| SB-040 | EP-v3 | **Memory notes written**: `project_elo_progress.md`, `feedback_time_management.md`, `feedback_overhead_sensitivity.md`, `MEMORY.md` | Documentation | Agent-initiated | BL-006 | `[M:MEMORY.md]` |
| SB-041 | EP-P6 | Endgame king PST + tapered eval wired into eval loop | Capability | Agent-initiated | BL-006 | `[T:#3115]`–`[T:#3140]` |
| SB-042 | EP-P6 | **Revert:** tapered king eval — 8/20 (40%) match regression | Quality/Hardening (negative result) | Agent-initiated | BL-006 | `[T:#3262]`; `[R:phase6_vs1500.pgn]` |
| SB-043 | EP-P6 | **Revert:** horizon check extensions — 9/20 (45%) regression (per-node overhead) | Quality/Hardening (negative result) | Agent-initiated | BL-006 | `[T:#3373]`; `[R:phase6b_vs1500.pgn]`; `[M:feedback_overhead_sensitivity.md]` |
| SB-044 | EP-v4 | PV move ordering at root (best move from previous iter gets score 20 000) | Capability | Agent-initiated | BL-006 | `[T:#3427]` |
| SB-045 | EP-v4 | **Persistent** killer + history tables across iterative-deepening iterations | Capability | Agent-initiated | BL-006 | `[T:#3420]` |
| SB-046 | EP-v4 | v4 match vs SF 1500 = 14/20 (70.0%) ⇒ ~1647 Elo (best single run) | Test/Validation | Agent-initiated | BL-006 | `[R:phase7_vs1500.pgn]`; `[T:#3477]` |
| SB-047 | EP-P8 | **Revert:** endgame king correction via phase-switch (phase counting cost too high) | Quality/Hardening (negative result) | Agent-initiated | BL-006 | `[T:#3569]`–`[T:#3574]`; `[R:phase8_vs1500.pgn]` (5.5/14 partial) |
| SB-048 | EP-v4b | Aggressive LMR R=2 for move-index ≥ 7 | Capability | Agent-initiated | BL-006 | `[T:#3606]`–`[T:#3616]` (17% node reduction at depth 5) |
| SB-049 | EP-v4b | v4b match vs SF 1500 = 13.5/20 (67.5%), LOS 94.6% | Test/Validation | Agent-initiated | BL-006 | `[R:phase9_vs1500.pgn]`; `[T:#3641]` |
| SB-050 | EP-Elo | Multi-level Elo triangulation: SF 1400 80%, SF 1500 70%, SF 1600 55%, SF 1700 30% | Test/Validation | User-driven | BL-007, UI-011 | `[R:elo_vs1400.pgn]`, `[R:elo_vs1600.pgn]`, `[R:elo_vs1700.pgn]`; `[T:#3713]` |
| SB-051 | EP-Elo | Final refined Elo report: weighted ~1621, realistic **~1630 Elo** (100 games) | Documentation | User-driven | BL-007 | `[T:#3713]`; `[M:project_elo_progress.md]` |

---

## Provenance summary

| Provenance | Count |
|---|---:|
| User-driven | 12 (SB-003..006, 009, 010, 011, 014, 015, 016, 050, 051) |
| Agent-initiated | 37 |
| Prerequisite | 2 (SB-001, SB-012) |
| **Total** | **51** |

## Notable reverts (captured as negative-result SB items)

- **SB-027** reverse-futility pruning
- **SB-033** check extension at first qply (v2)
- **SB-037** futility pruning in v3
- **SB-038** time-formula without safety buffer
- **SB-042** tapered king eval
- **SB-043** horizon check extensions (v4 attempt)
- **SB-047** endgame king correction via phase-switch

Six of seven reverts triggered agent-authored persistent memory notes
(`feedback_time_management.md`, `feedback_overhead_sensitivity.md`) that
influenced later steps — notably SB-044/045 which deliberately chose
**zero-per-node-cost** improvements.

## Mapping to the user-driven Feature Backlog

All 51 SB items roll up to only **7 BL items** (BL-001..007). Most of the
implementation volume — 37 agent-initiated items — lives under **BL-006**
("Progressively improve the engine's Elo"), consistent with the user's two
"please go ahead and try to improve the Elo" prompts (UI-009, UI-010). See
`README.md` for the BL table.
