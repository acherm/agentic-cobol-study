#!/usr/bin/env python3
"""Produce a compact, per-line summary of human user prompts with classification hints.
Also detect compaction-continuation and system-like wrappers."""
import json
import re

with open("/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/backlogs/chess-cobol-cc/_work/user_prompts.json") as f:
    ups = json.load(f)

# Classify each prompt: compaction summary (system-injected after auto-compact),
# interrupt marker, system-reminder only, real user input.
COMPACT_HINT = "This session is being continued from a previous conversation"
SYS_REMINDER_HINT = "<system-reminder>"
INTERRUPTED_HINT = "[Request interrupted"
COMMAND_TAG = re.compile(r"<command-name>|<local-command-stdout>")

rows = []
for up in ups:
    txt = up["text"]
    first_line = txt.split("\n", 1)[0][:200]
    tag = "USER"
    if COMPACT_HINT in txt[:300]:
        tag = "COMPACT"
    elif txt.startswith("[Request interrupted"):
        tag = "INTERRUPT"
    elif COMMAND_TAG.search(txt):
        tag = "CMD-OUT"
    elif txt.lstrip().startswith("<system-reminder>"):
        tag = "SYS-REM"
    rows.append((up["event_index"], up["timestamp"], tag, len(txt), first_line))

for idx, ts, tag, n, line in rows:
    print(f"[{idx:>5}] {ts} {tag:<9} len={n:<6} | {line}")

# Tag-count summary
from collections import Counter
c = Counter(r[2] for r in rows)
print("\nTag counts:", c.most_common())
print("Total:", len(rows))
print("Real USER turns:", c["USER"])
