The problem asks for the minimum total cost when splitting the array into contiguous sub‑arrays.  
If a sub‑array `l…r` is the `i`‑th one, its cost is  

```
( prefix_nums[r] + k·i ) * ( prefix_cost[r] – prefix_cost[l‑1] )
```

where `prefix_nums` and `prefix_cost` are the ordinary prefix sums of `nums` and `cost`.  
Let `dp[i][c]` be the minimum cost for the prefix `0…i` using exactly `c` sub‑arrays.  
The transition is

```
dp[i][c] = min_{j < i} dp[j][c‑1] + (pref_nums[i] + k·c) * (pref_cost[i] – pref_cost[j])
```

Rewrite it as

```
dp[i][c] = (pref_nums[i] + k·c) * pref_cost[i] +
           min_{j < i} ( dp[j][c‑1] – (pref_nums[i] + k·c) * pref_cost[j] )
```

For a fixed `c` the term `x = pref_nums[i] + k·c` grows with `i`.  
The inner minimisation is a classic “minimum of lines” problem: each `j` contributes a line  

```
value(x) = (‑pref_cost[j]) * x + dp[j][c‑1]
```

Since `pref_cost` is non‑decreasing, the slopes `‑pref_cost[j]` are non‑increasing, and queries
`x` are non‑decreasing. This allows a monotone convex‑hull trick (CHT) that yields
`O(n)` work for one `c`. Repeating for all `c = 1 … n` gives an overall `O(n²)` algorithm
(`n ≤ 1000`), which easily fits the limits.

The DP layers are processed iteratively, keeping only the previous layer (`dp_prev`) and
building a new layer (`dp_curr`). A hull is maintained for each layer `c`:
* for `c = 1` the hull is initialised with the line for the empty prefix (cost 0);
* for `c > 1` the hull starts empty – a prefix shorter than `c‑1` cannot be covered with
  `c‑1` sub‑arrays, so it correctly yields `INF`.

During the scan of the array we:
1. query the hull for the current `x`,
2. compute `dp_curr[i]`,
3. add a new line for index `i` using `dp_prev[i]` (if it is finite) for future queries.

The answer is the minimum `dp_curr[n‑1]` over all `c`.