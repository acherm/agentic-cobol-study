# Key features — `cobol-doom`

## Preamble

The project was asked, in a single five-word prompt ("Write a Doom game in COBOL"), to produce a
Doom-style first-person shooter inside a language — COBOL — that has no graphics primitives, no
real-time scheduling story, no pointers, and was designed for batch record processing. What
actually shipped is a real-time, 60 fps, DDA ray-casting FPS with enemies, pickups, doors,
three levels, difficulty tiers, an intermission screen, a PTY-driven self-play demo, and an
independent Java port. The COBOL file (`doom.cob`, ~1,076 LOC, 24 paragraphs) drives the main
loop and holds all game state; a C sidecar (`terminal-io.c`) provides the terminal I/O, DDA
ray tracer, textures, sprites and HUD rasterizer; `demo.c` is a `forkpty()` harness that
replays scripted keystrokes. "Key features" here are groups of ≥ depth-1 work items consolidated
from the 139-entry `SPECIFICATION_BACKLOG.md`; pure parameter tuning (Step 4) and individual
ASCII-art sprites are folded into their parent groups rather than ranked on their own.

## Ranked table

| # | SB id range | Title | Class | Depth | Effort | Score | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | S1-01, S1-14..S1-30, S2-01..S2-05, S7-13..S7-19, S7-22..S7-27 | **COBOL as host for a real-time interactive loop** — player state, state machine (Title / Playing / Dead / Win / Intermission), WASD + arrow input dispatch, wall-collision, weapon logic, enemy AI, sprint, difficulty tiers, per-frame `PERFORM` cadence, all in `PIC S9(9) COMP-5` integer arithmetic with no floating point and no pointers | **LNG** (sec. DOM) | 3 | 3 | 7.5 | `doom.cob:1-1076` (24 paragraphs, sections `GAME-LOOP`, `HANDLE-INPUT`, `UPDATE-ENEMIES`, `SETUP-LEVEL`, `START-NEW-GAME`) |
|   | _Significance note_ | Not just-an-algorithm. COBOL is a batch record-processing language; hosting a 60 fps game loop with state-machine dispatch and mutable integer physics in it is the out-of-paradigm achievement that makes the whole project interesting. | | | | | |
| 2 | S1-01, S2-01..S2-05, S3-03, S3-04 (settter pattern), S7-24, S7-30 | **COBOL ↔ C FFI boundary with setter-function ABI workaround** — `CALL … BY VALUE / BY REFERENCE` into C, `COMP-5` as the shared wire type, `RETURNING` of C results (`get_time_ms`, `read_key`, `check_los_c`), plus `set_hud_*` / `set_enemy_data` / `set_pickup_data` / `set_intermission_data` as a chunked-argument workaround for the ARM64 >8-param ABI limit | **SYS** (sec. LNG) | 3 | 2 | 6.0 | `terminal-io.c:75-146`, `doom.cob:712-817` (CALLs), `SPECIFICATION_BACKLOG.md` S2-03 citing [T:msg_156] |
|   | _Significance note_ | The engineering lives at the boundary. Two languages with incompatible ABIs (GnuCOBOL calling convention + macOS/ARM64 param limit) are glued into one process that exchanges per-frame state ~60 times a second without copying or marshalling layers. | | | | | |
| 3 | S3-01, S3-02, S3-03, S3-08, S3-09 | **DDA ray-caster with z-buffer and side shading** — replaces Step-1 naive per-pixel step-march; one ray per column, exact grid intersections, per-column depth buffer feeding sprite sorting, NS/EW side-shading, distance fog | **ALG** (sec. PRF) | 2 | 2 | 4.0 | `terminal-io.c:190-219` (`cast`), `terminal-io.c:220-225` (`zbuf`), backlog note "replaced in Step 3" at `[T:msg_191, msg_232]` |
|   | _Significance note_ | This one IS textbook — DDA grid-traversal ray-casting is Lode Vandevenne / Wolfenstein-era folklore. What raises it above a pure ALG row is that it's the second iteration of a measurably faster engine after the Step-3 rewrite (an explicit PRF loop), and that its output feeds a COBOL-driven loop, not a C `main`. | | | | | |
| 4 | S3-04..S3-12, S5-01..S5-10, S5-22, S3-18 | **Unicode half-block + 24-bit-true-color terminal framebuffer with Doom-style textures** — `▀` (U+2580) stacking for 2× vertical resolution, 1 MB pre-allocated output buffer with minimised ANSI state transitions, `fg_rgb`/`bg_rgb` RGB escape emitter, procedural STARTAN / TEKWALL / door / hell-marble textures, fog, gradient sky, checkered perspective floor, minimap, flickering-lights hash noise | **DOM** (sec. PRF) | 2 | 2 | 4.0 | `terminal-io.c:149-188` (buffer + color math), `terminal-io.c:229-454` (tex_startan / tex_techwall / tex_door / tex_hell / floor_color / ceiling_color) |
|   | _Significance note_ | Domain modelling of "what Doom looks like, expressed as monospace cells" — not an algorithm, but a hand-tuned sampled-texture model reducing Doom's palette and textures to values that survive through an ANSI terminal emulator at 60 Hz. | | | | | |
| 5 | S7-13..S7-19, S7-14 (SETUP-LEVEL), S7-15..S7-17 | **Multi-level system with per-level spawn tables in COBOL** — three map templates (L1 UAC Base, L2 Industrial, L3 Hell) held as 24-line `01 Lx-MAP-DATA` groups with `REDEFINES` onto a linear `X(576)` buffer, `SETUP-LEVEL` copies the template and calls level-specific `SPAWN-ENEMIES-Lx` / `PLACE-PICKUPS-Lx` paragraphs, intermission → level+1 progression, end-of-level-3 win state | **DOM** | 2 | 2 | 4.0 | `doom.cob:78-160` (L1/L2/L3 maps), `doom.cob:272-710` (SETUP-LEVEL + spawn tables), `doom.cob:790-813` (intermission → advance) |
|   | _Significance note_ | Classic domain modelling: Doom "level → monsters → pickups → exit" encoded as COBOL data groups + paragraph dispatch. The `REDEFINES` trick is how you get O(1) tile lookup in a language that hates pointers. | | | | | |
| 6 | S3-13..S3-17, S5-11..S5-19, S7-09..S7-12 | **Sprite pipeline: depth-sorted enemies + pickups + weapon overlay** — humanoid Imp / Pinky / Baron silhouettes with per-part colouring and damage tint, pickup sprites (green cross, yellow box, blue shield) with bobbing, weapon overlays (pistol / shotgun / plasma) with bob + muzzle flash, unified `sprites[]` list sorted back-to-front against the column z-buffer (`spr_cmp`) | **DOM** (sec. ALG) | 2 | 2 | 4.0 | `terminal-io.c:456-464` (spr_cmp), `terminal-io.c:466-602` (draw_enemy), `terminal-io.c:604-711` (draw_pickup), `terminal-io.c:713-811` (draw_weapon) |
|   | _Significance note_ | The painter's-algorithm / z-buffer-test sort is standard, but the actual art — stitching Doom monsters and UAC health-packs out of coloured unicode blocks — is domain work (what Doom is) more than algorithm work. | | | | | |
| 7 | S7-01..S7-08, S7-20, S7-21, S7-29..S7-31 | **Doom mechanics stack: doors, pickups, armor, intermission** — door tiles `D` in the map with F-key open mechanic (range + facing check) that mutates the map to walkable, up-to-20 pickup table with stimpack / clip / armor semantics and proximity collection, armor absorbs 1/3 incoming damage, end-of-level intermission with kill% / item% / time passed via `set_intermission_data` and rendered as progress bars | **DOM** | 2 | 2 | 4.0 | `doom.cob:185-204` (pickup table), `doom.cob:985-1085` (OPEN-DOOR, CHECK-PICKUPS, COLLECT-PICKUP), `terminal-io.c:1293-1387` (show_intermission_c) |
|   | _Significance note_ | Pure DOM: faithful encoding of Doom's gameplay vocabulary (doors / pickups / armor / intermission) on top of the ray-casting substrate. None of it is algorithmically novel, but all of it composes on top of features 1–3 and is meaningless without them. | | | | | |
| 8 | Whole Java port: `GameApplication.java`, `GameLogic.java`, `GameRenderer.java`, `LevelDefinition.java`, `LevelRepository.java`, `WorldMap.java`, `GameState.java`, `InputState.java`, `Enemy.java`, `Pickup.java`, `RayHit.java`, `GameMode.java`, `GameConstants.java`, `GameLabels.java`, `GamePanel.java`, `CobolDoom.java` — plus `Makefile` `java` / `run-java` / `java-smoke` targets | **Independent Java re-implementation as a cross-language oracle** — Swing / `Graphics2D` renderer with per-pixel ray-casting against the same map strings, same level definitions, same three levels, same enemy/pickup semantics as the COBOL build; smoke-test Make target for headless validation | **CMP** (sec. VER) | 3 | 3 | 7.5 | `GameLogic.java:1-60+` (mirrors COBOL state machine), `GameRenderer.java:26-60+` (DDA + Swing), `LevelRepository.java:1-48` (same maps as `doom.cob`), `Makefile:25-46` (`java`, `run-java`, `java-smoke`) |
|   | _Significance note_ | CMP by definition: the Java port has no value unless features 1–7 exist and are understood well enough to be re-encoded in a second language. It's also a lightweight VER oracle — if the Java port behaves differently on the same map, the COBOL version has a bug. | | | | | |
| 9 | S6-01..S6-11, S7-32 | **PTY-based self-play demo driver** — `demo.c` uses `forkpty()` to launch `doom` under a pseudo-terminal, feeds a timed script of `{delay_ms, keys, comment}` actions (title → difficulty → walk → sprint → doors → combat), relays game output to the real terminal, saves/restores termios, terminates child cleanly on exit, wired into the Makefile as `demo` / `run-demo` | **SYS** (sec. VER) | 2 | 2 | 4.0 | `demo.c:1-348`, specifically `demo.c:15` (`#include <util.h>` for macOS `forkpty`), `demo.c:17-26` (restore_term), `demo.c:30-80+` (scripted `Action` array), `Makefile:29-39` |
|   | _Significance note_ | Non-trivial SYS work: separate process, pseudo-terminal multiplexing, `select()`-style relay, signal-safe cleanup. Also functions as a reproducible regression harness — "the demo playthrough still completes" is a cheap end-to-end test. | | | | | |
| 10 | S1-04..S1-10, S3-04..S3-07, S1-09 | **Raw-mode terminal I/O and time substrate in C** — `tcgetattr` / `tcsetattr` to disable echo+canonical+signals, alternate screen buffer (`\033[?1049h`), cursor hide, non-blocking `read()` + ESC-sequence parser that maps arrow keys to synthetic codes 200–203, `gettimeofday`-based millisecond clock, `usleep(16000)` frame pacer, integer sin/cos tables scaled ×10 000 to route around GnuCOBOL's slow float path | **INF** (sec. SYS) | 2 | 1 | 3.0 | `terminal-io.c:12-72` |
|   | _Significance note_ | Plumbing, not algorithmics, but load-bearing plumbing: everything above this row — including the COBOL main loop — depends on raw-mode input, precise frame timing, and the `COMP-5`-compatible trig shim. | | | | | |
| 11 | S1-02, S1-03, S6-06, README, `Makefile:1-47` | **Cross-toolchain Makefile (GnuCOBOL + gcc + javac)** — single Makefile driving `cobc -x -free` to link `doom.cob` + `terminal-io.c` with `-lm`, `gcc -O2` for the `demo` binary, `javac` into a separate `build/java/` tree, plus `run` / `run-demo` / `run-java` / `java-smoke` orchestration targets | **INF** | 1 | 1 | 1.5 | `Makefile:1-47` |
|   | _Significance note_ | Standard INF work. Listed because without it no one can reproduce the build — three languages, three compilers, one `make all`. | | | | | |

