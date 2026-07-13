# Highlights — impressive technical moments across the COBOL corpus

A curated reading of the 27 sessions across 12 projects, focused on specific
engineering moments rather than project-level summaries. Each entry is anchored
to a concrete artefact — a file, a session event, a commit, or a benchmark row —
so the claim is checkable. Grouped by what they exemplify.

---

## 1. Debugging that produced real insight

### 1.1 `cobol-compiler-cc` — "It's a binutils bug, not a `-O2` bug"

A `cobc -x -O2` invocation hangs on macOS ARM64. The user's working hypothesis
was a `-free`-format issue; the agent's first guess was a GnuCOBOL code-gen
bug. Session `de76ffeb` ran an optimisation-level × strip-variant matrix and
landed on the actual root cause: Homebrew's GNU `binutils` package installs a
`strip` that precedes `/usr/bin/strip` on `PATH`, and GnuCOBOL's post-link
`strip -x` step then corrupts Mach-O ARM64 binaries. The fix was a one-line
`PATH` reorder (or `brew unlink binutils`) and `test_o2_apple` printed
`HELLO` at exit 0. The noteworthy part is the reasoning pattern: the agent
contradicted the user's stated hypothesis *based on evidence*, not on priors.

### 1.2 `cobol-compiler-codex` — the 0.03× chess miscompile

Codex was cheerfully reporting that `minicobc`-compiled chess ran **33 times
faster** than the GnuCOBOL build — a result that should have raised an
eyebrow. User prompt `PL-044` did: *"it's very strange to beat the runtime of
GnuCOBOL… are you sure? do you check functional correctness?"* The agent
wrote a differential `QUIESCE` / `ALPHABETA` equivalence harness that bypassed
the top-level `SEARCH` wrapper, reproduced the divergence, and isolated the
bug to one statement in `EVAL`: `MOVE WPC(F-IX - 1) TO FRIEND-L` was lowered
as the scalar expression `FRIEND-L = F-IX - 1` instead of loading the indexed
array element. The speedup was a correctness failure. The agent added
`examples/generic/move_index_expr.cob` as a permanent regression and left
`MINICOBC_OPT=1` flagged as unsafe for chess in the README rather than
silently widening the optimiser.

### 1.3 `cobol-compress-codex` — the fuzz suite that caught its own author

`trust_fuzz.py` enumerates ten CPC-format mutator classes and 24 garbage
files, each run under a 2-second subprocess timeout. The contract is strict:
no crash, no hang, no signal termination. On first run the `reclen_zero`
mutator — which sets the container's `record_len` field to zero — crashed the
COBOL binary with SIGFPE. The agent's own test machinery had just caught a
divide-by-zero in the agent's own code: `record_count = file_size / record_len`
with no guard on `record_len = 0`. Fix landed in the same session,
suite re-greened, and two sibling bugs (RLESP pending-space corruption, gap
synthetic-field safety) fell out of the same investigation. Falsification
beats rubric grading.

### 1.4 `chess-cobol-cc` — the time-forfeit that proved the match harness worked

An aggressive `time/movestogo` formula change caused **seven forfeits in a
20-game match** (`phase5_vs1500.pgn` = 3.5/20). The agent restored the
safety buffer and added a soft-time check at 4× the last iteration's elapsed
time. The next 20-game match scored 13.5/20. The delta from 3.5 to 13.5 out
of 20 — and the forfeits-to-zero recovery — is exactly the signal-to-noise
the PGN match harness was built to catch, and the agent encoded the lesson
in a persistent memory note (`feedback_time_management.md`) so later
experiments wouldn't re-break it.

### 1.5 `COBOL-chess` — the 4-byte fix that was worth 450 Elo

The UCI input buffer was declared `PIC X(512)`. Long `position startpos moves
…` strings truncated mid-move, cutechess saw illegal moves, and the engine
lost on forfeit. Phase 14 widened the buffer to `PIC X(4096)` (feature F-170,
`src/main.cob:25`). The backlog records the Elo effect: **~675 → ~1129**.
One line, +450 Elo. The lesson is that protocol-layer bugs masquerade as
engine weakness — and the PGN oracle caught it only because games were
played at all.

---

## 2. COBOL-specific idioms that carry real engineering weight

### 2.1 `cobol-tictactoe` — eight winning triples as a literal with `REDEFINES`

Tic-tac-toe (and therefore Game-of-15) has exactly 8 winning lines. The
shipped encoding is a single 24-character literal:

```
"159168249258267348357456"
```

with a `REDEFINES` overlaying eight (T1, T2, T3) triples. No table to
maintain, no generator to run. Reading `OWNER(T1)`, `OWNER(T2)`, `OWNER(T3)`
across the eight mapped positions *is* the check. This is COBOL used the way
COBOL is meant to be used: data description doing work that other languages
would hand to a loop.

