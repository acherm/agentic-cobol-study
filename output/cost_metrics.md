## Cost metrics — tokens (not dollars)

Dollars are rack-rate estimates and don't compare cleanly between Claude Code and Codex. Tokens are the primitive unit of compute. Below, each token type is summed per project × agent. All the raw data is in [`output/cost_metrics.csv`](output/cost_metrics.csv).

### A. Token profile per project × agent

| Project | Agent | Sessions | Input | Output | Cache read | Cache create | Reasoning | **Total tokens** | Cache hit % | Est. $ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `chess-cobol-cc` | Claude Code | 1 | 1,937 | 591,930 | 166,713,533 | 11,943,652 | 0 | **179,251,052** | 100.0% | $518 |
| `COBOL-chess` | Codex | 2 | 236,150,053 | 1,146,954 | 232,432,640 | 0 | 897,503 | **470,627,150** | 49.6% | $45 |
| `cobol-compiler-cc` | Claude Code | 2 | 7,243 | 1,567,526 | 2,933,801,019 | 35,551,366 | 0 | **2,970,927,154** | 100.0% | $5185 |
| `cobol-compiler-codex` | Codex | 4 | 499,374,995 | 2,350,772 | 479,668,736 | 0 | 1,187,284 | **982,581,787** | 49.0% | $108 |
| `cobol-compress-codex` | Codex | 2 | 17,091,122 | 145,816 | 16,413,312 | 0 | 73,872 | **33,724,122** | 49.0% | $4 |
| `cobol-compress-cobolcc` | Claude Code | 1 | 486 | 550,583 | 37,422,175 | 1,708,980 | 0 | **39,682,224** | 100.0% | $129 |
| `cobol-doom-cc` | Claude Code | 1 | 628 | 1,684,363 | 130,194,776 | 2,425,304 | 0 | **134,305,071** | 100.0% | $367 |
| `cobol-doom-codex` | Codex | 1 | 44,542,491 | 357,679 | 42,641,792 | 0 | 191,316 | **87,733,278** | 48.9% | $11 |
| `cobol-jb-cc` | Claude Code | 1 | 1,171 | 222,078 | 19,457,587 | 1,113,176 | 0 | **20,794,012** | 100.0% | $13 |
| `cobol-jb-codex` | Codex | 2 | 10,701,852 | 94,626 | 10,200,576 | 0 | 49,754 | **21,046,808** | 48.8% | $3 |
| `COBOL-pygame` | Codex | 1 | 1,102,142 | 47,872 | 1,025,920 | 0 | 34,000 | **2,209,934** | 48.2% | $1 |
| `cobol-pygame-cc` | Claude Code | 1 | 345 | 489,521 | 25,086,132 | 837,119 | 0 | **26,413,117** | 100.0% | $90 |
| `SATCobol-codex` | Codex | 1 | 43,570,745 | 290,821 | 41,474,048 | 0 | 146,500 | **85,482,114** | 48.8% | $11 |
| `SATCobol-cc` | Claude Code | 1 | 977 | 984,752 | 168,569,731 | 7,843,062 | 0 | **177,398,522** | 100.0% | $474 |
| `cobol-tictactoe` | Claude Code | 1 | 188 | 318,409 | 7,877,782 | 911,207 | 0 | **9,107,586** | 100.0% | $53 |
| `game15-cobol-codex` | Codex | 1 | 8,899,716 | 113,459 | 8,434,688 | 0 | 68,774 | **17,516,637** | 48.7% | $3 |

### B. Per-project totals (agents summed)

