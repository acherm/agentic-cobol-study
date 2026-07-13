# Assessment — `cobol-compress-codex` — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> **`cobpack`** binary with three subcommands (`compress`, `decompress`, `info`), a CPC v0 / v1 container format, NONE + RLESP codecs with AUTO-selection, CRC32 integrity, and the trust suite — **70+ assertions passing in under 30 s** including multi-run SHA-256 determinism proofs and randomized round-trip coverage.

> A clean **MVP with explicit trust claims** — determinism proven by SHA-256 equality across runs, round-trip proven by fuzz-generated schemas + records. That is already 'production-tier verification hygiene' for an MVP.

**Difficulty (auto-labelled):** High (idx 0.55). **Active collaboration time:** 0 h 54 m. **Sessions:** 3. **Backlog entries discovered:** 18. **Git commits:** 1.

## 1. Contract — what was asked

COBPACK — pure-COBOL columnar compressor for fixed-record data. MVP0 = NONE codec + columnar container; MVP1 = RLESP (space-run) codec with AUTO selection; extend with CRC32 and a rigorous trust-by-test suite (determinism, randomized round-trip, corruption / fuzz).

Opening user prompt (verbatim, truncated):

```
# COBPACK — MVP0 Specification (GNUCobol) ## Goal (MVP0) Build a command-line tool `cobpack` that can: 1. **Package** a fixed-length record file into a `.cpc` container (field-wise / columnar layout) using only the `NONE` codec (no compression). 2. **Unpack** that `.cpc` back into the original file **byte-identical**. 3. Provide `info` about the container. This MVP0 proves: * toolchain mastery in COBOL (multi-file build, binary-safe I/O), * schema parsing, * container serialization/deserialization, * round-trip correctness, with minimal algorithmic risk. --- ## Inputs / Outputs ### Record input * `--in input.dat`: binary file with `N` records of exactly `RECORD_LEN` bytes * Validation: file size must be a multiple of `RECORD_LEN`, else error. ### Schema input (MVP0) Plain text, line-based.
```

## 2. Delivered — externally-observable evidence

**`cobpack`** binary with three subcommands (`compress`, `decompress`, `info`), a CPC v0 / v1 container format, NONE + RLESP codecs with AUTO-selection, CRC32 integrity, and the trust suite — **70+ assertions passing in under 30 s** including multi-run SHA-256 determinism proofs and randomized round-trip coverage.

**Executables present in `SANDBOX/cobol-compress-codex/`** (at least *something* built):

- `cobpack` (146 KB)

**COBOL surface exercised.** 2 COBOL file(s), 1,812 code lines, 77 paragraphs (≈ function-like units), 7 sections, mastery score **44** distinct constructs across **9/10** capability categories.

**Backlog (auto-mined).** 18 `F-###` / `SB-###` / `S#-##` entries in the harvested / subagent-generated `SPECIFICATION_BACKLOG.md`. Prompts also produced 168 sub-request bullets; git history carries 1 commits.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

**Mean score across 9 BLs and 6 criteria: 1.92/2** (Q1 corr. 2, Q2 build 2, Q3 tests 2, Q4 robust 1.89, Q5 maintain 1.67, Q6 repro 2).

| BL | Q1 corr. | Q2 build/run | Q3 tests | Q4 robust | Q5 maintain | Q6 repro | Conf |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `BL-001` | 2 | 2 | 2 | 1 | 1 | 2 | High |
| `BL-002` | 2 | 2 | 2 | 2 | 1 | 2 | High |
| `BL-003` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-004` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-005` | 2 | 2 | NA | 2 | 2 | 2 | High |
| `BL-006` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-007` | 2 | 2 | 2 | 2 | 1 | 2 | High |
| `BL-008` | 2 | 2 | 2 | 2 | 2 | 2 | High |
| `BL-009` | 2 | 2 | 2 | 2 | 2 | 2 | High |

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** Commercial fixed-record packers (mainframe DB utilities, Recognosco-class tools) are decades of engineering with multi-codec support, indexed access, streaming, concurrency, and encryption.

**Where this result sits.** A clean **MVP with explicit trust claims** — determinism proven by SHA-256 equality across runs, round-trip proven by fuzz-generated schemas + records. That is already 'production-tier verification hygiene' for an MVP.

**Why the ceiling is out of reach here — honest constraints (not failures):**

- Scope was explicitly MVP0+MVP1 — no LZ-class codecs, no streaming, no encryption.
- COBOL has no native streaming I/O primitives beyond file records; a 1 MiB decompression buffer cap is a reasonable MVP bound.

## 5. What's genuinely impressive (evidence-anchored)

- **Pure COBOL implementation of a byte-level binary container** — this is not the shape of problem COBOL is usually pointed at, and it works.
- Explicit `TRUST.md` framework (70 assertions across determinism / randomized / corruption / cross-codec classes) is a higher verification bar than most production MVPs of the same size.
- Specification-driven: user supplied the MVP0 / MVP1 spec up front, agent delivered them in order with a clean commit, low user-intervention rate (11 prompts total).

## 6. Honest gaps

- Only two codecs — LZ-family deferred.
- 1 MiB decompression buffer cap — file-based, no pipe streaming.
- No indexed / random access.

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 14.4% (38 errors / 263 tool outputs).
- Bug-report-style user prompts: 3.
- Redirect-style user prompts: 0.
- Share of active time spent on `bug_fix`: 0.4% (0 min of 54 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/cobol-compress-codex`
- Sessions: 3 (primary agent: Codex gpt-5.4)
- Git history: 1 commits available in `/Users/mathieuacher/SANDBOX/cobol-compress-codex/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/cobol-compress-codex/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/cobol-compress-codex__*.jsonl`.

## 8. Final take

**A clean **MVP with explicit trust claims** — determinism proven by SHA-256 equality across runs, round-trip proven by fuzz-generated schemas + records.** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/cobol-compress-codex.json`, `output/backlogs/cobol-compress-codex/appendix.json` (when present), `output/complexity/cobol-compress-codex.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
