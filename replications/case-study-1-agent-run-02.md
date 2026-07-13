# COBOL AI Generation & Evolution — Case Study

> **PhD Research — Legacy Modernization via AI**  
> Domain: Payroll Management System | Steps: 1 generation + 5 evolutions | Compiler: GnuCOBOL

---

## Table of Contents

1. [Overview](#1-overview)
2. [Prompt 1 — Generate Base Program](#2-prompt-1--generate-base-program)
3. [Prompt 2 — Evolution 1: Social Contributions](#3-prompt-2--evolution-1-social-contributions)
4. [Prompt 3 — Evolution 2: Data Validation & Reject File](#4-prompt-3--evolution-2-data-validation--reject-file)
5. [Prompt 4 — Evolution 3: Reporting & Control Break](#5-prompt-4--evolution-3-reporting--control-break)
6. [Prompt 5 — Evolution 4: Multi-file Input & Merge](#6-prompt-5--evolution-4-multi-file-input--merge)
7. [Prompt 6 — Evolution 5: Refactoring](#7-prompt-6--evolution-5-refactoring)
8. [Evaluation Grid](#8-evaluation-grid)
9. [Usage Notes](#9-usage-notes)

---

## 1. Overview

### Objective

This case study measures the ability of an AI agent to generate a complete COBOL batch program from scratch, then incrementally evolve it through precise, reproducible prompts.

All variables are fixed so that any third party can replay the exact same sequence and compare results.

### Why Payroll?

The payroll domain was selected because it is the most representative of real-world mainframe COBOL batch programs. It naturally supports progressive feature additions:

- Input/output files (employees, payslips, rejects)
- Complex arithmetic (gross salary, deductions, net salary)
- Bracket logic and scales (`EVALUATE` / `88-levels`)
- Data validation and error handling
- End-of-job counters and totals

### Case Study Structure

| Step   | Description                                              | Prompt Used        |
|--------|----------------------------------------------------------|--------------------|
| Step 0 | Generate the base COBOL program                          | Generation Prompt  |
| Step 1 | Evolution 1 — Social contribution deductions             | Evolution Prompt   |
| Step 2 | Evolution 2 — Input validation + reject file             | Evolution Prompt   |
| Step 3 | Evolution 3 — Reporting & control break by category      | Evolution Prompt   |
| Step 4 | Evolution 4 — Multi-file input & merge                   | Evolution Prompt   |
| Step 5 | Evolution 5 — Refactoring (procedure division structure) | Evolution Prompt   |

> **Reproducibility note:** Every prompt is fully specified — no variable is left to the agent's interpretation. An evaluator can replay the case study by copy-pasting the prompts as-is and verify results using the grid in Section 5.

---

## 2. Prompt 1 — Generate Base Program

### Context

This first prompt instructs the agent to generate a complete COBOL batch program in the payroll domain. The program must compile successfully without errors (either on the first attempt or after the agent self-corrects).

### Fixed Variables

| Parameter        | Value                                                        |
|------------------|--------------------------------------------------------------|
| `domain`         | Payroll management system                                    |
| `n_loc`          | 300 lines                                                    |
| `n_files`        | 2 (`employees_input.dat` as input, `payslips_output.dat` as output) |
| `required patterns` | `PERFORM`, `EVALUATE`, `FILE SECTION`, `COMPUTE`, `88-levels` |
| `compiler`       | GnuCOBOL — `cobc -x -free -o program program.cbl`             |
| `filename`       | `program.cbl`                                              |

### Prompt — copy-paste as-is

```
You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program.

## Business Context
Domain: Payroll management system

## Technical Constraints
- Target lines of code (LOC): 300 lines
- Number of files the program must handle: 2
  (employees_input.dat as input, payslips_output.dat as output)
- Target compiler: GnuCOBOL (cobc)
- Compilation command: cobc -x -free -o program program.cbl

## Required COBOL Patterns
The program MUST contain the following constructs:
- PERFORM (with VARYING or UNTIL loop)
- EVALUATE (multi-branch conditional logic)
- FILE SECTION with FD entries
- COMPUTE (arithmetic expressions)
- 88-level condition names

## Requirements
- The program must be complete and self-contained (no external dependencies)
- All data is declared in the WORKING-STORAGE SECTION or FILE SECTION
- Copybooks are inlined in the program (no separate .cpy file)
- The program must compile without warnings or errors using GnuCOBOL
- The .cbl file must be named program.cbl
- Do not use comments to reach the target line count.

## Business Logic to Implement
1. Read employee records (ID, name, job category, hours worked, hourly rate)
2. Calculate gross salary: hours_worked * hourly_rate
   - Use EVALUATE to apply overtime bonus if hours_worked > 35
   - Category A: +20% bonus on overtime hours
   - Category B: +10% bonus on overtime hours
   - Category C: no overtime bonus
3. Write one payslip record per employee to output file
4. Display totals (total employees processed, total gross payroll) at end of job

## Test Data Generation
After successful compilation, create the following test data file:

employees_input.dat — create 10 records with this fixed-width layout:
  - Employee ID    : positions 1-6   (6 chars, left-padded with zeros)
  - Name           : positions 7-26  (20 chars, left-padded with spaces)
  - Job category   : position 27     (1 char: A, B, or C)
  - Hours worked   : positions 28-32 (5 digits, 2 implicit decimals: e.g. 04000 = 40.00)
  - Hourly rate    : positions 33-38 (6 digits, 2 implicit decimals: e.g. 025000 = 250.00)

The 10 records must cover the following scenarios:
  - 2 records category A, hours > 35  (overtime, +20% bonus)
  - 2 records category B, hours > 35  (overtime, +10% bonus)
  - 2 records category C, hours <= 35 (no overtime)
  - 1 record  category A, hours <= 35 (no overtime)
  - 1 record  category B, hours <= 35 (no overtime)
  - 1 record with hours worked = 00000  (will trigger ERR-002 in Step 2)
  - 1 record with hourly rate  = 000000 (will trigger ERR-003 in Step 2)

## Process
1. Think of the data structures that will represent employees and payslips
2. Generate the program.cbl file
3. Compile with: cobc -x -free -o program program.cbl
4. If compilation error -> fix and recompile
5. Repeat until successful compilation with no errors
6. Create the employees_input.dat test data file as specified above
7. Once compilation succeeds, run the program with ./program
8. Inspect the execution output and verify that the behavior matches the need
9. Once execution is verified, run the backlog extractor skill to update README.md
```

### Expected Outputs

- `program.cbl` created (~300 lines)
- Successful compilation with exit code 0
- `README.md` generated by the backlog extractor skill
- All required COBOL patterns present in the source

> ✅ **Validation criterion — Step 0:** Run `cobc -x -free -o program program.cbl` — compilation is valid if the output contains **no errors** (warnings are acceptable). The file must contain: `PERFORM`, `EVALUATE`, `FILE SECTION`, `COMPUTE`, and at least one level-88 condition name.

---

## 3. Prompt 2 — Evolution 1: Social Contributions

### Context

This first evolution adds social contribution deductions to the existing program. The agent must modify `program.cbl` without breaking existing functionality, then recompile successfully.

**Why this feature?** Social deductions are the natural follow-up to gross salary. This forces the agent to: add new data structures in `WORKING-STORAGE`, enrich the output record in `FILE SECTION`, and update calculation logic without introducing regressions.

### Fixed Variables

| Parameter    | Value                                                  |
|--------------|--------------------------------------------------------|
| `feature`    | Add social contribution deductions to the payroll calculation |
| `cobol_path` | `program.cbl` (same file as Step 0)                  |
| `compiler`   | `cobc -x -free -o program program.cbl`                   |

### Prompt — copy-paste as-is

```
You are a mainframe COBOL expert. You must modify an existing COBOL program.

## Feature to Add
Add social contribution deductions to the payroll calculation.

The following deductions must be applied to the gross salary to compute the net salary:
- Health insurance (Assurance maladie): 7.30% of gross salary
- Retirement contribution (Retraite): 6.90% of gross salary
- Unemployment insurance (Chomage): 2.40% of gross salary
- Total deduction = sum of the three contributions above
- Net salary = gross salary - total deduction

The output payslip record must be updated to include:
  gross salary, health deduction, retirement deduction,
  unemployment deduction, total deduction, net salary

Also update the end-of-job totals to display:
  total gross payroll AND total net payroll.


## Constraints
- The modified program must compile with: cobc -x -free -o program program.cbl
- Do not break existing functionality (file reading, gross salary calc, PERFORM/EVALUATE patterns)
- Only modify the file: program.cbl

## Process
1. Modify the file program.cbl
2. Compile with: cobc -x -free -o program program.cbl
3. If error -> fix and recompile
4. Repeat until successful compilation
5. Once compilation succeeds, run the program with ./program
6. Inspect the execution output and verify that the behavior matches the need
7. Once execution is verified, run the backlog extractor skill to update README.md
```

### Expected Outputs

- `program.cbl` updated with all 3 deductions calculated
- Output record enriched (6 new fields minimum)
- Successful compilation with exit code 0
- `README.md` updated by the backlog extractor skill
- No regression: Step 0 logic (overtime EVALUATE) still present

> ✅ **Validation criterion — Step 1:** Run `cobc -x -free -o program program.cbl` — valid if **no errors** in output. Source must contain rates `7.30`, `6.90`, and `2.40`. The output record must include a net salary field.

---

## 4. Prompt 3 — Evolution 2: Data Validation & Reject File

### Context

This second evolution adds robustness to the program: input data validation and writing of invalid records to a dedicated reject file. This is a fundamental pattern in production COBOL batch jobs.

**Why this feature?** Reject file handling is a classic COBOL batch pattern. It forces the addition of a 3rd `FILE` (`FD` entry), branching logic on validation, and end-of-job reject counters — maximizing COBOL construct coverage.

### Fixed Variables

| Parameter    | Value                                                         |
|--------------|---------------------------------------------------------------|
| `feature`    | Add input data validation with a reject file for invalid records |
| `cobol_path` | `program.cbl` (same file as previous steps)                 |
| `compiler`   | `cobc -x -free -o program program.cbl`                          |

### Prompt — copy-paste as-is

```
You are a mainframe COBOL expert. You must modify an existing COBOL program.

## Feature to Add
Add input data validation with a dedicated reject file for invalid records.

The following validation rules must be applied to each employee record before processing:
- Rule 1 (ERR-001): Employee ID must not be spaces or zeros
- Rule 2 (ERR-002): Hours worked must be > 0 and <= 80
- Rule 3 (ERR-003): Hourly rate must be > 0 and <= 999.99
- Rule 4 (ERR-004): Job category must be 'A', 'B', or 'C' (use existing 88-level names)

If a record fails ANY validation rule:
  - Do NOT process it (skip salary calculation)
  - Write it to a new output file: rejects_output.dat
  - The reject record must include: the original employee record + the error code (ERR-001 etc.)

At end of job, display updated totals:
  employees processed (valid), employees rejected, total gross payroll, total net payroll.

## Constraints
- The modified program must compile with: cobc -x -free -o program program.cbl
- Do not break existing functionality (gross salary, net salary, social contributions)
- Only modify the file: program.cbl
- The new file must be declared with a proper FD entry in FILE SECTION

## Process
1. Modify the file program.cbl
2. Compile with: cobc -x -free -o program program.cbl
3. If error -> fix and recompile
4. Repeat until successful compilation
5. Once compilation succeeds, run the program with ./program
6. Inspect the execution output and verify that the behavior matches the need
7. Once execution is verified, run the backlog extractor skill to update README.md
```

### Expected Outputs

- 3 files declared in `FILE SECTION` (`employees_input`, `payslips_output`, `rejects_output`)
- 4 validation rules implemented with error codes `ERR-001` to `ERR-004`
- Invalid records written to `rejects_output.dat`
- End-of-job counters display both valid and rejected counts
- Successful compilation with exit code 0
- `README.md` updated by the backlog extractor skill

> ✅ **Validation criterion — Step 2:** Run `cobc -x -free -o program program.cbl` — valid if **no errors** in output. Source must contain 3 `FD` entries. Error codes `ERR-001`, `ERR-002`, `ERR-003`, `ERR-004` must be present. `rejects_output` must be opened in `OUTPUT` mode.

---

## 5. Prompt 4 — Evolution 3: Reporting & Control Break

### Context

This third evolution adds an aggregated summary report generated at the end of the job. The agent must produce a new output file with totals broken down by employee category — the classic **control break** pattern, one of the most fundamental in COBOL batch processing.

**Why this feature?** Control break logic forces the agent to maintain running accumulators per category, reset them at the right moment, and write summary records after processing all input — a pattern that tests understanding of COBOL batch job structure beyond simple record-by-record processing.

### Fixed Variables

| Parameter    | Value                                                            |
|--------------|------------------------------------------------------------------|
| `feature`    | Add a category-level summary report using control break logic    |
| `cobol_path` | `program.cbl` (same file as previous steps)                      |
| `compiler`   | `cobc -x -free -o program program.cbl`                           |

### Prompt — copy-paste as-is

```
You are a mainframe COBOL expert. You must modify an existing COBOL program.

## Feature to Add
Add a category-level summary report generated at the end of the job.

A new output file report_output.dat must be created and declared with a proper FD entry.

For each employee category (A, B, C), the report must include one summary line containing:
- Category label (A, B, or C)
- Number of valid employees processed in that category
- Total gross payroll for that category
- Total net payroll for that category

The report must also include a grand total line at the end with:
- Total valid employees across all categories
- Total gross payroll across all categories
- Total net payroll across all categories

Implementation requirements:
- Use WORKING-STORAGE accumulators per category (one set per A, B, C)
- Accumulators must be incremented during record processing
- The report file must be written only during the end-of-job routine
- Use PERFORM to loop through category totals when writing the report

## Constraints
- The modified program must compile with: cobc -x -free -o program program.cbl
- Do not break existing functionality (validation, reject file, social contributions)
- Only modify the file: program.cbl
- The new file must be declared with a proper FD entry in FILE SECTION

## Process
1. Modify the file program.cbl
2. Compile with: cobc -x -free -o program program.cbl
3. If error -> fix and recompile
4. Repeat until successful compilation
5. Once compilation succeeds, run the program with ./program
6. Inspect the execution output and verify that the behavior matches the need
7. Once execution is verified, run the backlog extractor skill to update README.md
```

### Expected Outputs

- 4 files declared in `FILE SECTION` (employees_input, payslips_output, rejects_output, report_output)
- Per-category accumulators in `WORKING-STORAGE` (3 sets: A, B, C)
- `report_output.dat` written during end-of-job routine
- Grand total line present in report
- Successful compilation with no errors
- `README.md` updated by the backlog extractor skill

> ✅ **Validation criterion — Step 3:** Run `cobc -x -free -o program program.cbl` — valid if **no errors** in output. Source must contain 4 `FD` entries. `report_output` must be opened in `OUTPUT` mode. Per-category accumulator variables must be present for A, B, and C.

---

## 6. Prompt 5 — Evolution 4: Multi-file Input & Merge

### Context

This fourth evolution replaces the single input file with two distinct input files (`employees_fulltime.dat` and `employees_parttime.dat`) that the program must read and process together. This introduces multi-source input management — a very common pattern in production mainframe batch jobs.

**Why this feature?** Managing multiple input FDs and merging their records tests the agent's ability to handle more complex `FILE SECTION` declarations, multiple `READ` statements with `AT END` handling, and input sequencing logic — all typical of real-world COBOL batch programs.

### Fixed Variables

| Parameter    | Value                                                              |
|--------------|--------------------------------------------------------------------|
| `feature`    | Replace single input file with two input files (fulltime/parttime) |
| `cobol_path` | `program.cbl` (same file as previous steps)                        |
| `compiler`   | `cobc -x -free -o program program.cbl`                             |

### Prompt — copy-paste as-is

```
You are a mainframe COBOL expert. You must modify an existing COBOL program.

## Feature to Add
Replace the single employee input file with two separate input files that must both be processed.

The two input files are:
- employees_fulltime.dat  — contains full-time employee records (same record layout as before)
- employees_parttime.dat  — contains part-time employee records (same record layout as before)

Processing requirements:
- Both files must be declared with separate FD entries in FILE SECTION
- The program must read and process all records from employees_fulltime.dat first,
  then all records from employees_parttime.dat
- All existing processing logic applies to both files equally:
  validation, salary calculation, social contributions, payslip output, reject output
- The category-level report accumulators must aggregate across both files
- End-of-job totals must reflect all records from both files combined
- Add a WORKING-STORAGE counter to track how many records came from each file,
  and display these counts in the end-of-job summary

## Constraints
- The modified program must compile with: cobc -x -free -o program program.cbl
- Do not break existing functionality (validation, payslips, rejects, report, social contributions)
- Only modify the file: program.cbl
- Remove the old employees_input FD and replace it with the two new FD entries

After successful compilation, split the existing employees_input.dat into two test files:
  - employees_fulltime.dat  : records 1 to 6 from the original file
  - employees_parttime.dat  : records 7 to 10 from the original file
  (keep the same fixed-width record layout)

## Process
1. Modify the file program.cbl
2. Compile with: cobc -x -free -o program program.cbl
3. If error -> fix and recompile
4. Repeat until successful compilation
5. Once compilation succeeds, run the program with ./program
6. Inspect the execution output and verify that the behavior matches the need
7. Once execution is verified, run the backlog extractor skill to update README.md
```

### Expected Outputs

- `employees_input` FD removed, replaced by `employees_fulltime` and `employees_parttime` FDs
- Total of 5 `FD` entries in `FILE SECTION`
- Per-file record counters displayed in end-of-job summary
- All existing outputs (payslips, rejects, report) still produced correctly
- Successful compilation with no errors
- `README.md` updated by the backlog extractor skill

> ✅ **Validation criterion — Step 4:** Run `cobc -x -free -o program program.cbl` — valid if **no errors** in output. Source must contain 5 `FD` entries. Both `employees_fulltime` and `employees_parttime` must be opened in `INPUT` mode. Per-file counters must be present in `WORKING-STORAGE`.

---

## 7. Prompt 6 — Evolution 5: Refactoring

### Context

This final evolution is a **pure refactoring task**: the agent must restructure the `PROCEDURE DIVISION` into clearly named, cohesive paragraphs without changing any observable behavior. All output files must remain byte-for-byte identical before and after the refactoring.

**Why this feature?** Refactoring is the most demanding task for an AI agent on legacy code — it tests whether the agent can restructure logic while strictly preserving semantics. It also produces a program that is significantly more readable and maintainable, which is the end goal of any legacy modernization effort.

### Fixed Variables

| Parameter    | Value                                                              |
|--------------|--------------------------------------------------------------------|
| `feature`    | Refactor the PROCEDURE DIVISION into named, cohesive paragraphs    |
| `cobol_path` | `program.cbl` (same file as previous steps)                        |
| `compiler`   | `cobc -x -free -o program program.cbl`                             |

### Prompt — copy-paste as-is

```
You are a mainframe COBOL expert. You must refactor an existing COBOL program.

## Refactoring Task
Restructure the PROCEDURE DIVISION into clearly named, cohesive paragraphs.

The refactored program must use the following paragraph structure:

- 0000-MAIN            : top-level orchestrator, calls all other paragraphs via PERFORM
- 1000-INIT            : open all files, initialize all counters and accumulators
- 2000-PROCESS-LOOP    : main read loop, calls 3000 for each record
- 3000-PROCESS-RECORD  : dispatches to validation then processing
- 3100-VALIDATE-RECORD : applies all 4 validation rules, sets a validation flag
- 3200-COMPUTE-SALARY  : gross salary calculation and overtime logic
- 3300-COMPUTE-DEDUCTIONS : social contribution calculations
- 3400-UPDATE-ACCUMULATORS : updates category-level and file-level counters
- 4000-WRITE-PAYSLIP   : writes to payslips_output
- 4100-WRITE-REJECT    : writes to rejects_output
- 5000-WRITE-REPORT    : writes the category summary report to report_output
- 9000-TERMINATION     : close all files, display end-of-job summary

Rules:
- Each paragraph must have a single, clear responsibility
- All inter-paragraph calls must use PERFORM (no GOTO)
- No logic must be duplicated between paragraphs
- The observable behavior must be strictly identical to the input program:
  same output files, same records, same totals, same end-of-job display

## Constraints
- The modified program must compile with: cobc -x -free -o program program.cbl
- Do not change any business logic, calculation, or file handling behavior
- Only modify the file: program.cbl
- Do not add or remove any features — this is a structural refactoring only

## Process
1. Modify the file program.cbl
2. Compile with: cobc -x -free -o program program.cbl
3. If error -> fix and recompile
4. Repeat until successful compilation
5. Once compilation succeeds, run the program with ./program
6. Inspect the execution output and verify that the behavior matches the need
7. Once execution is verified, run the backlog extractor skill to update README.md
```

### Expected Outputs

- All 12 named paragraphs present in `PROCEDURE DIVISION`
- No `GOTO` statement anywhere in the source
- All inter-paragraph calls use `PERFORM`
- Successful compilation with no errors
- `README.md` updated by the backlog extractor skill
- **No behavioral change**: same output logic as Step 4

> ✅ **Validation criterion — Step 5:** Run `cobc -x -free -o program program.cbl` — valid if **no errors** in output. All 12 paragraph names (`0000-MAIN`, `1000-INIT`, `2000-PROCESS-LOOP`, etc.) must be present in the source. No `GOTO` keyword present. No new `FD` entries added or removed.

---

## 8. Evaluation Grid

Use this grid to objectively verify whether the agent produced equivalent results when replaying the case study.

### Step 0 — Generation

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | File created | `program.cbl` exists in workspace |
| 2 | Compilation OK | No errors in output of `cobc -x -free -o program program.cbl` |
| 3 | Approximate LOC | Between 250 and 350 lines |
| 4 | PERFORM pattern | Keyword `PERFORM` present in source |
| 5 | EVALUATE pattern | Keyword `EVALUATE` present in source |
| 6 | FILE SECTION | `FD employees_input` + `FD payslips_output` present |
| 7 | COMPUTE pattern | Keyword `COMPUTE` present in source |
| 8 | 88-levels | At least one level-88 condition declared |
| 9 | README.md | `README.md` generated by backlog extractor skill |

### Step 1 — Social Contributions

| # | Criterion | Verification |
|---|-----------|--------------|
| 10 | Compilation OK | No errors in compilation output |
| 11 | Health rate | Value `7.30` or `0.073` present in source |
| 12 | Retirement rate | Value `6.90` or `0.069` present in source |
| 13 | Unemployment rate | Value `2.40` or `0.024` present in source |
| 14 | Net salary computed | Variable for net salary present (any name) |
| 15 | Enriched output record | At least 5 fields in payslip record |
| 16 | No regression | EVALUATE overtime logic still present |
| 17 | README.md updated | `README.md` modified after Step 1 |

### Step 2 — Validation & Reject File

| # | Criterion | Verification |
|---|-----------|--------------|
| 18 | Compilation OK | No errors in compilation output |
| 19 | 3 FD entries | 3 `FD` declarations in `FILE SECTION` |
| 20 | Reject file | `rejects_output.dat` opened in `OUTPUT` mode |
| 21 | ERR-001 | String `ERR-001` present in source |
| 22 | ERR-002 | String `ERR-002` present in source |
| 23 | ERR-003 | String `ERR-003` present in source |
| 24 | ERR-004 | String `ERR-004` present in source |
| 25 | Reject counter | Variable for rejected record count present |
| 26 | No regression | Rates `7.30`, `6.90`, `2.40` still present |
| 27 | README.md updated | `README.md` modified after Step 2 |

### Step 3 — Reporting & Control Break

| # | Criterion | Verification |
|---|-----------|--------------|
| 28 | Compilation OK | No errors in compilation output |
| 29 | 4 FD entries | 4 `FD` declarations in `FILE SECTION` |
| 30 | Report file | `report_output.dat` opened in `OUTPUT` mode |
| 31 | Category A accumulators | Variables for category A count + gross + net present |
| 32 | Category B accumulators | Variables for category B count + gross + net present |
| 33 | Category C accumulators | Variables for category C count + gross + net present |
| 34 | Grand total line | Grand total record written to report |
| 35 | No regression | ERR-001 to ERR-004 and rates 7.30/6.90/2.40 still present |
| 36 | README.md updated | `README.md` modified after Step 3 |

### Step 4 — Multi-file Input & Merge

| # | Criterion | Verification |
|---|-----------|--------------|
| 37 | Compilation OK | No errors in compilation output |
| 38 | 5 FD entries | 5 `FD` declarations in `FILE SECTION` |
| 39 | Fulltime FD | `employees_fulltime` opened in `INPUT` mode |
| 40 | Parttime FD | `employees_parttime` opened in `INPUT` mode |
| 41 | Old input removed | `employees_input` FD no longer present |
| 42 | Per-file counters | Variables for fulltime and parttime record counts present |
| 43 | End-of-job display | Both per-file counts displayed in termination routine |
| 44 | No regression | Report accumulators and reject logic still present |
| 45 | README.md updated | `README.md` modified after Step 4 |

### Step 5 — Refactoring

| # | Criterion | Verification |
|---|-----------|--------------|
| 46 | Compilation OK | No errors in compilation output |
| 47 | 0000-MAIN | Paragraph `0000-MAIN` present in source |
| 48 | 1000-INIT | Paragraph `1000-INIT` present in source |
| 49 | 2000-PROCESS-LOOP | Paragraph `2000-PROCESS-LOOP` present in source |
| 50 | 3000-PROCESS-RECORD | Paragraph `3000-PROCESS-RECORD` present in source |
| 51 | 3100-VALIDATE-RECORD | Paragraph `3100-VALIDATE-RECORD` present in source |
| 52 | 3200-COMPUTE-SALARY | Paragraph `3200-COMPUTE-SALARY` present in source |
| 53 | 3300-COMPUTE-DEDUCTIONS | Paragraph `3300-COMPUTE-DEDUCTIONS` present in source |
| 54 | 3400-UPDATE-ACCUMULATORS | Paragraph `3400-UPDATE-ACCUMULATORS` present in source |
| 55 | 4000-WRITE-PAYSLIP | Paragraph `4000-WRITE-PAYSLIP` present in source |
| 56 | 4100-WRITE-REJECT | Paragraph `4100-WRITE-REJECT` present in source |
| 57 | 5000-WRITE-REPORT | Paragraph `5000-WRITE-REPORT` present in source |
| 58 | 9000-TERMINATION | Paragraph `9000-TERMINATION` present in source |
| 59 | No GOTO | Keyword `GOTO` absent from source |
| 60 | No new FD | FD count unchanged (still 5) |
| 61 | README.md updated | `README.md` modified after Step 5 |

### Scoring

| Score | Interpretation |
|-------|----------------|
| 61/61 | Perfect reproduction — identical results |
| 55–60/61 | Near-identical — minor acceptable differences |
| 43–54/61 | Partial reproduction — agent missed some constraints |
| < 43/61 | Insufficient reproduction — agent diverged significantly |

---

## 9. Usage Notes

### How to Replay the Case Study

1. Create a fresh, empty workspace for the experiment.
2. Copy **Prompt 1** (Section 2) and submit it to the agent in full.
3. Wait for the agent to finish (compilation + `README.md` generated). Record the exact content of `program.cbl`.
4. Copy **Prompt 2** (Section 3), then submit.
5. Wait for the agent to finish. Record the exact content of `program.cbl`.
6. Copy **Prompt 3** (Section 4), then submit.
7. Wait for the agent to finish. Record the exact content of `program.cbl`.
8. Copy **Prompt 4** (Section 5), then submit.
9. Wait for the agent to finish. Record the exact content of `program.cbl`.
10. Copy **Prompt 5** (Section 6), then submit.
11. Wait for the agent to finish. Record the exact content of `program.cbl`.
12. Copy **Prompt 6** (Section 7), then submit.
13. Wait for the agent to finish.
14. Evaluate results using the grid in Section 8.

### Important Notes

> ⚠️ **Placeholder substitution:** In every evolution prompt, the line `[INSERT HERE THE FULL CONTENT OF program.cbl...]` must be replaced with the complete COBOL source produced at the **immediately preceding step**. Always use the latest version — do not reuse an earlier step's source.

> ℹ️ **Expected variability:** COBOL variable names may differ between runs (e.g., `WS-GROSS-PAY` vs `GROSS-SALARY`). The evaluation grid accepts semantic equivalents. Only the numeric rates (`7.30`, `6.90`, `2.40`), error codes (`ERR-001` to `ERR-004`), and paragraph names in Step 5 are strictly required as-is.

> 🔁 **Refactoring validation:** For Step 5, behavioral equivalence cannot be verified by source inspection alone. If possible, run the refactored program against a test input file and compare output files byte-for-byte with the Step 4 output.

### References

- GnuCOBOL documentation: https://gnucobol.sourceforge.io/
- COBOL Standard ISO/IEC 1989:2014
- Backlog Extractor Skill — see `/mnt/skills/`