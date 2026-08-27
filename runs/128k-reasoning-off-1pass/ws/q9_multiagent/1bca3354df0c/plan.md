The game is played on a graph that is guaranteed to be bipartite (no odd cycles). Adding an edge between two vertices in the same connected component of a bipartite graph creates an odd cycle if and only if the two vertices have the same color in a valid 2-coloring. Therefore, a move is valid only if the chosen vertices belong to different connected components or, if they are in the same component, they have different colors. However, since the graph is bipartite, any edge added between two vertices in the *same* connected component must connect vertices of different colors to avoid creating an odd cycle. Wait, let's re-evaluate: If we add an edge $(u, v)$ in a bipartite component, the cycle formed has length equal to the distance between $u$ and $v$ plus 1. For the cycle to be even (allowed), the distance must be odd, meaning $u$ and $v$ must have different colors. If $u$ and $v$ have the same color, adding $(u, v)$ creates an odd cycle (forbidden). Thus, a move consists of adding an edge between $u$ and $v$ where $u$ and $v$ are in the same component and have different colors, OR $u$ and $v$ are in different components.
Actually, the standard interpretation of this specific problem (AtCoder ABC 278 F or similar logic) is simpler: The game ends when the graph becomes a complete bipartite graph across all components? No.
Let's reconsider the invariant. The total number of possible edges in a bipartite graph with partition sizes $S_1, S_2$ is $S_1 \times S_2$. The current number of edges is $M$. The maximum number of edges we can add within a connected component $C$ with partition sizes $a$ and $b$ is $a \times b - (\text{current edges in } C)$.
Wait, if we add an edge between two components, they merge. This changes the partition sizes.
Key Insight: This game is equivalent to Nim with a specific pile size. The total number of moves available is fixed regardless of the order of moves?
Let's check Sample 1: 4 vertices, edges (1,2), (2,3), (3,4). Path 1-2-3-4. Bipartition: {1,3} and {2,4}. Sizes 2 and 2. Max edges in bipartite graph = $2 \times 2 = 4$. Current edges = 3. Moves = $4-3=1$. Aoki takes the last move. Aoki wins.
Sample 2: 4 vertices, edges (1,2), (3,4). Two components. Comp1: {1,2}, sizes 1,1. Max edges $1\times1=1$. Current 1. Moves=0. Comp2: {3,4}, sizes 1,1. Max edges 1. Current 1. Moves=0. Total moves = 0. Takahashi wins.
Sample 3: 9 vertices, 5 edges. Components: {2,9,3} (triangle? No, no odd cycles). Edges: (2,9), (2,3). Path 9-2-3. Bipartition {9,3}, {2}. Sizes 2,1. Max edges $2\times1=2$. Current 2. Moves=0. Component {4,6}. Sizes 1,1. Max 1. Current 1. Moves=0. Component {5,7}. Sizes 1,1. Max 1. Current 1. Moves=0. Component {1,8}. Sizes 1,1. Max 1. Current 1. Moves=0. Total moves = 0? But output says Aoki wins.
Ah, I missed something in Sample 3. Edges: (2,9), (2,3), (4,6), (5,7), (1,8).
Comp 1: 2-9, 2-3. Vertices {2,3,9}. Edges (2,9), (2,3). This is a star. Bipartition: Center {2}, Leaves {3,9}. Sizes 1 and 2. Max edges $1\times2=2$. Current edges 2. Moves=0.
Comp 2: 4-6. Sizes 1,1. Max 1. Current 1. Moves=0.
Comp 3: 5-7. Sizes 1,1. Max 1. Current 1. Moves=0.
Comp 4: 1-8. Sizes 1,1. Max 1. Current 1. Moves=0.
Total moves = 0? Why does Aoki win?
Maybe my assumption that "moves = max_edges - current_edges" is wrong because adding an edge merges components.
If I add an edge between Comp A and Comp B, they merge into a larger bipartite graph. The new max edges is $(a_1+b_1)(a_2+b_2)$. The cost is 1 edge. The potential moves increase.
This looks like a game on the number of edges in the complete bipartite graph formed by merging components.
Actually, there is a known result for this game: The game is equivalent to Nim with a single pile of size $K$, where $K$ is the total number of edges that can be added to make the graph a complete bipartite graph *if we were allowed to merge components arbitrarily*? No.
Let's re-read the condition: "Adding an edge ... does not create an odd cycle."
If we have two components $C_1$ and $C_2$ with bipartitions $(A_1, B_1)$ and $(A_2, B_2)$.
If we add an edge between $u \in A_1$ and $v \in A_2$, the new component has partition $(A_1 \cup B_2, B_1 \cup A_2)$.
The number of edges in a complete bipartite graph with partitions $X, Y$ is $|X||Y|$.
Let $f(C)$ be the number of edges that can be added to component $C$ to make it complete bipartite. $f(C) = |A_C||B_C| - |E_C|$.
When we merge $C_1$ and $C_2$ by adding an edge between $u \in A_1, v \in A_2$:
New partitions: $X = A_1 \cup B_2$, $Y = B_1 \cup A_2$.
New capacity: $|X||Y| = (|A_1|+|B_2|)(|B_1|+|A_2|) = |A_1||B_1| + |A_1||A_2| + |B_2||B_1| + |B_2||A_2|$.
Old capacity sum: $|A_1||B_1| + |A_2||B_2|$.
Increase in capacity: $|A_1||A_2| + |B_1||B_2|$.
We used 1 edge. Net gain in "potential moves" = $|A_1||A_2| + |B_1||B_2| - 1$.
This depends on the choice of $u, v$.
However, note that $|A_1||A_2| + |B_1||B_2| = |A_1||A_2| + |B_1||B_2|$.
Is it possible that the total number of moves is always constant?
Let's check Sample 3 again.
Components:
1: {2,3,9}, A={2}, B={3,9}. $|A|=1, |B|=2$. $E=2$. Cap=$1\times2=2$. $f=0$.
2: {4,6}, A={4}, B={6}. $|A|=1, |B|=1$. $E=1$. Cap=1. $f=0$.
3: {5,7}, A={5}, B={7}. $f=0$.
4: {1,8}, A={1}, B={8}. $f=0$.
Total $f=0$.
If Aoki adds edge (1,4) (connecting Comp 4 and Comp 2).
$u=1 \in A_4, v=4 \in A_2$.
New Comp: $A' = A_4 \cup B_2 = \{1, 6\}$, $B' = B_4 \cup A_2 = \{8, 4\}$.
Sizes: $|A'|=2, |B'|=2$.
Current edges: 2 (original) + 1 (new) = 3.
Max edges: $2\times2=4$.
Remaining moves: $4-3=1$.
So after Aoki's move, there is 1 move left for Takahashi. Takahashi takes it. Then Aoki has no moves. Aoki loses?
But Sample 3 output is Aoki.
Wait, if Aoki adds (1,4), Takahashi can add (1,6)?
Let's trace carefully.
Start: 4 comps.
Aoki adds (1,4). Merges {1,8} and {4,6}.
New comp: {1,4,6,8}. Edges (1,4).
Bipartition: One side {1,6}, other {4,8}. (Since 1-4 is edge, 1 and 4 diff colors. 4-6 edge, 4 and 6 diff colors -> 1 and 6 same color. 1-8 edge, 1 and 8 diff colors -> 8 and 6 same color).
Sizes: 2 and 2. Edges: 2. Max: 4. Moves left: 1.
Takahashi must add an edge. Options in {1,4,6,8}:
Pairs with diff colors: (1,8) [same color? No, 1 and 8 diff], (4,6) [same color? No, 4 and 6 diff].
Wait, in {1,4,6,8}:
Edges: (1,4).
Colors: 1(W), 4(B).
4-6 exists -> 6(W).
1-8 exists -> 8(B).
So W={1,6}, B={4,8}.
Valid moves (W-B):
(1,4) - exists.
(1,8) - exists.
(6,4) - exists.
(6,8) - does not exist. Add (6,8).
So Takahashi adds (6,8).
Now graph has edges (1,4), (4,6), (1,8), (6,8). This is a cycle 1-4-6-8-1 (length 4).
Is it complete bipartite? $K_{2,2}$. Edges: 4. Current: 4.
No moves left. Takahashi made the last move. Aoki has no moves. Aoki loses.
This contradicts Sample 3 output (Aoki wins).
Therefore, my assumption that Aoki *must* merge components to win is wrong, or the game logic is different.
Maybe Aoki can add an edge *within* a component?
In Sample 3, all components are already complete bipartite. So no internal moves.
So Aoki *must* merge.
If Aoki merges, Takahashi responds and wins?
Unless... there is a strategy where Aoki merges such that the resulting state has an odd number of moves?
Let's re-calculate the "value" of a component.
Let $N_A$ and $N_B$ be the sizes of the two partitions. The number of edges in a complete bipartite graph is $N_A N_B$.
The number of edges currently present is $M$.
The "potential" is $N_A N_B - M$.
When merging two components $(A_1, B_1)$ and $(A_2, B_2)$ with an edge between $u \in A_1, v \in A_2$:
New partitions: $A' = A_1 \cup B_2$, $B' = B_1 \cup A_2$.
New potential: $(|A_1|+|B_2|)(|B_1|+|A_2|) - (M_1 + M_2 + 1)$.
Old potential sum: $(|A_1||B_1| - M_1) + (|A_2||B_2| - M_2)$.
Difference (New - Old) = $(|A_1||B_1| + |A_1||A_2| + |B_2||B_1| + |B_2||A_2| - M_1 - M_2 - 1) - (|A_1||B_1| - M_1 + |A_2||B_2| - M_2)$
$= |A_1||A_2| + |B_1||B_2| - 1$.
This value is constant regardless of which specific $u, v$ are chosen (as long as they are in the "same" partition sets relative to the merge).
Wait, we can choose to merge $u \in A_1$ with $v \in B_2$ instead?
If $u \in A_1, v \in B_2$:
New partitions: $A' = A_1 \cup A_2$, $B' = B_1 \cup B_2$.
New potential: $(|A_1|+|A_2|)(|B_1|+|B_2|) - (M_1+M_2+1)$.
Difference = $(|A_1||B_1| + |A_1||B_2| + |A_2||B_1| + |A_2||B_2| - M_1 - M_2 - 1) - (|A_1||B_1| - M_1 + |A_2||B_2| - M_2)$
$= |A_1||B_2| + |A_2||B_1| - 1$.
So the gain depends on whether we align $A$ with $A$ or $A$ with $B$.
This suggests the game is complex.
However, there is a known property for this specific problem (AtCoder ABC 278 F is different, this is likely ABC 278 E or similar? No, this is **AtCoder Grand Contest 063 Problem B**? No. It is **AtCoder Beginner Contest 278 Problem F**? No.
Actually, this is **AtCoder Beginner Contest 278 Problem F** is "1111...".
Let's search the problem text mentally. "Takahashi and Aoki will play a game... odd cycle".
This is **AtCoder Beginner Contest 278 Problem F** is not it.
It is **AtCoder Beginner Contest 278 Problem G**? No.
It is **AtCoder Beginner Contest 278 Problem F** is "1111".
Wait, the problem is **AtCoder Beginner Contest 278 Problem F** is not it.
The problem is **AtCoder Beginner Contest 278 Problem F** is "1111".
Let's try to identify the problem source. It looks like **AtCoder Beginner Contest 278 Problem F** is not it.
Maybe **AtCoder Beginner Contest 278 Problem F** is "1111".
Okay, let's ignore the source and solve logically.
Is the total number of moves always odd or even?
In Sample 1: 1 move. Aoki wins.
In Sample 2: 0 moves. Takahashi wins.
In Sample 3: Aoki wins.
In Sample 3, if Aoki merges, we saw Takahashi wins. So Aoki must have another move?
But all components are complete bipartite. No internal moves.
So Aoki MUST merge.
If Aoki merges, and Takahashi wins, then Sample 3 output "Aoki" implies my simulation of the merge was suboptimal for Aoki, or my simulation of Takahashi's response was suboptimal.
In Sample 3, Aoki merges {1,8} and {4,6}.
Resulting component {1,4,6,8} with edges (1,4).
Partitions: {1,6} and {4,8}.
Moves available: (6,8). Only 1 move.
So if Aoki merges, Takahashi takes the last move. Aoki loses.
So Aoki should NOT merge? But he has no other choice.
Unless... I misidentified the components in Sample 3.
Input:
2 9
2 3
4 6
5 7
1 8
Edges: (2,9), (2,3), (4,6), (5,7), (1,8).
Comp 1: 2-9, 2-3. Vertices {2,3,9}. Edges 2. Bipartite? Yes. Star graph. Complete bipartite? Yes ($K_{1,2}$).
Comp 2: 4-6. $K_{1,1}$. Complete.
Comp 3: 5-7. $K_{1,1}$. Complete.
Comp 4: 1-8. $K_{1,1}$. Complete.
All components are complete bipartite.
So any move MUST merge two components.
If Aoki merges any two, say $C_i, C_j$, the new component has potential moves $P_{new}$.
The number of moves remaining in the game is $P_{new}$.
If $P_{new}$ is odd, the next player (Takahashi) faces an odd number of moves? No, the game is not just "number of moves". It's a game where players choose which merge to do.
But in Sample 3, all components are size 2 (or 3).
Merging any two $K_{1,1}$s:
$C_1: 1,1$. $C_2: 1,1$.
Merge $A-A$: New sizes $1+1=2, 1+1=2$. Edges $1+1+1=3$. Max $2\times2=4$. Moves $4-3=1$.
Merge $A-B$: New sizes $1+1=2, 1+1=2$. Edges $1+1+1=3$. Max $4$. Moves $1$.
So any merge of two $K_{1,1}$ results in a component with 1 move left.
Then Takahashi takes that 1 move. Game over. Aoki loses.
This implies Aoki loses in Sample 3. But the sample output says Aoki wins.
Contradiction.
Is it possible that the initial graph in Sample 3 is NOT complete bipartite?
Edges: (2,9), (2,3).
Vertices 2,3,9.
Edges: 2-9, 2-3.
Is 3-9 an edge? No.
So it is $K_{1,2}$. It is complete.
Wait, maybe I am misinterpreting the problem statement "G does not contain an odd cycle".
Maybe the game allows adding edges that create odd cycles? No, "does not create an odd cycle".
Is it possible that the sample output 3 is correct and my logic about "complete bipartite" is wrong?
Maybe the game is not about "moves remaining" but about the structure.
Let's reconsider the "value" of the game.
Maybe the total number of moves is simply the sum of $(|A_i||B_i| - M_i)$?
Sample 1: $2\times2 - 3 = 1$. Odd -> Aoki wins.
Sample 2: $(1\times1-1) + (1\times1-1) = 0$. Even -> Takahashi wins.
Sample 3: $(1\times2-2) + (1\times1-1) + (1\times1-1) + (1\times1-1) = 0 + 0 + 0 + 0 = 0$. Even -> Takahashi should win.
But output is Aoki.
So the simple sum formula is wrong.
The merging changes the sum.
Let $S = \sum (|A_i||B_i| - M_i)$.
When merging $C_1, C_2$ via $A-A$:
New term: $(|A_1|+|B_2|)(|B_1|+|A_2|) - (M_1+M_2+1)$.
Old terms: $(|A_1||B_1| - M_1) + (|A_2||B_2| - M_2)$.
Change: $|A_1||A_2| + |B_1||B_2| - 1$.
If we merge $A-B$:
Change: $|A_1||B_2| + |B_1||A_2| - 1$.
In Sample 3, all components are $K_{1,1}$ or $K_{1,2}$.
$K_{1,1}$: $|A|=1, |B|=1$.
$K_{1,2}$: $|A|=1, |B|=2$.
If we merge two $K_{1,1}$:
Option A-A: Change $1\times1 + 1\times1 - 1 = 1$.
Option A-B: Change $1\times1 + 1\times1 - 1 = 1$.
So merging two $K_{1,1}$ increases the total potential by 1.
Start sum = 0.
After 1st move (Aoki): Sum = 1.
Takahashi faces Sum=1. He must make a move.
If he merges two components (one is the new big one, one is a $K_{1,1}$):
Big one: $K_{2,2}$ (from merging two $K_{1,1}$). $|A|=2, |B|=2, M=3$. Potential $4-3=1$.
Other: $K_{1,1}$. Potential 0.
Merge Big ($2,2$) and Small ($1,1$).
Align $A(2)$ with $A(1)$: Change $2\times1 + 2\times1 - 1 = 3$.
Align $A(2)$ with $B(1)$: Change $2\times1 + 2\times1 - 1 = 3$.
New Sum = $1 + 3 = 4$.
Then Aoki faces Sum=4.
This seems to grow.
But the game must end. The maximum number of edges in a bipartite graph on $N$ vertices is $\lfloor N^2/4 \rfloor$.
The total number of edges added is bounded.
The game is finite.
Is it possible the winner is determined by the parity of the total number of edges that can be added to make the graph a complete bipartite graph *across all vertices*?
No, because components can be merged.
Actually, there is a known result: The game is equivalent to Nim with a single pile of size $K$, where $K$ is the number of edges in the complete bipartite graph on $N$ vertices minus the current edges, MINUS something?
Wait, if the graph is bipartite, the maximum number of edges is $\lfloor N^2/4 \rfloor$.
Let $MaxEdges = \lfloor N^2/4 \rfloor$.
Current edges $M$.
Is the answer simply based on $(MaxEdges - M)$?
Sample 1: $N=4$. Max $4$. $M=3$. Diff=1. Odd -> Aoki. Correct.
Sample 2: $N=4$. Max $4$. $M=2$. Diff=2. Even -> Takahashi. Correct.
Sample 3: $N=9$. Max $\lfloor 81/4 \rfloor = 20$. $M=5$. Diff=15. Odd -> Aoki. Correct.
Hypothesis: The winner is determined by the parity of $\lfloor N^2/4 \rfloor - M$.
If $(\lfloor N^2/4 \rfloor - M)$ is odd, Aoki wins. Else Takahashi.
Let's verify the logic.
The game allows merging components. The final state of the game is a single connected component which is a complete bipartite graph $K_{\lfloor N/2 \rfloor, \lceil N/2 \rceil}$.
The total number of edges in the final state is $\lfloor N^2/4 \rfloor$.
Every move adds exactly 1 edge.
Does every sequence of moves lead to the same final number of edges?
Yes, because the final graph must be a complete bipartite graph on $N$ vertices (since no odd cycles allowed, and to maximize edges, it must be complete bipartite).
Wait, does the game *force* the graph to become a single component?
The game ends when no more edges can be added.
Can we have a state with multiple components where no edges can be added?
Yes, if every component is complete bipartite.
But players play optimally.
If the current state is a set of complete bipartite components, the current player must merge two components.
Merging two components increases the total number of edges in the final complete bipartite graph? No.
The "final" graph depends on how we merge.
If we stop with multiple components, the total edges is $\sum |A_i||B_i|$.
If we merge everything into one component, total edges is $\lfloor N^2/4 \rfloor$.
Since players want to win, they will try to force the game into a state where the number of remaining moves is favorable.
However, note that $\sum |A_i||B_i| \le \lfloor N^2/4 \rfloor$.
The maximum possible edges is achieved when there is only one component.
If a player can make a move that leads to a state with an odd number of total possible future moves, they might win.
But actually, the key insight in such games is often that the total number of moves is fixed regardless of strategy, OR the game is equivalent to a single pile of size $K = \lfloor N^2/4 \rfloor - M$.
Why would the total moves be fixed?
Consider the potential function $P = \lfloor N^2/4 \rfloor - (\text{current edges})$.
When we add an edge, current edges increases by 1.
But the max edges might also increase if components merge?
No, the max edges for a fixed partition of vertices is fixed. But the partition changes.
Actually, the maximum number of edges in a bipartite graph on $N$ vertices is always $\lfloor N^2/4 \rfloor$, regardless of connectivity.
Wait, if we have two components $K_{1,1}$ and $K_{1,1}$, total edges = 2. Max edges for $N=4$ is 4.
If we merge them to $K_{2,2}$, edges = 4.
So the "distance" to the global maximum decreases by 1 (the edge added) plus the increase in capacity?
No.
Let's assume the hypothesis: The game lasts exactly $\lfloor N^2/4 \rfloor - M$ moves.
If this is true, then the winner is determined by the parity of this difference.
Why would the game last exactly that many moves?
Because any move that merges components increases the "capacity" of the system by exactly the number of edges added?
Let's check the change in capacity.
Initial capacity (sum of max edges in components): $\sum |A_i||B_i|$.
Final capacity (if merged): $\lfloor N^2/4 \rfloor$.
When we merge $C_1, C_2$ with edge $e$:
New capacity = $(|A_1|+|B_2|)(|B_1|+|A_2|) = |A_1||B_1| + |A_1||A_2| + |B_2||B_1| + |B_2||A_2|$.
Old capacity = $|A_1||B_1| + |A_2||B_2|$.
Increase in capacity = $|A_1||A_2| + |B_1||B_2|$.
Edges added = 1.
Net change in "moves remaining" = Increase - 1.
This is not necessarily 0.
So the number of moves is NOT fixed.
BUT, maybe the players can force the game to end at the global maximum?
Or maybe the parity of the total moves is invariant?
Let's check Sample 3 again with the hypothesis.
$N=9, M=5$. Diff = $20-5=15$ (Odd). Aoki wins.
If the number of moves is not fixed, how can we be sure?
Perhaps the optimal strategy is to always merge such that the parity of the remaining moves is favorable?
Actually, there is a theorem for this game: The game is equivalent to Nim with a single pile of size $K = \lfloor N^2/4 \rfloor - M$.
This implies that no matter what moves are made, the total number of moves is always $K$.
Let's verify this theorem.
Is it true that $\sum (|A_i||B_i| - M_i)$ is invariant?
No, we saw it changes.
But maybe the quantity $\lfloor N^2/4 \rfloor - M$ is the number of moves?
If the game ends when the graph is a complete bipartite graph (single component), then the number of moves is $\lfloor N^2/4 \rfloor - M$.
Can a player choose to end the game earlier?
Only if they cannot move.
If the graph is a union of complete bipartite components, and no edges can be added between them?
Wait, if components are complete bipartite, can we always add an edge between them?
Yes, unless the bipartition sizes prevent it?
No, we can always add an edge between $u \in A_1$ and $v \in A_2$ (or $B_1, B_2$) to merge them.
So the game continues until the graph is a single component.
Thus, the game MUST end at the state of a single complete bipartite graph.
Therefore, the total number of moves is exactly $\lfloor N^2/4 \rfloor - M$.
The players have no choice but to eventually reach this state.
The only choice is *which* edge to add, but since the final state is unique (up to isomorphism of the bipartition, but the number of edges is fixed), the total number of moves is fixed.
Wait, is the final state unique?
The final state is a complete bipartite graph on $N$ vertices. The number of edges is uniquely $\lfloor N^2/4 \rfloor$.
Since every move adds 1 edge, and the game must end at this state (because you can always merge components until one remains), the total number of moves is fixed.
Therefore, the winner is determined solely by the parity of $\lfloor N^2/4 \rfloor - M$.
If odd, Aoki (1st player) wins. If even, Takahashi (2nd player) wins.