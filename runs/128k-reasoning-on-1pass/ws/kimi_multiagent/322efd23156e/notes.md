
## ideation
Core difficulty: each item belongs to exactly one vitamin group, so vitamin totals are independent except for the shared calorie budget. The objective is max-min rather than max-sum, and `A_i` is too large for DP over vitamin amounts. The useful small dimension is calories: `N, X <= 5000`, so `O(NX)` knapsack-style DP is feasible.

Key structure: split foods by `V_i` into 3 groups. For each group, run 0/1 knapsack over calories to get the best vitamin amount achievable for each calorie cost. Then convert “exactly c calories” to “at most c calories” with prefix maxima, giving a nondecreasing function `f_g(c)`.

Monotonicity enables binary search on answer `T`: define `need_g(T)` = minimum calories required for group `g` to reach at least `T`, found by binary searching the prefix-max array. Candidate `T` is feasible iff `need_1(T) + need_2(T) + need_3(T) <= X`. Proof sketch: if each group can reach `T` within those calorie amounts, union the chosen disjoint items; conversely any feasible selection with group calorie costs `c_g` implies `need_g(T) <= c_g`, so the sum of needs is at most `X`.

Pitfalls:
- Must handle missing vitamin groups: answer is 0 if any group has no items or cannot reach positive required `T`.
- Distinguish exact-cost DP from at-most-cost prefix maxima; initialize unreachable exact states with `-inf`.
- `need_g(T)` should be `X+1`/INF if unreachable; avoid infinite binary search ranges.
- Upper bound for binary search should be based on max possible group total, up to about `1e9`; use 64-bit in compiled languages, Python is fine.
- Each food is 0/1, not unbounded.
- `O(NX)` in Python is about 25M updates total across all groups, acceptable if loops are kept tight.

## worker: Implement the complete solution: parse input, buck
- Bucketed items by vitamin into 3 groups; since each food has exactly one vitamin, group choices are independent given a calorie split.
- Per group, ran 0/1 knapsack over calories `0..X` (`dp[c]` = max vitamin amount at exactly `c` calories, `-1` = unreachable), iterating `j` descending to enforce 0/1 usage. Two speedups: track `reach` (max calorie index touched so far) and cap stored values at `cap_val = min(group totals)` since the answer can never exceed that — keeps integers small and checks valid for any `T <= cap_val`.
- Converted each DP to "at most c calories" with prefix maxima, yielding nondecreasing arrays.
- `feasible(T)`: for each group, `bisect_left` finds the minimum calories to reach `>= T`; feasible iff the three minimums sum to `<= X`. Correctness: if needs sum `<= X`, union the three disjoint item sets; conversely any feasible selection with group costs `c_g` satisfies `need_g(T) <= c_g`, so needs sum `<= X`.
- Binary searched max feasible `T` in `[0, cap_val]`. Empty group ⇒ total 0 ⇒ answer 0 immediately.
- Complexity: `O(NX)` time (≤ 25M tight inner steps), `O(X)` memory per group; feasibility check `O(log X)`, binary search `O(log(1e9) · log X)`.
