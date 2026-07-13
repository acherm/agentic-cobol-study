#!/usr/bin/env python3
"""Generator for Game of N variants based on 3x3 magic squares.

A 3x3 magic square has the parametric form:
    e+a    e-a-b    e+b
    e-a+b    e     e+a-b
    e-b    e+a+b    e-a

where e is the center, and a, b are parameters.
The magic constant (target sum) is 3e.
"""

import itertools
import sys
import os

def generate_magic_square(e, a, b):
    """Generate a 3x3 magic square from parameters e, a, b."""
    return [
        [e+a,   e-a-b, e+b],
        [e-a+b, e,     e+a-b],
        [e-b,   e+a+b, e-a]
    ]

def get_numbers(square):
    """Extract the 9 numbers from the magic square."""
    return [n for row in square for n in row]

def get_winning_lines(square):
    """Get the 8 winning triplets (rows, cols, diagonals)."""
    lines = []
    # Rows
    for row in square:
        lines.append(tuple(row))
    # Columns
    for col in range(3):
        lines.append(tuple(square[row][col] for row in range(3)))
    # Diagonals
    lines.append(tuple(square[i][i] for i in range(3)))
    lines.append(tuple(square[i][2-i] for i in range(3)))
    return lines

def is_valid_variant(e, a, b):
    """Check if parameters produce 9 distinct numbers."""
    if a == 0 or b == 0 or a == b or a == -b:
        return False
    nums = get_numbers(generate_magic_square(e, a, b))
    return len(set(nums)) == 9

def find_variants(max_e=20, max_a=15, max_b=15, require_positive=True):
    """Find all valid variants within parameter bounds."""
    variants = []
    for e in range(1, max_e + 1):
        for a in range(-max_a, max_a + 1):
            for b in range(-max_b, max_b + 1):
                if a == 0 or b == 0:
                    continue
                if not is_valid_variant(e, a, b):
                    continue
                square = generate_magic_square(e, a, b)
                nums = get_numbers(square)
                if require_positive and any(n <= 0 for n in nums):
                    continue
                target = 3 * e
                lines = get_winning_lines(square)
                variants.append({
                    'e': e, 'a': a, 'b': b,
                    'square': square,
                    'numbers': sorted(set(nums)),
                    'target': target,
                    'lines': lines,
                })
    return variants

def format_number(n):
    """Format a number for display (remove trailing zeros for floats)."""
    if isinstance(n, float):
        if n == int(n):
            return str(int(n))
        return f"{n:g}"
    return str(n)

def _cobol_pic(n):
    """Generate a COBOL PIC clause for a number."""
    if isinstance(n, float) and n != int(n):
        decimal_places = len(str(n).split('.')[1]) if '.' in str(n) else 0
        int_part = int(n)
        int_digits = max(1, len(str(abs(int_part))))
        return f"PIC {'9' * int_digits}.{'9' * decimal_places}"
    else:
        n_int = int(n)
        int_digits = max(1, len(str(abs(n_int))))
        return f"PIC {'9' * int_digits}"

def _cobol_val(n):
    """Format a number as a COBOL literal."""
    if isinstance(n, float) and n != int(n):
        return f"{n:.2f}"
    return str(int(n))

def print_rules(variant, idx=None):
    """Print the rules for a game variant."""
    header = f"Game of {format_number(variant['target'])}"
    if idx is not None:
        header = f"Variant #{idx}: {header}"
    
    print("=" * len(header))
    print(header)
    print("=" * len(header))
    print()
    
    nums = [format_number(n) for n in variant['numbers']]
    print(f"Players alternate picking a number from {{{', '.join(nums)}}}.")
    print(f"A number may not be repeated.")
    print(f"The first player to hold three numbers summing to {format_number(variant['target'])} wins.")
    print(f"If all numbers are used with no winner, the game is a draw.")
    print()
    
    print("Magic square layout:")
    square = variant['square']
    max_len = max(len(format_number(n)) for row in square for n in row)
    for row in square:
        print("  " + "  ".join(format_number(n).rjust(max_len) for n in row))
    print()
    
    print(f"Winning lines (8 total, each sums to {format_number(variant['target'])}):")
    for i, line in enumerate(variant['lines'], 1):
        formatted = [format_number(n) for n in line]
        print(f"  {i}. {{{', '.join(formatted)}}}")
    print()

