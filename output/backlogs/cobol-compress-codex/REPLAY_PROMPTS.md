# Replay Prompts

Reusable prompts for reproducing the `cobpack` COBOL columnar record packer step by step. Each prompt is self-contained enough to copy-paste into a coding agent session. They specify **what** to build (behavior, inputs, outputs, verification), not **how** (no algorithm names, no data structure prescriptions, no COBOL-specific idioms).

Use them sequentially: each step builds on the previous one.

For reference on what was actually built (codec internals, bugs encountered, autonomous decisions), see [SPECIFICATION_BACKLOG.md](SPECIFICATION_BACKLOG.md).

---

## Step 1: CPC v0 Container and CLI (MVP0)

> Build a command-line tool written in GNUCobol (`cobc`) called `cobpack` that packs a file of fixed-length records into a columnar binary container and can unpack it byte-identically. Target Unix-like systems (macOS or Linux) and free-format COBOL source.
>
> Provide three subcommands:
> - `compress --schema <path> --in <path> --out <path> [--codec <mode>] [--verbose]`
> - `decompress --in <path> --out <path> [--verbose]`
> - `info --in <path>`
>
> A **schema file** is plain text describing the fixed-length record layout:
> - One line `RECORD_LEN=<N>` giving the record length in bytes
> - Zero or more `FIELD <NAME> <OFFSET> <LENGTH> <TYPE>` lines (TYPE is `X` for bytes or `9` for digits)
> - Comments (lines starting with `#`) and blank lines are allowed
> - Fields may leave gaps between or around them; fields must not overlap and must fit inside the record
>
> Example schema (gaps are intentional):
> ```
> # Includes gaps so the container must preserve non-field bytes too.
> RECORD_LEN=16
> FIELD ID 0 4 X
> FIELD NAME 4 4 X
> FIELD NUM 10 2 9
> ```
>
> The **CPC v0 container format** must be a deterministic little-endian binary file with:
> - An 8-byte magic `COBPACK\0`
> - A `uint32` version set to `0`
> - A `uint32` record length
> - A `uint64` record count
> - A `uint32` field count
> - A descriptor per field containing: `uint16` name length, the name bytes, `uint32` offset, `uint32` length, `uint8` type, `uint8` codec, `uint64` payload offset (absolute position in the container), `uint64` payload size
> - The field payloads concatenated in columnar order (all of field 1's bytes across every record, then field 2's, etc.)
>
> The gap bytes between declared fields must survive a round-trip byte-identically. Choose any mechanism you like for this, but there must be no separate "gap metadata" side-channel outside the schema/container you already define.
>
> For this step only one codec is needed: `NONE` (payloads stored verbatim).
>
> **Exit codes** (must be exercised by tests):
> - `0` — success
> - `1` — bad arguments, unreadable/invalid schema (including overlap), or input size not a multiple of `RECORD_LEN`
> - `2` — generic I/O failure
> - `3` — container is corrupt (bad magic, bad version, structural inconsistency detected during decode)
> - `4` — payload format error
>
> **Acceptance criteria:**
> - `compress` then `decompress` yields a file byte-identical to the input (verified with `cmp`)
> - Running `compress` twice on the same inputs produces byte-identical container files (determinism)
> - `info` prints human-readable metadata including the per-field codec (the string `codec=NONE` must appear for a `NONE`-coded field)
> - An input file of 0 bytes (0 records) compresses and decompresses cleanly
> - An overlapping schema is rejected with exit `1`
> - An input whose byte size is not a multiple of `RECORD_LEN` is rejected with exit `1`
> - A container with its first magic byte flipped is rejected by `decompress` with exit `3`
> - A container with its version byte bumped to a non-zero value is rejected by `decompress` with exit `3`
>
> Deliver `src/` with the COBOL sources, `build.sh` that compiles the binary to `./cobpack`, and a single `cobpack` binary after build.

---

## Step 2: Test Harness, Fixtures, and Negative Tests

