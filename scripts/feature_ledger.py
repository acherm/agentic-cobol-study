#!/usr/bin/env python3
"""Mine a per-project feature ledger from multiple sources.

Sources (in order of preference):
  1. `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` — table rows `| F-### | feat | evidence |`
     (this is the authoritative list when it exists; COBOL-chess uses this).
  2. README.md / REPORT.md — Features / Capabilities sections, bullet lists.
  3. User prompts — extract ordered/bulleted sub-requests per prompt.
  4. Git commit subjects — each commit that looks like a feature/change.

Outputs:
  output/features/<project>.json with:
    {
      "spec_backlog":    [{id, title, evidence, phase}],   # from F-### tables
      "readme_features": [str, ...],
      "prompt_subtasks": [{ts, prompt_idx, item}],
      "commit_subjects": [{sha, date, subject}],
      "total_features":  int,   # best-effort union
      "delivered_from_backlog": int,  # from backlog (considered "delivered")
    }
"""
import argparse, json, os, re, sys, glob
from collections import OrderedDict


BACKLOG_ROW_RE = re.compile(
    r"^\s*\|\s*(?P<id>(?:F|BL|SB|OP|S\d+|Step\s*\d+)-?[A-Z]*\d+)\s*\|\s*"
    r"(?P<title>[^|]+?)\s*\|\s*(?P<evidence>[^|]*?)\s*\|",
    re.M | re.I,
)
BACKLOG_HEADING_RE = re.compile(
    r"^#{2,4}\s+(?P<id>(?:F|BL|SB|OP|S\d+|Step\s*\d+)-?\d+)[\s\-—:]+(?P<title>[^\n]+)",
    re.M | re.I,
)
PHASE_HEADING_RE = re.compile(
    r"^#{1,3}\s+(Phase\s+\d+[^\n]*|Step\s+\d+[^\n]*|Iteration\s+\d+[^\n]*)",
    re.M | re.I,
)
FEATURES_HEADING_RE = re.compile(
    r"^#{1,3}\s*(Features?|Capabilities|What it does|What's included|Implemented)\b",
    re.M | re.I,
)
BULLET_RE = re.compile(r"^\s{0,3}[-*]\s+(.+?)$", re.M)
NUMBER_RE = re.compile(r"^\s{0,3}\d+\.\s+(.+?)$", re.M)
CHECKBOX_RE = re.compile(r"^\s*[-*]\s*\[[ xX]\]\s+(.+?)$", re.M)
BOOTSTRAP_MARKERS = (
    "# AGENTS.md", "<INSTRUCTIONS>", "<local-command-caveat>",
    "<command-name>", "<system-reminder>", "<ide_opened_file>",
    "<environment_context>", "<user_instructions>", "<project_doc>",
)


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return ""


def mine_backlog_files(proj_root, backlog_dir=None):
    """Find SPECIFICATION_BACKLOG.md / *BACKLOG*.md and extract entries.

    Looks in both the project root and (if supplied) in `backlog_dir`
    (typically `output/backlogs/<project>/` populated by the analyst
    subagents or by `harvest_backlogs.py`).

    If the same filename exists in both locations, the backlog_dir copy
    is preferred (the harvested / analyst-generated version is considered
    authoritative). This avoids double-counting.
    """
    seen_basenames = set()
    candidates = []
    # Prefer backlog_dir first, then skip same basename in proj_root.
    search_dirs = []
    if backlog_dir:
        search_dirs.append(backlog_dir)
    search_dirs.append(proj_root)
    for d in search_dirs:
        for pat in ("*BACKLOG*.md", "*backlog*.md", "*Backlog*.md",
                    "FEATURES.md", "features.md"):
            for fp in glob.glob(os.path.join(d, pat)):
                bn = os.path.basename(fp).lower()
                if bn in seen_basenames:
                    continue
                seen_basenames.add(bn)
                candidates.append(fp)
    items = []
    for path in sorted(set(candidates)):
        text = read_text(path)
        if not text:
            continue
        # Track the current phase heading we are under
        phase_positions = [(m.start(), m.group(1).strip())
                           for m in PHASE_HEADING_RE.finditer(text)]
        def phase_at(pos):
            cur = None
            for p, name in phase_positions:
                if p < pos:
                    cur = name
                else:
                    break
            return cur
        for m in BACKLOG_ROW_RE.finditer(text):
            fid = (m.group("id") or "").strip()
            title = (m.group("title") or "").strip()
            evidence = (m.group("evidence") or "").strip()
            if not fid and not title:
                continue
            if title.lower() in ("feature", "--------") or title.startswith("---"):
                continue
            items.append({
                "id":       fid,
                "title":    title,
                "evidence": evidence,
                "phase":    phase_at(m.start()),
                "source":   os.path.basename(path),
            })
        # Also heading-style entries: "### SB-001 — title"
        seen_ids = {(i["id"], i["title"][:40]) for i in items}
        for m in BACKLOG_HEADING_RE.finditer(text):
            fid = (m.group("id") or "").strip()
            title = (m.group("title") or "").strip(" —-:")
            key = (fid, title[:40])
            if key in seen_ids:
                continue
            seen_ids.add(key)
            items.append({
                "id":       fid,
                "title":    title,
                "evidence": "",
                "phase":    phase_at(m.start()),
                "source":   os.path.basename(path),
            })
    return items


