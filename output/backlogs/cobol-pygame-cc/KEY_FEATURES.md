# Key Features — cobol-pygame-cc (PYGAME-COBOL-CLAUDE)

## Preamble

> **Provenance.** Authored 2026-08-20 by the study authors from the archived raw
> session transcript (`output/raw_sessions/cobol-pygame-cc__956ecb73….jsonl`),
> the delivered source (764 COBOL code lines across 5 files + a 294-line SDL2
> C shim), and the replay pack's five-step protocol. Same conventions and
> score formula as the thirteen analyst-generated ledgers
> (depth × (1 + 0.5 × effort)).

The project answers the corpus's most open-ended prompt ("write a pygame
framework for COBOL") with a thin SDL2 C shim behind a copybook API, so that
game logic, physics, and rendering live entirely in COBOL. It ships four
runnable examples — a bouncing rectangle, an interactive demo, a BMP image
test, and a complete Flappy Bird clone in pure COBOL — plus a
fresh-user README whose "known gotchas" section documents real
GnuCOBOL-toolchain findings. The center of gravity is SYS (FFI/ABI design)
and LNG (COBOL-side language work), with the Flappy Bird game as the
composition capstone.

## Ranked table

| Rank | SB id | Title | Class | Depth | Effort | Score | Evidence | Significance note |
|------|-------|-------|-------|-------|--------|-------|----------|-------------------|
| 1 | F-01 | SDL2 C shim with a static-call-safe ABI (every function `int`-returning, singleton context, string+length convention) | SYS+LNG | 3 | 3 | 7.5 | `pygame_cobol.c` (294 LOC, 24 `pg_*` functions); README §Design decisions, §Gotcha 2 (`-fstatic-call` emits `extern int` — `void` returns corrupt the return register on ARM64) | The framework's foundation: an ABI designed around how GnuCOBOL's `-fstatic-call` actually generates calls, discovered and documented from observed misbehavior, not from a manual. |
| 2 | F-06 | Flappy Bird clone in pure COBOL on the framework (gravity, pipes, collision, score, restart) | CMP+ALG | 3 | 2 | 6.0 | commit `b9482aa`; `flappy.cob` (366 LOC, 34 CALLs); experimenter-observed playability (rubric draft Q1) | Only meaningful once the whole stack exists: window, colors, rects, events, timing. Physics and game state are COBOL data items; the C side draws pixels. The corpus's most visible composition artifact on this family. |
| 3 | F-02 | Copybook API: `PG-EVENT` record, keycode/event constants, `PG-RC`/`PG-ERROR-MSG`, `BINARY-LONG` mapping to C `int32_t` | LNG+DOM | 2 | 2 | 4.0 | `pygame_cobol.cpy` (90 LOC); README §Using the copybook, §Gotcha 5 | The COBOL-side contract: a 20-byte event record passed BY REFERENCE, constants for SDL's extended keycode range, and the representation argument for why `PIC 9(n)`/`COMP-3` would garble raw 32-bit writes. |
| 4 | F-04 | Toolchain gotcha diagnosis and documentation (`-fstatic-call`, `FUNCTION TRIM` PERFORM-loop bug on GnuCOBOL 3.2.0/ARM64, `-free`, string-length convention) | LNG+INF | 2 | 2 | 4.0 | README §Known gotchas 1–6 with symptom/cause/fix for each | Language-and-toolchain findings earned in-session (symptom-first write-ups), including a workaround for a real GnuCOBOL 3.2.0 ARM64 bug — knowledge transfer beyond this repo. |
| 5 | F-03 | BMP image pipeline: load/draw/scale/free with a 64-handle table, plus a C test-asset generator and visual test program | SYS+DOM | 2 | 2 | 4.0 | `pg_load_image`/`pg_draw_image_sized`/`pg_free_image` in `pygame_cobol.c`; `imgtest.cob` (186 LOC); `gen_test_bmp.c`; `test.bmp` | Handle-based resource management exposed to COBOL as 1-based `BINARY-LONG` handles with error sentinel −1; the generator makes the visual test reproducible from a clean checkout. |
| 6 | F-05 | Event loop and input mapping (non-blocking poll, keyboard/mouse events, Escape/close exit paths) | SYS | 2 | 1 | 3.0 | `pg_poll_event` + event constants; `demo.cob` (135 LOC) interactive example | The pygame-style interaction model: COBOL PERFORM loop polling a C-filled record until quit. |
| 7 | F-07 | Clean-checkout build system (Makefile: library, 4 examples, test asset; `make run-*` targets) | INF+VER | 1 | 1 | 1.5 | `Makefile`; clean-checkout `make` re-verified post-hoc (the pack's step-5 criterion) | The family's oracle is behavioral: everything builds and runs from a fresh clone. |
| 8 | F-08 | Frame timing: vsync renderer plus measure-and-sleep loop in the examples | PRF | 1 | 1 | 1.5 | README §Design decisions (PRESENTVSYNC); `bounce.cob` (138 LOC) timing loop | Modest but real: stable animation pacing across the examples. |

## Composition chains

1. **Shim → copybook → examples → Flappy Bird** — F-01 (ABI) → F-02 (COBOL
   contract) → F-05/F-08 (event/timing loops in bounce/demo) → F-03 (images)
   → F-06 (a complete game). Each layer is only exercisable because the
   previous one works; the game is the emergent capability the prompt asked
   for ("pygame for COBOL" demonstrated by an actual game).
2. **Misbehavior → gotcha → design rule** — the `void`-return corruption and
   `FUNCTION TRIM` loop bug (F-04) fed back into F-01's design decisions
   (all-`int` ABI) and the README's fresh-user warnings.

## Significance profile

| Class | Count in top 8 |
|-------|----------------|
| SYS   | 3 |
| LNG   | 3 |
| DOM   | 2 |
| CMP   | 1 |
| ALG   | 1 |
| INF   | 2 |
| VER   | 1 |
| PRF   | 1 |

Centre of gravity: **SYS + LNG**, with the Flappy Bird CMP entry as the
capstone — matching the family's design intent (COBOL as a caller into
modern ecosystems).

## Verdict

FFI-and-framework project: the achievement is a deliberately thin,
correctly-shaped boundary (C draws, COBOL decides) plus the documented
toolchain knowledge to keep it working — demonstrated end-to-end by a
playable pure-COBOL game and a clean-checkout build oracle.
