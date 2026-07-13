# RUNBOOK — the two missing ×2 replications (decided 2026-07-07: run both)

> **✅ CLOSED 2026-07-08 — THE 8×2 GRID IS COMPLETE.** R1 (payroll×Codex) done
> 2026-06-11/07-07 via the 6-step pack; R2 (pygame×Claude Code) done 2026-07-08
> (`claude-opus-4-6`, all 5 replay steps, Flappy Bird in pure COBOL, clean-checkout
> `make` re-verified). Both logs archived + manifested; both ingested. Corpus:
> **16 systems, 8/8 domains ×2**. Verification + rubric drafts:
> `replications/payroll-remaining-steps.md`. Historical instructions below.

Goal: complete the 8-domains × 2-agents grid (14 → **16 systems**) before the arXiv
submission. Two cells are missing:

| # | Case study | Exists | To run | Suggested folder |
|---|---|---|---|---|
| R1 | Payroll | `cobol-jb` (Claude Code) | **Codex CLI** | `~/SANDBOX/cobol-jb-codex` |
| R2 | pygame framework | `COBOL-pygame` (Codex) | **Claude Code** | `~/SANDBOX/cobol-pygame-cc` |

Deadline guardrail: if either run is not finished by **Wednesday morning**, fall back to
the paper's existing "two replications in progress" wording. The arXiv date wins.

Methodological note: the experimenter (first author) drives both sessions, as for all
prior systems — the human-in-the-loop role is part of the method. Note the CLI version
and model at session start (they go in the per-session table).

**Model choice (decided 2026-07-07): pin the corpus-era models, not the current default.**
- R2 (Claude Code): launch with `claude --model claude-opus-4-6` — verified still served
  on 2026-07-07. This matches 12 of the 13 corpus Claude Code sessions and keeps the two
  grid-completing cells inside the study's model era. Fallback if it disappears:
  `claude-opus-4-7` (already in the corpus via `cobol-doom-cc`), then `claude-opus-4-8`
  with a drift sentence in Threats. Do **not** use the Claude 5 family (Fable/Sonnet 5):
  a next-generation tier would invite the "late cells used a stronger model" critique.
- R1 (Codex): pin `gpt-5.4` if the CLI still offers it (`codex -m gpt-5.4`), same
  fallback logic (newest gpt-5.x, disclose the drift).
- Use default settings — no extra reasoning flags, no non-corpus features — so the
  sessions stay comparable to the corpus.
- Either way, extend the existing agent-and-version-drift paragraph in Threats with one
  sentence: the two replications ran ~3 months after the main window on <model, version>.

---

## R1 — Payroll × Codex — ⚠ STATUS CORRECTED 2026-07-07: ALREADY RUN on 2026-06-11

Discovered on disk (author was right): `~/SANDBOX/cobol-jb-codex` exists — built
**2026-06-11** by Codex CLI **0.138.0-alpha.7, model `gpt-5.4`** (corpus-consistent ✓),
one rollout (441 lines), **archived** into `output/raw_sessions/` on 2026-07-07 and
added to `MANIFEST.csv`. It was run **after the June 4 analysis freeze**, which is why
every artifact (REPORT.md, domain_coverage, metrics, the paper) still calls it missing.

State observed:
- 3 git commits matching replay Steps 1–3 (base program → social-contribution
  deductions → validation + reject file). `program.cbl` ≈ 500 lines; binary compiles.
- **Steps 4–5 appear NOT run** (no formatting-polish commit, no
  `VERIFICATION_REPORT.md`).
