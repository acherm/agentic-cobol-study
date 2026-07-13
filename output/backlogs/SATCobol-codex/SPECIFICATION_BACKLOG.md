# SPECIFICATION_BACKLOG.md — `SATCobol-codex`

> Agent-centric, step-wise backlog of what the Codex CLI agent actually
> implemented, grounded in one Codex rollout and the nine commits on
> `main`. Each `SB-###` is a spec statement about an externally observable
> capability or quality change, labelled with provenance.
>
> Companion file: [`README.md`](README.md) (user-driven backlog + prompt
> ledger + stats). Session used:
> `/Users/mathieuacher/.codex/sessions/2026/04/15/rollout-2026-04-15T14-18-52-019d9114-7f7f-7a23-a04c-5c6cf0b9c61c.jsonl`
> (`019d9114-7f7f-7a23-a04c-5c6cf0b9c61c`, Codex `0.119.0-alpha.11`, model `gpt-5.4`, 2026-04-15T12:19 → 2026-04-16T05:34).

## Purpose

Reflect **how** `cobsat` grew incrementally across nine commits plus
post-last-commit (uncommitted) work, mixing user-requested capabilities
and agent-initiated improvements / hardening.

## Step segmentation method

- **Primary**: git commits on `main` (9 commits, `6e49eb7…edb0942`). Each
  commit is a stable checkpoint with diffstat and a descriptive message.
  [G:commit log at `[R:.git/logs/HEAD]`]
- **Secondary**: post-`edb0942` work continuing in the same rollout
  (benchmark replay, another perf round, report-authoring). Segmented
  from session episodes. Labelled `EP-POST`.
- **Limitation**: the rollout was truncated mid-final-turn (agent
  announced a `docs/` benchmark report but no file was written —
  confirmed by `find ... -name "*.md"` returning only the sat4j
  README). Some SB items therefore rely on in-chat agent numbers only.

## Provenance labels

- **User-driven**: traced to a `UI-###` and `PL-###` (see `README.md`).
- **Agent-initiated**: decision made by the agent without a direct user
  request (style, hardening, fixture generation, heuristic tuning…).
- **Required prerequisite**: necessary to satisfy an explicit UI item
  even though it was not literally requested (e.g. `cobsat` wrapper
  implied by `./cobsat --parse`).

---

## SB table

