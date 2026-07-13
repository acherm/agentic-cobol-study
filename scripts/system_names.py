"""Canonical system identifiers (2026-07-10, author-requested).

The paper refers to the 16 systems by FAMILY-COBOL-AGENT identifiers.
Repository folders, session logs, and every artifact under output/ keep
the original folder names: they are the provenance keys of the frozen
raw logs (20/38 purged by local retention) and cannot be renamed without
corrupting traceability. This table is the single source of the mapping;
the paper's appendix table mirrors it.
"""

SYSTEM_ID = {
    "chess-cobol-cc":         "CHESS-COBOL-CLAUDE",
    "COBOL-chess":            "CHESS-COBOL-CODEX",
    "cobol-compiler-cc":      "COMPILER-COBOL-CLAUDE",
    "cobol-compiler-codex":   "COMPILER-COBOL-CODEX",
    "cobol-compress-cobolcc": "COMPRESS-COBOL-CLAUDE",
    "cobol-compress-codex":   "COMPRESS-COBOL-CODEX",
    "cobol-doom-cc":          "DOOM-COBOL-CLAUDE",
    "cobol-doom-codex":       "DOOM-COBOL-CODEX",
    "cobol-jb-cc":            "PAYROLL-COBOL-CLAUDE",
    "cobol-jb-codex":         "PAYROLL-COBOL-CODEX",
    "cobol-pygame-cc":        "PYGAME-COBOL-CLAUDE",
    "COBOL-pygame":           "PYGAME-COBOL-CODEX",
    "SATCobol-cc":            "SAT-COBOL-CLAUDE",
    "SATCobol-codex":         "SAT-COBOL-CODEX",
    "cobol-tictactoe":        "TTTGAME15-COBOL-CLAUDE",
    "game15-cobol-codex":     "TTTGAME15-COBOL-CODEX",
}

FAMILY = ["CHESS-COBOL", "COMPILER-COBOL", "COMPRESS-COBOL", "DOOM-COBOL",
          "PAYROLL-COBOL", "PYGAME-COBOL", "SAT-COBOL", "TTTGAME15-COBOL"]


def display(folder):
    return SYSTEM_ID.get(folder, folder)
