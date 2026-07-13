#!/usr/bin/env python3
"""Post-hoc verification of the two defects in the vibe/mistral-medium-3.5
pilot artifact (pilots/vibe-mistral-medium/game15.cbl), 2026-07-08.

Defect 1 (structural): the program enumerates all 9! fixed orderings of the
digits 1..9 and counts one "game" per ordering, so its total can only ever be
362,880. The true game-tree count (stop at first win) is 255,168.

Defect 2 (win detection): in CHECK-WIN-FOR-P1/P2 the lines
    IF P1-WINS-GAME EXIT PARAGRAPH
    PERFORM CHECK-TRIPLE-2-FOR-P1
    ...
carry no END-IF and no periods, so under COBOL scope rules every subsequent
PERFORM nests inside the first IF (and sits behind EXIT PARAGRAPH). Only
CHECK-TRIPLE-1 -- the {1,5,9} line -- is ever reached. The delivered output
(P1 43,200 / P2 17,280 / draws 302,400) is reproduced EXACTLY by only-{1,5,9}
detection, and would be 212,256 / 104,544 / 46,080 with correct detection
over the same 9! orderings.

Run: python3 replications/vibe-bug-verification.py   (takes a few seconds)
"""
from itertools import permutations

WINS = [(1,5,9),(1,6,8),(2,4,9),(2,5,8),(2,6,7),(3,4,8),(3,5,7),(4,5,6)]


def play(perm, lines):
    p1, p2 = set(), set()
    for i, n in enumerate(perm):
        (p1 if i % 2 == 0 else p2).add(n)
        who = p1 if i % 2 == 0 else p2
        if any(set(l) <= who for l in lines):
            return 1 if i % 2 == 0 else 2
    return 0


def count(lines):
    c = {0: 0, 1: 0, 2: 0}
    for perm in permutations(range(1, 10)):
        c[play(perm, lines)] += 1
    return c


full = count(WINS)
only159 = count([(1, 5, 9)])
print("9! orderings, CORRECT detection :", full[1], full[2], full[0])
print("9! orderings, only {1,5,9}      :", only159[1], only159[2], only159[0])
print("vibe program (delivered)        : 43200 17280 302400")
assert (only159[1], only159[2], only159[0]) == (43200, 17280, 302400), "hypothesis refuted"
print("=> only-{1,5,9} detection reproduces the delivered output exactly.")
