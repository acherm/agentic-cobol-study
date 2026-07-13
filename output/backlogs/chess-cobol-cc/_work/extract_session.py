#!/usr/bin/env python3
"""Extract user prompts + structural summary from the Claude Code session JSONL."""
import json
import sys
from collections import Counter

PATH = "/Users/mathieuacher/.claude/projects/-Users-mathieuacher-SANDBOX-chess-cobol-cc/9d9bb74e-18ea-4bb9-844c-b4e175998988.jsonl"
OUT_DIR = "/Users/mathieuacher/SANDBOX/cobol-meta-analysis/output/backlogs/chess-cobol-cc/_work"


def load_events():
    events = []
    with open(PATH, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
                events.append(ev)
            except Exception as e:
                print(f"PARSE ERR line {i}: {e}", file=sys.stderr)
    return events


def user_text_content(ev):
    """Return human-user text only (exclude tool_result messages)."""
    msg = ev.get("message")
    if not msg or msg.get("role") != "user":
        return None
    content = msg.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for block in content:
            if not isinstance(block, dict):
                continue
            t = block.get("type")
            if t == "text":
                texts.append(block.get("text", ""))
            elif t == "tool_result":
                return None
        if texts:
            return "\n".join(texts)
    return None


def assistant_text_content(ev):
    msg = ev.get("message")
    if not msg or msg.get("role") != "assistant":
        return None
    content = msg.get("content")
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))
        if texts:
            return "\n".join(texts)
    return None


def main():
    events = load_events()
    print(f"TOTAL events: {len(events)}")
    type_counts = Counter(ev.get("type", "?") for ev in events)
    print("Event types:", type_counts.most_common())

    versions = Counter()
    models = Counter()
    for ev in events:
        if ev.get("type") == "assistant":
            v = ev.get("version") or ev.get("cliVersion")
            if v:
                versions[v] += 1
            m = (ev.get("message") or {}).get("model")
            if m:
                models[m] += 1
    print("Versions:", versions.most_common(5))
    print("Models:", models.most_common(5))

    timestamps = [ev.get("timestamp") for ev in events if ev.get("timestamp")]
    if timestamps:
        print("First ts:", timestamps[0])
        print("Last ts:", timestamps[-1])

    user_prompts = []
    for idx, ev in enumerate(events):
        if ev.get("type") != "user":
            continue
        text = user_text_content(ev)
        if text is None:
            continue
        stripped = text.strip()
        if not stripped:
            continue
        user_prompts.append({
            "event_index": idx,
            "timestamp": ev.get("timestamp"),
            "uuid": ev.get("uuid"),
            "parentUuid": ev.get("parentUuid"),
            "text": stripped,
        })
    print(f"User-text events: {len(user_prompts)}")

    with open(f"{OUT_DIR}/user_prompts.json", "w") as f:
        json.dump(user_prompts, f, indent=2)

    for up in user_prompts[:5]:
        preview = up["text"][:500].replace("\n", " | ")
        print(f"[{up['event_index']}] {up['timestamp']} :: {preview}")

    tool_counts = Counter()
    for ev in events:
        if ev.get("type") != "assistant":
            continue
        msg = ev.get("message") or {}
        content = msg.get("content") or []
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                tool_counts[block.get("name", "?")] += 1
    print("Tool-use counts:", tool_counts.most_common())

    # Extract bash commands
    bash_cmds = []
    for ev in events:
        if ev.get("type") != "assistant":
            continue
        msg = ev.get("message") or {}
        content = msg.get("content") or []
        if not isinstance(content, list):
            continue
        for block in content:
            if (isinstance(block, dict) and block.get("type") == "tool_use"
                    and block.get("name") == "Bash"):
                cmd = (block.get("input") or {}).get("command", "")
                bash_cmds.append({"ts": ev.get("timestamp"), "cmd": cmd[:400]})
    with open(f"{OUT_DIR}/bash_cmds.json", "w") as f:
        json.dump(bash_cmds, f, indent=2)
    print(f"bash cmd count: {len(bash_cmds)}")


if __name__ == "__main__":
    main()
