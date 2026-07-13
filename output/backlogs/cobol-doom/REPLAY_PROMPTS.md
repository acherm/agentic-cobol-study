# Replay Prompts

Reusable prompts for reproducing the COBOL Doom-like project step by step. Each prompt is self-contained enough to copy-paste into a coding agent session. They specify **what** to build (behavior, inputs, outputs, verification), not **how** (no rendering algorithm names, no terminal-I/O API prescriptions, no COBOL/C split prescribed).

Use them sequentially: each step builds on the previous one. Unless a step says otherwise, the primary implementation language is COBOL (GnuCOBOL, free-format); you are free to add a glue layer in another language if you need OS features COBOL does not expose comfortably — that choice is yours.

For reference on what was actually built (algorithms chosen, bugs encountered, autonomous decisions), see [SPECIFICATION_BACKLOG.md](SPECIFICATION_BACKLOG.md).

---

## Step 1: Playable 2-D Grid with Walls

> Write a COBOL program (GnuCOBOL) that runs in a terminal and lets a human walk around a 2-D grid level from a top-down view.
>
> Required behaviour:
> - The level is a rectangular grid (roughly 20×20 or larger) made of wall cells and open cells, with a clearly visible layout of rooms and corridors.
> - The view is a top-down ASCII map: walls, open floor, and the player drawn at the player's current cell with a symbol that indicates facing direction.
> - The player can move with keys W/A/S/D (or the arrow keys) and quit with Q or ESC. Input must be read without requiring the user to press Enter after each key.
> - The player cannot walk through walls. Attempts to do so leave the player in place.
> - The screen is redrawn after every input so the view stays current. Redrawing must not scroll — the map stays anchored.
>
> Verification:
> - Launching the program shows the level with the player at a known start cell.
> - Pressing W/A/S/D (or arrows) moves the player one cell at a time when the target cell is open, and does nothing when it is a wall.
> - Pressing Q or ESC cleanly exits and restores the terminal (no stuck raw mode, cursor visible, shell prompt usable).
> - The program runs on macOS and Linux terminals with no external library beyond what ships with GnuCOBOL and the standard C library.
>
> You are free to choose how you handle raw keyboard input, how you store the map, and whether you introduce a small glue layer in another language for terminal control. Do not change the required behaviour.

---

## Step 2: First-Person Pseudo-3-D View

> Extend the program from Step 1 so that, in addition to the top-down map, the player sees a first-person view of the level rendered in the terminal.
>
> Required behaviour:
> - The player now has a continuous position (not just a cell index) and a facing angle that can be turned smoothly.
> - Controls: W/S move forward/backward, A/D turn left/right (or strafe — pick a convention and document it in the on-screen help), arrow keys as an alternative binding, Q or ESC to quit.
> - The main view is a first-person projection of the level as seen from the player's position and facing. Walls farther away appear smaller / dimmer than walls that are close. Walls that are immediately in front of the player fill most of the vertical viewport; walls at the edge of sight are thin slivers near the horizon.
> - The viewport should be at least 80 columns wide and 24 rows tall and should redraw at an acceptable frame rate — aim for at least 15 frames per second when standing still, so motion feels continuous rather than stuttery.
> - A small minimap (the top-down view from Step 1, with the player dot) should remain visible in a corner so the player can correlate the 3-D view with the level layout.
> - Wall collision from Step 1 still applies: the player's continuous position cannot cross into a wall cell. It is acceptable (and preferable) to let the player slide along a wall when pressing into it diagonally.
>
> Verification:
> - Walking toward a wall makes the wall visibly grow on screen; walking away makes it shrink.
> - Turning in place rotates the scene smoothly and leaves the player position unchanged on the minimap.
> - The frame rate stays playable (no visible chunky redraws) in an 80×24 terminal.
> - Quitting restores the terminal cleanly.
>
> You are free to choose your projection technique, your wall-shading scheme (colour, ASCII gradient, Unicode blocks — any works as long as depth is perceptible), and whether your core loop lives in COBOL or in a helper module called from COBOL. Do not prescribe a specific algorithm in your own mind — just satisfy the observable behaviour.

