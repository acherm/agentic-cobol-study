       IDENTIFICATION DIVISION.
       PROGRAM-ID. GAME15-TREE.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

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

       01  WS-CVAL          PIC S9 VALUE ZERO.
       01  WS-VSTR          PIC X(3) VALUE SPACES.
       01  WS-CNT-STR       PIC Z(9)9 VALUE ZERO.
       01  WS-TOT-STR       PIC Z(9)9 VALUE ZERO.
       01  WS-NUM-STR       PIC Z9 VALUE ZERO.

       01  POW3             PIC 9(5) OCCURS 9 TIMES.
       01  POW3X2           PIC 9(5) OCCURS 9 TIMES.

       01  CACHE-VAL        PIC S9 OCCURS 19684 TIMES.
       01  CACHE-CNT        PIC 9(10) OCCURS 19684 TIMES.
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
       01  MM-STK-BEST      PIC S9 OCCURS 11 TIMES VALUE ZERO.
       01  MM-CUR           PIC S9 VALUE ZERO.
       01  MM-RESULT        PIC S9 VALUE ZERO.

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

       01  SAVE-VAL         PIC 99 VALUE ZERO.
       01  SAVE-DEPTH       PIC 99 VALUE ZERO.
       01  SAVE-P1C         PIC 99 VALUE ZERO.
       01  SAVE-P2C         PIC 99 VALUE ZERO.
       01  SAVE-DONE        PIC 9 VALUE ZERO.
       01  SAVE-USED        PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  SAVE-P1N         PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  SAVE-P2N         PIC 9 OCCURS 9 TIMES VALUE ZERO.
       01  SAVE-KEY         PIC 9(5) VALUE ZERO.

       01  WS-ITER          PIC 9(10) VALUE ZERO.

       PROCEDURE DIVISION.
           PERFORM INIT-TABLES
           PERFORM INIT-CACHE
           PERFORM COMPUTE-ALL
           PERFORM COMPUTE-ROOT-CNT
           PERFORM PRINT-TREE
           STOP RUN.

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

       INIT-CACHE.
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 19683
               MOVE 2 TO CACHE-VAL(WS-I)
               MOVE 0 TO CACHE-CNT(WS-I)
           END-PERFORM.

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
           MOVE 0 TO WS-ITER
           PERFORM UNTIL MM-DONE = 1
               ADD 1 TO WS-ITER
               IF WS-ITER = 100000
                   DISPLAY "Iter=" WS-ITER " D=" MM-DEPTH
                   MOVE 0 TO WS-ITER
               END-IF
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
               END-IF
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
           PERFORM VARYING WS-I FROM 1 BY 1
               UNTIL WS-I > MM-P1-CNT - 2 OR MM-IS-WIN = 1
               ADD 1 TO WS-I GIVING WS-J
               PERFORM UNTIL WS-J > MM-P1-CNT - 1
                   OR MM-IS-WIN = 1
                   ADD 1 TO WS-J GIVING WS-K
                   PERFORM UNTIL WS-K > MM-P1-CNT
                       OR MM-IS-WIN = 1
                       COMPUTE MM-SUM = MM-P1-NUM(WS-I)
                           + MM-P1-NUM(WS-J)
                           + MM-P1-NUM(WS-K)
                       IF MM-SUM = 15
                           MOVE 1 TO MM-IS-WIN
                       END-IF
                       ADD 1 TO WS-K
                   END-PERFORM
                   ADD 1 TO WS-J
               END-PERFORM
           END-PERFORM.

       MM-CHK-P2.
           PERFORM VARYING WS-I FROM 1 BY 1
               UNTIL WS-I > MM-P2-CNT - 2 OR MM-IS-WIN = 1
               ADD 1 TO WS-I GIVING WS-J
               PERFORM UNTIL WS-J > MM-P2-CNT - 1
                   OR MM-IS-WIN = 1
                   ADD 1 TO WS-J GIVING WS-K
                   PERFORM UNTIL WS-K > MM-P2-CNT
                       OR MM-IS-WIN = 1
                       COMPUTE MM-SUM = MM-P2-NUM(WS-I)
                           + MM-P2-NUM(WS-J)
                           + MM-P2-NUM(WS-K)
                       IF MM-SUM = 15
                           MOVE 1 TO MM-IS-WIN
                       END-IF
                       ADD 1 TO WS-K
                   END-PERFORM
                   ADD 1 TO WS-J
               END-PERFORM
           END-PERFORM.

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
           MOVE CACHE-VAL(1) TO WS-CVAL
           PERFORM FMT-VAL
           DISPLAY "Root [" WS-VSTR "] (" WS-TOT-STR " games)"
           DISPLAY " "

           MOVE 0 TO WS-DEPTH
           MOVE 0 TO P1-CNT
           MOVE 0 TO P2-CNT
           MOVE 1 TO CACHE-KEY
           PERFORM VARYING WS-I FROM 1 BY 1 UNTIL WS-I > 9
               MOVE 0 TO USED-FLG(WS-I)
           END-PERFORM
           MOVE 1 TO WS-VAL
           MOVE 0 TO WS-DONE
           PERFORM PRT-LOOP.

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

       PRT-LOOP.
           PERFORM UNTIL WS-DONE = 1
               IF WS-VAL > 9
                   PERFORM PRT-BACK
               ELSE
                   IF USED-FLG(WS-VAL) = 0
                       PERFORM PRT-DESCEND
                   ELSE
                       ADD 1 TO WS-VAL
                   END-IF
               END-IF
           END-PERFORM.

       PRT-DESCEND.
           MOVE 1 TO USED-FLG(WS-VAL)
           ADD 1 TO WS-DEPTH
           DIVIDE WS-DEPTH BY 2 GIVING WS-QUO
               REMAINDER WS-REM
           IF WS-REM = 1
               ADD 1 TO P1-CNT
               MOVE WS-VAL TO P1-NUM(P1-CNT)
               ADD POW3(WS-VAL) TO CACHE-KEY
           ELSE
               ADD 1 TO P2-CNT
               MOVE WS-VAL TO P2-NUM(P2-CNT)
               ADD POW3X2(WS-VAL) TO CACHE-KEY
           END-IF

           MOVE CACHE-VAL(CACHE-KEY) TO WS-CVAL
           MOVE CACHE-CNT(CACHE-KEY) TO WS-CNT-STR
           PERFORM FMT-VAL

           MOVE WS-VAL TO WS-NUM-STR
           IF WS-DEPTH = 1
               DISPLAY "  |-- P1=" WS-NUM-STR
                   " [" WS-VSTR "] (" WS-CNT-STR " games)"
           ELSE
               IF WS-REM = 1
                   DISPLAY "  |-- P1=" WS-NUM-STR
                       " [" WS-VSTR "] (" WS-CNT-STR " games)"
               ELSE
                   DISPLAY "  |-- P2=" WS-NUM-STR
                       " [" WS-VSTR "] (" WS-CNT-STR " games)"
               END-IF
           END-IF

           IF WS-CNT-STR <= 0000000006
               MOVE WS-VAL TO SAVE-VAL
               MOVE WS-DEPTH TO SAVE-DEPTH
               MOVE P1-CNT TO SAVE-P1C
               MOVE P2-CNT TO SAVE-P2C
               MOVE CACHE-KEY TO SAVE-KEY
               MOVE WS-DONE TO SAVE-DONE
               PERFORM VARYING WS-I FROM 1 BY 1
                   UNTIL WS-I > 9
                   MOVE USED-FLG(WS-I) TO SAVE-USED(WS-I)
                   MOVE P1-NUM(WS-I) TO SAVE-P1N(WS-I)
                   MOVE P2-NUM(WS-I) TO SAVE-P2N(WS-I)
               END-PERFORM
               MOVE 0 TO WS-DONE
               MOVE 1 TO WS-VAL
               PERFORM PRT-LOOP
               MOVE SAVE-VAL TO WS-VAL
               MOVE SAVE-DEPTH TO WS-DEPTH
               MOVE SAVE-P1C TO P1-CNT
               MOVE SAVE-P2C TO P2-CNT
               MOVE SAVE-KEY TO CACHE-KEY
               MOVE SAVE-DONE TO WS-DONE
               PERFORM VARYING WS-I FROM 1 BY 1
                   UNTIL WS-I > 9
                   MOVE SAVE-USED(WS-I) TO USED-FLG(WS-I)
                   MOVE SAVE-P1N(WS-I) TO P1-NUM(WS-I)
                   MOVE SAVE-P2N(WS-I) TO P2-NUM(WS-I)
               END-PERFORM
               MOVE 1 TO USED-FLG(WS-VAL)
           ELSE
               MOVE 10 TO WS-VAL
           END-IF.

       PRT-BACK.
           IF WS-DEPTH > 0
               DIVIDE WS-DEPTH BY 2 GIVING WS-QUO
                   REMAINDER WS-REM
               IF WS-REM = 1
                   SUBTRACT 1 FROM P1-CNT
                   MOVE P1-NUM(P1-CNT + 1) TO WS-VAL
                   SUBTRACT POW3(WS-VAL) FROM CACHE-KEY
               ELSE
                   SUBTRACT 1 FROM P2-CNT
                   MOVE P2-NUM(P2-CNT + 1) TO WS-VAL
                   SUBTRACT POW3X2(WS-VAL) FROM CACHE-KEY
               END-IF
               MOVE 0 TO USED-FLG(WS-VAL)
               SUBTRACT 1 FROM WS-DEPTH
               ADD 1 TO WS-VAL
           ELSE
               MOVE 1 TO WS-DONE
           END-IF.
