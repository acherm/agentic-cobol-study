# SPECIFICATION BACKLOG — cobol-doom-codex

**Agent:** Codex (o4-mini) | **Session:** 019d9c4b (2026-04-17/18)

## Steps

### Step 1 — Top-Down Grid Walker (BL-001)
Probe phase (4 throwaway programs testing input methods) then 28x22 grid with REDEFINES, WASD/arrow movement, ANSI redraw. Commit `8127df8`.

### Step 2 — Terminal Alignment Fix (BL-002)
`stty raw` → `stty -icanon -echo` to preserve output post-processing. Commit `ec5133e`.

### Step 3 — First-Person Raycaster + SDL2 Bridge (BL-003)
Python pygame rejected by user ("faking COBOL"). Agent pivoted to SDL2 C bridge (`sdl_bridge.c`). DDA raycaster runs in COBOL (`FUNCTION SIN/COS`, `COMP-2`). Commit `4219ca2`.

### Step 4 — Enemies and Combat (BL-004)
10-slot enemy table, 2 types (Imp/Soldier), AI chase, contact damage, health/armor/ammo, weapon firing with raycasted hit detection.

### Step 5 — Levels, Demo, Level Selection (BL-005)
`levels.cpy` with 3 level definitions, objectives (exit-reach / clear-all), summary/intermission/win screens, `demo.c` scripted driver, pickups.

### Step 6 — BMP Sprite Graphics (BL-006)
BMP loading in SDL bridge, textured walls/enemies/pickups, improved HUD, level theming.

### Step 7 — Modular Refactoring into 11 COPY Books (BL-007)
Monolithic 1637 LOC → thin shell + 10 `gridwalker_*.cpy` + `levels.cpy`. Three smoke tests passing post-refactor.

## Cross-agent note

| Dimension | cobol-doom-cc (Claude Code) | cobol-doom-codex (Codex) |
|---|---|---|
| Rendering | Terminal (ANSI escapes) | SDL2 window (1280x720) |
| DDA raycaster | C (`terminal-io.c`) | **COBOL** (`gridwalker_raycast.cpy`) |
| Trig | Integer sin/cos ×10000 in C | `FUNCTION SIN/COS` (COMP-2) in COBOL |
| COPY books | 7 | 11 |
| Sprites | Procedural Unicode art | BMP files loaded by SDL |
| Main COBOL | `walker.cob` + 7 cpy (~1869 LOC) | `gridwalker.cob` shell + 11 cpy (~1647 LOC) |
