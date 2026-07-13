# `COMPRESS-COBOL-CODEX` — Case Study (repository folder `cobol-compress-codex`)

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/cobol-compress-codex/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-compress-codex` assessment](../assessments/cobol-compress-codex.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-compress-codex/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/cobol-compress-codex/KEY_FEATURES.md)
  
> 🔁 **Replay prompts** (step-wise, HOW-agnostic, for reproducing with a different agent): [`REPLAY_PROMPTS.md`](../backlogs/cobol-compress-codex/REPLAY_PROMPTS.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-compress-codex`  
**Sessions.** 3 (1 Claude Code + 2 Codex)  
**Activity window.** 2026-03-12 → 2026-04-16 (34 days)  
**Agents & models.** Claude Code/claude-opus-4-6, Codex/gpt-5.4

---

## RQ1 — Domain, intent, novelty

**What it is.** COBPACK — columnar compressor for fixed-record COBOL data (Codex-built, pure COBOL).

**Why it's interesting.** Specification-driven build of a MVP0 / MVP1 compressor with NONE + RLESP codecs and rigorous trust tests, implemented directly in COBOL.

**From the project's `README.md` (first sections):**

> **# cobpack — COBOL Columnar Record Packer**  
> A command-line tool written in GNUCobol that packages fixed-length record files into columnar `.cpc` containers with optional space-run compression (RLESP), and unpacks them byte-identically. Built in a single Codex (GPT-5.4) session on 2026-03-12 (~47 minutes, 3 turns).

> **## Quick Start**  
> ```sh ./build.sh # compile with cobc (GNUCobol) ./run_tests.sh # build + full test suite (<5s) ```

**Opening prompt that kicked off the project:**

