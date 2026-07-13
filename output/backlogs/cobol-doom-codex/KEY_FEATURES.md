# Key features — cobol-doom-codex

## Preamble
Doom-like FPS built by Codex with SDL2 graphical rendering. DDA raycaster runs in COBOL (not C). 11 COPY books. BMP sprites.

## Ranked table

| # | Title | Class | Depth | Effort | Score |
|---|---|---|---|---|---|
| 1 | DDA raycasting engine in COBOL (FUNCTION SIN/COS, COMP-2, gridwalker_raycast.cpy) | ALG+LNG | 3 | 2 | 6.0 |
| 2 | SDL2 C bridge + BMP sprite asset pipeline (sdl_bridge.c, *.bmp) | SYS+DOM | 3 | 3 | 7.5 |
| 3 | 11-copybook modular COBOL architecture (thin shell + 10 domain books + levels.cpy) | LNG+INF | 2 | 2 | 4.0 |
| 4 | Enemy system and combat mechanics (10-slot table, 2 types, AI, hit detection) | DOM | 2 | 2 | 4.0 |
| 5 | Multi-level system with level definitions in COPY book (3 levels, objectives) | DOM | 2 | 2 | 4.0 |
| 6 | COBOL as host for real-time 60 fps game loop (CBL_GC_NANOSLEEP, COMP-2 state) | LNG | 2 | 2 | 4.0 |
| 7 | Scripted demo + headless test infrastructure (demo.c, SDL dummy driver) | VER+SYS | 2 | 1 | 3.0 |
| 8 | Cross-toolchain Makefile (GnuCOBOL + gcc + SDL2) | INF | 1 | 1 | 1.5 |
| 9 | Runtime exploration + input-method prototyping (4 probe programs) | LNG | 1 | 1 | 1.5 |
| 10 | Terminal alignment bugfix (stty -icanon vs stty raw) | LNG | 1 | 0 | 1.0 |

## Significance profile

| Class | Count |
|---|---|
| LNG | 4 |
| SYS | 1 |
| ALG | 1 |
| DOM | 2 |
| VER | 1 |
| INF | 1 |

## Verdict
**Hybrid — LNG-centric with SYS seam.** DDA raycaster in COBOL (not C) is the strongest "COBOL does the computation" claim. SDL2 bridge + BMP sprites distinguish this from the terminal-based CC sibling.
