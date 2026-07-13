# STORY — `SATCobol-cc`

## The other half of a controlled experiment

This is the Claude Code replica of the SAT solver, run against the exact same
REPLAY_PROMPTS pack that drove its Codex sibling. Same opening prompt at
`2026-04-15T12:20:04Z`: DIMACS parser in free-format COBOL, `--parse` mode,
edge-case unit tests. Same step ladder from there — `--check-model`, uf75
parser validation, baseline DPLL, 200-instance soundness sweep, refactor,
watched literals, MiniSat crosscheck, extended benchmark, SAT4J acceptance
suite, phase/VSIDS/JW/Luby, full MiniSat comparison, advanced features.
Nine commits on the default branch, matching the sibling's nine. Then the
sessions diverge — not in what was asked, but in what the agent shipped and
how it organised the code to ship it.

## The domain — familiar, but seen twice

Everything from the domain brief carries over unchanged: DIMACS CNF input
with `c`/`%` comments and a `p cnf V C` header, SATLIB `uf*`/`uuf*` archives
as the benchmark corpus, SAT4J's JUnit suite as the external oracle, MiniSat
as the performance reference. The interesting twist is having two agents
solve it from the same instruction stream. What varies is agent-decided: the
internal architecture of the COBOL source, the order in which compatibility
patches land, the shape of the Makefile, the finishing move. Divergence
under identical scope is the research signal — this project exists to
produce that signal.

## Chronology — one rollout, 316 turns, and a finish that didn't quite finish

A single Claude Code session (`9f10dfb5-...`, `claude-opus-4-6`,
2.1.109), opened 2026-04-15T12:20 and running to 2026-04-16T13:48. 1 122
raw events, 316 per-turn rows in the extract. Active collaboration time
1 h 14 m of a 25 h wall span — the user dipped in and out while compilation,
benchmarks, and SAT4J runs churned. 21 distinct human prompts (13 BL, 42 SB,
17 UI entries, 19 PL entries) plus four "commit" one-liners and one
"retry/continue" meta. Commit cadence: nine clean milestones from
`049f4b5` (parser) to `c3b2a7c` (phase saving + VSIDS-lite + JW + Luby).

Then the coda. Commit `c3b2a7c` landed at 10:03; the 2 400-instance
MiniSat comparison finished at 13:16 with a 1.9× ratio; the user asked for
"advanced features" at 13:25; the agent wrote a first-UIP CDCL core
touching `propagate.cpy`, `search.cpy`, `cnf.cpy`, `cnf-data.cpy`,
`propagate-data.cpy`; claimed "33/33 unit tests pass + smokes correct" at
13:43:46; launched two parallel background benchmark processes at 13:48:06;
the log ends four seconds later at 13:48:13. Three EP-POST backlog items
(SB-040, SB-041, SB-042) sit on disk, uncommitted, with no attested
post-CDCL numbers.

## Delivered — `cobsat` and a twelve-copybook spine

The binary is `cobsat`, built at repo root by an 18-line Makefile (`cobc
-x -Wall -O2 -I src/copy`). No wrapper script, no `sat4j-test` / `perf`
/ `compare-minisat` phony targets — test shells are invoked directly. The
source is a 83-line dispatcher (`src/cobsat.cob`) plus twelve copybooks
under `src/copy/`, each logical module split into a data copybook
(`<mod>-data.cpy`, WORKING-STORAGE) and a logic copybook (`<mod>.cpy`,
PROCEDURE paragraphs): parser, cnf, propagate, search — four pairs — plus
I/O further fragmented across `io-files.cpy` (FILE-CONTROL), `io-fd.cpy`
(FD entries), `io-data.cpy` (scalars), and `io.cpy` (paragraphs). Twelve
copybooks where the Codex sibling used five. That finer decomposition was
not requested; the refactor prompt simply said "parser, cnf, propagate,
search, io". The data/logic split, and the four-way I/O split, are
agent-initiated structure.

