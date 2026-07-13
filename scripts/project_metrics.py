#!/usr/bin/env python3
"""Aggregate per-project metrics from multiple data sources.

Inputs:
  output/sessions_all.json        (high-level session summaries)
  output/turns/<project>__*.jsonl (per-turn timeline)
  output/complexity/<project>.json
  output/git/<project>.json
  output/projects.json            (file inventory, from analyze_projects.py)
  ~/SANDBOX/<project>/**          (README / SPECIFICATION for domain story)

Output:
  output/metrics/<project>.json   (everything needed to render the report)
"""
import argparse, json, os, re, sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from session_roles import session_role

ACTIVE_GAP_S = 600  # gaps <= 10 min count as active work
ERROR_RECOVERY_WINDOW = 3  # consecutive tool_use after an error counts as bug_fix

# SE-task taxonomy — what a human would call the activity.
# Old labels from deep_analyze.py get remapped here so the reports speak a
# consistent vocabulary.
SE_TASK_RENAME = {
    "implement": "feature",       # adding new functionality
    "fix":       "bug_fix",       # correcting a defect
    "optimize":  "performance",   # making it faster
    "test":      "test",          # writing or running tests / benchmarks
    "refactor":  "refactor",      # restructuring without behaviour change
    "research":  "understanding", # reading/searching to build a mental model
    "build":     "build",         # compile / makefile / deps
    "spec":      "spec",          # specs / architecture docs
    "doc":       "doc",           # README / comments / reports
    "port":      "port",          # translating between languages
    "review":    "verification",  # auditing / grid verification
    "meta":      "plan",          # task-tracking / planning
    "other":     "unknown",
    None:        "unknown",
}

FEATURE_TOOL_NAMES = {
    # tools that produce new code
    "Edit","Write","NotebookEdit","apply_patch",
}
RUN_TOOL_NAMES = {"Bash","exec_command","write_stdin"}

BIN_EXTS = {".o", ".out"}


def parse_iso(s):
    if not s: return None
    try:
        return datetime.fromisoformat(s.replace("Z","+00:00"))
    except Exception:
        return None


def load_turns(turn_dir, project, skip_session_ids=None):
    skip_session_ids = skip_session_ids or set()
    files = []
    for fn in sorted(os.listdir(turn_dir)):
        if fn.startswith(project + "__") and fn.endswith(".jsonl"):
            sid = fn[:-len(".jsonl")].split("__")[-1]
            if sid in skip_session_ids:
                continue
            files.append(os.path.join(turn_dir, fn))
    records = []
    for fp in files:
        with open(fp) as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
    return records, files


def se_task_label(raw):
    return SE_TASK_RENAME.get(raw, raw or "unknown")


def reclassify_turns(turns):
    """Apply the SE-task taxonomy + contextual rules to each turn.

    Contextual rule: if an edit/apply_patch follows an error tool_output within
    ERROR_RECOVERY_WINDOW steps, relabel as bug_fix regardless of raw label.
    Similarly, a Bash/exec_command that re-runs the same kind of command after
    an error becomes bug_fix (build-after-error = trying to fix the build).

    Also counts 'fix_cycles' = transitions error_output → editing_tool.
    Returns (turns_with_new_activity, fix_cycles_count, error_indices)
    """
    err_idx = []
    last_err = -10**9
    fix_cycles = 0
    out = []
    for i, r in enumerate(turns):
        r = dict(r)  # copy
        raw = r.get("activity")
        se = se_task_label(raw)
        kind = r.get("kind")
        tool = r.get("tool")
        # Track errors
        if kind == "tool_output" and r.get("is_error"):
            last_err = i
            err_idx.append(i)
        # Contextual relabel
        if (i - last_err) <= ERROR_RECOVERY_WINDOW and kind == "tool_use":
            if tool in FEATURE_TOOL_NAMES:
                se = "bug_fix"
                fix_cycles += 1
            elif tool in RUN_TOOL_NAMES:
                # retrying a build/test shortly after error
                se = "bug_fix"
        r["se_task"] = se
        out.append(r)
    return out, fix_cycles, err_idx


