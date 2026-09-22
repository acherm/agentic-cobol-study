# Meta-Analysis: COBOL Projects Built with Coding Agents

**Scope.** All `~/SANDBOX/*cobol*` / `*COBOL*` project directories on this machine, cross-referenced with locally-stored coding-agent session logs (`~/.claude/projects/*.jsonl` for Claude Code, `~/.codex/sessions/**/*.jsonl` for Codex).

**Generated.** 2026-04-15 (by automated scripts in `scripts/`, results in `output/`).

## 1. Methodology

- **Project discovery.** Listing of `~/SANDBOX/` filtered on `cobol` / `COBOL`.
- **Session discovery.** For Claude Code: one directory per project under `~/.claude/projects/`, each `.jsonl` is a session. For Codex: rollout files under `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*.jsonl`, matched on `session_meta.cwd`. For Cline: no on-disk JSONL trace was found in this environment — only artifacts.
- **Per-session metrics** (script: `scripts/parse_sessions.py`):
  - agent = `Claude Code` or `Codex`;
  - model from `message.model` (CC) or `turn_context.model` (Codex);
  - CLI version from `session_meta.cli_version` / Claude Code `version` field;
  - duration = wall-clock between first and last event (⚠ includes idle gaps across days when a session is resumed);
  - tool calls counted from `tool_use` blocks (CC) or `response_item.function_call` / `custom_tool_call` (Codex);
  - tokens from `message.usage` (CC) or `event_msg.token_count.info.total_token_usage` (Codex).
  - **cost is an upper-bound estimate** at public API rack rates — real spending under Team/Max subscriptions differs; rates table is inlined in `scripts/parse_sessions.py`.
- **LOC / inventory** (script: `scripts/analyze_projects.py`): walks each project, skipping `.git`, `build`, `external`, `node_modules`, `cutechess`; lines counted with Python `for _ in f`.
- **Activity classification.** Keyword matching on the first user prompt (see `ACTIVITY_KWS` in `scripts/analyze_projects.py`). This is a rough thematic proxy, not a full QA of every turn.
- **Deep per-turn analysis** (new): `scripts/deep_analyze.py` emits one JSONL per session under `output/turns/<project>__*.jsonl`, with one row per event (user prompt, assistant message, tool call, tool result). `scripts/project_metrics.py` turns those into per-project aggregates under `output/metrics/`; `scripts/generate_project_reports.py` renders a full RQ-labeled Markdown per project under `output/reports/`.
- **RQs** answered per-project are defined in [`RQ_FRAMEWORK.md`](RQ_FRAMEWORK.md). The full pipeline is one command: `scripts/run_all.sh`.

## 2. Summary at a glance

- **16 COBOL project folders** analysed (two folders — `cobol-vibes`, `test-cline-COBOL` — excluded because no agent session is preserved on disk); **16** with on-disk agent traces.
- **28 sessions** — 14 Claude Code + 14 Codex.
- **Coding agents used:** Claude Code (versions: 2.1.109, 2.1.110, 2.1.112, 2.1.173, 2.1.203, 2.1.74, 2.1.79, 2.1.87, 2.1.92) and Codex CLI (versions: 0.108.0-alpha.12, 0.115.0-alpha.11, 0.117.0-alpha.24, 0.118.0-alpha.2, 0.119.0-alpha.11, 0.138.0-alpha.7, 0.142.5, 0.98.0). No preserved JSONL for Cline on this machine.
- **Models observed:** `claude-opus-4-6`×11, `gpt-5.4`×11, `gpt-5.2`×2, `claude-opus-4-7`×1, `claude-sonnet-4-6`×1, `gpt-5.5`×1.
- **Tool calls (sum):** 15,233.
- **User turns (sum):** 534.
- **Aggregate wall-clock duration (sum of per-session spans, includes idle gaps):** 169d 6h 13m.
- **Estimated cost at API rack rates (upper bound, not subscription cost):** ~$7,112.
- **COBOL code across all projects:** 186 files, 58,643 LOC.

- **Activity period:** 2026-02-09 → 2026-07-08.

## 3. Projects at a glance

| Project | Domain | Agent(s) | Sessions | COBOL files / LOC | Tool calls | Dur (Σ wall) | Cost est. (USD) |
|---|---|---|---:|---:|---:|---:|---:|
| `CHESS-COBOL-CLAUDE` | Chess engine in COBOL (GnuCOBOL); engine playability + ELO measurement via cutechess. | Cl×1 | 1 | 1 / 3,460 | 1,156 | 17d 22h 51m | $518 |
| `CHESS-COBOL-CODEX` | Chess engine in COBOL (multi-session); architecture + specification backlog. | Co×2+Cl×1 | 3 | 16 / 3,988 | 1,990 | 29d 22h 9m | $66 |
| `COMPILER-COBOL-CLAUDE` | A COBOL compiler (and interpreter) written in COBOL. Translates COBOL to C; self-hosts non | Cl×3 | 3 | 36 / 18,908 | 3,740 | 11d 14h 20m | $5,185 |
| `COMPILER-COBOL-CODEX` | Alternative COBOL-to-C 'minicobc' compiler, driven by Codex. Benchmarks vs. GnuCOBOL. | Co×4 | 4 | 69 / 13,173 | 5,370 | 4d 21h 53m | $108 |
| `COMPRESS-COBOL-CODEX` | COBPACK — columnar packer / compressor for fixed-record COBOL data, implemented in pure CO | Co×2+Cl×1 | 3 | 2 / 2,021 | 305 | 11d 15h 46m | $29 |
| `COMPRESS-COBOL-CLAUDE` | COBPACK — columnar compressor (Claude-Code-built) — second-agent replica of the COBPACK do | Cl×1 | 1 | 3 / 2,126 | 136 | 1d 10h 48m | $129 |
| `DOOM-COBOL-CLAUDE` | Doom-like FPS in COBOL (Claude Code) — modular walker + ray-casting + enemies + levels. | Cl×1 | 1 | 8 / 1,869 | 152 | 20h 12m | $367 |
| `DOOM-COBOL-CODEX` | Doom-like FPS in COBOL (Codex) — gridwalker + SDL2 bridge + 11 COPY books + BMP sprites. | Co×1 | 1 | 12 / 2,096 | 631 | 20h 14m | $11 |
| `PAYROLL-COBOL-CLAUDE` | — | Cl×1 | 1 | 1 / 598 | 136 | 26d 1h 34m | $13 |
| `PAYROLL-COBOL-CODEX` | — | Co×2 | 2 | 1 / 647 | 199 | 26d 2h 2m | $3 |
| `PYGAME-COBOL-CODEX` | A pygame-style framework in COBOL (GnuCOBOL), exposing a Python-pygame-like interface. | Co×1+Cl×1 | 2 | 3 / 492 | 82 | 1h 35m | $17 |
| `PYGAME-COBOL-CLAUDE` | — | Cl×1 | 1 | 5 / 915 | 153 | 5h 30m | $90 |
| `SAT-COBOL-CODEX` | SAT solver in COBOL (Codex) — modular COPY books + MiniSat/SAT4J cross-checks + uf/uuf ben | Co×1 | 1 | 6 / 1,934 | 508 | 17h 24m | $11 |
| `SAT-COBOL-CLAUDE` | SAT solver in COBOL (Claude Code) — second-agent replica of the SAT domain. | Cl×1 | 1 | 13 / 1,675 | 360 | 1d 22h 41m | $474 |
| `TTTGAME15-COBOL-CLAUDE` | Game-of-15 and tic-tac-toe variants in COBOL with minimax-style tree search (Claude Code). | Cl×2 | 2 | 5 / 1,919 | 142 | 34d 19h 28m | $88 |
| `TTTGAME15-COBOL-CODEX` | Game of 15 in COBOL (Codex) — second-agent replica of the small-game domain. | Co×1 | 1 | 5 / 2,822 | 173 | 3h 37m | $3 |

Legend: `Cl×N` = Claude Code sessions; `Co×N` = Codex sessions.

### Highlights — impressive technical moments across the corpus

Hand-curated reading of the 27 sessions, focused on specific engineering moments (debugging feats, COBOL-specific idioms, verification discipline, performance iteration, architectural choices, cross-agent divergences). Every claim is anchored to a concrete artefact. See [`output/highlights.md`](output/highlights.md).

## Domain coverage — which problem classes have been attempted by which agent?

Projects are grouped by *problem domain*. The **primary agent** per project is the one whose earliest non-analyst session kicked the project off (i.e. authored the PL-ROOT build prompt); later sessions from the other agent (ports, comparisons, analyst re-runs) are listed in parentheses. A domain is **covered by both agents** iff at least one project in the domain has Claude Code as primary AND at least one has Codex as primary.

| Domain | Description | Claude-Code projects (primary) | Codex projects (primary) | Both agents? |
|---|---|---|---|:---:|
| **COBOL compiler (self-hosted)** | A COBOL compiler written in COBOL that compiles non-trivial COBOL programs. | `cobol-compiler-cc` | `cobol-compiler-codex` | ✓ |
| **Chess engine** | UCI-speaking playable chess engine with Elo-measured strength. | `chess-cobol-cc` | `COBOL-chess` _(also: Claude Code)_ | ✓ |
| **Columnar compressor (COBPACK)** | Columnar packer / compressor for fixed-record COBOL data, with codec + trust-suite. | `cobol-compress-cobolcc` | `cobol-compress-codex` _(also: Claude Code)_ | ✓ |
| **Game / graphics framework** | pygame-style SDL2 framework for GnuCOBOL + pure-COBOL Flappy Bird (Claude Code replica, 5-step replay pack). | `cobol-pygame-cc` | `COBOL-pygame` _(also: Claude Code)_ | ✓ |
| **Payroll case-study** | Payroll system, 6-step canonical protocol incl. multi-file merge + behavior-preserving refactoring (Codex). | `cobol-jb-cc` | `cobol-jb-codex` | ✓ |
| **Real-time ray-casting FPS** | Ray-casting 3-D FPS (Doom-like) with real-time rendering. | `cobol-doom-cc` | `cobol-doom-codex` | ✓ |
| **SAT solver** | DIMACS CNF SAT solver with CDCL, cross-checked against MiniSat / SAT4J. | `SATCobol-cc` | `SATCobol-codex` | ✓ |
| **Small game (tic-tac-toe / game-of-15)** | Game-of-15 / tic-tac-toe with minimax tree search. | `cobol-tictactoe` | `game15-cobol-codex` | ✓ |

