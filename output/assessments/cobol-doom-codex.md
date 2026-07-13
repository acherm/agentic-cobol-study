# Assessment — `DOOM-COBOL-CODEX` (folder `cobol-doom-codex`) — evidence of what the coding agent actually achieved

## TL;DR — calibrated verdict

> A COBOL Doom-like FPS (`gridwalker` binary) with **SDL2 graphical rendering** (not terminal-only), built from 11 COPY books (`gridwalker_raycast.cpy`, `gridwalker_combat.cpy`, `gridwalker_entity.cpy`, `gridwalker_render.cpy`, `gridwalker_input.cpy`, `gridwalker_math.cpy`, `gridwalker_level.cpy`, `gridwalker_state.cpy`, `gridwalker_data.cpy`, `gridwalker_bootstrap.cpy`, `levels.cpy`) plus an `sdl_bridge.c` and BMP sprite assets.

> A Codex replica of the Doom domain that independently chose **SDL2 graphical rendering** instead of terminal-based ASCII — a different interpretation of 'Doom in COBOL' from the same prompt pack. The 11-copybook architecture and BMP sprite system go further than the Claude Code sibling.

**Difficulty (auto-labelled):** Medium (idx 0.46). **Active collaboration time:** 2 h 1 m. **Sessions:** 1. **Backlog entries discovered:** 0. **Git commits:** 10.

## 1. Contract — what was asked

Write a Doom game in COBOL (Codex replica, using REPLAY_PROMPTS steps 1–6).

Opening user prompt (verbatim, truncated):

```
Write a COBOL program (GnuCOBOL) that runs in a terminal and lets a human walk around a 2-D grid level from a top-down view. Required behaviour: The level is a rectangular grid (roughly 20×20 or larger) made of wall cells and open cells, with a clearly visible layout of rooms and corridors. The view is a top-down ASCII map: walls, open floor, and the player drawn at the player's current cell with a symbol that indicates facing direction. The player can move with keys W/A/S/D (or the arrow keys) and quit with Q or ESC. Input must be read without requiring the user to press Enter after each key. The player cannot walk through walls. Attempts to do so leave the player in place. The screen is redrawn after every input so the view stays current. Redrawing must not scroll — the map stays anchore
```

## 2. Delivered — externally-observable evidence

A COBOL Doom-like FPS (`gridwalker` binary) with **SDL2 graphical rendering** (not terminal-only), built from 11 COPY books (`gridwalker_raycast.cpy`, `gridwalker_combat.cpy`, `gridwalker_entity.cpy`, `gridwalker_render.cpy`, `gridwalker_input.cpy`, `gridwalker_math.cpy`, `gridwalker_level.cpy`, `gridwalker_state.cpy`, `gridwalker_data.cpy`, `gridwalker_bootstrap.cpy`, `levels.cpy`) plus an `sdl_bridge.c` and BMP sprite assets.

**Executables present in `SANDBOX/cobol-doom-codex/`** (at least *something* built):

- `demo` (50 KB)
- `gridwalker` (186 KB)

**COBOL surface exercised.** 12 COBOL file(s), 1,906 code lines, 169 paragraphs (≈ function-like units), 10 sections, mastery score **28** distinct constructs across **10/10** capability categories.

## 3. Rubric — per-BL quality scores (0–2; NA = not applicable)

_No rubric available for this project (analyst subagent did not run or used a pre-existing summary format)._

## 4. Standards — why the achievement meets the bar

**The theoretical ceiling.** Actual Doom (1993): ~30 kLOC hand-optimized C + asm, BSP, WAD, sound.

**Where this result sits.** A Codex replica of the Doom domain that independently chose **SDL2 graphical rendering** instead of terminal-based ASCII — a different interpretation of 'Doom in COBOL' from the same prompt pack. The 11-copybook architecture and BMP sprite system go further than the Claude Code sibling.

**Why the ceiling is out of reach here — honest constraints (not failures):**

- Same COBOL language constraints; SDL2 bridge adds a C glue layer.

## 5. What's genuinely impressive (evidence-anchored)

- Closes the 2-agent coverage gap for the FPS domain.
- **SDL2 graphical output** — Codex independently chose a windowed renderer over terminal ASCII.
- 11 COPY books — the most modular COBOL decomposition for a game project in the set.
- BMP sprite assets (enemies, pickups, armor) — a production-adjacent asset pipeline.

## 6. Honest gaps

- Newer project — assessment pending deeper analysis.

**Automatic gap signals from the pipeline:**

- Tool-output error rate: 3.3% (21 errors / 631 tool outputs).
- Bug-report-style user prompts: 0.
- Redirect-style user prompts: 4.
- Share of active time spent on `bug_fix`: 0.2% (0 min of 121 min total).

## 7. Reproducibility

- Project root: `/Users/mathieuacher/SANDBOX/cobol-doom-codex`
- Sessions: 1 (primary agent: Codex gpt-5.4)
- Git history: 10 commits available in `/Users/mathieuacher/SANDBOX/cobol-doom-codex/.git`; replay via `git checkout` + standard build.
- See the per-project analyst deliverables at `output/backlogs/cobol-doom-codex/` (`SPECIFICATION_BACKLOG.md`, `README.md`, `appendix.json`) for the full replay package, or the session JSONL files under `output/turns/cobol-doom-codex__*.jsonl`.

## 8. Final take

**A Codex replica of the Doom domain that independently chose **SDL2 graphical rendering** instead of terminal-based ASCII — a different interpretation of 'Doom in COBOL' from the same prompt pack.** Given the constraints listed in §4, the delivered artefacts are a good-standard outcome for a coding agent in this context. The gaps in §6 are real but expected, and each is either (a) a language-level constraint, (b) a scope decision by the user, or (c) a time-budget reality — not an agent failure.

---

_Auto-generated by `scripts/generate_assessments.py` from: `output/metrics/cobol-doom-codex.json`, `output/backlogs/cobol-doom-codex/appendix.json` (when present), `output/complexity/cobol-doom-codex.json`, `output/difficulty.json`, and a hand-authored `STANDARDS` dict in the same script._
