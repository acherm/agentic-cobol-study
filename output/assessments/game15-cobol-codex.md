# Assessment — `game15-cobol-codex` — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> Codex-built playable programs: `game15` (interactive), `game15_tree` (minimax), `gameN.cob` (parameterized variant), plus `game015.cob` and `game015tree.cob` for the 0.15-variant — mirroring the file set of the Claude-Code sibling.

> **Cross-agent replication** of the small-game domain — built from the exemplar step-wise replay-prompt pack. The 2-agent coverage of this domain is now complete.

**Difficulty (auto-labelled):** Medium (idx 0.26). **Active collaboration time:** 0 h 33 m. **Sessions:** 1. **Backlog entries discovered:** 35. **Git commits:** 4.

## 1. Contract — what was asked

Codex replica of the Game-of-15 / tic-tac-toe domain — same contract as `cobol-tictactoe`, built following the exemplar `cobol-tictactoe/REPLAY_PROMPTS.md`.

Opening user prompt (verbatim, truncated):

```
Write a COBOL program (GnuCOBOL) for the "Game of 15". Rules: Two players alternate picking a number from {1, 2, ..., 9}. A number cannot be picked twice. A player wins when any three of their chosen numbers sum to exactly 15. If all nine numbers are picked and no player has won, the game is a draw. The program should enumerate every possible game (every legal sequence of moves to completion) and report: Player 1 wins (player who picks first) Player 2 wins Draws Total games
```

## 2. Delivered — externally-observable evidence

Codex-built playable programs: `game15` (interactive), `game15_tree` (minimax), `gameN.cob` (parameterized variant), plus `game015.cob` and `game015tree.cob` for the 0.15-variant — mirroring the file set of the Claude-Code sibling.

**Executables present in `SANDBOX/game15-cobol-codex/`** (at least *something* built):

- `game15` (69 KB)
- `game15_tree` (86 KB)

**COBOL surface exercised.** 5 COBOL file(s), 2,264 code lines, 88 paragraphs (≈ function-like units), 5 sections, mastery score **35** distinct constructs across **9/10** capability categories.

**Backlog (auto-mined).** 35 `F-###` / `SB-###` / `S#-##` entries in the harvested / subagent-generated `SPECIFICATION_BACKLOG.md`. Prompts also produced 0 sub-request bullets; git history carries 4 commits.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

**Mean score across 6 BLs and 6 criteria: 1.78/2** (Q1 corr. 2, Q2 build 2, Q3 tests 1.33, Q4 robust 1.67, Q5 maintain 1.83, Q6 repro 1.83).

| BL | Q1 corr. | Q2 build/run | Q3 tests | Q4 robust | Q5 maintain | Q6 repro | Conf |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BL-01` | 2 | 2 | 1 | 1 | 2 | 2 | High |
| `BL-02` | 2 | 2 | 1 | 1 | 1 | 2 | High |
| `BL-03` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-04` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-05` | 2 | 2 | 1 | 2 | 2 | 2 | High |
| `BL-06` | 2 | 2 | 1 | 2 | 2 | 1 | Medium |

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** Trivial — Game-of-15 is a solved 3×3 game; ceiling is elegance, not strength.

**Where this result sits.** **Cross-agent replication** of the small-game domain — built from the exemplar step-wise replay-prompt pack. The 2-agent coverage of this domain is now complete.

**Why the ceiling is out of reach here — honest constraints (not failures):**

- The domain is inherently shallow — perfect play is computable in microseconds.

## 5. What's genuinely impressive (evidence-anchored)

- **Closes the 2-agent coverage gap** for the small-game / minimax domain.
- Built directly from a step-wise replay-prompt pack — a portability test for the methodology.
- File naming mirrors the sibling (`game15` / `game015` / `gameN`), suggesting the replay prompts conveyed the intended shape.

## 6. Honest gaps

- Side-by-side comparison with `cobol-tictactoe` pending.

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 3.5% (6 errors / 173 tool outputs).
- Bug-report-style user prompts: 0.
- Redirect-style user prompts: 1.
- Share of active time spent on `bug_fix`: 0.1% (0 min of 33 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/game15-cobol-codex`
- Sessions: 1 (primary agent: Codex gpt-5.4)
- Git history: 4 commits available in `/Users/mathieuacher/SANDBOX/game15-cobol-codex/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/game15-cobol-codex/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/game15-cobol-codex__*.jsonl`.

## 8. Final take

****Cross-agent replication** of the small-game domain — built from the exemplar step-wise replay-prompt pack.** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/game15-cobol-codex.json`, `output/backlogs/game15-cobol-codex/appendix.json` (when present), `output/complexity/game15-cobol-codex.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
