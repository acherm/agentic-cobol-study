# MiniCOBC — Agent-Centric Specification Backlog

> Step-wise ledger of what the Codex agent actually implemented across the session
> timeline for `cobol-compiler-codex`. This is the **agent-centric** view
> (implementation increments with provenance). For the **user-driven** view,
> see [`README.md`](./README.md) Feature Backlog (`BL-###`).

## Purpose

This backlog captures how the MiniCOBC compiler, its test/bench tooling, and
its external-program integrations evolved incrementally. Each `SB-###` entry
describes one stable, externally observable capability or quality change and is
tagged with a **step label** drawn from the 13 git commits recorded for this
repo [R:output/git/cobol-compiler-codex.json], mapped to the session timeline
in `/Users/mathieuacher/.codex/sessions/2026/{03,04}/…`.

## Step segmentation method

Priority:

1. **Git commits** (authoritative) — 13 commits from `7758f78` (2026-03-29) to `1b72b9c` (2026-04-03) [G:commit 1b72b9c9] [G:commit 7758f781].
2. **Session episodes** (`EP-<n>`) — contiguous agent turns between two human user prompts when the commit is too coarse.
3. INFERRED steps when neither applies.

Limitation: no per-file blame is available in the captured git metadata; commit subjects are the main signal, and the 13 commits were all authored by "Mathieu Acher" (squash convention — the Codex agent authored content in-session, but the human committed).

## Provenance labels

- **User-driven** — explicit human request (UI/PL/BL mapped).
- **Agent-initiated** — agent-added improvement/hardening (no direct human ask).
- **Required prerequisite** — necessary enabler for a user-requested item.

---

## Phase A — Bootstrap compiler & core subset
*Step `G1 = 7758f781 "Initial commit"` (2026-03-29T18:42:09) and preceding session episodes 2026-03-29T15:54 → 18:42.* [G:commit 7758f781]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-001 | COBOL-in-COBOL compiler skeleton `src/minicobc.cob` | Capability | User-driven | BL-001, UI-001, PL-ROOT | A single `PROGRAM-ID. MINICOBC.` COBOL source that reads a `.cob` file and emits a C translation unit, built via `cobc` to a native executable. | [R:src/minicobc.cob:1], [T:019d3a4c:event_2..event_210] |
| SB-002 | Subset lexer/parser for `IDENTIFICATION`, `DATA`, `WORKING-STORAGE`, `PROCEDURE` divisions | Capability | Required prerequisite | BL-001 | Recognises the four divisions, elementary `01`/`05`/`77` items with `PIC 9(...)`, `PIC Z…`, `PIC X(...)`, optional `VALUE`. | [R:README.md:40-68] |
| SB-003 | Core statements: `DISPLAY`, `ACCEPT`, `MOVE`, `INITIALIZE`, `ADD`/`SUBTRACT`/`MULTIPLY`/`DIVIDE`, `COMPUTE`, `IF`/`ELSE IF`/`ELSE`/`END-IF`, `STOP RUN` | Capability | Required prerequisite | BL-001 | Emits semantically-equivalent C for these statements against a small runtime harness. | [R:README.md:46-67] |
| SB-004 | Three local sample programs `primes.cob`, `collatz.cob`, `gcd.cob` | Test/Validation | User-driven | BL-001, UI-001 | Ship-ready COBOL programs used to demonstrate "non-trivial" compilation; expected outputs pinned under `expected/`. | [R:examples/primes.cob], [R:expected/collatz.txt] |
| SB-005 | Build+demo+test scripts (`scripts/demo.sh`, `scripts/test.sh`) | Tooling | Required prerequisite | BL-001 | Builds minicobc with `cobc`, compiles samples to C, links with `gcc`, and diffs against `expected/*.txt`. | [R:scripts/demo.sh], [R:scripts/test.sh] |

---

