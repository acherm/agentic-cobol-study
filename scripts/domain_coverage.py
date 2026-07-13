#!/usr/bin/env python3
"""Map COBOL projects into problem-domains and flag two-agent coverage.

For each project we pick the **primary agent** — the one that did the
substantive feature build — by summing tool calls across every preserved
session. Secondary agents (typically a later analyst / meta pass) are listed
separately.

A domain is considered "covered by both agents" iff at least one project in
the domain has Claude Code as primary AND at least one has Codex as primary.

Emits a markdown fragment to stdout (or --out). Intended to be embedded in
the top-level `REPORT.md` and reviewed directly.
"""
import argparse, json, os, sys
from collections import Counter, defaultdict

# ----------------------------------------------------------------------------
# Hand-authored project → (domain, short domain description)
# Domains are problem classes, not language surface. Two different projects in
# the same domain are intentional replications (ideally one per agent).
# ----------------------------------------------------------------------------
DOMAIN = {
    "chess-cobol-cc":       ("Chess engine",                   "UCI-speaking playable chess engine with Elo-measured strength."),
    "COBOL-chess":          ("Chess engine",                   "UCI-speaking playable chess engine with Elo-measured strength."),
    "cobol-compiler-cc":    ("COBOL compiler (self-hosted)",   "A COBOL compiler written in COBOL that compiles non-trivial COBOL programs."),
    "cobol-compiler-codex": ("COBOL compiler (self-hosted)",   "A COBOL compiler written in COBOL that compiles non-trivial COBOL programs."),
    "cobol-compress-codex":   ("Columnar compressor (COBPACK)",  "Columnar packer / compressor for fixed-record COBOL data, with codec + trust-suite."),
    "cobol-compress-cobolcc": ("Columnar compressor (COBPACK)",  "Columnar packer / compressor for fixed-record COBOL data, with codec + trust-suite."),
    "cobol-doom-cc":        ("Real-time ray-casting FPS",      "Ray-casting 3-D FPS (Doom-like) with real-time rendering."),
    "cobol-doom-codex":     ("Real-time ray-casting FPS",      "Ray-casting 3-D FPS (Doom-like) with real-time rendering."),
    "cobol-jb":             ("Payroll case-study",             "Industrial-idiom payroll system (records → payslips + summary, verification grid)."),
    "cobol-jb-cc":          ("Payroll case-study",             "Payroll system, 6-step canonical protocol incl. multi-file merge + behavior-preserving refactoring (Claude Code)."),
    "cobol-jb-codex":       ("Payroll case-study",             "Payroll system, 6-step canonical protocol incl. multi-file merge + behavior-preserving refactoring (Codex)."),
    "COBOL-pygame":         ("Game / graphics framework",      "COBOL → C → Python → pygame FFI framework for 2-D games."),
    "cobol-pygame-cc":      ("Game / graphics framework",      "pygame-style SDL2 framework for GnuCOBOL + pure-COBOL Flappy Bird (Claude Code replica, 5-step replay pack)."),
    "SATCobol-codex":       ("SAT solver",                     "DIMACS CNF SAT solver with CDCL, cross-checked against MiniSat / SAT4J."),
    "SATCobol-cc":          ("SAT solver",                     "DIMACS CNF SAT solver with CDCL, cross-checked against MiniSat / SAT4J."),
    "cobol-tictactoe":      ("Small game (tic-tac-toe / game-of-15)", "Game-of-15 / tic-tac-toe with minimax tree search."),
    "game15-cobol-codex":   ("Small game (tic-tac-toe / game-of-15)", "Game-of-15 / tic-tac-toe with minimax tree search."),
}


ANALYST_MARKERS = (
    "post-session", "backlog & strategy", "backlog strategy",
    "please analyze thoroughly", "please analyse thoroughly",
    "two-pass workflow", "replay package", "prompt ledger",
    "pass 1 (extraction)", "pass 2 (interpretation)",
    "i would like to find traces of historical session",
    "look at the current repo", "verify whether the agent produced equivalent",
)


def _is_analyst_session(s):
    """True if this session's opening prompt looks like an analyst / meta pass
    rather than a substantive build."""
    prompt = (s.get("first_user_prompt") or "").lower()
    return any(m in prompt for m in ANALYST_MARKERS)


def primary_agent(sessions):
    """Return the agent that ORIGINATED the project (did the initial build).

    Strategy: pick the agent whose session has the PL-ROOT — i.e. the
    chronologically earliest session whose opening prompt is not an analyst /
    meta / verification pass. This aligns with "the agent that the user
    started the project with"; later sessions from the other agent (ports,
    comparisons, analyst reruns) are treated as secondary regardless of tool
    call count.

    Fallback: if every session is analyst-style (very unusual), take the
    earliest session overall.
    """
    if not sessions:
        return None
    substantive = [s for s in sessions if not _is_analyst_session(s)]
    pool = substantive or sessions
    earliest = min(pool, key=lambda s: s.get("start") or "")
    return earliest.get("agent","?")


