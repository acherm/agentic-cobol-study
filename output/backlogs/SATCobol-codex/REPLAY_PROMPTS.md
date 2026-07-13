# Replay Prompts

Reusable prompts for reproducing the `SATCobol` project step by step. Each prompt is self-contained enough to copy-paste into a coding agent session. They specify **what** to build (behavior, inputs, outputs, verification), not **how** (no algorithm names, no data-structure prescriptions, no COBOL-specific idioms).

Use them sequentially: each step builds on the previous one. The end state is a COBOL-based SAT solver binary `cobsat` that (1) parses DIMACS, (2) verifies models, (3) decides SAT/UNSAT on realistic SATLIB instances, (4) cross-checks against MiniSat or SAT4J, and (5) lands within a small multiplicative factor of MiniSat on the uf/uuf SATLIB families.

For reference on what was actually built (algorithms chosen, commits, benchmark numbers, autonomous decisions), see [SPECIFICATION_BACKLOG.md](SPECIFICATION_BACKLOG.md).

---

## Step 1: DIMACS CNF Parser

> Start a fresh workspace. Build a SAT solver in COBOL (GnuCOBOL, `cobc -x -free`). The first milestone is just the front end.
>
> Produce a binary `cobsat` (a shell wrapper `./cobsat` that compiles `build/cobsat` from `src/` is fine) that accepts a mode `./cobsat --parse file.cnf` and prints a normalised representation of the input: the declared number of variables, the declared number of clauses, and the flat list of literals grouped by clause. The exact text format is your choice, but it must be stable (tests will diff against it).
>
> The parser must accept the full DIMACS CNF dialect:
> - `c …` comment lines (anywhere, including between tokens of a clause)
> - a `p cnf V C` header line
> - arbitrary whitespace (spaces, tabs, multiple blank lines)
> - clauses that span multiple lines, terminated by `0`
> - CRLF as well as LF line endings
> - SATLIB-style trailing end markers (`%` line and/or an extra lone `0`) appearing **after** the declared number of clauses has been read — these must be tolerated, not treated as an extra clause
>
> Provide a `Makefile` with at least `build`, `test`, and `clean` targets. Use `cobc -x -free` (free-format COBOL) with an include path pointing at wherever you place reusable modules.
>
> Add a shell-based unit-test harness under `tests/` with fixtures exercising at least: empty lines, CRLF line endings, trailing spaces on tokens, runs of many spaces between tokens, comment lines interleaved between literals of a clause, a SATLIB-style `%` / trailing `0` end marker, and a large synthetic CNF of ~100 000 clauses (to show the parser streams rather than buffers). Each fixture must have an expected-output file and the test runner must diff and report `all tests passed` on success.
>
> Verification:
> - `make build` produces a working binary
> - `make test` ends with `all tests passed`
> - `./cobsat --parse tests/fixtures/<any>.cnf` produces the expected output for every fixture
> - The large synthetic fixture parses in a few seconds with no out-of-memory errors

---

## Step 2: Model Verifier Mode

> Extend `cobsat` with a second mode: `./cobsat --check-model file.cnf model.txt`.
>
> The model file contains a variable assignment as a whitespace-separated list of signed integers (a positive integer `v` means variable `v` is true, `-v` means it is false). Either a flat list or DIMACS `v … 0` style output must be accepted — both shapes appear in practice.
>
> Semantics: exit code **0** iff every clause of `file.cnf` is satisfied by the assignment; a non-zero exit code otherwise. On failure, print a short diagnostic naming the first violated clause.
>
> Extend the test harness with model fixtures under `tests/models/`:
> - a satisfying assignment for a trivially-SAT CNF
> - a satisfying assignment given in DIMACS `v … 0` style (leading `v`, trailing `0`)
> - a model that violates the **first** clause (expected exit non-zero, diagnostic points at clause 1)
> - a model that violates a **later** clause (expected exit non-zero, diagnostic points at that clause)
>
> `make test` must remain green and must now exercise both `--parse` and `--check-model` assertions.

---

## Step 3: Baseline SAT Solver