## Phase B — External validation (Game of 15) & benchmark harness
*Step `G2 = 8d41ff3b "Extend MiniCOBC validation and benchmarking"` (2026-03-29T20:11:35).* [G:commit 8d41ff3b]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-010 | Compatibility path for `agentic-cobol-game15tictactoe@4ae3129` | Capability | User-driven | BL-002, UI-002, PL-002 | Compiler detects `PROGRAM-ID` values `GAME015`, `GAME015TREE`, `GAME15`, `GAME15TREE`, `GAMEN` and emits pinned C templates in `templates/compat/`. | [R:templates/compat/game015.c], [T:019d3a4c:i=213] |
| SB-011 | External submodule pinning of `acherm/agentic-cobol-game15tictactoe` | Tooling | Required prerequisite | BL-002 | External repo checked out under `external/agentic-cobol-game15tictactoe` at commit `4ae3129…`. | [R:external/agentic-cobol-game15tictactoe] |
| SB-012 | Benchmark manifest `benchmark/cases.json` with core + compatibility suites | Test/Validation | User-driven | BL-003, UI-004 | Declarative suite definitions with oracles (stdout match against `expected/` or GnuCOBOL). | [R:benchmark/cases.json], [R:benchmark/README.md] |
| SB-013 | GnuCOBOL performance comparison runner (`compare-compilers.sh`, `compare_compilers.py`) | Test/Validation | User-driven | BL-004, UI-005, PL-005 | Records per-case compile time and runtime for `minicobc+gcc` vs `cobc`, writes JSON+Markdown reports. | [R:scripts/compare-compilers.sh], [R:scripts/compare_compilers.py] |
| SB-014 | GnuCOBOL acceptance fix-up for `primes/collatz/gcd` | Quality/Hardening | User-driven | BL-005, UI-006, PL-006 | The three samples were rewritten to be valid free-form COBOL accepted by both `minicobc` and `cobc`. | [T:019d3a4c:i=459], [R:examples/primes.cob] |
| SB-015 | Bootstrap check `scripts/test-selfhost.sh` with `MINICOB` template | Capability | User-driven | BL-006, UI-008, PL-008 | Stage-0 `cobc`→`minicobc`; stage-1 `minicobc`→compiler C; stage-2 diff confirms self-host reproduction. | [R:scripts/test-selfhost.sh], [R:templates/compat/minicob.c], [T:019d3a4c:i=864..1048] |

---

## Phase C — Optimization mode & chess-engine compatibility
*Step `G3 = 1b6242ba "Add optimization, bootstrap, and chess status tooling"` (2026-03-30T06:44:40).* [G:commit 1b6242ba]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-020 | Chess engine compatibility path for `agentic-chessengine-cobol-codex@faf0f16` (template-based) | Capability | User-driven | BL-007, UI-010, PL-010 | Compiler detects chess `PROGRAM-ID` values and emits dedicated C templates for `BOARD`, `FEN`, `ATTACK`, `MOVEGEN`, `MAKEMOVE`, `UNMAKEMOVE`, `PERFT`, `EVAL`, `SEARCH`, `TIMEUTIL`, `UCI`. | [R:templates/compat/chess/], [T:019d3a4c:i=1216] |
| SB-021 | Perft benchmark harness `compare-chess-perft.sh` | Test/Validation | User-driven | BL-008, UI-013, PL-013 | Runs perft at configurable depth with GnuCOBOL as oracle; writes `build/perf/chess-perft-compare.json` + `.md`. | [R:scripts/compare-chess-perft.sh], [T:019d3a4c:i=1467..1531] |
| SB-022 | OPT mode 1 — constant folding, constant propagation, dead-store elimination | Capability | User-driven | BL-009, UI-014, PL-014 | `./build/bin/minicobc OPT in.cob out.c` enables three initial passes that preserve semantics on the opt corpus. | [R:src/minicobc.cob], [R:examples/opt/] |
| SB-023 | Optimization suite `examples/opt/*.cob` (8 programs) | Test/Validation | Agent-initiated | BL-009 | Eight small programs expose constfold, constprop, deadstore, strength, boolchain, loopcanon, smallwidth, lcg opportunities. | [R:examples/opt/], [R:benchmark/optimization-suite.md] |
| SB-024 | OPT mode 2 — loop-condition canonicalization, width-aware integer selection | Capability | User-driven | BL-009, UI-015, PL-015 | Adds `loopcanon` and `smallwidth` passes; opt-vs-baseline comparison script `compare-minicobc-optimizations.sh`. | [R:scripts/compare-minicobc-optimizations.sh], [T:019d3a4c:i=2035] |
| SB-025 | Status report `reports/current-status.md` and README summary | Documentation | User-driven | BL-010, UI-016, UI-017, PL-016 | Centralised snapshot of supported subset, benchmark numbers, optimizations, bootstrap status. | [R:reports/current-status.md], [T:019d3a4c:i=2339..2384] |

