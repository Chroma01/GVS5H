The problem asks whether we can set all elements of an array to 1 using M operations, each of which either sets a specific range to 1 (Op 1), sets the complement of a range to 1 (Op 2), or does nothing (Op 0), with the goal of minimizing total cost. Note that Op 2 sets all indices *outside* [L_i, R_i] to 1. This is equivalent to saying that the indices *inside* [L_i, R_i] are "skipped" or not forced to 1 by this operation (they remain whatever they were). However, since we want *all* to be 1, an element x_j is 1 at the end if there is at least one operation that forces it to 1.

Let's reframe: For each index j, we need at least one operation i such that either:
1. Op 1 is chosen and L_i <= j <= R_i, OR
2. Op 2 is chosen and NOT (L_i <= j <= R_i) i.e., j < L_i or j > R_i.

This is a covering problem. Each operation offers two potential "coverings" if we pay cost 1:
- Op 1 covers the interval [L_i, R_i].
- Op 2 covers the union of intervals [1, L_i-1] U [R_i+1, N].

If we choose Op 0, it covers nothing.

We want to select a subset of operations and for each selected operation, choose type 1 or 2, such that every index 1..N is covered, minimizing the number of selected operations.

This can be modeled as a shortest path problem on a graph or using dynamic programming. Since N is up to 10^6, we need an efficient approach.

Let's define `dp[j]` as the minimum cost to cover the prefix `1..j`. However, Op 2 covers non-contiguous regions, which makes simple prefix DP tricky.

Alternative view:
An index `j` is NOT covered by Op 1 of interval `[L, R]` if `j < L` or `j > R`.
An index `j` is NOT covered by Op 2 of interval `[L, R]` if `L <= j <= R`.

So, if we pick Op 1 for interval `[L, R]`, it covers `[L, R]`.
If we pick Op 2 for interval `[L, R]`, it covers `[1, L-1]` and `[R+1, N]`.

Let's consider the complement: Which indices are *not* covered by a specific choice?
- Op 1 on `[L, R]` leaves `[1, L-1]` and `[R+1, N]` potentially uncovered by this op.
- Op 2 on `[L, R]` leaves `[L, R]` potentially uncovered by this op.

This looks like we are trying to cover the set `{1, ..., N}`.
Let's define `S_i` as the set of indices covered if we choose Op 1 for operation i, and `T_i` as the set of indices covered if we choose Op 2 for operation i.
We want to choose `c_i \in {0, 1, 2}` for each i to minimize `sum(c_i != 0)` such that `Union_{i: c_i != 0} (if c_i==1 then S_i else T_i) = {1..N}`.

This is a Set Cover problem, which is NP-hard in general. However, the sets have special structure (intervals or complements of intervals).

Let's use Dynamic Programming.
Let `dp[i]` be the minimum cost to cover the range `[1, i]`. But Op 2 covers tails, so covering `[1, i]` might involve an Op 2 that also covers `[j, N]` for some `j > i`. This suggests we might need to track the "rightmost uncovered" or similar.

Actually, let's look at the structure of "uncovered" regions.
If we only used Op 1, we would cover intervals.
If we only used Op 2, we would cover prefixes and suffixes.

Consider the state as the rightmost index that is *not yet guaranteed to be covered* by the operations chosen so far? No, because Op 2 covers the end.

Let's try a different DP state.
`dp[i]` = minimum cost to ensure that all indices in `[1, i]` are covered.
To compute `dp[i]`, we can consider the last operation that "completed" the coverage up to `i`.
However, an operation might cover a gap in the middle.

Let's refine the state.
`dp[i]` = min cost to cover `[1, i]`.
Transitions:
1. We can extend from `dp[i-1]` by covering `i` with some operation.
   - If we use Op 1 on `[L, R]` where `L <= i <= R`, this operation also covers `[L, R]`. So if we use this, we might jump to `dp[R]`.
   - If we use Op 2 on `[L, R]` where `i < L` or `i > R`.
     - If `i > R`, this Op 2 covers `[1, L-1]` and `[R+1, N]`. Since `i > R`, `i` is covered. But this operation also covers a prefix `[1, L-1]`. This suggests it might be better to think about covering from the right or using intervals.

Let's consider the union of covered sets.
Let `R_max[i]` be the maximum right endpoint of an interval `[L, R]` among all operations that can cover index `i` via Op 1? No.

Let's go back to basics.
We want to cover `[1, N]`.
Let `dp[i]` be the min cost to cover `[1, i]`.
Base case: `dp[0] = 0`.
For `i` from 1 to N:
`dp[i] = dp[i-1] + infinity` (initially)

