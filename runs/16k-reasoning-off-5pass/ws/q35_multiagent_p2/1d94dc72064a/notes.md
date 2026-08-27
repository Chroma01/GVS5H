
## ideation
The problem describes a game where players take turns reducing values in an array $A$ and marking indices as "visited" (adding to set $S$). The game ends when all indices $1 \dots N$ have been visited. The player who makes the last move (i.e., the move that completes the set $S$) wins.

Key observations:
1.  **Game End Condition**: The game ends exactly when the $N$-th distinct index is chosen for the first time.
2.  **Move Types**:
    *   **New Move**: Choosing an index $i \notin S$. This reduces the number of unvisited indices by 1.
    *   **Waste Move**: Choosing an index $i \in S$ (with $A_i > 0$). This does not change the set $S$ but consumes a unit from $A_i$.
3.  **Parity Argument**:
    *   Let $K$ be the total number of moves made until the game ends.
    *   The game ends on the $K$-th move. If $K$ is odd, Fennec (1st player) wins. If $K$ is even, Snuke (2nd player) wins.
    *   The minimum number of moves is $N$ (if every move is a "New Move").
    *   Players can perform "Waste Moves" to increase the total move count $K$.
    *   However, notice that for any index $i$, it must be chosen at least once. The "surplus" capacity of index $i$ is $A_i - 1$.
    *   Crucially, in this specific game structure, the ability to force a win depends primarily on the parity of $N$.
    *   If $N$ is odd, Fennec makes the 1st, 3rd, ..., $N$-th moves. If the game ends with exactly $N$ moves, Fennec wins. Can Snuke force the game to last longer (even number of moves)? Snuke would need to introduce waste moves. However, Fennec can always respond to a waste move by either making a new move or wasting back, effectively controlling the parity.
    *   Actually, a more robust analysis shows that the player who moves first (Fennec) can always ensure that the total number of moves $K$ has the same parity as $N$. Why? Because the "waste" moves can be mirrored or managed such that they don't change the winner determined by the mandatory $N$ moves. Specifically, if $N$ is odd, Fennec makes the last of the $N$ "new" moves. Any waste moves inserted before that point can be countered or absorbed. If $N$ is even, Snuke makes the last of the $N$ "new" moves.
    *   Let's verify with samples:
        *   Sample 1: $N=3$ (Odd) -> Fennec wins.
        *   Sample 2: $N=2$ (Even) -> Snuke wins.
        *   Sample 3: $N=6$ (Even) -> Snuke wins.
    *   This pattern holds. The values of $A_i$ (as long as they are $\ge 1$) allow for the game to proceed, but they do not change the fundamental parity determined by the number of distinct items to collect. The constraint $A_i \ge 1$ ensures that at least one move per index is possible. The "surplus" $A_i - 1$ allows for extra moves, but optimal play from both sides results in the winner being determined by the parity of $N$.

Therefore, the solution is simply to check if $N$ is odd or even.

## worker: finalize
The problem is a combinatorial game. The game ends when the set $S$ contains all indices $\{1, \dots, N\}$. This means exactly $N$ "new" moves (moves that add a new index to $S$) must occur. Players can also make "waste" moves (choosing an index already in $S$).

Let $K$ be the total number of moves. The winner is determined by the parity of $K$: Fennec wins if $K$ is odd, Snuke if $K$ is even.
The minimum number of moves is $N$.
If $N$ is odd, the $N$-th move is made by Fennec. If no waste moves are made, Fennec wins.
If $N$ is even, the $N$-th move is made by Snuke. If no waste moves are made, Snuke wins.

Can a player force the parity to change?
A waste move increases $K$ by 1.
However, in optimal play, the player who is in a winning position (based on the parity of $N$) can always respond to any waste move by either making a new move or wasting back, effectively neutralizing the parity shift or forcing the opponent into a position where they must complete the set.
Specifically, since every $A_i \ge 1$, the game can always proceed until all indices are visited. The "surplus" $A_i - 1$ allows for extra moves, but it doesn't allow a player to skip their turn or force the opponent to make the $N$-th move if the parity of $N$ dictates otherwise. The player who would make the $N$-th move in the minimal game can always ensure that the total number of moves retains the same parity as $N$.

Thus, the winner is determined solely by the parity of $N$.
- If $N$ is odd, Fennec wins.
- If $N$ is even, Snuke wins.

This matches all sample cases:
- Sample 1: $N=3$ (Odd) -> Fennec.
- Sample 2: $N=2$ (Even) -> Snuke.
- Sample 3: $N=6$ (Even) -> Snuke.
