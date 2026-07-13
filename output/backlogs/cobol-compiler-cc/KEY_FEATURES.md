# KEY_FEATURES — cobol-compiler-cc

## Preamble

The user asked the agent to *"write a COBOL compiler in COBOL and demonstrate it
can run non-trivial COBOL programs."* What was delivered is a two-binary
toolchain — `cobolint.cob` (~4 462 LOC, tree-walking interpreter) and
`cobolcc.cob` (~11 044 LOC, COBOL-to-C transpiler) — both themselves written in
COBOL and bootstrapped by GnuCOBOL, plus the programs they compile (9 tests,
the Game-of-15 suite, a 1 363-LOC COBOL DOOM port, and an 11-file 3 854-LOC
UCI chess engine) and the tournament/benchmark infrastructure that validates
them. A *key feature* here is a delivered capability of at least depth 1 that
is not pure infrastructure (build glue, README churn, isolated table
resize). The interesting question for this project is not "is this an
algorithm implementation?" — parsing and code-gen clearly are — but how much
of the value comes from **language modelling** (DOM on the COBOL standard
itself), **self-hosting ambition** (LNG), and the **emergent composition**
(CMP) that lets a DOOM port or a recursive alpha-beta search actually run
through a compiler written in the very language it is compiling.

## Ranked features

score = depth × (1 + effort × 0.5), range 0 → 7.5.

| rank | SB id | title | class | depth | effort | score | evidence |
|---:|---|---|---|:---:|:---:|---:|---|
| 1 | SB-006, SB-008, SB-010..SB-025 | `cobolcc` COBOL-to-C transpiler (front-end + back-end, ~11 KLOC) | **LNG** / DOM | 3 | 3 | **7.5** | `[R:/Users/mathieuacher/SANDBOX/cobol-compiler-cc/cobolcc.cob]` 11 044 LOC; initial seed `[G:7cc9b7d]` +6 049 insertions; grew across ~60 commits |
| 2 | SB-016 (aggregated 29 commits), SB-021, SB-026, SB-028 | Chess-engine compilation: multi-program files, RECURSIVE frame-pointer (Approach E), perft depth 5 = 4 865 609 | **CMP** / LNG | 3 | 3 | **7.5** | `[G:fb46bb7]` multi-program; `[G:cc1932b]` frame pointer (+452/-5); `[T:625f1b9f:i=8122]` "perft now 100% correct" |
| 3 | SB-001, SB-002 | `cobolint` tree-walking interpreter (lexer/preprocessor/parser/symbol-table/executor in COBOL) | **LNG** / ALG | 3 | 2 | **6.0** | `[R:cobolint.cob]` 4 462 LOC; regression for 9 programs including 34 704-game DFS `[T:625f1b9f:i=744]` |
| 4 | SB-009 | COBOL-DOOM end-to-end: 1 363-LOC free-format source → C → linked terminal binary via 24 external C CALLs | **CMP** / SYS | 3 | 2 | **6.0** | `[R:README.md:283]`; requires free-format + COMP-5 + CALL-to-C + FUNCTION SQRT + REDEFINES — all composed |
| 5 | SB-026, SB-028, SB-029, SB-030 | RECURSIVE programs: LOCAL-STORAGE local structs → frame-pointer struct with paragraph-function `#define` rebinding; LINKAGE self-copy guard; CU-GRP cross-file struct wrapping | **LNG** / DOM | 3 | 2 | **6.0** | `[G:06942ae]` +333; `[G:cc1932b]` +452; `[G:f289f1c]` +86; design derivation `[T:625f1b9f:i=8658]` |
| 6 | SB-008, SB-014, SB-024, SB-025 | Cross-language boundary: CALL USING BY VALUE/REFERENCE/RETURNING → C extern, COMP-5 binary types, LINKAGE scalar copy-in/out + group extern globals | **SYS** / DOM | 2 | 3 | **5.0** | `[G:1321b32]` +1 224; `[G:5ac6763]` +486; `[G:967f425]` extern globals |
| 7 | SB-011, SB-013, SB-019, SB-020 | COBOL language-feature coverage: EVALUATE (TRUE/strings/char switch), PERFORM FOREVER, FUNCTION MOD/ABS/SQRT/INTEGER-OF-DATE/TRIM, INSPECT TALLYING, reference modification, 1D/2D OCCURS strings, COPY path resolution | **DOM** | 2 | 3 | **5.0** | `[G:fef9782]`, `[G:d46c4a2]`, `[G:4a2cbbd]`, `[G:9346303]`, `[G:22df96b]`, `[G:875c2fd]` across 2026-04-04..05 |
| 8 | SB-008, SB-012 | Free-format / fixed-format dual-mode lexer (first-line-starts-with-letter detection, period-aware line joining, hyphen→underscore smart-splitting) | **DOM** / ALG | 2 | 2 | **4.0** | `[G:1321b32]`; line-joining fixes in `[G:d505af4]` and surrounding commits |
| 9 | SB-027, SB-028, BL-008 | Chess tournament via cutechess-cli (cobolcc-built vs GnuCOBOL-built engine, 20 games at two time controls, PGN + Elo gap explained by EXTERNAL semantics) | **CMP** / VER | 2 | 2 | **4.0** | `[R:README.md:310-335]`; perft reference match `[T:i=8122]`; `[T:i=10119]` first game quoted |
| 10 | SB-007, SB-023 | `benchmark.sh` — build + exec time, whitespace-tolerant diff, GnuCOBOL vs cobolcc table (game15 20×, perft 7.7×) | **VER** / INF | 2 | 1 | **3.0** | `[R:benchmark.sh]` 332 LOC; `[G:16102a9]` +339; perf table `[R:README.md:223-230]` |
| 11 | SB-032 | Root-cause analysis of `cobc -O2` hang on macOS ARM64: Homebrew GNU `strip` corrupts Mach-O; fix = PATH reorder / `brew unlink binutils` | **SYS** / VER | 2 | 1 | **3.0** | session `de76ffeb`; matrix `[T:de76ffeb:i=6]`; verified exit 0 `[T:de76ffeb:i=24]` |
| 12 | SB-018, SB-020 | Table / buffer scaling: symbols 200→800, instructions 500→1 000, line buffers 256→512, `cob_trim` 4 KB→8 KB — prerequisite for chess-engine correctness | **DOM** / INF | 1 | 2 | **2.0** | `[G:57d5f3a]`; `[T:625f1b9f:i=4623]` "162→35 errors"; `[G:875c2fd]` "10/11 at 0!" |

