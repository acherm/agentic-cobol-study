# STORY -- cobol-doom-codex

The Codex replica of Doom chose SDL2 graphical rendering and BMP sprites -- a radically different interpretation of the same prompts.

## Domain

The same six-step prompt sequence that produced the terminal-based Claude Code Doom was replayed against Codex: grid walker, then raycaster, then enemies, then levels, then graphical polish, then modular refactoring. The workspace started empty. Both agents received the same written requirements, the same GnuCOBOL 3.2 toolchain, the same macOS ARM64 host. The outputs diverge immediately and never converge.

## Chronology

The session opens on 2026-04-17 at 18:34 CEST. Codex spends its first fifteen minutes on something Claude Code never did: methodical input-method prototyping. Four throwaway COBOL programs test three different keyboard capture strategies before the agent settles on non-canonical terminal mode.

The grid walker lands at minute 9 (commit `8127df8`). The user immediately reports alignment issues. The agent diagnoses the root cause in under two minutes -- `stty raw` disables output post-processing -- and ships a one-line fix: `stty -icanon -echo min 0 time 1`. Commit `ec5133e`.

## The SDL2 decision

The first-person raycaster prompt is where the two agents permanently diverge. Claude Code went straight to a terminal-based approach with Unicode half-blocks and ANSI 24-bit color. Codex tried a different path first: a Python pygame raycaster with COBOL as a thin launcher. The user rejected this as "faking to write COBOL" and demanded that "the core part should be in COBOL." Codex's response was not to fall back to terminal rendering. Instead, it checked what native graphics libraries were available, confirmed SDL2 was installed, and built a narrow C bridge -- `sdl_bridge.c` -- that exposes only drawing and input primitives. The COBOL program retained the game loop, player state, movement, collision, and critically, the DDA raycaster itself.

This is the architectural fingerprint: the raycaster runs in COBOL. Claude Code's CC sibling delegates DDA grid traversal to its rendering layer; Codex keeps it in `gridwalker_raycast.cpy`, using `FUNCTION SIN`, `FUNCTION COS`, and `COMP-2` floating-point arithmetic. The C bridge does not know what a ray is.

## The 11-copybook architecture

The monolithic `gridwalker.cob` grew to 1,637 lines across nine named sections. When the user asked to split into separate files, Codex chose COPY books over separate `PROGRAM-ID` subprograms, citing the shared WORKING-STORAGE as the deciding constraint. The split was surgical: 10 domain-specific `.cpy` files plus `levels.cpy` for authored level data.

## The BMP asset pipeline

Claude Code's CC version generates all visual content procedurally. Codex went the other way: BMP files on disk, loaded by the SDL bridge, sampled per-pixel during rendering. This is closer to how the original 1993 Doom worked and produces higher visual fidelity, but at the cost of a heavier asset dependency (122 MB project vs 236 KB for the CC sibling).

## Comparison

Neither version is "better." The CC version optimizes for terminal portability and has the entire rendering pipeline in COBOL with zero C code. The Codex version optimizes for graphical fidelity and keeps the raycaster in COBOL while delegating pixel output to SDL2. Both agents independently chose the `REDEFINES`-based tile lookup, the `COMP-5`/`COMP-2` FFI wire types, and the `CBL_GC_NANOSLEEP` frame pacer -- convergent solutions to genuine constraints in the GnuCOBOL runtime.

## Why this counts

The raycaster runs in COBOL. The `PERFORM`-based DDA loop in `gridwalker_raycast.cpy` steps through the grid, computes perpendicular distances, and passes wall strip parameters to the SDL bridge for drawing. This is the strongest version of the "COBOL does the computation" claim among the Doom variants, alongside the CC sibling's claim of "COBOL does everything including rendering."
