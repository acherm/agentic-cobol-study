#!/usr/bin/env python3
"""Inspect raw user prompts: print full text of short ones + tags found in longer ones."""
import json
import re

with open("/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/backlogs/chess-cobol-cc/_work/user_prompts.json") as f:
    ups = json.load(f)

# Print short prompts in full; for longer ones, extract only non-tag text.
tag_regex = re.compile(r"<([a-zA-Z0-9_-]+)>")

real_user = []
for up in ups:
    t = up["text"]
    if "This session is being continued from a previous conversation" in t[:300]:
        continue
    if t.startswith("[Request interrupted"):
        continue
    if t.strip().startswith("<task-notification>"):
        continue
    # otherwise keep
    real_user.append(up)

print(f"Real user-typed turns: {len(real_user)}")
for up in real_user:
    sep = "=" * 78
    print(sep)
    print(f"EVENT {up['event_index']} @ {up['timestamp']}  uuid={up['uuid']}")
    # Strip system-reminder blocks that appear in-line
    t = up["text"]
    # remove system-reminder blocks
    cleaned = re.sub(r"<system-reminder>.*?</system-reminder>", "", t, flags=re.DOTALL)
    # remove command-name blocks
    cleaned = re.sub(r"<command-name>.*?</command-name>", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"<command-message>.*?</command-message>", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"<command-args>.*?</command-args>", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"<local-command-stdout>.*?</local-command-stdout>", "", cleaned, flags=re.DOTALL)
    cleaned = cleaned.strip()
    print(cleaned[:2000])
