# Assessment — `cobol-compiler-cc` — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> **`cobolcc`** (~11 000 COBOL LOC) — a COBOL-to-C compiler, and **`cobolint`** (~4 500 LOC) — a tree-walking interpreter, both written in COBOL. The compiler successfully compiles and runs: a COBOL DOOM port, a COBOL chess engine, and `agentic-cobol-game15tictactoe`. It handles fixed-format + free-format, COMP-5 binary types, LINKAGE SECTION CALLs to external C, RECURSIVE programs with paragraph functions, cross-file group struct wrapping, and a substantial intrinsic library.

> A **self-hosted working subset compiler** — it compiles real, non-trivial programs written by other agent sessions, including recursive chess search and a ray-casting FPS. It is not a competitor to GnuCOBOL, but it is an executable proof that the language-modelling, parsing, and code-gen pieces all fit together.

**Difficulty (auto-labelled):** Very-High (idx 0.83). **Active collaboration time:** 32 h 30 m. **Sessions:** 3. **Backlog entries discovered:** 32. **Git commits:** 74.

## 1. Contract — what was asked

Write a COBOL compiler in COBOL. Demonstrate it can run non-trivial COBOL programs.

Opening user prompt (verbatim, truncated):

```
Write a COBOL compiler in COBOL. Demonstrate that you can run some (non-trivial) COBOL programs thanks to the written compiler.
```

## 2. Delivered — externally-observable evidence

**`cobolcc`** (~11 000 COBOL LOC) — a COBOL-to-C compiler, and **`cobolint`** (~4 500 LOC) — a tree-walking interpreter, both written in COBOL. The compiler successfully compiles and runs: a COBOL DOOM port, a COBOL chess engine, and `agentic-cobol-game15tictactoe`. It handles fixed-format + free-format, COMP-5 binary types, LINKAGE SECTION CALLs to external C, RECURSIVE programs with paragraph functions, cross-file group struct wrapping, and a substantial intrinsic library.

**Executables present in `SANDBOX/cobol-compiler-cc/`** (at least *something* built):

- `cobolcc` (701 KB)
- `cobolint` (138 KB)
- `fizzbuzz_cc` (33 KB)
- `game015_cc` (33 KB)
- `game15_8_cc` (33 KB)
- `game15_8_ref` (51 KB)
- `game15_cc` (33 KB)
- `game15_ref` (51 KB)
- `game15l_ref` (51 KB)
- `game15m_ref` (51 KB)
- _(+18 more)_

**COBOL surface exercised.** 36 COBOL file(s), 15,912 code lines, 266 paragraphs (≈ function-like units), 40 sections, mastery score **57** distinct constructs across **10/10** capability categories.

**Backlog (auto-mined).** 32 `F-###` / `SB-###` / `S#-##` entries in the harvested / subagent-generated `SPECIFICATION_BACKLOG.md`. Prompts also produced 80 sub-request bullets; git history carries 74 commits.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

**Mean score across 9 BLs and 6 criteria: 1.64/2** (Q1 corr. 1.89, Q2 build 2, Q3 tests 1.75, Q4 robust 1.22, Q5 maintain 1.38, Q6 repro 1.67).

| BL | Q1 corr. | Q2 build/run | Q3 tests | Q4 robust | Q5 maintain | Q6 repro | Conf |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BL-001` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-002` | 2 | 2 | 1 | 1 | 1 | 2 | High |
| `BL-003` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-004` | 1 | 2 | 1 | 1 | 1 | 1 | Medium |
| `BL-005` | 2 | 2 | 2 | 1 | 1 | 1 | High |
| `BL-006` | 2 | NA | NA | 2 | 2 | 2 | High |
| `BL-007` | 2 | 2 | 2 | 1 | 2 | 2 | High |
| `BL-008` | 2 | 2 | 2 | 1 | 2 | 1 | High |
| `BL-009` | 2 | NA | 2 | 2 | NA | 2 | High |

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** **GnuCOBOL**: hundreds of thousands of LOC across 20+ years, full ANSI-85 + 2002 + 2014 standard coverage, thousands of passing test cases, mature diagnostic and error-recovery story, production deployment base.

**Where this result sits.** A **self-hosted working subset compiler** — it compiles real, non-trivial programs written by other agent sessions, including recursive chess search and a ray-casting FPS. It is not a competitor to GnuCOBOL, but it is an executable proof that the language-modelling, parsing, and code-gen pieces all fit together.

**Why the ceiling is out of reach here — honest constraints (not failures):**

- A full COBOL-85 implementation would need thousands of conformance-test-driven iterations — categorically beyond a single-session scope.
- Advanced error-recovery (IBM-style 'continue parsing after a comma mismatch') would require a real parser-combinator or LALR framework, not present here.
- Performance work was deferred — a pure `MOVE` in generated C is not yet comparable to GnuCOBOL's generated code.

## 5. What's genuinely impressive (evidence-anchored)

- **Self-hosting ambition**: ~11 000 LOC of COBOL compiled correctly by GnuCOBOL produces a binary that in turn compiles the very COBOL programs written in other sessions — a demonstrable closed loop.
- Non-trivial test corpus — DOOM's ~1 400 LOC of COBOL and a 3 500-LOC chess engine compile and run, end-to-end.
- Deep COBOL surface covered: 266 paragraphs / 40 sections, OCCURS × 161, REDEFINES × 21, COMP-5, COPY × 45, RECURSIVE × 23, full CALL-to-C — the language-feature fan-out is the hardest part and it is there.
- 32 `BL-###` entries backed by **74 git commits** — every feature is a checkpoint.

## 6. Honest gaps

- **No ANSI-85 conformance suite run** — coverage is demonstrated via program-level working examples, not formal standard-compliance checks.
- No nested program support verified; some intrinsic functions missing.
- Performance vs GnuCOBOL not yet benchmarked; the comparison is deferred to `cobol-compiler-codex`.
- Session ended with 9 bug-report-style prompts and a late push on `-O2` issues — exactly the intensive final phase you remembered.

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 8.7% (325 errors / 3740 tool outputs).
- Bug-report-style user prompts: 9.
- Redirect-style user prompts: 5.
- Share of active time spent on `bug_fix`: 3.2% (62 min of 1950 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/cobol-compiler-cc`
- Sessions: 3 (primary agent: Claude Code claude-opus-4-6)
- Git history: 74 commits available in `/Users/mathieuacher/SANDBOX/cobol-compiler-cc/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/cobol-compiler-cc/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/cobol-compiler-cc__*.jsonl`.

## 8. Final take

**A **self-hosted working subset compiler** — it compiles real, non-trivial programs written by other agent sessions, including recursive chess search and a ray-casting FPS.** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/cobol-compiler-cc.json`, `output/backlogs/cobol-compiler-cc/appendix.json` (when present), `output/complexity/cobol-compiler-cc.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
