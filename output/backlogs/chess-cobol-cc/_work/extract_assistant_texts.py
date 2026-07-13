#!/usr/bin/env python3
"""Extract assistant text messages around key user prompts + the compaction summaries."""
import json

PATH = "/Users/mathieuacher/.claude/projects/-Users-mathieuacher-SANDBOX-chess-cobol-cc/9d9bb74e-18ea-4bb9-844c-b4e175998988.jsonl"

def load():
    evs = []
    with open(PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            evs.append(json.loads(line))
    return evs

def assistant_text(ev):
    msg = ev.get("message") or {}
    if msg.get("role") != "assistant":
        return None
    content = msg.get("content") or []
    if not isinstance(content, list):
        return None
    texts = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            texts.append(block.get("text", ""))
    return "\n".join(texts) if texts else None

evs = load()
# Target events: 5..17 (init plan before Phase 1), 19..100 (Phase 1), 104..235 (Phase 2), 237..262 (Phase 3-4 start), 263 compaction
TARGETS = [
    (5, 18),       # planning after PL-ROOT
    (236, 262),    # just before first compaction; assistant summary
    (855, 870),    # around "please improve the Elo" context
    (1655, 1665),  # around 3rd compaction
    (3650, 3680),  # around "refine the Elo"
]
for lo, hi in TARGETS:
    print(f"\n================ RANGE {lo}..{hi} ================")
    for i in range(lo, min(hi + 1, len(evs))):
        ev = evs[i]
        if ev.get("type") == "user":
            msg = ev.get("message") or {}
            c = msg.get("content")
            if isinstance(c, str):
                print(f"[USER #{i}] {c[:400]}")
            elif isinstance(c, list):
                for b in c:
                    if isinstance(b, dict) and b.get("type") == "text":
                        print(f"[USER #{i}] {b.get('text', '')[:400]}")
        elif ev.get("type") == "assistant":
            t = assistant_text(ev)
            if t:
                print(f"[ASST #{i}] {t[:1500]}")

# Print the first compaction summary in full
print("\n================ COMPACT @ 263 ================")
ev = evs[263]
msg = ev.get("message") or {}
c = msg.get("content")
if isinstance(c, str):
    print(c[:8000])
elif isinstance(c, list):
    for b in c:
        if isinstance(b, dict) and b.get("type") == "text":
            print(b.get("text", "")[:8000])
