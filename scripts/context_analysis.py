#!/usr/bin/env python3
"""Per-session context-length trajectory + compaction detection.

For every session on disk we extract the turn-level "context consumed"
series (input_tokens + cache_read_tokens at each assistant / Codex turn)
and any explicit compaction events.

Both platforms expose compaction:

  - Claude Code: user messages carry `isCompactSummary: true` when the
    agent has condensed prior turns into a summary and restarted the
    conversation from it.

  - Codex CLI: emits `event_msg.type == "context_compacted"` (plus in some
    versions `thread_rolled_back`).

Outputs
-------
  output/context/<project>__<agent>__<session>.json — full per-turn series
  output/context/context_summary.csv                 — one row per session
  output/context_analysis.md                         — summary tables
                                                       embedded into REPORT.md

The per-turn JSON lets us plot later (sparklines / ribbon plots); the CSV
and MD give an at-a-glance picture of how close sessions got to the model's
context window.
"""
import argparse, csv, json, os, sys
from collections import defaultdict
from datetime import datetime

MODEL_CONTEXT = {
    # best-effort map of model → context window tokens
    "claude-opus-4-6":     1_000_000,  # 1M context variant
    "claude-opus-4-1":     200_000,
    "claude-opus-4":       200_000,
    "claude-sonnet-4-5":   200_000,
    "claude-sonnet-4":     200_000,
    "claude-sonnet-4-6":   1_000_000,
    "claude-haiku-4-5":    200_000,
    "gpt-5":               258_400,
    "gpt-5.4":             258_400,
    "gpt-5.3-codex":       258_400,
    "gpt-5.2":             258_400,
    "gpt-5.1":             258_400,
    "gpt-4o":              128_000,
    "o3":                  200_000,
    "o4-mini":             200_000,
}


def context_window_for(model):
    if not model: return None
    m = model.lower()
    if m in MODEL_CONTEXT: return MODEL_CONTEXT[m]
    # strip suffixes
    import re
    m2 = re.sub(r"\[.*?\]", "", m)
    if m2 in MODEL_CONTEXT: return MODEL_CONTEXT[m2]
    # fuzzy
    for k, v in MODEL_CONTEXT.items():
        if k in m: return v
    return None


def parse_iso(s):
    if not s: return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def analyse_claude_code(path, model_hint=None):
    """Return (series, compactions, model) where series is a list of dicts:
    [{ts, input_tokens, cache_read, context, kind}, …]
    `context` is input_tokens + cache_read_tokens — the actual amount of
    context processed at that turn.
    """
    series = []
    compactions = []
    model = model_hint
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get("type")
            ts = d.get("timestamp")
            msg = d.get("message") if isinstance(d.get("message"), dict) else None
            if t == "user" and d.get("isCompactSummary"):
                compactions.append({"ts": ts, "source": "isCompactSummary"})
                continue
            if t == "assistant" and msg:
                if not model and msg.get("model"):
                    model = msg["model"]
                usage = msg.get("usage") or {}
                inp = usage.get("input_tokens", 0) or 0
                cache_r = usage.get("cache_read_input_tokens", 0) or 0
                cache_c = usage.get("cache_creation_input_tokens", 0) or 0
                total_ctx = inp + cache_r + cache_c
                if total_ctx > 0:
                    series.append({
                        "ts": ts,
                        "input": inp,
                        "cache_read": cache_r,
                        "cache_create": cache_c,
                        "context": total_ctx,
                        "output": usage.get("output_tokens", 0) or 0,
                    })
    return series, compactions, model


def analyse_codex(path, model_hint=None):
    series = []
    compactions = []
    model = model_hint
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get("type")
            p = d.get("payload") or {}
            ts = d.get("timestamp")
            if t == "turn_context":
                if not model and p.get("model"):
                    model = p["model"]
            elif t == "event_msg":
                et = p.get("type")
                if et == "context_compacted":
                    compactions.append({"ts": ts, "source": "context_compacted"})
                elif et == "thread_rolled_back":
                    compactions.append({"ts": ts, "source": "thread_rolled_back"})
                elif et == "token_count":
                    info = p.get("info") or {}
                    ltu = info.get("last_token_usage") or {}
                    inp = ltu.get("input_tokens", 0) or 0
                    cache_r = ltu.get("cached_input_tokens", 0) or 0
                    out = ltu.get("output_tokens", 0) or 0
                    reason = ltu.get("reasoning_output_tokens", 0) or 0
                    total_ctx = inp  # Codex's input already = total input including cached
                    # Codex reports input_tokens INCLUDING cached. Keep as-is.
                    if total_ctx > 0:
                        series.append({
                            "ts": ts,
                            "input": inp - cache_r,
                            "cache_read": cache_r,
                            "cache_create": 0,
                            "context": total_ctx,
                            "output": out,
                            "reasoning": reason,
                        })
    return series, compactions, model


