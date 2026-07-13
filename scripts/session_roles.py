"""Canonical session-role classification (2026-07-10).

The project folders contain three kinds of recorded sessions:
  dev     — the agent works on the system (build, evolve, validate,
            document, refactor). Counts toward every development-effort
            metric (cost, tokens, tool calls, active time, prompts).
  analyst — OUR post-mortem instrument: the "Post-Session Backlog &
            Strategy Analyst" runs that reconstruct backlogs/rubrics.
            They are assessment overhead, not agent development work,
            and often run on a different agent than the one that built
            the system (e.g. Claude Code analyzing a Codex project).
            Excluded from every development-effort aggregate.
  empty   — zero-tool-call, zero-cost log shells (local-command-only
            transcripts). Excluded.

The analyst marker is the exact string every analyst session opens with.
Deterministic on purpose: no fuzzy matching, so the dev/analyst split is
mechanically reproducible from sessions_all.json alone.
"""

ANALYST_MARKER = "Post-Session Backlog & Strategy Analyst"


def session_role(s):
    fp = s.get("first_user_prompt") or ""
    if ANALYST_MARKER in fp:
        return "analyst"
    if not (s.get("tool_calls_total") or 0) and not (s.get("cost_usd") or 0):
        return "empty"
    return "dev"
