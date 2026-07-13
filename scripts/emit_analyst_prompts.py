#!/usr/bin/env python3
"""Emit per-project Post-Session-Analyst prompts.

For each project, a self-contained Markdown prompt is generated under
`prompts/per-project/<project>__<agent>.md`. Each prompt:

- explicitly names the project root + the agent that produced it,
- pre-lists the session JSONL files we already discovered (so the sub-agent
  does not waste time enumerating `~/.claude/projects` / `~/.codex/sessions`),
- **redirects all output files to `output/backlogs/<project>/`** inside the
  meta-analysis repo, rather than modifying the project folder itself. That
  keeps the original project dirs untouched while still producing the
  SPECIFICATION_BACKLOG.md / README.md deliverables.
- inlines a pointer to the master template (`prompts/post-session-analyst.md`)
  for reproducibility.
"""
import argparse, json, os, sys
from collections import defaultdict

MASTER = "prompts/post-session-analyst.md"

HEADER_TMPL = """# Post-Session Backlog & Strategy Analyst — `{project}`

> **Auto-generated prompt** for meta-analysis. Full template lives in
> [`prompts/post-session-analyst.md`](../post-session-analyst.md). This file
> specializes the template for a single project + a single agent family.

## Context you can rely on (already discovered)

- **Project root:** `{project_root}`
- **Coding agent(s) that produced this project:** {agent_family}
- **Number of sessions on disk:** {n_sessions}
- **Earliest session timestamp:** {first_ts}
- **Latest session timestamp:** {last_ts}

### Pre-identified session files (primary evidence)

{session_list}

### Do NOT modify the project folder in this run

For this meta-analysis run, do **not** write anything to `{project_root}`.
Write all artifacts — including `SPECIFICATION_BACKLOG.md`, the updated
`README.md`, the machine-readable appendix, and any intermediate notes — to:

```
{output_root}
```

This directory exists; create subfolders as you wish inside it.

The original project's `README.md` / `SPECIFICATION_BACKLOG.md` (if present)
must be treated as **evidence**, not as files to edit. If your PASS 1 output
would have replaced one of those files, save the new version inside the
output dir above with the same filename.

"""


def load_sessions(sessions_path, project):
    with open(sessions_path) as f:
        sessions = json.load(f)
    # match by project_dir (Claude Code) or by basename(project_cwd) (Codex)
    matches = []
    for s in sessions:
        pd = s.get("project_dir","")
        if pd.startswith("-Users-mathieuacher-SANDBOX-"):
            pd = pd[len("-Users-mathieuacher-SANDBOX-"):]
        cwd = s.get("project_cwd") or ""
        if pd == project or os.path.basename(cwd) == project:
            matches.append(s)
    # dedupe by session_id
    seen = set(); out = []
    for s in sorted(matches, key=lambda x: x.get("start") or ""):
        sid = s.get("session_id")
        if sid in seen: continue
        seen.add(sid); out.append(s)
    return out


def format_sessions(sessions):
    if not sessions:
        return "_(no sessions preserved on disk — analyse repo-only)_"
    lines = []
    for s in sessions:
        agent = s.get("agent","?")
        model = s.get("model","?")
        ver = s.get("version","?")
        start = (s.get("start") or "")[:16]
        end = (s.get("end") or "")[:16]
        sid = s.get("session_id","?")
        fp = s.get("file","?")
        lines.append(f"- `{agent}` v`{ver}` model `{model}` — `{sid}`  \n  "
                     f"path: `{fp}`  \n  "
                     f"window: {start} → {end}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions-json", required=True)
    ap.add_argument("--master", default=MASTER)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--backlogs-root", required=True,
                    help="Where the analyst should write its artefacts "
                         "(e.g. output/backlogs)")
    ap.add_argument("--projects-root", default=os.path.expanduser("~/SANDBOX"))
    ap.add_argument("--projects", nargs="+", required=True)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    master_body = ""
    if os.path.exists(args.master):
        with open(args.master) as f:
            master_body = f.read()
    else:
        print(f"[warn] master template not found at {args.master}", file=sys.stderr)

    for proj in args.projects:
        sessions = load_sessions(args.sessions_json, proj)
        agents = sorted({s.get("agent","?") for s in sessions})
        agent_family = ", ".join(agents) if agents else "unknown"
        project_root = os.path.join(args.projects_root, proj)
        output_root = os.path.join(args.backlogs_root, proj)
        os.makedirs(output_root, exist_ok=True)
        first_ts = sessions[0].get("start","?")[:16] if sessions else "—"
        last_ts  = sessions[-1].get("end","?")[:16]  if sessions else "—"
        header = HEADER_TMPL.format(
            project=proj,
            project_root=project_root,
            agent_family=agent_family,
            n_sessions=len(sessions),
            first_ts=first_ts, last_ts=last_ts,
            session_list=format_sessions(sessions),
            output_root=os.path.abspath(output_root),
        )
        body = master_body
        # Rewrite the per-agent notes preamble so the subagent sees only the
        # relevant one first, but keep both for completeness.
        emphasized = ""
        if any(a == "Claude Code" for a in agents):
            emphasized = "**This project used Claude Code.** Start your session-artifact discovery at `~/.claude/projects/`. Codex notes below are informational.\n\n"
        elif any(a == "Codex" for a in agents):
            emphasized = "**This project used Codex CLI.** Start your session-artifact discovery at `~/.codex/sessions/`. Claude Code notes below are informational.\n\n"
        body = body.replace("## PER-AGENT NOTES", emphasized + "## PER-AGENT NOTES")
        # suffix: explicit start command
        suffix = ("\n\n---\n\n## Start now\n\n"
                  "Work from the facts above. Produce the required artefacts "
                  f"in `{os.path.abspath(output_root)}`. Keep quotes ≤25 words. "
                  "Treat checkpoints CP1–CP3 as best-effort only (no human will "
                  "answer). When blocked, apply the default-if-unanswered "
                  "assumption listed in the master template.\n")
        out_path = os.path.join(args.out_dir, f"{proj}.md")
        with open(out_path, "w") as f:
            f.write(header + body + suffix)
        print(f"[ok] {out_path}  ({len(sessions)} sessions, agents: {agent_family})",
              file=sys.stderr)


if __name__ == "__main__":
    main()
