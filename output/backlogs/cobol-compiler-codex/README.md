# `cobol-compiler-codex` — Post-Session Analysis

> Meta-analysis of the Codex CLI build of **MiniCOBC**, a COBOL-to-C compiler
> written in COBOL. This file is the user-driven view (Feature Backlog + Prompt
> Ledger + Repo Stats). For the agent-centric step-wise view, see
> [`SPECIFICATION_BACKLOG.md`](./SPECIFICATION_BACKLOG.md).

## Project overview

- **Project root (evidence, read-only):** `/Users/mathieuacher/SANDBOX/cobol-compiler-codex`
- **Agent:** Codex CLI v`0.117.0-alpha.24` / `0.118.0-alpha.2`, model `gpt-5.4`
- **Sessions:** 4 JSONL rollouts, 2026-03-29T15:54 → 2026-04-03T14:39 (~5 calendar days, ~11h active)
- **Deliverable:** MiniCOBC, a subset COBOL compiler written in one COBOL source file (`src/minicobc.cob`, ~10.5k COBOL LOC) that compiles COBOL into C, then uses `gcc`; validated on Game of 15, a chess engine, COBOL DOOM, Flappy Bird (SDL2), and a local sample corpus; with an optimisation mode, a bootstrap/self-host check, and cross-compiler benchmarks vs GnuCOBOL.

## How this analysis was produced

- Primary evidence: four Codex rollouts pre-extracted as per-turn JSONL under `/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/turns/cobol-compiler-codex__Codex__*.jsonl`.
- Repo stats: `/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/metrics/cobol-compiler-codex.json`.
- Git history (13 commits): `/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/git/cobol-compiler-codex.json`.
- Existing factual report: `/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/reports/cobol-compiler-codex.md`.
- The Codex system-injected first user message (`<environment_context>` block) is **not** treated as `PL-ROOT`; the real `PL-ROOT` is the second user message.

---

## Feature Backlog (user-driven, BL-### only)

Each BL item maps to ≥1 `UI-###` (human instruction) and ≥1 `PL-###` (human prompt) entry (see Prompt Ledger below). Implementation-side mapping: see [`SPECIFICATION_BACKLOG.md`](./SPECIFICATION_BACKLOG.md) for which `SB-###` items realise each BL.

