# STORY — `cobol-jb`

An industrial-idiom payroll program in GnuCOBOL, graded against a self-authored 27-criterion verification grid. Textbook in the best sense.

## The clean industrial-COBOL project

Of all the COBOL exercises in this meta-analysis, `cobol-jb` is the one that reads most like a real mainframe batch program. Records stream in on the left, payslips come out on the right, a summary report is printed at the end, and invalid records are routed to a reject file. The shape is exactly how payroll has been written for fifty years. Claude Code (`claude-opus-4-6`, v2.1.91) did not reinvent the form; it reproduced it, cleanly, over four git commits on 2026-04-03.

The final artefact is a single 705-line `program.cbl` (PROGRAM-ID `PAYROLL-SYSTEM`), three accompanying `.dat` files (`employees_input.dat`, `payslips_output.dat`, `rejects_output.dat`), a `README.md`, and a self-applied `VERIFICATION_REPORT.md` scoring 25/27. No framework, no external library, no test runner. It compiles with `cobc -x -free -o program program.cbl` and runs.

## The domain — records in, payslips out

The prompt constraints (`case-study-1.md`) pin the shape: fixed-width employee records with ID, name, job category, hours, and hourly rate; category-based overtime (A +20%, B +10%, C 0%); three social-contribution rates (health 7.30%, retirement 6.90%, unemployment 2.40%); and four input-validation rules (ERR-001 ID not zero/spaces, ERR-002 hours in (0, 80], ERR-003 rate in (0, 999.99], ERR-004 category in {A,B,C}). What matters here is not the arithmetic — it is trivial — but the *form*: the employee record is a `PIC` layout, the category is an 88-level condition name, the overtime selector is an `EVALUATE TRUE`, and the deduction arithmetic is a `COMPUTE` with decimal precision. Getting the form right *is* the exercise.

## How the build went

Two Claude Code sessions opened the work. The first (session `434a5a96`, 14:45 → 15:59) handled the feature build. It started from `PL-ROOT` — "You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program" — and hit exactly one compile error: the first `cobc` run exited 97 on undefined `WS-EMP-FILE-STATUS` fields and a misplaced PROCEDURE DIVISION header. A single edit added the `FILE STATUS` working-storage fields and reordered the header; the next compile was clean. BL-002 (social contributions) and BL-003 (validation + reject file) then compiled on the first attempt — zero DBG loops thereafter.

The second session (`3fa13850`, 15:46 that afternoon through 11:03 the following morning, most of it idle) did the self-verification and then the push/rebase dance onto a GitHub fork.

Across the two sessions, eleven user prompts. Only five of them were coding: one per BL, plus the initial `PL-ROOT`. The other six were git/push/rebase operations — two of which were clarifications ("push in the main, not master"; "I want to keep history"). That is a 1:1 ratio of coding prompts to delivered features, which is as lean as this corpus gets.

## What was delivered

Concretely: `program.cbl` (705 LOC, one program); `employees_input.dat` regenerated to carry 8 valid rows spread across categories A/B/C and 4 invalid rows designed to fire each of ERR-001..004; `payslips_output.dat` at 180 lines of formatted output; `rejects_output.dat` at 4 lines; a `README.md` documenting build, run, input layout, and business logic (through Step 1); and `VERIFICATION_REPORT.md` — the distinguishing artefact — scoring 26 PASS / 1 PARTIAL / 1 FAIL against a 27-criterion grid self-authored from the case-study spec. The end-of-run totals: **6 425.65** total gross payroll, **5 359.06** total net payroll, 4 employees rejected, category counts 3 / 3 / 2.

Rubric scores across the four BLs sit at a mean 1.57/2, with Q1 correctness and Q2 build/run uniformly at 2 (four-for-four). The two points of weakness are Q3 (test rigor, 1.25) and Q5 (maintainability, 1.25) — consistent with a project that has no automated test harness.

## Validation — the self-applied grid

The distinguishing move is BL-004. After three feature commits, the agent was asked (without modifying `program.cbl`) to apply the 27-criterion verification grid from the case-study spec to the current repo. It recompiled to confirm `exit 0`, ran `wc -l` on `program.cbl`, ran `git log --oneline -- README.md` and `git show` to attribute criterion #27 to the BL-003 commit that had omitted the README update, and wrote `VERIFICATION_REPORT.md` honestly. Two failures are called out: **#3 LOC overshoot** (705 vs the 250–350 target; mostly verbose payslip formatting records) and **#27 README drift** (the BL-003 reject-file feature never got its README update). The agent did not hide either; it caught its own gap.

## Compute and context footprint

Forty minutes of active collaboration time. 281 assistant turns across the two sessions (126 on build, 44 on verify/publish, the rest spread across tool calls). Peak context: 73 k tokens out of the 1 M window — 7.3 %. No compaction events, no summarization pressure. On rack-rate pricing this project cost roughly $18. Low-stakes, low-footprint.

## Why it's impressive in context

The COBOL surface deployed is real. Three `FD` entries with proper `SELECT ... ASSIGN ... ORGANIZATION IS LINE SEQUENTIAL FILE STATUS IS`; 88-level condition names (e.g. `88 CATEGORY-WHITE-COLLAR VALUE 'W'`); nested `EVALUATE TRUE` blocks rather than cascades of nested `IF`; `COMPUTE var ROUNDED` for payroll arithmetic; decimal picture clauses (`PIC 9V9999` for rates, `ZZ,ZZ9.99` for summary output); `FUNCTION CURRENT-DATE` + `STRING ... DELIMITED BY SIZE` for run-date formatting; dual emit of summary lines to both the payslip file and stdout. The mastery metric counts 35 distinct constructs across 8 of 10 capability categories. None of it is language-pushing — no dynamic `CALL`, no CICS, no pointers — but what is deployed is the shape of a real-world batch mainframe program, not a schoolbook toy.

## Surprising insights

Three observations are worth flagging. First, the interaction economy: 5 coding prompts produced 4 feature commits — a 1:1 rate this corpus rarely matches. Most of the human effort went into git publishing, not specification. Second, the self-applied grid is a rare accountability signal; across this project set, almost no project has written its own PASS/FAIL acceptance matrix with per-criterion evidence pointers. Third, the honest grading — calling out its own LOC overshoot and its own README drift, with a `git show` trail to prove the latter — is exactly the self-awareness move one wants to see, and it is not the default behaviour of a coding agent asked to grade itself.
