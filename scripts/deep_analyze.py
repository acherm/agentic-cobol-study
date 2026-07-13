#!/usr/bin/env python3
"""Per-turn extraction from Claude Code and Codex session JSONL files.

Writes one `.jsonl` per session into `--out-dir`, with one record per
timeline event (user prompt, assistant message, tool call, tool result).
Records are small and uniform so downstream aggregation is cheap.

Record schema (one per line):
  {
    "agent":   "cc"|"codex",
    "session": "<id>",
    "i":       <event index>,
    "ts":      "<iso-8601>" | null,
    "role":    "user"|"assistant"|"tool_result"|"thinking"|"turn_context",
    "kind":    "prompt"|"tool_use"|"text"|"tool_output"|"reasoning",
    "tool":    "<tool name>"           # if kind == tool_use / tool_output
    "text_len": int,
    "preview": "<first 4000 chars>",
    "is_error": bool,
    "error_tags": ["cobc","gcc","traceback",...],
    "activity": "implement|fix|build|test|...",
    "gap_s":   int                      # seconds since previous event
  }
"""
import argparse, json, os, re, sys
from datetime import datetime

# --- classifiers -------------------------------------------------------------

ERROR_PATTERNS = [
    (re.compile(r"cobc:\s*\S+?:\d+:\s*error", re.I), "cobc"),
    (re.compile(r"\bsyntax error\b", re.I), "cobc"),
    (re.compile(r"\bundefined reference\b", re.I), "linker"),
    (re.compile(r"error:\s", re.I), "cc"),
    (re.compile(r"\bsegmentation fault\b", re.I), "segfault"),
    (re.compile(r"\bbus error\b", re.I), "busfault"),
    (re.compile(r"Traceback \(most recent call last\)"), "python"),
    (re.compile(r"\bFAIL(ED)?\b"), "testfail"),
    (re.compile(r"\bAssertionError\b"), "assert"),
    (re.compile(r"\babort(ed)?\b", re.I), "abort"),
    (re.compile(r"\bno such file\b", re.I), "missing"),
    (re.compile(r"command not found", re.I), "missing-cmd"),
    (re.compile(r"\bpermission denied\b", re.I), "perm"),
    (re.compile(r"\bexit(ed)? with code (?!0\b)\d+", re.I), "exit-nonzero"),
    (re.compile(r"\bstatus 1\b|\berror 1\b"), "exit-nonzero"),
]

ACTIVITY_USER_KWS = [
    ("spec",      ["spec", "specification", "architecture", "design", "feature backlog"]),
    ("fix",       ["fix", "bug", "error", "broken", "segfault", "doesn't work", "crash", "wrong"]),
    ("test",      ["test", "benchmark", "evaluate", "measure", "elo", "verify", "verification"]),
    ("doc",       ["readme", "document", "explain", "describe", "report"]),
    ("optimize",  ["optimize", "optimis", "faster", "slower", "perf"]),
    ("port",      ["port", "translate", "rewrite", "convert", "migrate"]),
    ("research",  ["analyze", "analyse", "investigate", "compare", "study", "research"]),
    ("refactor",  ["refactor", "clean up", "cleanup", "restructure", "rename"]),
    ("build",     ["compile", "build", "makefile", "gnucobol", "cobc ", "gcc "]),
    ("review",    ["review", "audit", "assess", "check that"]),
    ("implement", ["implement", "add ", "support ", "write a", "create", "build a"]),
]

ACTIVITY_TOOL_RULES = {
    # CC tools
    "Edit": "implement", "Write": "implement", "NotebookEdit": "implement",
    "Read": "research", "Grep": "research", "Glob": "research", "WebFetch": "research",
    "WebSearch": "research",
    "TaskCreate": "meta", "TaskUpdate": "meta", "TaskList": "meta", "TaskGet": "meta",
    "TaskOutput": "meta", "TaskStop": "meta", "Agent": "meta", "ToolSearch": "meta",
    # Codex tools
    "apply_patch": "implement",
    "update_plan": "meta",
    "write_stdin": "test",
    "wait_agent": "meta",
    "request_user_input": "meta",
}

