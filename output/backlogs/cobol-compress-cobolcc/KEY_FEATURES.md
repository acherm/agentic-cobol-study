# KEY_FEATURES.md -- cobol-compress-cobolcc (COBPACK)

## Preamble

COBPACK was commissioned as a pure-COBOL columnar packer/compressor for fixed-length record files. The Claude-Code-built replica distinguishes itself from its Codex sibling through a 3-file modular COBOL decomposition (cobpack + crc32 + rlesp) and a CRC32 subcommand implemented in COBOL rather than Python.

## Ranked table

| Rank | SB id | Title | Class | Depth | Effort | Score | Significance note |
|------|-------|-------|-------|-------|--------|-------|-------------------|
| 1 | SB-007 | Randomized round-trip fuzz (180 seeded cases) | VER | 3 | 2 | 6.0 | Generator-based property check across random schemas with gaps, codec overrides, 4 content modes. Found descriptor offset-bounds bug. |
| 2 | SB-008 | Corruption fuzz (mutation operators, 2s timeout, no-crash contract) | VER | 3 | 2 | 6.0 | Typed mutation model over CPC format with hard timeouts and signal-death detection. |
| 3 | SB-002 | CPC v0 container + main CLI (4 subcommands, gap synthesis, exit codes) | DOM | 3 | 2 | 6.0 | Self-describing binary container serialised byte-exactly in COBOL with CBL_* I/O, COMP-5 + REDEFINES. |
| 4 | SB-003 | RLESP codec as standalone COBOL subprogram (LINKAGE SECTION, two-pass) | ALG+LNG | 2 | 2 | 4.0 | Exercises COBOL's subprogram calling convention harder than Codex sibling's monolithic approach. |
| 5 | SB-004 | CRC32 as standalone COBOL subprogram (IEEE 802.3, CBL_XOR) | ALG+LNG | 2 | 2 | 4.0 | Production COBOL CRC32 — the feature the Codex sibling kept in Python. |
| 6 | SB-009 | Schema fuzz (adversarial garbage to --schema) | VER | 2 | 1 | 3.0 | Covers the schema input surface the Codex sibling's fuzz suite does not test. |
| 7 | SB-006 | Shell test harness with semantic assertions (323 LOC) | VER | 2 | 1 | 3.0 | Asserts semantic properties (AUTO < NONE for spaces; bad magic → exit 3; pinned golden CRC32). |
| 8 | SB-005 | Multi-file COBOL build (3 source files linked) | LNG | 2 | 1 | 3.0 | Exercises GnuCOBOL's multi-module compilation. Agent-initiated decomposition. |
| 9 | SB-010 | TRUST.md (216 LOC) with claims, evidence, limitations | DOM | 2 | 1 | 3.0 | Documents what the suite does and does not prove, including portability caveats. |
| 10 | SB-011 | Bug fixes driven by fuzz (descriptor offset-bounds guard) | PRF | 2 | 1 | 3.0 | Correctness-PRF: real bug found by fuzz, root-caused, fixed, pinned as regression guard. |

## Composition chains

1. Schema parser → CPC v0 container → NONE round-trip → RLESP codec → AUTO selection → CRC32 integrity
2. CPC v0 container → corruption fuzz → schema fuzz → bug fixes
3. Multi-file build → RLESP subprogram → CRC32 subprogram → CALL/LINKAGE interop
4. Shell harness → Python fuzz scripts → pinned golden CRC32 → TRUST.md claim

## Significance profile

| Class | Count (top 10) |
|-------|----------------|
| VER | 4 |
| DOM | 2 |
| ALG+LNG | 2 |
| LNG | 1 |
| PRF | 1 |

## Verdict

**Verification-centric hybrid with a language-achievement accent** — shares the Codex sibling's VER-dominated profile (VER=4/10) but adds a language-level dimension (LNG in 3 features) through the 3-file modular decomposition and the COBOL CRC32 subprogram.
