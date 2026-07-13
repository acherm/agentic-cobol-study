# KEY_FEATURES.md — `SATCobol-codex`

## 1. Preamble

The contract was "implement a SAT solver in COBOL that reads DIMACS CNF,
prints SAT-Competition-style output, and is cross-checked against SAT4J
and MiniSat on `uf*` / `uuf*` benchmark families". What the agent
actually delivered is richer than that sentence suggests: a modular
CDCL solver (watched literals + VSIDS + restarts + first-UIP learning +
non-chronological backjumping), an external-oracle verification harness
against two reference solvers (SAT4J + MiniSat), and three measured
rounds of performance engineering that closed the MiniSat time ratio
from 18.08× to 8.91× on the SATLIB uf/uuf ladder (75 → 100 → 125 → 150
vars).

A "key feature" below is any externally observable capability or
quality attribute of depth ≥ 1 that is **not purely build/infra**. Pure
Makefile / wrapper plumbing is mentioned once at the bottom of the
ranked table for completeness but is not a star of this project.
Entries that obviously belong together at feature granularity
(e.g. CDCL's watched-literals + VSIDS + restarts all live in
`search.cpy` + `propagate.cpy` and were grown across three commits) are
consolidated into a single row; the collapsed SB ids are listed in the
evidence column.

