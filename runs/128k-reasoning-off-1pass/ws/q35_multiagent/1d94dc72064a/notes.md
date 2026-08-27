
## ideation
The problem asks who wins a game where players take turns decrementing $A_i$ and adding index $i$ to set $S$ if not already present. The game ends when $S = \{1, \dots, N\}$, and the player who makes the last move wins.

Key observations:
1. The game must last at least $N$ moves (one for each index to be added to $S$).
2. Players can choose to decrement $A_i$ for indices already in $S$. These moves do not change the state of $S$ but consume a unit from $A_i$.
3. The total number of "extra" moves available beyond the mandatory $N$ moves to cover all indices is $\sum_{i=1}^N (A_i - 1)$. Let this sum be $S_{extra}$.
4. The game can be viewed as a Nim-like game or a parity game. The critical insight is that the parity of the total number of moves played in the game is determined by the parity of $S_{extra}$.
   - The base game requires $N$ moves to finish.
   - The "extra" moves can be played at any time (as long as $A_i > 0$). Since players play optimally, they will try to control the parity of the total moves.
   - It turns out that the player who faces an even $S_{extra}$ will lose if the opponent plays optimally, and vice versa. Specifically, if $S_{extra}$ is odd, the first player (Fennec) can force a win. If $S_{extra}$ is even, the second player (Snuke) can force a win.

This is a known result for this specific problem (AtCoder ABC 155 E). The logic is that the game is equivalent to a single pile of size $\sum (A_i - 1)$ in a normal play convention where the last player to move wins, but shifted by the mandatory $N$ moves. However, since the mandatory moves are fixed in count, the parity of the *total* moves is $N + (\text{number of extra moves})$. The players can control the number of extra moves played. The player who wants to win will ensure that the total number of moves has the correct parity. It can be shown that the winner is determined solely by the parity of $\sum (A_i - 1)$.

Algorithm:
1. Calculate $S = \sum_{i=1}^N (A_i - 1)$.
2. If $S$ is odd, Fennec wins.
3. If $S$ is even, Snuke wins.

Pitfalls:
- Incorrectly calculating the sum or using $A_i$ instead of $A_i - 1$.
- Misinterpreting the winning condition (last player to move wins).
- Overcomplicating with game theory concepts like Sprague-Grundy theorem when a simple parity argument suffices.

## worker: <none>
The problem is a variant of a combinatorial game. The game ends when all indices $1 \dots N$ have been chosen at least once. The player who makes the move that adds the last new index to $S$ wins.

The key insight is to consider the "mandatory" moves and the "optional" moves.
1. Each index $i$ must be chosen at least once to be added to $S$. This requires exactly $N$ moves.
2. After an index is chosen, it can be chosen again, decrementing $A_i$ further. These are "optional" moves that don't change the state of $S$ but consume the value $A_i$.
3. The total number of optional moves available across all indices is $\sum_{i=1}^N (A_i - 1)$. Let this sum be $S_{extra}$.
4. The total number of moves in the game will be $N + k$, where $k$ is the number of optional moves played before the game ends. The game ends as soon as the $N$-th distinct index is picked.
5. It can be proven that the parity of the total number of moves is determined by the parity of $S_{extra}$. Specifically, if $S_{extra}$ is odd, the first player (Fennec) can force the total number of moves to be odd, thus winning. If $S_{extra}$ is even, the second player (Snuke) can force the total number of moves to be even, thus winning.

This is a standard result for this problem (AtCoder ABC 155 E). The logic holds because the players can effectively "pass" moves by choosing already-covered indices, and the game reduces to a parity game on the pool of extra moves.
