#!/usr/bin/env python3
"""Parse Claude Code and Codex session logs.

Emits one JSON summary per session with:
  agent, model, version, session_id, project, start, end, duration_s,
  user_turns, assistant_turns, tool_calls, tool_breakdown,
  input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens,
  reasoning_tokens, cost_usd, first_user_prompt
"""
import json, os, sys, re, argparse
from collections import Counter
from datetime import datetime

# Pricing: USD per 1M tokens (best-effort, as of 2026). Conservative estimates.
# Source: anthropic/openai published public rates; cache_read discount applied.
PRICING = {
    # Claude
    "claude-opus-4-6":        {"in": 15.0, "out": 75.0, "cache_read": 1.5,  "cache_create": 18.75},
    "claude-opus-4":          {"in": 15.0, "out": 75.0, "cache_read": 1.5,  "cache_create": 18.75},
    "claude-opus-4-1":        {"in": 15.0, "out": 75.0, "cache_read": 1.5,  "cache_create": 18.75},
    "claude-opus-4-5":        {"in": 15.0, "out": 75.0, "cache_read": 1.5,  "cache_create": 18.75},
    "claude-sonnet-4-5":      {"in": 3.0,  "out": 15.0, "cache_read": 0.30, "cache_create": 3.75},
    "claude-sonnet-4":        {"in": 3.0,  "out": 15.0, "cache_read": 0.30, "cache_create": 3.75},
    "claude-sonnet-4-6":      {"in": 3.0,  "out": 15.0, "cache_read": 0.30, "cache_create": 3.75},
    "claude-haiku-4-5":       {"in": 1.0,  "out": 5.0,  "cache_read": 0.10, "cache_create": 1.25},
    "claude-3-5-sonnet":      {"in": 3.0,  "out": 15.0, "cache_read": 0.30, "cache_create": 3.75},
    "claude-3-5-haiku":       {"in": 0.80, "out": 4.0,  "cache_read": 0.08, "cache_create": 1.0},
    # Codex (GPT)
    "gpt-5":     {"in": 1.25, "out": 10.0, "cache_read": 0.125, "cache_create": 1.25},
    "gpt-5.4":   {"in": 1.25, "out": 10.0, "cache_read": 0.125, "cache_create": 1.25},
    "gpt-5.1":   {"in": 1.25, "out": 10.0, "cache_read": 0.125, "cache_create": 1.25},
    "gpt-4o":    {"in": 2.5,  "out": 10.0, "cache_read": 1.25,  "cache_create": 2.5},
    "o3":        {"in": 2.0,  "out": 8.0,  "cache_read": 0.5,   "cache_create": 2.0},
    "o4-mini":   {"in": 1.1,  "out": 4.4,  "cache_read": 0.275, "cache_create": 1.1},
    "codex-mini-latest": {"in": 1.5, "out": 6.0, "cache_read": 0.375, "cache_create": 1.5},
}

def price_for(model):
    if not model:
        return PRICING["claude-opus-4-6"]
    m = model.lower()
    # normalize
    m = re.sub(r"\[.*?\]", "", m)
    m = m.split("-2")[0] if re.search(r"-2\d{7}", m) else m
    if m in PRICING:
        return PRICING[m]
    # fuzzy
    for key in PRICING:
        if key in m or m.startswith(key):
            return PRICING[key]
    if "opus" in m:   return PRICING["claude-opus-4-6"]
    if "sonnet" in m: return PRICING["claude-sonnet-4-5"]
    if "haiku" in m:  return PRICING["claude-haiku-4-5"]
    if "gpt-5" in m:  return PRICING["gpt-5"]
    if "gpt-4o" in m: return PRICING["gpt-4o"]
    return PRICING["claude-opus-4-6"]