| ID     | Step              | Title                                             | Category            | Provenance               | Maps to            |
|--------|-------------------|---------------------------------------------------|---------------------|--------------------------|--------------------|
| SB-001 | `6e49eb7`         | DIMACS CNF parser in free-format COBOL            | Capability          | User-driven              | BL-001 / UI-001    |
| SB-002 | `6e49eb7`         | `./cobsat --parse file.cnf` normalized output     | Capability          | User-driven              | BL-001 / UI-001    |
| SB-003 | `6e49eb7`         | `./cobsat` wrapper + `Makefile` + `build/` layout | Tooling             | Required prerequisite    | BL-001             |
| SB-004 | `6e49eb7`         | Parser edge-case unit tests (5 cases) + runner    | Test/Validation     | User-driven              | BL-001 / UI-001    |
| SB-005 | `6e49eb7` (same)  | Large synthetic CNF regression (~100k clauses)    | Test/Validation     | Agent-initiated          | BL-002 / UI-002    |
| SB-006 | `6e49eb7` (same)  | SATLIB end-marker (`%`, trailing `0`) tolerance   | Behavior/Hardening  | Agent-initiated          | BL-005 / UI-005    |
| SB-007 | `6e49eb7`         | Initial commit on `main`                          | Tooling (OP-ish)    | User-driven              | OP-001 / UI-003    |
| SB-008 | `59d47ff`         | Model-checking mode `--check-model file.cnf m.txt`| Capability          | User-driven              | BL-003 / UI-004    |
| SB-009 | `59d47ff`         | Model fixtures (sat + failing) + runner assertions| Test/Validation     | User-driven              | BL-003 / UI-004    |
| SB-010 | `59d47ff`         | Baseline DPLL solver (unit-prop + backtracking)   | Capability          | User-driven              | BL-006 / UI-007    |
| SB-011 | `59d47ff`         | `s SATISFIABLE` / `v … 0` / `s UNSATISFIABLE` I/O | Behavior            | User-driven              | BL-006 / UI-007    |
| SB-012 | `59d47ff`         | Solve fixtures (pigeonhole-small, xor-like, …)    | Test/Validation     | User-driven              | BL-006 / UI-007    |
| SB-013 | `59d47ff` (impl)  | Soundness check on uf75/uuf75 SATLIB archives     | Test/Validation     | User-driven              | BL-007 / UI-009    |
| SB-014 | `14555932`        | Split monolith into 5 COPY books                  | Refactor            | User-driven              | BL-008 / UI-010    |
| SB-015 | `14555932`        | `-I src/modules` include path + build rule        | Tooling             | Required prerequisite    | BL-008             |
| SB-016 | `1ebd388f`        | Watched-literals unit propagation                 | Capability (perf)   | User-driven              | BL-009 / UI-011    |
| SB-017 | `1ebd388f`        | Occurrence-based branching heuristic              | Capability          | User-driven              | BL-009 / UI-011    |
| SB-018 | `1ebd388f`        | `tests/run-perf.sh` perf harness                  | Tooling             | User-driven              | BL-009 / UI-011    |
| SB-019 | `ca9a67a7`        | `scripts/crosscheck_minisat.sh` vs MiniSat        | Test/Validation     | User-driven              | BL-010 / UI-012    |
| SB-020 | `ca9a67a7`        | `tests/crosscheck_failures/` repro dir (gitkeep)  | Tooling             | Required prerequisite    | BL-010             |
| SB-021 | `bad44e0a`        | SAT4J regression suite translated to DIMACS       | Test/Validation     | User-driven              | BL-011 / UI-014    |
| SB-022 | `bad44e0a`        | `tests/sat4j/{fixtures,embedded}` + 2 manifests   | Test/Validation     | User-driven              | BL-011 / UI-014    |
| SB-023 | `bad44e0a`        | `tests/run-sat4j-tests.sh` runner + `make sat4j-test` | Tooling         | User-driven              | BL-011 / UI-014    |
| SB-024 | `c8cc713f`        | Restart policy (Luby/fixed) in search             | Capability (perf)   | User-driven              | BL-012 / UI-016    |
| SB-025 | `c8cc713f`        | Activity/VSIDS-like branching heuristic           | Capability (perf)   | User-driven              | BL-012 / UI-016    |
| SB-026 | `8c6ebcf1`        | `scripts/compare_minisat.sh` benchmark harness    | Test/Validation     | User-driven              | BL-013 / UI-017,018|
| SB-027 | `8c6ebcf1`        | `make compare-minisat` target                     | Tooling             | Required prerequisite    | BL-013             |
| SB-028 | `8c6ebcf1` (same) | Family sweep (uf/uuf × {75,100,125,150}) vs MiniSat| Test/Validation    | User-driven              | BL-013 / UI-017,018|
| SB-029 | `edb0942b`        | First-UIP clause learning + non-chronological backjump | Capability (perf)| User-driven             | BL-014 / UI-019    |
| SB-030 | `edb0942b`        | Before/after benchmark table (TOTAL +41.4%, 1.71×)| Documentation (chat)| User-driven              | BL-014 / UI-020    |
| SB-031 | `EP-POST-1`       | Second round of perf tuning (on top of `edb0942`) | Capability (perf)   | User-driven              | BL-015 / UI-021    |
| SB-032 | `EP-POST-1`       | Updated benchmark delta (TOTAL +48.5% / 1.94× vs baseline) | Documentation (chat) | User-driven        | BL-015 / UI-021    |
| SB-033 | `EP-POST-2` (incomplete) | Announce `docs/` benchmark report (not written)| Documentation  | User-driven              | BL-016 / UI-022    |