How can we cover `i`?
Option A: `i` is covered by an Op 1 on `[L, R]` where `L <= i <= R`.
If we pick such an operation, it covers `[L, R]`. The cost is 1. The previous state must have covered `[1, L-1]`. So we can transition from `dp[L-1]` to `dp[R]` with cost +1.
This suggests we should process intervals.

Option B: `i` is covered by an Op 2 on `[L, R]` where `i < L` or `i > R`.
Case B1: `i < L`. Then the Op 2 covers `[1, L-1]` and `[R+1, N]`. Since `i < L`, `i` is in `[1, L-1]`. This operation covers the prefix `[1, L-1]`. It also covers the suffix `[R+1, N]`.
Case B2: `i > R`. Then the Op 2 covers `[1, L-1]` and `[R+1, N]`. Since `i > R`, `i` is in `[R+1, N]`.

This implies that an Op 2 operation effectively covers a prefix and a suffix.
If we use an Op 2 on `[L, R]`, we pay 1, and we ensure `[1, L-1]` and `[R+1, N]` are covered. The gap `[L, R]` is NOT covered by this op.

So, the problem decomposes into covering the "gaps" left by Op 2s using Op 1s, or covering everything with Op 1s, or using a combination.

Let's define `dp[i]` as the min cost to cover `[1, i]`.
To compute `dp[i]`:
1. We can simply take `dp[i-1]` and cover `i` individually? No, operations cover ranges.

Let's use the interval-based DP.
Sort all "events" or use a segment tree / deque optimization.

Let `dp[i]` be the min cost to cover `[1, i]`.
Initialize `dp[0] = 0`, `dp[i] = infinity` for `i > 0`.

