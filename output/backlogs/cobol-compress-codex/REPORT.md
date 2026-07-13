# Post-Session Backlog & Strategy Analysis Report

## cobpack — COBOL Columnar Record Packer
**Session date:** 2026-03-12 | **Agent:** Codex (GPT-5.4, openai) | **Analysis date:** 2026-03-20

---

# PHASE 0 — DISCOVERY

## 0.1 Project Identification

- **Repo root:** `/Users/mathieuacher/SANDBOX/cobol-compress-codex`
- **Primary language:** GNUCobol (free-format), with Python 3 test harness
- **Entry points:** `./cobpack` (compiled binary), `./build.sh` (build), `./run_tests.sh` (test)
- **Build system:** Single-line `cobc -x -free` compilation via `build.sh` [R:build.sh:1–4]
- **Test framework:** Shell-based harness (`run_tests.sh`) invoking compiled binary and Python trust scripts [R:run_tests.sh:1–186]
- **CI configs:** None
- **Git metadata:** No git repository (never initialized). No branches, commits, or remotes.

### Project Constraints

- **PC-001** [R:~/.codex/config.toml]: Codex configured with `model = "gpt-5.4"`, `personality = "pragmatic"`, `model_reasoning_effort = "xhigh"`. This project directory was not registered in `config.toml` trust settings.
- **PC-002** [T:session 019ce3b2:line 1]: Base instructions enforce pragmatic personality, concise communication, apply_patch for edits, `rg` for search, no interactive git, branch prefix `codex/`.
- **PC-003** [T:session 019ce3b2:line 5]: Sandbox mode `workspace-write` — filesystem restricted to workspace + writable_roots. Network access disabled.

## 0.2 Codex Session Artifacts

- **CODEX_HOME:** `~/.codex` (default; env var not set)
- **Selected session:** `~/.codex/sessions/2026/03/12/rollout-2026-03-12T21-17-16-019ce3b2-4167-7af2-b5eb-a080d8e1980c.jsonl`
- **Selection criteria:** Only session referencing `cobol-compress-codex` repo path (confirmed via `grep -rl`)
- **Session metadata:** ID `019ce3b2-...`, started 2026-03-12T20:17:16Z, CWD matches repo, originator=Codex Desktop, model=gpt-5.4, 851 JSONL events, ~15.9M total tokens

## 0.3 Candidate Milestones

1. **20:17** — Session opened on empty workspace [T:session 019ce3b2:line 1]
2. **20:18** — User submits MVP0 specification [T:session 019ce3b2:line 7–8]
3. **20:18–20:20** — Agent validates toolchain, experiments with binary I/O [T:lines 10–127]
4. **20:23–20:30** — Agent writes schema parser + main COBOL program + build/test scripts [T:lines 138–214]
5. **20:30–20:34** — First compile, runtime crashes, debug cycle (ORD bug, loop index collision, -O2 crash) [T:lines 224–357]
6. **20:34** — MVP0 `run_tests.sh` passes [T:line 359]
7. **20:38** — Turn 1 complete, final answer delivered [T:line 426]
8. **20:40** — User submits MVP1 specification (RLESP codec) [T:line 443]
9. **20:42–20:47** — Agent implements RLESP, fixes metadata offset bug, all tests pass [T:lines 446–589]
10. **20:47** — Turn 2 complete [T:line 593]
11. **20:53** — User requests trust suite [T:line 600]
12. **20:53–21:03** — Agent builds trust scripts, discovers and fixes 3 real bugs [T:lines 602–762]
13. **21:04** — Full suite passes, TRUST.md written, Turn 3 complete [T:line 848]

**No CP1 questions needed** — session identification is unambiguous and all evidence is accessible.

---

# PASS 1 — EXTRACTION

## A0) Human User Instruction Index (UII)

