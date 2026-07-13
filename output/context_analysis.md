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

