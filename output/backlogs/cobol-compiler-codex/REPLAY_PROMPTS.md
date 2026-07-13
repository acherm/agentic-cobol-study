# Replay Prompts

Reusable prompts for reproducing the `minicobc` project step by step. Each prompt is self-contained enough to copy-paste into a coding agent session. They specify **what** to build (behavior, inputs, outputs, verification), not **how** (no lexer/parser/codegen strategy mandated, no data-structure prescriptions, no COBOL-specific compiler idioms required).

Use them sequentially: each step builds on the previous one. The end state is `minicobc`, a compiler for a documented subset of COBOL **written in COBOL** (bootstrapped with GnuCOBOL via `cobc -x -free`, emitting C that is linked with `gcc`), that (1) compiles and runs a corpus of non-trivial COBOL programs, (2) is **differentially tested against GnuCOBOL** — same program in, same observable stdout out, (3) **self-bootstraps** by compiling its own source `src/minicobc.cob`, (4) carries an optimization mode and a GnuCOBOL-vs-minicobc performance benchmark, and (5) compiles real-world COBOL codebases (a chess engine, the COBOL DOOM port, Flappy Bird) with a validation apparatus (perft counts, python-chess legality, end-to-end Elo) wrapped around GnuCOBOL as the oracle. The two load-bearing reproduction oracles throughout are **differential testing against GnuCOBOL** (`cobc -x -free`) and **self-bootstrap**.

For reference on what was actually built (subset supported, generic vs compatibility paths, commits, benchmark numbers, the miscompile that was caught), see [SPECIFICATION_BACKLOG.md](SPECIFICATION_BACKLOG.md).

