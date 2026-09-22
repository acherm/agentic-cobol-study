# Key Features — cobol-jb-codex (PAYROLL-COBOL-CODEX)

## Preamble

> **Provenance.** Authored 2026-08-20 by the study authors from the archived raw
> rollouts (June session extended by the 2026-07-07 resumption, re-archived in
> `output/raw_sessions/`), the delivered source (`program.cbl`, 572 code lines,
> 6 protocol commits), and the canonical payroll protocol
> (`replications/case-study-1-agent-run-02.md`, status in
> `replications/payroll-remaining-steps.md`). Same conventions and score
> formula as the thirteen analyst-generated ledgers
> (depth × (1 + 0.5 × effort)).

Same six-step protocol as its Claude sibling, on `gpt-5.4`, one commit per
step, plus an agent-maintained README backlog. The delivered program answers
the same structural criteria through a visibly different implementation:
lowercase identifier style, a leaner data division (103 data items vs the
sibling's 192), and its own record layouts — the payroll pair's non-copy
evidence at the idiom level. Feature classes concentrate in DOM and VER with
the step-5 refactoring as the composition entry.

## Ranked table

| Rank | SB id | Title | Class | Depth | Effort | Score | Evidence | Significance note |
|------|-------|-------|-------|-------|--------|-------|----------|-------------------|
| 1 | SB-5 | Behavior-preserving refactoring of the procedure division, zero GO TO | CMP+VER | 3 | 2 | 6.0 | commit `03c677a`; `program.cbl:207-647` (`0000-MAIN` … `9000-TERMINATION`, 12 prescribed paragraphs); step-4 vs step-5 differential execution byte-identical | The protocol's capstone: full restructuring with outputs frozen, verified by differential execution of the pre/post commits — the same oracle shape as its sibling, independently reached. |
| 2 | SB-4 | Dual-input multi-file merge (fulltime/parttime), 5 FDs, per-file counters | DOM | 2 | 2 | 4.0 | commit `65a755c`; `program.cbl:7-57` (5 lowercase SELECT/FD pairs); `2000-PROCESS-LOOP` dual-stream handling | Same multi-file topology as the sibling, distinct layout and read-loop structure. |
| 3 | SB-2 | Input validation with reject file (ERR-001..ERR-004) | DOM+VER | 2 | 2 | 4.0 | commit `17a479f`; `3100-VALIDATE-RECORD`; `4100-WRITE-REJECT`; session incident: 4-invalid-row test input left in place after step-2 debugging, restored before step 3 (`payroll-remaining-steps.md` §control findings) | Reject FD in OUTPUT mode with four rule codes; the debugging leftovers episode shows the validation path was genuinely exercised. |
| 4 | SB-3 | Category summary report (control break, per-category accumulators) | DOM | 2 | 1 | 3.0 | commit `c39c281`; `5000-WRITE-REPORT` | Prescribed control-break idiom written to the report FD. |
| 5 | SB-0 | Base payroll program (FDs, EVALUATE, COMPUTE, 88-levels) | DOM | 2 | 1 | 3.0 | commit `f39ee0a`; `3200-COMPUTE-SALARY` | Greenfield batch shape per protocol; free-format, lowercase idiom. |
| 6 | SB-1 | Social-contribution deductions with net-salary field | DOM | 1 | 1 | 1.5 | commit `cdd737b`; `3300-COMPUTE-DEDUCTIONS` (rates 0.073/0.069/0.024) | Protocol-checked rates and rounded arithmetic. |

## Composition chains

1. **Steps 0→4 → refactoring under a byte-identity oracle** — identical chain
   shape to the sibling: SB-5 is only checkable because SB-0..SB-4 ship
   deterministic, committed outputs. That both agents independently pass the
   same differential oracle is the pair's headline result.

## Significance profile

| Class | Count in top 6 |
|-------|----------------|
| DOM   | 5 |
| VER   | 2 |
| CMP   | 1 |
| ALG/LNG/SYS/INF/PRF/PRO | 0 |

Centre of gravity: **DOM + VER**, one CMP entry — mirroring the sibling, as
the protocol intends.

## Verdict

Protocol-fidelity project and the second half of the corpus's verified
refactoring pair: same structural criteria met through an independently
styled implementation, with the June-to-July session resumption and the
restored-input control finding documented in the replication notes.
