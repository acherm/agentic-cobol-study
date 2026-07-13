# `cobol-compiler-codex` — Key Features (classification & ranking)

## Preamble

MiniCOBC was asked to build "a COBOL compiler in COBOL" and demonstrate non-trivial programs through it. What actually shipped is a single-file `src/minicobc.cob` (~10.5k COBOL LOC) that emits C (then linked with `gcc`), validated against four external COBOL codebases (game15tictactoe, chess engine, DOOM, Flappy Bird/SDL2) and benchmarked head-to-head against GnuCOBOL on every one of them. Relative to the `-cc` sibling, the distinctive axis here is the **VER + PRF layer**: GnuCOBOL is wired in as an oracle, `cutechess-cli` runs end-to-end Elo matches, and the 48 SB entries map 1:1 onto 13 squash commits. A "key feature" is counted at ≥ depth 1 and excludes pure infra (commits, README attribution, etc.) unless it is a validation/benchmark artefact that carries substantive engineering.

## Ranked table (top 12)

| rank | SB/BL id | title | class | depth | effort | score | evidence |
|-----:|----------|-------|-------|------:|-------:|------:|----------|
| 1 | SB-001 / SB-002 / SB-003 (BL-001) | COBOL-to-C compiler skeleton + subset lexer/parser + core statements | ALG / LNG | 3 | 3 | 7.5 | `src/minicobc.cob` single-file ~10.5k LOC; 4 divisions, `PIC 9/X/Z`, `DISPLAY`, `MOVE`, arithmetic, `IF/ELSE IF/END-IF`, `STOP RUN`; written in COBOL itself |
| 2 | SB-031 / SB-032 / SB-033 / SB-034 / SB-035 (BL-012, BL-013) | Generic front-end re-architecture: `EVALUATE`, `PERFORM VARYING`, paragraph `PERFORM`, groups, `REDEFINES`, `OCCURS`, indexed refs, `CALL USING BY VALUE/REFERENCE/RETURNING`, `FUNCTION SQRT/NUMVAL/TRIM/MOD/REM`, multiline statements | ALG / DOM | 3 | 3 | 7.5 | `examples/generic/*.cob` (~45 programs); replaces template-based compat with real parsing pipeline; necessary for DOOM and generic chess |
| 3 | SB-050 / SB-051 / SB-052 / SB-060 / SB-061 (BL-018, BL-019) | Full generic chess-engine build (phases 1–4: `BOARD`, `FEN`, `ATTACK`, `MOVEGEN`, `MAKEMOVE/UNMAKE`, `PERFT`, `EVAL`, `SEARCH`, `TIMEUTIL`, `MOVE2UCI`, top-level `COBOCHESS`) through generic pipeline | CMP / DOM | 3 | 3 | 7.5 | `tests/chess/phase{1,2,3,4}_*_harness.c`; each phase cross-checks against GnuCOBOL; only possible because #1, #2 exist — pure emergent composition |
| 4 | SB-015 (BL-006) | Bootstrap / self-host check (stage-0 `cobc`→`minicobc`; stage-1 `minicobc`→compiler C; stage-2 diff) | LNG / VER | 3 | 2 | 6.0 | `scripts/test-selfhost.sh`, `templates/compat/minicob.c`; "compiler written in COBOL that compiles itself" via a pinned compat template — hallmark language-level achievement |
| 5 | SB-070 / SB-071 / SB-072 (BL-021) | `MOVE WPC(F-IX-1) TO FRIEND-L` indexed-source miscompile: isolated, direct `QUIESCE`/`ALPHABETA` equivalence harness, regression input, fix | VER / PRF | 3 | 2 | 6.0 | `scripts/test-chess-phase3-direct.sh`, `tests/chess/phase3_direct_harness.c`, `examples/generic/move_index_expr.cob`; user pushback "strange to beat GnuCOBOL — do you check correctness?" triggered self-correcting loop |
| 6 | SB-090 / SB-091 (BL-024) | End-to-end Elo assessment via real `cutechess-cli`: paired match, PGN export, Elo ±CI, no adjudication | CMP / VER | 2 | 3 | 5.0 | `scripts/run_chess_cutechess_elo.py`, `scripts/run-chess-cutechess-elo.sh`, `scripts/run-minicobc-chess-uci.sh` (`stdbuf` wrapper); requires the full chain compiler → UCI engine → tournament tooling |
| 7 | SB-022 / SB-023 / SB-024 (BL-009) | Optimization mode (`./minicobc OPT`): constant folding, constant propagation, dead-store elimination, strength reduction, loop-condition canonicalization, width-aware integer selection | PRF / ALG | 2 | 3 | 5.0 | `examples/opt/*.cob` (8 programs), `scripts/compare-minicobc-optimizations.sh`; baseline-vs-opt comparison; known miscompile on chess (`MINICOBC_OPT=1` flagged unsafe) — honest limitation |
| 8 | SB-013 / SB-014 / SB-012 (BL-003, BL-004, BL-005) | GnuCOBOL performance comparison harness + benchmark manifest + sample rewrites accepted by both compilers | VER / PRF | 2 | 2 | 4.0 | `benchmark/cases.json`, `scripts/compare-compilers.sh`, `scripts/compare_compilers.py`; per-case compile time + runtime JSON+MD reports vs `cobc` oracle |
| 9 | SB-030 / SB-033 / SB-034 / SB-037 (BL-011, BL-014) | COBOL DOOM build path: template bridge for `doom.cob`, external `CALL` to C helpers, `FUNCTION SQRT`, OPT-vs-baseline comparison | SYS / CMP | 2 | 2 | 4.0 | `templates/compat/doom/`, `scripts/build-cobol-doom.sh`, `scripts/compare-cobol-doom-opt.sh`; COBOL → C → renderer toolchain, externally-visible artefact repo |
| 10 | SB-062 / SB-063 / SB-064 (BL-020) | Chess benchmark diversification: fixed-depth search suite (default + extended profiles), depth-1 cross-check vs `python-chess` across 11 FENs, cautionary README caveat | VER / PRF | 2 | 2 | 4.0 | `scripts/compare-chess-search-suite.sh`, `scripts/compare-chess-depth1-suite.sh`; explicitly flags runtime ratios as "strong local signal, not a settled general claim" |
| 11 | SB-080 / SB-081 (BL-022, BL-023) | Paired-game tournament harness + MiniCOBC-vs-Stockfish tournament across `Skill Level` 0/5/10/15/20 | CMP / VER | 2 | 2 | 4.0 | `scripts/compare-chess-tournament.sh`, `scripts/compare-chess-stockfish-tournament.sh`; diversified starts with color swap, JSON+MD+PGN; meaningless without generic chess build |
| 12 | SB-042 (BL-016) | Flappy Bird / SDL2 compatibility path: `examples/flappy.cob` through pinned compat template, link with `src/cpg.c` SDL2 helper, `SDL_VIDEODRIVER=dummy` smoke test | SYS | 2 | 1 | 3.0 | `templates/compat/pygame/`, `scripts/build-cobol-pygame.sh`; COBOL → C → SDL2 FFI; shallower than DOOM because it stayed template-bound rather than graduating to generic |