> Add a third mode (the default when no flag is passed): `./cobsat file.cnf` runs a complete decision procedure on the formula and prints a SAT-Competition-style result.
>
> Output format (stdout, exactly):
> - On a satisfiable instance: a line `s SATISFIABLE`, followed by one or more lines starting with `v ` that together list every variable's assignment as signed integers, with the final `v` line ending in ` 0`. Example:
>   ```
>   s SATISFIABLE
>   v 1 -2 3 -4 5 0
>   ```
> - On an unsatisfiable instance: a single line `s UNSATISFIABLE`.
> - On any instance the solver refuses to decide (timeout, resource cap): a line `s UNKNOWN`.
>
> Exit codes (SAT-Competition convention):
> - `10` on SAT
> - `20` on UNSAT
> - `0` on UNKNOWN or on user errors that print a usage message
>
> Correctness constraints (these are what your tests must enforce; algorithm choice is yours):
> - Every `s SATISFIABLE` output must be accompanied by a model that `./cobsat --check-model` accepts with exit 0. Wire this self-check into the test runner: for every SAT fixture, feed the emitted model back through `--check-model` and fail on disagreement.
> - Every `s UNSATISFIABLE` output must be genuinely unsatisfiable (verify against fixtures whose status is pre-known, and later via cross-check in Step 6).
>
> Ship solver fixtures under `tests/fixtures/` covering at least: a chain of unit clauses forcing a unique model, a small XOR-like encoding with multiple solutions, an obvious contradiction (`x ∧ ¬x`), and a small pigeonhole instance (e.g. `PHP(4,3)`) that is UNSAT but small enough to decide in well under a second. `make test` stays green.
>
> Additionally, run the solver over the 100 instances of the SATLIB `uf75-325` family and the 100 instances of `uuf75-325` (place `tests/uf75-325.tar.gz` and `tests/uuf75-325.tar.gz` in the repo; extract at test time). Every `uf*` instance must be reported SAT with a model that re-verifies, and every `uuf*` instance must be reported UNSAT. Budget each instance at most a few seconds.

---

## Step 4: MiniSat Cross-Check Harness

> Add `scripts/crosscheck_minisat.sh` (invokable as a standalone script and as `make crosscheck` or equivalent). Given a single `.cnf` file, the script:
>
> 1. Runs `./cobsat` on the input and captures its stdout / exit code.
> 2. Normalises the input by piping it through `./cobsat --parse` (so MiniSat sees the same token stream the COBOL parser saw — this is the key property under test).
> 3. Runs `minisat` on the normalised CNF and captures its result.
> 4. Compares the SAT/UNSAT verdicts. On match, exits 0 silently.
> 5. On **mismatch** (or if `cobsat` emits a SAT verdict but the model fails `--check-model`, or if `minisat` itself errors out): stores a full repro bundle under `tests/crosscheck_failures/<instance>/` containing `cobsat.out`, `minisat.out`, `minisat.err`, and the normalised `.cnf`, then exits non-zero with a message naming the instance.
>
> Make `minisat` discoverable via `$PATH` by default, overridable via an environment variable such as `MINISAT_BIN`. The script must work when only a subset of inputs are available; it must not depend on being run from inside any particular subdirectory.
>
> Verification: run the cross-checker across a handful of SATLIB instances from `uf75-325` and `uuf75-325` and confirm zero mismatches. `tests/crosscheck_failures/` should be empty (or contain only a `.gitkeep`).

---

## Step 5: Benchmark Runner + PAR-2 Scoring

> Add `scripts/compare_minisat.sh` (also wired as `make compare-minisat`). Given one or more SATLIB-style `.tar.gz` archives (with a sensible default that picks up all `tests/uf*-*.tar.gz` and `tests/uuf*-*.tar.gz`), the script:
>
> 1. Extracts each archive into a temp directory.
> 2. Runs `./cobsat` and `minisat` on every instance, one at a time, with a per-instance wall-clock timeout (e.g. 60 s — overridable by env var). Records each run's verdict, exit code, and elapsed time.
> 3. Prints a per-family CSV (one row per archive) with at least these columns:
>    - `family`
>    - `cobsat_total`, `cobsat_avg`, `cobsat_max`
>    - `minisat_total`, `minisat_avg`, `minisat_max`
>    - `cobsat_over_minisat` (ratio of totals)
>    - a count of any instance where the two solvers disagree (should always be 0; non-zero ends the script with non-zero exit)
> 4. Prints a grand `TOTAL` row aggregating across all families.
>
> Support a PAR-2-style scoring column alongside raw totals: any timeout counts as `2 × timeout_seconds` in the accumulator. Document this in the script header.
>
> Before running end-to-end, place the eight SATLIB archives under `tests/`:
> `uf75-325`, `uuf75-325`, `uf100-430`, `uuf100-430`, `uf125-538`, `uuf125-538`, `uf150-645`, `uuf150-645`.
>
> Run the full comparator at least once and commit the resulting CSV (or embed it in a short Markdown note) as the **baseline** for later steps. Expect the baseline `cobsat_over_minisat` grand total to be large (double-digit multiplicative slowdown is fine at this point — this is the number Step 7 will beat).

