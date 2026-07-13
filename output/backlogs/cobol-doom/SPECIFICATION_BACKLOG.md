# SPECIFICATION BACKLOG — Agent-Implemented Features

This backlog is **feature-centric**: it lists every capability the agent implemented, decomposed into granular technical features, ordered by the step in which they appeared. This complements the user-request-centric backlog in `README.md`.

Evidence keys:
- `[T:msg_NNN]` — session transcript message index
- `[R:file:lines]` — repo file reference
- `[G:commit]` — git commit (note: all commits are post-hoc, 2026-03-13)

---

## Step 1 — Initial Implementation (BL-001)

> Trigger: `"Write a Doom game in COBOL"` [T:msg_004]

### Architecture

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S1-01 | Hybrid COBOL+C architecture — COBOL for game logic, C for terminal I/O and rendering | `doom.cob`, `terminal-io.c` | [T:msg_020] |
| S1-02 | Free-format COBOL compilation (`cobc -x -free`) | `Makefile:7` | [T:msg_047] |
| S1-03 | Makefile build system with `doom` target | `Makefile:18-23` | [T:msg_038] |

### Terminal I/O (C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S1-04 | Raw terminal mode (disable echo, canonical, signals) | `terminal-io.c:18-29` | [T:msg_020] |
| S1-05 | Terminal restore on exit | `terminal-io.c:31-37` | [R:terminal-io.c:31] |
| S1-06 | Non-blocking keyboard input via `read()` | `terminal-io.c:39-58` | [T:msg_020] |
| S1-07 | Alternate screen buffer (`\033[?1049h`) | `terminal-io.c:26` | [R:terminal-io.c:26] |
| S1-08 | Cursor hiding (`\033[?25l`) | `terminal-io.c:26` | [R:terminal-io.c:26] |
| S1-09 | Integer-based trigonometry (sin/cos scaled ×10000) | `terminal-io.c:70-71` | [T:msg_020] |
| S1-10 | Millisecond time function (`get_time_ms`) | `terminal-io.c:61-65` | [R:terminal-io.c:61] |

### Raycasting Engine (C, v1)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S1-11 | Per-pixel raycasting (naive step-march) | `terminal-io.c` (v1, replaced in Step 3) | [T:msg_191] |
| S1-12 | Distance-based wall shading (darker with distance) | `terminal-io.c` (v1) | [T:msg_061] |
| S1-13 | ASCII character rendering (`#`, `.`, etc.) | `terminal-io.c` (v1, replaced in Step 3) | [T:msg_061] |

### Game Logic (COBOL)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S1-14 | Player state (position, angle, health, ammo, score) | `doom.cob:16-31` | [T:msg_061] |
| S1-15 | Game state machine: Title → Playing → Dead → Win | `doom.cob:711-820` (GAME-LOOP) | [T:msg_061] |
| S1-16 | Title screen | `doom.cob` (GAME-LOOP title branch) | [T:msg_061] |
| S1-17 | Death screen with score | `terminal-io.c:1193` (show_death_c) | [T:msg_061] |
| S1-18 | Win screen with score | `terminal-io.c:1254` (show_win_c) | [T:msg_061] |
| S1-19 | WASD movement (forward/back/turn) | `doom.cob:851-960` (HANDLE-INPUT) | [T:msg_061] |
| S1-20 | Q/E strafe left/right | `doom.cob:851-960` | [T:msg_061] |
| S1-21 | Wall collision detection (X/Y independent) | `doom.cob:1008-1035` (CHECK-COLLISION) | [T:msg_061] |
| S1-22 | Shooting mechanic with cooldown | `doom.cob:1087-1112` (PLAYER-SHOOT) | [T:msg_061] |
| S1-23 | 3 weapons: Pistol, Shotgun, Plasma (keys 1/2/3) | `doom.cob` weapon switch in HANDLE-INPUT | [T:msg_061] |
| S1-24 | Weapon damage differentiation (pistol<shotgun<plasma) | `doom.cob:1087-1112` | [T:msg_061] |
| S1-25 | 20×20 map with rooms, corridors, doors, special walls | `doom.cob` (v1, expanded in Step 3) | [T:msg_061] |
| S1-26 | 5 enemies with 3 types: Imp, Soldier, Boss | `doom.cob` (v1, expanded later) | [T:msg_061] |
| S1-27 | Enemy AI: chase player, attack within range | `doom.cob:1170-1294` (UPDATE-ENEMIES) | [T:msg_061] |
| S1-28 | HUD: health, ammo, score, weapon, enemy count | `terminal-io.c` (render_frame HUD section) | [T:msg_061] |
| S1-29 | Damage flash (red overlay when hit) | `doom.cob:26` (DAMAGE-FLASH) | [T:msg_061] |
| S1-30 | Enemy hit detection (raycasted from player angle) | `doom.cob:1113-1169` (CHECK-ENEMY-HIT) | [T:msg_061] |

