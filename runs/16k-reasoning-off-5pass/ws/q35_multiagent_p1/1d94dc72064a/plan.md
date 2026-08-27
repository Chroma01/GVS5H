1.  **Analyze the Winning Condition**: The game ends when $S = \{1, 2, \dots, N\}$. This means every index $i$ must have been chosen at least once. The player who makes the move that completes the set $S$ wins.
2.  **Decompose the Game**: The game has two phases:
    *   **Phase 1**: Covering all indices. Each index $i$ needs to be chosen at least once. The "cost" to cover index $i$ is 1 move. However, players can also choose to reduce $A_i$ further after it's covered, or before it's covered.
    *   **Phase 2**: Reducing remaining values. Once all indices are in $S$, the game continues until all $A_i$ become 0? No, the rule says "If $S=\{1,\dots,N\}$, the game ends". So the game ends *immediately* when the last new index is added to $S$. The values of $A_i$ for $i \in S$ don't need to reach 0.
3.  **Re-evaluate**: The game ends as soon as every index has been picked at least once. The total number of moves is exactly $N$ *if* players only pick uncovered indices. But players can pick covered indices. Picking a covered index doesn't change $S$, so it just wastes a turn (or rather, passes the turn to the opponent without progressing towards the win condition).
4.  **Strategic Insight**:
    *   To win, you want to be the one to pick the *last* uncovered index.
    *   Let $K$ be the number of indices currently not in $S$. Initially $K=N$.
    *   If a player picks an uncovered index $i$, $K$ decreases by 1.
    *   If a player picks a covered index $i$, $K$ stays the same.
    *   Players want to control the parity of the total moves made when the last uncovered index is picked.
    *   However, players can also "pass" by picking covered indices. But picking a covered index requires $A_i \ge 1$. If all $A_i$ for covered indices are 0, you *must* pick an uncovered index (if any exist).
    *   Actually, the problem states: "it can be proven that until a winner is determined... players can always make a move". This implies we don't need to worry about getting stuck.
    *   Key realization: The game is equivalent to a Nim-like game or a parity game on the "uncovered" status.
    *   Let's consider the total "freedom" to pass. A player can pass on index $i$ as long as $A_i > 0$ and $i \in S$.
    *   Actually, a simpler view: The player who picks the last uncovered index wins. Let's say the indices are picked in some order. The player who picks the $N$-th distinct index wins.
    *   Can a player force the game to last a specific number of moves?
    *   Consider the sum of $A_i$. Each move reduces $\sum A_i$ by 1. But the game doesn't end when sum is 0. It ends when all indices are visited.
    *   Let's look at the "extra" moves. For each index $i$, after it is first picked, it can be picked $A_i - 1$ more times *before* it runs out. These extra picks act as "passes".
    *   Total potential passes = $\sum_{i=1}^N (A_i - 1) = (\sum A_i) - N$.
    *   The core game is: There are $N$ items to be collected. Each turn, you can either collect a new item or use a "pass" (pick an already collected item). Using a pass consumes 1 unit of "pass capacity".
    *   This is equivalent to: Two players take turns. There are $N$ "core" moves and $P = \sum (A_i - 1)$ "pass" moves. The player who makes the $N$-th core move wins. The pass moves can be inserted anywhere.
    *   If there are no passes ($P=0$), the game lasts exactly $N$ moves. Fennec wins if $N$ is odd, Snuke if $N$ is even.
    *   If there are passes, players can choose to insert passes. This is similar to a game where you can skip turns.
    *   Actually, this is a standard result: If the total number of "extra" moves (passes) is even, the parity of the winner is determined by $N$. If odd, it flips?
    *   Let's test Sample 1: $N=3, A=[1,9,2]$. $P = (1-1)+(9-1)+(2-1) = 0+8+1=9$. $N=3$ (odd). Output: Fennec.
    *   Sample 2: $N=2, A=[25,29]$. $P = 24+28=52$ (even). $N=2$ (even). Output: Snuke.
    *   Sample 3: $N=6, A=[1,9,2,25,2,9]$. $P = 0+8+1+24+1+8 = 42$ (even). $N=6$ (even). Output: Snuke.
    *   Hypothesis: The winner is determined by the parity of $N + P$.
        *   If $(N + P)$ is odd, Fennec wins.
        *   If $(N + P)$ is even, Snuke wins.
    *   Let's verify logic: The total number of moves in the game is $N + K$, where $K$ is the number of passes used. Since players play optimally to win, they will try to control the parity of the total moves.
    *   The player who wants to make the last move (the $N$-th distinct pick) will try to ensure the total number of moves is odd (for Fennec) or even (for Snuke).
    *   Since players can choose to use passes or not, the player who moves second in the "pass game" can mirror?
    *   Actually, if $P > 0$, the first player can always force a win if they want? No.
    *   Standard combinatorial game theory: This is equivalent to a game with $N$ "winning" tokens and $P$ "neutral" tokens. The game ends when all $N$ winning tokens are taken.
    *   If $P=0$, moves = $N$. Winner depends on $N \% 2$.
    *   If $P > 0$, the player who can control the parity of the total moves wins.
    *   It turns out that if $P$ is even, the parity is fixed to $N \% 2$. If $P$ is odd, the parity can be flipped?
    *   Let's check: $N=1, A=[2]$. $P=1$. Fennec picks index 1. $S=\{1\}$. Game ends. Fennec wins. $N+P = 2$ (even). But Fennec wins. My hypothesis failed.
    *   Correction: In $N=1, A=[2]$, Fennec picks index 1. $S=\{1\}$. Game ends immediately. The remaining $A_1=1$ is never used. So $P$ is not fully available.
    *   The "passes" are only available on indices that have *already* been picked.
    *   So, for the last index to be picked, it must be that all other $N-1$ indices are already in $S$.
    *   The total number of moves is $N + (\text{passes used on first } N-1 \text{ indices})$.
    *   The last index is picked on move $N + K$. The player is Fennec if $N+K$ is odd.
    *   Can the players control $K$?
    *   The players can use passes on any index $i$ that is already in $S$.
    *   This is equivalent to: There are $N-1$ "preparation" indices. The sum of their $A_i$ values determines the max passes. The last index is fixed? No, players choose which index is last.
    *   Actually, players can choose which index is the *last* one to be added to $S$.
    *   If a player wants to win, they will choose the last index such that the parity works out, if possible.
    *   Let $S_{total} = \sum A_i$.
    *   Consider the game as: Total moves = $\sum A_i$? No, game ends early.
    *   Let's look at the parity of $\sum A_i$.
    *   Sample 1: Sum = 12. Even. Fennec wins.
    *   Sample 2: Sum = 54. Even. Snuke wins.
    *   Sample 3: Sum = 48. Even. Snuke wins.
    *   $N=1, A=[2]$. Sum=2. Even. Fennec wins.
    *   $N=1, A=[1]$. Sum=1. Odd. Fennec wins.
    *   $N=2, A=[1,1]$. Sum=2. Even. Fennec picks 1, Snuke picks 2. Snuke wins.
    *   $N=2, A=[1,2]$. Sum=3. Odd. Fennec picks 1, Snuke picks 2. Snuke wins? Or Fennec picks 2 (S={2}), Snuke picks 1 (S={1,2}). Snuke wins.
    *   Wait, in $N=2, A=[1,2]$, if Fennec picks 1, $S=\{1\}$. Snuke picks 2, $S=\{1,2\}$. Snuke wins.
    *   If Fennec picks 2, $S=\{2\}, A=[1,1]$. Snuke can pick 1 (win) or 2 (pass). Snuke picks 1, wins.
    *   So Snuke wins. Sum=3 (Odd).
    *   It seems Snuke wins if $N$ is even?
    *   Sample 1: $N=3$ (odd) -> Fennec.
    *   Sample 2: $N=2$ (even) -> Snuke.
    *   Sample 3: $N=6$ (even) -> Snuke.
    *   $N=1$ (odd) -> Fennec.
    *   Is it just $N \% 2$?
    *   Let's check $N=2, A=[100, 100]$. $N$ even. Snuke should win.
    *   Fennec picks 1. Snuke picks 2. Snuke wins. Yes.
    *   What if $A_i$ are huge? The ability to pass doesn't change the fact that the *last* distinct index must be picked.
    *   If $N$ is odd, Fennec makes moves 1, 3, ..., N. So Fennec makes the N-th move.
    *   If $N$ is even, Snuke makes moves 2, 4, ..., N. So Snuke makes the N-th move.
    *   Can a player *avoid* making the N-th move? Only by forcing the opponent to make it? No, the N-th move is the one that completes S.
    *   Can a player delay the game? Yes, by using passes.
    *   If Fennec wants to win (N odd), she wants the total moves to be odd.
    *   If Snuke wants to win (N even), he wants total moves to be even.
    *   If there are passes available, can the player who is "losing" by parity force a win?
    *   Example: $N=2, A=[1,1]$. No passes. Snuke wins.
    *   Example: $N=2, A=[1,2]$. Pass available on index 2.
        *   Fennec picks 1. $S=\{1\}$.
        *   Snuke can pick 2 (win) or pick 2 again (pass, $A=[1,1], S=\{1,2\}$? No, if Snuke picks 2, $S$ becomes $\{1,2\}$ and game ends. So Snuke *must* pick 2 to win? Or can he pass?
        *   If Snuke picks 2, $S=\{1,2\}$, game ends, Snuke wins.
        *   Can Snuke pass? To pass, he must pick an index in $S$. Only index 1 is in $S$. $A_1=1$. He picks 1, $A=[0,2], S=\{1\}$.
        *   Now Fennec's turn. $S=\{1\}$. Uncovered: 2. $A_2=2$.
        *   Fennec picks 2. $S=\{1,2\}$. Game ends. Fennec wins.
        *   So if Snuke passes, Fennec wins. Snuke plays optimally, so he picks 2 and wins.
    *   So Snuke wins.
    *   Example: $N=2, A=[2,1]$.
        *   Fennec picks 1. $S=\{1\}, A=[1,1]$.
        *   Snuke picks 2. Wins.
        *   Fennec picks 2. $S=\{2\}, A=[2,0]$.
        *   Snuke picks 1. Wins.
        *   Snuke wins.
    *   It seems the answer is simply: **Fennec wins if N is odd, Snuke wins if N is even.**
    *   Why? Because the player who makes the N-th distinct move wins. The number of "core" moves is fixed at N. The "pass" moves can be inserted, but they come in pairs? Or rather, the player who is about to make the N-th move can always choose to make it immediately if they want to win?
    *   Actually, if you are in a winning position (parity matches your turn), you just take the last uncovered index.
    *   If you are in a losing position, can you force a pass?
    *   If you pass, you give the turn to the opponent. The opponent is now in the winning position.
    *   Since the game is finite and impartial (mostly), and the "pass" moves are just delaying, the player who can force the game to end on their turn wins.
    *   With optimal play, the player who would make the N-th move in the "no pass" scenario will win, because they can always choose to end the game on their turn if they are in a good parity spot, and if they are in a bad spot, they can't force the opponent to make a mistake?
    *   Actually, if $N$ is odd, Fennec makes moves 1, 3, ..., N. She makes the last move.
    *   If $N$ is even, Snuke makes moves 2, 4, ..., N. He makes the last move.
    *   The existence of passes allows a player to *skip* their turn effectively, but skipping a turn changes the parity of the *next* core move.
    *   However, the player who wants to win can just ignore passes and play the core game. The player who is losing can try to use a pass to change the parity.
    *   But if the loser uses a pass, the winner just uses a pass back? Or the winner takes the win?
    *   If the loser passes, the winner is now facing a state where it's their turn to make a core move, but the parity is shifted.
    *   Actually, this is a known result for this specific problem (AtCoder Fennec-Snuke). The answer is indeed based on the parity of N.