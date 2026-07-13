#!/usr/bin/env python3
"""Generate paper figures from output/* JSON. Every figure in the paper
is produced here, so regenerating the dataset regenerates the figures."""

import json, os, sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
from system_names import display as disp
OUT  = ROOT / 'output'
FIGS = ROOT / 'figures'
FIGS.mkdir(exist_ok=True)

PROJECTS = ['cobol-jb-cc','cobol-jb-codex','COBOL-pygame','cobol-pygame-cc','cobol-tictactoe','cobol-compress-codex',
            'SATCobol-codex','cobol-doom-cc','cobol-doom-codex',
            'chess-cobol-cc','COBOL-chess',
            'cobol-compiler-codex','cobol-compiler-cc',
            'game15-cobol-codex','SATCobol-cc','cobol-compress-cobolcc']

# Author-calibrated rubrics for projects that lack a backlog-analyst
# appendix (COBOL-chess, cobol-doom, cobol-tictactoe) or were added after
# the last subagent run (game15-cobol-codex, SATCobol-cc). Scores reflect
# per-assessment TL;DR + KEY_FEATURES evidence + the standards ceiling
# discussion; they are conservatively authored (1 = acceptable-for-scope,
# 2 = clearly-good).
AUTHORED_RUBRIC = {
    'COBOL-chess':        dict(Q1=2.0, Q2=2.0, Q3=2.0, Q4=1.5, Q5=2.0, Q6=2.0, n_bl=184),
    'cobol-doom':         dict(Q1=2.0, Q2=2.0, Q3=1.5, Q4=1.0, Q5=1.5, Q6=1.5, n_bl=139),
    'cobol-tictactoe':    dict(Q1=2.0, Q2=2.0, Q3=1.5, Q4=1.5, Q5=1.5, Q6=1.5, n_bl=12),
    'game15-cobol-codex': dict(Q1=2.0, Q2=2.0, Q3=1.0, Q4=1.0, Q5=1.5, Q6=1.5, n_bl=6),
    'SATCobol-cc':        dict(Q1=2.0, Q2=2.0, Q3=1.5, Q4=1.0, Q5=1.5, Q6=2.0, n_bl=9),
    'cobol-compress-cobolcc': dict(Q1=2.0, Q2=2.0, Q3=2.0, Q4=1.5, Q5=1.5, Q6=2.0, n_bl=9),
    'cobol-doom-cc':          dict(Q1=2.0, Q2=2.0, Q3=1.5, Q4=1.0, Q5=1.5, Q6=1.5, n_bl=10),
    'cobol-doom-codex':       dict(Q1=2.0, Q2=2.0, Q3=1.5, Q4=1.0, Q5=1.5, Q6=1.5, n_bl=10),
    # July 2026 grid-completing replicas (author-approved 2026-07-08; evidence +
    # rationale in replications/payroll-remaining-steps.md)
    'cobol-jb-cc':        dict(Q1=2.0, Q2=2.0, Q3=1.0, Q4=1.5, Q5=2.0, Q6=1.5, n_bl=6),
    'cobol-jb-codex':     dict(Q1=2.0, Q2=2.0, Q3=1.0, Q4=1.5, Q5=2.0, Q6=2.0, n_bl=6),
    'cobol-pygame-cc':    dict(Q1=2.0, Q2=2.0, Q3=1.0, Q4=1.0, Q5=1.5, Q6=1.5, n_bl=5),
}

# Sort by difficulty index (ascending).
with open(OUT/'difficulty.json') as f:
    DIFF = json.load(f)
PROJECTS_BY_DIFF = sorted(DIFF.keys(), key=lambda p: DIFF[p]['index'])

# Color map for difficulty labels.
DIFF_COLORS = {'Low':'#3182bd','Medium':'#f6c049','High':'#e6550d','Very-High':'#8b1a0e'}

def load_metrics(p):
    with open(OUT/'metrics'/f'{p}.json') as f:
        return json.load(f)

mpl.rcParams.update({'font.size':9,'axes.titlesize':10,'axes.labelsize':9,
                     'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':8,
                     'figure.titlesize':11,'pdf.fonttype':42,'ps.fonttype':42})