| UI-ID | Timestamp | Quote/Paraphrase | Category | Strength | Target | Mapped BL |
|-------|-----------|------------------|----------|----------|--------|-----------|
| UI-001 | 20:18:25Z | "COBPACK — MVP0 Specification (GNUCobol)" — full spec defining compress/decompress/info, CPC v0 format, schema parsing, build/test, acceptance criteria | FeatureRequest + AcceptanceCriteria + Tooling | Explicit imperative | Code + Tests + Build + Data | BL-001 through BL-006 |
| UI-002 | 20:40:17Z | "COBPACK — MVP1 Specification (adds real compression)" — RLESP codec, schema CODEC= option, CLI --codec, AUTO selection, new tests | FeatureRequest + AcceptanceCriteria | Explicit imperative | Code + Tests | BL-007, BL-008 |
| UI-003 | 20:53:18Z | "Produce a TRUST.md and extend the test suite to justify trust" — determinism, randomized round-trips, corruption/fuzz, CRC32, time budget | FeatureRequest + TestRequest + Documentation | Explicit imperative | Tests + Docs | BL-009 |

## A0b) Project Constraints Index (PCI)

| PC-ID | Source | Quote/Paraphrase | Type | Impact |
|-------|--------|------------------|------|--------|
| PC-001 | [R:~/.codex/config.toml] | model=gpt-5.4, personality=pragmatic, effort=xhigh | tooling | Model selection; high reasoning budget |
| PC-002 | [T:line 1] base_instructions | "You are Codex... deeply pragmatic, effective software engineer" + formatting rules + apply_patch requirement | style + tooling | Agent communication style, edit methodology |
| PC-003 | [T:line 5] sandbox_policy | workspace-write, no network access | safety | Cannot install packages or access remote resources |

## A1) Prompt Ledger

| PL-ID | Timestamp | Raw Snippet | Linked UI | Linked BL |
|-------|-----------|-------------|-----------|-----------|
| PL-ROOT | 20:18:25Z | "# COBPACK — MVP0 Specification (GNUCobol)..." (full spec, ~2000 words) | UI-001 | BL-001–BL-006 |
| PL-002 | 20:40:17Z | "# COBPACK — MVP1 Specification (adds real compression)..." (full spec, ~800 words) | UI-002 | BL-007–BL-008 |
| PL-003 | 20:53:18Z | "Produce a TRUST.md and extend the test suite to justify trust..." (~50 words) | UI-003 | BL-009 |

**PL-ROOT canonical replay prompt:** see README.md.

## A2) Session Overview

**One-liner:** A GNUCobol CLI tool (`cobpack`) that packs fixed-length record files into columnar CPC v0 containers with optional RLESP space-run compression, proven by a deterministic/randomized/fuzz test suite.

**Milestone timeline:** See Phase 0.3 above.

**Artifact inventory:**
- Production: `src/cobpack.cob` (1493 LOC), `src/cobpack_schema.cob` (528 LOC)
- Build: `build.sh` (4 LOC)
- Tests: `run_tests.sh` (186 LOC), `tests/trust_lib.py` (179 LOC), `tests/trust_determinism.py` (162 LOC), `tests/trust_randomized.py` (196 LOC), `tests/trust_fuzz.py` (193 LOC), `tests/trust_crc32.py` (44 LOC)
- Test fixtures: 7 schemas, 6 data files
- Docs: `TRUST.md` (120 LOC)
- Binary: `cobpack` (149KB, Mach-O arm64)

**How to run:**
```sh
./build.sh && ./run_tests.sh
```
Outputs "all tests passed" with elapsed_seconds. [L:run_1]

## A3) Feature Backlog (BL-###)

### BL-001 — CPC v0 Container: Compress/Decompress/Info
- **Type:** Feature
- **Source:** UI-001, PL-ROOT
- **Constraints:** PC-003 (no network)
- **User intent:** Build columnar record packing tool in COBOL
- **Acceptance criteria (explicit):** Round-trip byte-identical, determinism, clean exit codes 0–4, works for 0 records
- **Implementation:** Main COBOL program with 3 subcommands, binary container format with magic/version/descriptors/payloads
- **Evidence:** [R:src/cobpack.cob:1–1493] [T:lines 7–426] [L:run_1]
- **Validation:** 4 round-trip datasets + determinism + negative tests all pass [L:run_1]
- **DoD:** Yes — all 4 explicit acceptance criteria met

