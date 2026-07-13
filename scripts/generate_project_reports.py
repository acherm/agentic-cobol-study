#!/usr/bin/env python3
"""Emit a structured Markdown report per project, one RQ per section.

Reads output/metrics/<project>.json + optional domain notes map, and writes
output/reports/<project>.md. The narrative RQ1/RQ2/RQ3 are seeded from README
excerpts + first/last user prompts so the reader can see the full story from
the project itself (not hand-authored).
"""
import argparse, json, os, re, sys
from collections import Counter

DOMAIN_NOTES = {
    "chess-cobol-cc": {
        "short": "Chess engine in COBOL (GnuCOBOL).",
        "novelty": "Writing a performance-sensitive UCI-speaking engine in a language nobody writes engines in. Elo is the objective measure.",
        "sub_challenges": ["FEN parser","UCI protocol I/O","bitboard or mailbox representation","move generation (pseudo-legal / legal, castling, en-passant)","search with alpha-beta + move ordering","evaluation function","time management for cutechess matches"],
    },
    "COBOL-chess": {
        "short": "Chess engine in COBOL with formal architecture + spec backlog.",
        "novelty": "Second chess-engine attempt — this time led by Codex (GPT-5) instead of Claude, with explicit architecture / specification artefacts.",
        "sub_challenges": ["FEN/UCI I/O","move gen","search","opening book","openings + results directories","reproducible cutechess matches"],
    },
    "cobol-compiler-cc": {
        "short": "COBOL compiler (and interpreter) written in COBOL.",
        "novelty": "Self-hosting-ish: a COBOL→C compiler and a tree-walking interpreter, both authored in COBOL. The compiler's own source is ~11k COBOL LOC.",
        "sub_challenges": ["lexer + preprocessor","parser for COBOL 74/85 subset (fixed+free format)","PIC/USAGE decoding","DATA DIVISION → C struct generation","PROCEDURE DIVISION → C functions","COMP-5 binary types","PERFORM THRU paragraph ranges","RECURSIVE programs","CALL to external C","multi-program linking","COBOL intrinsics library","benchmark harness vs GnuCOBOL"],
    },
    "cobol-compiler-codex": {
        "short": "Alternative minicobc COBOL-to-C compiler, driven by Codex.",
        "novelty": "Second compiler implementation as a controlled replication with a different agent, same ambition (compile non-trivial COBOL).",
        "sub_challenges": ["subset of lexer/parser","code-gen","scripts/benchmarks","run known non-trivial programs (doom, game15tictactoe)","compare output/perf vs GnuCOBOL"],
    },
    "cobol-compress-cobolcc": {
        "short": "COBPACK — columnar compressor for fixed-record COBOL data (Claude-Code-built, pure COBOL) — second-agent replica of the COBPACK domain.",
        "novelty": "Cross-agent replication of the COBPACK specification with Claude Code; closes the 2-agent gap for the columnar-compressor domain. Three separate COBOL source files (cobpack + crc32 + rlesp).",
        "sub_challenges": ["schema parser","CPC v0/v1 container format","NONE + RLESP codecs","CRC32 integrity","determinism + round-trip trust suite","multi-file COBOL build"],
    },
    "cobol-compress-codex": {
        "short": "COBPACK — columnar compressor for fixed-record COBOL data (Codex-built, pure COBOL).",
        "novelty": "Specification-driven build of a MVP0 / MVP1 compressor with NONE + RLESP codecs and rigorous trust tests, implemented directly in COBOL.",
        "sub_challenges": ["fixed-format COBOL implementation","codec parity with -cc","test parity","binary compat"],
    },
    "cobol-doom-cc": {
        "short": "Doom-like FPS in COBOL (Claude Code) — walker + ray-casting + enemies + levels via copybook modules.",
        "novelty": "Second-generation clean Doom build with Claude Code; modular via 7 COPY books (render/world/entities/levels/screens).",
        "sub_challenges": ["ray casting via integer trig","raw-mode terminal input","COBOL ↔ C ABI for per-frame traffic","enemies / pickups / multi-level progression","modular COPY-book architecture"],
    },
    "cobol-doom-codex": {
        "short": "Doom-like FPS in COBOL (Codex) — gridwalker + SDL2 bridge + 11 COPY books.",
        "novelty": "Codex-built Doom replica with SDL2 graphical rendering (not terminal-only); modular via 11 COPY books.",
        "sub_challenges": ["ray casting via integer trig","SDL2 bridge from COBOL via C glue","enemies / pickups / multi-level","modular COPY-book architecture (11 modules)","BMP sprite assets"],
    },
    "cobol-jb": {
        "short": "Payroll processing case-study in GnuCOBOL.",
        "novelty": "Industrial-style domain exercise (employee records → payslips + summary) used as a replay/verification grid.",
        "sub_challenges": ["fixed-format input file","overtime rules per category","social-contribution rules","formatted output","verification report"],
    },
    "COBOL-pygame": {
        "short": "A pygame-like framework callable from COBOL (GnuCOBOL).",
        "novelty": "C glue + COPY books exposing pygame-style primitives to COBOL programs.",
        "sub_challenges": ["Python/C integration","COBOL → C FFI via CALL","input/event loop","sample games"],
    },
    "SATCobol-codex": {
        "short": "SAT solver in COBOL (Codex-built) with modular copybooks (`cnf`, `io`, `parser`, `propagate`, `search`) and SAT4J / MiniSat cross-checks.",
        "novelty": "Second-generation COBOL SAT attempt: a small 280-LOC core orchestrating five COPY books, validated against SAT4J + MiniSat on uf/uuf benchmark families at 75/100/125/150 variables.",
        "sub_challenges": ["DIMACS CNF parser in its own COPY","clause / literal representation in free-format COBOL","unit propagation module","decision heuristic module","SAT4J / MiniSat cross-check harness","perf runner over uf/uuf benchmark sets","result comparison + failure capture"],
    },
    "SATCobol-cc": {
        "short": "SAT solver in COBOL (Claude-Code-built) — the Claude-Code replica of the SAT domain, paired with the Codex-built `SATCobol-codex`.",
        "novelty": "Cross-agent replication: same SAT-solving contract, same `uf`/`uuf` benchmarks, different coding agent — lets us compare how two agents approach CDCL-style solving in COBOL side-by-side.",
        "sub_challenges": ["DIMACS CNF parser","clause/literal representation without pointers","unit propagation","decision heuristic","cross-check against MiniSat / SAT4J","performance parity vs the Codex sibling"],
    },
    "game15-cobol-codex": {
        "short": "Game of 15 / tic-tac-toe in COBOL (Codex-built) — the Codex replica of the small-game domain, paired with the Claude-Code-built `cobol-tictactoe`.",
        "novelty": "Cross-agent replication: same game-of-15 / minimax tree contract, different agent. Specifically exercises the `REPLAY_PROMPTS.md` produced for `cobol-tictactoe`.",
        "sub_challenges": ["game counting via enumeration","symmetry deduplication via magic square","optimal-play tree with avoid annotations","parameterized gameN variant","multi-variant interactive I/O"],
    },
    "cobol-tictactoe": {
        "short": "Game-of-15 / tic-tac-toe variants with minimax tree search in COBOL.",
        "novelty": "Numeric game-of-15 is isomorphic to tic-tac-toe; programme multiple size variants + full search tree.",
        "sub_challenges": ["game state encoding","minimax recursion via PERFORM","alpha-beta (later)","multi-variant (N boards)","interactive I/O"],
    },
}