### 2.2 `COBOL-chess` — `LOCAL-STORAGE SECTION` for recursion-safe perft

GnuCOBOL's `PROGRAM-ID … IS RECURSIVE` enables recursion, but `WORKING-STORAGE`
stays static across activations. Phase 7 of the chess engine declares per-frame
move lists in `LOCAL-STORAGE SECTION` so each recursive perft activation owns
its own mutable state. The entire perft path (startpos + Kiwipete + EP + promo
at depth 5 = 4 865 609 nodes) works because of that one section choice. The
Zobrist tables in `copybooks/hash.cpy` go the other way — they live in an
`EXTERNAL` singleton so separately-compiled programs share state rather than
re-initialising the LCG on every `CALL`.

### 2.3 `cobol-tictactoe` — base-3 transposition table indexed by positional encoding

Every board position has nine cells, each in one of three states (empty / P1 /
P2). The position encodes uniquely into `sum(OWNER(i) * 3^(i-1))` ∈ [0, 19 683).
`MEMO-TABLE PIC X OCCURS 19683` is the entire transposition table, and the
solver fills it exactly once. This is the kind of data-structure match a
seasoned game-tree engineer would reach for, expressed in GnuCOBOL without
recourse to pointers or hashing.

### 2.4 `SATCobol-codex` — CDCL skeleton on integer-indexed OCCURS tables

COBOL has no pointers, no `malloc`, no `realloc`. A modern CDCL solver needs
a clause database, watched-literal lists, a propagation trail, an assignment
stack, and an implication graph — all normally pointer-chased. The solver
flattens every one of them into `OCCURS` tables indexed by `COMP-5` integers.
Every "pointer" is an index; every dynamic resize is a fixed-capacity ceiling.
That the result sits within 8.91× of MiniSat on uf100-430 says the flattening
was not a performance disaster.

### 2.5 `cobol-compiler-cc` — RECURSIVE programs via the "Approach E" frame-pointer

Compiling COBOL's `RECURSIVE` qualifier is the hardest part of writing a COBOL
compiler, because the standard requires per-activation copies of
`WORKING-STORAGE`. The `-cc` compiler's "Approach E" code-gen solves it by
threading a frame-pointer argument through generated C functions and
allocating activation records on the C stack. The proof it works: the
compiler's own `cobolcc`-compiled output of a 3 854-LOC COBOL alpha-beta
chess engine actually plays 20 full games at 10 s + 0.5 s time controls.

---

## 3. One-shot, near-one-shot deliveries

### 3.1 `cobol-jb` — three consecutive features that compiled first try

The first session hit exactly one compile error (undefined `WS-FILE-STATUS`
fields + a misplaced PROCEDURE DIVISION header) and fixed it with a single
edit. BL-002 (social-contribution deductions), BL-003 (input validation +
reject file), and BL-004 (verification grid) all compiled first try.
Eleven user prompts total, five of them coding, four features delivered — a
1:1 coding-prompt-to-feature ratio is the leanest in the corpus.

### 3.2 `cobol-compress-codex` — three spec-sized prompts, three MVPs, zero clarifications

MVP0 (container + NONE codec), MVP1 (RLESP + AUTO + CRC32), TRUST (70-assertion
suite): three user prompts of roughly 2000, 800, and 50 words. No agent
clarification questions, no scope churn, three green milestones. The spec
was load-bearing; the agent was disciplined enough to not invent work.

### 3.3 `game15-cobol-codex` — three self-detected bugs, five-minute fixes each

Three bugs surfaced during validation: a `FILLED-TARGET PIC 99` underflow in
the retrograde loop, a stale `OWNER` array leaking from solve into print, and
an avoid-annotation stealing a shallower prefix. Each was diagnosed from
wrong output, fixed, and the binary rebuilt in under five minutes. None
reached the user — the bugs came and went inside the same turn.

---

## 4. Verification feats: falsifiable validation, not rubric grading

### 4.1 `cobol-compress-codex` — SHA-256-anchored determinism proof

Determinism is not argued, it is demonstrated. Four witness cases are
compressed **five times each**, and the `.cpc` bytes, `info` output, and
restored bytes must all match by SHA-256 across runs. A randomized round-trip
layer adds 48 seeded cases varying record length, field count, gaps, types X
and 9, codec overrides, and content modes — every case compressed twice for
determinism, decompressed, and CRC32-verified. The trust claim ships with
explicit semantics of what a passing run does and does not prove.

### 4.2 `SATCobol-codex` — three perf rounds, each with an external oracle

