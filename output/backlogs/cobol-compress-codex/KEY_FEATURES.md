# KEY_FEATURES.md — cobol-compress-codex (COBPACK)

## Preamble

COBPACK was commissioned as a pure-COBOL columnar packer/compressor for fixed-length record files: an MVP0 CLI (`compress`/`decompress`/`info`) over a CPC v0 binary container with a `NONE` codec, an MVP1 `RLESP` space-run codec with AUTO selection, and a Turn-3 "trust" layer (determinism, randomized round-trip, fuzz/corruption, CRC32 oracle). "Key feature" below means a delivered capability of depth >= 1, excluding pure infrastructure such as `build.sh` or test fixtures. The profile is strongly VER-weighted (the project's centre of gravity is verification hygiene) with substantial DOM work around the container/schema and a well-bounded ALG component for RLESP and CRC32.

## Ranked table

| Rank | SB/F id | Title | Class | Depth | Effort | Score | Evidence | Significance note |
|------|---------|-------|-------|-------|--------|-------|----------|-------------------|
| 1 | SB-015 | Randomized round-trip trust suite (48 seeded cases, varying schemas/content modes/codecs) | VER | 3 | 2 | 6.0 | `/Users/mathieuacher/SANDBOX/cobol-compress-codex/tests/trust_randomized.py`; REPORT.md B4 / Claim 3 | Not "just an algorithm": this is a generator-based property check that exercises compress/decompress/info across random schemas with gaps, codec overrides and content modes — and it actually *found three real COBOL bugs* (SB-010, SB-011, SB-012) that scripted tests missed. |
| 2 | SB-016 | Corruption / fuzz safety suite (24 garbage + 48 targeted mutations across 10 mutator classes, hard per-subprocess timeouts) | VER | 3 | 2 | 6.0 | `/Users/mathieuacher/SANDBOX/cobol-compress-codex/tests/trust_fuzz.py`; TRUST.md §3 | Goes well beyond "test the happy path": encodes a typed mutation model over the CPC format (magic, version, field_count, record_len, codec byte, payload offsets/sizes, truncation, invalid RLESP tag, length mismatch) and asserts the COBOL binary never hangs/crashes/signal-terminates — a verification bar most MVPs skip. |
| 3 | SB-003 | CPC v0 container format + main CLI (compress/decompress/info, columnar layout, exit codes 0–4) | DOM | 3 | 2 | 6.0 | `/Users/mathieuacher/SANDBOX/cobol-compress-codex/src/cobpack.cob` (1493 LOC); REPORT.md BL-001/003 | Depth is in the *domain modelling*, not an algorithm: designing a self-describing binary container (28-byte header + variable field descriptors + columnar payloads) and serialising/deserialising it byte-exactly in COBOL — a language with no pointers, no unions and no native little-endian helpers. The whole downstream suite hangs off this. |
| 4 | SB-008 | RLESP codec: two-pass encoder (analyze/write), decoder, AUTO selection | ALG | 2 | 2 | 4.0 | `src/cobpack.cob:569–902` (encode), `1189–1317` (decode) | RLE-for-spaces is textbook, so this is genuine ALG not DOM — but the two-pass analyze/write structure (to decide RLESP-vs-NONE by predicted size *before* emitting) plus MIN_RUN=4 / MAX_LIT=65535 block framing make it a non-trivial implementation in COBOL. Realised depth bounded by the algorithm's own simplicity. |
| 5 | SB-002 | Schema parser subprogram with gap synthesis (`__GAP_nnnn` fields, overlap/bounds validation, stable sort) | DOM | 2 | 2 | 4.0 | `/Users/mathieuacher/SANDBOX/cobol-compress-codex/src/cobpack_schema.cob` (528 LOC) | Pure domain modelling: the insight that uncovered record ranges must be materialised as *synthetic fields* so decompression is byte-identical without separate gap metadata is a design decision, not an algorithm. Validation (overlap, bounds, offset sort) and CODEC= extension (SB-009) live here. |
| 6 | SB-014 | Determinism proof-by-test (byte-identical `.cpc`, identical `info`, identical CRC, 4 witnesses × 5 reps) | VER | 2 | 1 | 3.0 | `/Users/mathieuacher/SANDBOX/cobol-compress-codex/tests/trust_determinism.py` | A named, evidence-based property (bitwise output stability) rather than a generic "re-run passes" check. Modest effort but it's the invariant the whole container relies on and it's checked across NONE, AUTO, schema-override and mixed-schema witnesses. |
| 7 | SB-017 | Pure-Python CRC32 reference + oracle vectors (known vectors + stdlib cross-check + 256 seeded random) | ALG | 2 | 1 | 3.0 | `/Users/mathieuacher/SANDBOX/cobol-compress-codex/tests/trust_crc32.py`, `tests/trust_lib.py` | Textbook CRC32 but double-anchored: against canonical test vectors *and* `binascii.crc32`. Used as an external integrity oracle across randomized/fuzz cases. Clearly ALG, not CMP — its depth comes from being a *trusted cross-check* not from the algorithm itself. |
| 8 | SB-013 | Trust library: subprocess harness, CPC v0 binary parser, seeded RNG factory | CMP | 2 | 1 | 3.0 | `/Users/mathieuacher/SANDBOX/cobol-compress-codex/tests/trust_lib.py` (180 LOC) | This exists only because SB-003 (CPC format) and SB-014/15/16 all need it: a shared `parse_container()` that re-reads the binary format in Python (mutation-aware), plus `run_command()` with timeout/signal detection. Composition-class: the "test infrastructure layer" the other three trust scripts plug into. |
| 9 | SB-009 | Per-field / CLI / AUTO codec-resolution chain (schema override > CLI `--codec` > AUTO heuristic) | DOM | 2 | 1 | 3.0 | `src/cobpack_schema.cob:254–277`; REPORT.md BL-007 | The feature itself is a small precedence ladder, but the *domain* choice — that a schema can pin `CODEC=RLESP` for a single field while the CLI defaults to AUTO, and that synthetic gap fields must be force-pinned to NONE (SB-011) — is real spec design, not glue. |
| 10 | SB-004+SB-005 | `run_tests.sh` harness (build + NONE round-trips + AUTO cases + schema-override + size assertion + negative exit-code tests + RLESP corruption tests + trust-suite dispatch with wall-clock budget) | VER | 2 | 1 | 3.0 | `/Users/mathieuacher/SANDBOX/cobol-compress-codex/run_tests.sh` (186 LOC) | The shell harness is more than infra: it asserts semantic properties (AUTO container < NONE container for spaces data; bad magic → exit 3; bad RLESP tag → exit 4; truncation → exit 4; RLESP length mismatch → exit 4) with a 2-minute global budget. It's the orchestrator that binds the verification stack together. |
| 11 | SB-010+SB-011+SB-012 | Test-driven COBOL bug hardening (RLESP pending-space corruption, synthetic-gap RLESP safety, PAYLOAD_OFFSET header-size fix) | PRF | 2 | 1 | 3.0 | REPORT.md EP-003-04/05; `src/cobpack.cob:544, 571–572, 686–691` | Not performance tuning — "correctness PRF": three real bugs found by the randomized suite, each root-caused by byte-level tracing and fixed in pure COBOL. Consolidated here because individually each is a single-line fix, but together they are the feedback loop that made the trust claim real. |
| 12 | SB-001 | GNUCobol binary-I/O capability study (ORGANIZATION SEQUENTIAL + PIC X(1) for raw bytes, 1-based ORD/CHAR) | LNG | 1 | 1 | 1.5 | REPORT.md EP-001-01/02; session lines 30–127 | Borderline, kept because it *qualifies* the whole project: establishing that byte-exact binary I/O is achievable in GNUCobol (a language where that is non-obvious) is the premise of SB-003. Low depth because the finding itself is ~3 lines of COBOL idiom, but it's a prerequisite language-level discovery. |

## Composition chains

1. **Schema parser → CPC v0 container → NONE round-trip → RLESP codec → AUTO selection**
   SB-002 → SB-003 → (SB-003 round-trip) → SB-008 → SB-009. AUTO selection is only meaningful because schema + container + a competing codec all exist: AUTO is the decision function over two codecs that must each already be correct.

2. **CPC v0 container → Python CPC parser → typed-mutation fuzz → COBOL bug fixes**
   SB-003 → SB-013 (`parse_container`) → SB-016 (10 mutator classes that target named container fields) → SB-010/011/012 (COBOL fixes). This is the chain that makes the project VER-heavy: the fuzzer can only mutate offsets/sizes/tags *because* there is an independent re-implementation of the format in Python, and the bugs it found fed straight back into the COBOL source.

3. **Schema parser → CPC v0 → CRC32 oracle → randomized generator → determinism check**
   SB-002 → SB-003 → SB-017 → SB-015 → SB-014. The randomized round-trip test is only possible once a schema generator and a container exist *and* there is an independent CRC32 the suite can trust to compare input vs restored bytes across 48 seeded cases.

4. **`build.sh` + `run_tests.sh` shell harness → trust_lib.py → four trust scripts → TRUST.md claim**
   SB-004 → SB-013 → SB-014/15/16/17 → SB-018. The TRUST.md claim ("no hang, no crash, deterministic, round-trip under randomized inputs, within a 2-minute budget") is an emergent property of the four underlying scripts plus the shell orchestrator with its enforced timeouts — none of the pieces alone would justify the claim.

## Significance profile

| Class | Count (top 12) | Notes |
|-------|----------------|-------|
| VER | 4 | SB-015, SB-016, SB-014, SB-004+SB-005 — dominant class; the project's centre of gravity. |
| DOM | 3 | SB-003 (container), SB-002 (schema + gap synthesis), SB-009 (codec resolution chain). |
| ALG | 2 | SB-008 (RLESP), SB-017 (CRC32). |
| CMP | 1 | SB-013 (trust_lib, only meaningful given the format + the three trust scripts). |
| PRF | 1 | SB-010+SB-011+SB-012 (correctness-PRF: iterative bug hardening driven by the fuzz suite). |
| LNG | 1 | SB-001 (GNUCobol raw-binary I/O enablement). |
| SYS | 0 | Minor only — Python↔COBOL boundary is via subprocess, not FFI. |
| INF | 0 | Present but deliberately excluded from "key features" (build.sh = 4 LOC; fixtures are data). |
| PRO | 0 | CPC is an in-house format; no published-spec compliance. |

## Verdict

**Verification-centric hybrid with a strong domain-modelling core** — the project is the most verification-hygienic of the COBOL set (VER = 4/12, plus a CMP test-infrastructure layer and a PRF fix cycle that is itself test-driven), built on a respectable DOM spine (SB-003 container + SB-002 schema) with a bounded ALG contribution (RLESP, CRC32). It is *not* algorithm-centric despite the "compressor" framing: the RLESP codec is the smallest of the three deep-depth pieces; the depth lives in the container, the schema, and — above all — in the trust suite.
