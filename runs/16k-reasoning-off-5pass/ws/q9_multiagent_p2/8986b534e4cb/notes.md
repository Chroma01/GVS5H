
## ideation
**Core Difficulty**:
The problem asks if there exists an assignment of integer weights $w_1, \dots, w_{N-1}$ such that for a subset of people (defined by range $[L, R]$), their path constraints are satisfied.
1.  **Start/End Constraint**: For person $i$, $\sum_{j \in \text{path}_i} w_j = 0$. This is a linear equality constraint.
2.  **Intermediate Constraint**: For person $i$, at any intermediate node $v$ on their path, the cumulative sum from $S_i$ to $v$ must be $\ge 1$ (since stamina must be a positive integer, and start is 0, so after first step it's $\ge 1$, etc.). Actually, the problem says "When departing Town $S_i$ ... stamina should be exactly 0". Then "At every other town... stamina should be a positive integer".
    *   Let $P_i$ be the sequence of nodes for person $i$. $P_i[0] = S_i, P_i[|P_i|-1] = T_i$.
    *   Stamina at $S_i$ is 0.
    *   Stamina at $P_i[k]$ ($0 < k < |P_i|-1$) must be $\ge 1$.
    *   Stamina at $T_i$ must be 0.
    *   Since the graph is a line, the path from $S$ to $T$ is unique. Let the edges be $e_1, e_2, \dots, e_k$. Let prefix sums be $s_0=0, s_j = s_{j-1} + w_{e_j}$.
    *   Constraints: $s_k = 0$, and $s_j \ge 1$ for $0 < j < k$.
    *   This implies $s_j \ge 1$ for all intermediate nodes. Since $s_k=0$, the last step must be negative enough to bring it back to 0.

## worker: Implement the core logic to check if a subset of p
The problem asks if a subset of people can be satisfied simultaneously. The condition for satisfaction is that no two people have interleaved intervals ($S_i < S_j < T_i < T_j$). This is equivalent to checking if there exists any pair $(i, j)$ in the range $[L, R]$ such that $S_i < S_j < T_i < T_j$.

We can solve this offline by iterating $R$ from 1 to $M$. For each $R$, we check if there exists an $i < R$ such that $L \le i < R$ and the crossing condition holds. The crossing condition is $S_i < S_R < T_i < T_R$.
This transforms into a 2D range query: find the minimum index $i$ such that $S_i < S_R$ and $T_i \in (S_R, T_R)$. If such an $i$ exists and $i \ge L$, then the query $[L, R]$ is satisfied.
We use a Merge Sort Tree over the $S$ coordinates to efficiently query the minimum index $i$ for a given range of $S$ and $T$. Specifically, for a query $(S_R, T_R)$, we query the range $S \in [1, S_R-1]$ and $T \in (S_R, T_R)$ to find the minimum index $i$.
We maintain a Fenwick Tree to handle the $L$ constraint. When we find a valid $i$ for $R$, we update the Fenwick Tree at position $i$ with +1. For a query $[L, R]$, we check if the prefix sum at $L$ is $> 0$, which indicates that there exists an $i \ge L$ satisfying the condition.
