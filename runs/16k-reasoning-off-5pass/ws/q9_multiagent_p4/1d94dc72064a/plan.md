The game is impartial and finite, but the winning condition depends on the parity of the total number of moves required to reach the state where $S = \{1, 2, \dots, N\}$. Each index $i$ must be added to $S$ exactly once, which happens on the first turn a player chooses index $i$ while $A_i > 0$. After that, any subsequent decrements of $A_i$ do not affect the set $S$. To minimize/maximize the total moves, players will choose to decrement $A_i$ only after index $i$ has been added to $S$, effectively burning down the remaining value of $A_i$. The total number of moves is the sum of the initial $A_i$ values minus the number of "wasted" moves where a player is forced to decrement an $A_i$ before it is added to $S$? Actually, let's re-evaluate.
Wait, the player who makes the move that completes $S$ wins. This means the player who makes the $M$-th move wins if $M$ is odd (Fennec), or loses if $M$ is even (Snuke), assuming the game *must* end in exactly $M$ moves.
However, players can choose *which* index to decrement.
If $A_i > 0$, a player can choose to decrement $A_i$. If $i \notin S$, $i$ gets added. If $i \in S$, it doesn't.
The game ends when $S$ is full.
Consider the total number of decrements needed to make all $A_i = 0$? No, the game stops as soon as $S$ is full.
Let $k$ be the number of indices $i$ where $A_i > 0$. Since $A_i \ge 1$ for all $i$ (given positive integers), all indices will eventually be added to $S$.
The crucial observation in similar problems (like AtCoder ABC 178 D or similar combinatorial games) is often about the parity of the sum or specific counts.
Let's trace the logic:
Every index $i$ must be "activated" (added to $S$) exactly once. This happens on the very first time index $i$ is chosen.
After index $i$ is in $S$, any further choices of $i$ just decrement $A_i$ without changing $S$.
Players want to control the parity of the total moves.
Total moves = (Moves to activate all indices) + (Moves to decrement remaining values of activated indices).
Actually, players can interleave these.
But note: Once $i \in S$, the value $A_i$ acts like a pile of stones that can be removed one by one. Before $i \in S$, the first removal also removes a stone but activates $i$.
So for each $i$, the total number of times it is chosen is exactly $A_i$.
The game ends when the last index is added to $S$.
Let $T$ be the total number of moves. The winner is determined by $T \pmod 2$.
Can players change $T$?
Suppose we have indices $1, \dots, N$. Each $i$ must be chosen $A_i$ times.
The game ends immediately after the move that adds the last missing index to $S$.
Let $U$ be the set of indices not yet in $S$. Initially $U = \{1, \dots, N\}$.
In each step, a player picks $i$.
If $i \in U$: $i$ is removed from $U$, $A_i$ becomes $A_i-1$.
If $i \notin U$: $A_i$ becomes $A_i-1$.
The game ends when $U$ is empty.
Notice that the total number of times index $i$ is chosen is exactly $A_i$.
Let $x_i$ be the number of times index $i$ is chosen *before* it is added to $S$. Since it must be added on the first choice, $x_i$ is either 0 (if chosen first) or... wait.
If I choose $i$ and $i \notin S$, it gets added. So $i$ is added on the *first* time it is chosen.
Therefore, for every $i$, exactly 1 choice of $i$ results in $i$ entering $S$. The other $A_i - 1$ choices result in $i$ staying in $S$.
Total moves = $\sum_{i=1}^N A_i$.
Wait, is it possible to stop earlier? No, because $A_i$ are positive integers. You cannot skip a turn. You must decrement.
The game ends exactly when the last index enters $S$.
Since every index $i$ must be chosen exactly $A_i$ times in total (because you can't choose it if $A_i=0$, and you stop only when $S$ is full, but you can't choose $i$ if $A_i=0$ anyway), the total number of moves performed in the entire game is exactly $\sum A_i$.
Why? Because the game stops when $S$ is full. At that moment, for every $i$, $i \in S$. This implies every $i$ has been chosen at least once.
Could an index be chosen more than $A_i$ times? No, because $A_i$ starts positive and decreases by 1 each time. If $A_i$ reaches 0, you can't choose it anymore.
So the total number of moves is exactly $\sum A_i$.
The winner is determined by the parity of $\sum A_i$.
If $\sum A_i$ is odd, Fennec (1st player) makes the last move (1, 3, 5...).
If $\sum A_i$ is even, Snuke (2nd player) makes the last move (2, 4, 6...).
Wait, let's check Sample 1:
A = [1, 9, 2]. Sum = 12. Even.
Sample output says Fennec wins.
My logic "Total moves = Sum" implies Snuke wins. Contradiction.
Re-read the rules carefully.
"Choose an index i such that $1 \le A_i$. Subtract 1 from $A_i$, and if $i \notin S$, add $i$ to $S$."
"If $S = \{1, \dots, N\}$, the game ends and the player who performed the last operation wins."
In Sample 1:
Fennec chooses 2. $A_2=8, S=\{2\}$.
Snuke chooses 2. $A_2=7, S=\{2\}$.
Fennec chooses 1. $A_1=0, S=\{1,2\}$.
Snuke chooses 2. $A_2=6, S=\{1,2\}$.
Fennec chooses 3. $A_3=1, S=\{1,2,3\}$. Game ends. Fennec wins.
Total moves in this example: 5.
Sum of A was 12.
Why did the sum decrease?
Ah, the game ends *as soon as* $S$ is full.
In the example:
Start: A=(1,9,2). Sum=12.
1. F picks 2. A=(1,8,2). Sum=11. S={2}.
2. S picks 2. A=(1,7,2). Sum=10. S={2}.
3. F picks 1. A=(0,7,2). Sum=9. S={1,2}.
4. S picks 2. A=(0,6,2). Sum=8. S={1,2}.
5. F picks 3. A=(0,6,1). Sum=7. S={1,2,3}. END.
The game ended when $S$ became full. At that point, $A_1=0, A_3=1, A_2=6$.
The remaining values $A_2=6$ and $A_3=1$ were NOT fully decremented to 0.
The game stops immediately upon completing $S$.
So the total number of moves is NOT $\sum A_i$.
The total number of moves is the number of steps to cover all indices.
Let $k$ be the number of indices $i$ such that $A_i > 0$. Initially all $N$.
Actually, the structure is:
We need to pick each index $i$ at least once to get it into $S$.
Once $i \in S$, we can pick it again to burn $A_i$.
But the game stops as soon as the last index enters $S$.
This looks like a game where players can choose to "activate" an index or "burn" an already activated index.
However, notice that if $A_i = 1$, picking $i$ activates it and sets $A_i=0$. You can never pick $i$ again.
If $A_i > 1$, picking $i$ activates it (if not already) and sets $A_i = A_i - 1$. You can pick it again later.
Key Insight:
Consider the indices with $A_i = 1$. Let this set be $Z$.
For any $i \in Z$, the only move involving $i$ is to pick it, which activates $i$ and sets $A_i=0$. After that, $i$ can never be picked again.
For any $i \notin Z$ (i.e., $A_i \ge 2$), a player can pick $i$. If $i$ is not in $S$, it gets added and $A_i$ becomes $A_i-1 \ge 1$. If $i$ is in $S$, $A_i$ becomes $A_i-1$.
Crucially, if $A_i \ge 2$, the player can choose to "waste" a move on $i$ even if $i$ is already in $S$, or activate it.
But wait, if $A_i \ge 2$, can a player force the game to continue?
Actually, the game is determined by the parity of the number of "mandatory" moves vs "optional" moves?
Let's look at the sample 1 again.
$A = [1, 9, 2]$.
$A_1 = 1$ (Mandatory: pick 1 once to activate, then done).
$A_3 = 2$ (Can be picked twice).
$A_2 = 9$ (Can be picked 9 times).
Total moves = 5.
Moves breakdown:
- Activate 1: 1 move.
- Activate 2: 1 move.
- Activate 3: 1 move.
- Extra moves on 2: 4 moves (since $9-1=8$? No, in the example $A_2$ went $9 \to 8 \to 7 \to 6$. That's 3 extra moves? Wait.
Initial $A_2=9$.
Move 1: F picks 2. $A_2=8$. (Activated).
Move 2: S picks 2. $A_2=7$.
Move 4: S picks 2. $A_2=6$.
Total extra moves on 2 = 3.
Total moves = 1 (act 1) + 1 (act 2) + 1 (act 3) + 3 (extra) = 6? No, the example had 5 moves.
Let's re-trace the example carefully.
Start: 1, 9, 2.
1. F picks 2. $A=(1,8,2)$. S={2}. (Used 1 of 9).
2. S picks 2. $A=(1,7,2)$. S={2}. (Used 2 of 9).
3. F picks 1. $A=(0,7,2)$. S={1,2}. (Used 1 of 1).
4. S picks 2. $A=(0,6,2)$. S={1,2}. (Used 3 of 9).
5. F picks 3. $A=(0,6,1)$. S={1,2,3}. END.
Total moves = 5.
Indices activated: 2 (moves 1,2,4), 1 (move 3), 3 (move 5).
Number of activations = 3 (all indices).
Number of extra moves on 2 = 3 (moves 2, 4, and... wait. Move 1 was activation. Move 2 extra. Move 4 extra. Total 2 extra?
Initial $A_2=9$. Final $A_2=6$. Difference = 3.
So 3 moves were made on index 2.
Total moves = (Sum of activations) + (Sum of extra moves).
Sum of activations = $N$ (since all must be activated).
Sum of extra moves = $\sum (A_i - 1)$ for those $i$ where we chose to do extra moves?
No, the total number of moves is simply the number of steps until $S$ is full.
Let $k$ be the number of indices with $A_i = 1$.
Let $m$ be the number of indices with $A_i \ge 2$.
If $A_i = 1$, that index MUST be picked exactly once, and then it's done. It contributes 1 to the total count and cannot be used for extra moves.
If $A_i \ge 2$, that index can be picked multiple times.
Actually, the game is equivalent to:
We have $N$ items to collect.
Items with $A_i=1$ can only be collected once.
Items with $A_i \ge 2$ can be collected once (to get the item) and then "burned" any number of times.
But the game ends as soon as all items are collected.
This is a standard game theory problem.
If there is at least one index with $A_i \ge 2$, the player who moves can control the parity?
Let's analyze based on the count of $A_i=1$.
Case 1: All $A_i = 1$.
Then every move activates a new index. Total moves = $N$.
Winner: Fennec if $N$ is odd, Snuke if $N$ is even.
Case 2: There exists some $A_i \ge 2$.
Let $k$ be the number of indices with $A_i = 1$.
Let $m$ be the number of indices with $A_i \ge 2$. ($m \ge 1$).
The indices with $A_i \ge 2$ can be used to "pad" the game length.
Specifically, if a player needs to change the parity of the total moves, they can use an index with $A_i \ge 2$ to make an extra move (if it's already activated) or activate it and then use it again?
Actually, if there is at least one $A_i \ge 2$, the second player (Snuke) can always mirror or adjust?
Let's look at Sample 2: $N=2, A=[25, 29]$. Both $\ge 2$.
Output: Snuke.
Sample 3: $N=6, A=[1, 9, 2, 25, 2, 9]$.
$A_1=1$. Others $\ge 2$.
Output: Snuke.
Hypothesis:
If all $A_i = 1$: Winner depends on $N \pmod 2$.
If there is at least one $A_i \ge 2$:
  If $N$ is odd? Sample 1: $N=3$ (odd), has $A_i \ge 2$, Winner Fennec.
  Sample 2: $N=2$ (even), has $A_i \ge 2$, Winner Snuke.
  Sample 3: $N=6$ (even), has $A_i \ge 2$, Winner Snuke.
  What if $N$ is odd and we have $A_i \ge 2$? Sample 1 says Fennec.
  What if $N$ is even and we have $A_i \ge 2$? Samples 2 and 3 say Snuke.
  Is it simply: If all $A_i=1$, check $N$. Else, if $N$ is odd -> Fennec, if $N$ is even -> Snuke?
  Wait, let's verify logic.
  If there is an $A_i \ge 2$, the player who faces the situation where only $A_i=1$ remain can be forced?
  Actually, consider the state where only indices with $A_i=1$ are left to be activated.
  Suppose we have $k$ indices with $A_i=1$ and $m$ indices with $A_i \ge 2$.
  The $m$ indices can be used to extend the game.
  If $m \ge 1$, the player who wants to win can ensure the total number of moves has a specific parity?
  Actually, if $m \ge 1$, the game length can be manipulated.
  Specifically, if the current number of moves needed to finish is $X$, and there is a "flexible" pile ($A_i \ge 2$), the current player can choose to add 1 or more moves?
  No, the game ends when the last index is picked.
  Let's think about the "last" index.
  The game ends when the $N$-th distinct index is picked.
  Suppose we have $k$ indices with $A_i=1$. These must be picked exactly once.
  Suppose we have $m$ indices with $A_i \ge 2$.
  The total number of moves will be $N + (\text{extra moves})$.
  The extra moves come from picking indices with $A_i \ge 2$ after they are activated.
  Can the players force the number of extra moves to be even or odd?
  If $m \ge 1$, the player whose turn it is can choose to pick an index with $A_i \ge 2$.
  If that index is not yet activated, it gets activated (count +1) and $A_i$ decreases.
  If it is already activated, it just decreases.
  The key is: Can the second player always mirror the first player to maintain parity?
  Or is it simpler?
  Let's re-examine Sample 1: $N=3$ (odd), has $\ge 2$. Fennec wins.
  Sample 2: $N=2$ (even), has $\ge 2$. Snuke wins.
  Sample 3: $N=6$ (even), has $\ge 2$. Snuke wins.
  Pattern: If there is any $A_i \ge 2$, the winner is determined by $N \pmod 2$.
  If $N$ is odd -> Fennec.
  If $N$ is even -> Snuke.
  What if all $A_i = 1$?
  Then total moves = $N$.
  If $N$ is odd -> Fennec.
  If $N$ is even -> Snuke.
  So the rule seems to be:
  If $N$ is odd, Fennec wins.
  If $N$ is even, Snuke wins.
  Wait, is it that simple?
  Let's check if there is any case where $N$ is even but Fennec wins.
  Suppose $N=2, A=[1, 1]$. Moves = 2. Snuke wins.
  Suppose $N=2, A=[2, 2]$.
  F picks 1. $A=[1,2], S=\{1\}$.
  S picks 2. $A=[1,1], S=\{1,2\}$. END. Snuke wins. (2 moves).
  Can Fennec force 3 moves?
  F picks 1. $A=[1,2], S=\{1\}$.
  S picks 1? $A=[0,2], S=\{1\}$.
  F picks 2. $A=[0,1], S=\{1,2\}$. END. (3 moves). Fennec wins?
  Wait, if Snuke plays optimally, he will avoid giving Fennec the win.
  In the scenario above:
  Start: 2, 2.
  F picks 1. State: $A=[1,2], S=\{1\}$.
  Snuke's turn. Options:
  1. Pick 1. $A=[0,2], S=\{1\}$.
     F's turn. Must pick 2 (only option to activate 2? No, can pick 2).
     F picks 2. $A=[0,1], S=\{1,2\}$. END. F wins.
  2. Pick 2. $A=[1,1], S=\{1,2\}$. END. Snuke wins.
  Snuke will choose option 2. So Snuke wins.
  So for $N=2, A=[2,2]$, Snuke wins.
  This matches "Even N -> Snuke".
  
  Is there any case where $N$ is odd and Snuke wins?
  Suppose $N=1, A=[2]$.
  F picks 1. $A=[1], S=\{1\}$. END. F wins.
  Suppose $N=3, A=[2,2,2]$.
  F picks 1. $A=[1,2,2], S=\{1\}$.
  S picks 2. $A=[1,1,2], S=\{1,2\}$.
  F picks 3. $A=[1,1,1], S=\{1,2,3\}$. END. F wins.
  Can Snuke prevent this?
  F picks 1.
  S picks 1? $A=[0,2,2], S=\{1\}$.
  F picks 2. $A=[0,1,2], S=\{1,2\}$.
  S picks 3. $A=[0,1,1], S=\{1,2,3\}$. END. Snuke wins?
  Wait, if S picks 3, $S$ becomes $\{1,2,3\}$. Snuke made the last move. Snuke wins.
  So if $N=3, A=[2,2,2]$, Snuke can win?
  Let's re-simulate $N=3, A=[2,2,2]$ with optimal play.
  Start: 2,2,2.
  F moves.
  Option A: F picks 1. $A=[1,2,2], S=\{1\}$.
    S moves.
    If S picks 2: $A=[1,1,2], S=\{1,2\}$.
      F moves.
      If F picks 3: $A=[1,1,1], S=\{1,2,3\}$. END. F wins.
      If F picks 1: $A=[0,1,2], S=\{1,2\}$.
        S moves.
        If S picks 3: $A=[0,1,1], S=\{1,2,3\}$. END. S wins.
        If S picks 2: $A=[0,0,2], S=\{1,2\}$.
          F picks 3. $A=[0,0,1], S=\{1,2,3\}$. END. F wins.
      So if F picks 1, S can win?
      Wait, if F picks 1, then S picks 2, then F picks 1?
      Let's trace:
      1. F: 1 -> (1,2,2), {1}
      2. S: 2 -> (1,1,2), {1,2}
      3. F: 1 -> (0,1,2), {1,2}
      4. S: 3 -> (0,1,1), {1,2,3}. END. Snuke wins.
      So if F plays 1, S can win.
    If S picks 1: $A=[0,2,2], S=\{1\}$.
      F moves.
      If F picks 2: $A=[0,1,2], S=\{1,2\}$.
        S moves.
        If S picks 3: $A=[0,1,1], S=\{1,2,3\}$. END. Snuke wins.
        If S picks 2: $A=[0,0,2], S=\{1,2\}$.
          F picks 3. $A=[0,0,1], S=\{1,2,3\}$. END. F wins.
      So S picks 3 and wins.
  It seems for $N=3, A=[2,2,2]$, Snuke wins.
  But my previous pattern "Odd N -> Fennec" was based on Sample 1 ($N=3, A=[1,9,2]$).
  In Sample 1, $A_1=1$.
  Here $A=[2,2,2]$, all $\ge 2$.
  So the condition might depend on whether there are $A_i=1$.
  
  Let's refine the hypothesis:
  Let $cnt1$ be the number of $A_i = 1$.
  Let $cntGe2$ be the number of $A_i \ge 2$.
  
  Case 1: $cntGe2 = 0$ (All $A_i = 1$).
    Total moves = $N$.
    Winner: Fennec if $N$ odd, Snuke if $N$ even.
  
  Case 2: $cntGe2 > 0$.
    If $N$ is odd:
      Sample 1 ($N=3$, has $\ge 2$): Fennec wins.
      My simulation of $N=3, [2,2,2]$ suggested Snuke wins.
      Let's re-evaluate $N=3, [2,2,2]$.
      Is it possible Fennec has a winning strategy?
      Maybe F picks 1, S picks 1, F picks 2, S picks 2, F picks 3?
      1. F: 1 -> (1,2,2), {1}
      2. S: 1 -> (0,2,2), {1}
      3. F: 2 -> (0,1,2), {1,2}
      4. S: 2 -> (0,0,2), {1,2}
      5. F: 3 -> (0,0,1), {1,2,3}. END. F wins.
      Ah! In step 4, S picked 2. $A_2$ went from 1 to 0.
      But $S=\{1,2\}$. $A_3=2$.
      Step 5: F picks 3. $A_3=1$. $S=\{1,2,3\}$. END.
      So F wins.
      Why did I think S wins earlier?
      In the previous trace:
      1. F: 1 -> (1,2,2), {1}
      2. S: 2 -> (1,1,2), {1,2}
      3. F: 1 -> (0,1,2), {1,2}
      4. S: 3 -> (0,1,1), {1,2,3}. END. S wins.
      So if S plays optimally (picking 2 in step 2), S wins?
      Wait, in step 2, S had choices: pick 1 or pick 2.
      If S picks 2 -> leads to S win (as traced).
      If S picks 1 -> leads to F win (as traced: F picks 2, S picks 3 -> S wins? No, let's re-trace S picks 1).
      Trace S picks 1:
      1. F: 1 -> (1,2,2), {1}
      2. S: 1 -> (0,2,2), {1}
      3. F: 2 -> (0,1,2), {1,2}
      4. S: 3 -> (0,1,1), {1,2,3}. END. S wins.
      So in both branches, Snuke wins?
      Wait, in branch 2 (S picks 1), step 4 S picks 3 and wins.
      In branch 1 (S picks 2), step 4 S picks 3 and wins?
      Let's re-check branch 1 step 4.
      State after 3: (0,1,2), {1,2}.
      S moves.
      If S picks 3: $A_3=1, S=\{1,2,3\}$. END. S wins.
      If S picks 2: $A_2=0, S=\{1,2\}$.
        F moves. Must pick 3. $A_3=1, S=\{1,2,3\}$. END. F wins.
      So S will pick 3 and win.
      So for $N=3, [2,2,2]$, Snuke wins.
      
      But Sample 1 ($N=3, [1,9,2]$) Fennec wins.
      Difference: Sample 1 has $A_1=1$.
      So the presence of $A_i=1$ matters.
      
      Revised Hypothesis:
      If there is any $A_i \ge 2$:
        If $N$ is odd, Fennec wins? (Sample 1 yes, but $[2,2,2]$ no).
        Wait, $[2,2,2]$ has $N=3$ (odd) and Snuke wins.
        Sample 1 has $N=3$ (odd) and Fennec wins.
        What is the difference? $A_1=1$ vs $A_1=2$.
        Maybe the condition is:
        If $N$ is odd and there is at least one $A_i=1$, Fennec wins?
        If $N$ is even and there is at least one $A_i=1$, Snuke wins?
        What if all $A_i \ge 2$?
        Sample 2 ($N=2$, all $\ge 2$): Snuke.
        My $[2,2,2]$ ($N=3$, all $\ge 2$): Snuke.
        So if all $A_i \ge 2$, Snuke always wins?
        Let's check $N=1, A=[2]$.
        F picks 1. $A=[1], S=\{1\}$. END. F wins.
        So $N=1$ (odd), all $\ge 2$, Fennec wins.
        So "All $\ge 2$ -> Snuke" is false for $N=1$.
        
        Let's try to find the invariant.
        The game is equivalent to:
        Total moves = $N + \sum_{i \in \text{activated}} (A_i - 1)$.
        But the game stops when the last index is activated.
        Let $k$ be the number of indices with $A_i=1$.
        If $k=N$, moves = $N$.
        If $k < N$, we have some flexibility.
        
        Actually, there is a known solution for this problem (AtCoder ABC 178 D? No, this is ABC 178 C? No. It's ABC 178 D is different. This is likely ABC 178 E? No.
        This is **AtCoder ABC 178 Problem D**? No.
        This is **AtCoder ABC 178 Problem C**? No.
        This is **AtCoder ABC 178 Problem ...**?
        Actually, this is **AtCoder ABC 178 Problem D** is "1 2 3 ...".
        Wait, the problem is **AtCoder ABC 178 Problem E**? No.
        It is **AtCoder ABC 178 Problem ...**?
        Actually, this is **AtCoder ABC 178 Problem D** is not it.
        This is **AtCoder ABC 178 Problem C**? No.
        This is **AtCoder ABC 178 Problem ...**?
        Wait, I recall this problem. It is **AtCoder ABC 178 Problem D**? No.
        It is **AtCoder ABC 178 Problem ...**?
        Actually, the problem is **AtCoder ABC 178 Problem D** is "1 2 3".
        The problem is **AtCoder ABC 178 Problem E**? No.
        The problem is **AtCoder ABC 178 Problem ...**?
        Okay, let's solve it logically.
        
        Let $cnt1$ be the number of $A_i=1$.
        If $cnt1 == N$:
          Winner = Fennec if $N \% 2 != 0$ else Snuke.
        Else ($cnt1 < N$):
          If $N$ is odd:
            Sample 1 ($N=3, cnt1=1$): Fennec.
            My $[2,2,2]$ ($N=3, cnt1=0$): Snuke.
          If $N$ is even:
            Sample 2 ($N=2, cnt1=0$): Snuke.
            Sample 3 ($N=6, cnt1=1$): Snuke.
            
          Pattern:
          If $N$ is even: Snuke always wins (regardless of $cnt1$).
          If $N$ is odd:
            If $cnt1 == N$: Fennec.
            If $cnt1 < N$:
              If $cnt1 == 0$: Snuke (from $[2,2,2]$).
              If $cnt1 > 0$: Fennec (from Sample 1).
              
          So for $N$ odd:
            If $cnt1 == N$: Fennec.
            If $cnt1 < N$:
               If $cnt1 == 0$: Snuke.
               If $cnt1 > 0$: Fennec.
          
          Wait, can we simplify?
          If $N$ is even -> Snuke.
          If $N$ is odd:
             If $cnt1 == 0$ -> Snuke.
             If $cnt1 > 0$ -> Fennec.
          
          Let's check $N=1, A=[2]$. $N=1$ (odd), $cnt1=0$.
          Prediction: Snuke.
          Reality: F picks 1, ends. F wins.
          So $N=1, cnt1=0$ -> Fennec.
          My pattern "If $cnt1=0$ -> Snuke" fails for $N=1$.
          
          Why $N=1$ is special?
          Because if $N=1$, the game ends in 1 move regardless of $A_1$.
          F moves, $S=\{1\}$, ends. F wins.
          So for $N=1$, Fennec always wins.
          
          What about $N=3, [2,2,2]$?
          F moves. $S=\{1\}$.
          S moves. Can S force a win?
          We found Snuke wins.
          So $N=3, cnt1=0$ -> Snuke.
          
          What about $N=3, [1,2,2]$? ($cnt1=1$).
          F moves.
          If F picks 1 (the 1): $A=[0,2,2], S=\{1\}$.
          S moves.
          If S picks 2: $A=[0,1,2], S=\{1,2\}$.
          F moves.
          If F picks 3: $A=[0,1,1], S=\{1,2,3\}$. END. F wins.
          If F picks 2: $A=[0,0,2], S=\{1,2\}$.
          S moves.
          If S picks 3: $A=[0,0,1], S=\{1,2,3\}$. END. S wins.
          So F should pick 3 and win.
          So $N=3, cnt1=1$ -> Fennec.
          
          So the rule for $N$ odd:
            If $cnt1 == 0$: Snuke (except $N=1$?).
            If $cnt1 > 0$: Fennec.
          But $N=1, cnt1=0$ -> Fennec.
          So if $N=1$, Fennec.
          If $N > 1$ and $N$ odd:
            If $cnt1 == 0$: Snuke.
            If $cnt1 > 0$: Fennec.
          
          And if $N$ even: Snuke.
          
          Let's combine:
          If $N$ is even: Snuke.
          If $N$ is odd:
            If $N == 1$: Fennec.
            Else if $cnt1 == 0$: Snuke.
            Else: Fennec.
            
          Is there a simpler way?
          Maybe: Snuke wins if ($N$ is even) OR ($N$ is odd AND $cnt1 == 0$ AND $N > 1$).
          Fennec wins otherwise.
          
          Let's double check $N=1, A=[1]$. $cnt1=1$. Fennec. (Correct).
          $N=1, A=[2]$. $cnt1=0$. Fennec. (Correct).
          $N=3, [2,2,2]$. $cnt1=0$. Snuke. (Correct).
          $N=3, [1,2,2]$. $cnt1=1$. Fennec. (Correct).
          $N=2, [1,1]$. $cnt1=2$. Snuke. (Correct).
          $N=2, [2,2]$. $cnt1=0$. Snuke. (Correct).
          
          So the logic holds.
          Algorithm:
          Read N.
          Read A.
          Count $cnt1$ (number of 1s).
          If $N \% 2 == 0$:
            Print Snuke.
          Else:
            If $N == 1$:
              Print Fennec.
            Else:
              If $cnt1 == 0$:
                Print Snuke.
              Else:
                Print Fennec.
                
          Wait, can we simplify the odd case?
          If $N$ is odd:
            Fennec wins if $cnt1 > 0$.
            Snuke wins if $cnt1 == 0$.
          Except $N=1$?
          If $N=1$, $cnt1$ can be 0 or 1.
          If $cnt1=0$ (i.e., $A_1 \ge 2$), Fennec wins.
          My rule says "If $cnt1==0$ -> Snuke". This is wrong for $N=1$.
          So $N=1$ is an exception.
          
          Final Logic:
          If $N$ is even: Snuke.
          If $N$ is odd:
             If $N == 1$: Fennec.
             Else:
                If $cnt1 == 0$: Snuke.
                Else: Fennec.
          
          This covers all samples.
          Sample 1: N=3 (odd), cnt1=1 (>0) -> Fennec. Correct.
          Sample 2: N=2 (even) -> Snuke. Correct.
          Sample 3: N=6 (even) -> Snuke. Correct.
          
          One more check: $N=3, [2,2,2]$. cnt1=0. -> Snuke. Correct.
          $N=1, [2]$. cnt1=0. -> Fennec. Correct.
          
          Implementation details:
          Read N.
          Read list A.
          Count 1s.
          Apply logic.