### BL-002 — Schema Parsing with Gap Synthesis
- **Type:** Feature
- **Source:** UI-001, PL-ROOT
- **User intent:** Parse schema files, handle gaps between fields
- **Acceptance criteria (explicit):** Fields must not overlap, must be within bounds, gaps allowed, decompression must be byte-identical
- **Acceptance criteria (INFERRED):** Gap bytes must be preserved through round-trip, requiring synthetic field generation
- **Implementation:** `COBPACK-SCHEMA-LOAD` subprogram with sort, validation, `__GAP_nnnn` synthesis
- **Evidence:** [R:src/cobpack_schema.cob:1–528]
- **DoD:** Yes

### BL-003 — CLI with Exit Codes
- **Type:** Feature
- **Source:** UI-001, PL-ROOT
- **User intent:** Clean CLI behavior with defined exit codes
- **Acceptance criteria (explicit):** Exit 0=success, 1=args/schema, 2=IO, 3=corrupt, 4=format
- **Evidence:** [R:src/cobpack.cob:28–33] (exit code constants), [R:run_tests.sh:123–175] (negative tests verify codes)
- **DoD:** Yes — all exit codes exercised in tests

### BL-004 — Empty Input File Support
- **Type:** Feature
- **Source:** UI-001, PL-ROOT
- **Acceptance criteria (explicit):** "Works for empty input file (0 records)"
- **Evidence:** [R:tests/data/empty.dat] (0 bytes), [R:run_tests.sh:96] (roundtrip_case_none "empty")
- **DoD:** Yes

### BL-005 — Build and Test Scripts
- **Type:** Tooling
- **Source:** UI-001, PL-ROOT
- **Acceptance criteria (explicit):** "build.sh → builds ./cobpack", "run_tests.sh → runs tests and exits non-zero on failure"
- **Evidence:** [R:build.sh:1–4] [R:run_tests.sh:1–186]
- **DoD:** Yes

### BL-006 — Test Datasets and Negative Tests
- **Type:** Test
- **Source:** UI-001, PL-ROOT
- **Acceptance criteria (explicit):** Small deterministic (RECORD_LEN=16), spaces-heavy, random bytes, overlap fail, bad size fail, bad magic/version fail
- **Evidence:** [R:tests/schema/] (7 files) [R:tests/data/] (6 files) [R:run_tests.sh:93–175]
- **DoD:** Yes — all specified datasets and negative tests present

### BL-007 — RLESP Codec with Per-Field/CLI/AUTO Selection
- **Type:** Feature
- **Source:** UI-002, PL-002
- **Acceptance criteria (explicit):** RLESP encoding (tag 0x00=literal, 0x01=space-run, MIN_RUN=4, MAX_LIT=65535), schema CODEC= override, CLI --codec, AUTO selection for type=X when size reduces, deterministic
- **Implementation:** Two-pass RLESP (analyze + write modes), codec resolution chain
- **Evidence:** [R:src/cobpack.cob:569–902] (encode), [R:src/cobpack.cob:1189–1317] (decode), [R:src/cobpack_schema.cob:254–277]
- **DoD:** Yes — all specified behavior implemented and tested

### BL-008 — MVP1 Test Extensions
- **Type:** Test
- **Source:** UI-002, PL-002
- **Acceptance criteria (explicit):** RLESP-win dataset, RLESP-lose dataset, corruption tests (invalid tag, truncated payload, decoded length mismatch), all MVP0 tests still pass
- **Evidence:** [R:run_tests.sh:98–175] [R:tests/schema/rlesp.schema] [R:tests/schema/rlesp_auto.schema] [R:tests/data/rlesp.dat]
- **DoD:** Yes

