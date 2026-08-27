
## ideation
The problem asks to maximize the minimum among three vitamin totals subject to a calorie budget `X`. Each food gives a positive amount of exactly one vitamin, with a cost (calories). `N, X ≤ 5000`, but `A_i` can be up to `2·10^5`.

**Core difficulty**  
The objective is the `min` of three sums, not a single sum. Directly maximizing the minimum suggests parametric search: guess a value `t` and check feasibility (can we obtain at least `t` of each vitamin within `X` calories?).

**Knapsack per vitamin**  
For a fixed `t`, we need for each vitamin the *minimum* calories to collect ≥ `t` units. That's like a knapsack where we want, for each cost, the maximum vitamin amount we can obtain using foods of that type. So we run a 0/1 knapsack per vitamin (weights = calories, values = vitamin amount) with capacity `X` (≤5000). After the knapsack, we have `best1[c] = max vitamin 1 amount with cost ≤ c` (by taking prefix max). Then the minimal cost to reach `t` for type 1 is the first index where `best1[c] ≥ t`, or `∞` if none.

Total calories needed to achieve at least `t` of each vitamin is the sum of these three minimal costs. Feasibility: sum ≤ `X`.

**Parametric search**  
`answer ≤ min(total vitamin 1 achievable, total vitamin 2 achievable, total vitamin 3 achievable)`. Upper bound can be the sum of all `A_i` for one vitamin, but safer to take the max total reachable for any vitamin (sum of all `A_i` of that type), or simply use a generous bound like `2·10^5 * 5000` (too big) – better: bound by the total amount of each vitamin achievable within `X` (knapsack result at `c = X`). So we can compute a global upper bound as `max over types of best[c=X]`. Binary search integer `t` in `[0, ub]`.

## worker: Implement the full solution in Python: parse input
- Group foods by vitamin type (1,2,3).
- For each type, run a 0/1 knapsack with capacity `X` (≤5000) to compute `dp[c]` = max vitamin amount with exact cost `c`. Then build a prefix-max array `best[c]` = max amount with cost ≤ `c`.
- Binary search the answer `t` in `[0, ub]` where `ub = max(best[t][X])`. For each candidate `t`, find the minimal cost per vitamin type to reach at least `t` (binary search on the non-decreasing `best` array). If the sum of three minimal costs ≤ `X`, the candidate is feasible.
- Complexity: three knapsacks `O(N·X)` (N,X ≤ 5000 → ~25M operations, fine in Python). Feasibility check is `O(log X)` per type. Binary search adds `O(log(ub)·log X)`.
- Edge cases: if a vitamin type cannot reach `t`, feasibility returns False. If no vitamin can be obtained, answer is 0.
