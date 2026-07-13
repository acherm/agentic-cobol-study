# SPECIFICATION_BACKLOG.md — Agent-Centric Step-Wise Implementation

## Purpose

This document captures the **agent-centric** step-wise implemented capabilities of the `cobpack` project as produced by a Codex (GPT-5.4) session on 2026-03-12. Unlike the user-driven Feature Backlog (in README.md), this backlog reflects **what the agent actually built, incrementally**, including agent-initiated improvements and prerequisites.

## Step Segmentation Method

Since no git history exists (repo was never initialized), steps are derived from **session episode analysis** of the Codex JSONL session log at `$CODEX_HOME/sessions/2026/03/12/rollout-...019ce3b2...jsonl` (851 events). Episodes are segmented by turn boundaries (3 turns) and stable compilation/test milestones within each turn. Limitation: without commits, step boundaries are approximate (based on timestamps and function-call clusters).

---

## SB Entries

### SB-001 — Toolchain Validation & Binary I/O Experiment
- **Step label:** INFERRED step 1 (Turn 1, ~20:18–20:20 UTC)
- **Category:** Tooling
- **Provenance:** Prerequisite
- **Mapping:** prerequisite for BL-001
- **Specification:** Verified GNUCobol (`cobc`) availability on macOS, confirmed that `ORGANIZATION IS SEQUENTIAL` with single-byte records provides raw binary I/O without delimiters, established that `FUNCTION ORD`/`FUNCTION CHAR` are 1-based.
- **Evidence:** [T:session 019ce3b2:lines 30–127] scratch programs compiled and tested with `xxd`
- **Validation:** Scratch binary written and byte-verified via `xxd`
- **Scope:** Discarded scratch files after validation

### SB-002 — Schema Parser Subprogram
- **Step label:** INFERRED step 2 (Turn 1, ~20:23–20:26 UTC)
- **Category:** Capability
- **Provenance:** User-driven
- **Mapping:** BL-001, UI-001
- **Specification:** `COBPACK-SCHEMA-LOAD` subprogram parses `RECORD_LEN=` and `FIELD <NAME> <OFFSET> <LENGTH> <TYPE>` lines, validates overlap/bounds, sorts fields by offset, synthesizes `__GAP_nnnn` fields for uncovered record ranges so decompression is byte-identical without separate gap metadata.
- **Evidence:** [R:src/cobpack_schema.cob:1–528]
- **Validation:** Compiled as part of multi-file build; exercised by all round-trip tests
- **Scope:** Handles comments, blank lines, out-of-order fields. Does not validate field-name uniqueness.

### SB-003 — Main CLI & CPC v0 Container (compress/decompress/info, NONE codec)
- **Step label:** INFERRED step 3 (Turn 1, ~20:27–20:34 UTC)
- **Category:** Capability
- **Provenance:** User-driven
- **Mapping:** BL-001, BL-002, BL-003, BL-004, UI-001
- **Specification:** `cobpack` binary with three subcommands: `compress --schema --in --out [--codec] [--verbose]`, `decompress --in --out [--verbose]`, `info --in`. CPC v0 binary container with 8-byte magic `COBPACK\0`, uint32 version=0, uint32 record_len, uint64 record_count, uint32 field_count, field descriptors (name_len uint16, name bytes, offset uint32, length uint32, type uint8, codec uint8, payload_offset uint64, payload_size uint64), then field payloads in columnar order. Exit codes: 0=ok, 1=args, 2=IO, 3=corrupt, 4=format.
- **Evidence:** [R:src/cobpack.cob:1–1493]
- **Validation:** [L:run_1] `./run_tests.sh` all tests passed
- **Scope:** 1 MiB output buffer limit for decompression. Reads input file multiple times (once per field for payload extraction).

### SB-004 — Build & Test Scripts
- **Step label:** INFERRED step 4 (Turn 1, ~20:30 UTC)
- **Category:** Tooling
- **Provenance:** User-driven
- **Mapping:** BL-005, UI-001
- **Specification:** `build.sh` compiles with `cobc -x -free -o cobpack src/cobpack.cob src/cobpack_schema.cob`. `run_tests.sh` builds, runs round-trip tests for 4 datasets (small, spaces, random, empty), determinism checks, negative tests (overlap schema, bad input size, bad magic, bad version), all with per-command timeouts.
- **Evidence:** [R:build.sh:1–4] [R:run_tests.sh:1–186]
- **Validation:** [L:run_1] passes in ~3 seconds

