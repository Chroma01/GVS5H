
## ideation
**Core difficulty**: We need to maximize total units bought subject to a convex quadratic cost per product. The naive DP or enumeration is impossible (N up to 2e5, M up to 1e18, P_i up to 2e9, and stock per product is huge).

**Key observations**:
1. Cost per product is `k² · P_i` (convex in k). To minimize cost for a given total X, we should buy more units from cheaper products (smaller P_i) and fewer from expensive ones. Since cost is super-linear, the optimal distribution is greedy: fill the cheapest product first, then next cheapest, etc.
2. For a target X, a feasible distribution exists iff we can assign `x_i ≥ 0` with `sum x_i = X` and `sum x_i²·P_i ≤ M`.
3. Since `M ≤ 1e18` and `P_i ≥ 1`, the maximum units per product is at most `sqrt(1e18) ≈ 1e9`. For any single product, the number of units is bounded by `floor(sqrt(M / P_i))`, but typically very small if P_i is large.

**Approach: Binary search + greedy feasibility check**:
- Binary search answer X in `[0, total_possible]`.
- To check X, sort P_i ascending.
- Maintain remaining units needed R = X and remaining budget B = M.
- For each product i (cheapest first):
  - We can take at most `t = floor(sqrt(B / P_i))` units from it (cost constraint).
  - We must leave at least `remaining_products = N - i - 1` units for the future (since we need total X and each future product contributes at least 0, but we can also say: at least 0). Actually we need to ensure we don't over-allocate early such that later products can't reach X. So we can take at most `R` (can't exceed need), and at most `t`. But we also need to ensure that the rest of the products (with higher P) can still possibly contribute: they have no lower bound, so we can take `min(R, t)`.
  - However, we also need to be careful: if we take too few early, later products may not have enough budget. But since later products are more expensive, we should take as much as possible from cheap ones. So `x_i = min(R, t)`.
  - But we must ensure that after taking `x_i`, we can still reach total X. Since later products can take up to `floor(sqrt(remaining_budget / P_j))` each, the total capacity of remaining products might be less than `R - x_i`. So we need to check if the remaining capacity is enough. Alternatively, use a known trick: the total maximum units we can buy with budget B from remaining products is bounded by sum of `floor(sqrt(B / P_j))`. But that's hard to compute quickly.

**Better greedy check (standard solution)**:
- Sort P ascending.
- R = X, B = M.
- For each i from 0 to N-1:
  - The remaining products (i+1 to N-1) must supply at least `R - max_take_i` units? No, they can supply 0, so no lower bound.
  - But we must ensure that we don't allocate more than what we can afford. If we take `x = min(R, floor(sqrt(B / P_i)))` units, we might run out of budget early for cheap products and have no budget left for expensive ones (which we wouldn't buy anyway). This greedy is actually correct: since cheaper products dominate, we should buy as much as possible from the cheapest.
  - The only subtlety: we need to ensure that the remaining products can still cover the remaining units. Since remaining products have higher P, their unit capacity is lower, but we only need a total of R - x. If R - x > sum_{j>i} floor(sqrt(B_rem / P_j)) at any point, we fail. But this is hard to check incrementally.

**Alternative viewpoint**: The problem is equivalent to minimizing total cost for a given number of units. By convexity and monotonicity of P, the optimal strategy is: sort P ascending, and for each product, buy as many as possible (limited by budget and need) before moving to the next.

**Refined greedy check**:
- Sort P ascending.
- R = X, B = M.
- For i in 0..N-1:
  - `max_take = floor(sqrt(B / P_i]))`
  - `take = min(R, max_take)`
  - `B -= take * take * P_i`
  - `R -= take`
  - If R == 0: return True
  - If B < 0: return False (shouldn't happen if max_take is correct, but careful with overflow)
- After loop, return (R == 0)

**Is this greedy correct?** Yes, because if we can buy X units total with cost ≤ M, then there exists a distribution. The greedy that maximizes units from cheapest products first never costs more than the optimal distribution for a given total X (by exchange argument: if optimal uses a cheaper product less and an expensive one more, swapping reduces cost). So if greedy fails (runs out of budget or can't reach X), optimal also fails.

Wait, is that true? The greedy takes as much as possible from the cheapest. If the optimal takes fewer from cheapest and more from expensive, then greedy's cost is lower or equal for the same total X. So if greedy's cost exceeds M, optimal's cost also exceeds M. If greedy can't reach X (because at some point remaining budget can't support the needed units from more expensive products), then optimal also can't.

**Binary search bounds**:
- Lower bound: 0.
- Upper bound: sum over i of `floor(sqrt(M / P_i))` (maximum units if we spent all M on each product independently). But this could be up to N * 1e9 ≈ 2e14, fits in 64-bit.
- Or simpler: upper bound = N * floor(sqrt(M / min(P_i))) but that's loose. Better: just use 2e18 or compute max_possible = sum_{i} int(sqrt(M // P_i)) + N (safety). But M=1e18, P_i=1 → max 1e9 per product, N=2e5 → 2e14. Safe in 64-bit.

**Implementation details**:
- Use `math.isqrt` for integer square root.
- Sort P.
- Binary search with `while lo < hi: mid = (lo + hi + 1) // 2; if feasible(mid): lo = mid else: hi = mid - 1`.
- Feasible function as described.

**Edge cases**:
- M = 0: answer 0.
- P_i = 0? No, P_i ≥ 1.
- Overflow: `take * take * P_i` can exceed 1e18. Use `min(take, isqrt(M // P_i))` to be safe.

**Complexity**: O(N log N) for sorting + O(N log Answer) for binary search. Answer ≤ 2e14, so log2 ≈ 48. N = 2e5, total ~1e7 operations. Fine.

## worker: Implement the solution in Python: read input, sort
The solution uses binary search on the answer X (total units) combined with a greedy feasibility check. The greedy works because cost is convex (k²·P_i), so to minimize cost for a fixed total X, we should buy as many units as possible from the cheapest products first. If the greedy fails to achieve X within budget M, then no distribution can. The upper bound for binary search is computed as the sum of maximum units per product if all budget were spent on each individually, which is safe and fits in 64-bit integers. `math.isqrt` is used for integer square root to avoid floating-point precision issues.
