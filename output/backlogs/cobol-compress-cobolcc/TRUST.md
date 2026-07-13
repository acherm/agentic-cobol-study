# TRUST.md — COBPACK MVP1

This document justifies trust in `cobpack`. It lists the properties the
tool promises, shows which test in `run_tests.sh` proves each one, and
explains how to reproduce the evidence. If you change the container
format or a codec, the tests below must be updated in lock-step.

`./run_tests.sh` (after `./build.sh`) runs the whole suite. It finishes
in **under 10 seconds on a modern laptop** and under 2 minutes even on
modest hardware; nothing in the suite is slow or flaky.

---

## 1. Claims and how they are tested

### 1.1 Byte-identical round-trip

**Claim.** For any valid `(schema, input)` pair, `compress` followed by
`decompress` produces a file byte-identical to the original input —
regardless of codec (`NONE`, `RLESP`, `AUTO`), regardless of schema
gaps, regardless of record count.

**Evidence.**
- Canonical fixtures: `small`, `empty`, `spaces`, `random` — each
  round-tripped with `NONE`, `RLESP`, and the default `AUTO`.
- `tests/data/random.dat` guarantees every byte 0..255 appears, proving
  binary safety.
- `empty.dat` (0 records) exercises the zero-record and empty-buffer
  edge cases.
- `tests/schema/spaces_rlesp.txt` pins `CODEC=RLESP` per-field on
  `spaces.dat` and must still round-trip.

See `run_tests.sh`: sections `== MVP0 round-trip ==`, `== MVP1: RLESP
explicit ==`.

**Gap handling.** The spec allows schema gaps (bytes not claimed by any
user field). The parser auto-inserts implicit `__GAP_<n>__` fields of
type `X`/`NONE` to cover those bytes, so round-trip stays byte-identical
even for schemas that omit parts of the record. This is exercised by
the randomized fuzzer (below), which frequently produces gapped
schemas.

### 1.2 Determinism — proof by test

**Claim.** For a given `(schema, input, codec)`, the produced `.cpc`
bytes are identical across runs on the same host, and stable across
builds of the tool as long as the format and codecs are unchanged.

**Evidence, two layers.**

1. **Same-run equality (`== determinism ==`)**: for each canonical
   dataset, compress twice into two different paths and `cmp -s` the
   outputs. Any source of nondeterminism (e.g. iteration over a hash
   map, uninitialized memory leaking out) would show up here.

2. **Pinned golden CRC32 (`== pinned CRC32 of canonical containers
   ==`)**: `tests/golden/cpc_crc32.txt` lists the expected CRC32 of each
   canonical container (one row per `(dataset, codec)`). Each run
   re-compresses those fixtures, asks `cobpack crc32 --in <file>` for
   the checksum, and fails loudly on any divergence. A code change that
   accidentally perturbs the byte layout is immediately visible as a
   pinned-hash mismatch.

To regenerate the goldens intentionally (e.g. after a deliberate format
change), run the snippet at the top of `tests/golden/cpc_crc32.txt` and
commit the new values.

### 1.3 Randomized round-trip (broad coverage)

**Claim.** The round-trip works not just on the hand-crafted fixtures
but on arbitrary legal schemas and arbitrary record contents.

**Evidence (`== randomized round-trip fuzz ==`).**
`tests/scripts/fuzz_random.py` generates, for each of several pinned
seeds:

- random `RECORD_LEN` ∈ [1, 128]
- 1..6 fields with random non-overlapping offsets and lengths,
  deliberately sometimes leaving gaps
- random field types (`X` or `9`) and random per-field codec
  (`NONE`, `RLESP`, or unpinned so the CLI picks)
- random record counts ∈ [0, 200]
- record data drawn from one of four distributions: uniform random,
  spaces-heavy, full-byte-range, and per-record repeat

For every iteration we run `compress → decompress` and byte-compare
against the original. `run_tests.sh` runs 3 × 60 = 180 iterations across
three fixed seeds (≈2 seconds). For higher-assurance soak testing, the
script also accepts larger counts:

```sh
python3 tests/scripts/fuzz_random.py --iters 1000 --seed 42
```

Seeds make failures reproducible: the `FAIL ... iter=N` line is enough
to regenerate the exact failing schema+data.

### 1.4 Corruption / fuzz — predictable failure, no crash, no hang

**Claim.** For *any* byte sequence fed as `--in`, `cobpack decompress`
and `cobpack info` must terminate within a bounded time, must not die
from a signal (no `SIGSEGV`, no `SIGBUS`), and must exit with one of
the documented codes (`0`, `2`, `3`, or `4`).

**Evidence (`== corruption fuzz (no crash / no hang) ==`).**
`tests/scripts/fuzz_corrupt.py` starts from three valid containers
(NONE-coded, RLESP-coded, random-data) and, for each iteration, applies
one of six mutation operators (single-byte flip, zero, max, many-bit
flip, truncate, extend) before running both `decompress` and `info`
with a 2-second timeout.