def active_time_by_activity(turns):
    """Attribute inter-event gaps (<= ACTIVE_GAP_S) to the *current* event's SE-task label."""
    buckets = Counter()
    total_active = 0
    total_wall = 0
    for r in turns:
        gap = r.get("gap_s", 0) or 0
        total_wall += gap
        if gap and gap <= ACTIVE_GAP_S:
            se = r.get("se_task") or se_task_label(r.get("activity"))
            if se == "unknown":
                # inherit from kind/role
                if r.get("kind") == "tool_output":
                    se = "build" if r.get("tool") in RUN_TOOL_NAMES else "understanding"
                elif r.get("role") == "assistant" and r.get("kind") == "text":
                    se = "understanding"
                elif r.get("role") == "assistant" and r.get("kind") == "reasoning":
                    se = "understanding"
            buckets[se] += gap
            total_active += gap
    return buckets, total_active, total_wall


def error_stats(turns):
    total_results = 0
    total_errors = 0
    tag_counts = Counter()
    for r in turns:
        if r.get("kind") == "tool_output":
            total_results += 1
            if r.get("is_error"):
                total_errors += 1
                for t in r.get("error_tags", []) or []:
                    tag_counts[t] += 1
    return {
        "tool_outputs": total_results,
        "tool_output_errors": total_errors,
        "error_rate": round(total_errors / total_results, 3) if total_results else 0.0,
        "error_tags": dict(tag_counts),
    }


BOOTSTRAP_MARKERS = (
    "# AGENTS.md", "<INSTRUCTIONS>", "<local-command-caveat>",
    "<command-name>", "<system-reminder>", "<ide_opened_file>",
    "<environment_context>", "<user_instructions>", "<project_doc>",
)

def _is_bootstrap_prompt(text):
    if not text:
        return True
    t = text.lstrip()[:200]
    return any(m in t for m in BOOTSTRAP_MARKERS)

def user_prompt_stats(turns):
    prompts = [r for r in turns
               if r.get("kind") == "prompt"
               and r.get("role") == "user"
               and not _is_bootstrap_prompt(r.get("preview",""))]
    prompts.sort(key=lambda r: r.get("ts") or "")
    lens = [r.get("text_len", 0) for r in prompts]
    activity = Counter(r.get("activity","unknown") for r in prompts)
    # classify each prompt by intent (initial-spec / clarify / redirect / ...)
    intent = Counter()
    for i, r in enumerate(prompts):
        p = (r.get("preview","") or "").strip()
        pl = len(p)
        pl_words = len(p.split())
        pl_lower = p.lower()
        if i == 0 and pl > 200:
            intent["initial-spec"] += 1
        elif pl_words < 6:
            intent["clarify"] += 1
        elif any(w in pl_lower for w in ("error", "crash", "segfault", "doesn't work", "fails", "broken", "wrong")):
            intent["bug-report"] += 1
        elif any(w in pl_lower for w in ("instead", "rather", "change", "switch to", "don't", "stop")):
            intent["redirect"] += 1
        elif any(w in pl_lower for w in ("review", "verify", "audit", "check", "summarize", "report")):
            intent["review-ask"] += 1
        elif any(w in pl_lower for w in ("continue", "resume", "keep going", "proceed")):
            intent["resume"] += 1
        else:
            intent["other"] += 1
    return {
        "count": len(prompts),
        "avg_len": round(sum(lens)/len(lens), 1) if lens else 0,
        "max_len": max(lens) if lens else 0,
        "total_chars": sum(lens),
        "activity_breakdown": dict(activity),
        "intent_breakdown": dict(intent),
        "first_prompt": prompts[0].get("preview") if prompts else None,
    }


def tool_use_stats(turns):
    tools = Counter()
    by_task = Counter()
    for r in turns:
        if r.get("kind") == "tool_use":
            tools[r.get("tool","?")] += 1
            by_task[r.get("se_task") or se_task_label(r.get("activity"))] += 1
    return {"total": sum(tools.values()), "by_tool": dict(tools), "by_se_task": dict(by_task)}


# --- narrative helpers ------------------------------------------------------

README_FILES = ["README.md", "README", "SPECIFICATION.md", "SPECIFICATION_BACKLOG.md",
                "ARCHITECTURE.md", "REPORT.md", "TRUST.md", "VERIFICATION_REPORT.md"]


def collect_readme_blob(proj_root):
    blob = {}
    for fn in README_FILES:
        fp = os.path.join(proj_root, fn)
        if os.path.isfile(fp):
            try:
                with open(fp, "r", encoding="utf-8", errors="replace") as f:
                    blob[fn] = f.read()
            except Exception:
                pass
    return blob