def fmt_dur(s):
    if not s: return "-"
    s = int(s)
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    if d: return f"{d}d {h}h {m}m"
    if h: return f"{h}h {m}m"
    return f"{m}m {s}s"


def fmt_int(n):
    return f"{n:,}" if isinstance(n, int) else str(n)


def pct(n, total):
    if not total: return "0%"
    return f"{100*n/total:.1f}%"


def truncate(s, n=400):
    if s is None: return ""
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n] + "…"


def render(m, difficulty=None):
    proj = m["project"]
    notes = DOMAIN_NOTES.get(proj, {})
    inv = m.get("inventory") or {}
    comp = m.get("complexity") or {}
    gitd = m.get("git") or {}
    sess = m.get("sessions") or []
    up = m.get("user_prompts") or {}
    at = m.get("active_time") or {}
    by_act = at.get("by_se_task_s") or at.get("by_activity_s") or {}
    tot_active = at.get("total_active_s") or 0
    errors = m.get("errors") or {}
    tool_use = m.get("tool_use") or {}
    dsig = (m.get("difficulty_signals") or {})
    dscore = difficulty or {}

    L = []
    E = L.append
    E(f"# `{proj}` — Case Study")
    E("")
    # Link to the calibrated assessment + backlog artefacts + replay prompts
    assessment_rel = f"../assessments/{proj}.md"
    backlog_rel = f"../backlogs/{proj}/SPECIFICATION_BACKLOG.md"
    story_abs = os.path.join(os.path.expanduser("~/SANDBOX/cobol-meta-analysis"),
                             f"output/backlogs/{proj}/STORY.md")
    story_rel = f"../backlogs/{proj}/STORY.md"
    replay_abs = os.path.join(os.path.expanduser("~/SANDBOX/cobol-meta-analysis"),
                              f"output/backlogs/{proj}/REPLAY_PROMPTS.md")
    replay_rel = f"../backlogs/{proj}/REPLAY_PROMPTS.md"
    key_feat_abs = os.path.join(os.path.expanduser("~/SANDBOX/cobol-meta-analysis"),
                                f"output/backlogs/{proj}/KEY_FEATURES.md")
    key_feat_rel = f"../backlogs/{proj}/KEY_FEATURES.md"
    if os.path.exists(story_abs):
        E(f"> 📝 **Story** (full narrative: context, novelty, evolution, validation, insight): [`STORY.md`]({story_rel})  ")
    E(f"> 📋 **Calibrated assessment** (evidence + strengths + honest gaps): [`{proj}` assessment]({assessment_rel})  ")
    E(f"> 📖 **Feature ledger** (agent-centric, step-wise): [`SPECIFICATION_BACKLOG.md`]({backlog_rel})")
    if os.path.exists(key_feat_abs):
        E(f"  ")
        E(f"> 🏆 **Key features** (ranked by significance × depth): [`KEY_FEATURES.md`]({key_feat_rel})")
    if os.path.exists(replay_abs):
        E(f"  ")
        E(f"> 🔁 **Replay prompts** (step-wise, HOW-agnostic, for reproducing with a different agent): [`REPLAY_PROMPTS.md`]({replay_rel})")
    E("")
    E(f"**Project root.** `{m.get('project_root')}`  ")
    E(f"**Sessions.** {len(sess)} ({sum(1 for s in sess if s['agent']=='Claude Code')} Claude Code + {sum(1 for s in sess if s['agent']=='Codex')} Codex)  ")
    if sess:
        E(f"**Activity window.** {sess[0].get('start','?')[:10]} → {sess[-1].get('end','?')[:10]} ({m.get('span_days',0)} days)  ")
    agent_models = sorted({s["agent"] + "/" + str(s.get("model","?")) for s in sess})
    E("**Agents & models.** " + ", ".join(agent_models))
    E("")
    E("---")
    E("")

    # ===== RQ1 =====
    E("## RQ1 — Domain, intent, novelty")
    E("")
    if notes:
        E(f"**What it is.** {notes.get('short','')}")
        E("")
        E(f"**Why it's interesting.** {notes.get('novelty','')}")
        E("")
    # Pull README first section + initial prompt
    excerpts = m.get("story_excerpts") or {}
    if "README.md" in excerpts:
        E("**From the project's `README.md` (first sections):**")
        E("")
        for sec, body in list(excerpts["README.md"].items())[:2]:
            body = truncate(body, 600)
            E(f"> **{sec}**  \n> {body}")
            E("")
    if up.get("first_prompt"):
        E("**Opening prompt that kicked off the project:**")
        E("")
        E("```")
        E(truncate(up["first_prompt"], 800))
        E("```")
        E("")

    # ===== RQ2 =====
    E("## RQ2 — Engineering challenges")
    E("")
    if notes.get("sub_challenges"):
        E("**Sub-challenges that a human engineer would have to solve (derived from the domain):**")
        E("")
        for sc in notes["sub_challenges"]:
            E(f"- {sc}")
        E("")
    # Evidence of challenges: error tags observed
    etags = errors.get("error_tags") or {}
    if etags:
        E("**Concrete difficulties actually encountered during the sessions**, counted from tool-result error signals:")
        E("")
        E("| Error class | Hits |")
        E("|---|---:|")
        for k, v in sorted(etags.items(), key=lambda x:-x[1]):
            label = {
                "cobc":"GnuCOBOL compiler error (incl. syntax)",
                "linker":"linker error (undefined reference)",
                "cc":"C compiler error",
                "segfault":"segmentation fault at runtime",
                "busfault":"bus error at runtime",
                "python":"Python traceback (tooling)",
                "testfail":"test suite reported FAIL",
                "assert":"assertion failed",
                "abort":"process aborted",
                "missing":"missing file",
                "missing-cmd":"command not found",
                "perm":"permission denied",
                "exit-nonzero":"command exited with non-zero status",
            }.get(k, k)
            E(f"| {label} | {v} |")
        E("")
    else:
        E("_No explicit error signatures were detected in tool outputs — either the project compiled cleanly or error text was in a format the detector missed._")
        E("")

    # ===== RQ2b — Feature ledger =====
    feats = m.get("features") or {}
    if feats:
        backlog = feats.get("spec_backlog") or []
        readme_f = feats.get("readme_features") or []
        prompt_sub = feats.get("prompt_subtasks") or []
        commit_sub = feats.get("commit_subjects") or []
        E("## RQ2b — Feature ledger (what was actually built)")
        E("")
        E("Feature-like items discovered across four sources. The backlog (when present) is the authoritative ledger; the other three are fall-back signals.")
        E("")
        E("| Source | Items |")
        E("|---|---:|")
        E(f"| `SPECIFICATION_BACKLOG.md` / `*BACKLOG*.md` (F-### rows) | **{len(backlog)}** |")
        E(f"| `README.md` / `REPORT.md` bullet lists under a Features heading | {len(readme_f)} |")
        E(f"| Bullet / numbered sub-requests inside user prompts | {len(prompt_sub)} |")
        E(f"| Git commit subjects | {len(commit_sub)} |")
        E("")
        if backlog:
            # Group by phase for display
            phases = {}
            order = []
            for it in backlog:
                ph = it.get("phase") or "_unclassified_"
                if ph not in phases:
                    phases[ph] = []
                    order.append(ph)
                phases[ph].append(it)
            E(f"**Backlog ({len(backlog)} F-### entries).** Grouped by phase:")
            E("")
            for ph in order:
                items = phases[ph]
                E(f"- **{ph}** — {len(items)} features  \n  " +
                  "; ".join(truncate(it['title'], 70) for it in items[:8]) +
                  (f" _(+{len(items)-8} more)_" if len(items) > 8 else ""))
            E("")
        if readme_f:
            E(f"**README/REPORT features ({len(readme_f)})** — first 8:")
            E("")
            for f_ in readme_f[:8]:
                E(f"- {truncate(f_, 180)}")
            E("")
        if prompt_sub:
            E(f"**Prompt-extracted sub-requests ({len(prompt_sub)})** — first 8 (sub-bullets inside user messages):")
            E("")
            for it in prompt_sub[:8]:
                E(f"- _[{(it.get('ts') or '')[:10]}]_ {truncate(it['item'], 160)}")
            E("")
        if commit_sub:
            E(f"**Git commits ({len(commit_sub)})** — first 8:")
            E("")
            for c in commit_sub[:8]:
                E(f"- `{c['sha']}` {c['date']}  {truncate(c['subject'], 150)}")
            E("")

    # ===== RQ3 =====
    E("## RQ3 — What was delivered")
    E("")
    # Look for verification/final report sections
    for f in ("VERIFICATION_REPORT.md","REPORT.md","TRUST.md"):
        if f in excerpts:
            E(f"**From `{f}`:**")
            E("")
            for sec, body in list(excerpts[f].items())[:2]:
                body = truncate(body, 500)
                E(f"> **{sec}**  \n> {body}")
                E("")
    # Artefacts: executables under root
    root = m["project_root"]
    execs = []
    if os.path.isdir(root):
        for fn in sorted(os.listdir(root)):
            fp = os.path.join(root, fn)
            if os.path.isfile(fp) and os.access(fp, os.X_OK) and not fn.endswith(".sh") and "." not in fn[1:]:
                try:
                    execs.append((fn, os.path.getsize(fp)))
                except Exception:
                    pass
    if execs:
        E("**Executables present in the root of the project** (evidence that something builds):")
        E("")
        for fn, sz in execs[:10]:
            E(f"- `{fn}` ({sz/1024:.0f} KB)")
        if len(execs) > 10:
            E(f"- _(+{len(execs)-10} more)_")
        E("")

    # Last assistant message — not stored in metrics (too large); approximate via session hint
    # skip

    # ===== RQ4 =====
    E("## RQ4 — Size and complexity")
    E("")
    by_lang = (inv.get("by_lang") or {})
    E("**File inventory** ({} files, {:.1f} MB).".format(inv.get("total_files",0), (inv.get("total_bytes",0) or 0)/1e6))
    E("")
    if by_lang:
        E("| Language | Files | LOC |")
        E("|---|---:|---:|")
        for lang, v in sorted(by_lang.items(), key=lambda x:-x[1].get("loc",0)):
            if v.get("files",0)==0 and v.get("loc",0)==0: continue
            E(f"| {lang} | {v.get('files',0)} | {fmt_int(v.get('loc',0))} |")
        E("")
    if comp and comp.get("aggregate"):
        agg = comp["aggregate"]
        E("**COBOL-specific structural metrics** (all `.cob`/`.cbl`/`.cpy` aggregated):")
        E("")
        E("| Metric | Value |")
        E("|---|---:|")
        E(f"| COBOL files | {agg.get('num_files',0)} |")
        E(f"| Total lines | {fmt_int(agg.get('total_lines',0))} |")
        E(f"| Code lines (non-blank, non-comment) | {fmt_int(agg.get('code_lines',0))} |")
        E(f"| Comment lines | {fmt_int(agg.get('comment_lines',0))} |")
        E(f"| Sections | {agg.get('sections',0)} |")
        E(f"| Paragraphs | {agg.get('paragraphs',0)} |")
        E(f"| Data items (level-number declarations) | {agg.get('data_items',0)} |")
        E(f"| Max IF/EVALUATE nesting (any file) | {agg.get('max_nesting_any_file',0)} |")
        E("")
        stmts = agg.get("statements") or {}
        stmts_row = sorted(stmts.items(), key=lambda x:-x[1])
        E("**COBOL statement frequency (top 10):**")
        E("")
        E("| Statement | Count |")
        E("|---|---:|")
        for k,v in stmts_row[:10]:
            if v==0: break
            E(f"| `{k}` | {fmt_int(v)} |")
        E("")
        if agg.get("top_files_by_code_lines"):
            E("**Largest COBOL files:**")
            E("")
            E("| File | Code lines |")
            E("|---|---:|")
            for row in agg["top_files_by_code_lines"][:5]:
                E(f"| `{row['file']}` | {fmt_int(row['code_lines'])} |")
            E("")
    if gitd.get("has_git"):
        E("**Git churn signal.** "
          f"{gitd.get('commits',0)} commits, "
          f"{gitd.get('churn',{}).get('insertions_total',0)} insertions / "
          f"{gitd.get('churn',{}).get('deletions_total',0)} deletions, "
          f"first {gitd.get('first_commit','?')[:10]}, last {gitd.get('last_commit','?')[:10]}.")
        E("")
    else:
        E("_No `.git` directory — project was not versioned locally._")
        E("")

    # ===== RQ4b — COBOL language mastery =====
    if comp and comp.get("aggregate") and comp["aggregate"].get("num_files", 0) > 0:
        agg = comp["aggregate"]
        caps = agg.get("capabilities") or {}
        E("## RQ4b — COBOL language mastery")
        E("")
        E(f"**Mastery score:** **{agg.get('mastery_score',0)}** distinct COBOL constructs used "
          f"across **{agg.get('categories_exercised',0)}/{len(caps)}** capability categories "
          f"(a pure \"Hello World\" scores 2–3; the reference GnuCOBOL test-suite programs cover ~70).")
        E("")
        # one-line per category: exercised? count + which specific constructs
        cat_desc = {
            "control_flow":   "branching / looping / termination (IF, PERFORM, EVALUATE, GO TO…)",
            "arithmetic":     "numeric ops (ADD/SUBTRACT/MULTIPLY/DIVIDE/COMPUTE, ROUNDED, ON SIZE ERROR)",
            "data_advanced":  "rich data descriptions (OCCURS/arrays, REDEFINES, USAGE COMP/COMP-3/COMP-5, 88-level condition names…)",
            "io_file":        "FILE SECTION, FD, OPEN/READ/WRITE/REWRITE/AT END/INVALID KEY, INDEXED / RELATIVE organizations",
            "string_ops":     "STRING/UNSTRING/INSPECT, reference modification `var(a:b)`",
            "tables_search":  "SEARCH / SEARCH ALL, SORT / MERGE, SET, INITIALIZE",
            "subprograms":    "CALL, LINKAGE SECTION, USING/GIVING, BY CONTENT/REFERENCE/VALUE, RECURSIVE",
            "copy_preproc":   "COPY books, REPLACING / REPLACE",
            "intrinsics":     "FUNCTION library (NUMVAL, UPPER-CASE, RANDOM, MOD, LENGTH, …)",
            "misc":           "DISPLAY / ACCEPT / STOP literal",
        }
        E("| Category | Exercised? | Total occurrences | Distinct constructs seen |")
        E("|---|:---:|---:|---|")
        for cat, desc in cat_desc.items():
            d = caps.get(cat) or {}
            total = d.get("total", 0)
            constructs = d.get("constructs", {}) or {}
            if total == 0:
                E(f"| **{cat}** <br/>_{desc}_ | — | 0 |  |")
            else:
                top = sorted(constructs.items(), key=lambda x:-x[1])
                lst = ", ".join(f"`{k}`×{v}" for k,v in top[:8])
                if len(top) > 8:
                    lst += f" _(+{len(top)-8} more)_"
                E(f"| **{cat}** <br/>_{desc}_ | ✓ | {total:,} | {lst} |")
        E("")
        # Light capability readouts
        agg_c = agg.get("capabilities") or {}
        notable = []
        for cat_name, ck in (("subprograms","CALL"),("subprograms","RECURSIVE"),
                             ("data_advanced","OCCURS"),("data_advanced","REDEFINES"),
                             ("data_advanced","USAGE_COMP_5"),("copy_preproc","COPY"),
                             ("tables_search","SEARCH_ALL"),("io_file","FD"),
                             ("string_ops","UNSTRING"),("intrinsics","FUNCTION")):
            v = (agg_c.get(cat_name,{}).get("constructs") or {}).get(ck, 0)
            if v:
                notable.append(f"`{ck}` ({v}×)")
        if notable:
            E("**Notable non-trivial constructs used:** " + ", ".join(notable) + ".")
            E("")
        E(f"**Procedural structure.** {agg.get('paragraphs',0)} paragraphs, {agg.get('sections',0)} sections "
          f"across {agg.get('num_files',0)} COBOL file(s). That means roughly "
          f"**{agg.get('paragraphs',0)} function-like units** (every paragraph is a PERFORM-able entry point; "
          f"a generalist mapping is: 1 paragraph ≈ 1 small function in C/Python).")
        E("")

    # ===== RQ5 =====
    E("## RQ5 — SE-task breakdown (how effort was spent)")
    E("")
    E("Active time = sum of inter-event gaps ≤ 10 min (gaps longer than that are treated as idle). "
      f"Total **active** collaboration time for this project: **{fmt_dur(tot_active)}** across {m.get('n_turns',0)} events.")
    E("")
    E("SE-task labels are assigned to every event with the following logic:")
    E("- the tool used determines the default label (e.g. `Edit`/`Write`/`apply_patch` → `feature`, `Read`/`Grep`/`Glob` → `understanding`, `Bash`/`exec_command` with a compiler in the command → `build`, with a test runner → `test`, etc.);")
    E("- **any edit or re-run that happens within 3 turns after an error tool output is relabeled `bug_fix`**, regardless of its default label. This is the contextual rule that separates _new feature_ from _debugging_.")
    E("")
    if by_act:
        total = sum(by_act.values())
        TASK_DESC = {
            "feature":       "adding new functionality",
            "bug_fix":       "correcting an observed defect",
            "performance":   "making it faster",
            "test":          "writing or running tests / benchmarks",
            "refactor":      "restructuring without behaviour change",
            "understanding": "reading / searching to build a mental model",
            "build":         "compile / makefile / dependency work",
            "spec":          "specifications / architecture writing",
            "doc":           "README / comments / final reports",
            "port":          "translating across languages",
            "verification":  "auditing / review / grid-verification",
            "plan":          "task tracking, planning",
            "unknown":       "could not classify confidently",
        }
        E("| SE task | Meaning | Active time | Share |")
        E("|---|---|---:|---:|")
        for task, t in sorted(by_act.items(), key=lambda x:-x[1]):
            E(f"| `{task}` | {TASK_DESC.get(task,'—')} | {fmt_dur(t)} | {pct(t,total)} |")
        E("")
    # Tool-use by SE task
    tba = (tool_use.get("by_se_task") or {})
    if tba:
        E("**Tool calls by SE task:**")
        E("")
        E("| SE task | Tool calls |")
        E("|---|---:|")
        for k,v in sorted(tba.items(), key=lambda x:-x[1]):
            E(f"| `{k}` | {fmt_int(v)} |")
        E("")

    # ===== RQ6 =====
    E("## RQ6 — Failures encountered")
    E("")
    tr = errors.get("tool_outputs", 0); te = errors.get("tool_output_errors", 0)
    E(f"Out of **{fmt_int(tr)} tool results**, **{fmt_int(te)}** ({pct(te,tr)}) contained an error signature.")
    E("")
    # Bug-report prompts
    intent = up.get("intent_breakdown") or {}
    if intent.get("bug-report"):
        E(f"The user filed **{intent['bug-report']} bug-report-style prompt(s)** (prompts containing words like 'error', 'crash', 'broken', 'wrong').")
        E("")
    # What the agent spent on fix-activity
    fix_time = by_act.get("fix", 0)
    if fix_time:
        E(f"Agent spent **{fmt_dur(fix_time)}** on fix activity — {pct(fix_time, tot_active)} of active time.")
        E("")

    # ===== RQ6b — difficulty =====
    E("## RQ6b — Difficulty assessment")
    E("")
    if dscore:
        label = dscore.get("label","?"); idx = dscore.get("index",0)
        mean_rank = dscore.get("mean_rank",0)
        E(f"**Auto-label: `{label}`** (difficulty index {idx:.2f}; mean rank across 7 signals = {mean_rank:.1f}).")
        E("")
        E("The label is computed from a rank-average of seven observable signals, each monotonic in 'harder':")
        E("")
        E("| Signal | This project | Rank (1=lowest across 11 projects) |")
        E("|---|---:|---:|")
        sig_labels = {
            "active_hours":           "Active hours (collaboration time)",
            "span_days":              "Calendar span (days first→last event)",
            "user_prompts":           "User prompts",
            "redirect_bug_prompts":   "Redirect / bug-report prompts",
            "error_rate":             "Tool-output error rate",
            "fix_cycles":             "Fix cycles (error → immediate retry)",
            "fix_time_share":         "Share of active time spent on `bug_fix`",
        }
        ranks = dscore.get("ranks") or {}
        for k, desc in sig_labels.items():
            val = dsig.get(k)
            if isinstance(val, float):
                val_s = f"{val:.3f}" if k in ("error_rate","fix_time_share") else f"{val:.1f}"
            else:
                val_s = f"{val}"
            E(f"| {desc} | {val_s} | {ranks.get(k,'-')} |")
        E("")
        E("_Note: calendar span can be inflated by resumed sessions across multiple days; read it together with active hours, not alone._")
        E("")

    # ===== RQ7 =====
    E("## RQ7 — User strategy")
    E("")
    E(f"- **User prompts total:** {up.get('count',0)}")
    E(f"- **Average prompt length:** {up.get('avg_len',0):.0f} chars; **max:** {fmt_int(up.get('max_len',0))} chars")
    E(f"- **Total chars written by user:** {fmt_int(up.get('total_chars',0))}")
    E(f"- **Sessions:** {len(sess)}; **span:** {m.get('span_days',0)} days")
    E(f"- **Long-prompt ratio** (≥500 chars): {sum(1 for p_ in _iter_prompts(m) if p_>=500)}/{up.get('count',0)}")
    E("")
    # sessions table
    if sess:
        E("| # | Agent | Model | Started | Wall dur | User turns | Tool calls | Cost est. |")
        E("|---:|---|---|---|---:|---:|---:|---:|")
        for i, s in enumerate(sess,1):
            E(f"| {i} | {s['agent']} | `{s.get('model','?')}` | {(s.get('start') or '?')[:16].replace('T',' ')} | {fmt_dur(s.get('duration_s'))} | {s.get('user_turns',0)} | {s.get('tool_calls_total',0)} | ${s.get('cost_usd',0):.2f} |")
        E("")

    # ===== RQ8 =====
    E("## RQ8 — User interventions (prompt typology)")
    E("")
    intent = up.get("intent_breakdown") or {}
    if intent:
        E("| Intent class | Prompts |")
        E("|---|---:|")
        for k, v in sorted(intent.items(), key=lambda x:-x[1]):
            E(f"| {k} | {v} |")
        E("")
    # First 10 user prompts as ledger
    prompt_ledger = _first_prompts(m, 10)
    if prompt_ledger:
        E("**Prompt ledger — first 10 user prompts (truncated):**")
        E("")
        for i, (ts, txt) in enumerate(prompt_ledger,1):
            E(f"{i}. _[{(ts or '')[:10]}]_ {truncate(txt, 240)}")
        E("")

    # ===== RQ9 =====
    E("## RQ9 — Compute & cost")
    E("")
    tokens = m.get("tokens") or {}
    E("| Metric | Value |")
    E("|---|---:|")
    E(f"| Wall-clock session span (sum, incl. idle) | {fmt_dur(m.get('wall_duration_s',0))} |")
    E(f"| Active collaboration time | {fmt_dur(tot_active)} |")
    E(f"| Tool calls | {fmt_int(m.get('tool_calls_total',0))} |")
    E(f"| Input tokens | {fmt_int(tokens.get('in',0))} |")
    E(f"| Output tokens | {fmt_int(tokens.get('out',0))} |")
    E(f"| Cache-read tokens | {fmt_int(tokens.get('cache_read',0))} |")
    E(f"| Cache-create tokens | {fmt_int(tokens.get('cache_create',0))} |")
    E(f"| Reasoning tokens (Codex) | {fmt_int(tokens.get('reasoning',0))} |")
    E(f"| Estimated cost at API rack rates | ${m.get('cost_usd',0):.2f} |")
    E("")

    # --- Appendix: top tool list --------------------
    bt = (tool_use.get("by_tool") or {})
    if bt:
        E("### Appendix — tool call breakdown")
        E("")
        E("| Tool | Calls |")
        E("|---|---:|")
        for k, v in sorted(bt.items(), key=lambda x:-x[1])[:20]:
            E(f"| `{k}` | {fmt_int(v)} |")
        E("")

    # Methodology footer
    E("---")
    E("")
    E("_Generated by `scripts/generate_project_reports.py`. RQs are defined in `RQ_FRAMEWORK.md`. Data files: `output/sessions_all.json`, `output/turns/<project>__*.jsonl`, `output/complexity/<project>.json`, `output/git/<project>.json`, `output/metrics/<project>.json`._")
    return "\n".join(L) + "\n"


