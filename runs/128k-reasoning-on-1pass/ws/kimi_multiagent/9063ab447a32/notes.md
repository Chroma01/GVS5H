
## ideation
Core difficulty: this is a convex separable knapsack/resource-allocation problem with enormous answer size, so simulating purchases one-by-one is impossible. The key insight is that the marginal cost of buying the `k`-th unit of product `i` is `(k^2 - (k-1)^2) P_i = (2k - 1) P_i`, which is strictly increasing in `k`. Therefore an optimal purchase is greedy by marginal cost: buy all available marginal units cheaper than some threshold, then possibly only some units exactly at the threshold.

The stock `10^100` is effectively infinite for all relevant purchases because any unit with marginal cost greater than `M` can never be included in a feasible purchase.

A clean threshold formulation: for a candidate marginal-cost limit `x`, product `i` contributes all units whose marginal cost `(2k-1)P_i <= x`. Solving gives `k_i(x) = floor((floor(x / P_i) + 1) / 2)` when `x >= P_i`, else `0`. The count is `sum k_i`, and the cost is `sum P_i k_i^2`. Both are monotone in `x`, so binary search the first threshold `c` whose full inclusion cost exceeds `M`. Then take everything with marginal cost `< c`, and fill remaining budget with as many marginal-cost-`c` units as possible.

Important details/pitfalls:
- Marginal cost is odd multiple of `P_i`: `(2k-1)P_i`, not `kP_i` or `k^2P_i`.
- Equality handling matters: many products may have the same marginal cost `c`; remaining budget may allow only some of them.
- Binary search invariant must ensure `calc_le(c-1)` is feasible and `calc_le(c)` is infeasible.
- Cap per-product `k` at `isqrt(M // P_i) + 1` during feasibility checks to avoid useless huge arithmetic and enable early exit when cost exceeds `M`.
- Python integers avoid overflow, but accumulated sums should still early-exit once `> M` for speed.
- Complexity target: `O(N log M)` with fast input; about `2e5 * 60` operations, acceptable in PyPy/C Python if loops are tight and use early termination.
- Edge cases: `N=1`; very large/small `P_i`; all products affordable up to marginal `M`; remaining budget smaller than `c`; duplicate marginal costs across products.

The proposed plan is fundamentally sound: binary search on marginal-cost threshold, compute exact feasible prefix below threshold, then distribute leftover yen among equal-threshold units.

## worker: finalize
Used the convex marginal-cost structure: the `k`-th unit of product `i` costs `(2k-1)P_i`, increasing in `k`, so an optimal purchase takes marginal units in increasing order. For a threshold `x`, product `i` contributes `k=(x//P_i+1)//2` units, with cost `P_i*k^2`. Binary search finds the first threshold `c` where taking all marginal costs `<= c` exceeds `M`; then everything `< c` is taken, and the leftover budget buys as many marginal-cost-`c` units as possible. Caps via `isqrt(M//P_i)+1` give early infeasibility and avoid huge arithmetic. Complexity is `O(N log M)`.
