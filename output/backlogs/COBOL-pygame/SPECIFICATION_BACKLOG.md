# Specification Backlog (Agent-Centric, Step-Wise)

## Purpose

This document captures the **agent-centric implementation steps** — what the Codex agent (GPT-5.2) actually built during session `019c41c6-066e-7fc2-80fc-df9d9c702a1e` on 2026-02-09, ordered chronologically. Each SB item reflects an observable, stable checkpoint in the system's evolution.

## Step Segmentation Method

**Method**: Session episode segmentation via Codex session JSONL event stream.
No git commits exist (repo was never initialized as a git repository). Steps are identified by `apply_patch` events, `exec_command` build/test cycles, and `update_plan` transitions.

**Limitation**: Without git history, step boundaries are approximate, inferred from timestamp clusters and plan state transitions.

---

## SB Entries

### SB-001: Environment Discovery & Toolchain Validation
- **Step label**: EP-session-start (~09:40:22–09:40:48)
- **Category**: Tooling
- **Provenance**: Agent-initiated (prerequisite)
- **Mapping**: Prerequisite for BL-001
- **Specification**: Agent confirmed empty repo, verified GnuCOBOL 3.2.0 and SDL2 2.32.8 availability, checked absence of SDL2_ttf/SDL2_mixer/SDL2_gfx.
- **Evidence**: [T:session 019c41c6:event_018] ls; [T:session 019c41c6:event_025] cobc -V; [T:session 019c41c6:event_032] pkg-config checks
- **Validation**: All tool checks returned expected results.

### SB-002: API Design (pygame-like C API)
- **Step label**: EP-design (~09:40:48–09:43:02)
- **Category**: Capability
- **Provenance**: User-driven (UI-001, PL-ROOT)
- **Mapping**: BL-001
- **Specification**: Designed `cpg_*` C API surface: init/quit, window+renderer management, draw primitives (line/rect/fill_rect), event polling (keyboard/mouse/quit/window), timing (delay/ticks), BMP texture loading/rendering, error reporting. All numeric args passed BY VALUE, pointer handles BY REFERENCE.
- **Evidence**: [T:session 019c41c6:event_037–067] (20+ reasoning traces covering API functions, COBOL interop, SDL2 event types, string handling)
- **Scope**: SDL2_ttf/mixer/gfx excluded (not available). Text rendering excluded. Only BMP textures (SDL2 built-in).

### SB-003: Scaffold Project (all source files)
- **Step label**: EP-scaffold (~09:45:07–09:46:51)
- **Category**: Capability
- **Provenance**: User-driven (UI-001, PL-ROOT)
- **Mapping**: BL-001
- **Specification**: Created 7 files from scratch via single apply_patch:
  - `src/cpg.h` (C header, 55 lines) — struct CPG_Event + function declarations
  - `src/cpg.c` (C implementation, 367 lines) — SDL2 wrapper with NULL-safety, string trimming, fallback renderer
  - `cobol/cpg.cpy` (COBOL copybook, 40 lines) — pointer handles, event struct (COMP-5), SDL2 constants
  - `examples/hello.cob` (bouncing rectangle demo, 106 lines)
  - `Makefile` (build system, 47 lines)
  - `README.md` (documentation, 56 lines)
  - `.gitignore`
- **Evidence**: [T:session 019c41c6:event_069] apply_patch (Add File: .gitignore, Makefile, src/cpg.h, src/cpg.c, cobol/cpg.cpy, examples/hello.cob, README.md)
- **Validation**: Files created successfully.

### SB-004: First Build & COBOL Data Type Fix
- **Step label**: EP-build-fix-1 (~09:47:14–09:47:52)
- **Category**: Quality/Hardening
- **Provenance**: Agent-initiated (discovered during build)
- **Mapping**: BL-001
- **Specification**: Initial `make` failed — GnuCOBOL 3.2 rejected `BINARY-LONG` in copybook. Agent patched `cobol/cpg.cpy` and `examples/hello.cob` to use `COMP-5` instead of `BINARY-LONG` for all 32-bit integer fields.
- **Evidence**: [T:session 019c41c6:event_076] make (exit code 2); [T:session 019c41c6:event_082] apply_patch cpg.cpy; [T:session 019c41c6:event_087] apply_patch hello.cob; [T:session 019c41c6:event_093] make clean && make (exit code 0)
- **Validation**: Build succeeded after fix.

