1. Read input and store intervals.
2. Compute the union of all intervals to check if $[1, N]$ is fully covered. If not, set `has_holes = True`.
3. Implement `solve_cover(L, R)` which returns the minimum number of intervals from the input needed to cover $[L, R]$. This uses a greedy strategy: sort intervals by start time, pick the one that starts $\le$ current position and extends furthest.
4. If `has_holes` is False, the answer is `solve_cover(1, N)`. Reconstruct the solution using only Op 1s.
5. If `has_holes` is True:
   - Initialize `min_total_cost` to infinity.
   - **Singleton Check**: For each $i$, cost = $1 + \text{solve\_cover}(L_i, R_i)$. Update `min_total_cost`.
   - **Pair Check**: We need to find $i, j$ minimizing $2 + \text{solve\_cover}(\max(L_i, L_j), \min(R_i, R_j))$.
     - Sort intervals by $L$.
     - Use a data structure to query the minimum `solve_cover` cost for intervals contained in $[L_i, R_i]$.
     - Specifically, for each $i$, we want to find $j$ such that $L_j \ge L_i$ and $R_j \le R_i$.
     - We can iterate $i$ and maintain a list of candidates.
     - Since $M$ is up to 200,000, we can't do $O(M^2)$.
     - However, we can observe that if we pick $i$ and $j$, the intersection is $[L_j, R_j]$ if $L_j \ge L_i$ and $R_j \le R_i$.
     - So we just need to find $j$ contained in $[L_i, R_i]$ with minimum `solve_cover` cost.
     - We can precompute `solve_cover` for all input intervals.
     - Then for each $i$, we want $\min \{ \text{cost}_j \mid L_j \ge L_i, R_j \le R_i \}$.
     - This is a 2D range minimum query. We can solve this by sorting by $L$ and using a Fenwick tree on $R$.
     - Iterate $i$ in increasing order of $L$. Add intervals with $L_j \le L_i$ to the Fenwick tree (indexed by $R_j$). Query the range $[L_i, R_i]$ for minimum cost.
     - Wait, we need $L_j \ge L_i$. So we should iterate $i$ and query for $j$ with $L_j \ge L_i$.
     - Better: Sort all intervals by $L$. Iterate $i$ from right to left (decreasing $L$). Add intervals with $L_j \le L_i$ to the structure? No.
     - We want $j$ such that $L_j \ge L_i$ and $R_j \le R_i$.
     -