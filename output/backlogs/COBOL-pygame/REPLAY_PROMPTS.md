# Replay Prompts

Reusable prompts for reproducing the "pygame-for-COBOL" framework project step by step. Each prompt is self-contained enough to copy-paste into a coding agent session. They specify **what** to build (behavior, inputs, outputs, verification), not **how** (no specific C API names, no FFI layout prescription, no COBOL-specific idioms mandated).

Use them sequentially: each step builds on the previous one.

For reference on what was actually built (which libraries were chosen, which bugs came up, which API shape the Codex agent settled on), see [SPECIFICATION_BACKLOG.md](SPECIFICATION_BACKLOG.md).

---

## Step 1: Minimal Graphical Framework for COBOL

> Create a small "pygame-like" graphical framework that can be called from **COBOL** programs compiled with **GnuCOBOL** (`cobc`). The framework itself may be written in any host language you think appropriate (e.g., a thin C layer over an existing cross-platform graphics/windowing library), as long as the result is a library that a COBOL program can link against and call.
>
> The framework must let a COBOL program do the following, through whatever calling convention you design:
>
> - Initialize and later shut down the graphics subsystem.
> - Open a single resizable window of a requested width and height with a caller-supplied title, and obtain whatever handle(s) are needed to draw into it.
> - Set a current drawing color (RGBA or equivalent).
> - Clear the window to the current color, and present/flip the frame so drawing becomes visible.
> - Draw basic 2D primitives: a line between two points, an outlined rectangle, and a filled rectangle.
> - Poll input events in a non-blocking loop; at minimum the caller must be able to distinguish: window-close requested, a key was pressed (with which key), a key was released, mouse motion, and mouse button down/up (with which button and where).
> - Sleep for a given number of milliseconds, and read a monotonic millisecond tick counter.
> - Update the window title at runtime.
>
> Deliver:
>
> - The framework source (C or equivalent) plus any COBOL copybook/include file needed so a COBOL program can reference event fields, key codes, and handle types symbolically rather than by magic numbers.
> - A build system (a `Makefile` is fine) that compiles the framework into a static library, then compiles a COBOL program against it into an executable.
> - A short `README.md` describing prerequisites and how to build and run.
>
> Design notes (non-prescriptive):
>
> - You choose the function names, the way handles are represented in COBOL (pointer, opaque integer, index, ...), the event-struct layout, the argument-passing convention (`BY VALUE` vs `BY REFERENCE`), and how strings are marshalled from COBOL to C. Pick whatever makes GnuCOBOL happy and document it.
> - You do **not** need to implement text rendering, audio, or loading arbitrary image formats at this step. Plain color rectangles are enough.
> - You may scope to one platform (macOS, Linux, or Windows) if cross-platform is costly; just say so in the README.
>
> Verification (required):
>
> - `make` (or the equivalent one-liner from your README) completes with no errors on a clean checkout.
> - The COBOL side compiles against your framework without needing any handwritten C glue inside the COBOL program — only a COPY of your copybook.

---

## Step 2: Visible-Animation Example Program

> Using the framework from Step 1, write an example **COBOL** program that proves the framework actually works end to end. The program must:
>
> - Open a window of roughly 640 x 480 with a descriptive title.
> - Run a main loop that, on each iteration: polls input, updates state, clears the window to a background color, draws at least one filled rectangle in a different color, and presents the frame.
> - Animate: the rectangle must visibly move (e.g., bounce off the window edges, or slide across) so a human watching the window can confirm rendering is live and not a static image.
> - Target roughly 60 frames per second using the timing primitives from Step 1 (sleep / ticks — you decide whether to use a fixed delay or measure-and-sleep).
> - Exit cleanly when the user closes the window **or** presses Escape. "Cleanly" means: the main loop terminates, the window is destroyed, the graphics subsystem is shut down, and the process exits with status 0.
>
> Wire this example into the build system from Step 1 (e.g., `make` builds it by default, `make run` launches it).
>
> Verification (required):
>
> - Running the example opens a window; the rectangle visibly moves; pressing Escape closes the window and the process exits without error; clicking the window's close button has the same effect.
> - The program contains only COBOL plus your copybook — no inline C, no FFI boilerplate beyond what the copybook and `CALL` statements provide.
>
> If your build or the COBOL runtime fails to find the framework's entry points at run time (a common GnuCOBOL pitfall because `CALL` can default to dynamic symbol lookup), investigate and fix it so the example runs out of the box. Document the fix in the README.

