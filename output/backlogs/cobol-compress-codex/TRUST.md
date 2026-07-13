# TRUST.md

`cobpack` MVP1 is trusted here by executable evidence, not by inspection alone.

## How trust is established

Run:

```sh
./run_tests.sh
```

The suite is deterministic and bounded.

- Default wall-clock budget: `< 2 minutes`
- Enforced by `run_tests.sh` via `TRUST_MAX_MINUTES` and per-command timeouts
- Randomized tests use fixed seeds
- Fuzz tests use fixed seeds and bounded subprocess timeouts

## What the suite proves

### 1. Determinism proof-by-test

`tests/trust_determinism.py` compresses the same witness cases multiple times and requires:

- identical `.cpc` bytes across repeated runs
- identical `info` output across repeated runs
- identical restored bytes after decompression

Witnesses include:

- fixed `NONE` cases
- `AUTO` selection cases
- schema-level codec override
- a generated mixed-schema case

### 2. Randomized round-trip testing

`tests/trust_randomized.py` generates seeded random schemas and data, then checks:

- `compress` twice -> identical containers
- `decompress` -> byte-identical restore
- CRC32(input) == CRC32(restored)
- `info` succeeds on produced containers

The generator varies:

- record length
- record count, including `0`
- field count, gaps, offsets, and lengths
- field types `X` and `9`
- schema codec overrides
- CLI codec mode `NONE`, `RLESP`, `AUTO`
- binary payloads, digits, alphabetic content, and space-heavy regions

### 3. Corruption and fuzz safety

`tests/trust_fuzz.py` builds valid seed containers and then creates seeded corruptions:

- invalid magic
- invalid version
- invalid field count
- invalid record length
- invalid codec byte
- bad payload offsets
- bad payload sizes
- truncation
- invalid `RLESP` tags
- `RLESP` decoded-length mismatches
- random garbage files

Each corrupted case is run through `info` and `decompress` under a hard timeout.

The trust claim is:

- no crash
- no hang
- no signal termination
- corruption is rejected predictably with non-success exits on `decompress`

Note:

- `info` is metadata-oriented, so payload-only corruption may still allow `info` to succeed. That is expected because CPC v0 has no CRC.

### 4. Optional CRC32 reference implementation

`tests/trust_crc32.py` contains a pure-Python CRC32 implementation used as an extra integrity oracle.

It is tested against:

- known vectors
- Python stdlib CRC32
- repository fixtures
- seeded random byte strings

CRC32 is not part of the CPC v0 format in this repository. It is a trust aid for the test suite.

## What a passing suite does not prove

A green run does not prove:

- formal correctness
- absence of all malformed-container bugs
- resistance to adversarial resource exhaustion beyond the configured limits
- support beyond the current implementation bounds

Current important implementation limits:

- decompression reconstructs into memory and enforces a 1 MiB output limit in `src/cobpack.cob`
- CPC v0 still has no in-container checksum or CRC field

## Why this is still useful

For MVP1, the suite gives strong practical evidence that:

- the CLI is stable
- outputs are reproducible
- `RLESP` works on real and generated cases
- random schemas/records round-trip correctly
- malformed inputs fail quickly and predictably instead of hanging
