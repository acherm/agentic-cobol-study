## Domain coverage — which problem classes have been attempted by which agent?

Projects are grouped by *problem domain*. The **primary agent** per project is the one whose earliest non-analyst session kicked the project off (i.e. authored the PL-ROOT build prompt); later sessions from the other agent (ports, comparisons, analyst re-runs) are listed in parentheses. A domain is **covered by both agents** iff at least one project in the domain has Claude Code as primary AND at least one has Codex as primary.

| Domain | Description | Claude-Code projects (primary) | Codex projects (primary) | Both agents? |
|---|---|---|---|:---:|
| **COBOL compiler (self-hosted)** | A COBOL compiler written in COBOL that compiles non-trivial COBOL programs. | `cobol-compiler-cc` | `cobol-compiler-codex` | ✓ |
| **Chess engine** | UCI-speaking playable chess engine with Elo-measured strength. | `chess-cobol-cc` | `COBOL-chess` _(also: Claude Code)_ | ✓ |
| **Columnar compressor (COBPACK)** | Columnar packer / compressor for fixed-record COBOL data, with codec + trust-suite. | `cobol-compress-cobolcc` | `cobol-compress-codex` _(also: Claude Code)_ | ✓ |
| **Game / graphics framework** | pygame-style SDL2 framework for GnuCOBOL + pure-COBOL Flappy Bird (Claude Code replica, 5-step replay pack). | `cobol-pygame-cc` | `COBOL-pygame` _(also: Claude Code)_ | ✓ |
| **Payroll case-study** | Payroll system, 6-step canonical protocol incl. multi-file merge + behavior-preserving refactoring (Codex). | `cobol-jb-cc` | `cobol-jb-codex` | ✓ |
| **Real-time ray-casting FPS** | Ray-casting 3-D FPS (Doom-like) with real-time rendering. | `cobol-doom-cc` | `cobol-doom-codex` | ✓ |
| **SAT solver** | DIMACS CNF SAT solver with CDCL, cross-checked against MiniSat / SAT4J. | `SATCobol-cc` | `SATCobol-codex` | ✓ |
| **Small game (tic-tac-toe / game-of-15)** | Game-of-15 / tic-tac-toe with minimax tree search. | `cobol-tictactoe` | `game15-cobol-codex` | ✓ |

**Two-agent coverage: 8 / 8 domains.**

Domains already attempted by **both** Claude Code and Codex:

- COBOL compiler (self-hosted)
- Chess engine
- Columnar compressor (COBPACK)
- Game / graphics framework
- Payroll case-study
- Real-time ray-casting FPS
- SAT solver
- Small game (tic-tac-toe / game-of-15)

