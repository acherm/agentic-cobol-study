# KEY_FEATURES.md — `SATCobol-cc`

## 1. Preamble

The contract was "implement a SAT solver in COBOL that reads DIMACS
CNF, prints SAT-Competition-style output, and is cross-checked against
MiniSat and SAT4J on `uf*`/`uuf*` and SAT4J's own acceptance suite".
What the Claude Code agent actually delivered is: a modular DPLL
solver with two-watched literals, an end-to-end SAT4J acceptance-suite
runner (113 translated fixtures with 111/113 pass at the final commit),
a 2 400-instance MiniSat cross-comparison (overall ratio 1.9× at
`c3b2a7c`), and three rounds of branching-heuristic evolution
(occurrence → VSIDS-lite with JW seeding + phase saving + Luby
restarts). A first-UIP CDCL extension was coded but **left uncommitted
and unbenchmarked** because the session was truncated 4 s after the
final benchmark launch.

A "key feature" below is any externally observable capability or
quality attribute of depth ≥ 1 that is **not purely build/infra**. The
minimal `Makefile` is mentioned once at the bottom for completeness.
Entries that obviously belong together at feature granularity (e.g.
VSIDS + phase + JW + Luby all landed in one commit) are consolidated
into a single row; the collapsed SB ids are listed in the evidence
column.

