
## ideation
The core difficulty lies in translating the stamina constraints into a structural property of the intervals defined by the people's paths.
1.  **Constraint Analysis**:
    *   Person $i$ travels from $S_i$ to $T_i$. Let $u_i = \min(S_i, T_i)$ and $v_i = \max(S_i, T_i)$. The path covers edges corresponding to nodes $u_i, u_i+1, \dots, v_i$.
    *   The condition "stamina is 0 at endpoints and positive in between" implies that the cumulative weight (prefix sum of edge strengths) $P_k$ satisfies:
        *   $P_{v_i} = P_{u_i - 1}$ (assuming 1-based indexing for nodes and prefix sums defined on nodes, or adjusted accordingly). Let's stick to node indices for prefix sums $P_0, \dots, P_N$.
        *   Actually, let $P_k$ be the stamina at node $k$. Then $P_{S_i} = 0$, $P_{T_i} = 0$, and $P_k > 0$ for $k$ strictly between $S_i$ and $T_i$.
        *   This implies that for any two people $i$ and $j$, if their intervals $(u_i, v_i)$ and $(u_j, v_j)$ "cross" (i.e., $u_i < u_j < v_i < v_j$), a contradiction arises.
        *   Proof of crossing contradiction:
            *   $i$ requires $P_{u_j} > P_{u_i} = 0$ (since $u_i < u_j < v_i$).
            *   $j$ requires $P_{v_i} > P_{u_j}$ (since $u_j < v_i < v_j$).
            *   $i$ requires $P_{v_i} = P_{u_i} = 0$.
            *   Combining these: $0 = P_{v_i} > P_{u_j} > 0$, which is impossible.
        *   Nested intervals ($u_i < u_j < v_j < v_i$) and disjoint intervals do not necessarily cause contradictions.
    *   Therefore, the set of people $\{L, \dots, R\}$ is valid if and only if **no two intervals in this subset cross**.