def extract_sections(md_text, max_chars=4000):
    """Return the first ~2 sections of markdown text as a dict."""
    out = {}
    parts = re.split(r"^(#{1,3})\s+(.+?)$", md_text, flags=re.M)
    # parts alternates: pre, level1, title1, body1, level2, title2, body2, ...
    i = 1
    collected = 0
    while i < len(parts) and collected < max_chars:
        level = parts[i]; title = parts[i+1]; body = parts[i+2] if i+2 < len(parts) else ""
        out[f"{level} {title.strip()}"] = body.strip()[:1500]
        collected += len(body)
        i += 3
    return out


def timeline_summary(turns):
    """Sample first N / last N events with activity+preview for 'story' section."""
    first = [r for r in turns if r.get("kind") in ("prompt","text","tool_use")][:30]
    last  = [r for r in turns if r.get("kind") in ("prompt","text","tool_use")][-30:]
    return {"first_events": first, "last_events": last}


# --- main -------------------------------------------------------------------

def build_project_metrics(proj, proj_root, sessions_all, turn_dir,
                          complexity_path, git_path, inventory_entry,
                          features_path=None):
    # sessions for this project from sessions_all.json
    project_sessions = []
    for s in sessions_all:
        pd = s.get("project_dir","")
        if pd.startswith("-Users-mathieuacher-SANDBOX-"):
            pd = pd[len("-Users-mathieuacher-SANDBOX-"):]
        cwd = s.get("project_cwd") or ""
        if pd == proj or os.path.basename(cwd) == proj:
            project_sessions.append(s)
    # dedupe
    seen = set(); ps = []
    for s in sorted(project_sessions, key=lambda x: x.get("start") or ""):
        sid = s.get("session_id")
        if sid in seen: continue
        seen.add(sid); ps.append(s)

    # Role split: only dev sessions count toward development-effort
    # aggregates. Analyst (post-mortem instrument) and empty (log shells)
    # sessions stay listed under "sessions" with their role, and are
    # summarized in "excluded_sessions".
    for s in ps:
        s["role"] = session_role(s)
    dev = [s for s in ps if s["role"] == "dev"]
    excluded_ids = {s.get("session_id") for s in ps if s["role"] != "dev"}

    turns_raw, turn_files = load_turns(turn_dir, proj,
                                       skip_session_ids=excluded_ids)
    turns, fix_cycles, err_indices = reclassify_turns(turns_raw)
    buckets, total_active, total_wall = active_time_by_activity(turns)
    errors = error_stats(turns)
    uprompts = user_prompt_stats(turns)
    tools = tool_use_stats(turns)

    # Session cadence (dev sessions only)
    starts = sorted([parse_iso(s["start"]) for s in dev if s.get("start")])
    ends = sorted([parse_iso(s["end"]) for s in dev if s.get("end")])
    span_days = (ends[-1] - starts[0]).days if (starts and ends) else 0

    # Tokens / cost (dev sessions only)
    tokens = {"in": 0, "out": 0, "cache_read": 0, "cache_create": 0, "reasoning": 0}
    cost = 0.0
    tool_calls_total = 0
    dur_wall = 0
    for s in dev:
        # Normalize "in" to FRESH input across vendors: Claude Code's
        # input_tokens already excludes cache reads; Codex's includes
        # them (parse_sessions stores the raw total_token_usage value).
        s_in = s.get("input_tokens",0) or 0
        if s.get("agent") == "Codex":
            s_in = max(s_in - (s.get("cache_read_tokens",0) or 0), 0)
        tokens["in"] += s_in
        tokens["out"] += s.get("output_tokens",0) or 0
        tokens["cache_read"] += s.get("cache_read_tokens",0) or 0
        tokens["cache_create"] += s.get("cache_creation_tokens",0) or 0
        tokens["reasoning"] += s.get("reasoning_tokens",0) or 0
        cost += s.get("cost_usd",0) or 0
        tool_calls_total += s.get("tool_calls_total",0) or 0
        dur_wall += s.get("duration_s",0) or 0

    # Complexity
    complexity = None
    if os.path.exists(complexity_path):
        with open(complexity_path) as f: complexity = json.load(f)
    git = None
    if os.path.exists(git_path):
        with open(git_path) as f: git = json.load(f)
    features = None
    if features_path and os.path.exists(features_path):
        with open(features_path) as f: features = json.load(f)

    readme = collect_readme_blob(proj_root)
    story_sections = {}
    for fn, txt in readme.items():
        story_sections[fn] = extract_sections(txt)

    timeline = timeline_summary(turns)

    # ---- difficulty signals ------------------------------------------------
    intents = uprompts.get("intent_breakdown") or {}
    redirect_prompts = intents.get("redirect", 0) + intents.get("bug-report", 0)
    up_count = uprompts.get("count", 0)
    active_hours = total_active / 3600.0
    errs = errors.get("tool_output_errors", 0)
    err_rate = errors.get("error_rate", 0.0)
    tool_per_prompt = tool_calls_total / up_count if up_count else 0
    user_per_active_hour = up_count / active_hours if active_hours > 0 else 0
    fix_time_share = (buckets.get("bug_fix", 0) / total_active) if total_active else 0

    difficulty_signals = {
        "active_hours":               round(active_hours, 2),
        "span_days":                  span_days,
        "user_prompts":               up_count,
        "redirect_bug_prompts":       redirect_prompts,
        "tool_calls":                 tool_calls_total,
        "n_turns":                    len(turns),
        "error_events":               errs,
        "error_rate":                 err_rate,
        "fix_cycles":                 fix_cycles,
        "fix_time_share":             round(fix_time_share, 3),
        "tool_calls_per_prompt":      round(tool_per_prompt, 1),
        "user_interventions_per_hr":  round(user_per_active_hour, 2),
    }

    excl = [s for s in ps if s["role"] != "dev"]
    excluded_summary = {
        "n_analyst": sum(1 for s in excl if s["role"] == "analyst"),
        "n_empty": sum(1 for s in excl if s["role"] == "empty"),
        "analyst_cost_usd": round(sum(s.get("cost_usd") or 0 for s in excl
                                      if s["role"] == "analyst"), 2),
        "analyst_tool_calls": sum(s.get("tool_calls_total") or 0 for s in excl
                                  if s["role"] == "analyst"),
        "note": "analyst/empty sessions are excluded from every aggregate "
                "in this file (cost, tokens, tool calls, active time, "
                "prompts, span, difficulty signals)",
    }

    return {
        "project": proj,
        "project_root": proj_root,
        "domain_files": list(readme.keys()),
        "inventory": inventory_entry or {},
        "complexity": complexity,
        "git": git,
        "sessions": ps,
        "n_dev_sessions": len(dev),
        "excluded_sessions": excluded_summary,
        "span_days": span_days,
        "active_time": {
            "total_active_s": total_active,
            "total_wall_gap_s": total_wall,
            "by_se_task_s": dict(buckets),
        },
        "tokens": tokens,
        "cost_usd": round(cost, 2),
        "tool_calls_total": tool_calls_total,
        "wall_duration_s": dur_wall,
        "user_prompts": uprompts,
        "tool_use": tools,
        "errors": errors,
        "difficulty_signals": difficulty_signals,
        "features": features,
        "story_excerpts": story_sections,
        "timeline_sample": timeline,
        "turn_files": turn_files,
        "n_turns": len(turns),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions-json", required=True)
    ap.add_argument("--projects-json", required=True,
                    help="output/projects.json (file inventory)")
    ap.add_argument("--turn-dir", required=True)
    ap.add_argument("--complexity-dir", required=True)
    ap.add_argument("--git-dir", required=True)
    ap.add_argument("--projects-root", default=os.path.expanduser("~/SANDBOX"))
    ap.add_argument("--features-dir", default=None)
    ap.add_argument("--projects", nargs="+", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    with open(args.sessions_json) as f:
        sessions_all = json.load(f)
    with open(args.projects_json) as f:
        proj_inv = json.load(f)

    for proj in args.projects:
        proj_root = os.path.join(args.projects_root, proj)
        inv = (proj_inv.get(proj) or {}).get("inventory") or {}
        feat_path = None
        if args.features_dir:
            feat_path = os.path.join(args.features_dir, f"{proj}.json")
        m = build_project_metrics(
            proj, proj_root, sessions_all, args.turn_dir,
            os.path.join(args.complexity_dir, f"{proj}.json"),
            os.path.join(args.git_dir, f"{proj}.json"),
            inv,
            features_path=feat_path,
        )
        outp = os.path.join(args.out_dir, f"{proj}.json")
        with open(outp, "w") as f:
            json.dump(m, f, indent=2, default=str)
        print(f"[ok] {proj}: turns={m['n_turns']}, active={m['active_time']['total_active_s']}s, err={m['errors']['tool_output_errors']}/{m['errors']['tool_outputs']}", file=sys.stderr)


if __name__ == "__main__":
    main()
