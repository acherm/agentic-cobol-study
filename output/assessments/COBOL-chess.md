# Assessment — `CHESS-COBOL-CODEX` (folder `COBOL-chess`) — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> A Codex-built chess engine (cobochess) whose **F-### backlog enumerates 184 features across 27 phases** (scaffold → board / FEN / attack / move gen / make-unmake → perft → UCI → time utility → eval rewrite for pawn structure / piece placement / king safety → LMR / NMP / aspiration / PVS / LMP / mate-distance pruning → Zobrist + TT → opening-book PGN). The repository carries a formal `ARCHITECTURE.md` and `SPECIFICATION.md` in addition to the backlog.

> Substantial engineering depth but **no Elo measurement preserved in this folder** (cutechess results live in sibling `chess-cobol-cc`). Judged on code / feature breadth, this is a thorough, by-the-book engine.

**Difficulty (auto-labelled):** High (idx 0.74). **Active collaboration time:** 4 h 58 m. **Sessions:** 3. **Backlog entries discovered:** 184. **Git commits:** 2.

## 1. Contract — what was asked

Second chess-engine attempt, Codex-led, with explicit architecture + specification backlog.

Opening user prompt (verbatim, truncated):

```
I want to build a chess engine in COBOL (GNUCobol)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels
```

## 2. Delivered — externally-observable evidence

A Codex-built chess engine (cobochess) whose **F-### backlog enumerates 184 features across 27 phases** (scaffold → board / FEN / attack / move gen / make-unmake → perft → UCI → time utility → eval rewrite for pawn structure / piece placement / king safety → LMR / NMP / aspiration / PVS / LMP / mate-distance pruning → Zobrist + TT → opening-book PGN). The repository carries a formal `ARCHITECTURE.md` and `SPECIFICATION.md` in addition to the backlog.

**COBOL surface exercised.** 16 COBOL file(s), 3,359 code lines, 70 paragraphs (≈ function-like units), 30 sections, mastery score **40** distinct constructs across **10/10** capability categories.

**Backlog (auto-mined).** 184 `F-###` / `SB-###` / `S#-##` entries in the harvested / subagent-generated `SPECIFICATION_BACKLOG.md`. Prompts also produced 92 sub-request bullets; git history carries 2 commits.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

_No rubric available for this project (analyst subagent did not run or used a pre-existing summary format)._

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** Same as `chess-cobol-cc`: 3500+ Elo with NNUE + SMP + tablebases.

**Where this result sits.** Substantial engineering depth but **no Elo measurement preserved in this folder** (cutechess results live in sibling `chess-cobol-cc`). Judged on code / feature breadth, this is a thorough, by-the-book engine.

**Why the ceiling is out of reach here — honest constraints (not failures):**

- Same COBOL language constraints as `chess-cobol-cc`.
- Codex session concentrated on **feature coverage and documentation rigor** rather than Elo tuning — the ~10 h active time here is a fraction of a real tuning campaign.

## 5. What's genuinely impressive (evidence-anchored)

- **184-entry phased backlog** with explicit evidence pointers — one of the most disciplined specification records in the set.
- Architecture and specification are spec'd **before** code in several phases — this is a professional workflow, not just vibe-coding.
- COBOL idioms deployed include `LOCAL-STORAGE SECTION` for recursion-safe perft, `EXTERNAL` shared singleton for Zobrist tables, `UNSTRING … DELIMITED BY SPACE` for FEN parsing — these are the right tools for the job.

## 6. Honest gaps

- No `run_n` Elo evidence in this folder (use sibling `chess-cobol-cc` for that).
- Deep game-play correctness is inferred from perft, not from tournament results here.

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 3.4% (66 errors / 1935 tool outputs).
- Bug-report-style user prompts: 10.
- Redirect-style user prompts: 0.
- Share of active time spent on `bug_fix`: 2.4% (7 min of 298 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/COBOL-chess`
- Sessions: 3 (primary agent: Codex gpt-5.2)
- Git history: 2 commits available in `/Users/mathieuacher/SANDBOX/COBOL-chess/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/COBOL-chess/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/COBOL-chess__*.jsonl`.

## 8. Final take

**Substantial engineering depth but **no Elo measurement preserved in this folder** (cutechess results live in sibling `chess-cobol-cc`).** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/COBOL-chess.json`, `output/backlogs/COBOL-chess/appendix.json` (when present), `output/complexity/COBOL-chess.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
