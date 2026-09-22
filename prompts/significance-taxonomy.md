# Significance taxonomy for ranking delivered features

Used by per-project `KEY_FEATURES.md` generators to classify and rank the top
features of each project. The goal is to answer two questions the simple
feature count cannot answer:

1. **Is the project "just" algorithm implementation, or is it deeper engineering?**
2. **How do features compose — does the complexity come from the sum of pieces, or from their interaction?**

## 1. Significance classes

Each feature is tagged with one primary class (and optionally a secondary).

| Code | Class | Meaning | Tell-tale sign |
|---|---|---|---|
| **ALG** | Algorithm implementation | A well-known algorithm encoded into the host language. Textbook. | "implements minimax with alpha-beta", "DDA ray-casting", "CDCL with watched literals". Reference implementations exist in any mainstream language. |
| **DOM** | Domain modelling | Encoding the problem's domain rules into data structures, file formats, control flow. | "FEN parser", "DIMACS CNF reader", "payroll overtime rules per category", "UCI command dispatcher". Requires understanding the *domain*, not inventing the algorithm. |
| **SYS** | System integration / FFI | Cross-runtime, cross-language, or cross-process cooperation. | "COBOL → C → Python → pygame FFI", "CALL to external C from LINKAGE SECTION", "launching cutechess-cli and parsing its PGN output". Engineering lives at the boundary. |
| **INF** | Infrastructure / tooling | Build scripts, Makefiles, test runners, packaging. Supports everything else. | `Makefile`, `run_tests.sh`, `bench.sh`, `cobolcc` driver script. |
| **PRO** | Protocol / standard compliance | Implementing a published specification someone else wrote. | UCI chess protocol, DIMACS CNF format, SAT-Competition output, DRAT/DRUP proofs. |
| **LNG** | Language-level achievement | Pushing the host language in an unusual direction. | "Self-hosting a COBOL compiler written in COBOL", "recursive PERFORM via explicit stack", "`LOCAL-STORAGE SECTION` for recursion safety", "C-glue indirect to COBOL's CALL". |
| **VER** | Correctness verification | Test harnesses, property-based tests, cross-checks against reference implementations. | perft node-count validation, SAT4J cross-check, `xxd` byte-equality, 28-criterion grid. |
| **PRF** | Performance engineering | Optimization iterations with measurement. | "three-round speedup 230→135→118 s", "MVV-LVA ordering + LMR + NMP + PVS", "cache-read analysis". |
| **CMP** | Emergent composition | A feature that is **only meaningful** because earlier features exist. | "Elo match runner" requires UCI loop + perft + time mgmt; "bench runner" requires solver + verifier; "compile DOOM" requires lexer + parser + codegen + intrinsic lib. |

## 2. Depth scale (0–3)

| Depth | Description | Examples |
|---|---|---|
| 0 | Trivial | "Hello world", `.gitignore`, a printed banner. |
| 1 | Standard component | A parser for a well-known format; a test runner; a basic struct layout. |
| 2 | Non-trivial | Minimax + alpha-beta; PERFORM-based explicit recursion stack; CDCL with watched literals. |
| 3 | Deep engineering | Self-hosted compiler; CDCL + VSIDS + restarts + backjumping verified against MiniSat; real-time ray-casting FPS in a language without pointers. |

## 3. Effort proxy (0–3)

| Effort | Description | Signal |
|---|---|---|
| 0 | Minutes | ≤ 50 LOC, ≤ 1 commit. |
| 1 | Hours | ~ 100–500 LOC, 1–3 commits, low debug churn. |
| 2 | A full session | ~ 500–2 000 LOC or multi-file, multiple commits, visible debug loops. |
| 3 | Multi-session | > 2 000 LOC or spans several sessions; requires reverts, rewrites, or explicit perf iteration. |

## 4. Ranking score

```
score = depth × (1 + effort * 0.5)   # range 0 → 7.5
```

This lets a deep+heavy feature (depth 3, effort 3) outrank a deep+quick one
(depth 3, effort 0). The score is used only to order the ranked list — not
to collapse nuance.

## 5. Composition chains

A **composition chain** is a sequence of features where the later one is
*meaningless without* the earlier one. Chains are the signal that complexity
is emergent, not additive. Example chain for a chess project:

> FEN parser → move generator → perft validator → UCI loop → Elo match runner

The last item is only possible — and only valuable — because the earlier four
exist and are correct. A project with 3–4 long composition chains is doing
system-level engineering, not isolated algorithm plumbing.

## 6. Report format per project

Each project gets a `output/backlogs/<project>/KEY_FEATURES.md` following this
structure:

1. **Preamble** — 1 paragraph stating what the project was asked to build and what qualifies here as a "key feature" (≥ depth 1, not purely infra).
2. **Ranked table** — top 8–12 features, one row each:
   `rank | SB/F id | title | class | depth | effort | score | evidence` plus a one-line "significance note" per row that says in plain English *why* this is not just-an-algorithm (or confirms that it is).
3. **Composition chains** — 2–4 chains written as arrow sequences with a one-sentence explanation of the emergent capability.
4. **Significance profile** — a short table: count per class across the top features, so the project's centre of gravity is visible at a glance.
5. **Verdict** — 1 sentence: "Algorithm-centric", "Domain-modeling-centric", "System-integration-centric", "Language-achievement-centric", or a hybrid.

The per-project docs are then rolled up into a cross-project table in the
top-level `REPORT.md` by `scripts/key_features_rollup.py`.
