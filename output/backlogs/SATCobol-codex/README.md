# `SATCobol-codex` — Post-session analysis (PASS 1)

> Analyst-produced README (not the original repo's README — the repo has
> no top-level README). Companion file: [`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md)
> (agent-centric step-wise backlog).

## Project overview

A minimal **SAT solver written in COBOL**, built from scratch in a
single Codex CLI rollout on 2026-04-15 → 2026-04-16. The binary
`cobsat` ships three modes: a DIMACS parser (`--parse`), a model
checker (`--check-model`), and a DPLL solver with watched literals,
activity-based branching, restarts, clause learning, and
non-chronological backjumping. Validation covers edge-case DIMACS
fixtures, translated SAT4J regressions (128 file-based + 11 embedded
cases), and family benchmarks on SATLIB `uf/uuf` at 75 / 100 / 125 /
150 variables, including a MiniSat cross-check and a MiniSat
comparator. Status at final commit: `all tests passed`, MiniSat sweep
matched (100 % SAT/UNSAT agreement is not directly attested; 0
crosscheck failures are attested on the fixture subset).

This project is distinct from, but thematically related to, the older
`cobol-SAT` project (different codebase, different sessions).

## Evidence sources

- **Session rollout** (single, primary evidence):
  `/Users/mathieuacher/.codex/sessions/2026/04/15/rollout-2026-04-15T14-18-52-019d9114-7f7f-7a23-a04c-5c6cf0b9c61c.jsonl`
  (2 819 lines, Codex `0.119.0-alpha.11`, model `gpt-5.4`,
  personality `pragmatic`, reasoning effort `xhigh`, sandbox
  `workspace-write`, `cwd` = `/Users/mathieuacher/SANDBOX/SATCobol-codex`).
  Per-turn extract at
  `/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/turns/SATCobol-codex__Codex__019d9114-7f7f-7a23-a04c-5c6cf0b9c61c.jsonl`
  (620 lines — truncated; raw session is authoritative for post-line-620 events).
- **Git history** (9 commits on `main`):
  `6e49eb7 Add COBOL DIMACS parser and tests` →
  `59d47ff Add model checking and baseline DPLL solver` →
  `14555932 Refactor solver into modules` →
  `1ebd388f Optimize solver propagation and branching` →
  `ca9a67a7 Add Minisat cross-check script` →
  `bad44e0a Add translated SAT4J regression suite` →
  `c8cc713f Add restarts and activity-based branching` →
  `8c6ebcf1 Add Minisat comparison benchmark script` →
  `edb0942b Add clause learning and backjumping`. Evidence:
  `[R:.git/logs/HEAD]`.
- **Build/test logs** observed live inside the rollout (no re-runs
  performed by the analyst).

## Project constraints (PCI)

| ID    | Source                                                           | Type          | Summary                                                                                  |
|-------|------------------------------------------------------------------|---------------|------------------------------------------------------------------------------------------|
| PC-001| Codex base instructions (`session_meta.base_instructions.text`)   | tooling/style | Persist, parallelise tool calls, ASCII editing default, avoid destructive git commands.  |
| PC-002| Codex desktop developer instructions (`turn_context`)             | tooling       | Emit `::git-stage`/`::git-commit` directives; branch prefix `codex/`.                    |
| PC-003| `sandbox_policy: workspace-write`, `network_access: false`        | safety        | Writes restricted to project root; shell network restricted (requires escalation).       |
| PC-004| `cwd: /Users/mathieuacher/SANDBOX/SATCobol-codex` (env context)   | build         | All paths resolve relative to the project root; affects artefact placement.              |

No `AGENTS.md`, `CONTRIBUTING`, `.codex/config.toml`, or repo-level
README exist in `SATCobol-codex/`. Verified: `[R:/Users/mathieuacher/SANDBOX/SATCobol-codex/]`.

## Human user instruction index (UII)

Timestamps below are `…Z` from the rollout. Full prompts referenced by
line number in the raw session (same path as above).

| ID    | T               | Category            | Strength          | Target surface  | Quote / paraphrase (≤25 words)                                                                     | → BL     |
|-------|-----------------|---------------------|-------------------|-----------------|-----------------------------------------------------------------------------------------------------|----------|
| UI-001| 2026-04-15T12:19| FeatureRequest+Test | Explicit imperative| Code + Tests    | "Implement a robust DIMACS CNF parser in COBOL…`--parse file.cnf`…unit tests".                     | BL-001   |
| UI-002| 2026-04-15T12:33| Scenario/Hardening  | Suggestion         | Code            | "consider large DIMACS formula, coming from https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html".        | BL-002   |
| UI-003| 2026-04-15T12:35| Tooling (ops)       | Explicit imperative| Repo structure  | "create a git and commit".                                                                          | OP-001   |
| UI-004| 2026-04-15T12:37| FeatureRequest+Test | Explicit imperative| Code + Tests    | Add `--check-model file.cnf model.txt`; 0 iff satisfies; tests with SAT and failing models.         | BL-003   |
| UI-005| 2026-04-15T12:53| Scenario/Test       | Explicit imperative| Tests           | "in tests/ folder I have put two archives…uf75-325/uuf75-325…please check it's working".            | BL-004   |
| UI-006| 2026-04-15T13:00| Question            | Question           | Runtime         | "what about --check-model ?".                                                                        | BL-004+  |
| UI-007| 2026-04-15T13:05| FeatureRequest+Test | Explicit imperative| Code + Tests    | "Implement a baseline DPLL solver…s SATISFIABLE/v…0/UNSATISFIABLE…pigeonhole small/xor-like tests". | BL-006   |
| UI-008| 2026-04-15T14:03| Question            | Question           | Runtime         | "does it work with uf75-325 and uuf75-325?".                                                         | BL-007   |
| UI-009| 2026-04-15T14:07| Tooling (ops)       | Explicit imperative| Repo            | "please commit".                                                                                     | OP-002   |
| UI-010| 2026-04-15T14:09| RefactorRequest     | Explicit imperative| Code            | "Refactor solver code into modules (parser, cnf, propagate, search, io) without breaking tests".    | BL-008   |
| UI-011| 2026-04-15T14:32| FeatureRequest+Test | Explicit imperative| Code + Tests    | "Add watched literals…simple branching heuristic…perf test script on medium CNFs…avoid regressions".| BL-009   |
| UI-012| 2026-04-15T15:15| FeatureRequest      | Explicit imperative| Tooling         | "Add `scripts/crosscheck_minisat.sh`…compare SAT/UNSAT…store repro on mismatch, exit non-zero".     | BL-010   |
| UI-013| 2026-04-15T16:04| Scenario/Test       | Explicit imperative| Tests           | Test on uf/uuf 100, 125, 150 archives with "moderate / harder / strong challenge" ladder.            | BL-010b  |
| UI-014| 2026-04-15T16:20| FeatureRequest+Test | Explicit imperative| Tests           | "Demonstrate soundness by passing the test suite of SAT4J…convert the tests in COBOL first".        | BL-011   |
| UI-015| 2026-04-15T16:46| Tooling (ops)       | Explicit imperative| Repo            | "please commit".                                                                                     | OP-003   |
| UI-016| 2026-04-15T16:47| FeatureRequest      | Explicit imperative| Code            | "Implement restarts and better branching heuristic. Measure speedup if any and ensure no regressions"| BL-012  |
| UI-017| 2026-04-15T19:24| TestRequest         | Suggestion         | Tests           | "please run a more significant benchmark (complete set of instances perhaps)".                       | BL-013   |
| UI-018| 2026-04-16T04:13| TestRequest         | Explicit imperative| Tests           | "compare to minisat".                                                                                | BL-013   |
| UI-019| 2026-04-16T04:47| FeatureRequest      | Explicit imperative| Code            | "Implement advanced features of a SAT solver to try improving performance".                         | BL-014   |
| UI-020| 2026-04-16T05:12| DocRequest          | Explicit imperative| Docs            | "please commit, and before synthesize a table with new numbers against old numbers…to show the gains"| BL-014  |
| UI-021| 2026-04-16T05:17| FeatureRequest      | Explicit imperative| Code            | "let's try another round of performance improvement (without trading functional correctness)".       | BL-015   |
| UI-022| 2026-04-16T05:32| DocRequest          | Explicit imperative| Docs            | "write a report on benchmark results…comparison with minisat…document features step-wisely implemented".| BL-016 |

Out of 23 "user_message" events, 7 are one-word "commit"/"please
commit" (OP-scoped) and 1 is a Meta ack ("yes please" at 04:42:31).

## Prompt ledger (PL)

- **`PL-ROOT`** — `T:2026-04-15T12:19:03` — RAW (quoted ≤25 w):
  "Implement a robust DIMACS CNF parser in COBOL…`--parse file.cnf`…
  unit tests…empty lines, CRLF, trailing spaces, many spaces, comment
  lines between tokens." Linked: UI-001; BL-001.
- **`PL-ROOT` (CANONICAL replay)** — reproduce from an empty directory:
  > You are starting a fresh workspace at `./SATCobol-codex`.
  > Build a COBOL SAT solver step by step. First milestone: implement
  > a DIMACS CNF parser in free-format COBOL (`src/cobsat.cob` +
  > optional COPY books), compiled with `cobc -x -free` via a
  > `Makefile` and a `cobsat` wrapper script. The parser must accept
  > `c` comment lines, a `p cnf V C` header, arbitrary whitespace,
  > multi-line clauses, and `0` clause terminators. Expose a mode
  > `./cobsat --parse file.cnf` that prints a normalised
  > representation (number of vars, clauses, and flat list of
  > literals). Add a shell-based unit-test harness under `tests/`
  > covering: empty lines, CRLF line endings, trailing spaces,
  > runs of many spaces, and comment lines interleaved between
  > tokens. Commit to `main` once all tests pass.
- **`PL-001`** `T:2026-04-15T12:33` — "consider large DIMACS formula"
  (SATLIB). → UI-002 / BL-002.
- **`PL-002`** `T:2026-04-15T12:35` — "create a git and commit". →
  UI-003 / OP-001.
- **`PL-003`** `T:2026-04-15T12:37` — `--check-model file.cnf
  model.txt`. → UI-004 / BL-003.
- **`PL-004`** `T:2026-04-15T12:53` — Validate on uf75/uuf75 archives.
  → UI-005 / BL-004.
- **`PL-005`** `T:2026-04-15T13:00` — "what about --check-model ?". →
  UI-006.
- **`PL-006`** `T:2026-04-15T13:05` — Baseline DPLL solver. → UI-007 /
  BL-006.
- **`PL-007`** `T:2026-04-15T14:03` — "does it work with uf75-325 and
  uuf75-325?". → UI-008 / BL-007.
- **`PL-008`** `T:2026-04-15T14:07` — "please commit". → UI-009.
- **`PL-009`** `T:2026-04-15T14:09` — "Refactor solver code into
  modules (parser, cnf, propagate, search, io)". → UI-010 / BL-008.
- **`PL-010`** `T:2026-04-15T14:25` — "please commit".
- **`PL-011`** `T:2026-04-15T14:32` — Watched literals + branching
  heuristic + perf script. → UI-011 / BL-009.
- **`PL-012`** `T:2026-04-15T15:10` — "please commit".
- **`PL-013`** `T:2026-04-15T15:15` — `crosscheck_minisat.sh`. →
  UI-012 / BL-010.
- **`PL-014`** `T:2026-04-15T15:29` — "commit".
- **`PL-015`** `T:2026-04-15T16:04` — Test on uf/uuf 100/125/150
  archives. → UI-013 / BL-010b.
- **`PL-016`** `T:2026-04-15T16:20` — SAT4J regression translation. →
  UI-014 / BL-011.
- **`PL-017`** `T:2026-04-15T16:46` — "please commit".
- **`PL-018`** `T:2026-04-15T16:47` — Restarts + branching heuristic.
  → UI-016 / BL-012.
- **`PL-019`** `T:2026-04-15T19:23` — "commit".
- **`PL-020`** `T:2026-04-15T19:24` — "more significant benchmark". →
  UI-017.
- **`PL-021`** `T:2026-04-16T04:13` — "compare to minisat". → UI-018 /
  BL-013.
- **`PL-022`** `T:2026-04-16T04:42:03` — "please commit".
- **`PL-023`** `T:2026-04-16T04:42:31` — "yes please" (confirmation of
  agent's proposed commit split).
- **`PL-024`** `T:2026-04-16T04:47` — "advanced features of a SAT
  solver to try improving performance". → UI-019 / BL-014.
- **`PL-025`** `T:2026-04-16T05:12` — "commit, and before synthesize a
  table with new numbers against old numbers". → UI-020.
- **`PL-026`** `T:2026-04-16T05:17` — "another round of performance
  improvement". → UI-021 / BL-015.
- **`PL-027`** `T:2026-04-16T05:32` — "write a report on benchmark
  results…document…features step-wisely implemented". → UI-022 /
  BL-016.

## User-driven Feature Backlog (`BL-###`)

Implementation order, one row per backlog item. DoD = whether the
session produced verified evidence the item landed. "Repro" gives the
commit checkpoint or the session event id.

| ID     | Title                                                        | Type         | UI / PL        | DoD     | Commit         |
|--------|--------------------------------------------------------------|--------------|----------------|---------|----------------|
| BL-001 | DIMACS parser + `--parse` + edge-case unit tests             | Feature+Test | UI-001 / PL-ROOT| Yes    | `6e49eb7`      |
| BL-002 | Large DIMACS / SATLIB-scale hardening                        | Test         | UI-002 / PL-001 | Yes    | `6e49eb7` (same)|
| BL-003 | `--check-model` mode + model fixtures                        | Feature+Test | UI-004 / PL-003 | Yes    | `59d47ff`      |
| BL-004 | uf75-325 / uuf75-325 archive validation (parser)             | Test         | UI-005 / PL-004 | Yes    | `6e49eb7` (post-commit sweep)|
| BL-005 | SATLIB `%` end-marker tolerance (implied by BL-004)          | Bugfix       | UI-005 (implicit) | Yes  | `6e49eb7`      |
| BL-006 | Baseline DPLL solver + solve fixtures                        | Feature+Test | UI-007 / PL-006 | Yes    | `59d47ff`      |
| BL-007 | uf75/uuf75 solver soundness sweep                            | Test         | UI-008 / PL-007 | Yes    | `59d47ff` (post)|
| BL-008 | Modularise solver into 5 COPY books                          | Refactor     | UI-010 / PL-009 | Yes    | `14555932`     |
| BL-009 | Watched literals + occurrence branching + perf harness        | Feature+Test | UI-011 / PL-011 | Yes    | `1ebd388f`     |
| BL-010 | MiniSat cross-check script                                   | Tooling+Test | UI-012 / PL-013 | Yes    | `ca9a67a7`     |
| BL-010b| Extend validation to uf/uuf 100, 125, 150                    | Test         | UI-013 / PL-015 | Yes    | (pre-`bad44e0a`)|
| BL-011 | Translate SAT4J test suite to DIMACS + runner                | Test+Tooling | UI-014 / PL-016 | Yes    | `bad44e0a`     |
| BL-012 | Restarts + activity-based branching                          | Feature      | UI-016 / PL-018 | Yes    | `c8cc713f`     |
| BL-013 | MiniSat comparison benchmark across all families             | Test+Tooling | UI-017,018 / PL-020,021 | Yes | `8c6ebcf1`|
| BL-014 | Clause learning + backjumping + before/after table           | Feature+Docs | UI-019,020 / PL-024,025 | Partial | `edb0942b`|
| BL-015 | Second round of perf tuning                                  | Feature      | UI-021 / PL-026 | Partial | uncommitted   |
| BL-016 | Standalone benchmark/feature report (Markdown under `docs/`) | Documentation| UI-022 / PL-027 | No     | not delivered  |

**DoD notes**
- BL-014 "Partial": the clause-learning commit landed and the agent
  printed a CSV before/after table in-chat, but no persistent report
  file was produced in this BL.
- BL-015 "Partial": second-round tuning is reflected in on-disk
  `src/modules/*.cpy` line counts larger than those of `edb0942b`, and
  second-round numbers were printed in-chat, but the changes were
  never committed before the session ended.
- BL-016 "No": agent message at `2026-04-16T05:34:08` announces a
  Markdown file under `docs/`; `docs/` does not exist in the workspace
  and no `apply_patch` writing such a file is present in the tail of
  the rollout.

## Reproducibility Ops (non-feature, `OP-###`)

Listed because the user explicitly asked for them multiple times.

| ID    | UI / PL        | Action                                | Evidence                |
|-------|----------------|----------------------------------------|-------------------------|
| OP-001| UI-003 / PL-002| `git init` + initial commit            | commit `6e49eb7`        |
| OP-002| UI-009 / PL-008| commit after `--check-model` + DPLL    | commit `59d47ff`        |
| OP-003| UI-015 / PL-017| commit after SAT4J translation         | commit `bad44e0a`       |
| OP-004| PL-010         | commit after refactor                  | commit `14555932`       |
| OP-005| PL-012         | commit after watched literals + perf   | commit `1ebd388f`       |
| OP-006| PL-014         | commit after crosscheck script         | commit `ca9a67a7`       |
| OP-007| PL-019         | commit after restarts + branching      | commit `c8cc713f`       |
| OP-008| PL-022,023     | commit compare_minisat script          | commit `8c6ebcf1`       |
| OP-009| PL-025         | commit after clause learning           | commit `edb0942b`       |

(Second-round perf work in BL-015 and the BL-016 docs task were never
committed.)

## Replay package (per BL)

For each BL below: raw = UI/PL snippet; canonical = polished prompt
suitable for a clean repro. Preconditions common to all: GnuCOBOL
`cobc` in `$PATH`; optional `minisat` in `$PATH` for BL-010 and
BL-013; Bash + standard POSIX tools; `tar` for SATLIB archives.
Checkpoint = the commit it produces.

### BL-001 — parser + `--parse` + edge-case tests
- RAW: PL-ROOT (see above).
- CANONICAL: See `PL-ROOT` canonical block above. Validate with
  `make build && make test` — expected final line `all tests passed`.
- Checkpoint: `[G:commit 6e49eb7]`.

### BL-002 — SATLIB-scale parser hardening
- RAW: `consider large DIMACS formula, coming from https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html for instance`.
- CANONICAL: "Verify the DIMACS parser handles realistic SATLIB-scale
  inputs (≥ 10⁵ clauses) without regressions. Add a synthetic
  large-instance regression test to `tests/` and keep `make test`
  green."
- Checkpoint: in `6e49eb7` (same commit as BL-001).

### BL-003 — `--check-model`
- RAW: PL-003 (see above).
- CANONICAL: "Add a `--check-model file.cnf model.txt` mode to
  `cobsat`. Exit 0 iff the assignment satisfies every clause,
  non-zero otherwise. Add tests with: a satisfying model (any CNF),
  a failing model that violates the first clause, and a failing model
  that violates a later clause. Expose the mode from the CLI
  dispatcher alongside `--parse`."
- Checkpoint: `[G:commit 59d47ff]`.

### BL-004 — uf75/uuf75 archive validation
- RAW: PL-004 (see above).
- CANONICAL: "The archives `tests/uf75-325.tar.gz` and
  `tests/uuf75-325.tar.gz` each contain 100 DIMACS instances. Extract
  them into a temp dir and run `./cobsat --parse` on every file to
  confirm the parser handles real SATLIB files without errors.
  Capture any file that trips the parser and fix the parser rather
  than the fixtures."
- Checkpoint: agent evidence
  `[T:session 019d9114:evt@2026-04-15T12:54:53]` "The real SATLIB
  sweep passed".

### BL-005 — SATLIB end-marker tolerance
- RAW: implicit (surfaced while satisfying BL-004).
- CANONICAL: "When the declared number of clauses has been read,
  accept trailing `%` and trailing `0` markers and stop; reject any
  extra literal tokens. Add a `satlib-end-marker` regression fixture."
- Checkpoint: `[G:commit 6e49eb7]` (folded into initial commit).

### BL-006 — Baseline DPLL solver
- RAW: PL-006.
- CANONICAL: "Implement a DPLL solver in COBOL on top of the existing
  parser: unit propagation + chronological backtracking. Output
  `s SATISFIABLE` followed by one or more `v … 0` lines on SAT, or
  `s UNSATISFIABLE` on UNSAT. Add fixtures covering unit chains,
  XOR-like encodings, contradictions, and a small pigeonhole case.
  Ensure `--check-model` passes on every SAT model produced."
- Checkpoint: `[G:commit 59d47ff]`.

### BL-007 — uf75/uuf75 solver soundness
- RAW: PL-007.
- CANONICAL: "Run the DPLL solver over all 200 instances of
  `uf75-325` and `uuf75-325`. Confirm every `uf*` → SAT and every
  `uuf*` → UNSAT."
- Checkpoint: attested in session, not materialised as a test target.

### BL-008 — Modularise
- RAW: PL-009.
- CANONICAL: "Refactor `src/cobsat.cob` so that parsing, CNF
  representation, unit propagation, search, and I/O each live in their
  own COPY book under `src/modules/{parser,cnf,propagate,search,io}.cpy`.
  Update the `Makefile` to pass `-I src/modules`. All existing tests
  must still pass unchanged."
- Checkpoint: `[G:commit 14555932]`.

### BL-009 — Watched literals + branching + perf script
- RAW: PL-011.
- CANONICAL: "Introduce watched-literal unit propagation without
  changing external behaviour. Add a simple branching heuristic
  (literal with highest occurrence count). Add `tests/run-perf.sh`
  that times `./cobsat` on a small set of medium CNFs and fails on
  regressions exceeding a documented threshold."
- Checkpoint: `[G:commit 1ebd388f]`.

### BL-010 — MiniSat cross-check
- RAW: PL-013.
- CANONICAL: "Write `scripts/crosscheck_minisat.sh` that, given a
  `.cnf`, runs `./cobsat` and then `minisat` on the normalised DIMACS
  (emit via `./cobsat --parse`), compares SAT/UNSAT outcomes, and on
  mismatch stores a repro (cobsat.out, minisat.out/err, normalised.cnf)
  under `tests/crosscheck_failures/` and exits non-zero."
- Checkpoint: `[G:commit ca9a67a]`.

### BL-010b — Extend validation to uf/uuf 100/125/150
- RAW: PL-015.
- CANONICAL: "Place `uf100-430.tar.gz`, `uuf100-430.tar.gz`,
  `uf125-538.tar.gz`, `uuf125-538.tar.gz`, `uf150-645.tar.gz`,
  `uuf150-645.tar.gz` under `tests/` and verify the solver still
  terminates with the expected answer on a sampled subset."
- Checkpoint: session-only.

### BL-011 — SAT4J translation
- RAW: PL-016.
- CANONICAL: "From the SAT4J tree
  (`https://gitlab.ow2.org/sat4j/sat4j`), extract: (1) every file-based
  CNF referenced by `org.sat4j.minisat.TestsFonctionnels` and
  `org.sat4j.CLITest`; (2) the `aim/jnh/pigeons` cases from
  `AbstractM2Test`; (3) DIMACS regressions for BugSAT118/162/179/180/
  181/182/184. Place them under `tests/sat4j/{fixtures,embedded}` with
  a manifest TSV mapping each CNF to its SAT4J test id and expected
  outcome. Add `tests/run-sat4j-tests.sh` + `make sat4j-test`. Document
  what was **not** translated (pseudo-Boolean, cardinality, MUS,
  iteration)."
- Checkpoint: `[G:commit bad44e0a]`.

### BL-012 — Restarts + activity branching
- RAW: PL-018.
- CANONICAL: "Add restarts (Luby or a simple fixed-interval policy)
  and an activity-based (VSIDS-style) branching heuristic to the DPLL
  search. Confirm no regressions against `make test` and `make perf`."
- Checkpoint: `[G:commit c8cc713f]`.

### BL-013 — MiniSat comparison benchmark
- RAW: PL-020 + PL-021.
- CANONICAL: "Add `scripts/compare_minisat.sh` which, given one or
  more SATLIB-style tar.gz archives (defaulting to the four families
  under `tests/`), runs `./cobsat` and `minisat` on every instance and
  prints a per-family CSV with total/avg/max times and a
  `cobsat_over_minisat` ratio. Expose as `make compare-minisat`. Run
  it once over the full uf/uuf × {75,100,125,150} grid."
- Checkpoint: `[G:commit 8c6ebcf1]`.

### BL-014 — Clause learning + backjumping + before/after table
- RAW: PL-024 + PL-025.
- CANONICAL: "Add first-UIP clause learning and non-chronological
  backjumping to the solver. Re-run `scripts/compare_minisat.sh`.
  Produce a table (Markdown) that puts the before/after totals side by
  side across all eight families, including the `cobsat/minisat`
  ratio." (The table was produced in-chat; no file.)
- Checkpoint: `[G:commit edb0942b]`.
- In-chat numbers observed:

```
family,     base_t,  new_t, pct,  speedup, base_ratio, new_ratio, delta
uf75-325,   1.348,   1.266, +6.1%, 1.06x,   4.00,       3.44,      +0.56
uuf75-325,  2.434,   1.573, +35.3%,1.55x,   6.44,       4.09,      +2.35
uf100-430, 23.785,  21.078, +11.4%,1.13x,   6.06,       5.10,      +0.96
uuf100-430,72.561,  32.876, +54.7%,2.21x,  15.45,       7.02,      +8.43
uf125-538,  5.996,   5.990,  +0.1%,1.00x,  11.11,      11.11,      +0.00
uuf125-538,23.743,   9.947, +58.1%,2.39x,  33.89,      14.35,     +19.54
uf150-645, 15.965,  18.717, -17.2%,0.85x,  20.67,      24.19,      -3.52
uuf150-645,84.681,  43.541, +48.6%,1.94x,  60.31,      32.33,     +27.98
TOTAL,    230.513, 134.988, +41.4%,1.71x,  18.08,      10.45,      +7.63
```

### BL-015 — Second round of perf tuning
- RAW: PL-026.
- CANONICAL: "Attempt another round of performance improvements that
  preserve functional correctness. Re-run the benchmark comparator
  and report deltas." Second-round in-chat numbers (post-baseline):
  TOTAL 118.701 s (+48.5 % vs baseline, 1.94 ×), ratio 8.91.
  **No commit recorded.**

### BL-016 — Benchmark / feature report
- RAW: PL-027.
- CANONICAL: "Write a Markdown report (suggested path: `docs/
  benchmark-report.md`) with: methodology, per-stage feature changes
  with commit hashes, per-family before/after tables, and the final
  MiniSat comparison. Commit when complete." **Not delivered.**

## How to run / build / test

All commands below are evidence-based; no re-runs performed.

- `make build` → `cobc -x -free -I src/modules -o build/cobsat src/cobsat.cob`
- `make test` → `./tests/run-tests.sh` (expects `all tests passed`),
  then `./tests/run-sat4j-tests.sh`.
- `make sat4j-test` → subset runner.
- `make perf` → `./tests/run-perf.sh`.
- `make compare-minisat` → `./scripts/compare_minisat.sh` (SATLIB
  archives under `tests/`).
- `./cobsat --parse file.cnf` | `./cobsat --check-model file.cnf
  model.txt` | `./cobsat file.cnf`.

Observed last attested run: `make test` → `all tests passed` at
`[T:session 019d9114:evt@2026-04-15T15:16:56]` (post-`ca9a67a`).

## Repo quantification (A5)

Exclusions: `.git/`, `build/`, `.DS_Store`, `.gitkeep`, archive tarballs.

### Files and LOC (only tracked source / scripts / tests)

| Path                                           | Lines | Kind              |
|------------------------------------------------|-------|-------------------|
| `src/cobsat.cob`                               | 263   | production (COBOL main) |
| `src/modules/cnf.cpy`                          | 301   | production (COBOL copybook) |
| `src/modules/io.cpy`                           | 105   | production (COBOL copybook) |
| `src/modules/parser.cpy`                       | 470   | production (COBOL copybook) |
| `src/modules/propagate.cpy`                    | 194   | production (COBOL copybook) |
| `src/modules/search.cpy`                       | 378   | production (COBOL copybook) |
| `scripts/compare_minisat.sh`                   | 212   | tooling (shell)   |
| `scripts/crosscheck_minisat.sh`                | 102   | tooling (shell)   |
| `tests/run-tests.sh`                           | 210   | tests (shell)     |
| `tests/run-perf.sh`                            | 144   | tests (shell)     |
| `tests/run-sat4j-tests.sh`                     | 129   | tests (shell)     |
| `Makefile`                                     | 28    | build (make)      |
| `cobsat` (wrapper)                             | 15    | tooling (shell)   |
| `.gitignore`                                   | 4     | config            |
| `tests/sat4j/README.md`                        | 25    | docs (subdir)     |

### Aggregate

| Kind               | Files | LOC   |
|--------------------|-------|-------|
| COBOL production   | 6     | 1 711 |
| Shell tooling      | 3     | 329   |
| Shell tests        | 3     | 483   |
| Build (Makefile)   | 1     | 28    |
| Config/gitignore   | 1     | 4     |
| Docs (sat4j only)  | 1     | 25    |
| **Total (tracked code)** | **15** | **2 580** |

### Data / examples (not counted as code)

- 128 DIMACS fixtures under `tests/sat4j/fixtures/{aim,jnh,pigeons}/`
  plus `aim-50-{yes,no}-ok.cnf` and `bug001.cnf`.
- 11 embedded `bugsatNNN*.cnf` fixtures under `tests/sat4j/embedded/`.
- 2 TSV manifests (`manifest-file-based.tsv`, `manifest-embedded.tsv`).
- 8 SATLIB archives: `uf{75,100,125,150}-*.tar.gz`,
  `uuf{75,100,125,150}-*.tar.gz` (user-supplied, untracked).
- 11 parser edge-case fixtures under `tests/fixtures/*.cnf` + 9
  matching `tests/expected/*.out/.err` + 4 `tests/models/*.model`.

### Directories

`.`, `src/`, `src/modules/`, `scripts/`, `tests/`,
`tests/expected/`, `tests/fixtures/`, `tests/models/`,
`tests/crosscheck_failures/`, `tests/sat4j/`,
`tests/sat4j/fixtures/{aim,jnh,pigeons}`,
`tests/sat4j/embedded/`. Total tracked directories: 13.

### Entry points

- Program entrypoint: `src/cobsat.cob` → binary `build/cobsat` (via
  `cobsat` wrapper).
- Test entrypoints: `tests/run-tests.sh`, `tests/run-sat4j-tests.sh`,
  `tests/run-perf.sh`.
- Build entrypoint: `Makefile`.

Cite: `[S:stats_run_1 = analyst Grep counts + find listings, per
tool invocations in this session]`.

## Agent-centric backlog

See [`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md) for the
step-wise `SB-001…SB-033` list (what the agent actually did, labelled
User-driven / Agent-initiated / Required prerequisite).

## Limitations / missing evidence

- The rollout was truncated mid-final-turn; BL-016 was announced but
  never materialised. The repo has no top-level `README.md`, so users
  cloning the project see only directory structure.
- BL-015 changes exist on disk but are **uncommitted** — replay from a
  `git clone` will land on `edb0942b` and miss the second-round perf
  tuning; the in-chat "TOTAL 118.701 s / 1.94 ×" numbers are the only
  evidence of that work and are not independently re-verifiable
  without a re-run.
- Multiple reasoning events in the Codex rollout are stored as
  encrypted blobs (`encrypted_content` in `reasoning` response items);
  the analyst could only consult the plaintext `agent_message` payloads.
- No `AGENTS.md` or `.codex/config.toml` means the Codex base-instruction
  personality (`pragmatic`, `xhigh` reasoning) is the only inherited
  policy; it is documented as PC-001..PC-004 rather than as repo
  artefacts.
- The analyst did not re-run `make test`, `make compare-minisat`, or
  the SAT4J runner; all "pass" claims cite the session's own
  `tool_output` events.

## Repro Ops (non-feature)

See the `OP-###` table above. The user requested a commit per logical
milestone (9 commits total, all on `main`, linear history). No tags,
no branches, no remote recorded.

---

**PASS 1 COMPLETE.**

For PASS 2 strategy/outcome/interaction analysis, see
[`REPORT.md`](REPORT.md) and the machine-readable
[`appendix.json`](appendix.json).