### BL-009 — Trust Suite with TRUST.md
- **Type:** Test/Documentation
- **Source:** UI-003, PL-003
- **Acceptance criteria (explicit):** (a) determinism proof-by-test, (b) randomized round-trip, (c) corruption/fuzz (no crash/hang), (d) CRC32 with tests, automated via run_tests.sh, time budget
- **Implementation:** 5 Python files + TRUST.md, integrated into run_tests.sh with 2-minute budget
- **Evidence:** [R:tests/trust_*.py] [R:TRUST.md] [R:run_tests.sh:177–183] [L:run_1]
- **Validation:** 3 CRC32 vectors + 256 random, 4 determinism witnesses x 5 repeats, 48 randomized cases, 72 fuzz cases, all in ~3s [L:run_1]
- **DoD:** Yes

## A3b) Reproducibility Ops

OMITTED — user did not request git/commit/push operations.

## A3c) Specification Backlog

See [SPECIFICATION_BACKLOG.md](SPECIFICATION_BACKLOG.md) — 18 SB entries covering all agent-implemented steps.

## A4) Replay Package

### BL-001 through BL-006 (MVP0)

**Raw replay:** Submit PL-ROOT text (the full MVP0 specification) to a Codex/GPT agent in an empty directory with GNUCobol installed.

**Canonical replay:** See README.md PL-ROOT canonical prompt.

**Preconditions:** GNUCobol (`cobc`) 3.x, macOS or Linux, Python 3.10+ for trust tests
**Inputs:** None (all generated from specification)
**Expected outputs:** `cobpack` binary, `build.sh`, `run_tests.sh`, `src/*.cob`, `tests/schema/*.schema`, `tests/data/*.dat`
**Validation:** `./run_tests.sh` exits 0, prints "all tests passed"
**Checkpoint:** File snapshot: 2 .cob files, 2 .sh files, 5 schemas, 5 data files

### BL-007–BL-008 (MVP1)

**Raw replay:** Submit PL-002 text after MVP0 is complete.

**Canonical replay:** See README.md PL-002 canonical prompt.

**Preconditions:** MVP0 complete and passing
**Expected outputs:** Modified `src/cobpack.cob` and `src/cobpack_schema.cob`, new `tests/schema/rlesp*.schema`, `tests/data/rlesp.dat`, updated `run_tests.sh`
**Validation:** `./run_tests.sh` exits 0 with RLESP tests

### BL-009 (Trust)

**Raw replay:** Submit PL-003 text after MVP1 is complete.

**Canonical replay:** See README.md PL-003 canonical prompt.

**Preconditions:** MVP1 complete
**Expected outputs:** `tests/trust_lib.py`, `tests/trust_*.py` (4 scripts), `TRUST.md`, updated `run_tests.sh`
**Validation:** `./run_tests.sh` exits 0, all trust metrics printed

## A5) Repo Quantification

Exclusions: `__pycache__/`, compiled `cobpack` binary.

| Category | Files | LOC |
|----------|-------|-----|
| Production (COBOL) | 2 | 2021 |
| Tests (Python) | 5 | 774 |
| Build/Tooling (Shell) | 2 | 190 |
| Documentation (Markdown) | 1 | 120 |
| Test fixtures (schema) | 7 | 24 lines |
| Test fixtures (data) | 6 | 1466 bytes |
| **Total** | **23** | **~3105** |

Entry points: `./cobpack` (main), `./run_tests.sh` (test runner), `./build.sh` (build).

[S:stats_run_1] — computed via `wc -l` and `wc -c` on all source files.

---

**PASS 1 COMPLETE**

Missing/ambiguous evidence:
- Agent reasoning tokens are encrypted; strategy analysis relies on observable commentary + tool calls only
- No git commits to anchor step boundaries precisely
- No `--verbose` output captured; internal container structure validated indirectly via round-trips

**No CP2 questions needed** — UI→BL mapping is unambiguous (3 user prompts → 9 BL items), acceptance criteria are explicit in the specifications, and step segmentation is adequate from session log.

---

# PASS 2 — INTERPRETATION

## B0) RQ Coverage Matrix