> Add a `run_tests.sh` script and `tests/` fixtures that exercise every acceptance criterion from Step 1.
>
> **Fixtures (under `tests/`):**
>
> Schema files in `tests/schema/`:
> - `small.schema` — `RECORD_LEN=16` with a few fields and intentional gaps (see Step 1 example)
> - `spaces.schema` — a single record-wide `X` field, useful as a spaces-dominated fixture
> - `random.schema` — a single record-wide `X` field over a short record length (e.g. `RECORD_LEN=16`)
> - `empty.schema` — valid schema for a zero-record file
> - `overlap.schema` — **invalid**: two fields whose byte ranges overlap
>
> Data files in `tests/data/`:
> - `small.dat` — 80 bytes (5 records of 16) matching `small.schema`
> - `spaces.dat` — 96 bytes, mostly ASCII spaces
> - `random.dat` — 256 bytes of arbitrary binary content
> - `empty.dat` — 0 bytes
> - `bad_size.dat` — 10 bytes (intentionally not a multiple of 16, for the "bad size" negative test)
>
> **`run_tests.sh` must:**
> 1. Invoke `build.sh` first.
> 2. Enforce a per-subprocess timeout using `timeout` or `gtimeout`; fail the suite if either is missing.
> 3. Enforce an overall wall-clock budget (reasonable default, around 2 minutes, configurable via an env var).
> 4. For each of `small`, `spaces`, `random`, `empty`:
>    - `compress --codec NONE` twice and assert the two containers are byte-identical (determinism)
>    - `decompress` once and assert `cmp` of original vs. restored passes
>    - `info` and assert `codec=NONE` appears in the output
> 5. Run the three negative tests: overlap schema (expect exit `1`), `bad_size.dat` with `small.schema` (expect exit `1`), bad-magic container (expect exit `3`), bad-version container (expect exit `3`). Use `dd`/`printf` with `conv=notrunc` to mutate bytes in a valid container.
> 6. Fail fast and print `"all tests passed"` plus elapsed seconds on success.
>
> The whole suite must complete in well under the configured budget (a few seconds is typical for this MVP). Exit non-zero on any failure.

---

## Step 3: Add a Space-Run Codec (MVP1)

> Extend `cobpack` with a second codec that compresses runs of ASCII space (`0x20`) bytes inside field payloads. Call it `RLESP` in the container's codec byte and in user-facing output. Payload framing is up to you — pick an encoding that:
> - Stores short space runs literally when a run is too short to pay for overhead (choose a minimum run length; around 4 is reasonable)
> - Bounds any literal block by a 16-bit length (so no single literal block exceeds 65535 bytes)
> - Can be decoded strictly: the decoder must detect invalid tag bytes, truncated blocks, and decoded-length mismatches and reject them with exit `4`
>
> **Schema extension:** each `FIELD` line accepts an optional 6th token of the form `CODEC=NONE` or `CODEC=RLESP`. Example:
> ```
> RECORD_LEN=16
> FIELD PAD 0 16 X CODEC=RLESP
> ```
>
> **CLI extension:** `compress` accepts `--codec NONE|RLESP|AUTO`. Precedence of codec selection per field, highest wins:
> 1. Per-field `CODEC=` in the schema
> 2. The `--codec` CLI flag
> 3. `AUTO`: pick `RLESP` only for `X`-typed user fields **and only when** the RLESP-encoded payload is strictly smaller than the raw payload; otherwise fall back to `NONE`
>
> Synthetic gap bytes (however you represent them internally) must not be RLESP-encoded — always store gaps losslessly with `NONE` regardless of the CLI/schema request.
>
> **Acceptance criteria:**
> - Every Step 1 / Step 2 test still passes unchanged.
> - On a spaces-heavy dataset (e.g. a 1024-byte file of 16-byte records dominated by spaces, packed with a single 16-byte `X` field), `--codec AUTO` must pick `RLESP` (confirmed by `codec=RLESP` in `info`) and the resulting container must be strictly smaller than the `--codec NONE` container for the same input.
> - On a random-bytes dataset, `--codec AUTO` must **not** pick `RLESP`.
> - A per-field schema `CODEC=RLESP` overrides `--codec NONE`: the container's codec byte for that field must still be `RLESP`.
> - Round-trip correctness and determinism hold for every codec combination.
> - Decoding a container whose RLESP stream has been mutated (invalid tag byte, truncated by one byte at the end, or a length field altered so the decoded output length no longer matches the expected field size) must exit with code `4` and must not crash, hang, or terminate by signal.

---

## Step 4: MVP1 Test Extensions

> Add these fixtures and tests, wired into `run_tests.sh`. All earlier tests must still pass.
>
> **New fixtures:**
> - `tests/schema/rlesp.schema` — one 16-byte `X` field with `CODEC=RLESP`
> - `tests/schema/rlesp_auto.schema` — one 16-byte `X` field with no codec token (for AUTO testing)
> - `tests/data/rlesp.dat` — 1024 bytes of 16-byte records, content designed so RLESP wins (spaces-dominant, with some non-space bytes mixed in)
>
> **New test cases in `run_tests.sh`:**
> - AUTO on the spaces-dominant dataset: compress twice (determinism), decompress and `cmp`, and assert `info` shows `codec=RLESP`.
> - AUTO on `random.dat` with `random.schema`: assert `info` does **not** show `codec=RLESP`.
> - Schema override: `--codec NONE` combined with `rlesp.schema` on `rlesp.dat` must still produce `codec=RLESP` in `info`.
> - Size comparison: same dataset compressed once with `--codec NONE` and once with `--codec AUTO` — assert the AUTO output is strictly smaller.
> - Three corruption negative tests, each expected to exit `4`:
>   - Flip one byte inside the RLESP payload so its tag becomes invalid.
>   - Truncate the container by one byte.
>   - Mutate a length word inside an RLESP block so the decoded length no longer matches the expected field size.
>
> Every mutation should use `dd`/`printf` with `conv=notrunc` on a previously generated valid container. Use per-command timeouts; no test may hang on corrupted input.