Each run reports a histogram of exit codes; the suite fails on any
signal death (rc < 0 or rc ≥ 128) or any timeout. The script keeps the
seed fixed so a failure is reproducible.

Additionally, `== schema fuzz (parser robustness) ==`
(`tests/scripts/fuzz_schema.py`) feeds random or near-valid garbage to
`--schema` and asserts the same property for the compress path.

A deliberately regressed check — reverting the descriptor offset-bounds
guard in `READ-CPC-FILE` — was found by a single corruption iteration
(see git history for details). That bug was caught, fixed
(`FLD-OFFSET + FLD-LENGTH ≤ RECORD_LEN` now validated on read), and
pinned by this fuzz loop.

### 1.5 Optional: CRC32 subcommand

**Claim.** `cobpack crc32 --in FILE` emits `crc32: <8 lowercase hex>`
computed with the IEEE 802.3 polynomial (`0xEDB88320`, init
`0xFFFFFFFF`, xor-out `0xFFFFFFFF`), matching standard libraries.

**Evidence (`== CRC32 test vectors ==`).** The suite checks standard
test vectors:

| input                                             | expected      |
|---------------------------------------------------|---------------|
| (empty)                                           | `00000000`    |
| `a`                                               | `e8b7be43`    |
| `abc`                                             | `352441c2`    |
| `123456789`                                       | `cbf43926`    |
| `The quick brown fox jumps over the lazy dog`     | `414fa339`    |
| `bytes(range(256)) * 8`                           | `9f5edd58`    |

The CRC32 implementation is a standalone COBOL subprogram
(`src/crc32.cob`, `CRC32_COMPUTE`). It uses `CBL_XOR` for the 4-byte
XOR in the inner loop and builds the 256-entry lookup table lazily on
the first call.

---

## 2. Environment & portability notes

- Tested with **GnuCOBOL 3.2.0** on macOS/ARM64 (Darwin 24). The code
  calls `CBL_OPEN_FILE`, `CBL_CREATE_FILE`, `CBL_READ_FILE`,
  `CBL_WRITE_FILE`, `CBL_CLOSE_FILE`, `CBL_CHECK_FILE_EXIST`, and
  `CBL_XOR`. These are all GnuCOBOL built-ins and work on Linux.
- Container integers are **little-endian**. The implementation uses
  `USAGE COMP-5` (native byte order) plus `REDEFINES PIC X(n)` to emit
  the bytes. This is correct on every little-endian host (all x86, all
  ARM in practice). On a hypothetical big-endian host the byte order
  would invert and `.cpc` files would not be interoperable with this
  build — the test suite's pinned-hash check would flag it immediately.
- `CBL_*` file-I/O takes offsets/counts as big-endian `BINARY` fields
  (`PIC 9(n) USAGE BINARY`). The code reflects this and wraps it in
  `WRITE-BUF-A-CHUNKED` / `READ-BLOCKS-INTO-BUF-A`.
- We do not persist a format-level CRC in the container in MVP1. If
  that becomes a requirement, `CRC32_COMPUTE` already exists and can be
  wired into `WRITE-CPC-FILE` and `READ-CPC-FILE`.

---

## 3. Reproducing the evidence

```sh
./build.sh            # compiles src/*.cob into ./cobpack
./run_tests.sh        # full suite, exits non-zero on any failure
```

For a deeper soak (not in the default suite for time-budget reasons):

```sh
python3 tests/scripts/fuzz_random.py  --iters 2000 --seed <N>
python3 tests/scripts/fuzz_corrupt.py --iters 2000 --seed <N> \
        --source path/to/valid.cpc
python3 tests/scripts/fuzz_schema.py  --iters 2000 --seed <N>
```

All three scripts print `exits=...` histograms and fail with a
reproducible seed on any crash, hang, or unexpected divergence.

## 4. Exit-code contract

| code | meaning                                 |
|------|-----------------------------------------|
| 0    | success                                 |
| 1    | invalid CLI arguments or schema         |
| 2    | I/O error (open/read/write/alloc)       |
| 3    | corrupt container (bad magic/version,   |
|      | bad geometry, unknown codec)            |
| 4    | format/codec error (RLESP, payload      |
|      | mismatch, truncated payload)            |

The corruption fuzzer verifies every observed exit code lies in this
range.

## 5. Known limitations of MVP1

- Schema names longer than 64 bytes are rejected by the parser.
- Container format supports ≤ 256 fields (`C-MAX-FIELDS`) and
  `RECORD_LEN ≤ 65536` (`C-MAX-RECORD-LEN`). Both limits are enforced
  on read and on schema parse.
- Compression/decompression loads the whole input into memory. A 1 GiB
  input needs ≈ 2 GiB of RSS.
- Timing uses `ACCEPT ... FROM TIME` (HH:MM:SS.cc); it wraps at
  midnight and has 10 ms resolution. This is a reporting-only concern.
