# Running the Post-Session Analyst on missing projects

The per-project prompts under `prompts/per-project/*.md` are self-contained:
each one can be handed to a Claude Code general-purpose sub-agent that runs
inside this repository. Artefacts are written to
`output/backlogs/<project>/` — the original project folders are **not**
modified.

## Projects that already have a `SPECIFICATION_BACKLOG.md`

| Project | #backlog entries mined |
|---|---:|
| `COBOL-chess` | 184 (phase-tagged) |
| `cobol-doom` | 139 (step-tagged, `S1-..`/`S2-..` scheme) |
| `cobol-tictactoe` | 31 |
| `cobol-compress-codex` | 18 (`SB-` heading scheme) |
| `COBOL-pygame` | 11 |

These are already harvested under `output/backlogs/<project>/` by
`scripts/harvest_backlogs.py` and their counts flow into the feature ledger.

## Projects where the analyst has never run

| Project | Agent(s) | Sessions | Prompt file |
|---|---|---:|---|
| `chess-cobol-cc` | Claude Code | 1 | `prompts/per-project/chess-cobol-cc.md` |
| `cobol-compiler-cc` | Claude Code | 3 | `prompts/per-project/cobol-compiler-cc.md` |
| `cobol-compiler-codex` | Codex | 4 | `prompts/per-project/cobol-compiler-codex.md` |
| `cobol-compress-cc` | Claude Code | 1 | `prompts/per-project/cobol-compress-cc.md` |
| `cobol-jb` | Claude Code | 2 | `prompts/per-project/cobol-jb.md` |
| `cobol-SAT` | Claude Code + Codex | 2 | `prompts/per-project/cobol-SAT.md` |

## How to run one manually

Open the project's prompt file and hand its entire contents to a Claude Code
`general-purpose` sub-agent. The sub-agent will:

1. Enumerate repo structure (fast, already partly done — see the
   "Context you can rely on" section at the top of the prompt).
2. Read the pre-identified session JSONL(s) from `~/.claude/projects/…` or
   `~/.codex/sessions/…`.
3. Run `cloc`-style repo stats, and build/run the project only when needed.
4. Produce `output/backlogs/<project>/SPECIFICATION_BACKLOG.md`,
   `README.md`, the machine-readable JSON appendix, and a running `REPORT.md`.
5. Return a concise summary.

## How to run all 6 in parallel

One `Agent(subagent_type="general-purpose")` call per project, fired in the
same message (so they run concurrently). Budget: each sub-agent will read
~10–230 MB of JSONL per project and perform dozens of `Read`/`Grep` calls.
Expect each to take several minutes and consume meaningful context + token
budget.

Example invocation template (to be sent to the orchestrator agent):

```
Agent({
  description: "<project> post-session analyst",
  subagent_type: "general-purpose",
  prompt: <paste the full contents of prompts/per-project/<project>.md>
})
```

## Known caveats

- The `cobol-compiler-cc` session is ~230 MB — the sub-agent will have to
  stream it (not load fully) and may need multiple passes.
- For `cobol-SAT`, one session is Codex (Feb 2026, the substantive build)
  and the other is Claude Code (April 2026, a much later "look for traces"
  conversation). Instruct the sub-agent to treat the Codex session as the
  primary evidence for BL/SB reconstruction.
- For any project with no real user prompts (very rare — e.g. if everything
  came from `AGENTS.md`), the sub-agent will mark `PL-ROOT = UNKNOWN` and
  rely on repo evidence, as the master prompt specifies.