**Two-agent coverage: 8 / 8 domains.**

Domains already attempted by **both** Claude Code and Codex:

- COBOL compiler (self-hosted)
- Chess engine
- Columnar compressor (COBPACK)
- Game / graphics framework
- Payroll case-study
- Real-time ray-casting FPS
- SAT solver
- Small game (tic-tac-toe / game-of-15)

## Cost metrics — tokens (not dollars)

Dollars are rack-rate estimates and don't compare cleanly between Claude Code and Codex. Tokens are the primitive unit of compute. Below, each token type is summed per project × agent. All the raw data is in [`output/cost_metrics.csv`](output/cost_metrics.csv).

### A. Token profile per project × agent

| Project | Agent | Sessions | Input | Output | Cache read | Cache create | Reasoning | **Total tokens** | Cache hit % | Est. $ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `chess-cobol-cc` | Claude Code | 1 | 1,937 | 591,930 | 166,713,533 | 11,943,652 | 0 | **179,251,052** | 100.0% | $518 |
| `COBOL-chess` | Codex | 2 | 236,150,053 | 1,146,954 | 232,432,640 | 0 | 897,503 | **237,297,007** | 49.6% | $45 |
| `cobol-compiler-cc` | Claude Code | 2 | 7,243 | 1,567,526 | 2,933,801,019 | 35,551,366 | 0 | **2,970,927,154** | 100.0% | $5185 |
| `cobol-compiler-codex` | Codex | 4 | 499,374,995 | 2,350,772 | 479,668,736 | 0 | 1,187,284 | **501,725,767** | 49.0% | $108 |
| `cobol-compress-codex` | Codex | 2 | 17,091,122 | 145,816 | 16,413,312 | 0 | 73,872 | **17,236,938** | 49.0% | $4 |
| `cobol-compress-cobolcc` | Claude Code | 1 | 486 | 550,583 | 37,422,175 | 1,708,980 | 0 | **39,682,224** | 100.0% | $129 |
| `cobol-doom-cc` | Claude Code | 1 | 628 | 1,684,363 | 130,194,776 | 2,425,304 | 0 | **134,305,071** | 100.0% | $367 |
| `cobol-doom-codex` | Codex | 1 | 44,542,491 | 357,679 | 42,641,792 | 0 | 191,316 | **44,900,170** | 48.9% | $11 |
| `cobol-jb-cc` | Claude Code | 1 | 1,171 | 222,078 | 19,457,587 | 1,113,176 | 0 | **20,794,012** | 100.0% | $13 |
| `cobol-jb-codex` | Codex | 2 | 10,701,852 | 94,626 | 10,200,576 | 0 | 49,754 | **10,796,478** | 48.8% | $3 |
| `COBOL-pygame` | Codex | 1 | 1,102,142 | 47,872 | 1,025,920 | 0 | 34,000 | **1,150,014** | 48.2% | $1 |
| `cobol-pygame-cc` | Claude Code | 1 | 345 | 489,521 | 25,086,132 | 837,119 | 0 | **26,413,117** | 100.0% | $90 |
| `SATCobol-codex` | Codex | 1 | 43,570,745 | 290,821 | 41,474,048 | 0 | 146,500 | **43,861,566** | 48.8% | $11 |
| `SATCobol-cc` | Claude Code | 1 | 977 | 984,752 | 168,569,731 | 7,843,062 | 0 | **177,398,522** | 100.0% | $474 |
| `cobol-tictactoe` | Claude Code | 1 | 188 | 318,409 | 7,877,782 | 911,207 | 0 | **9,107,586** | 100.0% | $53 |
| `game15-cobol-codex` | Codex | 1 | 8,899,716 | 113,459 | 8,434,688 | 0 | 68,774 | **9,013,175** | 48.7% | $3 |

### B. Per-project totals (agents summed)

| Project | Sessions | Input | Output | Cache read | Cache create | Reasoning | **Total tokens** | Est. $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cobol-compiler-cc` | 2 | 7,243 | 1,567,526 | 2,933,801,019 | 35,551,366 | 0 | **2,970,927,154** | $5185 |
| `cobol-compiler-codex` | 4 | 499,374,995 | 2,350,772 | 479,668,736 | 0 | 1,187,284 | **501,725,767** | $108 |
| `COBOL-chess` | 2 | 236,150,053 | 1,146,954 | 232,432,640 | 0 | 897,503 | **237,297,007** | $45 |
| `chess-cobol-cc` | 1 | 1,937 | 591,930 | 166,713,533 | 11,943,652 | 0 | **179,251,052** | $518 |
| `SATCobol-cc` | 1 | 977 | 984,752 | 168,569,731 | 7,843,062 | 0 | **177,398,522** | $474 |
| `cobol-doom-cc` | 1 | 628 | 1,684,363 | 130,194,776 | 2,425,304 | 0 | **134,305,071** | $367 |
| `cobol-doom-codex` | 1 | 44,542,491 | 357,679 | 42,641,792 | 0 | 191,316 | **44,900,170** | $11 |
| `SATCobol-codex` | 1 | 43,570,745 | 290,821 | 41,474,048 | 0 | 146,500 | **43,861,566** | $11 |
| `cobol-compress-cobolcc` | 1 | 486 | 550,583 | 37,422,175 | 1,708,980 | 0 | **39,682,224** | $129 |
| `cobol-pygame-cc` | 1 | 345 | 489,521 | 25,086,132 | 837,119 | 0 | **26,413,117** | $90 |
| `cobol-jb-cc` | 1 | 1,171 | 222,078 | 19,457,587 | 1,113,176 | 0 | **20,794,012** | $13 |
| `cobol-compress-codex` | 2 | 17,091,122 | 145,816 | 16,413,312 | 0 | 73,872 | **17,236,938** | $4 |
| `cobol-jb-codex` | 2 | 10,701,852 | 94,626 | 10,200,576 | 0 | 49,754 | **10,796,478** | $3 |
| `cobol-tictactoe` | 1 | 188 | 318,409 | 7,877,782 | 911,207 | 0 | **9,107,586** | $53 |
| `game15-cobol-codex` | 1 | 8,899,716 | 113,459 | 8,434,688 | 0 | 68,774 | **9,013,175** | $3 |
| `COBOL-pygame` | 1 | 1,102,142 | 47,872 | 1,025,920 | 0 | 34,000 | **1,150,014** | $1 |
| **GRAND TOTAL** | — | **861,446,091** | **10,957,161** | **4,321,414,447** | **62,333,866** | **2,649,003** | **4,423,859,853** | **$7016** |

### C. Normalized ratios (compute per unit of deliverable)

Output tokens are the cleanest comparison axis (everything the agent actually generated). Ratios below divide output tokens by:

- `COBOL LOC` — what ended up in the delivered `.cob`/`.cbl`/`.cpy` files,
- `F-### backlog entry` — deliverable units of work,
- `user prompt` — unit of user direction.

| Project | Output tokens | COBOL LOC | Output / LOC | Backlog | Output / BL | User prompts | Output / prompt |
|---|---:|---:|---:|---:|---:|---:|---:|
| `cobol-compiler-cc` | 1,567,526 | 15,912 | 99 | 32 | 48,985 | 100 | 15,675 |
| `cobol-compiler-codex` | 2,350,772 | 11,680 | 201 | 61 | 38,537 | 96 | 24,487 |
| `COBOL-chess` | 1,146,954 | 3,359 | 341 | 184 | 6,233 | 25 | 45,878 |
| `chess-cobol-cc` | 591,930 | 2,920 | 203 | 51 | 11,606 | 47 | 12,594 |
| `SATCobol-cc` | 984,752 | 1,347 | 731 | 87 | 11,319 | 31 | 31,766 |
| `cobol-doom-cc` | 1,684,363 | 1,616 | 1,042 | 13 | 129,566 | 20 | 84,218 |
| `cobol-doom-codex` | 357,679 | 1,906 | 188 | 0 | — | 31 | 11,538 |
| `SATCobol-codex` | 290,821 | 1,706 | 170 | 63 | 4,616 | 29 | 10,028 |
| `cobol-compress-cobolcc` | 550,583 | 1,819 | 303 | 11 | 50,053 | 7 | 78,655 |
| `cobol-pygame-cc` | 489,521 | 764 | 641 | 0 | — | 17 | 28,795 |
| `cobol-jb-cc` | 222,078 | 535 | 415 | 0 | — | 29 | 7,658 |
| `cobol-compress-codex` | 145,816 | 1,812 | 80 | 18 | 8,101 | 9 | 16,202 |
| `cobol-jb-codex` | 94,626 | 572 | 165 | 0 | — | 19 | 4,980 |
| `cobol-tictactoe` | 318,409 | 1,537 | 207 | 31 | 10,271 | 14 | 22,744 |
| `game15-cobol-codex` | 113,459 | 2,264 | 50 | 35 | 3,242 | 11 | 10,314 |
| `COBOL-pygame` | 47,872 | 398 | 120 | 11 | 4,352 | 3 | 15,957 |

### D. Caveats on token semantics

- **`input_tokens`** here is the *non-cached* input (new prompt tokens processed). Claude Code reports this directly; Codex reports `cached_input_tokens` separately and we subtract it from the raw total.
- **`output_tokens`** includes `thinking` blocks for Claude Code (they are charged at output rate). Codex reports `reasoning_output_tokens` in a separate bucket; we keep them in `reasoning_tokens` to make the hidden-CoT load visible.
- **`cache_read_tokens`** are billed at ~10 % of input rate on both platforms — a high cache-hit rate is a strong efficiency indicator for long-running sessions (Codex sessions on this machine often show 50–80 %).
- **`cache_creation_tokens`** (Claude-specific) are billed at ~125 % of input rate; they pay once and amortise across subsequent turns.
- **`reasoning_tokens`** (Codex-only) are billed at output rate but are invisible in the transcript. Projects with heavy reasoning_tokens are doing more hidden deliberation per user turn.
- **`cost_usd`** is a rack-rate upper bound; actual billing under Team / Max / Pro subscriptions differs. Use tokens for comparison.
- For reproducibility, every number here is recomputable from `output/sessions_all.json` with `scripts/cost_metrics.py`.

## Context-length trajectory + compaction

Per-turn context size = `input_tokens + cache_read + cache_create` for Claude Code, and `input_tokens` (which already includes cached) for Codex. This is the amount of tokens the model actually ingests to produce one response — i.e. how much of the context window is being used right now.