def _iter_prompts(m):
    """Yield all user-prompt lengths by reading the stored turn JSONLs."""
    lens = []
    for fp in m.get("turn_files") or []:
        try:
            with open(fp) as f:
                for line in f:
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    if r.get("role") == "user" and r.get("kind") == "prompt":
                        lens.append(r.get("text_len", 0) or 0)
        except Exception:
            continue
    return lens


BOOTSTRAP_MARKERS = (
    "# AGENTS.md", "<INSTRUCTIONS>", "<local-command-caveat>",
    "<command-name>", "<system-reminder>", "<ide_opened_file>",
    "<environment_context>", "<user_instructions>", "<project_doc>",
)

def _is_bootstrap(text):
    if not text: return True
    t = text.lstrip()[:200]
    return any(m in t for m in BOOTSTRAP_MARKERS)

def _first_prompts(m, n):
    """Pull first N real user prompts with ts from the turn samples."""
    out = []
    for fp in m.get("turn_files") or []:
        try:
            with open(fp) as f:
                for line in f:
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    if r.get("role")=="user" and r.get("kind")=="prompt":
                        prev = r.get("preview","") or ""
                        if _is_bootstrap(prev):
                            continue
                        out.append((r.get("ts"), prev))
        except Exception:
            continue
    out.sort(key=lambda x: x[0] or "")
    return out[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics-dir", required=True)
    ap.add_argument("--difficulty-json", default=None,
                    help="optional output/difficulty.json (adds difficulty section)")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--projects", nargs="+", required=True)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    difficulty = {}
    if args.difficulty_json and os.path.exists(args.difficulty_json):
        with open(args.difficulty_json) as f:
            difficulty = json.load(f)
    for p in args.projects:
        mp = os.path.join(args.metrics_dir, f"{p}.json")
        if not os.path.exists(mp):
            print(f"[miss] {p}", file=sys.stderr); continue
        with open(mp) as f: m = json.load(f)
        md = render(m, difficulty.get(p))
        out = os.path.join(args.out_dir, f"{p}.md")
        with open(out, "w") as f: f.write(md)
        print(f"[ok] {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