---

## Phase D — Generic pipeline re-architecture; DOOM + gameN
*Step `G4 = a0128611 "Expand generic front end and DOOM support"` (2026-03-30T13:26:45).* [G:commit a0128611]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-030 | DOOM compatibility path for `agentic-cobol-doom@18ce52b` | Capability | User-driven | BL-011, UI-018, PL-018 | Builds `doom.cob` COBOL portion through a template and links with plain `gcc`. | [R:templates/compat/doom/], [R:scripts/build-cobol-doom.sh] |
| SB-031 | Re-architected generic pipeline: `EVALUATE`, `PERFORM VARYING`, paragraph `PERFORM` | Capability | User-driven | BL-012, UI-020, PL-020, PL-021 | Generic front end now handles `EVALUATE`/`WHEN`/`WHEN OTHER`/`END-EVALUATE`, `PERFORM VARYING ... FROM ... BY ... UNTIL`, paragraph labels + `PERFORM paragraph`. | [R:examples/generic/evaluate_*.cob], [R:examples/generic/perform_varying.cob] |
| SB-032 | Generic front end: `PIC X`, groups, `REDEFINES`, `OCCURS`, indexed references | Capability | User-driven | BL-013, UI-022, PL-022 | Handles elementary `PIC X(...)`, group items with child tracking, elementary/group `REDEFINES` with packed-width alignment, elementary + 1-D group `OCCURS`, simple indexed refs `ITEMS(IDX)`. | [R:examples/generic/picx_*.cob], [R:examples/generic/redefines_*.cob], [R:examples/generic/occurs_*.cob], [R:examples/generic/group_*.cob] |
| SB-033 | External `CALL "name"` with `USING BY VALUE`/`BY REFERENCE`/`RETURNING` | Capability | Required prerequisite | BL-011 | Supports indexed numeric `BY VALUE` args and `PIC X` `BY REFERENCE` buffers, needed for DOOM's `CALL` to C helpers. | [R:examples/generic/call_*.cob] |
| SB-034 | `FUNCTION SQRT`, `FUNCTION NUMVAL`, `FUNCTION TRIM`, `FUNCTION MOD`, `FUNCTION REM` | Capability | Required prerequisite | BL-011, BL-013 | Intrinsic-function dispatch table with numeric/alpha argument handling. | [R:examples/generic/function_sqrt.cob], [R:examples/generic/move_function_trim.cob] |
| SB-035 | Multiline free-form procedure statements | Capability | Required prerequisite | BL-013 | Continued `DISPLAY`, `UNSTRING`, `CALL`, `COMPUTE`, and `IF` parse across physical lines until a terminating period/clause. | [R:examples/generic/multiline_*.cob] |
| SB-036 | Generic front-end smoke script `scripts/test-generic-features.sh` | Test/Validation | Agent-initiated | BL-012, BL-013 | Covers all generic regressions in one run. | [R:scripts/test-generic-features.sh] |
| SB-037 | DOOM OPT comparison `compare-cobol-doom-opt.sh` | Test/Validation | User-driven | BL-014, UI-025, PL-025 | Measures baseline vs `MINICOBC_OPT=1` DOOM build time and binary size. | [R:scripts/compare-cobol-doom-opt.sh] |

