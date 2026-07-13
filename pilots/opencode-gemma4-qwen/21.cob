       IDENTIFICATION DIVISION.
        PROGRAM-ID. GAME-OF-N.

        DATA DIVISION.
        WORKING-STORAGE SECTION.

        01  TOTAL-GAMES      PIC 9(10) VALUE ZERO.
        01  UNIQUE-GAMES     PIC 9(10) VALUE ZERO.
        01  UNIQUE-FLAG      PIC 9 VALUE ZERO.

        01  WS-CMDLINE       PIC X(256) VALUE SPACES.
        01  WS-POS           PIC 999 VALUE ZERO.

        01  WS-USED.
            05  USED-FLG     PIC 9 OCCURS 9 TIMES VALUE ZERO.

        01  WS-P1-NUMS.
            05  P1-NUM       PIC 9 OCCURS 9 TIMES VALUE ZERO.
        01  P1-CNT           PIC 99 VALUE ZERO.

        01  WS-P2-NUMS.
            05  P2-NUM       PIC 9 OCCURS 9 TIMES VALUE ZERO.
        01  P2-CNT           PIC 99 VALUE ZERO.

        01  WS-DEPTH         PIC 99 VALUE ZERO.
        01  WS-VAL           PIC 99 VALUE ZERO.

        01  WS-I             PIC 99 VALUE ZERO.
        01  WS-J             PIC 99 VALUE ZERO.
        01  WS-K             PIC 99 VALUE ZERO.
        01  WS-SUM           PIC 9(5) VALUE ZERO.
        01  WS-IS-WIN        PIC 9 VALUE ZERO.

        01  WS-REM           PIC 9 VALUE ZERO.
        01  WS-QUO           PIC 99 VALUE ZERO.

        01  WS-STACK-VAL     PIC 99 OCCURS 10 TIMES VALUE ZERO.
        01  WS-SP            PIC 99 VALUE ZERO.

        01  WS-DONE          PIC 9 VALUE ZERO.

        01  WS-GAME-SEQ      PIC 9 OCCURS 9 TIMES VALUE ZERO.

        01  WS-PERM-ALL      PIC 9 OCCURS 72 TIMES.

        01  WS-TRANSFORMED   PIC 9 OCCURS 9 TIMES VALUE ZERO.
        01  WS-IS-CANONICAL  PIC 9 VALUE ZERO.
        01  WS-PER           PIC 99 VALUE ZERO.
        01  WS-CMP           PIC S9 VALUE ZERO.
        01  WS-PERM-IDX      PIC 99 VALUE ZERO.

        01  WS-NUM-DISP      PIC 99 OCCURS 9 TIMES.
        01  WS-NUM-STR       PIC X(10) VALUE SPACES.

        01  TARGET-VALUE     PIC 99 VALUE 21.

        01  WIN-TABLE.
            05  WIN-ROW      OCCURS 8 TIMES.
                10  WIN-LINE PIC 9 OCCURS 3 TIMES.

        PROCEDURE DIVISION.
            ACCEPT WS-CMDLINE FROM COMMAND-LINE
            MOVE ZERO TO WS-POS
            PERFORM UNTIL WS-POS > 248
                ADD 1 TO WS-POS
                IF WS-CMDLINE(WS-POS:8) = "--unique"
                    MOVE 1 TO UNIQUE-FLAG
                END-IF
            END-PERFORM

            PERFORM INIT-WIN-LINES
            PERFORM INIT-NUM-DISPLAY
            PERFORM INIT-PERMS
            MOVE ZERO TO TOTAL-GAMES
            MOVE ZERO TO UNIQUE-GAMES
            MOVE ZERO TO WS-DEPTH
            MOVE ZERO TO P1-CNT
            MOVE ZERO TO P2-CNT
            MOVE ZERO TO WS-SP
            MOVE ZERO TO WS-DONE
            PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 9
                MOVE ZERO TO USED-FLG(WS-I)
            END-PERFORM
            MOVE 1 TO WS-VAL
            PERFORM UNTIL WS-DONE = 1
                PERFORM MAIN-STEP
            END-PERFORM
            IF UNIQUE-FLAG = 1
                DISPLAY "Total: " TOTAL-GAMES
                DISPLAY "Unique: " UNIQUE-GAMES
            ELSE
                DISPLAY "Total number of possible games: "
                    TOTAL-GAMES
            END-IF
            STOP RUN.

        INIT-WIN-LINES.
            MOVE 2 TO WIN-LINE(1,1)
            MOVE 9 TO WIN-LINE(1,2)
            MOVE 4 TO WIN-LINE(1,3)
            MOVE 7 TO WIN-LINE(2,1)
            MOVE 5 TO WIN-LINE(2,2)
            MOVE 3 TO WIN-LINE(2,3)
            MOVE 6 TO WIN-LINE(3,1)
            MOVE 1 TO WIN-LINE(3,2)
            MOVE 8 TO WIN-LINE(3,3)
            MOVE 2 TO WIN-LINE(4,1)
            MOVE 7 TO WIN-LINE(4,2)
            MOVE 6 TO WIN-LINE(4,3)
            MOVE 9 TO WIN-LINE(5,1)
            MOVE 5 TO WIN-LINE(5,2)
            MOVE 1 TO WIN-LINE(5,3)
            MOVE 4 TO WIN-LINE(6,1)
            MOVE 3 TO WIN-LINE(6,2)
            MOVE 8 TO WIN-LINE(6,3)
            MOVE 2 TO WIN-LINE(7,1)
            MOVE 5 TO WIN-LINE(7,2)
            MOVE 8 TO WIN-LINE(7,3)
            MOVE 4 TO WIN-LINE(8,1)
            MOVE 5 TO WIN-LINE(8,2)
            MOVE 6 TO WIN-LINE(8,3)
            EXIT.

        INIT-NUM-DISPLAY.
            MOVE 1 TO WS-NUM-DISP(1)
            MOVE 2 TO WS-NUM-DISP(2)
            MOVE 3 TO WS-NUM-DISP(3)
            MOVE 6 TO WS-NUM-DISP(4)
            MOVE 7 TO WS-NUM-DISP(5)
            MOVE 8 TO WS-NUM-DISP(6)
            MOVE 11 TO WS-NUM-DISP(7)
            MOVE 12 TO WS-NUM-DISP(8)
            MOVE 13 TO WS-NUM-DISP(9)
            EXIT.

        INIT-PERMS.
            MOVE 1 TO WS-PERM-ALL(1)
            MOVE 2 TO WS-PERM-ALL(2)
            MOVE 3 TO WS-PERM-ALL(3)
            MOVE 4 TO WS-PERM-ALL(4)
            MOVE 5 TO WS-PERM-ALL(5)
            MOVE 6 TO WS-PERM-ALL(6)
            MOVE 7 TO WS-PERM-ALL(7)
            MOVE 8 TO WS-PERM-ALL(8)
            MOVE 9 TO WS-PERM-ALL(9)
            MOVE 7 TO WS-PERM-ALL(10)
            MOVE 4 TO WS-PERM-ALL(11)
            MOVE 1 TO WS-PERM-ALL(12)
            MOVE 8 TO WS-PERM-ALL(13)
            MOVE 5 TO WS-PERM-ALL(14)
            MOVE 2 TO WS-PERM-ALL(15)
            MOVE 9 TO WS-PERM-ALL(16)
            MOVE 6 TO WS-PERM-ALL(17)
            MOVE 3 TO WS-PERM-ALL(18)
            MOVE 9 TO WS-PERM-ALL(19)
            MOVE 8 TO WS-PERM-ALL(20)
            MOVE 7 TO WS-PERM-ALL(21)
            MOVE 6 TO WS-PERM-ALL(22)
            MOVE 5 TO WS-PERM-ALL(23)
            MOVE 4 TO WS-PERM-ALL(24)
            MOVE 3 TO WS-PERM-ALL(25)
            MOVE 2 TO WS-PERM-ALL(26)
            MOVE 1 TO WS-PERM-ALL(27)
            MOVE 3 TO WS-PERM-ALL(28)
            MOVE 6 TO WS-PERM-ALL(29)
            MOVE 9 TO WS-PERM-ALL(30)
            MOVE 2 TO WS-PERM-ALL(31)
            MOVE 5 TO WS-PERM-ALL(32)
            MOVE 8 TO WS-PERM-ALL(33)
            MOVE 1 TO WS-PERM-ALL(34)
            MOVE 4 TO WS-PERM-ALL(35)
            MOVE 7 TO WS-PERM-ALL(36)
            MOVE 1 TO WS-PERM-ALL(37)
            MOVE 4 TO WS-PERM-ALL(38)
            MOVE 7 TO WS-PERM-ALL(39)
            MOVE 2 TO WS-PERM-ALL(40)
            MOVE 5 TO WS-PERM-ALL(41)
            MOVE 8 TO WS-PERM-ALL(42)
            MOVE 3 TO WS-PERM-ALL(43)
            MOVE 6 TO WS-PERM-ALL(44)
            MOVE 9 TO WS-PERM-ALL(45)
            MOVE 9 TO WS-PERM-ALL(46)
            MOVE 6 TO WS-PERM-ALL(47)
            MOVE 3 TO WS-PERM-ALL(48)
            MOVE 8 TO WS-PERM-ALL(49)
            MOVE 5 TO WS-PERM-ALL(50)
            MOVE 2 TO WS-PERM-ALL(51)
            MOVE 7 TO WS-PERM-ALL(52)
            MOVE 4 TO WS-PERM-ALL(53)
            MOVE 1 TO WS-PERM-ALL(54)
            MOVE 3 TO WS-PERM-ALL(55)
            MOVE 2 TO WS-PERM-ALL(56)
            MOVE 1 TO WS-PERM-ALL(57)
            MOVE 6 TO WS-PERM-ALL(58)
            MOVE 5 TO WS-PERM-ALL(59)
            MOVE 4 TO WS-PERM-ALL(60)
            MOVE 9 TO WS-PERM-ALL(61)
            MOVE 8 TO WS-PERM-ALL(62)
            MOVE 7 TO WS-PERM-ALL(63)
            MOVE 7 TO WS-PERM-ALL(64)
            MOVE 8 TO WS-PERM-ALL(65)
            MOVE 9 TO WS-PERM-ALL(66)
            MOVE 4 TO WS-PERM-ALL(67)
            MOVE 5 TO WS-PERM-ALL(68)
            MOVE 6 TO WS-PERM-ALL(69)
            MOVE 1 TO WS-PERM-ALL(70)
            MOVE 2 TO WS-PERM-ALL(71)
            MOVE 3 TO WS-PERM-ALL(72).

        MAIN-STEP.
            IF WS-DEPTH = 9
                ADD 1 TO TOTAL-GAMES
                IF UNIQUE-FLAG = 1
                    PERFORM CHECK-CANONICAL
                    IF WS-IS-CANONICAL = 1
                        ADD 1 TO UNIQUE-GAMES
                    END-IF
                END-IF
                PERFORM BACKTRACK-ONE
            ELSE
                IF WS-VAL > 9
                    PERFORM BACKTRACK-ONE
                ELSE
                    IF USED-FLG(WS-VAL) = ZERO
                        PERFORM MAKE-MOVE
                    ELSE
                        ADD 1 TO WS-VAL
                    END-IF
                END-IF
            END-IF.

        MAKE-MOVE.
            MOVE 1 TO USED-FLG(WS-VAL)
            ADD 1 TO WS-DEPTH
            MOVE WS-VAL TO WS-GAME-SEQ(WS-DEPTH)
            DIVIDE WS-DEPTH BY 2 GIVING WS-QUO
                REMAINDER WS-REM
            IF WS-REM = 1
                ADD 1 TO P1-CNT
                MOVE WS-VAL TO P1-NUM(P1-CNT)
            ELSE
                ADD 1 TO P2-CNT
                MOVE WS-VAL TO P2-NUM(P2-CNT)
            END-IF
            ADD 1 TO WS-SP
            MOVE WS-VAL TO WS-STACK-VAL(WS-SP)
            MOVE ZERO TO WS-IS-WIN
            IF WS-REM = 1
                IF P1-CNT >= 3
                    PERFORM CHECK-P1-WIN
                END-IF
            ELSE
                IF P2-CNT >= 3
                    PERFORM CHECK-P2-WIN
                END-IF
            END-IF
            IF WS-IS-WIN = 1
                ADD 1 TO TOTAL-GAMES
                IF UNIQUE-FLAG = 1
                    PERFORM CHECK-CANONICAL
                    IF WS-IS-CANONICAL = 1
                        ADD 1 TO UNIQUE-GAMES
                    END-IF
                END-IF
                PERFORM BACKTRACK-ONE
            ELSE
                MOVE 1 TO WS-VAL
            END-IF.

        CHECK-CANONICAL.
            MOVE 1 TO WS-IS-CANONICAL
            PERFORM VARYING WS-PER FROM 2 BY 1
                UNTIL WS-PER > 8 OR WS-IS-CANONICAL = 0
                PERFORM APPLY-PERM
                PERFORM COMPARE-GAME
                IF WS-CMP < 0
                    MOVE 0 TO WS-IS-CANONICAL
                END-IF
            END-PERFORM.

        APPLY-PERM.
            COMPUTE WS-PERM-IDX = (WS-PER - 1) * 9
            PERFORM VARYING WS-I FROM 1 BY 1
                UNTIL WS-I > WS-DEPTH
                MOVE WS-GAME-SEQ(WS-I) TO WS-J
                ADD WS-J TO WS-PERM-IDX
                MOVE WS-PERM-ALL(WS-PERM-IDX)
                    TO WS-TRANSFORMED(WS-I)
                COMPUTE WS-PERM-IDX = (WS-PER - 1) * 9
            END-PERFORM.

        COMPARE-GAME.
            MOVE 0 TO WS-CMP
            PERFORM VARYING WS-I FROM 1 BY 1
                UNTIL WS-I > WS-DEPTH OR WS-CMP NOT = 0
                IF WS-TRANSFORMED(WS-I) < WS-GAME-SEQ(WS-I)
                    MOVE -1 TO WS-CMP
                ELSE
                    IF WS-TRANSFORMED(WS-I) > WS-GAME-SEQ(WS-I)
                        MOVE 1 TO WS-CMP
                    END-IF
                END-IF
            END-PERFORM.

        BACKTRACK-ONE.
            IF WS-DEPTH > ZERO
                DIVIDE WS-DEPTH BY 2 GIVING WS-QUO
                    REMAINDER WS-REM
                IF WS-REM = 1
                    SUBTRACT 1 FROM P1-CNT
                    MOVE P1-NUM(P1-CNT + 1) TO WS-VAL
                ELSE
                    SUBTRACT 1 FROM P2-CNT
                    MOVE P2-NUM(P2-CNT + 1) TO WS-VAL
                END-IF
                MOVE ZERO TO USED-FLG(WS-VAL)
                SUBTRACT 1 FROM WS-DEPTH
                IF WS-SP > ZERO
                    MOVE WS-STACK-VAL(WS-SP) TO WS-VAL
                    SUBTRACT 1 FROM WS-SP
                    ADD 1 TO WS-VAL
                ELSE
                    ADD 1 TO WS-VAL
                END-IF
            ELSE
                MOVE 1 TO WS-DONE
            END-IF.

        CHECK-P1-WIN.
            PERFORM VARYING WS-I FROM 1 BY 1
                UNTIL WS-I > 8 OR WS-IS-WIN = 1
                MOVE ZERO TO WS-SUM
                PERFORM VARYING WS-J FROM 1 BY 1
                    UNTIL WS-J > 3
                    MOVE WIN-LINE(WS-J, WS-I) TO WS-K
                    ADD P1-NUM(WS-K) TO WS-SUM
                END-PERFORM
                IF WS-SUM = TARGET-VALUE
                    MOVE 1 TO WS-IS-WIN
                END-IF
            END-PERFORM.

        CHECK-P2-WIN.
            PERFORM VARYING WS-I FROM 1 BY 1
                UNTIL WS-I > 8 OR WS-IS-WIN = 1
                MOVE ZERO TO WS-SUM
                PERFORM VARYING WS-J FROM 1 BY 1
                    UNTIL WS-J > 3
                    MOVE WIN-LINE(WS-J, WS-I) TO WS-K
                    ADD P2-NUM(WS-K) TO WS-SUM
                END-PERFORM
                IF WS-SUM = TARGET-VALUE
                    MOVE 1 TO WS-IS-WIN
                END-IF
            END-PERFORM.