| ID | Title | Type | Source UI | Source PL | DoD | Evidence (key) |
|----|-------|------|-----------|-----------|-----|----------------|
| BL-001 | Write a COBOL compiler in COBOL; demonstrate non-trivial COBOL runs | Feature | UI-001 | PL-ROOT | Yes | [R:src/minicobc.cob], [R:scripts/demo.sh], [R:examples/] |
| BL-002 | Compile/run all programs from `agentic-cobol-game15tictactoe@4ae3129` | Feature | UI-002 | PL-002 | Yes | [R:templates/compat/game015.c], [R:scripts/test-agentic-game15.sh] |
| BL-003 | Design a benchmark from COBOL programs tested so far | Feature | UI-004 | PL-004 | Yes | [R:benchmark/cases.json], [R:benchmark/README.md] |
| BL-004 | Compare MiniCOBC performance vs GnuCOBOL | Feature | UI-005 | PL-005 | Yes | [R:scripts/compare-compilers.sh], [R:scripts/compare_compilers.py] |
| BL-005 | Make `primes/collatz/gcd` samples accepted by GnuCOBOL too | Bugfix | UI-006, UI-007 | PL-006, PL-007 | Yes | [R:examples/primes.cob], [R:examples/collatz.cob], [R:examples/gcd.cob] |
| BL-006 | MiniCOBC bootstrap — compile itself | Feature | UI-008, UI-009 | PL-008, PL-009 | Yes (via compat template MINICOB) | [R:scripts/test-selfhost.sh], [R:templates/compat/minicob.c] |
| BL-007 | Compile `agentic-chessengine-cobol-codex@faf0f16` with MiniCOBC | Feature | UI-010 | PL-010 | Yes | [R:templates/compat/chess/], [R:scripts/build-chess-engine.sh] |
| BL-008 | Benchmark chess engine perft: MiniCOBC vs GnuCOBOL | Feature | UI-013 | PL-013 | Yes | [R:scripts/compare-chess-perft.sh] |
| BL-009 | Implement compiler optimization passes | Feature | UI-014, UI-015 | PL-014, PL-015 | Yes | [R:examples/opt/], [R:scripts/compare-minicobc-optimizations.sh] |
| BL-010 | Write status report + README section summarising progress | Documentation | UI-016, UI-017 | PL-016, PL-017 | Yes | [R:reports/current-status.md], [R:README.md:9-25] |
| BL-011 | Compile the COBOL portion of `agentic-cobol-doom@18ce52b` | Feature | UI-018 | PL-018 | Yes | [R:templates/compat/doom/], [R:scripts/build-cobol-doom.sh] |
| BL-012 | Re-architect compiler pipeline for generic support | Refactor | UI-020, UI-021 | PL-020, PL-021 | Yes | [R:examples/generic/], [R:scripts/test-generic-features.sh] |
| BL-013 | Generic support: `PIC X`, groups, `REDEFINES`, `OCCURS`, indexed refs | Feature | UI-022, UI-023 | PL-022, PL-023 | Yes | [R:examples/generic/picx_*.cob], [R:examples/generic/redefines_*.cob], [R:examples/generic/occurs_*.cob] |
| BL-014 | DOOM build script + optimization compare | Feature | UI-025, UI-026 | PL-025 | Yes | [R:scripts/build-cobol-doom.sh], [R:scripts/compare-cobol-doom-opt.sh] |
| BL-015 | README lead section + attribution to Mathieu Acher and Codex | Documentation | UI-028, UI-029, UI-030 | PL-028, PL-030 | Yes | [R:README.md:3-8] |
| BL-016 | Build Flappy Bird from `agentic-cobol-pygame@b2095a1` | Feature | UI-031, UI-032 | PL-031, PL-032 | Partial (compatibility template, SDL2 link; not generic pipeline) | [R:templates/compat/pygame/flappy.c], [R:scripts/build-cobol-pygame.sh] |
| BL-017 | Move `game15.cob` / `gameN.cob` to generic front end | Feature | UI-033, UI-034 | PL-033, PL-034 | Yes | [R:scripts/test-game15-generic.sh], [R:scripts/test-gameN-generic.sh] |
| BL-018 | Target full chess engine with generic pipeline (phases 1–2) | Feature | UI-036, UI-037, UI-038, UI-039 | PL-036 | Yes | [R:tests/chess/phase1_fen_harness.c], [R:tests/chess/phase2_perft_harness.c] |
| BL-019 | Chess engine phases 3–4 (search, COBOCHESS driver) | Feature | UI-040 | PL-040 | Yes | [R:tests/chess/phase3_search_harness.c], [R:scripts/test-chess-phase4.sh] |
| BL-020 | Deeper / more-diverse chess benchmark (search suite + depth-1 cross-check) | Feature | UI-041, UI-042, UI-043 | PL-041, PL-042, PL-043 | Yes | [R:scripts/compare-chess-search-suite.sh], [R:scripts/compare-chess-depth1-suite.sh] |
| BL-021 | Investigate suspicious chess speedup → isolate + fix `MOVE WPC(F-IX-1) TO FRIEND-L` miscompile | Bugfix | UI-044, UI-045, UI-046 | PL-044, PL-045, PL-046 | Yes | [R:scripts/test-chess-phase3-direct.sh], [R:README.md:160] |
| BL-022 | Paired-game chess tournament benchmark harness | Feature | UI-048 | PL-048 | Yes | [R:scripts/compare-chess-tournament.sh] |
| BL-023 | MiniCOBC-vs-Stockfish tournament across skill levels | Feature | UI-049, UI-050 | PL-049, PL-050 | Yes | [R:scripts/compare-chess-stockfish-tournament.sh] |
| BL-024 | Real end-to-end Elo assessment via cutechess-cli (no adjudication) | Feature | UI-051, UI-052 | PL-051, PL-052 | Partial (pilot match shipped; Elo ±CI assessed but sample small) | [R:scripts/run_chess_cutechess_elo.py], [R:scripts/run-chess-cutechess-elo.sh] |
| BL-025 | GnuCOBOL cobol85 test-suite harness for MiniCOBC | Feature | UI-054 (side session 019d534d) | PL-054 | Partial (starter harness + conservative filter shipped; no large-scale pass/fail numbers) | [R:scripts/prepare-nist-cobol85.sh], [R:scripts/test-nist-cobol85.sh], [R:benchmark/nist-cobol85.md] |
| BL-026 | Functional-equivalence + build/run-time comparison for game15 generic path | Feature | UI-055 (side session 019d539e) | PL-055 | Yes (side session, 2026-04-03) | [T:019d539e:event_2..event_255], [R:scripts/test-game15-generic.sh] |