BASH_BUILD_RE = re.compile(r"\b(cobc|gcc|g\+\+|clang|make|cargo)\b")
BASH_TEST_RE  = re.compile(r"\b(pytest|./run_tests|cutechess|./\w*test|ctest|npm test|go test)\b")
BASH_DEBUG_RE = re.compile(r"\b(gdb|lldb|strace|dtrace|objdump|nm\s)\b")


def classify_user_text(s):
    if not s:
        return "unknown"
    t = s.lower()
    for label, kws in ACTIVITY_USER_KWS:
        for kw in kws:
            if kw in t:
                return label
    return "other"


def classify_bash(cmd):
    if not cmd:
        return "build"
    c = cmd.lower()
    if BASH_TEST_RE.search(c):  return "test"
    if BASH_BUILD_RE.search(c): return "build"
    if BASH_DEBUG_RE.search(c): return "fix"
    if any(k in c for k in ("git commit","git push","git log","git status")): return "meta"
    if c.strip().startswith(("./",)) or "bin/" in c:  # running built artefact
        return "test"
    if any(k in c for k in ("cat ","ls ","head","tail","grep")):
        return "research"
    return "build"


def classify_assistant_tool(tool_name, input_obj):
    if tool_name in ACTIVITY_TOOL_RULES:
        return ACTIVITY_TOOL_RULES[tool_name]
    if tool_name == "Bash" and isinstance(input_obj, dict):
        return classify_bash(input_obj.get("command", ""))
    if tool_name == "exec_command" and isinstance(input_obj, dict):
        return classify_bash(input_obj.get("cmd", ""))
    return "other"


def detect_errors(text):
    if not text:
        return [], False
    tags = set()
    for rx, tag in ERROR_PATTERNS:
        if rx.search(text):
            tags.add(tag)
    return sorted(tags), bool(tags)


