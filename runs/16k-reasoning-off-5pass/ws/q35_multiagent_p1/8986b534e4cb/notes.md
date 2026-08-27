
## ideation
The problem asks whether a set of people's travel constraints can be simultaneously satisfied by assigning integer weights to edges of a line graph.
1.  **Modeling**: The stamina condition implies that for each person $i$ traveling between $S_i$ and $T_i$, if we define $L_i = \min(S_i, T_i)$ and $R_i = \max(S_i, T_i)$, the prefix sums of edge weights $P$ must satisfy $P_{L_i} = P_{R_i}$ and $P_v > P_{L_i}$ for all $v \in (L_i, R_i)$.
2.  **Conflict Analysis**: These constraints form a laminar family if and only if no two intervals $[L_i, R_i]$ and $[L_j, R_j]$ "cross". Crossing is defined as $L_i < L_j < R_i < R_j$ (or symmetric). Nested intervals ($L_i < L_j < R_j < R_i$) are compatible. Disjoint intervals are compatible.
3.  **Reduction**: The problem reduces to checking if the subset of people in each query range $[L_k, R_k]$ contains any pair of crossing intervals.
4.  **Algorithm**:
    *   For each person $j$, determine if there exists an earlier person $i < j$ such that $i$ and $j$ cross.
    *   A crossing occurs if $L_i < L_j$ and $L_j < R_i < R_j$.
    *   To efficiently find such conflicts, we can sweep through people $j=1 \dots M$. For each $j$, we want to know if there is an $i < j$ with $L_i < L_j$ and $R_i \in (L_j, R_j)$.
    *   Specifically, let $M_j = \max \{ R_i \mid i < j, L_i < L_j \}$. If $M_j > L_j$, there is at least one $i$ with $L_i < L_j$ and $R_i > L_j$. Let $idx_j$ be the index achieving this maximum.
    *   If $M_j < R_j$, then $R_{idx_j} \in (L_j, R_j)$, so $idx_j$ and $j$ cross. We record $conflict\_idx[j] = idx_j$.
    *   If $M_j \ge R_j$, then any $i$ with $L_i < L_j$ either has $R_i \le L_j$ (no overlap) or $R_i \ge R_j$ (nested/covering, which is compatible). Thus, no crossing conflict with any $i < j$ exists.
    *   So, $j$ has a conflict with some $i < j$ if and only if $L_j < M_j < R_j$. In that case, the conflict is with $idx_j$.
    *   For a query $[L, R]$, it is valid if and only if for all $j \in [L, R]$, if $j$ has a conflict with some $i < j$, then $i < L$. That is, $conflict\_idx[j] < L$.
    *   This is equivalent to $\max_{j=L}^R conflict\_idx[j] < L$. (If no conflict, $conflict\_idx[j] = -\infty$).
    *   We can precompute $conflict\_idx$ array using a Segment Tree or Fenwick Tree to maintain the maximum $R_i$ for active $L_i$ ranges. Then use a Sparse Table or Segment Tree for Range Maximum Query on $conflict\_idx$.

## worker: (None)
The problem reduces to checking if a set of intervals contains any crossing pair. Two intervals $[L_i, R_i]$ and $[L_j, R_j]$ with $i < j$ cross if $L_i < L_j < R_i < R_j$. Nested intervals ($L_i < L_j < R_j < R_i$) are compatible.

We process people in order $1 \dots M$. For each person $j$, we want to find if there exists an $i < j$ such that $L_i < L_j$ and $R_i \in (L_j, R_j)$.
To do this efficiently, we maintain a data structure (Segment Tree) that stores, for each starting position $L$, the maximum ending position $R$ of an interval starting at $L$.
When processing $j$ with $(L_j, R_j)$:
1. Query the maximum $R_i$ among all $i < j$ with $L_i < L_j$. This is a range maximum query on the Segment Tree over the domain $[1, L_j - 1]$.
2. Let this maximum be $M_j$ and the corresponding index be $idx_j$.
3. If $M_j > L_j$ and $M_j < R_j$, then the interval $idx_j$ crosses $j$. We record $conflict\_idx[j] = idx_j$.
4. Otherwise, no $i < j$ crosses $j$ in a way that creates a conflict (if $M_j \ge R_j$, the interval is nested/covering, which is fine; if $M_j \le L_j$, no overlap).
5. Update the Segment Tree at position $L_j$ with $(R_j, j)$.

After computing $conflict\_idx$ for all $j$, a query $[L, R]$ is valid if and only if for all $j \in [L, R]$, any conflicting $i < j$ satisfies $i < L$. This is equivalent to $\max_{j=L}^R conflict\_idx[j] < L$.
We use a Sparse Table or Segment Tree for Range Maximum Query on the $conflict\_idx$ array to answer each query in $O(1)$ or $O(\log M)$.

Complexity:
- Segment Tree operations for each person: $O(\log N)$. Total $O(M \log N)$.
- RMQ Segment Tree build: $O(M)$.
- Query: $O(\log M)$. Total $O(Q \log M)$.
- Overall: $O(M \log N + Q \log M)$, which fits within constraints.
