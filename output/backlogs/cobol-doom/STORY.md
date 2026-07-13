# STORY — cobol-doom

## 1. The premise

COBOL was standardised in 1960 to process fixed-length records in batches: payroll runs, insurance ledgers, overnight reconciliations. It has no graphics primitives, no pointers, no real-time scheduler, no floating-point culture. "Write a Doom game in COBOL" is therefore a category error — which is exactly why it is interesting. The project is the novelty. What shipped from a five-word prompt is a 60 fps first-person shooter whose inner loop — state machine, input dispatch, enemy AI, collision, pickups, level progression — runs in COBOL paragraphs, not in the C sidecar that paints the screen.

The core artefacts: a `doom` binary of 164 KB, a `demo` harness of 34 KB, one 1,076-line `doom.cob` with 24 paragraphs, and one `terminal-io.c` of roughly 1,400 lines providing the rendering and input substrate. All COBOL work was done by **Claude Code** (`claude-opus-4-6`, v2.1.63) in a single session starting 2 March 2026.

_Note: the repository also contains a Java port (`GameLogic.java`, `GameRenderer.java`, etc.) which was produced in a separate Codex session on 13 March as a translation/migration exercise. That Java work is a distinct experiment — not part of the COBOL Doom build story — and is excluded from the analysis below._

## 2. Domain and compromise

A ray-caster is the right engine for this constraint. BSP rendering with textured WAD assets — the path the 1993 id Software team took — is out of reach: GnuCOBOL has no access to VGA, SDL or the framebuffer, and its floating-point path is slow enough that per-pixel trig would blow the frame budget. The agent pushed the compromise hard: raw-mode terminal (`tcsetattr` to drop echo, canonical, signals), alternate screen buffer (`\033[?1049h`), cursor hide, Unicode half-blocks (`U+2580`) stacked vertically to double the cell resolution, 24-bit RGB escapes, and integer sin/cos tables scaled by 10,000 so that COBOL's `PIC S9(9) COMP-5` can carry angles without a float detour.

The engineering lives at the COBOL ↔ C seam. Two ABIs meet there, and neither is designed for per-frame traffic. The agent chose `COMP-5` as the wire type, `BY VALUE` / `BY REFERENCE` for argument direction, and — when macOS on ARM64 capped the usable register-argument count — a bank of setter functions (`set_hud_armor`, `set_enemy_data`, `set_pickup_data`, `set_intermission_data`) that chunk state across the boundary roughly sixty times a second. This is the ABI workaround that keeps COBOL in the driver's seat; without it, the "hard inner loop runs in COBOL" claim collapses into "C does the work".

## 3. Chronology — one Claude Code session, seven steps

The substantive COBOL build is a single Claude Code session (2 March 2026), with the agent's own step labels running from S1 through S7.

**Step S1** lays down the hybrid architecture — thirty backlog entries covering the raw-mode tty substrate, player state in COBOL, a Title → Playing → Dead → Win state machine, WASD + strafe movement, wall collision, three weapons with cooldowns, five enemies across three types, HUD and damage flash. The first raycaster is a naive per-pixel step-march (S1-11).

**Step S2** fixes "keys not working" by migrating every interop variable to `COMP-5` and introducing the setter pattern.

**Step S3** is the consequential rewrite: column-based DDA grid traversal (SB-031 / S3-02) replaces the step-march, a z-buffer feeds sprite sorting, Unicode half-blocks double the vertical resolution, and a 1 MB output buffer with minimised ANSI state changes pushes the frame rate to a 16 ms target. The agent iterated on its own engine — not because the user asked for DDA, but because "improve the speed and look and feel" forced the question of what the rendering primitive should be.

**Step S4** is twelve parameter tunes to balance movement and damage.

**Step S5** paints STARTAN, TEKWALL, door and hell-marble textures; adds Imp, Pinky and Baron silhouettes; and builds the brown status bar with the `[^_^] / [o_o] / [>_<] / [x_x]` face indicator.

**Step S6** adds the `forkpty()` self-play demo — a PTY-based driver that feeds scripted keystrokes and relays the game's terminal output.

**Step S7** lands the Doom vocabulary: F-key door opening that mutates walkable tiles, a twenty-slot pickup table (stimpack / clip / armor vest), three levels with `REDEFINES` onto a linear 576-cell buffer, per-level spawn paragraphs, an intermission screen, armor absorbing a third of incoming damage, a sprint toggle, and a C-side `check_los_c` so enemies cannot cheat through walls.

## 4. Delivered

A `doom` binary of 164 KB that plays: title screen, difficulty select (Easy / Normal / Hard), three levels (UAC Base, Industrial Complex, Hell), enemies that chase and shoot, pickups that heal and rearm, doors that open when you face them and press F, sprint, an intermission with kill and item percentages, and a win screen after level three. A `demo` binary that drives the game through a pseudo-terminal with a scripted keystroke schedule. The SPECIFICATION_BACKLOG.md carries 139 S-## entries decomposed by step trigger — all from the single Claude Code session.

## 5. Validation and loose ends

What did not close cleanly: the session carries complaints of "slow" rendering and "keys broken" that were not fully resolved, and the input path is fragile under some terminal emulators. The automated pipeline flags a 4.0 % tool-output error rate (13 errors in 329 tool outputs), one bug-report-style prompt, and only 1.7 % of active time spent in `bug_fix` — the ratio of fresh capability to remediation is high, but a user sitting at a different terminal may hit one of the unresolved edges.

## 6. Compute and context footprint

The Claude Code build session used about two hours fifty-three minutes of active collaboration, 952 turns total across all sessions (including the later analyst pass), one compaction. Peak context on the Claude Code side reached 165 k of a 1 M window (16 %) — well within the Opus 1M ceiling. No context pressure was a factor on this project.

## 7. Why this counts

The inner loop runs in COBOL. Not "a COBOL file exists and C does the rendering" — the per-frame `PERFORM HANDLE-INPUT / UPDATE-ENEMIES / CHECK-PICKUPS / RENDER-GAME-FRAME` cadence, the state machine dispatch, the mutable integer physics, the level progression, the difficulty scaling, all live in `doom.cob` and call into C only for I/O and rasterisation. This is not a demo stub with a COBOL wrapper; it is a playable game whose game loop happens to be written in a language built for batch record processing.

## 8. Surprising insights

The agent iterated on its own engine. The Step-1 raycaster was a naive step-march; by Step-3 the agent had replaced it with a DDA grid traversal (SB-031) and a z-buffer, not because the user asked for a specific algorithm but because "improve the speed and look and feel" forced the question of what the rendering primitive should be. That kind of self-revision — agent choosing a better algorithm because the user's vague quality request demanded it — is the shape of engineering judgement, not just code generation.

The project also stands out for its sheer out-of-paradigm character: COBOL has no cultural tradition of real-time interactive programs. The `PERFORM`-based game loop, the `COMP-5` setter-function ABI for 60 fps cross-language traffic, and the integer-trig workaround are all solutions to problems that simply don't arise in COBOL's natural domain. That they work at all — producing a playable game, not just a compiling prototype — is the point.
