
## ideation
**Core difficulty**

The two conditions are decoupled except for the global constant `H`:
- Condition 1 forces `U_i' + D_i' = H` for all `i` (after grinding).
- Condition 2 restricts only the upper teeth sequence `{U_i'}`: they must stay within `[0, U_i]` and satisfy `|U_i' - U_{i+1}'| ≤ X`.

If we fix `H`, the lower teeth are forced to `D_i' = H - U_i'`, which is feasible iff `0 ≤ U_i' ≤ H` (since `D_i' ≥ 0` ⇔ `U_i' ≤ H`).  
For a feasible `H`, the required grinding cost is:
```
total = Σ (U_i - U_i') + Σ (D_i - (H - U_i'))
      = Σ (U_i + D_i) - N·H
```
So **larger `H` is always better** (cost decreases linearly). The maximum possible `H` is `H_max = min_i (U_i + D_i)`.  
Thus the problem reduces to:

> **Find the largest `H` (≤ `H_max`) such that there exists a sequence `{u_i}` with**  
> `0 ≤ u_i ≤ U_i`, `u_i + D_i ≥ H` (i.e. `u_i ≥ H - D_i`), and `|u_{i+1} - u_i| ≤ X`.

**Feasibility check for a fixed `H`**

Define for each `i`:
```
low_i  = max(0, H - D_i)
high_i = U_i
```
We need `u_i ∈ [low_i, high_i]` and `|u_{i+1} - u_i| ≤ X`.

This is a classic interval feasibility for a chain. A greedy approach works:
- Process left → right: maintain the feasible interval `[lo, hi]` for the current `u_i`.
  Initially `lo = low_0, hi = high_0`.
  For each `i` from `0` to `N-2`:
  - The next tooth `u_{i+1}` must lie in `[low_{i+1}, high_{i+1}]` **and** in `[u_i - X, u_i + X]`.
  - Since we only need *some* value, we can propagate:
    ```
    lo = max(low_{i+1}, lo - X)
    hi = min(high_{i+1}, hi + X)
    ```
    If `lo > hi`, infeasible.
- After the pass, if we never failed, `H` is feasible.

**Why greedy works**: The constraints are a "difference ≤ X" chain. Propagating the feasible interval is equivalent to checking whether the intersection of constraints is non-empty. Because the constraint is symmetric and only depends on the immediate neighbor, maintaining the intersection of all possible values is correct and optimal.

## worker: Implement the full Python solution: write the feas
- The feasibility check `can(H)` propagates a feasible interval `[lo, hi]` for the upper tooth `u_i` left-to-right. Initially, `u_0 ∈ [max(0, H - D_0), U_0]`. For each step, the next tooth must lie in its own allowed interval and also within `X` of the previous, giving the interval intersection update. If at any point the interval becomes empty, `H` is infeasible.
- We binary search the largest `H` in `[0, min_i(U_i + D_i)]` that is feasible. The monotonicity holds: as `H` increases, lower bounds `max(0, H - D_i)` increase (or stay), shrinking the feasible region, so feasibility is monotone decreasing.
- The final answer is `Σ(U_i + D_i) - N * H_best`, derived from the cost formula. All arithmetic is in Python ints, avoiding overflow issues.
- The code reads inputs robustly (handling possible line splits) and runs in `O(N log C)` time where `C ≤ 2·10^9`, well within limits for `N ≤ 2·10^5`.