def mine_readme_features(proj_root, backlog_dir=None):
    """Pull bullet lists under a Features / Capabilities heading from README.md / REPORT.md."""
    results = []
    search_dirs = [proj_root]
    if backlog_dir:
        search_dirs.append(backlog_dir)
    for d in search_dirs:
        for fn in ("README.md", "REPORT.md"):
            fp = os.path.join(d, fn)
            text = read_text(fp)
            if not text:
                continue
            for m in FEATURES_HEADING_RE.finditer(text):
                start = m.end()
                nxt = re.search(r"\n#{1,6}\s", text[start:])
                end = start + (nxt.start() if nxt else 2000)
                segment = text[start:end]
                for bm in BULLET_RE.finditer(segment):
                    bullet = bm.group(1).strip()
                    if 5 < len(bullet) < 300:
                        results.append(bullet)
                for bm in NUMBER_RE.finditer(segment):
                    bullet = bm.group(1).strip()
                    if 5 < len(bullet) < 300:
                        results.append(bullet)
    # dedupe, preserving order
    seen = set()
    out = []
    for f_ in results:
        k = f_.lower()
        if k in seen: continue
        seen.add(k); out.append(f_)
    return out


def is_bootstrap(text):
    if not text: return True
    t = text.lstrip()[:200]
    return any(m in t for m in BOOTSTRAP_MARKERS)


def mine_prompt_subtasks(turn_files):
    """Walk through user prompts, split each into sub-requests (bullet / numbered items)."""
    out = []
    for fp in turn_files:
        if not os.path.exists(fp): continue
        try:
            with open(fp) as f:
                for line in f:
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    if r.get("role") != "user" or r.get("kind") != "prompt":
                        continue
                    p = r.get("preview","") or ""
                    if is_bootstrap(p):
                        continue
                    ts = r.get("ts")
                    items = []
                    # checkboxes first
                    items += [m for m in CHECKBOX_RE.findall(p)]
                    items += [m for m in BULLET_RE.findall(p) if len(m) < 200]
                    items += [m for m in NUMBER_RE.findall(p) if len(m) < 200]
                    # keep distinct short imperatives
                    seen = set()
                    for it in items:
                        it = re.sub(r"\s+", " ", it).strip()
                        if len(it) < 5 or len(it) > 200:
                            continue
                        if it.lower() in seen:
                            continue
                        seen.add(it.lower())
                        out.append({"ts": ts, "item": it})
                    # if no bullets found, the prompt itself is one request: skip
        except Exception:
            continue
    return out


def mine_git_subjects(git_json_path):
    if not os.path.exists(git_json_path):
        return []
    with open(git_json_path) as f:
        d = json.load(f)
    if not d.get("has_git"):
        return []
    out = []
    for c in d.get("commit_log", []):
        subj = c.get("subject","")
        if not subj or "Merge" in subj.split()[:1]:
            continue
        out.append({"sha": c["sha"][:10], "date": c["date"][:10], "subject": subj})
    return out


def build_ledger(proj, proj_root, turn_files, git_json, backlog_dir=None):
    spec = mine_backlog_files(proj_root, backlog_dir=backlog_dir)
    readme = mine_readme_features(proj_root, backlog_dir=backlog_dir)
    prompts = mine_prompt_subtasks(turn_files)
    commits = mine_git_subjects(git_json)
    # Estimate total unique "feature-ish" items the user/agent captured
    unique_titles = set()
    for it in spec:
        t = (it.get("title") or "").lower().strip()
        if t: unique_titles.add(t[:80])
    for t in readme:
        unique_titles.add(t.lower()[:80])
    return {
        "project": proj,
        "spec_backlog": spec,
        "delivered_from_backlog": len([i for i in spec if i.get("id","").startswith("F-")]),
        "readme_features": readme,
        "prompt_subtasks": prompts,
        "commit_subjects": commits,
        "total_features_proxy": len(unique_titles) + len(prompts),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--projects-root", default=os.path.expanduser("~/SANDBOX"))
    ap.add_argument("--turn-dir", required=True)
    ap.add_argument("--git-dir", required=True)
    ap.add_argument("--backlogs-dir", default=None,
                    help="output/backlogs; when set, SPECIFICATION_BACKLOG.md "
                         "files generated by the analyst subagents are also mined.")
    ap.add_argument("--projects", nargs="+", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    for proj in args.projects:
        root = os.path.join(args.projects_root, proj)
        turn_files = sorted(
            os.path.join(args.turn_dir, fn) for fn in os.listdir(args.turn_dir)
            if fn.startswith(proj + "__") and fn.endswith(".jsonl")
        )
        git_json = os.path.join(args.git_dir, f"{proj}.json")
        backlog_dir = os.path.join(args.backlogs_dir, proj) if args.backlogs_dir else None
        ledger = build_ledger(proj, root, turn_files, git_json, backlog_dir=backlog_dir)
        outp = os.path.join(args.out_dir, f"{proj}.json")
        with open(outp, "w") as f:
            json.dump(ledger, f, indent=2)
        print(f"[ok] {proj}: backlog={len(ledger['spec_backlog'])}, readme={len(ledger['readme_features'])}, "
              f"subtasks={len(ledger['prompt_subtasks'])}, commits={len(ledger['commit_subjects'])}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
