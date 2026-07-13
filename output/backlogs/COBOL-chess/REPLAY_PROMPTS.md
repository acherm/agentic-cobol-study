# Replay Prompts

Reusable prompts for reproducing the `cobochess` project step by step. Each prompt is self-contained enough to copy-paste into a coding agent session. They specify **what** to build (behavior, inputs, outputs, verification), not **how** (no algorithm names, no data-structure prescriptions, no COBOL-specific idioms — the board representation, move encoding, search techniques and evaluation terms are all the agent's to choose).

Use them sequentially: each step builds on the previous one. The end state is a COBOL-built chess engine binary `cobochess` that (1) loads any position from FEN, (2) generates **only legal** moves, (3) reproduces known **perft** node counts exactly from the start position and a handful of standard test positions, (4) speaks enough **UCI** to be driven by `cutechess-cli`, and (5) plays measurable games against a strength-limited **Stockfish** so its Elo can be estimated with a confidence interval (target ~1600 Elo). The reproduction oracle for *correctness* is perft node counts and move legality; the oracle for *strength* is the Stockfish/Elo match harness.

For reference on what was actually built (board representation chosen, search techniques in the order they were added, the Elo ladder from ~675 to ~1635, and the autonomous decisions along the way), see [SPECIFICATION_BACKLOG.md](SPECIFICATION_BACKLOG.md).

> **How to read this replay.** `cobochess` was built *objective-first*, not
> spec-first: after the initial plan, the session became an exploratory,
> human-steered loop chasing a moving target — playing strength — interleaved with
> reactive toolchain debugging. The steps below are an **idealized linearization**
> of that process: a faithful recipe for the *end state*, not a transcript of how
> it unfolded. Step 7 is marked **`[objective loop]`** — you iterate until a
> stopping oracle (an Elo target) is met, and the number of iterations, and whether
> the target is reached at all, is **not deterministic**: a fresh agent may plateau
> at a different strength. The actual ordered human interventions are preserved
> verbatim at the end, under [*What actually happened*](#what-actually-happened-the-real-session-trace).

---

## Step 1: Scaffold + Board Model + FEN Loader

> Start a fresh workspace. Build a chess engine in COBOL (GnuCOBOL, `cobc -x -free`, free-format). This first milestone is the project skeleton plus the ability to load and round-trip an arbitrary chess position.
>
> Produce a build that emits a single binary `bin/cobochess`. Provide a `Makefile` with at least `build`, `perft`, `uci-smoke`, `clean`, and `rebuild` targets, plus a `README.md` and a `.gitignore`. Lay out the tree with separate directories for COBOL sources, shared copybooks/includes, test fixtures, and tooling.
>
> The engine must internally represent a full chess position: the 64-square board, side to move, castling rights, en-passant target square, and the half-move and full-move clocks. Add a FEN loader: given any of the six-field FEN strings, the engine must populate that position exactly — piece placement, side to move, castling availability (`KQkq` / `-`), en-passant square (algebraic ↔ internal index), and both clocks. Loading an invalid FEN must be reported as an error, not silently accepted.
>
> Expose two command-line modes for later correctness work (they will be fleshed out in Step 3):
> - `./bin/cobochess --perft "<FEN>" <depth>`
> - `./bin/cobochess --perft-startpos <depth>`
>
> Verification:
> - `make build` produces a runnable `bin/cobochess`.
> - Loading the start-position FEN (`rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`) reconstructs the standard starting array, white to move, all four castling rights, no en-passant square.
> - Loading a position with an en-passant target (e.g. after `1. e4`, the FEN ending `... w KQkq e3 0 1`) records the correct en-passant square; loading one with partial castling rights (e.g. `Kq`) records exactly those.
> - An ill-formed FEN (wrong field count, bad rank length) is rejected with a non-zero exit / error status rather than producing a corrupt position.

---

## Step 2: Legal Move Generation + Make/Unmake

> Add full legal move generation for the position loaded in Step 1. Generate every move that is legal under the rules of chess and no illegal move — this includes the awkward cases:
> - pawn single and double pushes, diagonal captures, **en passant** captures, and **promotion** to all four piece types (on both quiet pushes and captures);
> - knight, bishop, rook, queen and king moves;
> - **castling** king-side and queen-side for both colours, permitted only when the right is still held, the squares between king and rook are empty, the rook is on its home square, the king is not currently in check, and the king does not pass over or land on an attacked square;
> - exclusion of any move that would leave the moving side's own king in check.
>
> Provide a way to apply a move to the position and then take it back, restoring the previous position exactly (board, castling rights, en-passant square, both clocks, side to move). Make/unmake must round-trip perfectly so the move generator can be used recursively.
>
> How you decide legality (filtering pseudo-legal moves vs. generating strictly legal moves), how you detect that a square is attacked, and how you encode a move are all your choice.
>
> Verification:
> - From the start position the generator yields exactly **20** legal moves; from the standard "Kiwipete" position (`r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1`) it yields exactly **48**.
> - Apply-then-undo on every generated move from several positions returns the position to a byte-identical state (assert the post-undo FEN equals the original FEN).
> - A position where en passant would expose the king to check does **not** include that en-passant capture among the legal moves.
> - Castling is offered only when all of its preconditions hold, and is omitted (for that side/wing) when the king would pass through an attacked square.

---

## Step 3: Perft Correctness Harness

> Wire up the two CLI perft modes from Step 1 so that `--perft "<FEN>" <depth>` and `--perft-startpos <depth>` each run a recursive move-count (count the leaf nodes of the legal move tree to the given depth) and print the node count in a stable, machine-readable form (e.g. `nodes=<N>`). A parse error must exit non-zero.
>
> Add a perft regression suite: a small data file of `(FEN, depth, expected-nodes)` cases covering at least the start position, the Kiwipete position, an en-passant-edge position, and a promotion-heavy position, each taken to a useful depth. Add a checker (a script under the tooling directory, wired as `make perft`) that runs the engine on every case and compares the produced node count against the expected value, failing loudly on any mismatch.
>
> Verification — these are the canonical perft node counts; every one must match exactly:
> - **Start position:** depth 1 = 20, depth 2 = 400, depth 3 = 8 902, depth 4 = 197 281, depth 5 = 4 865 609.
> - **Kiwipete** (`r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1`): depth 1 = 48, depth 2 = 2 039, depth 3 = 97 862.
> - The en-passant-edge and promotion fixtures match their pre-known counts to the chosen depth.
> - `make perft` runs the whole suite and reports every case `[OK]`; a single mismatch makes the target fail. This suite is the regression gate — no later move-generator change is acceptable unless `make perft` still passes.

---

## Step 4: Evaluation, Search, and `bestmove`

> Make the engine *choose* moves. Add a static evaluation of a position (a numeric score, positive for the side to move) and a search that, given a position and a depth or time budget, returns a single best move plus a score.
>
> Requirements on observable behaviour (the internal search technique and evaluation terms are yours):
> - Searching deeper must not change the legality of the move returned: the chosen move is always one of the legal moves from Step 2.
> - The engine must correctly recognise terminal positions: report a forced mate (no legal moves while in check) and a draw by stalemate (no legal moves while not in check). It should also treat the fifty-move and repetition draw conditions as draws during search.
> - A search to a fixed depth on the start position must complete and return a sensible opening move; a search on a position with a one-move mate must find that mate.
> - During search, emit progress in UCI `info` form at least once per completed depth: `info depth <D> nodes <N> score cp <S> pv <move ...>`.
>
> Verification:
> - On a "mate in one" position the engine returns the mating move and reports a mate/very-large score.
> - On a stalemate position the engine reports no legal move (and does not crash or return an illegal move).
> - Repeated searches of the start position at the same depth are deterministic and return a legal first move.
> - Node counts reported in `info` lines grow monotonically with depth, and total search time stays bounded by the requested budget.

---

## Step 5: UCI Protocol + Time Management

> Wrap the search in a UCI command loop so the engine can be driven by a GUI or by `cutechess-cli`. With no CLI flags, `./bin/cobochess` must read UCI commands from stdin and respond on stdout. Support at minimum:
> - `uci` → an `id name` line, an `id author` line, an `option name Hash type spin default 16 min 1 max 1024` line, then `uciok`;
> - `isready` → `readyok`;
> - `ucinewgame` → reset any per-game search state;
> - `position startpos [moves <m1> <m2> ...]` and `position fen <6-field-fen> [moves ...]`, applying each listed coordinate move (with promotion suffix `q/r/b/n`) in order;
> - `go depth <N>`, `go movetime <ms>`, and clock-driven `go wtime <ms> btime <ms> winc <ms> binc <ms> movestogo <n>`;
> - `stop` and `quit`.
> - Every `go` must end with a `bestmove <move>` line (coordinate notation, promotion suffix where relevant), or `bestmove 0000` if there is no legal move.
>
> Under clock-driven `go`, allocate thinking time from the side-to-move's own clock and increment with a simple budget rule, keeping a safety reserve so the engine never flags. The exact allocation formula is yours.
>
> **Critical:** the input line buffer must be large enough to hold a full `position startpos moves ...` line for a long game (hundreds of plies). A buffer that truncates long move lists will cause the engine to misparse the position and play an illegal move, forfeiting the game. Size it generously (thousands of characters).
>
> Add a UCI smoke test (a script under tooling, wired as `make uci-smoke`) that pipes a minimal session — `uci`, `isready`, `position startpos`, `go depth 3`, `quit` — into the engine and asserts it sees `uciok`, `readyok`, and a final `bestmove`.
>
> Verification:
> - `make uci-smoke` passes: `uciok`, `readyok`, and a legal `bestmove` are all observed.
> - A long `position startpos moves <…200+ plies…>` line is parsed correctly and the resulting `go` returns a **legal** move (this is the buffer-size check — feed a real long game and confirm the move is legal in the final position).
> - `go movetime 1000` returns a `bestmove` within roughly the budget; clock-driven `go wtime … btime …` never consumes the whole remaining clock on a single move.

---

## Step 6: Elo Measurement Harness vs Stockfish

> Build the harness that turns "it plays legal chess" into a measured playing strength. Add tooling (under the tooling directory) that:
> 1. Runs engine-vs-engine matches through `cutechess-cli`, pairing `cobochess` against `stockfish` configured to a capped strength (via Stockfish's strength-limit / skill options), over a configurable number of games, time control, and a deterministic opening suite so games are varied but reproducible. Make the Stockfish strength cap and the game count parameters.
> 2. Writes the games out as PGN (plus a JSON summary) into a results directory.
> 3. Parses the resulting PGN and computes an Elo estimate for `cobochess` relative to the (known) opponent rating, **with a 95% confidence interval**. The PGN parser must attribute wins/draws/losses correctly **per game regardless of which colour `cobochess` had** — both colours appear across a match, so a parser that assumes a fixed colour will report a wrong score.
> 4. Ship a small deterministic opening book / suite so matches do not all start from the same line.
>
> Verification:
> - A short match (e.g. a few dozen games) against strength-limited Stockfish runs end to end and produces a PGN plus a JSON summary in the results directory.
> - The Elo calculator reads that PGN and reports W/D/L counts that sum to the number of games played, with `cobochess` games counted correctly whether it was White or Black (sanity-check: hand-count results in a tiny PGN and confirm the tool agrees).
> - The reported Elo estimate comes with a 95% confidence interval; running more games narrows the interval.
> - Against Stockfish capped near ~1600, the engine scores well enough that its estimated Elo lands in the same neighbourhood (the reference build reached ~1600 here; an early, untuned build will score far lower — that gap is the headroom Step 7 closes).

---

## Step 7: Strength Iteration Loop  `[objective loop]`

> **Objective, not a milestone.** This step has no fixed endpoint — it is the
> open-ended core of the project. You pursue an Elo *target* through repeated
> change-measure-keep/revert cycles; the work is done when the **stopping oracle**
> (estimated Elo near the target, with earlier gates still green) is satisfied, not
> after a set number of edits. How many cycles this takes, and whether the target
> is reached, depends on the agent — in the original session this is where most of
> the human steering happened.
>
> Now make it strong. Without breaking any earlier gate — `make perft` must stay green (move generation stays correct), `make uci-smoke` must stay green, and the engine must never return an illegal move — improve the engine's playing strength until its estimated Elo against the Step 6 harness lands near the ~1600 target.
>
> Work in short iteration cycles. Each cycle:
> 1. Pick one specific, *measurable* target (e.g. "raise estimated Elo vs Stockfish@1320 by ~100", "stop losing on time in long games", "reach an even score vs Stockfish@1600").
> 2. Change the engine — search quality, move ordering, evaluation richness, time use, or a position-caching scheme are all fair game; the techniques are entirely your choice.
> 3. Re-run `make perft` and `make uci-smoke` — **neither may regress**, and no game in a spot-check match may contain an illegal move.
> 4. Re-run a measurement match through the Step 6 harness and record the new estimated Elo with its confidence interval.
> 5. If the target is met, keep the change; otherwise revert and try something else.
>
> Concrete milestones to aim for (these come from the reference Codex run on the same setup, so they are achievable on commodity hardware; your numbers need not match exactly but should land in the same ballpark):
> - **Baseline** (end of Step 6): a playable but weak engine, estimated Elo only a few hundred.
> - **Buffer/time fix**: resolving the long-`position`-line truncation and any obvious time-management forfeits alone takes estimated Elo from roughly ~675 to ~1129 — fix this before tuning anything algorithmic.
> - **Move ordering + richer evaluation**: better move ordering and a positional (beyond material) evaluation take estimated Elo to roughly ~1589.
> - **Position caching + deeper search**: a transposition/position cache plus deeper, more selective search take estimated Elo to roughly ~1635 against Stockfish near 1600.
>
> At the end of each milestone, record (and commit) a short note: what changed, the before/after estimated Elo with confidence intervals, and confirmation that `make perft` and `make uci-smoke` still pass.

---

## Step 8: macOS Build Hardening

> Make the build survive a clean checkout on macOS arm64, where the default GnuCOBOL toolchain can produce a binary the kernel refuses to launch (it gets SIGKILLed at startup because of a missing/invalid code signature or a quarantine extended attribute, or because a stripped Mach-O is corrupted). Without this, every perft and match run can fail with signal 9 even though the engine is correct.
>
> Harden the Makefile and tooling so a fresh `make clean build` yields a binary that actually runs:
> - ad-hoc code-sign the freshly built binary and clear the `com.apple.quarantine` extended attribute;
> - force the Apple toolchain ahead of any GNU `strip` on `PATH` (a GNU `strip` corrupts the Mach-O), and pass the macOS target/SDK flags the linker needs;
> - serialise the build (don't let `clean` race `build`) and add a small post-build health check that runs the engine once (e.g. `--perft-startpos 1`), detects a SIGKILL, prints diagnostics, and retries the build a few times before giving up.
>
> Verification:
> - On macOS arm64, a fresh `make clean build` followed by `make perft` runs the engine without any signal-9 failure.
> - The post-build health check reports the binary is launchable (start-position perft at depth 1 returns 20, not a crash).
> - The build is reproducible: repeating `make clean build` does not intermittently fail due to a `clean`/`build` race.

---

## What actually happened (the real session trace)

The steps above are an idealized recipe. For honesty about the *open-ended,
objective-driven* nature of this build, here is the actual ordered sequence of
human prompts from the reference Codex session
(`COBOL-chess__Codex__019c41c7`, 26 user turns). Note how little of it is
specification and how much is **steering, measurement, and toolchain debugging** —
the spec is essentially one prompt (#3), and the rest is a strength-chasing loop
plus a long macOS build fight.

1. *[AGENTS.md skills/instructions preamble]*
2. "I want to build a chess engine in COBOL (GnuCOBOL)… at the end I want to test it and assess its Elo by playing games."
3. **"PLEASE IMPLEMENT THIS PLAN: # COBOL (GnuCOBOL) UCI Chess Engine + Elo Harness …"** (~10 K-char plan — Steps 1–6 are a linearization of *this single prompt*)
4. *[paste: `make build` — "Nothing to be done"]*
5. *[paste: `elo_calc.py` output — first Elo estimate]*
6. "it's working but it's not accurate: there is a mix of games with white and black side, and it seems to assume the engine always has [one colour]" — **the human catches an oracle bug in the harness**
7. "Elo of cobochess is not good at all… before improving it, investigate whether there's a misconfiguration about reading [results]"
8. "depth 4: is it for cobochess? such a depth is very low"
9. "I basically want to see games of the best 'variant' of cobochess"
10. **"the current implementation is very weak. Try to significantly improve the engine"** ← objective loop begins
11. "good… let's try to beat Stockfish @1600 now"
12. "indeed estimated 1600 Elo… now try to significantly improve the strength of the engine"
13. "continue…"
14. "how to assess new Elo rating?"
15–21, 24–26. *[repeated pastes of `make clean build && make perft && make uci-smoke` failures — macOS arm64 SIGKILL / code-signing / `com.apple.quarantine` / GNU-`strip` debugging → this is what Step 8 distils]*
22. *[turn aborted by the user on purpose]*
23. "I didn't give the permission but actually fine with the last command, sorry"

*Reading:* one specification prompt, then an objective ("get strong / beat 1600")
pursued by iterative steering, with a large fraction of turns spent on
measurement-harness correctness and platform build survival — not on the chess
algorithms themselves.
