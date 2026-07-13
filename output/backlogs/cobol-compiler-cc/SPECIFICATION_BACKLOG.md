# SPECIFICATION_BACKLOG — cobol-compiler-cc

**Purpose.** Agent-centric, step-wise view of what the agent (Claude Code, model `claude-opus-4-6`, CLI 2.1.87 / 2.1.92) actually implemented across the three `~/.claude/projects/…/*.jsonl` sessions that built `/Users/mathieuacher/SANDBOX/cobol-compiler-cc`. This is complementary to the user-driven feature backlog in `README.md` (this dir).

**Step segmentation method.** Priority 1 — **git commits** captured from the session logs (each commit printed by the agent via `git log` / `git commit` surfaces a stable checkpoint; 60+ commits observed). Priority 2 — session episodes between user prompts for non-committed improvements. The main session is 625f1b9f (10,199 extracted turn events, 2026-03-29 → 2026-04-10); session de76ffeb is a short build-flag follow-up; 18eb3ca2 is a 3-event noop.

**Limitations.** (i) The raw session transcript is ~230 MB; analysis relied on the per-turn compact extract (`output/turns/…`) plus targeted reads of the raw JSONL. (ii) I did not run builds/tests here; "validation" evidence is quoted from the agent's own reported `cobc`/`gcc`/`./binary` outputs in the session. (iii) The 2-hour full game15 interpreter run was cut by timeout (aborted); the compiler path later made full runs feasible. (iv) Commit hashes reference the project repo (read-only for this meta-analysis).

