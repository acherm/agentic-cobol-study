# KEY_FEATURES — `cobol-jb`

## Preamble

`cobol-jb` is a GnuCOBOL payroll batch program built from a fixed-variable
case-study prompt: read an `employees_input.dat` fixed-layout record stream,
apply category-based overtime rules + three social-contribution rates,
validate each record against four business rules (ERR-001..004), emit a
formatted `payslips_output.dat` and a `rejects_output.dat`, print end-of-job
totals, and self-verify the result against a 27-criterion grid. A "key
feature" here is any delivered capability at depth ≥ 1 that is not pure
infrastructure (commits, `.gitignore`, rebase ops) — the centre of gravity is
**domain modelling** (payroll rules + COBOL record layouts), with a
meaningful VER tier (the self-applied grid) and a thin INF tier (build + data
harness). No algorithmic novelty: COBOL is exactly the idiom industrial
payroll was written in.

## Ranked table (top 11)

| Rank | SB / BL id | Title | Class | Depth | Effort | Score | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | BL-001 / SB-001..008 | Payroll domain data model: 3 FDs, 88-level category names, fixed-layout `EMPLOYEE-RECORD` (ID / name / cat / hours / rate), formatted payslip record with date, category description, regular/overtime split, gross/deductions/net, summary layout | **DOM** | 2 | 2 | 4.0 | `R:program.cbl` L9-51, L139-312; `VERIFICATION_REPORT.md` #1,#6,#8,#19; SB-001,002,006,007 |
|  |  | *Significance note — this is the heart of the exercise: encoding payroll domain shapes into COBOL record/picture clauses. Not an algorithm; a faithful translation of business data layout into FDs and 88-levels.* |  |  |  |  |  |
| 2 | BL-003 / SB-022..026 | Input-validation rules ERR-001..004 + routed reject file: `ELSE IF` chain on ID=0/spaces, hours ∈ (0,80], rate ∈ (0,999.99], category ∈ {A,B,C}; invalid rows skip salary math, flow to a third `FD REJECT-FILE` opened `OUTPUT` with original fields + error code | **DOM** | 2 | 2 | 4.0 | `R:program.cbl` L20-23, L49-51, L314-325, L414-449; `VERIFICATION_REPORT.md` #19-25; SB-022..026 |
|  |  | *Significance note — pure domain engineering: each rule is a business constraint, the reject flow preserves Step-0/1 arithmetic semantics (no regression per criterion #26), and the reject record is itself a second output format the agent had to design.* |  |  |  |  |  |
| 3 | BL-002 / SB-015..018 | Social-contribution deductions: rate constants 0.0730 / 0.0690 / 0.0240 encoded as `PIC 9V9999`, three `COMPUTE` deductions, `WS-TOTAL-DEDUCT = H+R+U`, `WS-NET-SALARY = gross - total`, payslip record extended from 8 to 13+ fields, totals extended with `Total Net Payroll` | **DOM** | 2 | 1 | 3.0 | `R:program.cbl` L102-105, L249-277, L503-513, L617-619; `VERIFICATION_REPORT.md` #11-17; SB-015..018 |
|  |  | *Significance note — DOM evolution with no regression. The rates are not algorithms, they are legislated business numbers; the depth lives in (a) correct decimal picture clauses (V9999 for 4-digit precision), (b) threading new fields through the payslip AND the end-of-job totals AND the accumulator block without breaking Step-0 overtime math.* |  |  |  |  |  |
| 4 | BL-004 / SB-031..032 | Self-applied 27-criterion verification grid → `VERIFICATION_REPORT.md` (25/27); recompile exit 0, `wc -l`, `git log --oneline -- README.md`, `git show` to attribute #27 fail to the BL-003 commit that omitted the README update | **VER** | 2 | 1 | 3.0 | `R:VERIFICATION_REPORT.md` (full); SB-031, SB-032; session `[T:3fa13850:L11-24]` |
|  |  | *Significance note — this is the strongest VER signal in the whole project set: a structured PASS/FAIL grid with per-criterion evidence and a self-detected gap (#27). Not a test harness in the SAT/chess sense, but a verifiable acceptance matrix — the closest this domain gets to formal checking.* |  |  |  |  |  |
| 5 | BL-001 / SB-004,005 | Category-based overtime engine: outer `EVALUATE TRUE` on `EMP-HOURS > WS-STANDARD-HOURS`, inner `EVALUATE TRUE` on CATEGORY-A/B/C selecting multiplier (1.20 / 1.10 / 1.00), `COMPUTE WS-GROSS-SALARY = regular-pay + overtime-pay` | **DOM** | 2 | 1 | 3.0 | `R:program.cbl` L97-100, L454-501; SB-004, SB-005; `VERIFICATION_REPORT.md` #5,#7,#16 |
|  |  | *Significance note — borderline DOM/ALG but clearly DOM: the overtime multipliers are business policy, not an algorithm. The nested EVALUATE TRUE is idiomatic COBOL decision-table style; the depth is in getting the regular/overtime split + per-category multiplier to survive both evolutions (BL-002, BL-003).* |  |  |  |  |  |
| 6 | BL-001 / SB-002, SB-003 | Batch I/O loop: `SELECT ... ASSIGN ... ORGANIZATION IS LINE SEQUENTIAL FILE STATUS IS WS-*-FILE-STATUS`, `OPEN INPUT/OUTPUT`, priming + iterating `READ ... AT END SET END-OF-FILE`, outer `PERFORM 2000-PROCESS-EMPLOYEES UNTIL END-OF-FILE`, three-file CLOSE | **DOM** | 1 | 1 | 1.5 | `R:program.cbl` L9-23, L327-412, L700-703; SB-002, SB-003, SB-011; `VERIFICATION_REPORT.md` #6 |
|  |  | *Significance note — standard COBOL batch-loop skeleton, but load-bearing: every other feature hangs off this control skeleton. Kept at depth 1 because it is a textbook idiom, not a design invention.* |  |  |  |  |  |
| 7 | BL-001 / SB-008 + BL-003 / SB-026 | End-of-job summary report: 11 `WS-SUMMARY-LINE-*` records (employees processed, total gross, total net, A/B/C counts, regular/overtime hrs, errors, rejected), written both to payslip file and `DISPLAY`-ed; accumulators grow across evolutions | **DOM** | 1 | 1 | 1.5 | `R:program.cbl` L262-312, L626-698; SB-008, SB-018, SB-026 |
|  |  | *Significance note — report-layout design: picture clauses (`ZZ,ZZ9.99`) for right-aligned numeric formatting, grouping, dual emit (file + console). Standard COBOL report idiom, but is the user-visible deliverable.* |  |  |  |  |  |
| 8 | BL-001 / SB-009 | Compile-error recovery: first `cobc -x -free` exits 97 on undefined `WS-EMP-FILE-STATUS` + misplaced DATA DIVISION header; single-edit fix (add FILE STATUS working-storage fields) → next compile exit 0 | **LNG** | 1 | 1 | 1.5 | `[T:434a5a96:L19-25]`; SB-009; `appendix.json` strategy_annotations_per_bl.BL-001.dbg_loops=1 |
|  |  | *Significance note — the one DBG loop in the whole project. Tagged LNG because the fix was language-mechanics (COBOL DATA DIVISION ordering + FILE STATUS declaration), not a bug in business logic. A minor but real COBOL idiosyncrasy the agent had to repair.* |  |  |  |  |  |
| 9 | BL-001 / SB-010 + BL-003 / SB-027 | Hand-authored test corpus: `employees_input.dat` with 8 valid rows across A/B/C + 4 invalid rows (one per ERR-001..004) designed to exercise each validation branch; `payslips_output.dat` (180 lines) and `rejects_output.dat` (4 lines) produced and visually checked | **VER** | 1 | 1 | 1.5 | `R:employees_input.dat`, `R:payslips_output.dat`, `R:rejects_output.dat`; SB-010, SB-011, SB-027, SB-028 |
|  |  | *Significance note — the project has no test runner, but this fixture is the empirical VER layer: the 4-row invalid set is a smoke-test that each ERR code fires. Depth 1 because visual inspection, not automated assertions.* |  |  |  |  |  |
| 10 | BL-001 / SB-012 + BL-002 / SB-020 | README.md authored and updated once (Step-0 structure + Step-1 social-contribution table + extended example payslip); NOT updated after Step-2 (criterion #27 FAIL, SB-030b) | **INF** | 1 | 1 | 1.5 | `R:README.md`; SB-012, SB-020, SB-030b; `VERIFICATION_REPORT.md` #27 |
|  |  | *Significance note — documentation-as-infrastructure. Included because the verification grid treats README freshness as a first-class acceptance criterion; the omission is the dominant quality-failure mode flagged in §6 of the assessment.* |  |  |  |  |  |
| 11 | BL-001 / SB-001 + misc | COBOL idiom breadth: `FUNCTION CURRENT-DATE` + `STRING ... DELIMITED BY SIZE` for run-date formatting, `INITIALIZE` for arithmetic zeroing, `ROUNDED`-free `COMPUTE` on V99 pictures, dual-output (file + DISPLAY) summary, FILE STATUS 88-levels covering `00`/`10`/error range | **LNG** | 1 | 1 | 1.5 | `R:program.cbl` L139-151, L337-347, L452, L684-698; assessment §5 "idiomatic COBOL" |
|  |  | *Significance note — COBOL-as-host idiomatic surface: 35 distinct constructs across 8/10 capability categories per the mastery metric. Not language-pushing (no recursion, no dynamic CALL, no pointers), but the constructs deployed are what makes this the "cleanest industrial-COBOL" project in the set.* |  |  |  |  |  |

## Composition chains

1. **Record layout → overtime engine → deductions → net salary → totals**
   (SB-001 → SB-004/005 → SB-015/016 → SB-017/018 → SB-026 summary)
   — The end-of-job totals block is only meaningful because the per-record
   gross/overtime/deduction/net chain behind it is correct; each evolution
   added both a per-record field and a new accumulator + summary line, which
   is the composition the agent had to thread without regression.

2. **FD skeleton → PERFORM UNTIL loop → validation gate → reject routing**
   (SB-002 → SB-003 → SB-023 → SB-024)
   — The reject-file feature (BL-003) is only possible because Step-0 already
   had the READ/UNTIL/CLOSE skeleton plus FILE STATUS handling; the
   validation gate inserts `IF RECORD-IS-INVALID … ELSE …` *inside* the
   existing 2000-loop, so the earlier control structure is load-bearing.

3. **Source program → 3-FD runtime → test corpus → verification grid**
   (SB-001 → SB-011/019/028 → SB-010/027 → SB-031/032)
   — `VERIFICATION_REPORT.md` is the emergent top of the stack: it can only
   assign 25/27 because the compile succeeds (criteria #2/#10/#18), the
   payslip/reject runs produced inspectable artefacts (criteria #6/#19/#20),
   and the validation branches have observable side-effects (#21-25). The
   grid is *about* the earlier features and would be vacuous without them.

4. **Compile-error recovery → clean-first-compile evolutions**
   (SB-009 → SB-019 clean → SB-028 clean → SB-032 recompile exit 0)
   — The one DBG loop at BL-001 hardened `WS-FILE-STATUS` declarations
   upstream; BL-002 and BL-003 then compiled cleanly on first attempt
   because the earlier fix prevented the class of error recurring. A small
   chain, but a real one.

## Significance profile

| Class | Count (top 11) | Notes |
|---|---|---|
| DOM | 5 | Record layout, validation rules, deductions, overtime rules, I/O loop — the centre of gravity |
| VER | 2 | 27-criterion grid; hand-authored test corpus covering all ERR branches |
| LNG | 2 | DBG recovery on DATA DIVISION / FILE STATUS; idiom breadth |
| INF | 1 | README as acceptance-criterion documentation |
| ALG | 0 | — |
| SYS | 0 | Self-contained program, no FFI |
| PRO | 0 | No published protocol involved |
| PRF | 0 | No perf iteration |
| CMP | 1 | End-of-job summary (listed under DOM rank 7) is mildly emergent; the verification report (rank 4, tagged VER) is the strongest CMP candidate since it composes every earlier feature |

Primary class: **DOM** (5/11). Secondary: **VER** (2/11) and **LNG** (2/11).
CMP is implicit in the four composition chains above rather than a
standalone row.

## Verdict

**Domain-modelling-centric**, with a distinctive VER layer (the self-applied
27-criterion grid) that lifts it above a plain "textbook COBOL" rating — the
cleanest industrial-COBOL project in the set, carried by faithful payroll
record layouts and a cross-step no-regression chain rather than any
algorithmic content.