---

## Step 2 — Fix Key Controls / C-COBOL Interop (BL-002)

> Trigger: `"the key controls seem not working"` [T:msg_066]

| # | Feature / Fix | Where | Evidence |
|---|---------------|-------|----------|
| S2-01 | COMP-5 type conversion for all C-interop variables | `doom.cob:13-43` (all `PIC S9(9) COMP-5`) | [T:msg_075, msg_082] |
| S2-02 | Numeric EVALUATE replacing 88-level conditions (COMP-5 compat) | `doom.cob` GAME-LOOP state dispatch | [T:msg_128] |
| S2-03 | Setter-function pattern for C globals (ARM64 ABI workaround for >8 params) | `terminal-io.c:118-148` (set_hud_*, set_enemy_data, etc.) | [T:msg_156] |
| S2-04 | Frame sleep via C `usleep(16000)` wrapper (replacing broken `C$SLEEP`) | `terminal-io.c:68` | [T:msg_090] |
| S2-05 | BY REFERENCE parameter passing for setter calls | `doom.cob:1296-1343` | [T:msg_160] |

---

## Step 3 — Performance & Visual Overhaul (BL-003)

> Trigger: `"please improve the game, especially the speed and look and feel"` [T:msg_182]

### Renderer Rewrite (C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S3-01 | Column-based raycasting (1 ray/column, ~22× fewer rays) | `terminal-io.c:842+` (render_frame) | [T:msg_232] |
| S3-02 | DDA algorithm (exact grid intersections, replacing naive step-march) | `terminal-io.c:194-223` (cast) | [T:msg_232] |
| S3-03 | Z-buffer per column for sprite depth testing | `terminal-io.c:225` (zbuf) | [T:msg_232] |
| S3-04 | Unicode half-block rendering (`▀`, U+2580) for 2× vertical resolution | `terminal-io.c` render_frame output | [T:msg_208, msg_216] |
| S3-05 | 1MB buffered output with minimal ANSI state changes | `terminal-io.c:149-165` (buf, bput, fg_rgb, bg_rgb) | [T:msg_232] |
| S3-06 | True-color (24-bit RGB) rendering | `terminal-io.c:161-167` (fg_rgb, bg_rgb using `\033[38;2;R;G;Bm`) | [T:msg_232] |
| S3-07 | 60fps frame target (16ms sleep) | `terminal-io.c:68` | [T:msg_232] |
| S3-08 | NS/EW wall side shading (EW walls 30% darker) | `terminal-io.c:369-390` (wall_color) | [T:msg_232] |
| S3-09 | Distance-based fog with smooth gradient | `terminal-io.c:369+` | [T:msg_232] |
| S3-10 | Gradient sky (deep blue at zenith → lighter at horizon) | `terminal-io.c` render_frame sky | [T:msg_232] |
| S3-11 | Checkered floor with perspective-correct distance shading | `terminal-io.c:392-418` (floor_color) | [T:msg_232] |
| S3-12 | Crosshair overlay (`+`) at center | `terminal-io.c` render_frame | [T:msg_232] |