**Compaction** is detected from explicit agent events: Claude Code flags a user message with `isCompactSummary: true` when it replaces the prior history with a condensed summary; Codex emits `event_msg.type == "context_compacted"` (and occasionally `thread_rolled_back`). A compaction is a reliable indicator that the session was running close to — or over — the model's context window.

### A. Per-project roll-up

| Project | Sessions | Peak context | Model | Peak window | Peak util. % | Compactions | Sessions ≥ 90 % of window |
|---|---:|---:|---|---:|---:|---:|---:|
| `cobol-compiler-cc` | 3 | 978,117 | `claude-opus-4-6` | 1,000,000 | 97.8% | 3 | 1 |
| `cobol-doom-cc` | 1 | 634,006 | `claude-opus-4-7` | 200,000 | 317.0% | 0 | 1 |
| `SATCobol-cc` | 1 | 544,028 | `claude-opus-4-6` | 1,000,000 | 54.4% | 0 | 0 |
| `cobol-compress-cobolcc` | 1 | 264,411 | `claude-opus-4-6` | 1,000,000 | 26.4% | 0 | 0 |
| `cobol-compiler-codex` | 4 | 244,646 | `gpt-5.4` | 258,400 | 94.7% | 30 | 1 |
| `COBOL-chess` | 3 | 240,665 | `gpt-5.2` | 258,400 | 93.1% | 8 | 1 |
| `SATCobol-codex` | 1 | 203,859 | `gpt-5.4` | 258,400 | 78.9% | 2 | 0 |
| `cobol-compress-codex` | 3 | 202,194 | `gpt-5.4` | 258,400 | 78.2% | 2 | 0 |
| `cobol-doom-codex` | 1 | 198,411 | `gpt-5.4` | 258,400 | 76.8% | 4 | 0 |
| `game15-cobol-codex` | 1 | 187,942 | `gpt-5.4` | 258,400 | 72.7% | 1 | 0 |
| `chess-cobol-cc` | 1 | 167,327 | `claude-opus-4-6` | 1,000,000 | 16.7% | 5 | 0 |
| `cobol-tictactoe` | 2 | 140,410 | `claude-opus-4-6` | 1,000,000 | 14.0% | 2 | 0 |
| `COBOL-pygame` | 2 | 110,711 | `claude-opus-4-6` | 1,000,000 | 17.2% | 0 | 0 |
| `cobol-jb` | 2 | 72,808 | `claude-opus-4-6` | 1,000,000 | 7.3% | 0 | 0 |

### B. Per-session detail

Columns: turn count (assistant turns with usage info), context-window size, peak context reached (and % of window it is), median / p90 / p99 of the context-length distribution, first-turn & last-turn context (to see the growth pattern), and count of compaction events in that session.

| Project | Agent | Model | Turns | Window | Peak | % | p50 | p90 | p99 | First | Last | Compactions |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `COBOL-chess` | Claude Code | `claude-opus-4-6` | 84 | 1,000,000 | 128,073 | 13% | 51,457 | 119,076 | 127,827 | 19,513 | 128,073 | 0 |
| `COBOL-chess` | Codex | `gpt-5.2` | 3696 | 258,400 | 240,665 | 93% | 131,403 | 197,120 | 235,137 | 15,747 | 105,198 | **8** |
| `COBOL-chess` | Codex | `gpt-5.4` | 30 | 258,400 | 126,455 | 49% | 100,900 | 113,838 | 124,964 | 11,234 | 126,455 | 0 |
| `COBOL-pygame` | Claude Code | `claude-opus-4-6` | 73 | 1,000,000 | 110,711 | 11% | 65,351 | 109,278 | 110,549 | 20,031 | 110,711 | 0 |
| `COBOL-pygame` | Codex | `gpt-5.2` | 67 | 258,400 | 44,546 | 17% | 34,862 | 40,632 | 44,546 | 14,380 | 40,710 | 0 |
| `SATCobol-cc` | Claude Code | `claude-opus-4-6` | 645 | 1,000,000 | 544,028 | 54% | 285,131 | 455,300 | 517,176 | 23,649 | 426,705 | 0 |
| `SATCobol-codex` | Codex | `gpt-5.4` | 439 | 258,400 | 203,859 | 79% | 107,556 | 167,325 | 200,788 | 14,764 | 150,751 | **2** |
| `chess-cobol-cc` | Claude Code | `claude-opus-4-6` | 1811 | 1,000,000 | 167,327 | 17% | 101,374 | 153,822 | 165,367 | 15,115 | 165,989 | **5** |
| `cobol-compiler-cc` | Claude Code | `?` | 0 | 0 | 0 | — | 0 | 0 | 0 | 0 | 0 | 0 |
| `cobol-compiler-cc` | Claude Code | `claude-opus-4-6` | 6364 | 1,000,000 | 978,117 | 98% | 442,105 | 872,672 | 967,071 | 15,555 | 232,011 | **3** |
| `cobol-compiler-cc` | Claude Code | `claude-opus-4-6` | 17 | 1,000,000 | 21,695 | 2% | 20,592 | 21,218 | 21,218 | 16,166 | 21,695 | 0 |
| `cobol-compiler-codex` | Codex | `gpt-5.4` | 3451 | 258,400 | 244,646 | 95% | 147,579 | 206,581 | 238,036 | 14,270 | 201,722 | **30** |
| `cobol-compiler-codex` | Codex | `gpt-5.4` | 75 | 258,400 | 208,546 | 81% | 138,594 | 199,726 | 207,648 | 14,320 | 208,546 | 0 |
| `cobol-compiler-codex` | Codex | `gpt-5.4` | 26 | 258,400 | 120,009 | 46% | 72,569 | 102,480 | 114,131 | 14,332 | 120,009 | 0 |
| `cobol-compiler-codex` | Codex | `gpt-5.4` | 61 | 258,400 | 121,999 | 47% | 99,877 | 117,865 | 121,462 | 14,301 | 121,999 | 0 |
| `cobol-compress-cobolcc` | Claude Code | `claude-opus-4-6` | 230 | 1,000,000 | 264,411 | 26% | 174,390 | 249,901 | 262,047 | 26,570 | 264,411 | 0 |
| `cobol-compress-codex` | Claude Code | `claude-opus-4-6` | 53 | 1,000,000 | 132,079 | 13% | 62,285 | 109,672 | 125,469 | 20,035 | 132,079 | 0 |
| `cobol-compress-codex` | Codex | `gpt-5.4` | 191 | 258,400 | 202,194 | 78% | 85,071 | 146,340 | 156,435 | 13,538 | 31,478 | **2** |
| `cobol-compress-codex` | Codex | `gpt-5.4` | 11 | 258,400 | 70,714 | 27% | 29,167 | 69,882 | 69,882 | 14,708 | 70,714 | 0 |
| `cobol-doom-cc` | Claude Code | `claude-opus-4-7` | 333 | 200,000 | 634,006 | 317% | 463,538 | 618,017 | 632,128 | 23,752 | 634,006 | 0 |
| `cobol-doom-codex` | Codex | `gpt-5.4` | 507 | 258,400 | 198,411 | 77% | 83,575 | 155,627 | 193,044 | 14,855 | 99,442 | **4** |
| `cobol-jb` | Claude Code | `claude-opus-4-6` | 44 | 1,000,000 | 39,042 | 4% | 33,419 | 36,501 | 38,892 | 16,721 | 39,042 | 0 |
| `cobol-jb` | Claude Code | `claude-opus-4-6` | 126 | 1,000,000 | 72,808 | 7% | 47,748 | 70,425 | 72,636 | 16,379 | 72,808 | 0 |
| `cobol-tictactoe` | Claude Code | `claude-opus-4-6` | 109 | 1,000,000 | 123,259 | 12% | 59,097 | 100,619 | 122,676 | 18,440 | 43,325 | **1** |
| `cobol-tictactoe` | Claude Code | `claude-opus-4-6` | 124 | 1,000,000 | 140,410 | 14% | 62,314 | 118,011 | 139,305 | 15,119 | 48,651 | **1** |
| `game15-cobol-codex` | Codex | `gpt-5.4` | 115 | 258,400 | 187,942 | 73% | 85,588 | 160,850 | 166,423 | 14,792 | 39,417 | **1** |

### C. How to read this

- **Sessions with compactions > 0** are sessions where the agent hit a soft ceiling and had to fold prior history into a summary — expect loss of fine-grained trace fidelity downstream of that point.
- **Peak / window ≥ 80 %** means the session ran close to the model's limit. Even without a compaction event, the agent's cache effectiveness drops here (more churn on cache_read tokens).
- For Claude Code, the 1 M-context Opus variant (`claude-opus-4-6 [1M]`) raises the ceiling 5× over the 200 k baseline — this is why the compiler / chess sessions can run for 15+ active hours without mandatory compaction.
- Codex's 258 400-token context window on `gpt-5.*` is smaller than Claude's Opus 1 M — you will see Codex hit compaction sooner on projects of comparable feature depth.
- Raw per-session per-turn series are saved to [`output/context/*.json`](output/context), suitable for sparkline / ribbon-plot rendering; the summary CSV is at [`output/context_summary.csv`](output/context_summary.csv).

## Feature classification — significance profile per project

Every project's top 8–12 features are classified by a 9-class taxonomy (see [`prompts/significance-taxonomy.md`](prompts/significance-taxonomy.md) for definitions) in [`output/backlogs/<project>/KEY_FEATURES.md`](output/backlogs/). The table below shows the count of top-features that fall in each class, per project. **Dominant** = the two or three classes with the highest counts — where the project actually spends its engineering weight.

Classes: `ALG` algorithm · `DOM` domain modelling · `SYS` system integration / FFI · `INF` infrastructure · `PRO` protocol compliance · `LNG` language-level achievement · `VER` verification · `PRF` performance engineering · `CMP` emergent composition.