---

## Step 6: SAT4J Regression Suite Translation

> Using the SAT4J source tree as reference (https://gitlab.ow2.org/sat4j/sat4j), extract the DIMACS-shaped test inputs its Java test suite uses, translate them into standalone `.cnf` files under `tests/sat4j/`, and drive them through `./cobsat`.
>
> Concretely:
> - Collect every file-based CNF referenced by the file-based functional / CLI tests of SAT4J's core solver into `tests/sat4j/fixtures/`.
> - Extract CNFs embedded in parametric test classes (typically `aim`, `jnh`, `pigeons` families, plus targeted regressions for the `BugSATxxx` issue cases) into `tests/sat4j/embedded/`.
> - Ship two TSV manifests (e.g. `manifest-file-based.tsv`, `manifest-embedded.tsv`) mapping each `.cnf` to (a) the originating SAT4J test identifier and (b) the expected verdict (`SAT` or `UNSAT`).
> - Write `tests/run-sat4j-tests.sh` (exposed as `make sat4j-test`) that iterates the manifests, runs `./cobsat` on each instance, checks the verdict, and self-verifies every SAT verdict via `--check-model`.
> - In a short README under `tests/sat4j/`, document what is deliberately **not** translated: pseudo-Boolean / cardinality test cases, MUS / explanation tests, iteration-style tests that rely on SAT4J's Java API.
>
> Verification: `make sat4j-test` runs the full translated suite and reports all cases pass. Aim for > 100 file-based fixtures plus ~10 embedded regression cases; if you cannot reach a given count, document which SAT4J tests you skipped and why.

---

## Step 7: Performance Iteration Loop

> Now make it fast. Without changing observable behaviour (every existing test stays green, every verdict stays correct, every `--check-model` self-check keeps passing), improve the solver's runtime until it lands within a small multiplicative factor of MiniSat on the SATLIB families set up in Step 5.
>
> Work in short iteration cycles. Each cycle:
> 1. Decide on one specific, *measurable* target (e.g. "halve the total time on `uuf100-430`", "bring `cobsat_over_minisat` on `uuf125-538` under 15", "eliminate any family where we time out more than 2 instances").
> 2. Change the solver.
> 3. Re-run `make test`, `make sat4j-test`, and `scripts/crosscheck_minisat.sh` on a sample — **none** of these may regress.
> 4. Re-run `make compare-minisat` end-to-end.
> 5. Produce a side-by-side Markdown table of the previous vs. current per-family totals and ratios, plus the grand `TOTAL` row.
> 6. If the target is met, commit; otherwise revert and try a different change.
>
> Algorithmic choices are entirely yours — you may add or remove ideas freely as long as external behaviour is preserved and the benchmark numbers move in the right direction.
>
> Concrete milestones to aim for (these come from the reference Codex run on the same corpus, so they are achievable on commodity hardware; your numbers need not match exactly but should land in the same ballpark):
> - **Baseline** (end of Step 5): grand `TOTAL` around 220–240 s wall-clock over the eight families, `cobsat_over_minisat` around 18×.
> - **Mid milestone**: grand `TOTAL` under 140 s, `cobsat_over_minisat` under 11×, and no family above 3× its own previous time.
> - **Final milestone**: grand `TOTAL` under 120 s, `cobsat_over_minisat` under 10×, and on `uf100-430` / `uuf100-430` specifically, `cobsat_over_minisat` at or below ~9× (these are the headline families).
>
> At the end of each milestone, write (and commit) a short Markdown report capturing: the changes made, the before/after CSV, and any family that regressed (negative speedup) with a note on why.

---
