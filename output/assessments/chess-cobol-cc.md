# Assessment — `CHESS-COBOL-CLAUDE` (folder `chess-cobol-cc`) — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> A full UCI chess engine (`chess-engine`, ~100 KB binary) with perft-validated move generation, alpha-beta + quiescence + LMR + null-move pruning + PVS + aspiration windows, Zobrist hashing with a transposition table, piece-square + pawn-structure + king-safety evaluation, and clock-aware time management. Measured at **~1630 Elo** across 400 games vs cutechess-cli-hosted Stockfish capped at 1400 / 1500 / 1600 / 1700 (PGN artefacts preserved under `elo_vs1400.pgn`…`elo_vs1700.pgn`).

> ~1630 Elo ≈ solid intermediate club player — beats casual humans reliably, loses to strong humans. The engine plays **legal, tactically aware chess** with correct castling, en-passant, promotions, stalemate / threefold / 50-move rules, and sensible time use.

**Difficulty (auto-labelled):** High (idx 0.61). **Active collaboration time:** 15 h 31 m. **Sessions:** 1. **Backlog entries discovered:** 51. **Git commits:** 1.

## 1. Contract — what was asked

Build a UCI chess engine in GnuCOBOL and measure its Elo by playing against strength-capped Stockfish.

Opening user prompt (verbatim, truncated):

```
I want to build a chess engine in COBOL (using GNU Cobol)… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of “similar” levels.
```

## 2. Delivered — externally-observable evidence

A full UCI chess engine (`chess-engine`, ~100 KB binary) with perft-validated move generation, alpha-beta + quiescence + LMR + null-move pruning + PVS + aspiration windows, Zobrist hashing with a transposition table, piece-square + pawn-structure + king-safety evaluation, and clock-aware time management. Measured at **~1630 Elo** across 400 games vs cutechess-cli-hosted Stockfish capped at 1400 / 1500 / 1600 / 1700 (PGN artefacts preserved under `elo_vs1400.pgn`…`elo_vs1700.pgn`).

**Executables present in `SANDBOX/chess-cobol-cc/`** (at least *something* built):

- `chess-engine` (105 KB)
- `chess-engine-dbg` (57 KB)
- `chess-engine-fast` (89 KB)
- `chess-engine-new` (57 KB)
- `chess-engine-noopt` (272 KB)
- `chess-engine-o1` (105 KB)
- `chess-engine-o3` (57 KB)
- `chess-engine-os` (61 KB)
- `chess-engine-test2` (105 KB)
- `chess-engine-v1` (89 KB)
- _(+6 more)_

**COBOL surface exercised.** 1 COBOL file(s), 2,920 code lines, 81 paragraphs (≈ function-like units), 2 sections, mastery score **38** distinct constructs across **10/10** capability categories.

**Backlog (auto-mined).** 51 `F-###` / `SB-###` / `S#-##` entries in the harvested / subagent-generated `SPECIFICATION_BACKLOG.md`. Prompts also produced 99 sub-request bullets; git history carries 1 commits.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

**Mean score across 7 BLs and 6 criteria: 1.56/2** (Q1 corr. 2, Q2 build 2, Q3 tests 1.83, Q4 robust 1.17, Q5 maintain 1.29, Q6 repro 1.14).

| BL | Q1 corr. | Q2 build/run | Q3 tests | Q4 robust | Q5 maintain | Q6 repro | Conf |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BL-001` | 2 | NA | NA | NA | 2 | 2 | High |
| `BL-002` | 2 | 2 | 2 | 1 | 1 | 1 | High |
| `BL-003` | 2 | 2 | 1 | 1 | 1 | 1 | High |
| `BL-004` | 2 | 2 | 2 | 1 | 1 | 1 | High |
| `BL-005` | 2 | 2 | 2 | 1 | 1 | 1 | High |
| `BL-006` | 2 | 2 | 2 | 1 | 1 | 1 | Med |
| `BL-007` | 2 | 2 | 2 | 2 | 2 | 1 | High |

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** Top modern engines (Stockfish, Leela) are **3500+ Elo**. They rely on bitboards, SIMD, NNUE neural evaluation, SMP search, tablebases, and years of continuous tuning.

**Where this result sits.** ~1630 Elo ≈ solid intermediate club player — beats casual humans reliably, loses to strong humans. The engine plays **legal, tactically aware chess** with correct castling, en-passant, promotions, stalemate / threefold / 50-move rules, and sensible time use.

**Why the ceiling is out of reach here — honest constraints (not failures):**

- COBOL has **no pointers**, so bitboards require `USAGE COMP-5` + `FUNCTION MOD` for bit manipulation — orders of magnitude slower than native ints.
- **No native SIMD**; no multi-threading primitives in GnuCOBOL's runtime; search is strictly single-core.
- **No NNUE** evaluation — that would need a runtime linear-algebra layer and trained weights, both out of scope for a session.
- **No tablebase integration** (Syzygy / Gaviota) — the engine plays king-pawn endgames from its own eval, which is a known class of engine weakness.
- Active collaboration was **~15 h 30 m** across a 17-day calendar window; a single engine author hand-tuning at this level would typically iterate for months.

## 5. What's genuinely impressive (evidence-anchored)

- Full UCI command loop in COBOL, including clock-driven `go wtime/btime/winc/binc/movestogo` — this is the protocol a real tournament host speaks.
- Perft correctness was verified at depths 1–4 on startpos, kiwipete, EP-edge, and promotion positions — moving illegally is the #1 way a custom engine fails, and this one does not.
- Search includes techniques (LMR, NMP, aspiration, PVS, killer + history heuristics) that are standard in engines up to ~2400 Elo.
- Reproducible Elo measurement: PGN files + opening book + explicit cutechess match harness — the claim is **checkable**, not self-reported.

## 6. Honest gaps

- No NNUE (design choice, language constraint) — classical hand-tuned evaluation only.
- No SMP search — GnuCOBOL runtime doesn't expose threads.
- No pondering / multi-PV / Chess960 support.
- Elo ceiling of ~1700 for this engine class is a language-level constraint, not a bug.

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 2.8% (32 errors / 1155 tool outputs).
- Bug-report-style user prompts: 0.
- Redirect-style user prompts: 3.
- Share of active time spent on `bug_fix`: 0.3% (2 min of 931 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/chess-cobol-cc`
- Sessions: 1 (primary agent: Claude Code claude-opus-4-6)
- Git history: 1 commits available in `/Users/mathieuacher/SANDBOX/chess-cobol-cc/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/chess-cobol-cc/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/chess-cobol-cc__*.jsonl`.

## 8. Final take

**~1630 Elo ≈ solid intermediate club player — beats casual humans reliably, loses to strong humans.** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/chess-cobol-cc.json`, `output/backlogs/chess-cobol-cc/appendix.json` (when present), `output/complexity/chess-cobol-cc.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