### Significance notes (one-liner per row)

1. Not "just an algorithm": writing a parser + codegen **in COBOL** is an LNG move, and 10.5k COBOL LOC in one source is well past textbook. Still grounded in standard recursive-descent / template-emission — hence ALG primary, LNG secondary.
2. Not just-an-algorithm: the depth here is the *interaction* between the data-description model (`OCCURS`, `REDEFINES`, packed groups) and the procedural statements — each new construct forces re-architecting the symbol table + codegen.
3. Pure CMP: this feature could not exist without #1 and #2, and exists only because the chess engine is a realistic stress test. Four harnesses, each cross-checking against GnuCOBOL — emergent capability.
4. LNG par excellence: the depth-3 item on the taxonomy's own scale ("Self-hosted compiler"); caveat is that Phase-2 uses a compat template (`minicob.c`) rather than a pure generic re-compile, hence the effort is 2 rather than 3.
5. Not just a bug fix: building a *direct-equivalence* harness that bypasses the top-level `SEARCH` wrapper to isolate the miscompile is a VER construction; the prompt trail (`PL-044 → PL-045 → PL-046`) shows the agent owning the investigation after redirect.
6. CMP: Elo assessment requires compiler + UCI-compliant output + line-buffered wrapper + paired-match logic + PGN parser. The pilot sample is small (scored `Q6=0` reproducibility) but the pipeline is real.
7. PRF with honest reporting: 6+ passes implemented and measured, with the known-unsafe flag on chess documented rather than hidden.
8. VER/PRF is the project's distinguishing axis — GnuCOBOL is wired in as an oracle on every case, not just as a comparison point. This is what separates `-codex` from `-cc`.
9. SYS: the challenge is at the COBOL↔C boundary (`CALL "name" USING BY VALUE/REFERENCE`), not in writing a renderer. DOOM is a shipped artefact (published repo) — externally visible milestone.
10. VER with methodological honesty: cross-check vs `python-chess` (third reference, not just GnuCOBOL), and the caveat language is itself a signal of calibration.
11. CMP: tournament harnesses are only valuable because the engine plays legally and UCI works end-to-end. Stockfish skill sweep is textbook-style but its setup is substantial.
12. SYS but shallower: template-based rather than graduated to the generic front-end (`BL-016` is marked Partial in the rubric). Included because it extends the SYS profile beyond DOOM.

