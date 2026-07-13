# Post-session analysis — `cobol-jb`

> Meta-analysis of the `cobol-jb` Claude Code sessions. The project folder `/Users/mathieuacher/SANDBOX/cobol-jb` is treated as **read-only evidence**. All artefacts here belong to this output directory. See [`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md) for the agent-centric step-wise backlog and [`appendix.json`](appendix.json) for the machine-readable appendix. A combined Phase-0 / PASS-1 / PASS-2 narrative with rubric scoring lives in [`REPORT.md`](REPORT.md).

## Project overview

`cobol-jb` is a **GnuCOBOL payroll management case-study** used in a PhD research programme on legacy-modernisation with AI agents. The agent (Claude Code v2.1.91, `claude-opus-4-6`) was prompted to (i) generate a complete COBOL batch program from scratch, (ii) evolve it twice (social contributions, then input validation + reject file), and (iii) in a second session, self-verify the result against a 27-criterion grid.

Two sessions on disk (2026-04-03):

- `434a5a96-69b6-43bb-b0dc-dbccafc2ee29.jsonl` — feature-building (14:45 → 15:59)
- `3fa13850-2149-4f81-ac43-899fba3d4ef5.jsonl` — verification + publish (15:46 → 11:03 the next morning; long idle gap before final push/rebase)

Primary language: **COBOL** (1 source file, `program.cbl`, 705 LOC).

## Feature Backlog (user-driven)

| ID | Title | Type | UI | PL | DoD | Commit |
|---|---|---|---|---|---|---|
| BL-001 | Base COBOL payroll program (reads employees, computes gross salary with category-based overtime, writes payslips, prints summary) | Feature | UI-001 | PL-ROOT | Yes | `b4c6c66` |
| BL-002 | Social-contribution deductions (health 7.30%, retirement 6.90%, unemployment 2.40%) + net salary + extended totals | Feature | UI-003 | PL-001 | Yes | `a566a9e` |
| BL-003 | Input validation (ERR-001…ERR-004) + reject file `rejects_output.dat` + valid/rejected counters | Feature | UI-005 | PL-002 | **Partial** — code complete, but README not updated (criterion #27 fail) | `704baa8` |
| BL-004 | Self-applied verification report (27-criterion grid → `VERIFICATION_REPORT.md`, 25/27) | Documentation / Test | UI-007 | PL-003 | Yes | `71d46f1` |

No other BL items: remaining user turns were Ops (commits + push + rebase) or clarifications, all captured under OP-### in `SPECIFICATION_BACKLOG.md`.

### Human User Instruction Index (UII)

| ID | Session / line | Quote (≤25w) / paraphrase | Category | Strength | Target | → BL |
|---|---|---|---|---|---|---|
| UI-001 | 434a5a96:L5 | "You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program. … Domain: Payroll management system" | FeatureRequest + Constraint | Explicit imperative | Code | BL-001 |
| UI-002 | 434a5a96:L63 | "create a git and commit" | Tooling / Ops | Explicit imperative | Repo structure | OP-001 (not a BL) |
| UI-003 | 434a5a96:L86 | "Add social contribution deductions to the payroll calculation." (+ rates, output fields, totals) | FeatureRequest | Explicit imperative | Code | BL-002 |
| UI-004 | 434a5a96:L130 | "please commit (incl. update of README)" | Tooling / Docs | Explicit imperative | Repo + Docs | OP-002 + nudges BL-002 DoD |
| UI-005 | 434a5a96:L155 | "Add input data validation with a dedicated reject file for invalid records." (+ 4 rules, counters) | FeatureRequest + AcceptanceCriteria | Explicit imperative | Code | BL-003 |
| UI-006 | 434a5a96:L227 | "please commit" | Tooling | Explicit imperative | Repo | OP-003 |
| UI-007 | 3fa13850:L3 | "look at the current repo … grid to objectively verify whether the agent produced equivalent results" | TestRequest / AcceptanceCriteria | Explicit imperative | Runtime + Docs | BL-004 |
| UI-008 | 3fa13850:L30 | "please commit this report" | Tooling | Explicit imperative | Repo | OP-004 |
| UI-009 | 3fa13850:L47 | "please push on Github in this fork repo: https://github.com/acherm/cobol-agentic-dev-case-studies" | Tooling / Ops | Explicit imperative | Repo remote | OP-005 |
| UI-010 | 3fa13850:L58 | "push in the main, not master" | ScopeChange | Explicit imperative | Repo remote | OP-005 |
| UI-011 | 3fa13850:L67 | "I want to keep history" | Constraint | Explicit imperative | Repo remote | OP-005 |

### Project Constraints Index (PCI)

| ID | Source | Paraphrase | Type | Impact |
|---|---|---|---|---|
| PC-001 | `[R:case-study-1.md]` | Fixed-variable case-study protocol (LOC=300, compiler `cobc -x -free -o program program.cbl`, required COBOL patterns, file names) | repo policy | Shapes `PL-ROOT`, `PL-001`, `PL-002` verbatim |
| PC-002 | `[R:case-study-1/.agents/skills/cobol-backlog-writer/SKILL.md]` | "Backlog extractor skill" referenced in the prompts ("run the backlog extractor skill to generate README.md") | tooling | Explains the agent's step-6 README authoring reflex |
| PC-003 | `[R:.gitignore]` | Ignore compiled binary `program` + OS artefacts | build | Agent re-opened and extended during Step-2 |

## Prompt Ledger summary

### `PL-ROOT` — initial from-scratch prompt

**Raw** (evidence `[T:434a5a96:L5]`) — excerpt ≤25 words:
> "You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program. Domain: Payroll management system."

**Canonical replay prompt** (clean / minimal / complete):
```
Role: Mainframe COBOL expert. Produce a single self-contained COBOL source program named `program.cbl`.

Target: GnuCOBOL. Must compile with: cobc -x -free -o program program.cbl

Scope:
- Domain: Payroll management.
- ~300 LOC (no comment-padding).
- Two files: employees_input.dat (input), payslips_output.dat (output).
- Must use: PERFORM, EVALUATE, FILE SECTION (FD entries), COMPUTE, 88-level condition names.

Business logic:
1. Read employee records: ID, name, job category (A/B/C), hours worked, hourly rate.
2. Compute gross salary = hours * rate, with overtime bonus (hours > 35) via EVALUATE:
   A → +20%, B → +10%, C → 0%.
3. Write one formatted payslip per employee.
4. Print end-of-job totals (#employees, total gross).

Process:
1. Write `program.cbl`.
2. Compile with the command above; iterate until exit code 0 and no errors.
3. Run `./program` once to confirm it produces `payslips_output.dat`.
4. Generate a `README.md` documenting the program (build, run, input layout, business logic, example output).
```

### Per-BL prompts

| BL | `PL-###` | Raw (≤25 words) + pointer | Canonical replay prompt |
|---|---|---|---|
| BL-001 | `PL-ROOT` | see above | see above |
| BL-002 | `PL-001` `[T:434a5a96:L86]` | "Add social contribution deductions … Health 7.30%, Retirement 6.90%, Unemployment 2.40%" | "Modify `program.cbl`: add health (7.30%), retirement (6.90%), unemployment (2.40%) deductions on gross; compute net = gross − total-deduction; enrich payslip record with all 4 values; display total gross + total net at end of job. Recompile cleanly with `cobc -x -free -o program program.cbl` and update `README.md`." |
| BL-003 | `PL-002` `[T:434a5a96:L155]` | "Add input data validation with a dedicated reject file for invalid records … Rules ERR-001..004" | "Modify `program.cbl`: before processing, validate each record: ERR-001 ID not zero/spaces; ERR-002 hours ∈ (0, 80]; ERR-003 rate ∈ (0, 999.99]; ERR-004 category ∈ {A,B,C}. Invalid records skip salary math and are written to a 3rd FD `rejects_output.dat` (OPEN OUTPUT) with the original record + error code. End-of-job totals must show valid count, rejected count, total gross, total net. Recompile cleanly; update `README.md`." |
| BL-004 | `PL-003` `[T:3fa13850:L3]` | "look at the current repo … grid to objectively verify whether the agent produced equivalent results" | "Without modifying `program.cbl`, apply the 27-item verification grid (case-study-1.md §5) to the current repo. Recompile to confirm exit 0, then populate the grid (PASS/FAIL + evidence). Output `VERIFICATION_REPORT.md` with the per-step breakdown and a final score out of 27." |

## Reproduction instructions

Preconditions: macOS or Linux; GnuCOBOL `cobc` ≥ 3.2 on `$PATH`.

```
# 1. Start from empty workspace
mkdir cobol-jb && cd cobol-jb

# 2. BL-001 — submit PL-ROOT canonical prompt to Claude Code
#    Expect: program.cbl + README.md + employees_input.dat

# 3. Validate
cobc -x -free -o program program.cbl   # exit 0, no errors (warnings OK)
./program                               # produces payslips_output.dat + summary on stdout
# Checkpoint BL-001: program.cbl compiles; payslips_output.dat non-empty; README.md exists.

# 4. BL-002 — submit PL-001 canonical prompt
cobc -x -free -o program program.cbl
./program
# Checkpoint BL-002: source contains 0.0730 / 0.0690 / 0.0240 (or 7.30/6.90/2.40); NET field present; totals include "Total Net Payroll".

# 5. BL-003 — submit PL-002 canonical prompt
cobc -x -free -o program program.cbl
./program
# Checkpoint BL-003: 3 FD entries; ERR-001..004 strings present; rejects_output.dat written; "Employees Rejected" counter displayed.

# 6. BL-004 — submit PL-003 canonical prompt
# Checkpoint BL-004: VERIFICATION_REPORT.md lists 27 rows; final score reported.
```

Commit checkpoints (observed on disk):

| BL | Commit | Snapshot files |
|---|---|---|
| BL-001 | `[G:b4c6c66]` | `program.cbl`, `README.md`, `employees_input.dat`, `.gitignore` |
| BL-002 | `[G:a566a9e]` | `program.cbl`, `README.md` |
| BL-003 | `[G:704baa8]` | `program.cbl`, `employees_input.dat`, `.gitignore` |
| BL-004 | `[G:71d46f1]` | `VERIFICATION_REPORT.md` |

## Repo stats (A5) — `[S:stats_run_1]`

Scope: working tree of `/Users/mathieuacher/SANDBOX/cobol-jb` at HEAD `4b148bc` (post-rebase). Excludes `.git/`. Duplicates in `case-study-1/` (an evidence snapshot from a different fork/run) are listed separately.

**Top-level (production)**:

| File | Kind | Lines |
|---|---|---|
| `program.cbl` | production code (COBOL) | 705 |
| `program` | compiled binary (not tracked) | — |
| `employees_input.dat` | data / example | 12 |
| `payslips_output.dat` | generated data | 180 |
| `rejects_output.dat` | generated data | 4 |
| `README.md` | docs | 111 |
| `case-study-1.md` | docs (prompt spec) | 346 |
| `VERIFICATION_REPORT.md` | docs (test report) | 57 |
| `.gitignore` | config | ≤ a few lines |

**`case-study-1/` subfolder (evidence snapshot from a different session)**:

| File | Kind | Lines |
|---|---|---|
| `case-study-1/program.cbl` | snapshot | 395 |
| `case-study-1/README.md` | snapshot | (docs) |
| `case-study-1/session-ses_2b16.md` | session transcript | 222,331 bytes |
| `case-study-1/.agents/skills/cobol-backlog-writer/SKILL.md` | tooling | — |
| `case-study-1/{employees,payslips,rejects}_*.dat` | snapshot data | small |

**Language breakdown (top level)**:

| Language | #files | LOC |
|---|---|---|
| COBOL (`.cbl`) | 1 | 705 |
| Markdown (`.md`) | 3 | 514 |
| Data (`.dat`) | 3 | 196 |
| Config (`.gitignore`) | 1 | ~3 |

**Program-kind classification (top level)**:

| Kind | Count | LOC |
|---|---|---|
| Production code | 1 | 705 |
| Tests | 0 | 0 |
| Build/tooling | 1 (`.gitignore`) | ~3 |
| Docs | 3 | 514 |
| Data/examples | 3 | 196 |

**Entry points**: main = `program.cbl` (PROGRAM-ID `PAYROLL-SYSTEM`); build = `cobc -x -free -o program program.cbl`; run = `./program`; no test runner.

## Session-level interaction metrics

| Metric | Session 434a5a96 (build) | Session 3fa13850 (verify + publish) |
|---|---|---|
| Duration (first→last event) | 2026-04-03 14:45 → 15:59 (~74 min) | 2026-04-03 15:46 → 2026-04-04 11:03 (long idle) |
| Human user turns | 6 | 5 |
| Assistant turns | 126 | 44 |
| Bash tool uses | 31 | 18 |
| Edit tool uses | 25 | 0 |
| Write tool uses | 6 | 3 |
| Read tool uses | 6 | 4 |
| Grep tool uses | 6 | 0 |
| Glob tool uses | 0 | 1 |
| tool_result events | 74 | 26 |
| User prompts per BL | BL-001: 1, BL-002: 1, BL-003: 1, Ops: 3 | BL-004: 1, Ops: 4 |

Key failure / recovery observations from session evidence:

- Session 434a5a96 event L19/20: first `cobc` run exited 97 with `'WS-EMP-FILE-STATUS' is not defined` plus PROCEDURE DIVISION missing → agent edited the program once (L23) and the next compile (L25) succeeded with no output (clean). DBG loop count for BL-001 = **1**.
- BL-002 and BL-003 compiled cleanly on first attempt (L119, L191 emitted no errors). DBG loops = 0.
- Session 3fa13850 event L71/72: a `git rebase origin/main master` produced 2 `add/add` conflicts in `.gitignore` + `README.md`; agent resolved by writing consolidated versions (L80, L83), ran `rebase --continue` (L86), then `git push origin master:main`. Ops, not a feature.

## Specification Backlog

See [`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md) — 33 SB entries, step-segmented by the four meaningful commits, with provenance labels (User-driven / Agent-initiated / Required prerequisite) and one documented gap (SB-030b).

## Repro Ops (non-feature)

See the **Reproducibility Ops** section inside `SPECIFICATION_BACKLOG.md` (OP-001 … OP-005). Ops are kept out of the Feature Backlog per master-template rules.

## Limitations / missing evidence

- `case-study-1/session-ses_2b16.md` inside the project folder looks like a different session from another experiment run (Claude.ai web?) and is NOT one of the two pre-identified JSONLs; we treat it as evidence-context only and do not harvest prompts from it.
- The second session has a ~19-hour gap between the verification-commit turn (2026-04-03T15:54) and the final push/rebase turn (2026-04-04T11:03). We treat it as a single logical session per the per-project prompt.
- No automated test suite exists. Validation is (i) GnuCOBOL compile exit code, (ii) visual inspection of `payslips_output.dat` / `rejects_output.dat`, (iii) the 27-criterion grid in `VERIFICATION_REPORT.md`. Rubric scores reflect this (see `REPORT.md`).
- `program.cbl` is 705 LOC — ~2× the `PL-ROOT` LOC target (250–350). The VERIFICATION_REPORT flags this as criterion #3 FAIL; not a blocker for functional DoD.
- BL-003 has a **partial DoD**: criterion #27 (README update after Step 2) was missed; agent (in STEP-3) self-detected the gap in the verification report.
- CP1, CP2, CP3 questions were not asked (no human available); defaults were applied per master template.
