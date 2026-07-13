# Raw session transcripts — archival snapshot

This folder preserves the **raw agent session transcripts** that the meta-analysis
was derived from, so the study keeps its raw provenance even after the source
files disappear from `~/.claude/` and `~/.codex/`.

## Why this exists

The pipeline reads transcripts live from:
- Claude Code: `~/.claude/projects/<encoded-project>/<session_id>.jsonl`
- Codex: `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-*.jsonl`

Claude Code deletes `~/.claude/projects/*.jsonl` automatically after
`cleanupPeriodDays` (default **30 days**, not overridden on this machine), keyed
on file mtime. By **2026-06-04**, that auto-cleanup had already purged **20 of the
21 Claude Code transcripts** in this study (every one past its 30-day window). The
only Claude Code survivor was the still-active `cobol-meta-analysis` session, which
was itself ~8 days from being purged. All 17 Codex transcripts survived because
`~/.codex/` is not subject to Claude Code's cleanup.

## Contents

- `raw_transcripts.tar.gz` — the **18 transcripts still on disk on 2026-06-04**
  (1 Claude Code + 17 Codex), named `<project>__<agent>__<session_id>.jsonl`,
  matching the convention in `output/turns/`. 134 MB raw → ~35 MB compressed.
- `MANIFEST.csv` — **all 38 sessions** in the study, each marked `archived`
  (raw file captured here) or `LOST (auto-cleanup)` (raw file already gone;
  only the derived artifacts below survive).

## What survives for the 20 lost sessions

Their raw transcripts are **unrecoverable** (no copy on disk or in git history), but
the committed derived artifacts capture ~98.5% of their content:
- `output/sessions_all.json` — session-level metrics for all 38.
- `output/turns/*.jsonl` — per-turn record (`deep_analyze.py`), keeping 4000 chars
  per message / 2000 per tool I/O. Across the 20 lost sessions: 16,359 turns
  preserved, only 241 (1.5%) clipped beyond those caps.
- `output/context/*.json`, `output/metrics/`, `output/reports/`, and the rest of `output/`.

What is **not** recoverable for those 20: verbatim text beyond the per-turn caps
(241 turns), and the ability to re-extract any field the pipeline did not already compute.

## To extract the archive

```sh
mkdir -p /tmp/raw && tar -xzf raw_transcripts.tar.gz -C /tmp/raw
```
