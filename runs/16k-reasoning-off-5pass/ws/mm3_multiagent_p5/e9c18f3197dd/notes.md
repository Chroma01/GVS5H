
## ideation
The problem is essentially an assignment: we have up to 5e4 nums and at most 4 targets. For each target `t` and each num `n`, the cheapest cost to turn `n` into a multiple of `t` is `((t - n % t) % t)`. We must assign each target to a distinct num (each num can satisfy at most one target) and minimize the sum of costs.

Key observations:
- The minimal cost for a given `(n, t)` is easy: `cost = (t - n % t) % t`.
- Since `target.length <= 4`, the assignment search space is small if we limit the candidate nums per target.
- For a fixed target, the optimal num is among those with the smallest costs; we don't need to consider all 5e4 nums. Taking the top‑K cheapest (e.g., K = 50 or even 100) for each target is sufficient because the optimal solution must use one of these cheap candidates for each target (if a solution uses a more expensive candidate, swapping it with a cheaper unused one would not increase cost unless indices conflict; we can handle conflicts by trying all combos).
- With K = 50 and k ≤ 4, we have at most 50^4 = 6.25M combinations, which is fine in Python with pruning.

Approach:
1. For each target `t`, compute `cost[i] = (t - nums[i] % t) % t` for all i.
2. Build a list of `(cost, index)` per target, sort by cost ascending, and keep the first K entries.
3. Use backtracking (DFS) over the targets: at each step pick one of the K candidates for that target, ensure the index hasn't been used, accumulate cost, and prune if current cost >= best.
4. Return the minimum total cost found.

Pitfalls:
- We must track used indices to avoid assigning two targets to the same num.
- If a target already has a multiple in nums (cost 0), we can immediately consider it; the algorithm will handle it naturally.
- Edge case: `target.length == 0`? Not possible per constraints (1 ≤ target.length), but we can still guard.
- K should be chosen carefully: too small might miss optimal; too large increases combinations. K = 60–80 is safe for n ≤ 5e4 and k ≤ 4. We can also use a more aggressive bound (e.g., up to 200) if performance allows; 50 is usually enough because we only have 4 targets.
- All values are ≤ 1e4, so the cost per pair is at most 1e4, and total cost fits in int.

Complexity:
- Computing costs: O(m * k) ≤ 2e5.
- Sorting and truncating: O(m log m * k) but we only sort each list of size m, so O(m log m * k) ≤ 5e4 * log(5e4) * 4 ≈ 5e6.
- Backtracking: at most K^k combinations with pruning; with K = 50 and k = 4 worst-case 6.25M, each operation cheap.

This yields a correct and efficient solution.

## worker: Implement the `Solution` class with the `minimumIn
- Implemented as described: cost precomputation for each `(num, target)` pair, sort and keep top‑K (60) cheapest candidates per target, then backtrack over targets enforcing distinct indices.
- Pruning: skip recursion when `current_cost >= best`.
- Complexity: precomputation O(m·k) ≤ 2·10⁵; sorting O(m log m · k) ≤ ~5·10⁶; backtracking ≤ K^k = 60⁴ = 12.96M worst‑case (far less with pruning), easily fast for given constraints.
- Edge cases handled implicitly: existing multiples give cost 0 and are naturally chosen; distinct indices enforced via `used` array; integer overflow not an issue (max total cost ≤ 4·10⁴).
