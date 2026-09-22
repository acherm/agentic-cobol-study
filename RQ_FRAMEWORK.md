# Research-Question Framework for Per-Project Reports

Each per-project report (`output/reports/<project>.md`) follows the same RQ-indexed
structure, filled by scripts under `scripts/`. Everything is derivable from three
data sources: (i) the project folder, (ii) `.git` history if present, (iii) the
coding-agent JSONL transcripts under `~/.claude/projects/` and `~/.codex/sessions/`.

## RQ index

| # | Question | Sections of report | Data sources |
|---|---|---|---|
| RQ1 | **What is this project about?** Domain of interest, novelty, the why. | §1 Story | README / SPECIFICATION / first user prompt |
| RQ2 | **What were the engineering challenges?** High-level + sub-challenges. | §2 Challenges | README + last-N assistant summaries + activity mix |
| RQ3 | **What was delivered at the end?** Working artefact? What works / what doesn't? | §3 Outcome | README "what works" sections + last assistant turn + presence of binaries + tests-pass signals |
| RQ2b | **What features were actually built?** Feature ledger from backlog / README / prompts / git. | §2b Feature ledger | `scripts/feature_ledger.py` |
| RQ4 | **How big and how complex is the code?** Files, LOC, COBOL structural metrics. | §4 Size & complexity | `scripts/cobol_complexity.py` + file inventory |
| RQ4b | **How much of the COBOL language is exercised?** Mastery score, capability matrix (10 categories). | §4b COBOL mastery | `scripts/cobol_complexity.py` (capabilities) |
| RQ5 | **How was time/effort allocated across SE tasks?** | §5 Effort distribution | Active-time attribution per turn classification |
| RQ6 | **What failed and how often?** Build errors, runtime errors, dead-ends, abandoned paths. | §6 Failures | Tool-result error mining, "fix"-prompt count |
| RQ6b | **How hard was this, objectively?** Composite difficulty index + auto-label (Low/Medium/High/Very-High). | §6b Difficulty | 7-signal rank average: active_hours, span_days, user_prompts, redirect/bug prompts, error_rate, fix_cycles, fix_time_share |
| RQ7 | **What user strategy drove the collaboration?** Specs up-front vs vibes, length of prompts, number of sessions, resume pattern. | §7 Strategy | Prompt corpus stats + session cadence |
| RQ8 | **Which user interventions were needed?** Types of user messages (initial, clarify, redirect, review, bug report). | §8 User interventions | User-prompt classifier |
| RQ9 | **What did it cost in compute?** Tool calls, tokens, estimated USD, wall/active time. | §9 Cost | Tokens & costs from session parser |

## Taxonomies

### SE-task classes (per turn)

The per-turn label is assigned in two passes. First, a default label is
derived from the tool used and the command string (e.g. `Edit`/`apply_patch`
→ `feature`, `Bash` running `cobc` → `build`). Then a **contextual rule**
fires: any edit or re-run that happens within 3 turns after an error tool
output is relabeled `bug_fix`. This is what separates "adding new code" from
"trying to make broken code work".

- `feature` — adding new functionality
- `bug_fix` — correcting an observed defect
- `performance` — making it faster (optimizing)
- `test` — writing, running, or interpreting tests / benchmarks
- `refactor` — restructuring without behaviour change
- `understanding` — reading existing code, searching for context (was `research`)
- `build` — compile / makefile / deps
- `spec` — specifications / architecture docs
- `doc` — README / comments / reports
- `port` — translating between languages / formats
- `verification` — auditing, review, grid-verification (was `review`)
- `plan` — task tracking, housekeeping (was `meta`)
- `unknown`

### Error signals mined from tool-result output
- GnuCOBOL compiler errors (`cobc:` prefix, `syntax error`, `unresolved symbol`)
- C compiler/linker errors (`error:`, `undefined reference`)
- Segmentation fault / bus error / abort
- Python traceback
- `FAIL(ED)` in test-runner output
- Non-zero exit code (when explicit in the tool stub)

### User-prompt intent classes
- `initial-spec` — first prompt of a session, contains requirements
- `clarify` — short follow-up answering an agent question
- `redirect` — change of direction mid-session
- `bug-report` — user describes a failure they observed
- `review-ask` — user asks for review / verification / summary
- `resume` — resumed session (short "continue" style)
- `other`

## Pipeline

```
~/.claude/projects/*.jsonl   \
~/.codex/sessions/**/*.jsonl  ──► scripts/deep_analyze.py
                                      │
                                      ▼
                               output/turns/<session>.jsonl  (one row per turn)
                                      │
~/SANDBOX/<project>/ ──► scripts/cobol_complexity.py + scripts/git_stats.py
                                      │
                                      ▼
                           scripts/project_metrics.py  ──► output/metrics/<project>.json
                                      │
                                      ▼
                      scripts/generate_project_reports.py  ──► output/reports/<project>.md
                                      │
                                      ▼
                          scripts/generate_report.py (cross)  ──► REPORT.md
```

Everything is idempotent; `scripts/run_all.sh` rebuilds in order.

## Difficulty index — ground-truth validation

Automated difficulty labels were sanity-checked against the user's recollection
of how each project felt to build:

| User's recollection | Auto-label |
|---|---|
| "compress was smooth" (`cobol-compress-cc`) | **Low** (0.21) ✓ |
| "game of 15 was smooth" (`cobol-tictactoe`) | **Medium** (0.37), borderline Low — reasonable |
| "chess needed more effort / pushing" (`chess-cobol-cc`, `COBOL-chess`) | **High** (0.50, 0.69) ✓ |
| "compiler was intensive, especially at the end" (`cobol-compiler-cc`) | **Very-High** (0.86) ✓ top rank on active hours, prompts, redirects and fix cycles |

The bug-fix contextual re-classification is what surfaces the "intensive end"
of the compiler project: a simple tool-based classifier would mis-label every
`Edit` as `feature`, hiding the fact that 42 of them came directly after a
failed build.