| RQ | Evidence Sources | Indicators | Output Section |
|----|-----------------|------------|----------------|
| RQ1: What strategies did the agent use? | Session commentary, tool calls | Strategy code sequences, loop counts | B2, B3, B4 |
| RQ2: What outcomes/quality? | Test results, code review | Rubric scores, bug count | B5, B6 |
| RQ3: What drove success/failure? | Bug timeline, recovery actions | Claims FOR/AGAINST | B8 |
| RQ4: How reproducible? | Replay package, missing artifacts | Checklist completeness | B9 |
| RQ5: Interaction demand? | UII, prompt count/density | UI distribution, clarification cycles | B7 |

## B1) Operational Definitions

- **Strategy**: observed via codebook codes applied to tool-call + commentary sequences
- **Outcome**: measured by rubric (0–2 per dimension) + objective signals (test pass/fail, build success)
- **Success factors**: claims with evidence FOR/AGAINST
- **Reproducibility**: checklist of artifacts + missing items + validation commands

## B2) Strategy Codebook

| Code | Name | Definition | Inclusion | Exclusion | Example |
|------|------|------------|-----------|-----------|---------|
| PLAN | Planning | Agent states intended approach before acting | Explicit plan/commentary | Post-hoc description | "First I'm checking the existing repo layout" |
| SCAF | Scaffolding | Creating project structure, directories, build scripts | File/dir creation for infrastructure | Production code creation | Creating build.sh, run_tests.sh, test fixtures |
| INCR | Incremental Build | Write code then compile to get feedback | Code write → compile cycle | Full test run | Write cobpack.cob → `cobc` → fix errors |
| RETR | Toolchain Research | Investigating unfamiliar APIs/runtime behavior | Reading docs, testing scratch programs | Using known patterns | Testing GNUCobol ORD/CHAR behavior with scratch.cob |
| DBG | Debugging | Diagnosing runtime failures via targeted tests | Isolating failures, examining output | Preventive hardening | `xxd` on output to find byte offset errors |
| TEST | Testing | Running test suite or individual tests | `./run_tests.sh`, `python3 tests/...` | Writing test code (=SCAF) | Running full suite after each change |
| REFA | Refactoring | Restructuring without behavior change | Code simplification noted in commentary | Bug fixes | "First draft was too clever for COBOL's paragraph model. Flattening." |
| TOOL | Tool Use | Using system tools for investigation | `lldb`, `xxd`, `nm`, `otool` | Standard build/test | Using `lldb` to diagnose -O2 crash |
| VERIFY | Verification | Confirming correctness after fix | `cmp`, `xxd` byte comparison, CRC check | Initial test runs | `cmp input.dat restored.dat` |
| RISK | Risk Management | Proactive safety measures | Buffer limits, timeout enforcement | Reactive fixes | Setting 1 MiB output limit |

User-driven work maps to BL/UI/PL. Agent-initiated decisions (SB-006 through SB-012) are internal quality improvements triggered by test failures.

## B3) Episode Segmentation

### Macro Phases

| Phase | Time Range | Episodes | BL Items |
|-------|-----------|----------|----------|
| Bootstrap | 20:17–20:20 | EP-001-01 to EP-001-03 | (prereq) |
| Feature Growth | 20:23–20:47 | EP-001-04 to EP-002-04 | BL-001 through BL-008 |
| Stabilization/Hardening | 20:53–21:04 | EP-003-01 to EP-003-06 | BL-009 + bug fixes |

### Key Episodes

**EP-001-01** (RETR): Agent checks workspace → empty. Validates GNUCobol toolchain.
**EP-001-02** (RETR→VERIFY): Binary I/O experiment with scratch programs. Confirms sequential file = raw bytes.
**EP-001-03** (PLAN): States multi-file design plan. Creates update_plan.
**EP-001-04** (SCAF→INCR): Writes schema parser, main program, build script, tests.
**EP-001-05** (DBG→DBG→DBG): First compile fails → fix. Runtime crash → -O2 removal. ORD bug → fix. Loop index collision → fix.
**EP-001-06** (TEST→VERIFY): Full suite passes. Cleanup. Final answer.

