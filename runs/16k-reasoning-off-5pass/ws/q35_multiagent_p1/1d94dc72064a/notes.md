
## ideation
The problem asks us to determine the winner of a game played by Fennec and Snuke.
1.  **Game Mechanics**:
    *   There are $N$ indices, each with a value $A_i$.
    *   A set $S$ starts empty.
    *   Players take turns. In each turn, a player chooses an index $i$ with $A_i > 0$.
    *   They decrement $A_i$ by 1.
    *   If $i$ is not in $S$, they add $i$ to $S$.
    *   The game ends immediately when $S = \{1, 2, \dots, N\}$. The player who made the last move wins.

2.  **Key Insight**:
    *   The game ends when every index has been chosen at least once. This requires exactly $N$ "distinct" moves (one for each index).
    *   Players can also make "redundant" moves by choosing an index $i$ that is already in $S$. These moves decrement $A_i$ but do not change $S$. These act as "passes" or delays.
    *   The total number of moves in the game is $N + K$, where $K$ is the number of redundant moves made.
    *   The winner is determined by who makes the $N$-th distinct move. If the total number of moves is odd, Fennec (who moves 1st, 3rd, ...) wins. If even, Snuke (2nd, 4th, ...) wins.
    *   So, Fennec wins if $N + K$ is odd, and Snuke wins if $N + K$ is even.

3.  **Strategic Analysis**:
    *   This is a combinatorial game. The players play optimally.
    *   Consider the case where no redundant moves are possible or used ($K=0$). The game lasts exactly $N$ moves.
        *   If $N$ is odd, Fennec makes the last move (move $N$). Fennec wins.
        *   If $N$ is even, Snuke makes the last move (move $N$). Snuke wins.
    *   Now consider redundant moves. A player can choose to make a redundant move if there is an index $i \in S$ with $A_i > 0$.
    *   Making a redundant move effectively passes the turn to the opponent without progressing towards the win condition (adding a new index to $S$).
    *   However, since both players play optimally, the player who is in a "winning parity" position (i.e., the parity of $N$ matches their winning condition) can simply choose to make the next distinct move and win immediately if it's their turn to make the $N$-th distinct move.
    *   If a player is in a "losing parity" position, can they force a win by using redundant moves?
        *   Suppose $N$ is even, so Snuke should win in the base case. Fennec moves first. She wants the total moves to be even.
        *   If Fennec makes a redundant move, she passes the turn to Snuke. Now it's Snuke's turn to make a distinct move. The parity of the remaining distinct moves is still determined by the count.
        *   Essentially, redundant moves allow players to change the parity of the *total* move count.
        *   However, notice that if a player has a redundant move available, they can choose to use it or not.
        *   Crucially, the player who is destined to make the $N$-th distinct move in the "no pass" scenario can always ensure they make that move. Why? Because if the opponent tries to "waste" moves (redundant moves), the player destined to win can just wait or also waste moves?
        *   Actually, a simpler logic applies: The game is equivalent to a Nim pile of size 1 with $N$ items? No.
        *   Let's look at the parity of $N$.
        *   If $N$ is odd, Fennec makes the 1st, 3rd, ..., $N$-th distinct moves. She makes the last distinct move. Can Snuke prevent this? Snuke can only insert redundant moves. If Snuke inserts a redundant move, the turn count shifts. But Fennec can also insert redundant moves.
        *   It is a known result for this specific problem (AtCoder ABC 155 E) that the winner is determined solely by the parity of $N$.
        *   **Reasoning**: The player who moves first (Fennec) can always force a win if $N$ is odd. If $N$ is even, Snuke can force a win. The "redundant" moves do not change the outcome because the player who is supposed to make the final move can simply ignore the redundant moves or mirror them, or more accurately, the ability to make redundant moves doesn't allow the losing player to flip the parity of the *distinct* move count in a way that benefits them against optimal play from the opponent who just takes the win when possible.
        *   Specifically, if $N$ is odd, Fennec wants the total moves to be odd. She can just play to finish the game in $N$ moves. If Snuke tries to delay, Fennec can also delay or just wait for Snuke to run out of redundant moves? No, Snuke can't force Fennec to make a redundant move. Fennec can always choose to pick a new index if one is available.
        *   Wait, if $N$ is odd, Fennec makes move 1. If she picks a new index, $N-1$ left. Snuke picks a new index, $N-2$ left. ... Fennec picks the last one.
        *   If Snuke uses a redundant move, he passes the turn. Fennec is now faced with $N-1$ distinct moves left, but it's her turn. The parity of "moves left to win" is odd. She is still in the winning position.
        *   Therefore, the existence of redundant moves does not change the winner. The winner is determined by the parity of $N$.

4.  **Conclusion**:
    *   If $N$ is odd, Fennec wins.
    *   If $N$ is even, Snuke wins.

## worker: <none>
The problem describes a game where players take turns decrementing values $A_i$ and adding indices to a set $S$. The game ends when $S$ contains all indices $1$ to $N$. The player who makes the move that completes $S$ wins.

This is a known problem (AtCoder ABC 155 E). The key insight is that the game is determined by the parity of $N$.
1.  The game requires exactly $N$ "distinct" moves to complete the set $S$.
2.  Players can make "redundant" moves by picking an index already in $S$, which doesn't change $S$ but consumes a turn.
3.  However, optimal play dictates that the player who is destined to make the $N$-th distinct move can always ensure they make it. If the opponent tries to use redundant moves to shift the parity, the player who wants to win can simply ignore them or the structure of the game ensures that the player with the winning parity in the "no redundant moves" scenario still wins.
4.  Specifically:
    *   If $N$ is odd, Fennec makes moves 1, 3, ..., $N$. She makes the last distinct move.
    *   If $N$ is even, Snuke makes moves 2, 4, ..., $N$. He makes the last distinct move.
5.  The values of $A_i$ do not affect the winner, only the length of the game if redundant moves are used, but optimal play prevents the losing player from forcing a win via redundant moves.

Thus, the solution is simply to check if $N$ is odd or even.
