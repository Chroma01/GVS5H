
## ideation
**Core Difficulty**: The problem is a combinatorial game on a graph. The key insight is recognizing that the game state space is finite, acyclic (in terms of move count), and impartial. The winning condition depends on the parity of the total number of valid moves available from the initial state to a terminal state, assuming optimal play (which in such "normal play" games with a fixed total move count often simplifies to checking if the total moves is odd or even).

**Key Observations**:
1.  **Graph Structure**: The initial graph has no odd cycles, so it is a **bipartite graph** (specifically, a forest since it's simple and acyclic initially, but even if it had even cycles, it's bipartite).
2.  **Move Condition**: Adding an edge $(u, v)$ is valid if and only if it does not create an odd cycle. In a bipartite graph, adding an edge between two vertices in the same partition creates an odd cycle. Adding an edge between vertices in different partitions creates an even cycle. Therefore, a move is valid if and only if $u$ and $v$ belong to **different** partitions of the connected component they reside in.
3.  **Game Progression**:
    *   Initially, the graph is a collection of disjoint bipartite components. Let a component have partition sizes $A$ and $B$.
    *   Any valid move connects a node from set $A$ to a node from set $B$.
    *   Once an edge is added between $A$ and $B$, the component remains bipartite. The new edge effectively "uses up" one potential connection between the two sets.
    *   Crucially, adding an edge between $u \in A$ and $v \in B$ does not merge two separate components (since they are already in the same component to have a defined distance/partition relation relative to each other? Wait, let's re-evaluate).
    *   **Correction on Component Merging**: If $u$ and $v$ are in *different* connected components, say $C_1$ and $C_2$, adding an edge $(u, v)$ merges them. For the cycle condition:
        *   Let $C_1$ have partitions $A_1, B_1$ and $C_2$ have $A_2, B_2$.
        *   If we connect $u \in A_1$ and $v \in A_2$, the path from $u$ to $v$ in the new graph involves the new edge. Does this create an odd cycle?
        *   Actually, the rule is: "Adding an edge ... does not create an odd cycle."
        *   If we connect two different components, no cycle is created *at all* (since there was no path between them). Thus, connecting two different components is **always valid** regardless of their internal bipartitions?
        *   **Wait**, let's re-read carefully: "G does not already have an edge... Adding an edge ... does not create an odd cycle."
        *   If $u$ and $v$ are in different components, adding $(u,v)$ creates a path between them but **no cycle**. A path is not a cycle. So no odd cycle is created.
        *   Therefore, **any** pair $(u, v)$ from different connected components is a valid move.
        *   If $u$ and $v$ are in the same component, a cycle is formed. The cycle length is $dist(u,v) + 1$. We need $dist(u,v) + 1$ to be even $\implies dist(u,v)$ is odd. In a bipartite graph, $dist(u,v)$ is odd iff $u$ and $v$ are in different partitions.

4.  **Total Moves Calculation**:
    *   The game ends when the graph is a **complete multipartite graph**? No.
    *   Let's analyze the "capacity" of the graph.
    *   Consider the final state. In the final state, for every pair of vertices $(u, v)$, either they are connected, or adding the edge would create an odd cycle.
    *   If $u, v$ are in the same component in the final state, they must be in the same partition (otherwise we could add the edge).
    *   If $u, v$ are in different components in the final state... wait, can we always merge components?
    *   Suppose we have two components. Can we always add an edge between them? Yes, because no cycle is formed.
    *   So, players will keep merging components until there is only **one** connected component?
    *   Once there is one component, can we still add edges? Yes, between nodes in different partitions.
    *   The game ends when the single component is such that all pairs of nodes in different partitions are already connected. This means the component becomes a **complete bipartite graph** $K_{A, B}$.
    *   In a complete bipartite graph $K_{A, B}$, any pair $(u, v)$ with $u \in A, v \in B$ is connected. Any pair $(u, v)$ with $u, v \in A$ or $u, v \in B$ would create an odd cycle (triangle if size $\ge 3$, or just an odd cycle generally).
    *   So the terminal state is a complete bipartite graph spanning all $N$ vertices.
    *   The total number of edges in a complete bipartite graph with partitions of size $A$ and $B$ (where $A+B=N$) is $A \times B$.
    *   However, the partition sizes $A$ and $B$ are not fixed initially?
    *   Let's trace the "bipartition" invariant.
    *   In any bipartite graph, the vertices can be colored black/white.
    *   When we merge two components $C_1$ (sizes $a_1, b_1$) and $C_2$ (sizes $a_2, b_2$) by adding an edge $(u, v)$:
        *   If $u \in A_1$ and $v \in A_2$: The new component has partitions $(A_1 \cup A_2, B_1 \cup B_2)$. Total sizes: $A_1+A_2, B_1+B_2$.
        *   If $u \in A_1$ and $v \in B_2$: The new component has partitions $(A_1 \cup B_2, B_1 \cup A_2)$. Total sizes: $A_1+B_2, B_1+A_2$.
    *   Notice that the sum $A+B = N$ is constant. But the individual values of $A$ and $B$ change based on how we merge.
    *   Does the final state depend on the moves?
    *   The game ends when the graph is a complete bipartite graph $K_{X, Y}$ with $X+Y=N$. The number of edges is $X \times Y$.
    *   The number of moves made = (Final Edges) - (Initial Edges).
    *   Since the winner depends on the parity of the moves, we need $(X \times Y - M) \pmod 2$.
    *   Is $X \times Y$ constant regardless of the sequence of moves?
    *   Let's check the merge operation parity.
        *   Case 1: Merge $A_1, B_1$ and $A_2, B_2$ via $A_1-A_2$. New sizes: $A_1+A_2, B_1+B_2$. Product $P_{new} = (A_1+A_2)(B_1+B_2)$.
        *   Case 2: Merge via $A_1-B_2$. New sizes: $A_1+B_2, B_1+A_2$. Product $P'_{new} = (A_1+B_2)(B_1+A_2)$.
        *   Difference: $P_{new} - P'_{new} = (A_1+A_2)(B_1+B_2) - (A_1+B_2)(B_1+A_2)$
            $= (A_1 B_1 + A_1 B_2 + A_2 B_1 + A_2 B_2) - (A_1 B_1 + A_1 A_2 + B_2 B_1 + B_2 A_2)$
            $= A_1 B_2 + A_2 B_1 - A_1 A_2 - B_1 B_2$.
        *   This difference is not necessarily 0. So the final product $X \times Y$ **depends** on the moves?
    *   **Contradiction**: In impartial games where the total number of moves is fixed, the winner is determined by parity. If the final state varies, the game length varies, and it's not a simple "total moves" game unless the parity of the total moves is invariant.
    *   Let's re-evaluate the "Total Moves" hypothesis. Maybe the parity of $X \times Y$ is invariant?
        *   Consider $N=4$. Initial: $K_{2,2}$ (2+2). $2 \times 2 = 4$.
        *   Split into two $K_{1,1}$ (1+1). Sizes: $(1,1)$ and $(1,1)$.
        *   Merge via $1-1$ (A-A): New $(2,2)$. Prod 4.
        *   Merge via $1-1$ (A-B): New $(2,2)$. Prod 4.
        *   Here parity is same.
        *   Consider $N=3$. Initial: $K_{1,2}$ (1+2). Prod 2.
        *   Split? Can't split. Start with disconnected: $K_{1,1}$ and $K_{1,0}$ (isolated).
        *   Comp 1: $(1,1)$. Comp 2: $(1,0)$.
        *   Merge A-A: New $(2,1)$. Prod 2.
        *   Merge A-B: New $(2,1)$. Prod 2.
        *   It seems $X \times Y \pmod 2$ might be invariant.
        *   Let's check the difference formula modulo 2:
            $D = A_1 B_2 + A_2 B_1 - A_1 A_2 - B_1 B_2$.
            Modulo 2: $D \equiv A_1 B_2 + A_2 B_1 + A_1 A_2 + B_1 B_2 \pmod 2$.
            Note that $(A_1+B_1)(A_2+B_2) = A_1 A_2 + A_1 B_2 + B_1 A_2 + B_1 B_2 = N_1 N_2$.
            So $D \equiv N_1 N_2 \pmod 2$.
            This means the product changes by $N_1 N_2 \pmod 2$ depending on the merge type?
            Wait, if $N_1 N_2$ is odd, the parity flips. If $N_1 N_2$ is even, parity stays.
            This implies the final parity depends on the merge choices if we have components of odd size.
    *   **Re-reading the problem statement carefully**: "A player who cannot perform this operation loses".
    *   Is it possible the game is equivalent to Nim? Or is the "Total Moves" actually fixed?
    *   Let's look at the sample cases.
        *   Sample 1: 4 vertices, edges (1,2), (2,3), (3,4). This is a path 1-2-3-4. Bipartition: {1,3} and {2,4}. Sizes 2, 2.
            *   Valid moves: Pairs in different sets.
            *   Pairs: (1,4) [diff], (2,3) [diff]. (1,2) exists, (2,3) exists, (3,4) exists. (1,3) same, (2,4) same.
            *   Available: (1,4) and (2,3).
            *   If Aoki picks (1,4): Graph becomes 1-2-3-4 plus 1-4. Cycle 1-2-3-4-1 (len 4, even). Now partitions {1,3}, {2,4}. Edge (1,4) connects them.
            *   Remaining pairs in diff sets: (2,3). Is (2,3) an edge? Yes.
            *   So after (1,4), no moves left?
            *   Wait, (2,3) is an edge. So no moves. Aoki wins (1 move).
            *   If Aoki picks (2,3): Graph 1-2-3-4 plus 2-3. Cycle 2-3-4-1-2

## worker: [todo] Read the input $N$, $M$, and the list of ed
The problem is a combinatorial game on a bipartite graph. The game ends when the graph becomes a complete bipartite graph $K_{X,Y}$. The total number of moves is $X \times Y - M$. The winner is determined by the parity of this number.
Key insights:
1.  If $N$ is odd, the final partitions $X, Y$ must have different parities (one odd, one even), so $X \times Y$ is even. Moves = Even - $M$. If $M$ is odd, moves are odd (Aoki wins). If $M$ is even, moves are even (Takahashi wins). Wait, my previous deduction for $N$ odd was "Aoki wins". Let's re-verify.
    *   Sample 3: N=9 (odd), M=5 (odd). Output Aoki.
    *   My logic: Moves = Even - Odd = Odd. Aoki wins.
    *   What if M is even? e.g. N=3, M=0. Moves = Even - Even = Even. Takahashi wins?
    *   Let's check N=3, M=0. 3 isolated vertices (T, T, T).
    *   Aoki merges T+T -> U or S.
    *   If she chooses U (2,1), then we have U, T.
    *   Then merge U+T -> T.
    *   Final T (1,2). Moves = 2 - 0 = 2. Even. Takahashi wins.
    *   If she chooses S (1,1) from T+T? No, T+T -> U or S.
    *   T(1,0)+T(1,0) -> U(2,0) or S(1,1)?
    *   Wait, T(1,0) means partitions 1,0.
    *   Merge A(1)-A(1) -> A=2, B=0. U.
    *   Merge A(1)-B(0) -> A=1, B=1. S.
    *   So she can choose S.
    *   If she chooses S(1,1), then we have S, T.
    *   Merge S+T -> T or S.
    *   If she chooses S, final S(1,2)? No, S(1,1)+T(1,0) -> S(2,1)?
    *   S(1,1) + T(1,0).
    *   Connect S_odd - T_odd -> A=1+1=2, B=1+0=1. U.
    *   Connect S_odd - T_even -> A=1+0=1, B=1+0=1. S.
    *   So she can choose S.
    *   Final S(1,2). Moves = 2 - 0 = 2. Even. Takahashi wins.
    *   So for N=3, M=0, Takahashi wins.
    *   My code says: N odd -> Aoki wins. This is WRONG for N=3, M=0.
    *   Wait, Sample 3: N=9, M=5. Output Aoki.
    *   My code for N odd always prints Aoki.
    *   But N=3, M=0 should be Takahashi.
    *   Let's re-read the problem. "Aoki going first".
    *   Maybe the "Total Moves" parity is not the only factor?
    *   Or maybe my N=3, M=0 analysis is wrong.
    *   Let's re-evaluate N=3, M=0.
    *   Components: T, T, T.
    *   Aoki moves.
    *   She can merge T+T -> U or S.
    *   If she chooses U(2,0). State: U, T.
    *   Takahashi moves. U+T -> T. State: T.
    *   Aoki moves. T alone? No, must merge. But only 1 component.
    *   Wait, if only 1 component, no merges.
    *   But she can add edges within the component!
    *   In T(1,2), she can add 2 edges.
    *   So the game continues.
    *   The "Total Moves" is fixed by the final state.
    *   If final state is T(1,2), Moves = 2. Even. Takahashi wins.
    *   Can Aoki force a different final state?
    *   From T, T, T.
    *   Aoki merges T+T -> S(1,1). State: S, T.
    *   Takahashi merges S+T -> U or S.
    *   If he chooses U(2,1). State: U. Final U. Moves = 2. Even.
    *   If he chooses S(1,2). State: S. Final S. Moves = 2. Even.
    *   So Moves is always 2.
    *   So Takahashi wins.
    *   So for N=3, M=0, Takahashi wins.
    *   But my code says Aoki.
    *   So the "N odd -> Aoki" rule is wrong.
    *   The rule should be:
    *   If N is odd, Final is T. Moves = Even - M.
    *   Aoki wins if Moves is Odd => Even - M is Odd => M is Odd.
    *   So if N is odd, Aoki wins if M is odd, Takahashi if M is even.
    *   Let's check Sample 3: N=9, M=5 (odd). Aoki wins. Correct.
    *   So for N odd: Aoki if M odd, Takahashi if M even.
    *   This is equivalent to: Aoki if (N%2==1 and M%2==1) or ...
    *   Actually, let's unify.
    *   If N is odd, Final parity is Even.
    *   Moves = Even - M.
    *   Aoki wins if Moves is Odd => M is Odd.
    *   So if N is odd, Aoki wins iff M is odd.
    *   If N is even:
    *   If count(T) > 0: Aoki can choose Final parity.
    *     If M even, she chooses S (Odd). Moves = Odd - Even = Odd. Wins.
    *     If M odd, she chooses U (Even). Moves = Even - Odd = Odd. Wins.
    *     So if count(T) > 0, Aoki always wins.
    *   If count(T) == 0:
    *     Final parity fixed by S count.
    *     If S count odd -> Final S (Odd).
    *     If S count even -> Final U (Even).
    *     Aoki wins if Moves is Odd.
    *     Moves = Final - M.
    *     If Final Odd: Moves = Odd - M. Odd if M even.
    *     If Final Even: Moves = Even - M. Odd if M odd.
    *     So Aoki wins if (Final Odd and M even) or (Final Even and M odd).
    *     i.e., (Final parity) != (M parity).
    *     Final parity is S count parity.
    *     So Aoki wins if (S count % 2) != (M % 2).

    # Revised Logic:
    # 1. If N % 2 == 1:
    #      If M % 2 == 1: Aoki
    #      Else: Takahashi
    # 2. If N % 2 == 0:
    #      If t_count > 0: Aoki
    #      Else:
    #         If (s_count % 2) != (M % 2): Aoki
    #         Else: Takahashi

    # Let's re-verify N=3, M=0.
    # N=3 (odd). M=0 (even). Takahashi. Correct.
    # Sample 3: N=9 (odd). M=5 (odd). Aoki. Correct.
    # Sample 1: N=4 (even). t_count=0. s_count=0. M=3 (odd).
    #   0 != 1 -> Aoki. Correct.
    # Sample 2: N=4 (even). t_count=0. s_count=2. M=2 (even).
    #   0 != 0 -> False. Takahashi. Correct.

    # This unified logic seems correct.

## worker: Implement the revised logic in the code. Ensure al
The solution implements the derived game theory logic:
1.  **Graph Analysis**: The graph is a forest (no odd cycles initially), so it's bipartite. We use BFS to find connected components and their bipartition sizes $(c0, c1)$.
2.  **Component Classification**:
    *   **Type T**: Total size $c0+c1$ is odd.
    *   **Type S**: Total size is even, but partitions are $(odd, odd)$.
    *   **Type U**: Total size is even, partitions are $(even, even)$.
3.  **Winning Condition**:
    *   **Case N is Odd**: The final state must be a complete bipartite graph $K_{X,Y}$ where $X+Y=N$ (odd). Thus, one partition is odd and the other even, making the total edges $X \times Y$ even. The number of moves is $Even - M$. Aoki wins if moves is odd, which happens if $M$ is odd.
    *   **Case N is Even**:
        *   If there is at least one Type T component ($t\_count > 0$), the first player (Aoki) can manipulate the merge process to force the final state to have either odd or even edges, whichever makes her win. Thus, Aoki always wins.
        *   If there are no Type T components ($t\_count == 0$), the parity of the final number of edges is fixed by the initial configuration. Specifically, it is odd if $s\_count$ is odd, and even if $s\_count$ is even. Aoki wins if the parity of the final edges differs from the parity of $M$.

This logic covers all edge cases including $N=1$ and disconnected graphs.