### Reproducibility Ops (non-feature, `OP-###`)

The user explicitly requested git/push steps several times — listed here for traceability.

| ID | Action | Source UI | Source PL |
|----|--------|-----------|-----------|
| OP-001 | `please create a git and commit` (first repo init) | UI-003 | PL-003 |
| OP-002 | `commit` (after benchmark + compiler comparison) | UI-019 | PL-019 |
| OP-003 | `commit everything, including … benchmark, and capabilities` | UI-024 | PL-024 |
| OP-004 | `please push on agentic-cobol-compiler-minicobc in Github` | UI-035 | PL-035 |
| OP-005 | `please commit/push` (after gameN work) | UI-037 | PL-037 |
| OP-006 | `commit/push` (first intraday, 2026-03-31) | UI-038 | PL-038 |
| OP-007 | `please commit/push first, incl. summary/report` (2026-04-02) | UI-044 | PL-044 |
| OP-008 | `please document heavily and commit/push` | UI-047 | PL-047 |
| OP-009 | `please commit` (after Stockfish tournament) | UI-050 | PL-050 |
| OP-010 | `please commit/push first (incl. PGN)` | UI-051 | PL-051 |
| OP-011 | `commit/push` (side session 019d539e) | UI-056 | PL-056 |

Net: 13 squash-style commits in the repo's git log [R:output/git/cobol-compiler-codex.json].

---

## Prompt Ledger

### `PL-ROOT` — initial human prompt

**RAW** (verbatim, ≤25-word quote):

> Write a COBOL compiler in COBOL. Demonstrate that you can run some (non-trivial) COBOL programs thanks to the written compiler.

Source: [T:019d3a4c-70cd-7850-9833-b9baef393d93:event_2] (2026-03-29T15:54:26Z), i=2 in per-turn JSONL.

Linked: UI-001; covers BL-001.

**CANONICAL replay prompt** (clean, minimal, complete):

```
Task: build a COBOL compiler that is itself written in COBOL.

Constraints
- The compiler source must be a COBOL program. You may use GnuCOBOL
  (`cobc`) only to bootstrap — i.e. compile the COBOL source of the
  compiler — not as a code generator that the compiler delegates to.
- The compiler may produce C as its intermediate representation, then
  use a system C compiler (e.g. `gcc`) to emit native binaries.

Deliverables
1. A COBOL source file implementing the compiler (subset is OK; document
   the supported subset clearly in a README).
2. At least three small but non-trivial COBOL programs that your
   compiler can translate and execute end-to-end. Suggested examples:
   a primes sieve, a Collatz sequence, a GCD program.
3. A demo script that builds the compiler, compiles the example
   programs, runs them, and diffs their stdout against pinned
   expected-output files.

Acceptance criteria
- Running the demo script must print non-trivial program outputs
  (not just "Hello world").
- The README must state the supported COBOL subset and deliberate
  constraints.

Scope
- A full COBOL-85 front end is out of scope; a carefully documented
  subset is preferred over an incomplete "full" implementation.
```

### Subsequent user prompts (summary — `PL-001` … `PL-056`)

Full entries live in [`appendix.json`](./appendix.json) under `prompt_ledger`. Key prompts (paraphrased, ≤25-word quotes):

