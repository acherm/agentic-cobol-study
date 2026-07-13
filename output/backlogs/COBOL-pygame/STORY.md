# STORY — COBOL-pygame

## Can COBOL call SDL2?

Yes. That is the whole story. `CALL "cpg_init" USING BY VALUE width height` from a GnuCOBOL program, and an SDL2 window opens. Poll an event, blit a rectangle, tick the clock — all via `CALL` into a C shim. The folder is named `COBOL-pygame`, which is misleading: there is no Python and no pygame module in the runtime path. The chain that actually runs is **COBOL → C (`cpg_*`) → SDL2**. The agent silently reinterpreted the user's "pygame" as "pygame-shaped primitives backed by SDL2", which is the only interpretation that could work inside a COBOL `CALL` ABI. The value of the project is the cross-runtime boundary; there is no algorithmic content.

## Why the boundary is the hard part

COBOL's inter-language contract is rigid. Every C function callable from COBOL must accept parameters through `USING BY VALUE` (scalars) or `USING BY REFERENCE` (pointers, records), with fixed-width space-padded strings and no null terminators. There is no native C pointer type; opaque SDL2 handles (`SDL_Window*`, `SDL_Renderer*`, `SDL_Texture*`) have to round-trip through `USAGE POINTER` cells, which in turn means every C entry point takes `void**` so that COBOL can pass an 01-level `POINTER` by reference to hold the address. SDL2's tagged `SDL_Event` union has to be flattened into a fixed POD (eight `int32_t` fields) so COBOL's fixed-record model can receive it. Every string arrives as `(const char*, int len)` because COBOL has no null terminator convention. That is why the feature profile comes out SYS-heavy and LNG-heavy: the whole project is plumbing at a language boundary. The actual `cpg_*` surface — `cpg_init`, `cpg_quit`, `cpg_create_window`, `cpg_set_draw_color`, `cpg_draw_line`, `cpg_fill_rect`, `cpg_poll_event`, `cpg_delay`, `cpg_ticks`, `cpg_load_bmp`, `cpg_render_copy`, and friends — is seventeen functions chosen to be the smallest surface that still runs a game.

## Two sessions, 229 turns, one commit

The repo was built in a single Codex build session on **9 February 2026** (session `019c41c6`, GPT-5.2, xhigh reasoning, ~61 minutes) from an empty directory. Six user prompts in that session — realistically, three load-bearing ones: "Write a pygame framework for COBOL", a terminal paste of `libcob: error: module 'cpg_init' not found`, and "write a Flappy bird in COBOL now, thanks to the new framework." Zero clarification questions from the agent; three sequential, non-contradictory requests. A second session on **19 March 2026** was a Claude Code analyst pass that produced the backlog and appendix but wrote no new code. Together the two sessions logged **229 turns**, **11 SB entries**, and exactly **one git commit** (git was initialized after the fact; the build session ran without version control).

## What was delivered

Eight files, 1,031 LOC, split roughly 422 C / 492 COBOL / 47 Make / 56 Markdown / 14 config.

- `src/cpg.c` (367 LOC) — the `cpg_*` C shim with NULL-safety on every entry point, `cpg_copy_trim` for COBOL string marshalling, and a fallback software renderer.
- `src/cpg.h` (55 LOC) — API declarations plus the `CPG_Event` POD.
- `cobol/cpg.cpy` (40 LOC) — the copybook that makes the framework look native: `USAGE POINTER` handles, a `CPG-EVENT` 01-record mirroring the C struct with `COMP-5` fields, and `78`-level constants for SDL2 event types and keycodes.
- `examples/hello.cob` (106 LOC) — bouncing-rectangle smoke test.
- `examples/flappy.cob` (346 LOC) — Flappy Bird with gravity, three scrolling pipes (`OCCURS 3 TIMES`) with randomised gaps, AABB collision detection, score in the window title, game-over/restart via level-88 state flags, and a ~60 FPS loop.
- `Makefile`, `README.md`, `.gitignore`.

Three build failures, all self-repaired within one cycle each: `BINARY-LONG` rejected by GnuCOBOL 3.2 (switched to `COMP-5`), `libcob: module 'cpg_init' not found` (added `-fstatic-call` — GnuCOBOL defaults to dynamic `dlsym` resolution, which silently fails against a statically linked C library), and a pipe-rendering variable bug in Flappy.

## Validation — and what it did not cover

"Working" here means the build is green and the example games can be launched. The agent ran in a sandbox without a display, so runtime verification was the user's job: implicit confirmation came from the bug report in session one (the user had already managed to run `make`) and from the absence of follow-up after Flappy was delivered. There are no automated tests. The weak link was Makefile prerequisite tracking — the first `-fstatic-call` rebuild did not trigger because the Makefile itself was not listed as a prerequisite to build targets; the agent patched that in the same fix.

## Compute and context footprint

This project is striking for how cheap it was. Combined across both sessions: **peak context 111 k on the Claude Code analyst run (out of 1 M available) and 45 k on the Codex build (out of 258 k)**, **zero compactions in either session**, and total spend of **~6.9 M tokens** across build + analysis — **the lowest total tokens of any buildable deliverable in the cohort**. The build session alone was ~1.15 M tokens in 61 minutes. The model never hit a wall that required summarisation or context reset.

## Why the result is worth flagging

Few COBOL projects even attempt COBOL → C → SDL2. Most legacy COBOL lives inside batch pipelines, CICS, or DB2 — the language has no cultural tradition of real-time graphics, and its CALL ABI actively resists it. What the agent delivered is not a pygame replica; it is the minimal, consistent, NULL-safe FFI contract that a COBOL caller needs before any graphics are possible, plus two callers that exercise the contract end-to-end.

## Surprising insight: the purest system-integration project in the set

In the feature-class profile, **the top 12 ranked features contain zero ALG, zero DOM, zero VER, zero PRO, and zero PRF entries**. The centre of gravity is entirely SYS (FFI / cross-runtime) and LNG (COBOL-dialect and CALL-resolution knowledge), with CMP appearing only twice and exactly where it should — at the two composition proofs, hello and Flappy. Compared to the chess, compiler, and SAT projects, COBOL-pygame contains no algorithmic invention at all. That is not a failure mode; it is the whole point. The deliverable is a boundary, and the boundary holds.