def build_coverage(sessions_all, projects):
    proj_agents = {}
    for p in projects:
        sess = []
        for s in sessions_all:
            pd = s.get("project_dir","")
            if pd.startswith("-Users-mathieuacher-SANDBOX-"):
                pd = pd[len("-Users-mathieuacher-SANDBOX-"):]
            cwd = s.get("project_cwd") or ""
            if pd == p or os.path.basename(cwd) == p:
                sess.append(s)
        prim = primary_agent(sess)
        agents = sorted({s.get("agent","?") for s in sess})
        proj_agents[p] = {
            "primary": prim,
            "all_agents": agents,
            "n_sessions": len({s.get("session_id") for s in sess}),
            "tool_calls": sum(s.get("tool_calls_total",0) or 0 for s in sess),
        }

    # Group by domain
    domains = defaultdict(list)
    for p, info in proj_agents.items():
        d, desc = DOMAIN.get(p, ("_Unclassified_", ""))
        domains[d].append((p, info, desc))
    return proj_agents, domains


def render(proj_agents, domains):
    L = []; E = L.append
    E("## Domain coverage — which problem classes have been attempted by which agent?")
    E("")
    E("Projects are grouped by *problem domain*. The **primary agent** per project "
      "is the one whose earliest non-analyst session kicked the project off "
      "(i.e. authored the PL-ROOT build prompt); later sessions from the other "
      "agent (ports, comparisons, analyst re-runs) are listed in parentheses. "
      "A domain is **covered by both agents** iff at least one project in the "
      "domain has Claude Code as primary AND at least one has Codex as primary.")
    E("")
    E("| Domain | Description | Claude-Code projects (primary) | Codex projects (primary) | Both agents? |")
    E("|---|---|---|---|:---:|")
    gap_cc = []   # domains missing a Claude-Code replica
    gap_cx = []   # domains missing a Codex replica
    for d in sorted(domains):
        rows = domains[d]
        cc = []; cx = []
        desc = ""
        for p, info, description in rows:
            desc = description or desc
            prim = info["primary"]
            others = [a for a in info["all_agents"] if a != prim]
            suffix = f" _(also: {', '.join(others)})_" if others else ""
            entry = f"`{p}`{suffix}"
            if prim == "Claude Code":
                cc.append(entry)
            elif prim == "Codex":
                cx.append(entry)
            else:
                # unknown — treat as no-coverage
                pass
        both = "✓" if cc and cx else "—"
        if not cc:
            gap_cc.append(d)
        if not cx:
            gap_cx.append(d)
        E(f"| **{d}** | {desc} | {'<br>'.join(cc) or '— _(no Claude-Code replica yet)_'} | {'<br>'.join(cx) or '— _(no Codex replica yet)_'} | {both} |")
    E("")
    # Gap summary
    covered = sorted(d for d in domains if d not in gap_cc and d not in gap_cx)
    E(f"**Two-agent coverage: {len(covered)} / {len(domains)} domains.**")
    E("")
    if covered:
        E("Domains already attempted by **both** Claude Code and Codex:")
        E("")
        for d in covered:
            E(f"- {d}")
        E("")
    if gap_cc:
        E("Domains **missing a Claude-Code replica** (currently Codex-only):")
        E("")
        for d in gap_cc:
            if d in gap_cx: continue  # covered by neither, odd
            E(f"- {d}")
        E("")
    if gap_cx:
        E("Domains **missing a Codex replica** (currently Claude-Code-only):")
        E("")
        for d in gap_cx:
            if d in gap_cc: continue
            E(f"- {d}")
        E("")
    neither = sorted(set(gap_cc) & set(gap_cx))
    if neither:
        E("Domains with **no assignable primary agent** (session data missing):")
        E("")
        for d in neither:
            E(f"- {d}")
        E("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions-json", required=True)
    ap.add_argument("--projects", nargs="+", required=True)
    ap.add_argument("--out", default="-")
    args = ap.parse_args()
    with open(args.sessions_json) as f:
        sessions = json.load(f)
    proj_agents, domains = build_coverage(sessions, args.projects)
    md = render(proj_agents, domains)
    if args.out == "-":
        sys.stdout.write(md)
    else:
        with open(args.out, "w") as f:
            f.write(md)


if __name__ == "__main__":
    main()
