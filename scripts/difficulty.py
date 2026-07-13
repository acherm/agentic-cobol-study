#!/usr/bin/env python3
"""Compute a cross-project difficulty index from per-project metrics.

Difficulty is a latent construct; we approximate it with a rank-average of
seven observable signals that are each monotonically associated with "hard":

  1. active_hours                    (more active time = harder)
  2. span_days                       (more days to come back = harder)
  3. user_prompts                    (more interventions = harder)
  4. redirect_bug_prompts            (more user corrections = harder)
  5. error_rate                      (more tool errors = harder)
  6. fix_cycles                      (more error→edit retries = harder)
  7. fix_time_share                  (bigger slice of work was bug-fixing = harder)

For each project we compute the rank of each signal (1 = smallest), take the
mean rank, normalize to [0,1], and bucket into four labels by quartile.

Outputs:
  output/difficulty.json : {project: {signals, ranks, mean_rank, index, label}}
"""
import argparse, json, os, sys
from statistics import mean

SIGNALS = [
    "active_hours", "span_days", "user_prompts", "redirect_bug_prompts",
    "error_rate", "fix_cycles", "fix_time_share",
]

LABELS = ["Low", "Medium", "High", "Very-High"]


def rank(vals):
    """Return 1-based ranks (ties averaged, larger = higher rank)."""
    idx = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[idx[j + 1]] == vals[idx[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[idx[k]] = avg
        i = j + 1
    return ranks


def bucket(x, n_buckets=4):
    """Bucket a value in [0,1] into 0..n_buckets-1 by quartile."""
    if x < 0.25: return 0
    if x < 0.50: return 1
    if x < 0.75: return 2
    return 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics-dir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    projs = []
    sigs = {s: [] for s in SIGNALS}
    for fn in sorted(os.listdir(args.metrics_dir)):
        if not fn.endswith(".json"): continue
        with open(os.path.join(args.metrics_dir, fn)) as f:
            m = json.load(f)
        proj = m["project"]
        d = m.get("difficulty_signals") or {}
        projs.append((proj, d))
        for s in SIGNALS:
            sigs[s].append(d.get(s, 0) or 0)

    # ranks per signal
    ranks_per_signal = {s: rank(sigs[s]) for s in SIGNALS}

    out = {}
    for i, (proj, d) in enumerate(projs):
        ranks = {s: ranks_per_signal[s][i] for s in SIGNALS}
        mean_rank = mean(ranks.values())
        # normalize to [0,1]
        index = (mean_rank - 1) / (len(projs) - 1) if len(projs) > 1 else 0.5
        lab = LABELS[bucket(index)]
        out[proj] = {
            "signals": d,
            "ranks": ranks,
            "mean_rank": round(mean_rank, 2),
            "index": round(index, 3),
            "label": lab,
        }

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    # Print a small ranking summary
    ranked = sorted(out.items(), key=lambda x: -x[1]["index"])
    print("Project difficulty ranking (highest first):", file=sys.stderr)
    for p, v in ranked:
        print(f"  {v['label']:10s} idx={v['index']:.2f} mean_rank={v['mean_rank']:.1f}  {p}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
