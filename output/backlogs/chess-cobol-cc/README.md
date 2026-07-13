# chess-cobol-cc — Post-session Analysis

> Meta-analysis of the `chess-cobol-cc` project driven by **Claude Code 2.1.74**
> (`claude-opus-4-6`). Single session `9d9bb74e-…` (~28 MB JSONL, 3734 events)
> running 17 days from **2026-03-12** to **2026-03-30**.
>
> This file is **not** the project README — the project lives (read-only for
> this run) at `/Users/mathieuacher/SANDBOX/chess-cobol-cc`. All analysis
> artefacts are written here under
> `/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/backlogs/chess-cobol-cc/`.

---

## 1. Project overview

Build a **UCI-compliant chess engine in COBOL** (GNU Cobol 3.2.0) from scratch,
then **assess its Elo rating** by playing automated matches against Stockfish
(`cutechess-cli` + `UCI_LimitStrength`). The agent proposed a 4-phase plan and
the user accepted; implementation evolved into 9 internal "phase" labels and
5 binary snapshots (`v1`, `v2`, `v3b`, `v4`, `v4b`).

- Primary source: **`chess-engine.cob`** — one ~3460-line COBOL source file.
- Primary outcome: **~1630 Elo** (weighted average over 100 games vs SF
  1400/1500/1600/1700) — solidly club-player range.

