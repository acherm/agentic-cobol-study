#!/usr/bin/env bash
# End-to-end pipeline: sessions → turns → complexity+git → features → metrics
# → difficulty → reports.
#
# ⚠ FROZEN INPUTS: as of 2026-06, 20 of 38 raw session logs have been deleted by
# Claude Code's 30-day local retention (see Appendix "Data provenance" / REPORT.md).
# `parse_sessions.py` and `deep_analyze.py` read those raw logs and SILENTLY SKIP
# missing files — re-running them would rebuild output/sessions_all.json and
# output/turns/ from only the 18 survivors, corrupting every token/cost/session
# aggregate. Treat output/sessions_all.json and output/turns/ as committed, frozen
# inputs. The downstream steps (metrics → difficulty → figures → reports) read
# those committed artifacts and are safe to re-run. To deliberately rebuild from
# raw anyway, run with REBUILD_FROM_RAW=1 (only valid before the logs were lost).
set -euo pipefail
REBUILD_FROM_RAW="${REBUILD_FROM_RAW:-0}"

cd "$(dirname "$0")/.."

PROJECTS=(
  chess-cobol-cc COBOL-chess
  cobol-compiler-cc cobol-compiler-codex
  cobol-compress-codex cobol-compress-cobolcc
  cobol-doom-cc cobol-doom-codex
  cobol-jb-cc cobol-jb-codex
  COBOL-pygame cobol-pygame-cc
  SATCobol-codex SATCobol-cc
  cobol-tictactoe game15-cobol-codex
)

mkdir -p output output/turns output/complexity output/git output/features \
         output/metrics output/reports output/assessments output/backlogs

echo "[1/8] parse sessions"
if [[ "$REBUILD_FROM_RAW" != "1" && -s output/sessions_all.json ]]; then
  echo "      [skip] using committed output/sessions_all.json (frozen; 20/38 raw logs deleted)."
  echo "             set REBUILD_FROM_RAW=1 to override (will drop deleted sessions)."
else
  python3 scripts/parse_sessions.py --project-filter cobol --out output/sessions_all.json
fi

echo "[2/8] project file inventory"
python3 scripts/analyze_projects.py \
  --sessions output/sessions_all.json \
  --out output/projects.json \
  --projects "${PROJECTS[@]}"

echo "[3/8] deep turn analysis"
python3 scripts/deep_analyze.py \
  --sessions-json output/sessions_all.json \
  --out-dir output/turns

echo "[4/8] COBOL construct detection + git"
for p in "${PROJECTS[@]}"; do
  python3 scripts/cobol_complexity.py --project-root "$HOME/SANDBOX/$p" --out "output/complexity/$p.json" 2>/dev/null
  python3 scripts/git_stats.py        --project-root "$HOME/SANDBOX/$p" --out "output/git/$p.json" 2>/dev/null
done

echo "[5a/8] harvest existing backlogs"
python3 scripts/harvest_backlogs.py \
  --out-dir output/backlogs \
  --projects "${PROJECTS[@]}"

echo "[5b/8] emit per-project analyst prompts"
python3 scripts/emit_analyst_prompts.py \
  --sessions-json output/sessions_all.json \
  --out-dir prompts/per-project \
  --backlogs-root output/backlogs \
  --projects "${PROJECTS[@]}"

echo "[5c/8] feature ledger (mines both project roots and output/backlogs/)"
python3 scripts/feature_ledger.py \
  --turn-dir output/turns --git-dir output/git \
  --backlogs-dir output/backlogs \
  --out-dir output/features \
  --projects "${PROJECTS[@]}"

echo "[6/8] project metrics"
python3 scripts/project_metrics.py \
  --sessions-json output/sessions_all.json \
  --projects-json output/projects.json \
  --turn-dir output/turns \
  --complexity-dir output/complexity \
  --git-dir output/git \
  --features-dir output/features \
  --out-dir output/metrics \
  --projects "${PROJECTS[@]}"

echo "[7/8] difficulty index"
python3 scripts/difficulty.py --metrics-dir output/metrics --out output/difficulty.json

echo "[7b/8] domain coverage"
python3 scripts/domain_coverage.py \
  --sessions-json output/sessions_all.json \
  --projects "${PROJECTS[@]}" \
  --out output/domain_coverage.md

echo "[7c/8] token-level cost metrics"
python3 scripts/cost_metrics.py \
  --sessions-json output/sessions_all.json \
  --metrics-dir output/metrics \
  --projects "${PROJECTS[@]}" \
  --out-csv output/cost_metrics.csv \
  --out-md  output/cost_metrics.md

echo "[7d-pre/8] key-features rollup (parses per-project KEY_FEATURES.md)"
python3 scripts/key_features_rollup.py \
  --backlogs-dir output/backlogs \
  --projects "${PROJECTS[@]}" \
  --out-md output/key_features_summary.md || echo "(no per-project KEY_FEATURES.md found — skipping)"

echo "[7d/8] context length + compaction analysis"
# ⚠ FROZEN like stage 1: context series need per-turn token usage from RAW logs.
# 20/38 raws are purged — re-running would rewrite context_summary.csv/md from
# the surviving raws only, silently dropping rows for the lost sessions.
# Set REBUILD_CONTEXT=1 to run anyway (e.g., scoped experiments with custom outs).
if [[ "${REBUILD_CONTEXT:-0}" == "1" ]]; then
  mkdir -p output/context
  python3 scripts/context_analysis.py \
    --sessions-json output/sessions_all.json \
    --out-series-dir output/context \
    --out-csv output/context_summary.csv \
    --out-md  output/context_analysis.md \
    --projects "${PROJECTS[@]}"
else
  echo "      [skip] frozen (June 4 outputs kept; REBUILD_CONTEXT=1 to override)"
fi

echo "[8a/8] render per-project reports"
python3 scripts/generate_project_reports.py \
  --metrics-dir output/metrics \
  --difficulty-json output/difficulty.json \
  --out-dir output/reports \
  --projects "${PROJECTS[@]}"

echo "[8b/8] render per-project calibrated assessments"
python3 scripts/generate_assessments.py \
  --metrics-dir output/metrics \
  --backlogs-dir output/backlogs \
  --difficulty-json output/difficulty.json \
  --out-dir output/assessments \
  --projects "${PROJECTS[@]}"

echo "[8c/8] render top-level report"
python3 scripts/generate_report.py \
  --projects output/projects.json \
  --metrics-dir output/metrics \
  --reports-dir output/reports \
  --out REPORT.md

echo "Done. Top-level REPORT.md + per-project output/reports/*.md"