## Composition chains

1. **Compiler core → generic re-architecture → generic chess engine (phases 1–4) → tournament harness → cutechess Elo**
   `SB-001/002/003 → SB-031/032/033 → SB-050/051/060/061 → SB-080/081 → SB-090/091`. Each step is meaningless without the previous: Elo is only a number if the engine is legal; the engine is only legal if `SEARCH`+`MOVEGEN` are correct; those are only correct if the generic front end emits the right code. Five-link chain — the project's spine.

2. **Compiler core → benchmark manifest → GnuCOBOL comparison → chess perft harness → diversified search suite + depth-1 cross-check (python-chess)**
   `SB-001/003 → SB-012 → SB-013 → SB-021 → SB-062/063`. The VER/PRF chain: every benchmark escalates the rigor of the oracle (GnuCOBOL stdout → GnuCOBOL perft counts → python-chess legality). Explains the "scientifically useful framing" from the assessment TL;DR.

3. **Compiler core → generic front end → self-correcting bug hunt on `MOVE WPC(F-IX-1)`**
   `SB-001 → SB-031/032 → SB-070/071/072`. The user pushback ("strange to beat GnuCOBOL — do you check correctness?") only makes sense because #2 produced the surprising speedup; the fix only matters because the generic front end produces the bad code. Chain is short but is the clearest demonstration of the project's self-correcting loop.

4. **Generic front end + `CALL USING BY VALUE/REFERENCE` + `FUNCTION SQRT` → DOOM build path**
   `SB-031/033/034 → SB-030/037`. SYS chain: no single piece is rocket science, but DOOM only compiles because the COBOL↔C boundary is spec'd out end-to-end; SQRT is needed for ray-casting math, `BY REFERENCE` `PIC X` buffers for framebuffers.

## Significance profile

Count per primary class across the top 12 features (secondary tags in parentheses):

| Class | Count (primary) | Also as secondary |
|-------|:---------------:|:-----------------:|
| ALG (Algorithm implementation) | 2 | 2 |
| DOM (Domain modelling) | 0 | 2 |
| SYS (System integration / FFI) | 2 | 0 |
| INF (Infrastructure) | 0 | 0 |
| PRO (Protocol / standard) | 0 | 0 |
| LNG (Language-level achievement) | 1 | 1 |
| VER (Correctness verification) | 3 | 3 |
| PRF (Performance engineering) | 1 | 4 |
| CMP (Emergent composition) | 3 | 1 |

Centre of gravity: **VER + CMP + PRF** combined dominate the top half (7 of 12 primary tags), with ALG/LNG anchoring the compiler itself. This is the hallmark of the `-codex` project: the compiler is the baseline, but the scientific apparatus around it — oracles, tournaments, Elo, caveats — is where the engineering depth lives.

## Verdict

**Hybrid: ALG/LNG foundation + VER/PRF superstructure with heavy CMP** — a COBOL-in-COBOL subset compiler (ALG+LNG) whose distinguishing contribution is a benchmark-driven comparison apparatus against GnuCOBOL and a self-correcting verification loop (VER+PRF+CMP), pushed into emergent territory by compiling real-world COBOL (DOOM, chess engine, Flappy) and running end-to-end Elo matches through `cutechess-cli`.
