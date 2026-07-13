#!/usr/bin/env python3
"""Extract assistant text messages after event 3659 to the end."""
import json

PATH = "/Users/mathieuacher/.claude/projects/-Users-mathieuacher-SANDBOX-chess-cobol-cc/9d9bb74e-18ea-4bb9-844c-b4e175998988.jsonl"

evs = []
with open(PATH) as f:
    for line in f:
        line = line.strip()
        if line:
            evs.append(json.loads(line))

START = 3660
for i in range(START, len(evs)):
    ev = evs[i]
    if ev.get("type") == "assistant":
        msg = ev.get("message") or {}
        c = msg.get("content") or []
        if not isinstance(c, list):
            continue
        for b in c:
            if isinstance(b, dict) and b.get("type") == "text":
                t = b.get("text", "")
                if t.strip():
                    print(f"\n[ASST #{i}] {ev.get('timestamp')}\n{t[:1200]}")

# Count bash commands in this range
cnt = 0
for i in range(START, len(evs)):
    ev = evs[i]
    if ev.get("type") != "assistant":
        continue
    msg = ev.get("message") or {}
    c = msg.get("content") or []
    if not isinstance(c, list):
        continue
    for b in c:
        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Bash":
            cnt += 1
print(f"\n\nBash commands after #{START}: {cnt}")