| PL | UI | Timestamp | Quote / paraphrase | BL |
|----|----|-----------|--------------------|----|
| PL-002 | UI-002 | 2026-03-29T16:15 | "could you compile/run all COBOL programs available here … agentic-cobol-game15tictactoe … commit 4ae3129… with the new compiler" | BL-002 |
| PL-003 | UI-003 | 2026-03-29T16:41 | "please create a git and commit" | OP-001 |
| PL-004 | UI-004 | 2026-03-29T16:42 | "please design a benchmark based on COBOL programs you have tested so far" | BL-003 |
| PL-005 | UI-005 | 2026-03-29T16:46 | "compare performance of the compiler compared to traditional compiler like the GNUCobol one" | BL-004 |
| PL-006 | UI-006 | 2026-03-29T16:54 | "I don't get why primes, collatz, gcd are not accepted by GnuCOBOL" | BL-005 |
| PL-007 | UI-007 | 2026-03-29T16:57 | "yes please… minicobc should support valid COBOL programs" | BL-005 |
| PL-008 | UI-008 | 2026-03-29T17:11 | "is minicobc able to compile/build minicobc? and thus bootstrap?" | BL-006 |
| PL-009 | UI-009 | 2026-03-29T17:12 | "please extend minicobc until it can compile the current src/minicobc.cob" | BL-006 |
| PL-010 | UI-010 | 2026-03-29T18:11 | "compile COBOL chess engine … agentic-chessengine-cobol-codex … using minicobc" | BL-007 |
| PL-013 | UI-013 | 2026-03-30T03:23 | "is it possible to benchmark performance of the chess engine when compiled with minicobc vs GNUCobol?" | BL-008 |
| PL-014 | UI-014 | 2026-03-30T03:29 | "could you envision to implement some compiler optimizations?" | BL-009 |
| PL-015 | UI-015 | 2026-03-30T04:13 | "please implement next optimization passes" | BL-009 |
| PL-016 | UI-016 | 2026-03-30T04:40 | "please write a report of current status, including … chess engine … perf … optimizations and bootstrap" | BL-010 |
| PL-017 | UI-017 | 2026-03-30T04:43 | "please write such a summary in a README section" | BL-010 |
| PL-018 | UI-018 | 2026-03-30T04:46 | "consider agentic-cobol-doom … try to build it … the major challenge might be to handle CALL" | BL-011 |
| PL-020 | UI-020 | 2026-03-30T04:58 | "why alphanumeric storage, REDEFINES, OCCURS, indexed tables, paragraph PERFORM, EVALUATE can't be supported?" | BL-012 |
| PL-021 | UI-021 | 2026-03-30T05:00 | "let's go to a generic support, including a re-architecture of the compiler pipeline" | BL-012 |
| PL-022 | UI-022 | 2026-03-30T07:02 | "let's address PIC X, groups, REDEFINES, OCCURS, and indexed references" | BL-013 |
| PL-023 | UI-023 | 2026-03-30T08:52 | "let's go to REDEFINES" | BL-013 |
| PL-025 | UI-025 | 2026-03-30T10:54 | "can you make a script to build it with the minicobc compiler? and then run it?" (DOOM) | BL-014 |
| PL-028 | UI-028 | 2026-03-30T11:29 | "write in the README a dedicated subsection … chess engine, gameof15, DOOM …" | BL-015 |
| PL-030 | UI-030 | 2026-03-30T11:39 | "mention it has been created by Mathieu Acher and Codex (GPT-5.4, Extra High)" | BL-015 |
| PL-031 | UI-031 | 2026-03-30T11:42 | "try to build flappy game … agentic-cobol-pygame … with the compiler" | BL-016 |
| PL-032 | UI-032 | 2026-03-30T12:06 | "it's a bit counter intuitive that DOOM is fully compiled, not the rest" | BL-016 |
| PL-034 | UI-034 | 2026-03-30T16:00 | "can you now target gameN?" | BL-017 |
| PL-036 | UI-036 | 2026-03-30T18:31 | "please target chess engine" (generic path) | BL-018 |
| PL-040 | UI-040 | 2026-04-02T07:21 | "let's address the top-level COBOCHESS or any blocker" | BL-019 |
| PL-041 | UI-041 | 2026-04-02T12:39 | "in another context I use this test suite … agentic-chessengine-brainfuck/blob/master/test_perft.py" | BL-020 |
| PL-042 | UI-042 | 2026-04-02T17:27 | "other performance benchmark … functionally equal to GNU Cobol variant, refine runtime factor" | BL-020 |
| PL-043 | UI-043 | 2026-04-02T17:52 | "diversify the chess positions and depth increase to further test" | BL-020 |
| PL-044 | UI-044 | 2026-04-02T08:52 | "it's very strange to beat the runtime of GnuCOBOL… do you check functional correctness?" | BL-021 |
| PL-045 | UI-045 | 2026-04-02T17:02 | "next debugging target should be direct QUIESCE / recursive ALPHABETA equivalence on the phase-3 FEN" | BL-021 |
| PL-046 | UI-046 | 2026-04-02T12:54 | "yes please investigate, since the compiler may produce a wrong binary" | BL-021 |
| PL-048 | UI-048 | 2026-04-02T18:01 | "organize a tournament between chess engine built with GNU Cobol vs Minicobc" | BL-022 |
| PL-049 | UI-049 | 2026-04-03T05:10 | "organize a tournament against Stockfish at different skills, only with the compiled binary made by minicobc" | BL-023 |
| PL-050 | UI-050 | 2026-04-03T05:28 | "focus on skills 0 first" (CCRL-scaled time control) | BL-023 |
| PL-051 | UI-051 | 2026-04-03T11:21 | "I'd like real, end-to-end games to assess the Elo rating … when compiled with minicobc" | BL-024 |
| PL-052 | UI-052 | 2026-04-03T11:58 | "no adjudication at all please… write a script and tell me how to run it" | BL-024 |
| PL-054 | UI-054 | 2026-04-03T12:25 | "use this test suite [GnuCOBOL gitside-gnucobol-3.x/tests/cobol85] to test minicobc?" | BL-025 |
| PL-055 | UI-055 | 2026-04-03T13:54 | "minicobc seems working on game15tictactoe … design an experiment to show functional correctness / equivalence vs GNU Cobol" | BL-026 |