Validation rides on two external oracles. `scripts/crosscheck_minisat.sh`
(180 LOC) runs `./cobsat --solve` and MiniSat side by side over 2 400
SATLIB instances (uf/uuf × {100, 125, 150}) and captures structured repro
bundles on mismatch — 2 400/2 400 verdicts agreed, final cobsat/minisat
ratio 1.9× at commit `c3b2a7c`. `tests/run_sat4j_tests.sh` drives 113
fixtures translated from SAT4J's `AbstractM2Test.java`,
`TestsFonctionnels.java`, and `BugSAT175.java` against a committed
`expected.tbl` verdict table, with a 30-second per-instance timeout. The
headline here is that SAT4J was actually *executed* end-to-end: 94/113
pass at `57de05d`, 111/113 pass at `c3b2a7c` after JW seeding + phase
saving + VSIDS-lite + Luby restarts. The Codex sibling translated the
fixtures but never attested an end-to-end run.

## Validation and compatibility glue

Two separate parser-compatibility patches landed, one more than the sibling.
The first was the SATLIB `%` end-of-data trailer — SATLIB files terminate
with `%\n0\n`, and the initial parser read that trailing `0` as a stray
clause, inflating counts. Fix committed at `88e8e99`. The second was the
SAT4J missing-trailing-`0`: SAT4J's Java reader is lenient, so several
`ii`-family fixtures omit the terminator; MiniSat also rejects them. The
agent diagnosed the asymmetry from the live session output and looosened
the parser in `57de05d`. The Codex sibling only ever shipped the first
patch.

The 1.9× MiniSat ratio reads worse than the sibling's 8.91×, but that
comparison is asymmetric. The 1.9× number was measured *before* CDCL, on
the two-watched-literals + VSIDS-lite + phase-saving + Luby build at
`c3b2a7c`. The sibling's 8.91× was measured *after* CDCL committed at
`edb0942b` plus a second perf round. The 4.7× gap between the two numbers
is the lost CDCL commit, not a quality regression — the CDCL code exists
on disk in this project, it simply never got attested, benchmarked, or
persisted.

## Compute and context

Well below the model's context window; no compaction events; the single
rollout held every turn. Tool-use distribution: 177 Bash, 58 Write, 51
Edit, 24 Read, 1 ToolSearch — Bash-heavy because benchmarks and test runs
dominate the traffic. 30 `make` invocations, 12 `perf.sh`, 13
`run_sat4j_tests.sh`, 13 `crosscheck_minisat.sh`, 3 direct `cobc`,
26 git-status-or-log checks. Tool-output error rate 1.7 %
(2 errors / 115 outputs). Zero bug-report or redirect prompts from the
user — the session ran forward, not backward. Rack-rate compute is roughly
$20 for the session.

## Why this replication matters

The two-agent coverage gap for the SAT domain is now closed. The interesting
finding is where the agents diverged under identical scope. Backlog items
(BL-001 through BL-013) are byte-identical between siblings. Prompt ledger
entries match. Capabilities at the final commit are comparable. What the
CC agent chose differently, without prompting, is structural: a finer
copybook decomposition, a data/logic split per module, a four-way I/O split,
an *additional* parser lenience patch for SAT4J, and an end-to-end SAT4J
execution (not merely a translation). What the Codex agent chose differently
is different structural: a 5-copybook layout, a wrapper script, phony Make
targets, and — critically — landing the CDCL commit before session exhaustion.

## What the replay actually transferred

Replay-prompt portability, measured on this pair, is a scoped phenomenon.
*Scope* transfers: the same 13 BLs were produced, the same 19 PLs fired,
the same SATLIB and SAT4J corpora got wired in at the same points.
*Architecture* does not: each agent picked its own copybook granularity,
its own parser-patch strategy, its own benchmark ordering, its own finish
move. Across the two projects the same contract produced two genuinely
different COBOL codebases that happen to pass broadly the same tests. That
divergence — not the overlap — is why running the same prompts twice was
worth the compute.
