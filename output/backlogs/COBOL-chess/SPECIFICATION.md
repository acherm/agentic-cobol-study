# COBOL Chess Engine — cobochess

A UCI chess engine written in COBOL (GnuCOBOL 3.2.x) with an estimated Elo of ~1600-1700.

## Feature Backlog

| ID | Title | Type | Status |
|----|-------|------|--------|
| BL-001 | Core Chess Engine (0x88, UCI, search, eval) | Feature | Done |
| BL-002 | Perft Validation Suite | Test | Done |
| BL-003 | Strength Improvement Phase 1 (~675→~1600) | Feature | Done |
| BL-004 | Strength Improvement Phase 2 (1600→~1700) | Feature | Partial |
| BL-005 | Elo Measurement Harness | Tooling | Done |
| BL-006 | Elo Calculator Bug Fixes | Bugfix | Done |
| BL-007 | macOS Build System Fix (SIGKILL) | Bugfix | Partial |

## Prompt Ledger

### PL-ROOT (Initial Prompt)
**Raw:** "I want to build a chess engine in COBOL (GNUCobol)... at the end, I want to test this chess engine and assess its Elo rating, typically by playing games against chess engines of 'similar' levels"

**Canonical:** Build a UCI chess engine in COBOL (GnuCOBOL, free-format). 0x88 mailbox board, modular .cob files, iterative deepening alpha-beta + quiescence, material + PST eval. Include perft test suite and cutechess-cli + Stockfish Elo harness.

### Per-Feature Prompts
- **BL-001:** "PLEASE IMPLEMENT THIS PLAN: # COBOL (GnuCOBOL) UCI Chess Engine + Elo Harness [detailed plan]"
- **BL-003:** "the current implementation is very weak. Try to significantly improve the engine" → "let's try to beat Stockfish @1600 now"
- **BL-004:** "now try to significantly improve the strength of the engine" → "continue..."
- **BL-007:** "perft failed (signal 9)" → "please fix the build workflow"

## Reproduction Instructions

### Prerequisites
- GnuCOBOL 3.2.x (`cobc`)
- Python 3
- Stockfish (in PATH)
- cutechess-cli (in PATH)
- macOS arm64 with Xcode CLI tools

### Build & Test
```sh
make build              # Compile engine
make perft              # Run perft validation (16 test cases)
make uci-smoke          # UCI protocol smoke test
```

### Elo Assessment
```sh
python3 tools/elo_run.py --games 200 --sf-elo 1320    # Baseline
python3 tools/elo_run.py --games 200 --sf-elo 1600    # Target level
python3 tools/elo_run.py --games 20 --sf-elo 1800     # Ceiling test
```

### Checkpoints
No git commits available. File snapshot as of Feb 11, 2026 (with binary rebuilt Feb 19).

## Repo Statistics
- **27 project files**, **5,286 total LOC**
- COBOL: 16 files, 3,988 LOC (75%)
- Python tooling: 4 files, 681 LOC (13%)
- 1,178 test games played across 54 match sessions

## Limitations
- No git history (repo not initialized)
- macOS build can fail due to quarantine/strip issues
- No CI/CD pipeline
- Eval/search improvements from Phase 2 may have regressed after build crisis