2.  **Algorithm Selection**:
    *   The problem reduces to: For each query $[L, R]$, check if there exists any pair $(i, j)$ with $L \le i < j \le R$ such that interval $i$ and interval $j$ cross.
    *   Two intervals $i$ and $j$ (with $u_i < u_j$) cross if $u_i < u_j < v_i < v_j$.
    *   We can precompute for each interval $i$, the "nearest crossing interval" $next\_cross[i]$. Specifically, let $bad[i]$ be the smallest index $j > i$ such that $i$ and $j$ cross. If no such $j$ exists, $bad[i] = \infty$.
    *   A range $[L, R]$ is invalid if there exists an $i \in [L, R]$ such that $bad[i] \in [L, R]$. Since $bad[i] > i \ge L$, this simplifies to checking if $\min_{i \in [L, R]} bad[i] \le R$.
    *   To compute $bad[i]$ efficiently:
        *   Iterate $j$ from 1 to $M$.
        *   Maintain a data structure of active intervals (those $i < j$ with $u_i < u_j < v_i$).
        *   Among active intervals, we need those with $v_i < v_j$ to form a crossing ($u_i < u_j < v_i < v_j$).
        *   We want the smallest $j$ for each $i$. So for a fixed $j$, we find all active $i$ with $v_i < v_j$. For each such $i$, we can update $bad[i] = \min(bad[i], j)$.
        *   To do this efficiently, we can use a Segment Tree or Fenwick Tree over the values of $v$. We store the index $i$ at position $v_i$.
        *   For current $j$, query the range $[u_j, v_j - 1]$ in the data structure to find active intervals with $v_i \in [u_j, v_j - 1]$. Actually, we just need to know if there are any, and update them. But we need to update *all* such $i$? No, we only need the *first* $j$ that crosses $i$.
        *   Better approach: For each $i$, we want the smallest $j > i$ such that $u_i < u_j < v_i < v_j$.
        *   We can iterate $j$ from 1 to $M$. For each $j$, we want to find all $i < j$ such that $u_i < u_j$ and $v_i \in (u_j, v_j)$.
        *   We can maintain a set of active intervals sorted by $v_i$. When processing $j$, we remove intervals with $v_i < u_j$ (they are no longer active/crossing potential for future $j$'s in the "nested" sense, but wait, if $v_i < u_j$, they are disjoint, so they don't cross).
        *   Actually, the condition for crossing is $u_i < u_j < v_i < v_j$.
        *   So for current $j$, we look at all $i < j$ such that $u_i < u_j$ and $v_i > u_j$. Among these, we care about those with $v_i < v_j$.
        *   We can use a Segment Tree over the domain of $v$ coordinates ($1 \dots N$). The segment tree will store the minimum index $i$ for a given $v_i$ range? Or just store $i$ at position $v_i$.
        *   Let's store pairs $(v_i, i)$ in a data structure.
        *   When processing $j$:
            1.  Query for any $i$ currently in the structure such that $v_i < v_j$. Since we want to update $bad[i]$ for *all* such $i$ that also satisfy $u_i < u_j < v_i$, we need to be careful.
            2.  The condition $u_i < u_j$ is satisfied if we only add $i$ to the structure when we pass $u_i$? No, we process by index $j$.
            3.  Let's refine: We want to find for each $i$, the smallest $j > i$ with $u_i < u_j < v_i < v_j$.
            4.  We can iterate $j$ from 1 to $M$. We maintain a set of "active" intervals $i < j$ that have started ($u_i < u_j$) but not ended ($v_i \ge u_j$).
            5.  Among active intervals, we want those with $v_i < v_j$.
            6.  If there are any, the smallest such $j$ is the $bad[i]$ for those $i$.
            7.  To efficiently find and update these $i$, we can use a Segment Tree over the values of $v_i$. The segment tree stores the minimum index $i$ for each $v$ value? No, multiple intervals can have same $v$. We want to update $bad[i]$.
            8.  Actually, we just need to know if there is *any* active $i$ with $v_i < v_j$. If there are multiple, they all get their $bad[i]$ set to $j$ (if not already set).
            9.  We can use a Segment Tree that supports:
                *   `add(v, i)`: Insert interval $i$ with end $v$.
                *   `query_and_remove(v_max)`: Find all intervals with $v < v_max$, set their $bad$ to current $j$, and remove them? No, we can't remove them because they might cross a later $j'$? No, if $i$ crosses $j$, then $bad[i]=j$. We don't care about later crossings. So once $bad[i]$ is set, we can remove $i$ from the structure.
                *   So, `query_and_remove(v_max)`: Find all intervals with $v < v_max$. For each, set $bad[i] = j$ and remove.
                *   This can be done by finding the minimum $v$ in the range $[1, v_j - 1]$. If min $v < v_j$, we extract the interval(s) with that min $v$, set their $bad$, and remove. We repeat until min $v \ge v_j$ or no intervals left.
                *   Wait, an interval $i$ is active if $v_i \ge u_j$. So we should only query in range $[u_j, v_j - 1]$.
                *   Algorithm:
                    *   Initialize $bad[i] = \infty$.
                    *   Use a Segment Tree over $v \in [1, N]$. Each leaf stores a list of interval indices $i$ that have that $v_i$. Or just the minimum $i$? We need to process all. A `std::set` or a Segment Tree that returns the minimum $v$ in a range is useful.
                    *   Actually, a simpler way: Use a Segment Tree that stores the minimum $v_i$ in a range. But we need to retrieve the index $i$.
                    *   Let's use a Segment Tree where each node stores the minimum $v$ value present in its range, and the index $i$ associated with it.
                    *   When processing $j$:
                        1.  Remove any intervals from the structure that have $v_i < u_j$? No, those are disjoint and don't cross. They can be permanently removed.
                        2.  Query the range $[u_j, v_j - 1]$ for the minimum $v$. Let this be $v_{min}$ at index $i_{min}$.
                        3.  If such an interval exists ($v_{min} < v_j$), then $i_{min}$ crosses $j$. Set $bad[i_{min}] = j$. Remove $i_{min}$ from the structure. Repeat step 2.
                        4.  Add current interval $j$ to the structure at position $v_j$.

