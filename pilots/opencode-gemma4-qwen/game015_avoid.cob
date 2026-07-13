       IDENTIFICATION DIVISION.
       PROGRAM-ID. GAME15-AVOID.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

       01  TOTAL-GAMES      PIC 9(10) VALUE ZERO.
       01  UNIQUE-GAMES     PIC 9(10) VALUE ZERO.

       01  WS-CMDLINE       PIC X(256) VALUE SPACES.
       01  WS-POS           PIC 999 VALUE ZERO.
       01  UNIQUE-FLAG      PIC 9 VALUE ZERO.
       01  TREE-FLAG        PIC 9 VALUE ZERO.
       01  MAX-DEPTH        PIC 99 VALUE 99.
       01  WS-DEPTH-NUM     PIC 99 VALUE ZERO.

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
       01  WS-SUM           PIC 99 VALUE ZERO.
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

       01  POW3             PIC 9(5) OCCURS 9 TIMES.
       01  POW3X2           PIC 9(5) OCCURS 9 TIMES.

       01  CACHE-VAL        PIC S9 OCCURS 19684 TIMES VALUE 2.
       01  CACHE-CNT        PIC 9(10) OCCURS 19684 TIMES VALUE 0.
       01  CACHE-KEY        PIC 9(5) VALUE 1.

       01  MM-USED          PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  MM-P1-NUM        PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  MM-P2-NUM        PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  MM-P1-CNT        PIC 99 VALUE ZERO.
       01  MM-P2-CNT        PIC 99 VALUE ZERO.
       01  MM-DEPTH         PIC 99 VALUE ZERO.
       01  MM-VAL           PIC 99 VALUE ZERO.
       01  MM-REM           PIC 9 VALUE ZERO.
       01  MM-QUO           PIC 99 VALUE ZERO.
       01  MM-IS-WIN        PIC 9 VALUE ZERO.
       01  MM-SUM           PIC 99 VALUE ZERO.
       01  MM-DONE          PIC 9 VALUE ZERO.
       01  MM-SP            PIC 99 VALUE ZERO.
       01  MM-STK-VAL       PIC 99 OCCURS 11 TIMES VALUE ZERO.
       01  MM-STK-BEST      PIC S9 OCCURS 11 TIMES VALUE 2.
       01  MM-CUR           PIC S9 VALUE ZERO.
       01  MM-I             PIC 99 VALUE ZERO.
       01  MM-J             PIC 99 VALUE ZERO.
       01  MM-K             PIC 99 VALUE ZERO.

       01  CNT-USED         PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  CNT-P1-NUM       PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  CNT-P2-NUM       PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  CNT-P1-CNT       PIC 99 VALUE ZERO.
       01  CNT-P2-CNT       PIC 99 VALUE ZERO.
       01  CNT-DEPTH        PIC 99 VALUE ZERO.
       01  CNT-VAL          PIC 99 VALUE ZERO.
       01  CNT-REM          PIC 9 VALUE ZERO.
       01  CNT-QUO          PIC 99 VALUE ZERO.
       01  CNT-IS-WIN       PIC 9 VALUE ZERO.
       01  CNT-SUM          PIC 99 VALUE ZERO.
       01  CNT-DONE         PIC 9 VALUE ZERO.
       01  CNT-SP           PIC 99 VALUE ZERO.
       01  CNT-STK-VAL      PIC 99 OCCURS 11 TIMES VALUE ZERO.
       01  CNT-RESULT       PIC 9(10) VALUE ZERO.

       01  WS-CVAL          PIC S9 VALUE ZERO.
       01  WS-PVAL          PIC S9 VALUE ZERO.
       01  WS-VSTR          PIC X(3) VALUE SPACES.
       01  WS-MOVE-STR      PIC X(3) VALUE SPACES.
       01  WS-CNT-STR       PIC Z(9)9 VALUE ZERO.
       01  WS-TOT-STR       PIC Z(9)9 VALUE ZERO.
       01  WS-NUM-STR       PIC Z9 VALUE ZERO.

       01  TREE-PVAL        PIC S9 VALUE ZERO.
       01  TREE-DEPTH       PIC 99 VALUE ZERO.
       01  TREE-P1-CNT      PIC 99 VALUE ZERO.
       01  TREE-P2-CNT      PIC 99 VALUE ZERO.
       01  TREE-P1-NUM      PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  TREE-P2-NUM      PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  TREE-USED        PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  TREE-VAL         PIC 99 VALUE ZERO.
       01  TREE-REM         PIC 9 VALUE ZERO.
       01  TREE-QUO         PIC 99 VALUE ZERO.
       01  TREE-KEY         PIC 9(5) VALUE 1.
       01  TREE-STACK-PVAL  PIC S9 OCCURS 10 TIMES VALUE 0.
       01  TREE-STACK-LOOP  PIC 99 OCCURS 10 TIMES VALUE 0.
       01  TREE-STACK-POS   PIC 99 VALUE 0.

       PROCEDURE DIVISION.
           ACCEPT WS-CMDLINE FROM COMMAND-LINE
           MOVE ZERO TO WS-POS
           MOVE 99 TO MAX-DEPTH
           PERFORM PARSE-ARGS

           IF TREE-FLAG = 1
               PERFORM INIT-TABLES
               PERFORM COMPUTE-ALL
               PERFORM COMPUTE-ROOT-CNT
               PERFORM PRINT-TREE
           ELSE
               PERFORM INIT-PERMS
               MOVE ZERO TO TOTAL-GAMES
               MOVE ZERO TO UNIQUE-GAMES
               MOVE ZERO TO WS-DEPTH
               MOVE ZERO TO P1-CNT
               MOVE ZERO TO P2-CNT
               MOVE ZERO TO WS-SP
               MOVE ZERO TO WS-DONE
               PERFORM VARYING WS-I FROM 1 BY 1
                   UNTIL WS-I > 9
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
           END-IF
           STOP RUN.

       PARSE-ARGS.
           PERFORM UNTIL WS-POS > 248
               ADD 1 TO WS-POS
               IF WS-CMDLINE(WS-POS:8) = "--unique"
                   MOVE 1 TO UNIQUE-FLAG
               END-IF
               IF WS-CMDLINE(WS-POS:6) = "--tree"
                   MOVE 1 TO TREE-FLAG
               END-IF
               IF WS-CMDLINE(WS-POS:7) = "--depth"
                   ADD 8 TO WS-POS
                   MOVE 0 TO WS-DEPTH-NUM
                   PERFORM UNTIL WS-POS > 256
                       EVALUATE WS-CMDLINE(WS-POS:1)
                           WHEN "0"
                               COMPUTE WS-DEPTH-NUM =
                                   WS-DEPTH-NUM * 10
                           WHEN "1"
                               COMPUTE WS-DEPTH-NUM =
                                   WS-DEPTH-NUM * 10 + 1
                           WHEN "2"
                               COMPUTE WS-DEPTH-NUM =
                                   WS-DEPTH-NUM * 10 + 2
                           WHEN "3"
                               COMPUTE WS-DEPTH-NUM =
                                   WS-DEPTH-NUM * 10 + 3
                           WHEN "4"
                               COMPUTE WS-DEPTH-NUM =
                                   WS-DEPTH-NUM * 10 + 4
                           WHEN "5"
                               COMPUTE WS-DEPTH-NUM =
                                   WS-DEPTH-NUM * 10 + 5
                           WHEN "6"
                               COMPUTE WS-DEPTH-NUM =
                                   WS-DEPTH-NUM * 10 + 6
                           WHEN "7"
                               COMPUTE WS-DEPTH-NUM =
                                   WS-DEPTH-NUM * 10 + 7
                           WHEN "8"
                               COMPUTE WS-DEPTH-NUM =
                                   WS-DEPTH-NUM * 10 + 8
                           WHEN "9"
                               COMPUTE WS-DEPTH-NUM =
                                   WS-DEPTH-NUM * 10 + 9
                           WHEN OTHER
                               EXIT PERFORM
                       END-EVALUATE
                       ADD 1 TO WS-POS
                   END-PERFORM
                   MOVE WS-DEPTH-NUM TO MAX-DEPTH
               END-IF
           END-PERFORM.

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
               UNTIL WS-I > WS-DEPTH
               OR WS-CMP NOT = 0
               IF WS-TRANSFORMED(WS-I) < WS-GAME-SEQ(WS-I)
                   MOVE -1 TO WS-CMP
               ELSE
                   IF WS-TRANSFORMED(WS-I) >
                       WS-GAME-SEQ(WS-I)
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
               UNTIL WS-I > P1-CNT - 2 OR WS-IS-WIN = 1
               ADD 1 TO WS-I GIVING WS-J
               PERFORM UNTIL WS-J > P1-CNT - 1
                   OR WS-IS-WIN = 1
                   ADD 1 TO WS-J GIVING WS-K
                   PERFORM UNTIL WS-K > P1-CNT
                       OR WS-IS-WIN = 1
                       COMPUTE WS-SUM = P1-NUM(WS-I)
                           + P1-NUM(WS-J)
                           + P1-NUM(WS-K)
                       IF WS-SUM = 15
                           MOVE 1 TO WS-IS-WIN
                       END-IF
                       ADD 1 TO WS-K
                   END-PERFORM
                   ADD 1 TO WS-J
               END-PERFORM
           END-PERFORM.

       CHECK-P2-WIN.
           PERFORM VARYING WS-I FROM 1 BY 1
               UNTIL WS-I > P2-CNT - 2 OR WS-IS-WIN = 1
               ADD 1 TO WS-I GIVING WS-J
               PERFORM UNTIL WS-J > P2-CNT - 1
                   OR WS-IS-WIN = 1
                   ADD 1 TO WS-J GIVING WS-K
                   PERFORM UNTIL WS-K > P2-CNT
                       OR WS-IS-WIN = 1
                       COMPUTE WS-SUM = P2-NUM(WS-I)
                           + P2-NUM(WS-J)
                           + P2-NUM(WS-K)
                       IF WS-SUM = 15
                           MOVE 1 TO WS-IS-WIN
                       END-IF
                       ADD 1 TO WS-K
                   END-PERFORM
                   ADD 1 TO WS-J
               END-PERFORM
           END-PERFORM.

       INIT-TABLES.
           MOVE 1 TO POW3(1)
           MOVE 3 TO POW3(2)
           MOVE 9 TO POW3(3)
           MOVE 27 TO POW3(4)
           MOVE 81 TO POW3(5)
           MOVE 243 TO POW3(6)
           MOVE 729 TO POW3(7)
           MOVE 2187 TO POW3(8)
           MOVE 6561 TO POW3(9)
           MOVE 2 TO POW3X2(1)
           MOVE 6 TO POW3X2(2)
           MOVE 18 TO POW3X2(3)
           MOVE 54 TO POW3X2(4)
           MOVE 162 TO POW3X2(5)
           MOVE 486 TO POW3X2(6)
           MOVE 1458 TO POW3X2(7)
           MOVE 4374 TO POW3X2(8)
           MOVE 13122 TO POW3X2(9).

       COMPUTE-ALL.
           MOVE 0 TO MM-DEPTH
           MOVE 0 TO MM-P1-CNT
           MOVE 0 TO MM-P2-CNT
           MOVE 0 TO MM-SP
           MOVE 1 TO CACHE-KEY
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 9
               MOVE 0 TO MM-USED(WS-I)
           END-PERFORM
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 11
               MOVE 2 TO MM-STK-BEST(WS-I)
           END-PERFORM
           MOVE 1 TO MM-VAL
           MOVE 0 TO MM-DONE
           PERFORM UNTIL MM-DONE = 1
               PERFORM MM-STEP
           END-PERFORM.

       MM-STEP.
           IF MM-DEPTH = 9
               MOVE 0 TO CACHE-VAL(CACHE-KEY)
               ADD 1 TO CACHE-CNT(CACHE-KEY)
               PERFORM MM-BACK
           ELSE
               IF MM-VAL > 9
                   PERFORM MM-FIN
                   PERFORM MM-BACK
               ELSE
                   IF MM-USED(MM-VAL) = 0
                       PERFORM MM-MK
                   ELSE
                       ADD 1 TO MM-VAL
                   END-IF
               END-IF
           END-IF.

       MM-MK.
           MOVE 1 TO MM-USED(MM-VAL)
           ADD 1 TO MM-DEPTH
           DIVIDE MM-DEPTH BY 2 GIVING MM-QUO
               REMAINDER MM-REM
           IF MM-REM = 1
               ADD 1 TO MM-P1-CNT
               MOVE MM-VAL TO MM-P1-NUM(MM-P1-CNT)
               ADD POW3(MM-VAL) TO CACHE-KEY
           ELSE
               ADD 1 TO MM-P2-CNT
               MOVE MM-VAL TO MM-P2-NUM(MM-P2-CNT)
               ADD POW3X2(MM-VAL) TO CACHE-KEY
           END-IF
           ADD 1 TO MM-SP
           MOVE MM-VAL TO MM-STK-VAL(MM-SP)
           MOVE 0 TO MM-IS-WIN
           IF MM-REM = 1
               IF MM-P1-CNT >= 3
                   PERFORM MM-CHK-P1
               END-IF
           ELSE
               IF MM-P2-CNT >= 3
                   PERFORM MM-CHK-P2
               END-IF
           END-IF
           IF MM-IS-WIN = 1
               IF MM-REM = 1
                   MOVE 1 TO CACHE-VAL(CACHE-KEY)
                   MOVE 1 TO MM-STK-BEST(MM-SP)
               ELSE
                   MOVE -1 TO CACHE-VAL(CACHE-KEY)
                   MOVE -1 TO MM-STK-BEST(MM-SP)
               END-IF
               ADD 1 TO CACHE-CNT(CACHE-KEY)
               MOVE 10 TO MM-VAL
           ELSE
               IF MM-DEPTH = 9
                   MOVE 0 TO CACHE-VAL(CACHE-KEY)
                   MOVE 0 TO MM-STK-BEST(MM-SP)
                   ADD 1 TO CACHE-CNT(CACHE-KEY)
                   MOVE 10 TO MM-VAL
               ELSE
                   DIVIDE MM-DEPTH BY 2 GIVING MM-QUO
                       REMAINDER MM-REM
                   IF MM-REM = 0
                       MOVE -2 TO MM-STK-BEST(MM-SP)
                   ELSE
                       MOVE 2 TO MM-STK-BEST(MM-SP)
                   END-IF
                   MOVE 1 TO MM-VAL
               END-IF
           END-IF.

       MM-FIN.
           IF MM-SP > 0
               MOVE MM-STK-BEST(MM-SP) TO CACHE-VAL(CACHE-KEY)
           END-IF.

       MM-BACK.
           IF MM-DEPTH > 0
               MOVE MM-STK-BEST(MM-SP) TO MM-CUR
               IF MM-SP > 1
                   DIVIDE MM-DEPTH BY 2 GIVING MM-QUO
                       REMAINDER MM-REM
                   IF MM-REM = 0
                       IF MM-CUR > MM-STK-BEST(MM-SP - 1)
                           MOVE MM-CUR TO
                               MM-STK-BEST(MM-SP - 1)
                       END-IF
                   ELSE
                       IF MM-CUR < MM-STK-BEST(MM-SP - 1)
                           MOVE MM-CUR TO
                               MM-STK-BEST(MM-SP - 1)
                       END-IF
                   END-IF
               END-IF
               DIVIDE MM-DEPTH BY 2 GIVING MM-QUO
                   REMAINDER MM-REM
               IF MM-REM = 1
                   SUBTRACT 1 FROM MM-P1-CNT
                   MOVE MM-P1-NUM(MM-P1-CNT + 1) TO MM-VAL
                   SUBTRACT POW3(MM-VAL) FROM CACHE-KEY
               ELSE
                   SUBTRACT 1 FROM MM-P2-CNT
                   MOVE MM-P2-NUM(MM-P2-CNT + 1) TO MM-VAL
                   SUBTRACT POW3X2(MM-VAL) FROM CACHE-KEY
               END-IF
               MOVE 0 TO MM-USED(MM-VAL)
               SUBTRACT 1 FROM MM-DEPTH
               MOVE MM-STK-VAL(MM-SP) TO MM-VAL
               SUBTRACT 1 FROM MM-SP
               ADD 1 TO MM-VAL
           ELSE
               MOVE 1 TO MM-DONE
           END-IF.

       MM-CHK-P1.
           PERFORM VARYING MM-I FROM 1 BY 1
               UNTIL MM-I > MM-P1-CNT - 2 OR MM-IS-WIN = 1
               ADD 1 TO MM-I GIVING MM-J
               PERFORM UNTIL MM-J > MM-P1-CNT - 1
                   OR MM-IS-WIN = 1
                   ADD 1 TO MM-J GIVING MM-K
                   PERFORM UNTIL MM-K > MM-P1-CNT
                       OR MM-IS-WIN = 1
                       COMPUTE MM-SUM = MM-P1-NUM(MM-I)
                           + MM-P1-NUM(MM-J)
                           + MM-P1-NUM(MM-K)
                       IF MM-SUM = 15
                           MOVE 1 TO MM-IS-WIN
                       END-IF
                       ADD 1 TO MM-K
                   END-PERFORM
                   ADD 1 TO MM-J
               END-PERFORM
           END-PERFORM.

       MM-CHK-P2.
           PERFORM VARYING MM-I FROM 1 BY 1
               UNTIL MM-I > MM-P2-CNT - 2 OR MM-IS-WIN = 1
               ADD 1 TO MM-I GIVING MM-J
               PERFORM UNTIL MM-J > MM-P2-CNT - 1
                   OR MM-IS-WIN = 1
                   ADD 1 TO MM-J GIVING MM-K
                   PERFORM UNTIL MM-K > MM-P2-CNT
                       OR MM-IS-WIN = 1
                       COMPUTE MM-SUM = MM-P2-NUM(MM-I)
                           + MM-P2-NUM(MM-J)
                           + MM-P2-NUM(MM-K)
                       IF MM-SUM = 15
                           MOVE 1 TO MM-IS-WIN
                       END-IF
                       ADD 1 TO MM-K
                   END-PERFORM
                   ADD 1 TO MM-J
               END-PERFORM
           END-PERFORM.

       TREE-COMPUTE-VAL.
           MOVE TREE-DEPTH TO MM-DEPTH
           MOVE TREE-P1-CNT TO MM-P1-CNT
           MOVE TREE-P2-CNT TO MM-P2-CNT
           MOVE 0 TO MM-SP
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 9
               MOVE TREE-P1-NUM(WS-I) TO MM-P1-NUM(WS-I)
               MOVE TREE-P2-NUM(WS-I) TO MM-P2-NUM(WS-I)
               IF TREE-USED(WS-I) = 0
                   MOVE 0 TO MM-USED(WS-I)
               ELSE
                   MOVE 1 TO MM-USED(WS-I)
               END-IF
           END-PERFORM
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 11
               MOVE 2 TO MM-STK-BEST(WS-I)
           END-PERFORM
           MOVE 1 TO MM-VAL
           MOVE 0 TO MM-DONE
           PERFORM UNTIL MM-DONE = 1
               PERFORM MM-STEP
           END-PERFORM
           IF MM-SP > 0
               MOVE MM-STK-BEST(MM-SP) TO WS-CVAL
           ELSE
               MOVE 0 TO WS-CVAL
           END-IF.

       COMPUTE-ROOT-CNT.
           MOVE 0 TO CNT-DEPTH
           MOVE 0 TO CNT-P1-CNT
           MOVE 0 TO CNT-P2-CNT
           MOVE 0 TO CNT-SP
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 9
               MOVE 0 TO CNT-USED(WS-I)
           END-PERFORM
           MOVE 1 TO CNT-VAL
           MOVE 0 TO CNT-DONE
           MOVE 0 TO CNT-RESULT
           PERFORM UNTIL CNT-DONE = 1
               PERFORM CNT-STEP
           END-PERFORM
           MOVE CNT-RESULT TO WS-TOT-STR.

       CNT-STEP.
           IF CNT-DEPTH = 9
               ADD 1 TO CNT-RESULT
               PERFORM CNT-BACK
           ELSE
               IF CNT-VAL > 9
                   PERFORM CNT-BACK
               ELSE
                   IF CNT-USED(CNT-VAL) = 0
                       PERFORM CNT-MK
                   ELSE
                       ADD 1 TO CNT-VAL
                   END-IF
               END-IF
           END-IF.

       CNT-MK.
           MOVE 1 TO CNT-USED(CNT-VAL)
           ADD 1 TO CNT-DEPTH
           DIVIDE CNT-DEPTH BY 2 GIVING CNT-QUO
               REMAINDER CNT-REM
           IF CNT-REM = 1
               ADD 1 TO CNT-P1-CNT
               MOVE CNT-VAL TO CNT-P1-NUM(CNT-P1-CNT)
           ELSE
               ADD 1 TO CNT-P2-CNT
               MOVE CNT-VAL TO CNT-P2-NUM(CNT-P2-CNT)
           END-IF
           ADD 1 TO CNT-SP
           MOVE CNT-VAL TO CNT-STK-VAL(CNT-SP)
           MOVE 0 TO CNT-IS-WIN
           IF CNT-REM = 1
               IF CNT-P1-CNT >= 3
                   PERFORM CNT-CHK-P1
               END-IF
           ELSE
               IF CNT-P2-CNT >= 3
                   PERFORM CNT-CHK-P2
               END-IF
           END-IF
           IF CNT-IS-WIN = 1
               ADD 1 TO CNT-RESULT
               PERFORM CNT-BACK
           ELSE
               MOVE 1 TO CNT-VAL
           END-IF.

       CNT-BACK.
           IF CNT-DEPTH > 0
               DIVIDE CNT-DEPTH BY 2 GIVING CNT-QUO
                   REMAINDER CNT-REM
               IF CNT-REM = 1
                   SUBTRACT 1 FROM CNT-P1-CNT
                   MOVE CNT-P1-NUM(CNT-P1-CNT + 1) TO CNT-VAL
               ELSE
                   SUBTRACT 1 FROM CNT-P2-CNT
                   MOVE CNT-P2-NUM(CNT-P2-CNT + 1) TO CNT-VAL
               END-IF
               MOVE 0 TO CNT-USED(CNT-VAL)
               SUBTRACT 1 FROM CNT-DEPTH
               IF CNT-SP > 0
                   MOVE CNT-STK-VAL(CNT-SP) TO CNT-VAL
                   SUBTRACT 1 FROM CNT-SP
                   ADD 1 TO CNT-VAL
               ELSE
                   ADD 1 TO CNT-VAL
               END-IF
           ELSE
               MOVE 1 TO CNT-DONE
           END-IF.

       CNT-CHK-P1.
           PERFORM VARYING WS-I FROM 1 BY 1
               UNTIL WS-I > CNT-P1-CNT - 2 OR CNT-IS-WIN = 1
               ADD 1 TO WS-I GIVING WS-J
               PERFORM UNTIL WS-J > CNT-P1-CNT - 1
                   OR CNT-IS-WIN = 1
                   ADD 1 TO WS-J GIVING WS-K
                   PERFORM UNTIL WS-K > CNT-P1-CNT
                       OR CNT-IS-WIN = 1
                       COMPUTE CNT-SUM = CNT-P1-NUM(WS-I)
                           + CNT-P1-NUM(WS-J)
                           + CNT-P1-NUM(WS-K)
                       IF CNT-SUM = 15
                           MOVE 1 TO CNT-IS-WIN
                       END-IF
                       ADD 1 TO WS-K
                   END-PERFORM
                   ADD 1 TO WS-J
               END-PERFORM
           END-PERFORM.

       CNT-CHK-P2.
           PERFORM VARYING WS-I FROM 1 BY 1
               UNTIL WS-I > CNT-P2-CNT - 2 OR CNT-IS-WIN = 1
               ADD 1 TO WS-I GIVING WS-J
               PERFORM UNTIL WS-J > CNT-P2-CNT - 1
                   OR CNT-IS-WIN = 1
                   ADD 1 TO WS-J GIVING WS-K
                   PERFORM UNTIL WS-K > CNT-P2-CNT
                       OR CNT-IS-WIN = 1
                       COMPUTE CNT-SUM = CNT-P2-NUM(WS-I)
                           + CNT-P2-NUM(WS-J)
                           + CNT-P2-NUM(WS-K)
                       IF CNT-SUM = 15
                           MOVE 1 TO CNT-IS-WIN
                       END-IF
                       ADD 1 TO WS-K
                   END-PERFORM
                   ADD 1 TO WS-J
               END-PERFORM
           END-PERFORM.

       PRINT-TREE.
           DISPLAY "Game of 15 -- Optimal Play Tree"
           DISPLAY "==============================="
           DISPLAY " "
           DISPLAY "Legend: P1+ = P1 wins  |"
               " P2+ = P2 wins  |  D = Draw"
           DISPLAY " "
           DISPLAY "Branches = safe/optimal moves"
           DISPLAY "Avoid    = moves that lose"
           DISPLAY "Depth limit: " MAX-DEPTH
           DISPLAY " "
           PERFORM FMT-VAL
           DISPLAY "Root [" WS-VSTR "] ("
               WS-TOT-STR " games)"
           DISPLAY " "

           MOVE 0 TO TREE-DEPTH
           MOVE 0 TO TREE-P1-CNT
           MOVE 0 TO TREE-P2-CNT
           MOVE 1 TO TREE-KEY
           MOVE 0 TO TREE-PVAL
           PERFORM VARYING WS-I FROM 1 BY 1
               UNTIL WS-I > 9
               MOVE 0 TO TREE-USED(WS-I)
           END-PERFORM
           MOVE 1 TO TREE-VAL
           MOVE 0 TO TREE-STACK-POS
           PERFORM TREE-WALK.

       FMT-VAL.
           IF WS-CVAL = 1
               MOVE "P1+" TO WS-VSTR
           ELSE
               IF WS-CVAL = -1
                   MOVE "P2+" TO WS-VSTR
               ELSE
                   MOVE "D  " TO WS-VSTR
               END-IF
           END-IF.

       FMT-MOVE.
           IF WS-CVAL = 1
               MOVE "P1+" TO WS-MOVE-STR
           ELSE
               IF WS-CVAL = -1
                   MOVE "P2+" TO WS-MOVE-STR
               ELSE
                   MOVE "D  " TO WS-MOVE-STR
               END-IF
           END-IF.

       TREE-WALK.
           PERFORM UNTIL TREE-VAL > 9
               IF TREE-USED(TREE-VAL) = 0
                   PERFORM TREE-VISIT
               END-IF
               ADD 1 TO TREE-VAL
           END-PERFORM.

       TREE-VISIT.
           MOVE 1 TO TREE-USED(TREE-VAL)
           ADD 1 TO TREE-DEPTH
           DIVIDE TREE-DEPTH BY 2 GIVING TREE-QUO
               REMAINDER TREE-REM
           IF TREE-REM = 1
               ADD 1 TO TREE-P1-CNT
               MOVE TREE-VAL TO TREE-P1-NUM(TREE-P1-CNT)
               ADD POW3(TREE-VAL) TO TREE-KEY
           ELSE
               ADD 1 TO TREE-P2-CNT
               MOVE TREE-VAL TO TREE-P2-NUM(TREE-P2-CNT)
               ADD POW3X2(TREE-VAL) TO TREE-KEY
           END-IF

            IF TREE-DEPTH >= MAX-DEPTH
                MOVE TREE-VAL TO WS-NUM-STR
                DISPLAY "  ... (depth limit)"
            ELSE
                PERFORM TREE-COMPUTE-VAL
                PERFORM FMT-MOVE
                MOVE TREE-VAL TO WS-NUM-STR

                IF TREE-PVAL = 0
                    IF TREE-REM = 1
                        DISPLAY "  |-- P1=" WS-NUM-STR
                            " [" WS-MOVE-STR "]"
                    ELSE
                        DISPLAY "  |-- P2=" WS-NUM-STR
                            " [" WS-MOVE-STR "]"
                    END-IF
                ELSE
                    IF TREE-REM = 1
                        IF WS-CVAL >= TREE-PVAL
                            DISPLAY "  |-- P1=" WS-NUM-STR
                                " [" WS-MOVE-STR "]"
                        ELSE
                            DISPLAY "  AVOID P1=" WS-NUM-STR
                                " [" WS-MOVE-STR "]"
                        END-IF
                    ELSE
                        IF WS-CVAL <= TREE-PVAL
                            DISPLAY "  |-- P2=" WS-NUM-STR
                                " [" WS-MOVE-STR "]"
                        ELSE
                            DISPLAY "  AVOID P2=" WS-NUM-STR
                                " [" WS-MOVE-STR "]"
                        END-IF
                    END-IF
                END-IF

                ADD 1 TO TREE-STACK-POS
                MOVE TREE-PVAL TO
                    TREE-STACK-PVAL(TREE-STACK-POS)
                MOVE TREE-VAL TO
                    TREE-STACK-LOOP(TREE-STACK-POS)
                MOVE TREE-DEPTH TO
                    TREE-STACK-DEPTH(TREE-STACK-POS)
                MOVE TREE-P1-CNT TO
                    TREE-STACK-P1C(TREE-STACK-POS)
                MOVE TREE-P2-CNT TO
                    TREE-STACK-P2C(TREE-STACK-POS)
                PERFORM VARYING WS-I FROM 1 BY 1
                    UNTIL WS-I > 9
                    COMPUTE WS-J = (TREE-STACK-POS - 1)
                        * 9 + WS-I
                    MOVE TREE-P1-NUM(WS-I) TO
                        TREE-STACK-P1N(WS-J)
                    MOVE TREE-P2-NUM(WS-I) TO
                        TREE-STACK-P2N(WS-J)
                    MOVE TREE-USED(WS-I) TO
                        TREE-STACK-USED(WS-J)
                END-PERFORM
                MOVE WS-CVAL TO TREE-PVAL
                MOVE 1 TO TREE-VAL
                PERFORM TREE-WALK
                MOVE TREE-STACK-PVAL(TREE-STACK-POS) TO
                    TREE-PVAL
                MOVE TREE-STACK-LOOP(TREE-STACK-POS) TO
                    TREE-VAL
                MOVE TREE-STACK-DEPTH(TREE-STACK-POS) TO
                    TREE-DEPTH
                MOVE TREE-STACK-P1C(TREE-STACK-POS) TO
                    TREE-P1-CNT
                MOVE TREE-STACK-P2C(TREE-STACK-POS) TO
                    TREE-P2-CNT
                PERFORM VARYING WS-I FROM 1 BY 1
                    UNTIL WS-I > 9
                    COMPUTE WS-J = (TREE-STACK-POS - 1)
                        * 9 + WS-I
                    MOVE TREE-STACK-P1N(WS-J) TO
                        TREE-P1-NUM(WS-I)
                    MOVE TREE-STACK-P2N(WS-J) TO
                        TREE-P2-NUM(WS-I)
                    MOVE TREE-STACK-USED(WS-J) TO
                        TREE-USED(WS-I)
                END-PERFORM
                SUBTRACT 1 FROM TREE-STACK-POS
            END-IF

           DIVIDE TREE-DEPTH BY 2 GIVING TREE-QUO
               REMAINDER TREE-REM
           IF TREE-REM = 1
               SUBTRACT 1 FROM TREE-P1-CNT
               SUBTRACT POW3(TREE-VAL) FROM TREE-KEY
           ELSE
               SUBTRACT 1 FROM TREE-P2-CNT
               SUBTRACT POW3X2(TREE-VAL) FROM TREE-KEY
           END-IF
           MOVE 0 TO TREE-USED(TREE-VAL)
           SUBTRACT 1 FROM TREE-DEPTH.