- Current on-disk `employees_input.dat` is a 4-row all-invalid rejects test (different
  layout/data than the replay pack's sample); re-running the binary yields 4/4 correct
  ERR-001..004 rejects, 0 valid. The full-input totals check (6,425.65 / 5,359.06) must
  be recovered from the rollout log or re-run during ingest.

Remaining for R1 — ✅ RESOLVED 2026-07-07: the canonical 6-step protocol was located
(`cobol-agentic-dev-case-studies` repo, branch `agent-run-02`); the author is completing
BOTH payroll runs to all 6 steps with full logs. **See
[`payroll-remaining-steps.md`](payroll-remaining-steps.md)** for the control report,
status matrix (Codex: steps 3–5 remaining; CC: steps 4–5), pre-resume fixes (restore
jb-codex's full input from `git show f39ee0a:employees_input.dat`; install the
backlog-writer skill), and the step-5 refactoring payoff for the paper. After step 5 +
evaluation grid: archive logs, ingest into the pipeline.

### ⚠ Bonus discovery: `~/SANDBOX/cobol-jb-cc` (role to decide)

A SECOND new payroll run exists: Claude Code, **model `claude-sonnet-4-6`** (not the
corpus Opus), one session started 2026-06-11, **resumed 2026-07-07** (same day as this
note), Steps 1–3 committed. Its raw log was 4 days from the 30-day purge —
**archived 2026-07-07** (`output/raw_sessions/cobol-jb-cc__e901e55b….jsonl`;
session still active, re-archive after it ends). Role in the paper to decide:
exclude / auxiliary mid-tier-model data point (bridges pilots ↔ frontier corpus) /
replay-pack validation evidence. It is NOT the missing cell (payroll×CC already exists
as `cobol-jb`).

## R2 — pygame × Claude Code (~1–2 h expected; sibling: 0.6 active h, but sibling stopped early — this replica may go further)

```bash
mkdir ~/SANDBOX/cobol-pygame-cc && cd ~/SANDBOX/cobol-pygame-cc && git init
claude   # note CLI version + model
```

Feed the five steps of
`output/backlogs/COBOL-pygame/REPLAY_PROMPTS.md`
sequentially, verbatim (Step 1 framework + copybook + Makefile → Step 2 bouncing-rectangle
example → Step 3 BMP/image support → Step 4 Flappy Bird in pure COBOL → Step 5 README +
clean-checkout reproducibility). Boundary rule is encoded in Step 4: *"No C code inside the
game itself"* — enforce it if the agent drifts (that enforcement is itself data: log it).

Scope decision to make explicit in your notes: the Codex sibling effectively delivered
Steps 1–2 (+Flappy example); running all 5 steps makes the CC replica *richer* than the
sibling. Either stop at the sibling's scope (strict replication) or run all 5 and say so
in the paper (the corpus already has asymmetric siblings; just document it).

---

## Immediately after EACH session (same day — this is the data-loss lesson)

1. **Archive the raw log** into the repo:
   - Codex: `cp ~/.codex/sessions/2026/07/<DD>/rollout-*.jsonl <repo>/output/raw_sessions/`
     (pick the file whose `session_meta.cwd` is the new project dir).
   - Claude Code: `cp ~/.claude/projects/-Users-mathieuacher-SANDBOX-cobol-pygame-cc/*.jsonl <repo>/output/raw_sessions/`
     — do it the same day; do not trust `cleanupPeriodDays`.
   - Append both to `output/raw_sessions/MANIFEST.csv` (and note CLI version + model).
2. **Ingest into the pipeline** (scoped rebuild — do NOT blanket-run `REBUILD_FROM_RAW=1`,
   which would rebuild aggregates from the depleted April logs):
   - Add the two new sessions to `output/sessions_all.json` and emit their
     `output/turns/*.jsonl` (run `scripts/parse_sessions.py` / `scripts/deep_analyze.py`
     restricted to the two new project dirs, then merge — check each script's filtering
     options first).
   - Then re-run stages 2, 4–8 of `scripts/run_all.sh` (they read committed artifacts).
   - Re-run `scripts/emit_paper_numbers.py` → `draft/numbers.tex` refreshes the paper's
     headline macros.
3. **Post-session analyst** (optional this week, needed for rubric parity): run
   `prompts/post-session-analyst.md` on each new project (or author-calibrate the rubric
   as for the other 5 †-marked systems and mark it † in Fig. rubric).
4. Paper deltas (Wed): Table 1 +2 rows, per-session appendix +2 rows, "6/8 ×2" → "8/8 ×2",
   remove "two replications in progress" sentences (grep: `in progress`, `planned`),
   corpus counts via `numbers.tex`, add 2 one-line vignette capsules in the appendix.