```
# COBPACK — MVP0 Specification (GNUCobol) ## Goal (MVP0) Build a command-line tool `cobpack` that can: 1. **Package** a fixed-length record file into a `.cpc` container (field-wise / columnar layout) using only the `NONE` codec (no compression). 2. **Unpack** that `.cpc` back into the original file **byte-identical**. 3. Provide `info` about the container. This MVP0 proves: * toolchain mastery in COBOL (multi-file build, binary-safe I/O), * schema parsing, * container serialization/deserialization, * round-trip correctness, with minimal algorithmic risk. --- ## Inputs / Outputs ### Record input * `--in input.dat`: binary file with `N` records of exactly `RECORD_LEN` bytes * Validation: file size must be a multiple of `RECORD_LEN`, else error. ### Schema input (MVP0) Plain text, line-based.…
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- fixed-format COBOL implementation
- codec parity with -cc
- test parity
- binary compat

**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:

| Error class | Hits |
|---|---:|
| command exited with non-zero status | 28 |
| C compiler error | 14 |
| missing file | 6 |
| Python traceback (tooling) | 6 |
| assertion failed | 5 |
| GnuCOBOL compiler error (incl. syntax) | 3 |
| permission denied | 1 |
| process aborted | 1 |

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **18** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 168 |
| Git commit subjects | 1 |

**Backlog (18 F-### entries).** Grouped by phase:

- **_unclassified_** — 18 features  
  Toolchain Validation & Binary I/O Experiment; Schema Parser Subprogram; Main CLI & CPC v0 Container (compress/decompress/info, NONE codec); Build & Test Scripts; Test Fixtures (schemas + data); Bug Fix: ORD/CHAR 1-Based Offset; Bug Fix: Nested PERFORM Loop Index Collision; RLESP Codec (encode + decode + AUTO selection) _(+10 more)_

**Prompt-extracted sub-requests (168)** — first 8 (sub-bullets inside user messages):

- _[2026-03-19]_ PASS 1 (Extraction): reconstruct (i) a USER-DRIVEN Feature Backlog, (ii) an AGENT-CENTRIC Specification Backlog (step-wise), plus Prompt Ledger + Replay Package…
- _[2026-03-19]_ SPECIFICATION_BACKLOG.md
- _[2026-03-19]_ README.md (must reference SPECIFICATION_BACKLOG.md)
- _[2026-03-19]_ PASS 2 (Interpretation): characterize strategies, outcomes/quality, interaction demand; correlate with lightweight metrics.
- _[2026-03-19]_ I will NOT provide transcripts proactively.
- _[2026-03-19]_ You must analyze the repo as-is (git history may be minimal/absent).
- _[2026-03-19]_ Codex stores local state under CODEX_HOME (defaults to ~/.codex).
- _[2026-03-19]_ $CODEX_HOME/sessions/**.jsonl (session event streams)

**Git commits (1)** — first 8:

- `f478e7fbfa` 2026-03-23  Initial import: COBPACK MVP1 with trust suite

## RQ3 — What was delivered

**From `REPORT.md`:**

> **# Post-Session Backlog & Strategy Analysis Report**  
> 

> **## cobpack — COBOL Columnar Record Packer**  
> **Session date:** 2026-03-12 | **Agent:** Codex (GPT-5.4, openai) | **Analysis date:** 2026-03-20 ---

**From `TRUST.md`:**

> **# TRUST.md**  
> `cobpack` MVP1 is trusted here by executable evidence, not by inspection alone.

> **## How trust is established**  
> Run: ```sh ./run_tests.sh ``` The suite is deterministic and bounded. - Default wall-clock budget: `< 2 minutes` - Enforced by `run_tests.sh` via `TRUST_MAX_MINUTES` and per-command timeouts - Randomized tests use fixed seeds - Fuzz tests use fixed seeds and bounded subprocess timeouts

**Executables present in the root of the project** (evidence that something builds):

- `cobpack` (146 KB)

## RQ4 — Size and complexity

**File inventory** (29 files, 0.3 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 2 | 2,021 |
| Markdown | 4 | 930 |
| Python | 5 | 774 |
| JSON | 1 | 370 |
| Shell | 2 | 190 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 2 |
| Total lines | 2,021 |
| Code lines (non-blank, non-comment) | 1,812 |
| Comment lines | 4 |
| Sections | 7 |
| Paragraphs | 77 |
| Data items (level-number declarations) | 173 |
| Max IF/EVALUATE nesting (any file) | 4 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 408 |
| `PERFORM` | 233 |
| `IF` | 188 |
| `EXIT` | 132 |
| `COMPUTE` | 29 |
| `ADD` | 22 |
| `DISPLAY` | 14 |
| `READ` | 13 |
| `OPEN` | 11 |
| `CLOSE` | 11 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `src/cobpack.cob` | 1,341 |
| `src/cobpack_schema.cob` | 471 |

**Git churn signal.** 1 commits, 4318 insertions / 0 deletions, first 2026-03-23, last 2026-03-23.

## RQ4b — COBOL language mastery

**Mastery score:** **44** distinct COBOL constructs used across **9/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 1,109 | `IF`×376, `EXIT`×323, `PERFORM`×272, `PERFORM_UNTIL`×39, `ELSE`×29, `PERFORM_VARYING`×28, `WHEN`×22, `EVALUATE`×12 _(+2 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 71 | `COMPUTE`×36, `ADD`×22, `SUBTRACT`×7, `DIVIDE`×5, `ROUNDED`×1 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 186 | `PIC_9`×103, `PIC_X`×41, `USAGE_COMP_5`×39, `OCCURS`×3 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 162 | `READ`×55, `WRITE`×40, `START`×21, `AT_END`×15, `CLOSE`×11, `OPEN_INPUT`×8, `FD`×3, `SELECT`×3 _(+3 more)_ |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 27 | `REFERENCE_MOD`×12, `DELIMITED_BY`×7, `STRING`×6, `UNSTRING`×2 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 8 | `INITIALIZE`×4, `SORT`×2, `SET`×2 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 7 | `GIVING`×3, `USING`×2, `LINKAGE_SECTION`×1, `CALL`×1 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | — | 0 |  |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 13 | `FUNCTION`×13 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 26 | `DISPLAY`×20, `ACCEPT`×6 |

**Notable non-trivial constructs used:** `CALL` (1×), `OCCURS` (3×), `USAGE_COMP_5` (39×), `FD` (3×), `UNSTRING` (2×), `FUNCTION` (13×).

**Procedural structure.** 77 paragraphs, 7 sections across 2 COBOL file(s). That means roughly **77 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **54m 56s** across 802 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `understanding` | reading / searching to build a mental model | 23m 49s | 43.4% |
| `build` | compile / makefile / dependency work | 23m 44s | 43.2% |
| `feature` | adding new functionality | 6m 33s | 11.9% |
| `test` | writing or running tests / benchmarks | 0m 36s | 1.1% |
| `bug_fix` | correcting an observed defect | 0m 12s | 0.4% |
| `plan` | task tracking, planning | 0m 2s | 0.1% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `build` | 99 |
| `feature` | 55 |
| `test` | 52 |
| `bug_fix` | 32 |
| `understanding` | 15 |
| `plan` | 10 |

## RQ6 — Failures encountered

Out of **263 tool results**, **38** (14.4%) contained an error signature.

The user filed **3 bug-report-style prompt(s)** (prompts containing words like 'error', 'crash', 'broken', 'wrong').

## RQ6b — Difficulty assessment

**Auto-label: `High`** (difficulty index 0.55; mean rank across 7 signals = 9.3).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 0.9 | 6.0 |
| Calendar span (days first→last event) | 34 | 15.0 |
| User prompts | 10 | 4.0 |
| Redirect / bug-report prompts | 3 | 7.5 |
| Tool-output error rate | 0.144 | 14.0 |
| Fix cycles (error → immediate retry) | 5 | 11.5 |
| Share of active time spent on `bug_fix` | 0.004 | 7.0 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 10
- **Average prompt length:** 1054 chars; **max:** 4,269 chars
- **Total chars written by user:** 10,536
- **Sessions:** 3; **span:** 34 days
- **Long-prompt ratio** (≥500 chars): 5/10

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Codex | `gpt-5.4` | 2026-03-12 20:18 | 10d 17h 9m | 8 | 237 | $4.16 |
| 2 | Claude Code | `claude-opus-4-6` | 2026-03-19 15:50 | 22h 34m | 4 | 42 | $24.73 |
| 3 | Codex | `gpt-5.4` | 2026-04-16 09:58 | 2m 37s | 1 | 26 | $0.20 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| bug-report | 3 |
| review-ask | 2 |
| other | 2 |
| clarify | 2 |
| initial-spec | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-03-12]_ # COBPACK — MVP0 Specification (GNUCobol) ## Goal (MVP0) Build a command-line tool `cobpack` that can: 1. **Package** a fixed-length record file into a `.cpc` container (field-wise / columnar layout) using only the `NONE` codec (no compress…
2. _[2026-03-12]_ # COBPACK — MVP1 Specification (adds real compression) ## Goal (MVP1) Extend MVP0 by adding one codec: **RLESP** (space-run encoding for 0x20). Keep backward compatibility with CPC v0. MVP1 proves the agent can implement a **non-trivial alg…
3. _[2026-03-12]_ <turn_aborted> The user interrupted the previous turn on purpose. Any running unified exec processes were terminated. If any tools/commands were aborted, they may have partially executed; verify current state before retrying. </turn_aborted…
4. _[2026-03-12]_ # COBPACK — MVP1 Specification (adds real compression) ## Goal (MVP1) Extend MVP0 by adding one codec: **RLESP** (space-run encoding for 0x20). Keep backward compatibility with CPC v0. MVP1 proves the agent can implement a **non-trivial alg…
5. _[2026-03-12]_ Produce a TRUST.md and extend the test suite to justify trust in COBPACK MVP1. I want: (a) determinism proof-by-test, (b) randomized round-trip testing with generated schemas/records, (c) corruption/fuzz tests that ensure predictable failur…
6. _[2026-03-20]_ is it possible to have a decompress(compress(x)) == x kind of test?
7. _[2026-03-23]_ can you create a git, commit and push on Github repo (to be created) agentic-cobol-compress?
8. _[2026-03-23]_ done for browser step...
9. _[2026-03-23]_ public
10. _[2026-04-16]_ the thread of Codex session is not visible in the left-hand side of Codex app... can you analyze history/sessions of this folder, and report on user prompts used?

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 10d 17h 12m |
| Active collaboration time | 54m 56s |
| Tool calls | 263 |
| Input tokens | 677,810 |
| Output tokens | 145,816 |
| Cache-read tokens | 16,413,312 |
| Cache-create tokens | 0 |
| Reasoning tokens (Codex) | 73,872 |
| Estimated cost at API rack rates | $4.36 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `exec_command` | 183 |
| `apply_patch` | 60 |
| `write_stdin` | 15 |
| `update_plan` | 5 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