## Composition chains

- **Chain A — the real-time loop itself:** raw-mode tty + `read_key` + `get_time_ms` + `frame_sleep` (row 10) → `COMP-5` FFI bridge with setter-arg chunking (row 2) → COBOL `GAME-LOOP` state machine with `PERFORM HANDLE-INPUT / UPDATE-ENEMIES / CHECK-PICKUPS / RENDER-GAME-FRAME` (row 1) → DDA ray-caster called from inside that loop (row 3) → textured framebuffer + sprites flushed every 16 ms (rows 4 + 6). The emergent capability is "a 60 Hz interactive program whose inner loop is COBOL"; remove any link and the chain collapses to a demo program.
- **Chain B — Doom as a domain:** map `REDEFINES` tile grid + DDA (rows 3, 5) → textures keyed on tile character (row 4) → sprite pipeline with z-buffer test (row 6) → door / pickup / armor / intermission mechanics that mutate the same tile grid (row 7) → multi-level progression that swaps the grid and respawns tables (row 5). The emergent capability is a game that *feels* like Doom, which is a DOM claim, not an ALG claim.
- **Chain C — cross-language verification:** the COBOL/C game (rows 1–7) → independent Java re-implementation sharing map strings, level tables and mechanics (row 8) → Makefile orchestrating both builds + `java-smoke` target (row 11). The emergent capability is a cheap differential oracle: the Java port is only useful because something exists to compare it against.
- **Chain D — reproducible self-play:** COBOL game binary (rows 1–7) → PTY driver with scripted keystrokes (row 9) → Makefile `run-demo` wiring (row 11). The emergent capability is hands-free regression playthrough; the demo is meaningless without a working game behind the PTY.