---

## Per-item specifications

### SB-001 — DIMACS CNF parser (free-format COBOL)
Step: `6e49eb7` (initial). Parser accepts `c` comments, `p cnf V C`
header, arbitrary whitespace, multi-line clauses, and `0` terminators;
implemented as line-sequential token stream in `src/modules/parser.cpy`.
Evidence: `[R:src/modules/parser.cpy]`,
`[T:session 019d9114:evt@2026-04-15T12:25:06]` agent: "The first
compile succeeded. I'm exercising the binary against representative CNF
snippets now".

### SB-002 — `--parse` mode
`./cobsat --parse file.cnf` prints normalized representation (vars /
clauses / literals). Evidence: `[R:src/cobsat.cob]` CLI switch;
regression coverage in `tests/run-tests.sh`.

### SB-003 — Wrapper & build infrastructure
`cobsat` shell wrapper auto-(re)builds `build/cobsat` via
`cobc -x -free -I src/modules`. `Makefile` exposes
`build|test|sat4j-test|perf|compare-minisat|clean`. Evidence:
`[R:cobsat:1-16]`, `[R:Makefile:1-28]`.

### SB-004 — Parser edge-case test harness
`tests/run-tests.sh` asserts: `empty-lines`, `trailing-spaces`,
`many-spaces`, `comments-between-tokens`, `crlf`. Fixtures in
`tests/fixtures/*.cnf` and expected outputs in `tests/expected/*.out`.
Evidence: `[R:tests/run-tests.sh:1-212]`,
`[L:make test → "all tests passed"]` at
`[T:session 019d9114:evt@2026-04-15T15:16:56]`.

### SB-005 — Large-instance regression (agent-initiated)
Agent measured the parser on a synthetic ~100 k-clause CNF and then
added a `large-synthetic` regression rather than redesigning. Evidence:
`[T:session 019d9114:evt@2026-04-15T12:34:57]` agent: "The parser
already streams a six-figure clause file cleanly, so I'm not changing
the core algorithm just to speculate".

### SB-006 — SATLIB end-marker tolerance (agent-initiated fix)
Real `uf75-325` files contain `%\n0\n` after the declared number of
clauses. Agent patched parser to accept end markers once the declared
clause count is reached. Evidence: agent message at
`[T:session 019d9114:evt@2026-04-15T12:54:14]` "I'm patching the
parser to accept SATLIB-style trailing end markers now"; test
`satlib-end-marker.cnf/.out`.

### SB-007 — Initial commit
`6e49eb7 Add COBOL DIMACS parser and tests`. Evidence:
`[R:.git/logs/HEAD:1]`. User-requested (`create a git and commit`).

### SB-008 — `--check-model` mode
`./cobsat --check-model file.cnf model.txt` exits 0 iff every clause is
satisfied by the assignment, non-zero otherwise. Evidence:
`[R:src/cobsat.cob]`, runner assertions in `tests/run-tests.sh`.

### SB-009 — Model fixtures
`tests/models/{satisfying-basic,satisfying-prefixed,failing-first-clause,failing-third-clause}.model`
plus matching `.out/.err` expected files. Evidence:
`[R:tests/models/]`, `[R:tests/expected/failing-*.err]`.

### SB-010 — Baseline DPLL solver
Unit propagation + chronological backtracking, simple first-unassigned
branching. Evidence: `[R:src/modules/propagate.cpy]`,
`[R:src/modules/search.cpy]`; agent final message for that turn at
`[T:session 019d9114:evt@2026-04-15T13:31…13:48]`.

### SB-011 — DIMACS-style solver I/O
Prints `s SATISFIABLE` + one or more `v … 0` lines (SAT) or
`s UNSATISFIABLE`. Evidence: `[R:src/modules/io.cpy]`; fixture
`tests/fixtures/solve-*.cnf`.

