#!/usr/bin/env python3
"""Dump all compaction summaries in full."""
import json

PATH = "/Users/mathieuacher/.claude/projects/-Users-mathieuacher-SANDBOX-chess-cobol-cc/9d9bb74e-18ea-4bb9-844c-b4e175998988.jsonl"
OUT = "/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/backlogs/chess-cobol-cc/_work/compactions.md"

evs = []
with open(PATH) as f:
    for line in f:
        line = line.strip()
        if line:
            evs.append(json.loads(line))

marker = "This session is being continued from a previous conversation"

out = []
for i, ev in enumerate(evs):
    if ev.get("type") != "user":
        continue
    msg = ev.get("message") or {}
    c = msg.get("content")
    text = None
    if isinstance(c, str):
        text = c
    elif isinstance(c, list):
        for b in c:
            if isinstance(b, dict) and b.get("type") == "text":
                text = b.get("text", "")
                break
    if text and marker in text[:300]:
        out.append(f"\n\n# COMPACTION at event #{i} ({ev.get('timestamp')})\n\n{text}")

with open(OUT, "w") as f:
    f.write("".join(out))
print(f"Wrote {len(out)} compactions to {OUT}; total chars={sum(len(x) for x in out)}")
