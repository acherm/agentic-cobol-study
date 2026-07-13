#!/usr/bin/env python3
"""Generate a Markdown meta-report from projects.json."""
import json, os, sys, argparse
from collections import Counter, defaultdict

# Project descriptions (domain of interest) — filled in by hand + file inspection
DOMAIN_NOTES = {
    "chess-cobol-cc": "Chess engine in COBOL (GnuCOBOL); engine playability + ELO measurement via cutechess.",
    "COBOL-chess":    "Chess engine in COBOL (multi-session); architecture + specification backlog.",
    "cobol-compiler-cc":  "A COBOL compiler (and interpreter) written in COBOL. Translates COBOL to C; self-hosts non-trivial programs.",
    "cobol-compiler-codex": "Alternative COBOL-to-C 'minicobc' compiler, driven by Codex. Benchmarks vs. GnuCOBOL.",
    "cobol-compress-codex": "COBPACK — columnar packer / compressor for fixed-record COBOL data, implemented in pure COBOL (Codex-built).",
    "cobol-compress-cobolcc": "COBPACK — columnar compressor (Claude-Code-built) — second-agent replica of the COBPACK domain.",
    "cobol-doom-cc": "Doom-like FPS in COBOL (Claude Code) — modular walker + ray-casting + enemies + levels.",
    "cobol-doom-codex": "Doom-like FPS in COBOL (Codex) — gridwalker + SDL2 bridge + 11 COPY books + BMP sprites.",
    "cobol-jb":   "Payroll management case-study system in GnuCOBOL (employee records → payslips + summary).",
    "COBOL-pygame": "A pygame-style framework in COBOL (GnuCOBOL), exposing a Python-pygame-like interface.",
    "SATCobol-codex": "SAT solver in COBOL (Codex) — modular COPY books + MiniSat/SAT4J cross-checks + uf/uuf benchmark families.",
    "SATCobol-cc":    "SAT solver in COBOL (Claude Code) — second-agent replica of the SAT domain.",
    "cobol-tictactoe": "Game-of-15 and tic-tac-toe variants in COBOL with minimax-style tree search (Claude Code).",
    "game15-cobol-codex": "Game of 15 in COBOL (Codex) — second-agent replica of the small-game domain.",
}

# Broad activity families (for the summary table)
ACTIVITIES = [
    "Implement feature", "Refactor", "Debug / Fix", "Test", "Document",
    "Optimize", "Port/Rewrite", "Research", "Build/Config", "Review/Audit",
]


def fmt_dur(s):
    if not s:
        return "-"
    s = int(s)
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    if d:
        return f"{d}d {h}h {m}m"
    if h:
        return f"{h}h {m}m"
    return f"{m}m {s}s"