Reference evidence bundle:
[`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md) (33 SB entries,
9 episodes), [`appendix.json`](appendix.json),
[`README.md`](README.md), assessment at
`/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/assessments/SATCobol-codex.md`,
project root `/Users/mathieuacher/SANDBOX/SATCobol-codex/`.

## 2. Ranked table (top features by `depth × (1 + effort × 0.5)`)

| rank | SB/F id | title | class | depth | effort | score | evidence |
|---|---|---|:-:|:-:|:-:|:-:|---|
| 1 | F-CDCL (SB-010, SB-016, SB-017, SB-024, SB-025, SB-029) | CDCL solver core: watched literals + VSIDS activity/decay + Luby/fixed restarts + first-UIP clause learning + non-chronological backjump | ALG | 3 | 3 | 7.5 | `/Users/mathieuacher/SANDBOX/SATCobol-codex/src/modules/propagate.cpy` (194+ LOC), `search.cpy` (378 LOC), `cnf.cpy` (301 LOC); commits `59d47ff → 1ebd388f → c8cc713f → edb0942b`; 1706 total COBOL LOC; mastery score 42 across 9/10 capability categories |
| 2 | F-PERF (SB-030, SB-031, SB-032) | Three-round performance engineering with measurement: TOTAL 230.513 s → 134.988 s → 118.701 s, MiniSat ratio 18.08× → 10.45× → 8.91×, per-family CSV attested in-chat | PRF | 3 | 3 | 7.5 | `appendix.json` benchmark rows; session events `2026-04-16T05:13:05` and `2026-04-16T05:33:53`; `scripts/compare_minisat.sh` (253 LOC); `tests/run-perf.sh` |
| 3 | F-LEARN (SB-029) | First-UIP clause learning + non-chronological backjump (as a standalone algorithmic achievement on top of baseline DPLL) | ALG | 3 | 2 | 6.0 | commit `edb0942b Add clause learning and backjumping`; diffs in `search.cpy` + `propagate.cpy` + `cnf.cpy`; biggest single-commit perf gain (1.71× TOTAL) |
| 4 | F-MINISAT-XCHK (SB-019, SB-020) | MiniSat cross-check oracle with structured repro capture on mismatch (normalised CNF + cobsat stdout + minisat out/err stored under `tests/crosscheck_failures/`) | VER | 2 | 2 | 4.0 | `scripts/crosscheck_minisat.sh` (122 LOC); commit `ca9a67a7`; exit-non-zero-on-disagreement contract |
| 5 | F-SAT4J (SB-021, SB-022, SB-023) | SAT4J regression suite translated to DIMACS — 128 file-based fixtures (aim / jnh / pigeons / bugrepros) + 11 embedded "bugsat*" files, two TSV manifests, `tests/run-sat4j-tests.sh`, `make sat4j-test` | VER | 2 | 2 | 4.0 | `tests/sat4j/{fixtures,embedded}/`, `manifest-file-based.tsv`, `manifest-embedded.tsv`; commit `bad44e0a`; `tests/sat4j/README.md` documents the pseudo-Boolean/MUS scope exclusions |
| 6 | F-MINISAT-BENCH (SB-026, SB-027, SB-028) | MiniSat comparison benchmark harness: sweeps uf/uuf × {75, 100, 125, 150}, emits per-family CSV with totals/avg/max and `cobsat_over_minisat` ratio, `MINISAT_BIN` override, wired as `make compare-minisat` | CMP | 2 | 2 | 4.0 | `scripts/compare_minisat.sh` (253 LOC); `Makefile:24-25`; commit `8c6ebcf1`; uses MiniSat as external timing oracle |
| 7 | F-MODULES (SB-014, SB-015) | 5-COPY-book modular decomposition (`parser / cnf / propagate / search / io`) included via COBOL `COPY` directives with `-I src/modules` plumbing — a clean hand-rolled module system inside a language that has no native one | LNG | 2 | 2 | 4.0 | `src/modules/*.cpy` (5 files, 1448 LOC total); `src/cobsat.cob` orchestrator (~280 LOC); commit `14555932 Refactor solver into modules`; mirrored `-I` in both `Makefile` and `cobsat` wrapper |
| 8 | F-PARSER (SB-001, SB-002, SB-006) | DIMACS CNF parser in free-format COBOL — `c` comments, `p cnf V C` header, arbitrary whitespace, multi-line clauses, `0` terminators, SATLIB `%`-style end-marker tolerance, plus `--parse` normalised-output mode | DOM | 2 | 2 | 4.0 | `src/modules/parser.cpy` (470 LOC); commit `6e49eb7`; edge-case + SATLIB end-marker fixtures in `tests/fixtures/`; DIMACS is an externally-specified format (secondary PRO tag) |
| 9 | F-CHECKMODEL (SB-008, SB-009) | `--check-model file.cnf model.txt` mode: parses a proposed assignment, exits 0 iff every clause is satisfied, non-zero with a targeted error message otherwise; four fixture models (2 passing, 2 failing with per-clause error) | DOM | 1 | 1 | 1.5 | `src/cobsat.cob` CLI dispatch; `tests/models/{satisfying-*.model, failing-*.model}`; `tests/expected/failing-*.err`; commit `59d47ff` |
| 10 | F-PARSER-TESTS (SB-004, SB-005) | Parser edge-case harness (empty lines / CRLF / trailing spaces / many spaces / comments between tokens) plus an agent-initiated ~100 k-clause synthetic regression | VER | 1 | 1 | 1.5 | `tests/run-tests.sh` (212 LOC); `tests/fixtures/*.cnf`; `tests/expected/*.out`; agent decision log `2026-04-15T12:34:57` |
| 11 | F-BUILD (SB-003, SB-007, SB-015, SB-018, SB-020, SB-027) | `cobsat` wrapper auto-rebuilds via `cobc -x -free -I src/modules`; `Makefile` exposes `build / test / sat4j-test / perf / compare-minisat / clean`; `tests/run-perf.sh`; git hygiene (9 bisectable commits, 1:1 with user "commit" prompts) | INF | 1 | 1 | 1.5 | `cobsat` wrapper (16 lines); `Makefile` (28 lines); `.gitignore`; `.git/logs/HEAD` shows 9 linear commits on `main` |

**Significance notes (one line each, keyed to rank):**

1. **F-CDCL** — Not just-an-algorithm. CDCL-with-watched-literals is a textbook algorithm but has **zero reference implementations in COBOL**; the language has no pointers, no dynamic memory, no recursion-by-default, so the entire clause database, watch lists, trail, assignment stack, and conflict analysis graph have to be emulated via fixed-capacity `COMP-5 OCCURS` tables. The textbook becomes a non-trivial engineering problem again.
2. **F-PERF** — Not just-an-algorithm: perf work is iterated and **measured against an external oracle (MiniSat)**, not self-reported. Three distinct rounds, each with a per-instance CSV comparison, and one honestly-reported regression (`uf150-645 −17.2 %`). This is engineering discipline, not a victory lap.
3. **F-LEARN** — Textbook algorithm (first-UIP + backjump) **but** its correct interaction with watched literals, VSIDS bumping at analysis time, and the fixed-capacity clause DB is where bugs live; landing it as one green commit is depth-3 work.
4. **F-MINISAT-XCHK** — Pure VER: this is the mechanism by which SAT/UNSAT verdicts are made *externally falsifiable* rather than self-reported. Repro capture is the non-trivial detail.
5. **F-SAT4J** — VER with heavy mechanical translation effort: 128 + 11 DIMACS fixtures plus TSV manifests mapping each to its upstream SAT4J test id. Scope-exclusions (pseudo-Boolean, MUS, cardinality, `ii`) are documented, which is a soundness claim in itself.
6. **F-MINISAT-BENCH** — CMP (emergent composition): this only works because F-PARSER (normalisation), F-CDCL (something to time), and the SATLIB archive tests (corpus) already exist. The number "8.91×" is only meaningful on top of those three.
7. **F-MODULES** — LNG: COBOL has no native module system. Using `COPY` books as include units with a shared `-I` path in both Makefile and wrapper is pushing the language; the 5-book decomposition (`parser/cnf/propagate/search/io`) is cleaner than most COBOL-in-the-wild and explicitly cleaner than the sibling `cobol-SAT` project per the assessment §5.
8. **F-PARSER** — DOM: DIMACS is a published format, so the depth comes from robustness (multi-line clauses, whitespace tolerance, SATLIB `%\n0\n` trailer found empirically on real `uf75-325` files). Secondary PRO tag because DIMACS is an externally-specified standard.
9. **F-CHECKMODEL** — DOM: simple clause-by-clause evaluator. Low depth but it **is** a separate public mode, not an internal helper, and it has real failing-case fixtures with expected `.err` output.
10. **F-PARSER-TESTS** — VER: five-case harness plus a scale-test. Standard but present, and the large-synthetic case was agent-initiated hardening (SB-005).
11. **F-BUILD** — INF, included for completeness only. Notable mostly for the 1:1 commit-to-user-prompt cadence (9 of each), which is repo hygiene more than engineering depth.

## 3. Composition chains

Four chains are clearly visible in the backlog. The last item of each chain is *only meaningful* because the earlier items are in place and correct.

- **Chain A — correctness oracle:**
  F-PARSER → F-CHECKMODEL → F-CDCL → F-MINISAT-XCHK → F-SAT4J
  > A parser must exist before a model-checker is useful; the model-checker is the lightweight self-oracle; CDCL produces the models; MiniSat cross-check externalises the oracle; SAT4J fixture translation raises the corpus size to 128 + 11 instances. Without the earlier nodes, the last two have nothing to compare.

- **Chain B — performance measurement:**
  F-CDCL → F-MINISAT-XCHK → F-MINISAT-BENCH → F-PERF
  > Perf numbers require something correct to measure (CDCL + external oracle), a harness to produce per-family CSV (the benchmark script), and iteration on top. The 230.5 → 118.7 s curve is **only a claim** once the earlier three are in place.

- **Chain C — language-level modularity unlocks iteration:**
  F-PARSER (monolith) → F-MODULES (refactor) → F-CDCL (watched lits) → F-LEARN (clause learning)
  > Splitting the monolith into `parser / cnf / propagate / search / io` is what made the later heavy edits (watched literals inside `propagate.cpy`, clause learning inside `cnf.cpy` + `search.cpy`) feasible without rewrites. The refactor is a language-level enabler, not decoration.

- **Chain D — external-standard regression vs published suite:**
  F-PARSER → F-SAT4J (128 DIMACS fixtures + manifests) → F-CDCL (the system under test)
  > Translating SAT4J's Java-level unit tests into DIMACS fixtures is only useful if the parser handles the translated files and the solver can run them. The SAT4J node is pure VER emerging on top of DOM + ALG.

## 4. Significance profile

Count per primary class across the top 11 rows (secondary tags in parens are not counted here, so each feature contributes once):

| Class | Count | Share | Notes |
|---|:-:|:-:|---|
| ALG | 2 | 18 % | F-CDCL, F-LEARN (the algorithmic core + its hardest sub-step) |
| PRF | 1 | 9 % | F-PERF (three measured rounds) |
| VER | 3 | 27 % | F-MINISAT-XCHK, F-SAT4J, F-PARSER-TESTS |
| CMP | 1 | 9 % | F-MINISAT-BENCH (emerges on top of ALG + VER) |
| LNG | 1 | 9 % | F-MODULES (COPY-book module system) |
| DOM | 2 | 18 % | F-PARSER (DIMACS), F-CHECKMODEL |
| INF | 1 | 9 % | F-BUILD |
| PRO | 0 | — | (F-PARSER carries a secondary PRO tag; not double-counted) |
| SYS | 0 | — | No cross-runtime / FFI work — COBOL stays self-contained, shells out only for MiniSat timings |

**Centre of gravity.** ALG + PRF + VER together are 6/11 = **55 %** of the ranked features, with LNG + CMP contributing another 18 %. Pure DOM + INF is only 27 %. That is a rich profile: the project earns points in at least **six of nine** significance classes, with VER dominating the count and ALG/PRF dominating the score.

## 5. Verdict

**Balanced hybrid — ALG + PRF + VER, with a genuine LNG supporting act.** This is neither "just-an-algorithm" nor "just-domain-modelling": the CDCL core is textbook, but re-hosting it on COBOL's fixed-capacity arrays is depth-3 engineering; the three-round perf curve is measured against MiniSat, not self-reported; and correctness rests on two independent external oracles (SAT4J, MiniSat) rather than on the author's own tests. The 5-COPY-book architecture is the quiet LNG contribution that made the later heavy edits (watched literals, clause learning) feasible. The most balanced significance profile in the cohort so far.
