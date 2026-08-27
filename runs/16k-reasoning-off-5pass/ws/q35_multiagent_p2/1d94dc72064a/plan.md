The key insight is to analyze the game in two phases:
1. **Phase 1: Covering all indices.** The game ends when $S = \{1, 2, \dots, N\}$. This means every index $i$ must have been chosen at least once. For each index $i$, it takes exactly one move to "activate" it (add to $S$) for the first time. However, players can choose to subtract from an already-activated index or a new one.
2. **Total Moves Analysis:** Let $T$ be the total number of moves until the game ends. The game ends when all indices have been activated. The total number of subtractions performed across all indices must be at least $N$ (one for each index to reach 0 or just to be activated? No, the condition is just that $i$ was chosen. But note: to activate index $i$, you must subtract from $A_i$ at least once. The game ends immediately when the last new index is activated. The values of $A_i$ don't need to go to 0, they just need to be positive when chosen. Wait, the rule says "Choose an index $i$ such that $1 \le A_i$". So $A_i$ must be positive. The game ends when $S=\{1,\dots,N\}$.

Actually, a simpler perspective:
The game is equivalent to a Nim-like game or a parity argument.
Let's consider the total number of moves required to "finish" the game. The game ends when every index has been picked at least once.
However, players can waste moves by picking already-picked indices.
But note: if a player picks an index $i$ that is already in $S$, it doesn't help them win the "cover all" condition faster, but it changes the parity of the total move count.

Let's look at the minimum number of moves to end the game. This is $N$ moves (one for each index). If the total "capacity" of the array allows the game to end in exactly $N$ moves, the winner is determined by the parity of $N$.
However, players can extend the game.
Actually, this is a known problem type. The total number of moves in the game is determined by the sum of $A_i$? No, because the game ends as soon as all indices are touched, not when all $A_i$ become 0.

Let's re-read carefully: "If $S=\{1,2,\dots,N\}$, the game ends".
So, the game ends the moment the $N$-th distinct index is chosen.
Each index $i$ must be chosen at least once.
Let $k_i$ be the number of times index $i$ is chosen. We must have $k_i \ge 1$ for all $i$.
The total number of moves is $K = \sum k_i$.
The game ends when the last new index is added.
The players play optimally.
This is equivalent to: There are $N$ items to collect. Each move collects one item (if not already collected) or "wastes" a move on an already collected item.
But wait, you can only choose $i$ if $A_i \ge 1$.
So, index $i$ can be chosen at most $A_i$ times.
The constraint is that we must choose each index at least once.
The total number of moves $K$ will be $N + W$, where $W$ is the number of "wasted" moves (choosing an index already in $S$).
The player who makes the $K$-th move wins.
If $K$ is odd, Fennec (1st player) wins. If $K$ is even, Snuke (2nd player) wins.

Who controls $W$?
The game ends as soon as the set $S$ is full.
The minimum moves is $N$.
Can the second player force the total moves to be even? Or can the first player force it to be odd?
Actually, this is a standard impartial game.
Consider the sum $S_A = \sum A_i$.
The total number of times any index can be chosen is bounded by $A_i$.
However, the game ends *early*.

Let's look at the sample cases.
Sample 1: N=3, A=[1,9,2]. Output: Fennec.
Sample 2: N=2, A=[25,29]. Output: Snuke.
Sample 3: N=6, A=[1,9,2,25,2,9]. Output: Snuke.

Hypothesis:
The game is determined by the parity of $\sum A_i$?
Sample 1: Sum = 1+9+2 = 11 (Odd) -> Fennec.
Sample 2: Sum = 25+29 = 54 (Even) -> Snuke.
Sample 3: Sum = 1+9+2+25+2+9 = 48 (Even) -> Snuke.

Let's test this hypothesis.
If the hypothesis is "Winner is determined by parity of $\sum A_i$", then:
If $\sum A_i$ is odd, Fennec wins.
If $\sum A_i$ is even, Snuke wins.

Why would this be?
Think of the game as consuming tokens. Each move consumes 1 token from some $A_i$.
The game ends when all indices have been touched.
But wait, the game doesn't require $A_i$ to reach 0. It just requires $A_i \ge 1$ to make a move.
The condition "game ends when $S=\{1..N\}$" means we stop as soon as we have picked every index at least once.

Let's consider the total number of moves $K$.
The minimum $K$ is $N$.
The maximum $K$ is $\sum A_i$? No, because we stop early.
However, note that if a player wants to win, they can choose to "waste" moves on indices that still have $A_i > 1$ (or even $A_i=1$ if they are willing to let it become 0, but you can't pick if $A_i=0$).
Actually, once an index is picked, it stays in $S$.
The crucial observation in similar problems (like "Nim with a pass" or "parity games") is often about the total parity.

Let's verify with a small case.
N=1, A=[1]. Sum=1 (Odd). Fennec picks index 1. S={1}. Game ends. Fennec wins. Correct.
N=1, A=[2]. Sum=2 (Even). Fennec picks index 1. S={1}. Game ends. Fennec wins.
Wait. If N=1, A=[2], Sum=2 (Even), but Fennec wins.
So the simple parity of sum hypothesis is **WRONG**.

Let's re-evaluate N=1, A=[2].
Fennec picks 1. S={1}. Game ends. Fennec wins.
So for N=1, Fennec always wins.

Let's look at N=2, A=[1,1]. Sum=2 (Even).
Fennec picks 1. S={1}. A=[0,1].
Snuke picks 2. S={1,2}. Game ends. Snuke wins.
So for N=2, A=[1,1], Snuke wins.

N=2, A=[1,2]. Sum=3 (Odd).
Fennec picks 1. S={1}. A=[0,2].
Snuke picks 2. S={1,2}. Game ends. Snuke wins.
Wait. If Fennec picks 1, Snuke picks 2 and wins.
What if Fennec picks 2? S={2}. A=[1,1].
Snuke picks 1. S={1,2}. Game ends. Snuke wins.
So for N=2, A=[1,2], Snuke wins.
But Sum=3 is Odd. My previous hypothesis said Fennec. So hypothesis is definitely wrong.

Let's look at the structure again.
The game ends when the last *new* index is picked.
This is equivalent to: We have $N$ items. Each move picks an item.
If the item hasn't been picked, it's a "new" pick.
If it has been picked, it's a "waste".
The game ends when $N$ new picks have occurred.
The player who makes the $N$-th new pick wins.

Let $K$ be the total number of moves.
$K = N + W$, where $W$ is the number of wasted moves.
The winner is Fennec if $K$ is odd, Snuke if $K$ is even.

Who controls $W$?
Players can choose to waste moves on any index $i$ that is already in $S$ and has $A_i > 0$ (remaining capacity).
Actually, even if $A_i$ becomes 0, it's still in $S$. You can't pick it anymore.
So, the ability to waste moves depends on the remaining "surplus" of the indices.
Let $R_i = A_i - 1$ be the surplus of index $i$ after it has been picked once.
Total surplus $S_{surplus} = \sum (A_i - 1) = \sum A_i - N$.

If $S_{surplus} = 0$ (i.e., all $A_i = 1$), then no wasted moves are possible.
The game lasts exactly $N$ moves.
Winner is Fennec if $N$ is odd, Snuke if $N$ is even.

If $S_{surplus} > 0$, players can choose to waste moves.
However, note that wasting a move consumes 1 from the surplus of an index.
Once an index's surplus is exhausted (i.e., $A_i$ becomes 0), it can no longer be used for wasting.

This looks like a game on the surplus.
But the "new" picks are mandatory to end the game.
Actually, the players can interleave new picks and waste picks.

Key Insight:
The total number of moves is $N + W$.
The players can control $W$ to some extent.
However, notice that if a player is in a winning position, they will try to make $K$ odd. If in a losing position, they will try to make $K$ even.

Consider the total surplus $S_{surplus} = \sum A_i - N$.
Each waste move reduces $S_{surplus}$ by 1.
Each new move reduces the "number of uncovered indices" by 1, but does not reduce surplus (it uses 1 from $A_i$, so if $A_i > 1$, surplus reduces by 1? No.
When you pick a NEW index $i$:
- $A_i$ decreases by 1.
- If $A_i$ was 1, it becomes 0. Surplus contribution goes from 0 to -1? No, surplus is defined as $A_i - 1$.
Let's define surplus $s_i = A_i - 1$.
Initially, total surplus $S = \sum s_i$.
When you pick a NEW index $i$:
- $A_i$ becomes $A_i - 1$.
- New surplus $s_i' = A_i - 1 - 1 = s_i - 1$.
- So picking a NEW index reduces total surplus by 1.
When you pick an OLD index $i$ (waste):
- $A_i$ becomes $A_i - 1$.
- New surplus $s_i' = A_i - 1 - 1 = s_i - 1$.
- So picking an OLD index also reduces total surplus by 1.

Wait! Every single move reduces the total surplus $S = \sum (A_i - 1)$ by exactly 1?
Let's check.
Initial state: $A_i$. Surplus $s_i = A_i - 1$.
Move on $i$: $A_i \to A_i - 1$.
New surplus $s_i' = (A_i - 1) - 1 = A_i - 2 = s_i - 1$.
Yes! Every move reduces the total surplus by 1.

The game ends when all indices have been picked at least once.
Let $K$ be the total number of moves.
The game ends at move $K$.
At this point, all indices are in $S$.
Does the game end when surplus reaches 0?
No. The game ends when $S=\{1,\dots,N\}$.
However, note that if $A_i=1$, you can pick it only once. After that, $A_i=0$, and you can't pick it again.
If $A_i > 1$, you can pick it multiple times.

The total number of moves $K$ is bounded by the total initial "capacity" $\sum A_i$.
But more importantly, consider the state when the game ends.
At the end, all indices are in $S$.
The total number of moves made is $K$.
The total reduction in surplus is $K$.
Initial surplus $S_{init} = \sum A_i - N$.
Final surplus $S_{final} = \sum (A_i^{final} - 1)$.
Note that $A_i^{final} \ge 0$.
Also, for each $i$, $A_i^{final} = A_i^{initial} - k_i$, where $k_i$ is the number of times $i$ was picked.
$\sum k_i = K$.
$S_{final} = \sum (A_i - k_i - 1) = \sum A_i - N - K = S_{init} - K$.

The game ends when the last new index is picked.
This doesn't directly fix $K$.

However, there is a known result for this specific problem (ABC 249 F? No, ABC 256? Actually, this is **AtCoder Beginner Contest 263, Problem F**? No. It is **AtCoder Beginner Contest 277, Problem F**? No.
This problem is **AtCoder Beginner Contest 283, Problem F**? No.
It is **AtCoder Beginner Contest 293, Problem F**? No.

Let's look at the constraints and the nature of the game.
Since every move reduces the total surplus by 1, and the game must end, the total number of moves $K$ is not fixed by the surplus alone because the game can end before the surplus is exhausted.

But wait!
If a player can choose to waste a move, they can change the parity of the total moves.
If a player cannot waste a move (because all available indices have $A_i=1$ and are already picked, or no indices are left to pick and no surplus?), they must pick a new index.

Actually, the critical observation is:
**The player who makes the last move wins.**
The game ends when the $N$-th distinct index is picked.
Let's consider the total number of moves $K$.
$K = N + W$.
$W$ is the number of waste moves.
Each waste move requires an index $i \in S$ with $A_i > 1$ (remaining capacity).
Essentially, the "waste moves" are drawn from the total surplus $S_{init} = \sum A_i - N$.
However, you can only waste on an index if it has been picked AND still has $A_i > 1$.

If $S_{init} = 0$ (all $A_i=1$), then $W=0$. $K=N$.
Fennec wins if $N$ is odd.

If $S_{init} > 0$, can the first player always force a win?
Or does it depend on parity?

Let's look at Sample 2: N=2, A=[25, 29].
$S_{init} = 25+29-2 = 52$.
Output: Snuke.
$N=2$ (Even). If $W=0$, Snuke wins.
Can Fennec force $W$ to be odd?
If Fennec wastes a move, $W$ increases by 1.
But Snuke can also waste.

Actually, this is a **parity game on the total number of moves**.
The total number of moves $K$ satisfies $N \le K \le \sum A_i$.
But more specifically, the game is equivalent to:
There are $N$ "mandatory" moves (one for each index).
There are $S_{init}$ "optional" moves (surplus).
However, the optional moves can only be taken on indices that are already "activated".

This is equivalent to a game where:
1. Players must take turns picking an unactivated index until all are activated.
2. At any point, a player can choose to "burn" a surplus token from an activated index.

But the players can interleave these.
Actually, if there is ANY surplus ($S_{init} > 0$), the player whose turn it is can choose to waste a move if there is an activated index with surplus.
If there are no activated indices with surplus, they MUST pick a new index.

Let's analyze the parity.
If $S_{init}$ is even, and $N$ is even, Snuke wins (Sample 2).
If $S_{init}$ is even, and $N$ is odd?
Sample 1: N=3, A=[1,9,2]. $S_{init} = 1+9+2-3 = 9$ (Odd).
Output: Fennec.
$N=3$ (Odd). $S_{init}=9$ (Odd).

Let's test N=1, A=[2]. $S_{init} = 2-1=1$ (Odd).
Output: Fennec.
$N=1$ (Odd).

Let's test N=2, A=[1,1]. $S_{init} = 0$ (Even).
Output: Snuke.
$N=2$ (Even).

Let's test N=2, A=[1,2]. $S_{init} = 1+2-2=1$ (Odd).
Earlier I concluded Snuke wins for A=[1,2].
Let's re-verify A=[1,2].
Fennec moves:
- Pick 1 (new). S={1}. A=[0,2]. Surplus of 1 is 0. Surplus of 2 is 1.
  Snuke moves:
  - Pick 2 (new). S={1,2}. Game ends. Snuke wins.
- Pick 2 (new). S={2}. A=[1,1]. Surplus of 2 is 0. Surplus of 1 is 0.
  Snuke moves:
  - Pick 1 (new). S={1,2}. Game ends. Snuke wins.
So Snuke wins.
Here $N=2$ (Even), $S_{init}=1$ (Odd). Snuke wins.

Let's test N=3, A=[1,1,1]. $S_{init}=0$.
$N=3$ (Odd). Fennec picks 1. Snuke picks 2. Fennec picks 3. Fennec wins.

Let's test N=3, A=[1,1,2]. $S_{init}=1$.
Fennec moves:
- Pick 3 (new). S={3}. A=[1,1,1]. Surplus 0.
  Snuke picks 1. S={1,3}.
  Fennec picks 2. S={1,2,3}. Fennec wins.
- Pick 1 (new). S={1}. A=[0,1,2].
  Snuke picks 2. S={1,2}. A=[0,0,2].
  Fennec picks 3. S={1,2,3}. Fennec wins.
- Pick 2 (new). Similar.
So Fennec wins.
$N=3$ (Odd), $S_{init}=1$ (Odd). Fennec wins.

It seems the winner is determined by the parity of $N$?
If $N$ is odd, Fennec wins.
If $N$ is even, Snuke wins.

Let's check Sample 2 again. N=2 (Even) -> Snuke.
Sample 3. N=6 (Even) -> Snuke.
Sample 1. N=3 (Odd) -> Fennec.

Is it just the parity of $N$?
Let's try to break it.
N=2, A=[100, 100]. $S_{init} = 198$ (Even).
If parity of N determines it, Snuke wins.
Can Fennec force a win?
Fennec picks 1. S={1}.
Snuke picks 2. S={1,2}. Game ends. Snuke wins.
Fennec picks 1. S={1}.
Snuke wastes on 1? S={1}. A=[98,100].
Fennec picks 2. S={1,2}. Game ends. Fennec wins?
Wait. If Snuke wastes, he might lose.
Snuke plays optimally.
If Snuke picks 2, he wins immediately. So he will pick 2.
So Snuke wins.

What if N=2, A=[1, 100]?
Fennec picks 1. S={1}. A=[0,100].
Snuke picks 2. S={1,2}. Snuke wins.
Fennec picks 2. S={2}. A=[1,99].
Snuke picks 1. S={1,2}. Snuke wins.
Snuke wins.

What if N=3, A=[1,1,100]?
Fennec picks 3. S={3}.
Snuke picks 1. S={1,3}.
Fennec picks 2. S={1,2,3}. Fennec wins.
Fennec wins.

It seems the answer is simply:
**If N is odd, Fennec wins. If N is even, Snuke wins.**

Why?
The game ends when the $N$-th distinct index is picked.
The player who picks the $N$-th distinct index wins.
The players can waste moves, but wasting a move does not change the fact that $N$ new moves are required.
However, wasting a move changes the parity of the total move count.
But notice: if a player wastes a move, the other player can just pick a new index (if available) or also waste.
The key is that the player who is "behind" in terms of parity can be forced to waste, or the player who is "ahead" can force the end.

Actually, there is a simpler argument:
The total number of moves $K$ has the same parity as $N + W$.
If $S_{init} > 0$, the player who wants to change the parity of $K$ can do so by wasting a move, PROVIDED they have a move available.
But if $N$ is odd, Fennec makes moves 1, 3, ..., N. The N-th move is made by Fennec.
If no waste moves are made, Fennec wins.
If waste moves are made, they come in pairs? No.

However, in all samples and small cases, the parity of $N$ seems to dictate the winner.
Let's assume the answer is based on the parity of $N$.