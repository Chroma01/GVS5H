
## ideation
The problem is to maximize total units bought across N product types, each with infinite stock, where buying `k` units of type `i` costs `k² * P_i` yen, under a total budget `M`. The cost function per type is convex (quadratic) and separable across types.

Key observation: Because marginal costs increase with the number of units taken from a single product (`(2j-1)*P_i` for the `j`-th unit), and products are independent, the globally optimal way to maximize total units for a given budget is to buy as many units as possible from the cheapest product first, then the next cheapest, and so on. This is a classic greedy result for convex separable costs with a shared budget (exchange argument: shifting units from a more expensive product to a cheaper one never increases cost and can only increase or keep total units).

Thus the problem reduces to:
- Sort the prices `P_i` in non-decreasing order.
- Iterate through the sorted list, and for each product with price `p`, take the maximum number of units `k` such that `k² * p ≤ remaining_budget`. That is `k = floor(sqrt(remaining_budget / p))`.
- Subtract `k² * p` from the remaining budget and add `k` to the total units.
- Continue until all products processed or budget exhausted.

This greedy directly yields the maximum total units; no binary search or feasibility check is needed.

Constraints: `N ≤ 2·10⁵`, `M ≤ 10¹⁸`, `P_i ≤ 2·10⁹`. Python's arbitrary-precision integers and `math.isqrt` (or `int(remaining**0.5)` carefully) handle the arithmetic safely. Sorting is `O(N log N)`, which is well within limits.

Pitfalls:
- Using floating-point sqrt for large integers can cause precision errors; use integer square root (`math.isqrt` in Python 3.8+).
- The budget can become zero early, so break early.
- Total answer can be up to roughly `sqrt(M) + ...`; with `M = 10¹⁸` and `P_i = 1`, answer is `10⁹`, which fits easily in Python int.

## worker: The solution is fully described and the algorithm 
The greedy strategy of buying as many units as possible from the cheapest product first is optimal because the per-unit marginal cost is increasing (convex) and products are independent. Sorting prices and iteratively taking the maximum feasible `k` from each product yields the global maximum total units under the budget. Integer arithmetic and `math.isqrt` avoid floating-point precision issues; Python's arbitrary-precision integers safely handle values up to `10^18` and beyond. The algorithm runs in `O(N log N)` time due to sorting, with `O(N)` memory.
