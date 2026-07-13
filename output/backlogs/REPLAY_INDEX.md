# Replay Prompts — index

One replay package **per system family**. Each `REPLAY_PROMPTS.md` is a sequence of
self-contained, copy-pasteable prompts (the *what*, not the *how*) with an explicit
**Verification** block per step (the "things to check"). One coding agent per family
is sufficient; Codex is preferred where its raw session log survived intact.

## How to read the "Mode" column

- **Spec-driven** — a fixed external oracle and a milestone sequence; the replay is a
  *faithful recipe* and replaying the steps reproduces the system.
- **Objective-driven** — the goal was a moving target pursued through contingent
  human–agent loops; the replay is an *idealized linearization*. Replaying it
  deterministically need not reproduce the trajectory, so these files also ship a
  verbatim **"What actually happened"** prompt trace and mark their open-ended steps
  `[objective loop]` (run until a stopping oracle is met). See the paper's
  *Reusability of the study* (spec-driven ↔ objective-driven axis).

## The packages

| Family | System (dir) | Agent | Raw log | Mode | End state / reproduction oracle |
|---|---|---|---|---|---|
| chess | [`COBOL-chess`](COBOL-chess/REPLAY_PROMPTS.md) | Codex | present | **objective-driven** | `cobochess` UCI engine — exact **perft** node counts + legality; strength via **Stockfish/Elo** harness (~1600) |
| compiler | [`cobol-compiler-codex`](cobol-compiler-codex/REPLAY_PROMPTS.md) | Codex | present | **objective-driven** | `minicobc` COBOL-in-COBOL — **differential vs GnuCOBOL** + **self-bootstrap** |
| SAT | [`SATCobol-codex`](SATCobol-codex/REPLAY_PROMPTS.md) | Codex | present | spec-driven | `cobsat` — DIMACS + model-verify; **MiniSat / SAT4J** cross-check |
| compress | [`cobol-compress-codex`](cobol-compress-codex/REPLAY_PROMPTS.md) | Codex | present | spec-driven | `cobpack` columnar packer — round-trip + determinism; TRUST-suite parity |
| doom | [`cobol-doom`](cobol-doom/REPLAY_PROMPTS.md) | Codex | present | spec-driven | COBOL Doom-like — playable; module/COPY-book layout |
| pygame | [`COBOL-pygame`](COBOL-pygame/REPLAY_PROMPTS.md) | Codex | present | spec-driven | "pygame-for-COBOL" framework — SDL2 smoke under `SDL_VIDEODRIVER=dummy` |
| 15 / tic-tac-toe | [`cobol-tictactoe`](cobol-tictactoe/REPLAY_PROMPTS.md) | Claude Code | **deleted** | spec-driven | Game-of-15 / tic-tac-toe executables — minimax parity; replay parity (Codex sibling: `game15-cobol-codex`) |
| payroll | [`cobol-jb`](cobol-jb/REPLAY_PROMPTS.md) | Claude Code | **deleted** | spec-driven | COBOL payroll case-study — verification grid |

**Raw log** = whether the underlying agent transcript still exists on disk (see
[Appendix "Data provenance"](../../REPORT.md) / `output/raw_sessions/`). The two
`deleted`-raw packages were authored *before* their Claude Code logs aged out and
cannot be regenerated from raw; the six `present` packages remain re-derivable.

For per-system ground truth (features actually built, commits, benchmark numbers,
autonomous decisions), each family dir also carries `SPECIFICATION_BACKLOG.md`.
