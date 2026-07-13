# SPECIFICATION_BACKLOG.md — `SATCobol-cc`

> Agent-centric, step-wise backlog of what the Claude Code agent actually
> implemented, grounded in one CC session (`9f10dfb5-…`) and the nine
> commits on the project's default branch. Each `SB-###` is a spec
> statement about an externally observable capability or quality change,
> labelled with provenance.
>
> Companion file: [`README.md`](README.md) (user-driven backlog + prompt
> ledger + stats). Session used:
> `/Users/mathieuacher/.claude/projects/-Users-mathieuacher-SANDBOX-SATCobol-cc/9f10dfb5-e448-463b-bffe-21fa2006c9ae.jsonl`
> (1 122 events, Claude Code `2.1.109`, model `claude-opus-4-6`,
> 2026-04-15T12:20 → 2026-04-16T13:48).

## Purpose

Reflect **how** `cobsat` (this CC replica of the Codex-built `SATCobol-codex`)
grew incrementally across nine commits plus post-last-commit (uncommitted)
CDCL work, mixing user-requested capabilities and agent-initiated
improvements / hardening.

## Step segmentation method

- **Primary**: git commits on the default branch (9 commits,
  `049f4b5…c3b2a7c`). Each commit is a stable checkpoint with a
  descriptive message. Evidence: `[R:.git/logs/HEAD:1-11]`.
- **Secondary**: post-`c3b2a7c` work continuing in the same rollout
  (CDCL implementation + benchmarks in progress). Segmented from session
  episodes. Labelled `EP-POST`.
- **Limitation**: the session was truncated mid-final-turn (agent
  kicked off two parallel background benchmarks at 2026-04-16T13:48 and
  no further events exist). CDCL code is present on disk in
  `src/copy/{propagate,search,cnf,cnf-data,propagate-data}.cpy` but was
  **not committed**; no final CDCL benchmark numbers are attested.

## Provenance labels

- **User-driven**: traced to a `UI-###` and `PL-###` (see `README.md`).
- **Agent-initiated**: decision made by the agent without a direct user
  request (style, hardening, fixture generation, heuristic tuning…).
- **Required prerequisite**: necessary to satisfy an explicit UI item
  even though it was not literally requested (e.g. `Makefile` for
  `--parse`).

---

## SB table