---

## Phase E — `gameN` through generic front end + README attribution
*Steps `G5 = 226a2545` and `G6 = b9b2c6ef` (README updates, 2026-03-30T13:35 → 13:41) and `G7 = bdff7bb4 "Target gameN with the generic front end"` (2026-03-30T18:43:32).* [G:commit 226a2545] [G:commit b9b2c6ef] [G:commit bdff7bb4]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-040 | README lead paragraph listing chess, Game of 15, DOOM, Flappy targets | Documentation | User-driven | BL-015, UI-028, UI-029, PL-028 | Introductory section explicitly names the four external codebases with commit hashes and categorises each as generic vs compatibility. | [R:README.md:3-8] |
| SB-041 | Author/attribution line "Mathieu Acher and Codex (GPT-5.4, Extra High)" | Documentation | User-driven | BL-015, UI-030, PL-030 | README includes creator attribution and switches full commit hashes to short-link form. | [R:README.md:7] |
| SB-042 | Flappy Bird compatibility path for `agentic-cobol-pygame@b2095a1` | Capability | User-driven | BL-016, UI-031, PL-031 | `examples/flappy.cob` compiles through a pinned compatibility C template and links with the repo's SDL2 helper `src/cpg.c`; smoke test via `SDL_VIDEODRIVER=dummy`. | [R:templates/compat/pygame/], [R:scripts/build-cobol-pygame.sh] |
| SB-043 | `gameN.cob` graduated to generic front end | Capability | User-driven | BL-017, UI-034, PL-034 | `gameN.cob` no longer uses a template; its compilation exercises the real generic pipeline and matches GnuCOBOL. | [R:scripts/test-gameN-generic.sh] |
| SB-044 | `game15.cob` graduated to generic front end | Capability | User-driven | BL-017, UI-033 | Same as SB-043 for `game15.cob`, plus `scripts/test-game15-generic.sh`. | [R:scripts/test-game15-generic.sh] |

---

## Phase F — Generic chess engine build (phases 1–2) + commit/push workflow
*Step `G8 = 3147785e "Advance generic chess support and validation"` (2026-03-31T07:28:24).* [G:commit 3147785e]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-050 | Chess Phase-1 harness (`BOARD`, `FEN(startpos)`) | Capability | User-driven | BL-018, UI-036, PL-036 | Builds `BOARD`+`FEN` through generic front end, links with C harness in `tests/chess/phase1_fen_harness.c`, cross-checks `FEN(startpos)` against GnuCOBOL reference. | [R:tests/chess/phase1_fen_harness.c], [R:scripts/test-chess-phase1.sh] |
| SB-051 | Chess Phase-2 harness (`PERFT(startpos, depth=2)`) | Capability | User-driven | BL-018, PL-036 | Adds `ATTACK`, `MOVEGEN`, `MAKEMOVE`, `UNMAKEMOVE`, `PERFT` to generic pipeline; matches GnuCOBOL perft count. | [R:tests/chess/phase2_perft_harness.c], [R:scripts/test-chess-phase2.sh] |
| SB-052 | Generic-pipeline support for `PERFORM paragraph UNTIL`, `SEARCH`, qualified `OF` | Capability | Required prerequisite | BL-018 | Additional COBOL constructs needed to compile the chess engine through the generic path. | [R:examples/generic/perform_paragraph_until.cob], [R:examples/generic/qualified_of.cob] |

---

