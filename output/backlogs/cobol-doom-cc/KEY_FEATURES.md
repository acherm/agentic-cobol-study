# Key Features -- cobol-doom-cc

## Preamble
Doom-like FPS built by Claude Code with pure terminal rendering. Entire pipeline (DDA raycasting, truecolor framebuffer, sprite projection, weapon HUD, minimap) in COBOL. No C rendering code — only POSIX write()/read() syscalls.

## Ranked table

| # | Title | Class | Depth | Effort | Score |
|---|---|---|---|---|---|
| 1 | DDA raycaster with truecolor framebuffer, entirely in COBOL (pd-render.cpy, 814 LOC) | LNG+ALG | 3 | 3 | 7.5 |
| 2 | POSIX syscall I/O bypass (write/read replacing DISPLAY/CBL_READ_KBD_CHAR) | LNG+SYS | 3 | 2 | 6.0 |
| 3 | Enemy AI, sprites, z-buffered projection (7 enemies, 2 kinds, inverse camera matrix) | DOM+ALG | 2 | 2 | 4.0 |
| 4 | Multi-level system with data-driven level definitions (3 levels, 2 goal types) | DOM | 2 | 2 | 4.0 |
| 5 | Pickups, HUD, ammo/armor/weapon system (2 weapons, 3 pickup kinds) | DOM | 2 | 2 | 4.0 |
| 6 | Weapon HUD sprites + creature silhouettes (structured pixel art in COBOL) | DOM+LNG | 2 | 1 | 3.0 |
| 7 | 7-COPY-book modular refactoring (verified byte-identical output) | INF+LNG | 2 | 1 | 3.0 |
| 8 | Top-down 2D grid walker (foundation) | DOM | 1 | 1 | 1.5 |
| 9 | Demo script (regression harness) | VER+INF | 1 | 1 | 1.5 |
| 10 | Arrow key ESC sequence parser (CSI + SS3 modes) | DOM | 1 | 1 | 1.5 |

## Significance profile

| Class | Count |
|---|---|
| LNG | 2 |
| DOM | 5 |
| INF | 1 |
| VER | 1 |
| ALG | 0 (+2 sec) |

## Verdict
**Language-achievement-centric with DOM superstructure.** Entire rendering pipeline runs in COBOL paragraphs with zero C code. The POSIX syscall bypass is the enabling language-level workaround.
