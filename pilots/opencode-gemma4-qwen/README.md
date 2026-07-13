# Pilot P1/P2 — OpenCode CLI with Gemma 4 26B-A4B (local) and Qwen 3.6-plus (hosted free tier)

Two exploratory pilot sessions (April 4–6, 2026) on the corpus's easiest domain family
(Game of 15 — number-picking game isomorphic to tic-tac-toe; **not** the sliding 15-puzzle),
run with the **OpenCode CLI** (not Claude Code). Copied verbatim from
`~/SANDBOX/gemma4-test/` on 2026-07-07 for preservation; the original directory has no git history.

## Sessions

| File | Model (per-turn tag in export) | Serving | Window | Outcome |
|---|---|---|---|---|
| `session-ses_2a67.md` | Gemma 4 (local) — config id `google/gemma-4-26b-a4b`, logged under LM Studio placeholder `YOUR_LM_STUDIO_MODEL_ID` | local, LM Studio @ `127.0.0.1:1234/v1` | 2026-04-04 19:24 → 20:17 (~53 min; first turn alone ≈35 min) | **Failure**: 15 `cobc` invocations, 231 error lines, 0 successful compiles; hallucinated non-COBOL constructs (function-style paragraph calls, `PASS.`), corrupted tokens (`PROCEDCR PROCEDURE DIVISION.`); fabricated results ("1344", later "44,360" via an *unrun* Python fallback); abandoned COBOL |
| `session-ses_2a64.md` | `qwen3.6-plus-free` (hosted free tier; from a global OpenCode config not in this folder) | API | 2026-04-04 20:19 → 2026-04-06 01:18 (~29 h span, mostly idle; ≈64 min agent time + one empty 16,410 s turn) | **Mixed**: base Game-of-15 suite correct — `255168` total / `31896` unique (matches the corpus oracle); Game-of-N generator repeatedly emitted invalid COBOL (`duplicate OCCURS clause`, …), "Game of 21" never compiled in-session; ended stalled after 7 bare "retry" prompts |

OpenCode Markdown exports record per-turn wall-clock only — **no token or cost logging**.

## Provenance caveats (bind any use in the paper)

1. The `ses_2a64` export starts mid-work: the authoring of the working base `game15.cob`
   happened in an earlier **unlogged** session — which model wrote it, and at what iteration
   cost, cannot be attributed from these logs.
2. The working `game21` binary and clean `21.cob` in the original folder are timestamped
   2026-04-07, **after** the last logged activity; their successful build is not attributable
   to either model. They are included here for completeness only.
3. Gemma quantization/build is unrecorded (LM Studio placeholder id).
4. Two build environments were used: native macOS arm64 and a Debian/GnuCOBOL 4 Docker
   container (`Dockerfile`).
5. The `.c/.c.h/.c.l.h/.i` files in the original folder are GnuCOBOL `cobc -C` build
   artifacts (generated code), not model-written C; they are not copied here.

## Contents

- `opencode.json` — OpenCode provider config (LM Studio local, Gemma 4 26B-A4B).
- `Dockerfile` — Debian bookworm + gnucobol4 build container.
- `session-ses_2a67.md`, `session-ses_2a64.md` — full OpenCode session exports.
- `game15.cob`, `game015.cob`, `015.cob`, `21.cob`, `game15_tree.cob`, `game015_tree.cob`,
  `game15_avoid.cob`, `game015_avoid.cob` — COBOL sources present in the pilot folder
  (see caveats 1–2 for attribution limits).
- `game15_tree.txt`, `game15_avoid_tree.txt` — generated game-tree analyses
  (root: 255,168 terminal games).
- `game_n_generator.py` — the Game-of-N variant generator whose COBOL-emitting template
  was the failing final task of `ses_2a64`.
