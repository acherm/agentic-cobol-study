       IDENTIFICATION DIVISION.
       PROGRAM-ID. GAME15.

       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  COUNTERS.
           05  P1-WINS      PIC 9(7) VALUE 0.
           05  P2-WINS      PIC 9(7) VALUE 0.
           05  DRAWS        PIC 9(7) VALUE 0.
           05  TOTAL-GAMES  PIC 9(7) VALUE 0.

       01  PERMUTATION.
           05  NUM          PIC 9(2) OCCURS 9 TIMES.

       01  HANDS.
           05  P1-HAND.
               10  P1-NUM   PIC 9(2) OCCURS 5 TIMES VALUE 0.
           05  P2-HAND.
               10  P2-NUM   PIC 9(2) OCCURS 4 TIMES VALUE 0.

       01  GAME-STATE.
           05  P1-COUNT     PIC 9(2) VALUE 0.
           05  P2-COUNT     PIC 9(2) VALUE 0.
           05  GAME-ENDED   PIC X VALUE 'N'.
               88  END-OF-GAME VALUE 'Y'.

       01  WINNING-NUMBERS.
           05  WIN1N1 PIC 9(2) VALUE 1.
           05  WIN1N2 PIC 9(2) VALUE 5.
           05  WIN1N3 PIC 9(2) VALUE 9.
           05  WIN2N1 PIC 9(2) VALUE 1.
           05  WIN2N2 PIC 9(2) VALUE 6.
           05  WIN2N3 PIC 9(2) VALUE 8.
           05  WIN3N1 PIC 9(2) VALUE 2.
           05  WIN3N2 PIC 9(2) VALUE 4.
           05  WIN3N3 PIC 9(2) VALUE 9.
           05  WIN4N1 PIC 9(2) VALUE 2.
           05  WIN4N2 PIC 9(2) VALUE 5.
           05  WIN4N3 PIC 9(2) VALUE 8.
           05  WIN5N1 PIC 9(2) VALUE 2.
           05  WIN5N2 PIC 9(2) VALUE 6.
           05  WIN5N3 PIC 9(2) VALUE 7.
           05  WIN6N1 PIC 9(2) VALUE 3.
           05  WIN6N2 PIC 9(2) VALUE 4.
           05  WIN6N3 PIC 9(2) VALUE 8.
           05  WIN7N1 PIC 9(2) VALUE 3.
           05  WIN7N2 PIC 9(2) VALUE 5.
           05  WIN7N3 PIC 9(2) VALUE 7.
           05  WIN8N1 PIC 9(2) VALUE 4.
           05  WIN8N2 PIC 9(2) VALUE 5.
           05  WIN8N3 PIC 9(2) VALUE 6.

       01  WORK-VARS.
           05  I            PIC 9(2).
           05  K            PIC 9(2).
           05  MOVE-NO      PIC 9(2).
           05  CURR-NUM     PIC 9(2).
           05  TEMP         PIC 9(2).
           05  MOD-RESULT   PIC 9(2).
           05  ALL-DONE     PIC X VALUE 'N'.
               88  ALL-PERMS-DONE VALUE 'Y'.
           05  HAS-N1       PIC X VALUE 'N'.
               88  HAS-NUM1 VALUE 'Y'.
           05  HAS-N2       PIC X VALUE 'N'.
               88  HAS-NUM2 VALUE 'Y'.
           05  HAS-N3       PIC X VALUE 'N'.
               88  HAS-NUM3 VALUE 'Y'.
           05  P1-WON       PIC X VALUE 'N'.
               88  P1-WINS-GAME VALUE 'Y'.
           05  P2-WON       PIC X VALUE 'N'.
               88  P2-WINS-GAME VALUE 'Y'.

       01  PERM-GEN.
           05  K1           PIC 9(2).
           05  K2           PIC 9(2).
           05  SWAP-TEMP    PIC 9(2).
           05  START-IDX    PIC 9(2).
           05  END-IDX      PIC 9(2).

       PROCEDURE DIVISION.
       MAIN-LOGIC.
           PERFORM INIT-WINNING-NUMBERS
           PERFORM INIT-FIRST-PERM
           PERFORM PROCESS-CURRENT-PERM
           PERFORM UNTIL ALL-PERMS-DONE
               PERFORM NEXT-PERMUTATION
               IF NOT ALL-PERMS-DONE
                   PERFORM PROCESS-CURRENT-PERM
               END-IF
           END-PERFORM
           PERFORM DISPLAY-RESULTS
           STOP RUN.

       INIT-WINNING-NUMBERS.
           MOVE 1 TO WIN1N1
           MOVE 5 TO WIN1N2
           MOVE 9 TO WIN1N3
           MOVE 1 TO WIN2N1
           MOVE 6 TO WIN2N2
           MOVE 8 TO WIN2N3
           MOVE 2 TO WIN3N1
           MOVE 4 TO WIN3N2
           MOVE 9 TO WIN3N3
           MOVE 2 TO WIN4N1
           MOVE 5 TO WIN4N2
           MOVE 8 TO WIN4N3
           MOVE 2 TO WIN5N1
           MOVE 6 TO WIN5N2
           MOVE 7 TO WIN5N3
           MOVE 3 TO WIN6N1
           MOVE 4 TO WIN6N2
           MOVE 8 TO WIN6N3
           MOVE 3 TO WIN7N1
           MOVE 5 TO WIN7N2
           MOVE 7 TO WIN7N3
           MOVE 4 TO WIN8N1
           MOVE 5 TO WIN8N2
           MOVE 6 TO WIN8N3.

       INIT-FIRST-PERM.
           MOVE 1 TO NUM(1)
           MOVE 2 TO NUM(2)
           MOVE 3 TO NUM(3)
           MOVE 4 TO NUM(4)
           MOVE 5 TO NUM(5)
           MOVE 6 TO NUM(6)
           MOVE 7 TO NUM(7)
           MOVE 8 TO NUM(8)
           MOVE 9 TO NUM(9).

       PROCESS-CURRENT-PERM.
           ADD 1 TO TOTAL-GAMES
           MOVE 0 TO P1-COUNT P2-COUNT
           MOVE 'N' TO GAME-ENDED P1-WON P2-WON

           PERFORM VARYING MOVE-NO FROM 1 BY 1
                   UNTIL MOVE-NO > 9 OR END-OF-GAME
               MOVE NUM(MOVE-NO) TO CURR-NUM
               COMPUTE MOD-RESULT = FUNCTION MOD(MOVE-NO 2)
               IF MOD-RESULT = 1
                   ADD 1 TO P1-COUNT
                   MOVE CURR-NUM TO P1-NUM(P1-COUNT)
                   IF P1-COUNT >= 3
                       PERFORM CHECK-WIN-FOR-P1
                   END-IF
                   IF P1-WINS-GAME
                       ADD 1 TO P1-WINS
                       SET END-OF-GAME TO TRUE
                   END-IF
               ELSE
                   ADD 1 TO P2-COUNT
                   MOVE CURR-NUM TO P2-NUM(P2-COUNT)
                   IF P2-COUNT >= 3
                       PERFORM CHECK-WIN-FOR-P2
                   END-IF
                   IF P2-WINS-GAME
                       ADD 1 TO P2-WINS
                       SET END-OF-GAME TO TRUE
                   END-IF
               END-IF
           END-PERFORM

           IF NOT END-OF-GAME
               ADD 1 TO DRAWS
           END-IF.

       CHECK-WIN-FOR-P1.
           MOVE 'N' TO P1-WON
           PERFORM CHECK-TRIPLE-1-FOR-P1
           IF P1-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-2-FOR-P1
           IF P1-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-3-FOR-P1
           IF P1-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-4-FOR-P1
           IF P1-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-5-FOR-P1
           IF P1-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-6-FOR-P1
           IF P1-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-7-FOR-P1
           IF P1-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-8-FOR-P1.

       CHECK-WIN-FOR-P2.
           MOVE 'N' TO P2-WON
           PERFORM CHECK-TRIPLE-1-FOR-P2
           IF P2-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-2-FOR-P2
           IF P2-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-3-FOR-P2
           IF P2-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-4-FOR-P2
           IF P2-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-5-FOR-P2
           IF P2-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-6-FOR-P2
           IF P2-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-7-FOR-P2
           IF P2-WINS-GAME EXIT PARAGRAPH
           PERFORM CHECK-TRIPLE-8-FOR-P2.

       CHECK-TRIPLE-1-FOR-P1.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P1-COUNT
               IF P1-NUM(K) = WIN1N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P1-NUM(K) = WIN1N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P1-NUM(K) = WIN1N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P1-WON
           END-IF.

       CHECK-TRIPLE-2-FOR-P1.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P1-COUNT
               IF P1-NUM(K) = WIN2N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P1-NUM(K) = WIN2N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P1-NUM(K) = WIN2N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P1-WON
           END-IF.

       CHECK-TRIPLE-3-FOR-P1.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P1-COUNT
               IF P1-NUM(K) = WIN3N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P1-NUM(K) = WIN3N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P1-NUM(K) = WIN3N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P1-WON
           END-IF.

       CHECK-TRIPLE-4-FOR-P1.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P1-COUNT
               IF P1-NUM(K) = WIN4N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P1-NUM(K) = WIN4N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P1-NUM(K) = WIN4N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P1-WON
           END-IF.

       CHECK-TRIPLE-5-FOR-P1.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P1-COUNT
               IF P1-NUM(K) = WIN5N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P1-NUM(K) = WIN5N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P1-NUM(K) = WIN5N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P1-WON
           END-IF.

       CHECK-TRIPLE-6-FOR-P1.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P1-COUNT
               IF P1-NUM(K) = WIN6N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P1-NUM(K) = WIN6N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P1-NUM(K) = WIN6N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P1-WON
           END-IF.

       CHECK-TRIPLE-7-FOR-P1.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P1-COUNT
               IF P1-NUM(K) = WIN7N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P1-NUM(K) = WIN7N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P1-NUM(K) = WIN7N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P1-WON
           END-IF.

       CHECK-TRIPLE-8-FOR-P1.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P1-COUNT
               IF P1-NUM(K) = WIN8N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P1-NUM(K) = WIN8N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P1-NUM(K) = WIN8N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P1-WON
           END-IF.

       CHECK-TRIPLE-1-FOR-P2.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P2-COUNT
               IF P2-NUM(K) = WIN1N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P2-NUM(K) = WIN1N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P2-NUM(K) = WIN1N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P2-WON
           END-IF.

       CHECK-TRIPLE-2-FOR-P2.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P2-COUNT
               IF P2-NUM(K) = WIN2N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P2-NUM(K) = WIN2N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P2-NUM(K) = WIN2N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P2-WON
           END-IF.

       CHECK-TRIPLE-3-FOR-P2.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P2-COUNT
               IF P2-NUM(K) = WIN3N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P2-NUM(K) = WIN3N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P2-NUM(K) = WIN3N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P2-WON
           END-IF.

       CHECK-TRIPLE-4-FOR-P2.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P2-COUNT
               IF P2-NUM(K) = WIN4N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P2-NUM(K) = WIN4N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P2-NUM(K) = WIN4N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P2-WON
           END-IF.

       CHECK-TRIPLE-5-FOR-P2.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P2-COUNT
               IF P2-NUM(K) = WIN5N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P2-NUM(K) = WIN5N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P2-NUM(K) = WIN5N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P2-WON
           END-IF.

       CHECK-TRIPLE-6-FOR-P2.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P2-COUNT
               IF P2-NUM(K) = WIN6N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P2-NUM(K) = WIN6N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P2-NUM(K) = WIN6N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P2-WON
           END-IF.

       CHECK-TRIPLE-7-FOR-P2.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P2-COUNT
               IF P2-NUM(K) = WIN7N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P2-NUM(K) = WIN7N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P2-NUM(K) = WIN7N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P2-WON
           END-IF.

       CHECK-TRIPLE-8-FOR-P2.
           MOVE 'N' TO HAS-N1 HAS-N2 HAS-N3
           PERFORM VARYING K FROM 1 BY 1 UNTIL K > P2-COUNT
               IF P2-NUM(K) = WIN8N1
                   MOVE 'Y' TO HAS-N1
               END-IF
               IF P2-NUM(K) = WIN8N2
                   MOVE 'Y' TO HAS-N2
               END-IF
               IF P2-NUM(K) = WIN8N3
                   MOVE 'Y' TO HAS-N3
               END-IF
           END-PERFORM
           IF HAS-NUM1 AND HAS-NUM2 AND HAS-NUM3
               MOVE 'Y' TO P2-WON
           END-IF.

       NEXT-PERMUTATION.
           MOVE 'N' TO ALL-DONE
           MOVE 0 TO K1
           PERFORM VARYING I FROM 1 BY 1 UNTIL I > 8
               IF NUM(I) < NUM(I + 1)
                   MOVE I TO K1
               END-IF
           END-PERFORM

           IF K1 = 0
               SET ALL-PERMS-DONE TO TRUE
               EXIT PARAGRAPH
           END-IF

           MOVE 0 TO K2
           COMPUTE I = K1 + 1
           PERFORM UNTIL I > 9
               IF NUM(I) > NUM(K1)
                   MOVE I TO K2
               END-IF
               ADD 1 TO I
           END-PERFORM

           MOVE NUM(K1) TO SWAP-TEMP
           MOVE NUM(K2) TO NUM(K1)
           MOVE SWAP-TEMP TO NUM(K2)

           COMPUTE START-IDX = K1 + 1
           MOVE 9 TO END-IDX
           PERFORM UNTIL START-IDX >= END-IDX
               MOVE NUM(START-IDX) TO SWAP-TEMP
               MOVE NUM(END-IDX) TO NUM(START-IDX)
               MOVE SWAP-TEMP TO NUM(END-IDX)
               ADD 1 TO START-IDX
               SUBTRACT 1 FROM END-IDX
           END-PERFORM.

       DISPLAY-RESULTS.
           DISPLAY " "
           DISPLAY "Game of 15 - All possible games enumeration"
           DISPLAY "=========================================="
           DISPLAY "Total games:    " TOTAL-GAMES
           DISPLAY "Player 1 wins:  " P1-WINS
           DISPLAY "Player 2 wins:  " P2-WINS
           DISPLAY "Draws:          " DRAWS
           DISPLAY " "
           COMPUTE TEMP = P1-WINS + P2-WINS + DRAWS
           DISPLAY "Verification:   " P1-WINS " + " P2-WINS " + " DRAWS = " TEMP
           .