### SB-005 — Test Fixtures (schemas + data)
- **Step label:** INFERRED step 5 (Turn 1, ~20:30 UTC)
- **Category:** Test/Validation
- **Provenance:** User-driven
- **Mapping:** BL-006, UI-001
- **Specification:** 7 schema files (small, spaces, random, empty, overlap, rlesp, rlesp_auto) under `tests/schema/`, 6 data files (small.dat 80B, spaces.dat 96B, random.dat 256B, empty.dat 0B, rlesp.dat 1024B, bad_size.dat 10B) under `tests/data/`. Schemas exercise: gaps, numeric fields, full-record coverage, overlap detection, codec overrides.
- **Evidence:** [R:tests/schema/*.schema] [R:tests/data/*.dat sizes]

### SB-006 — Bug Fix: ORD/CHAR 1-Based Offset
- **Step label:** INFERRED step 6 (Turn 1, ~20:32 UTC)
- **Category:** Quality/Hardening
- **Provenance:** Agent-initiated (discovered during first run)
- **Mapping:** related to BL-001
- **Specification:** Fixed little-endian read/write routines to account for GNUCobol's 1-based `FUNCTION ORD` and `FUNCTION CHAR`. Previously all byte values were off by one.
- **Evidence:** [T:session 019ce3b2:line ~341]

### SB-007 — Bug Fix: Nested PERFORM Loop Index Collision
- **Step label:** INFERRED step 7 (Turn 1, ~20:33 UTC)
- **Category:** Quality/Hardening
- **Provenance:** Agent-initiated
- **Mapping:** related to BL-001
- **Specification:** Separated loop indices (`ws-jindex`, `ws-kindex`) for nested record/field iteration to avoid clobbering during payload serialization.
- **Evidence:** [T:session 019ce3b2:line ~344–356]

### SB-008 — RLESP Codec (encode + decode + AUTO selection)
- **Step label:** INFERRED step 8 (Turn 2, ~20:42–20:47 UTC)
- **Category:** Capability
- **Provenance:** User-driven
- **Mapping:** BL-007, BL-008, UI-002
- **Specification:** RLESP space-run encoding for 0x20 bytes with MIN_RUN=4, MAX_LIT=65535. Two-pass encode: analyze mode (size estimation) then write mode. AUTO selection compresses type=X fields with RLESP only when encoded size < raw size. Schema-level `CODEC=RLESP|NONE` overrides CLI `--codec`. Decoder validates tag bytes (0x00=literal, 0x01=space-run), block lengths, and decoded length == expected length.
- **Evidence:** [R:src/cobpack.cob:569–902] (encode) [R:src/cobpack.cob:1189–1317] (decode)
- **Validation:** round-trip tests with RLESP, AUTO selection tests, corruption tests

### SB-009 — Schema Codec Extension
- **Step label:** INFERRED step 9 (Turn 2, ~20:42 UTC)
- **Category:** Capability
- **Provenance:** User-driven
- **Mapping:** BL-007, UI-002
- **Specification:** Schema parser accepts optional 6th token `CODEC=NONE` or `CODEC=RLESP` per field line. Precedence: schema override > CLI `--codec` > AUTO.
- **Evidence:** [R:src/cobpack_schema.cob:254–277]

### SB-010 — Bug Fix: RLESP Pending Space Corruption
- **Step label:** INFERRED step 10 (Turn 3, ~21:03 UTC)
- **Category:** Quality/Hardening
- **Provenance:** Agent-initiated (discovered by randomized testing)
- **Mapping:** related to BL-007
- **Specification:** Fixed `rlesp-feed-byte`: when flushing pending spaces (< MIN_RUN) into the literal buffer, the current non-space byte was being overwritten. Added `ws-rle-saved-byte` to preserve it across the pending-space flush.
- **Evidence:** [T:session 019ce3b2:line ~780] [R:src/cobpack.cob:686–691]

### SB-011 — Bug Fix: Synthetic Gap Field RLESP Safety
- **Step label:** INFERRED step 11 (Turn 3, ~21:02 UTC)
- **Category:** Quality/Hardening
- **Provenance:** Agent-initiated
- **Mapping:** related to BL-007
- **Specification:** Synthetic gap fields (ws-field-synthetic=1) are now forced to CODEC-NONE to avoid RLESP corruption of gap bytes that may not be space-dominated.
- **Evidence:** [R:src/cobpack.cob:571–572]

### SB-012 — Bug Fix: PAYLOAD_OFFSET Header Size
- **Step label:** INFERRED step 12 (Turn 3, ~21:02 UTC)
- **Category:** Quality/Hardening
- **Provenance:** Agent-initiated
- **Mapping:** related to BL-001
- **Specification:** Fixed descriptor byte count calculation: header is 28 bytes (8 magic + 4 version + 4 record_len + 8 record_count + 4 field_count), not 24.
- **Evidence:** [R:src/cobpack.cob:544]

### SB-013 — Trust Library (`trust_lib.py`)
- **Step label:** INFERRED step 13 (Turn 3, ~20:57 UTC)
- **Category:** Test/Validation
- **Provenance:** User-driven
- **Mapping:** BL-009, UI-003
- **Specification:** Shared Python library with: `run_command()` (subprocess with timeout, signal detection, exit code validation), `crc32()` (pure-Python CRC32 implementation), `parse_container()` (binary CPC v0 parser for mutation-based fuzzing), `make_rng()` (seeded Random factory).
- **Evidence:** [R:tests/trust_lib.py:1–180]

### SB-014 — Determinism Proof-by-Test (`trust_determinism.py`)
- **Step label:** INFERRED step 14 (Turn 3, ~20:57 UTC)
- **Category:** Test/Validation
- **Provenance:** User-driven
- **Mapping:** BL-009, UI-003
- **Specification:** Compresses 4 witness cases 5 times each, asserts byte-identical containers, identical info output, identical CRC32, and successful round-trip decompression.
- **Evidence:** [R:tests/trust_determinism.py:1–162]

### SB-015 — Randomized Round-Trip Testing (`trust_randomized.py`)
- **Step label:** INFERRED step 15 (Turn 3, ~20:58 UTC)
- **Category:** Test/Validation
- **Provenance:** User-driven
- **Mapping:** BL-009, UI-003
- **Specification:** Generates 48 seeded random schemas and data (varying record length 1–64, record count 0–24, field count 1–6, gaps, types X/9, codec overrides, content modes: spaces/alpha/runs/random/digits). For each: compress twice (determinism), decompress (round-trip), CRC32 verify.
- **Evidence:** [R:tests/trust_randomized.py:1–196]

### SB-016 — Corruption/Fuzz Testing (`trust_fuzz.py`)
- **Step label:** INFERRED step 16 (Turn 3, ~20:59 UTC)
- **Category:** Test/Validation
- **Provenance:** User-driven
- **Mapping:** BL-009, UI-003
- **Specification:** 24 random garbage files + 48 targeted mutations (10 mutator types: magic, version, field_count_zero, record_len_zero, codec_invalid, payload_offset, payload_size, truncate, invalid_rlesp_tag, rlesp_mismatch). Each tested under 2s timeout. Asserts: no crash, no hang, no signal termination, non-zero exit on decompress.
- **Evidence:** [R:tests/trust_fuzz.py:1–193]

### SB-017 — CRC32 Reference Implementation (`trust_crc32.py`)
- **Step label:** INFERRED step 17 (Turn 3, ~20:59 UTC)
- **Category:** Test/Validation
- **Provenance:** User-driven
- **Mapping:** BL-009, UI-003
- **Specification:** Tests pure-Python CRC32 against known vectors (empty, "123456789", fox), stdlib `binascii.crc32`, all repository fixtures, and 256 seeded random byte strings.
- **Evidence:** [R:tests/trust_crc32.py:1–44]

### SB-018 — TRUST.md Documentation
- **Step label:** INFERRED step 18 (Turn 3, ~21:04 UTC)
- **Category:** Documentation
- **Provenance:** User-driven
- **Mapping:** BL-009, UI-003
- **Specification:** Documents what the trust suite proves (determinism, randomized round-trips, corruption safety, CRC32 oracle) and what it does not prove (formal correctness, exhaustive adversarial coverage). States implementation limits (1 MiB output, no in-container CRC).
- **Evidence:** [R:TRUST.md:1–120]