def percentiles(values, pcts=(0.5, 0.9, 0.99, 1.0)):
    if not values: return {f"p{int(p*100)}": 0 for p in pcts}
    s = sorted(values)
    out = {}
    for p in pcts:
        i = min(len(s)-1, int(p * (len(s)-1)))
        out[f"p{int(p*100)}"] = s[i]
    return out


def summarize(series, compactions, model):
    ctxs = [r["context"] for r in series]
    window = context_window_for(model) or 0
    peak = max(ctxs) if ctxs else 0
    util_pct = (100.0 * peak / window) if window else None
    return {
        "model": model or "?",
        "context_window": window,
        "turns_with_usage": len(series),
        "peak_context": peak,
        "peak_utilization_pct": round(util_pct, 1) if util_pct is not None else None,
        "median_context": percentiles(ctxs, (0.5,))["p50"],
        "p90_context": percentiles(ctxs, (0.9,))["p90"],
        "p99_context": percentiles(ctxs, (0.99,))["p99"],
        "first_context": ctxs[0] if ctxs else 0,
        "last_context": ctxs[-1] if ctxs else 0,
        "compactions": len(compactions),
        "compaction_events": compactions,
    }


def fmt_int(n):
    if n is None: return "—"
    return f"{int(n):,}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions-json", required=True)
    ap.add_argument("--out-series-dir", required=True)
    ap.add_argument("--out-csv", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--projects", nargs="+", required=True)
    args = ap.parse_args()
    os.makedirs(args.out_series_dir, exist_ok=True)

    with open(args.sessions_json) as f:
        sessions_all = json.load(f)

    rows = []  # for CSV + MD
    proj_summary = defaultdict(lambda: {
        "sessions": 0, "peak_context": 0, "peak_model": "?",
        "total_compactions": 0, "worst_utilization": 0.0,
        "any_above_90pct": 0,
    })

    for s in sessions_all:
        path = s.get("file")
        if not path or not os.path.exists(path):
            continue
        pd = s.get("project_dir","")
        if pd.startswith("-Users-mathieuacher-SANDBOX-"):
            pd = pd[len("-Users-mathieuacher-SANDBOX-"):]
        cwd = s.get("project_cwd") or ""
        project = pd if pd in args.projects else os.path.basename(cwd)
        if project not in args.projects:
            continue
        agent = s.get("agent","?")
        sid = s.get("session_id") or os.path.basename(path).replace(".jsonl","")
        model_hint = s.get("model")
        if agent == "Claude Code":
            series, compactions, model = analyse_claude_code(path, model_hint)
        elif agent == "Codex":
            series, compactions, model = analyse_codex(path, model_hint)
        else:
            continue
        summ = summarize(series, compactions, model)
        out_path = os.path.join(args.out_series_dir, f"{project}__{agent}__{sid}.json")
        with open(out_path, "w") as f:
            json.dump({"project": project, "agent": agent, "session_id": sid,
                       "model": model, "file": path,
                       "summary": summ, "series": series}, f, indent=2, default=str)

        # row
        rows.append({
            "project": project, "agent": agent, "session_id": sid,
            "model": model or "?",
            "turns": summ["turns_with_usage"],
            "context_window": summ["context_window"],
            "peak_context": summ["peak_context"],
            "peak_util_pct": summ["peak_utilization_pct"],
            "median_context": summ["median_context"],
            "p90_context": summ["p90_context"],
            "p99_context": summ["p99_context"],
            "first_context": summ["first_context"],
            "last_context": summ["last_context"],
            "compactions": summ["compactions"],
        })

        # project roll-up
        ps = proj_summary[project]
        ps["sessions"] += 1
        if summ["peak_context"] > ps["peak_context"]:
            ps["peak_context"] = summ["peak_context"]
            ps["peak_model"] = model or "?"
            ps["peak_window"] = summ["context_window"]
        ps["total_compactions"] += summ["compactions"]
        if summ.get("peak_utilization_pct") and summ["peak_utilization_pct"] > ps["worst_utilization"]:
            ps["worst_utilization"] = summ["peak_utilization_pct"]
        if summ.get("peak_utilization_pct") and summ["peak_utilization_pct"] >= 90:
            ps["any_above_90pct"] += 1

    # Write CSV
    fieldnames = ["project","agent","session_id","model","turns","context_window",
                  "peak_context","peak_util_pct","median_context","p90_context",
                  "p99_context","first_context","last_context","compactions"]
    with open(args.out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader()
        for r in sorted(rows, key=lambda x: (x["project"], x["agent"], x["session_id"])):
            w.writerow(r)
    print(f"[ok] {args.out_csv} ({len(rows)} sessions)", file=sys.stderr)

    # Write MD
    L = []; E = L.append
    E("## Context-length trajectory + compaction")
    E("")
    E("Per-turn context size = `input_tokens + cache_read + cache_create` for "
      "Claude Code, and `input_tokens` (which already includes cached) for Codex. "
      "This is the amount of tokens the model actually ingests to produce one "
      "response — i.e. how much of the context window is being used right now.")
    E("")
    E("**Compaction** is detected from explicit agent events: Claude Code flags a "
      "user message with `isCompactSummary: true` when it replaces the prior "
      "history with a condensed summary; Codex emits `event_msg.type == "
      "\"context_compacted\"` (and occasionally `thread_rolled_back`). A "
      "compaction is a reliable indicator that the session was running close to "
      "— or over — the model's context window.")
    E("")

    # Per-project roll-up
    E("### A. Per-project roll-up")
    E("")
    E("| Project | Sessions | Peak context | Model | Peak window | Peak util. % | Compactions | Sessions ≥ 90 % of window |")
    E("|---|---:|---:|---|---:|---:|---:|---:|")
    for proj in sorted(proj_summary, key=lambda p: -proj_summary[p]["peak_context"]):
        ps = proj_summary[proj]
        util = f"{ps['worst_utilization']:.1f}%" if ps["worst_utilization"] else "—"
        window = ps.get("peak_window") or "—"
        E(f"| `{proj}` | {ps['sessions']} | {fmt_int(ps['peak_context'])} | "
          f"`{ps['peak_model']}` | {fmt_int(window) if window != '—' else '—'} | "
          f"{util} | {ps['total_compactions']} | {ps['any_above_90pct']} |")
    E("")

    # Per-session detail
    E("### B. Per-session detail")
    E("")
    E("Columns: turn count (assistant turns with usage info), context-window size, "
      "peak context reached (and % of window it is), median / p90 / p99 of the "
      "context-length distribution, first-turn & last-turn context (to see the "
      "growth pattern), and count of compaction events in that session.")
    E("")
    E("| Project | Agent | Model | Turns | Window | Peak | % | p50 | p90 | p99 | First | Last | Compactions |")
    E("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in sorted(rows, key=lambda x: (x["project"], x["agent"], x["session_id"])):
        util = f"{r['peak_util_pct']:.0f}%" if r["peak_util_pct"] is not None else "—"
        compmark = f"**{r['compactions']}**" if r["compactions"] else "0"
        E(f"| `{r['project']}` | {r['agent']} | `{r['model']}` | "
          f"{r['turns']} | {fmt_int(r['context_window'])} | {fmt_int(r['peak_context'])} | "
          f"{util} | {fmt_int(r['median_context'])} | {fmt_int(r['p90_context'])} | "
          f"{fmt_int(r['p99_context'])} | {fmt_int(r['first_context'])} | "
          f"{fmt_int(r['last_context'])} | {compmark} |")
    E("")

    # Caveats + what to read for
    E("### C. How to read this")
    E("")
    E("- **Sessions with compactions > 0** are sessions where the agent hit a soft "
      "ceiling and had to fold prior history into a summary — expect loss of "
      "fine-grained trace fidelity downstream of that point.")
    E("- **Peak / window ≥ 80 %** means the session ran close to the model's limit. "
      "Even without a compaction event, the agent's cache effectiveness drops "
      "here (more churn on cache_read tokens).")
    E("- For Claude Code, the 1 M-context Opus variant (`claude-opus-4-6 [1M]`) "
      "raises the ceiling 5× over the 200 k baseline — this is why the compiler / "
      "chess sessions can run for 15+ active hours without mandatory compaction.")
    E("- Codex's 258 400-token context window on `gpt-5.*` is smaller than Claude's "
      "Opus 1 M — you will see Codex hit compaction sooner on projects of "
      "comparable feature depth.")
    E("- Raw per-session per-turn series are saved to "
      f"[`output/context/*.json`]({args.out_series_dir}), suitable for sparkline / "
      "ribbon-plot rendering; the summary CSV is at "
      f"[`output/context_summary.csv`]({args.out_csv}).")
    E("")

    with open(args.out_md, "w") as f:
        f.write("\n".join(L) + "\n")
    print(f"[ok] {args.out_md}", file=sys.stderr)


if __name__ == "__main__":
    main()