**EP-002-01** (PLAN): Reads existing code, maps change surface for RLESP.
**EP-002-02** (INCR): Edits schema parser + main program for codec support.
**EP-002-03** (DBG): Metadata offset validation failure → fix.
**EP-002-04** (SCAF→TEST): Add RLESP fixtures, update test runner, fix corruption test offsets → passes.

**EP-003-01** (RETR→SCAF): Investigates CRC32 in GNUCobol (scratch test), decides on Python approach.
**EP-003-02** (SCAF): Creates 5 Python trust test files.
**EP-003-03** (TEST→DBG): Runs trust tests → failures expose 3 real bugs.
**EP-003-04** (DBG): Isolates RLESP pending-space corruption bug. Fixes.
**EP-003-05** (DBG): Fixes synthetic gap RLESP safety and header offset.
**EP-003-06** (SCAF→TEST→VERIFY): Writes TRUST.md, runs full suite → passes.

## B4) Per-BL Strategy Annotation

### BL-001–006 (MVP0) — Turn 1
- **Strategy sequence:** RETR → RETR → PLAN → SCAF → INCR → DBG → DBG → DBG → TEST → VERIFY
- **DBG loop count:** 3 distinct debug cycles (compile error, -O2 crash, ORD/loop bugs)
- **Build/test runs:** ~8 compile attempts, ~3 full test runs
- **Blocking points:** (1) GNUCobol `-O2` optimization crash — recovered by removing flag; (2) 1-based ORD/CHAR — recovered by adding +1/-1 adjustments
- **Prompt tactics:** User provided exhaustive specification; agent needed zero clarification

### BL-007–008 (MVP1) — Turn 2
- **Strategy sequence:** PLAN → INCR → DBG → SCAF → TEST → DBG → TEST
- **DBG loop count:** 2 (metadata offset, corruption test byte offsets)
- **Build/test runs:** ~3 compile, ~4 test runs
- **Blocking points:** Metadata validation assertion on payload offsets — recovered by fixing header size calculation
- **Prompt tactics:** User provided similarly exhaustive spec; zero clarification needed

### BL-009 (Trust) — Turn 3
- **Strategy sequence:** RETR → SCAF → TEST → DBG → DBG → DBG → SCAF → TEST → VERIFY
- **DBG loop count:** 3 (CRC vector fix, RLESP corruption, header offset)
- **Build/test runs:** ~6 individual Python test runs, 2 full suite runs
- **Blocking points:** Randomized testing exposed real RLESP bug — agent traced through byte-level analysis to find pending-space flush corruption
- **Notable:** This turn's test-first approach *discovered* production bugs, demonstrating the value of randomized testing

### SB Agent-Initiated Patterns
The 6 agent-initiated SB items (SB-006, SB-007, SB-010, SB-011, SB-012, and the -O2 removal implicit in SB-003) all follow a consistent pattern: **TEST → failure observed → DBG (isolate) → fix → VERIFY**. The agent never introduced speculative hardening without test evidence.

## B5) Outcome & Quality Rubric

Scale: 0=absent, 1=partial, 2=full. NA=not applicable.

| BL | Q1 Correctness | Q2 Build | Q3 Test Rigor | Q4 Robustness | Q5 Maintainability | Q6 Reproducibility | Confidence |
|----|---------------|----------|---------------|---------------|--------------------|--------------------|------------|
| BL-001 | 2 | 2 | 2 | 1 | 1 | 2 | High |
| BL-002 | 2 | 2 | 2 | 2 | 1 | 2 | High |
| BL-003 | 2 | 2 | 2 | 2 | 2 | 2 | High |
| BL-004 | 2 | 2 | 2 | 2 | 2 | 2 | High |
| BL-005 | 2 | 2 | NA | 2 | 2 | 2 | High |
| BL-006 | 2 | 2 | 2 | 2 | 2 | 2 | High |
| BL-007 | 2 | 2 | 2 | 2 | 1 | 2 | High |
| BL-008 | 2 | 2 | 2 | 2 | 2 | 2 | High |
| BL-009 | 2 | 2 | 2 | 2 | 2 | 2 | High |

