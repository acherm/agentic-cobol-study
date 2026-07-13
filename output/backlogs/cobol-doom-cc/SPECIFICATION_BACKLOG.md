# Specification Backlog -- cobol-doom-cc

**Agent:** Claude Code (claude-opus-4-7, v2.1.112) | **Session:** 01bcb47f (2026-04-17/18)

## Steps

### SB-001 — Top-down 2D grid walker (commit 75c27ad)
20x40 grid, WASD, wall collision, ANSI-home redraw. stty + CBL_READ_KBD_CHAR for raw input.

### SB-002 — Fix invisible output (commit c0b9bc7)
Bypass GnuCOBOL DISPLAY via POSIX write() to fd 1. CR+LF for alignment.

### SB-003 — DDA raycaster with minimap (commit 8a47a28)
DDA grid-walk per column using FUNCTION COS/SIN. COMP-2 player position. Minimap overlay.

### SB-004 — Unicode half-block + truecolor rendering
Unicode U+2580 with 24-bit RGB ANSI codes. Each cell = 2 vertical pixels.

### SB-005 — Arrow key support (commit 9d2d9c4)
ESC[A-D + ESC O A-D parsing. Removed alt-screen. Per-row frame writes.

### SB-006 — Enemies and combat (commit 5ed8682)
7 enemies, 2 kinds (IMP/DEMON). Chase AI. Sprite projection via inverse camera matrix. Per-column z-buffer. SPACE fires weapon.

### SB-007 — Pickups, HUD, weapons
8 pickups (health/ammo/armor). HUD strip. 2 selectable weapons (pistol/shotgun).

### SB-008 — POSIX read() for input (commit f0418eb)
Bypassed CBL_READ_KBD_CHAR (ncurses) with direct read() syscall.

### SB-009 — 3 levels + progression
3 distinct levels, goal types (kill-all / reach-exit), summary/win/death screens.

### SB-010 — Level-select menu (commit 93b93fa)
Startup menu, levels 1-3, Q to exit.

### SB-011 — Demo script
demo.sh (~118 LOC) feeding scripted keystrokes. Makefile targets: demo, play, clean.

### SB-012 — Weapon sprites + creature silhouettes (commit 69ab81f)
Structured ASCII art: pistol, shotgun. Enemy silhouettes with tapered oval, glowing eye dots.

### SB-013 — 7-COPY-book refactoring (commit e9854b2)
85-line main + 7 copybooks. Byte-identical output verified. Demo still passes.

## Cross-agent note

| Dimension | cobol-doom-cc | cobol-doom-codex |
|---|---|---|
| Rendering | Pure terminal (POSIX write + 24-bit ANSI + Unicode) | SDL2 window (1280x720) |
| C code | None (only POSIX syscalls) | sdl_bridge.c + sdl_sprite.c (1839 LOC) |
| COPY books | 7 (1781 LOC) | 11 (2078 LOC) |
| DDA raycaster | COBOL (pd-render.cpy, 814 LOC) | COBOL (gridwalker_raycast.cpy, 181 LOC) |
| Sprites | Procedural Unicode art in COBOL | BMP files loaded by SDL |
| Cost | $367 | $11 |