### Sprites (C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S3-13 | Enemy sprites in 3D view (humanoid: head, body, arms, legs) | `terminal-io.c:466-602` (draw_enemy) | [T:msg_232] |
| S3-14 | Enemy color coding: red Imps, blue Soldiers, purple Boss | `terminal-io.c:466+` | [T:msg_232] |
| S3-15 | Damaged enemy visual (red tint) | `terminal-io.c:466+` | [T:msg_232] |
| S3-16 | Weapon ASCII art at bottom (Pistol/Shotgun/Plasma) | `terminal-io.c:713-811` (draw_weapon) | [T:msg_232] |
| S3-17 | Muzzle flash effect when shooting | `terminal-io.c:713+` | [T:msg_232] |

### Minimap & HUD (C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S3-18 | Minimap in top-right corner (walls, player `@`, enemies `!`) | `terminal-io.c` render_frame minimap section | [T:msg_232] |
| S3-19 | Visual health bar (color-coded) | `terminal-io.c` HUD section | [T:msg_232] |

### Gameplay (COBOL)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S3-20 | Arrow key support (alongside WASD) | `terminal-io.c:46-52` (ESC sequence parsing → codes 200-203) + `doom.cob` HANDLE-INPUT | [T:msg_199, msg_232] |
| S3-21 | Wall sliding (X/Y independent collision) | `doom.cob:1008-1035` | [T:msg_232] |
| S3-22 | 24×24 expanded map with more rooms and corridors | `doom.cob:51-76` (MAP-DATA) | [T:msg_199] |
| S3-23 | 8 enemies across map (up from 5) | `doom.cob` spawn routines | [T:msg_232] |
| S3-24 | Hit score bonus (+10 per hit, +100 per kill) | `doom.cob` CHECK-ENEMY-HIT | [T:msg_232] |
| S3-25 | Enemy wall collision detection | `doom.cob:1256-1294` (ENEMY-CHASE) | [T:msg_232] |

---

## Step 4 — Gameplay Balance Tuning (BL-004)

> Trigger: `"I can move but not enough quickly... dying very quickly"` [T:msg_237]

| # | Parameter | Before | After | Where | Evidence |
|---|-----------|--------|-------|-------|----------|
| S4-01 | Move speed | 18 | 40 | `doom.cob:41` | [T:msg_268] |
| S4-02 | Turn speed | 10 | 25 | `doom.cob:42` | [T:msg_268] |
| S4-03 | Starting ammo | 50 | 80 | `doom.cob:22` | [T:msg_268] |
| S4-04 | Enemy attack cooldown | 20 frames (~0.3s) | 90 frames (~1.5s) | `doom.cob` enemy attack logic | [T:msg_268] |
| S4-05 | Enemy attack range | 350 | 300 | `doom.cob` UPDATE-ENEMIES | [T:msg_268] |
| S4-06 | Imp damage | 5 | 3 | `doom.cob` UPDATE-ENEMIES | [T:msg_268] |
| S4-07 | Soldier damage | 12 | 6 | `doom.cob` UPDATE-ENEMIES | [T:msg_268] |
| S4-08 | Boss damage | 20 | 10 | `doom.cob` UPDATE-ENEMIES | [T:msg_268] |
| S4-09 | Enemy chase interval (Imp) | 6 | 15 frames | `doom.cob` UPDATE-ENEMIES | [T:msg_268] |
| S4-10 | Enemy chase interval (Soldier) | 8 | 20 frames | `doom.cob` UPDATE-ENEMIES | [T:msg_268] |
| S4-11 | Enemy chase interval (Boss) | 4 | 12 frames | `doom.cob` UPDATE-ENEMIES | [T:msg_268] |
| S4-12 | Enemy chase step size | 6 | 4 | `doom.cob:1256+` | [T:msg_268] |

---

## Step 5 — Doom-Style Graphics (BL-005)

> Trigger: `"please improve graphics such that it looks like more Doom"` [T:msg_273]