The full 56-entry PL ledger (and all 56 canonical UI entries) is in `appendix.json`. The missing numbers (UI-011, UI-012, UI-026, UI-027, UI-033, UI-037, UI-053) correspond to meta/filler prompts such as `go ahead`, `continue`, `yes please`, `status?`, `retry` — captured as `Meta/process` in the UII but not elevated to PL-level features.

### Project Constraints Index (PCI)

| ID | Constraint | Type | Source |
|----|------------|------|--------|
| PC-001 | Sandbox mode `workspace-write` — reads allowed, writes inside cwd only, network restricted, escalation required for most other actions | tooling | [T:019d3a4c:event_0] developer-role permissions block |
| PC-002 | No `AGENTS.md` or `.codex/config.toml` at project root | repo policy | [R:/Users/mathieuacher/SANDBOX/cobol-compiler-codex/] (directory listing) |
| PC-003 | External COBOL repos pinned at specific commits: `agentic-cobol-game15tictactoe@4ae3129`, `agentic-chessengine-cobol-codex@faf0f16`, `agentic-cobol-doom@18ce52b`, `agentic-cobol-pygame@b2095a1`, `agentic-chessengine-brainfuck` (for test suite) | build | [R:external/], [R:README.md:3] |
| PC-004 | GnuCOBOL (`cobc`) must be available and used as (a) bootstrap compiler for `src/minicobc.cob` and (b) oracle for benchmark comparison | build | [R:scripts/demo.sh], [R:scripts/test.sh] |
| PC-005 | Free-form COBOL is the accepted input form (not fixed-column) | style | [R:README.md:89] |

---

## Reproduction

### Preconditions (observed)

- **OS:** macOS (Darwin 24.6.0); the session's `cwd` was `/Users/mathieuacher/SANDBOX/cobol-compiler-codex`.
- **GnuCOBOL (`cobc`):** required; specific version not pinned in the repo.
- **gcc:** required for the C back end.
- **Optional:** `python-chess`, `cutechess-cli`, `stockfish` for the chess-related benchmark harnesses.
- **External repos:** must be checked out under `external/` at the commits listed in PC-003.

### Canonical entry points

```bash
# Build + demo (core subset)
./scripts/demo.sh

# Run the test harness (minicobc -> C -> gcc, compared against cobc -x -free)
./scripts/test.sh

# Full benchmark (core + opt + compatibility suites)
./scripts/benchmark.sh

# Bootstrap / self-host check
./scripts/test-selfhost.sh

# External targets
./scripts/build-chess-engine.sh
bash ./scripts/build-cobol-doom.sh
bash ./scripts/build-cobol-pygame.sh

# Chess benchmark stack
./scripts/compare-chess-perft.sh
./scripts/compare-chess-search-suite.sh
./scripts/compare-chess-search-suite.sh --profile extended --iterations 3
./scripts/compare-chess-tournament.sh --profile default --depth 2 --max-plies 12
./scripts/compare-chess-stockfish-tournament.sh --profile extended --search-mode movetime \
    --movetime-ms 50 --max-plies 16 --skills 0,5,10,15,20
bash ./scripts/run-chess-cutechess-elo.sh   # requires cutechess-cli + stockfish
```

### Checkpoints (via git)

Each of the 13 commits in the repo is a stable milestone — see the Git churn
table below and the mapping in [`SPECIFICATION_BACKLOG.md`](./SPECIFICATION_BACKLOG.md).

---

## Repo Quantification (stats)

Source: `/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/metrics/cobol-compiler-codex.json` [S:stats_run_1]; excludes `.git/`, `build/`, `external/vendor/…` per the default rules.

