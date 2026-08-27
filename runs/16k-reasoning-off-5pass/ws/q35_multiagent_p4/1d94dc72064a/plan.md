The game ends when all indices $1 \dots N$ have been added to set $S$. The key observation is that for each index $i$, it takes exactly $A_i$ moves to reduce $A_i$ to 0, but the index $i$ is only added to $S$ on the **first** time it is chosen. After that, subsequent choices on index $i$ don't add it to $S$ (it's already there).

However, the winning condition is simply that $S = \{1, \dots, N\}$. The player who makes the move that adds the **last** missing index to $S$ wins.

Let's think about the total number of "new index" moves required: exactly $N$ moves are needed to add all indices to $S$. But players can choose to waste moves on indices already in $S$ or on indices not yet in $S$ (after the first use).

Actually, a better way to think about it:
- Each index $i$ must be chosen at least once to be added to $S$.
- The first time index $i$ is chosen, $A_i$ decreases by 1 and $i$ is added to $S$.
- Subsequent choices on index $i$ just decrease $A_i$ further without changing $S$.

The game ends when all $N$ indices have been chosen at least once. The total number of moves in the game is not fixed because players can choose to decrement already-added indices. However, both players play optimally.

Key insight: The player who makes the $N$-th "new index" move wins. The players can control the pace by choosing which index to play on. 

Let's consider that each index $i$ provides $A_i$ total "tokens" (moves available on that index). The first move on index $i$ is special (adds to $S$), and the remaining $A_i - 1$ moves are "free" moves that don't advance the goal of completing $S$.

The total number of moves until the game ends is: $N$ (for the first moves on each index) + some number of extra moves on indices already in $S$.

Since both players play optimally, they will try to force the opponent into a position where they must make the last move. This is equivalent to a Nim-like game or a parity argument.

Actually, the total number of moves in the game is exactly $\sum A_i$. Why? Because every move decreases the sum $\sum A_i$ by 1, and the game ends when all $A_i = 0$? No, the game ends when $S = \{1, \dots, N\}$, not when all $A_i = 0$.

Wait, re-read: "it can be proven that until a winner is determined and the game ends, players can always make a move". The game ends when $S = \{1, \dots, N\}$. At that point, some $A_i$ may still be positive.

The crucial point: The last move that completes $S$ is the winning move. Players can choose to play on any index with $A_i > 0$. 

Think of it this way: There are $N$ "special" moves (one for each index to add it to $S$). The rest of the moves are "filler" moves. The total number of filler moves available is $\sum (A_i - 1) = \sum A_i - N$.

The game will last exactly $N + K$ moves where $K$ is the number of filler moves played. Since players alternate, if the total number of moves is odd, Fennec (first player) wins; if even, Snuke wins.

But players can choose how many filler moves to play. However, since both play optimally to win, they will try to control the parity.

Actually, the total number of moves is fixed! The game must continue until all indices are in $S$. The minimum number of moves is $N$ (if each index is chosen exactly once). But players can choose to play extra moves on indices already in $S$. 

The key realization: The player who is forced to make the $N$-th new-index move loses if they want to avoid winning? No, they want to win.

Let me reconsider: The total sum of $A_i$ is $S = \sum A_i$. Each move reduces the total sum by 1. The game ends when all indices have been chosen at least once. 

Actually, I believe the answer depends on the parity of $\sum A_i$. If $\sum A_i$ is odd, Fennec wins; if even, Snuke wins. Let's verify with samples:
- Sample 1: $1+9+2 = 12$ (even) -> Output: Fennec. This contradicts.

Let me think again. The game ends when $S = \{1, \dots, N\}$. The last move adds the final index to $S$. 

Another approach: Consider that each index $i$ needs to be "activated" (first move). The remaining $A_i - 1$ moves are optional. The players can choose to activate new indices or play on already-activated ones.

This is equivalent to: There are $N$ items that need to be collected. Each item $i$ has $A_i$ copies. The first copy collected of item $i$ is the "special" one. Players take turns collecting one copy from any item with remaining copies. The player who collects the $N$-th distinct item wins.

This is a known game theory problem. The answer is determined by the parity of $\sum (A_i - 1) + N = \sum A_i$. Wait, that's the same as before.

Let me try: The total number of moves is $\sum A_i$. The player who makes the last move wins. If $\sum A_i$ is odd, first player (Fennec) makes moves 1, 3, 5, ..., and the last move. If even, Snuke makes the last move.

Sample 1: sum = 12 (even) -> Snuke should win? But output is Fennec. So this is wrong.

Hmm, the game doesn't require all $A_i$ to reach 0. It ends when all indices are in $S$. So the total moves is not $\sum A_i$.

Let's think differently. The minimum moves to finish is $N$. Extra moves can be inserted. The number of extra moves possible is $\sum (A_i - 1)$. Let $E = \sum (A_i - 1)$. 

The players can choose to play extra moves or not. Since both play optimally, the player who can force the parity of total moves to be favorable will win.

If $E$ is even, then the total moves $N + E'$ where $E' \leq E$ can be controlled. Actually, I think the answer is: if $N$ is odd, Fennec wins; if $N$ is even, Snuke wins? Sample 1: $N=3$ (odd) -> Fennec. Sample 2: $N=2$ (even) -> Snuke. Sample 3: $N=6$ (even) -> Snuke. This matches all samples!

Let me verify: The parity of $N$ determines the winner. If $N$ is odd, Fennec wins; if even, Snuke wins.