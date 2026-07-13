# Replay Prompts

Reusable prompts for reproducing the COBOL payroll case-study step by step. Each prompt is self-contained enough to copy-paste into a coding agent session. They specify **what** to build (behavior, inputs, outputs, verification), not **how** (no algorithm names, no data structure prescriptions, no COBOL-specific idioms).

Use them sequentially: each step builds on the previous one.

For reference on what was actually built (constructs chosen, gaps encountered, autonomous decisions), see [SPECIFICATION_BACKLOG.md](SPECIFICATION_BACKLOG.md).

---

## Step 1: Base Payroll Program

> Write a COBOL program (GnuCOBOL) for a payroll management system. It must compile with `cobc -x -free -o program program.cbl` and be named `program.cbl`.
>
> The program reads employee records from `employees_input.dat` and writes one formatted payslip per employee to `payslips_output.dat`. At end of job it displays summary totals on standard output.
>
> **Input record layout** (one employee per line, fixed-width, space-separated fields):
> ```
> EMPID  NAME                           C HHHHH RRRRR
> ```
> - `EMPID`: 6-digit employee identifier
> - `NAME`: 30-character employee name (space-padded)
> - `C`: 1-character job category (`A`, `B`, or `C`)
> - `HHHHH`: hours worked, 5 digits representing a value with 2 decimals (e.g. `04200` = 42.00 hours)
> - `RRRRR`: hourly rate in EUR, 5 digits representing a value with 2 decimals (e.g. `02500` = 25.00 EUR)
>
> **Sample input** (`employees_input.dat`):
> ```
> 000001 Dupont Marie                   A 04200 02500
> 000002 Martin Jean                    B 03500 01800
> 000003 Durand Sophie                  C 04000 01500
> 000004 Bernard Lucas                  A 03000 03000
> 000005 Petit Claire                   B 03850 02200
> 000006 Robert Thomas                  C 02800 01200
> 000007 Richard Emma                   A 04500 02800
> 000008 Moreau Pierre                  B 03600 01950
> ```
>
> **Business rules for gross salary**:
> 1. Regular hours = `MIN(hours_worked, 35)`; overtime hours = `MAX(hours_worked - 35, 0)`.
> 2. Regular pay = regular hours × hourly rate.
> 3. Overtime pay depends on job category:
>    - Category A (Senior/Management): overtime hours paid at 1.20 × hourly rate (+20% bonus)
>    - Category B (Standard Employee): overtime hours paid at 1.10 × hourly rate (+10% bonus)
>    - Category C (Junior/Intern): overtime hours paid at 1.00 × hourly rate (no bonus)
> 4. Gross salary = regular pay + overtime pay.
>
> **Payslip output**: for each employee, write a readable formatted block to `payslips_output.dat` including: employee name and ID, job category (with its label), hours worked, hourly rate, regular hours + regular pay, overtime hours + overtime pay, overtime multiplier, and gross salary. Monetary values in EUR with 2 decimals and thousands separators.
>
> **End-of-job summary** (on standard output): total employees processed and total gross payroll.
>
> Include a `README.md` describing the build command, run command, input layout, and business rules.
>
> **Verification**:
> - `cobc -x -free -o program program.cbl` exits 0 with no errors (warnings acceptable).
> - `./program` runs cleanly and creates a non-empty `payslips_output.dat`.
> - For the sample input above (8 employees), total gross payroll is `6,425.65 EUR`, with 3 category-A, 3 category-B, and 2 category-C employees.

---

## Step 2: Social-Contribution Deductions and Net Salary

