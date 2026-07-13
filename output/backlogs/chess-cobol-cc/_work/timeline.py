#!/usr/bin/env python3
"""Extract milestones: Write/Edit/Bash commands that reference 'phase' or 'v1'/'v2' binaries or cutechess matches.
Also rough per-day activity counts."""
import json
from collections import Counter

PATH = "/Users/mathieuacher/.claude/projects/-Users-mathieuacher-SANDBOX-chess-cobol-cc/9d9bb74e-18ea-4bb9-844c-b4e175998988.jsonl"

evs = []
with open(PATH) as f:
    for line in f:
        line = line.strip()
        if line:
            evs.append(json.loads(line))

per_day = Counter()
cutechess_runs = []
edit_file_history = []

for i, ev in enumerate(evs):
    ts = ev.get("timestamp") or ""
    day = ts[:10]
    per_day[day] += 1
    if ev.get("type") != "assistant":
        continue
    msg = ev.get("message") or {}
    c = msg.get("content") or []
    if not isinstance(c, list):
        continue
    for b in c:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "tool_use":
            name = b.get("name")
            inp = b.get("input") or {}
            if name == "Bash":
                cmd = inp.get("command", "")
                if "cutechess-cli" in cmd or "cutechess" in cmd.lower():
                    cutechess_runs.append({
                        "idx": i,
                        "ts": ts,
                        "cmd": cmd[:400],
                    })

print("Per-day counts (events):")
for day, n in sorted(per_day.items()):
    print(f"  {day}: {n}")

print(f"\nCutechess runs: {len(cutechess_runs)}")
for r in cutechess_runs[:20]:
    print(f"  #{r['idx']:>4} {r['ts']}  {r['cmd'][:200]}")
