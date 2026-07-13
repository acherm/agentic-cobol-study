# Payroll redo — control report and remaining steps (2026-07-07)

> **✅ COMPLETED AND INGESTED (2026-07-07 evening).** Both runs finished all 6 steps
> (6 commits each). Verification performed: 12/12 prescribed paragraphs, 0 `GO TO`,
> 5 FDs, ERR-001..004, rates present (`.0730/.0690/.0240` CC; `0.073/0.069/0.024`
> Codex) — and **step-4 vs step-5 differential execution: payslips, rejects, report,
> and stdout byte-identical for BOTH agents** (the refactoring preserved behavior).
> Logs archived (CC session final; Codex June rollout *extended by the July 7
> resumption* — re-archived; plus a 7-minute `gpt-5.5` session-recovery QA exchange,
> kept as a meta session). Pipeline re-run: corpus = **15 systems**, payroll ×2 via
> `cobol-jb-cc` (sonnet-4-6, 535 code lines, 1.95 active h, High 0.62) +
> `cobol-jb-codex` (gpt-5.4, 572 code lines, 0.51 active h, High 0.67); original
> `cobol-jb` retired to `output/superseded/`. Domain coverage 7/8. Paper updated
> (pass 2) and compiles clean. **Open item: author-calibrate the Q1–Q6 rubric for
> the two new systems** (currently rendered as "pending" in Fig. rubric and worded
> as "thirteen of the 15 scored" in the paper); the pack's agent-self-applied grid
> was not run (author-applied structural checks documented instead). Historical
> control notes below.

**Canonical protocol:** `cobol-agentic-dev-case-studies` repo, branch **`agent-run-02`**,
`case-study-1.md` — 6 steps (0–5), per-step structural validation criteria, extended
evaluation grid (§8). Preserved verbatim in this repo:
[`case-study-1-agent-run-02.md`](case-study-1-agent-run-02.md) and the pack's
[`cobol-backlog-writer-SKILL.md`](cobol-backlog-writer-SKILL.md).
Intent (author, 2026-07-07): redo payroll with BOTH agents so the domain has **full raw
logs + all 6 steps** (the corpus `cobol-jb` has lost logs and only steps 0–2).

## Step ladder and status

| Step | Feature | Oracle (structural) | `cobol-jb-codex` (Codex gpt-5.4) | `cobol-jb-cc` (CC sonnet-4-6) |
|---|---|---|---|---|
| 0 | Base payroll program | compiles; PERFORM/EVALUATE/FILE SECTION/COMPUTE/88-level; ~250–350 LOC | ✅ 06-11, commit `f39ee0a` | ✅ 06-11 |
| 1 | Social contributions | rates 7.30/6.90/2.40; net-salary field | ✅ 06-11, commit `cdd737b` | ✅ 06-12 |
| 2 | Validation + reject file | 3 FDs; ERR-001..004; rejects in OUTPUT mode | ✅ 06-11, commit `17a479f` | ✅ 06-12 |
| 3 | Category report (control break) | 4 FDs; report_output OUTPUT mode; per-category accumulators | ⬜ **next** | ✅ 07-07 (prompt = pack-verbatim ✓) |
| 4 | Multi-file input & merge (fulltime/parttime) | 5 FDs; both inputs INPUT mode; per-file counters | ⬜ | ⬜ **next** |
| 5 | **Refactoring** (pure, behavior-preserving) | 12 named paragraphs (0000-MAIN … 9000-TERMINATION); **no GOTO**; outputs byte-identical | ⬜ | ⬜ |
| — | Evaluation grid (§8 of pack) | full grid over steps 0–5 | ⬜ after step 5 | ⬜ after step 5 |

Steps 3–5 prompts: copy-paste **verbatim** from `case-study-1-agent-run-02.md`
(§5 Prompt 4, §6 Prompt 5, §7 Prompt 6). Commit after each step. Archive logs same day
(`output/raw_sessions/` + MANIFEST) — both current logs are already archived
(2026-07-07 snapshots); re-archive after completion.

## ⚠ Control findings — fix before resuming

1. **`cobol-jb-codex` input is currently a 4-invalid-rows test file** (last state of the
   step-2 debugging). Running it now yields 0 valid employees, so step 3's report would
   be empty. Restore before step 3:
   ```bash
   cd ~/SANDBOX/cobol-jb-codex
   git show f39ee0a:employees_input.dat > employees_input.dat   # the 5 valid records
   cat >> employees_input.dat <<'EOF'
   000000ALICE MARTIN                  A040000002500
   000201BRUNO LAMBERT                 B000000001875
   000202CHLOE DURAND                  C032000000000
   000203DAVID MOREAU                  D045500002200
   EOF
   ```
   (5 valid + 4 invalid = mirrors the pack's mixed-input spirit; `cobol-jb-cc` has a
   10-record input, pack-conformant.)
2. **Backlog-writer skill is not installed in either redo workspace** — every prompt's
   Process step 7 says "run the backlog extractor skill", and `cobol-jb-cc` has no
   README.md at all (the skill never fired). Fix:
   - Claude Code (`cobol-jb-cc`): `mkdir -p ~/SANDBOX/cobol-jb-cc/.claude/skills/cobol-backlog-writer`
     and copy `cobol-backlog-writer-SKILL.md` there as `SKILL.md`.
   - Codex (`cobol-jb-codex`): no skill mechanism — copy the SKILL.md content into
     `~/SANDBOX/cobol-jb-codex/AGENTS.md` so step 7 resolves, or consciously keep the
     June behavior (agent-maintained README) and note the deviation.
3. **Resume commands:** `cd ~/SANDBOX/cobol-jb-codex && codex -m gpt-5.4` (pin the
   corpus model) · `cobol-jb-cc` continues in its existing session
   (`claude-sonnet-4-6` — see model note below).

