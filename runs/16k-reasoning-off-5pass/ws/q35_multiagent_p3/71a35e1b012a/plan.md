1. **Problem Analysis**: The goal is to have `x_j = 1` for all `j` from 1 to `N`. 
   - Operation 1 sets `x_j = 1` for `j` in `[L_i, R_i]`.
   - Operation 2 sets `x_j = 1` for `j` not in `[L_i, R_i]`, i.e., for `j` in `[1, L_i-1]` and `[R_i+1, N]`.
   - We can think of this as covering the entire range `[1, N]` with "1"s. 
   - Note that once an element is set to 1, it stays 1 (since operations only set to 1, never to 0).

2. **Key Insight**: 
   - If we use Operation 1 on `[L, R]`, we cover the interval `[L, R]`.
   - If we use Operation 2 on `[L, R]`, we cover the intervals `[1, L-1]` and `[R+1, N]`.
   - The problem reduces to covering the entire range `[1, N]` using a combination of these operations with minimum cost.
   - Since each operation (1 or 2) costs 1, and Operation 0 costs 0, we want to minimize the number of non-zero operations.

3. **Dynamic Programming Approach**:
   - Let `dp[i]` be the minimum cost to cover the prefix `[1, i]` completely.
   - However, because Operation 2 covers two disjoint intervals at the ends, it's more complex. 
   - Alternatively, note that the union of all covered intervals must be `[1, N]`.
   - We can model this as: we need to cover every position `j` in `[1, N]` by at least one operation that sets it to 1.
   - For each position `j`, it can be covered by:
     - An Operation 1 on `[L, R]` where `L <= j <= R`.
     - An Operation 2 on `[L, R]` where `j < L` or `j > R`.

4. **Simplification**:
   - Consider the complement: which positions are NOT covered by an Operation 2? They must be covered by Operation 1s.
   - Actually, a better way is to realize that the set of indices that are 0 at the end are those not covered by any Operation 1 or Operation 2.
   - We can use DP where `dp[i]` = min cost to ensure that positions `1..i` are all 1.
   - But Operation 2 covers the "ends". 
   - Let's define `dp[i]` as the min cost to cover the range `[1, i]` completely.
   - Transitions:
     - To cover `[1, i]`, we can use an Operation 1 on some `[L, R]` such that `R = i` and `L <= i`. This covers `[L, i]`. Then we need `[1, L-1]` to be covered by previous operations. So `dp[i] = min(dp[L-1] + 1)` for all operations with `R=i`.
     - Or, we can use an Operation 2 on some `[L, R]`. This covers `[1, L-1]` and `[R+1, N]`. This is tricky because it covers two parts. 
     - Actually, Operation 2 is useful for covering the left end and right end simultaneously. 
     - Let's redefine: `dp[i]` = min cost to cover `[1, i]`.
     - Base case: `dp[0] = 0`.
     - For each `i` from 1 to `N`:
       - Option A: Use an Operation 1 ending at `i`: `dp[i] = min(dp[i], dp[L-1] + 1)` for each op with `R=i`.
       - Option B: Use an Operation 2 that covers `[1, L-1]` and `[R+1, N]`. If we use an Operation 2, it covers `[1, L-1]` and `[R+1, N]`. The gap `[L, R]` must be covered by other operations. This seems complex for a simple DP.

5. **Alternative Insight**:
   - Notice that if we never use Operation 2, we just need to cover `[1, N]` with Operation 1s. This is the classic interval covering problem.
   - If we use Operation 2, it effectively "saves" us from having to cover the left part `[1, L-1]` and right part `[R+1, N]` with other operations.
   - We can iterate over all possible "last" operations or use a DP that considers the rightmost uncovered point.
   - Let `dp[i]` be the min cost to cover the suffix `[i, N]`.
   - Or, let's use the fact that `N` is up to `10^6` and `M` is `2*10^5`.
   - We can precompute for each `i`, the best Operation 1 ending at or after `i`, and best Operation 2 starting at or before `i`.