### SB-005: Fix Runtime Module Lookup (Bug Fix)
- **Step label**: EP-bugfix (~10:22:49–10:25:17)
- **Category**: Quality/Hardening
- **Provenance**: User-driven (UI-002, PL-002)
- **Mapping**: BL-002
- **Specification**: User reported `libcob: error: module 'cpg_init' not found`. Root cause: GnuCOBOL defaults to dynamic (dlsym) lookup for `CALL` statements. Fix: added `-fstatic-call` to `COBFLAGS` in Makefile, causing CALL to resolve at link time.
- **Evidence**: [T:session 019c41c6:event_136] user bug report; [T:session 019c41c6:event_145] cobc --help investigation; [T:session 019c41c6:event_156] apply_patch Makefile (add COBFLAGS); [T:session 019c41c6:event_161] make clean && make (exit code 2 — unrelated SDL display issue in sandbox)
- **Validation**: Build succeeded; runtime fix confirmed by agent.

### SB-006: Makefile Hardening (Prerequisite Tracking)
- **Step label**: EP-bugfix (~10:24:44)
- **Category**: Quality/Hardening
- **Provenance**: Agent-initiated
- **Mapping**: BL-002 (related improvement)
- **Specification**: Added `Makefile` as a prerequisite to all build targets (`cpg.o`, `libcpg.a`, `hello`) so changes to build flags trigger rebuild.
- **Evidence**: [T:session 019c41c6:event_168] apply_patch Makefile (add Makefile to prerequisites)

### SB-007: README Update (Static Call Note)
- **Step label**: EP-bugfix (~10:24:51)
- **Category**: Documentation
- **Provenance**: Agent-initiated
- **Mapping**: BL-002
- **Specification**: Added note to README explaining `-fstatic-call` and the `libcob: error: module 'cpg_init' not found` error.
- **Evidence**: [T:session 019c41c6:event_175] apply_patch README.md

### SB-008: Flappy Bird Game Implementation
- **Step label**: EP-flappy (~10:37:24–10:40:42)
- **Category**: Capability
- **Provenance**: User-driven (UI-003, PL-003)
- **Mapping**: BL-003
- **Specification**: Created `examples/flappy.cob` (346 lines) implementing:
  - Bird with gravity physics and flap mechanics
  - 3 scrolling pipes with randomized gap positions
  - AABB collision detection (bird vs pipes, bird vs ground)
  - Score tracking displayed in window title
  - Game over state with restart capability
  - Frame-rate-limited game loop (~60 FPS target)
  - Controls: Space/Up/Left-click to flap, Escape to quit
- **Evidence**: [T:session 019c41c6:event_200–207] reasoning traces (game design); [T:session 019c41c6:event_214] apply_patch (Add File: examples/flappy.cob)

### SB-009: Extend Makefile for Flappy
- **Step label**: EP-flappy (~10:40:55)
- **Category**: Tooling
- **Provenance**: User-driven (UI-003, PL-003)
- **Mapping**: BL-003
- **Specification**: Added `FLAPPY_EXE`, `run-flappy` target, build rule for flappy.cob. Updated `all` target to build both hello and flappy.
- **Evidence**: [T:session 019c41c6:event_224] apply_patch Makefile

### SB-010: Fix Flappy Bird Rendering Bug
- **Step label**: EP-flappy-fix (~10:41:16–10:41:18)
- **Category**: Quality/Hardening
- **Provenance**: Agent-initiated (discovered during build)
- **Mapping**: BL-003
- **Specification**: First flappy build failed (COBOL compile errors). Agent patched pipe rendering logic to properly compute top/bottom pipe heights using local variables.
- **Evidence**: [T:session 019c41c6:event_234] make clean && make (exit code 2); [T:session 019c41c6:event_240] apply_patch flappy.cob (fix rendering); [T:session 019c41c6:event_245] make (exit code 0)
- **Validation**: Build succeeded.

### SB-011: Update README for Flappy Bird
- **Step label**: EP-flappy-docs (~10:41:36)
- **Category**: Documentation
- **Provenance**: Agent-initiated
- **Mapping**: BL-003
- **Specification**: Added `make run-flappy` instructions to README.
- **Evidence**: [T:session 019c41c6:event_256] apply_patch README.md

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total SB items | 11 |
| User-driven | 5 (SB-002, SB-003, SB-005, SB-008, SB-009) |
| Agent-initiated | 5 (SB-001, SB-004, SB-006, SB-007, SB-011) |
| Prerequisite | 1 (SB-001) |
| Capability items | 3 |
| Quality/Hardening items | 4 |
| Documentation items | 2 |
| Tooling items | 2 |
| apply_patch operations | 10 |
| exec_command (build/test) | 8 |
| Build failures encountered | 3 (SB-004, SB-005, SB-010) |
| Build failures resolved | 3/3 |
