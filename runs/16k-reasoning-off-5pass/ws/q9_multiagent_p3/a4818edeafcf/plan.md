The problem requires maximizing the sum of distinct elements in three contiguous subarrays formed by splitting the array at two indices $i$ and $j$. Since $N$ is up to $3 \times 10^5$, an $O(N^2)$ solution is too slow. We can iterate over the first split point $i$, but calculating the optimal second split point $j$ for each $i$ naively is still expensive. Instead, we can precompute prefix and suffix distinct counts. For a fixed $i$, the first part's distinct count is known. We need to maximize `distinct(i+1, j) + distinct(j+1, N)`. This sub-problem can be solved efficiently by observing that as $j$ increases, the second term decreases while the first increases. However, a more robust approach for this specific "harder version" (likely referring to AtCoder ABC 229 Problem E or similar) involves iterating $i$ and using a data structure or precomputed arrays to find the best $j$. Given the constraints and typical patterns, we can iterate $i$ from $1$ to $N-2$. For each $i$, the left part is fixed. We need to find $j$ ($i < j < N$) maximizing the sum of distincts in the middle and right. We can precompute `suff[j]` = distinct count in $A[j..N]$. Then for a fixed $i$, we want to maximize `distinct(i+1, j) + suff[j+1]`. We can iterate $j$ from $i+1$ to $N-1$. To optimize, we can use the fact that we are looking for a peak or use a segment tree / monotonic stack approach, but given the specific structure of "distinct counts", a simpler $O(N)$ or $O(N \log N)$ pass after precomputing suffixes is possible. Actually, the standard efficient solution for this specific problem (ABC 229 E) is to iterate $i$ and then realize that we just need to check transitions. Wait, the standard solution for this specific "3 parts" distinct sum problem is often $O(N)$ by iterating the first cut and then using a precomputed array for the best split of the remaining suffix. Let's refine: Precompute `pref[k]` (distinct in $A[1..k]$) and `suff[k]` (distinct in $A[k..N]$). Iterate $i$ from $1$ to $N-2$. The first part is `pref[i]`. Now we need to split $A[i+1..N]$ into two parts to maximize distinct sum. Let the split be at $j$. We want `distinct(i+1, j) + distinct(j+1, N)`. Note that `distinct(j+1, N)` is exactly `suff[j+1]`. The term `distinct(i+1, j)` is `pref[j] - pref[i]` ONLY if no elements in $A[1..i]$ appear in $A[i+1..j]$. This condition is hard to check directly for all $j$. 
Alternative approach: Iterate $i$ (first cut). The left part is fixed. We need to maximize `distinct(i+1, j) + suff[j+1]`. We can precompute an array `best_suffix[k]` which stores $\max_{k \le j < N} (\text{distinct}(k, j) + \text{suff}[j+1])$. But `distinct(k, j)` depends on $k$. 
Correct $O(N)$ logic: Iterate $i$ from $1$ to $N-2$. We want $\max_{j} (\text{distinct}(i+1, j) + \text{suff}[j+1])$. Notice that as $i$ increases, the set of available elements for the middle/right shifts. 
Actually, the most efficient way is:
1. Precompute `suff[x]` = distinct count in $A[x..N]$.
2. Iterate $i$ from $1$ to $N-2$.
3. We need $\max_{j=i+1}^{N-1} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
Let $f(i, j) = \text{distinct}(i+1, j)$. We want $\max (f(i, j) + \text{suff}[j+1])$.
This looks like it might be $O(N^2)$ if not careful. However, notice that $f(i, j) = \text{distinct}(1, j) - \text{distinct}(1, i)$ is false because of overlaps.
Let's reconsider the constraints and problem type. This is likely solvable by iterating $i$ and maintaining the best $j$ as $i$ increments? No, the range shifts.
Wait, there is a known trick. The maximum sum of distincts in 3 parts is bounded by $N$.
Let's try a different angle. Iterate $i$ (first cut). The left part contributes $D_1$. The remaining array $A[i+1..N]$ needs to be split into two parts with max distinct sum. Let $g(k, m) = \text{distinct}(k, m) + \text{distinct}(m+1, N)$. We want $\max_{m} g(i+1, m)$.
Let $H[k] = \max_{m=k}^{N-1} (\text{distinct}(k, m) + \text{suff}[m+1])$. If we can compute $H[k]$ for all $k$, then the answer is $\max_i ( \text{pref}[i] + H[i+1] )$.
How to compute $H[k]$ efficiently?
$H[k] = \max ( \text{distinct}(k, k) + \text{suff}[k+1], \text{distinct}(k, k+1) + \text{suff}[k+2], \dots )$.
Note that $\text{distinct}(k, m) = \text{distinct}(k, m-1) + 1$ if $A[m]$ is new, else same.
This looks like we can compute $H[k]$ from $H[k+1]$?
$H[k] = \max ( 1 + \text{suff}[k+1], \text{distinct}(k, k+1) + \text{suff}[k+2], \dots )$.
Actually, $\text{distinct}(k, m) = \text{distinct}(k+1, m) + (1 \text{ if } A[k] \text{ not in } A[k+1..m] \text{ else } 0)$.
So $H[k] = \max ( 1 + \text{suff}[k+1], \max_{m} (\text{distinct}(k+1, m) + (A[k] \notin A[k+1..m] ? 1 : 0) + \text{suff}[m+1]) )$.
This seems complicated to update.
Let's step back. Is there an $O(N)$ solution?
Yes. The function $val(j) = \text{distinct}(i+1, j) + \text{suff}[j+1]$ is not necessarily unimodal, but we can observe that we only care about the "new" elements.
Actually, the standard solution for this specific problem (AtCoder ABC 229 E) is:
Iterate $i$ from $1$ to $N-2$.
We need $\max_{j} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
Let's define $dp[x] = \max_{j \ge x} (\text{distinct}(x, j) + \text{suff}[j+1])$.
Then $dp[x] = \max( 1 + \text{suff}[x+1], \text{distinct}(x, x+1) + \text{suff}[x+2], \dots )$.
Notice that $\text{distinct}(x, j) = \text{distinct}(x+1, j) + (1 \text{ if } A[x] \text{ is new in } A[x+1..j] \text{ else } 0)$.
So $dp[x] = \max( 1 + \text{suff}[x+1], \max_{j \ge x+1} (\text{distinct}(x+1, j) + (A[x] \text{ new?}) + \text{suff}[j+1]) )$.
The term inside the max is $dp[x+1]$ if $A[x]$ is already present in the optimal range for $x+1$, or something slightly larger if it adds a new element.
Actually, simpler: $dp[x] = \max( 1 + \text{suff}[x+1], dp[x+1] + (1 \text{ if } A[x] \text{ is not in the optimal segment for } x+1 \text{ else } 0) )$. This is tricky because the optimal segment for $x+1$ might not include $A[x]$'s position relative to $x$.
Wait, the optimal $j$ for $x$ might be different from $x+1$.
Let's try a different property. The total distinct count is at most $N$.
Maybe we can just iterate $i$ and for each $i$, find the best $j$ using a two-pointer or similar? No, $O(N^2)$.
Let's re-read the constraints. $N=3 \cdot 10^5$. $O(N \log N)$ or $O(N)$ is needed.
The correct approach for this specific problem (ABC 229 E) is:
1. Precompute `suff[i]` = distinct count in $A[i..N]$.
2. Iterate $i$ from $1$ to $N-2$.
3. We want $\max_{j} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
Let $f(i, j) = \text{distinct}(i+1, j)$.
Observe that $f(i, j) = f(i, j-1) + (1 \text{ if } A[j] \text{ not in } A[i+1..j-1] \text{ else } 0)$.
This doesn't help directly with the max over $j$.
However, note that we can rewrite the objective:
Maximize $\text{distinct}(1, i) + \text{distinct}(i+1, j) + \text{distinct}(j+1, N)$.
Let's fix $j$ and vary $i$? Same issue.
Let's use the property that we can precompute `best[i]` = $\max_{j \ge i} (\text{distinct}(i, j) + \text{suff}[j+1])$.
Then the answer is $\max_i (\text{pref}[i] + \text{best}[i+1])$.
How to compute `best[i]`?
`best[i] = max(distinct(i, i) + suff[i+1], distinct(i, i+1) + suff[i+2], ...)`
`best[i] = max(1 + suff[i+1], max_{j >= i+1} (distinct(i, j) + suff[j+1]))`.
Note that `distinct(i, j) = distinct(i+1, j) + (1 if A[i] not in A[i+1..j] else 0)`.
So `best[i] = max(1 + suff[i+1], max_{j >= i+1} (distinct(i+1, j) + (A[i] not in A[i+1..j]) + suff[j+1]))`.
The term `max_{j >= i+1} (distinct(i+1, j) + suff[j+1])` is exactly `best[i+1]`.
So `best[i] = max(1 + suff[i+1], best[i+1] + (1 if A[i] not in A[i+1..j_opt] else 0))`.
The problem is the condition `A[i] not in A[i+1..j_opt]` depends on the optimal $j$ for $i+1$.
However, we can observe that if $A[i]$ appears in $A[i+1..N]$, let the first occurrence be at index $k$. Then for any $j < k$, $A[i]$ is new. For $j \ge k$, $A[i]$ is not new.
So we can split the range of $j$ into $[i+1, k-1]$ and $[k, N-1]$.
In $[i+1, k-1]$, `distinct(i, j) = distinct(i+1, j) + 1`. So the max in this range is `max_{j in [i+1, k-1]} (distinct(i+1, j) + 1 + suff[j+1]) = 1 + max_{j in [i+1, k-1]} (distinct(i+1, j) + suff[j+1])`.
In $[k, N-1]$, `distinct(i, j) = distinct(i+1, j)`. So the max is `max_{j in [k, N-1]} (distinct(i+1, j) + suff[j+1])`.
We know `best[i+1] = max( max_{j in [i+1, k-1]} (...), max_{j in [k, N-1]} (...) )`.
Let $M_1 = \max_{j \in [i+1, k-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1])$ and $M_2 = \max_{j \in [k, N-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
Then `best[i+1] = max(M_1, M_2)`.
The term we need for `best[i]` is `max(1 + M_1, M_2)`.
We can compute $M_1$ and $M_2$ if we know where the first occurrence of $A[i]$ is.
Let $next\_occ[i]$ be the index of the first occurrence of $A[i]$ in $A[i+1..N]$. If none, infinity.
Then $M_1$ is the max over $j \in [i+1, next\_occ[i]-1]$.
$M_2$ is the max over $j \in [next\_occ[i], N-1]$.
We can precompute these using a segment tree or simply by noticing that we can compute `best` backwards?
Actually, we can maintain the max values.
Let's define `pref_max[i]` = $\max_{j \in [i, N-1]} (\text{distinct}(i, j) + \text{suff}[j+1])$. This is our `best[i]`.
We need to compute `best[i]` from `best[i+1]`.
We know `best[i+1] = max(M_1, M_2)`.
We need `best[i] = max(1 + M_1, M_2)`.
If `best[i+1] == M_1`, then `best[i] = max(1 + M_1, M_2)`. Since $M_1 \ge M_2$ (because `best[i+1]` is the max of both), then $1+M_1 > M_2$, so `best[i] = 1 + M_1`.
If `best[i+1] == M_2`, then `best[i] = max(1 + M_1, M_2)`. Here $M_2 \ge M_1$. So `best[i] = max(1 + M_1, M_2)`.
We need to know if $M_1$ is close to $M_2$.
Actually, we can just store the pair $(M_1, M_2)$? No, $M_1$ depends on the range.
Wait, $M_1$ is the max over a prefix of the suffix range. As $i$ decreases, the range $[i+1, next\_occ[i]-1]$ grows.
This suggests we can compute `best` backwards from $N-1$ to $1$.
At step $i$, we know `best[i+1]`. We need to split the range of $j$ considered in `best[i+1]` based on $next\_occ[i]$.
But `best[i+1]` aggregates over all $j \ge i+1$. We don't know the split point $M_1$ vs $M_2$ just from `best[i+1]`.
We need to store more info. Maybe `best[i]` isn't enough.
Alternative: Use a Segment Tree.
Build a segment tree over indices $1..N$. Each leaf $j$ stores value $V_j = \text{suff}[j+1]$.
We want to query $\max_{j \in [L, R]} (\text{distinct}(i+1, j) + V_j)$.
But `distinct(i+1, j)` changes with $i$.
Actually, `distinct(i+1, j) = \text{distinct}(1, j) - \text{distinct}(1, i)$ is false.
Correct logic:
Iterate $i$ from $1$ to $N-2$.
We want $\max_{j} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
Let's precompute `suff`.
Then, we can iterate $i$ and maintain a data structure of values $val(j) = \text{distinct}(i+1, j) + \text{suff}[j+1]$.
As $i$ increases to $i+1$, the range of the middle part shifts. $A[i+1]$ is removed from the start of the middle part.
This is hard to maintain.

Let's go back to the $O(N)$ logic with $next\_occ$.
We need to compute $M_1 = \max_{j \in [i+1, k-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1])$ and $M_2 = \max_{j \in [k, N-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1])$ where $k = next\_occ[i]$.
Notice that for $j \ge k$, $\text{distinct}(i, j) = \text{distinct}(i+1, j)$.
So $M_2$ for $i$ is exactly the same as the contribution of $[k, N-1]$ to `best[i+1]`.
For $j < k$, $\text{distinct}(i, j) = \text{distinct}(i+1, j) + 1$.
So $M_1$ for $i$ is $1 + \max_{j \in [i+1, k-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
Let $G[i] = \max_{j \in [i, N-1]} (\text{distinct}(i, j) + \text{suff}[j+1])$. This is what we called `best[i]`.
We need to know $\max_{j \in [i, k-1]} (\text{distinct}(i, j) + \text{suff}[j+1])$.
Let's define $H[i] = \max_{j \in [i, N-1]} (\text{distinct}(i, j) + \text{suff}[j+1])$.
We need to compute $H[i]$.
$H[i] = \max ( 1 + \text{suff}[i+1], \max_{j \in [i+1, k-1]} (\text{distinct}(i, j) + \text{suff}[j+1]), \max_{j \in [k, N-1]} (\text{distinct}(i, j) + \text{suff}[j+1]) )$.
Note $\text{distinct}(i, j) = \text{distinct}(i+1, j) + 1$ for $j < k$.
So the middle term is $1 + \max_{j \in [i+1, k-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
The last term is $\max_{j \in [k, N-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
Let $P[x] = \max_{j \in [x, N-1]} (\text{distinct}(x, j) + \text{suff}[j+1])$. This is $H[x]$.
We need to compute $P[i]$ from $P[i+1]$.
$P[i] = \max ( 1 + \text{suff}[i+1], 1 + \max_{j \in [i+1, k-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1]), \max_{j \in [k, N-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1]) )$.
The term $\max_{j \in [k, N-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1])$ is NOT $P[i+1]$ because $P[i+1]$ includes $j \in [i+1, k-1]$.
Let $Q[x] = \max_{j \in [x, N-1]} (\text{distinct}(x, j) + \text{suff}[j+1])$.
We need to track the max over two ranges.
Actually, we can just compute $P[i]$ by iterating? No.
Wait, $k = next\_occ[i]$.
If $k = i+1$, then the range $[i+1, k-1]$ is empty. $P[i] = \max(1+\text{suff}[i+1], \max_{j \in [i+1, N-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1]))$.
The second term is exactly $P[i+1]$. So $P[i] = \max(1+\text{suff}[i+1], P[i+1])$.
If $k > i+1$, then we have a non-empty range.
We need $\max_{j \in [i+1, k-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
Let this be $LocalMax[i+1, k-1]$.
Then $P[i] = \max(1+\text{suff}[i+1], 1 + LocalMax[i+1, k-1], \max_{j \in [k, N-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1]))$.
The last term is $\max(P[i+1], \text{something})$. Actually, $P[i+1] = \max(LocalMax[i+1, k-1], \max_{j \in [k, N-1]} ...)$.
So $P[i] = \max(1+\text{suff}[i+1], 1 + LocalMax[i+1, k-1], P[i+1])$.
Since $P[i+1] \ge LocalMax[i+1, k-1]$, $1 + LocalMax \le 1 + P[i+1]$.
But we don't know if $P[i+1]$ comes from the left or right part.
However, note that $1 + LocalMax[i+1, k-1]$ is likely larger than $LocalMax[i+1, k-1]$.
Is it possible that $P[i+1]$ comes from the right part (where $A[i]$ is not new) and $1+LocalMax$ is smaller?
Yes.
So we need to know $\max_{j \in [i+1, k-1]} (\text{distinct}(i+1, j) + \text{suff}[j+1])$.
This value is simply the max of the function $f(j) = \text{distinct}(i+1, j) + \text{suff}[j+1]$ over $j \in [i+1, k-1]$.
Notice that as $i$ decreases, $i+1$ decreases, and the function changes.
This seems to require a segment tree where we update values as $i$ changes.
But wait, we can compute $P[i]$ backwards.
We need to query range max of a specific function.
The function for $i+1$ is $g_{i+1}(j) = \text{distinct}(i+1, j) + \text{suff}[j+1]$.
The function for $i$ is $g_i(j) = \text{distinct}(i, j) + \text{suff}[j+1]$.
For $j < k$, $g_i(j) = g_{i+1}(j) + 1$.
For $j \ge k$, $g_i(j) = g_{i+1}(j)$.
So $P[i] = \max( \max_{j < k} (g_{i+1}(j) + 1), \max_{j \ge k} g_{i+1}(j) )$.
$P[i] = \max( 1 + \max_{j \in [i+1, k-1]} g_{i+1}(j), \max_{j \in [k, N-1]} g_{i+1}(j) )$.
We know $P[i+1] = \max( \max_{j \in [i+1, k-1]} g_{i+1}(j), \max_{j \in [k, N-1]} g_{i+1}(j) )$.
Let $L = \max_{j \in [i+1, k-1]} g_{i+1}(j)$ and $R = \max_{j \in [k, N-1]} g_{i+1}(j)$.
$P[i+1] = \max(L, R)$.
$P[i] = \max(1+L, R)$.
We need to know $L$ and $R$ separately.
We can maintain a segment tree over $j \in [1, N-1]$ storing $g_{i+1}(j)$.
Initially for $i=N-1$, $g_{N-1}(j)$ is defined.
As we move from $i+1$ to $i$, we update the segment tree: for $j < k$, value increases by 1.
This is a range add update!
Algorithm:
1. Compute `suff` array.
2. Initialize a segment tree (or Fenwick tree if we only need max) over indices $1..N-1$.
3. For $j$ from $1$ to $N-1$, initial value $val[j] = \text{distinct}(N, j) + \text{suff}[j+1]$. Wait, distinct(N, j) is just 1 if $j \ge N$? No, $j$ goes up to $N-1$.
   Actually, we start from $i=N-2$ down to $1$.
   Base case: $i=N-2$. Range $j \in [N-1, N-1]$. $g_{N-2}(N-1) = \text{distinct}(N-1, N-1) + \text{suff}[N] = 1 + 0 = 1$.
   Wait, `suff[N]` should be 0. `suff[N+1]` is 0.
   Let's define `suff[x]` for $x \in [1, N]$. `suff[N] = 1` (if we consider non-empty? No, problem says non-empty subarrays).
   The split is $1..i$, $i+1..j$, $j+1..N$.
   $j$ goes from $i+1$ to $N-1$.
   So $j+1$ goes from $i+2$ to $N$.
   `suff[x]` = distinct in $A[x..N]$. `suff[N] = 1`. `suff[N+1] = 0`.
   Initialize segment tree with values for $i=N-2$.
   $j$ can only be $N-1$.
   $val[N-1] = \text{distinct}(N-1, N-1) + \text{suff}[N] = 1 + 1 = 2$.
   Then iterate $i$ from $N-3$ down to $1$.
   Find $k = next\_occ[i]$.
   Update segment tree: range $[i+1, k-1]$ add 1.
   Query max in $[i+1, N-1]$. This is $P[i]$.
   Update global answer with $\text{pref}[i] + P[i]$.
   Complexity: $O(N \log N)$.