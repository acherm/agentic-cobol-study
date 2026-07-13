# SATCobol-codex — a CDCL SAT solver in COBOL, within 9x of MiniSat

A conflict-driven clause-learning SAT solver, written in free-format COBOL, with watched literals, VSIDS, Luby restarts, first-UIP learning, and non-chronological backjumping — finishing the SATLIB `uf`/`uuf` benchmark sweep at 100 variables within a single-digit multiple of MiniSat's time. That is the artefact the Codex CLI agent produced in one 14-hour session on 2026-04-15, and it is the project worth staring at.

## The problem and the language it was solved in

CDCL is the skeleton every serious modern SAT solver shares: keep two "watched" literals per clause so unit propagation only visits the clauses it must, bump a per-variable activity score on conflicts and decay it periodically so branching follows the action (VSIDS), restart the search on a Luby schedule so the heuristic can escape bad prefixes, analyse each conflict back to the first unique implication point to learn a new clause, and backjump non-chronologically to the deepest level consistent with the learnt clause. In C or C++ this is textbook. In COBOL — free-format GnuCOBOL compiled with `cobc -x -free` — it is not, because the language has no pointers, no `malloc`, no `realloc`, no recursion-by-default, and no native module system. The clause database, the watch lists, the propagation trail, the assignment stack, and the implication graph all have to live inside fixed-capacity `OCCURS` tables indexed by `COMP-5` integers. Every "pointer" is an index. Every dynamic resize is a pre-sized ceiling. And the whole thing has to stay readable enough that the agent can keep editing it across nine commits.

Correctness, crucially, is not self-reported. The session wires in two external oracles. SAT4J's Java regression suite — the `aim`, `jnh`, and `pigeons` families, plus the `BugSAT118/162/179/180/181/182/184` repros — is mechanically translated to 128 file-based DIMACS fixtures and 11 embedded `bugsat*` cases, each mapped through a TSV manifest back to its upstream test id. MiniSat is wired in as both a differential checker (`scripts/crosscheck_minisat.sh` stores a full repro bundle on any disagreement) and a timing reference (`scripts/compare_minisat.sh` emits a per-family CSV with a `cobsat_over_minisat` ratio). The solver is never allowed to grade its own work.

## A single session in nine commits

One Codex rollout, model `gpt-5.4`, reasoning effort `xhigh`, personality `pragmatic`, workspace-write sandbox. Window: 2026-04-15T12:19Z to 2026-04-16T05:34Z. Active collaboration time across the window: about 46 minutes — the rest is the agent compiling, running tests, and measuring. 620 turns, 28 user messages, peak context 204k of the 258k window (78.9%), with 2 compactions to keep the session live.

The work breaks cleanly into nine episodes (EP1..EP9), one per commit:

1. `6e49eb7` — DIMACS parser, `--parse` normalised-output mode, edge-case harness (empty lines, CRLF, trailing spaces, runs of whitespace, comments between tokens), plus a ~100k-clause synthetic regression the agent added on its own initiative, plus the SATLIB `%`-then-`0` end-marker tolerance the agent patched in after the real `uf75-325` files tripped the parser.
2. `59d47ff` — `--check-model` mode and the baseline DPLL solver with unit propagation, chronological backtracking, and `s SATISFIABLE` / `v ... 0` / `s UNSATISFIABLE` output.
3. `14555932` — the refactor: the monolithic `cobsat.cob` is split into five COPY books under `src/modules/` (`cnf`, `io`, `parser`, `propagate`, `search`), included via `COPY` with `-I src/modules` mirrored in both the `Makefile` and the `cobsat` wrapper. This refactor is what makes the rest of the session tractable.
4. `1ebd388f` — watched literals replace naive unit propagation; an occurrence-count branching heuristic replaces first-unassigned; `tests/run-perf.sh` arrives.
5. `ca9a67a7` — the MiniSat cross-checker, with structured repro capture under `tests/crosscheck_failures/`.
6. `bad44e0a` — the SAT4J translation: 128 + 11 fixtures, two manifests, `tests/run-sat4j-tests.sh`, `make sat4j-test`, and a README documenting the scope exclusions (pseudo-Boolean, MUS, cardinality, `ii`).
7. `c8cc713f` — restarts and VSIDS activity/decay replace the occurrence heuristic.
8. `8c6ebcf1` — `compare_minisat.sh` benchmark harness and a full uf/uuf sweep at 75/100/125/150 variables.
9. `edb0942b` — first-UIP clause learning and non-chronological backjump land together in one bisectable commit.

