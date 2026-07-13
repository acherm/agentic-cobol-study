#!/usr/bin/env python3
"""Aggregate per-project KEY_FEATURES.md into a cross-project table.

Each `output/backlogs/<project>/KEY_FEATURES.md` is expected to follow the
structure defined in `prompts/significance-taxonomy.md`: a `## Significance
profile` table (one row per class) + a `## Verdict` line. This script parses
those sections across all projects and emits a cross-project summary.

Column labels differ slightly across projects (subagents aren't perfectly
consistent), but every table matches the same regex: a markdown row with
the class code in the first column and the first integer in any cell that
follows.
"""
import argparse, os, re, sys
from collections import defaultdict

CLASSES = ["ALG","DOM","SYS","INF","PRO","LNG","VER","PRF","CMP"]
CLASS_DESC = {
    "ALG": "Algorithm",
    "DOM": "Domain modelling",
    "SYS": "System integration / FFI",
    "INF": "Infrastructure / tooling",
    "PRO": "Protocol compliance",
    "LNG": "Language-level achievement",
    "VER": "Correctness verification",
    "PRF": "Performance engineering",
    "CMP": "Emergent composition",
}

# Match a markdown row whose first non-empty cell is a class code, then
# capture the first integer in any later cell.
ROW_RE = re.compile(
    r"^\s*\|\s*\**\s*([A-Z]{3})\s*(?:\([^)]*\))?\s*\**\s*\|"
    r"[^|]*?(\d+)",
    re.M,
)
VERDICT_RE = re.compile(
    r"^#{2,3}\s*(?:\d+\.\s*)?Verdict\s*\n+(.+?)(?:^#|\Z)",
    re.M | re.S | re.I,
)


def parse_one(path):
    """Return dict: {class_code: count, 'verdict': str, 'n_top_features': int}."""
    with open(path) as f:
        text = f.read()
    # Locate the "## [N.] Significance profile" heading and read until next H2
    m = re.search(r"^##\s*(?:\d+\.\s*)?Significance profile\b", text, re.M | re.I)
    section = text[m.start():] if m else ""
    nxt = re.search(r"^##\s", section[1:], re.M)
    if nxt:
        section = section[:nxt.start()+1]
    counts = {c: 0 for c in CLASSES}
    for cm in ROW_RE.finditer(section):
        cls = cm.group(1)
        if cls in counts:
            counts[cls] = max(counts[cls], int(cm.group(2)))
    n_top = sum(counts.values())

    # Verdict
    verdict = ""
    vm = VERDICT_RE.search(text)
    if vm:
        body = vm.group(1).strip()
        # first non-empty meaningful sentence (drop bold marker, quote chars)
        verdict = re.sub(r"\s+", " ", body).strip()[:400]

    # Identify dominant classes: top-2 by count
    ranked = sorted(counts.items(), key=lambda kv: -kv[1])
    dominant = [c for c, n in ranked if n > 0][:3]
    return {
        "counts": counts,
        "verdict": verdict,
        "n_top_features": n_top,
        "dominant": dominant,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backlogs-dir", required=True)
    ap.add_argument("--projects", nargs="+", required=True)
    ap.add_argument("--out-md", required=True)
    args = ap.parse_args()

    per_project = {}
    for p in args.projects:
        fp = os.path.join(args.backlogs_dir, p, "KEY_FEATURES.md")
        if not os.path.exists(fp):
            print(f"[skip] {p}: no KEY_FEATURES.md", file=sys.stderr); continue
        per_project[p] = parse_one(fp)
        d = per_project[p]
        print(f"[{p}] top={d['n_top_features']} dom={d['dominant']}", file=sys.stderr)

    L = []; E = L.append
    E("## Feature classification — significance profile per project")
    E("")
    E("Every project's top 8–12 features are classified by a 9-class taxonomy "
      "(see [`prompts/significance-taxonomy.md`](prompts/significance-taxonomy.md) "
      "for definitions) in "
      "[`output/backlogs/<project>/KEY_FEATURES.md`](output/backlogs/). "
      "The table below shows the count of top-features that fall in each class, per project. "
      "**Dominant** = the two or three classes with the highest counts — where the project "
      "actually spends its engineering weight.")
    E("")
    E("Classes: "
      "`ALG` algorithm · "
      "`DOM` domain modelling · "
      "`SYS` system integration / FFI · "
      "`INF` infrastructure · "
      "`PRO` protocol compliance · "
      "`LNG` language-level achievement · "
      "`VER` verification · "
      "`PRF` performance engineering · "
      "`CMP` emergent composition.")
    E("")
    # Header with class codes
    E("| Project | Top | " + " | ".join(CLASSES) + " | Dominant |")
    E("|---|---:|" + "|".join([":---:"]*len(CLASSES)) + "|---|")
    # Sort by n_top_features desc for readability
    ordered = sorted(per_project.items(), key=lambda kv: -kv[1]["n_top_features"])
    for p, d in ordered:
        cells = []
        for c in CLASSES:
            n = d["counts"].get(c, 0)
            cells.append(f"**{n}**" if n == max(d["counts"].values()) and n > 0 else (str(n) if n else "—"))
        dom = " + ".join(d["dominant"]) if d["dominant"] else "—"
        E(f"| `{p}` | {d['n_top_features']} | " + " | ".join(cells) + f" | **{dom}** |")
    E("")

    # Per-class cross-project roll-up
    E("### Class → projects where it is dominant")
    E("")
    by_class = defaultdict(list)
    for p, d in per_project.items():
        if d["dominant"]:
            top = d["dominant"][0]
            by_class[top].append(p)
    E("| Class | Description | Projects where this class leads |")
    E("|---|---|---|")
    for c in CLASSES:
        ps = by_class.get(c, [])
        desc = CLASS_DESC[c]
        E(f"| `{c}` | {desc} | {', '.join(f'`{p}`' for p in ps) if ps else '—'} |")
    E("")

    # Grand totals
    E("### Cross-project totals")
    E("")
    totals = {c: sum(d["counts"].get(c, 0) for d in per_project.values()) for c in CLASSES}
    grand = sum(totals.values())
    E("| Class | Total top-feature count across projects | Share |")
    E("|---|---:|---:|")
    for c in CLASSES:
        share = (100 * totals[c] / grand) if grand else 0
        E(f"| `{c}` {CLASS_DESC[c]} | {totals[c]} | {share:.1f}% |")
    E(f"| **Total top-features ranked** | **{grand}** | 100.0% |")
    E("")

    # Verdicts
    E("### Verdicts at a glance")
    E("")
    E("| Project | Verdict (auto-extracted from `KEY_FEATURES.md`) |")
    E("|---|---|")
    for p, d in sorted(per_project.items()):
        verdict = d["verdict"] or "_(no verdict sentence found)_"
        # trim to one sentence
        v = re.split(r"(?<=[.!?])\s", verdict, maxsplit=1)[0]
        v = v.replace("|","\\|")
        if len(v) > 260: v = v[:260] + "…"
        E(f"| `{p}` | {v} |")
    E("")

    # Caveat
    E("_Numbers above are parsed from the `## Significance profile` tables inside "
      "each `KEY_FEATURES.md`. Column semantics (primary vs primary+secondary) varies "
      "slightly across projects — the parser always takes the **first integer** of "
      "each row, which corresponds to the primary-class count. For the nuance, see "
      "the individual per-project files._")
    E("")
    with open(args.out_md, "w") as f:
        f.write("\n".join(L) + "\n")
    print(f"[ok] {args.out_md}", file=sys.stderr)


if __name__ == "__main__":
    main()