### SB-012 — Solve fixtures
`solve-unit-chain`, `solve-xor-like`, `solve-contradiction`,
`solve-pigeonhole-small`. Evidence: `[R:tests/fixtures/solve-*.cnf]`,
`[L:"all tests passed"]` at 2026-04-15T15:16:56.

### SB-013 — Soundness sweep over SATLIB uf75/uuf75
Full 200 instance pass (100 SAT, 100 UNSAT) with `make test` green.
Evidence: agent at `[T:session 019d9114:evt@2026-04-15T12:54:53]`
"The real SATLIB sweep passed".

### SB-014 — Modularisation refactor (`parser/cnf/propagate/search/io`)
Split into five COPY books under `src/modules/*.cpy`, included from
`src/cobsat.cob` via `COPY` directives. Sizes now: `cnf.cpy` 301,
`io.cpy` 105, `parser.cpy` 470, `propagate.cpy` 194, `search.cpy` 378
LOC. Evidence: `[R:src/modules/]`, commit `14555932 Refactor solver
into modules`.

### SB-015 — Include path plumbing
`Makefile` passes `-I src/modules`; `cobsat` wrapper mirrors it.
Evidence: `[R:Makefile:12]`, `[R:cobsat:12]`.

### SB-016 — Watched literals
`src/modules/propagate.cpy` maintains two watched literals per clause;
external behaviour (SAT/UNSAT/model) unchanged. Evidence:
`[R:src/modules/propagate.cpy]`, commit `1ebd388f Optimize solver
propagation and branching`.

### SB-017 — Occurrence-based branching heuristic
Chooses unassigned literal with highest current occurrence count.
Evidence: same commit; `[R:src/modules/search.cpy]`.

### SB-018 — Perf script
`tests/run-perf.sh` times the solver against a medium-CNF set and
prints per-instance timings. Evidence: `[R:tests/run-perf.sh]`;
`make perf` target.

### SB-019 — MiniSat cross-checker
`scripts/crosscheck_minisat.sh` runs `./cobsat`, normalises with
`./cobsat --parse`, runs `minisat` on the normalised CNF, compares
SAT/UNSAT, and stores a repro (cobsat stdout, minisat out/err,
normalised.cnf) into `tests/crosscheck_failures/` on mismatch. Exits
non-zero on mismatch or MiniSat failure. Evidence:
`[R:scripts/crosscheck_minisat.sh:1-122]`,
`[T:session 019d9114:evt@2026-04-15T15:17:06]`.

### SB-020 — Crosscheck failures dir
`tests/crosscheck_failures/.gitkeep` retained; rest gitignored.
Evidence: `[R:.gitignore:3-4]`.

### SB-021 / SB-022 / SB-023 — SAT4J regression translation
128 DIMACS fixtures (`aim`, `jnh`, `pigeons`, plus one-off bug repros)
plus 11 embedded "bugsat*" files, two manifests
(`manifest-file-based.tsv`, `manifest-embedded.tsv`) mapping each case
to its SAT4J test id, a runner `tests/run-sat4j-tests.sh`, and a
`make sat4j-test` target. README documents scope exclusions (pseudo-
Boolean, MUS, cardinality, `ii` family). Evidence:
`[R:tests/sat4j/README.md]`, `[R:tests/sat4j/manifest-file-based.tsv]`,
`[R:tests/run-sat4j-tests.sh]`, `[R:Makefile:6,18-19]`.

### SB-024 — Restarts
Restart policy added in `src/modules/search.cpy` (commit `c8cc713f Add
restarts and activity-based branching`). Evidence: `[R:src/modules/search.cpy]`.

### SB-025 — Activity/VSIDS-like branching
Score-bumping + decay, replacing the occurrence heuristic. Evidence:
same commit; `[R:src/modules/search.cpy]`.