def parse_iso(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


# --- Claude Code session ----------------------------------------------------

def analyze_claude_code(path, out):
    session = os.path.basename(path).replace(".jsonl", "")
    prev = None
    i = 0
    # Map tool_use_id -> tool name so we can tag the matching tool_result
    tool_id_to_name = {}
    with open(path, "r", encoding="utf-8", errors="replace") as f, open(out, "w") as w:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            ts = parse_iso(d.get("timestamp"))
            gap = int((ts - prev).total_seconds()) if (ts and prev) else 0
            t = d.get("type")
            msg = d.get("message") if isinstance(d.get("message"), dict) else None
            if not msg:
                continue
            if t == "user":
                content = msg.get("content")
                if isinstance(content, str):
                    rec = {"agent":"cc","session":session,"i":i,
                           "ts": ts.isoformat() if ts else None,"gap_s":gap,
                           "role":"user","kind":"prompt",
                           "text_len":len(content),
                           "preview":content[:4000],
                           "activity": classify_user_text(content)}
                    w.write(json.dumps(rec) + "\n"); i += 1
                elif isinstance(content, list):
                    tool_results = [c for c in content if isinstance(c,dict) and c.get("type")=="tool_result"]
                    texts = [c for c in content if isinstance(c,dict) and c.get("type")=="text"]
                    if tool_results:
                        for tr in tool_results:
                            body = tr.get("content")
                            if isinstance(body, list):
                                out_txt = "".join(x.get("text","") for x in body if isinstance(x,dict))
                            else:
                                out_txt = body or ""
                            out_txt = str(out_txt)
                            tuid = tr.get("tool_use_id")
                            tool_name = tool_id_to_name.get(tuid, "")
                            # Only apply error detection to tools that execute
                            # commands; skip passive readers so "error:" strings
                            # inside source code don't create false positives.
                            passive_tools = {"Read","Grep","Glob","WebFetch","WebSearch","TaskList","TaskGet","TaskOutput"}
                            if tool_name in passive_tools:
                                is_err = bool(tr.get("is_error"))
                                tags = []
                            else:
                                tags, is_err = detect_errors(out_txt)
                                is_err = is_err or bool(tr.get("is_error"))
                            rec = {"agent":"cc","session":session,"i":i,
                                   "ts": ts.isoformat() if ts else None,"gap_s":gap,
                                   "role":"tool_result","kind":"tool_output",
                                   "tool":tool_name,
                                   "text_len":len(out_txt),
                                   "preview":out_txt[:4000],
                                   "is_error":is_err,"error_tags":tags,
                                   "activity":None}
                            w.write(json.dumps(rec) + "\n"); i += 1
                    if texts:
                        txt = "\n".join(c.get("text","") for c in texts)
                        rec = {"agent":"cc","session":session,"i":i,
                               "ts": ts.isoformat() if ts else None,"gap_s":gap,
                               "role":"user","kind":"prompt",
                               "text_len":len(txt),"preview":txt[:4000],
                               "activity":classify_user_text(txt)}
                        w.write(json.dumps(rec) + "\n"); i += 1
            elif t == "assistant":
                content = msg.get("content") or []
                for c in content:
                    if not isinstance(c, dict):
                        continue
                    if c.get("type") == "text":
                        txt = c.get("text","")
                        rec = {"agent":"cc","session":session,"i":i,
                               "ts": ts.isoformat() if ts else None,"gap_s":gap,
                               "role":"assistant","kind":"text",
                               "text_len":len(txt),"preview":txt[:4000],
                               "activity":None}
                        w.write(json.dumps(rec) + "\n"); i += 1
                    elif c.get("type") == "tool_use":
                        tn = c.get("name","")
                        inp = c.get("input") or {}
                        act = classify_assistant_tool(tn, inp)
                        preview = json.dumps(inp, default=str)[:2000]
                        tuid = c.get("id")
                        if tuid:
                            tool_id_to_name[tuid] = tn
                        rec = {"agent":"cc","session":session,"i":i,
                               "ts": ts.isoformat() if ts else None,"gap_s":gap,
                               "role":"assistant","kind":"tool_use",
                               "tool":tn,"activity":act,
                               "text_len":len(preview),"preview":preview}
                        w.write(json.dumps(rec) + "\n"); i += 1
                    elif c.get("type") == "thinking":
                        txt = c.get("thinking","")
                        rec = {"agent":"cc","session":session,"i":i,
                               "ts": ts.isoformat() if ts else None,"gap_s":gap,
                               "role":"assistant","kind":"reasoning",
                               "text_len":len(txt),"activity":None,
                               "preview":txt[:2000]}
                        w.write(json.dumps(rec) + "\n"); i += 1
            if ts:
                prev = ts
    return i


# --- Codex session ----------------------------------------------------------

def analyze_codex(path, out):
    session = None
    prev = None
    i = 0
    with open(path, "r", encoding="utf-8", errors="replace") as f, open(out, "w") as w:
        call_args = {}  # call_id -> {"name":..., "args":...}
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            ts = parse_iso(d.get("timestamp"))
            gap = int((ts - prev).total_seconds()) if (ts and prev) else 0
            t = d.get("type")
            p = d.get("payload") or {}
            if t == "session_meta":
                session = p.get("id") or session
            elif t == "response_item":
                rt = p.get("type")
                if rt == "message":
                    role = p.get("role","?")
                    content = p.get("content") or []
                    if isinstance(content, list):
                        txt = "".join(c.get("text","") for c in content if isinstance(c,dict))
                    else:
                        txt = str(content)
                    rec = {"agent":"codex","session":session,"i":i,
                           "ts": ts.isoformat() if ts else None,"gap_s":gap,
                           "role":role,"kind":"prompt" if role=="user" else "text",
                           "text_len":len(txt),"preview":txt[:4000],
                           "activity": classify_user_text(txt) if role=="user" else None}
                    w.write(json.dumps(rec) + "\n"); i += 1
                elif rt in ("function_call","custom_tool_call"):
                    name = p.get("name","")
                    args_raw = p.get("arguments","")
                    try:
                        args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
                    except Exception:
                        args = {}
                    cid = p.get("call_id")
                    if cid:
                        call_args[cid] = {"name":name,"args":args}
                    act = classify_assistant_tool(name, args if isinstance(args, dict) else {})
                    preview = (args_raw if isinstance(args_raw, str) else json.dumps(args, default=str))[:2000]
                    rec = {"agent":"codex","session":session,"i":i,
                           "ts": ts.isoformat() if ts else None,"gap_s":gap,
                           "role":"assistant","kind":"tool_use","tool":name,
                           "activity":act,"text_len":len(preview),"preview":preview}
                    w.write(json.dumps(rec) + "\n"); i += 1
                elif rt in ("function_call_output","custom_tool_call_output"):
                    cid = p.get("call_id")
                    out_obj = p.get("output")
                    if isinstance(out_obj, dict):
                        out_txt = out_obj.get("output") or out_obj.get("content") or ""
                    elif isinstance(out_obj, str):
                        try:
                            o = json.loads(out_obj)
                            out_txt = o.get("output") if isinstance(o, dict) else out_obj
                            if not isinstance(out_txt, str): out_txt = json.dumps(out_txt)
                        except Exception:
                            out_txt = out_obj
                    else:
                        out_txt = ""
                    out_txt = str(out_txt or "")
                    tags, is_err = detect_errors(out_txt)
                    tool = (call_args.get(cid) or {}).get("name","")
                    rec = {"agent":"codex","session":session,"i":i,
                           "ts": ts.isoformat() if ts else None,"gap_s":gap,
                           "role":"tool_result","kind":"tool_output","tool":tool,
                           "text_len":len(out_txt),
                           "preview":out_txt[:4000],
                           "is_error":is_err,"error_tags":tags,
                           "activity":None}
                    w.write(json.dumps(rec) + "\n"); i += 1
                elif rt == "reasoning":
                    # summary field contains bullets
                    summary = p.get("summary") or []
                    if isinstance(summary, list):
                        txt = "\n".join(s.get("text","") for s in summary if isinstance(s,dict))
                    else:
                        txt = str(summary)
                    rec = {"agent":"codex","session":session,"i":i,
                           "ts": ts.isoformat() if ts else None,"gap_s":gap,
                           "role":"assistant","kind":"reasoning",
                           "text_len":len(txt),"preview":txt[:2000],
                           "activity":None}
                    w.write(json.dumps(rec) + "\n"); i += 1
            if ts:
                prev = ts
    return i


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions-json", required=True,
                    help="output/sessions_all.json from parse_sessions.py")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    with open(args.sessions_json) as f:
        sessions = json.load(f)

    for s in sessions:
        path = s.get("file")
        if not path or not os.path.exists(path):
            continue
        sid = s.get("session_id") or os.path.basename(path).replace(".jsonl","")
        project = s.get("project_dir") or "unknown"
        # Resolve project_dir from Claude Code encoded name to real dirname
        if project.startswith("-Users-mathieuacher-SANDBOX-"):
            project = project[len("-Users-mathieuacher-SANDBOX-"):]
        elif s.get("project_cwd"):
            project = os.path.basename(s["project_cwd"])
        outp = os.path.join(args.out_dir, f"{project}__{s['agent']}__{sid}.jsonl")
        if os.path.exists(outp) and os.path.getsize(outp) > 0:
            continue  # idempotent
        if s["agent"] == "Claude Code":
            n = analyze_claude_code(path, outp)
        else:
            n = analyze_codex(path, outp)
        print(f"[{s['agent'][:5]}] {project} {sid}  → {n} events", file=sys.stderr)


if __name__ == "__main__":
    main()
