#!/usr/bin/env python3
"""Extract assistant text messages between event 3088 (4th compaction) and 3659 (user's last refine Elo) to understand phases 6-9."""
import json

PATH = "/Users/mathieuacher/.claude/projects/-Users-mathieuacher-SANDBOX-chess-cobol-cc/9d9bb74e-18ea-4bb9-844c-b4e175998988.jsonl"

evs = []
with open(PATH) as f:
    for line in f:
        line = line.strip()
        if line:
            evs.append(json.loads(line))

START, STOP = 3089, 3660
# Focus on assistant text blocks
for i in range(START, STOP):
    ev = evs[i]
    if ev.get("type") == "assistant":
        msg = ev.get("message") or {}
        c = msg.get("content") or []
        if not isinstance(c, list):
            continue
        for b in c:
            if isinstance(b, dict) and b.get("type") == "text":
                t = b.get("text", "").strip()
                if t:
                    # Filter short tool-prep one-liners? keep all but trim
                    print(f"\n[ASST #{i}] {ev.get('timestamp')}\n{t[:700]}")