**Significance notes (one line per row):**

1. Writing a working compiler *in COBOL itself* is the core language-level achievement; the DOM content (COBOL's PIC/OCCURS/REDEFINES/LINKAGE semantics) is not a textbook — every case has to be re-derived from the standard. Depth 3 / Effort 3.
2. Getting a recursive alpha-beta chess engine to run through the agent's own compiler is emergent: it needs every front-end feature, the RECURSIVE rewrite, cross-file CU-GRP wrapping, and numeric correctness — none of which matter individually. Depth 3 / Effort 3.
3. The interpreter is not a throwaway: it is the executable reference against which the compiler's output is diff-compared, and its front-end is literally reused by `cobolcc`. Not a textbook tree-walker because COBOL's fixed-format, continuation, and group-item rules are in the *host* language.
4. DOOM-in-COBOL compiling and linking is not an algorithm — it is the proof that the SYS boundary (COBOL ↔ C) works on a real ~1.4 KLOC program. Pure CMP: meaningless without the whole front-end + COMP-5 + CALL-to-C.
5. Approach E (frame-pointer struct with `#define FIELD _ws_FOO->FIELD` rebound per call) is a genuinely non-obvious code-gen design; the agent iterated from "local struct" to "pointer indirection" across several commits after observing that paragraph functions could not see the stack frame.
6. This is where COBOL-to-C stops being a toy. BY VALUE vs BY REFERENCE vs RETURNING, extern void fix, and copy-in/copy-out semantics are DOM content, but the emitted `extern` + `&(int){5}` literal-by-reference is SYS engineering.
7. Breadth of COBOL standard coverage is the raw material for everything else; not algorithmically deep per construct but sheer count (≥30 features added across ~10 commits).
8. Free-format detection and line-joining are non-trivial because COBOL's rules about period-terminated sentences and column-7 continuation interact with hyphen-containing identifiers.
9. The tournament is classic CMP: it is only meaningful because the compiler, the chess engine compile, and a third-party PGN tool all work together. VER because the 17-3 Elo gap was traced to EXTERNAL-as-static — a real compiler-behaviour finding.
10. Whitespace-tolerant diff + build-time + exec-time table is a clean VER harness, not just a script — it established the 20× / 7.7× numbers now quoted in README.
11. Pure SYS diagnosis of a toolchain bug outside the agent's own code; noteworthy because the conclusion contradicted the user's stated hypothesis (not a `-O2` bug but a `strip` bug).
12. Hardening that unblocks the chess corpus; depth 1 only because individually each resize is mechanical, but cumulatively it is what moved the pass rate from 8/11 to 11/11.

## Composition chains

1. **cobolint front-end → cobolcc front-end → cobolcc back-end → COBOL-DOOM compile → runnable terminal DOOM**
   The lexer/parser/symbol-table written for the interpreter is reused verbatim by the transpiler; DOOM is a demo that is only possible because *all* of the front-end plus COMP-5 plus CALL-to-C plus FUNCTION SQRT exist simultaneously.
2. **cobolcc → COPY/LINKAGE/multi-program → RECURSIVE frame pointer → perft(d5)=4 865 609 → cutechess-cli tournament → "cobolcc 3 – gnucobol 17, EXTERNAL is the cause"**
   The tournament's *diagnostic value* (pinpointing EXTERNAL-as-static as the Elo gap) is only accessible because the chess engine built by cobolcc actually plays legal games.
3. **interpreter correct on game15 subsets 4..8 → interpreter times out at N=9 → compiler pivot (PL-003) → cobolcc game15 in 0.01 s (20× GnuCOBOL) → benchmark.sh formalises the comparison**
   The performance artefact is meaningful only because the correctness artefact exists first; the pivot itself is a composition edge, not just a feature.
4. **COBOL parser in COBOL + code-gen in COBOL + GnuCOBOL bootstrap → self-hosted binary → compiles external COBOL programs written by *other* agent sessions**
   The self-hosting loop closes here: `cobolcc` compiled by GnuCOBOL compiles COBOL-DOOM / cobochess / game15 authored by sibling sessions — the project's LNG claim is a composition, not a single feature.

## Significance profile

| Class | Primary count (top 12) | Secondary count | Notes |
|---|:---:|:---:|---|
| LNG | 3 | 2 | Self-hosting + recursion rewrite — the project's centre of gravity |
| DOM | 3 | 4 | Encoding COBOL-85 semantics (PIC, OCCURS, REDEFINES, LINKAGE, EVALUATE) |
| CMP | 3 | 0 | DOOM, chess engine, tournament — emergent-only value |
| SYS | 2 | 2 | CALL-to-C boundary + macOS binutils diagnosis |
| VER | 1 | 2 | Perft cross-check + benchmark diff + tournament PGN |
| ALG | 0 | 2 | Parsing/tree-walk are textbook in other languages, atypical here |
| INF | 0 | 2 | Build/bench scripts supporting, not leading |
| PRO | 0 | 0 | No published protocol implemented by the compiler itself (chess engine's UCI is inherited) |
| PRF | 0 | 0 | Perf numbers exist (20×, 7.7×) but were *observed*, not iterated on |

Centre of gravity: **LNG + DOM + CMP**, with SYS supporting. No PRO, no PRF, and ALG is deliberately secondary — the parsing/code-gen algorithms are not the interesting part; the fact that they are written in COBOL and compose up to DOOM is.

## Verdict

**Language-achievement-centric hybrid (LNG + DOM + CMP)** — a self-hosted COBOL
subset compiler whose significance is not the parsing algorithm but the
composition chain that lets a compiler written in COBOL, compiled by GnuCOBOL,
compile a COBOL DOOM port and a recursive UCI chess engine authored by
sibling agent sessions.
