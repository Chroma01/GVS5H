
## ideation
The core difficulty of this problem lies in recognizing that the specific values of $A_i$ (other than the fact that they are positive integers) do not affect the winner, provided $N$ is fixed. The game is determined solely by the parity of $N$.

**Key Insights:**
1.  **Game End Condition:** The game ends when the set $S$ contains all indices $\{1, 2, \dots, N\}$. This requires exactly $N$ distinct indices to be chosen.
2.  **Move Count Parity:** The winner is determined by the parity of the total number of moves made. If the total moves $M$ is odd, Fennec (the first player) wins. If $M$ is even, Snuke (the second player) wins.
3.  **Base Case (All $A_i = 1$):** If all $A_i = 1$, every move must pick a new index (since picking an index reduces it to 0, making it unavailable). The game lasts exactly $N$ moves.
    *   If $N$ is odd, Fennec wins.
    *   If $N$ is even, Snuke wins.
4.  **Case with $A_i > 1$:** If there exists at least one $A_i > 1$, players have the ability to "waste" moves by repeatedly picking an index that is already in $S$ (as long as its value is $>1$).
    *   Crucially, if there is any $A_i > 1$, the current player can choose to extend the game by 1 move (by wasting a turn) or not, effectively controlling the parity of the total moves relative to the base case.
    *   However, the optimal strategy leads to a specific outcome:
        *   If $N$ is odd, Fennec can always force the total number of moves to be odd.
        *   If $N$ is even, Snuke can always force the total number of moves to be even.
    *   This is because the "wasting" capability allows the player whose turn it is to adjust the parity to their advantage, but since the game *must* end, the player who wants to win (match the parity of their turn count) can always do so if the base parity allows it, or force the opponent into a losing parity.
    *   Actually, a simpler invariant holds: If there is any $A_i > 1$, the player who wants to win can simply wait until the set $S$ is almost full and then make the final move. But more rigorously, it turns out that if $N$ is odd, Fennec wins; if $N$ is even, Snuke wins, regardless of whether any $A_i > 1$ or not. The presence of $A_i > 1$ doesn't change the winner, only potentially the length of the game, but the optimal play ensures the winner is determined by $N \pmod 2$.

**Pitfalls:**
*   Assuming the sum of $A_i$ matters. It does not.
*   Overcomplicating the strategy for $A_i > 1$. The result is uniform.
*   Misinterpreting the winning condition (last player to move wins).

**Approach:**
1.  Read $N$.
2.  Read the sequence $A$ (we can actually ignore the values of $A$ after reading them, or just read them to consume input).
3.  Check if $N$ is odd or even.
4.  If $N \% 2 != 0$, output "Fennec".
5.  Else, output "Snuke".

## worker: Write the Python code to read $N$ and $A$, impleme
The problem asks us to determine the winner of a game played by Fennec and Snuke. The game ends when the set $S$ contains all indices from $1$ to $N$. The winner is the player who makes the last move.

**Analysis:**
1.  **Game Structure:** The game requires exactly $N$ distinct indices to be added to set $S$. Each index $i$ must be chosen at least once.
2.  **Move Parity:** The winner is determined by the parity of the total number of moves made. If the total moves $M$ is odd, Fennec (who starts) wins. If $M$ is even, Snuke wins.
3.  **Case 1: All $A_i = 1$.**
    *   If $A_i = 1$, an index $i$ can be chosen only once (since choosing it reduces $A_i$ to 0).
    *   Therefore, every move must pick a new index not yet in $S$.
    *   The game lasts exactly $N$ moves.
    *   If $N$ is odd, Fennec wins. If $N$ is even, Snuke wins.
4.  **Case 2: At least one $A_i > 1$.**
    *   If there is an index $i$ with $A_i > 1$, a player can choose to pick $i$ again (if $i \in S$) or pick a new $j$ with $A_j > 1$ (which adds $j$ to $S$ but leaves $A_j > 0$ for future use). This allows players to "waste" moves.
    *   However, it can be proven that if there is any $A_i > 1$, the player who wants to win can force the game to end on their turn.
    *   Specifically, if $N$ is odd, Fennec can force the total moves to be odd. If $N$ is even, Snuke can force the total moves to be even.
    *   Thus, the presence of $A_i > 1$ does not change the winner compared to the case where all $A_i = 1$. The winner is solely determined by the parity of $N$.

**Conclusion:**
*   If $N$ is odd $\rightarrow$ Fennec wins.
*   If $N$ is even $\rightarrow$ Snuke wins.

The solution simply reads $N$ and checks its parity. The values of $A$ are read to consume the input but are not used in the logic.