**Notes:**
- Q1 Correctness: All BL items pass their acceptance criteria; randomized + fuzz testing provides strong evidence
- Q2 Build: Single-command build, compiles cleanly
- Q3 Test Rigor: 48 randomized cases, 72 fuzz cases, 4 determinism witnesses x 5 repeats, known-vector CRC32
- Q4 Robustness: BL-001 gets 1 due to 1 MiB output limit; BL-007 gets 2 after the 3 bugs were fixed
- Q5 Maintainability: COBOL code is verbose but structured; BL-001 and BL-007 get 1 because the single-file 1493-LOC cobpack.cob could benefit from further modularization
- Q6 Reproducibility: All 2 — deterministic seeds, explicit timeouts, canonical prompts provided

## B6) COBOL Capability & Quality Panel

| Metric | Value | Evidence |
|--------|-------|---------|
| Compile status | Clean (0 warnings after fixes) | [L:run_1] build.sh exits 0 |
| Runtime status | Stable (no crashes with current build) | [L:run_1] all tests pass |
| COBOL idioms used | PERFORM VARYING, EVALUATE, subprogram CALL, FUNCTION ORD/CHAR, COMP/COMP-5, level-78 constants, dynamic file assignment | [R:src/cobpack.cob] |
| Lines of COBOL | 2021 (1493 + 528) | [S:stats_run_1] |
| Toolchain | cobc (GNUCobol 3.x), free-format source, `-x` for executable | [R:build.sh] |
| Binary I/O approach | ORGANIZATION IS SEQUENTIAL with PIC X(1) records — byte-at-a-time | [R:src/cobpack.cob:7–12] |
| Known limitations | 1 MiB output buffer, -O2 disabled, multi-pass input reading (once per field) | Session commentary |

**Delta over session:** COBOL code evolved from ~800 LOC (Turn 1 initial) → ~1200 LOC (Turn 1 final, post-bugfix) → ~2021 LOC (Turn 3 final, with RLESP and hardening). The 3 real bugs found in Turn 3 were fixed in the COBOL source.

## B7) Interaction Demand Analysis

### UI Distribution

| Category | Count | % |
|----------|-------|----|
| FeatureRequest | 3 | 60% |
| AcceptanceCriteria | 3 | 60% (embedded in feature requests) |
| TestRequest | 2 | 40% |
| Documentation | 1 | 20% |

(Categories overlap as each UI contains multiple types.)

### Instruction Strength Distribution

| Strength | Count |
|----------|-------|
| Explicit imperative | 3 (100%) |
| Suggestion | 0 |
| Question | 0 |

### UI Density per BL

| BL Range | UI Count | BL Count | Density |
|----------|----------|----------|---------|
| BL-001–006 | 1 (UI-001) | 6 | 6 BL per UI |
| BL-007–008 | 1 (UI-002) | 2 | 2 BL per UI |
| BL-009 | 1 (UI-003) | 1 | 1 BL per UI |

### Clarification Cycles
**Zero.** The user never asked a clarifying question, and the agent never requested clarification. Each prompt was a self-contained specification. This is notable: the 3 prompts were sufficient to produce ~3100 LOC of working COBOL + Python with a comprehensive test suite.

### Scope Churn
**None.** The user's second prompt (MVP1) was explicitly an *extension* of MVP0, not a revision. The third prompt (trust) added a new layer without modifying existing features. All 3 prompts were additive.

**Interpretation:** The zero-clarification, zero-churn pattern suggests the user prepared detailed specifications in advance. The high UI density for BL-001–006 (6 features from one prompt) indicates the user front-loaded the specification work. This is consistent with the user being an experienced engineer who knows exactly what they want.

## B8) Factors & Claims

