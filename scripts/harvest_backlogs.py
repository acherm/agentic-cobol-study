#!/usr/bin/env python3
"""Harvest already-existing backlog artefacts from each project folder.

Looks for any of these at the project root:
  SPECIFICATION_BACKLOG.md, SPECIFICATION.md, BACKLOG.md, FEATURES.md,
  ARCHITECTURE.md, REPLAY_PROMPTS.md, REPORT.md, APPENDIX.json, appendix.json

and copies them to `output/backlogs/<project>/` (read-only snapshot). Also
writes `output/backlogs/status.json` summarizing which projects already have
a SPECIFICATION_BACKLOG (so we know where the analyst still needs to run).
"""
import argparse, json, os, shutil, sys

WANTED = [
    "SPECIFICATION_BACKLOG.md",
    "SPECIFICATION.md",
    "BACKLOG.md",
    "FEATURES.md",
    "ARCHITECTURE.md",
    "REPLAY_PROMPTS.md",
    "REPORT.md",
    "APPENDIX.json",
    "appendix.json",
    "TRUST.md",
    "VERIFICATION_REPORT.md",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--projects-root", default=os.path.expanduser("~/SANDBOX"))
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--projects", nargs="+", required=True)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    status = {}
    for proj in args.projects:
        src_dir = os.path.join(args.projects_root, proj)
        dst_dir = os.path.join(args.out_dir, proj)
        os.makedirs(dst_dir, exist_ok=True)
        found = []
        has_backlog = False
        for fn in WANTED:
            fp = os.path.join(src_dir, fn)
            if os.path.isfile(fp):
                shutil.copy2(fp, os.path.join(dst_dir, fn))
                found.append(fn)
                if fn == "SPECIFICATION_BACKLOG.md":
                    has_backlog = True
        status[proj] = {
            "has_specification_backlog": has_backlog,
            "harvested_files": found,
        }
        print(f"[{'✓' if has_backlog else '·'}] {proj}: {', '.join(found) or '—'}",
              file=sys.stderr)
    with open(os.path.join(args.out_dir, "status.json"), "w") as f:
        json.dump(status, f, indent=2)
    # Print summary
    missing = [p for p, v in status.items() if not v["has_specification_backlog"]]
    print(f"\nMissing SPECIFICATION_BACKLOG.md in {len(missing)} projects: {', '.join(missing)}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
