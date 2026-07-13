# STORY -- cobol-doom-cc

The clean Claude Code redo of Doom in COBOL -- modular from the start, 7 COPY books, terminal rendering, no Java tangent.

## The pure-terminal bet

Claude Code's first architectural decision set the trajectory: everything stays in the terminal. No SDL2, no graphical window, no C rendering sidecar, no BMP sprites. The rendering pipeline -- DDA raycasting, wall-slice height computation, truecolor pixel shading, sprite projection, weapon HUD, minimap -- would live entirely in COBOL paragraphs, with output going to the terminal as 24-bit RGB ANSI escape sequences and Unicode half-block characters.

This was not the path of least resistance. The immediate consequence was a two-hour debugging struggle with GnuCOBOL's I/O layer. The agent wrote the initial grid walker in under ten minutes and it compiled cleanly on the first try. But when the user ran it, nothing appeared. The map only showed up when pressing Q to quit -- a stdout block-buffering issue. The agent bypassed GnuCOBOL's DISPLAY entirely, calling POSIX write() directly from COBOL. Rows terminated with explicit CR+LF. The same pattern repeated with input: CBL_READ_KBD_CHAR pulled in ncurses and swallowed arrow keys. The fix: POSIX read() from fd 0. These two syscall workarounds became the foundation for everything.

## Six steps, twenty user turns

Step 1 produced the 2D grid walker. Step 2 was the big leap: a full DDA raycaster using FUNCTION COS/SIN, continuous COMP-2 position, per-column wall-slice height, then Unicode half-blocks with 24-bit truecolor -- 814 lines of pure COBOL in pd-render.cpy. Step 3 added 7 enemies of 2 kinds with chase AI, sprite projection via inverse camera matrix, and a per-column z-buffer. Step 4 brought pickups, HUD, ammo economy, and two selectable weapons. Step 5 split into three data-driven levels with progression. Step 6 produced demo.sh for automated regression.

The final refactoring split 1,750 lines into an 85-line main plus 7 cohesive copybooks (ws-levels, ws-entities, ws-render, pd-screens, pd-level, pd-world, pd-render), verified by byte-identical frame output.

## Comparison with the Codex sibling

Given the same six prompts on the same day, Codex took a fundamentally different path: SDL2 graphical bridge in C (1,839 LOC), BMP sprite files (122 MB project), pixel-rendered window at 1280x720. Codex's COBOL handles the game loop and raycasting; the C bridge provides SDL2 primitives. Claude Code's COBOL produces the entire visual output -- no C rendering code at all, only POSIX syscalls. The cost gap is dramatic: $367 (Opus 4.7) vs $11 (GPT-5.4).

## What it means

The 814-line pd-render.cpy is the artefact that carries the claim: an entire DDA raycaster + truecolor framebuffer + sprite projector + weapon HUD renderer in COBOL paragraphs, with C involved only at the level of individual POSIX syscalls. Whether that claim is interesting depends on whether you think the language constraint matters. For a study of what coding agents can do with COBOL, the fact that Claude Code chose (and sustained) pure-terminal architecture while Codex chose SDL2 is the comparative finding.
