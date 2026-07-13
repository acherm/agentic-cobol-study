# Assessment — `TTTGAME15-COBOL-CLAUDE` (folder `cobol-tictactoe`) — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> **Three playable programs**: `game15` (interactive play), `game015tree` / `game15tree` (minimax tree search), `gameN` (N-variant). All compile and run; the tree-search variants solve the game optimally against a human.

> **A clean, smooth success.** Game of 15 is isomorphic to tic-tac-toe (3×3 magic square); the interesting engineering is doing recursion in COBOL — which the delivered programs accomplish via `PERFORM` with level-indexed stack frames. Two sessions, ~3 active hours end-to-end, 1.4 % tool-output error rate — among the smoothest projects in the set (matches the user's recollection of 'it just worked').

**Difficulty (auto-labelled):** Medium (idx 0.29). **Active collaboration time:** 2 h 4 m. **Sessions:** 2. **Backlog entries discovered:** 31. **Git commits:** 5.

## 1. Contract — what was asked

Implement the Game of 15 (say numbers 1..9, first to a triple summing to 15 wins) and its tree-search AI in COBOL. Add tic-tac-toe variants and multi-size boards.

Opening user prompt (verbatim, truncated):

```
The game of 15 is defined as follows: Two players in turn say a number between one and nine. A particular number may not be repeated. The game is won by the player who has said three numbers whose sum is 15. If all the numbers are used and no one gets three numbers that add up to 15 then the game is a draw. Write a COBOL program (using GNUCobol) that computes the number of possible games in the game of 15...
```

## 2. Delivered — externally-observable evidence

**Three playable programs**: `game15` (interactive play), `game015tree` / `game15tree` (minimax tree search), `gameN` (N-variant). All compile and run; the tree-search variants solve the game optimally against a human.

**Executables present in `SANDBOX/cobol-tictactoe/`** (at least *something* built):

- `game015` (53 KB)
- `game015tree` (86 KB)
- `game15` (52 KB)
- `game15tree` (86 KB)
- `gameN` (71 KB)

**COBOL surface exercised.** 5 COBOL file(s), 1,537 code lines, 34 paragraphs (≈ function-like units), 5 sections, mastery score **28** distinct constructs across **8/10** capability categories.

**Backlog (auto-mined).** 31 `F-###` / `SB-###` / `S#-##` entries in the harvested / subagent-generated `SPECIFICATION_BACKLOG.md`. Prompts also produced 70 sub-request bullets; git history carries 5 commits.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

_No rubric available for this project (analyst subagent did not run or used a pre-existing summary format)._

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** Perfect-play solvers exist trivially in one-liners in languages with dynamic dispatch and recursion stacks. 'Ceiling' here is more about elegance than strength.

**Where this result sits.** **A clean, smooth success.** Game of 15 is isomorphic to tic-tac-toe (3×3 magic square); the interesting engineering is doing recursion in COBOL — which the delivered programs accomplish via `PERFORM` with level-indexed stack frames. Two sessions, ~3 active hours end-to-end, 1.4 % tool-output error rate — among the smoothest projects in the set (matches the user's recollection of 'it just worked').

**Why the ceiling is out of reach here — honest constraints (not failures):**

- Game theory is trivial for 3×3 — the only dimension to scale is board size (gameN).

## 5. What's genuinely impressive (evidence-anchored)

- **Correct optimal play** verified interactively (minimax with no ties when one side should win).
- Recursive tree search in COBOL using `PERFORM` with level-tracked stack indexing — the right idiom for a language without a call stack.
- Multiple variants in one codebase: `game15`, `game015tree`, `game15tree`, `gameN`, each a small, composable program.
- Smooth collaboration: **2.8 % tool-output error rate**, one of the lowest in the project set — matches the user's recollection of the project feeling easy.

## 6. Honest gaps

- I/O polish is minimal (plain text prompts, no undo).
- No network play / no persistence.

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 1.5% (1 errors / 67 tool outputs).
- Bug-report-style user prompts: 0.
- Redirect-style user prompts: 1.
- Share of active time spent on `bug_fix`: 0.0% (0 min of 124 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/cobol-tictactoe`
- Sessions: 2 (primary agent: Claude Code claude-opus-4-6)
- Git history: 5 commits available in `/Users/mathieuacher/SANDBOX/cobol-tictactoe/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/cobol-tictactoe/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/cobol-tictactoe__*.jsonl`.

## 8. Final take

****A clean, smooth success.** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/cobol-tictactoe.json`, `output/backlogs/cobol-tictactoe/appendix.json` (when present), `output/complexity/cobol-tictactoe.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