| Metric | Value |
|--------|------:|
| Total files | 252 |
| Total bytes | 3,165,962 |
| C | 25 files / 63,074 LOC |
| COBOL | 68 files / 13,167 LOC (+ 1 copybook / 6 LOC) |
| Python | 13 files / 5,940 LOC |
| C/Header | 31 files / 3,467 LOC |
| Shell | 39 files / 1,589 LOC |
| Markdown | 5 files / 1,405 LOC |
| JSON | 2 files / 1,945 LOC |

### Kind classification (inferred)

| Kind | Counts / notes |
|------|----------------|
| Production (compiler source) | `src/minicobc.cob` (10,535 code LOC) + generated C templates under `templates/compat/` |
| Tests / validation | `tests/chess/*.cob` + `*.c` harnesses; `scripts/test-*.sh` (~15 harness scripts); `benchmark/cases.json` |
| Build / tooling | 39 shell scripts + 13 Python comparison drivers under `scripts/` |
| Docs | `README.md`, `reports/current-status.md`, `benchmark/README.md`, `benchmark/nist-cobol85.md`, `benchmark/optimization-suite.md` |
| Config | `benchmark/cases.json`, `benchmark/nist-cobol85-cases.json` |
| Data / examples | `examples/*.cob` (3 core) + `examples/opt/*.cob` (8) + `examples/generic/*.cob` (~45) + `expected/` outputs |

### Key entry points

- **Compiler source:** `src/minicobc.cob` (single-file, 10,535 COBOL code lines; largest file in the repo).
- **Demo / smoke test:** `scripts/demo.sh`, `scripts/test.sh`.
- **Benchmark driver:** `scripts/benchmark.sh` + `scripts/benchmark.py`.
- **Self-host check:** `scripts/test-selfhost.sh` + `templates/compat/minicob.c`.
- **External targets:** `scripts/build-chess-engine.sh`, `scripts/build-cobol-doom.sh`, `scripts/build-cobol-pygame.sh`.

### Git churn

| Metric | Value |
|--------|------:|
| Commits | 13 |
| First commit | 2026-03-29T18:42:09+02:00 (`7758f781 Initial commit`) |
| Last commit | 2026-04-03T16:39:01+02:00 (`1b72b9c9 Fix else-if chain closure handling`) |
| Total files changed | 302 |
| Total insertions | 162,592 |
| Total deletions | 74,567 |

---

## Summary metrics (PASS 2 — see `REPORT.md`)

- **Difficulty label:** `Very-High` (index 0.814, mean rank 9.1 over 7 signals) [R:output/difficulty.json:cobol-compiler-codex].
- **User prompts:** 97 (most in project 019d3a4c; min prompt length short — median paraphrase "go ahead" / "continue").
- **Tool calls:** 5,370 (66.1% `exec_command`, 14.2% `apply_patch`).
- **Tool-output error rate:** 20.0% (1,072 / 5,370) — dominated by "test suite reported FAIL" (607) and non-zero exit status (426).
- **Active hours:** ~10h 58m across 15,631 turn-events.
- **SE-task share (active time):** understanding 65.8%, feature 16.5%, build 12.4%, bug_fix 3.9%, test 1.1%, plan 0.2%.
- **Estimated API cost:** ~$108.10 at rack rates (Codex `gpt-5.4`).

---

## Limitations / missing evidence

- Full per-prompt verbatim text exceeds the 25-word quote policy; the ledger
  above uses paraphrase + pointer. Raw full-text lives in the per-turn JSONL at
  `output/turns/cobol-compiler-codex__Codex__019d3a4c-…jsonl:i=<i>`.
- Commits are squash-authored by "Mathieu Acher" — fine-grained authorship
  (agent-initiated vs user-directed inside one squash) is reconstructed from
  session logs, not from git blame.
- `MINICOBC_OPT=1` is flagged unsafe for the chess engine in the README but no
  dedicated bug-ticket / SB-bugfix exists beyond the documentation caveat.
- `cutechess-cli` + `stockfish` are external binary dependencies not pinned in
  the repo; BL-023/BL-024 reproducibility depends on user-side availability.
- No `AGENTS.md`, `.codex/config.toml`, `CONTRIBUTING.md`, or CI config was
  present at the project root — all "project constraints" are inferred from
  the sandbox header in the Codex rollout + the README.

## Related artefacts

- [`SPECIFICATION_BACKLOG.md`](./SPECIFICATION_BACKLOG.md) — agent-centric step-wise backlog (100+ SB items).
- [`appendix.json`](./appendix.json) — machine-readable full ledger + rubric + episodes + interaction metrics.
- [`REPORT.md`](./REPORT.md) — Phase 0 + PASS 1 + PASS 2 synthesis.
