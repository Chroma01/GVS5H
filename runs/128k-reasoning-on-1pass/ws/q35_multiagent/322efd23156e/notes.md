
## ideation
The problem asks us to select a subset of foods to maximize the minimum total amount of vitamins 1, 2, and 3, subject to a total calorie constraint $X$. Each food provides exactly one type of vitamin.

This problem can be decomposed into three independent knapsack-like problems, one for each vitamin type. For a fixed target minimum intake $K$, we need to check if it's possible to obtain at least $K$ units of each vitamin with total calories $\le X$. Since the items for each vitamin are disjoint, we can compute the minimum cost to achieve at least $K$ units for each vitamin independently and sum them up.

The function "is it possible to achieve minimum intake $K$" is monotonic. If we can achieve $K$, we can certainly achieve $K-1$. This suggests using binary search on the answer $K$.

For a fixed $K$, we need to find the minimum cost to get $\ge K$ units of vitamin $i$. This is equivalent to finding the smallest cost $c$ such that the maximum amount of vitamin $i$ achievable with cost $\le c$ is at least $K$.

We can solve the subproblem for each vitamin using a 0/1 Knapsack DP. Let `dp[c]` be the maximum amount of a specific vitamin achievable with exactly `c` calories. We can compute this array for each vitamin type. The size of the DP array is $X+1$. Since $X \le 5000$ and $N \le 5000$, the complexity $O(N \cdot X)$ is acceptable ($2.5 \times 10^7$ operations).

After computing the `dp` arrays, we can compute a `best` array where `best[c]` is the maximum amount achievable with cost $\le c$ (prefix maximum of `dp`). Then, for a given $K$, we can find the minimum cost to achieve $\ge K$ using binary search (or `bisect_left`) on the `best` array.

Optimizations:
1.  **Sentinel Value**: Instead of checking `if dp[j-c] != -1`, we can initialize `dp` with a very small number (e.g., $-10^{15}$) and rely on arithmetic. Since max possible sum of $A_i$ is $10^9$, a sentinel of $-10^{15}$ ensures that unreachable states remain distinguishable from valid states (which are $\ge 0$) and don't accidentally become valid.
2.  **Reachable Range**: We can track the maximum cost index `max_reachable` that has been updated to a non-negative value. The inner loop for updating `dp` only needs to run up to `max_reachable + c`, reducing the number of iterations.
3.  **Fast I/O**: Use `sys.stdin.read` for fast input parsing.

## worker: (none)
The problem asks us to maximize the minimum total intake among three vitamins, subject to a calorie constraint. This can be solved by binary searching on the answer $K$. For a fixed $K$, we need to check if it's possible to get at least $K$ units of each vitamin with total calories $\le X$. Since the foods for each vitamin are disjoint, we can compute the minimum cost to achieve at least $K$ units for each vitamin independently.

For each vitamin type, we use a 0/1 Knapsack DP to compute the maximum value (vitamin units) achievable for each possible cost. The DP state `dp[c]` stores the max value with exactly cost `c`. We then compute a prefix maximum array `best[c]` which stores the max value achievable with cost $\le c$. This allows us to quickly find the minimum cost to achieve at least $K$ units using binary search (`bisect_left`).

The complexity is $O(N \cdot X)$ for the DP and $O(\log(\sum A) \cdot \log X)$ for the binary search, which fits well within the time limits. The use of a large negative sentinel value (`NEG_INF`) allows us to avoid explicit checks for unreachable states in the inner loop, speeding up the Python implementation.