### Wall Textures (C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S5-01 | STARTAN-style texture: brown/tan metal panels with rivets, grooves, horizontal stripes | `terminal-io.c:229-258` (tex_startan) | [T:msg_307] |
| S5-02 | TEKWALL-style texture: gray metal, green tech stripes, vent slits, blinking indicator lights | `terminal-io.c:260-292` (tex_techwall) | [T:msg_307] |
| S5-03 | Door texture: UAC-style, yellow/black warning stripes, paneled body, metal handle | `terminal-io.c:294-329` (tex_door) | [T:msg_307] |
| S5-04 | Hell/marble texture: red marble, sinusoidal veins, skull motifs, lava cracks | `terminal-io.c:331-367` (tex_hell) | [T:msg_307] |
| S5-05 | Wall type alternation (STARTAN/TEKWALL) based on position | `terminal-io.c:369-390` (wall_color) | [T:msg_307] |

### Floor & Ceiling (C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S5-06 | Textured floor: dark stone tiles, grout lines, blood stains | `terminal-io.c:392-418` (floor_color) | [T:msg_307] |
| S5-07 | Textured ceiling: dark tech panels, flickering ceiling lights | `terminal-io.c:420-454` (ceiling_color) | [T:msg_307] |

### Lighting (C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S5-08 | Flickering lights: hash-based noise for subtle per-frame variation | `terminal-io.c:184-192` (hash) | [T:msg_307] |
| S5-09 | Distance fog with steeper Doom-like falloff | `terminal-io.c:369+` | [T:msg_307] |
| S5-10 | NS/EW wall shading increased to 35% | `terminal-io.c:369+` | [T:msg_307] |

### Sprites (C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S5-11 | Imp sprite: brown skin, horns, brow ridge, yellow glowing eyes, teeth | `terminal-io.c:466+` (draw_enemy) | [T:msg_307] |
| S5-12 | Pinky Demon sprite: pink-red skin, orange eyes, bulkier body | `terminal-io.c:466+` | [T:msg_307] |
| S5-13 | Baron sprite: green/brown skin, red eyes, horns, larger size | `terminal-io.c:466+` | [T:msg_307] |
| S5-14 | Damaged enemy bloody red tint | `terminal-io.c:466+` | [T:msg_307] |
| S5-15 | Pistol sprite: slide, barrel, grip with crosshatch, trigger guard, hand | `terminal-io.c:713+` (draw_weapon) | [T:msg_307] |
| S5-16 | Shotgun sprite: double barrel, pump forend with wood grain, receiver, stock | `terminal-io.c:713+` | [T:msg_307] |
| S5-17 | Plasma rifle sprite: blue energy coils (animated), glowing window (pulsing), tech body | `terminal-io.c:713+` | [T:msg_307] |
| S5-18 | Weapon bob animation while moving | `terminal-io.c:713+` | [T:msg_307] |
| S5-19 | Muzzle flash bleeds into weapon sprite | `terminal-io.c:713+` | [T:msg_307] |

### Title Screen & HUD (C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S5-20 | DOOM logo rendered with Unicode block characters (█▀▄) | `terminal-io.c:1114-1191` (show_title_c) | [T:msg_304] |
| S5-21 | "WRITTEN IN COBOL" subtitle with brown banner | `terminal-io.c:1114+` | [T:msg_304] |
| S5-22 | Brown status bar HUD (color 48;5;94) matching Doom's palette | `terminal-io.c` render_frame HUD | [T:msg_307] |
| S5-23 | Doomguy face indicator: `[^_^]` happy → `[o_o]` alert → `[>_<]` hurt → `[x_x]` dead | `terminal-io.c:813-840` (draw_face_hud) | [T:msg_307] |

### Controls (COBOL)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S5-24 | ESC key quit (alongside X) | `doom.cob` HANDLE-INPUT | [T:msg_286] |

---

## Step 6 — Automated Demo Driver (BL-006)