> Extend `program.cbl` to compute and report social-contribution deductions on top of the gross salary.
>
> **Deductions** (all applied to the gross salary):
> - Health insurance: **7.30%** of gross
> - Retirement contribution: **6.90%** of gross
> - Unemployment insurance: **2.40%** of gross
> - Total deduction = sum of the three
> - Net salary = gross salary − total deduction
>
> Values must be rounded to 2 decimals (standard half-up or banker's rounding is fine — be consistent).
>
> **Payslip output**: each payslip block must now additionally include, in a clearly labelled "Social Contributions" section: health deduction, retirement deduction, unemployment deduction, total deduction, and net salary. All monetary values in EUR with 2 decimals.
>
> **End-of-job summary** (on standard output): keep total employees processed and total gross payroll, and add **total net payroll**. Optionally also report totals per category and total regular/overtime hours.
>
> **Constraints**:
> - Do not break Step 1 behavior: gross-salary computation and category-based overtime rules must remain intact.
> - The program must still compile cleanly with `cobc -x -free -o program program.cbl`.
> - Update `README.md` to document the new deduction fields and extended summary.
>
> **Verification** (using the 8-employee sample input from Step 1):
> - Compilation exits 0 with no errors.
> - Source contains the rates `7.30`, `6.90`, `2.40` (or `0.0730`, `0.0690`, `0.0240`).
> - Payslip output contains a net-salary field per employee.
> - End-of-job summary shows:
>   ```
>   Total Employees Processed  :       8
>   Total Gross Payroll        :      6,425.65 EUR
>   Total Net Payroll          :      5,359.06 EUR
>   ```
> - Example expected per-employee values (employee 000001, Dupont Marie, cat A, 42h @ 25.00 EUR):
>   gross 1,085.00 / health 79.20 / retire 74.86 / unempl 26.04 / total deduct 180.10 / net 904.90.

---

## Step 3: Input Validation and Reject File

> Extend `program.cbl` to validate each input record before processing and to route invalid records to a dedicated reject file.
>
> **Validation rules** (apply in order; the first rule that fails assigns the error code):
> - `ERR-001`: Employee ID must not be spaces or all zeros.
> - `ERR-002`: Hours worked must be strictly greater than 0 and at most 80.
> - `ERR-003`: Hourly rate must be strictly greater than 0 and at most 999.99.
> - `ERR-004`: Job category must be `A`, `B`, or `C`.
>
> **Behavior**:
> - A record that fails any rule is NOT processed (no salary math, no payslip written).
> - Invalid records are written to a new output file `rejects_output.dat`, each reject line containing the **original employee record** followed by the **error code** (e.g. `ERR-002`).
> - Valid records continue to produce a payslip exactly as in Step 2.
>
> **End-of-job summary** (on standard output): in addition to totals from Step 2, add:
> - Total employees rejected (count written to the reject file)
> - Errors encountered (can equal rejected count if one error code per record)
>
> Keep the distinction clear between employees processed (valid) and employees rejected.
>
> **Extended sample input** (`employees_input.dat`) — add 4 invalid rows at the end so each rule fires once:
> ```
> 000001 Dupont Marie                   A 04200 02500
> 000002 Martin Jean                    B 03500 01800
> 000003 Durand Sophie                  C 04000 01500
> 000004 Bernard Lucas                  A 03000 03000
> 000005 Petit Claire                   B 03850 02200
> 000006 Robert Thomas                  C 02800 01200
> 000007 Richard Emma                   A 04500 02800
> 000008 Moreau Pierre                  B 03600 01950
> 000000 Ghost Employee                 A 03500 02000
> 000010 Lazy Worker                    B 00000 02000
> 000011 Greedy Boss                    A 04000 00000
> 000012 Unknown Category               X 03500 01500
> ```
>
> **Expected `rejects_output.dat`**:
> ```
> 000000 Ghost Employee                 A 03500 02000 ERR-001
> 000010 Lazy Worker                    B 00000 02000 ERR-002
> 000011 Greedy Boss                    A 04000 00000 ERR-003
> 000012 Unknown Category               X 03500 01500 ERR-004
> ```
>
> **Constraints**:
> - Do not break Step 1 / Step 2 behavior: overtime rules, deduction rates (7.30%, 6.90%, 2.40%), and net-salary computation must remain intact.
> - The program must still compile cleanly with `cobc -x -free -o program program.cbl`.
> - Update `README.md` to document the validation rules, the reject file, and the new summary counters.
>
> **Verification** (with the 12-employee input above):
> - Compilation exits 0 with no errors.
> - Three distinct input/output files are declared in the program (`employees_input.dat`, `payslips_output.dat`, `rejects_output.dat`); the reject file is opened in output mode.
> - Source contains the strings `ERR-001`, `ERR-002`, `ERR-003`, `ERR-004`.
> - `rejects_output.dat` has exactly 4 lines, matching the expected content above.
> - End-of-job summary shows 8 employees processed, 4 rejected, total gross payroll `6,425.65 EUR`, total net payroll `5,359.06 EUR`.
> - Source still contains `7.30`, `6.90`, `2.40` and the overtime bonus logic.

---

## Step 4: Formatting and Summary Report Polish

> Polish the payslip output and end-of-job summary so that the generated artefacts are publication-quality.
>
> Each payslip block in `payslips_output.dat` should be visually separated (e.g., a banner line of `=` characters between employees) and include:
> - A run header (report title + run date) at the top of the file.
> - A clearly labelled payslip header identifying the employee.
> - Employee ID, job category (with its human-readable label: `A - Senior/Management`, `B - Standard Employee`, `C - Junior/Intern`), date issued.
> - Hours worked, hourly rate, regular hours with pay, overtime hours with pay, overtime multiplier.
> - A `GROSS SALARY` line, a `Social Contributions` sub-section with the three deductions and the total, and a final `NET SALARY` line.
>
> The end-of-job summary on standard output should be framed by a banner (e.g., `*` characters) and include, at minimum:
> ```
> Total Employees Processed  :       8
> Total Gross Payroll        :      6,425.65 EUR
> Total Net Payroll          :      5,359.06 EUR
> Category A Employees       :       3
> Category B Employees       :       3
> Category C Employees       :       2
> Total Regular Hours        :      268.00
> Total Overtime Hours       :       26.50
> Errors Encountered         :       4
> Employees Rejected         :       4
> ```
>
> Monetary values must use 2 decimals and comma thousands-separators; hour counts use 2 decimals. The run date can be filled from the system clock.
>
> **Constraints**:
> - No regression: all Step 1–3 behavior and verification rules still apply.
> - The program must still compile cleanly with `cobc -x -free -o program program.cbl`.
>
> **Verification**:
> - Running `./program` with the 12-employee input produces a `payslips_output.dat` whose first payslip (Dupont Marie, cat A, 42h @ 25.00 EUR) contains the lines:
>   ```
>   GROSS SALARY   :     1,085.00 EUR
>   ...
>   NET SALARY     :       904.90 EUR
>   ```
> - The end-of-job summary block on stdout matches the totals shown above exactly for the counts (8, 3, 3, 2, 4, 4) and the monetary totals (`6,425.65` / `5,359.06`).

---

## Step 5: Self-Applied Verification Grid

> Without modifying `program.cbl`, produce a `VERIFICATION_REPORT.md` file that scores the repository against the following 27-criterion grid. For each criterion, record PASS or FAIL with a short evidence note (file name / line range / command output).
>
> **Step 0 — Base generation (9 criteria)**:
> 1. `program.cbl` exists in the workspace.
> 2. Compilation: `cobc -x -free -o program program.cbl` exits 0 with no errors.
> 3. Approximate LOC between 250 and 350.
> 4. Source uses a loop / iteration construct for processing records.
> 5. Source uses a multi-branch conditional construct for the category-based overtime logic.
> 6. File declarations for `employees_input.dat` and `payslips_output.dat` are present.
> 7. Source uses explicit arithmetic expressions for the salary calculations.
> 8. Source declares at least one named boolean/flag condition.
> 9. `README.md` exists and documents the base program.
>
> **Step 1 — Social contributions (8 criteria)**:
> 10. Compilation still exits 0 with no errors.
> 11. Health rate `7.30` (or `0.073`) present in source.
> 12. Retirement rate `6.90` (or `0.069`) present in source.
> 13. Unemployment rate `2.40` (or `0.024`) present in source.
> 14. A net-salary variable is declared (any name).
> 15. Payslip output record has at least 5 distinct fields.
> 16. Overtime / category branching logic from Step 0 still present (no regression).
> 17. `README.md` was updated after Step 1.
>
> **Step 2 — Validation & reject file (10 criteria)**:
> 18. Compilation still exits 0 with no errors.
> 19. Three file declarations present (`employees_input.dat`, `payslips_output.dat`, `rejects_output.dat`).
> 20. `rejects_output.dat` is opened in output mode.
> 21. String `ERR-001` present in source.
> 22. String `ERR-002` present in source.
> 23. String `ERR-003` present in source.
> 24. String `ERR-004` present in source.
> 25. A rejected-record counter variable is declared.
> 26. Rates `7.30`, `6.90`, `2.40` still present (no regression).
> 27. `README.md` was updated after Step 2.
>
> **Process**:
> 1. Recompile the program and run it once against `employees_input.dat` to confirm reproducibility.
> 2. Use `grep`, `wc -l`, and `git log`/`git show` on `README.md` to gather evidence for each criterion.
> 3. Write `VERIFICATION_REPORT.md` with one row per criterion, a "Step X: n/m" subtotal, a "Failures Summary" section, and a final `Score: N/27` line.
>
> **Scoring interpretation**:
> - 27/27: Perfect reproduction.
> - 24–26/27: Near-identical — minor acceptable differences.
> - 19–23/27: Partial reproduction — some constraints missed.
> - < 19/27: Insufficient reproduction — significant divergence.
>
> Target: 25/27 or better. Typical near-misses observed in prior runs: criterion #3 (LOC above the 350 upper bound because of verbose formatting records) and criterion #27 (README not updated when the validation feature was added).