**Legend.**
- Provenance: **User-driven** (traces to a UI/PL/BL), **Agent-initiated** (no direct UI, emerged from agent's internal loop), **Required prerequisite** (unblocks a user request).
- Evidence pointers: `[T:…]` = session-log turn id/line; `[G:…]` = git commit hash (as printed in session); `[R:…]` = repo file; `[L:…]` = command output quoted in-session.

## Mapping summary (SB → BL / UI / PL)

| BL | User-driven SBs | Notes |
|---|---|---|
| BL-001 Self-hosted COBOL interpreter + test suite | SB-001 → SB-005 | PL-ROOT + PL-001 "git commit + README" |
| BL-002 Compile Game-of-15 repo (game15, game015) via interpreter | SB-004, SB-005 | PL-002 (GitHub repo reference) |
| BL-003 Pivot to COBOL-to-C compiler (cobolcc) | SB-006 → SB-010 | PL-003 "interpreter too slow" |
| BL-004 Extend cobolcc to compile COBOL-DOOM | SB-011 → SB-013 | PL-004 (DOOM repo) + PL-005/PL-006 (slowness/keys) |
| BL-005 Compile cobochess (11 files, 3,854 LOC) | SB-014 → SB-030 | PL-007 + long "let's adress remaining errors" loop (PL-010..PL-025) |
| BL-006 Document compilation status / README updates | SB-005, SB-017, SB-031 | PL-008 (README request) + PL-029 |
| BL-007 Performance benchmark (GnuCOBOL vs cobolcc) | SB-022, SB-023 | PL-026 "design a performance benchmark" |
| BL-008 Chess tournament (cutechess-cli) | SB-028, SB-029, SB-030 | PL-027 "organize a tournament" + PL-028 "large time budget" |
| BL-009 Clarify build-flag claims (`-free`, `-O2`) | SB-031 | short session de76ffeb / PL-030 |

---

## Step-wise SB items

### SB-001 — Bootstrap project skeleton and decide on interpreter-first design
- **Step label:** INFERRED step 0 (pre-commit, session start 2026-03-29T15:55)
- **Category:** Capability / Planning
- **Provenance:** User-driven (PL-ROOT, UI-001).
- **Mapping:** BL-001.
- **Specification statement:** On the empty `cobol-compiler-cc` directory, the agent inspected the environment (`cobc --version`), chose an interpreter-first strategy, and authored `cobolint.cob` (COBOL source lexer/preprocessor, parser, symbol table, executor with IF/PERFORM/COMPUTE etc.), plus 9 test COBOL programs under `tests/`.
- **Evidence:** `[T:625f1b9f:i=0]` PL-ROOT; `[T:625f1b9f:i=3]` `cobc --version` call; `[R:/Users/mathieuacher/SANDBOX/cobol-compiler-cc/cobolint.cob]` 4,462 lines; `[R:/Users/mathieuacher/SANDBOX/cobol-compiler-cc/tests/test1-hello.cob..test9-game15-8.cob]`.
- **Validation:** see SB-002.
- **Scope notes:** No commit was created for days — the agent worked against the file system until the user asked for a commit (PL-001). The README the agent initially wrote is the pre-compiler version (later heavily edited).

### SB-002 — Interpreter correctness on 9 test programs + game15 subsets
- **Step label:** INFERRED step 1 (2026-03-29 → 2026-03-31; ends before commit `0eae806`)
- **Category:** Test/Validation
- **Provenance:** User-driven (UI-001 acceptance: "run some (non-trivial) COBOL programs").
- **Mapping:** BL-001.
- **Specification statement:** `cobolint` correctly interprets tests 1-9 (hello, factorial 1!-12!, FizzBuzz 1-30, Fibonacci 25 terms, prime sieve to 100, game6, game15-6, game15-7, game15-8 = 34,704 games), with outputs matching the GnuCOBOL reference.
- **Evidence:** `[T:625f1b9f:i=744]` final regression bash run output: "PLAYER 1 WINS: 12816 / PLAYER 2 WINS: 11520 / DRAWS: 10368 / TOTAL GAMES: 34704" — matches the reference table in `README` ([R:README.md:200-207]).
- **Validation:** End-to-end regression in-session produced expected numeric outputs for all 9 tests.
- **Scope notes:** Full 9-number `game15.cob` (255,168 paths) on the interpreter timed out at 2h17m (6,126 s CPU) — correctness was only proven up to 8 numbers [T:625f1b9f:i=740].

### SB-003 — Attempt full game15.cob via interpreter (timeout) — motivation for compiler pivot
- **Step label:** INFERRED step 1b (2026-03-30 → 2026-03-31)
- **Category:** Behavior / Test
- **Provenance:** User-driven (UI-002 "compile/run all COBOL programs available here github.com/acherm/agentic-cobol-game15tictactoe").
- **Mapping:** BL-002.
- **Specification statement:** The interpreter can execute `game15.cob` / `game015.cob` semantically, but at ~4000× overhead for DFS-heavy subscripted code the full run does not complete in 2 hours. Algorithm verified correct at every subset 4..8.
- **Evidence:** `[T:625f1b9f:i=672..683]` many "timeout 600s/1200s/60min/2h" task-notifications with status=failed exit code 124; `[T:625f1b9f:i=740]` final CPU accounting "6125.98s user … 2:17:13.61 total".
- **Scope notes:** Directly motivated PL-003 ("interpreter way too long… please write a COBOL-to-C compiler").

### SB-004 — Initial git commit (`0eae806`): interpreter + tests + first README
- **Step label:** `[G:commit 0eae806]` 2026-03-31T12:24 "COBOLINT: A COBOL interpreter written in COBOL"
- **Category:** Tooling / Documentation / Refactor-none
- **Provenance:** User-driven (PL-001: "stop the running… please git commit, including a README…").
- **Mapping:** BL-001, BL-006.
- **Specification statement:** First commit of the repo (root commit) stages `.gitignore`, `README.md`, `cobolint.cob`, `tests/test1..test9-game15-8.cob` — 12 files / 5,366 insertions.
- **Evidence:** `[T:625f1b9f:i=776]` "[master (root-commit) 0eae806] 12 files changed, 5366 insertions(+)".

### SB-005 — Interpreter documentation (initial README)
- **Step label:** part of `[G:commit 0eae806]`
- **Category:** Documentation
- **Provenance:** User-driven (PL-001 "documenting supported features of COBOL, architecture, feature of the interpreter, results").
- **Mapping:** BL-006.
- **Specification statement:** README documents supported COBOL features (Data Division / Procedure / Conditions / Subscripts), 9 test program descriptions, interpreter overhead tables, and build instructions.
- **Evidence:** `[R:/Users/mathieuacher/SANDBOX/cobol-compiler-cc/README.md:1-245]` (large portions later rewritten for cobolcc).

### SB-006 — New `cobolcc.cob` — COBOL-to-C compiler v1 (5 game tests pass)
- **Step label:** `[G:commit 7cc9b7d]` 2026-03-31T17:27 "Add COBOL-to-C compiler (cobolcc): all 5 game programs now compile and run"
- **Category:** Capability
- **Provenance:** User-driven (PL-003 "Please write a compiler (eg COBOL-to-C) instead. Reuse as much as possible your interpreter infrastructure").
- **Mapping:** BL-003.
- **Specification statement:** `cobolcc` reads a COBOL source, reuses the shared front-end (lexer/preprocessor/parser/symbol-table from `cobolint`), and emits a `.c` file that `gcc -O2 -lm` links to a native binary. Initial target: tests 1–9 produce identical output to the interpreter/GnuCOBOL reference.
- **Evidence:** `[T:625f1b9f:i=904]` commit output "3 files changed, 6049 insertions(+), 25 deletions(-) create mode 100644 cobolcc.cob".
- **Scope notes:** First commit of `cobolcc.cob`. The file will grow from ~6 KLOC to ~11 KLOC across all subsequent commits.

### SB-007 — `cobolcc` verified on game15 / game015 (0.01 s, 20× speedup vs GnuCOBOL)
- **Step label:** post-`[G:commit 7cc9b7d]`, before `1321b32` (2026-04-03 early morning)
- **Category:** Test/Validation
- **Provenance:** User-driven (UI "is the compiler working on agentic-cobol-game15tictactoe/? what's the performance compared to GNU Cobol?" — PL-009).
- **Mapping:** BL-002, BL-003.
- **Specification statement:** Compiler produces a working `game15` (all 255,168 paths) and `game015` that runs in ~0.01 s vs GnuCOBOL 0.20 s (20×).
- **Evidence:** `[R:README.md:224-233]` performance table; session follow-up reports 20× speedup (referenced in README, whose text traces back to the post-7cc9b7d run).

### SB-008 — Free-format support, COMP-5, CALL to external C — extend cobolcc for DOOM + chess
- **Step label:** `[G:commit 1321b32]` 2026-04-03T16:32 "Extend cobolcc: free-format, COMP-5, CALL to C, DOOM + chess engine support"
- **Category:** Capability
- **Provenance:** User-driven (PL-004 "consider github.com/acherm/agentic-cobol-doom … try to build it").
- **Mapping:** BL-004, BL-005 (seed).
- **Specification statement:** cobolcc adds: free-format detection (first-line-starts-with-letter), COMP-5 binary types (PIC S9(9) → int, PIC S9(18) → long long), CALL "func" USING BY VALUE/REFERENCE/RETURNING emitting C function calls with extern declarations, and `#include <math.h>` for FUNCTION SQRT. 1,224 LOC added to `cobolcc.cob`.
- **Evidence:** `[T:625f1b9f:i=2042]` commit "[master 1321b32] 1 file changed, 1224 insertions(+), 56 deletions(-)".

### SB-009 — COBOL-DOOM compiles and links end-to-end (1,363 LOC free-format)
- **Step label:** inside `[G:commit 1321b32]` (first milestone proved)
- **Category:** Capability / Test
- **Provenance:** User-driven (PL-004).
- **Mapping:** BL-004.
- **Specification statement:** `doom.cob` (1,363 lines, free format, 24 external C function calls, FUNCTION SQRT, EVALUATE WHEN OTHER, reference modification, 24×24 map via REDEFINES) transpiles to C and links with doom's C runtime to a runnable terminal binary.
- **Evidence:** `[R:README.md:283]` "**doom.cob** **1,363** **Free** … 24 external C function CALLs"; session log confirms via "how to run this compiled DOOM?" (UI-011) and follow-up perf complaints.
- **Scope notes:** Runtime performance and keyboard input (arrow keys) were reported as poor/broken (PL-005, PL-006); no further fix of DOOM was made in this session — the user moved on to chess.

### SB-010 — COPY path resolution, LINKAGE locals, parameter naming (start of chess)
- **Step label:** `[G:commit e643e3d]` 2026-04-04T03:46 "Fix COPY path resolution, LINKAGE locals, parameter naming for chess engine"
- **Category:** Capability / Behavior
- **Provenance:** User-driven (PL-007).
- **Mapping:** BL-005.
- **Specification statement:** `cobolcc` now resolves `COPY "copybooks/types.cpy"` relative to the source file with a fallback search, treats LINKAGE SECTION variables as function parameters (copy-in/copy-out), and sanitises COBOL parameter names for C (hyphens → underscores preserved only in names, not subtraction operators). 144 LOC / 10 del.
- **Evidence:** `[T:625f1b9f:i=2251]` commit output.

### SB-011 — Inline IF, PERFORM FOREVER, EXIT PARAGRAPH/PERFORM, FUNCTION MOD
- **Step label:** `[G:commit fef9782]` 2026-04-04T04:55 (+211 LOC)
- **Category:** Capability
- **Provenance:** Required prerequisite (chess engine uses these idioms; user prompt PL-010 "please adress all remaining errors").
- **Mapping:** BL-005.
- **Evidence:** `[T:625f1b9f:i=2392]`.

### SB-012 — FUNCTION handling, group-name macros, MOVE token spacing
- **Step label:** `[G:commit d505af4]` (+100)
- **Category:** Capability/Bugfix
- **Provenance:** Agent-initiated + Required prereq (discovered while fixing chess compilation errors).
- **Mapping:** BL-005.
- **Evidence:** `[T:625f1b9f:i=2489]`.

### SB-013 — EVALUATE TRUE / EVALUATE on strings / char switch / multi-target MOVE / FUNCTION in expressions
- **Step label:** `[G:commit d46c4a2]` (+197/-46)
- **Category:** Capability
- **Provenance:** Required prereq for chess (fen.cob EVALUATE).
- **Mapping:** BL-005.
- **Evidence:** `[T:625f1b9f:i=2594]`.

### SB-014 — CALL group passing, filter bad constant macros, extern void fix
- **Step label:** `[G:commit 1efb319]`
- **Category:** Bugfix
- **Provenance:** Agent-initiated during chess compile loop.
- **Mapping:** BL-005.
- **Evidence:** `[T:625f1b9f:i=2645]`.

### SB-015 — LINKAGE variables emitted as file-scope static (chess engine compilation)
- **Step label:** `[G:commit 740b7d7]` (−125 LOC, simplification)
- **Category:** Refactor / Behavior
- **Provenance:** Agent-initiated.
- **Mapping:** BL-005.
- **Evidence:** `[T:625f1b9f:i=2682]`. Later reworked by SB-024 into proper extern globals.

### SB-016 — Case-preserving strings, GOBACK/EXIT paragraph, extern declarations, dedup — compile of individual chess files
- **Step label:** commits ef00bab, e816dc0, 59bd673, 98ba3e9, 48bb34c, ac8b20e, b3c026e, d3d16e7, 5d05177, 8f03c07, 3dc6a83, e23b47e, 412ed0f, 2b1c634, 219915b, d2b1238, 510307c, 59359a5, 728acbe, 152fac3, 1b98f4b, a6e8155, a043a33, ab95355, ca6220f, 9f489a0, ac97b02, 9528b62, cfb79b3 (2026-04-04 → 2026-04-05 morning; 29 commits).
- **Category:** Bugfix + Capability (aggregated "fix-the-error" loop).
- **Provenance:** User-driven drive ("let's adress remaining errors" repeated ≥13 times — PL-010..PL-025) + Agent-initiated fixes inside each episode.
- **Mapping:** BL-005.
- **Specification statement:** Iteratively extends `cobolcc` to parse and translate the chess idioms found in uci.cob, eval.cob, movegen.cob, perft.cob, fen.cob, makemove.cob: inline-IF ending with GOBACK, FUNCTION ABS in COMPUTE, period-aware line joining, FUNCTION INTEGER-OF-DATE, 2D subscript comma-merge (COMPUTE + tokenizer), hyphen→underscore smart-splitting, RETURN_CODE register, cob_trim helper, multi-parameter PROCEDURE DIVISION USING, literal BY REFERENCE via `&(int){5}`, COMP-5 2D arrays, strcmp compound-OR conditions, 8/11 → 10/11 chess files compile.
- **Evidence:** 29 commit-lines in `[T:625f1b9f]` between i=2714 and i=4441; `[T:625f1b9f:i=4440]` "Fix strcmp for compound OR conditions: fen.cob now compiles".
- **Scope notes:** Interspersed with compaction (`/compact`) events and two auto-summaries at i=5266 and i=9474.

### SB-017 — README: comprehensive compilation status and feature documentation
- **Step label:** `[G:commit 52b5d90]` 2026-04-05T08:17 (+121/-6)
- **Category:** Documentation
- **Provenance:** User-driven (PL-029 "before further investigating errors, can you document somewhere what can be compiled so far").
- **Mapping:** BL-006.
- **Evidence:** `[T:625f1b9f:i=4457]`.

### SB-018 — Buffer resizing, symbol table 200 → 400 → 800 entries, strcmp scoping
- **Step label:** `[G:commit 57d5f3a]` / `583e40d`
- **Category:** Quality/Hardening
- **Provenance:** Agent-initiated (fixing "variable corruption" via table overflow).
- **Mapping:** BL-005.
- **Evidence:** `[T:625f1b9f:i=4623]` "symbol table 400→800: fixes search.cob variable corruption (162→35 errors)".

### SB-019 — LOW-VALUES/SPACES→GEN-INITIALIZE, paren handling in conditions, XCAL extern scan
- **Step label:** commits `4a2cbbd`, `fd60ea6`, `f9212b5` (2026-04-05T13:38..13:52)
- **Category:** Capability/Bugfix.
- **Provenance:** Required prereq + Agent-initiated.
- **Mapping:** BL-005.
- **Evidence:** `[T:625f1b9f:i=4836..i=4923]`.

### SB-020 — STRING FUNCTION TRIM, OCCURS string arrays 1D/2D, main.cob compiles (10/11 → 11/11 first compile pass)
- **Step label:** commits `9346303`, `22df96b`, `9f7440e`, `875c2fd` (2026-04-05T14:32..17:36)
- **Category:** Capability
- **Provenance:** Required prereq for chess linking.
- **Mapping:** BL-005.
- **Evidence:** `[T:625f1b9f:i=5225]` "Line buffers 256→512: main.cob now compiles! 10/11 at 0!".

### SB-021 — Multi-program COBOL file support — chess engine compiles + links + runs (first UCI)
- **Step label:** `[G:commit fb46bb7]` 2026-04-05T21:51 "Multi-program COBOL file support: chess engine now compiles, links, and runs" (+165/-39)
- **Category:** Capability
- **Provenance:** User-driven (PL-022 "fully linking is the next step") + Required prereq.
- **Mapping:** BL-005.
- **Specification statement:** `cobolcc` now handles a single `.cob` file that contains multiple PROGRAM-IDs (search.cob has SEARCH + ALPHABETA RECURSIVE + QUIESCE RECURSIVE), scoping symbol table per sub-program and managing `#define` conflicts.
- **Evidence:** `[T:625f1b9f:i=5991]`.

### SB-022 — EVALUATE TRUE condition translation; ACCEPT FROM ARGUMENT-NUMBER/VALUE
- **Step label:** `[G:commit e5dff13]`
- **Category:** Bugfix / Capability
- **Provenance:** User-driven (PL-023 "please fix this bug about the conditional translation"; UCI argv parsing).
- **Mapping:** BL-005.
- **Evidence:** `[T:625f1b9f:i=6145]`.

### SB-023 — `benchmark.sh` + empty-main fix (measure cobolcc vs GnuCOBOL)
- **Step label:** `[G:commit 16102a9]` "add benchmark script" (+339 LOC, new file); followed by `129f8c2` (whitespace-tolerant comparison)
- **Category:** Tooling / Test
- **Provenance:** User-driven (PL-026 "design a performance benchmark that would basically consist in building and running existing COBOL programs you already consider…").
- **Mapping:** BL-007.
- **Specification statement:** `benchmark.sh` compiles every test program twice (GnuCOBOL and cobolcc→gcc -O2), runs both with a timeout, diff-compares output, and records build+execution wallclock; produces a summary table used in `README.md#Performance`.
- **Evidence:** `[R:/Users/mathieuacher/SANDBOX/cobol-compiler-cc/benchmark.sh:1-332]`; `[T:625f1b9f:i=6221]`.

### SB-024 — LINKAGE scalar/string copy-in/out, group BY REFERENCE — clean cross-file sharing
- **Step label:** `[G:commit 5ac6763]` (+486 LOC) and `[G:commit 967f425]` "Clean LINKAGE variable sharing: extern/global for cross-file linking" (+57/-21)
- **Category:** Capability / Refactor
- **Provenance:** User-driven (PL "let's go for a clean solution").
- **Mapping:** BL-005, BL-008.
- **Evidence:** `[T:625f1b9f:i=6582, i=7319]`.

### SB-025 — CALL USING group detection; non-static only for groups passed in CALL
- **Step label:** `[G:commit 579bbc1]` (+58/-5)
- **Category:** Refactor
- **Provenance:** Agent-initiated (following SB-024's broader global-visibility decision).
- **Mapping:** BL-005.
- **Evidence:** `[T:625f1b9f:i=7432]`.

### SB-026 — RECURSIVE program support: stack-allocated WS local structs (PERFT works)
- **Step label:** `[G:commit 06942ae]` 2026-04-06T21:17 (+333/-6)
- **Category:** Capability
- **Provenance:** User-driven (PL-027 "let's adress this remaining issue in MAKEMOVE… remaining issues").
- **Mapping:** BL-005.
- **Specification statement:** For `PROGRAM-ID. FOO RECURSIVE` with no paragraph functions, WORKING-STORAGE group items are emitted as function-local C structs with `#define FIELD _l_STRUCT.FIELD`, giving each recursive call its own frame. Enables correct `PERFT`.
- **Evidence:** `[T:625f1b9f:i=7760]`.

### SB-027 — Chess perft correct (depth 1 = 20, depth 5 = 4,865,609) after MAKEMOVE legality fix
- **Step label:** commits `358678e`, `13163f5` (2026-04-07T12:11..12:18)
- **Category:** Test / Validation + Bugfix
- **Provenance:** User-driven (PL "yes please investigate"; perft acceptance criterion).
- **Mapping:** BL-005 / BL-008.
- **Evidence:** `[T:625f1b9f:i=8058]` "Chess perft working: depth 1=20 (correct!), depth 2=450, depth 3=10687"; `[T:625f1b9f:i=8122]` "perft now 100% correct".

### SB-028 — RECURSIVE frame-pointer struct (Approach E): ALPHABETA / QUIESCE with paragraph functions
- **Step label:** `[G:commit cc1932b]` 2026-04-08T13:56 "RECURSIVE frame pointer (Approach E): ALPHABETA/QUIESCE search working" (+452/-5)
- **Category:** Capability
- **Provenance:** User-driven (PL "the issue deserves a careful, in-depth plan"; explicit plan → "yes go").
- **Mapping:** BL-005, BL-008.
- **Specification statement:** For RECURSIVE programs *with* paragraph functions, the compiler now emits `struct _ws_FOO` at file scope, a `static struct _ws_FOO *_ws_FOO` pointer, and `#define FIELD _ws_FOO->FIELD`. The function body allocates a local frame, saves the outer pointer, activates itself, and restores on every GOBACK/exit. Paragraph functions access fields unchanged via the `#define`s.
- **Evidence:** `[T:625f1b9f:i=8880]`; design derivation at `[T:625f1b9f:i=8658]`.

### SB-029 — Runtime self-copy guard for LINKAGE group copy-in/out
- **Step label:** commits `4ac6bd2` and `610bd6d` (2026-04-08T21:43 and 22:03)
- **Category:** Quality/Hardening
- **Provenance:** Agent-initiated (fix for cross-file corruption observed in tournament).
- **Mapping:** BL-005 / BL-008.
- **Evidence:** `[T:625f1b9f:i=9194, i=9317]`.

### SB-030 — CU-GRP struct wrapping for cross-file CALL USING groups (final compiler fix)
- **Step label:** `[G:commit f289f1c]` 2026-04-10T04:22 (+86/-26)
- **Category:** Capability / Refactor
- **Provenance:** User-driven (PL-028 "run a tournament with large time budget").
- **Mapping:** BL-005 / BL-008.
- **Specification statement:** Groups passed via CALL USING across files are auto-wrapped in contiguous C structs, with `#undef`-then-re-`#define` sequences to avoid macro collisions between a struct member and a top-level `#define`.
- **Evidence:** `[T:625f1b9f:i=10110]`. Side bugs fixed alongside (see README "Bugs fixed this session" table): INSPECT TALLYING + TRIM, PIC 9 overflow, first-child duplicate CU-GRP, LOCAL-STORAGE CU-GRP exclusion, numeric literal BY REFERENCE → `&(int){5}`, TIMEUTIL replaced with `gettimeofday`, `cob_trim` buffer enlarged 4 KB → 8 KB.

### SB-031 — README rewrite: chess engine fully working, document EXTERNAL limitation, tournament results (20 games)
- **Step label:** `[G:commit a578b0a]` 2026-04-10T04:48 (+95/-30)
- **Category:** Documentation
- **Provenance:** User-driven (PL-029 "please commit and document this current limitation, also write-up current status of the compiler wrt chess and in general").
- **Mapping:** BL-006 / BL-008.
- **Specification statement:** README now records compilation status of all 11 chess files, the tournament (cobolcc 3 wins / GnuCOBOL 17 wins over 20 games at 10s+0.5s and 30s+1s), the root cause of the Elo gap (EXTERNAL storage treated as static per TU → broken transposition table), and the list of 7 manual patches currently applied to `main.c`.
- **Evidence:** `[R:/Users/mathieuacher/SANDBOX/cobol-compiler-cc/README.md:300-456]`; commit at `[T:625f1b9f:i=10195]`.

### SB-032 — Investigation of `-free` / `-O2` build-flag claims (follow-up session de76ffeb)
- **Step label:** session de76ffeb, 2026-04-05T21:30 → 22:01 (11 user turns)
- **Category:** Research / Documentation
- **Provenance:** User-driven (PL-030: "can you investigate such claims?").
- **Mapping:** BL-009.
- **Specification statement:** Confirmed all 36 `.cob` files use fixed-format (`*` in column 7), so `-free` would mis-parse them. Disproved the `-O2` "GnuCOBOL bug" hypothesis — root cause is that Homebrew GNU Binutils `strip` is first in PATH and corrupts Mach-O ARM64 binaries when GnuCOBOL invokes `strip -x` at -O2/-O3/-Os. Workaround: `brew unlink binutils` or put `/usr/bin` first in PATH; verified: with `PATH=/usr/bin:$PATH cobc -x -O2 …`, `test_o2_apple` prints HELLO with exit 0.
- **Evidence:** `[T:de76ffeb:i=5]` (format report), `[T:de76ffeb:i=6]` (strip matrix), `[T:de76ffeb:i=24]` (`HELLO\nExit code: 0`).
- **Scope notes:** No repo code change resulted — this was a diagnostic session. BL-009's "acceptance" is the written-up answer, not code.

---

## Agent-initiated threads (summary)

Several non-BL threads emerged inside the main session as the agent debugged the chess engine. They are captured above as Provenance = "Agent-initiated":

- Symbol/instruction/constant/paragraph table resizing (200 → 800, 500 → 1000, 300 constants, etc.) — SB-018.
- Buffer widenings: source lines 1500 → 3000, line width 256 → 512, tokens 30 → 80, ARG fields 100 → 256, `cob_trim` 4 KB → 8 KB — SB-018, SB-020, SB-030.
- Two full code-generation refactors mid-chess: LINKAGE static-emission → extern globals (SB-015 → SB-024), and CU-GRP struct wrapping policy (SB-025 → SB-030).
- Post-transpilation manual patches to `main.c` (7 items: GO UNSTRING rewrite, `fgets` EOF guard, IN_LINE space padding, SEARCH init guards, `cob_trim` alternating buffers, `setbuf(stdout,NULL)`, TIMEUTIL replacement) — captured in README as "Manual patches required".

These are intentionally **not** promoted to BL items because the user never requested them directly — they are prerequisites the agent chose while pursuing BL-005 / BL-008.
