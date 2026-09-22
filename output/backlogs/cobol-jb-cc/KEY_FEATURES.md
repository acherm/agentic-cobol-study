# Key Features — cobol-jb-cc (PAYROLL-COBOL-CLAUDE)

## Preamble

> **Provenance.** Authored 2026-08-20 by the study authors from the archived raw
> session transcript (`output/raw_sessions/cobol-jb-cc__e901e55b….jsonl`), the
> delivered source (`program.cbl`, 535 code lines, 6 protocol commits), and the
> canonical payroll protocol (`replications/case-study-1-agent-run-02.md`,
> status in `replications/payroll-remaining-steps.md`). The July replicas'
> sessions post-date the analyst-subagent pass that generated the other
> thirteen ledgers; same conventions, same score formula
> (depth × (1 + 0.5 × effort)).

The project executes the externally authored six-step payroll protocol
(steps 0–5) on `claude-sonnet-4-6`, one commit per step. The task family
deliberately targets canonical mainframe idioms rather than novelty: FDs,
88-levels, EVALUATE, COMPUTE ROUNDED, control-break reporting, multi-file
merge, and a prescribed behavior-preserving refactoring. The key features
therefore sit in domain modelling (DOM) and verification (VER), with one
composition entry: the step-5 refactoring, which is only meaningful on top of
all five prior steps and was proven behavior-preserving by differential
execution of the pre- and post-refactoring commits.

## Ranked table

| Rank | SB id | Title | Class | Depth | Effort | Score | Evidence | Significance note |
|------|-------|-------|-------|-------|--------|-------|----------|-------------------|
| 1 | SB-5 | Behavior-preserving refactoring into 12 prescribed paragraphs, zero GO TO | CMP+VER | 3 | 2 | 6.0 | commit `f185429`; `program.cbl:290-598` (`0000-MAIN` … `9000-TERMINATION`); step-4 vs step-5 differential execution: payslips, rejects, report, stdout byte-identical | Only meaningful once steps 0–4 exist: the whole program is restructured (PERFORM-only, cohesive numbered paragraphs) under a byte-identity oracle. This is the corpus's explicit refactoring exercise, ×2 agents. |
| 2 | SB-4 | Dual-input multi-file merge (fulltime/parttime), 5 FDs, per-file counters | DOM | 2 | 2 | 4.0 | commit `d5fc902`; `program.cbl:11-56` (5 SELECT/FD pairs), `2100-READ-NEXT-RECORD` with per-stream `AT END` EVALUATEs | Classic mainframe multi-file topology: two sequential inputs consumed to exhaustion with independent end-flags and per-file counters, three outputs. |
| 3 | SB-2 | Input validation with reject file (ERR-001..ERR-004) | DOM+VER | 2 | 2 | 4.0 | commit `9718d9d`; `3100-VALIDATE-RECORD` EVALUATE cascade; `4100-WRITE-REJECT`; `rejects_output.dat` | Four rule codes with a dedicated reject FD in OUTPUT mode; the reject path doubles as the program's robustness surface and was exercised one row per rule. |
| 4 | SB-3 | Category-level control-break report with indexed accumulator table | DOM | 2 | 1 | 3.0 | commit `0b3240b`; `WS-CAT-ENTRY OCCURS 3 INDEXED BY WS-CAT-IDX` (`program.cbl:141`); `5000-5300` report paragraphs | Per-category accumulators + grand total written to a fifth file — the control-break idiom the protocol prescribes. |
| 5 | SB-0 | Base payroll program (FDs, 88-levels, EVALUATE, fixed-width parsing) | DOM | 2 | 1 | 3.0 | commit `583a5ae`; `3200-COMPUTE-SALARY` nested EVALUATEs | Greenfield step: canonical batch shape (read–validate–compute–write) in free-format GnuCOBOL. |
| 6 | SB-1 | Social-contribution deductions with rounded arithmetic | DOM | 1 | 1 | 1.5 | commit `a645433`; `3300-COMPUTE-DEDUCTIONS` (`COMPUTE … ROUNDED`, rates .0730/.0690/.0240) | Small but protocol-checked: three named rates, net-salary field, ROUNDED arithmetic. |

## Composition chains

1. **Steps 0→4 → refactoring under a byte-identity oracle** — SB-0..SB-4 build
   the behavior; SB-5 restructures all of it with the outputs frozen. The
   differential execution of the two commits is the emergent verification
   capability: refactoring is only checkable because every prior feature ships
   committed inputs and deterministic outputs.

## Significance profile

| Class | Count in top 6 |
|-------|----------------|
| DOM   | 5 |
| VER   | 2 |
| CMP   | 1 |
| ALG/LNG/SYS/INF/PRF/PRO | 0 |

Centre of gravity: **DOM + VER**, one load-bearing CMP entry (the verified
refactoring). No algorithmic or FFI content — by protocol design.

## Verdict

Canonical-idiom project: the value is not novelty but protocol fidelity —
six steps, six commits, structural criteria met at every step, and a
behavior-preserving refactoring proven on byte-identical outputs.
