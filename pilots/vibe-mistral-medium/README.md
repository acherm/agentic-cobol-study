# Pilot P3 — Mistral vibe CLI with mistral-medium-3.5

One exploratory pilot trajectory (June 26, 2026) on the corpus's easiest domain family
(Game of 15 — number-picking game isomorphic to tic-tac-toe), run with **Mistral's vibe CLI**.
Copied verbatim from `~/SANDBOX/vibes-test/` on 2026-07-07 for preservation.

## Stack

- Harness: Mistral vibe CLI (no version string recorded in the logs).
- Model: `mistral-medium-3.5` (provider-side name `mistral-vibe-cli-latest`), Mistral API,
  `thinking: high`, `temperature: 1.0`. (Not "Mistral Pro", not devstral — devstral entries
  exist in the config but were never used.)
- Secrets check 2026-07-07: `meta.json` files embed the config; they contain only the
  env-var *name* `MISTRAL_API_KEY`, no key material.

## Shape and totals

One continuous trajectory split over three sessions chained by `parent_session_id`,
each split triggered by auto-compaction at 100k tokens:

`session_20260626_151517_f36a1668` → `session_20260626_154544_05f3c87f` → `session_20260626_215903_07f9c098`

Totals (cumulative `stats` in the final `meta.json`): 166 steps, 152 tool calls (24 failed),
**10,310,165 input + 125,157 output tokens, $16.40**, ≈6 h 45 min wall clock
(the 6-hour middle session almost certainly includes a long idle gap — its only human
message is "sorry continue"). Note: per-session `stats` blocks are **cumulative across the
chain**; per-session figures require deltas.

Human involvement (6 real turns, no code written by the human): the task prompt,
"you didn't write anything?", "how to compile and make it run?", one pasted `cobc` error
dump (the human ran the *first* compile), "sorry continue", "/export".

## Outcome: plausible but wrong (two verified defects — corrected 2026-07-08)

The final `game15.cbl` (523 lines) **compiles, runs, and prints totals that pass its own
printed consistency check** — and every number is wrong. The final state was reached only
after at least four distinct wrong-output regimes (all-P1-wins, all-draws, P1-only wins,
final). Two independent defects, both verified post-hoc
(`replications/vibe-bug-verification.py`):

1. **Structural**: the program enumerates all **9! = 362,880 fixed orderings** of the
   digits 1–9 and counts one "game" per ordering, so its total can only ever be 362,880.
   The true game tree (stop at first win) has **255,168** games — the oracle the frontier
   corpus artifacts match.
2. **Win detection (the reason the win/draw split is wrong)**: in `CHECK-WIN-FOR-P1/P2`,
   the lines `IF P1-WINS-GAME EXIT PARAGRAPH` carry no `END-IF` and no period, so under
   COBOL scope rules the subsequent `PERFORM`s nest inside the first `IF` and are
   unreachable. **Only the {1,5,9} triple is ever checked.** A reference implementation
   with only-{1,5,9} detection reproduces the delivered counts *exactly*
   (43,200 / 17,280 / 302,400). Correct detection over the same 9! orderings would give
   212,256 / 104,544 / 46,080 (the program detects 19% of its own detectable wins).

So the 9! total is **not** an "algorithmic choice to enumerate move orders": the output
is the product of a latent COBOL scope bug on top of the wrong combinatorial object.

⚠ On the chatbot commentary embedded in `ANALYSIS.md`: its behavioral intuition (games
effectively running past wins) is directionally right — undetected wins do run to move 9
— but its mechanism (a missing early `return`) is wrong, and its closing claim that
"your code is correct for what it's computing" is refuted by defect 2. Use the
two-defect diagnosis above.

## Contents

- `session_*/messages.jsonl` — full turn-by-turn transcripts (with reasoning content).
- `session_*/meta.json` — config + cumulative stats + full system prompt.
- `game15.cbl` — final delivered source (the wrong-object enumerator).
- `ANALYSIS.md` — the author's raw contemporaneous notes ("results are eventually
  wrong… very bad session") + pasted output + external chatbot commentary (see caveat above).

The compiled `game15` binary is not copied (arch-specific; rebuild with
`cobc -x -o game15 game15.cbl`).