def generate_cobol(variant, output_path=None):
    """Generate COBOL source code for a game variant."""
    target = variant['target']
    numbers = variant['numbers']
    n = len(numbers)
    
    # Map numbers to indices 1..9 for internal representation
    num_to_idx = {n: i+1 for i, n in enumerate(numbers)}
    idx_to_num = {i+1: n for i, n in enumerate(numbers)}
    
    # Convert winning lines to index-based
    win_lines = []
    for line in variant['lines']:
        win_lines.append(tuple(num_to_idx[n] for n in line))
    
    # Format target for COBOL
    target_pic = _cobol_pic(target)
    target_val = _cobol_val(target)
    
    # Build WIN-LINE initialization lines
    win_init_lines = []
    for i, line in enumerate(win_lines):
        for j, idx in enumerate(line):
            win_init_lines.append(f"            MOVE {idx} TO WIN-LINE({i+1},{j+1})")
    
    # Build number display initialization lines
    num_init_lines = []
    for i in range(1, 10):
        n = idx_to_num[i]
        num_init_lines.append(f"            MOVE {_cobol_val(n)} TO WS-NUM-DISP({i})")
    
    win_init_block = "\n".join(win_init_lines)
    num_init_block = "\n".join(num_init_lines)
    
    parts = []
    parts.append("       IDENTIFICATION DIVISION.")
    parts.append("        PROGRAM-ID. GAME-OF-N.")
    parts.append("")
    parts.append("        DATA DIVISION.")
    parts.append("        WORKING-STORAGE SECTION.")
    parts.append("")
    parts.append("        01  TOTAL-GAMES      PIC 9(10) VALUE ZERO.")
    parts.append("        01  UNIQUE-GAMES     PIC 9(10) VALUE ZERO.")
    parts.append("        01  UNIQUE-FLAG      PIC 9 VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-CMDLINE       PIC X(256) VALUE SPACES.")
    parts.append("        01  WS-POS           PIC 999 VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-USED.")
    parts.append("            05  USED-FLG     PIC 9 OCCURS 9 TIMES VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-P1-NUMS.")
    parts.append("            05  P1-NUM       PIC 9 OCCURS 9 TIMES VALUE ZERO.")
    parts.append("        01  P1-CNT           PIC 99 VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-P2-NUMS.")
    parts.append("            05  P2-NUM       PIC 9 OCCURS 9 TIMES VALUE ZERO.")
    parts.append("        01  P2-CNT           PIC 99 VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-DEPTH         PIC 99 VALUE ZERO.")
    parts.append("        01  WS-VAL           PIC 99 VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-I             PIC 99 VALUE ZERO.")
    parts.append("        01  WS-J             PIC 99 VALUE ZERO.")
    parts.append("        01  WS-K             PIC 99 VALUE ZERO.")
    parts.append("        01  WS-SUM           PIC 9(5) VALUE ZERO.")
    parts.append("        01  WS-IS-WIN        PIC 9 VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-REM           PIC 9 VALUE ZERO.")
    parts.append("        01  WS-QUO           PIC 99 VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-STACK-VAL     PIC 99 OCCURS 10 TIMES VALUE ZERO.")
    parts.append("        01  WS-SP            PIC 99 VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-DONE          PIC 9 VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-GAME-SEQ      PIC 9 OCCURS 9 TIMES VALUE ZERO.")
    parts.append("")
    parts.append("        01  WS-PERM-ALL      PIC 9 OCCURS 72 TIMES.")
    parts.append("")
    parts.append("        01  WS-TRANSFORMED   PIC 9 OCCURS 9 TIMES VALUE ZERO.")
    parts.append("        01  WS-IS-CANONICAL  PIC 9 VALUE ZERO.")
    parts.append("        01  WS-PER           PIC 99 VALUE ZERO.")
    parts.append("        01  WS-CMP           PIC S9 VALUE ZERO.")
    parts.append("        01  WS-PERM-IDX      PIC 99 VALUE ZERO.")
    parts.append("")
    parts.append(f"        01  WS-NUM-DISP      {_cobol_pic(target)} OCCURS 9 TIMES.")
    parts.append("        01  WS-NUM-STR       PIC X(10) VALUE SPACES.")
    parts.append("")
    parts.append(f"        01  TARGET-VALUE     {target_pic} VALUE {target_val}.")
    parts.append("")
    parts.append("        01  WIN-TABLE.")
    parts.append("            05  WIN-ROW      OCCURS 8 TIMES.")
    parts.append("                10  WIN-LINE PIC 9 OCCURS 3 TIMES.")
    parts.append("")
    parts.append("        PROCEDURE DIVISION.")
    parts.append("            ACCEPT WS-CMDLINE FROM COMMAND-LINE")
    parts.append("            MOVE ZERO TO WS-POS")
    parts.append("            PERFORM UNTIL WS-POS > 248")
    parts.append("                ADD 1 TO WS-POS")
    parts.append("                IF WS-CMDLINE(WS-POS:8) = \"--unique\"")
    parts.append("                    MOVE 1 TO UNIQUE-FLAG")
    parts.append("                END-IF")
    parts.append("            END-PERFORM")
    parts.append("")
    parts.append("            PERFORM INIT-WIN-LINES")
    parts.append("            PERFORM INIT-NUM-DISPLAY")
    parts.append("            PERFORM INIT-PERMS")
    parts.append("            MOVE ZERO TO TOTAL-GAMES")
    parts.append("            MOVE ZERO TO UNIQUE-GAMES")
    parts.append("            MOVE ZERO TO WS-DEPTH")
    parts.append("            MOVE ZERO TO P1-CNT")
    parts.append("            MOVE ZERO TO P2-CNT")
    parts.append("            MOVE ZERO TO WS-SP")
    parts.append("            MOVE ZERO TO WS-DONE")
    parts.append("            PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 9")
    parts.append("                MOVE ZERO TO USED-FLG(WS-I)")
    parts.append("            END-PERFORM")
    parts.append("            MOVE 1 TO WS-VAL")
    parts.append("            PERFORM UNTIL WS-DONE = 1")
    parts.append("                PERFORM MAIN-STEP")
    parts.append("            END-PERFORM")
    parts.append("            IF UNIQUE-FLAG = 1")
    parts.append("                DISPLAY \"Total: \" TOTAL-GAMES")
    parts.append("                DISPLAY \"Unique: \" UNIQUE-GAMES")
    parts.append("            ELSE")
    parts.append("                DISPLAY \"Total number of possible games: \"")
    parts.append("                    TOTAL-GAMES")
    parts.append("            END-IF")
    parts.append("            STOP RUN.")
    parts.append("")
    parts.append("        INIT-WIN-LINES.")
    parts.extend(win_init_lines)
    parts.append("            EXIT.")
    parts.append("")
    parts.append("        INIT-NUM-DISPLAY.")
    parts.extend(num_init_lines)
    parts.append("            EXIT.")
    parts.append("")
    parts.append("        INIT-PERMS.")
    parts.append("            MOVE 1 TO WS-PERM-ALL(1)")
    parts.append("            MOVE 2 TO WS-PERM-ALL(2)")
    parts.append("            MOVE 3 TO WS-PERM-ALL(3)")
    parts.append("            MOVE 4 TO WS-PERM-ALL(4)")
    parts.append("            MOVE 5 TO WS-PERM-ALL(5)")
    parts.append("            MOVE 6 TO WS-PERM-ALL(6)")
    parts.append("            MOVE 7 TO WS-PERM-ALL(7)")
    parts.append("            MOVE 8 TO WS-PERM-ALL(8)")
    parts.append("            MOVE 9 TO WS-PERM-ALL(9)")
    parts.append("            MOVE 7 TO WS-PERM-ALL(10)")
    parts.append("            MOVE 4 TO WS-PERM-ALL(11)")
    parts.append("            MOVE 1 TO WS-PERM-ALL(12)")
    parts.append("            MOVE 8 TO WS-PERM-ALL(13)")
    parts.append("            MOVE 5 TO WS-PERM-ALL(14)")
    parts.append("            MOVE 2 TO WS-PERM-ALL(15)")
    parts.append("            MOVE 9 TO WS-PERM-ALL(16)")
    parts.append("            MOVE 6 TO WS-PERM-ALL(17)")
    parts.append("            MOVE 3 TO WS-PERM-ALL(18)")
    parts.append("            MOVE 9 TO WS-PERM-ALL(19)")
    parts.append("            MOVE 8 TO WS-PERM-ALL(20)")
    parts.append("            MOVE 7 TO WS-PERM-ALL(21)")
    parts.append("            MOVE 6 TO WS-PERM-ALL(22)")
    parts.append("            MOVE 5 TO WS-PERM-ALL(23)")
    parts.append("            MOVE 4 TO WS-PERM-ALL(24)")
    parts.append("            MOVE 3 TO WS-PERM-ALL(25)")
    parts.append("            MOVE 2 TO WS-PERM-ALL(26)")
    parts.append("            MOVE 1 TO WS-PERM-ALL(27)")
    parts.append("            MOVE 3 TO WS-PERM-ALL(28)")
    parts.append("            MOVE 6 TO WS-PERM-ALL(29)")
    parts.append("            MOVE 9 TO WS-PERM-ALL(30)")
    parts.append("            MOVE 2 TO WS-PERM-ALL(31)")
    parts.append("            MOVE 5 TO WS-PERM-ALL(32)")
    parts.append("            MOVE 8 TO WS-PERM-ALL(33)")
    parts.append("            MOVE 1 TO WS-PERM-ALL(34)")
    parts.append("            MOVE 4 TO WS-PERM-ALL(35)")
    parts.append("            MOVE 7 TO WS-PERM-ALL(36)")
    parts.append("            MOVE 1 TO WS-PERM-ALL(37)")
    parts.append("            MOVE 4 TO WS-PERM-ALL(38)")
    parts.append("            MOVE 7 TO WS-PERM-ALL(39)")
    parts.append("            MOVE 2 TO WS-PERM-ALL(40)")
    parts.append("            MOVE 5 TO WS-PERM-ALL(41)")
    parts.append("            MOVE 8 TO WS-PERM-ALL(42)")
    parts.append("            MOVE 3 TO WS-PERM-ALL(43)")
    parts.append("            MOVE 6 TO WS-PERM-ALL(44)")
    parts.append("            MOVE 9 TO WS-PERM-ALL(45)")
    parts.append("            MOVE 9 TO WS-PERM-ALL(46)")
    parts.append("            MOVE 6 TO WS-PERM-ALL(47)")
    parts.append("            MOVE 3 TO WS-PERM-ALL(48)")
    parts.append("            MOVE 8 TO WS-PERM-ALL(49)")
    parts.append("            MOVE 5 TO WS-PERM-ALL(50)")
    parts.append("            MOVE 2 TO WS-PERM-ALL(51)")
    parts.append("            MOVE 7 TO WS-PERM-ALL(52)")
    parts.append("            MOVE 4 TO WS-PERM-ALL(53)")
    parts.append("            MOVE 1 TO WS-PERM-ALL(54)")
    parts.append("            MOVE 3 TO WS-PERM-ALL(55)")
    parts.append("            MOVE 2 TO WS-PERM-ALL(56)")
    parts.append("            MOVE 1 TO WS-PERM-ALL(57)")
    parts.append("            MOVE 6 TO WS-PERM-ALL(58)")
    parts.append("            MOVE 5 TO WS-PERM-ALL(59)")
    parts.append("            MOVE 4 TO WS-PERM-ALL(60)")
    parts.append("            MOVE 9 TO WS-PERM-ALL(61)")
    parts.append("            MOVE 8 TO WS-PERM-ALL(62)")
    parts.append("            MOVE 7 TO WS-PERM-ALL(63)")
    parts.append("            MOVE 7 TO WS-PERM-ALL(64)")
    parts.append("            MOVE 8 TO WS-PERM-ALL(65)")
    parts.append("            MOVE 9 TO WS-PERM-ALL(66)")
    parts.append("            MOVE 4 TO WS-PERM-ALL(67)")
    parts.append("            MOVE 5 TO WS-PERM-ALL(68)")
    parts.append("            MOVE 6 TO WS-PERM-ALL(69)")
    parts.append("            MOVE 1 TO WS-PERM-ALL(70)")
    parts.append("            MOVE 2 TO WS-PERM-ALL(71)")
    parts.append("            MOVE 3 TO WS-PERM-ALL(72).")
    parts.append("")
    parts.append("        MAIN-STEP.")
    parts.append("            IF WS-DEPTH = 9")
    parts.append("                ADD 1 TO TOTAL-GAMES")
    parts.append("                IF UNIQUE-FLAG = 1")
    parts.append("                    PERFORM CHECK-CANONICAL")
    parts.append("                    IF WS-IS-CANONICAL = 1")
    parts.append("                        ADD 1 TO UNIQUE-GAMES")
    parts.append("                    END-IF")
    parts.append("                END-IF")
    parts.append("                PERFORM BACKTRACK-ONE")
    parts.append("            ELSE")
    parts.append("                IF WS-VAL > 9")
    parts.append("                    PERFORM BACKTRACK-ONE")
    parts.append("                ELSE")
    parts.append("                    IF USED-FLG(WS-VAL) = ZERO")
    parts.append("                        PERFORM MAKE-MOVE")
    parts.append("                    ELSE")
    parts.append("                        ADD 1 TO WS-VAL")
    parts.append("                    END-IF")
    parts.append("                END-IF")
    parts.append("            END-IF.")
    parts.append("")
    parts.append("        MAKE-MOVE.")
    parts.append("            MOVE 1 TO USED-FLG(WS-VAL)")
    parts.append("            ADD 1 TO WS-DEPTH")
    parts.append("            MOVE WS-VAL TO WS-GAME-SEQ(WS-DEPTH)")
    parts.append("            DIVIDE WS-DEPTH BY 2 GIVING WS-QUO")
    parts.append("                REMAINDER WS-REM")
    parts.append("            IF WS-REM = 1")
    parts.append("                ADD 1 TO P1-CNT")
    parts.append("                MOVE WS-VAL TO P1-NUM(P1-CNT)")
    parts.append("            ELSE")
    parts.append("                ADD 1 TO P2-CNT")
    parts.append("                MOVE WS-VAL TO P2-NUM(P2-CNT)")
    parts.append("            END-IF")
    parts.append("            ADD 1 TO WS-SP")
    parts.append("            MOVE WS-VAL TO WS-STACK-VAL(WS-SP)")
    parts.append("            MOVE ZERO TO WS-IS-WIN")
    parts.append("            IF WS-REM = 1")
    parts.append("                IF P1-CNT >= 3")
    parts.append("                    PERFORM CHECK-P1-WIN")
    parts.append("                END-IF")
    parts.append("            ELSE")
    parts.append("                IF P2-CNT >= 3")
    parts.append("                    PERFORM CHECK-P2-WIN")
    parts.append("                END-IF")
    parts.append("            END-IF")
    parts.append("            IF WS-IS-WIN = 1")
    parts.append("                ADD 1 TO TOTAL-GAMES")
    parts.append("                IF UNIQUE-FLAG = 1")
    parts.append("                    PERFORM CHECK-CANONICAL")
    parts.append("                    IF WS-IS-CANONICAL = 1")
    parts.append("                        ADD 1 TO UNIQUE-GAMES")
    parts.append("                    END-IF")
    parts.append("                END-IF")
    parts.append("                PERFORM BACKTRACK-ONE")
    parts.append("            ELSE")
    parts.append("                MOVE 1 TO WS-VAL")
    parts.append("            END-IF.")
    parts.append("")
    parts.append("        CHECK-CANONICAL.")
    parts.append("            MOVE 1 TO WS-IS-CANONICAL")
    parts.append("            PERFORM VARYING WS-PER FROM 2 BY 1")
    parts.append("                UNTIL WS-PER > 8 OR WS-IS-CANONICAL = 0")
    parts.append("                PERFORM APPLY-PERM")
    parts.append("                PERFORM COMPARE-GAME")
    parts.append("                IF WS-CMP < 0")
    parts.append("                    MOVE 0 TO WS-IS-CANONICAL")
    parts.append("                END-IF")
    parts.append("            END-PERFORM.")
    parts.append("")
    parts.append("        APPLY-PERM.")
    parts.append("            COMPUTE WS-PERM-IDX = (WS-PER - 1) * 9")
    parts.append("            PERFORM VARYING WS-I FROM 1 BY 1")
    parts.append("                UNTIL WS-I > WS-DEPTH")
    parts.append("                MOVE WS-GAME-SEQ(WS-I) TO WS-J")
    parts.append("                ADD WS-J TO WS-PERM-IDX")
    parts.append("                MOVE WS-PERM-ALL(WS-PERM-IDX)")
    parts.append("                    TO WS-TRANSFORMED(WS-I)")
    parts.append("                COMPUTE WS-PERM-IDX = (WS-PER - 1) * 9")
    parts.append("            END-PERFORM.")
    parts.append("")
    parts.append("        COMPARE-GAME.")
    parts.append("            MOVE 0 TO WS-CMP")
    parts.append("            PERFORM VARYING WS-I FROM 1 BY 1")
    parts.append("                UNTIL WS-I > WS-DEPTH OR WS-CMP NOT = 0")
    parts.append("                IF WS-TRANSFORMED(WS-I) < WS-GAME-SEQ(WS-I)")
    parts.append("                    MOVE -1 TO WS-CMP")
    parts.append("                ELSE")
    parts.append("                    IF WS-TRANSFORMED(WS-I) > WS-GAME-SEQ(WS-I)")
    parts.append("                        MOVE 1 TO WS-CMP")
    parts.append("                    END-IF")
    parts.append("                END-IF")
    parts.append("            END-PERFORM.")
    parts.append("")
    parts.append("        BACKTRACK-ONE.")
    parts.append("            IF WS-DEPTH > ZERO")
    parts.append("                DIVIDE WS-DEPTH BY 2 GIVING WS-QUO")
    parts.append("                    REMAINDER WS-REM")
    parts.append("                IF WS-REM = 1")
    parts.append("                    SUBTRACT 1 FROM P1-CNT")
    parts.append("                    MOVE P1-NUM(P1-CNT + 1) TO WS-VAL")
    parts.append("                ELSE")
    parts.append("                    SUBTRACT 1 FROM P2-CNT")
    parts.append("                    MOVE P2-NUM(P2-CNT + 1) TO WS-VAL")
    parts.append("                END-IF")
    parts.append("                MOVE ZERO TO USED-FLG(WS-VAL)")
    parts.append("                SUBTRACT 1 FROM WS-DEPTH")
    parts.append("                IF WS-SP > ZERO")
    parts.append("                    MOVE WS-STACK-VAL(WS-SP) TO WS-VAL")
    parts.append("                    SUBTRACT 1 FROM WS-SP")
    parts.append("                    ADD 1 TO WS-VAL")
    parts.append("                ELSE")
    parts.append("                    ADD 1 TO WS-VAL")
    parts.append("                END-IF")
    parts.append("            ELSE")
    parts.append("                MOVE 1 TO WS-DONE")
    parts.append("            END-IF.")
    parts.append("")
    parts.append("        CHECK-P1-WIN.")
    parts.append("            PERFORM VARYING WS-I FROM 1 BY 1")
    parts.append("                UNTIL WS-I > 8 OR WS-IS-WIN = 1")
    parts.append("                MOVE ZERO TO WS-SUM")
    parts.append("                PERFORM VARYING WS-J FROM 1 BY 1")
    parts.append("                    UNTIL WS-J > 3")
    parts.append("                    MOVE WIN-LINE(WS-J, WS-I) TO WS-K")
    parts.append("                    ADD P1-NUM(WS-K) TO WS-SUM")
    parts.append("                END-PERFORM")
    parts.append("                IF WS-SUM = TARGET-VALUE")
    parts.append("                    MOVE 1 TO WS-IS-WIN")
    parts.append("                END-IF")
    parts.append("            END-PERFORM.")
    parts.append("")
    parts.append("        CHECK-P2-WIN.")
    parts.append("            PERFORM VARYING WS-I FROM 1 BY 1")
    parts.append("                UNTIL WS-I > 8 OR WS-IS-WIN = 1")
    parts.append("                MOVE ZERO TO WS-SUM")
    parts.append("                PERFORM VARYING WS-J FROM 1 BY 1")
    parts.append("                    UNTIL WS-J > 3")
    parts.append("                    MOVE WIN-LINE(WS-J, WS-I) TO WS-K")
    parts.append("                    ADD P2-NUM(WS-K) TO WS-SUM")
    parts.append("                END-PERFORM")
    parts.append("                IF WS-SUM = TARGET-VALUE")
    parts.append("                    MOVE 1 TO WS-IS-WIN")
    parts.append("                END-IF")
    parts.append("            END-PERFORM.")
    parts.append("")
    
    cobol = "\n".join(parts)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(cobol)
        print(f"Generated COBOL code: {output_path}")
    
    return cobol

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Game of N variant generator')
    parser.add_argument('--list', action='store_true', help='List all variants')
    parser.add_argument('--generate', type=str, metavar='TARGET', help='Generate COBOL code for target N')
    parser.add_argument('--max-e', type=int, default=20, help='Max center value')
    parser.add_argument('--max-param', type=int, default=15, help='Max parameter value')
    parser.add_argument('--allow-negative', action='store_true', help='Allow negative numbers')
    args = parser.parse_args()
    
    variants = find_variants(args.max_e, args.max_param, args.max_param, not args.allow_negative)
    
    if args.list:
        print(f"Found {len(variants)} variants:\n")
        for i, v in enumerate(variants, 1):
            print_rules(v, i)
            if i < len(variants):
                print("-" * 40)
                print()
    elif args.generate:
        target = float(args.generate)
        # Scale decimal targets to integers
        scale = 1
        scaled_target = target
        while scaled_target != int(scaled_target) and scale <= 10000:
            scale *= 10
            scaled_target = target * scale
        scaled_target = int(scaled_target)
        
        matching = [v for v in variants if v['target'] == scaled_target]
        if not matching:
            print(f"No variant found with target {target} (scaled: {scaled_target})")
            sys.exit(1)
        variant = matching[0]
        # Scale numbers back for display
        variant = dict(variant)
        variant['numbers'] = [n / scale for n in variant['numbers']]
        variant['square'] = [[n / scale for n in row] for row in variant['square']]
        variant['lines'] = [[n / scale for n in line] for line in variant['lines']]
        variant['target'] = target
        variant['scale'] = scale
        
        output = args.generate.replace('.', '') + '.cob'
        generate_cobol(variant, output)
        print_rules(variant)
    else:
        print("Usage: python3 game_n_generator.py --list")
        print("       python3 game_n_generator.py --generate 0.15")
        print()
        print("Available targets:", sorted(set(v['target'] for v in variants)))

if __name__ == '__main__':
    main()
