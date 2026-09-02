# Coding Agents Can Develop COBOL Systems — study hub

Companion repository for the multi-case empirical study **“Coding Agents Can Develop COBOL Systems”** (2026): 16 non-trivial COBOL systems developed from
scratch by two frontier coding agents (Claude Code and Codex CLI) across 8
domain families, each family implemented by **both** agents (paired runs shared goals or
replay specifications to varying degrees). Validation evidence ranges from
independent differential checks and known values (differential execution
against GnuCOBOL, rated tournaments, cross-solver checks, byte-identical
replays) to property tests, demonstrations, and source inspection, and its
independence and coverage vary by system.

This hub contains the **analysis pipeline, derived datasets, session
material, and reproducible tables/figures**. Each system lives in its own
repository (below), preserved as the agent produced it.

## The 16 systems

| System | Repository | What it is | Dev agent (model) | Difficulty |
|---|---|---|---|---|
| `CHESS-COBOL-CLAUDE` | [agentic-chessengine-cobol-cc](https://github.com/acherm/agentic-chessengine-cobol-cc) | a UCI chess engine written in COBOL | Claude Code (`claude-opus-4-6`) | High |
| `CHESS-COBOL-CODEX` | [agentic-chessengine-cobol-codex](https://github.com/acherm/agentic-chessengine-cobol-codex) | a UCI chess engine written in COBOL, architecture-first (184-feature backlog) | Codex (`gpt-5.2`) | High |
| `COMPILER-COBOL-CLAUDE` | [agentic-cobol-compiler-cobolcc](https://github.com/acherm/agentic-cobol-compiler-cobolcc) | a COBOL compiler (and interpreter) written in COBOL, emitting C (self-hosting reported in the transcript, not independently reproduced) | Claude Code (`claude-opus-4-6`) | Very-High |
| `COMPILER-COBOL-CODEX` | [agentic-cobol-compiler-minicobc](https://github.com/acherm/agentic-cobol-compiler-minicobc) | minicobc, a COBOL-to-C compiler written in COBOL | Codex (`gpt-5.4`) | Very-High |
| `COMPRESS-COBOL-CLAUDE` | [agentic-cobol-compress-cc](https://github.com/acherm/agentic-cobol-compress-cc) | the COBPACK columnar compression container implemented in COBOL | Claude Code (`claude-opus-4-6`) | Low |
| `COMPRESS-COBOL-CODEX` | [agentic-cobol-compress](https://github.com/acherm/agentic-cobol-compress) | the COBPACK columnar compression container implemented in COBOL | Codex (`gpt-5.4`) | High |
| `DOOM-COBOL-CLAUDE` | [agentic-cobol-doom-cc](https://github.com/acherm/agentic-cobol-doom-cc) | a Doom-like ray-casting FPS with the game logic in COBOL (C sidecar paints the screen) | Claude Code (`claude-opus-4-7`) | Medium |
| `DOOM-COBOL-CODEX` | [agentic-cobol-doom-codex](https://github.com/acherm/agentic-cobol-doom-codex) | a Doom-like ray-casting FPS with the game logic in COBOL (12 COPY-book modules) | Codex (`gpt-5.4`) | Medium |
| `PAYROLL-COBOL-CLAUDE` | [agentic-cobol-payroll-cc](https://github.com/acherm/agentic-cobol-payroll-cc) | a payroll batch system built under an externally authored six-step protocol | Claude Code (`claude-sonnet-4-6`) | High |
| `PAYROLL-COBOL-CODEX` | [agentic-cobol-payroll-codex](https://github.com/acherm/agentic-cobol-payroll-codex) | a payroll batch system built under an externally authored six-step protocol | Codex (`gpt-5.4`) | High |
| `PYGAME-COBOL-CLAUDE` | [agentic-cobol-pygame-cc](https://github.com/acherm/agentic-cobol-pygame-cc) | a pygame-style graphical framework for GnuCOBOL (SDL2 C shim + copybook), including Flappy Bird in pure COBOL | Claude Code (`claude-opus-4-6`) | High |
| `PYGAME-COBOL-CODEX` | [agentic-cobol-pygame](https://github.com/acherm/agentic-cobol-pygame) | a pygame-style graphical framework callable from COBOL (COBOL to C to Python/SDL) | Codex (`gpt-5.2`) | Medium |
| `SAT-COBOL-CLAUDE` | [agentic-cobol-sat-cc](https://github.com/acherm/agentic-cobol-sat-cc) | a DIMACS SAT solver in COBOL (replication of the Codex sibling from replay prompts) | Claude Code (`claude-opus-4-6`) | Low |
| `SAT-COBOL-CODEX` | [agentic-cobol-sat-codex](https://github.com/acherm/agentic-cobol-sat-codex) | a CDCL SAT solver in COBOL (watched literals, VSIDS, restarts, backjumping) | Codex (`gpt-5.4`) | Medium |
| `TTTGAME15-COBOL-CLAUDE` | [agentic-cobol-game15tictactoe](https://github.com/acherm/agentic-cobol-game15tictactoe) | exhaustive enumeration and optimal play for the Game of 15 (isomorphic to tic-tac-toe) | Claude Code (`claude-opus-4-6`) | Medium |
| `TTTGAME15-COBOL-CODEX` | [agentic-cobol-game15-codex](https://github.com/acherm/agentic-cobol-game15-codex) | the Game-of-15 suite, cross-agent replication of the Claude Code sibling via replay prompts | Codex (`gpt-5.4`) | Medium |

System identifiers follow `FAMILY-COBOL-AGENT`. The repositories keep their
original folder/repo names, which key every artifact in `output/`.

## What is in this repository

- `scripts/` — the full analysis pipeline (`run_all.sh`, 8 stages: session
  parsing, per-turn SE-task classification, COBOL construct extraction,
  backlog harvesting, per-system metrics, difficulty index, reports).
  `session_roles.py` documents the deterministic development-vs-analyst
  session filter; `system_names.py` maps repository folders to system IDs.
- `output/` — committed derived artifacts: `sessions_all.json`, per-turn
  event streams (`turns/`), per-system metrics, complexity and git stats,
  difficulty index, cost metrics, reports, assessments, and the archived raw
  session logs (`raw_sessions/`, with `MANIFEST.csv`).
- `figures/`, `tables/` — the generated figures (PDF) and LaTeX tables, with
  `scripts/make_figures.py` and `scripts/gen_appendix_tables.py` to
  regenerate them from `output/`.
- `pilots/` — three motivating pilot sessions on non-frontier stacks
  (OpenCode with Gemma 4 and Qwen 3.6-plus, vibe with mistral-medium-3.5),
  logs and artifacts.
- `replications/` — the runbook and the externally authored six-step payroll
  protocol used for the canonical replications.
- `REPORT.md` — the generated top-level analysis report.

## Reproducing

Every number in the study reproduces from the committed artifacts:

```bash
bash scripts/run_all.sh          # stages 2+ re-run from committed inputs
python3 scripts/make_figures.py  # regenerates figures/ from output/
```

**Frozen inputs**: `output/sessions_all.json` and `output/turns/` are frozen.
18 of 38 study-relevant raw session logs were deleted by the agent CLI's
30-day local retention before archiving (20 survive). Re-running stage 1
would silently rebuild from the surviving raw logs only. The archived survivors are in
`output/raw_sessions/`. See the study's data-provenance appendix.

## Replay packs

Each system repository ships its replay pack (`REPLAY_PROMPTS.md` or
equivalent): the opening prompt with the COBOL-boundary constraint, expected
deliverables, and oracles per activity, so a third agent can be run
activity-by-activity against the same specifications.

## License

MIT (see `LICENSE`), covering the analysis code and, for simplicity, the
committed datasets and generated reports in this repository. Each system
repository carries its own MIT license.

## Citation

Paper under submission (arXiv preprint forthcoming). Until then, please cite
this repository.