---

## Step 3: Enemies

> Add enemies to the game.
>
> Required behaviour:
> - Place between 5 and 10 enemies in the level at authored positions. At least two visibly different enemy kinds should exist (different colour, silhouette, or symbol so the player can tell them apart at a glance).
> - Each enemy is visible as a sprite in the first-person view: it appears in the correct screen position based on its world position and the player's facing, gets larger when close and smaller when far, and is hidden when a wall is between it and the player.
> - Enemies are also visible on the minimap, distinct from walls and the player.
> - Enemies move: at minimum, they move toward the player when the player is nearby, and they cannot walk through walls.
> - If an enemy is close enough to the player, the enemy damages the player. The player has a health value that starts at 100 and decreases when hit. When health reaches zero the game ends with a "you died" screen and a way to exit to the shell.
> - The player can fire a weapon with a key (Space or Ctrl). A shot hits the enemy the player is currently facing, within some forward range; multiple hits are required to kill an enemy. Killed enemies disappear from both views.
>
> Verification:
> - Walking up to an enemy causes the player's health to drop over time until the player dies, unless the player kills it first.
> - Shooting in the direction of an enemy kills it after a few hits; the corpse/enemy no longer appears in the 3-D view or the minimap.
> - Enemies never clip through walls and never appear through walls in the 3-D view.
> - Killing all enemies in the level leaves the player free to walk around with no further damage taken.
>
> You decide enemy movement cadence, attack timing, shot mechanics, and how you render the sprites; tune the numbers so the game feels fair (not trivially easy, not instantly lethal).

---

## Step 4: Pickups and HUD

> Add a heads-up display and collectible pickups.
>
> Required behaviour:
> - A HUD is permanently visible at the bottom (or edge) of the screen. It shows at least: current health, current ammo, a kill count or score, and the currently-selected weapon. The HUD must not overlap the first-person viewport — either reserve rows for it or draw it in a dedicated strip.
> - Shooting consumes ammo; when ammo reaches zero the weapon no longer fires (it can click, flash, or simply do nothing, but it must not damage enemies).
> - Place pickups in the level at authored positions, visible both in the first-person view and on the minimap, with at least these kinds:
>   - Health pickup — restores some health up to the maximum (100).
>   - Ammo pickup — adds ammo.
>   - One additional pickup kind of your choice (armour, a stronger weapon, a key, etc.) — its effect must be reflected in the HUD.
> - Picking up an item happens automatically when the player walks over it (or within a small radius). The pickup then disappears from both views.
> - At least two selectable weapons exist, switched with number keys (e.g. 1 / 2 / 3). Different weapons should feel different — a reasonable axis is damage per shot or ammo cost per shot — and the HUD must show which weapon is active.
>
> Verification:
> - Taking damage from enemies, then walking over a health pickup, visibly raises the health value in the HUD (without exceeding the maximum).
> - Firing the weapon decreases the ammo counter; walking over an ammo pickup increases it.
> - Switching weapons with the number keys changes both the HUD indicator and the feel of firing.
> - Pickups, once collected, do not reappear and are no longer shown in either view.
>
> You are free to choose pickup appearance, numeric values, and how you store the pickup list. The constraint is the observable loop: player takes damage, player heals, player runs out of ammo, player refills — all visible in the HUD.

---

## Step 5: Level Definition Format and Multiple Levels

