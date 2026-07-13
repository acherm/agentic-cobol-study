## Feature classification — significance profile per project

Every project's top 8–12 features are classified by a 9-class taxonomy (see [`prompts/significance-taxonomy.md`](prompts/significance-taxonomy.md) for definitions) in [`output/backlogs/<project>/KEY_FEATURES.md`](output/backlogs/). The table below shows the count of top-features that fall in each class, per project. **Dominant** = the two or three classes with the highest counts — where the project actually spends its engineering weight.

Classes: `ALG` algorithm · `DOM` domain modelling · `SYS` system integration / FFI · `INF` infrastructure · `PRO` protocol compliance · `LNG` language-level achievement · `VER` verification · `PRF` performance engineering · `CMP` emergent composition.

| Project | Top | ALG | DOM | SYS | INF | PRO | LNG | VER | PRF | CMP | Dominant |
|---|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| `chess-cobol-cc` | 12 | 2 | **3** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **DOM + ALG + SYS** |
| `cobol-compiler-cc` | 12 | — | **3** | 2 | — | — | **3** | 1 | — | **3** | **DOM + LNG + CMP** |
| `cobol-compiler-codex` | 12 | 2 | — | 2 | — | — | 1 | **3** | 1 | **3** | **VER + CMP + ALG** |
| `cobol-compress-codex` | 12 | 2 | 3 | — | — | — | 1 | **4** | 1 | 1 | **VER + DOM + ALG** |
| `SATCobol-codex` | 11 | 2 | 2 | — | 1 | — | 1 | **3** | 1 | 1 | **VER + ALG + DOM** |
| `SATCobol-cc` | 11 | **3** | 2 | — | 1 | — | 1 | **3** | — | 1 | **ALG + VER + DOM** |
| `cobol-tictactoe` | 11 | 1 | **6** | — | — | — | 2 | — | — | 2 | **DOM + LNG + CMP** |
| `game15-cobol-codex` | 11 | 1 | **7** | — | — | — | 2 | — | — | 1 | **DOM + LNG + ALG** |
| `cobol-doom-codex` | 10 | 1 | 2 | 1 | 1 | — | **4** | 1 | — | — | **LNG + DOM + ALG** |
| `COBOL-chess` | 9 | 2 | **3** | — | 1 | 1 | 1 | 1 | — | — | **DOM + ALG + INF** |
| `cobol-doom-cc` | 9 | — | **5** | — | 1 | — | 2 | 1 | — | — | **DOM + LNG + INF** |
| `cobol-compress-cobolcc` | 8 | — | 2 | — | — | — | 1 | **4** | 1 | — | **VER + DOM + LNG** |
| `COBOL-pygame` | 8 | — | — | **3** | 1 | — | 2 | — | — | 2 | **SYS + LNG + CMP** |

### Class → projects where it is dominant

| Class | Description | Projects where this class leads |
|---|---|---|
| `ALG` | Algorithm | `SATCobol-cc` |
| `DOM` | Domain modelling | `chess-cobol-cc`, `COBOL-chess`, `cobol-compiler-cc`, `cobol-doom-cc`, `cobol-tictactoe`, `game15-cobol-codex` |
| `SYS` | System integration / FFI | `COBOL-pygame` |
| `INF` | Infrastructure / tooling | — |
| `PRO` | Protocol compliance | — |
| `LNG` | Language-level achievement | `cobol-doom-codex` |
| `VER` | Correctness verification | `cobol-compiler-codex`, `cobol-compress-codex`, `cobol-compress-cobolcc`, `SATCobol-codex` |
| `PRF` | Performance engineering | — |
| `CMP` | Emergent composition | — |

### Cross-project totals

| Class | Total top-feature count across projects | Share |
|---|---:|---:|
| `ALG` Algorithm | 16 | 11.8% |
| `DOM` Domain modelling | 38 | 27.9% |
| `SYS` System integration / FFI | 9 | 6.6% |
| `INF` Infrastructure / tooling | 7 | 5.1% |
| `PRO` Protocol compliance | 2 | 1.5% |
| `LNG` Language-level achievement | 22 | 16.2% |
| `VER` Correctness verification | 22 | 16.2% |
| `PRF` Performance engineering | 5 | 3.7% |
| `CMP` Emergent composition | 15 | 11.0% |
| **Total top-features ranked** | **136** | 100.0% |