> **How to read this replay.** `minicobc` was built *objective-first* and highly
> exploratorily: across ~90 turns the human repeatedly redirected the goal ("now
> make it bootstrap", "now compile DOOM", "now go generic", "now the chess engine"),
> and the single most important result — a caught **miscompile** — surfaced only
> because the human distrusted a suspiciously good benchmark, not from any planned
> step. The steps below are an **idealized linearization** of that process: a
> faithful recipe for the *end state*, not a transcript of how it unfolded. Steps
> marked **`[objective loop]`** (Step 4 self-bootstrap, Step 8 miscompile hunt) have
> no fixed endpoint — you iterate until a stopping oracle is met, and success is not
> guaranteed on a linear pass. Several middle steps were *emergent expansions*
> ("now also compile X"), not a pre-planned roadmap. The actual ordered human
> interventions are preserved verbatim at the end, under
> [*What actually happened*](#what-actually-happened-the-real-session-trace).

---

## Step 1: COBOL-in-COBOL Compiler Core + Sample Corpus

> Start a fresh workspace. Build a COBOL compiler whose own source is a COBOL program. The compiler — call its binary `minicobc` — reads a free-format `.cob` file and emits a C translation unit; a system C compiler (`gcc`) then turns that C into a native executable. GnuCOBOL (`cobc -x -free`) may be used **only** to bootstrap your compiler (compile its COBOL source) and later as an oracle — never as a code generator your compiler delegates to.
>
> A documented subset is required, not a full COBOL-85 front end. The first milestone must recognise the four divisions (`IDENTIFICATION`, `DATA` with `WORKING-STORAGE`, `PROCEDURE`), elementary `01`/`05`/`77` items with `PIC 9(...)`, `PIC Z…`, `PIC X(...)` and optional `VALUE`, and a core set of statements: `DISPLAY`, `ACCEPT`, `MOVE`, `INITIALIZE`, `ADD`/`SUBTRACT`/`MULTIPLY`/`DIVIDE`, `COMPUTE`, `IF`/`ELSE IF`/`ELSE`/`END-IF`, and `STOP RUN`.
>
> Ship three small but **non-trivial** COBOL programs your compiler can translate and run end-to-end — a primes sieve, a Collatz-sequence printer, and a GCD program — under `examples/`, each with a pinned expected-output file under `expected/`.
>
> Provide a demo script (`scripts/demo.sh`) and a test script (`scripts/test.sh`): build `minicobc` from its COBOL source with `cobc -x -free`, compile each example program to C, link with `gcc`, run, and diff stdout against `expected/*.txt`. Document the supported subset and the deliberate constraints in a `README.md`.
>
> Verification:
> - `scripts/demo.sh` builds `minicobc` and prints non-trivial program output (not "Hello world") for primes, Collatz, and GCD.
> - `scripts/test.sh` diffs each example's stdout against its `expected/*.txt` and reports success for all three.
> - The README states the supported COBOL subset and the constraints.
> - `minicobc`'s own source is a single `PROGRAM-ID.` COBOL file that `cobc -x -free` accepts.

---

## Step 2: Differential Testing Against GnuCOBOL

> Your three sample programs currently pass only against pinned `expected/` files. Tighten the oracle: every sample program in `examples/` must be valid free-format COBOL that **both** `minicobc` and GnuCOBOL (`cobc -x -free`) accept and run, producing **byte-identical stdout**.
>
> Rewrite `primes.cob`, `collatz.cob`, and `gcd.cob` as needed so `cobc -x -free` compiles them cleanly, then extend the test harness so that for each program it: (a) compiles+runs it through `minicobc` → C → `gcc`, (b) compiles+runs the same source through `cobc -x -free`, and (c) diffs the two stdout streams. A mismatch is a test failure that names the offending program and shows the diff. This GnuCOBOL differential check — same program in, same observable output out — is the primary correctness oracle for the rest of the project.
>
> Verification:
> - `cobc -x -free examples/primes.cob` (and `collatz`, `gcd`) compiles with no errors.
> - For each sample, `minicobc` stdout == `cobc -x -free` stdout (empty diff); `scripts/test.sh` fails loudly on any divergence.
> - The pinned `expected/*.txt` files still match, so both oracles (golden file + GnuCOBOL diff) agree.

---

## Step 3: External Corpus + Benchmark Manifest + GnuCOBOL Performance Comparison

> Point `minicobc` at a real external COBOL codebase: the Game-of-15 / tic-tac-toe programs from `acherm/agentic-cobol-game15tictactoe` pinned at commit `4ae3129`. Check the repo out under `external/agentic-cobol-game15tictactoe` at that commit, and make `minicobc` compile and run its programs, with GnuCOBOL output as the oracle for each (it is acceptable at this stage to bridge the hardest programs through a pinned compatibility C template under `templates/compat/`, as long as the observable output matches GnuCOBOL — record clearly which programs use the generic path and which use a template).
>
> Then design a benchmark out of every COBOL program exercised so far. Ship a declarative manifest `benchmark/cases.json` enumerating each case with its oracle (stdout match against `expected/` **or** against GnuCOBOL). Add a comparison runner (`scripts/compare-compilers.sh` + a `compare_compilers.py`) that, for each case, records compile time and run time for `minicobc + gcc` versus `cobc -x -free`, and writes a JSON + Markdown report.
>
> Verification:
> - Every Game-of-15 program either runs through `minicobc` with stdout matching `cobc -x -free`, or is documented as template-bridged with matching output.
> - The benchmark suite passes all of its declared cases (verdicts match the oracle column in `benchmark/cases.json`).
> - The comparison runner produces a JSON + Markdown report with per-case `minicobc` vs `cobc` compile-time and run-time columns; a baseline report is committed.

---

## Step 4: Self-Bootstrap  `[objective loop]`

> **Objective, not a one-shot milestone.** This step is "extend the subset *until*
> it accepts its own source" — an open-ended loop, not a fixed change. Each cycle:
> run `minicobc` on `src/minicobc.cob`, find the next unsupported construct it
> trips on, add support for it (keeping every earlier oracle green), repeat. The
> **stopping oracle** is a real three-stage self-host reproduction (below). In the
> original session this objective was *not* in the plan — it arose mid-build from
> the human asking "is minicobc able to compile minicobc, and thus bootstrap?";
> whether it converges on a linear pass is not guaranteed.
>
> Demonstrate that `minicobc` can compile `minicobc`. Extend the compiler's subset until it accepts its own source `src/minicobc.cob`, and add a bootstrap / self-host check `scripts/test-selfhost.sh` that performs a three-stage reproduction:
>
> - **stage 0:** build `minicobc` from its COBOL source with `cobc -x -free` (the trusted bootstrap binary).
> - **stage 1:** run that `minicobc` on `src/minicobc.cob` to emit the compiler's own C translation unit, and build a second compiler binary from it.
> - **stage 2:** confirm self-host reproduction — the stage-1 compiler reproduces the corpus results (every Step 1–3 sample still compiles and still matches GnuCOBOL stdout), and the bootstrap output is stable / diffable.
>
> If a pinned compatibility template is needed to make `src/minicobc.cob` go through (e.g. a `MINICOB` template under `templates/compat/`), that is acceptable provided the self-host check is real and the reproduction is verified — document the boundary in the README.
>
> Verification:
> - `scripts/test-selfhost.sh` runs all three stages and reports self-host success.
> - The stage-1 (`minicobc`-built) compiler reproduces the test corpus: every sample still matches `cobc -x -free` stdout.
> - The bootstrap is reproducible (re-running the script yields the same stable result, exit code 0).

---

## Step 5: Compile a Real Chess Engine + Perft Differential

> Take a challenging real-world target: the COBOL chess engine from `acherm/agentic-chessengine-cobol-codex` pinned at commit `faf0f16`. Check it out under `external/`, and make `minicobc` build it (a pinned compatibility template path under `templates/compat/chess/` is acceptable at this stage; graduating it to the generic front end comes later). The build script (`scripts/build-chess-engine.sh`) must produce a working engine binary.
>
> Then benchmark it the way only a chess engine lets you: **perft**. Add `scripts/compare-chess-perft.sh` that runs perft at a configurable depth on the `minicobc`-built engine and on the `cobc -x -free`-built engine, and confirms the **perft node counts are identical** (perft is an exact, position-determined integer — it is a far stronger oracle than a timing number). Record per-engine wall-clock time and the `minicobc`-vs-GnuCOBOL ratio in `build/perf/chess-perft-compare.json` + `.md`.
>
> Verification:
> - `scripts/build-chess-engine.sh` produces a runnable engine built by `minicobc`.
> - `scripts/compare-chess-perft.sh` reports identical perft node counts for the `minicobc` build and the `cobc -x -free` build at the chosen depth (any divergence fails the script).
> - A JSON + Markdown perft report is written with both engines' timings and the runtime ratio.

---

## Step 6: Optimization Mode

> Add an opt-in optimization mode — `./build/bin/minicobc OPT in.cob out.c` (also reachable via `MINICOBC_OPT=1`) — that applies semantics-preserving passes: start with constant folding, constant propagation, and dead-store elimination, then add strength reduction, loop-condition canonicalization, and width-aware integer selection.
>
> Ship a dedicated optimization corpus `examples/opt/*.cob` (around eight small programs, each exposing one opportunity: constfold, constprop, deadstore, strength, loopcanon, smallwidth, a boolean chain, an LCG). Add a comparison script `scripts/compare-minicobc-optimizations.sh` that runs each program baseline vs `OPT` and records the difference. The hard constraint: **OPT must not change observable behavior** — every opt-corpus program, every Step 1–5 sample, must still match GnuCOBOL stdout (and the chess perft counts must be unchanged) with OPT on. If any target is unsafe under OPT, document the limitation in the README rather than silently widening the optimiser.
>
> Verification:
> - With OPT enabled, every opt-corpus and earlier-sample program still matches `cobc -x -free` stdout (no behavior change).
> - `scripts/compare-minicobc-optimizations.sh` reports baseline-vs-OPT measurements for all eight programs.
> - Any target where OPT is unsafe (e.g. the chess engine's perft) is flagged in the README, not hidden.

---

## Step 7: Generic Front-End Re-architecture (DOOM + Generic Chess)

> Replace the per-program compatibility templates with a real generic front end so non-trivial COBOL compiles through actual parsing + codegen, not pinned C. Re-architect the pipeline to handle: `EVALUATE`/`WHEN`/`WHEN OTHER`/`END-EVALUATE`; `PERFORM VARYING ... FROM ... BY ... UNTIL`; paragraph labels and `PERFORM paragraph` (incl. `PERFORM paragraph UNTIL`); alphanumeric storage (`PIC X`), group items, `REDEFINES` with packed-width alignment, `OCCURS` and indexed references `ITEMS(IDX)`; external `CALL "name" USING BY VALUE / BY REFERENCE / RETURNING`; intrinsic functions (`FUNCTION SQRT`, `NUMVAL`, `TRIM`, `MOD`, `REM`); `SEARCH`; qualified `OF`; and multiline free-form statements continued across physical lines.
>
> Use this generic front end to compile two new real targets and graduate two existing ones:
> - The COBOL portion of `acherm/agentic-cobol-doom` @ `18ce52b` — the hard part is the `CALL` boundary to C helpers; build it with `scripts/build-cobol-doom.sh` and publish it as a shareable artefact.
> - The Flappy Bird program from `acherm/agentic-cobol-pygame` @ `b2095a1`, linked against the repo's SDL2 helper, smoke-tested under `SDL_VIDEODRIVER=dummy` (a compatibility template here is acceptable — note it as Partial).
> - Move `game15.cob` and `gameN.cob` off templates onto the generic path.
> - Compile the chess engine through the generic pipeline in staged harnesses (`BOARD`/`FEN`, then `PERFT`, then `SEARCH`, then the top-level `COBOCHESS` driver), cross-checking each phase against GnuCOBOL.
>
> Add a generic-feature smoke script `scripts/test-generic-features.sh` covering every new construct with a regression input under `examples/generic/`.
>
> Verification:
> - `scripts/test-generic-features.sh` passes for every generic construct (each `examples/generic/*.cob` matches `cobc -x -free` stdout).
> - `game15.cob` / `gameN.cob` compile through the generic front end (no template) and match GnuCOBOL.
> - Each chess phase harness (`tests/chess/phase{1,2,3,4}_*`) matches the GnuCOBOL reference: `FEN(startpos)` text, perft counts, shallow-search output, and `COBOCHESS --perft-startpos 2`.
> - `scripts/build-cobol-doom.sh` builds the COBOL DOOM target end-to-end; the Flappy build smoke-tests under `SDL_VIDEODRIVER=dummy`.

---

## Step 8: Validation Apparatus — Miscompile Hunt, Tournaments, Elo  `[objective loop]`

> **This step exists because a human distrusted a result.** It is not a planned
> validation phase — in the original session it was triggered by the human reacting
> to a suspicious benchmark ("it's very strange to beat the runtime of GnuCOBOL…
> are you sure? do you check functional correctness?"). The replay only works if
> you adopt the same skeptical stance: treat any too-good result as a *miscompile
> hypothesis* and loop — form the hypothesis, build a direct equivalence harness,
> isolate the offending statement, fix codegen, re-check — until functional
> equivalence against GnuCOBOL (and a third reference, `python-chess`) holds. The
> **stopping oracle** is byte/perft/move equivalence across the suites below; the
> number of bugs you find this way is not knowable in advance.
>
> Harden the validation around the chess build and treat any suspicious result as a bug, not a win. If the `minicobc`-built engine ever appears to **beat** the GnuCOBOL build's runtime by a large margin, do not trust it — that is a red flag for a miscompile producing a cheaper-but-wrong binary. Investigate functional equivalence directly:
>
> - Build a direct equivalence harness (`scripts/test-chess-phase3-direct.sh` + a C harness) that bypasses the top-level `SEARCH` wrapper and cross-checks `QUIESCE`, recursive `ALPHABETA`, and first-reply moves of the `minicobc` build against the GnuCOBOL build on a fixed FEN. When it diverges, isolate the exact statement, add a minimal regression input under `examples/generic/` that reproduces the miscompile, fix the codegen, and confirm the regression now matches GnuCOBOL.
> - Add a depth-1 cross-check suite that compares generated moves against `python-chess` across a set of FENs (a third independent reference beyond GnuCOBOL), and a diversified fixed-depth search suite over several positions.
> - Add tournament harnesses: paired games `minicobc`-built engine vs GnuCOBOL-built engine (color-swapped starts, no illegal moves recorded), then vs Stockfish across `Skill Level` settings, and finally a real end-to-end Elo assessment through `cutechess-cli` (no adjudication) that plays games, exports PGN, and reports an Elo estimate with a confidence interval.
> - In the README, flag that `minicobc`-vs-GnuCOBOL runtime ratios are "a strong local signal, not a settled general claim," and that `MINICOBC_OPT=1` is unsafe for the chess engine.
>
> Verification:
> - The direct equivalence harness fails on the miscompile, then passes after the fix; the regression input matches `cobc -x -free` output.
> - The depth-1 suite agrees with `python-chess` on every position; the search suite's normalized `info …` / `bestmove` lines match the GnuCOBOL build.
> - The tournament harnesses record no illegal moves; the `cutechess-cli` run plays unadjudicated games, exports PGN, and prints an Elo ± CI.
> - The README carries the caveat on runtime ratios and the OPT-unsafe-for-chess note.

---

## What actually happened (the real session trace)

The steps above are an idealized recipe. For honesty about the *open-ended,
objective-driven* nature of this build, here is the actual ordered sequence of
human prompts from the reference Codex session
(`cobol-compiler-codex__Codex__019d3a4c`, ~90 user turns, condensed). The goal was
redirected repeatedly; the roadmap is retrospective. Bold marks the turns where a
new objective *emerged* or a human judgment changed the course.

1. "Write a COBOL compiler in COBOL. Demonstrate you can run some (non-trivial) COBOL programs with it."
2. "compile/run all COBOL programs at `acherm/agentic-cobol-game15tictactoe` (commit `4ae3129`)"
3. "create a git and commit" · 4. "design a benchmark from the programs tested so far" · 5. "compare performance vs GnuCOBOL"
6. **"I don't get why primes, collatz, gcd are not accepted by GnuCOBOL"** — human probing the differential oracle
7. "minicobc should support valid COBOL programs"
8. **"is minicobc able to compile/build minicobc, and thus bootstrap?"** ← *self-bootstrap objective emerges (Step 4)*
9. "extend minicobc until it can compile its own `src/minicobc.cob`" · 10. "benchmark minicobc when compiled by minicobc" · 11. "include GnuCOBOL in the benchmark" · 12. "commit"
13. **"now a challenging case: compile the COBOL chess engine (`agentic-chessengine-cobol-codex`, `faf0f16`)"** ← *emergent expansion (Step 5)*
14. "leveraging perft, benchmark the chess engine compiled with minicobc vs GnuCOBOL"
15. "implement some compiler optimizations?" (Step 6) · 16. "I want a better COBOL compiler *in general*, not just for chess — design/collect a set of COBOL programs" · 17. "compare no-opt vs opt vs GnuCOBOL" · 18. "next optimization passes"
19–21. "write a status report" · "put it in a README section" · "commit"
22. **"now consider `agentic-cobol-doom` (`18ce52b`) and build the COBOL part"** ← *emergent expansion (Step 7)*
23. "why can't alphanumeric storage, REDEFINES, OCCURS, indexed tables, paragraph PERFORM, EVALUATE be supported?"
24. **"let's go to generic support — re-architect the compiler pipeline"** ← *the pivot off per-program templates*
25–37. *[generic re-arch, driven by short redirections — "let's go" / "continue" / "go ahead"; PIC X, groups, REDEFINES, OCCURS, indexed refs, "full group-overlay support"; interleaved "still not compiling DOOM?"]*
38–41. *[build & run DOOM via minicobc; "did you include optimization?"; commit]*
42–48. *[README subsections; push a new GitHub repo `agentic-cobol-compiler-minicobc`; attribution "created by Mathieu Acher and Codex (GPT-5.4, Extra High)"]*
49. "build the flappy game (`agentic-cobol-pygame`, `b2095a1`) with the compiler"
50–53. **"what do you mean by 'targeted compatibility path'? is it a rewriting? a hack? … at the end, minicobc is compiling *what*?"** — human auditing how much is *really* compiled vs templated
54–56. "fill the gap with `game15.cob`" · "target `gameN`?" · "commit/push"
57. "significant progress in generic compilation on non-trivial programs (chess)…"
58–66. *[chess via generic front end, phased: "target chess engine" → "plan first" → phase 1 → PERFT → SEARCH → top-level COBOCHESS; commits]*
67. "how good is perft performance, minicobc vs GnuCOBOL?"
68. **"it's very strange to beat the runtime of GnuCOBOL… are you sure? do you check functional correctness?"** ← *miscompile hunt trigger (Step 8)*
69–80. *[miscompile investigation: "the compiler may produce a wrong binary"; "could it be randomness?"; external perft test suite; depth=5; "are the proposed moves the same?"; direct QUIESCE / recursive-ALPHABETA equivalence on a fixed FEN; document & commit]*
81. "tournament: chess engine built with GnuCOBOL vs minicobc" · 82. "tournament vs Stockfish at different skills, only the minicobc-built binary" · 83. "commit"
84. "--movetime 50 ms is too small; use 120+1, CCRL 40/4 scale" · 85. "retry/run"
86. **"I'd like real, end-to-end games to assess the Elo of the chess engine compiled with minicobc"**
87–89. "status?" · "status?" · "commit/push (incl. PGN)"
90. "no adjudication at all… write a script and tell me how to run it: play games, export them, report Elo"

*Reading:* the only fixed spec was prompt 1 ("a COBOL compiler in COBOL").
Everything load-bearing — bootstrap, genericity, the miscompile, the Elo
apparatus — **emerged from human steering and reactive skepticism**, not a plan.
This is the open-ended end of the corpus's spec-driven ↔ objective-driven spectrum.