| Project | Top | ALG | DOM | SYS | INF | PRO | LNG | VER | PRF | CMP | Dominant |
|---|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `chess-cobol-cc` | 12 | 2 | **3** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **DOM + ALG + SYS** |
| `cobol-compiler-cc` | 12 | — | **3** | 2 | — | — | **3** | 1 | — | **3** | **DOM + LNG + CMP** |
| `cobol-compiler-codex` | 12 | 2 | — | 2 | — | — | 1 | **3** | 1 | **3** | **VER + CMP + ALG** |
| `cobol-compress-codex` | 12 | 2 | 3 | — | — | — | 1 | **4** | 1 | 1 | **VER + DOM + ALG** |
| `SATCobol-codex` | 11 | 2 | 2 | — | 1 | — | 1 | **3** | 1 | 1 | **VER + ALG + DOM** |
| `SATCobol-cc` | 11 | **3** | 2 | — | 1 | — | 1 | **3** | — | 1 | **ALG + VER + DOM** |
| `cobol-tictactoe` | 11 | 1 | **6** | — | — | — | 2 | — | — | 2 | **DOM + LNG + CMP** |
| `game15-cobol-codex` | 11 | 1 | **7** | — | — | — | 2 | — | — | 1 | **DOM + LNG + ALG** |
| `cobol-doom-codex` | 10 | 1 | 2 | 1 | 1 | — | **4** | 1 | — | — | **LNG + DOM + ALG** |
| `COBOL-chess` | 9 | 2 | **3** | — | 1 | 1 | 1 | 1 | — | — | **DOM + ALG + INF** |
| `cobol-doom-cc` | 9 | — | **5** | — | 1 | — | 2 | 1 | — | — | **DOM + LNG + INF** |
| `cobol-compress-cobolcc` | 8 | — | 2 | — | — | — | 1 | **4** | 1 | — | **VER + DOM + LNG** |
| `COBOL-pygame` | 8 | — | — | **3** | 1 | — | 2 | — | — | 2 | **SYS + LNG + CMP** |

### Class → projects where it is dominant

| Class | Description | Projects where this class leads |
|---|---|---|
| `ALG` | Algorithm | `SATCobol-cc` |
| `DOM` | Domain modelling | `chess-cobol-cc`, `COBOL-chess`, `cobol-compiler-cc`, `cobol-doom-cc`, `cobol-tictactoe`, `game15-cobol-codex` |
| `SYS` | System integration / FFI | `COBOL-pygame` |
| `INF` | Infrastructure / tooling | — |
| `PRO` | Protocol compliance | — |
| `LNG` | Language-level achievement | `cobol-doom-codex` |
| `VER` | Correctness verification | `cobol-compiler-codex`, `cobol-compress-codex`, `cobol-compress-cobolcc`, `SATCobol-codex` |
| `PRF` | Performance engineering | — |
| `CMP` | Emergent composition | — |

### Cross-project totals

| Class | Total top-feature count across projects | Share |
|---|---:|---:|
| `ALG` Algorithm | 16 | 11.8% |
| `DOM` Domain modelling | 38 | 27.9% |
| `SYS` System integration / FFI | 9 | 6.6% |
| `INF` Infrastructure / tooling | 7 | 5.1% |
| `PRO` Protocol compliance | 2 | 1.5% |
| `LNG` Language-level achievement | 22 | 16.2% |
| `VER` Correctness verification | 22 | 16.2% |
| `PRF` Performance engineering | 5 | 3.7% |
| `CMP` Emergent composition | 15 | 11.0% |
| **Total top-features ranked** | **136** | 100.0% |

### Verdicts at a glance

