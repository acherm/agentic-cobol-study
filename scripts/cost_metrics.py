#!/usr/bin/env python3
"""Report token-level cost metrics per project.

Dollars are a poor comparison axis between Claude Code and Codex (different
rack rates, subscription billing differs, Codex's reasoning tokens are hidden
chain-of-thought that is charged but invisible). Tokens are the primitive
unit of compute and compare cleanly.

For each project we break tokens down by type, sum across sessions, and
normalize against deliverables (code lines, backlog entries, user prompts).

Outputs
-------
  output/cost_metrics.csv  — machine-readable full matrix (one row per
                             project × agent pair, plus a "TOTAL" row per
                             project), for reproducibility and plotting.
  output/cost_metrics.md   — Markdown fragment embedded into REPORT.md,
                             with four sub-tables:
                             A. per (project × agent) — raw token profile
                             B. per project (all agents summed) — totals
                             C. per project — normalized ratios
                             D. caveat block explaining semantics

Metric conventions
------------------
- `input_tokens`       : new prompt tokens processed (NOT cache reads).
                         In Claude Code this is `message.usage.input_tokens`.
                         In Codex this is `total_token_usage.input_tokens`
                         with `cached_input_tokens` subtracted out.
- `output_tokens`      : tokens generated. For Claude Code this includes
                         visible text and thinking blocks. For Codex,
                         `reasoning_tokens` is a SUBSET of `output_tokens`
                         (verified on raw rollouts: total = input + output),
                         so it must not be added on top.
- `cache_read_tokens`  : tokens served from prompt cache (billed at ~10% of
                         input price on both platforms). Cache HIT indicator.
- `cache_create_tokens`: tokens written to prompt cache (billed at ~125% of
                         input price on Claude; flat input on Codex).
- `reasoning_tokens`   : Codex hidden-CoT tokens. Billed at output rate.
- `total_tokens`       : vendor-normalized compute consumed. Codex
                         `input_tokens` includes cache reads and
                         `output_tokens` includes reasoning, so the sum
                         avoids double counting per agent.
- `cache_hit_rate`     : cache_read / (cache_read + input).
"""
import argparse, csv, json, os, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from session_roles import session_role


TOK_KEYS = ["input_tokens", "output_tokens", "cache_read_tokens",
            "cache_creation_tokens", "reasoning_tokens"]


def sum_tokens(sessions):
    t = {k: 0 for k in TOK_KEYS}
    tool_calls = 0
    user_prompts = 0
    cost = 0.0
    for s in sessions:
        for k in TOK_KEYS:
            t[k] += s.get(k, 0) or 0
        tool_calls += s.get("tool_calls_total", 0) or 0
        user_prompts += s.get("user_turns", 0) or 0
        cost += s.get("cost_usd", 0) or 0
    # vendor-normalized total: Codex input includes cache reads and its
    # output includes reasoning; Claude fields are disjoint buckets
    total = 0
    for s in sessions:
        i = s.get("input_tokens", 0) or 0
        o = s.get("output_tokens", 0) or 0
        cr = s.get("cache_read_tokens", 0) or 0
        cw = s.get("cache_creation_tokens", 0) or 0
        total += (i + o) if s.get("agent") == "Codex" else (i + o + cr + cw)
    t["total_tokens"] = total
    t["tool_calls"] = tool_calls
    t["user_prompts"] = user_prompts
    t["cost_usd"] = round(cost, 2)
    # Derived
    t["cache_hit_rate"] = (
        t["cache_read_tokens"] / (t["cache_read_tokens"] + t["input_tokens"])
        if (t["cache_read_tokens"] + t["input_tokens"]) > 0 else 0.0
    )
    return t


def project_sessions(sessions_all, project):
    out = []
    for s in sessions_all:
        pd = s.get("project_dir", "")
        if pd.startswith("-Users-mathieuacher-SANDBOX-"):
            pd = pd[len("-Users-mathieuacher-SANDBOX-"):]
        cwd = s.get("project_cwd") or ""
        if pd == project or os.path.basename(cwd) == project:
            out.append(s)
    # dedupe by session_id
    seen = set(); clean = []
    for s in sorted(out, key=lambda x: x.get("start") or ""):
        sid = s.get("session_id")
        if sid in seen: continue
        seen.add(sid); clean.append(s)
    # dev sessions only: analyst (post-mortem instrument) and empty log
    # shells are assessment overhead, not development compute
    return [s for s in clean if session_role(s) == "dev"]