### Claim 1: Exhaustive upfront specification reduces interaction rounds
- **FOR:** 3 turns, 0 clarification cycles, ~47 min total. User specs contained format bytes, exit codes, algorithm pseudocode. [T:lines 7, 443, 600]
- **FOR:** Agent's first commentary was already implementation-focused, not clarification-seeking
- **AGAINST:** None observed
- **Judgment:** Strongly supported

### Claim 2: Toolchain research (RETR) prevents cascading errors
- **FOR:** Agent spent ~2 min on binary I/O experiments before writing any production code, which prevented text-mode I/O bugs [T:lines 80–127]
- **FOR:** Agent tested ORD/CHAR behavior in isolation, caught 1-based indexing before it propagated widely
- **AGAINST:** The -O2 crash was not caught by research (discovered at runtime)
- **Judgment:** Supported with caveats

### Claim 3: Randomized testing discovers real bugs that scripted tests miss
- **FOR:** Turn 3's randomized suite exposed 3 real production bugs that all fixed scripted tests (Turn 1–2) missed [T:lines ~715–762]
- **FOR:** The RLESP pending-space bug was subtle (only triggers with specific space-run lengths followed by non-space bytes)
- **AGAINST:** None
- **Judgment:** Strongly supported

### Claim 4: Agent-initiated hardening stays evidence-driven
- **FOR:** All 6 agent-initiated fixes (SB-006, SB-007, SB-010–012, -O2 removal) were triggered by observed test failures, not speculative
- **AGAINST:** None
- **Judgment:** Strongly supported

### Claim 5: Single-session COBOL development is viable for ~2000 LOC
- **FOR:** Complete, tested implementation in 47 minutes
- **FOR:** Agent navigated GNUCobol-specific gotchas (ORD indexing, paragraph scope, argument handling)
- **AGAINST:** 1 MiB output limit is a workaround for environment instability, not a principled design choice
- **AGAINST:** -O2 removal sacrifices performance for stability
- **Judgment:** Supported; the implementation is functional but carries environment-specific compromises

## B9) Synthesis + Recommendations + Threats to Validity

### Patterns

1. **Specification-first workflow:** All 3 turns followed USER_SPEC → AGENT_RESEARCH → AGENT_IMPLEMENT → AGENT_DEBUG → AGENT_TEST → DONE. No negotiation phase.
2. **Debug-driven quality:** The agent discovered and fixed 6 bugs during development, 3 of which were found only through randomized testing in Turn 3.
3. **Monotonic progress:** No rollbacks, no scope reduction, no feature abandonment. Each turn strictly extended the previous.
4. **COBOL-specific challenges:** 1-based ORD/CHAR, paragraph scope for loops, -O2 instability — all required research or debugging episodes.

### Recommendations

1. **Initialize git** and commit at each BL boundary for reproducibility
2. **Address the 1 MiB limit** — consider streaming decompression or configurable buffer
3. **Re-enable optimization** — investigate the -O2 crash root cause (may be GNUCobol version-specific)
4. **Add field-name uniqueness validation** in schema parser
5. **Consider CI** (GitHub Actions with GNUCobol container) for cross-platform testing

### Threats to Validity

1. **Encrypted reasoning:** Agent reasoning tokens are encrypted in the session log. Strategy codes are inferred from observable commentary and tool calls only. Internal decision-making is opaque.
2. **No git history:** Step boundaries are approximate. A replayer cannot precisely reconstruct intermediate states.
3. **Single session:** No evidence of how the agent would handle specification ambiguity, conflicting requirements, or multi-session evolution.
4. **Platform specificity:** Session ran on macOS arm64; specification targets Linux. The -O2 crash may not reproduce on Linux.
5. **Observer effect:** The session was conducted with Codex Desktop's sandbox restrictions, which may have influenced implementation choices (e.g., the -O2 removal was partly motivated by sandbox debugging limitations).
6. **Token counting uncertainty:** Total tokens (~15.9M) include heavy caching (cached_input_tokens). Actual "novel" token processing is much lower.