### SB-026 / SB-027 / SB-028 — MiniSat benchmark comparator
`scripts/compare_minisat.sh` times `build/cobsat` vs `minisat` on a set
of archives (or the four SATLIB families by default), prints a per-
family CSV with `cobsat_total/avg/max`, `minisat_total/avg/max`, and
`cobsat_over_minisat` ratio, plus a grand total. Exposes env overrides
`MINISAT_BIN`. Wired as `make compare-minisat`. Evidence:
`[R:scripts/compare_minisat.sh:1-253]`, `[R:Makefile:24-25]`.

### SB-029 — Clause learning + backjumping
First-UIP analysis and non-chronological backjump. Evidence: commit
`edb0942 Add clause learning and backjumping`; edited
`src/modules/{search,propagate,cnf}.cpy`.

### SB-030 — Before/after perf numbers (in-chat)
Agent produced a CSV comparing pre-`edb0942` vs post-`edb0942`: TOTAL
230.513 s → 134.988 s (+41.4 %, 1.71 ×); cobsat_over_minisat 18.08 →
10.45. Notable: `uuf100-430` 2.21 ×, `uuf125-538` 2.39 ×,
`uuf150-645` 1.94 ×; one regression `uf150-645` −17.2 %. Evidence:
`[T:session 019d9114:evt@2026-04-16T05:13:05]`.

### SB-031 — Second perf round (post-commit, uncommitted)
After the user asked for "another round of performance improvement"
the agent applied further tuning (reasoning encrypted — not directly
quotable) but the session ended before a commit. Evidence:
`[T:session 019d9114:evt@2026-04-16T05:17:37 → 05:34]`. Uncommitted
changes expected in the workspace tree (current on-disk file sizes are
larger than `edb0942` totals: `cnf.cpy` 301, `search.cpy` 378).

### SB-032 — Updated benchmark numbers (in-chat)
Second-round comparison vs baseline: TOTAL 230.513 → 118.701 s
(+48.5 %, 1.94 ×); `cobsat_over_minisat` 18.08 → 8.91. Evidence:
`[T:session 019d9114:evt@2026-04-16T05:33:53]`.

### SB-033 — Final report (ANNOUNCED, NOT WRITTEN)
Agent stated it would write a standalone Markdown file under `docs/`
but the session was truncated before any file was created. Evidence:
`[T:session 019d9114:evt@2026-04-16T05:34:08]` agent: "I have the data
structured. I'm writing the report as a standalone Markdown document
under `docs/`…"; repo search confirms `docs/` does not exist. Status:
**Not delivered**.

---

## Mapping summary

| SB range    | Commit      | Related BL / UI                  |
|-------------|-------------|----------------------------------|
| SB-001…007  | `6e49eb7`   | BL-001, BL-002 (UI-001, UI-002)  |
| SB-008…013  | `59d47ff`   | BL-003, BL-006, BL-007           |
| SB-014…015  | `14555932`  | BL-008 (UI-010)                  |
| SB-016…018  | `1ebd388f`  | BL-009 (UI-011)                  |
| SB-019…020  | `ca9a67a`   | BL-010 (UI-012)                  |
| SB-021…023  | `bad44e0a`  | BL-011 (UI-014)                  |
| SB-024…025  | `c8cc713f`  | BL-012 (UI-016)                  |
| SB-026…028  | `8c6ebcf1`  | BL-013 (UI-017, UI-018)          |
| SB-029…030  | `edb0942`   | BL-014 (UI-019, UI-020)          |
| SB-031…032  | EP-POST-1   | BL-015 (UI-021)                  |
| SB-033      | EP-POST-2   | BL-016 (UI-022) — NOT DELIVERED  |

## Limitations

- No repo-level README/AGENTS.md, so PC items are minimal (see README §
  "Project constraints"). Everything the agent read as "project
  policy" was Codex's own system prompt.
- The rollout ends mid-generation; SB-031/SB-032 reflect in-chat numbers
  with no committed artefact; SB-033 was never materialised.
- Some agent reasoning blobs are encrypted (Codex encrypted
  `reasoning.encrypted_content`); claims sourced from those are labelled
  `agent_message` only.
