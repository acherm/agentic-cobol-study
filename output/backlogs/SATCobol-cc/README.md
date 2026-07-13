# `SATCobol-cc` — Post-session analysis (PASS 1)

> Analyst-produced README (not the original repo's README — the repo has
> no top-level README). Companion file:
> [`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md) (agent-centric,
> step-wise backlog).

## Project overview

A **SAT solver written in COBOL**, built from scratch in a single Claude
Code session on 2026-04-15 → 2026-04-16. The binary `cobsat` ships
three modes: a DIMACS parser (`--parse`), a model checker
(`--check-model`), and a DPLL-derived solver (`--solve`) that evolved
from baseline DPLL → two-watched literals + occurrence branching →
phase saving + VSIDS-lite + JW + Luby restarts. Validation covers
edge-case DIMACS fixtures (32 runner cases), translated SAT4J fixtures
(113 instances across `aim/ii/jnh/pigeons` + misc), 8 SATLIB archives
(`uf/uuf` × {75, 100, 125, 150}), a MiniSat cross-checker, and a
2 400-instance comparison sweep vs MiniSat (overall 1.9× slower).

This project is the **Claude Code replica** of the Codex-built
`SATCobol-codex`. The two projects received the same starter prompt and
a broadly similar instruction stream. Points of divergence are captured
in the final "Cross-agent note" section.

## Evidence sources

- **Session rollout** (single, primary evidence):
  `/Users/mathieuacher/.claude/projects/-Users-mathieuacher-SANDBOX-SATCobol-cc/9f10dfb5-e448-463b-bffe-21fa2006c9ae.jsonl`
  (1 122 events, Claude Code `2.1.109`, model `claude-opus-4-6`,
  `cwd = /Users/mathieuacher/SANDBOX/SATCobol-cc`).
  Per-turn extract at
  `/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/turns/SATCobol-cc__Claude Code__9f10dfb5-e448-463b-bffe-21fa2006c9ae.jsonl`
  (316 lines — truncated; raw session is authoritative).
- **Git history** (9 commits on default branch, plus two `reset` no-ops):
  `049f4b5 Initial COBOL DIMACS CNF parser with --parse mode` →
  `3fc5cdd Add --check-model mode for evaluating CNF assignments` →
  `88e8e99 Treat SATLIB '%' line as end-of-data; ship uf75/uuf75 benchmarks` →
  `bdea674 Add baseline DPLL solver (--solve) with unit propagation` →
  `b2d8324 Refactor cobsat into per-module copybooks (io, parser, cnf, propagate, search)` →
  `de35d40 Two-watched literals + occurrence branching; perf script; larger benchmarks` →
  `a121b45 Add scripts/crosscheck_minisat.sh to cross-verify against minisat` →
  `57de05d Pass SAT4J's acceptance test suite` →
  `c3b2a7c Phase saving, VSIDS-lite, JW branching, Luby restarts`.
  Evidence: `[R:.git/logs/HEAD]`.
- **Build/test logs** observed live inside the rollout (no re-runs
  performed by the analyst).

## Project constraints (PCI)

| ID    | Source                                                | Type         | Summary                                                                                      |
|-------|-------------------------------------------------------|--------------|----------------------------------------------------------------------------------------------|
| PC-001| `.claude/settings.local.json` (allow-list)            | tooling/perms | `git init *`, `git add *`, Read access to `/private/tmp/sat4j/**` test sources.             |
| PC-002| Claude Code default base-instructions (implicit)       | tooling/style | Tool-use with Write/Edit/Read/Bash; no explicit repo policy echoed in events.               |
| PC-003| `.gitignore`                                           | build        | Ignores `cobsat`, `build/`, `*.o`, `*.so`, `*.dylib`, `tests/bench/`, `tests/crosscheck_failures/`, `.DS_Store`. |

No `AGENTS.md`, `CONTRIBUTING`, `CLAUDE.md`, or repo-level `README.md`
exist in `SATCobol-cc/`. Verified: `[R:/Users/mathieuacher/SANDBOX/SATCobol-cc/]`.

## Human user instruction index (UII)

Timestamps in UTC from the rollout. 21 distinct human prompts (after
filtering out `<task-notification>` auto-messages and the two
duplicated `UF75 archive` pastes that Claude Code emitted at
`14:05:27` / `14:05:36` — 1 s apart, identical text).

| ID     | T                         | Category               | Strength             | Target surface | Quote / paraphrase (≤25 words)                                                                          | → BL    |
|--------|---------------------------|------------------------|----------------------|----------------|---------------------------------------------------------------------------------------------------------|---------|
| UI-001 | 2026-04-15T12:20:04       | FeatureRequest+Test    | Explicit imperative  | Code + Tests   | "Implement a robust DIMACS CNF parser in COBOL…`--parse file.cnf`…unit tests (empty, CRLF, trailing, many spaces, comments between tokens)". | BL-001 |
| UI-002 | 2026-04-15T12:53:32       | Tooling (ops)          | Explicit imperative  | Repo structure | "create a git and commit".                                                                              | OP-001 |
| UI-003 | 2026-04-15T12:54:56       | FeatureRequest+Test    | Explicit imperative  | Code + Tests   | "`./cobsat --check-model file.cnf model.txt` returns 0 iff model satisfies…tests with known SAT / fail models". | BL-002 |
| UI-004 | 2026-04-15T14:05:27 (×2)  | Scenario/Test          | Explicit imperative  | Tests          | "in tests/ I have put uf75-325/uuf75-325 archives…please check it's working".                          | BL-003 |
| UI-005 | 2026-04-15T14:26:18       | FeatureRequest+Test    | Explicit imperative  | Code + Tests   | "Implement a baseline DPLL solver…`s SATISFIABLE`/`v … 0`/`s UNSATISFIABLE`…pigeonhole/xor-like tests". | BL-004 |
| UI-006 | 2026-04-15T15:03:35       | Meta/process           | Meta                 | Runtime        | "retry/continue".                                                                                       | — (ack)|
| UI-007 | 2026-04-15T15:31:13       | Question               | Question             | Runtime        | "does it work with uf75-325 and uuf75-325?".                                                            | BL-005 |
| UI-008 | 2026-04-15T15:41:36       | Tooling (ops)          | Explicit imperative  | Repo           | "please commit".                                                                                        | OP-005 |
| UI-009 | 2026-04-15T15:41:50       | RefactorRequest        | Explicit imperative  | Code           | "Refactor solver code into modules (parser, cnf, propagate, search, io) without breaking tests".        | BL-006 |
| UI-010 | 2026-04-15T15:57:37       | FeatureRequest+Test    | Explicit imperative  | Code + Tests   | "Add watched literals…simple branching heuristic (highest occurrence)…perf test script…avoid regressions". | BL-007 |
| UI-011 | 2026-04-15T19:10:15       | FeatureRequest         | Explicit imperative  | Tooling        | "Add `scripts/crosscheck_minisat.sh`…compare SAT/UNSAT…store repro on mismatch, exit non-zero".         | BL-008 |
| UI-012 | 2026-04-16T04:45:16       | Scenario/Test          | Explicit imperative  | Tests          | Test on uf/uuf 100, 125, 150 archives ("moderate / harder / strong challenge" ladder).                 | BL-009 |
| UI-013 | 2026-04-16T05:10:51       | FeatureRequest+Test    | Explicit imperative  | Tests          | "Demonstrate soundness by passing SAT4J's test suite…convert tests in COBOL first…pass the tests".      | BL-010 |
| UI-014 | 2026-04-16T07:32:32       | Question               | Question             | Runtime        | "status?".                                                                                              | BL-010 |
| UI-015 | 2026-04-16T08:55:59       | FeatureRequest         | Explicit imperative  | Code           | "Implement restarts and better branching heuristic. Measure speedup if any and ensure no regressions".  | BL-011 |
| UI-016a| 2026-04-16T10:10:27       | TestRequest            | Explicit imperative  | Tests          | "please run a more significant benchmark (complete set of instances)…uf/uuf 100/125/150".               | BL-012 |
| UI-016b| 2026-04-16T13:09:46       | TestRequest            | Explicit imperative  | Tests          | "compare to minisat".                                                                                   | BL-012 |
| UI-017 | 2026-04-16T13:25:04       | FeatureRequest         | Explicit imperative  | Code           | "Implement advanced features of a SAT solver to try improving performance (without trading correctness)". | BL-013 |

Commit-only prompts (UI-002, UI-008, and two further `commit`/`please
commit` at `16:48:51` and `19:10:15`-adjacent) fold into `OP-###`.

## Prompt ledger (PL)

- **`PL-ROOT`** — `T:2026-04-15T12:20:04` — RAW (≤25 w): "Implement a
  robust DIMACS CNF parser in COBOL: c comments, `p cnf V C`, arbitrary
  whitespace, multi-line clauses, 0 terminators. Add `--parse` mode and
  edge-case unit tests." Linked: UI-001; BL-001.
- **`PL-ROOT` (CANONICAL replay)**:
  > You are starting a fresh workspace at `./SATCobol-cc`. Build a
  > COBOL SAT solver incrementally. First milestone: implement a DIMACS
  > CNF parser in free-format COBOL (`src/cobsat.cob` + per-module
  > copybooks under `src/copy/`), compiled with `cobc -x -Wall -O2
  > -I src/copy` via a `Makefile`. The parser must accept `c` / `%`
  > comments, a `p cnf V C` header, arbitrary whitespace, multi-line
  > clauses, and `0` clause terminators. Expose `./cobsat --parse
  > file.cnf` that prints a normalised representation (vars, clauses,
  > flat list of literals). Add a shell-based test harness
  > `tests/run_tests.sh` with fixtures `simple`, `empty_lines`, `crlf`,
  > `many_spaces`, `trailing_spaces`, `multiline`, `interleaved_comments`,
  > `comment_between_tokens`. Each fixture has an expected golden
  > string. Commit once tests are green.
- **`PL-001`** `T:2026-04-15T12:53:32` — "create a git and commit". →
  UI-002 / OP-001.
- **`PL-002`** `T:2026-04-15T12:54:56` — `--check-model file.cnf
  model.txt`. → UI-003 / BL-002.
- **`PL-003`** `T:2026-04-15T14:05:27` — Validate on uf75/uuf75
  archives. → UI-004 / BL-003.
- **`PL-004`** `T:2026-04-15T14:26:18` — Baseline DPLL solver. → UI-005
  / BL-004.
- **`PL-005`** `T:2026-04-15T15:03:35` — "retry/continue" (meta).
- **`PL-006`** `T:2026-04-15T15:27:36` — "please commit".
- **`PL-007`** `T:2026-04-15T15:31:13` — "does it work with uf75-325
  and uuf75-325?" → UI-007 / BL-005.
- **`PL-008`** `T:2026-04-15T15:41:36` — "please commit".
- **`PL-009`** `T:2026-04-15T15:41:50` — "Refactor solver code into
  modules (parser, cnf, propagate, search, io)". → UI-009 / BL-006.
- **`PL-010`** `T:2026-04-15T15:57:37` — Watched literals + branching
  heuristic + perf script. → UI-010 / BL-007.
- **`PL-011`** `T:2026-04-15T16:48:51` — "commit".
- **`PL-012`** `T:2026-04-15T19:10:15` — `scripts/crosscheck_minisat.sh`.
  → UI-011 / BL-008.
- **`PL-013`** `T:2026-04-16T04:45:16` — Extend benchmarks to uf/uuf
  {100,125,150}. → UI-012 / BL-009.
- **`PL-014`** `T:2026-04-16T05:10:51` — SAT4J regression translation.
  → UI-013 / BL-010.
- **`PL-015`** `T:2026-04-16T07:32:32` — "status?".
- **`PL-016`** `T:2026-04-16T08:55:59` — Restarts + better branching.
  → UI-015 / BL-011.
- **`PL-017`** `T:2026-04-16T10:10:27` — "more significant benchmark".
  → UI-016a / BL-012.
- **`PL-018`** `T:2026-04-16T13:09:46` — "compare to minisat". →
  UI-016b / BL-012.
- **`PL-019`** `T:2026-04-16T13:25:04` — "advanced features of a SAT
  solver to try improving performance". → UI-017 / BL-013.

## User-driven Feature Backlog (`BL-###`)

Implementation order, one row per backlog item. DoD = whether the
session produced verified evidence the item landed. "Repro" gives the
commit checkpoint or the session event id.

| ID     | Title                                                              | Type            | UI / PL               | DoD     | Commit           |
|--------|--------------------------------------------------------------------|-----------------|-----------------------|---------|------------------|
| BL-001 | DIMACS parser + `--parse` + edge-case unit tests                   | Feature+Test    | UI-001 / PL-ROOT      | Yes     | `049f4b5`        |
| BL-002 | `--check-model` mode + model fixtures                              | Feature+Test    | UI-003 / PL-002       | Yes     | `3fc5cdd`        |
| BL-003 | uf75-325 / uuf75-325 parser validation (+ SATLIB `%` fix)          | Test+Bugfix     | UI-004 / PL-003       | Yes     | `88e8e99`        |
| BL-004 | Baseline DPLL solver (`--solve`) + solve fixtures                  | Feature+Test    | UI-005 / PL-004       | Yes     | `bdea674`        |
| BL-005 | uf75/uuf75 200-instance solver soundness                           | Test            | UI-007 / PL-007       | Yes     | `bdea674` (post) |
| BL-006 | Refactor into 12 copybooks (`io / parser / cnf / propagate / search` × data+logic) | Refactor | UI-009 / PL-009 | Yes     | `b2d8324`        |
| BL-007 | Watched literals + occurrence branching + `tests/perf.sh`          | Feature+Test    | UI-010 / PL-010       | Yes     | `de35d40`        |
| BL-008 | MiniSat cross-check script (`scripts/crosscheck_minisat.sh`)       | Tooling+Test    | UI-011 / PL-012       | Yes     | `a121b45`        |
| BL-009 | Extend validation to uf/uuf {100, 125, 150} (2 400-instance sweep) | Test            | UI-012 / PL-013       | Yes     | (post-`a121b45`) |
| BL-010 | SAT4J acceptance suite: translate Java tests to DIMACS + runner    | Test+Tooling    | UI-013,014 / PL-014   | Yes     | `57de05d`        |
| BL-011 | Phase saving + VSIDS-lite + JW + Luby restarts                     | Feature         | UI-015 / PL-016       | Yes     | `c3b2a7c`        |
| BL-012 | MiniSat comparison on all 2 400 instances (1.9× overall)           | Test            | UI-016a,b / PL-017,018| Yes     | (post-`c3b2a7c`) |
| BL-013 | CDCL (first-UIP + clause learning + non-chrono backjump)           | Feature         | UI-017 / PL-019       | Partial | uncommitted      |

**DoD notes**
- BL-005 "Yes (session-only)": agent attests 100/100 SAT on uf75-325
  and 100/100 UNSAT on uuf75-325 at `[T:2026-04-15T15:35-41]`; no
  `make`-exposed target.
- BL-009 "Yes (session-only)": 2 400/2 400 correct (SB-028); attested
  at `[T:2026-04-16T10:22:24]` but no tarball/out file is checked in.
- BL-012 "Yes (session-only)": cobsat 101.6 s / minisat 52.6 s / ratio
  1.9× across 2 400 instances attested at `[T:2026-04-16T13:16:16]`;
  no CSV committed.
- BL-013 "Partial": CDCL code is present on disk in
  `src/copy/{propagate,search,cnf,cnf-data,propagate-data}.cpy`
  (confirmed by analyst grep for `first-UIP`, `ANALYZE-CONFLICT`,
  `BACKJUMP-TO-LEVEL`, `ADD-LEARNT-CLAUSE`, `WS-LEARNT`). Agent claims
  "33/33 unit tests pass + smokes correct" at
  `[T:2026-04-16T13:43:46]`. **No commit**; final CDCL benchmark
  launched at 13:48 and the session log ends 4 s later. No attested
  post-CDCL benchmark numbers.

## Reproducibility Ops (non-feature, `OP-###`)

The user asked for a commit three times (`create a git and commit`,
`please commit`×N). Commit cadence: 9 commits, one per major milestone,
plus a few "commit" prompts that folded directly into the next feature
commit.

| ID    | UI / PL           | Action                                         | Evidence    |
|-------|-------------------|------------------------------------------------|-------------|
| OP-001| UI-002 / PL-001   | `git init` + initial commit                    | `049f4b5`   |
| OP-002| PL-006            | commit after `--check-model`                   | `3fc5cdd`   |
| OP-003| (implicit)        | commit after `%` fix + uf75 archives           | `88e8e99`   |
| OP-004| PL-008            | commit after baseline DPLL                     | `bdea674`   |
| OP-005| (implicit)        | commit after refactor                          | `b2d8324`   |
| OP-006| PL-011            | commit after watched literals + perf           | `de35d40`   |
| OP-007| (implicit)        | commit after crosscheck script                 | `a121b45`   |
| OP-008| (implicit)        | commit after SAT4J suite                       | `57de05d`   |
| OP-009| (implicit)        | commit after phase/VSIDS/JW/Luby               | `c3b2a7c`   |

BL-012's benchmark numbers and BL-013's CDCL code were never committed.

## Replay package (per BL)

For each BL below: raw = UI/PL snippet; canonical = polished prompt
suitable for a clean repro. Preconditions common to all: GnuCOBOL
`cobc` in `$PATH`; optional `minisat` in `$PATH` for BL-008 and BL-012;
Bash + standard POSIX tools + `python3` (for `tests/perf.sh` timing);
`tar` for SATLIB archives.

### BL-001 — parser + `--parse` + edge-case tests
- RAW: PL-ROOT (see above).
- CANONICAL: See `PL-ROOT` canonical block above. Validate with
  `make && make test`.
- Checkpoint: `[G:commit 049f4b5]`.

### BL-002 — `--check-model`
- RAW: PL-002.
- CANONICAL: "Add a `--check-model file.cnf model.txt` mode to
  `./cobsat`. Accept DIMACS solution-style `v`-lines, bare integers,
  and `c`/`s` comment lines. Exit 0 iff the assignment satisfies every
  clause; otherwise print `UNSAT clause N: <clause>` to stderr and exit
  non-zero. Under `tests/fixtures/`, add paired `.sat.model` and
  `.unsat.model` files for every existing parser fixture."
- Checkpoint: `[G:commit 3fc5cdd]`.

### BL-003 — uf75/uuf75 parser validation + `%` fix
- RAW: PL-003.
- CANONICAL: "The archives `tests/uf75-325.tar.gz` and
  `tests/uuf75-325.tar.gz` each contain 100 DIMACS instances. Extract
  them, run `./cobsat --parse` on every file. SATLIB files end with
  `%\n0\n`; treat `%` as end-of-data rather than reading the trailing
  `0` as a new clause."
- Checkpoint: `[G:commit 88e8e99]`.

### BL-004 — baseline DPLL `--solve`
- RAW: PL-004.
- CANONICAL: "Implement a DPLL solver on top of the existing parser:
  unit propagation + chronological backtracking, iterative (explicit
  `(var, kind)` trail, not COBOL recursion). Output `s SATISFIABLE`
  then one or more `v … 0` lines on SAT, or `s UNSATISFIABLE` on UNSAT.
  Add fixtures `unit_chain`, `contradiction`, `xor3`, `xor3_unsat`,
  `php2_3`, `php3_2`, `php4_3`. The runner must re-feed every SAT model
  back through `--check-model` to self-verify."
- Checkpoint: `[G:commit bdea674]`.

### BL-005 — uf75/uuf75 solver soundness
- RAW: PL-007 ("does it work with uf75-325 and uuf75-325?").
- CANONICAL: "Run `./cobsat --solve` over all 200 instances of
  `uf75-325` and `uuf75-325`. Confirm every `uf*` → SAT and every
  `uuf*` → UNSAT, and verify each SAT model via `--check-model`."
- Checkpoint: session-only; attested at
  `[T:2026-04-15T15:35-41]` inside commit `bdea674`.

### BL-006 — Modularise into copybooks
- RAW: PL-009.
- CANONICAL: "Refactor the single `src/cobsat.cob` (~920 LOC) into a
  thin main file (IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE
  dispatch, `COPY` directives) plus 12 copybooks under `src/copy/`:
  `io-files.cpy`, `io-fd.cpy`, `io-data.cpy`, `io.cpy`,
  `parser-data.cpy`, `parser.cpy`, `cnf-data.cpy`, `cnf.cpy`,
  `propagate-data.cpy`, `propagate.cpy`, `search-data.cpy`,
  `search.cpy`. Update `Makefile` to pass `-I src/copy`. All existing
  tests must still pass."
- Checkpoint: `[G:commit b2d8324]`.

### BL-007 — Watched literals + branching + perf
- RAW: PL-010.
- CANONICAL: "Introduce two-watched-literals unit propagation without
  changing external behaviour. Add a branching heuristic that picks the
  unassigned variable with highest occurrence count. Add
  `tests/perf.sh` that times `./cobsat --solve` on uf75/uuf75 (and
  optionally uf150/uuf150) and prints per-set total / mean / max wall
  time. Also commit the larger SATLIB archives
  (uf{100,125,150}-*.tar.gz and matching uuf*)."
- Checkpoint: `[G:commit de35d40]`.

### BL-008 — MiniSat crosscheck
- RAW: PL-012.
- CANONICAL: "Write `scripts/crosscheck_minisat.sh` that, for each
  CNF, runs `./cobsat --solve` and `minisat`, compares SAT/UNSAT, and
  on SAT also validates cobsat's model via `--check-model`. Strip
  SATLIB's `%` trailer before invoking minisat. On mismatch or
  solver error, store `input.cnf`, `cobsat.out`, `minisat.out`,
  `minisat.stdout`, and a `STATUS` file under
  `tests/crosscheck_failures/<basename>/` and exit 1."
- Checkpoint: `[G:commit a121b45]`.

### BL-009 — Extended benchmark sweep
- RAW: PL-013.
- CANONICAL: "Run `./cobsat --solve` across all 2 400 instances of
  uf/uuf × {100, 125, 150}. Assert every `uf*` → SAT and every `uuf*`
  → UNSAT, and record per-family totals."
- Checkpoint: session-only; attested 2 400/2 400 at
  `[T:2026-04-16T10:22:24]`.

### BL-010 — SAT4J translation
- RAW: PL-014.
- CANONICAL: "Fetch SAT4J (https://gitlab.ow2.org/sat4j/sat4j) and
  extract: (1) `AbstractM2Test.java` acceptance cases (aim / ii / jnh
  / pigeons), (2) `TestsFonctionnels.java` file-based fixtures
  (aim-50-*-ok, bug001, test3, testcomments), (3) `BugSAT175.java`
  fixtures. Place them under `tests/sat4j/{aim,ii,jnh,pigeons,…}/*.cnf`
  (113 files). Add `tests/sat4j/expected.tbl` listing the SAT/UNSAT
  verdict per file, and `tests/run_sat4j_tests.sh` that iterates the
  table with a 30-s per-case timeout and classifies pass / fail /
  skip(timeout). Also loosen the parser to accept a missing trailing
  `0` (SAT4J's Java reader is lenient about it)."
- Checkpoint: `[G:commit 57de05d]`. Attested: 94 pass / 0 fail / 19
  skip.

### BL-011 — Phase saving + VSIDS-lite + JW + Luby restarts
- RAW: PL-016.
- CANONICAL: "Add phase saving (`WS-PHASE(v)` reused across backtracks
  / restarts), VSIDS-lite activity scoring (`WS-ACT(v)`, bumped on
  every conflict, periodic decay), Jeroslow-Wang initial activity
  seeding (each clause of length k contributes 2^(10-k) to its
  literals), and Luby restarts with a large base (so restarts only
  fire on pathological instances — without clause learning, aggressive
  restarts lose progress). Re-run `tests/run_sat4j_tests.sh` and
  confirm no regressions."
- Checkpoint: `[G:commit c3b2a7c]`. Attested: SAT4J 94 → 111 pass (19 →
  2 skip); uf150 −13 %, uuf150 −30 % runtime; overall +9 % total
  because of regressions on easy sets.

### BL-012 — MiniSat comparison benchmark
- RAW: PL-017 + PL-018.
- CANONICAL: "Run `./cobsat --solve` and `minisat` on every instance of
  all eight SATLIB families (uf/uuf × {100, 125, 150} — the four
  75-var archives having already been validated). Print per-family
  totals for cobsat and minisat plus a `cobsat_over_minisat` ratio."
  Attested numbers (session `[T:2026-04-16T13:16:16]`):
  `total 2400 instances, cobsat 101.6 s, minisat 52.6 s, ratio 1.9×`.
- Checkpoint: session-only; no CSV committed.

### BL-013 — CDCL (advanced features)
- RAW: PL-019.
- CANONICAL: "Implement first-UIP conflict analysis, non-chronological
  backjumping, and a learnt-clause database on top of the existing
  two-watched-literals + VSIDS engine. Extend `cnf-data.cpy` to size
  the clause DB for originals + learnts; add
  `WS-LEARNT` scratch buffer, `WS-LEVEL(v)`, `WS-REASON(v)` to
  `propagate-data.cpy`; rewrite `search.cpy` as a CDCL main loop
  (PROPAGATE → ANALYZE-CONFLICT → BACKJUMP-TO-LEVEL → ADD-LEARNT-CLAUSE
  → PROPAGATE-LIT). Rerun all tests and both benchmark sweeps."
- Checkpoint: **uncommitted** on-disk at last-event
  `[T:2026-04-16T13:48:13]`. CDCL code present in
  `src/copy/{search,propagate,cnf,cnf-data,propagate-data}.cpy`;
  `33/33 unit tests` claimed; no final benchmark attested.

## How to run / build / test

All commands below are evidence-based; no re-runs performed.

- `make` → `cobc -x -Wall -O2 -I src/copy -o cobsat src/cobsat.cob`
  (binary lands at repo root, not under `build/`; `build/` is in
  `.gitignore` but not used by `Makefile`).
- `make test` → `tests/run_tests.sh` (32 cases across parse /
  check-model / solve).
- `tests/perf.sh [N] [big|small-only]` → perf tripwire on uf75/uuf75
  (± uf150/uuf150).
- `tests/run_sat4j_tests.sh` → 113 SAT4J cases with 30-s timeout.
- `scripts/crosscheck_minisat.sh FILE.cnf…` or
  `scripts/crosscheck_minisat.sh DIR` → cobsat vs minisat.
- `./cobsat --parse file.cnf` | `./cobsat --check-model file.cnf model.txt`
  | `./cobsat --solve file.cnf`.

Observed last attested test run: `33/33 unit tests pass + smokes
correct` at `[T:2026-04-16T13:43:46]` after the (uncommitted) CDCL
edit. Note: the "33" figure corresponds to runner cases after the CDCL
refactor added a handful of new cases to `run_tests.sh`, up from ~27 at
`c3b2a7c`.

## Repo quantification (A5)

Exclusions: `.git/`, `build/`, `.DS_Store`, `.gitkeep`, archive tarballs,
`tests/bench/` (extracted benchmarks — gitignored),
`tests/crosscheck_failures/` (empty, gitignored).

### Files and LOC (tracked source / scripts / tests)

| Path                                           | Lines | Kind                        |
|------------------------------------------------|-------|-----------------------------|
| `src/cobsat.cob`                               | 83    | production (COBOL dispatch) |
| `src/copy/parser.cpy`                          | 404   | production (COBOL copybook) |
| `src/copy/propagate.cpy`                       | 419   | production (COBOL copybook) |
| `src/copy/cnf.cpy`                             | 189   | production (COBOL copybook) |
| `src/copy/search.cpy`                          | 139   | production (COBOL copybook) |
| `src/copy/io.cpy`                              | 152   | production (COBOL copybook) |
| `src/copy/cnf-data.cpy`                        | 92    | production (COBOL data)     |
| `src/copy/parser-data.cpy`                     | 24    | production (COBOL data)     |
| `src/copy/propagate-data.cpy`                  | 105   | production (COBOL data)     |
| `src/copy/search-data.cpy`                     | 9     | production (COBOL data)     |
| `src/copy/io-data.cpy`                         | 31    | production (COBOL data)     |
| `src/copy/io-fd.cpy`                           | 10    | production (COBOL data)     |
| `src/copy/io-files.cpy`                        | 7     | production (COBOL data)     |
| `scripts/crosscheck_minisat.sh`                | 180   | tooling (shell)             |
| `tests/run_tests.sh`                           | 292   | tests (shell)               |
| `tests/perf.sh`                                | 106   | tests (shell)               |
| `tests/run_sat4j_tests.sh`                     | 141   | tests (shell)               |
| `Makefile`                                     | 18    | build (make)                |
| `.gitignore`                                   | 9     | config                      |
| `.claude/settings.local.json`                  | 12    | config (permission allow-list) |
| `tests/sat4j/expected.tbl`                     | 113   | test data (verdict table)   |

### Aggregate

| Kind                      | Files | LOC    |
|---------------------------|-------|--------|
| COBOL production (main + logic copybooks) | 6 | 1 386 |
| COBOL data copybooks      | 7     | 278    |
| **COBOL total**           | **13** | **1 664** |
| Shell tooling             | 1     | 180    |
| Shell tests               | 3     | 539    |
| Build (Makefile)          | 1     | 18     |
| Config                    | 2     | 21     |
| Test data (verdict table) | 1     | 113    |
| **Grand total (tracked code + scripts)** | **21** | **2 535** |

### Data / examples (not counted as code)

- 113 DIMACS fixtures under `tests/sat4j/{aim,ii,jnh,pigeons}/` + 13
  misc (`aim-50-*-ok.cnf`, `bug001.cnf`, `bug175*.cnf`, `test3.dimacs`,
  `testcomments.{cnf,dimacs}`).
- 22 parser / solver edge-case fixtures under `tests/fixtures/` (8
  `.cnf` + 9 `.model` + 7 solve-CNFs — some overlap).
- 8 SATLIB archives: `uf{75,100,125,150}-*.tar.gz`,
  `uuf{75,100,125,150}-*.tar.gz` (committed to `tests/`, totalling ~5
  MB).
- `tests/bench/` (extracted SATLIB archives — gitignored, ~2 400 CNF
  files).

### Directories

`.`, `.claude/`, `src/`, `src/copy/`, `scripts/`, `tests/`,
`tests/fixtures/`, `tests/sat4j/`, `tests/sat4j/{aim,ii,jnh,pigeons}`,
`tests/crosscheck_failures/` (empty — `.gitignore`'d). Total tracked
directories: 11.

### Entry points

- Program entrypoint: `src/cobsat.cob` → binary `./cobsat` at repo
  root (no wrapper script, unlike the Codex sibling).
- Test entrypoints: `tests/run_tests.sh`, `tests/run_sat4j_tests.sh`,
  `tests/perf.sh`.
- Build entrypoint: `Makefile`.

Cite: `[S:stats_run_1 = analyst Glob + wc counts on 2026-04-16]`.

## Agent-centric backlog

See [`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md) for the
step-wise `SB-001…SB-042` list (what the agent actually did, labelled
User-driven / Agent-initiated / Required prerequisite).

## Limitations / missing evidence

- The session was truncated at `2026-04-16T13:48:17Z` mid-final-turn —
  BL-013 (CDCL) has on-disk code and a `33/33 tests` claim but **no
  commit and no post-CDCL benchmark numbers**. Replay from a `git
  clone` will land on `c3b2a7c` and miss the CDCL work.
- The repo has no top-level `README.md`, so users cloning the project
  see only directory structure and the `Makefile`. The only in-repo
  docs are commit messages and inline COBOL `*>` comments.
- Analyst did not re-run `make test`, `tests/perf.sh`, the crosscheck,
  or the SAT4J runner; all "pass"/"N/N correct" claims cite the
  session's own `tool_output` events.
- `.claude/settings.local.json` shows a minimal allow-list; no
  `CLAUDE.md` / `AGENTS.md` / `.codex/config.toml` means Claude Code's
  default base instructions are the only inherited policy.

## Cross-agent note — divergence from `SATCobol-codex`

Both projects received the same `PL-ROOT` and a broadly similar
instruction stream. Observable differences:

| Axis                         | `SATCobol-codex`                                    | `SATCobol-cc` (this project)                                                     |
|------------------------------|-----------------------------------------------------|----------------------------------------------------------------------------------|
| Agent / model                | Codex CLI 0.119.0 / `gpt-5.4`                       | Claude Code 2.1.109 / `claude-opus-4-6`                                          |
| Session length               | 17h span, 1 rollout                                 | 25h span, 1 rollout (1 122 events)                                               |
| Commits on default branch    | 9 (all landed)                                      | 9 (plus uncommitted CDCL work)                                                    |
| Module layout                | 5 copybooks (`parser/cnf/propagate/search/io`)      | **12** copybooks — same five modules, each split into `<mod>-data.cpy` + `<mod>.cpy`; plus I/O further split (`io-files`, `io-fd`, `io-data`, `io.cpy`) |
| Build surface                | `Makefile` with `build/test/sat4j-test/perf/compare-minisat/clean` + `cobsat` wrapper script | Minimal `Makefile` (`all/test/clean`); binary at repo root, no wrapper; test scripts invoked directly |
| Parser strictness            | Strict on trailing `0` (SATLIB `%` fix only)        | Also loosens trailing-`0` requirement to match SAT4J's Java reader (SB-032)      |
| SAT4J fixtures               | 128 file-based + 11 embedded "bugsat*" + 2 manifests | 113 fixtures (72 aim + 41 ii + 50 jnh + 2 pigeons + 13 misc) + 1 expected.tbl   |
| SAT4J result                 | Not run end-to-end (only translation attested)      | **94 pass / 0 fail / 19 skip** pre-heuristic → **111 pass / 0 fail / 2 skip** post-heuristic (ii cases dominate the skip delta) |
| Branching-heuristic evolution | occurrence → VSIDS + decay (c8cc713f)              | occurrence → JW-weighted + VSIDS-lite + phase saving + Luby (single commit c3b2a7c) |
| Restart policy                | Luby/fixed                                          | Luby with large base (agent-tuned after observing that without clause learning restarts threw away progress) |
| Final "advanced features"     | **CDCL (first-UIP + backjump) committed** as `edb0942b`; +41.4 % total-time improvement attested; second perf round uncommitted | **CDCL uncommitted**; "33/33 tests" claim only; final benchmark launched but session truncated 4 s later |
| MiniSat ratio (final attested) | 8.91× (CDCL + 2 perf rounds)                      | 1.9× (pre-CDCL, ratio is per the 2 400-instance sweep at `c3b2a7c`)              |
| User-prompt count             | 27 events (incl. 8 one-word "commit"s + 1 meta)    | 21 human prompts (incl. 4 "commit"s, 1 "retry/continue", 1 "status?")            |
| Reproducibility of final state | Clean: every feature is at a commit                 | Partial: CDCL work unreachable via `git clone`                                    |
| Benchmark reporting artefact  | In-chat CSV; Markdown report announced but **not written** (`docs/` absent) | In-chat tables only; no report file requested and none written                  |
| Repo docs (README)            | Absent                                              | Absent                                                                           |

Net effect: the CC replica is **architecturally cleaner** (finer
module decomposition, explicit data/logic split) and pushed the
branching heuristic one consolidation-step further than Codex did in
`c8cc713f`, but lost the CDCL finish line because of session
truncation, so the final-commit comparison favours the Codex project by
one major commit (CDCL) and one perf round. In solver-capability terms
both reach "baseline DPLL + watched literals + smart branching +
restarts"; only Codex also reaches "CDCL with clause learning" in a
persisted, committed state.

---

**PASS 1 COMPLETE.**

For the machine-readable appendix, see
[`appendix.json`](appendix.json). For ranked key features, see
[`KEY_FEATURES.md`](KEY_FEATURES.md).