> Split the hard-coded level from the previous steps into a reusable level definition, and ship at least three different levels.
>
> Required behaviour:
> - Define a clear, data-only representation of a level that contains:
>   - the grid of cells (walls / open floor / special tiles such as a level-exit tile, and optionally doors),
>   - the player's starting position and starting facing angle,
>   - the list of enemies to spawn (position + kind, and optionally starting HP),
>   - the list of pickups to spawn (position + kind).
> - The game must load one of three concrete levels at startup and play it. A level ends either when the player reaches a designated goal tile or when all enemies in the level are defeated — pick one rule per level and make it obvious to the player what is expected (a message in the HUD, a recognisable goal tile, etc.).
> - Finishing a level advances to the next. Finishing the last level wins the game and shows a win screen. Dying at any point ends the game and shows a death screen.
> - The three levels must be visibly distinct: different map layouts, different enemy and pickup placement. A visual theme change (wall appearance, colour palette) is nice but not required.
> - Between levels, briefly show a summary screen (level number, kills, time, or similar) before the next level starts.
>
> Verification:
> - Starting the game puts the player in level 1. Completing the level condition advances to level 2, then level 3, then the win screen.
> - Each level's starting position, enemies, and pickups match the data in its definition (changing the data changes the level without touching the main game loop).
> - Dying on any level shows the death screen and does not skip ahead.
> - The game can be re-run from the shell without manual cleanup between runs.
>
> You choose the on-disk or in-source format (embedded arrays, external text file, JSON, your own mini-format). The requirement is that adding a fourth level should be a matter of authoring one more level definition, not editing the render or input code.

---

## Step 6: Automated Demo

> Add a way to watch the game play itself, so anyone can see what the project does without installing or learning the controls.
>
> Required behaviour:
> - Provide a second executable (e.g. `demo`) that launches the main game and feeds it a scripted sequence of keystrokes, as if a human were playing. The demo must relay the game's output to the real terminal so the viewer sees exactly what a player would see.
> - The scripted sequence must exercise the main features: starting a new game, walking around, turning, shooting enemies, picking up items, switching weapons, and advancing at least one level.
> - When the demo ends or is interrupted (Ctrl-C), it must shut the game child down cleanly and restore the terminal to a usable state.
> - Provide a single build command (e.g. a Makefile target) that builds both the game and the demo, and a run command that starts the demo.
>
> Verification:
> - Running the demo command shows the game being played end-to-end with no human input.
> - Pressing Ctrl-C during the demo returns cleanly to the shell with a visible cursor and no garbled terminal state.
> - The demo script is editable: changing the scheduled keystrokes changes what the viewer sees, without touching the game code.
>
> You pick the mechanism for feeding keystrokes to the game (pseudo-terminal, named pipe, a built-in replay mode inside the game itself, etc.) as long as the viewer-facing behaviour above is met.

---

## Step 7 (optional): Java Port for Cross-Language Comparison

> Port the game to Java, keeping the same feature set as the COBOL version, so the two implementations can be compared side by side.
>
> Required behaviour:
> - The Java port runs as a standalone Java application and reproduces the Step 1–5 feature set: first-person view with minimap, enemies, pickups, HUD, at least three levels, win/death screens.
> - It may render into a graphical window instead of the terminal (that is the natural Java choice); if so, it must support equivalent controls (W/A/S/D or arrows, fire, weapon switch, quit) and show a HUD with health, ammo, weapon, and score.
> - Level definitions should be shared in intent with the COBOL version: the same three levels, the same enemy kinds, the same pickup kinds, the same level-end rules. The on-disk format may differ (idiomatic Java classes are fine) but changing a level in one port and mirroring the change in the other should be a mechanical edit.
> - Provide a headless smoke-test mode (a command-line flag, e.g. `--smoke-test`) that initialises the game, runs a few frames of update logic without opening a window, and exits with status 0. This lets CI verify the port builds and the core loop runs.
> - Add Makefile (or equivalent) targets to build the Java port, run it, and run the smoke test.
>
> Verification:
> - `make java` (or equivalent) compiles the Java sources with no warnings.
> - `make run-java` launches the game and plays like the COBOL version in terms of features.
> - `make java-smoke` exits 0 in a headless environment (no display).
> - A reader comparing the two ports can match each COBOL game-logic concept to a Java class or method.
>
> You choose the Java module layout, rendering library, and how much code you share via data files. The goal is a second implementation that is recognisable as "the same game" without being a literal transliteration.
