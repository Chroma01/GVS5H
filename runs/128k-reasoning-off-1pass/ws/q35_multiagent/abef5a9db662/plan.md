The key observation is that for a given initial rating $X$, the final rating is $X + \text{count of contests where the rating was in } [L_i, R_i] \text{ during that contest}$. However, the rating changes dynamically, so we cannot simply check if $X \in [L_i, R_i]$. Instead, we can simulate the process in reverse or use a more clever approach.

Actually, let's think forward. The rating starts at $X$. For each contest $i$, if current rating $r \in [L_i, R_i]$, then $r \leftarrow r+1$. We need to compute the final rating for many queries. Since $N, Q$ are up to $2 \times 10^5$ and $5 \times 10^5$, we cannot simulate each query independently ($O(NQ)$ is too slow).

We can precompute the answer for all possible initial ratings $X \in [1, 500000]$. Let $f(X)$ be the final rating given initial rating $X$. We can compute $f(X)$ for all $X$ by simulating the contests once, but we need to do it efficiently.

Notice that the transformation is: $r_{i} = r_{i-1} + 1$ if $L_i \leq r_{i-1} \leq R_i$, else $r_i = r_{i-1}$. This is equivalent to: $r_i = r_{i-1} + \mathbb{I}(L_i \leq r_{i-1} \leq R_i)$.

We can process all initial ratings simultaneously. Let's maintain an array `rating` where `rating[x]` is the current rating of someone who started with $x$. Initially, `rating[x] = x` for all $x$. For each contest $[L, R]$, we want to increment `rating[x]` for all $x$ such that the current value `rating[x]` is in $[L, R]$. This is still tricky because the condition depends on the current (dynamic) value.

Alternative approach: Process contests in order. For each contest $[L_i, R_i]$, we need to identify all initial ratings $X$ whose current rating falls in $[L_i, R_i]$. If we could efficiently find and update these, we'd be done.

Let's use a different perspective. Let $g_i(r)$ be the rating after contest $i$ given that the rating before contest $i$ was $r$. Then $g_i(r) = r + 1$ if $L_i \leq r \leq R_i$, else $r$. The final rating is $g_N(g_{N-1}(\dots g_1(X)\dots))$.

Since the function $g_i$ is simple, the composition is also piecewise linear with slope 0 or 1. Specifically, the final function $F(X) = \text{final rating}$ is non-decreasing and $F(X) \geq X$. Moreover, $F(X) - X$ is the number of contests where the rating was in the range.

We can compute $F(X)$ for all $X$ by maintaining the current rating for each $X$. But updating all $X$ for each contest is $O(\text{max\_rating} \cdot N)$ which is $5 \times 10^5 \times 2 \times 10^5$, too slow.

Better idea: Use a segment tree or Fenwick tree to track which initial ratings have which current rating. Or, process the contests and use the fact that the mapping is monotone.

Actually, here's a clean approach: 
1. Initialize an array `ans` of size $500001$ where `ans[x] = x`.
2. For each contest $[L, R]$, we need to increment `ans[x]` for all $x$ such that `ans[x]` is in $[L, R]$.
3. To do this efficiently, we can use a DSU-like structure or a set of intervals. Since `ans[x]` is non-decreasing in $x$ (if $x_1 < x_2$, then after any number of contests, `ans[x_1] \leq ans[x_2]`), the values `ans[x]` form a non-decreasing sequence.

So, for each contest $[L, R]$, we find the range of $x$ such that `ans[x] \in [L, R]`. Since `ans` is non-decreasing, this is a contiguous range $[l, r]$. We then increment `ans[x]` for all $x \in [l, r]$. This can be done with a lazy segment tree or by maintaining the array and using binary search to find the range, then using a difference array or similar to apply increments.

But incrementing a range in an array that is non-decreasing and we need to query point values... We can use a segment tree with lazy propagation. The segment tree will store the current rating for each initial $X$. Each contest requires:
- Query: find the smallest $x$ such that `tree[x] \geq L` and the largest $x$ such that `tree[x] \leq R`.
- Update: increment all values in the range $[l, r]$.

Since the array is non-decreasing, we can binary search on the segment tree to find the range $[l, r]$ where `tree[x] \in [L, R]`. Then apply a range increment.

Max rating can go up to $500000 + 200000 = 700000$. So we need the segment tree to handle values up to $700000$. The number of initial ratings is $500000$.

Steps:
1. Build a segment tree over indices $1$ to $500000$, initialized with `tree[x] = x`.
2. For each contest $[L, R]$:
   a. Find the smallest index $l$ such that `tree[l] \geq L`.
   b. Find the largest index $r$ such that `tree[r] \leq R`.
   c. If $l \leq r$, increment all values in `tree[l..r]` by 1.
3. After all contests, for each query $X$, output `tree[X]`.

Finding $l$ and $r$ can be done with binary search on the segment tree in $O(\log (\text{max\_X}))$. Range update is $O(\log (\text{max\_X}))$. Total time: $O(N \log (\text{max\_X}) + Q)$.