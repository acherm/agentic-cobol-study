# Case Study Verification Report

**Date:** 2026-04-03
**Score:** 25/27 — Near-identical reproduction (minor acceptable differences)

## Step 0 — Generation

| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| 1 | File created | PASS | `program.cbl` exists |
| 2 | Compilation OK | PASS | `cobc -x -free` exits 0, no errors |
| 3 | Approximate LOC (250–350) | FAIL | 705 lines — well above the 350 upper bound |
| 4 | PERFORM pattern | PASS | Multiple `PERFORM` statements |
| 5 | EVALUATE pattern | PASS | Multiple `EVALUATE TRUE` blocks |
| 6 | FILE SECTION FDs | PASS | `FD EMPLOYEE-FILE` + `FD PAYSLIP-FILE` present, `ASSIGN TO` clauses match expected filenames |
| 7 | COMPUTE pattern | PASS | Extensively used for salary calculations |
| 8 | 88-levels | PASS | Many: `CATEGORY-A/B/C`, `EMP-FILE-EOF`, `END-OF-FILE`, etc. |
| 9 | README.md | PASS | Created in commit `b4c6c66` |

**Step 0: 8/9**

## Step 1 — Social Contributions

| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| 10 | Compilation OK | PASS | Compiles cleanly |
| 11 | Health rate 7.30/0.073 | PASS | `0.0730` in source + `"Health (7.30%)"` in payslip |
| 12 | Retirement rate 6.90/0.069 | PASS | `0.0690` in source + `"Retire (6.90%)"` in payslip |
| 13 | Unemployment rate 2.40/0.024 | PASS | `0.0240` in source + `"Unempl (2.40%)"` in payslip |
| 14 | Net salary variable | PASS | `WS-NET-SALARY` declared |
| 15 | Enriched output (≥5 fields) | PASS | 13+ fields in payslip output |
| 16 | No regression — EVALUATE overtime | PASS | Overtime EVALUATE logic intact |
| 17 | README.md updated after Step 1 | PASS | Modified in commit `a566a9e` |

**Step 1: 8/8**

## Step 2 — Validation & Reject File

| # | Criterion | Result | Notes |
|---|-----------|--------|-------|
| 18 | Compilation OK | PASS | Compiles cleanly |
| 19 | 3 FD entries | PASS | `FD EMPLOYEE-FILE`, `FD PAYSLIP-FILE`, `FD REJECT-FILE` |
| 20 | Reject file in OUTPUT mode | PASS | `OPEN OUTPUT REJECT-FILE` assigned to `"rejects_output.dat"` |
| 21 | ERR-001 | PASS | Present in validation logic |
| 22 | ERR-002 | PASS | Present in validation logic |
| 23 | ERR-003 | PASS | Present in validation logic |
| 24 | ERR-004 | PASS | Present in validation logic |
| 25 | Reject counter | PASS | `WS-REJECTED-COUNT` declared |
| 26 | No regression — rates 7.30, 6.90, 2.40 | PASS | All rates still present |
| 27 | README.md updated after Step 2 | FAIL | README not modified in Step 2 commit |

**Step 2: 9/10**

## Failures Summary

1. **#3 — LOC count**: 705 lines vs. expected 250–350. The program is functional but roughly 2x the expected size, mostly due to verbose payslip formatting records.
2. **#27 — README not updated after Step 2**: The README documents Steps 0 and 1 features but was not updated in the Step 2 commit to document validation/reject file functionality.
