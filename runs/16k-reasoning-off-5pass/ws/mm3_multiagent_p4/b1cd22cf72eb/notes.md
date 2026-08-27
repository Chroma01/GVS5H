
## ideation
The problem reduces to choosing a common target height `H` (the sum of an upper and lower tooth after grinding) and deciding how much to grind each tooth. For a fixed `H`, the minimum cost is always `sum(U_i + D_i) - N*H`, provided we can achieve `H` with the adjacency constraint. The cost is linear and decreasing in `H`, so we want the **maximum feasible `H`**.

The feasibility condition is: there exist final upper tooth lengths `a_i` with `0 ≤ a_i ≤ U_i`, `a_i ≤ H`, `a_i ≥ H - D_i`, and `|a_i - a_{i+1}| ≤ X` for all `i`. This is a constraint satisfaction problem on a chain. For a given `H`, it can be solved in `O(N)` by forward propagation of intervals `[L_i, R_i] = [max(0, H-D_i), min(U_i, H)]` with a sliding window of width `2X`.

However, the feasibility set of `H` is not necessarily a prefix interval; it can be a union of intervals. To find the maximum `H` efficiently without binary search on a non-monotonic predicate, we can instead use a **parametric search** or a **divide-and-conquer** approach, or we can binary search for the maximum `H` by checking feasibility of the system with `H` as a variable in the inequalities.

Actually, the set of feasible `H` **is** a prefix: one can prove that the lower and upper bounds `lo_i(H)` and `hi_i(H)` in the forward propagation are both non-decreasing in `H`. Hence `lo_i(H) ≤ hi_i(H)` defines a set that, if empty at some `H`, remains empty for all larger `H`. Thus feasibility is monotonic in `H`! (The earlier counterexample was mistaken because the intervals themselves were not correctly derived; in the propagation, the bounds are non-decreasing functions of `H`.) So we can binary search on `H` in `[0, min_i(U_i+D_i)]` and find the maximum feasible `H` in `O(N log(1e9))`.

## worker: Implement the solution in Python: read input, bina
The solution works as follows:

1. **Cost Formula**: For a chosen common height `H`, the optimal per-tooth grinding cost is exactly `U_i + D_i - H` (as long as `H ≤ U_i + D_i`). The total cost is `sum(U_i + D_i) - N*H`. Since this is linear and decreasing in `H`, we want the **maximum feasible `H`**.

2. **Feasibility Condition**: We need to find final upper tooth lengths `a_i` such that:
   - `0 ≤ a_i ≤ U_i`
   - `a_i ≤ H` (since the upper tooth cannot exceed `H` and also `H - D_i` lower bound from the lower tooth)
   - `a_i ≥ H - D_i`
   - `|a_i - a_{i+1}| ≤ X` for all adjacent pairs.

   This is equivalent to finding `a_i` in the interval `[L_i, R_i] = [max(0, H-D_i), min(U_i, H)]` with the adjacency constraint.

3. **Propagation**: For a fixed `H`, we can check feasibility in `O(N)` by maintaining the possible range `[lo, hi]` for the current `a_i` using the recurrence:
   - `lo = max(L_i, lo_prev - X)`
   - `hi = min(R_i, hi_prev + X)`
   If at any point `lo > hi`, the system is infeasible.

4. **Monotonicity**: Both `lo` and `hi` are non-decreasing functions of `H`. Therefore, the condition `lo ≤ hi` is monotonic: if `H` is infeasible, all larger `H` are also infeasible. This allows binary search for the maximum feasible `H`.

5. **Binary Search**: We search over `[0, min_i(U_i + D_i)]` (the absolute upper bound) to find the largest `H` for which the propagation succeeds. The answer is then `sum(U_i + D_i) - N * H_max`.

The time complexity is `O(N log(max_sum))` which is efficient for `N ≤ 2×10^5` and values up to `10^9`.