## Significance profile

Primary-class count across the top 11 features (secondary classes shown in parentheses when present):

| Class | Count | Rows |
|---|---|---|
| LNG | 1 (+1 sec) | 1 — plus row 2's secondary |
| SYS | 2 (+1 sec) | 2, 9 — plus row 10's secondary |
| ALG | 1 (+1 sec) | 3 — plus row 6's secondary |
| DOM | 3 (+1 sec) | 4, 5, 6, 7 — plus row 1's secondary |
| PRF | 0 (+2 sec) | secondary on rows 3, 4 |
| CMP | 1 (+0) | 8 |
| VER | 0 (+2 sec) | secondary on rows 8, 9 |
| INF | 2 (+0) | 10, 11 |
| PRO | 0 | — |

Centre of gravity: **LNG + DOM** with a strong **SYS** seam at the COBOL/C boundary and one genuine **CMP** artefact (the Java port).

## Verdict

**Hybrid — language-achievement-centric with a domain-modelling superstructure and a system-integration seam:** the interesting claim is not the DDA algorithm (textbook) but that a 60 fps interactive Doom-like, with state machine, enemies, doors, pickups and three levels, runs with its inner loop written in COBOL and talks to a C renderer over a hand-rolled `COMP-5`/setter-function ABI, cross-validated by an independent Java port.