---

## Step 5: Trust Suite — Determinism, Randomized, Fuzz, CRC32

> Add a Python trust suite that provides executable evidence of correctness and robustness beyond scripted fixtures. Put all scripts under `tests/` and wire them into `run_tests.sh` after the shell-level tests.
>
> Requirements (language: Python 3.10+, no third-party dependencies):
>
> **Shared library `tests/trust_lib.py`:**
> - A subprocess helper that runs a `cobpack` command with a hard timeout, detects signal termination, and lets callers assert on exit code.
> - A pure-Python CRC32 (do not rely on `zlib`/`binascii` for the implementation itself — those are for cross-checking).
> - A binary parser that reads a CPC v0 container back into a structured form (header + field descriptors + raw payloads) so fuzz tests can target specific bytes.
> - A seeded `random.Random` factory so every randomized test is reproducible.
>
> **`tests/trust_crc32.py` — CRC32 oracle self-test:**
> - Assert your CRC32 matches stdlib CRC32 on: the empty string, `"123456789"`, the classic "quick brown fox" sentence, every fixture under `tests/data/`, and ~256 seeded random byte strings of varied lengths.
>
> **`tests/trust_determinism.py` — determinism proof-by-test:**
> - Pick at least 4 witness cases covering: a fixed `NONE` case, an `AUTO` case, a schema-level codec override case, and a generated mixed case.
> - Compress each witness 5 times and assert byte-identical container files, byte-identical `info` stdout, and byte-identical restored files with matching CRC32.
>
> **`tests/trust_randomized.py` — randomized round-trips:**
> - Generate around 48 seeded cases, varying: record length (1–64), record count (including 0), field count (1–6), gaps, field types (`X` and `9`), per-field codec overrides, CLI codec mode, and data content mode (all spaces, alphabetic, space-run heavy, pseudo-random binary, digits).
> - For each case: compress twice (identical bytes), decompress (byte-identical restore), `info` succeeds, and input CRC32 equals restored CRC32.
>
> **`tests/trust_fuzz.py` — corruption / fuzz safety:**
> - Build valid seed containers, then produce around 48 targeted mutations covering at least: bad magic, bad version, zeroed field count, zeroed record length, invalid codec byte, bogus payload offset, bogus payload size, trailing truncation, invalid RLESP tag, and RLESP decoded-length mismatch.
> - Also run around 24 completely random garbage files of varied sizes through `info` and `decompress`.
> - For every input: run under a short timeout (e.g. 2 s). Assert the process does **not** crash, does **not** hang, and is **not** killed by a signal. On `decompress`, a non-success exit is required; on `info`, payload-only corruption may still succeed (this is expected because CPC v0 has no in-container checksum).
>
> **Integration:** `run_tests.sh` invokes the four Python scripts with a per-script timeout and enforces the overall wall-clock budget. On a typical laptop the full suite (shell + Python) should finish in just a few seconds. No randomized test may use an unseeded RNG.

---

## Step 6: TRUST.md

> Write `TRUST.md` at the repo root. Describe what the test suite proves and what it does not prove, in plain language.
>
> Cover at minimum:
> - How to run it (`./run_tests.sh`) and the wall-clock budget + the env var that controls it.
> - The four trust pillars with one short section each: determinism, randomized round-trip, corruption/fuzz safety, CRC32 oracle.
> - For each pillar, state the concrete property being asserted (identical bytes across repeat compressions, byte-identical restore on random schemas, no crash/hang/signal and non-success decompress exit on corrupt inputs, CRC32 matches stdlib and known vectors).
> - Honest limitations: no formal correctness proof, no exhaustive adversarial coverage, current implementation limits (e.g. a fixed in-memory decompression output cap — pick a reasonable value like 1 MiB and document it — and the absence of an in-container checksum in CPC v0).
> - A short "why this is still useful" section summarizing the practical guarantees for MVP1.
>
> No code changes in this step, just the markdown. After adding `TRUST.md`, re-run `./run_tests.sh` and confirm the suite still prints `"all tests passed"` within the budget.