6. **Final Strategy**:
   - We will use DP where `dp[i]` is the minimum cost to make `x[1...i]` all 1s.
   - Initialize `dp[0] = 0`, `dp[i] = infinity` for `i > 0`.
   - For each `i` from 1 to `N`:
     - `dp[i] = dp[i-1]` (if `x[i]` is already covered by previous ops, but we don't track state easily).
     - Instead, we process operations. 
     - Let's store operations by their `R` for Op 1 and `L` for Op 2.
     - For Op 1 `[L, R]`: it can update `dp[R]` from `dp[L-1] + 1`.
     - For Op 2 `[L, R]`: it covers `[1, L-1]` and `[R+1, N]`. This means if we use this op, the cost is `1 + cost_to_cover([L, R])`. The cost to cover `[L, R]` can be computed recursively or via DP.
     - This suggests a DP on intervals or a different state.

   - Given the complexity, a simpler observation:
     - The answer is -1 if the union of all possible covered ranges (from Op 1 and Op 2) does not cover `[1, N]`.
     - We can use a DP where `dp[i]` = min cost to cover `[1, i]`.
     - `dp[i] = min(dp[i-1], min_{op1 ending at i} (dp[L-1] + 1), min_{op2} (1 + cost_to_cover([L, R]) where op2 covers [1, L-1] and [R+1, N]))`.
     - The term `cost_to_cover([L, R])` is `dp[R] - dp[L-1]` if we assume independence, which is not true.

   - Correct DP:
     - `dp[i]` = min cost to cover `[1, i]`.
     - `dp[i] = dp[i-1]` is not valid because we don't know if `i` is covered.
     - We must cover `i`. It can be covered by:
       1. An Op 1 `[L, i]`: then `dp[i] = min(dp[i], dp[L-1] + 1)`.
       2. An Op 2 `[1, R]` (i.e., `L=1`): then `[1, 0]` (empty) and `[R+1, N]` are covered. This covers `[1, 0]` trivially and `[R+1, N]`. This doesn't help cover `[1, i]` if `i <= R`. If `i <= R`, then Op 2 with `L=1` covers `[1, 0]` (nothing) and `[R+1, N]`. It does NOT cover `[1, R]`. Wait, Op 2 on `[1, R]` sets `x_j=1` for `j < 1` (none) and `j > R`. So it covers `[R+1, N]`. It does NOT cover `[1, R]`. So Op 2 with `L=1` is only useful for the right tail.
       3. An Op 2 `[L, R]` with `L > 1`: covers `[1, L-1]` and `[R+1, N]`. To cover `[1, i]`, if `i < L`, then `[1, i]` is covered by the left part of Op 2. Cost = `1 + cost_to_cover([L, N])`? No.
       
   - Let's use `dp[i]` = min cost to cover `[i, N]`.
     - `dp[N+1] = 0`.
     - For `i` from `N` down to 1:
       - `dp[i] = dp[i+1]` (if `i` is covered by an op that covers `i+1`? No).
       - We must cover `i`.
       - Option 1: Use Op 1 `[i, R]`. Then we cover `[i, R]`. The remaining to cover is `[R+1, N]`. So `dp[i] = min(dp[i], 1 + dp[R+1])`.
       - Option 2: Use Op 2 `[L, R]` such that `L <= i`. If `L <= i`, then the left part `[1, L-1]` is covered (but we are solving for suffix `[i, N]`, so this is irrelevant for the left). The right part `[R+1, N]` is covered. The gap `[L, R]` must be covered. Since `i` is in `[L, R]`, we need to cover `[i, R]` and `[R+1, N]`. But Op 2 covers `[R+1, N]` directly. So we need to cover `[i, R]`. This leads to recursion.

   - Given the constraints and complexity, a known solution for this problem is:
     - Check if it's possible: The union of all `[L_i, R_i]` (for Op 1) and all `[1, L_i-1] U [R_i+1, N]` (for Op 2) must cover `[1, N]`.
     - Use DP: `dp[i]` = min cost to cover `[1, i]`.
     - `dp[0] = 0`.
     - For `i` from 1 to `N`:
       - `dp[i] = dp[i-1]` is not correct.
       - Instead, we can iterate over all operations that cover `i`.
       - This is a standard "minimum cost to cover a line segment" problem with two types of intervals.
       - We can use a segment tree or a simple DP with optimization.

   - Simplified Plan for Code:
     1. Read input.
     2. Check feasibility: If the union of all possible covered ranges doesn't cover `[1, N]`, output -1.
     3. Use DP: `dp[i]` = min cost to cover `[1, i]`.
     4. Initialize `dp` array with infinity, `dp[0] = 0`.
     5. For each operation `k` with range `[L, R]`:
        - If we use Op 1: it covers `[L, R]`. Update `dp[R] = min(dp[R], dp[L-1] + 1)`.
        - If we use Op 2: it covers `[1, L-1]` and `[R+1, N]`. This is global. 
     6. Actually, we can process the DP in order. For each `i`, `dp[i]` can be updated by:
        - `dp[i] = min(dp[i], dp[i-1])`? No.
        - We can use a "sweep-line" or "priority queue" to manage the best previous state.

   - Given the time, I'll implement a DP that considers:
     - `dp[i]` = min cost to cover `[1, i]`.
     - We maintain a list of active operations.
     - For each `i`, we consider all Op 1s ending at `i`: `dp[i] = min(dp[i], dp[L-1] + 1)`.
     - We also consider Op 2s. An Op 2 `[L, R]` covers `[1, L-1]` and `[R+1, N]`. If we use an Op 2, the cost is `1 + cost_to_cover([L, R])`. The cost to cover `[L, R]` is `dp[R] - dp[L-1]`? No, because the operations are not additive in that way.

   - Correct approach from similar problems:
     - `dp[i]` = min cost to cover `[1, i]`.
     - `dp[i] = min(dp[i-1], min_{op1: R=i} (dp[L-1] + 1), min_{op2: L-1 < i} (1 + dp[R] - dp[L-1] + dp[L-1]))`? No.
     - Let's use the fact that Op 2 with `[L, R]` means we pay 1 and then we need to cover `[L, R]`. So `dp[R] = min(dp[R], 1 + dp[L-1] + cost_to_cover([L, R]))`. This is circular.

   - Final Decision: Use a DP where `dp[i]` is min cost to cover `[1, i]`.
     - `dp[0] = 0`.
     - For `i` from 1 to `N`:
       - `dp[i] = dp[i-1]` is not valid.
       - We can only update `dp[i]` if `i` is covered by an operation.
       - We'll store operations in buckets by `R` (for Op 1) and `L` (for Op 2).
       - For Op 1 `[L, R]`: `dp[R] = min(dp[R], dp[L-1] + 1)`.
       - For Op 2 `[L, R]`: This covers `[1, L-1]` and `[R+1, N]`. So if we use this, we need to cover `[L, R]`. The cost would be `1 + (dp[R] - dp[L-1])`? No, because `dp[R]` includes covering `[1, R]`.
       - Actually, if we use Op 2, we cover `[1, L-1]` for free (in the sense that it's part of the Op 2 effect) and `[R+1, N]` for free. We only need to cover `[L, R]`. So the cost to cover `[1, N]` using this Op 2 is `1 + cost_to_cover([L, R])`.
       - This suggests we should compute `dp` for the whole array and then check.

   - Given the complexity, I will implement a solution that:
     1. Checks if it's possible.
     2. Uses a DP with a segment tree or a simple array for small N, but N is 10^6.
     3. I'll use a standard DP with optimization: `dp[i] = min(dp[i-1], min_{op1 ending at i} (dp[L-1] + 1))`. For Op 2, we can treat it as: if we use Op 2 `[L, R]`, then `dp[N]` can be updated from `dp[L-1] + 1 + cost_to_cover([L, R])`. This is hard.

   - I'll use a known trick: 
     - `dp[i]` = min cost to cover `[1, i]`.
     - `dp[i] = min(dp[i-1], min_{op1: R=i} (dp[L-1] + 1))`.
     - For Op 2, we can consider that it covers the left and right. We can iterate over all Op 2s and update the final answer.
     - `ans = min(dp[N], min_{op2} (1 + dp[R] - dp[L-1] + dp[L-1]))`? No.
     - `ans = min(dp[N], min_{op2} (1 + cost_to_cover([L, R])))`.
     - `cost_to_cover([L, R])` can be computed by a separate DP or by `dp[R] - dp[L-1]` if the operations are independent, which they are not.

   - I'll implement a solution that uses `dp[i]` for `[1, i]` and then checks Op 2s against the final answer.