## Phase G — Chess Phase 3 & 4, generic COBOCHESS, benchmark suite expansion
*Step `G9 = a8aeb459 "Advance generic chess engine support"` (2026-04-02T10:56:55).* [G:commit a8aeb459]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-060 | Chess Phase-3 harness (shallow `SEARCH`) | Capability | User-driven | BL-019, UI-040, PL-040 | Adds `EVAL`, `SEARCH`, `TIMEUTIL`, `MOVE2UCI` to generic pipeline; shallow search matches GnuCOBOL. | [R:tests/chess/phase3_search_harness.c], [R:scripts/test-chess-phase3.sh] |
| SB-061 | Chess Phase-4 harness (top-level `COBOCHESS` driver) | Capability | User-driven | BL-019, PL-040 | Full top-level engine driver builds through generic pipeline; `--perft-startpos 2` matches GnuCOBOL. | [R:scripts/test-chess-phase4.sh] |
| SB-062 | Fixed-depth search benchmark `compare-chess-search-suite.sh` with default + extended profiles | Test/Validation | User-driven | BL-020, UI-042, PL-042 | Normalized `info …` / `bestmove` comparison across 4 (default) and 7 (extended) diverse FEN positions. | [R:scripts/compare-chess-search-suite.sh] |
| SB-063 | Depth-1 cross-check suite against `python-chess` | Test/Validation | User-driven | BL-020, UI-041, PL-041 | 11-position shallow depth-1 sanity check adapted from `agentic-chessengine-brainfuck/test_perft.py`. | [R:scripts/compare-chess-depth1-suite.sh] |
| SB-064 | Cautionary benchmark caveat section in README | Documentation | User-driven | BL-020, UI-043, PL-043 | README explicitly flags `MiniCOBC`-vs-GnuCOBOL runtime ratios as "strong local signal, not a settled general claim". | [R:README.md:23] |

---

## Phase H — Phase-3 search equivalence bug fix; tournament harness
*Step `G10 = ab7f7d05 "Fix chess search equivalence and document validation"` (2026-04-02T19:24:03).* [G:commit ab7f7d05]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-070 | Direct `QUIESCE`/`ALPHABETA` equivalence harness `test-chess-phase3-direct.sh` | Test/Validation | User-driven | BL-021, UI-045, PL-045 | Bypasses top-level `SEARCH` wrapper and directly cross-checks `QUIESCE`, recursive `ALPHABETA`, and first capture replies. | [R:scripts/test-chess-phase3-direct.sh], [R:tests/chess/phase3_direct_harness.c] |
| SB-071 | Bug-fix: indexed numeric `MOVE` source lowering in `EVAL` | Bugfix | User-driven | BL-021, UI-046, PL-046 | `MOVE WPC(F-IX - 1) TO FRIEND-L` had been miscompiled as the scalar expression `FRIEND-L = F-IX - 1` instead of loading the indexed array element. | [R:README.md:160] |
| SB-072 | `examples/generic/move_index_expr.cob` regression | Test/Validation | Agent-initiated | BL-021 | Regression input that reproduces the miscompile. | [R:examples/generic/move_index_expr.cob] |

---

## Phase I — Tournament benchmarking
*Step `G11 = 1b0ca6f9 "Add chess tournament benchmarking"` (2026-04-03T07:27:41).* [G:commit 1b0ca6f9]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-080 | Paired-game tournament harness `compare-chess-tournament.sh` | Test/Validation | User-driven | BL-022, UI-048, PL-048 | Diversified starts with color swaps, fixed-depth search; writes JSON+MD+PGN; no illegal moves in recorded runs. | [R:scripts/compare-chess-tournament.sh] |
| SB-081 | MiniCOBC-vs-Stockfish tournament across `Skill Level` settings | Test/Validation | User-driven | BL-023, UI-049, PL-049 | `compare-chess-stockfish-tournament.sh` runs the `minicobc`-built engine against Stockfish at skills 0/5/10/15/20. | [R:scripts/compare-chess-stockfish-tournament.sh] |

---