---

## Step 3: Extend the Framework with Bitmap / Image Support

> Extend the framework from Step 1 so that a COBOL program can load an image from disk and draw it into the window.
>
> Requirements:
>
> - Support at least one common image file format that can be loaded without pulling in a heavyweight third-party dependency (e.g., BMP is a reasonable minimum; if the underlying library you chose already supports more, expose more).
> - A COBOL program can: load an image from a file path into an opaque texture/surface handle, learn its pixel dimensions, draw it at an (x, y) position with an optional destination size, and later release the handle.
> - Errors (file missing, unsupported format, out of memory, etc.) are reported in a way a COBOL program can detect and surface — for example a non-zero return code plus a way to retrieve a human-readable error string into a COBOL buffer.
>
> Update the copybook (or equivalent) so the COBOL side has names for the new handle type and any new constants.
>
> Verification (required):
>
> - Add a tiny test program or extend the Step 2 example so that pressing a key (or just at startup) loads a small image you ship in the repo and draws it. The image must appear in the window.
> - Deliberately loading a missing file returns a detectable error to the COBOL caller and does **not** crash.

---

## Step 4: A Real Game — Flappy Bird

> Using the framework from Steps 1–3, implement **Flappy Bird** as a COBOL program. No C code inside the game itself — game logic, physics, rendering calls, input handling, and scoring all live in a single `.cob` file that uses the framework.
>
> Behavior:
>
> - A tall portrait-ish window (roughly 480 x 640 works well, but you pick).
> - A "bird" (a single colored rectangle is fine) sits at a fixed horizontal position. Gravity pulls it downward each frame. Pressing Space, Up-arrow, or clicking the left mouse button applies an upward impulse ("flap").
> - A small number of "pipes" (3 is enough) scroll from right to left at a constant speed. Each pipe has a vertical gap the bird must fly through. When a pipe exits the left edge, it wraps around to the right with a newly randomized gap position.
> - There is a ground strip at the bottom that the bird can crash into.
> - Collision detection: if the bird's bounding box overlaps any pipe (top or bottom segment) or touches the ground, the game enters a "game over" state.
> - Score: each time the bird successfully passes a pipe, score increments by 1. The score is visible to the player — displaying it in the window title is fine (text rendering inside the window is **not** required).
> - Game-over state: the bird stops moving, input no longer flaps; pressing Space (or clicking) resets the game to its initial state with score 0.
> - The main loop is frame-rate-limited to roughly 60 FPS.
> - Escape or the window-close button exits cleanly.
>
> Wire the game into the build system so it builds alongside the Step 2 example and can be run with a single command (e.g., `make run-flappy`).
>
> Verification (required):
>
> - Building the whole project from a clean state succeeds with one `make` invocation.
> - Running the game: a window appears with sky/pipes/ground/bird visible; gravity pulls the bird down if nothing is pressed; pressing Space flaps the bird up; pipes scroll leftward; flying into a pipe or the ground ends the game; pressing Space after a game-over restarts it; the score visibly increments when a pipe is passed; Escape exits cleanly.
> - No crashes, no hangs, no leaked windows after exit.

---

## Step 5: Documentation and Reproducibility

> Finalize the project so a fresh user can reproduce it without reading source code.
>
> Write or update:
>
> - `README.md` at the repo root covering: what the project is, prerequisites (GnuCOBOL version, graphics/system libraries, platform), how to build, how to run each example, the list of functions the framework exposes (with one-line descriptions), and how a COBOL program is expected to use the copybook (argument-passing conventions, handle lifecycle).
> - A short list of **known gotchas** the COBOL-calling-a-C-library path can hit on the toolchains you tested — for example, any compiler flags that are required for the COBOL runtime to resolve the framework's symbols, or any data-type substitutions you had to make in the copybook to satisfy your GnuCOBOL version. State the error message a user would see if they forget each flag, so they can match symptoms to fixes.
> - A minimal "example skeleton" snippet in the README showing the shortest-possible COBOL program that opens a window, clears it once, waits for a key, and exits — useful as a starting template.
>
> Verification (required):
>
> - Delete the `build/` (or equivalent) directory; follow the README instructions verbatim from a shell; both the bouncing-rectangle example and Flappy Bird build and run.
> - The README's "framework functions" list matches what the copybook actually exposes (no drift).
