# Assessment — `SATCobol-cc` — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> A Claude-Code-built CDCL SAT solver in COBOL (`cobsat` binary), modular across a 5-component layout (`src/modules/`), with a cross-check harness against MiniSat / SAT4J.

> **Cross-agent replication** of the SAT domain — the interesting comparison is not vs Kissat but vs the Codex-built `SATCobol-codex`: same contract, different agent. The 2-agent coverage of this domain is now complete.

**Difficulty (auto-labelled):** Low (idx 0.23). **Active collaboration time:** 1 h 14 m. **Sessions:** 1. **Backlog entries discovered:** 87. **Git commits:** 10.

## 1. Contract — what was asked

Claude-Code replica of the SAT-solver domain — same DIMACS CNF contract as `SATCobol-codex`, built following the `SATCobol-codex/REPLAY_PROMPTS.md` step-wise prompts.

Opening user prompt (verbatim, truncated):

```
Implement a robust DIMACS CNF parser in COBOL: supports c comments, p cnf <vars> <clauses>, arbitrary whitespace, multiple lines per clause, and 0 clause terminators. Add a parser-only mode: ./cobsat --parse file.cnf prints a normalized representation (vars, clauses, literals). Add unit tests under tests/ that cover: empty lines, CRLF line endings, trailing spaces, many spaces, comment lines between tokens.
```

## 2. Delivered — externally-observable evidence

A Claude-Code-built CDCL SAT solver in COBOL (`cobsat` binary), modular across a 5-component layout (`src/modules/`), with a cross-check harness against MiniSat / SAT4J.

**Executables present in `SANDBOX/SATCobol-cc/`** (at least *something* built):

- `cobsat` (68 KB)

**COBOL surface exercised.** 13 COBOL file(s), 1,347 code lines, 94 paragraphs (≈ function-like units), 3 sections, mastery score **41** distinct constructs across **9/10** capability categories.

**Backlog (auto-mined).** 87 `F-###` / `SB-###` / `S#-##` entries in the harvested / subagent-generated `SPECIFICATION_BACKLOG.md`. Prompts also produced 0 sub-request bullets; git history carries 10 commits.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

**Mean score across 13 BLs and 6 criteria: 1.82/2** (Q1 corr. 1.92, Q2 build 1.92, Q3 tests 1.85, Q4 robust 1.92, Q5 maintain 1.69, Q6 repro 1.62).

| BL | Q1 corr. | Q2 build/run | Q3 tests | Q4 robust | Q5 maintain | Q6 repro | Conf |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BL-001` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-002` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-003` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-004` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-005` | 2 | 2 | 1 | 2 | 1 | 1 | Med |
| `BL-006` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-007` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-008` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-009` | 2 | 2 | 2 | 2 | 1 | 1 | Med |
| `BL-010` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-011` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-012` | 2 | 2 | 2 | 2 | 1 | 1 | Med |
| `BL-013` | 1 | 1 | 1 | 1 | 1 | 0 | Low |

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** Same as `SATCobol-codex`: industrial CDCL (Kissat, CaDiCaL) with clause minimization, phase saving, proof generation.

**Where this result sits.** **Cross-agent replication** of the SAT domain — the interesting comparison is not vs Kissat but vs the Codex-built `SATCobol-codex`: same contract, different agent. The 2-agent coverage of this domain is now complete.

**Why the ceiling is out of reach here — honest constraints (not failures):**

- Same COBOL language constraints as the Codex sibling (no pointers, fixed-capacity arrays).
- Scope was replication, not novel SAT research.

## 5. What's genuinely impressive (evidence-anchored)

- **Closes the 2-agent coverage gap** for the SAT domain.
- Built from the `SATCobol-codex/REPLAY_PROMPTS.md` pack — a real test that the step-wise replay prompts are portable across agents.
- Independent arrival at the same modular COPY-book decomposition.

## 6. Honest gaps

- Head-to-head perf numbers vs MiniSat + vs the Codex sibling awaiting analyst subagent.

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 1.7% (2 errors / 115 tool outputs).
- Bug-report-style user prompts: 0.
- Redirect-style user prompts: 0.
- Share of active time spent on `bug_fix`: 0.1% (0 min of 74 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/SATCobol-cc`
- Sessions: 1 (primary agent: Claude Code claude-opus-4-6)
- Git history: 10 commits available in `/Users/mathieuacher/SANDBOX/SATCobol-cc/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/SATCobol-cc/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/SATCobol-cc__*.jsonl`.

## 8. Final take

****Cross-agent replication** of the SAT domain — the interesting comparison is not vs Kissat but vs the Codex-built `SATCobol-codex`: same contract, different agent.** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/SATCobol-cc.json`, `output/backlogs/SATCobol-cc/appendix.json` (when present), `output/complexity/SATCobol-cc.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
