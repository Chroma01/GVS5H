
## ideation
**Core problem**  
We can only *decrease* tooth lengths (cost 1 per unit). We want to reach a state where all upper+lower pairs sum to a common constant H, and the upper lengths form a sequence with adjacent differences ≤ X.

**Key observations**

1. If we pick a target sum H, the only way to achieve it for column i is to reduce a total of `S_i - H` across the two teeth (where `S_i = U_i + D_i`). Any distribution of that reduction between the upper and lower tooth is allowed, as long as both resulting lengths stay non‑negative.
2. For a fixed H, the upper length `U'_i` must lie in an interval  
   `L_i = max(0, H - D_i)` ≤ `U'_i` ≤ `min(U_i, H)` = `R_i`.  
   This interval is non‑empty exactly when `H ≤ S_i` (i.e. H is feasible for that column).
3. With these intervals, the adjacency condition `|U'_i - U'_{i+1}| ≤ X` can be checked greedily:
   - `lo_1 = L_1`, `hi_1 = R_1`.
   - For `i > 1`:  
     `lo_i = max(L_i, lo_{i-1} - X)`  
     `hi_i = min(R_i, hi_{i-1} + X)`.
   - Feasible iff at the end `lo_N ≤ hi_N` (interval non‑empty).
4. The total cost to reach H is `Σ S_i - N·H`. Since Σ S_i is constant, minimizing cost ⇔ **maximizing** H.
5. Feasibility is monotone: if H works, any smaller H also works (intervals only widen). Therefore we can binary‑search the maximum feasible H.

## worker: Implement the solution in Python: read input, bina
Implemented binary search on the target sum H from 0 to max(S_i). For each H, the feasible range for each upper tooth is `[max(0, H-D_i), min(U_i, H)]`. Propagating these intervals with the constraint `|U_i - U_{i+1}| ≤ X` gives a greedy check: new lower bound is `max(L_i, prev_lo - X)`, new upper bound is `min(R_i, prev_hi + X)`. Feasibility holds if the final interval is non‑empty. Because feasibility is monotone, binary search finds the maximum H; the minimal total cost is `sum(S_i) - N·H`. Complexity O(N log maxS) and O(1) extra memory.