Transitions for `dp[i]`:
1. **Extend from previous**: If `i` is covered by an operation that also covered `i-1`, we might not add cost. But it's hard to track.
   
   Instead, let's look at what covers the "rightmost" part of the covered prefix.
   
   Let's consider the operations that can help cover up to `i`.
   
   **Type 1 Transition**:
   If we use Op 1 on `[L, R]`, it covers `[L, R]`. To use this to cover up to `R`, we need `[1, L-1]` to be already covered.
   So, for each operation `k` with Op 1 on `[L_k, R_k]`, we can update:
   `dp[R_k] = min(dp[R_k], dp[L_k - 1] + 1)`
   
   **Type 2 Transition**:
   If we use Op 2 on `[L, R]`, it covers `[1, L-1]` and `[R+1, N]`.
   This operation is special because it covers a prefix `[1, L-1]` for free (cost 1) and a suffix `[R+1, N]`.
   If we use Op 2, we pay 1. The prefix `[1, L-1]` is covered. The suffix `[R+1, N]` is covered.
   The gap `[L, R]` must be covered by other operations.
   
   This suggests we can split the problem.
   Let's say we decide to use a set of Op 2s. Each Op 2 `j` covers `[1, L_j-1]` and `[R_j+1, N]`.
   The union of these prefixes is `[1, max(L_j-1)]` if we pick the one with max `L_j-1`? No, it's the union of `[1, L_j-1]`, which is `[1, max_j(L_j-1)]`.
   Similarly, the union of suffixes is `[min_j(R_j+1), N]`.
   
   Let `P = max(L_j - 1)` over all chosen Op 2s.
   Let `S = min(R_j + 1)` over all chosen Op 2s.
   
   The Op 2s cover `[1, P]` and `[S, N]`.
   If `P >= S - 1`, then the entire array `[1, N]` is covered by Op 2s alone. Cost = number of Op 2s.
   If `P < S - 1`, then the gap `[P+1, S-1]` is not covered by Op 2s. We must cover this gap using Op 1s.
   Note: Op 1s can also be used to cover parts of `[1, P]` or `[S, N]`, but since Op 2s already cover them, we only *need* to cover `[P+1, S-1]`.
   However, an Op 1 might cover a range that overlaps with the gap. We need to cover `[P+1, S-1]` using Op 1s.
   The cost would be `|{Op 2s}| + cost_to_cover(P+1, S-1)`.
   
   But we can also mix Op 1s and Op 2s arbitrarily.
   
   Let's define `dp[i]` as the min cost to cover `[1, i]` using any combination of operations.
   
   We can process `i` from 1 to N.
   
   `dp[i]` can be updated by:
   1. `dp[i] = dp[i-1]` if `i` is "free"? No.
   
   Let's stick to the interval updates.
   `dp` array of size N+1, init `inf`, `dp[0]=0`.
   
   For each operation `k` with `[L_k, R_k]`:
   - **Op 1**: `dp[R_k] = min(dp[R_k], dp[L_k - 1] + 1)`
   - **Op 2**: This covers `[1, L_k-1]` and `[R_k+1, N]`.
     This is a global update. It says: if we use this Op 2, we pay 1, and we have covered `[1, L_k-1]` and `[R_k+1, N]`.
     This doesn't fit easily into a standard `dp[i]` = cover `[1, i]` because it covers a suffix.
     
   Let's change the DP state.
   `dp[i]` = min cost to cover `[1, i]`.
   `dp2[i]` = min cost to cover `[i, N]`.
   
   This might be symmetric.
   
   Let's try a combined approach.
   We can iterate over all possible "split points" or "gaps".
   
   Actually, notice that Op 2 on `[L, R]` is equivalent to:
   Cost 1, covers `[1, L-1] U [R+1, N]`.
   
   Let's consider the set of all Op 2s we might use.
   If we use a set of Op 2s, let `L_max = max(L_k - 1)` and `R_min = min(R_k + 1)`.
   The covered region is `[1, L_max] U [R_min, N]`.
   The uncovered region is `(L_max, R_min)`.
   We need to cover `(L_max, R_min)` using Op 1s.
   The cost is `|Set of Op 2s| + min_cost_to_cover(L_max+1, R_min-1)`.
   
   If `L_max >= R_min - 1`, the gap is empty or invalid, so cost is just `|Set of Op 2s|`.
   
   We can iterate over all possible pairs of `(L_max, R_min)`? No, too many.
   
   However, `L_max` must be `L_k - 1` for some operation `k`, and `R_min` must be `R_j + 1` for some operation `j`.
   
   Let's precalculate `min_op1_cost(a, b)` = min cost to cover `[a, b]` using only Op 1s.
   This is a standard interval covering problem.
   `min_op1_cost(a, b)` can be solved with DP:
   `g[i]` = min cost to cover `[a, i]`.
   `g[a-1] = 0`.
   For `i` from `a` to `b`:
     `g[i] = min(g[i-1] + 1)`? No, Op 1 covers ranges.
     `g[i] = min_{k: L_k <= i <= R_k} (g[L_k - 1] + 1)`? No, `g` is relative to `a`.
     Let `h[i]` be min cost to cover `[a, i]`.
     `h[i] = min( h[i-1] + 1, min_{k: R_k=i, L_k<=i} (h[L_k-1] + 1) )`?
     Actually, standard greedy or DP for interval covering:
     Sort intervals.
     `dp[x]` = min cost to cover `[a, x]`.
     `dp[x] = min(dp[x-1] + 1, min_{k: R_k=x} (dp[L_k-1] + 1))`?
     Wait, if we use Op 1 on `[L, R]`, it covers `[L, R]`. If we are covering `[a, x]`, and we use `[L, R]` with `R=x`, we need `[a, L-1]` covered.
     So `dp[x] = min(dp[x-1] + 1, min_{k: R_k=x} (dp[L_k-1] + 1))`.
     Note: `dp[x-1] + 1` assumes we cover `x` with a "unit" interval or something? No, this formula is for when we can cover any single point with cost 1. But we don't have unit intervals.
     Correct DP for covering `[a, b]` with Op 1s:
     Let `f[i]` be min cost to cover `[a, i]`.
     `f[a-1] = 0`.
     For `i` from `a` to `b`:
       `f[i] = f[i-1] + 1` is NOT valid unless we have an interval `[i, i]`.
       Instead, `f[i] = min( f[i-1] + 1, min_{k: R_k >= i and L_k <= i} ... )`?
       
       Actually, the standard way:
       `f[i] = min_{k: R_k = i} (f[L_k - 1] + 1)`
       And also `f[i] = min(f[i], f[i-1])`? No, if `[a, i-1]` is covered, `[a, i]` might not be.
       
       Let's use a segment tree or just iterate.
       Since N is 10^6, we need O(N log N) or O(N).
       
       Let's define `best_op1[i]` = min cost to cover `[1, i]` using Op 1s.
       `best_op1[0] = 0`.
       For `i` from 1 to N:
         `best_op1[i] = best_op1[i-1] + 1` (assuming we can cover `i` with cost 1, e.g., if there's an interval ending at `i` starting at `i`, or we treat it as a fallback? No, this is wrong).
         
       Correct logic for `best_op1[i]` (covering `[1, i]` with Op 1s):
       `best_op1[i] = infinity`.
       For each operation `k` with `R_k == i`:
         `best_op1[i] = min(best_op1[i], best_op1[L_k - 1] + 1)`
       Also, if `best_op1[i-1]` is finite, can we extend?
       Only if there is an interval `[i, i]` or similar.
       Generally, `best_op1[i]` is not necessarily `best_op1[i-1] + 1`.
       
       However, we can compute `best_op1` for all `i` efficiently.
       Let `ops_ending_at[i]` be list of `L_k` for ops with `R_k == i`.
       `best_op1[i] = min( best_op1[i-1] + 1, min_{L in ops_ending_at[i]} (best_op1[L-1] + 1) )`?
       The term `best_op1[i-1] + 1` is only valid if we can cover `i` with a "cost 1" operation that covers `i` and extends left. But we don't have arbitrary intervals.
       Actually, if we have an interval `[L, R]` covering `i`, we use `best_op1[L-1] + 1`.
       If we don't have an interval ending at `i`, `best_op1[i]` might be `best_op1[i-1]`? No, `i` must be covered.
       
       So, `best_op1[i] = min_{k: R_k >= i} ...`? No.
       
       Let's just compute `best_op1[i]` for all `i` using the recurrence:
       `best_op1[i] = infinity`
       For each `k` such that `R_k == i`:
         `best_op1[i] = min(best_op1[i], best_op1[L_k - 1] + 1)`
       If `best_op1[i]` is still infinity, it means `[1, i]` cannot be covered by Op 1s alone.
       
       Now, back to the main problem.
       We iterate over all possible "Op 2 configurations".
       An Op 2 configuration is defined by a set of operations.
       Let `S` be the set of indices of operations where we choose Op 2.
       Let `L_max = max_{k in S} (L_k - 1)`.
       Let `R_min = min_{k in S} (R_k + 1)`.
       Cost = `|S| + min_cost_to_cover(L_max + 1, R_min - 1)`.
       
       If `L_max + 1 > R_min - 1`, the gap is empty, so `min_cost = 0`.
       
       We need to minimize `|S| + min_cost_to_cover(L_max + 1, R_min - 1)` over all subsets `S`.
       
       This is still exponential.
       
       Observation:
       We can iterate over the "last" Op 2 used for the prefix and the "first" Op 2 used for the suffix?
       
       Let's iterate over all possible values of `L_max` and `R_min`.
       `L_max` can be any `L_k - 1`.
       `R_min` can be any `R_j + 1`.
       
       For a fixed `L_max` and `R_min`, we want to minimize `|S|` such that:
       `max_{k in S} (L_k - 1) = L_max`
       `min_{k in S} (R_k + 1) = R_min`
       And we must have `L_max < R_min - 1` (otherwise gap is empty).
       
       Actually, we don't need the max/min to be exactly `L_max` and `R_min`. We just need `max <= L_max` and `min >= R_min`?
       No, if `max < L_max`, we could have used a smaller `L_max`.
       
       Let's define:
       `A[l]` = min number of Op 2s needed such that `max(L_k - 1) <= l`.
       This is equivalent to: all chosen Op 2s must have `L_k - 1 <= l` => `L_k <= l + 1`.
       So `A[l]` is the min number of Op 2s from the set `{k : L_k <= l + 1}`?
       No, we just pick ANY subset. To minimize count, we pick 0 if possible?
       If we pick 0 Op 2s, `L_max` is undefined (or -1), `R_min` is undefined (or N+1).
       
       Let's handle the case of 0 Op 2s separately.
       Cost = `min_cost_to_cover(1, N)` using Op 1s.
       
       For 1 or more Op 2s:
       Let `u` be the operation that provides the maximum `L_k - 1`. Let `l_val = L_u - 1`.
       Let `v` be the operation that provides the minimum `R_k + 1`. Let `r_val = R_v + 1`.
       
       We can iterate over all pairs `(u, v)`? M is 200,000, so M^2 is too big.
       
       Instead, iterate over `u` (the op determining `L_max`).
       For a fixed `u`, `L_max = L_u - 1`.
       We want to choose a set `S` containing `u` (to ensure max is at least `L_u-1`, and we can enforce `u` is the one with max L) and possibly other ops `k` with `L_k - 1 <= L_u - 1`.
       We want to minimize `|S| + min_cost_to_cover(L_u, R_min - 1)`.
       
       This is complex. Given the time, I will implement a solution that:
       1. Computes `best_op1[i]` for all `i`.
       2. Iterates over all possible `L_max` (from `L_k-1`) and `R_min` (from `R_j+1`).
       3. Uses precomputed data to find min cost.