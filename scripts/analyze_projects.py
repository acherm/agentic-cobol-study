#!/usr/bin/env python3
"""Aggregate per-project stats by combining file inventory with session summaries."""
import json, os, re, sys, argparse
from collections import Counter, defaultdict

# Map ~/.claude/projects names <-> real project dirs
def claude_proj_to_path(name):
    # strip leading '-Users-...'
    m = name[len("-Users-mathieuacher-SANDBOX-"):] if name.startswith("-Users-mathieuacher-SANDBOX-") else name
    return os.path.expanduser(f"~/SANDBOX/{m}")

CODE_EXTS = {
    ".cob": "COBOL", ".cbl": "COBOL", ".cpy": "COBOL",
    ".c": "C", ".h": "C/Header", ".cpp": "C++", ".cc": "C++", ".hpp": "C++",
    ".py": "Python", ".java": "Java", ".rs": "Rust", ".go": "Go",
    ".sh": "Shell", ".bash": "Shell",
    ".js": "JS", ".ts": "TS",
    ".md": "Markdown",
    ".mk": "Makefile", "Makefile": "Makefile",
    ".yml": "YAML", ".yaml": "YAML",
    ".json": "JSON",
}

IGNORE_DIRS = {"build", ".git", "node_modules", "__pycache__", ".claude", "external",
               "cutechess", "tmp_one", "shell_snapshots"}


def classify(fn):
    if fn == "Makefile" or fn.endswith("Makefile"):
        return "Makefile"
    _, ext = os.path.splitext(fn)
    return CODE_EXTS.get(ext.lower())


def loc(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def scan_project(root, max_file_mb=5):
    by_lang = defaultdict(lambda: {"files": 0, "loc": 0, "bytes": 0})
    total_files = 0
    total_bytes = 0
    cobol_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]
        rel = os.path.relpath(dirpath, root)
        for fn in filenames:
            if fn.startswith(".DS_Store"):
                continue
            full = os.path.join(dirpath, fn)
            try:
                sz = os.path.getsize(full)
            except Exception:
                continue
            total_files += 1
            total_bytes += sz
            lang = classify(fn)
            if not lang:
                continue
            if sz > max_file_mb * 1024 * 1024:
                by_lang[lang]["files"] += 1
                by_lang[lang]["bytes"] += sz
                continue
            n = loc(full)
            by_lang[lang]["files"] += 1
            by_lang[lang]["loc"] += n
            by_lang[lang]["bytes"] += sz
            if lang in ("COBOL", "COBOL-copybook"):
                cobol_files.append({"path": os.path.relpath(full, root), "loc": n, "bytes": sz})
    return {
        "root": root,
        "total_files": total_files,
        "total_bytes": total_bytes,
        "by_lang": {k: dict(v) for k, v in by_lang.items()},
        "cobol_files": cobol_files,
    }


# ---- activity classification from prompts/tool names ----
ACTIVITY_KWS = [
    ("Implement feature", ["implement", "feature", "add support", "support for", "add "]),
    ("Refactor", ["refactor", "rename", "restructure", "clean up", "cleanup"]),
    ("Debug / Fix", ["fix", "bug", "error", "issue", "crash", "segfault", "doesn't work", "broken", "wrong"]),
    ("Test", ["test", "benchmark", "verify", "validate"]),
    ("Document", ["document", "readme", "explain", "describe", "report"]),
    ("Optimize", ["optimi", "speed", "perf", "slower", "faster", "profile"]),
    ("Port/Rewrite", ["port", "rewrite", "translate", "convert", "migrate"]),
    ("Research", ["research", "investigate", "compare", "study", "analysis", "analyze", "evaluate"]),
    ("Build/Config", ["makefile", "compile", "build", "setup", "configure", "ci/cd", "docker"]),
    ("Review/Audit", ["review", "audit", "verify", "check"]),
]


def classify_activity(text):
    if not text:
        return ["Unclassified"]
    t = text.lower()
    hits = []
    for label, kws in ACTIVITY_KWS:
        for kw in kws:
            if kw in t:
                hits.append(label); break
    return hits or ["Unclassified"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions", required=True)
    ap.add_argument("--projects-root", default=os.path.expanduser("~/SANDBOX"))
    ap.add_argument("--projects", nargs="+", required=True,
                    help="List of project directory names under ~/SANDBOX to analyze")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.sessions) as f:
        sessions = json.load(f)

    # Build index: project_name -> [sessions]
    by_proj = defaultdict(list)
    for s in sessions:
        pd = s.get("project_dir", "")
        # Map Claude Code project_dir (encoded) to real name
        if pd.startswith("-Users-mathieuacher-SANDBOX-"):
            pd = pd[len("-Users-mathieuacher-SANDBOX-"):]
        by_proj[pd].append(s)
        # For Codex, also try via project_cwd basename
        cwd = s.get("project_cwd")
        if cwd:
            base = os.path.basename(cwd)
            if base != pd:
                by_proj[base].append(s)

    out = {}
    for proj in args.projects:
        pdir = os.path.join(args.projects_root, proj)
        if not os.path.isdir(pdir):
            print(f"[skip] {proj} not found", file=sys.stderr)
            continue
        inv = scan_project(pdir)
        # dedupe sessions by session_id
        seen = set()
        ps = []
        for s in by_proj.get(proj, []):
            sid = s.get("session_id")
            if sid in seen:
                continue
            seen.add(sid)
            ps.append(s)
        # sort by start
        ps.sort(key=lambda s: s.get("start") or "")
        # aggregate activities from prompts
        activity_cnt = Counter()
        for s in ps:
            for a in classify_activity(s.get("first_user_prompt") or ""):
                activity_cnt[a] += 1
        out[proj] = {
            "inventory": inv,
            "sessions": ps,
            "activity_counts": dict(activity_cnt),
        }
        print(f"[ok] {proj}: {inv['total_files']} files, {len(ps)} sessions", file=sys.stderr)

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2, default=str)


if __name__ == "__main__":
    main()