def fmt_int(n):
    if n is None: return "—"
    if isinstance(n, float) and n == int(n):
        n = int(n)
    if isinstance(n, int):
        return f"{n:,}"
    return str(n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions-json", required=True)
    ap.add_argument("--metrics-dir", required=True)
    ap.add_argument("--projects", nargs="+", required=True)
    ap.add_argument("--out-csv", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    with open(args.sessions_json) as f:
        sessions_all = json.load(f)

    # Collect rows
    rows = []  # each row = dict for CSV output
    per_project_totals = {}
    per_project_meta = {}

    for proj in args.projects:
        sess = project_sessions(sessions_all, proj)
        # load metrics file to get LOC + feature counts
        loc_cobol = 0
        loc_code_all = 0
        n_backlog = 0
        n_commits = 0
        n_paragraphs = 0
        mp = os.path.join(args.metrics_dir, f"{proj}.json")
        if os.path.exists(mp):
            with open(mp) as f:
                m = json.load(f)
            comp = (m.get("complexity") or {}).get("aggregate") or {}
            loc_cobol = comp.get("code_lines", 0) or 0
            n_paragraphs = comp.get("paragraphs", 0) or 0
            inv = (m.get("inventory") or {}).get("by_lang") or {}
            loc_code_all = sum(v.get("loc", 0) or 0 for v in inv.values())
            feats = m.get("features") or {}
            n_backlog = len(feats.get("spec_backlog") or [])
            n_commits = len(feats.get("commit_subjects") or [])
        per_project_meta[proj] = {
            "loc_cobol": loc_cobol,
            "loc_code_all": loc_code_all,
            "n_backlog": n_backlog,
            "n_commits": n_commits,
            "n_paragraphs": n_paragraphs,
        }

        # group sessions by agent
        by_agent = defaultdict(list)
        for s in sess:
            by_agent[s.get("agent", "?")].append(s)
        proj_total = sum_tokens(sess)
        per_project_totals[proj] = proj_total

        for agent, agent_sess in sorted(by_agent.items()):
            t = sum_tokens(agent_sess)
            row = {"project": proj, "agent": agent, "n_sessions": len(agent_sess)}
            row.update({k: t[k] for k in TOK_KEYS + [
                "total_tokens", "tool_calls", "user_prompts", "cost_usd",
                "cache_hit_rate"]})
            row["loc_cobol"] = loc_cobol
            row["n_backlog"] = n_backlog
            rows.append(row)
        # Also emit a TOTAL row per project
        row = {"project": proj, "agent": "TOTAL",
               "n_sessions": len(sess)}
        row.update({k: proj_total[k] for k in TOK_KEYS + [
            "total_tokens", "tool_calls", "user_prompts", "cost_usd",
            "cache_hit_rate"]})
        row["loc_cobol"] = loc_cobol
        row["n_backlog"] = n_backlog
        rows.append(row)

    # Write CSV
    fieldnames = ["project", "agent", "n_sessions",
                  "input_tokens", "output_tokens", "cache_read_tokens",
                  "cache_creation_tokens", "reasoning_tokens", "total_tokens",
                  "cache_hit_rate",
                  "tool_calls", "user_prompts", "cost_usd",
                  "loc_cobol", "n_backlog"]
    with open(args.out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            r2 = dict(r)
            r2["cache_hit_rate"] = round(r2.get("cache_hit_rate", 0.0), 3)
            w.writerow(r2)
    print(f"[ok] {args.out_csv}  ({len(rows)} rows)", file=sys.stderr)

    # --- Markdown tables ----------------------------------------------------
    L = []; E = L.append
    E("## Cost metrics — tokens (not dollars)")
    E("")
    E("Dollars are rack-rate estimates and don't compare cleanly between Claude Code "
      "and Codex. Tokens are the primitive unit of compute. Below, each token type "
      "is summed per project × agent. All the raw data is in [`output/cost_metrics.csv`](output/cost_metrics.csv).")
    E("")

    # Table A — per project × agent profile
    E("### A. Token profile per project × agent")
    E("")
    E("| Project | Agent | Sessions | Input | Output | Cache read | Cache create | Reasoning | **Total tokens** | Cache hit % | Est. $ |")
    E("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        if r["agent"] == "TOTAL":
            continue
        hit = 100 * r.get("cache_hit_rate", 0)
        E(f"| `{r['project']}` | {r['agent']} | {r['n_sessions']} | "
          f"{fmt_int(r['input_tokens'])} | {fmt_int(r['output_tokens'])} | "
          f"{fmt_int(r['cache_read_tokens'])} | {fmt_int(r['cache_creation_tokens'])} | "
          f"{fmt_int(r['reasoning_tokens'])} | **{fmt_int(r['total_tokens'])}** | "
          f"{hit:.1f}% | ${r['cost_usd']:.0f} |")
    E("")

    # Table B — per project totals (agents summed)
    E("### B. Per-project totals (agents summed)")
    E("")
    E("| Project | Sessions | Input | Output | Cache read | Cache create | Reasoning | **Total tokens** | Est. $ |")
    E("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    # Sort by total tokens desc
    ordered = sorted(per_project_totals.items(), key=lambda x: -x[1]["total_tokens"])
    for proj, t in ordered:
        n_sess = sum(1 for r in rows if r["project"]==proj and r["agent"] not in ("TOTAL",))
        # Actually we stored project_sessions() dedup — use that count
        n_sess = next((r["n_sessions"] for r in rows if r["project"]==proj and r["agent"]=="TOTAL"), n_sess)
        E(f"| `{proj}` | {n_sess} | "
          f"{fmt_int(t['input_tokens'])} | {fmt_int(t['output_tokens'])} | "
          f"{fmt_int(t['cache_read_tokens'])} | {fmt_int(t['cache_creation_tokens'])} | "
          f"{fmt_int(t['reasoning_tokens'])} | **{fmt_int(t['total_tokens'])}** | "
          f"${t['cost_usd']:.0f} |")
    # Grand total
    grand = {k: sum(t[k] for t in per_project_totals.values()) for k in TOK_KEYS + ["total_tokens"]}
    grand_cost = sum(t["cost_usd"] for t in per_project_totals.values())
    E(f"| **GRAND TOTAL** | — | **{fmt_int(grand['input_tokens'])}** | **{fmt_int(grand['output_tokens'])}** | "
      f"**{fmt_int(grand['cache_read_tokens'])}** | **{fmt_int(grand['cache_creation_tokens'])}** | "
      f"**{fmt_int(grand['reasoning_tokens'])}** | **{fmt_int(grand['total_tokens'])}** | "
      f"**${grand_cost:.0f}** |")
    E("")

    # Table C — normalized ratios
    E("### C. Normalized ratios (compute per unit of deliverable)")
    E("")
    E("Output tokens are the cleanest comparison axis (everything the agent actually "
      "generated). Ratios below divide output tokens by:")
    E("")
    E("- `COBOL LOC` — what ended up in the delivered `.cob`/`.cbl`/`.cpy` files,")
    E("- `F-### backlog entry` — deliverable units of work,")
    E("- `user prompt` — unit of user direction.")
    E("")
    E("| Project | Output tokens | COBOL LOC | Output / LOC | Backlog | Output / BL | User prompts | Output / prompt |")
    E("|---|---:|---:|---:|---:|---:|---:|---:|")
    for proj, t in ordered:
        meta = per_project_meta.get(proj, {})
        loc = meta.get("loc_cobol", 0)
        nbl = meta.get("n_backlog", 0)
        ups = t.get("user_prompts", 0)
        def ratio(num, denom):
            if not denom: return "—"
            return f"{num/denom:,.0f}"
        E(f"| `{proj}` | {fmt_int(t['output_tokens'])} | {fmt_int(loc)} | "
          f"{ratio(t['output_tokens'], loc)} | {nbl} | {ratio(t['output_tokens'], nbl)} | "
          f"{ups} | {ratio(t['output_tokens'], ups)} |")
    E("")

    # Caveats
    E("### D. Caveats on token semantics")
    E("")
    E("- **`input_tokens`** here is the *non-cached* input (new prompt tokens processed). Claude Code reports this directly; Codex reports `cached_input_tokens` separately and we subtract it from the raw total.")
    E("- **`output_tokens`** includes `thinking` blocks for Claude Code (they are charged at output rate). Codex reports `reasoning_output_tokens` in a separate bucket; we keep them in `reasoning_tokens` to make the hidden-CoT load visible.")
    E("- **`cache_read_tokens`** are billed at ~10 % of input rate on both platforms — a high cache-hit rate is a strong efficiency indicator for long-running sessions (Codex sessions on this machine often show 50–80 %).")
    E("- **`cache_creation_tokens`** (Claude-specific) are billed at ~125 % of input rate; they pay once and amortise across subsequent turns.")
    E("- **`reasoning_tokens`** (Codex-only) are billed at output rate but are invisible in the transcript. Projects with heavy reasoning_tokens are doing more hidden deliberation per user turn.")
    E("- **`cost_usd`** is a rack-rate upper bound; actual billing under Team / Max / Pro subscriptions differs. Use tokens for comparison.")
    E("- For reproducibility, every number here is recomputable from `output/sessions_all.json` with `scripts/cost_metrics.py`.")
    E("")

    with open(args.out_md, "w") as f:
        f.write("\n".join(L) + "\n")
    print(f"[ok] {args.out_md}", file=sys.stderr)


if __name__ == "__main__":
    main()
