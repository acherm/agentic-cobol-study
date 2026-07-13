# game15-cobol-codex — STORY

## The replica that isn't a copy

Byte-identical prompts. A different agent. A substantively different architecture. `game15-cobol-codex` is the Codex-built twin of `cobol-tictactoe`: the six human prompts came verbatim from the Claude-Code sibling's `REPLAY_PROMPTS.md` (PL-ROOT plus PL-02..PL-06 match the sibling's replay pack byte-for-byte), and Codex was asked to build the Game of 15 from the same canonical brief. The outputs match — same oracles (255,168 / 31,896), same five-file set, zero hangs, zero user clarifications in either run — but the code underneath diverges so systematically that the project is best read as a controlled experiment in replay-prompt portability.

## Domain: same game, same oracle

The underlying target is identical to `cobol-tictactoe`. Two players alternate picks from {1..9}; the first to hold any three numbers summing to 15 wins; exhaustive enumeration yields 131,184 / 77,904 / 46,080 / 255,168. The Game of 15 is isomorphic to tic-tac-toe through the 3x3 magic square, so the algorithms are textbook and the oracle is fixed. What varies is *how* each agent chooses to embed those algorithms into GnuCOBOL — and that is the research question this project was built to probe: when you hand two agents the exact same prompt pack, how much of the resulting code is the prompt, and how much is the agent?

## Chronology: one session, four commits

One Codex session on 2026-04-16 (09:49 to 13:26 UTC, about 3h37m wall clock) produced everything. The human side stayed strict replay mode: six feature prompts (1:1 with BL-01..BL-06) plus five procedural "commit" instructions — no clarifications, no scope churn, no follow-ups. Codex responded with 32 specification-backlog items, three self-detected bug fixes, and four commits on branch `codex/game15`: `29cbcaa` (enumerator), `c41b9b5` (unique flag + tree + avoid, bundled into one commit because the user issued a single "commit" across those steps), `f9c2eb1` (0.15 variants), and `ce67d51` (generalised Game of N). Twenty `cobc -x -free` invocations, all clean after the initial scaffold compile. The three bugs — `FILLED-TARGET PIC 99` underflowing the retrograde loop, a stale `OWNER` array leaking from solve into print, and an avoid-line stealing a one-level-shallow prefix — were all diagnosed and fixed by the agent in under five minutes apiece, without user intervention.

## Delivered: five programs mirroring the sibling's roles

The file set is the sibling's file set, with exactly one naming drift:

- `game15.cob` (500 LOC) — counter with `--unique` symmetry flag
- `game15_tree.cob` (671 LOC) — optimal-play tree (underscore; the sibling writes `game15tree`)
- `game015.cob` (501 LOC) — 0.15 counter variant
- `game015tree.cob` (685 LOC) — 0.15 tree variant
- `gameN.cob` (465 LOC) — generalised `<target-sum> [<max-number>]` program

Total production COBOL: **2,822 LOC** vs the Claude-Code sibling's roughly **2,020 LOC** — a **+40%** size delta. Same behaviour, same oracles, noticeably heavier implementation.

## Architectural divergences from the CC sibling

This is where the replica becomes interesting. Four places show Codex making a categorically different data-structure choice on the same prompt text.

**Symmetry deduplication.** Both agents reduce the D4 orbit of each move sequence to its lexicographic minimum. Claude Code hashes that canonical form into a standard set. Codex instead ranks it via falling-factorial weights plus a per-length offset table, then declares a static `SEEN-CANONICAL PIC X OCCURS 986409` array — a **986,409-byte bitmap** that covers 9! plus lower-length offsets of the permutation prefix space of {1..9}. It is a custom perfect hash for variable-length permutation prefixes, built from scratch in COBOL, sized to the full address space rather than to reachability.

**Tree solver.** Claude Code does lazy top-down minimax with a memoization table filled on visit. Codex does eager **bottom-up retrograde analysis over all 19,683 base-3 states**: outer loop `FILLED-TARGET` from 9 down to 0, validity filter pruning impossible piece-count configurations, then minimax folded into the retrograde fill so every parent's children are guaranteed solved before it is evaluated. The printer is a pure query over the filled `STATE-OUTCOME(19683)` table. Fill the whole space, then walk; don't walk, then cache.

**Win check.** Claude Code encodes the eight winning lines as a magic-triple string `"159168249258267348357456"` with `REDEFINES`. Codex writes out **eight explicit tic-tac-toe-line IFs** — `IF OWNER(1)=CP AND OWNER(5)=CP AND OWNER(9)=CP`, one per line, post-magic-square. Same eight triples, opposite idiom.

**0.15 rendering.** Claude Code inlines `"0.0"` as a string prefix at display sites. Codex introduces a `MOVE-LABEL PIC X(4) OCCURS 9` lookup table pre-filled with `"0.01".."0.09"`, then reaches through it at every display site — a small dedicated indirection rather than an inline format.

Every tree walk, in every program, is driven by a hand-managed per-level stack — no `CALL … RECURSIVE` anywhere.

## Validation and difficulties

Zero recursion, zero hangs, zero user clarifications — in both runs. The three bug fixes (F-01 underflow, F-02 stale owner, F-03 avoid-line prefix) were all self-detected by running the binary and reading the output; none reached the user. One recurrent anti-pattern is worth noting: three times Codex rebuilt a binary at `/tmp/` while another shell still pointed at the stale copy, diagnosed the mismatch each time, and switched to sequential `cobc … && /tmp/bin …` invocations. A Codex-specific habit rather than a capability gap.

## Compute and context

Comfortable. One session, 533 turns, 173 tool uses, 20 compiles, 49 runs. No context pressure, no retries against compile errors, no oracle mismatches after the first correct build per BL. The agent had room to choose eager over lazy and did so deliberately (reasoning block at event_114: "bottom-up minimax over all reachable board states"; event_022: "explicit backtracking rather than recursive self-calls").

## Why it matters

`game15-cobol-codex` closes the 2-agent coverage gap for the small-game / minimax domain and turns the sibling project into a matched pair. It lets the methodology itself be measured: the replay prompts are portable across agents to the level of *scope, file set, and oracles*, but not to the level of *data structures or memory-compute tradeoffs*.

## The surprising insight

The shared assumption behind replay-prompt benchmarking is that identical prompts on identical problems should produce substantially similar code. The paired Game-of-15 projects falsify that at the implementation level. Same six prompts, same five-file layout, same externally observable counts, and yet Codex writes 40% more lines, declares a 986,409-byte factorial-rank bitmap where its sibling uses a hash set, eagerly fills 19,683 states where its sibling lazily memoises, and replaces a magic-triple string with eight hand-written IFs. "Same prompt implies same implementation" is wrong. Prompts control scope; they do not homogenise architecture.
