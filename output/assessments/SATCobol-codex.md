# Assessment — `SATCobol-codex` — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> **`cobsat`** — a modular COBOL solver (`src/cobsat.cob` ≈ 280 LOC orchestrating five COPY modules: `cnf.cpy`, `io.cpy`, `parser.cpy`, `propagate.cpy`, `search.cpy`). Implements CDCL with **watched literals, VSIDS, restarts, and backjumping**. Validated against SAT4J + MiniSat on uf/uuf benchmark families at 75 / 100 / 125 / 150 variables, with a perf regression suite. In-session benchmark shows TOTAL time **230.5 s → 135.0 s → 118.7 s** across three optimisation rounds, closing the MiniSat ratio from 18.08× down to 8.91×.

> **A competitive minimalist CDCL solver in COBOL** — runs in the same ballpark as textbook reference implementations, and within **~9×** of MiniSat on uf100 / uuf100. For a language with no pointers, clause-database work must be emulated via integer arrays; being single-digit-multiple of MiniSat is genuinely strong.

**Difficulty (auto-labelled):** Medium (idx 0.44). **Active collaboration time:** 0 h 45 m. **Sessions:** 1. **Backlog entries discovered:** 63. **Git commits:** 10.

## 1. Contract — what was asked

Implement a SAT solver in COBOL that reads DIMACS CNF, prints SAT-Competition-style output, and is cross-checked against SAT4J and MiniSat on `uf*` / `uuf*` benchmark families.

Opening user prompt (verbatim, truncated):

```
Implement a robust DIMACS CNF parser in COBOL: supports c comments, p cnf <vars> <clauses>, arbitrary whitespace, multiple lines per clause, and 0 clause terminators. Add a parser-only mode: ./cobsat --parse file.cnf prints a normalized representation (vars, clauses, literals). Add unit tests under tests/ that cover: empty lines, CRLF line endings, trailing spaces, many spaces, comment lines between tokens.
```

## 2. Delivered — externally-observable evidence

**`cobsat`** — a modular COBOL solver (`src/cobsat.cob` ≈ 280 LOC orchestrating five COPY modules: `cnf.cpy`, `io.cpy`, `parser.cpy`, `propagate.cpy`, `search.cpy`). Implements CDCL with **watched literals, VSIDS, restarts, and backjumping**. Validated against SAT4J + MiniSat on uf/uuf benchmark families at 75 / 100 / 125 / 150 variables, with a perf regression suite. In-session benchmark shows TOTAL time **230.5 s → 135.0 s → 118.7 s** across three optimisation rounds, closing the MiniSat ratio from 18.08× down to 8.91×.

**Executables present in `SANDBOX/SATCobol-codex/`** (at least *something* built):

- `cobsat` (0 KB)

**COBOL surface exercised.** 6 COBOL file(s), 1,706 code lines, 70 paragraphs (≈ function-like units), 3 sections, mastery score **42** distinct constructs across **9/10** capability categories.

**Backlog (auto-mined).** 63 `F-###` / `SB-###` / `S#-##` entries in the harvested / subagent-generated `SPECIFICATION_BACKLOG.md`. Prompts also produced 0 sub-request bullets; git history carries 10 commits.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

**Mean score across 17 BLs and 6 criteria: 1.74/2** (Q1 corr. 1.82, Q2 build 2, Q3 tests 1.81, Q4 robust 1.81, Q5 maintain 1.5, Q6 repro 1.53).

| BL | Q1 corr. | Q2 build/run | Q3 tests | Q4 robust | Q5 maintain | Q6 repro | Conf |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BL-001` | 2 | 2 | 2 | 2 | 1 | 2 | High |
| `BL-002` | 2 | 2 | 2 | 2 | 1 | 2 | High |
| `BL-003` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-004` | 2 | 2 | 2 | 2 | 1 | 1 | High |
| `BL-005` | 2 | 2 | 2 | 2 | 1 | 2 | High |
| `BL-006` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-007` | 2 | 2 | 1 | 2 | 1 | 1 | Med |
| `BL-008` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-009` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-010` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-010b` | 2 | 2 | 1 | 2 | 1 | 1 | Med |
| `BL-011` | 2 | 2 | 2 | 1 | 2 | 2 | High |
| `BL-012` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-013` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-014` | 2 | 2 | 2 | 2 | 2 | 1 | Med |
| `BL-015` | 1 | 2 | 1 | 2 | 2 | 0 | Low |
| `BL-016` | 0 | NA | NA | NA | NA | 0 | High |

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** Production SAT solvers (Kissat, CaDiCaL) are C/C++ with learned-clause minimization, phase saving, LBD-based clause database management, proof generation, and years of benchmark-driven tuning.

**Where this result sits.** **A competitive minimalist CDCL solver in COBOL** — runs in the same ballpark as textbook reference implementations, and within **~9×** of MiniSat on uf100 / uuf100. For a language with no pointers, clause-database work must be emulated via integer arrays; being single-digit-multiple of MiniSat is genuinely strong.

**Why the ceiling is out of reach here — honest constraints (not failures):**

- COBOL has no pointers / dynamic memory → clause database is a fixed-capacity `COMP-5` OCCURS table; no realloc, no CDCL-inprocessing.
- No learned-clause minimization / LBD.
- No proof generation (DRAT / DRUP) — out of session scope.
- Benchmarks limited to ≤ 150 variables — industrial instances are millions of variables.

## 5. What's genuinely impressive (evidence-anchored)

- **CDCL with watched literals + VSIDS + restarts + backjumping** — the standard algorithmic skeleton of a modern SAT solver, implemented in COBOL.
- **Modular COPY-book architecture** — cnf / io / parser / propagate / search — is a cleaner decomposition than the `cobol-SAT` sibling.
- **1:1 commit-to-user-prompt cadence**: 9 commits, 9 user 'commit' prompts — the agent kept the repo in a clean, bisectable state after every feature.
- SAT4J + MiniSat cross-checks give an **external oracle** — correctness is not self-reported.
- Perf work is measured, not guessed: three optimisation rounds with real timings.

## 6. Honest gaps

- BL-015 (post-turn-17 perf tweaks) is on-disk but **uncommitted** — second-round speedup is in-session-only evidence.
- No learned-clause minimization → clause DB grows unbounded on hard instances.
- No external DRAT / DRUP proof — UNSAT results are not externally certifiable.
- Session was truncated mid-turn; a post-session summary (`docs/` report, BL-016) never landed.

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 13.9% (26 errors / 187 tool outputs).
- Bug-report-style user prompts: 0.
- Redirect-style user prompts: 0.
- Share of active time spent on `bug_fix`: 7.0% (3 min of 45 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/SATCobol-codex`
- Sessions: 1 (primary agent: Codex gpt-5.4)
- Git history: 10 commits available in `/Users/mathieuacher/SANDBOX/SATCobol-codex/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/SATCobol-codex/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/SATCobol-codex__*.jsonl`.

## 8. Final take

****A competitive minimalist CDCL solver in COBOL** — runs in the same ballpark as textbook reference implementations, and within **~9×** of MiniSat on uf100 / uuf100.** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/SATCobol-codex.json`, `output/backlogs/SATCobol-codex/appendix.json` (when present), `output/complexity/SATCobol-codex.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