> Trigger: `"could you make an automated demonstration where 'you' play with the keyboards?"` [T:msg_312]

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S6-01 | PTY-based demo driver using `forkpty()` | `demo.c:1-348` | [T:msg_314] |
| S6-02 | Scripted keystroke schedule (delay + key + comment) | `demo.c:30-34, 35+` (Action struct, script array) | [R:demo.c:30-50] |
| S6-03 | Terminal relay: game output forwarded to real terminal | `demo.c` main loop | [T:msg_314] |
| S6-04 | Terminal state save/restore on demo exit | `demo.c:17-26` (restore_term) | [R:demo.c:20] |
| S6-05 | Graceful child process termination (SIGTERM + waitpid) | `demo.c` | [T:msg_332] |
| S6-06 | Makefile targets: `demo`, `run-demo` | `Makefile:29-39` | [T:msg_319] |

### Demo Script Content

| # | Scene | Evidence |
|---|-------|----------|
| S6-07 | Title screen pause (2s) | [R:demo.c:37] |
| S6-08 | Difficulty selection | [R:demo.c:38] |
| S6-09 | Walk forward, explore corridors | [R:demo.c:42-46] |
| S6-10 | Turn, strafe, scout | [R:demo.c:48-50] |
| S6-11 | Shoot enemies, switch weapons | [T:msg_360] |

---

## Step 7 — Advanced Doom Features (BL-007)

> Trigger: `"implement advanced features of Doom, mainly by editing the COBOL code"` [T:msg_365]

### Doors (COBOL)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S7-01 | Door tiles (`D`) in map data | `doom.cob:56,60,66+` (map definitions) | [T:msg_416] |
| S7-02 | Open door mechanic: F key, face door tile, changes to walkable | `doom.cob:985-1007` (OPEN-DOOR) | [T:msg_416] |
| S7-03 | Door range check (within 150 units + facing) | `doom.cob:985+` | [R:doom.cob:985] |

### Pickups (COBOL + C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S7-04 | Pickup data structure (up to 20 pickups: position, type, active flag) | `doom.cob:185-204` | [R:doom.cob:185] |
| S7-05 | Health stimpack pickup (+25 HP, capped at 100) | `doom.cob:1051-1085` (COLLECT-PICKUP) | [T:msg_416] |
| S7-06 | Ammo clip pickup (+15 ammo) | `doom.cob:1051+` | [T:msg_416] |
| S7-07 | Armor vest pickup (+100 armor) | `doom.cob:1051+` | [T:msg_416] |
| S7-08 | Pickup proximity collection (within 80 units) | `doom.cob:1036-1050` (CHECK-PICKUPS) | [R:doom.cob:1036] |
| S7-09 | Pickup sprites in 3D view (green cross, yellow box, blue shield) | `terminal-io.c:604-711` (draw_pickup) | [T:msg_416] |
| S7-10 | Bobbing pickup animation | `terminal-io.c:604+` | [T:msg_416] |
| S7-11 | Pickups shown on minimap as green `*` | `terminal-io.c` minimap section | [T:msg_416] |
| S7-12 | Unified sprite sorting (enemies + pickups depth-sorted together) | `terminal-io.c:456-464` (sprites array, spr_cmp) | [T:msg_416] |

### Multi-Level System (COBOL)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S7-13 | 3 level maps: L1 (UAC Base), L2 (Industrial Complex), L3 (Hell) | `doom.cob:78-160` (L1/L2/L3-MAP-DATA) | [T:msg_416] |
| S7-14 | Level setup with map copy + enemy/pickup spawning per level | `doom.cob:272-335` (SETUP-LEVEL) | [R:doom.cob:272] |
| S7-15 | Level 1 spawn: 7 enemies, 5 pickups | `doom.cob:336-610` (SPAWN-ENEMIES-L1, PLACE-PICKUPS-L1) | [T:msg_416] |
| S7-16 | Level 2 spawn: 8 enemies, 6 pickups | `doom.cob:404-651` | [T:msg_416] |
| S7-17 | Level 3 spawn: 10 enemies, 9 pickups | `doom.cob:481-710` | [T:msg_416] |
| S7-18 | Level progression: kill all enemies → advance to next level | `doom.cob:800-820` (GAME-LOOP level check) | [T:msg_416] |
| S7-19 | Win condition after level 3 | `doom.cob:800+` | [T:msg_416] |