### Verdicts at a glance

| Project | Verdict (auto-extracted from `KEY_FEATURES.md`) |
|---|---|
| `COBOL-chess` | **Hybrid: algorithm-centric with serious domain-modelling and verification backbone, plus a LNG accent from COBOL-specific recursion tricks** — a thorough, by-the-book chess engine where the sophistication lives in composing a 1 000-line search module on top o… |
| `COBOL-pygame` | **System-integration-centric, with a language-achievement backbone** — the project's substance is the COBOL↔C↔SDL2 boundary (ABI, handles, struct mirrors, dialect-specific linker semantics), not algorithms; the two composition features (hello, Flappy) are valu… |
| `SATCobol-cc` | **Verification-centric hybrid — ALG + VER with a genuine LNG supporting act, CDCL left unfinished.** This is neither "just-an-algorithm" nor "just-domain-modelling": baseline DPLL is textbook, but the iterative-trail port is non-trivial COBOL engineering; the … |
| `SATCobol-codex` | **Balanced hybrid — ALG + PRF + VER, with a genuine LNG supporting act.** This is neither "just-an-algorithm" nor "just-domain-modelling": the CDCL core is textbook, but re-hosting it on COBOL's fixed-capacity arrays is depth-3 engineering; the three-round per… |
| `chess-cobol-cc` | **Hybrid, centre-of-gravity LNG + PRF + SYS, not "just minimax":** the top three ranks are a language-level achievement (explicit-stack search in COBOL), a performance-engineering loop (14 measured INCR→TEST→RETR cycles with 7 reverts), and an emergent composi… |
| `cobol-compiler-cc` | **Language-achievement-centric hybrid (LNG + DOM + CMP)** — a self-hosted COBOL subset compiler whose significance is not the parsing algorithm but the composition chain that lets a compiler written in COBOL, compiled by GnuCOBOL, compile a COBOL DOOM port and… |
| `cobol-compiler-codex` | **Hybrid: ALG/LNG foundation + VER/PRF superstructure with heavy CMP** — a COBOL-in-COBOL subset compiler (ALG+LNG) whose distinguishing contribution is a benchmark-driven comparison apparatus against GnuCOBOL and a self-correcting verification loop (VER+PRF+C… |
| `cobol-compress-cobolcc` | **Verification-centric hybrid with a language-achievement accent** — shares the Codex sibling's VER-dominated profile (VER=4/10) but adds a language-level dimension (LNG in 3 features) through the 3-file modular decomposition and the COBOL CRC32 subprogram. |
| `cobol-compress-codex` | **Verification-centric hybrid with a strong domain-modelling core** — the project is the most verification-hygienic of the COBOL set (VER = 4/12, plus a CMP test-infrastructure layer and a PRF fix cycle that is itself test-driven), built on a respectable DOM s… |
| `cobol-doom-cc` | **Language-achievement-centric with DOM superstructure.** Entire rendering pipeline runs in COBOL paragraphs with zero C code. |
| `cobol-doom-codex` | **Hybrid — LNG-centric with SYS seam.** DDA raycaster in COBOL (not C) is the strongest "COBOL does the computation" claim. |
| `cobol-tictactoe` | Hybrid **domain-modelling + language-achievement** project with strong emergent composition: the algorithm content is textbook (one minimax, one DFS), but the magic-square/D4 encoding, the COBOL-recursion-via-explicit-stack, and the counter -> tree -> avoid ->… |
| `game15-cobol-codex` | Hybrid **domain-modelling + language-achievement** project with strong emergent composition — same verdict as the Claude-Code sibling, but with Codex leaning a step further into **eager, table-driven domain encodings** (the 986,409-byte factorial-rank bitmap a… |

_Numbers above are parsed from the `## Significance profile` tables inside each `KEY_FEATURES.md`. Column semantics (primary vs primary+secondary) varies slightly across projects — the parser always takes the **first integer** of each row, which corresponds to the primary-class count. For the nuance, see the individual per-project files._

