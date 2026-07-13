# SPECIFICATION_BACKLOG — `cobol-jb`

Agent-centric, step-wise backlog of what the coding agent (Claude Code, `claude-opus-4-6`, v2.1.91) actually implemented in the `cobol-jb` project (GnuCOBOL payroll case-study). Companion artefact to [`README.md`](README.md) in this output directory. The canonical project folder (read-only evidence) is `/Users/mathieuacher/SANDBOX/cobol-jb`.

## Purpose

SB items capture the incremental implementation work (capabilities, quality/hardening, tooling, documentation, validation) observed across the two Claude Code session JSONLs and the four project git commits. They are labelled with provenance:

- **User-driven** — maps to an explicit user instruction (`UI-###`) / prompt (`PL-###`) / feature backlog item (`BL-###`).
- **Agent-initiated** — not explicitly requested, added by the agent (reasonable extrapolation or internal housekeeping).
- **Required prerequisite** — strictly necessary to satisfy an explicit user acceptance criterion.

## Step segmentation

Priority order (master template): (1) git commits → (2) session episodes → (3) INFERRED. This project has a clean commit chain, so commits are used as primary steps.

| Step | Commit | Title (commit subject) | Session evidence |
|---|---|---|---|
| STEP-0 | `b4c6c66` | Add COBOL payroll management system | session 434a5a96 — `PL-ROOT` (2026-04-03T14:45) through `git commit` (T15:33) |
| STEP-1 | `a566a9e` | Add social contribution deductions to payroll calculation | session 434a5a96 (T15:34 → T15:39) |
| STEP-2 | `704baa8` | Add input validation with reject file for invalid records | session 434a5a96 (T15:40 → T15:44) |
| STEP-3 | `71d46f1` | Add verification report scoring 25/27 on case study reproduction | session 3fa13850 (T15:46 → T15:54) |
| STEP-4 | `22a3d0d / cf26a12 / ad841ed / ca7cf7a / 4b148bc` | rebase onto `origin/main` (fork alignment) | session 3fa13850 (T15:56 → T15:59) — **Ops, non-feature** |

Step segmentation limitation: the rebase chain (STEP-4) consists of a single logical publishing action — it is captured as one `OP-###` in the Ops section below, NOT as an SB capability.

## SB table