Reference evidence bundle:
[`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md) (42 SB entries
including 3 uncommitted, 13 episodes), [`appendix.json`](appendix.json),
[`README.md`](README.md), project root
`/Users/mathieuacher/SANDBOX/SATCobol-cc/`.

## 2. Ranked table (top features by `depth × (1 + effort × 0.5)`)

| rank | SB/F id | title | class | depth | effort | score | evidence |
|---|---|---|:-:|:-:|:-:|:-:|---|
| 1 | F-CDCL-UC (SB-040, SB-041, SB-042) | **Uncommitted** CDCL core: first-UIP conflict analysis + non-chronological backjump + learnt-clause DB + asserting-literal propagation | ALG | 3 | 2 | 6.0 | `/Users/mathieuacher/SANDBOX/SATCobol-cc/src/copy/search.cpy:7-20` comment block; `propagate.cpy:203-…` `ANALYZE-CONFLICT`; `ADD-LEARNT-CLAUSE`, `BACKJUMP-TO-LEVEL`, `WS-LEARNT` present on disk; agent claim "33/33 unit tests pass + smokes correct" at `[T:2026-04-16T13:43:46]`. Not in git; no post-CDCL benchmark attested. |
| 2 | F-DPLL (SB-012, SB-013, SB-014, SB-015, SB-016) | Baseline DPLL solver core: iterative unit propagation + chronological backtracking with explicit `(var, kind)` trail, `s SATISFIABLE`/`v … 0` SAT-Competition I/O, self-validation via `--check-model` | ALG | 3 | 2 | 6.0 | `src/copy/search.cpy` (139 LOC), `propagate.cpy` (419 LOC), `cnf.cpy` (189 LOC); commit `bdea674`; 7 solve-fixtures + uf75/uuf75 200-instance sweep (`[T:2026-04-15T15:31-41]`) |
| 3 | F-HEUR (SB-021, SB-022, SB-034, SB-035, SB-036, SB-037) | Two-watched literals + occurrence branching → then VSIDS-lite + phase saving + Jeroslow-Wang seeding + Luby restarts with agent-tuned large base | ALG | 3 | 2 | 6.0 | commits `de35d40` then `c3b2a7c`; `WS-ACT`, `WS-PHASE` in `propagate-data.cpy`; SAT4J 94 → 111 pass (`[T:2026-04-16T10:03:27]`); +30 % on hard uuf150 |
| 4 | F-SAT4J (SB-029, SB-030, SB-031, SB-032, SB-033, SB-038) | SAT4J acceptance suite end-to-end: 113 translated DIMACS fixtures (aim / ii / jnh / pigeons + 13 misc) + `expected.tbl` verdict table + `run_sat4j_tests.sh` 30-s-timeout runner; attested 111/113 pass at final commit | VER | 2 | 3 | 5.0 | `tests/sat4j/{aim,ii,jnh,pigeons}/*.cnf` (113 files) + `expected.tbl` (113 lines); `tests/run_sat4j_tests.sh` (141 LOC); commit `57de05d`; 13 runner invocations in session; agent extracted from `AbstractM2Test.java` / `TestsFonctionnels.java` / `BugSAT175.java` (SAT4J GitLab source) |
| 5 | F-MINISAT-XCHK (SB-025, SB-026, SB-027) | MiniSat cross-check script with structured repro capture on mismatch (input.cnf + cobsat.out + minisat.out + minisat.stdout + STATUS) and SATLIB `%`-trailer stripping before invoking MiniSat | VER | 2 | 2 | 4.0 | `scripts/crosscheck_minisat.sh` (180 LOC); commit `a121b45`; 13 invocations logged; exit-non-zero-on-disagreement contract |
| 6 | F-BENCH (SB-028, SB-039) | 2 400-instance benchmark sweep + cobsat-vs-minisat comparison across uf/uuf × {100, 125, 150}: overall 1.9×, per-family 1.3× → 5.8×, 0 verdict errors — composes over F-DPLL + F-HEUR + F-MINISAT-XCHK | CMP | 2 | 2 | 4.0 | session `[T:2026-04-16T10:22:24]` (2400/2400 correct) + `[T:2026-04-16T13:16:16]` (cobsat 101.6 s vs minisat 52.6 s); no CSV committed |
| 7 | F-MODULES (SB-018, SB-019, SB-020) | **12-COPY-book** modular decomposition with explicit `data-copybook` vs `logic-copybook` split per module (`io-files / io-fd / io-data / io` + `{parser,cnf,propagate,search}-data.cpy` + `{…}.cpy`); finer-grained than sibling Codex (which uses 5 copybooks) | LNG | 2 | 2 | 4.0 | `src/copy/*.cpy` (12 files, 1 581 LOC); `src/cobsat.cob` dispatch (83 LOC); commit `b2d8324 Refactor cobsat into per-module copybooks`; `-I src/copy` in `Makefile` |
| 8 | F-PARSER (SB-001, SB-002, SB-009, SB-032) | DIMACS CNF parser in free-format COBOL — `c` / `%` comments, `p cnf V C` header, arbitrary whitespace, multi-line clauses, `0` terminators, **SATLIB `%`-trailer tolerance**, plus SAT4J-style missing-trailing-`0` leniency, plus `--parse` normalised-output mode | DOM | 2 | 2 | 4.0 | `src/copy/parser.cpy` (404 LOC); commits `049f4b5` + `88e8e99` (% fix) + `57de05d` (SAT4J lenience); 8 edge-case fixtures in `tests/fixtures/`; DIMACS is an externally-specified format (secondary PRO tag) |
| 9 | F-CHECKMODEL (SB-006, SB-007, SB-008) | `--check-model file.cnf model.txt` mode: parses a proposed assignment, exits 0 iff every clause is satisfied, non-zero with precise `UNSAT clause N: <clause>` message otherwise; 9 paired sat/unsat/partial model fixtures | DOM | 1 | 1 | 1.5 | `src/cobsat.cob` CLI dispatch; `tests/fixtures/*.model` (9 files); `tests/run_tests.sh` asserts exact error format via regex; commit `3fc5cdd` |
| 10 | F-PARSER-TESTS (SB-004) | Parser edge-case harness (32 numbered runner cases across empty_lines / CRLF / trailing / many-spaces / multiline / interleaved_comments / comment_between_tokens / check-model / solve) | VER | 1 | 1 | 1.5 | `tests/run_tests.sh` (292 LOC); `tests/fixtures/*.cnf` + `*.model`; golden-string comparison on `--parse` output |
| 11 | F-BUILD (SB-003, SB-023) | Minimal `Makefile` (`all / test / clean`, 18 LOC); `tests/perf.sh` regression-tripwire with python3 sub-second timing; 9 bisectable commits on default branch | INF | 1 | 1 | 1.5 | `Makefile` (18 lines); `.gitignore` (9 lines); `.git/logs/HEAD` shows 9 linear commits + 2 HEAD resets |

**Significance notes (one line each, keyed to rank):**

1. **F-CDCL-UC** — Not just-an-algorithm, but **unfinished**. First-UIP + backjumping in COBOL requires hand-rolling conflict-graph traversal, the learnt-clause DB growth, and two-watched-literals invalidation on backjump, all on fixed-capacity `OCCURS` tables. The code exists on disk and the agent claims 33/33 unit tests pass, but the session was truncated 4 s after the final benchmark launch — so there is no commit, no attested benchmark improvement, and no reproducible `git clone` path to the CDCL binary. Score-wise a depth-3 feature, but the effort cap (2) reflects the unverified/uncommitted state.
2. **F-DPLL** — Textbook algorithm, but the COBOL port chose an **iterative** formulation with an explicit `(var, kind)` trail rather than `PERFORM` recursion, to keep stack depth bounded on 2 400-instance sweeps. The commit message explicitly notes "Iterative DPLL: … explicit trail". Depth-3 because this is the spine that every later commit edits; effort-2 because the baseline landed in one commit.
3. **F-HEUR** — This row absorbs two heuristic-evolution commits. The second (`c3b2a7c`) is non-trivial: JW seeding + VSIDS-lite + phase saving + Luby **and** an agent-initiated diagnosis that "without clause learning, aggressive restarts throw away progress" → large restart base. That tuning step is the signature of measured engineering, not a theory-dump.
4. **F-SAT4J** — VER with heavy mechanical translation effort: the agent fetched SAT4J's Java source tree and extracted test verdicts from `AbstractM2Test.java`, `TestsFonctionnels.java`, and `BugSAT175.java` into 113 DIMACS fixtures + a `expected.tbl` verdict table. The 111/113 pass rate at `c3b2a7c` is an externally falsifiable claim grounded in SAT4J's own JUnit asserts. Effort-3 because this is the single longest episode (05:10 → 08:34, 3h24).
5. **F-MINISAT-XCHK** — Pure VER: SAT/UNSAT verdicts are made externally falsifiable. The agent-initiated detail — strip SATLIB `%` trailer before invoking MiniSat — is the kind of undocumented compatibility glue that only appears when you actually run the tool.
6. **F-BENCH** — CMP (emergent composition): only meaningful because F-DPLL (something to time), F-HEUR (the new heuristic), F-MINISAT-XCHK (the external oracle), and the 8 committed SATLIB archives (corpus) already exist. The "1.9×" number is only meaningful on top of those four.
7. **F-MODULES** — LNG: COBOL has no native module system. The CC replica goes **further** than the Codex sibling: each module has both a `<mod>-data.cpy` (WORKING-STORAGE records) and a `<mod>.cpy` (PROCEDURE paragraphs), plus I/O is split across four copybooks (`io-files` FILE-CONTROL, `io-fd` FD entries, `io-data` scalars, `io.cpy` paragraphs). That is a deliberate separation-of-concerns that pays off when the CDCL edit only touches 5 copybooks without altering `src/cobsat.cob`.
8. **F-PARSER** — DOM: DIMACS is a published format, so the depth comes from robustness (multi-line clauses, whitespace tolerance, **two** separate real-world compatibility patches: SATLIB `%\n0\n` end-of-data, and SAT4J's lenient missing-trailing-`0`). Secondary PRO tag because DIMACS is an externally-specified standard.
9. **F-CHECKMODEL** — DOM: clause-by-clause evaluator. Low depth but it **is** a separate public mode with its own error format (`UNSAT clause N: <offending-clause>` asserted by regex) and 9 fixture models including a `multiline.partial.model` for the partial-assignment case.
10. **F-PARSER-TESTS** — VER: a 32-case runner harness that re-feeds every SAT model back through `--check-model` — a small but meaningful internal-consistency check that catches a whole class of bugs.
11. **F-BUILD** — INF, included for completeness only. Notably **minimal** (18-line `Makefile`, no wrapper script, no `sat4j-test` / `perf` / `compare-minisat` targets — scripts invoked directly). Compare sibling's 28-line `Makefile` with 6 phony targets.

## 3. Composition chains

Four chains are clearly visible in the backlog. The last item of each chain is *only meaningful* because the earlier items are in place and correct.

- **Chain A — correctness oracle:**
  F-PARSER → F-CHECKMODEL → F-DPLL → F-MINISAT-XCHK → F-SAT4J
  > A parser must exist before a model-checker is useful; the model-checker is the lightweight self-oracle every SAT answer self-runs through; DPLL produces the models; MiniSat cross-check externalises the oracle; SAT4J acceptance-suite translation raises the corpus to 113 published-verdict instances. Without the earlier nodes, the last two have nothing to compare.

- **Chain B — heuristic evolution on a stable substrate:**
  F-PARSER → F-DPLL → F-MODULES → F-HEUR → F-SAT4J
  > The data/logic copybook split (F-MODULES) is what made two heuristic rewrites — watched literals at `de35d40`, then VSIDS+phase+JW+Luby at `c3b2a7c` — feasible without touching `src/cobsat.cob`. F-SAT4J is the *regression witness*: 94 → 111 pass after F-HEUR proves the heuristic did not break soundness.

- **Chain C — performance measurement:**
  F-DPLL → F-HEUR → F-MINISAT-XCHK → F-BENCH
  > Perf numbers require something correct to measure (DPLL + heuristic), an external oracle (MiniSat), and a 2 400-instance sweep harness. The "1.9×" ratio is **only a claim** once the earlier three are in place and 2 400/2 400 verdicts agree.

- **Chain D — (broken) algorithmic ladder:**
  F-DPLL → F-HEUR → F-CDCL-UC → (post-CDCL benchmark — NOT DELIVERED)
  > This is the chain that **did not finish**. The CDCL code sits on disk but never gets a commit, a re-run of SAT4J, or a re-run of the 2 400-instance comparator. Session truncation is the break; in the Codex sibling, the same chain terminates cleanly at `edb0942b` + a perf round.

## 4. Significance profile

Count per primary class across the top 11 rows (secondary tags in parens are not counted here, so each feature contributes once):

| Class | Count | Share | Notes |
|---|:-:|:-:|---|
| ALG | 3 | 27 % | F-CDCL-UC (uncommitted), F-DPLL, F-HEUR |
| VER | 3 | 27 % | F-SAT4J, F-MINISAT-XCHK, F-PARSER-TESTS |
| CMP | 1 | 9 % | F-BENCH (emerges on top of ALG + VER + DOM) |
| LNG | 1 | 9 % | F-MODULES (12-COPY-book split with data/logic separation) |
| DOM | 2 | 18 % | F-PARSER (DIMACS + SATLIB + SAT4J lenience), F-CHECKMODEL |
| INF | 1 | 9 % | F-BUILD |
| PRF | 0 | — | No standalone perf-engineering row: heuristic work is folded into F-HEUR; no multi-round perf ladder is attested (the would-be PRF row requires the post-CDCL benchmark which was never produced). |
| PRO | 0 | — | (F-PARSER carries a secondary PRO tag; not double-counted) |
| SYS | 0 | — | No cross-runtime / FFI work — COBOL stays self-contained, shells out only for MiniSat timings |

**Centre of gravity.** ALG + VER + CMP together are 7/11 = **64 %** of the ranked features, with LNG + DOM contributing another 27 %. The project earns points in **six of nine** significance classes. Unlike the Codex sibling, PRF is notably **absent** as a standalone class: there is no measured multi-round perf ladder because the CDCL round never got attested numbers.

## 5. Verdict

**Verification-centric hybrid — ALG + VER with a genuine LNG supporting act, CDCL left unfinished.** This is neither "just-an-algorithm" nor "just-domain-modelling": baseline DPLL is textbook, but the iterative-trail port is non-trivial COBOL engineering; the 12-copybook data/logic split is the quiet LNG contribution that made the later heavy edits (watched literals, VSIDS+phase+JW+Luby, and the uncommitted CDCL) feasible; correctness rests on **two independent external oracles** (SAT4J's own verdict table, MiniSat's exit codes); and the 2 400-instance sweep is an emergent composition. The project would have matched the Codex sibling's "balanced ALG + PRF + VER" profile if CDCL had landed a commit — instead, session truncation caps the ranked ladder at heuristic evolution, and the CDCL achievement exists only as on-disk, unverified code.