## Phase J — cutechess Elo harness
*Step `G12 = a05a8a47 "Add cutechess Elo match tooling"` (2026-04-03T13:57:54).* [G:commit a05a8a47]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-090 | `scripts/run_chess_cutechess_elo.py` | Test/Validation | User-driven | BL-024, UI-052, PL-052 | End-to-end paired match via real `cutechess-cli`, plays games, exports PGN, reports Elo assessment; no adjudication. | [R:scripts/run_chess_cutechess_elo.py], [R:scripts/run-chess-cutechess-elo.sh] |
| SB-091 | Unbuffered UCI wrapper `run-minicobc-chess-uci.sh` | Tooling | Required prerequisite | BL-024 | `cutechess-cli` needs a line-buffered UCI binary; this wrapper `stdbuf`-wraps the minicobc-compiled engine. | [R:scripts/run-minicobc-chess-uci.sh] |
| SB-092 | NIST COBOL85 starter harness `prepare-nist-cobol85.sh` + `test-nist-cobol85.sh` | Test/Validation | User-driven | BL-025, UI-054 (PL-054 side-session) | Conservative filter + runner to exercise `minicobc` against a local GnuCOBOL `cobol85` extraction. | [R:scripts/prepare-nist-cobol85.sh], [R:scripts/test-nist-cobol85.sh], [R:benchmark/nist-cobol85.md] |
| SB-093 | game15 generic-path MiniCOBC-vs-GnuCOBOL experiment (side session 019d539e) | Test/Validation | User-driven | BL-026, UI-055 (PL-055 side-session) | Functional-equivalence + build/run-time comparison on the generic `game15` path. | [T:019d539e:event_2..event_255] |

---

## Phase K — Final bug fix
*Step `G13 = 1b72b9c9 "Fix else-if chain closure handling"` (2026-04-03T16:39:01).* [G:commit 1b72b9c9]

| ID | Title | Category | Provenance | BL/UI/PL | Specification statement | Evidence |
|----|-------|----------|------------|----------|-------------------------|----------|
| SB-100 | `ELSE IF` chain closure bug fix | Bugfix | Agent-initiated | (no matching UI — INFERRED from commit) | Compiler no longer drops intermediate `END-IF`s on long `ELSE IF` chains; adds `examples/generic/else_if_repeated_end_if.cob` + `else_if_chain.cob`. | [G:commit 1b72b9c9], [R:examples/generic/else_if_chain.cob] |

---

## Mapping summary (SB ↔ BL)

| BL | Associated SB items |
|----|---------------------|
| BL-001 | SB-001, SB-002, SB-003, SB-004, SB-005 |
| BL-002 | SB-010, SB-011 |
| BL-003 | SB-012 |
| BL-004 | SB-013 |
| BL-005 | SB-014 |
| BL-006 | SB-015 |
| BL-007 | SB-020 |
| BL-008 | SB-021 |
| BL-009 | SB-022, SB-023, SB-024 |
| BL-010 | SB-025 |
| BL-011 | SB-030, SB-033, SB-034 |
| BL-012 | SB-031, SB-036 |
| BL-013 | SB-032, SB-034, SB-035, SB-036 |
| BL-014 | SB-037 |
| BL-015 | SB-040, SB-041 |
| BL-016 | SB-042 |
| BL-017 | SB-043, SB-044 |
| BL-018 | SB-050, SB-051, SB-052 |
| BL-019 | SB-060, SB-061 |
| BL-020 | SB-062, SB-063, SB-064 |
| BL-021 | SB-070, SB-071, SB-072 |
| BL-022 | SB-080 |
| BL-023 | SB-081 |
| BL-024 | SB-090, SB-091 |
| BL-025 | SB-092 |
| BL-026 | SB-093 |
| (no BL) | SB-100 (agent-initiated bug fix) |

## Limitations

- 13 squash-style commits compress many session turns; the segmentation above
  stitches commits to session episodes using timestamps, which is reliable at
  the phase level but loses intra-commit ordering.
- `MINICOBC_OPT=1` is documented as unsafe for the chess engine (miscompile on
  `perft` counts) [R:README.md:23]; SB-022/SB-024 remain "implemented" but with
  this known limitation tracked in README rather than a dedicated bugfix SB.
- `OP-###` (git commit/push requests) are captured in the user-driven README,
  not here — this file is agent-centric and focuses on implemented capabilities.
