# `COMPRESS-COBOL-CLAUDE` — Case Study (repository folder `cobol-compress-cobolcc`)

> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`](../backlogs/cobol-compress-cobolcc/STORY.md)  
> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`cobol-compress-cobolcc` assessment](../assessments/cobol-compress-cobolcc.md)  
> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`](../backlogs/cobol-compress-cobolcc/SPECIFICATION_BACKLOG.md)
  
> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`](../backlogs/cobol-compress-cobolcc/KEY_FEATURES.md)

**Project root.** `/Users/mathieuacher/SANDBOX/cobol-compress-cobolcc`  
**Sessions.** 1 (1 Claude Code + 0 Codex)  
**Activity window.** 2026-04-16 → 2026-04-17 (1 days)  
**Agents & models.** Claude Code/claude-opus-4-6

---

## RQ1 — Domain, intent, novelty

**What it is.** COBPACK — columnar compressor for fixed-record COBOL data (Claude-Code-built, pure COBOL) — second-agent replica of the COBPACK domain.

**Why it's interesting.** Cross-agent replication of the COBPACK specification with Claude Code; closes the 2-agent gap for the columnar-compressor domain. Three separate COBOL source files (cobpack + crc32 + rlesp).

**Opening prompt that kicked off the project:**

```
# COBPACK — MVP0 Specification (GNUCobol) ## Goal (MVP0) Build a command-line tool `cobpack` that can: 1. **Package** a fixed-length record file into a `.cpc` container (field-wise / columnar layout) using only the `NONE` codec (no compression). 2. **Unpack** that `.cpc` back into the original file **byte-identical**. 3. Provide `info` about the container. Implement a solution in COBOL, write COBOL programs, don't write a C driver or any workaround. You can use other programming languages for instrumenting the test infrastructure, but really the goal is to have a COBOL-based implementation. This MVP0 proves: * toolchain mastery in COBOL (multi-file build, binary-safe I/O), * schema parsing, * container serialization/deserialization, * round-trip correctness, with minimal algorithmic risk. …
```

## RQ2 — Engineering challenges

**Sub-challenges that a human engineer would have to solve (derived from the domain):**

- schema parser
- CPC v0/v1 container format
- NONE + RLESP codecs
- CRC32 integrity
- determinism + round-trip trust suite
- multi-file COBOL build

_No explicit error signatures were detected in tool outputs — either the project compiled cleanly or error text was in a format the detector missed._

## RQ2b — Feature ledger (what was actually built)

Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.

| Source | Items |
|---|---:|
| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **11** |
| `README.md` / `REPORT.md` bullet lists under a Features heading | 0 |
| Bullet / numbered sub-requests inside user prompts | 62 |
| Git commit subjects | 1 |

**Backlog (11 F-### entries).** Grouped by phase:

- **_unclassified_** — 11 features  
  Toolchain Validation; Main CLI Program with CPC v0 Container (cobpack.cob); RLESP Codec as Separate Subprogram (rlesp.cob); CRC32 as Separate Subprogram (crc32.cob); Build Script (multi-file compilation); Test Harness and Fixtures; Randomized Round-Trip Fuzz; Corruption Fuzz _(+3 more)_

**Prompt-extracted sub-requests (62)** — first 8 (sub-bullets inside user messages):

- _[2026-04-16]_ toolchain mastery in COBOL (multi-file build, binary-safe I/O),
- _[2026-04-16]_ schema parsing,
- _[2026-04-16]_ container serialization/deserialization,
- _[2026-04-16]_ round-trip correctness,
- _[2026-04-16]_ `--in input.dat`: binary file with `N` records of exactly `RECORD_LEN` bytes
- _[2026-04-16]_ Validation: file size must be a multiple of `RECORD_LEN`, else error.
- _[2026-04-16]_ `RECORD_LEN=<integer>`
- _[2026-04-16]_ `FIELD <NAME> <OFFSET> <LENGTH> <TYPE>`

**Git commits (1)** — first 8:

- `f0fe4e9697` 2026-04-17  Initial cobpack implementation: MVP0 + MVP1 + trust suite

## RQ3 — What was delivered

**From `TRUST.md`:**

> **# TRUST.md — COBPACK MVP1**  
> This document justifies trust in `cobpack`. It lists the properties the tool promises, shows which test in `run_tests.sh` proves each one, and explains how to reproduce the evidence. If you change the container format or a codec, the tests below must be updated in lock-step. `./run_tests.sh` (after `./build.sh`) runs the whole suite. It finishes in **under 10 seconds on a modern laptop** and under 2 minutes even on modest hardware; nothing in the suite is slow or flaky. ---

> **## 1. Claims and how they are tested**  
> 

**Executables present in the root of the project** (evidence that something builds):

- `cobpack` (86 KB)

## RQ4 — Size and complexity

**File inventory** (24 files, 0.2 MB).

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 3 | 2,126 |
| Python | 4 | 516 |
| Shell | 2 | 323 |
| Markdown | 1 | 215 |

**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):

| Metric | Value |
|---|---:|
| COBOL files | 3 |
| Total lines | 2,126 |
| Code lines (non-blank, non-comment) | 1,819 |
| Comment lines | 188 |
| Sections | 10 |
| Paragraphs | 74 |
| Data items (level-number declarations) | 209 |
| Max IF/EVALUATE nesting (any file) | 4 |

**COBOL statement frequency (top 10):**

| Statement | Count |
|---|---:|
| `MOVE` | 388 |
| `IF` | 147 |
| `PERFORM` | 121 |
| `EXIT` | 105 |
| `DISPLAY` | 93 |
| `ADD` | 55 |
| `COMPUTE` | 48 |
| `SET` | 33 |
| `CALL` | 23 |
| `EVALUATE` | 8 |

**Largest COBOL files:**

| File | Code lines |
|---|---:|
| `src/cobpack.cob` | 1,537 |
| `src/rlesp.cob` | 203 |
| `src/crc32.cob` | 79 |

**Git churn signal.** 1 commits, 3239 insertions / 0 deletions, first 2026-04-17, last 2026-04-17.

## RQ4b — COBOL language mastery

**Mastery score:** **50** distinct COBOL constructs used across **10/10** capability categories (a pure "Hello World" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).

| Category | Exercised? | Total occurrences | Distinct constructs seen |
|---|:---:|---:|---|
| **control_flow** <br/>_branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)_ | ✓ | 745 | `IF`×294, `EXIT`×161, `PERFORM`×158, `PERFORM_UNTIL`×36, `WHEN`×33, `PERFORM_VARYING`×21, `EVALUATE`×16, `ELSE`×15 _(+3 more)_ |
| **arithmetic** <br/>_numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)_ | ✓ | 109 | `ADD`×57, `COMPUTE`×47, `DIVIDE`×3, `SUBTRACT`×2 |
| **data_advanced** <br/>_rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)_ | ✓ | 319 | `PIC_9`×111, `USAGE_COMP_5`×105, `PIC_X`×56, `USAGE_BINARY`×16, `REDEFINES`×11, `USAGE_POINTER`×11, `LEVEL_77`×6, `OCCURS`×3 |
| **io_file** <br/>_FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations_ | ✓ | 45 | `START`×15, `READ`×12, `WRITE`×9, `OPEN_INPUT`×2, `CLOSE`×2, `FD`×1, `SELECT`×1, `ASSIGN`×1 _(+2 more)_ |
| **string_ops** <br/>_STRING/UNSTRING/INSPECT, reference modification `var(a:b)`_ | ✓ | 40 | `REFERENCE_MOD`×35, `STRING`×3, `DELIMITED_BY`×2 |
| **tables_search** <br/>_SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE_ | ✓ | 33 | `SET`×33 |
| **subprograms** <br/>_CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE_ | ✓ | 80 | `CALL`×46, `USING`×26, `LINKAGE_SECTION`×4, `BY_VALUE`×4 |
| **copy_preproc** <br/>_COPY books, REPLACING / REPLACE_ | ✓ | 13 | `COPY`×13 |
| **intrinsics** <br/>_FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)_ | ✓ | 87 | `FUNCTION`×46, `FUNCTION_TRIM`×29, `FUNCTION_NUMVAL`×8, `FUNCTION_MOD`×2, `FUNCTION_LOWER`×1, `FUNCTION_LENGTH`×1 |
| **misc** <br/>_DISPLAY / ACCEPT / STOP literal_ | ✓ | 101 | `DISPLAY`×93, `ACCEPT`×8 |

**Notable non-trivial constructs used:** `CALL` (46×), `OCCURS` (3×), `REDEFINES` (11×), `USAGE_COMP_5` (105×), `COPY` (13×), `FD` (1×), `FUNCTION` (46×).

**Procedural structure.** 74 paragraphs, 10 sections across 3 COBOL file(s). That means roughly **74 function-like units** (every paragraph is a PERFORM-able entry point; a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).

## RQ5 — SE-task breakdown (how effort was spent)

Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). Total **active** collaboration time for this project: **1m 2s** across 4 events.

SE-task labels are assigned to every event with the following logic:
- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);
- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.

| SE task | Meaning | Active time | Share |
|---|---|---:|---:|
| `build` | compile / makefile / dependency work | 0m 56s | 90.3% |
| `understanding` | reading / searching to build a mental model | 0m 6s | 9.7% |

**Tool calls by SE task:**

| SE task | Tool calls |
|---|---:|
| `build` | 1 |

## RQ6 — Failures encountered

Out of **1 tool results**, **0** (0.0%) contained an error signature.

## RQ6b — Difficulty assessment

**Auto-label: `Low`** (difficulty index 0.08; mean rank across 7 signals = 2.2).

The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':

| Signal | This project | Rank (1=lowest across 11 projects) |
|---|---:|---:|
| Active hours (collaboration time) | 0.0 | 1.0 |
| Calendar span (days first→last event) | 1 | 7.5 |
| User prompts | 1 | 1.0 |
| Redirect / bug-report prompts | 0 | 2.0 |
| Tool-output error rate | 0.000 | 1.0 |
| Fix cycles (error → immediate retry) | 0 | 1.5 |
| Share of active time spent on `bug_fix` | 0.000 | 1.5 |

_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._

## RQ7 — User strategy

- **User prompts total:** 1
- **Average prompt length:** 7285 chars; **max:** 7,285 chars
- **Total chars written by user:** 7,285
- **Sessions:** 1; **span:** 1 days
- **Long-prompt ratio** (≥500 chars): 1/1

| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2026-04-16 05:42 | 1d 10h 48m | 7 | 136 | $129.48 |

## RQ8 — User interventions (prompt typology)

| Intent class | Prompts |
|---|---:|
| initial-spec | 1 |

**Prompt ledger — first 10 user prompts (truncated):**

1. _[2026-04-16]_ # COBPACK — MVP0 Specification (GNUCobol) ## Goal (MVP0) Build a command-line tool `cobpack` that can: 1. **Package** a fixed-length record file into a `.cpc` container (field-wise / columnar layout) using only the `NONE` codec (no compress…

## RQ9 — Compute & cost

| Metric | Value |
|---|---:|
| Wall-clock session span (sum, incl. idle) | 1d 10h 48m |
| Active collaboration time | 1m 2s |
| Tool calls | 136 |
| Input tokens | 486 |
| Output tokens | 550,583 |
| Cache-read tokens | 37,422,175 |
| Cache-create tokens | 1,708,980 |
| Reasoning tokens (Codex) | 0 |
| Estimated cost at API rack rates | $129.48 |

### Appendix — tool call breakdown

| Tool | Calls |
|---|---:|
| `Bash` | 1 |

---

_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._
