#!/usr/bin/env python3
"""Compute repo statistics for chess-cobol-cc (read-only)."""
import os
from pathlib import Path

ROOT = Path("/Users/mathieuacher/SANDBOX/chess-cobol-cc")

# Ignore default patterns
IGNORE_DIRS = {"node_modules", "dist", "build", "target", ".venv", "vendor", "coverage", ".git"}

files = []
dirs = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    # prune
    dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
    rel = Path(dirpath).relative_to(ROOT)
    if str(rel) != ".":
        dirs.append(str(rel))
    for fn in filenames:
        files.append(Path(dirpath) / fn)

print(f"Total files: {len(files)}")
print(f"Total dirs (excluding root): {len(dirs)}")

def ext(p):
    n = p.name
    if "." in n:
        return n.rsplit(".", 1)[-1].lower()
    return "<noext>"

# Classification
cats = {"cobol": [], "c_generated": [], "h_generated": [],
        "pgn_data": [], "binary": [], "config": [], "object": [], "other": []}

for p in files:
    n = p.name
    e = ext(p)
    if e == "cob":
        cats["cobol"].append(p)
    elif e == "c":
        cats["c_generated"].append(p)
    elif e == "h":
        cats["h_generated"].append(p)
    elif e == "pgn":
        cats["pgn_data"].append(p)
    elif e == "json":
        cats["config"].append(p)
    elif e == "o":
        cats["object"].append(p)
    else:
        # Identify binaries: executable no extension, large
        if n.startswith("chess-engine") and "." not in n:
            cats["binary"].append(p)
        elif n == "cobolchess":
            cats["binary"].append(p)
        else:
            cats["other"].append(p)

for k, v in cats.items():
    print(f"\nCategory {k}: {len(v)}")
    for p in v:
        try:
            sz = p.stat().st_size
        except Exception:
            sz = -1
        # LOC for text
        loc = "-"
        if k in ("cobol", "c_generated", "h_generated", "config", "other", "pgn_data"):
            try:
                with open(p, "rb") as f:
                    data = f.read()
                # Avoid binary counts
                loc = data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)
            except Exception:
                loc = "?"
        print(f"  {p.relative_to(ROOT)}  size={sz}  loc={loc}")