def fmt_int(n):
    return f"{n:,}" if isinstance(n, int) else str(n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--projects", required=True)
    ap.add_argument("--metrics-dir", default=None,
                    help="optional output/metrics dir to enrich cross-project tables")
    ap.add_argument("--reports-dir", default="output/reports",
                    help="where per-project reports live (for linking)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    with open(args.projects) as f:
        data = json.load(f)

    metrics = {}
    if args.metrics_dir and os.path.isdir(args.metrics_dir):
        for proj in data.keys():
            mp = os.path.join(args.metrics_dir, f"{proj}.json")
            if os.path.exists(mp):
                with open(mp) as f:
                    metrics[proj] = json.load(f)
    difficulty = {}
    diff_path = os.path.join(os.path.dirname(args.metrics_dir or "output"), "difficulty.json") if args.metrics_dir else None
    if diff_path and os.path.exists(diff_path):
        with open(diff_path) as f:
            difficulty = json.load(f)

    lines = []
    E = lines.append
    E("# Meta-Analysis: COBOL Projects Built with Coding Agents")
    E("")
    E("**Scope.** All `~/SANDBOX/*cobol*` / `*COBOL*` project directories on this machine, cross-referenced with locally-stored coding-agent session logs (`~/.claude/projects/*.jsonl` for Claude Code, `~/.codex/sessions/**/*.jsonl` for Codex).")
    E("")
    E("**Generated.** 2026-04-15 (by automated scripts in `scripts/`, results in `output/`).")
    E("")
    E("## 1. Methodology")
    E("")
    E("- **Project discovery.** Listing of `~/SANDBOX/` filtered on `cobol` / `COBOL`.")
    E("- **Session discovery.** For Claude Code: one directory per project under `~/.claude/projects/`, each `.jsonl` is a session. For Codex: rollout files under `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*.jsonl`, matched on `session_meta.cwd`. For Cline: no on-disk JSONL trace was found in this environment — only artifacts.")
    E("- **Per-session metrics** (script: `scripts/parse_sessions.py`):")
    E("  - agent = `Claude Code` or `Codex`;")
    E("  - model from `message.model` (CC) or `turn_context.model` (Codex);")
    E("  - CLI version from `session_meta.cli_version` / Claude Code `version` field;")
    E("  - duration = wall-clock between first and last event (⚠ includes idle gaps across days when a session is resumed);")
    E("  - tool calls counted from `tool_use` blocks (CC) or `response_item.function_call` / `custom_tool_call` (Codex);")
    E("  - tokens from `message.usage` (CC) or `event_msg.token_count.info.total_token_usage` (Codex).")
    E("  - **cost is an upper-bound estimate** at public API rack rates — real spending under Team/Max subscriptions differs; rates table is inlined in `scripts/parse_sessions.py`.")
    E("- **LOC / inventory** (script: `scripts/analyze_projects.py`): walks each project, skipping `.git`, `build`, `external`, `node_modules`, `cutechess`; lines counted with Python `for _ in f`.")
    E("- **Activity classification.** Keyword matching on the first user prompt (see `ACTIVITY_KWS` in `scripts/analyze_projects.py`). This is a rough thematic proxy, not a full QA of every turn.")
    E("- **Deep per-turn analysis** (new): `scripts/deep_analyze.py` emits one JSONL per session under `output/turns/<project>__*.jsonl`, with one row per event (user prompt, assistant message, tool call, tool result). `scripts/project_metrics.py` turns those into per-project aggregates under `output/metrics/`; `scripts/generate_project_reports.py` renders a full RQ-labeled Markdown per project under `output/reports/`.")
    E("- **RQs** answered per-project are defined in [`RQ_FRAMEWORK.md`](RQ_FRAMEWORK.md). The full pipeline is one command: `scripts/run_all.sh`.")
    E("")

    # Global stats
    total_sessions = 0
    total_tools = 0
    total_cost = 0.0
    total_duration = 0
    total_user = 0
    agents = Counter()
    models = Counter()
    versions = defaultdict(set)
    cob_loc_total = 0
    cob_files_total = 0
    for proj, d in data.items():
        inv = d["inventory"]
        cob = inv["by_lang"].get("COBOL", {})
        cob_loc_total += cob.get("loc", 0)
        cob_files_total += cob.get("files", 0)
        for s in d["sessions"]:
            total_sessions += 1
            total_tools += s.get("tool_calls_total", 0)
            total_cost += s.get("cost_usd", 0) or 0
            total_duration += s.get("duration_s", 0) or 0
            total_user += s.get("user_turns", 0) or 0
            agents[s["agent"]] += 1
            if s.get("model"):
                models[s["model"]] += 1
            if s.get("version"):
                versions[s["agent"]].add(s["version"])

    E("## 2. Summary at a glance")
    E("")
    n_projects = len(data)
    n_with_sessions = len([p for p,d in data.items() if d['sessions']])
    E(f"- **{n_projects} COBOL project folders** analysed (two folders — `cobol-vibes`, `test-cline-COBOL` — excluded because no agent session is preserved on disk); **{n_with_sessions}** with on-disk agent traces.")
    E(f"- **{total_sessions} sessions** — {agents.get('Claude Code',0)} Claude Code + {agents.get('Codex',0)} Codex.")
    E(f"- **Coding agents used:** Claude Code (versions: {', '.join(sorted(versions['Claude Code']))}) and Codex CLI (versions: {', '.join(sorted(versions['Codex']))}). No preserved JSONL for Cline on this machine.")
    E(f"- **Models observed:** " + ", ".join(f"`{m}`×{n}" for m, n in models.most_common()) + ".")
    E(f"- **Tool calls (sum):** {fmt_int(total_tools)}.")
    E(f"- **User turns (sum):** {fmt_int(total_user)}.")
    E(f"- **Aggregate wall-clock duration (sum of per-session spans, includes idle gaps):** {fmt_dur(total_duration)}.")
    E(f"- **Estimated cost at API rack rates (upper bound, not subscription cost):** ~${total_cost:,.0f}.")
    E(f"- **COBOL code across all projects:** {fmt_int(cob_files_total)} files, {fmt_int(cob_loc_total)} LOC.")
    E("")

    # Date range
    starts = [s.get("start") for d in data.values() for s in d["sessions"] if s.get("start")]
    if starts:
        starts_sorted = sorted(starts)
        E(f"- **Activity period:** {starts_sorted[0][:10]} → {starts_sorted[-1][:10]}.")
    E("")

    E("## 3. Projects at a glance")
    E("")
    E("| Project | Domain | Agent(s) | Sessions | COBOL files / LOC | Tool calls | Dur (Σ wall) | Cost est. (USD) |")
    E("|---|---|---|---:|---:|---:|---:|---:|")
    for proj, d in data.items():
        inv = d["inventory"]
        cob = inv["by_lang"].get("COBOL", {})
        sess = d["sessions"]
        ag = Counter(s["agent"] for s in sess)
        ag_s = "+".join(f"{a[:2]}×{n}" for a, n in ag.items()) or "—"
        dur = sum(s.get("duration_s", 0) for s in sess)
        cost = sum(s.get("cost_usd", 0) for s in sess)
        tools = sum(s.get("tool_calls_total", 0) for s in sess)
        E(f"| `{proj}` | {DOMAIN_NOTES.get(proj,'—')[:90]} | {ag_s} | {len(sess)} | {cob.get('files',0)} / {fmt_int(cob.get('loc',0))} | {fmt_int(tools)} | {fmt_dur(dur)} | ${cost:,.0f} |")
    E("")
    E("Legend: `Cl×N` = Claude Code sessions; `Co×N` = Codex sessions.")
    E("")
    # Highlights pointer (hand-curated, lives at output/highlights.md)
    if os.path.exists("output/highlights.md"):
        E("### Highlights — impressive technical moments across the corpus")
        E("")
        E("Hand-curated reading of the 27 sessions, focused on specific engineering moments "
          "(debugging feats, COBOL-specific idioms, verification discipline, performance "
          "iteration, architectural choices, cross-agent divergences). Every claim is "
          "anchored to a concrete artefact. See [`output/highlights.md`](output/highlights.md).")
        E("")
    # Domain coverage fragment (if pre-generated)
    cov_path = "output/domain_coverage.md"
    if os.path.exists(cov_path):
        with open(cov_path) as f:
            E(f.read().rstrip())
        E("")
    # Cost metrics fragment (if pre-generated)
    cost_path = "output/cost_metrics.md"
    if os.path.exists(cost_path):
        with open(cost_path) as f:
            E(f.read().rstrip())
        E("")
    # Context analysis fragment (if pre-generated)
    ctx_path = "output/context_analysis.md"
    if os.path.exists(ctx_path):
        with open(ctx_path) as f:
            E(f.read().rstrip())
        E("")
    # Feature classification roll-up
    kf_path = "output/key_features_summary.md"
    if os.path.exists(kf_path):
        with open(kf_path) as f:
            E(f.read().rstrip())
        E("")
    # Per-project report links
    if args.reports_dir:
        E("### Per-project artefacts")
        E("")
        E("Each row: narrative story, case study (RQ-labeled metrics), calibrated assessment (context + strengths + honest gaps), feature ledger (F-### / SB-### entries), key-features ranking, and reusable replay prompts for reproducing the project with a different agent.")
        E("")
        E("| Project | Story | Case study | Assessment | Backlog | Key features | Replay prompts |")
        E("|---|---|---|---|---|---|---|")
        base_abs_dir = os.path.dirname(os.path.abspath(args.out))
        for proj in data.keys():
            def _cell(rel, label):
                return f"[{label}]({rel})" if os.path.exists(os.path.join(base_abs_dir, rel)) else "—"
            E(f"| `{proj}` "
              f"| {_cell(f'output/backlogs/{proj}/STORY.md','story')} "
              f"| [report]({args.reports_dir}/{proj}.md) "
              f"| [assessment](output/assessments/{proj}.md) "
              f"| [backlog](output/backlogs/{proj}/SPECIFICATION_BACKLOG.md) "
              f"| {_cell(f'output/backlogs/{proj}/KEY_FEATURES.md','key')} "
              f"| {_cell(f'output/backlogs/{proj}/REPLAY_PROMPTS.md','replay')} |")
        E("")
    # Cross-project quantitative table from metrics
    if metrics:
        E("### Cross-project quantitative view (from deep analysis)")
        E("")
        E("| Project | Difficulty | Turns | Active time | bug_fix share | Error rate | User prompts | Avg prompt len |")
        E("|---|---|---:|---:|---:|---:|---:|---:|")
        def _pct(n,d):
            return f"{100*n/d:.1f}%" if d else "—"
        def _pct_f(x):
            return f"{100*x:.1f}%" if x else "—"
        # Sort by difficulty index (descending) for easier reading
        order = sorted(data.keys(), key=lambda p: -(difficulty.get(p,{}).get("index",0) or 0))
        for proj in order:
            m = metrics.get(proj)
            if not m:
                continue
            at = m.get("active_time") or {}
            tot = at.get("total_active_s") or 0
            by = at.get("by_se_task_s") or at.get("by_activity_s") or {}
            fix = by.get("bug_fix", 0)
            errs = m.get("errors") or {}
            up = m.get("user_prompts") or {}
            d = difficulty.get(proj, {})
            lab = d.get("label","—")
            idx = d.get("index")
            lab_s = f"{lab} ({idx:.2f})" if idx is not None else lab
            E(f"| `{proj}` | {lab_s} | {m.get('n_turns',0):,} | {fmt_dur(tot)} | {_pct(fix,tot)} | {_pct(errs.get('tool_output_errors',0), errs.get('tool_outputs',0))} | {up.get('count',0)} | {up.get('avg_len',0):.0f} |")
        E("")
        # COBOL mastery + feature count
        E("### COBOL language mastery (what programs exercise the language surface)")
        E("")
        E("Mastery score = number of distinct COBOL constructs observed in the project's `.cob`/`.cbl`/`.cpy` files. Categories = how many of the 10 capability categories the project touches (control flow, arithmetic, data-advanced, I/O, string-ops, tables/search, subprograms, copy/preproc, intrinsics, misc).")
        E("")
        E("| Project | Mastery | Categories | Paragraphs (≈functions) | Sections | LOC (code) | Notable constructs |")
        E("|---|---:|---:|---:|---:|---:|---|")
        for proj in order:
            m = metrics.get(proj) or {}
            comp = (m.get("complexity") or {}).get("aggregate") or {}
            caps = comp.get("capabilities") or {}
            # Notable
            notable_probe = [
                ("subprograms","CALL"),("subprograms","RECURSIVE"),
                ("data_advanced","OCCURS"),("data_advanced","REDEFINES"),
                ("data_advanced","USAGE_COMP_5"),("copy_preproc","COPY"),
                ("tables_search","SEARCH_ALL"),("io_file","FD"),
                ("string_ops","UNSTRING"),("intrinsics","FUNCTION"),
            ]
            nt = []
            for cat, name in notable_probe:
                v = (caps.get(cat,{}).get("constructs") or {}).get(name, 0)
                if v:
                    nt.append(f"`{name}`({v})")
            n_cats = comp.get("categories_exercised", 0)
            E(f"| `{proj}` | {comp.get('mastery_score',0)} | {n_cats}/10 | {comp.get('paragraphs',0)} | {comp.get('sections',0)} | {comp.get('code_lines',0):,} | " +
              (", ".join(nt[:6]) if nt else "—") + " |")
        E("")
        # Feature ledger summary
        E("### Feature inventory (what was actually built)")
        E("")
        E("A prompt often expands into many sub-features. The ledger tallies features from four sources; the `F-###` backlog is the authoritative one when present. `prompt subtasks` = bullet / numbered items found inside user messages. `commits` = git commit subjects. Total = deduplicated union (rough lower bound; see per-project reports for the full ledger).")
        E("")
        E("| Project | F-### backlog | README features | Prompt subtasks | Git commits | Total (dedup proxy) |")
        E("|---|---:|---:|---:|---:|---:|")
        for proj in order:
            m = metrics.get(proj) or {}
            feats = m.get("features") or {}
            E(f"| `{proj}` | **{len(feats.get('spec_backlog') or [])}** | {len(feats.get('readme_features') or [])} | {len(feats.get('prompt_subtasks') or [])} | {len(feats.get('commit_subjects') or [])} | {feats.get('total_features_proxy', 0)} |")
        E("")
        # Difficulty signals matrix
        E("### Difficulty signals (raw values)")
        E("")
        E("Each project's difficulty label is the quartile of its mean rank across seven signals. Raw values below; full derivation in `scripts/difficulty.py`.")
        E("")
        E("| Project | Active h | Span d | Prompts | Redirect/bug | Err rate | Fix cycles | Fix-time share |")
        E("|---|---:|---:|---:|---:|---:|---:|---:|")
        for proj in order:
            d = difficulty.get(proj, {})
            s = d.get("signals") or {}
            E(f"| `{proj}` | {s.get('active_hours','-')} | {s.get('span_days','-')} | {s.get('user_prompts','-')} | {s.get('redirect_bug_prompts','-')} | {_pct_f(s.get('error_rate',0))} | {s.get('fix_cycles','-')} | {_pct_f(s.get('fix_time_share',0))} |")
        E("")

    E("## 4. Per-project detail")
    E("")
    for proj, d in data.items():
        inv = d["inventory"]
        sess = d["sessions"]
        E(f"### `{proj}`")
        E("")
        E(f"**Domain.** {DOMAIN_NOTES.get(proj,'—')}")
        E("")
        by_lang = inv["by_lang"]
        langs = sorted(by_lang.items(), key=lambda x: -x[1]["loc"])
        E("**Inventory.** {} files, {:.1f} MB total.".format(inv["total_files"], inv["total_bytes"]/1e6))
        E("")
        if langs:
            E("| Language | Files | LOC |")
            E("|---|---:|---:|")
            for lang, v in langs:
                if v["loc"] == 0 and v["files"] == 0:
                    continue
                E(f"| {lang} | {v['files']} | {fmt_int(v['loc'])} |")
            E("")
        if not sess:
            E("_No agent sessions found on disk._ (The artefacts in the folder suggest agent-assisted authoring, but no matching `.jsonl` trace exists in `~/.claude/projects` or `~/.codex/sessions`.)")
            E("")
            continue
        E("**Sessions.**")
        E("")
        E("| # | Agent | Model | CLI ver | Start | Duration (wall) | User turns | Assist. turns | Tool calls | Top tools | Tokens in/out/cache | Cost est. |")
        E("|---:|---|---|---|---|---:|---:|---:|---:|---|---|---:|")
        for i, s in enumerate(sess, 1):
            tb = s.get("tool_breakdown", {})
            top = ", ".join(f"{k}×{v}" for k, v in sorted(tb.items(), key=lambda x:-x[1])[:3])
            tok = f"{fmt_int(s.get('input_tokens',0))}/{fmt_int(s.get('output_tokens',0))}/{fmt_int(s.get('cache_read_tokens',0))}"
            E(f"| {i} | {s['agent']} | `{s.get('model','?')}` | {s.get('version','?')} | {(s.get('start') or '?')[:16].replace('T',' ')} | {fmt_dur(s.get('duration_s'))} | {s.get('user_turns',0)} | {s.get('assistant_turns',0)} | {s.get('tool_calls_total',0)} | {top} | {tok} | ${s.get('cost_usd',0):.2f} |")
        E("")
        # First prompts as hints on activities
        E("**Opening prompt(s) / tasks:**")
        E("")
        for i, s in enumerate(sess, 1):
            p = (s.get("first_user_prompt") or "").strip().replace("\n", " ")
            if len(p) > 280:
                p = p[:280] + "…"
            E(f"{i}. _[{s['agent']}, {s.get('start','')[:10]}]_ {p or '(no captured user text)'}")
        E("")
        # Activity counts on prompts
        ac = d.get("activity_counts", {})
        if ac:
            E("**Activity classes seen in opening prompts:** " +
              ", ".join(f"{k} ({v})" for k, v in sorted(ac.items(), key=lambda x:-x[1])))
            E("")

    # Aggregate activities across projects
    all_activities = Counter()
    for d in data.values():
        for k, v in d.get("activity_counts", {}).items():
            all_activities[k] += v

    E("## 5. What kinds of SE tasks were performed?")
    E("")
    E("Activity labels are derived from first-prompt keywords plus tool-breakdown patterns; they describe the *intent* of a session, not every turn inside it.")
    E("")
    E("### 5.1 Activity distribution across sessions")
    E("")
    E("| Activity class | Sessions |")
    E("|---|---:|")
    for k in ACTIVITIES:
        E(f"| {k} | {all_activities.get(k,0)} |")
    if all_activities.get("Unclassified"):
        E(f"| _Unclassified_ | {all_activities['Unclassified']} |")
    E("")
    E("### 5.2 'Features' built — one-line per project")
    E("")
    E("Counting the main engineering deliverables across the analysed projects, broadly:")
    E("")
    E("1. **Chess engines in COBOL** (2 projects: `chess-cobol-cc`, `COBOL-chess`) — move generation, search, evaluation, PGN I/O, ELO benchmarking vs cutechess.")
    E("2. **COBOL compilers in COBOL** (2 projects: `cobol-compiler-cc`, `cobol-compiler-codex`) — lexer, preprocessor, parser, COBOL→C code generator, COBOL interpreter, multi-program linking, RECURSIVE programs, COMP-5, CALL to C, a large intrinsic library. The `-cc` build produces a self-hosted compiler of ~11k COBOL LOC.")
    E("3. **COBPACK columnar compressor** (`cobol-compress-codex`) — pure COBOL implementation of a fixed-record packer with NONE + RLESP codecs, CRC32, determinism / randomised round-trip test harness, schema-aware packing.")
    E("4. **Doom in COBOL** + Java port + C demo (`cobol-doom`) — ray-casting engine, enemies, pickups, level definitions.")
    E("5. **Payroll case-study in COBOL** (`cobol-jb`) — fixed-format records, overtime rules, social contributions, payslip + summary report, verification grid.")
    E("6. **pygame-for-COBOL framework** (`COBOL-pygame`) — C glue exposing pygame-like primitives callable from GnuCOBOL, plus examples.")
    E("7. **SAT solver in COBOL** (`SATCobol-codex`) — DIMACS CNF parser, unit-propagation + search split across 5 COPY modules, SAT4J / MiniSat cross-check harness, uf/uuf benchmark sets at 75 / 100 / 125 / 150 vars.")
    E("8. **Games: Game-of-15 / tic-tac-toe** (`cobol-tictactoe`) — minimax tree search, N-variant, multiple board sizes.")
    E("")
    E("### 5.3 Tool-use patterns")
    E("")
    E("Across all sessions, dominant tools were:")
    E("")
    tool_totals = Counter()
    tool_agent = {"Claude Code": Counter(), "Codex": Counter()}
    for d in data.values():
        for s in d["sessions"]:
            for k, v in (s.get("tool_breakdown") or {}).items():
                tool_totals[k] += v
                tool_agent[s["agent"]][k] += v
    E("| Tool | Calls | Dominant agent |")
    E("|---|---:|---|")
    for tool, n in tool_totals.most_common(15):
        dom = "Claude Code" if tool_agent["Claude Code"][tool] >= tool_agent["Codex"][tool] else "Codex"
        E(f"| `{tool}` | {fmt_int(n)} | {dom} |")
    E("")
    E("Takeaways:")
    E("")
    E("- Codex spends the overwhelming majority of its tool budget on `exec_command` (shell) and `write_stdin` (interactive pipes) — lots of compile-run-inspect loops; edits go through `apply_patch`.")
    E("- Claude Code splits its budget across `Bash`, `Edit`, `Read`, `Write`, `Grep`, `Agent` and `TaskUpdate` — showing a richer planning/editing toolchain but fewer raw shell cycles per session.")
    E("- Both agents show heavy *iterative* workflows (build → run → fix) on COBOL, consistent with GnuCOBOL's finicky formatting rules and the multi-day debugging cycles visible in `chess-cobol-cc`, `cobol-compiler-cc`, `cobol-doom`, and `cobol-tictactoe`.")
    E("")

    E("## 6. Coding agents — versions seen on disk")
    E("")
    E("| Agent | Models | CLI versions |")
    E("|---|---|---|")
    for ag in ("Claude Code", "Codex"):
        ms = Counter()
        vs = set()
        for d in data.values():
            for s in d["sessions"]:
                if s["agent"] != ag:
                    continue
                if s.get("model"):
                    ms[s["model"]] += 1
                if s.get("version"):
                    vs.add(s["version"])
        E(f"| {ag} | {', '.join(f'`{k}`×{v}' for k,v in ms.most_common())} | {', '.join(sorted(vs))} |")
    E("")
    E("**Notes on versions.**")
    latest_cc_ver = sorted({s.get("version","") for d in data.values() for s in d["sessions"]
                             if s.get("agent") == "Claude Code" and s.get("version","").startswith("2.")})
    latest_cc = latest_cc_ver[-1] if latest_cc_ver else "?"
    E(f"- Claude Code CLI on this machine ranges from **2.1.63** (earliest seen, Mar 2026, `cobol-doom`) to **{latest_cc}** (most recent Claude-Code-driven session in the set).")
    E("- Codex CLI ranges from **0.98.0** (Feb 2026) to **0.118.0-alpha.2** (April 2026); Codex model names evolved `gpt-5.2` → `gpt-5.3-codex` → `gpt-5.4` over the window.")
    E("- Claude model: consistently `claude-opus-4-6` (1M context).")
    E("")

    E("## 7. Caveats")
    E("")
    E("- **Duration ≠ active work.** The `duration_s` field is last-event-minus-first-event; resumed sessions (most notably `chess-cobol-cc`, 18d; `cobol-compiler-cc`, 11d; `cobol-doom`, 27d) span many days with long idle gaps. A more faithful 'active work' estimate would require summing inter-event gaps below some threshold.")
    E("- **Cost is an API-rack-rate upper bound.** Actual billing under Team / Max / Pro subscriptions does not map linearly to the token counts; take these figures as an order-of-magnitude signal of compute intensity, not a cash figure.")
    E("- **Two folders excluded** from the main analysis: `cobol-vibes` and `test-cline-COBOL` have artefacts (Flappy-Bird variants in COBOL) but no preserved agent JSONL traces on this machine.")
    E("- **Activity labels are shallow.** Derived from first-prompt keywords; a proper classification would read every turn.")
    E("")

    with open(args.out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