| Project | Verdict (auto-extracted from `KEY_FEATURES.md`) |
|---|---|
| `COBOL-chess` | **Hybrid: algorithm-centric with serious domain-modelling and verification backbone, plus a LNG accent from COBOL-specific recursion tricks** — a thorough, by-the-book chess engine where the sophistication lives in composing a 1 000-line search module on top o… |
| `COBOL-pygame` | **System-integration-centric, with a language-achievement backbone** — the project's substance is the COBOL↔C↔SDL2 boundary (ABI, handles, struct mirrors, dialect-specific linker semantics), not algorithms; the two composition features (hello, Flappy) are valu… |
| `SATCobol-cc` | **Verification-centric hybrid — ALG + VER with a genuine LNG supporting act, CDCL left unfinished.** This is neither "just-an-algorithm" nor "just-domain-modelling": baseline DPLL is textbook, but the iterative-trail port is non-trivial COBOL engineering; the … |
| `SATCobol-codex` | **Balanced hybrid — ALG + PRF + VER, with a genuine LNG supporting act.** This is neither "just-an-algorithm" nor "just-domain-modelling": the CDCL core is textbook, but re-hosting it on COBOL's fixed-capacity arrays is depth-3 engineering; the three-round per… |
| `chess-cobol-cc` | **Hybrid, centre-of-gravity LNG + PRF + SYS, not "just minimax":** the top three ranks are a language-level achievement (explicit-stack search in COBOL), a performance-engineering loop (14 measured INCR→TEST→RETR cycles with 7 reverts), and an emergent composi… |
| `cobol-compiler-cc` | **Language-achievement-centric hybrid (LNG + DOM + CMP)** — a self-hosted COBOL subset compiler whose significance is not the parsing algorithm but the composition chain that lets a compiler written in COBOL, compiled by GnuCOBOL, compile a COBOL DOOM port and… |
| `cobol-compiler-codex` | **Hybrid: ALG/LNG foundation + VER/PRF superstructure with heavy CMP** — a COBOL-in-COBOL subset compiler (ALG+LNG) whose distinguishing contribution is a benchmark-driven comparison apparatus against GnuCOBOL and a self-correcting verification loop (VER+PRF+C… |
| `cobol-compress-cobolcc` | **Verification-centric hybrid with a language-achievement accent** — shares the Codex sibling's VER-dominated profile (VER=4/10) but adds a language-level dimension (LNG in 3 features) through the 3-file modular decomposition and the COBOL CRC32 subprogram. |
| `cobol-compress-codex` | **Verification-centric hybrid with a strong domain-modelling core** — the project is the most verification-hygienic of the COBOL set (VER = 4/12, plus a CMP test-infrastructure layer and a PRF fix cycle that is itself test-driven), built on a respectable DOM s… |
| `cobol-doom-cc` | **Language-achievement-centric with DOM superstructure.** Entire rendering pipeline runs in COBOL paragraphs with zero C code. |
| `cobol-doom-codex` | **Hybrid — LNG-centric with SYS seam.** DDA raycaster in COBOL (not C) is the strongest "COBOL does the computation" claim. |
| `cobol-tictactoe` | Hybrid **domain-modelling + language-achievement** project with strong emergent composition: the algorithm content is textbook (one minimax, one DFS), but the magic-square/D4 encoding, the COBOL-recursion-via-explicit-stack, and the counter -> tree -> avoid ->… |
| `game15-cobol-codex` | Hybrid **domain-modelling + language-achievement** project with strong emergent composition — same verdict as the Claude-Code sibling, but with Codex leaning a step further into **eager, table-driven domain encodings** (the 986,409-byte factorial-rank bitmap a… |

_Numbers above are parsed from the `## Significance profile` tables inside each `KEY_FEATURES.md`. Column semantics (primary vs primary+secondary) varies slightly across projects — the parser always takes the **first integer** of each row, which corresponds to the primary-class count. For the nuance, see the individual per-project files._

### Per-project artefacts

Each row: narrative story, case study (RQ-labeled metrics), calibrated assessment (context + strengths + honest gaps), feature ledger (F-### / SB-### entries), key-features ranking, and reusable replay prompts for reproducing the project with a different agent.

| Project | Story | Case study | Assessment | Backlog | Key features | Replay prompts |
|---|---|---|---|---|---|---|
| `CHESS-COBOL-CLAUDE` | [story](output/backlogs/chess-cobol-cc/STORY.md) | [report](output/reports/chess-cobol-cc.md) | [assessment](output/assessments/chess-cobol-cc.md) | [backlog](output/backlogs/chess-cobol-cc/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/chess-cobol-cc/KEY_FEATURES.md) | — |
| `CHESS-COBOL-CODEX` | [story](output/backlogs/COBOL-chess/STORY.md) | [report](output/reports/COBOL-chess.md) | [assessment](output/assessments/COBOL-chess.md) | [backlog](output/backlogs/COBOL-chess/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/COBOL-chess/KEY_FEATURES.md) | [replay](output/backlogs/COBOL-chess/REPLAY_PROMPTS.md) |
| `COMPILER-COBOL-CLAUDE` | [story](output/backlogs/cobol-compiler-cc/STORY.md) | [report](output/reports/cobol-compiler-cc.md) | [assessment](output/assessments/cobol-compiler-cc.md) | [backlog](output/backlogs/cobol-compiler-cc/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/cobol-compiler-cc/KEY_FEATURES.md) | — |
| `COMPILER-COBOL-CODEX` | [story](output/backlogs/cobol-compiler-codex/STORY.md) | [report](output/reports/cobol-compiler-codex.md) | [assessment](output/assessments/cobol-compiler-codex.md) | [backlog](output/backlogs/cobol-compiler-codex/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/cobol-compiler-codex/KEY_FEATURES.md) | [replay](output/backlogs/cobol-compiler-codex/REPLAY_PROMPTS.md) |
| `COMPRESS-COBOL-CODEX` | [story](output/backlogs/cobol-compress-codex/STORY.md) | [report](output/reports/cobol-compress-codex.md) | [assessment](output/assessments/cobol-compress-codex.md) | [backlog](output/backlogs/cobol-compress-codex/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/cobol-compress-codex/KEY_FEATURES.md) | [replay](output/backlogs/cobol-compress-codex/REPLAY_PROMPTS.md) |
| `COMPRESS-COBOL-CLAUDE` | [story](output/backlogs/cobol-compress-cobolcc/STORY.md) | [report](output/reports/cobol-compress-cobolcc.md) | [assessment](output/assessments/cobol-compress-cobolcc.md) | [backlog](output/backlogs/cobol-compress-cobolcc/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/cobol-compress-cobolcc/KEY_FEATURES.md) | — |
| `DOOM-COBOL-CLAUDE` | [story](output/backlogs/cobol-doom-cc/STORY.md) | [report](output/reports/cobol-doom-cc.md) | [assessment](output/assessments/cobol-doom-cc.md) | [backlog](output/backlogs/cobol-doom-cc/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/cobol-doom-cc/KEY_FEATURES.md) | — |
| `DOOM-COBOL-CODEX` | [story](output/backlogs/cobol-doom-codex/STORY.md) | [report](output/reports/cobol-doom-codex.md) | [assessment](output/assessments/cobol-doom-codex.md) | [backlog](output/backlogs/cobol-doom-codex/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/cobol-doom-codex/KEY_FEATURES.md) | — |
| `PAYROLL-COBOL-CLAUDE` | — | [report](output/reports/cobol-jb-cc.md) | [assessment](output/assessments/cobol-jb-cc.md) | [backlog](output/backlogs/cobol-jb-cc/KEY_FEATURES.md) | [key](output/backlogs/cobol-jb-cc/KEY_FEATURES.md) | — |
| `PAYROLL-COBOL-CODEX` | — | [report](output/reports/cobol-jb-codex.md) | [assessment](output/assessments/cobol-jb-codex.md) | [backlog](output/backlogs/cobol-jb-codex/KEY_FEATURES.md) | [key](output/backlogs/cobol-jb-codex/KEY_FEATURES.md) | — |
| `PYGAME-COBOL-CODEX` | [story](output/backlogs/COBOL-pygame/STORY.md) | [report](output/reports/COBOL-pygame.md) | [assessment](output/assessments/COBOL-pygame.md) | [backlog](output/backlogs/COBOL-pygame/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/COBOL-pygame/KEY_FEATURES.md) | [replay](output/backlogs/COBOL-pygame/REPLAY_PROMPTS.md) |
| `PYGAME-COBOL-CLAUDE` | — | [report](output/reports/cobol-pygame-cc.md) | [assessment](output/assessments/cobol-pygame-cc.md) | [backlog](output/backlogs/cobol-pygame-cc/KEY_FEATURES.md) | [key](output/backlogs/cobol-pygame-cc/KEY_FEATURES.md) | — |
| `SAT-COBOL-CODEX` | [story](output/backlogs/SATCobol-codex/STORY.md) | [report](output/reports/SATCobol-codex.md) | [assessment](output/assessments/SATCobol-codex.md) | [backlog](output/backlogs/SATCobol-codex/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/SATCobol-codex/KEY_FEATURES.md) | [replay](output/backlogs/SATCobol-codex/REPLAY_PROMPTS.md) |
| `SAT-COBOL-CLAUDE` | [story](output/backlogs/SATCobol-cc/STORY.md) | [report](output/reports/SATCobol-cc.md) | [assessment](output/assessments/SATCobol-cc.md) | [backlog](output/backlogs/SATCobol-cc/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/SATCobol-cc/KEY_FEATURES.md) | — |
| `TTTGAME15-COBOL-CLAUDE` | [story](output/backlogs/cobol-tictactoe/STORY.md) | [report](output/reports/cobol-tictactoe.md) | [assessment](output/assessments/cobol-tictactoe.md) | [backlog](output/backlogs/cobol-tictactoe/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/cobol-tictactoe/KEY_FEATURES.md) | [replay](output/backlogs/cobol-tictactoe/REPLAY_PROMPTS.md) |
| `TTTGAME15-COBOL-CODEX` | [story](output/backlogs/game15-cobol-codex/STORY.md) | [report](output/reports/game15-cobol-codex.md) | [assessment](output/assessments/game15-cobol-codex.md) | [backlog](output/backlogs/game15-cobol-codex/SPECIFICATION_BACKLOG.md) | [key](output/backlogs/game15-cobol-codex/KEY_FEATURES.md) | — |

### Cross-project quantitative view (from deep analysis)

| Project | Difficulty | Turns | Active time | bug_fix share | Error rate | User prompts | Avg prompt len |
|---|---|---:|---:|---:|---:|---:|---:|
| `COMPILER-COBOL-CLAUDE` | Very-High (0.83) | 10,225 | 1d 8h 30m | 3.2% | 8.7% | 98 | 512 |
| `COMPILER-COBOL-CODEX` | Very-High (0.81) | 15,631 | 10h 58m | 3.9% | 20.0% | 97 | 83 |
| `CHESS-COBOL-CODEX` | High (0.73) | 5,640 | 4h 58m | 2.4% | 3.4% | 26 | 1554 |
| `PAYROLL-COBOL-CODEX` | High (0.71) | 638 | 30m 41s | 11.9% | 16.1% | 19 | 698 |
| `PAYROLL-COBOL-CLAUDE` | High (0.63) | 415 | 1h 57m | 7.0% | 5.1% | 21 | 1153 |
| `CHESS-COBOL-CLAUDE` | High (0.61) | 3,023 | 15h 31m | 0.3% | 2.8% | 47 | 1793 |
| `PYGAME-COBOL-CLAUDE` | High (0.56) | 434 | 2h 6m | 7.8% | 3.3% | 17 | 2086 |
| `COMPRESS-COBOL-CODEX` | High (0.54) | 802 | 54m 56s | 0.4% | 14.4% | 10 | 1054 |
| `SAT-COBOL-CODEX` | High (0.50) | 1,676 | 1h 50m | 4.6% | 11.0% | 29 | 124 |
| `DOOM-COBOL-CODEX` | Medium (0.46) | 1,920 | 2h 1m | 0.2% | 3.3% | 32 | 283 |
| `DOOM-COBOL-CLAUDE` | Medium (0.40) | 506 | 3h 14m | 0.7% | 0.7% | 20 | 479 |
| `PYGAME-COBOL-CODEX` | Medium (0.37) | 97 | 4m 16s | 5.1% | 9.7% | 3 | 115 |
| `TTTGAME15-COBOL-CLAUDE` | Medium (0.29) | 206 | 2h 4m | 0.0% | 1.5% | 12 | 953 |
| `TTTGAME15-COBOL-CODEX` | Medium (0.26) | 533 | 33m 4s | 0.1% | 3.5% | 11 | 396 |
| `SAT-COBOL-CLAUDE` | Low (0.22) | 316 | 1h 14m | 0.1% | 1.7% | 8 | 170 |
| `COMPRESS-COBOL-CLAUDE` | Low (0.08) | 4 | 1m 2s | 0.0% | 0.0% | 1 | 7285 |

### COBOL language mastery (what programs exercise the language surface)

Mastery score = number of distinct COBOL constructs observed in the project's `.cob`/`.cbl`/`.cpy` files. Categories = how many of the 10 capability categories the project touches (control flow, arithmetic, data-advanced, I/O, string-ops, tables/search, subprograms, copy/preproc, intrinsics, misc).

| Project | Mastery | Categories | Paragraphs (≈functions) | Sections | LOC (code) | Notable constructs |
|---|---:|---:|---:|---:|---:|---|
| `COMPILER-COBOL-CLAUDE` | 57 | 10/10 | 266 | 40 | 15,912 | `CALL`(55), `RECURSIVE`(23), `OCCURS`(161), `REDEFINES`(21), `USAGE_COMP_5`(2), `COPY`(45) |
| `COMPILER-COBOL-CODEX` | 60 | 10/10 | 246 | 70 | 11,680 | `CALL`(277), `RECURSIVE`(14), `OCCURS`(217), `REDEFINES`(60), `USAGE_COMP_5`(149), `COPY`(44) |
| `CHESS-COBOL-CODEX` | 40 | 10/10 | 70 | 30 | 3,359 | `CALL`(77), `RECURSIVE`(3), `OCCURS`(25), `USAGE_COMP_5`(489), `COPY`(34), `UNSTRING`(4) |
| `PAYROLL-COBOL-CODEX` | 34 | 7/10 | 14 | 3 | 572 | `OCCURS`(1), `FD`(5) |
| `PAYROLL-COBOL-CLAUDE` | 30 | 5/10 | 23 | 4 | 535 | `OCCURS`(1), `REDEFINES`(1), `FD`(5) |
| `CHESS-COBOL-CLAUDE` | 38 | 10/10 | 81 | 2 | 2,920 | `RECURSIVE`(1), `OCCURS`(23), `REDEFINES`(9), `COPY`(3), `FUNCTION`(29) |
| `PYGAME-COBOL-CLAUDE` | 28 | 10/10 | 48 | 4 | 764 | `CALL`(94), `OCCURS`(1), `COPY`(4), `FUNCTION`(2) |
| `COMPRESS-COBOL-CODEX` | 44 | 9/10 | 77 | 7 | 1,812 | `CALL`(1), `OCCURS`(3), `USAGE_COMP_5`(39), `FD`(3), `UNSTRING`(2), `FUNCTION`(13) |
| `SAT-COBOL-CODEX` | 42 | 9/10 | 70 | 3 | 1,706 | `OCCURS`(22), `USAGE_COMP_5`(81), `COPY`(5), `FD`(2), `FUNCTION`(67) |
| `DOOM-COBOL-CODEX` | 28 | 10/10 | 169 | 10 | 1,906 | `CALL`(42), `OCCURS`(28), `USAGE_COMP_5`(220), `COPY`(11), `FUNCTION`(40) |
| `DOOM-COBOL-CLAUDE` | 34 | 9/10 | 71 | 1 | 1,616 | `CALL`(15), `OCCURS`(7), `REDEFINES`(1), `USAGE_COMP_5`(12), `COPY`(7), `FUNCTION`(43) |
| `PYGAME-COBOL-CODEX` | 31 | 10/10 | 11 | 2 | 398 | `CALL`(39), `OCCURS`(1), `USAGE_COMP_5`(55), `COPY`(2), `FUNCTION`(4) |
| `TTTGAME15-COBOL-CLAUDE` | 28 | 8/10 | 34 | 5 | 1,537 | `OCCURS`(38), `REDEFINES`(6), `UNSTRING`(6), `FUNCTION`(20) |
| `TTTGAME15-COBOL-CODEX` | 35 | 9/10 | 88 | 5 | 2,264 | `OCCURS`(69), `UNSTRING`(3), `FUNCTION`(34) |
| `SAT-COBOL-CLAUDE` | 41 | 9/10 | 94 | 3 | 1,347 | `OCCURS`(19), `USAGE_COMP_5`(67), `COPY`(12), `FD`(2), `FUNCTION`(23) |
| `COMPRESS-COBOL-CLAUDE` | 50 | 10/10 | 74 | 10 | 1,819 | `CALL`(46), `OCCURS`(3), `REDEFINES`(11), `USAGE_COMP_5`(105), `COPY`(13), `FD`(1) |

### Feature inventory (what was actually built)

A prompt often expands into many sub-features. The ledger tallies features from four sources; the `F-###` backlog is the authoritative one when present. `prompt subtasks` = bullet / numbered items found inside user messages. `commits` = git commit subjects. Total = deduplicated union (rough lower bound; see per-project reports for the full ledger).

| Project | F-### backlog | README features | Prompt subtasks | Git commits | Total (dedup proxy) |
|---|---:|---:|---:|---:|---:|
| `COMPILER-COBOL-CLAUDE` | **32** | 0 | 80 | 74 | 112 |
| `COMPILER-COBOL-CODEX` | **61** | 0 | 0 | 13 | 61 |
| `CHESS-COBOL-CODEX` | **184** | 8 | 92 | 2 | 284 |
| `PAYROLL-COBOL-CODEX` | **0** | 0 | 128 | 6 | 128 |
| `PAYROLL-COBOL-CLAUDE` | **0** | 0 | 143 | 6 | 143 |
| `CHESS-COBOL-CLAUDE` | **51** | 0 | 99 | 1 | 115 |
| `PYGAME-COBOL-CLAUDE` | **0** | 0 | 41 | 2 | 41 |
| `COMPRESS-COBOL-CODEX` | **18** | 0 | 168 | 1 | 186 |
| `SAT-COBOL-CODEX` | **63** | 0 | 0 | 10 | 44 |
| `DOOM-COBOL-CODEX` | **0** | 0 | 0 | 10 | 0 |
| `DOOM-COBOL-CLAUDE` | **13** | 0 | 0 | 15 | 13 |
| `PYGAME-COBOL-CODEX` | **11** | 0 | 31 | 1 | 42 |
| `TTTGAME15-COBOL-CLAUDE` | **31** | 0 | 70 | 5 | 101 |
| `TTTGAME15-COBOL-CODEX` | **35** | 0 | 0 | 4 | 35 |
| `SAT-COBOL-CLAUDE` | **87** | 0 | 0 | 10 | 57 |
| `COMPRESS-COBOL-CLAUDE` | **11** | 0 | 62 | 1 | 73 |

### Difficulty signals (raw values)

Each project's difficulty label is the quartile of its mean rank across seven signals. Raw values below; full derivation in `scripts/difficulty.py`.

| Project | Active h | Span d | Prompts | Redirect/bug | Err rate | Fix cycles | Fix-time share |
|---|---:|---:|---:|---:|---:|---:|---:|
| `COMPILER-COBOL-CLAUDE` | 32.51 | 11 | 98 | 14 | 8.7% | 42 | 3.2% |
| `COMPILER-COBOL-CODEX` | 10.97 | 4 | 97 | 5 | 20.0% | 152 | 3.9% |
| `CHESS-COBOL-CODEX` | 4.98 | 38 | 26 | 10 | 3.4% | 6 | 2.4% |
| `PAYROLL-COBOL-CODEX` | 0.51 | 26 | 19 | 6 | 16.1% | 7 | 11.9% |
| `PAYROLL-COBOL-CLAUDE` | 1.95 | 26 | 21 | 7 | 5.1% | 1 | 7.0% |
| `CHESS-COBOL-CLAUDE` | 15.52 | 17 | 47 | 3 | 2.8% | 5 | 0.3% |
| `PYGAME-COBOL-CLAUDE` | 2.11 | 0 | 17 | 14 | 3.3% | 2 | 7.8% |
| `COMPRESS-COBOL-CODEX` | 0.92 | 34 | 10 | 3 | 14.4% | 5 | 0.4% |
| `SAT-COBOL-CODEX` | 1.84 | 0 | 29 | 0 | 11.0% | 4 | 4.6% |
| `DOOM-COBOL-CODEX` | 2.03 | 0 | 32 | 4 | 3.3% | 3 | 0.2% |
| `DOOM-COBOL-CLAUDE` | 3.24 | 0 | 20 | 4 | 0.7% | 1 | 0.7% |
| `PYGAME-COBOL-CODEX` | 0.07 | 0 | 3 | 1 | 9.7% | 3 | 5.1% |
| `TTTGAME15-COBOL-CLAUDE` | 2.07 | 6 | 12 | 1 | 1.5% | 0 | — |
| `TTTGAME15-COBOL-CODEX` | 0.55 | 0 | 11 | 1 | 3.5% | 1 | 0.1% |
| `SAT-COBOL-CLAUDE` | 1.24 | 1 | 8 | 0 | 1.7% | 1 | 0.1% |
| `COMPRESS-COBOL-CLAUDE` | 0.02 | 1 | 1 | 0 | — | 0 | — |

## 4. Per-project detail

### `chess-cobol-cc`

**Domain.** Chess engine in COBOL (GnuCOBOL); engine playability + ELO measurement via cutechess.

**Inventory.** 49 files, 3.3 MB total.

| Language | Files | LOC |
|---|---:|---:|
| C | 1 | 7,667 |
| COBOL | 1 | 3,460 |
| C/Header | 2 | 451 |
| Markdown | 1 | 17 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2.1.74 | 2026-03-12 19:37 | 17d 22h 51m | 47 | 1814 | 1156 | Bash×712, Edit×178, Read×143 | 1,937/591,930/166,713,533 | $518.44 |

**Opening prompt(s) / tasks:**

1. _[Claude Code, 2026-03-12]_ I want to build a chess engine in COBOL (using GNU Cobol)… at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of “similar” levels.

**Activity classes seen in opening prompts:** Test (1), Build/Config (1)

### `COBOL-chess`

**Domain.** Chess engine in COBOL (multi-session); architecture + specification backlog.

**Inventory.** 145 files, 4.3 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 16 | 3,988 |
| Markdown | 4 | 1,149 |
| JSON | 55 | 983 |
| Python | 4 | 681 |
| Makefile | 1 | 105 |
| Shell | 1 | 42 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Codex | `gpt-5.2` | 0.98.0 | 2026-02-09 09:42 | 2d 1h 16m | 24 | 21 | 1872 | exec_command×845, write_stdin×829, apply_patch×190 | 233,512,188/1,125,255/229,924,096 | $44.48 |
| 2 | Claude Code | `claude-opus-4-6` | 2.1.79 | 2026-03-19 12:54 | 27d 20h 46m | 10 | 85 | 55 | Bash×41, Read×5, Agent×5 | 53,152/44,782/5,121,398 | $20.74 |
| 3 | Codex | `gpt-5.4` | 0.115.0-alpha.11 | 2026-03-19 14:00 | 6m 50s | 1 | 11 | 63 | exec_command×55, write_stdin×7, apply_patch×1 | 2,637,865/21,699/2,508,544 | $0.69 |

**Opening prompt(s) / tasks:**

1. _[Codex, 2026-02-09]_ I want to build a chess engine in COBOL (GNUCobol)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of "similar" levels
2. _[Claude Code, 2026-03-19]_ You are a “Post-Session Backlog & Strategy Analyst” operating locally inside the current repository.  PRIMARY GOAL Produce an evidence-based, reproducible post-session report using a strict TWO-PASS workflow: - PASS 1 (Extraction): reconstruct the feature backlog + prompt ledger …
3. _[Codex, 2026-03-19]_ Please analyze thorughly the repo and write a README.md to document the architecture and features (being heavily inspired by the README of https://github.com/acherm/agentic-chessengine-latex-TeXCCChess and https://blog.mathieuacher.com/TeXCCChessEngine/)... I suggest a "light" RE…

**Activity classes seen in opening prompts:** Implement feature (2), Document (2), Port/Rewrite (2), Test (1), Build/Config (1), Research (1)

### `cobol-compiler-cc`

**Domain.** A COBOL compiler (and interpreter) written in COBOL. Translates COBOL to C; self-hosts non-trivial programs.

**Inventory.** 107 files, 4.1 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 36 | 18,908 |
| C | 16 | 3,068 |
| Markdown | 3 | 742 |
| Shell | 1 | 332 |
| C/Header | 2 | 67 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2.1.87 | 2026-03-29 15:55 | 11d 13h 49m | 97 | 6368 | 3734 | Bash×1928, Edit×656, Read×649 | 7,210/1,564,342/2,933,497,292 | $5183.70 |
| 2 | Claude Code | `None` | 2.1.87 | 2026-03-30 08:54 | 0m 2s | 6 | 0 | 0 |  | 0/0/0 | $0.00 |
| 3 | Claude Code | `claude-opus-4-6` | 2.1.92 | 2026-04-05 21:30 | 30m 58s | 3 | 17 | 6 | Bash×4, Agent×2 | 33/3,184/303,727 | $1.27 |

**Opening prompt(s) / tasks:**

1. _[Claude Code, 2026-03-29]_ Write a COBOL compiler in COBOL. Demonstrate that you can run some (non-trivial) COBOL programs thanks to the written compiler.
2. _[Claude Code, 2026-03-30]_ <local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>
3. _[Claude Code, 2026-04-05]_ On the build flags: -free was actually never correct — the compiler source uses fixed-format comments (* in column 7), which aren't valid in free-format COBOL. GnuCOBOL was   apparently tolerant of it, but fixed-format is the right mode. The -O2 issue is a GnuCOBOL 3.2.0 bug on m…

**Activity classes seen in opening prompts:** Build/Config (2), Unclassified (1), Debug / Fix (1), Research (1)

### `cobol-compiler-codex`

**Domain.** Alternative COBOL-to-C 'minicobc' compiler, driven by Codex. Benchmarks vs. GnuCOBOL.

**Inventory.** 252 files, 3.2 MB total.

| Language | Files | LOC |
|---|---:|---:|
| C | 25 | 63,074 |
| COBOL | 69 | 13,173 |
| Python | 13 | 5,940 |
| C/Header | 31 | 3,467 |
| JSON | 2 | 1,945 |
| Shell | 39 | 1,589 |
| Markdown | 5 | 1,405 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Codex | `gpt-5.4` | 0.117.0-alpha.24 | 2026-03-29 15:54 | 4d 20h 5m | 89 | 1470 | 5070 | exec_command×3850, apply_patch×747, write_stdin×424 | 481,684,489/2,237,920/463,565,056 | $102.97 |
| 2 | Codex | `gpt-5.4` | 0.118.0-alpha.2 | 2026-04-03 12:25 | 58m 13s | 4 | 43 | 130 | exec_command×113, apply_patch×10, write_stdin×5 | 10,406,472/65,793/9,396,224 | $3.10 |
| 3 | Codex | `gpt-5.4` | 0.118.0-alpha.2 | 2026-04-03 13:41 | 5m 9s | 1 | 13 | 55 | exec_command×49, write_stdin×5, apply_patch×1 | 1,869,373/13,904/1,699,968 | $0.56 |
| 4 | Codex | `gpt-5.4` | 0.118.0-alpha.2 | 2026-04-03 13:54 | 44m 38s | 2 | 42 | 115 | exec_command×101, write_stdin×9, apply_patch×5 | 5,414,661/33,155/5,007,488 | $1.47 |

**Opening prompt(s) / tasks:**

1. _[Codex, 2026-03-29]_ Write a COBOL compiler in COBOL. Demonstrate that you can run some (non-trivial) COBOL programs thanks to the written compiler.
2. _[Codex, 2026-04-03]_ I'm seeking a way to test the minicobc COBOL compiler...  GNU Cobol is another compiler internally and continuously tested using eg  https://github.com/OCamlPro/gnucobol/tree/gitside-gnucobol-3.x/tests/cobol85  Would it be possible to use this test suite to test minicobc?
3. _[Codex, 2026-04-03]_ mathieuacher@Mathieus-MacBook-Pro cobol-compiler-codex % MINICOBC_VERBOSE=1 ./scripts/run-cobol-doom.sh  libcob: warning: implicit CLOSE of TARGET-C-FILE ('build/doom/generic/doom.c') libcob: warning: implicit CLOSE of INPUT-CODE-FILE ('build/doom/generic/doom.c.expanded.cob')
4. _[Codex, 2026-04-03]_ The minicobc compiler seems working on agentic-cobol-game15tictactoe... What's the performance compared to GNU Cobol? Please design an experiment to show functional correctness/equivalence (wrt GNU Cobol) and report on build/execution time

**Activity classes seen in opening prompts:** Build/Config (4), Test (1), Document (1), Optimize (1), Port/Rewrite (1), Research (1)

### `cobol-compress-codex`

**Domain.** COBPACK — columnar packer / compressor for fixed-record COBOL data, implemented in pure COBOL (Codex-built).

**Inventory.** 29 files, 0.3 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 2 | 2,021 |
| Markdown | 4 | 930 |
| Python | 5 | 774 |
| JSON | 1 | 370 |
| Shell | 2 | 190 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Codex | `gpt-5.4` | 0.108.0-alpha.12 | 2026-03-12 20:18 | 10d 17h 9m | 8 | 74 | 237 | exec_command×159, apply_patch×60, write_stdin×15 | 16,647,174/138,451/16,029,696 | $4.16 |
| 2 | Claude Code | `claude-opus-4-6` | 2.1.79 | 2026-03-19 15:50 | 22h 34m | 4 | 53 | 42 | Read×20, Bash×16, Write×4 | 2,755/26,816/2,512,024 | $24.73 |
| 3 | Codex | `gpt-5.4` | 0.119.0-alpha.11 | 2026-04-16 09:58 | 2m 37s | 1 | 7 | 26 | exec_command×24, update_plan×2 | 443,948/7,365/383,616 | $0.20 |

**Opening prompt(s) / tasks:**

1. _[Codex, 2026-03-12]_ # COBPACK — MVP0 Specification (GNUCobol)  ## Goal (MVP0)  Build a command-line tool `cobpack` that can:  1. **Package** a fixed-length record file into a `.cpc` container (field-wise / columnar layout) using only the `NONE` codec (no compression). 2. **Unpack** that `.cpc` back …
2. _[Claude Code, 2026-03-19]_ You are a “Post-Session Backlog & Strategy Analyst” operating locally inside the current repository.  PRIMARY GOAL Produce an evidence-based, reproducible post-session report using a strict TWO-PASS workflow: - PASS 1 (Extraction): reconstruct (i) a USER-DRIVEN Feature Backlog, (…
3. _[Codex, 2026-04-16]_ the thread of Codex session is not visible in the left-hand side of Codex app... can you analyze history/sessions of this folder, and report on user prompts used?

**Activity classes seen in opening prompts:** Document (2), Port/Rewrite (2), Debug / Fix (1), Build/Config (1), Implement feature (1), Research (1)

### `cobol-compress-cobolcc`

**Domain.** COBPACK — columnar compressor (Claude-Code-built) — second-agent replica of the COBPACK domain.

**Inventory.** 24 files, 0.2 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 3 | 2,126 |
| Python | 4 | 516 |
| Shell | 2 | 323 |
| Markdown | 1 | 215 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2.1.110 | 2026-04-16 05:42 | 1d 10h 48m | 7 | 230 | 136 | Bash×66, Edit×22, Write×16 | 486/550,583/37,422,175 | $129.48 |

**Opening prompt(s) / tasks:**

1. _[Claude Code, 2026-04-16]_ # COBPACK — MVP0 Specification (GNUCobol)  ## Goal (MVP0)  Build a command-line tool `cobpack` that can:  1. **Package** a fixed-length record file into a `.cpc` container (field-wise / columnar layout) using only the `NONE` codec (no compression). 2. **Unpack** that `.cpc` back …

**Activity classes seen in opening prompts:** Implement feature (1), Debug / Fix (1), Build/Config (1)

### `cobol-doom-cc`

**Domain.** Doom-like FPS in COBOL (Claude Code) — modular walker + ray-casting + enemies + levels.

**Inventory.** 12 files, 0.2 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 8 | 1,869 |
| Shell | 1 | 118 |
| Makefile | 1 | 21 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Claude Code | `claude-opus-4-7` | 2.1.112 | 2026-04-17 16:35 | 20h 12m | 20 | 334 | 152 | Bash×79, Edit×53, Write×11 | 628/1,684,363/130,194,776 | $367.10 |

**Opening prompt(s) / tasks:**

1. _[Claude Code, 2026-04-17]_ Write a COBOL program (GnuCOBOL) that runs in a terminal and lets a human walk around a 2-D grid level from a top-down view.  Required behaviour:  The level is a rectangular grid (roughly 20×20 or larger) made of wall cells and open cells, with a clearly visible layout of rooms a…

**Activity classes seen in opening prompts:** Unclassified (1)

### `cobol-doom-codex`

**Domain.** Doom-like FPS in COBOL (Codex) — gridwalker + SDL2 bridge + 11 COPY books + BMP sprites.

**Inventory.** 81 files, 122.6 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 12 | 2,096 |
| C | 2 | 1,839 |
| Makefile | 1 | 21 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Codex | `gpt-5.4` | 0.119.0-alpha.11 | 2026-04-17 16:34 | 20h 14m | 31 | 233 | 631 | exec_command×402, apply_patch×87, write_stdin×84 | 44,542,491/357,679/42,641,792 | $11.28 |

**Opening prompt(s) / tasks:**

1. _[Codex, 2026-04-17]_ Write a COBOL program (GnuCOBOL) that runs in a terminal and lets a human walk around a 2-D grid level from a top-down view.  Required behaviour:  The level is a rectangular grid (roughly 20×20 or larger) made of wall cells and open cells, with a clearly visible layout of rooms a…

**Activity classes seen in opening prompts:** Unclassified (1)

### `cobol-jb-cc`

**Domain.** —

**Inventory.** 10 files, 0.2 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 1 | 598 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Claude Code | `claude-sonnet-4-6` | 2.1.173 | 2026-06-11 10:10 | 26d 1h 34m | 29 | 250 | 136 | Bash×62, Edit×61, Read×10 | 1,171/222,078/19,457,587 | $13.35 |

**Opening prompt(s) / tasks:**

1. _[Claude Code, 2026-06-11]_ <local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>

**Activity classes seen in opening prompts:** Unclassified (1)

### `cobol-jb-codex`

**Domain.** —

**Inventory.** 10 files, 0.1 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 1 | 647 |
| Markdown | 1 | 67 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Codex | `gpt-5.4` | 0.138.0-alpha.7 | 2026-06-11 10:18 | 26d 1h 55m | 18 | 107 | 179 | exec_command×161, apply_patch×18 | 10,338,751/88,940/9,914,496 | $2.66 |
| 2 | Codex | `gpt-5.5` | 0.142.5 | 2026-07-07 11:16 | 6m 44s | 1 | 7 | 20 | exec_command×14, list_threads×3, read_thread×1 | 363,101/5,686/286,080 | $0.19 |

**Opening prompt(s) / tasks:**

1. _[Codex, 2026-06-11]_ You are a mainframe COBOL expert. Generate a complete, self-contained COBOL program.  ## Business Context Domain: Payroll management system  ## Technical Constraints - Target lines of code (LOC): 300 lines - Number of files the program must handle: 2   (employees_input.dat as inp…
2. _[Codex, 2026-07-07]_ there are existing sessions I'd like to resume in this folder... but they do not appear in the left-hand side. Can you depict it? or tell me how to "restore" it?

**Activity classes seen in opening prompts:** Optimize (1), Build/Config (1), Unclassified (1)

### `COBOL-pygame`

**Domain.** A pygame-style framework in COBOL (GnuCOBOL), exposing a Python-pygame-like interface.

**Inventory.** 12 files, 0.1 MB total.

| Language | Files | LOC |
|---|---:|---:|
| Markdown | 3 | 775 |
| COBOL | 3 | 492 |
| JSON | 1 | 472 |
| C | 1 | 367 |
| C/Header | 1 | 55 |
| Makefile | 1 | 47 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Codex | `gpt-5.2` | 0.98.0 | 2026-02-09 09:40 | 1h 1m | 3 | 3 | 31 | exec_command×12, apply_patch×10, update_plan×9 | 1,102,142/47,872/1,025,920 | $0.70 |
| 2 | Claude Code | `claude-opus-4-6` | 2.1.79 | 2026-03-19 15:47 | 34m 29s | 5 | 73 | 51 | Bash×31, Read×15, Write×4 | 287/31,163/4,325,396 | $15.90 |

**Opening prompt(s) / tasks:**

1. _[Codex, 2026-02-09]_ Write a pygame framework for COBOL (using GNUcobol)
2. _[Claude Code, 2026-03-19]_ You are a “Post-Session Backlog & Strategy Analyst” operating locally inside the current repository.  PRIMARY GOAL Produce an evidence-based, reproducible post-session report using a strict TWO-PASS workflow: - PASS 1 (Extraction): reconstruct (i) a USER-DRIVEN Feature Backlog, (…

**Activity classes seen in opening prompts:** Unclassified (1), Implement feature (1), Document (1), Port/Rewrite (1)

### `cobol-pygame-cc`

**Domain.** —

**Inventory.** 19 files, 0.4 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 5 | 915 |
| Markdown | 1 | 407 |
| C | 2 | 349 |
| Makefile | 1 | 50 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2.1.203 | 2026-07-08 09:40 | 5h 30m | 17 | 264 | 153 | Bash×59, Edit×42, Read×38 | 345/489,521/25,086,132 | $90.04 |

**Opening prompt(s) / tasks:**

1. _[Claude Code, 2026-07-08]_ Create a small "pygame-like" graphical framework that can be called from COBOL programs compiled with GnuCOBOL (cobc). The framework itself may be written in any host language you think appropriate (e.g., a thin C layer over an existing cross-platform graphics/windowing library),…

**Activity classes seen in opening prompts:** Build/Config (1)

### `SATCobol-codex`

**Domain.** SAT solver in COBOL (Codex) — modular COPY books + MiniSat/SAT4J cross-checks + uf/uuf benchmark families.

**Inventory.** 191 files, 6.8 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 6 | 1,934 |
| Shell | 5 | 936 |
| Markdown | 2 | 271 |
| Makefile | 1 | 28 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Codex | `gpt-5.4` | 0.119.0-alpha.11 | 2026-04-15 12:19 | 17h 24m | 29 | 263 | 508 | exec_command×306, write_stdin×147, apply_patch×43 | 43,570,745/290,821/41,474,048 | $10.71 |

**Opening prompt(s) / tasks:**

1. _[Codex, 2026-04-15]_ Implement a robust DIMACS CNF parser in COBOL: supports c comments, p cnf <vars> <clauses>, arbitrary whitespace, multiple lines per clause, and 0 clause terminators. Add a parser-only mode: ./cobsat --parse file.cnf prints a normalized representation (vars, clauses, literals). A…

**Activity classes seen in opening prompts:** Implement feature (1), Test (1), Port/Rewrite (1)

### `SATCobol-cc`

**Domain.** SAT solver in COBOL (Claude Code) — second-agent replica of the SAT domain.

**Inventory.** 2832 files, 28.2 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 13 | 1,675 |
| Shell | 4 | 719 |
| Makefile | 1 | 18 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2.1.109 | 2026-04-15 12:20 | 1d 22h 41m | 31 | 647 | 360 | Bash×210, Edit×67, Write×58 | 977/984,752/168,569,731 | $473.78 |

**Opening prompt(s) / tasks:**

1. _[Claude Code, 2026-04-15]_ Implement a robust DIMACS CNF parser in COBOL: supports c comments, p cnf <vars> <clauses>, arbitrary whitespace, multiple lines per clause, and 0 clause terminators. Add a parser-only mode: ./cobsat --parse file.cnf prints a normalized representation (vars, clauses, literals). A…

**Activity classes seen in opening prompts:** Implement feature (1), Test (1), Port/Rewrite (1)

### `cobol-tictactoe`

**Domain.** Game-of-15 and tic-tac-toe variants in COBOL with minimax-style tree search (Claude Code).

**Inventory.** 15 files, 0.5 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 5 | 1,919 |
| Markdown | 3 | 430 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Claude Code | `claude-opus-4-6` | 2.1.74 | 2026-03-12 19:46 | 6d 19h 51m | 14 | 125 | 67 | Bash×46, Edit×8, Write×6 | 188/318,409/7,877,782 | $52.79 |
| 2 | Claude Code | `claude-opus-4-6` | 2.1.79 | 2026-03-19 10:11 | 27d 23h 36m | 21 | 109 | 75 | Bash×36, Read×18, Edit×14 | 1,428/40,823/5,858,725 | $35.00 |

**Opening prompt(s) / tasks:**

1. _[Claude Code, 2026-03-12]_ The game of 15 is defined as follows: Two players in turn say a number between one and nine. A particular number may not be repeated. The game is won by the player who has said three numbers whose sum is 15. If all the numbers are used and no one gets three numbers that add up to…
2. _[Claude Code, 2026-03-19]_ You are a “Post-Session Backlog & Strategy Analyst” operating locally inside a repository.  GOAL Run a strict TWO-PASS post-session analysis: - PASS 1 (Extraction): reconstruct an ex-post backlog and replay package for reproducibility. - PASS 2 (Interpretation): characterize codi…

**Activity classes seen in opening prompts:** Implement feature (1), Port/Rewrite (1), Research (1)

### `game15-cobol-codex`

**Domain.** Game of 15 in COBOL (Codex) — second-agent replica of the small-game domain.

**Inventory.** 8 files, 0.2 MB total.

| Language | Files | LOC |
|---|---:|---:|
| COBOL | 5 | 2,822 |

**Sessions.**

| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |
|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|
| 1 | Codex | `gpt-5.4` | 0.119.0-alpha.11 | 2026-04-16 09:49 | 3h 37m | 11 | 77 | 173 | exec_command×145, apply_patch×18, write_stdin×9 | 8,899,716/113,459/8,434,688 | $2.77 |

**Opening prompt(s) / tasks:**

1. _[Codex, 2026-04-16]_ Write a COBOL program (GnuCOBOL) for the "Game of 15".  Rules: Two players alternate picking a number from {1, 2, ..., 9}. A number cannot be picked twice. A player wins when any three of their chosen numbers sum to exactly 15. If all nine numbers are picked and no player has won…

**Activity classes seen in opening prompts:** Document (1), Port/Rewrite (1)

## 5. What kinds of SE tasks were performed?

Activity labels are derived from first-prompt keywords plus tool-breakdown patterns; they describe the *intent* of a session, not every turn inside it.

### 5.1 Activity distribution across sessions

| Activity class | Sessions |
|---|---:|
| Implement feature | 8 |
| Refactor | 0 |
| Debug / Fix | 3 |
| Test | 5 |
| Document | 7 |
| Optimize | 2 |
| Port/Rewrite | 10 |
| Research | 5 |
| Build/Config | 12 |
| Review/Audit | 0 |
| _Unclassified_ | 6 |

### 5.2 'Features' built — one-line per project

Counting the main engineering deliverables across the analysed projects, broadly:

1. **Chess engines in COBOL** (2 projects: `chess-cobol-cc`, `COBOL-chess`) — move generation, search, evaluation, PGN I/O, ELO benchmarking vs cutechess.
2. **COBOL compilers in COBOL** (2 projects: `cobol-compiler-cc`, `cobol-compiler-codex`) — lexer, preprocessor, parser, COBOL→C code generator, COBOL interpreter, multi-program linking, RECURSIVE programs, COMP-5, CALL to C, a large intrinsic library. The `-cc` build produces a self-hosted compiler of ~11k COBOL LOC.
3. **COBPACK columnar compressor** (`cobol-compress-codex`) — pure COBOL implementation of a fixed-record packer with NONE + RLESP codecs, CRC32, determinism / randomised round-trip test harness, schema-aware packing.
4. **Doom in COBOL** + Java port + C demo (`cobol-doom`) — ray-casting engine, enemies, pickups, level definitions.
5. **Payroll case-study in COBOL** (`cobol-jb`) — fixed-format records, overtime rules, social contributions, payslip + summary report, verification grid.
6. **pygame-for-COBOL framework** (`COBOL-pygame`) — C glue exposing pygame-like primitives callable from GnuCOBOL, plus examples.
7. **SAT solver in COBOL** (`SATCobol-codex`) — DIMACS CNF parser, unit-propagation + search split across 5 COPY modules, SAT4J / MiniSat cross-check harness, uf/uuf benchmark sets at 75 / 100 / 125 / 150 vars.
8. **Games: Game-of-15 / tic-tac-toe** (`cobol-tictactoe`) — minimax tree search, N-variant, multiple board sizes.

### 5.3 Tool-use patterns

Across all sessions, dominant tools were:

| Tool | Calls | Dominant agent |
|---|---:|---|
| `exec_command` | 6,236 | Codex |
| `Bash` | 3,290 | Claude Code |
| `write_stdin` | 1,534 | Codex |
| `apply_patch` | 1,190 | Codex |
| `Edit` | 1,102 | Claude Code |
| `Read` | 942 | Claude Code |
| `Grep` | 462 | Claude Code |
| `Write` | 146 | Claude Code |
| `update_plan` | 97 | Codex |
| `TaskUpdate` | 54 | Claude Code |
| `TaskOutput` | 53 | Claude Code |
| `view_image` | 37 | Codex |
| `TaskCreate` | 32 | Claude Code |
| `Agent` | 29 | Claude Code |
| `ToolSearch` | 9 | Claude Code |

Takeaways:

- Codex spends the overwhelming majority of its tool budget on `exec_command` (shell) and `write_stdin` (interactive pipes) — lots of compile-run-inspect loops; edits go through `apply_patch`.
- Claude Code splits its budget across `Bash`, `Edit`, `Read`, `Write`, `Grep`, `Agent` and `TaskUpdate` — showing a richer planning/editing toolchain but fewer raw shell cycles per session.
- Both agents show heavy *iterative* workflows (build → run → fix) on COBOL, consistent with GnuCOBOL's finicky formatting rules and the multi-day debugging cycles visible in `chess-cobol-cc`, `cobol-compiler-cc`, `cobol-doom`, and `cobol-tictactoe`.

## 6. Coding agents — versions seen on disk

| Agent | Models | CLI versions |
|---|---|---|
| Claude Code | `claude-opus-4-6`×11, `claude-opus-4-7`×1, `claude-sonnet-4-6`×1 | 2.1.109, 2.1.110, 2.1.112, 2.1.173, 2.1.203, 2.1.74, 2.1.79, 2.1.87, 2.1.92 |
| Codex | `gpt-5.4`×11, `gpt-5.2`×2, `gpt-5.5`×1 | 0.108.0-alpha.12, 0.115.0-alpha.11, 0.117.0-alpha.24, 0.118.0-alpha.2, 0.119.0-alpha.11, 0.138.0-alpha.7, 0.142.5, 0.98.0 |

**Notes on versions.**
- Claude Code CLI on this machine ranges from **2.1.63** (earliest seen, Mar 2026, `cobol-doom`) to **2.1.92** (most recent Claude-Code-driven session in the set).
- Codex CLI ranges from **0.98.0** (Feb 2026) to **0.118.0-alpha.2** (April 2026); Codex model names evolved `gpt-5.2` → `gpt-5.3-codex` → `gpt-5.4` over the window.
- Claude model: consistently `claude-opus-4-6` (1M context).

## 7. Caveats

- **Duration ≠ active work.** The `duration_s` field is last-event-minus-first-event; resumed sessions (most notably `chess-cobol-cc`, 18d; `cobol-compiler-cc`, 11d; `cobol-doom`, 27d) span many days with long idle gaps. A more faithful 'active work' estimate would require summing inter-event gaps below some threshold.
- **Cost is an API-rack-rate upper bound.** Actual billing under Team / Max / Pro subscriptions does not map linearly to the token counts; take these figures as an order-of-magnitude signal of compute intensity, not a cash figure.
- **Two folders excluded** from the main analysis: `cobol-vibes` and `test-cline-COBOL` have artefacts (Flappy-Bird variants in COBOL) but no preserved agent JSONL traces on this machine.
- **Activity labels are shallow.** Derived from first-prompt keywords; a proper classification would read every turn.