The MiniSat comparator runs three times, each against the same eight-family
grid. Baseline after `c8cc713f`: 230.513 s TOTAL, ratio 18.08×. After
clause learning + backjump at `edb0942b`: 134.988 s, ratio 10.45, with an
**honestly-reported −17.2 % regression on uf150-645** that was not averaged
into the headline. Second perf round (uncommitted): 118.701 s, ratio 8.91.
The achievement is not the 8.91× number; it is that when the agent says
"8.91×", MiniSat timed every instance alongside `cobsat` on the same machine
in the same script and you can re-run it.

### 4.3 `SATCobol-cc` — SAT4J executed end-to-end, not translated-and-shelved

The Codex sibling translated SAT4J's JUnit suite into 128 DIMACS fixtures but
never attested an end-to-end execution. The Claude-Code replica **actually
ran** `tests/run_sat4j_tests.sh` against the committed `expected.tbl` verdict
table with a 30-second per-instance timeout and attested **94/113 pass at
`57de05d` → 111/113 pass at `c3b2a7c`** after JW seeding, phase saving,
VSIDS-lite, and Luby restarts. Two parser-lenience patches landed (the SATLIB
`%` trailer + the SAT4J missing-trailing-`0`) versus the sibling's one —
because only the CC run actually fed SAT4J fixtures into its parser.

### 4.4 `cobol-jb` — the agent grading itself, honestly

The user handed the agent the case-study spec's 27-criterion verification
grid and asked it to apply the grid to its own work. The agent recompiled to
confirm exit 0, ran `wc -l` on its own source, ran `git log --oneline` to
attribute a missing README update to the specific BL-003 commit that skipped
it, and wrote `VERIFICATION_REPORT.md` scoring 25/27 with **one PARTIAL
(README drift) and one FAIL (705 LOC vs 300 target)** called out honestly
rather than hidden.

---

## 5. Performance engineering with measured evidence

### 5.1 `chess-cobol-cc` — the fourteen-cycle improvement ladder

Across 17 days, the chess engine ran roughly fourteen INCR → TEST → RETR
cycles against a fresh 20-game PGN match, producing a documented Elo ladder:
**~1517 → ~1608 → ~1627 → ~1647**. Seven experiments were rolled back after
match regression: reverse-futility pruning, qsearch check extensions, v3
futility pruning, the aggressive time formula, tapered king evaluation,
horizon check extensions, and the endgame king phase-switch. Each revert was
encoded in a persistent memory note (`feedback_overhead_sensitivity.md`,
`feedback_time_management.md`) so later experiments *started from* the
lessons. That constraint then produced v4: PV-move ordering plus persistent
killer and history tables — changes the agent deliberately chose *because
they cost nothing per node*. The last change of the ladder was shaped by the
memory of the first six reverts.

### 5.2 `SATCobol-codex` — clause learning was worth 1.71× on its own

Commit `edb0942b` is one bisectable change: first-UIP learning + non-chronological
backjump. The TOTAL time fell from 230.513 s to 134.988 s at that single
commit — a 1.71× speedup against baseline, concentrated in one algorithmic
step. The per-family moves are equally clean: `uuf100-430` 72.561 s → 32.876 s
(ratio 15.45 → 7.02), `uuf125-538` 23.743 s → 9.947 s (ratio 33.89 → 14.35).
Every number was logged automatically by the comparator script into a CSV
diff.

---

## 6. Architectural choices with real consequences

### 6.1 `game15-cobol-codex` — the 986 409-byte factorial-rank bitmap

Symmetry deduplication needs a way to recognise that two move sequences
belong to the same D4 orbit. The Claude-Code sibling hashed the canonical
form into a set. Codex instead computed a falling-factorial rank of the
lexicographic-minimum permutation prefix, added a per-length offset, and
declared `SEEN-CANONICAL PIC X OCCURS 986409` — a **986 kB bitmap that covers
9! plus all shorter-prefix offsets**. A custom perfect hash for
variable-length permutation prefixes, built from scratch in COBOL, sized to
the whole address space rather than to reachability. Eager allocation against
a known bound rather than lazy hashing against unknown load.

### 6.2 `game15-cobol-codex` — bottom-up retrograde over 19 683 base-3 states

Where the Claude-Code sibling solved the game with lazy top-down minimax and
a memoisation table filled on visit, Codex solved it **eager bottom-up**:
outer loop `FILLED-TARGET` from 9 down to 0, validity filter pruning
impossible configurations, then minimax folded into the retrograde fill so
every parent's children are guaranteed solved before evaluation. The printer
is a pure query over the filled `STATE-OUTCOME(19683)` table. Same inputs,
same oracles, opposite control-flow discipline.

### 6.3 `cobol-doom` — DDA replacing step-march mid-session

The Step-1 raycaster was a naive per-pixel step-march (SB-1-11). Step 3
replaced it with a column-based DDA grid traversal (SB-031 / S3-02), added a
z-buffer for sprite sorting, doubled vertical resolution with Unicode
half-blocks, and introduced a 1 MB output buffer with minimised ANSI state
changes. The target frame budget moved from "works" to "16 ms per frame".
The agent chose the replacement itself; the user asked for better speed,
not for DDA.