| ID     | Step         | Title                                                          | Category             | Provenance            | Maps to                |
|--------|--------------|----------------------------------------------------------------|----------------------|-----------------------|------------------------|
| SB-001 | `049f4b5`    | DIMACS CNF parser in free-format COBOL (`--parse`)             | Capability           | User-driven           | BL-001 / UI-001        |
| SB-002 | `049f4b5`    | `./cobsat --parse file.cnf` normalised output mode             | Capability           | User-driven           | BL-001 / UI-001        |
| SB-003 | `049f4b5`    | `Makefile` + `cobsat` binary at repo root (no wrapper)         | Tooling              | Required prerequisite | BL-001                 |
| SB-004 | `049f4b5`    | Parser edge-case tests (empty / crlf / trailing / many / interleaved / multiline) | Test/Validation | User-driven       | BL-001 / UI-001        |
| SB-005 | `049f4b5`    | Initial commit on default branch                               | Tooling (OP-ish)     | User-driven           | OP-001 / UI-002        |
| SB-006 | `3fc5cdd`    | `--check-model file.cnf model.txt` mode                        | Capability           | User-driven           | BL-002 / UI-003        |
| SB-007 | `3fc5cdd`    | Per-fixture sat / unsat / partial `.model` fixtures (9 files)  | Test/Validation      | User-driven           | BL-002 / UI-003        |
| SB-008 | `3fc5cdd`    | Per-clause failure error format (`UNSAT clause N: …`)          | Behavior             | Agent-initiated       | BL-002                 |
| SB-009 | `88e8e99`    | SATLIB `%` end-of-data trailer tolerance in parser             | Behavior/Hardening   | User-driven (implied) | BL-003 / UI-004        |
| SB-010 | `88e8e99`    | Ship `uf75-325.tar.gz` + `uuf75-325.tar.gz` under `tests/`     | Test/Validation      | User-driven           | BL-003 / UI-004        |
| SB-011 | `88e8e99`    | 200-instance uf75/uuf75 sweep via `--parse` (SAT/UNSAT-agnostic) | Test/Validation    | User-driven           | BL-003 / UI-004        |
| SB-012 | `bdea674`    | Baseline DPLL solver (`--solve`, unit-prop + chrono backtrack) | Capability           | User-driven           | BL-004 / UI-005        |
| SB-013 | `bdea674`    | `s SATISFIABLE` / `v … 0` / `s UNSATISFIABLE` solver I/O       | Behavior             | User-driven           | BL-004 / UI-005        |
| SB-014 | `bdea674`    | Solve fixtures (unit_chain, contradiction, xor3, xor3_unsat, php*) | Test/Validation  | User-driven           | BL-004 / UI-005        |
| SB-015 | `bdea674`    | Iterative DPLL with explicit trail `(var, kind)` entries       | Capability           | Agent-initiated       | BL-004                 |
| SB-016 | `bdea674`    | `--check-model` self-validation on every SAT model             | Test/Validation      | User-driven           | BL-004 / UI-005        |
| SB-017 | (post-`bdea674`) | uf75/uuf75 200-instance solve soundness (session-attested) | Test/Validation      | User-driven           | BL-005 / UI-007        |
| SB-018 | `b2d8324`    | Split 920-line monolith into 12 copybooks under `src/copy/`    | Refactor             | User-driven           | BL-006 / UI-009        |
| SB-019 | `b2d8324`    | Separate `*-data.cpy` (data) vs `*.cpy` (logic) per module     | Refactor             | Agent-initiated       | BL-006                 |
| SB-020 | `b2d8324`    | `-I src/copy` include path in `Makefile`                       | Tooling              | Required prerequisite | BL-006                 |
| SB-021 | `de35d40`    | Two-watched-literals unit propagation                          | Capability (perf)    | User-driven           | BL-007 / UI-010        |
| SB-022 | `de35d40`    | Occurrence-count branching heuristic                           | Capability           | User-driven           | BL-007 / UI-010        |
| SB-023 | `de35d40`    | `tests/perf.sh` regression-tripwire harness                    | Tooling              | User-driven           | BL-007 / UI-010        |
| SB-024 | `de35d40`    | Larger bench archives (uf100/uuf100/uf125/uuf125/uf150/uuf150) | Test/Validation      | Agent-initiated       | BL-007                 |
| SB-025 | `a121b45`    | `scripts/crosscheck_minisat.sh` vs MiniSat                     | Test/Validation      | User-driven           | BL-008 / UI-011        |
| SB-026 | `a121b45`    | Repro capture on mismatch → `tests/crosscheck_failures/<name>/` | Test/Validation     | User-driven           | BL-008 / UI-011        |
| SB-027 | `a121b45`    | Strip SATLIB `%` trailer before feeding MiniSat                | Behavior/Hardening   | Agent-initiated       | BL-008                 |
| SB-028 | (post-`a121b45`) | 2400-instance sweep (uf/uuf × {100,125,150})              | Test/Validation      | User-driven           | BL-009 / UI-012        |
| SB-029 | `57de05d`    | SAT4J acceptance suite translated to DIMACS (113 fixtures)     | Test/Validation      | User-driven           | BL-010 / UI-013        |
| SB-030 | `57de05d`    | `tests/sat4j/expected.tbl` SAT/UNSAT verdict table             | Test/Validation      | User-driven           | BL-010 / UI-013        |
| SB-031 | `57de05d`    | `tests/run_sat4j_tests.sh` runner with timeout + skip handling | Tooling              | User-driven           | BL-010 / UI-013        |
| SB-032 | `57de05d`    | Parser lenience: accept missing trailing `0` (SAT4J-style)     | Behavior/Hardening   | Agent-initiated       | BL-010                 |
| SB-033 | `57de05d`    | 94 pass / 0 fail / 19 skip result on SAT4J suite (attested)    | Test/Validation      | User-driven           | BL-010                 |
| SB-034 | `c3b2a7c`    | Phase saving (`WS-PHASE(v)` reused across backtracks/restarts) | Capability (perf)    | User-driven           | BL-011 / UI-015        |
| SB-035 | `c3b2a7c`    | VSIDS-lite activity scoring (`WS-ACT(v)`, decay on conflict)   | Capability (perf)    | User-driven           | BL-011 / UI-015        |
| SB-036 | `c3b2a7c`    | Jeroslow-Wang (JW) initial activity seeding                    | Capability (perf)    | Agent-initiated       | BL-011                 |
| SB-037 | `c3b2a7c`    | Luby restart sequence with large base (restarts-as-fail-safe)  | Capability (perf)    | User-driven           | BL-011 / UI-015        |
| SB-038 | `c3b2a7c`    | SAT4J suite regression: 94 → 111 pass (19 → 2 skip)            | Test/Validation      | User-driven           | BL-011                 |
| SB-039 | (post-`c3b2a7c`) | 2400-instance cobsat-vs-minisat benchmark (1.9× ratio)    | Test/Validation      | User-driven           | BL-012 / UI-016        |
| SB-040 | `EP-POST-1` (uncommitted) | CDCL core: first-UIP + non-chronological backjump + learnt DB | Capability | User-driven    | BL-013 / UI-017        |
| SB-041 | `EP-POST-1` (uncommitted) | 33/33 unit tests + smokes pass on CDCL build (attested) | Test/Validation | User-driven      | BL-013                 |
| SB-042 | `EP-POST-1` (incomplete) | Final CDCL benchmark launched, **not completed** (session truncated) | Test/Validation | User-driven | BL-013            |