See **[`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md)** for the
agent-centric, step-wise backlog (51 SB items across 9 named phases and
6 verified reverts).

---

## 2. Feature Backlog (user-driven)

Only items explicitly requested by the human user — **or** strictly required to
satisfy an explicit user acceptance criterion — are included. Every item maps
to ≥1 UI entry (see §5) and ≥1 PL entry (see §4). 11 distinct human prompts
are the sole direct input evidence; everything else is agent-initiated (see
the SB in `SPECIFICATION_BACKLOG.md`).

| ID | Title | Type | UI | PL | DoD | Outcome summary |
|---|---|---|---|---|---|---|
| **BL-001** | Produce a build-plan for a COBOL chess engine + Elo assessment | Documentation / Tooling | UI-001 | PL-ROOT | Yes | 4-phase plan proposed, user accepted `[T:#14]` |
| **BL-002** | Implement Phase 1: board + UCI + random-legal moves | Feature | UI-002 | PL-001 | Yes | Builds, 20/20 clean stress games `[R:stress_test2.pgn]` |
| **BL-003** | Implement Phase 2: material + PST + 1-ply search | Feature | UI-003 | PL-002 | Yes | Phase 2 match complete `[R:phase2_games.pgn]` |
| **BL-004** | Implement Phase 3: alpha-beta search at depth 3–4 | Feature | UI-004 | PL-003 | Yes | Match `vs SF 1320` recorded `[R:phase3_test.pgn]` |
| **BL-005** | Implement Phase 4: iterative deepening + time management | Feature | UI-005..UI-008 | PL-004 | Yes | Phase-4 match recorded `[R:phase4_test.pgn]` |
| **BL-006** | Progressively improve the engine's Elo (open-ended) | Feature (open-ended) | UI-009, UI-010 | PL-005, PL-006 | Yes | 9 phases, 7 reverts, best v4 = 1647 Elo `[M:project_elo_progress.md]` |
| **BL-007** | Refine the Elo assessment via multi-level calibration | Feature | UI-011 | PL-007 | Yes | 100-game triangulation → ~1630 Elo `[T:#3713]` |

**No `OP-###` items.** The user never asked for repo init, git commits, GitHub
publishing, or any other reproducibility-ops. The directory has no `.git/`.

---

## 3. Reproduction

### Preconditions (from session evidence)

- **macOS** (Darwin): paths observed are `/opt/homebrew/...`.
- **GNU COBOL 3.2.0** via Homebrew (`/opt/homebrew/Cellar/gnucobol/3.2_1/…`).
- **GMP 6.3.0** (COBOL dependency).
- **Stockfish** at `/opt/homebrew/bin/stockfish`.
- **cutechess-cli** on `$PATH`.

### Build (critical flag: `-fwrapv`, see SB-026)

```sh
COB_CFLAGS="-O2 -fwrapv \
  -I/opt/homebrew/Cellar/gmp/6.3.0/include \
  -I/opt/homebrew/Cellar/gnucobol/3.2_1/include" \
  cobc -x -o chess-engine chess-engine.cob
```

Without `-fwrapv`, the binary **hangs before `MAIN-PROGRAM`** (GNU COBOL
optimizer bug, session evidence `[T:#1661]` §4).

### Run (UCI sanity)

```sh
printf 'uci\nisready\nposition startpos\ngo depth 4\nquit\n' \
  | timeout 30 ./chess-engine
```

### Validate (20-game match, SF 1500)

```sh
cutechess-cli \
  -engine name=CobolChess cmd=./chess-engine proto=uci \
  -engine name=Stockfish  cmd=/opt/homebrew/bin/stockfish proto=uci \
     option.UCI_LimitStrength=true option.UCI_Elo=1500 \
  -each tc=40/60 \
  -rounds 20 \
  -pgnout match.pgn \
  -recover
```

Expected: **~67–70 %** score vs SF 1500 (= ~1620–1650 Elo) for the current
`chess-engine` binary (v4b).

### Checkpoints (file-snapshot style — no git)

| Milestone | Binary | PGN | Est. Elo |
|---|---|---|---|
| Phase 3 (alpha-beta) | `cobolchess` | `phase3_test.pgn` | ~1000–1200 |
| Phase 4b (quiescence + killers) | — | `phase4b_test.pgn` | ~1350 |
| v1 (time-mgmt fixed) | `chess-engine-v1` | `phase4d_timefix.pgn`, `phase4d_vs1500.pgn` | 1517 |
| v2 (bishop pair, rook files) | `chess-engine-v2` | `phase4e_vs1500.pgn` | 1608 |
| v3b (pawn struct + LMR + soft-time) | `chess-engine-v3b` | `phase5b_vs1500.pgn` | 1627 |
| v4 (PV order + persistent hist/killers) | `chess-engine-v4` | `phase7_vs1500.pgn` | 1647 |
| v4b (aggressive LMR R=2) | `chess-engine-v4b`, `chess-engine` | `phase9_vs1500.pgn` | ~1627 |
| Elo triangulation | `chess-engine-v4b` | `elo_vs1400.pgn`, `elo_vs1600.pgn`, `elo_vs1700.pgn` | **~1630** |

---

## 4. Prompt Ledger (summary)

**11 human-authored prompts** across the whole session. All tagged `<task-notification>` messages and 5 auto-compaction continuations were system-injected, not user prompts, and are excluded here.

### `PL-ROOT` — raw (event #4, 2026-03-12T19:37:41.818Z)

> "I want to build a chess engine in COBOL (using GNU Cobol)… at the end, I
> want to test this chess engine and assess its Elo rating, typically by
> playing games against chess engines of 'similar' levels."

### `PL-ROOT` — canonical replay prompt

> Build a **UCI-compliant chess engine in GNU COBOL 3.2** from scratch in
> `chess-engine.cob` targeting a single-file design. Iterate through classic
> phases (board + UCI + random moves → material + PST → alpha-beta → iterative
> deepening + time mgmt → quiescence / killers / LMR / eval refinements).
> After each phase, run a 20-game UCI match via `cutechess-cli` against
> Stockfish with `UCI_LimitStrength` at calibrated Elo, save the PGN, and
> update a memory note with results. Compile with `COB_CFLAGS="-O2 -fwrapv …"`
> (required to avoid a GNU COBOL `-O2` hang). Final goal: estimate the
> engine's Elo across 4+ opponent levels (SF 1400 / 1500 / 1600 / 1700).

### Per-BL raw + canonical prompts

| BL | Raw (≤25 w) | Canonical |
|---|---|---|
| BL-001 | "[propose plan for] chess engine in COBOL + Elo test" (from PL-ROOT) | "Propose a phased implementation plan for a UCI chess engine in GNU COBOL with Elo assessment via cutechess-cli. List each phase, its scope, and its Elo target." |
| BL-002 | "Let's go for Phase 1" (PL-001, #18) | "Implement Phase 1 of the plan: 8×8 board, FEN parser, UCI protocol (`uci`, `isready`, `position`, `go`, `quit`), pseudo-legal move generation for all pieces + castling + legal-move filtering, and random legal-move selection. Validate with a 10-game stress run." |
| BL-003 | "go to Phase 2" (PL-002, #103) | "Add material evaluation (P=100, N=320, B=330, R=500, Q=900, K=20000) and piece-square tables; pick the move with the best 1-ply score. Keep everything in `chess-engine.cob`." |
| BL-004 | "go" (PL-003, #236, interpreted as 'proceed to Phase 3') | "Add alpha-beta search at depth 3–4 using an explicit stack (COBOL recursion is inconvenient); handle `go depth N`. Run a 10-game match vs `UCI_Elo=1320`." |
| BL-005 | "continue" / "continue" / "yes" (PL-004, #445/558/574, continuations of Phase 4) | "Add iterative deepening and UCI `wtime/btime/movestogo` time management. Target safe 40/60 time control vs SF." |
| BL-006 | "please go ahead and try to improve the Elo" ×2 (PL-005, #733; PL-006, #857) | "Iteratively improve the engine's Elo: add quiescence, killers, MVV-LVA, delta pruning, history heuristic, aspiration windows, LMR, positional eval (bishop pair, rook-file, pawn structure). After each change, run a 20-game match vs Stockfish at a calibrated Elo, update `project_elo_progress.md`, and revert changes that regress (validating the per-node-cost constraint, see `feedback_overhead_sensitivity.md`)." |
| BL-007 | "no refine the Elo assessment" (PL-007, #3659) | "Do not add more engine improvements; instead run additional 20-game matches at SF 1400, 1600, 1700 to triangulate the engine's actual Elo. Report a weighted estimate and a realistic central figure." |

Full PL table lives in `appendix.json` → `prompt_ledger`.

---

## 5. User Instruction Index (summary)

11 human-authored segments, 0 `<system-reminder>`-only, 0 `<command-*>` wrappers seen.

| UI | Category | Strength | Target surface | Maps to |
|---|---|---|---|---|
| UI-001 | FeatureRequest | Explicit imperative | Code + Runtime | BL-001, BL-002 |
| UI-002 | Scenario/ScopeChange | Explicit imperative | Code | BL-002 |
| UI-003 | Scenario/ScopeChange | Explicit imperative | Code | BL-003 |
| UI-004 | Scenario/ScopeChange | Explicit imperative (terse "go") | Code | BL-004 |
| UI-005 | Continuation | Explicit imperative (terse "continue") | Code | BL-005 |
| UI-006 | Continuation | Explicit imperative (terse "continue") | Code | BL-005 |
| UI-007 | Agreement | Explicit imperative (terse "yes") | Code | BL-005 |
| UI-008 | Question/Clarification | Question ("status?") | Meta | — (Unmapped: meta) |
| UI-009 | FeatureRequest | Explicit imperative | Code | BL-006 |
| UI-010 | FeatureRequest | Explicit imperative (repeat) | Code | BL-006 |
| UI-011 | ScopeChange | Explicit imperative | Runtime/Tests | BL-007 |

Full UI table + raw text lives in `appendix.json` → `user_instruction_index`.

---

## 6. Repo statistics

Computed by `_work/repo_stats.py` over `/Users/mathieuacher/SANDBOX/chess-cobol-cc`,
excluding `.git/`, `node_modules/`, `build/` etc. (none present).

- **Total files:** 47
- **Total directories** (excl. root): 1 (`.claude/`)
- **No git repository.**

| Kind | Files | LOC | Notes |
|---|---:|---:|---|
| COBOL production | 1 | **3460** | `chess-engine.cob` (single-file design) |
| C (generated, build artefact) | 1 | 7667 | `chess-engine.c` — cobc intermediate output |
| H (generated) | 2 | 451 | `chess-engine.c.h`, `chess-engine.c.l.h` |
| Object files | 1 | — | `chess-engine.o` |
| Binaries (engine snapshots) | 16 | — | `cobolchess`, `chess-engine`, `chess-engine-v1..v4b`, variants `-dbg/-fast/-new/-noopt/-o1/-os/-o3/-test2/-v4test` |
| PGN test/match data | 25 | 17 288 | `phase*.pgn` + `stress_test*.pgn` + `elo_vs*.pgn` + `test_games.pgn` |
| Config | 1 | 29 | `.claude/settings.local.json` |
| Tests (dedicated) | 0 | 0 | No separate test harness — PGNs are the test oracle |
| Build scripts | 0 | 0 | Build is an ad-hoc `cobc` invocation captured in `.claude/settings.local.json` permissions |

**Key entry points:** `chess-engine.cob` (source) → `chess-engine` (binary) →
`cutechess-cli` (oracle). No CI; no `Makefile`; no tests directory.

`[S:stats_run_1]` output in `_work/repo_stats.py` stdout.

---

## 7. Reference to the Specification Backlog

The **agent-centric step-wise** backlog lives in
[`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md) — 51 SB items covering
every observable capability the engine exhibited across 9 phases, all five
auto-compaction windows, and the 7 agent-authored reverts.

---

## 8. Limitations & evidence gaps

- **No git history** for the project. All temporal segmentation relies on
  JSONL event indices + the agent's self-assigned phase/version labels.
- **Compaction-summary bias.** The richest evidence is five agent-authored
  "conversation-continued" summaries (`[T:#263, #865, #1661, #2648, #3088]`).
  Capability claims sourced from these summaries are therefore self-reported.
  We cross-check them against the `phase*.pgn` file names and `chess-engine-v*`
  binary mtimes, which match.
- **No re-execution.** Because this meta-analysis run is **read-only** against
  `/Users/mathieuacher/SANDBOX/chess-cobol-cc`, we did **not** re-run `cobc` or
  `cutechess-cli`. All `[L:run_n]` pointers are therefore **absent**; we rely
  on `[T:…]` and `[R:…]` only. This is flagged under
  `threats_to_validity` in `appendix.json`.
- **Terse prompts.** 6 of 11 human prompts are ≤ 15 characters
  ("go", "yes", "continue", "status?"). The agent's phase labels, binary
  version tags, and phase-plan interpretation are therefore **inferred from
  the initial plan** (SB-002) rather than user-specified.
- **No acceptance criteria were stated explicitly** for BL-006 (Elo target).
  The implicit criterion is "more Elo than the previous step" — satisfied per
  `project_elo_progress.md` (1517 → 1608 → 1627 → 1647).

See `REPORT.md` and `appendix.json` (`open_questions`) for the full list.

---

## 9. Machine-readable appendix

See [`appendix.json`](appendix.json) for the complete structured export
(session metadata, UII, PCI, PL, BL, SB, replay_plan, repo_stats, RQ-coverage,
strategy codebook, episodes, rubric scores, interaction metrics, COBOL panel,
process-tracing claims, threats to validity, open questions).