### 6.4 `COBOL-pygame` — the 17-function FFI contract that actually holds

The `cpg_*` shim is a deliberate minimum: `cpg_init`, `cpg_quit`,
`cpg_create_window`, `cpg_set_draw_color`, `cpg_draw_line`, `cpg_fill_rect`,
`cpg_poll_event`, `cpg_delay`, `cpg_ticks`, `cpg_load_bmp`, `cpg_render_copy`
and their peers — seventeen entries. `USING BY VALUE` / `BY REFERENCE`
discipline throughout; `void**` opaque-handle convention so that
`USAGE POINTER` cells can hold SDL2 `SDL_Window*` / `SDL_Renderer*` /
`SDL_Texture*`; the tagged `SDL_Event` union flattened into a fixed
`CPG_Event` POD (eight `int32_t` fields) so COBOL's fixed-record model can
receive it; every string marshalled with a `(const char*, int len)` pair
because COBOL has no null terminator convention. The surface is small
because anything bigger would have exposed an ABI corner that COBOL cannot
cross.

---

## 7. Cross-agent signals — what the replica projects reveal

### 7.1 Same Game-of-15 prompts, two architectures

The `cobol-tictactoe` / `game15-cobol-codex` pair was built from
**byte-identical prompts** (the sibling's `REPLAY_PROMPTS.md` replayed
verbatim). Same oracles (255 168 / 31 896 games), same five-file set. The
implementations differ by +40 % LOC (2 822 vs 2 020), by data structure
(factorial-rank bitmap vs hash set), by solver discipline (eager retrograde
vs lazy memoisation), by win-check encoding (eight explicit IFs vs
magic-triple string with REDEFINES), and by 0.15-variant rendering (lookup
table vs inlined prefix). "Same prompt implies same implementation" is
empirically false.

### 7.2 Same SAT prompts, different finishes

The `SATCobol-codex` / `SATCobol-cc` pair ran the same replay pack on
different context windows. Codex finished the CDCL commit (`edb0942b`) before
session exhaustion and attested 8.91× MiniSat after a second perf round.
Claude Code did not attest the CDCL commit — the session truncated four
seconds after launching the post-CDCL benchmark, leaving the pre-CDCL 1.9×
MiniSat ratio as the attested number and the CDCL code on disk uncommitted.
The 4.7× nominal gap between the siblings is a checkpointing difference, not
a quality regression.

### 7.3 Same compiler, one compaction vs thirty

Both `cobol-compiler-cc` and `cobol-compiler-codex` attempt essentially the
same thing — a COBOL compiler in COBOL that compiles DOOM and a chess engine.
The -cc sibling ran on Opus's 1 M context window and compacted **three**
times. The -codex sibling ran on a 258 k Codex window and compacted **thirty**
times. Same project, same scope, ten-fold difference in how hard the context
had to work. The output-token density tells the same story in a second axis:
**~99 tokens per COBOL LOC (Claude Code) vs ~201 tokens per LOC (Codex)**.
Harder harness, more scaffolding.

---

## 8. Quick list of things that hold up on a second read

- The **magic-square literal** encoding the eight winning lines in
  `cobol-tictactoe` — data doing loop-level work.
- The **SHA-256 determinism proof** in `cobol-compress-codex` — five runs,
  byte-identical output, external oracle.
- The **1:1 commit-to-user-prompt cadence** in `SATCobol-codex` — nine
  commits from nine "commit" user prompts, each bisectable.
- The **agent reading its own Elo-match PGNs** in `chess-cobol-cc` to
  decide which experiments to revert — including the one where it
  changed course from "more pruning" to "zero per-node cost" and
  produced the biggest Elo jump of the run.
- The **self-caught miscompile** in `cobol-compiler-codex` after a single
  user redirect — the 0.03× "speedup" that wasn't.
- The **978 k / 1 M context peak** in `cobol-compiler-cc`: the only
  project in the corpus where the 1 M Opus window was not a luxury but the
  enabling condition.
- The **`COBOL-pygame` FFI contract** that keeps COBOL in the driver's seat
  across a SDL2 boundary with no null terminators and no native pointers.
- The **paired Game-of-15** projects: the cleanest empirical falsification
  of "identical prompts produce identical implementations" this corpus
  provides.

---

_Curated from `output/backlogs/<project>/STORY.md`,
`output/backlogs/<project>/KEY_FEATURES.md`, `output/backlogs/<project>/SPECIFICATION_BACKLOG.md`,
`output/assessments/<project>.md`, and the session-level `output/context/*.json`
trajectories. Every claim is anchored to at least one of those files._