| Project | Sessions | Input | Output | Cache read | Cache create | Reasoning | **Total tokens** | Est. $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cobol-compiler-cc` | 2 | 7,243 | 1,567,526 | 2,933,801,019 | 35,551,366 | 0 | **2,970,927,154** | $5185 |
| `cobol-compiler-codex` | 4 | 499,374,995 | 2,350,772 | 479,668,736 | 0 | 1,187,284 | **982,581,787** | $108 |
| `COBOL-chess` | 2 | 236,150,053 | 1,146,954 | 232,432,640 | 0 | 897,503 | **470,627,150** | $45 |
| `chess-cobol-cc` | 1 | 1,937 | 591,930 | 166,713,533 | 11,943,652 | 0 | **179,251,052** | $518 |
| `SATCobol-cc` | 1 | 977 | 984,752 | 168,569,731 | 7,843,062 | 0 | **177,398,522** | $474 |
| `cobol-doom-cc` | 1 | 628 | 1,684,363 | 130,194,776 | 2,425,304 | 0 | **134,305,071** | $367 |
| `cobol-doom-codex` | 1 | 44,542,491 | 357,679 | 42,641,792 | 0 | 191,316 | **87,733,278** | $11 |
| `SATCobol-codex` | 1 | 43,570,745 | 290,821 | 41,474,048 | 0 | 146,500 | **85,482,114** | $11 |
| `cobol-compress-cobolcc` | 1 | 486 | 550,583 | 37,422,175 | 1,708,980 | 0 | **39,682,224** | $129 |
| `cobol-compress-codex` | 2 | 17,091,122 | 145,816 | 16,413,312 | 0 | 73,872 | **33,724,122** | $4 |
| `cobol-pygame-cc` | 1 | 345 | 489,521 | 25,086,132 | 837,119 | 0 | **26,413,117** | $90 |
| `cobol-jb-codex` | 2 | 10,701,852 | 94,626 | 10,200,576 | 0 | 49,754 | **21,046,808** | $3 |
| `cobol-jb-cc` | 1 | 1,171 | 222,078 | 19,457,587 | 1,113,176 | 0 | **20,794,012** | $13 |
| `game15-cobol-codex` | 1 | 8,899,716 | 113,459 | 8,434,688 | 0 | 68,774 | **17,516,637** | $3 |
| `cobol-tictactoe` | 1 | 188 | 318,409 | 7,877,782 | 911,207 | 0 | **9,107,586** | $53 |
| `COBOL-pygame` | 1 | 1,102,142 | 47,872 | 1,025,920 | 0 | 34,000 | **2,209,934** | $1 |
| **GRAND TOTAL** | — | **861,446,091** | **10,957,161** | **4,321,414,447** | **62,333,866** | **2,649,003** | **5,258,800,568** | **$7016** |

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
| `cobol-compress-codex` | 145,816 | 1,812 | 80 | 18 | 8,101 | 9 | 16,202 |
| `cobol-pygame-cc` | 489,521 | 764 | 641 | 0 | — | 17 | 28,795 |
| `cobol-jb-codex` | 94,626 | 572 | 165 | 0 | — | 19 | 4,980 |
| `cobol-jb-cc` | 222,078 | 535 | 415 | 0 | — | 29 | 7,658 |
| `game15-cobol-codex` | 113,459 | 2,264 | 50 | 35 | 3,242 | 11 | 10,314 |
| `cobol-tictactoe` | 318,409 | 1,537 | 207 | 31 | 10,271 | 14 | 22,744 |
| `COBOL-pygame` | 47,872 | 398 | 120 | 11 | 4,352 | 3 | 15,957 |

### D. Caveats on token semantics

- **`input_tokens`** here is the *non-cached* input (new prompt tokens processed). Claude Code reports this directly; Codex reports `cached_input_tokens` separately and we subtract it from the raw total.
- **`output_tokens`** includes `thinking` blocks for Claude Code (they are charged at output rate). Codex reports `reasoning_output_tokens` in a separate bucket; we keep them in `reasoning_tokens` to make the hidden-CoT load visible.
- **`cache_read_tokens`** are billed at ~10 % of input rate on both platforms — a high cache-hit rate is a strong efficiency indicator for long-running sessions (Codex sessions on this machine often show 50–80 %).
- **`cache_creation_tokens`** (Claude-specific) are billed at ~125 % of input rate; they pay once and amortise across subsequent turns.
- **`reasoning_tokens`** (Codex-only) are billed at output rate but are invisible in the transcript. Projects with heavy reasoning_tokens are doing more hidden deliberation per user turn.
- **`cost_usd`** is a rack-rate upper bound; actual billing under Team / Max / Pro subscriptions differs. Use tokens for comparison.
- For reproducibility, every number here is recomputable from `output/sessions_all.json` with `scripts/cost_metrics.py`.