def parse_iso(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def parse_claude_code(path):
    """Parse a Claude Code JSONL session file."""
    session_id = os.path.basename(path).replace(".jsonl", "")
    project_dir = os.path.basename(os.path.dirname(path))
    first_ts = None
    last_ts = None
    user_turns = 0
    assistant_turns = 0
    tool_calls = Counter()
    in_toks = out_toks = cache_read = cache_create = reasoning_toks = 0
    models = Counter()
    first_prompt = None
    version = None
    activities = Counter()
    text_chars = 0
    n_lines = 0

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            n_lines += 1
            try:
                d = json.loads(line)
            except Exception:
                continue
            ts = d.get("timestamp")
            if ts:
                t = parse_iso(ts)
                if t:
                    if first_ts is None or t < first_ts:
                        first_ts = t
                    if last_ts is None or t > last_ts:
                        last_ts = t
            v = d.get("version") or d.get("cliVersion")
            if v and not version:
                version = v
            t = d.get("type")
            msg = d.get("message") if isinstance(d.get("message"), dict) else None
            if t == "user" and msg:
                content = msg.get("content")
                if isinstance(content, str):
                    user_turns += 1
                    if first_prompt is None:
                        first_prompt = content[:500]
                elif isinstance(content, list):
                    has_tool_result = any(isinstance(c, dict) and c.get("type") == "tool_result" for c in content)
                    if not has_tool_result:
                        user_turns += 1
                        if first_prompt is None:
                            txt = " ".join(c.get("text","") for c in content if isinstance(c, dict) and c.get("type")=="text")
                            if txt:
                                first_prompt = txt[:500]
            elif t == "assistant" and msg:
                assistant_turns += 1
                model = msg.get("model")
                if model:
                    models[model] += 1
                content = msg.get("content") or []
                if isinstance(content, list):
                    for c in content:
                        if not isinstance(c, dict):
                            continue
                        if c.get("type") == "tool_use":
                            tool_calls[c.get("name","unknown")] += 1
                        elif c.get("type") == "text":
                            text_chars += len(c.get("text",""))
                usage = msg.get("usage") or {}
                in_toks       += usage.get("input_tokens", 0) or 0
                out_toks      += usage.get("output_tokens", 0) or 0
                cache_read    += usage.get("cache_read_input_tokens", 0) or 0
                cache_create  += usage.get("cache_creation_input_tokens", 0) or 0
    # cost
    model_key = models.most_common(1)[0][0] if models else None
    p = price_for(model_key)
    cost = (in_toks*p["in"] + out_toks*p["out"] + cache_read*p["cache_read"] + cache_create*p["cache_create"]) / 1_000_000
    duration_s = int((last_ts - first_ts).total_seconds()) if first_ts and last_ts else 0
    return {
        "agent": "Claude Code",
        "model": model_key,
        "all_models": dict(models),
        "version": version,
        "session_id": session_id,
        "project_dir": project_dir,
        "file": path,
        "file_size": os.path.getsize(path),
        "n_lines": n_lines,
        "start": first_ts.isoformat() if first_ts else None,
        "end": last_ts.isoformat() if last_ts else None,
        "duration_s": duration_s,
        "user_turns": user_turns,
        "assistant_turns": assistant_turns,
        "tool_calls_total": sum(tool_calls.values()),
        "tool_breakdown": dict(tool_calls),
        "input_tokens": in_toks,
        "output_tokens": out_toks,
        "cache_read_tokens": cache_read,
        "cache_creation_tokens": cache_create,
        "reasoning_tokens": 0,
        "cost_usd": round(cost, 4),
        "first_user_prompt": first_prompt,
        "assistant_text_chars": text_chars,
    }


def parse_codex(path):
    """Parse a Codex rollout JSONL file."""
    session_id = None
    cwd = None
    version = None
    models = Counter()
    first_ts = None
    last_ts = None
    user_turns = 0
    assistant_turns = 0
    tool_calls = Counter()
    in_toks = out_toks = cache_read = reasoning_toks = 0
    first_prompt = None
    base_instr_len = 0
    n_lines = 0

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            n_lines += 1
            try:
                d = json.loads(line)
            except Exception:
                continue
            ts = d.get("timestamp")
            if ts:
                t = parse_iso(ts)
                if t:
                    if first_ts is None or t < first_ts:
                        first_ts = t
                    if last_ts is None or t > last_ts:
                        last_ts = t
            t = d.get("type")
            p = d.get("payload") or {}
            if t == "session_meta":
                session_id = p.get("id") or session_id
                cwd = p.get("cwd") or cwd
                version = p.get("cli_version") or version
                bi = p.get("base_instructions", {})
                if isinstance(bi, dict):
                    base_instr_len = len(bi.get("text",""))
            elif t == "turn_context":
                m = p.get("model")
                if m:
                    models[m] += 1
            elif t == "event_msg":
                et = p.get("type")
                if et == "user_message":
                    user_turns += 1
                    if first_prompt is None:
                        m = p.get("message") or p.get("text") or ""
                        if isinstance(m, str):
                            first_prompt = m[:500]
                elif et == "agent_message":
                    assistant_turns += 1
                elif et == "token_count":
                    info = p.get("info")
                    if info:
                        tu = info.get("total_token_usage") or {}
                        in_toks = max(in_toks, tu.get("input_tokens", 0) or 0)
                        out_toks = max(out_toks, tu.get("output_tokens", 0) or 0)
                        cache_read = max(cache_read, tu.get("cached_input_tokens", 0) or 0)
                        reasoning_toks = max(reasoning_toks, tu.get("reasoning_output_tokens", 0) or 0)
            elif t == "response_item":
                rt = p.get("type")
                if rt == "function_call":
                    tool_calls[p.get("name","unknown")] += 1
                elif rt == "custom_tool_call":
                    tool_calls[p.get("name","custom")] += 1
    model_key = models.most_common(1)[0][0] if models else None
    pr = price_for(model_key)
    net_in = max(in_toks - cache_read, 0)
    cost = (net_in*pr["in"] + cache_read*pr["cache_read"] + out_toks*pr["out"]) / 1_000_000
    duration_s = int((last_ts - first_ts).total_seconds()) if first_ts and last_ts else 0
    project_dir = os.path.basename(cwd) if cwd else "unknown"
    return {
        "agent": "Codex",
        "model": model_key,
        "all_models": dict(models),
        "version": version,
        "session_id": session_id or os.path.basename(path),
        "project_dir": project_dir,
        "project_cwd": cwd,
        "file": path,
        "file_size": os.path.getsize(path),
        "n_lines": n_lines,
        "start": first_ts.isoformat() if first_ts else None,
        "end": last_ts.isoformat() if last_ts else None,
        "duration_s": duration_s,
        "user_turns": user_turns,
        "assistant_turns": assistant_turns,
        "tool_calls_total": sum(tool_calls.values()),
        "tool_breakdown": dict(tool_calls),
        "input_tokens": in_toks,
        "output_tokens": out_toks,
        "cache_read_tokens": cache_read,
        "cache_creation_tokens": 0,
        "reasoning_tokens": reasoning_toks,
        "cost_usd": round(cost, 4),
        "first_user_prompt": first_prompt,
        "base_instructions_len": base_instr_len,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cc-dir", default=os.path.expanduser("~/.claude/projects"))
    ap.add_argument("--codex-dir", default=os.path.expanduser("~/.codex/sessions"))
    ap.add_argument("--project-filter", help="substring of cwd/project to include")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    results = []

    # Claude Code
    if os.path.isdir(args.cc_dir):
        for proj in sorted(os.listdir(args.cc_dir)):
            if args.project_filter and args.project_filter.lower() not in proj.lower():
                continue
            p = os.path.join(args.cc_dir, proj)
            if not os.path.isdir(p):
                continue
            for fn in sorted(os.listdir(p)):
                if fn.endswith(".jsonl"):
                    full = os.path.join(p, fn)
                    try:
                        r = parse_claude_code(full)
                        results.append(r)
                        print(f"[cc] {proj} {fn} duration={r['duration_s']}s tools={r['tool_calls_total']}", file=sys.stderr)
                    except Exception as e:
                        print(f"[cc-err] {full}: {e}", file=sys.stderr)

    # Codex
    if os.path.isdir(args.codex_dir):
        for root, _, files in os.walk(args.codex_dir):
            for fn in files:
                if not fn.endswith(".jsonl"):
                    continue
                full = os.path.join(root, fn)
                try:
                    r = parse_codex(full)
                    cwd = r.get("project_cwd") or ""
                    if args.project_filter and args.project_filter.lower() not in cwd.lower():
                        continue
                    results.append(r)
                    print(f"[codex] {r.get('project_dir')} {fn} duration={r['duration_s']}s tools={r['tool_calls_total']}", file=sys.stderr)
                except Exception as e:
                    print(f"[codex-err] {full}: {e}", file=sys.stderr)

    with open(args.out, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Wrote {len(results)} session summaries to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