| ID | Step | Title | Category | Provenance | Maps to |
|---|---|---|---|---|---|
| SB-001 | STEP-0 | COBOL payroll program skeleton (IDENTIFICATION/ENVIRONMENT/DATA/PROCEDURE divisions) | Capability | User-driven | BL-001, UI-001, PL-ROOT |
| SB-002 | STEP-0 | File I/O: `FD EMPLOYEE-FILE` + `FD PAYSLIP-FILE`, `OPEN INPUT/OUTPUT`, line-sequential records | Capability | User-driven | BL-001, UI-001 |
| SB-003 | STEP-0 | `PERFORM UNTIL` main processing loop over employee records | Capability | User-driven | BL-001, UI-001 |
| SB-004 | STEP-0 | `EVALUATE` branch applying category-based overtime bonus (A +20%, B +10%, C 0%) | Behavior | User-driven | BL-001, UI-001 |
| SB-005 | STEP-0 | `COMPUTE` arithmetic for gross salary = regular + overtime pay | Capability | User-driven | BL-001, UI-001 |
| SB-006 | STEP-0 | 88-level condition names (`CATEGORY-A/B/C`, `END-OF-FILE`) | Quality/Hardening | User-driven | BL-001, UI-001 |
| SB-007 | STEP-0 | Formatted payslip output record + header/separator lines | Capability | User-driven | BL-001, UI-001 |
| SB-008 | STEP-0 | End-of-job totals display (employees processed, total gross payroll) | Capability | User-driven | BL-001, UI-001 |
| SB-009 | STEP-0 | Compile-error recovery: undefined `WS-*-FILE-STATUS` fields added after first `cobc` run exited 97 | Quality/Hardening | Required prerequisite | BL-001 (acceptance criterion: "compile without errors") |
| SB-010 | STEP-0 | Sample `employees_input.dat` authored (8 valid employee records across categories A/B/C) | Test/Validation | Agent-initiated | BL-001 (used to exercise `./program` end-to-end) |
| SB-011 | STEP-0 | Run validation: `./program` executes cleanly and produces `payslips_output.dat` | Test/Validation | Required prerequisite | BL-001 |
| SB-012 | STEP-0 | `README.md` initial authoring (project overview, build/run instructions, business logic table) | Documentation | User-driven (process step 6 of `PL-ROOT`) | BL-001 |
| SB-013 | STEP-0 | `.gitignore` created to exclude compiled binary `program` + OS artefacts | Tooling | Agent-initiated | — |
| SB-014 | STEP-0 | Git repo initialised + initial commit `b4c6c66` | Tooling | User-driven | UI-002, OP-001 |
| SB-015 | STEP-1 | `WORKING-STORAGE` extended with social-contribution rate constants (`0.0730`, `0.0690`, `0.0240`) | Capability | User-driven | BL-002, UI-003 |
| SB-016 | STEP-1 | `COMPUTE` deductions (health, retirement, unemployment) + net salary = gross - total-deduction | Behavior | User-driven | BL-002, UI-003 |
| SB-017 | STEP-1 | Payslip output record enriched (13+ fields inc. gross, 3 deductions, total deduction, net) | Capability | User-driven | BL-002, UI-003 |
| SB-018 | STEP-1 | End-of-job totals extended: total net payroll alongside total gross | Capability | User-driven | BL-002, UI-003 |
| SB-019 | STEP-1 | Re-compile + re-run validation (cleanly produces new payslips file) | Test/Validation | Required prerequisite | BL-002 |
| SB-020 | STEP-1 | `README.md` update (social-contributions table, new example payslip, extended fields table) | Documentation | User-driven | BL-002 (user asked "incl. update of README") / UI-004 |
| SB-021 | STEP-1 | Git commit `a566a9e` (`README.md` + `program.cbl`) | Tooling | User-driven | UI-004, OP-002 |
| SB-022 | STEP-2 | 3rd `FD REJECT-FILE` assigned to `rejects_output.dat`, opened `OUTPUT` | Capability | User-driven | BL-003, UI-005 |
| SB-023 | STEP-2 | Validation predicates with error codes `ERR-001…ERR-004` (ID, hours, rate, category) | Behavior | User-driven | BL-003, UI-005 |
| SB-024 | STEP-2 | Reject writing: invalid records routed to reject file with original data + error code | Capability | User-driven | BL-003, UI-005 |
| SB-025 | STEP-2 | Guard: invalid records skip salary/deduction processing (preserves Step-0/1 math) | Quality/Hardening | User-driven | BL-003, UI-005 |
| SB-026 | STEP-2 | End-of-job totals extended: `Employees Rejected` + `Errors Encountered` counters | Capability | User-driven | BL-003, UI-005 |
| SB-027 | STEP-2 | Sample `employees_input.dat` regenerated to include 4 invalid rows exercising ERR-001…004 | Test/Validation | Agent-initiated | BL-003 (demonstrates each rule fires) |
| SB-028 | STEP-2 | Re-compile + run validation (4 rejects observed on screen, reject file written) | Test/Validation | Required prerequisite | BL-003 |
| SB-029 | STEP-2 | `.gitignore` amended (ignores additional runtime artefacts) | Tooling | Agent-initiated | — |
| SB-030 | STEP-2 | Git commit `704baa8` (`program.cbl` + `.gitignore` + `employees_input.dat`) | Tooling | User-driven | UI-006, OP-003 |
| SB-030b | STEP-2 | **Missed update**: `README.md` not updated to document validation/reject feature (criterion #27 fail) | Documentation (GAP) | Agent-gap | BL-003 (partial DoD) |
| SB-031 | STEP-3 | `VERIFICATION_REPORT.md` authored: 27-criterion evaluation grid self-applied, 25/27 score | Documentation | User-driven | BL-004, UI-007 |
| SB-032 | STEP-3 | Evidence-collection tool calls: `cobc` recompile, `wc -l`, `git log --oneline -- README.md`, `git show` to attribute criterion #27 failure | Test/Validation | User-driven | BL-004 |
| SB-033 | STEP-3 | Git commit `71d46f1` (`VERIFICATION_REPORT.md`) | Tooling | User-driven | UI-008, OP-004 |

## Feature-level Backlog mapping

| BL | Commit | SB items implementing it |
|---|---|---|
| BL-001 (Base payroll program) | `b4c6c66` | SB-001…SB-014 |
| BL-002 (Social contribution deductions) | `a566a9e` | SB-015…SB-021 |
| BL-003 (Input validation + reject file) | `704baa8` | SB-022…SB-030, SB-030b (gap) |
| BL-004 (Self-verification report) | `71d46f1` | SB-031…SB-033 |

## Reproducibility Ops (non-feature)

These are the **explicit** user requests for git / repo-publishing operations. They are OUT OF SCOPE for the Feature Backlog but traced here for replay completeness.

| ID | Title | User instruction | Evidence |
|---|---|---|---|
| OP-001 | Init repo + initial commit | UI-002 "create a git and commit" | `[T:434a5a96:L63]`, commit `b4c6c66` |
| OP-002 | Commit Step-1 changes (+ README) | UI-004 "please commit (incl. update of README)" | `[T:434a5a96:L130]`, commit `a566a9e` |
| OP-003 | Commit Step-2 changes | UI-006 "please commit" | `[T:434a5a96:L227]`, commit `704baa8` |
| OP-004 | Commit verification report | UI-008 "please commit this report" | `[T:3fa13850:L30]`, commit `71d46f1` |
| OP-005 | Push fork + rebase onto `origin/main` (keep history) | UI-009 (push) + UI-010 (main, not master) + UI-011 (keep history) | `[T:3fa13850:L47,58,67]`, remote add + rebase + push-to-main |

Note: STEP-4 (5 rebase commits on disk) is a single logical reproducibility op (OP-005), not an SB capability.

## Evidence pointer legend

- `[R:path:lines]` → file in `/Users/mathieuacher/SANDBOX/cobol-jb`
- `[T:<session-id>:L<line>]` → event line in `~/.claude/projects/-Users-mathieuacher-SANDBOX-cobol-jb/<session-id>.jsonl`
- `[G:<short-hash>]` → git commit in project `.git/logs/HEAD`

See `README.md` (this output dir) for the full evidence-backed narrative and `appendix.json` for the machine-readable index.
