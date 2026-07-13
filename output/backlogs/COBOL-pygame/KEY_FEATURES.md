# Key Features — COBOL-pygame

## Preamble

The project was asked to "write a pygame framework for COBOL (using GNUcobol)": build a graphical framework callable from GnuCOBOL programs, then demonstrate it with playable examples. The delivered chain is **COBOL `CALL` → C shim (`cpg_*`) → SDL2** (the "pygame-like" framing is naming; there is no Python in the runtime path — the agent correctly reinterpreted "pygame" as "SDL2-backed primitives with a pygame-shaped surface"). A "key feature" here is anything at depth ≥ 1 that either (a) crosses the COBOL/C/SDL2 boundary, (b) encodes framework surface into a COBOL-idiomatic copybook, or (c) composes the framework into a runnable COBOL program. Pure documentation and trivial Makefile targets are excluded. Total corpus is ~1,031 LOC across 8 files; expect an SYS-heavy profile with LNG support (COBOL-side idioms pushed against GnuCOBOL's CALL ABI) and one CMP peak at the Flappy Bird composition.

## Ranked table

| Rank | SB/BL id | Title | Class | Depth | Effort | Score | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | SB-002 / SB-003 / BL-001 | `cpg_*` C shim bridging GnuCOBOL `CALL` to SDL2 (17-function surface, `void**` handle ABI, `BY VALUE`/`BY REFERENCE` discipline) | SYS (LNG) | 3 | 2 | 6.0 | `/Users/mathieuacher/SANDBOX/COBOL-pygame/src/cpg.c` (367 LOC); `/Users/mathieuacher/SANDBOX/COBOL-pygame/src/cpg.h:21-48`; 20+ API-design reasoning traces [T:event_037–067] |
|  |  | Significance note: This is the load-bearing engineering of the whole project — not an algorithm, but a working cross-runtime contract. Every function takes `void**` because GnuCOBOL has no native pointer type other than `USAGE POINTER`, and the double-indirection lets COBOL pass an 01-level `POINTER` cell by reference to hold opaque SDL2 `*Window`/`*Renderer`/`*Texture`. The hard part is negotiated at the boundary, not inside any one function. |
| 2 | SB-008 / BL-003 | Flappy Bird in COBOL on top of the framework (gravity, 3 scrolling pipes with randomized gaps, AABB collisions, score→title, game-over/restart, ~60 FPS loop) | CMP (DOM) | 2 | 2 | 4.0 | `/Users/mathieuacher/SANDBOX/COBOL-pygame/examples/flappy.cob` (346 LOC); [T:event_200–214] |
|  |  | Significance note: Composition feature — exists *only because* the shim (#1), the copybook (#3) and the event-struct mirror (#4) work. Not an algorithm: the substance is expressing game state (`OCCURS 3 TIMES` pipe array, level-88 state flags `STATE-PLAYING`/`STATE-GAMEOVER`, `FUNCTION RANDOM` seeded by `cpg_ticks`) in COBOL idioms under a real-time frame budget. |
| 3 | SB-003 | `cpg.cpy` COBOL copybook: `USAGE POINTER` handles + `CPG-EVENT` 01-record + level-78 constants for SDL2 event types and keycodes | LNG (DOM) | 2 | 1 | 3.0 | `/Users/mathieuacher/SANDBOX/COBOL-pygame/cobol/cpg.cpy` (40 LOC) |
|  |  | Significance note: Language-level — makes the framework *look* native to a COBOL caller by hoisting `SDL_QUIT=256`, `SDLK_ESCAPE=27`, etc. into `78`-level constants and giving the event a conventional 01/05 layout. Domain modelling of SDL2's surface into COBOL vocabulary. |
| 4 | SB-003 | `CPG_Event` struct ↔ COBOL 01-record layout mirror with `COMP-5` fields chosen for C `int32_t` ABI compatibility | SYS | 2 | 1 | 3.0 | `/Users/mathieuacher/SANDBOX/COBOL-pygame/src/cpg.h:10-19`; `/Users/mathieuacher/SANDBOX/COBOL-pygame/cobol/cpg.cpy:9-18`; `cpg_poll_event` demux `/Users/mathieuacher/SANDBOX/COBOL-pygame/src/cpg.c:197-237` |
|  |  | Significance note: Cross-runtime data contract. The C side flattens SDL2's tagged union (`SDL_Event`) into a fixed 8×`int32_t` POD so that COBOL's fixed-record model can receive it by reference. This is integration engineering — misalign a field and COBOL reads garbage. |
| 5 | SB-005 / BL-002 | `-fstatic-call` diagnosis & Makefile fix for `libcob: error: module 'cpg_init' not found` (static vs dynamic `CALL` resolution in GnuCOBOL) | LNG (INF) | 2 | 1 | 3.0 | `/Users/mathieuacher/SANDBOX/COBOL-pygame/Makefile:14`; [T:event_136–182] |
|  |  | Significance note: A deep GnuCOBOL-specific gotcha, not a generic build tweak. GnuCOBOL defaults to `dlsym` lookup for `CALL "c_name"`, which silently fails against a *statically linked* C library. Fixing it requires understanding both the COBOL runtime's call model and the C linker — pure language-boundary engineering. |
| 6 | SB-002 | NULL-safety + trimmed-string marshalling at every C entry point (COBOL space-padded fixed-width strings → `char*` + `int len`) | SYS | 2 | 1 | 3.0 | `/Users/mathieuacher/SANDBOX/COBOL-pygame/src/cpg.c:8-32` (`cpg_copy_trim`), used at `:53-93`, `:123-134`, `:252-294` |
|  |  | Significance note: Every `cpg_*` function is NULL-guarded and every string argument arrives as `(const char*, int len)` because COBOL has no null-terminator convention. This is the friction tax of the FFI boundary paid consistently — not an algorithm, but the right plumbing. |
| 7 | SB-001 / SB-003 / SB-009 | Makefile build system: sdl2-config integration, C static archive (`libcpg.a`), `cobc -x -free -fstatic-call` linker command, two example targets | INF | 1 | 1 | 1.5 | `/Users/mathieuacher/SANDBOX/COBOL-pygame/Makefile` (47 LOC) |
|  |  | Significance note: Standard Make plumbing, but the mixed-toolchain rule (`$(COBC) -x $(COBFLAGS) ... $< $(CPG_LIB) $(SDL_LIBS)`) correctly composes cobc + cc + ar + sdl2-config — the non-trivial bit is knowing cobc can accept a `.a` and extra `-l` flags on its command line. |
| 8 | SB-003 | `hello.cob` bouncing-rectangle demo: first end-to-end SDL2 frame driven from COBOL (event loop, clear/fill/present, delay-based pacing) | CMP | 1 | 1 | 1.5 | `/Users/mathieuacher/SANDBOX/COBOL-pygame/examples/hello.cob` (106 LOC) |
|  |  | Significance note: Composition — the minimal proof that #1+#3+#4 actually render. Without it there's no evidence the framework *works*. Depth is low because the game logic is trivial; its value is as the framework's smoke test. |
| 9 | SB-004 | `BINARY-LONG` → `COMP-5` portability fix for GnuCOBOL 3.2 (initial build failure and recovery) | LNG | 1 | 0 | 1.0 | `/Users/mathieuacher/SANDBOX/COBOL-pygame/cobol/cpg.cpy:11-18`; [T:event_076–093] |
|  |  | Significance note: A small but real COBOL-dialect diagnosis. `BINARY-LONG` is valid ISO-2002 COBOL but not accepted by GnuCOBOL 3.2 in this position; `COMP-5` gives the same 32-bit-binary-native semantics with wider compiler coverage. One-line fix, concrete language-level knowledge. |

## Composition chains

1. **C shim (#1) → event-struct mirror (#4) → copybook (#3) → hello demo (#8)** — the minimal vertical slice proving that an SDL2 frame can be rendered and an SDL2 event can be received, both driven from a COBOL `PROCEDURE DIVISION`. This is the chain that legitimizes every other feature.
2. **C shim (#1) → copybook (#3) → event-struct mirror (#4) → `-fstatic-call` fix (#5) → Flappy Bird (#2)** — a playable game at ~60 FPS is only meaningful once the CALL resolution is actually wired: without #5 the COBOL binary crashes on `cpg_init`; without #1/#3/#4 there is nothing to call. Flappy is the emergent capability.
3. **Makefile (#7) → C shim (#1) → hello (#8) + Flappy (#2)** — the build system composes the mixed toolchain (cc for C, ar for archive, cobc for COBOL+link) into a single `make` that produces two runnable binaries. Change #7 and both examples stop building.
4. **`BINARY-LONG`→`COMP-5` fix (#9) → copybook (#3) → event-struct mirror (#4)** — the data-type choice in the copybook is a precondition for the struct layout to compile at all; without #9 the whole copybook-based interop chain never boots.

## Significance profile

| Class | Count (primary) | Count (incl. secondary) |
|---|---:|---:|
| SYS (System integration / FFI) | 3 | 4 |
| LNG (Language-level achievement) | 2 | 4 |
| CMP (Emergent composition) | 2 | 2 |
| DOM (Domain modelling) | 0 | 2 |
| INF (Infrastructure / tooling) | 1 | 2 |
| ALG | 0 | 0 |
| PRO | 0 | 0 |
| VER | 0 | 0 |
| PRF | 0 | 0 |

Centre of gravity: **SYS + LNG**, with CMP appearing twice exactly where composition pays off (hello, Flappy). Zero ALG/PRO/VER/PRF — consistent with the assessment's "FFI proof-of-concept" verdict: no algorithm invention, no standard to comply with, no measured performance, no verification harness.

## Verdict

**System-integration-centric, with a language-achievement backbone** — the project's substance is the COBOL↔C↔SDL2 boundary (ABI, handles, struct mirrors, dialect-specific linker semantics), not algorithms; the two composition features (hello, Flappy) are valuable as proofs that the boundary works, not as algorithmic contributions.