# ------------------------------------------------------------------
# FIG 1: Difficulty landscape (rank-average index across 7 signals)
# ------------------------------------------------------------------
def fig_difficulty():
    projs  = PROJECTS_BY_DIFF
    idx    = [DIFF[p]['index']*100 for p in projs]
    labels = [DIFF[p]['label']      for p in projs]
    colors = [DIFF_COLORS[l]        for l in labels]

    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    bars = ax.barh([disp(p) for p in projs], idx, color=colors, edgecolor='black', linewidth=0.4)
    ax.set_xlabel('Difficulty index ($(\\bar{r}-1)/15 \\times 100$)')
    ax.set_xlim(0, 100)
    ax.axvline(25,  color='gray', lw=0.5, ls=':'); ax.text(26,  -0.6, 'Low',      fontsize=7, color='gray')
    ax.axvline(50,  color='gray', lw=0.5, ls=':'); ax.text(51,  -0.6, 'Medium',   fontsize=7, color='gray')
    ax.axvline(75,  color='gray', lw=0.5, ls=':'); ax.text(76,  -0.6, 'High',     fontsize=7, color='gray')
    for b, lbl, v in zip(bars, labels, idx):
        ax.text(v+1, b.get_y()+b.get_height()/2, lbl, va='center', fontsize=7)
    ax.set_title('Per-project difficulty index (low = easier, high = harder)')
    plt.tight_layout()
    plt.savefig(FIGS/'difficulty.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 2: SE-task distribution (stacked) per project, active time share
# ------------------------------------------------------------------
def fig_se_tasks():
    tasks = ['understanding','build','feature','bug_fix','test','spec','doc','plan','performance','unknown']
    colors = plt.get_cmap('tab10')(np.linspace(0,1,len(tasks)))
    data = {t: [] for t in tasks}
    for p in PROJECTS_BY_DIFF:
        m = load_metrics(p)
        bt = m['active_time']['by_se_task_s']
        tot = max(sum(max(v,0) for v in bt.values()), 1)
        for t in tasks:
            data[t].append(max(bt.get(t,0),0)/tot*100)

    fig, ax = plt.subplots(figsize=(7.0, 4.1))
    bot = np.zeros(len(PROJECTS_BY_DIFF))
    for t, c in zip(tasks, colors):
        vals = np.array(data[t])
        ax.barh([disp(p) for p in PROJECTS_BY_DIFF], vals, left=bot, color=c, label=t,
                edgecolor='white', linewidth=0.3)
        bot += vals
    ax.set_xlabel('Share of active collaboration time (\\%)')
    ax.set_xlim(0, 100)
    ax.legend(loc='center left', bbox_to_anchor=(1.01, 0.5), frameon=False)
    ax.set_title('How active time is spent, per project (projects sorted by difficulty)')
    plt.tight_layout()
    plt.savefig(FIGS/'se_tasks.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 3: Tool use -- per-agent normalized distribution
# ------------------------------------------------------------------
def fig_tool_use():
    agents = {'Claude Code': {}, 'Codex': {}}
    for p in PROJECTS:
        m = load_metrics(p)
        for sess in m['sessions']:
            agent = sess['agent']
            for t, c in sess.get('tool_breakdown', {}).items():
                agents[agent][t] = agents[agent].get(t, 0) + c
    # Top 8 tools across both
    all_tools = {}
    for a in agents.values():
        for t, c in a.items():
            all_tools[t] = all_tools.get(t, 0) + c
    top = [t for t,_ in sorted(all_tools.items(), key=lambda x:-x[1])[:10]]

    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    w = 0.4
    x = np.arange(len(top))
    cc = [agents['Claude Code'].get(t,0) for t in top]
    co = [agents['Codex'].get(t,0)       for t in top]
    ax.bar(x-w/2, cc, w, label='Claude Code', color='#3182bd', edgecolor='black', lw=0.3)
    ax.bar(x+w/2, co, w, label='Codex',       color='#e6550d', edgecolor='black', lw=0.3)
    ax.set_xticks(x, top, rotation=30, ha='right')
    ax.set_ylabel('Tool calls (count)')
    ax.set_yscale('log')
    ax.legend(frameon=False)
    ax.set_title('Tool-use profile per agent (top 10 tools across the corpus)')
    ax.grid(True, axis='y', ls=':', lw=0.3, which='major')
    plt.tight_layout()
    plt.savefig(FIGS/'tool_use.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 4: Error density vs activity -- does more effort mean more errors?
# ------------------------------------------------------------------
def fig_error_density():
    xs, ys, labels, colors, sizes = [], [], [], [], []
    for p in PROJECTS:
        s = DIFF[p]['signals']
        m = load_metrics(p)
        # COBOL LOC
        inv = m['inventory']['by_lang'].get('COBOL', {'loc':0})
        loc = inv['loc']
        xs.append(s['active_hours'])
        ys.append(s['error_rate']*100)
        labels.append(p)
        colors.append(DIFF_COLORS[DIFF[p]['label']])
        sizes.append(max(30, loc/20))

    fig, ax = plt.subplots(figsize=(6.8, 4.3))
    for x, y, lbl, c, sz in zip(xs, ys, labels, colors, sizes):
        ax.scatter(x, y, s=sz, c=c, edgecolors='black', linewidths=0.5, alpha=0.85)
        ax.annotate(disp(lbl), (x,y), xytext=(4,4), textcoords='offset points',
                    fontsize=7)
    ax.set_xscale('log')
    ax.set_xlabel('Active collaboration time (hours, log scale)')
    ax.set_ylabel('Tool-output error rate (\\%)')
    ax.grid(True, ls=':', lw=0.3)
    # Legend for difficulty
    for lbl, c in DIFF_COLORS.items():
        ax.scatter([], [], s=40, c=c, edgecolors='black', linewidths=0.5, label=lbl)
    ax.legend(title='Difficulty', loc='upper right', frameon=False)
    ax.set_title('Active time vs error density (bubble area $\\propto$ COBOL LOC)')
    plt.tight_layout()
    plt.savefig(FIGS/'errors_vs_time.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 5: Cost vs LOC (bubble = prompts)
# ------------------------------------------------------------------
def fig_cost_loc():
    xs, ys, labels, colors, sizes = [], [], [], [], []
    for p in PROJECTS:
        m = load_metrics(p)
        loc = m['inventory']['by_lang'].get('COBOL', {'loc':0})['loc']
        cost = m['cost_usd']
        prompts = m['user_prompts']['count']
        if loc == 0: loc = 1
        xs.append(loc); ys.append(cost); labels.append(p)
        colors.append(DIFF_COLORS[DIFF[p]['label']])
        sizes.append(max(30, prompts*4))
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for x, y, lbl, c, sz in zip(xs, ys, labels, colors, sizes):
        ax.scatter(x, y, s=sz, c=c, edgecolors='black', linewidths=0.5, alpha=0.85)
        ax.annotate(disp(lbl), (x,y), xytext=(4,4), textcoords='offset points',
                    fontsize=7)
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlabel('COBOL LOC produced (log scale)')
    ax.set_ylabel('API rack-rate cost upper bound (USD, log scale)')
    ax.grid(True, ls=':', lw=0.3)
    for lbl, c in DIFF_COLORS.items():
        ax.scatter([], [], s=40, c=c, edgecolors='black', linewidths=0.5, label=lbl)
    ax.legend(title='Difficulty', loc='upper left', frameon=False)
    ax.set_title('Compute cost vs COBOL output (bubble $\\propto$ user-prompt count)')
    plt.tight_layout()
    plt.savefig(FIGS/'cost_vs_loc.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 6: Error-tag composition per project (stacked)
# ------------------------------------------------------------------
def fig_error_tags():
    # Canonicalise tags.
    all_tags_set = []
    tags = {}
    for p in PROJECTS_BY_DIFF:
        m = load_metrics(p)
        et = m['errors']['error_tags'] or {}
        tags[p] = et
        for t in et: all_tags_set.append(t)
    preferred = ['cc','cobc','testfail','exit-nonzero','missing','segfault',
                 'busfault','abort','python','assert','perm','missing-cmd']
    tag_names = [t for t in preferred if any(tags[p].get(t,0)>0 for p in PROJECTS_BY_DIFF)]
    cmap = plt.get_cmap('Paired')(np.linspace(0,1,len(tag_names)))

    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    bot = np.zeros(len(PROJECTS_BY_DIFF))
    for t, c in zip(tag_names, cmap):
        vals = np.array([tags[p].get(t,0) for p in PROJECTS_BY_DIFF])
        ax.barh([disp(p) for p in PROJECTS_BY_DIFF], vals, left=bot, color=c, label=t,
                edgecolor='white', linewidth=0.3)
        bot += vals
    ax.set_xlabel('Error events (count)')
    ax.legend(loc='center left', bbox_to_anchor=(1.01, 0.5), frameon=False, ncol=1)
    ax.set_title('Failure signatures per project (sorted by difficulty)')
    plt.tight_layout()
    plt.savefig(FIGS/'error_tags.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 7: Intent typology (prompt typology) -- corpus total
# ------------------------------------------------------------------
def fig_intents():
    totals = {}
    for p in PROJECTS:
        m = load_metrics(p)
        for k, v in m['user_prompts']['intent_breakdown'].items():
            totals[k] = totals.get(k, 0) + v
    labels = ['initial-spec','clarify','redirect','bug-report','review-ask','resume','other']
    vals = [totals.get(l, 0) for l in labels]
    # Activity breakdown
    act = {}
    for p in PROJECTS:
        m = load_metrics(p)
        for k, v in m['user_prompts']['activity_breakdown'].items():
            act[k] = act.get(k, 0) + v
    act_labels = ['implement','test','spec','fix','build','port','optimize','doc','research','refactor','other']
    act_vals = [act.get(l, 0) for l in act_labels]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.4))
    c1 = plt.get_cmap('tab10')(np.linspace(0,0.9,len(labels)))
    ax1.bar(labels, vals, color=c1, edgecolor='black', lw=0.3)
    ax1.set_title(f'User-prompt intent ({sum(vals)} prompts)')
    ax1.tick_params(axis='x', rotation=40)
    for l in ax1.get_xticklabels(): l.set_ha('right')
    ax1.set_ylabel('Count')

    c2 = plt.get_cmap('tab10')(np.linspace(0,0.9,len(act_labels)))
    # Highlight refactor
    colors = []
    for l in act_labels:
        colors.append('#8b1a0e' if l=='refactor' else '#4C72B0')
    ax2.bar(act_labels, act_vals, color=colors, edgecolor='black', lw=0.3)
    ax2.set_title(f'First-prompt activity ({sum(act_vals)} prompts)')
    ax2.tick_params(axis='x', rotation=40)
    for l in ax2.get_xticklabels(): l.set_ha('right')
    # Annotate refactor
    if 'refactor' in act_labels:
        i = act_labels.index('refactor')
        ax2.text(i, act_vals[i]+1, str(act_vals[i]), ha='center', fontsize=8, color='#8b1a0e', weight='bold')
    plt.tight_layout()
    plt.savefig(FIGS/'intents.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 8: Active vs wall-clock gap (idle inflation)
# ------------------------------------------------------------------
def fig_active_vs_wall():
    projs = PROJECTS_BY_DIFF
    active_h = []
    wall_h   = []
    for p in projs:
        m = load_metrics(p)
        active_h.append(m['active_time']['total_active_s'] / 3600)
        # span from difficulty signals; use wall_duration_s summed across sessions
        wall_h.append(m['wall_duration_s'] / 3600)
    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    x = np.arange(len(projs))
    w = 0.4
    ax.bar(x - w/2, wall_h,   w, label='Wall-clock span (sum, incl.\ idle)', color='#9ecae1', edgecolor='black', lw=0.3)
    ax.bar(x + w/2, active_h, w, label='Active collaboration time',         color='#08519c', edgecolor='black', lw=0.3)
    ax.set_yscale('log')
    ax.set_xticks(x, [disp(p) for p in projs], rotation=30, ha='right')
    ax.set_ylabel('Hours (log scale)')
    ax.legend(frameon=False)
    ax.set_title('Wall-clock vs active time: most session span is idle')
    plt.tight_layout()
    plt.savefig(FIGS/'active_vs_wall.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 9: COBOL construct coverage heatmap (projects x statement class)
# ------------------------------------------------------------------
def fig_constructs():
    statements = ['MOVE','IF','PERFORM','STRING','COMPUTE','ADD','SUBTRACT',
                  'EVALUATE','EXIT','CALL','DISPLAY','ACCEPT','OPEN','CLOSE',
                  'READ','WRITE','UNSTRING','INSPECT','SEARCH','STOP']
    # Ordered by a capability ranking: data manip / arithmetic / control / I/O / interop.
    projs = list(PROJECTS_BY_DIFF)
    M = np.zeros((len(projs), len(statements)))
    for i, p in enumerate(projs):
        with open(OUT/'complexity'/f'{p}.json') as f:
            c = json.load(f)
        st = c['aggregate'].get('statements', {})
        for j, s in enumerate(statements):
            M[i, j] = st.get(s, 0)
    # Log-scale with +1 offset so zeros remain visible
    Mlog = np.log10(M + 1)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    im = ax.imshow(Mlog, aspect='auto', cmap='YlGnBu')
    ax.set_xticks(range(len(statements)), statements, rotation=55, ha='right')
    ax.set_yticks(range(len(projs)), [disp(p) for p in projs])
    # Annotate with raw counts
    for i in range(len(projs)):
        for j in range(len(statements)):
            v = int(M[i, j])
            if v > 0:
                txt = str(v) if v < 1000 else f'{v/1000:.1f}k'
                col = 'white' if Mlog[i, j] > Mlog.max()*0.55 else 'black'
                ax.text(j, i, txt, ha='center', va='center',
                        fontsize=6.5, color=col)
    cb = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.01)
    cb.set_label('log$_{10}$(count + 1)')
    ax.set_title('COBOL statement usage per project (PROCEDURE DIVISION verbs)')
    plt.tight_layout()
    plt.savefig(FIGS/'constructs.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 10: Rubric heatmap (projects x Q1..Q6), from output/assessments
# ------------------------------------------------------------------
def fig_rubric():
    import re
    criteria = ['Q1\ncorrectness','Q2\nbuild/run','Q3\ntests',
                'Q4\nrobustness','Q5\nmaintain','Q6\nrepro']
    keys = ['Q1','Q2','Q3','Q4','Q5','Q6']
    projs = list(PROJECTS_BY_DIFF)
    M = np.full((len(projs), 6), np.nan)
    n_bls = [None]*len(projs)
    authored = [False]*len(projs)
    for i, p in enumerate(projs):
        # Try subagent-harvested rubric first
        path = ROOT / 'output' / 'assessments' / f'{p}.md'
        if path.exists():
            txt = path.read_text()
            m = re.search(r"Mean score across (\d+) BLs and 6 criteria:\s*([0-9.]+|None)/2.*?"
                          r"Q1 corr\. ([0-9.]+|None),\s*Q2 build ([0-9.]+|None),\s*Q3 tests ([0-9.]+|None),\s*"
                          r"Q4 robust ([0-9.]+|None),\s*Q5 maintain ([0-9.]+|None),\s*Q6 repro ([0-9.]+|None)", txt)
            if m:
                n_bls[i] = int(m.group(1))
                vals = [m.group(j) for j in range(3, 9)]
                got = False
                for k, v in enumerate(vals):
                    try: M[i, k] = float(v); got = True
                    except: pass
                if got: continue
        # Fall back to author-calibrated
        if p in AUTHORED_RUBRIC:
            r = AUTHORED_RUBRIC[p]
            for k, ck in enumerate(keys):
                M[i, k] = r[ck]
            n_bls[i] = r['n_bl']
            authored[i] = True

    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    im = ax.imshow(M, aspect='auto', cmap='RdYlGn', vmin=0, vmax=2)
    ax.set_xticks(range(6), criteria)
    ylabels = []
    for i, p in enumerate(projs):
        mark = r'$^{\dagger}$' if authored[i] else ''
        if n_bls[i]:
            ylabels.append(f'{disp(p)}{mark} (n={n_bls[i]})')
        else:
            ylabels.append(f'{disp(p)}{mark}')
    ax.set_yticks(range(len(projs)), ylabels)
    for i in range(len(projs)):
        for j in range(6):
            v = M[i, j]
            if not np.isnan(v):
                ax.text(j, i, f'{v:.2f}', ha='center', va='center',
                        color=('white' if v < 0.8 else 'black'), fontsize=7)
            else:
                ax.text(j, i, '---', ha='center', va='center', color='gray', fontsize=8)
    cb = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.01, ticks=[0, 1, 2])
    cb.set_label('score (0--2)')
    ax.set_title('Per-project rubric: mean Q1--Q6 over backlog ($\\dagger$ = author-calibrated)')
    plt.tight_layout()
    plt.savefig(FIGS/'rubric.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 12: Feature-class distribution per project from KEY_FEATURES.md
# Classes: LNG (language), DOM (domain), ALG (algorithm), CMP (composition),
#          SYS (system), VER (verification), INF (infrastructure),
#          PRF (performance), PRO (protocol)
# ------------------------------------------------------------------
def fig_feature_classes():
    import re
    CLASSES = ['ALG','DOM','LNG','CMP','SYS','VER','PRF','PRO','INF']
    colors_cls = dict(zip(CLASSES, plt.get_cmap('tab10')(np.linspace(0, 0.9, len(CLASSES)))))
    projs = list(PROJECTS_BY_DIFF)
    # Pool depth*effort score per (project, primary class).
    M = np.zeros((len(projs), len(CLASSES)))
    for i, p in enumerate(projs):
        fp = ROOT / 'output' / 'backlogs' / p / 'KEY_FEATURES.md'
        if not fp.exists():
            continue
        txt = fp.read_text()
        for line in txt.splitlines():
            if not line.startswith('|'): continue
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) < 7: continue
            # Parse depth, effort, score
            try:
                score = float(cells[6].strip())
            except: continue
            # Primary class
            for cell in cells:
                cc = cell.replace('**','').replace('*','').strip()
                m2 = re.match(r'^([A-Z]{3,4})\b', cc)
                if m2 and m2.group(1) in CLASSES:
                    M[i, CLASSES.index(m2.group(1))] += score
                    break

    # Stacked horizontal bar by total depth*effort score
    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    left = np.zeros(len(projs))
    for j, cls in enumerate(CLASSES):
        vals = M[:, j]
        ax.barh([disp(p) for p in projs], vals, left=left, color=colors_cls[cls],
                label=cls, edgecolor='white', linewidth=0.3)
        for i, v in enumerate(vals):
            if v >= 4:
                ax.text(left[i] + v/2, i, f'{v:.0f}',
                        ha='center', va='center', fontsize=6.5,
                        color='white' if v >= 10 else 'black')
        left += vals
    ax.set_xlabel('Total feature score (depth $\\times$ (1 + effort $\\times$ 0.5), per project)')
    ax.legend(loc='lower right', ncol=2, fontsize=7, frameon=False,
              title='feature class')
    ax.set_title('Feature-kind significance per project (from KEY\\_FEATURES.md)')
    plt.tight_layout()
    plt.savefig(FIGS/'feature_classes.pdf'); plt.close()

# ------------------------------------------------------------------
# FIG 11: Verb-family view of COBOL construct usage per project
# ------------------------------------------------------------------
def fig_verb_families():
    FAMILIES = {
        'Data / movement':    ['MOVE','STRING','UNSTRING','INITIALIZE','INSPECT','SET'],
        'Arithmetic':          ['ADD','SUBTRACT','MULTIPLY','DIVIDE','COMPUTE'],
        'Control flow':        ['IF','PERFORM','EVALUATE','EXIT','STOP','GOBACK','GO'],
        'File / terminal I/O': ['OPEN','CLOSE','READ','WRITE','ACCEPT','DISPLAY','REWRITE','DELETE','START'],
        'Interop / subprogram':['CALL'],
    }
    projs = list(PROJECTS_BY_DIFF)
    # Totals per (project, family)
    M = np.zeros((len(projs), len(FAMILIES)))
    for i, p in enumerate(projs):
        with open(OUT/'complexity'/f'{p}.json') as f: c = json.load(f)
        st = c['aggregate'].get('statements', {})
        for j, (name, verbs) in enumerate(FAMILIES.items()):
            M[i, j] = sum(st.get(v, 0) for v in verbs)
    # stacked horizontal bar
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    cols = plt.get_cmap('tab10')(np.linspace(0, 1, len(FAMILIES)))
    left = np.zeros(len(projs))
    for j, (name, _) in enumerate(FAMILIES.items()):
        vals = M[:, j]
        ax.barh([disp(p) for p in projs], vals, left=left, color=cols[j], label=name,
                edgecolor='white', linewidth=0.3)
        # Annotate on each segment if big enough
        for i, v in enumerate(vals):
            if v > 60:
                ax.text(left[i] + v/2, i, f'{int(v)}', ha='center',
                        va='center', fontsize=6.5,
                        color='white' if v > 300 else 'black')
        left += vals
    ax.set_xlabel('PROCEDURE-DIVISION statement count (grouped)')
    ax.set_xscale('log')
    ax.set_xlim(1, max(left.max()*1.4, 10))
    ax.legend(loc='lower right', frameon=False, ncol=1, fontsize=7)
    ax.set_title('COBOL verb families deployed per project')
    plt.tight_layout()
    plt.savefig(FIGS/'verb_families.pdf'); plt.close()

if __name__ == '__main__':
    fig_difficulty()
    fig_se_tasks()
    fig_tool_use()
    fig_error_density()
    fig_cost_loc()
    fig_error_tags()
    fig_intents()
    fig_active_vs_wall()
    fig_constructs()
    fig_rubric()
    fig_verb_families()
    fig_feature_classes()
    print('Wrote', len(list(FIGS.glob('*.pdf'))), 'PDFs to', FIGS)
