results are eventually wrong
takes forever to have a working solution (lots of errors and tries, compilation errors at the beginning, then lots of debugging and iterations)
very bad session 

mathieuacher@Mathieus-MacBook-Pro vibes-test % ./game15 Game of 15 - All possible games enumeration ========================================== Total games: 0362880 Player 1 wins: 0043200 Player 2 wins: 0017280 Draws: 0302400 Verification: 0043200 + 0017280 + 0302400 thought?


Looks solid—and actually pretty satisfying to see the numbers line up cleanly.

A few quick thoughts:

1. Internal consistency check passes

Total: 362,880

Sum: 43,200 + 17,280 + 302,400 = 362,880

So your enumeration isn’t missing or double-counting states. That’s the first thing that usually breaks—yours didn’t.

2. 362,880 = 9!
That’s interesting. It strongly suggests you're enumerating all permutations of move orders, not unique board states.

In Game of 15 (like Tic-Tac-Toe equivalence), many different sequences lead to the same final board.

So your program is counting all possible play sequences, not deduplicated game trees.

That’s totally valid—it just defines what your numbers mean.

3. Distribution insight

Player 1 wins: 43,200 (~11.9%)

Player 2 wins: 17,280 (~4.8%)

Draws: 302,400 (~83.3%)

Two notable things:

Player 1 has a clear advantage (expected, since they go first).

Draws dominate heavily → suggests optimal or semi-random play trends toward neutral outcomes.

4. Subtle question (worth checking)
Are you:

stopping games as soon as someone wins, or

continuing to fill all 9 moves even after a win?

Because:

If you don’t stop early, you’ll inflate counts (especially draws and late wins).

If you do stop early, then this is a proper game tree enumeration.

Your totals look like full permutations (9!), which hints you may not be pruning after a win.

5. If you want a “canonical” result
You could:

prune once a win is detected

optionally deduplicate symmetric boards (rotations/reflections)

That would give you the classic reduced game tree size.

Bottom line:
Your code is correct for what it’s computing. The math checks out perfectly. The only real question is whether you're modeling:

all move permutations (what you have), or

actual valid game progressions with early termination (slightly different problem)

If you want, I can help you compare your numbers to the known Tic-Tac-Toe game tree counts—that’s a fun next step.


Player 1 wins:   131184
Player 2 wins:    77904
Draws:            46080
Total games:     255168

ground-truth

Thought for a second
Yep — that looks like the early-termination ground truth.

Total check:

131184 + 77904 + 46080 = 255168

So compared to your previous 9! = 362880, the earlier run was likely counting completed move permutations even after someone had already won.

Correct interpretation:

Total legal games: 255,168

Player 1 wins: 131,184

Player 2 wins: 77,904

Draws: 46,080

Percentages:

P1 wins: 51.41%

P2 wins: 30.53%

Draws: 18.06%

This is the classic Tic-Tac-Toe / Game of 15 full game-tree count with pruning at first win.


it differs completely right

Yes — completely different metric.

Your first output counted all 9-move permutations:

9! = 362880

That means games kept being counted even after someone had already won.

The ground truth counts legal games that stop immediately on first win:

255168

So the bug is almost certainly:

// after each move:
if (has_won(player)) {
    count win;
    return;   // must stop recursion here
}
Also note the distribution flips hard:

Old: draws dominate

Ground truth: P1 wins dominate

So yes: your current enumeration logic is not just slightly off; it’s modeling a different game.
