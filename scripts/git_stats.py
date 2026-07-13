#!/usr/bin/env python3
"""Extract lightweight git-history statistics for a project folder.

Emits JSON: { has_git, commits, first_commit, last_commit, authors, churn_by_commit }.
If the folder has no `.git`, emits {has_git: false}.
"""
import argparse, json, os, subprocess, sys


def run(cmd, cwd):
    try:
        r = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True, check=False)
        return r.stdout
    except Exception:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    root = args.project_root
    git_dir = os.path.join(root, ".git")
    data = {"root": root}
    if not os.path.isdir(git_dir):
        data["has_git"] = False
        with open(args.out, "w") as f:
            json.dump(data, f, indent=2)
        return
    data["has_git"] = True
    # commits
    log = run(["git", "log", "--all", "--pretty=format:%H|%aI|%an|%s"], root)
    commits = []
    for line in log.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({"sha": parts[0], "date": parts[1],
                            "author": parts[2], "subject": parts[3]})
    data["commits"] = len(commits)
    data["commit_log"] = commits
    if commits:
        data["first_commit"] = commits[-1]["date"]
        data["last_commit"] = commits[0]["date"]
    # authors
    authors = {}
    for c in commits:
        authors[c["author"]] = authors.get(c["author"], 0) + 1
    data["authors"] = authors
    # churn
    shortstat = run(["git", "log", "--all", "--shortstat", "--pretty=format:::COMMIT::%H|%aI"], root)
    files_changed_total = 0
    ins_total = 0
    del_total = 0
    per_commit = []
    cur = None
    for line in shortstat.splitlines():
        if line.startswith("::COMMIT::"):
            if cur:
                per_commit.append(cur)
            sha, iso = line[len("::COMMIT::"):].split("|", 1)
            cur = {"sha": sha, "date": iso, "files": 0, "ins": 0, "del": 0}
        else:
            s = line.strip()
            if not s or not cur:
                continue
            import re
            m = re.search(r"(\d+) files? changed", s)
            if m: cur["files"] = int(m.group(1)); files_changed_total += cur["files"]
            m = re.search(r"(\d+) insertions?\(\+\)", s)
            if m: cur["ins"] = int(m.group(1)); ins_total += cur["ins"]
            m = re.search(r"(\d+) deletions?\(\-\)", s)
            if m: cur["del"] = int(m.group(1)); del_total += cur["del"]
    if cur:
        per_commit.append(cur)
    data["churn"] = {
        "files_changed_total": files_changed_total,
        "insertions_total": ins_total,
        "deletions_total": del_total,
        "per_commit": per_commit,
    }
    with open(args.out, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {args.out}: {len(commits)} commits, {ins_total}+/{del_total}-", file=sys.stderr)


if __name__ == "__main__":
    main()