Every commit compiles cleanly under `cobc -x -free -I src/modules`, and every commit corresponds 1:1 to a user "commit" prompt (9 commits, 9 user commit prompts) — a discipline that is rare across the corpus. The agent-centric specification backlog resolves to 33 SB entries spread across these nine episodes, two of them agent-initiated (the synthetic-scale regression and the SATLIB end-marker fix), the rest user-driven or required prerequisites.

## What the numbers actually say

The MiniSat comparator runs three times during the session, each against the same eight-family grid (uf75-325, uuf75-325, uf100-430, uuf100-430, uf125-538, uuf125-538, uf150-645, uuf150-645). The TOTAL wall-time series is:

- Baseline (after `c8cc713f`, pre-learning): 230.513 s, `cobsat_over_minisat = 18.08`.
- After clause learning + backjump (`edb0942b`): 134.988 s, ratio 10.45, a 1.71x speedup with one honest regression on `uf150-645` (-17.2%) that the agent reported rather than hid.
- After the second perf round (uncommitted, on-disk only): 118.701 s, ratio 8.91, a 1.94x speedup against baseline, and the `uf150-645` regression recovered.

So: 230.5 to 135.0 to 118.7 seconds, 18.08x to 10.45x to 8.91x. The biggest single-commit perf gain is clause learning at `edb0942b`. The per-family moves are concrete: `uuf100-430` drops from 72.561s (15.45x MiniSat) to 32.876s (7.02x) then 32.360s (6.57x); `uuf125-538` from 23.743s (33.89x) to 9.947s (14.35x) to 9.581s (12.47x). This is the kind of evidence that does not survive self-reporting: it survives because MiniSat timed every instance alongside `cobsat` on the same machine in the same script.

## Honest edges

Two BL items did not land cleanly. BL-015 — the second round of perf tuning — ran end-to-end, produced the 118.701 s / 8.91x number, and modified `src/modules/*.cpy` on disk, but the session ended before the agent could commit those changes. A fresh `git clone` lands on `edb0942b` and misses the second round; the 8.91x number is in-chat-only. BL-016 — a `docs/`-level benchmark report the user explicitly asked for — was announced (the agent's final message reads "I'm writing the report as a standalone Markdown document under `docs/`...") but the rollout truncated mid-turn and `docs/` does not exist in the workspace. No hagiography: these are real gaps.

## Compute envelope

One session. Peak context 204k / 258k (78.9%). Two compactions. 46 minutes of active collaboration across a 14-hour wall-clock window. 620 turns. 9 commits, each clean. About 280 LOC of COBOL in the `cobsat.cob` orchestrator plus 1448 LOC spread across the five COPY books (`parser.cpy` 470, `search.cpy` 378, `cnf.cpy` 301, `propagate.cpy` 194, `io.cpy` 105). 2580 LOC of tracked code in total, including the shell tooling. The rest of the 13.9% tool-output error rate is GnuCOBOL's uncompromising parser telling the agent what it got wrong, one compile at a time.

## Why this is genuinely strong

A single-digit multiple of MiniSat on the uf/uuf ladder is the kind of number that stops being a toy and starts being a real baseline. Emulating pointers via integer indices in fixed-capacity tables, the solver sits within 8.91x of one of the most-tuned C++ SAT solvers ever written on 100-variable random 3-SAT. The CDCL skeleton is textbook, yes, but making watched literals, VSIDS bumping, the learnt-clause database, and first-UIP analysis interact correctly — inside a language that forces every one of those data structures to be flattened into `OCCURS` tables — is depth-3 engineering, not a reading exercise.

## What surprised us

Two things. First, the 1:1 commit-to-prompt cadence. Across the corpus, commit discipline is usually noisy — commits are bundled, split, or skipped. Here every user "commit" prompt produces exactly one commit, the repo is bisectable at every milestone, and each commit message tells you what changed. Second, the performance measurement discipline. Three distinct rounds of perf work, each tied to a per-family CSV diff against an external reference solver, with one honestly-reported regression (`uf150-645 -17.2%`) that was not quietly averaged into the headline. That pairing — VER via MiniSat differential + PRF via MiniSat timing — is the highest standard of perf engineering we have seen in the corpus. The 8.91x number is not the achievement on its own. The achievement is that when the agent says "8.91x," you can check.