## DRAFT author-calibrated rubric (2026-07-08 — awaiting author approval)

Calibration convention as for the other †-marked systems: conservative, 0.5 steps,
1 = acceptable-for-scope, 2 = clearly-good. n_bl = 6 (one backlog entry per protocol
step). Anchors: `cobol-jb` (harvested: 2/2/1.25/1.25/1.25/1.75 = 1.57), doom pair
(authored: 2/2/1.5/1.0/1.5/1.5), `SATCobol-cc` (2/2/1.5/1.0/1.5/2.0).

| Criterion | `cobol-jb-cc` | `cobol-jb-codex` | Evidence / rationale |
|---|---:|---:|---|
| Q1 correctness | 2.0 | 2.0 | Every step's structural criteria pass; reject path exercised one row per rule (ERR-001..004 correct); user inspected per-step outputs in-session; step-5 behavior preservation **differential-verified**. Caveat: salary arithmetic not cross-checked against an independent implementation (each agent generated its own test data). |
| Q2 build/run | 2.0 | 2.0 | `cobc -x -free` clean at every step; binaries run; end-of-job summaries correct in form. |
| Q3 tests | 1.0 | 1.0 | **No agent-authored test artifact.** Validation was manual runs + author-applied post-hoc checks; the pack's self-applied grid was not run by the agents. Lowest defensible score above 0-with-content. |
| Q4 robustness | 1.5 | 1.5 | Explicit 4-rule validation + reject file is a robustness feature, tested with one invalid row per rule; dual-file `AT END` handling. No fuzz/malformed-layout testing beyond that; fixed-width parsing brittle by design. |
| Q5 maintainability | 2.0 | 2.0 | Post-refactor structure objectively strong: 12 cohesive numbered paragraphs, PERFORM-only, no `GO TO`, no duplicated logic — verified structurally. Caveat: the target structure was *prescribed* by the step-5 prompt; the agents' achievement is the faithful, behavior-preserving restructuring. |
| Q6 reproducibility | 1.5 | 2.0 | Both: 6 clean commits (one per step), full raw logs archived, canonical external prompt pack, committed inputs; rebuild-from-commit demonstrated (the differential check). `cobol-jb-codex` maintains a README/backlog; **`cobol-jb-cc` has no README** (backlog skill not installed) → −0.5. |
| **Mean** | **1.67** | **1.75** | vs. superseded `cobol-jb` 1.57; corpus mean moves 1.63 → ≈1.64 over 15/15. |

### `cobol-pygame-cc` draft (added 2026-07-08, same convention; n_bl=5 protocol steps)

| Criterion | Score | Rationale |
|---|---:|---|
| Q1 correctness | 2.0 | All four example programs behave as specified (experimenter-observed: animation, BMP render, playable Flappy with gravity/pipes/score/restart); oracle is behavioral by nature of the domain. |
| Q2 build/run | 2.0 | Clean-checkout `make` builds framework + 4 executables — re-verified post-hoc headlessly (the pack's own step-5 criterion). |
| Q3 tests | 1.0 | No automated assertions; `imgtest` + `gen_test_bmp` are manual visual test programs. |
| Q4 robustness | 1.0 | Clean exit paths (Escape/close); copybook has error fields, but the missing-file error path wasn't independently exercised — raise to 1.5 if you verify it. |
| Q5 maintainability | 1.5 | Copybook API, small focused C shim, one file per example, Makefile, 15 KB fresh-user README with gotchas. |
| Q6 reproducibility | 1.5 | Clean-checkout rebuild verified; README complete; full raw log archived; only **2 git commits** for 5 steps (coarse granularity) → −0.5. |
| **Mean** | **1.50** | vs. Codex sibling `COBOL-pygame` 1.33 — plausibly better (Flappy, README, verified rebuild). |

On approval of all three: (i) add them to `AUTHORED_RUBRIC` in `draft/make_figures.py`
(n_bl = 6/6/5) and regenerate `rubric.pdf`; (ii) flip the paper's three "thirteen of
the \nSystems{} systems (three July replicas pending)" passages (abstract, RQ3,
conclusion) to sixteen-of-sixteen wording with the updated mean
((1.63·13 + 1.67 + 1.75 + 1.50)/16 ≈ **1.63** — unchanged, pleasingly).

## Notes for the paper (recorded in PAPER_PLAN)

- **Step 5 closes the paper's #1 honest gap on one domain.** The corpus currently
  reports "explicit refactoring absent (1 of 392 prompts), planned follow-up". Once
  both runs finish step 5, the payroll domain has an explicit, behavior-preserving
  refactoring ×2 agents with a structural oracle. Update: intro honest-gaps bullet,
  RQ3 honest-gaps paragraph, follow-up list ("explicit-refactor experiment" → partially
  done), threats construct-validity wording.
- **Model note:** `cobol-jb-cc` runs `claude-sonnet-4-6`, a tier below the corpus Opus.
  Decision parked (author: "decide after it finishes"): corpus-cell replacement (adds a
  third Claude tier — disclose), vs. keep `cobol-jb` (Opus, lost logs) as the corpus
  cell with the redo pair as the fully-logged 6-step extension.
- **Protocol prehistory:** two OpenCode + `gpt-5.1-codex` runs of this case study
  predate the corpus: 2026-04-02 (`cobol-jb/case-study-1/session-ses_2b16.md`) and
  2026-04-09 (`agent-run-02` branch, `session-ses_28db.md`, reached ≥ step 4 of an
  earlier pack revision). Classify as protocol-development runs (excluded from the
  corpus; one provenance sentence). The case-studies repo is the citable home of the
  payroll protocol (Sopra Steria collaboration).
