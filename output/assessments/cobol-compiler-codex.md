# Assessment — `cobol-compiler-codex` — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> **`minicobc`** — a separate COBOL-to-C compiler (distinct codebase from `cobol-compiler-cc`) that **compiles the COBOL DOOM port** (published as `agentic-cobol-doom`) and the game15tictactoe suite, then **benchmarks its output against GnuCOBOL's output** on those programs.

> Similar subset-compiler class to the `-cc` sibling, but with **benchmark-driven comparison** to GnuCOBOL — a rarer and more scientifically useful framing.

**Difficulty (auto-labelled):** Very-High (idx 0.81). **Active collaboration time:** 10 h 58 m. **Sessions:** 4. **Backlog entries discovered:** 61. **Git commits:** 13.

## 1. Contract — what was asked

Parallel 'minicobc' COBOL-to-C compiler, Codex-driven, with explicit benchmarks vs GnuCOBOL.

Opening user prompt (verbatim, truncated):

```
Write a COBOL compiler in COBOL. Demonstrate that you can run some (non-trivial) COBOL programs thanks to the written compiler.
```

## 2. Delivered — externally-observable evidence

**`minicobc`** — a separate COBOL-to-C compiler (distinct codebase from `cobol-compiler-cc`) that **compiles the COBOL DOOM port** (published as `agentic-cobol-doom`) and the game15tictactoe suite, then **benchmarks its output against GnuCOBOL's output** on those programs.

**COBOL surface exercised.** 69 COBOL file(s), 11,680 code lines, 246 paragraphs (≈ function-like units), 70 sections, mastery score **60** distinct constructs across **10/10** capability categories.

**Backlog (auto-mined).** 61 `F-###` / `SB-###` / `S#-##` entries in the harvested / subagent-generated `SPECIFICATION_BACKLOG.md`. Prompts also produced 0 sub-request bullets; git history carries 13 commits.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

**Mean score across 26 BLs and 6 criteria: 1.48/2** (Q1 corr. 1.65, Q2 build 1.96, Q3 tests 1.71, Q4 robust 1, Q5 maintain 1.04, Q6 repro 1.58).

| BL | Q1 corr. | Q2 build/run | Q3 tests | Q4 robust | Q5 maintain | Q6 repro | Conf |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BL-001` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-002` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-003` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-004` | 2 | 2 | 2 | 1 | 1 | 1 | High |
| `BL-005` | 2 | 2 | 1 | 1 | 1 | 2 | High |
| `BL-006` | 1 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-007` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-008` | 1 | 2 | 2 | 1 | 1 | 1 | Medium |
| `BL-009` | 1 | 2 | 2 | 0 | 1 | 2 | High |
| `BL-010` | 2 | NA | NA | 1 | 1 | 2 | High |
| `BL-011` | 2 | 2 | 1 | 1 | 1 | 2 | High |
| `BL-012` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-013` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-014` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-015` | 2 | NA | NA | 1 | 2 | 2 | High |
| `BL-016` | 1 | 2 | 1 | 1 | 1 | 1 | Medium |
| `BL-017` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-018` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-019` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-020` | 1 | 2 | 2 | 1 | 1 | 1 | Medium |
| `BL-021` | 2 | 2 | 2 | 2 | 1 | 2 | High |
| `BL-022` | 1 | 2 | 1 | 1 | 1 | 1 | Medium |
| `BL-023` | 1 | 2 | 1 | 1 | 1 | 1 | Medium |
| `BL-024` | 1 | 2 | 1 | 1 | 1 | 0 | Low |
| `BL-025` | 1 | 1 | 1 | 1 | 1 | 0 | Low |
| `BL-026` | 2 | 2 | 2 | 1 | 1 | 1 | Medium |

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** Same as `cobol-compiler-cc`: full GnuCOBOL-class standard compliance.

**Where this result sits.** Similar subset-compiler class to the `-cc` sibling, but with **benchmark-driven comparison** to GnuCOBOL — a rarer and more scientifically useful framing.

**Why the ceiling is out of reach here — honest constraints (not failures):**

- Same COBOL-surface-coverage limits as the `-cc` sibling.
- A documented `MINICOBC_OPT=1` miscompile on the chess engine was found during the session (uncovered by a user 'are you sure?' redirect) — honest finding, flagged.

## 5. What's genuinely impressive (evidence-anchored)

- **48 SB entries mapped 1:1 to 13 git commits across 11 phases (A..K)** — the most disciplined step segmentation in the set.
- Rubric shows 17 of 26 BLs at `Q1=2` (correctness full), and 22/26 at `Q2=2` (builds and runs) — high success rate.
- Compiling DOOM and publishing it as an artefact repo is a real externally-visible milestone: the agent produced a shareable deliverable, not just a local binary.
- Agent caught its own miscompile via a property-style regression test after a user pushback — this is the self-correcting loop you want to see.

## 6. Honest gaps

- External binaries (stockfish, cutechess-cli) are **unpinned** → BL-024/BL-025 reproducibility scored 0.
- Squash commits compress intra-phase ordering, so the fine-grained sequence inside each phase is partially inferred from session episodes.
- 20% tool-output error rate — the highest in the set — reflects a lot of compile-run-inspect cycles, not a defect rate of the delivered compiler.

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 20.0% (1072 errors / 5370 tool outputs).
- Bug-report-style user prompts: 1.
- Redirect-style user prompts: 4.
- Share of active time spent on `bug_fix`: 3.9% (25 min of 658 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/cobol-compiler-codex`
- Sessions: 4 (primary agent: Codex gpt-5.4)
- Git history: 13 commits available in `/Users/mathieuacher/SANDBOX/cobol-compiler-codex/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/cobol-compiler-codex/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/cobol-compiler-codex__*.jsonl`.

## 8. Final take

**Similar subset-compiler class to the `-cc` sibling, but with **benchmark-driven comparison** to GnuCOBOL — a rarer and more scientifically useful framing.** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/cobol-compiler-codex.json`, `output/backlogs/cobol-compiler-codex/appendix.json` (when present), `output/complexity/cobol-compiler-codex.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
