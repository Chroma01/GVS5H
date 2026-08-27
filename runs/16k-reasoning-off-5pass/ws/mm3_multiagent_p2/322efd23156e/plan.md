We solve via parametric search with per-type knapsack:
1. Read input and group foods by vitamin type.
2. For each type, run a 0/1 knapsack over calorie capacity X to compute the maximum total amount of that vitamin achievable with each exact cost, then convert to a non‑decreasing “best” array (max amount with cost ≤ c).
3. Binary‑search the answer `ans`. For a candidate `ans`, compute the minimal calories needed for each type to reach at least `ans` (linear scan of that type’s `best` array). If the three minima sum to ≤ X the candidate is feasible.
4. The maximum feasible `ans` is the answer.