---

## Per-item specifications

### SB-001 — DIMACS CNF parser (free-format COBOL)
Step: `049f4b5` (initial). Parser accepts `c`/`%` comments, `p cnf V C`
header, arbitrary whitespace, multi-line clauses, and `0` terminators;
implemented in a single `src/cobsat.cob` (920 LOC before the refactor).
Evidence: `[R:src/cobsat.cob]` (post-refactor dispatch only, logic now
in `parser.cpy`), commit message "Initial COBOL DIMACS CNF parser with
--parse mode".

### SB-002 — `--parse` mode
`./cobsat --parse file.cnf` prints a normalised representation.
Evidence: `[R:src/cobsat.cob:28-36]` CLI switch; regression coverage in
`tests/run_tests.sh`. Unlike the sibling `SATCobol-codex`, there is no
`cobsat` **wrapper** script — the binary is built at repo root directly
by the `Makefile`.

### SB-003 — Build infrastructure
`Makefile` at repo root: `cobc -x -Wall -O2 -I src/copy` compiles
`src/cobsat.cob` + wildcard `src/copy/*.cpy` → `./cobsat`. Exposes
`all`, `test`, `clean`. Evidence: `[R:Makefile:1-18]`. No multi-target
orchestration (no `sat4j-test` / `perf` / `compare-minisat` targets —
those are invoked directly as `tests/*.sh` and `scripts/*.sh`).

### SB-004 — Parser edge-case test harness
`tests/run_tests.sh` has 32 numbered cases covering `simple`,
`empty_lines`, `many_spaces`, `trailing_spaces`, `crlf`, `multiline`,
`interleaved_comments`, `comment_between_tokens` plus check-model and
solve fixtures. Evidence: `[R:tests/run_tests.sh:1-292]`,
`[T:2026-04-15T12:52:xx]` agent "all tests pass".

