# game15-cobol-codex — Post-Session Analysis

Two-pass backlog + strategy analysis of the Codex CLI session that produced the `game15-cobol-codex` project. This is the **Codex replica** of the Claude-Code-built `cobol-tictactoe`; the human prompts were taken verbatim from that project's `REPLAY_PROMPTS.md`.

> **Project root:** `/Users/mathieuacher/SANDBOX/game15-cobol-codex` (read-only for this analysis)
> **Agent:** Codex CLI `v0.119.0-alpha.11`, model `gpt-5.4`
> **Session:** `019d95b1-8660-75c2-8a6b-44dfbafc0a19` (single session, 2026-04-16T09:49 → 13:26 UTC, ~3h37m wall-clock)
> **Raw log:** `~/.codex/sessions/2026/04/16/rollout-2026-04-16T11-48-52-019d95b1-8660-75c2-8a6b-44dfbafc0a19.jsonl`
> **Normalised turn log used here:** `output/turns/game15-cobol-codex__Codex__019d95b1-8660-75c2-8a6b-44dfbafc0a19.jsonl` (533 turns)

Companion artefacts in this folder:

- [`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md) — agent-centric step-wise backlog (`SB-01` … `SB-32` + `F-01` … `F-03`).
- [`KEY_FEATURES.md`](KEY_FEATURES.md) — top-12 ranked-feature profile per the [significance taxonomy](../../../prompts/significance-taxonomy.md).
- [`appendix.json`](appendix.json) — machine-readable index of all PASS 1/2 artefacts.

---

## Phase 0 — Discovery

### 0.1 Project identification

- **Primary language:** GnuCOBOL (free format, `>>SOURCE FORMAT FREE`)
- **Entry points:** five standalone `PROGRAM-ID` modules, each compiled with `cobc -x -free <name>.cob`
  - `game15.cob` — enumerator + `--unique` [R:game15.cob:500 lines]
  - `game15_tree.cob` — minimax tree renderer with `avoid:` and `--depth N` [R:game15_tree.cob:671 lines]
  - `game015.cob` — 0.15 variant of the counter [R:game015.cob:501 lines]
  - `game015tree.cob` — 0.15 variant of the tree [R:game015tree.cob:685 lines]
  - `gameN.cob` — generalised Game of N with runtime triples [R:gameN.cob:465 lines]
- **Build system:** none — direct `cobc -x -free <src>.cob`; no Makefile, no tests beyond manual spot-checks.
- **Git metadata:** single branch `codex/game15`, 4 commits (`29cbcaa` → `c41b9b5` → `f9c2eb1` → `ce67d51`), single author `Mathieu Acher`. `.gitignore` ignores compiled binaries `game15` and `game15_tree`. `[R:.gitignore:1-2]`
- **Agent constraints (not user prompts):** none project-level (no `AGENTS.md`, no `.codex/config.toml` in the repo). Codex's built-in `<permissions>` / `<INSTRUCTIONS>` bootstrap seen at session turn 0 was filtered out before declaring `PL-ROOT`. `[T:event_000]`

### 0.2 Session selection

Single session matches the repo `cwd = /Users/mathieuacher/SANDBOX/game15-cobol-codex` (see `session_meta`). No ambiguity; selected directly.

### 0.3 Candidate milestones

1. `T+00:00` — PL-ROOT (enumerator prompt) → write `game15.cob` → first compile clean → first run matches oracle 255,168 → commit `29cbcaa` `[T:event_002 … event_053]`.
2. `T+07:34` — PL-02 (`--unique`) → symmetry table + factorial rank + 986,409-entry bitmap → matches 31,896 → (no commit yet, rolled into step 4) `[T:event_061 … event_088]`.
3. `T+15:54` — PL-03 (optimal tree) → bottom-up retrograde solve + iterative DFS printer → **2 bugs** (`FILLED-TARGET` underflow, stale `OWNER`) → matches `[Draw]` oracle `[T:event_096 … event_241]`.
4. `T+29:37` — PL-04 (avoid) → safe/bad split in classifier → **1 bug** (avoid-line indentation) → commit `c41b9b5` bundles PL-02 + PL-03 + PL-04 `[T:event_243 … event_337]`.
5. `T+2:34:14` — PL-05 (0.15 variants) → `cp` then display-only patch → compile → commit `f9c2eb1` `[T:event_344 … event_415]`.
6. `T+3:23:34` — PL-06 (gameN) → two-argument parser, triple generator, enumeration guard, pool listing → commit `ce67d51` `[T:event_420 … event_526]`.

---

## PASS 1 — Extraction (factual)

### A0 — Human user instruction index (UII)

12 user-role prompt events; the first is Codex's system environment block and 5 are one-word "commit"/"create a git and commit" procedural instructions. Six are feature requests; one is a tooling request.

| ID | `[T:event_###]` | Paraphrase / short quote | Category | Strength | Target surface | Maps to BL |
|----|------|--------------------------|----------|----------|----------------|------------|
| UI-00 | `event_001` | Environment context (cwd, shell, date) | Meta/process | Constraint-only | — | — |
| UI-01 | `event_002` | "Write a COBOL program (GnuCOBOL) for the Game of 15 […] enumerate every possible game […] report P1 wins, P2 wins, draws, total games." | FeatureRequest | Explicit imperative | Code | BL-01 |
| UI-02 | `event_040` | "create a git and commit" | Tooling | Explicit imperative | Repo structure | OP-01 |
| UI-03 | `event_061` | "Add a --unique command-line flag […] Game of 15 is isomorphic to Tic-Tac-Toe […] remove symmetric duplicates. Keep reporting the original totals." | FeatureRequest + AcceptanceCriteria | Explicit imperative | Code + UX | BL-02 |
| UI-04 | `event_089` | "commit" | Tooling | Explicit imperative | Repo structure | OP-02 |
| UI-05 | `event_096` | "Write a new COBOL program that displays the Game of 15 optimal play tree as ASCII art. […] Support a --depth N flag." | FeatureRequest + Scenario | Explicit imperative | Code + UX | BL-03 |
| UI-06 | `event_243` | "Enhance the optimal play tree: at each decision point […] show which available moves would be mistakes. […] avoid: line […]" | FeatureRequest + Scenario | Explicit imperative | UX / output | BL-04 |
| UI-07 | `event_316` | "commit" | Tooling | Explicit imperative | Repo structure | OP-03 |
| UI-08 | `event_344` | Game of 0.15 variant: "Create two programs: game015.cob and game015tree.cob. Only the display format changes." | FeatureRequest + Constraint | Explicit imperative | Code + UX | BL-05 |
| UI-09 | `event_394` | "commit" | Tooling | Explicit imperative | Repo structure | OP-04 |
| UI-10 | `event_420` | Game of N generator: "Usage `./gameN <target-sum> [<max-number>]` […] winning triples […] skip enumeration when max-number > 9 […] usage message." | FeatureRequest + Scenario | Explicit imperative | Code + UX | BL-06 |
| UI-11 | `event_502` | "commit" | Tooling | Explicit imperative | Repo structure | OP-05 |

Strength distribution: 11 Explicit imperative, 1 Constraint-only (env context). No Questions or Suggestions — this is replay-mode usage.

### A0b — Project constraints index (PCI)

- **PC-01** — `.gitignore` (`game15`, `game15_tree`): repo-policy, agent-created; does not constrain behaviour. `[R:.gitignore:1-2]`
- **PC-02** — `session_meta.base_instructions` = Codex built-in default "You are Codex […]" (no project-level AGENTS.md). Impact on replay: default Codex behaviour (filesystem sandbox workspace-write, shell approvals). `[T:session_meta header]`

No `.codex/config.toml`, no `AGENTS.md`, no `CONTRIBUTING.md` inside the repo.

### A1 — Prompt ledger (PL)

| ID | `[T:…]` | Raw snippet | Linked UI | Linked BL |
|----|---------|-------------|-----------|-----------|
| PL-ROOT | `event_002` | "Write a COBOL program (GnuCOBOL) for the 'Game of 15'. Rules: Two players alternate picking a number from {1, 2, ..., 9} …" | UI-01 | BL-01 |
| PL-02 | `event_061` | "Add a --unique command-line flag to the game counter. The Game of 15 is isomorphic to Tic-Tac-Toe …" | UI-03 | BL-02 |
| PL-03 | `event_096` | "Write a new COBOL program that displays the Game of 15 optimal play tree as ASCII art …" | UI-05 | BL-03 |
| PL-04 | `event_243` | "Enhance the optimal play tree: at each decision point, before listing the optimal (safe) moves, show which available moves would be mistakes …" | UI-06 | BL-04 |
| PL-05 | `event_344` | "The Game of 0.15 is defined as follows: two players alternate picking a number among {0.01 … 0.09} …" | UI-08 | BL-05 |
| PL-06 | `event_420` | "Write a COBOL program that generalizes the game to any target sum and number range …" | UI-10 | BL-06 |

Each raw prompt is **textually identical** (modulo whitespace) to the corresponding step in `output/backlogs/cobol-tictactoe/REPLAY_PROMPTS.md` [R:../cobol-tictactoe/REPLAY_PROMPTS.md:11-144]. This confirms the replay-pack origin.

#### Canonical `PL-ROOT` replay prompt

> Write a GnuCOBOL program that enumerates every legal completed game of the Game of 15 (two players alternately pick from {1..9} without repetition; a player wins when any three of their picks sum to 15; if all nine are picked and no one has won, it is a draw). Report the four counts: Player 1 wins, Player 2 wins, Draws, Total games. Expected oracle: `131184 / 77904 / 46080 / 255168`.

(Canonical replay prompts for BL-02…BL-06 are in the §A4 replay package below.)

### A2 — Session overview

- **One-liner:** Codex built 5 standalone GnuCOBOL programs over ~3h37m wall-clock in a single session, following the 6-step replay pack from the Claude-Code sibling.
- **Milestone timeline:** see §0.3.
- **Artifact inventory:**
  - Source: 5 `.cob` files, 2822 LOC total.
  - Binaries: 2 compiled artefacts checked in (`game15`, `game15_tree`) at session's final state — but `.gitignore` excludes them from subsequent commits.
  - No tests, no Makefile, no CI, no README in the project itself.
- **Run/build/test commands** (observed in session):
  - Build: `cobc -x -free <src>.cob [-o /tmp/<bin>]` — 20 invocations, all clean after first `game15.cob` compile. `[T:event_031, 074, 119, 128, 136, 171, 197, 202, 209, 220, 257, 273, 279, 290, 382, 383, 434, 457, 476]`
  - Run: `./game15`, `./game15 --unique`, `/tmp/game15_tree --depth {0,1,2,3}`, `/tmp/game15_tree > /tmp/game15_tree_full.txt`, `/tmp/gameN [args]`.
  - Test: no test harness; validation is one-off oracle matching against the counts in the prompts.

### A3 — Feature backlog (BL) — user-driven only

| ID | Title | Type | UI | PL | Acceptance criteria (from prompt) | Implementation summary | DoD |
|----|-------|------|----|----|----------------------------------|-----------------------|-----|
| BL-01 | Game of 15 game counter | Feature | UI-01 | PL-ROOT | Oracle `131184 / 77904 / 46080 / 255168` | `game15.cob`: iterative DFS (`SEARCH-DEPTH` + `NEXT-CANDIDATE` stack), direct tic-tac-toe-line win check, stop-on-win | Yes `[T:event_036]` |
| BL-02 | `--unique` symmetry deduplication | Feature | UI-03 | PL-02 | Oracle `16398 / 9738 / 5760 / 31896`; original totals still reported | 8×9 D4 symmetry table, min-over-orbit canonicalisation, factorial-rank into 986,409-byte `SEEN-CANONICAL` bitmap | Yes `[T:event_080]` |
| BL-03 | Optimal play tree renderer | Feature | UI-05 | PL-03 | Full tree has only `[Draw]` leaves; `--depth N` limits display | `game15_tree.cob`: retrograde bottom-up solve over all 19,683 base-3 states, iterative DFS with depth-10 explicit stack, `\|--/+--` connectors | Yes (after 2 bugs fixed) `[T:event_229, 297]` |
| BL-04 | `avoid:` annotations | Feature | UI-06 | PL-04 | `avoid: n1, n2, …` printed before safe children at each decision | Safe/bad split in `BUILD-OPTIMAL-CHILDREN`; `DISPLAY-AVOID-LINE` with child-prefix alignment | Yes (after 1 bug fixed) `[T:event_297]` |
| BL-05 | Game of 0.15 variants | Feature | UI-08 | PL-05 | Counts identical to Game of 15; labels use `0.0X` | `game015.cob` / `game015tree.cob`: duplicated sources + `MOVE-LABEL(9)` table `"0.01".."0.09"` for the tree, display-only banner for the counter | Yes `[T:event_386-388]` |
| BL-06 | Game of N generator | Feature | UI-10 | PL-06 | Classic `15 9` → 8 triples, 255,168 games; validation + skip path | `gameN.cob`: two-arg CLI (`UNSTRING`), runtime triple generator (84 slots), parameterised DFS, default `max = target-3`, skip when `max > 9`, number-pool listing | Yes `[T:event_477-495]` |

No BL items were cut or deferred.

### A3b — Reproducibility ops (OP) — non-feature

Five explicit "commit" / "create a git and commit" user instructions → one OP per commit. Recorded here because the user requested them; they are **not** features.

| ID | Command executed | Evidence |
|----|------------------|----------|
| OP-01 | `git init -b codex/game15`, `git add game15.cob .gitignore`, `git commit -m "Add Game of 15 enumerator"` → `29cbcaa` | `[T:event_047, 050, 053]`, `[G:29cbcaa]` |
| OP-02 | `git add .gitignore game15.cob game15_tree.cob`, `git commit -m "Add unique counts and optimal play tree"` → `c41b9b5` | `[T:event_332, 336]`, `[G:c41b9b5]` |
| OP-03 | (rolled into OP-02; the "commit" after avoid was collected with the tree commit) | `[T:event_319-336]` |
| OP-04 | `git add game015.cob game015tree.cob`, `git commit -m "Add Game of 0.15 programs"` → `f9c2eb1` | `[T:event_405, 414]`, `[G:f9c2eb1]` |
| OP-05 | `git add gameN.cob`, `git commit -m "Add generalized Game of N program"` → `ce67d51` (after resolving a stale `.git/index.lock`) | `[T:event_511, 525, 526]`, `[G:ce67d51]` |

### A3c — Specification backlog (SB)

See [`SPECIFICATION_BACKLOG.md`](SPECIFICATION_BACKLOG.md). 32 SB items + 3 bug fixes (`F-01..F-03`).

### A4 — Replay package (raw + canonical prompts per BL)

Raw prompts are the `PL-##` entries above (taken verbatim from the replay pack). Canonical replay prompts (minimal + complete, no algorithm prescription) are as follows. They match the Claude-Code sibling's replay pack step-for-step so the two projects are replayable from a single canonical set.

- **BL-01** — see `PL-ROOT` canonical above.
- **BL-02** — "Add a `--unique` CLI flag to the Game of 15 counter. When passed, additionally report counts where two games identical up to square symmetries (8 rotations/reflections of the 3×3 magic square) are counted once. Keep the original totals. Expected oracle: `16398 / 9738 / 5760 / 31896`."
- **BL-03** — "Write a separate GnuCOBOL program that prints the Game of 15 optimal-play tree. Show only moves that preserve the outcome under optimal play; annotate each node `[Draw]`/`[P1 wins]`/`[P2 wins]`; use `\|--` / `+--` connectors. Support `--depth N` to truncate with `...`."
- **BL-04** — "At every decision point in the tree, also list moves that would be mistakes. Print `avoid: n1, n2, …` before the safe branches at the same indent column as those branches. Skip the line when there are no bad moves."
- **BL-05** — "Produce two additional programs (`game015.cob`, `game015tree.cob`) that report the Game of 0.15 (numbers {0.01 … 0.09}, target 0.15). The logic must stay byte-for-byte identical to the Game of 15 programs; only the displayed number labels and banner change."
- **BL-06** — "Write `gameN.cob` parameterised by `<target-sum> [<max-number>]`. List the pool, generate all winning triples at runtime, enumerate games when `max-number ≤ 9`, skip enumeration with an explanatory message otherwise. Include argument validation and a usage message."

Preconditions: GnuCOBOL (`cobc`) in `$PATH`. Reproduction: compile each `.cob` with `cobc -x -free`, run binary with the arguments listed in the validation evidence `[T:event_*]` above.

### A5 — Repo quantification stats

| Category | #files | LOC |
|----------|--------|-----|
| GnuCOBOL production source | 5 | 2822 |
| Git hygiene (`.gitignore`) | 1 | 2 |
| Compiled binaries checked in (but git-ignored in HEAD) | 2 | — |
| Tests / CI / build scripts | 0 | 0 |
| Documentation (README) | 0 | 0 |

Per-file LOC:

- `game15.cob` — 500
- `game15_tree.cob` — 671
- `game015.cob` — 501
- `game015tree.cob` — 685
- `gameN.cob` — 465

`[S:stats_run_1]` computed via `wc -l *.cob`.

### PASS 1 STOP MARKER

**PASS 1 COMPLETE.**

Missing/ambiguous evidence: (i) no run-time measurements captured (cobc release binary run-time for `--unique` was not timed); (ii) no oracle for `gameN 12 8 / 10 7` — Codex only validated the classic `15 9` case and the skip path; the Claude-Code REPLAY_PROMPTS.md lists other test cases that Codex did not run; (iii) the 0.15 tree binary was only spot-checked at `--depth 2, 3` — no full-tree oracle.

---

## PASS 2 — Interpretation

### B0 — RQ coverage matrix

| RQ | Evidence sources | Indicators | Output sections |
|----|------------------|-----------|------------------|
| RQ1 What strategies did the agent use? | session log (tool_use sequences, reasoning blocks) | strategy-code counts per BL, sequences | B2, B4 |
| RQ2 Outcomes/quality per BL | binary run output, commit contents | oracle match, #bugs, build clean | B5, B6 |
| RQ3 Success/failure factors | tool_use + assistant_text pairs during bug-fix loops | claims FOR/AGAINST | B8 |
| RQ4 Interaction demand | UII + PL | #user prompts/BL, clarification cycles, scope churn | B7 |
| RQ5 Reproducibility | repo + replay pack + session | canonical prompt → oracle match | A4, B5 |

### B1 — Operational definitions

- **Strategy code** = a labelled segment of the agent's work (defined in B2).
- **Outcome** = per-BL 6-dimension rubric (B5).
- **Reproducibility** = "does a fresh `cobc -x -free` + oracle check pass on HEAD?" — Yes for all 6 BLs (for the oracles the agent itself validated).
- **Interaction demand** = # of user prompts per BL (see §A0).

### B2 — Strategy codebook

| Code | Definition | Inclusion | Example from session |
|------|------------|-----------|----------------------|
| PLAN | Writing or restating an end-to-end approach before coding | Reasoning block or assistant_text naming steps 1..N | `event_020` "Plan for the implementation: 1. Create… 2. Use… 3. Iterate…" |
| SCAF | Writing the first working scaffold of a new module | First `apply_patch` / write of a new `.cob` file | `event_026` (game15.cob scaffold), `event_361..362` (cp 015 variants) |
| INCR | Adding a well-defined capability on top of a working base | Subsequent patch within same `.cob` | SB-07..SB-11 (unique) on top of SB-01..SB-06 |
| RETR | Retrograde / bottom-up planning choice | Explicit choice to solve from leaves up | `event_114` "bottom-up minimax over all reachable board states" (SB-13) |
| DBG | Diagnose a failure → read output → patch → recompile | Cycle of `cobc` + `./bin` + `apply_patch` after a failure | 3 times (F-01, F-02, F-03) |
| TEST | Running the binary against a known oracle | `./game15` / `/tmp/game15_tree --depth …` | `event_036, 080, 141, 211, 223, 298, 441` |
| REFA | Rename / restructure existing code | Minimal, no full-module refactor observed | (none material) |
| TOOL | Tooling / repo action (git init, commit) | `git` subcommands | 5× (OP-01..OP-05) |
| PROMPT | Self-prompting with an intermediate plan | Agent writes plan then writes file | `event_020, 065, 114, 253, 355, 430` |
| RISK | Explicit discussion of risk / non-trivial tradeoff | Reasoning block naming a tradeoff | `event_022` ("explicit backtracking rather than recursive self-calls"), `event_114` (retrograde vs memoised root-minimax) |
| VERIFY | Validating output format against the prompt's example | Full-tree run + `wc -l` + spot-check | `event_235-237` (12,134-line full tree), `event_298-300` (full tree with avoid) |

### B3 — Episode segmentation

- **Macro phases:** bootstrap (BL-01), feature-growth (BL-02/03/04), stabilisation (0 — no separate stabilisation phase), variant (BL-05), generalisation (BL-06).
- **Meso episodes:** one per BL (6 total).
- **Micro episodes:** 173 tool_use steps across all BLs. Breakdown: 20 `cobc`, 49 run-the-binary, 35 `sed/nl/rg` read, 15 `apply_patch`, 28 `git …`, 26 misc (ps, ls, python3 instrumentation).

### B4 — Per-BL strategy annotation

| BL | Strategy sequence | #build | #run | #DBG loops | Blockers & recovery |
|----|-------------------|--------|------|------------|---------------------|
| BL-01 | PLAN → SCAF → TEST → VERIFY | 1 | 1 | 0 | none |
| BL-02 | PLAN → RISK (choice of factorial-rank vs hash set) → INCR → TEST → VERIFY | 1 | 2 | 0 | none; oracle matched first try |
| BL-03 | PLAN → RISK (retrograde vs memoised root-minimax) → SCAF → DBG (F-01 `FILLED-TARGET` underflow) → DBG (F-02 stale `OWNER`) → TEST → VERIFY (12,134-line full tree) | 5 | 7 | 2 | two stalls diagnosed by adding Python instrumentation + rebuilding `/tmp` binary serially (was running in parallel with stale `/tmp` output) |
| BL-04 | PLAN → INCR (safe/bad split) → DBG (F-03 avoid-line indent) → TEST → VERIFY | 3 | 7 | 1 | stale-binary confusion again; agent explicitly notes "debug lines you see came from an older `/tmp` binary" |
| BL-05 | PROMPT ("duplicate then patch display only") → SCAF (`cp`) → INCR (`MOVE-LABEL` table + banner) → TEST | 2 | 3 | 0 | `apply_patch` failed once because initialisation-order differed between the two copied files; recovered by patching each file narrowly |
| BL-06 | PLAN → SCAF → TEST → INCR (pool listing + broader target-sum) → TEST → VERIFY | 3 | 6 | 1 (regression: rebuilt binary vs stale `/tmp/gameN`) | stale-binary confusion a third time |

**Recurring tactic:** Codex repeatedly fell into a "parallel compile + run against the old `/tmp` binary" trap. It self-diagnosed each time and made later runs sequential (`cobc … && /tmp/bin …`).

**SB-improvement pattern:** the only SB items that were *not* in response to an explicit UI are the choice of data structures (factorial-rank bitmap, retrograde state table, explicit per-level stack, `MOVE-LABEL` table) and defensive guards (`DEFAULT-WAS-CAPPED`, `ENUMERATION-MODE` skip, `ARGUMENT-ERROR`). All are architectural, not cosmetic.

### B5 — Outcome & quality rubric (0 = fail, 1 = partial, 2 = pass, NA = not assessable)

| BL | Q1 Correctness | Q2 Build/run | Q3 Test rigor | Q4 Robustness | Q5 Maintainability | Q6 Reproducibility | Confidence |
|----|----------------|--------------|---------------|---------------|--------------------|---------------------|------------|
| BL-01 | 2 (oracle matches) | 2 | 1 (one oracle) | 1 (no bad-input handling) | 2 | 2 | High |
| BL-02 | 2 (oracle matches) | 2 | 1 | 1 (requires spaces around `--unique`) | 1 (986,409-byte magic bitmap, LENGTH-OFFSET table is undocumented) | 2 | High |
| BL-03 | 2 (root is `[Draw]`; 12,134-line full tree) | 2 | 2 (full run + shallow spot-checks) | 2 | 2 (iterative DFS, retrograde solve — clean separation) | 2 | High |
| BL-04 | 2 (P1:1 avoid-set = 2,3,4,7 matches sibling REPLAY oracle) | 2 | 2 | 2 | 2 | 2 | High |
| BL-05 | 2 (counts identical, tree rendered with `0.0X`) | 2 | 1 (only `--unique` + shallow tree checked) | 2 | 2 (display-layer only diff) | 2 | High |
| BL-06 | 2 for `15 9` oracle; NA for `12 8` / `10 7` (not run) | 2 | 1 (classic case + 2 edge cases only) | 2 (validation, skip-path, capped default) | 2 | 1 (extended oracles missing) | Medium |

**Aggregate:** 11/12 BL×Q cells at 2/2 where applicable; 0 failures, 0 hangs in shipped code.

### B6 — COBOL capability panel

- **Compile status:** 20 `cobc -x -free <src>.cob` invocations, all clean after the first `game15.cob` scaffold (which also compiled first try). No warnings flagged in the session output.
- **Idioms used:**
  - `>>SOURCE FORMAT FREE` header for every file.
  - `OCCURS` with level-05 and level-15 nested tables (for 2-D tables like `SYMMETRY-VALUE(sym, n)` and `NODE-CHILD-MOVE(level, k)`).
  - `PERFORM … VARYING … UNTIL` for all loops; no `CALL … RECURSIVE`.
  - `STRING … WITH POINTER LINE-PTR` for line assembly.
  - `INSPECT TALLYING FOR ALL` for flag detection.
  - `FUNCTION TRIM / LENGTH / NUMVAL / MOD` intrinsics.
  - Early paragraph exits via `EXIT PARAGRAPH` inside `IF`.
  - Explicit re-initialisation block at program start (fighting non-deterministic storage layout — a cobc quirk the agent mitigates by zeroing everything).
- **Toolchain:** `cobc` (GnuCOBOL) free format; binaries placed in `/tmp/` during dev, only final `./game15` and `./game15_tree` ever sit at repo root (and are git-ignored).
- **Delta over time:** no idiom regression; each new `.cob` reuses the same idiom set. `game15_tree.cob` introduces explicit per-level stack tables, `gameN.cob` introduces data-driven triple storage — both strict supersets of the earlier idioms.

### B7 — Interaction demand analysis

- **UI density per BL:** exactly 1 feature prompt per BL (replay mode). Total 6 feature prompts + 5 tooling "commit" prompts + 1 env meta = 12.
- **Clarification cycles:** zero. No user follow-up, no clarification question from the agent.
- **Scope churn:** zero. Each prompt mapped 1:1 to the scope delivered.
- **Relation to quality:** the zero-churn flat interaction is a feature of replay-mode evaluation, not a measure of prompt quality — the agent was not confused, but also was not challenged to re-plan.

### B8 — Factors & claims (process tracing)

| Claim | Evidence FOR | Evidence AGAINST | Judgment |
|-------|--------------|-------------------|----------|
| Codex chose a more "mechanical" solver architecture than Claude Code (full retrograde + factorial-bitmap) | `BUILD-OUTCOME-TABLE` iterates 0..19683 *and* back down to filled=0, even when only reachable states matter; `SEEN-CANONICAL(986409)` sizes the bitmap to 9! + lower-length offsets, ignoring reachability | could be justified as simpler to prove correct | Supported — architecture prioritises easy-to-reason-about over memory-minimal |
| Codex avoids recursion even where legal | Every tree walk is an explicit `NODE-*` stack; comment at `game15_tree.cob:436` "Iterative DFS avoids relying on recursive CALL behavior in GnuCOBOL" | — | Supported; matches the sibling's choice too |
| Codex diagnoses its own bugs quickly | 3 bug fixes, mean time-to-fix < 5 min each; all found by reading output + adding Python instrumentation | F-02 took ~4 compiles before root-cause | Supported |
| The "stale /tmp binary" anti-pattern is recurrent for Codex | 3 distinct occurrences (BL-03, BL-04, BL-06); agent recognises it each time and switches to `cobc … && /tmp/bin …` | — | Supported; worth flagging as Codex-specific |

### B9 — Synthesis + recommendations + threats

**Patterns:**

1. Six user prompts → six clean BLs, one commit per macro unit (after the dev merged `--unique`+tree+avoid into one commit). Zero re-work at the BL level.
2. Architecture is uniformly "enumerate all, then cull" (986,409 bitmap, 19,683 state table) rather than "enumerate only reachable". Trades memory for simpler invariants.
3. Zero recursion: every walk is an explicit per-level stack. Consistent across all 5 programs.
4. Debug style: Python `<<'PY'` one-liners used as probes rather than adding COBOL `DISPLAY` instrumentation. `[T:event_184, 357]`

**Recommendations:**

- Capture the "stale /tmp binary" case into a repeatable replay-testing checklist.
- Add the `gameN 12 8` and `gameN 10 7` oracles to the replay pack so the Codex run has the same validation pressure as the Claude-Code sibling.

**Threats to validity:**

- Single session, single agent, single replay-pack source — n=1 per cell.
- Oracle in the replay pack is the *Claude-Code* output; if the Claude-Code sibling had a latent bug, both runs would pass together.
- "Same prompts produced same counts" is the only cross-agent equivalence check performed here; internal correctness could in principle differ on unreached paths.

---

## Cross-agent note (Codex vs Claude Code on the same replay pack)

Both projects received the same 6 prompts (confirmed by byte-compare against `output/backlogs/cobol-tictactoe/REPLAY_PROMPTS.md`). They produced functionally equivalent, oracle-matching outputs — but with **systematically different idioms and a different file set**.

### File set

| File | cobol-tictactoe (Claude Code) | game15-cobol-codex (Codex) |
|------|------------------------------|----------------------------|
| counter | `game15.cob` | `game15.cob` |
| tree | `game15tree.cob` (no underscore) | `game15_tree.cob` (underscore) |
| 0.15 counter | `game015.cob` | `game015.cob` |
| 0.15 tree | `game015tree.cob` | `game015tree.cob` |
| gameN | `gameN.cob` | `gameN.cob` |

Same 5-file set; Codex added an underscore in the tree program name. No extra files in either project.

### LOC comparison (production COBOL only)

| File | CC LOC | Codex LOC | Δ |
|------|--------|-----------|---|
| game15 | ~260 | 500 | +240 (Codex has larger per-file init blocks + the 986,409-entry bitmap declaration) |
| tree  | ~550 | 671 | +121 (Codex uses full retrograde table + explicit per-level stack) |
| game015 | ~260 | 501 | +241 |
| game015tree | ~550 | 685 | +135 |
| gameN | ~400 | 465 | +65 |
| **total** | **~2020** | **2822** | **+40 %** |

Codex is systematically heavier. The two biggest structural reasons:

1. **Symmetry dedup (BL-02).**
   - Claude Code: compute canonical form as "min of 8 symmetric images of the move sequence", then use a standard hash/set implementation.
   - Codex: same "min of 8 images", but hashes into a **986,409-byte static bitmap** indexed by a falling-factorial rank (`SEEN-CANONICAL PIC X OCCURS 986409`). This is unusual — Codex computes 9! + lower-length offsets and declares the full table up front. `[R:game15.cob:55-70, 381-407]`
2. **Optimal tree (BL-03).**
   - Claude Code: two-pass minimax with a base-3 **memoization table** populated lazily during top-down minimax.
   - Codex: **bottom-up retrograde analysis** over the full base-3 address space `[1, 19683]`, with validity + outcome tables filled in fill-count order before any printing begins. `[R:game15_tree.cob:227-243]`

Both converge on correct `[Draw]` / 31,896 outputs, but Codex's architectural preference is "fill the whole state space, then query"; Claude Code's is "memoize only what you visit".

### Idiom choices

| Aspect | Claude Code | Codex |
|--------|-------------|-------|
| Winning lines | Magic-triple string `"159168249258267348357456"` with REDEFINES | Direct tic-tac-toe lines, `IF OWNER(1)=CP AND OWNER(5)=CP AND OWNER(9)=CP` — 8 explicit IFs |
| Canonical dedup | sort-of-orbit + compact hash | min-of-orbit + 986,409-byte bitmap (factorial rank) |
| Minimax | lazy memoization on visit | eager retrograde over full 3^9 = 19,683 states |
| Tree walk | per-depth `BEST-VAL` + `IS-LAST` arrays (what CC called "explicit stack") | 7-field per-level node stack (`NODE-MOVE / NODE-STATE-ID / NODE-OUTCOME / NODE-CHILD-LIST / NODE-BAD-LIST / NODE-NEXT-CHILD / NODE-LAST`), more stack-like |
| 0.15 rendering | prefix `"0.0"` + digit, inline in existing printer | dedicated `MOVE-LABEL PIC X(4) OCCURS 9` lookup table |
| `--unique` flag parsing | direct string compare | `INSPECT … TALLYING FOR ALL " --unique "` with wrapper spaces |
| Default max in gameN | `max = target - 3` heuristic, agent commentary ("games tend to end in draws") | same heuristic, but *justified* in the reasoning block ("values above that cannot appear in any distinct winning triple") |
| Game character rules | qualitative commentary ("few / many triples → draws / quick") | omitted — Codex just lists triples and the pool |

### Replay-prompt pack influence

The replay pack visibly drove the structure:

- Same 6 PL entries (byte-identical), same 6 BLs, same file-count profile (5 `.cob`).
- Same 4 commit rhythm on `codex/game15` as the Claude-Code sibling's intended segmentation (Codex bundled PL-02 + PL-03 + PL-04 into one commit because the human user sent one `commit` between them; CC fired off its own commits mid-step).
- Same oracles used for validation (Codex checked `./game15` → 255,168 and `./game15 --unique` → 31,896; matches CC).

What the replay pack did **not** fix:

- Data structures (magic-triple string vs direct lines; lazy vs eager memoization; tiny hash vs 986,409-byte bitmap).
- Module boundaries within `gameN.cob` (Codex separates validation, rules, pool display, triple generation, enumeration; CC interleaves them).
- Display format details (CC's indent width, Codex's flat 4-char indent kept from the base tree).
- Commentary depth (CC adds domain commentary in `gameN`; Codex stays mechanical).

### Bottom line for the cross-agent comparison

Codex delivered the same six user-visible capabilities with the same file set but chose **eager, table-driven, memory-heavy architectures** where Claude Code chose **lazy, symbolic, memory-light idioms**. Both zero-hang, both oracle-correct, both zero-recursion, both explicit-stack for tree walks. The replay-prompt pack controlled *scope* perfectly (6 BLs → 6 BLs, same oracles); it did not homogenise *approach*.
