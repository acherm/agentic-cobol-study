# SPECIFICATION_BACKLOG.md -- Agent-Centric Step-Wise Implementation

## Purpose

This document captures the **agent-centric** step-wise implemented capabilities of the `cobpack` project as produced by a Claude Code (claude-opus-4-6) session on 2026-04-16. Unlike a user-driven Feature Backlog, this backlog reflects **what the agent actually built, incrementally**, including agent-initiated improvements and prerequisites.

## Step Segmentation Method

No git history exists. Steps are derived from **session episode analysis** of the Claude Code JSONL session log. The session spanned 2026-04-16T05:42 through 2026-04-17T09:31. Episodes are segmented by tool-call clusters, Write/Edit sequences, and Bash build/test invocations.

---

## SB Entries

### SB-001 — Toolchain Validation
- **Category:** Tooling | **Provenance:** Prerequisite
- **Specification:** Verified GNUCobol (`cobc` 3.2.0) on macOS/ARM64.

### SB-002 — Main CLI Program with CPC v0 Container (cobpack.cob)
- **Category:** Capability | **Provenance:** User-driven
- **Specification:** `cobpack.cob` (1 790 LOC) implementing compress/decompress/info/crc32 subcommands, CPC v0 binary container, schema parsing with gap synthesis, CLI argument parsing, exit codes 0–4. Uses `CBL_OPEN_FILE`, `CBL_READ_FILE`, `CBL_WRITE_FILE` for byte-level binary I/O.

### SB-003 — RLESP Codec as Separate Subprogram (rlesp.cob)
- **Category:** Capability | **Provenance:** User-driven
- **Specification:** Standalone COBOL subprogram `rlesp.cob` (226 LOC) exposing `RLESP-ENCODE` and `RLESP-DECODE` via LINKAGE SECTION. Two-pass encode, tag-based format, MIN_RUN=4, AUTO selection.

### SB-004 — CRC32 as Separate Subprogram (crc32.cob)
- **Category:** Capability | **Provenance:** User-driven
- **Specification:** Standalone COBOL subprogram `crc32.cob` (110 LOC) exposing `CRC32_COMPUTE` via LINKAGE SECTION. IEEE 802.3 polynomial, 256-entry lookup table, CBL_XOR.

### SB-005 — Build Script (multi-file compilation)
- **Category:** Tooling | **Provenance:** User-driven
- **Specification:** `build.sh` compiles 3 source files: `cobc -x -free -o cobpack src/cobpack.cob src/crc32.cob src/rlesp.cob`.

### SB-006 — Test Harness and Fixtures
- **Category:** Test/Validation | **Provenance:** User-driven
- **Specification:** `run_tests.sh` (323 LOC) with round-trip, determinism, RLESP, CRC32 vectors, negative tests, pinned golden CRC32 values.

### SB-007 — Randomized Round-Trip Fuzz
- **Category:** Test/Validation | **Provenance:** User-driven
- **Specification:** `tests/scripts/fuzz_random.py` — 180 seeded cases across random schemas with gaps/codec overrides and 4 content modes.

### SB-008 — Corruption Fuzz
- **Category:** Test/Validation | **Provenance:** User-driven
- **Specification:** `tests/scripts/fuzz_corrupt.py` — mutation operators over CPC containers with 2-second timeout, no-crash contract.

### SB-009 — Schema Fuzz
- **Category:** Test/Validation | **Provenance:** User-driven
- **Specification:** `tests/scripts/fuzz_schema.py` — adversarial garbage to `--schema`, parser robustness (absent from Codex sibling).

### SB-010 — TRUST.md Documentation
- **Category:** Documentation | **Provenance:** User-driven
- **Specification:** Documents what the trust suite proves, portability notes, exit-code contract, known limitations.

### SB-011 — Agent-Initiated Bug Fixes
- **Category:** Quality/Hardening | **Provenance:** Agent-initiated
- **Specification:** Descriptor offset-bounds guard bug caught by fuzz loop and fixed in-session (TRUST.md:120–124).

---

## Cross-agent note

**vs. Codex sibling (`cobol-compress-codex`)**

- **File decomposition:** Claude Code: 3 files by algorithm axis (cobpack + crc32 + rlesp). Codex: 2 files by concern axis (cobpack + cobpack_schema). Orthogonal choices.
- **CRC32:** Claude Code implemented in production COBOL (`crc32.cob`). Codex implemented in Python only (test oracle).
- **Schema fuzz:** Claude Code adds `fuzz_schema.py` (schema-surface fuzzing) which Codex lacks.
- **Prompt structure:** Claude Code received 1 merged prompt (7 285 chars). Codex received 3 staged prompts across 12 interactions.
- **COBOL inter-module interface:** Claude Code uses 46 CALL statements + 4 LINKAGE SECTION declarations. Codex uses CALL for schema only.
- **LOC:** Claude Code 2 126 vs Codex 2 021 (+5%, mostly the standalone CRC32 subprogram).