### SB-005 — Initial commit
`049f4b5 Initial COBOL DIMACS CNF parser with --parse mode`. Evidence:
`[R:.git/logs/HEAD:1]`. User-requested via `UI-002` ("create a git and
commit").

### SB-006 — `--check-model` mode
`./cobsat --check-model file.cnf model.txt` returns 0 iff the assignment
satisfies every clause, non-zero otherwise. Accepts DIMACS solution-style
v-lines, bare integers, and `c`/`s` comment lines. Evidence:
`[R:src/cobsat.cob:37-51]`, commit `3fc5cdd`.

### SB-007 — Model fixtures
Per parser-fixture, two model files: `simple.sat.model`,
`simple.unsat.model`, `empty_lines.sat.model`, `empty_lines.unsat.model`,
`many_spaces.sat.model`, `many_spaces.unsat.model`,
`multiline.sat.model`, `multiline.unsat.model`, `multiline.partial.model`.
Evidence: `[R:tests/fixtures/*.model]` (9 files).

### SB-008 — Per-clause failure error format
Failing `--check-model` prints `UNSAT clause N: <offending-clause>` on
stderr and returns non-zero. Evidence:
`[R:tests/run_tests.sh:77-81]` asserts the exact format via regex.

### SB-009 — SATLIB `%` end-marker tolerance
SATLIB-style DIMACS files terminate with `%\n0\n`. The parser was
reading that trailing `0` as a new clause, inflating the count; the fix
treats `%` as end-of-data. Evidence: commit message `88e8e99`; session
agent message `[T:2026-04-15T14:11:xx]`.

### SB-010 — Ship uf75/uuf75 archives
`tests/uf75-325.tar.gz` (139 KB) + `tests/uuf75-325.tar.gz` (139 KB),
100 instances each. Evidence: `[R:tests/uf75-325.tar.gz]`,
`[R:tests/uuf75-325.tar.gz]`.

### SB-011 — 200-instance parser sweep
Agent extracted both archives and ran `--parse` on all 200 files; all
passed after the `%` fix. Evidence: session event
`[T:2026-04-15T14:11:57]` commit preamble.

### SB-012 — Baseline DPLL solver (`--solve`)
Iterative DPLL with unit propagation + chronological backtracking;
clauses stored CSR-style in working storage; per-variable state table
(unassigned / true / false); explicit trail of `(var, kind)` entries.
Evidence: `[R:src/copy/search.cpy]` (post-refactor),
`[R:src/copy/propagate.cpy]`, commit `bdea674`.

### SB-013 — Solver I/O
Prints `s SATISFIABLE` + `v … 0` lines (SAT) or `s UNSATISFIABLE`
(UNSAT). Evidence: `[R:src/copy/io.cpy]`.

### SB-014 — Solve fixtures
`unit_chain.cnf`, `contradiction.cnf`, `xor3.cnf`, `xor3_unsat.cnf`,
`php3_2.cnf`, `php4_3.cnf`, `php2_3.cnf`. Evidence:
`[R:tests/fixtures/*.cnf]`.

### SB-015 — Iterative (non-recursive) DPLL
Agent chose an iterative formulation using an explicit trail rather
than COBOL `PERFORM` recursion. Evidence: commit `bdea674` message:
"Iterative DPLL: … explicit trail of (var, kind) entries".

### SB-016 — `--check-model` on every SAT model
The test runner re-feeds cobsat's own `v-lines` through
`--check-model` to self-verify SAT answers. Evidence:
`[R:tests/run_tests.sh:111-180]`.

### SB-017 — uf75/uuf75 solve soundness
Session event `[T:2026-04-15T15:31-41]` after `UI-007 "does it work
with uf75-325 and uuf75-325?"`: agent attests 100/100 SAT on uf75-325
and 100/100 UNSAT on uuf75-325. Not mapped to a dedicated `make`
target.

### SB-018 — Refactor into copybooks
Split `src/cobsat.cob` (920 LOC monolith) into a thin main file
(dispatch + COPY directives, 83 LOC) plus **12** copybooks under
`src/copy/`. Evidence: `[R:src/cobsat.cob:1-83]`, commit `b2d8324`.

### SB-019 — Data/logic split
Each logical module has two copybooks: `<mod>-data.cpy` (working-storage
records) and `<mod>.cpy` (PROCEDURE DIVISION paragraphs). Same for I/O
(`io-files.cpy` for FILE-CONTROL, `io-fd.cpy` for FD entries,
`io-data.cpy`, `io.cpy`). Evidence: 12 `*.cpy` files in `src/copy/`.
This is finer-grained than the Codex sibling's 5-copybook layout.

### SB-020 — Include path
`Makefile` passes `-I src/copy`. Evidence: `[R:Makefile:2]`.

### SB-021 — Watched literals
Two-watched-literals propagation replacing naive scan. Evidence:
`[R:src/copy/propagate.cpy]`, commit `de35d40` ("Replaces the naive
'scan every clause every pass' propagator with a two-watched-literals
scheme").

### SB-022 — Occurrence-count branching
Pick unassigned variable with highest positive+negative occurrence
count. Evidence: `[R:src/copy/search.cpy]` PICK paragraph; commit
`de35d40`.

### SB-023 — Perf harness
`tests/perf.sh` times `--solve` across uf75/uuf75 (and optionally
uf150/uuf150) and prints total/mean/max per set. Uses `python3` for
sub-second timing. Evidence: `[R:tests/perf.sh:1-106]`.

### SB-024 — Larger bench archives
Agent-initiated: downloads `uf{100,125,150}-*.tar.gz` +
`uuf{100,125,150}-*.tar.gz` into `tests/` (6 archives) to enable harder
benchmarks. Evidence: `ls tests/*.tar.gz` shows 8 archives.

### SB-025 — MiniSat cross-checker
`scripts/crosscheck_minisat.sh`: runs `./cobsat --solve`, then
`minisat` on the same CNF, compares verdicts; on SAT also validates
cobsat's model via `--check-model`. Evidence:
`[R:scripts/crosscheck_minisat.sh:1-180]`, commit `a121b45`.

### SB-026 — Repro capture
On mismatch, stores `input.cnf`, `cobsat.out`, `minisat.out`,
`minisat.stdout`, `STATUS` under `tests/crosscheck_failures/<basename>/`.
Evidence: `[R:scripts/crosscheck_minisat.sh:10-15]`.

### SB-027 — SATLIB `%` trailer stripped for MiniSat
Agent-initiated: MiniSat errors on the `%` trailer, so the
crosschecker strips it before invoking MiniSat. Evidence: commit
`a121b45` message body.

### SB-028 — 2400-instance sweep
Agent ran full uf/uuf × {100, 125, 150} benchmark (2 400 instances) in
background (`[T:2026-04-16T04:51:54]` task notification). 2 400 / 2 400
correct. Evidence: session `[T:2026-04-16T10:22:24]`:
"**2400/2400 correct.**".

### SB-029 — SAT4J fixtures
113 DIMACS fixtures under `tests/sat4j/{aim,ii,jnh,pigeons}` plus
`aim-50-*-ok.cnf`, `bug001.cnf`, `bug175*.cnf`, `test3.dimacs`,
`testcomments.{cnf,dimacs}`. Extracted from SAT4J's Java test sources
(`AbstractM2Test`, `TestsFonctionnels`, `BugSAT175`). Evidence:
`[R:tests/sat4j/]` (113 files + expected.tbl).

### SB-030 — Expected-verdicts table
`tests/sat4j/expected.tbl` lists 113 lines of form `SAT|UNSAT
path/to.cnf`. Evidence: `[R:tests/sat4j/expected.tbl:1-113]`.

### SB-031 — SAT4J runner
`tests/run_sat4j_tests.sh` iterates `expected.tbl`, runs
`./cobsat --solve` with a 30-second timeout per instance; classifies
pass / fail / skip(timeout). Evidence:
`[R:tests/run_sat4j_tests.sh:1-141]`.

### SB-032 — Parser lenience for SAT4J files
Accept missing trailing `0` (SAT4J's Java reader is lenient about it).
Evidence: session `[T:2026-04-16T07:18:50]` agent: "Minisat also
rejects that file — SAT4J's reader is lenient about a missing trailing
`0`. Let me make our parser match that leniency".

### SB-033 — SAT4J result (pre-heuristic)
At commit `57de05d`: **94 pass, 0 fail, 19 skip (timeout)** on 113
tests. Evidence: session `[T:2026-04-16T08:34:20]` commit attestation.

### SB-034 — Phase saving
`WS-PHASE(v)` records last assigned value; decisions reuse it across
backtracks and restarts. Evidence: `[R:src/copy/propagate-data.cpy]`,
`[R:src/copy/search.cpy]`, commit `c3b2a7c`.

### SB-035 — VSIDS-lite
`WS-ACT(v)` seeded from JW; bumped on every conflict for variables
touched in the (implicit) reason set; periodic decay. Evidence: same
commit; `[R:src/copy/propagate.cpy]`.

### SB-036 — JW initial seeding
Agent-initiated: each clause of length k contributes `2^(10−k)` to its
literals' activity at init. Equivalent to plain counts on uniform 3-SAT
but discriminates on mixed-length industrial clauses. Evidence: commit
`c3b2a7c` message body.

### SB-037 — Luby restarts with large base
Luby sequence, but restart base tuned large enough that restarts only
fire on pathological instances (without clause learning, restarts throw
away progress). Evidence: session `[T:2026-04-16T09:50:29]`: "set a
much larger restart base so they only fire on pathological instances".

### SB-038 — SAT4J result (post-heuristic)
**111 pass / 0 fail / 2 skip** on the same 113-test suite — a 17-test
improvement over SB-033 driven primarily by JW+phase+VSIDS on
industrial (`ii`) cases. Evidence: session `[T:2026-04-16T10:03:27]`:
"SAT4J suite jumps from 94→111 pass (19→2 skip)".

### SB-039 — cobsat-vs-minisat benchmark (2 400 instances)
Background run, full 2 400-instance sweep. **cobsat 101.6 s / minisat
52.6 s / ratio 1.9×** overall; per-family ratios 1.3× → 5.8× (worst on
uuf150-645). Evidence: session `[T:2026-04-16T13:16:16]`.

### SB-040 — CDCL core (UNCOMMITTED)
After the minisat comparison, agent decided "CDCL is the right next
step" and implemented first-UIP conflict analysis +
non-chronological backjump + learnt-clause database, editing
`propagate.cpy`, `search.cpy`, `cnf.cpy`, `cnf-data.cpy`,
`propagate-data.cpy`. On-disk evidence: `[R:src/copy/search.cpy:7-20]`
comment block describes CDCL loop; `[R:src/copy/propagate.cpy:203+]`
contains `ANALYZE-CONFLICT`; `WS-LEARNT` slot at
`[R:src/copy/search.cpy:117]`. **No commit**: `.git/logs/HEAD` ends
at `c3b2a7c` (2026-04-16T10:03).

### SB-041 — CDCL unit tests attested
Agent reports "33/33 unit tests pass + smokes correct" at
`[T:2026-04-16T13:43:46]`. Not independently re-verified by the
analyst.

### SB-042 — Final CDCL benchmark — NOT DELIVERED
Agent launched two parallel background benchmark runs at
`[T:2026-04-16T13:48:06-13]` and the session log ends 4 s later. No
final CDCL numbers are attested; no commit. Status: **Not delivered**.

---

## Mapping summary

| SB range     | Commit       | Related BL / UI                  |
|--------------|--------------|----------------------------------|
| SB-001…005   | `049f4b5`    | BL-001 (UI-001), OP-001 (UI-002) |
| SB-006…008   | `3fc5cdd`    | BL-002 (UI-003)                  |
| SB-009…011   | `88e8e99`    | BL-003 (UI-004)                  |
| SB-012…016   | `bdea674`    | BL-004 (UI-005)                  |
| SB-017       | (post)       | BL-005 (UI-007)                  |
| SB-018…020   | `b2d8324`    | BL-006 (UI-009)                  |
| SB-021…024   | `de35d40`    | BL-007 (UI-010)                  |
| SB-025…027   | `a121b45`    | BL-008 (UI-011)                  |
| SB-028       | (post)       | BL-009 (UI-012)                  |
| SB-029…033   | `57de05d`    | BL-010 (UI-013)                  |
| SB-034…038   | `c3b2a7c`    | BL-011 (UI-015)                  |
| SB-039       | (post)       | BL-012 (UI-016)                  |
| SB-040…042   | EP-POST-1    | BL-013 (UI-017) — Partial        |

## Limitations

- No repo-level `CLAUDE.md` / `AGENTS.md`. Only `.claude/settings.local.json`
  exists (4 allow-list entries: `git init *`, `git add *`, three `Read`
  paths into `/private/tmp/sat4j`). PC items therefore minimal.
- Session truncated during final CDCL benchmark — SB-040/041/042
  reflect uncommitted on-disk state + chat claims with no attested
  final numbers.
- Analyst did not re-run `make test`, `tests/perf.sh`,
  `tests/run_sat4j_tests.sh`, or the crosschecker; all "pass" claims
  cite session `tool_output` events.
