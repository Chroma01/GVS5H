
## ideation
The problem asks for the minimum total cost (each unit of grinding costs 1 yen) to make the teeth "fit together well". We can only decrease lengths. The final state requires a common sum `H = U_i' + D_i'` for all `i`, and the final upper teeth sequence must be `X`-Lipschitz: `|U_i' - U_{i+1}'| ≤ X`.

Key observations:
- For a fixed `H`, the total cost is `Σ (U_i + D_i) - N*H`, which is independent of how we distribute the reduction between upper and lower teeth. So we only need to maximize feasible `H`.
- `H` must satisfy `H ≤ U_i + D_i` for all `i`, i.e., `H ≤ min(S_i)` where `S_i = U_i + D_i`.
- For a given `H`, the final upper length `A_i = U_i'` must lie in `[L_i, R_i]` where:
  - `L_i = max(0, H - D_i)` (to keep `D_i' = H - A_i ≥ 0` and `≤ D_i`)
  - `R_i = min(U_i, H)` (since we cannot increase lengths)
- Feasibility of the Lipschitz condition can be checked greedily in O(N) by maintaining the allowed range `[low, high]` of `A_i` after processing each tooth. The recurrence: `low = max(L_i, low - X)`, `high = min(R_i, high + X)`. If `low > high` at any point, infeasible. Initially the range is unbounded (or a very large range).
- Feasibility is monotonic non-decreasing in `H`: as `H` increases, both `L_i` and `R_i` generally increase or stay the same, relaxing constraints. So we can binary search the maximum feasible `H` in `[0, min S_i]`.

Algorithm:
1. Read `N, X`, arrays `U, D`. Compute `S_i = U_i + D_i`, total sum `T = Σ S_i`, and `minS = min S_i`.
2. Binary search `H` in `[0, minS]` for the largest feasible value using the O(N) check.
3. Answer = `T - N * H`.

Complexities: O(N log max_S) time, O(1) extra space. Use 64-bit integers (Python int handles automatically).

## worker: Implement the feasibility check function `check(H)
The solution binary searches the optimal common sum `H`. For a fixed `H`, the required upper tooth lengths `A_i` must lie in `[max(0, H-D_i), min(U_i, H)]`. The Lipschitz condition is checked by maintaining a feasible interval `[low, high]` that evolves as `low = max(L_i, low - X)`, `high = min(R_i, high + X)`. Feasibility is monotonic in `H`, so the largest feasible `H` yields the minimum cost `Σ S_i - N*H`. The complexity is `O(N log max_S)` with `O(1)` extra space, well within limits for `N ≤ 2·10^5`.