### Armor System (COBOL + C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S7-20 | Armor stat (absorbs 1/3 of incoming damage) | `doom.cob:21` (PLAYER-ARMOR) + UPDATE-ENEMIES damage calc | [T:msg_416] |
| S7-21 | Armor display in HUD ("AR" value) | `terminal-io.c:126` (set_hud_armor) + HUD rendering | [T:msg_416] |

### Sprint (COBOL + C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S7-22 | Sprint toggle (R key) — doubles movement speed | `doom.cob:30` (IS-SPRINTING), `doom.cob:43` (EFFECTIVE-SPEED) | [T:msg_416] |
| S7-23 | Sprint "RUN" indicator in HUD | `terminal-io.c:127` (set_hud_sprint) + HUD rendering | [T:msg_416] |

### Enemy AI Improvement (COBOL + C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S7-24 | Enemy line-of-sight check via C raycast (no cheat through walls) | `terminal-io.c:75-96` (check_los_c) + `doom.cob:1179+` (UPDATE-SINGLE-ENEMY) | [T:msg_416] |

### Difficulty System (COBOL + C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S7-25 | Difficulty selection on title screen (1=Easy, 2=Normal, 3=Hard) | `doom.cob:711+` (GAME-LOOP title branch, keys 1/2/3) | [T:msg_416] |
| S7-26 | Easy: enemies 2/3 HP, half damage, more ammo | `doom.cob:822-847` (START-NEW-GAME) | [T:msg_416] |
| S7-27 | Hard: enemies 3/2 HP, 50% more damage, less ammo | `doom.cob:822-847` | [T:msg_416] |
| S7-28 | Difficulty shown on title screen | `terminal-io.c:1114+` (show_title_c) | [T:msg_416] |

### Intermission (COBOL + C)

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S7-29 | Intermission screen between levels: Kills %, Items %, Time | `terminal-io.c:1293-1387` (show_intermission_c) | [T:msg_416] |
| S7-30 | Intermission data passing via setter (kills, items, time, level) | `terminal-io.c:141-147` (set_intermission_data) | [R:terminal-io.c:141] |
| S7-31 | Progress bars for kill/item percentages | `terminal-io.c:1293+` | [T:msg_416] |

### Demo Update

| # | Feature | Where | Evidence |
|---|---------|-------|----------|
| S7-32 | Demo script updated for new features (difficulty select, door opening, pickups, sprint) | `demo.c:35+` | [T:msg_400] |

---

## Summary

| Step | Features | Trigger |
|------|----------|---------|
| Step 1 | 30 features | "Write a Doom game in COBOL" |
| Step 2 | 5 fixes | "keys not working" |
| Step 3 | 25 features | "improve speed and look and feel" |
| Step 4 | 12 parameter tunes | "move too slowly, dying too fast" |
| Step 5 | 24 features | "look more like Doom" |
| Step 6 | 11 features | "automated demonstration" |
| Step 7 | 32 features | "advanced features of Doom" |
| **Total** | **139 features/changes** | **7 user prompts** |

### Feature Counts by Subsystem

| Subsystem | Count |
|-----------|-------|
| Raycasting / Rendering engine (C) | 37 |
| Game logic (COBOL) | 42 |
| Textures / Visual art (C) | 22 |
| HUD / UI (C) | 12 |
| Sprites (C) | 13 |
| Terminal I/O (C) | 7 |
| Build / Tooling | 8 |
| Balance parameters | 12 |

### Feature Counts by Kind

| Kind | Count |
|------|-------|
| New capability | 107 |
| Bug fix / interop fix | 5 |
| Parameter tuning | 12 |
| Replacement / rewrite | 6 |
| Tooling / infrastructure | 9 |
