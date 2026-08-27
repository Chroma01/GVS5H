We must pick `k` disjoint length‑`x` windows and pay for each the minimum number of `+1/-1` operations to make all its elements equal.  
For a fixed window the optimal target is any median, and the cost equals the sum of absolute deviations to that median.  
Thus the problem becomes:  
1. Compute for every possible window `i … i+x‑1` the minimal cost `cost[i]`.  
2. Choose `k` non‑overlapping windows minimizing the sum of their costs.

`cost[i]` is obtained with a sliding‑window median. We use a Fenwick tree (BIT) for frequencies and a second BIT for the sum of values, after coordinate‑compressing `nums`. While the window slides we keep the current window sum, query the median by order‑statistic on the frequency BIT, and compute the L1 distance to that median in O(log n). This gives all `cost[i]` in O(n log n).

With the array `cost[0 … m‑1]` (`m = n‑x+1`) the selection of `k` windows is a classic DP with fixed window size.  
Let `dp[t][i]` be the minimum total cost to place `t` windows inside the first `i` elements (i = prefix length).  
Transition:  
```
dp[t][i] = min(dp[t][i‑1],                     # skip element i‑1
               cost[i‑x] + dp[t‑1][i‑x])      # place a window ending at i‑1
```
The answer is `dp[k][n]`. Only two rows are needed (previous and current), giving O(k·n) time and O(n) memory.

Both phases together run in O((n log n) + k·n) ≤ 2·10⁶ operations for the given limits, well within constraints.