3.  **Implementation Details**:
    *   Segment Tree size $N$.
    *   Each node stores `(min_v, index)`.
    *   `update(pos, index)`: Set leaf `pos` to `(v, index)`. If multiple intervals have same $v$, we might need a list. But since we remove them, we can just store one? No, multiple intervals can end at same $v$. We should store a list or handle collisions. Given constraints, we can store a `vector<int>` at each leaf or use a `set` of pairs `(v, i)`.
    *   Actually, a `std::set<pair<int, int>>` storing `(v_i, i)` for active intervals is easier.
    *   For each $j$:
        1.  Remove all $i$ from set where $v_i < u_j$. (These are disjoint, no longer relevant).
        2.  Find the first element in set with $v < v_j$. Since the set is sorted by $v$, we can use `lower_bound({v_j, -inf})`.
        3.  Iterate from that position backwards? No, `lower_bound` gives first element $\ge v_j$. We want elements $< v_j$.
        4.  So we look at elements with $v < v_j$. We also need $v \ge u_j$.
        5.  So we query the range $[u_j, v_j - 1]$.
        6.  In a `set`, we can find `it = lower_bound({u_j, -inf})`.
        7.  While `it != end` and `it->first < v_j`:
            *   $i = it->second$.
            *   $bad[i] = j$.
            *   `it = set.erase(it)`.
        8.  Insert `{v_j, j}` into set.

4.  **Query Processing**:
    *   After computing $bad[1 \dots M]$, build a Segment Tree or Sparse Table for Range Minimum Query (RMQ) on the array $bad$.
    *   For each query $[L, R]$, compute $m = \min_{i \in [L, R]} bad[i]$.
    *   If $m \le R$, output "No", else "Yes".

5.  **Pitfalls**:
    *   Indices: Ensure 1-based indexing is handled correctly.
    *   $bad[i]$ initialization: Use a large number (e.g., $M+1$).
    *   Empty ranges in set operations.
    *   Performance: $O(M \log N + Q \log M)$ or $O(M \log M + Q \log M)$ depending on implementation. $N, M, Q \le 2 \cdot 10^5$, so this is efficient enough.

## worker: Implement the logic to parse input and normalize i
1.  **Problem Transformation**: The stamina constraints imply that for any two people $i$ and $j$, if their paths "cross" (i.e., $u_i < u_j < v_i < v_j$), it's impossible to satisfy both. Nested or disjoint paths are fine. Thus, the problem reduces to checking if any pair of intervals in the query range crosses.
2.  **Finding Crossing Pairs**: We iterate through each person $j$ and maintain a set of "active" intervals (those that have started but not ended). An active interval $i$ crosses $j$ if $v_i < v_j$. We use a Segment Tree over the $v$ coordinates to efficiently find and remove these crossing intervals.
3.  **Segment Tree for Active Intervals**:
    *   Leaves represent possible values of $v_i$.
    *   Each leaf stores a list of interval indices $i$ that end at that $v_i$.
    *   Internal nodes store the count of active intervals in their range.
    *   For each $j$, we first remove intervals with $v_i < u_j$ (disjoint).
    *   Then we query the range $[u_j, v_j - 1]$ to find all active intervals $i$ with $v_i < v_j$. These are the ones that cross $j$. We record $bad[i] = j$ and remove them.
    *   Finally, we add $j$ to the tree at position $v_j$.
4.  **Query Processing**: After computing the `bad` array where `bad[i]` is the smallest index $j > i$ that crosses $i$ (or $\infty$ if none), a query $[L, R]$ is invalid if there exists any $i \in [L, R]$ such that $bad[i] \le R$. This is checked using a Range Minimum Query (RMQ) on the `bad` array.
5.  **Complexity**:
    *   Processing intervals: Each interval is added and removed once. Segment tree operations are $O(\log N)$. Total $O(M \log N)$.
    *   Queries: RMQ is $O(\log M)$ per query. Total $O(Q \log M)$.
    *   Overall: $O(M \log N + Q \log M)$, which fits within the time limits for $N, M, Q \le 2 \cdot 10^5$.
