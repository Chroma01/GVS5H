
## ideation
Core difficulty: only grinding down means final upper/lower lengths \(u_i,d_i\) must satisfy \(0\le u_i\le U_i\), \(0\le d_i\le D_i\), \(u_i+d_i=H\), and adjacent uppers differ by at most \(X\). For a fixed common sum \(H\), the split at each position is forced into an interval:  
\(u_i\in[\max(0,H-D_i),\min(U_i,H)]\). If feasible, total removed cost is always \(\sum(U_i+D_i)-NH\), independent of how the split is chosen, so the optimization reduces to finding the maximum feasible integer \(H\).

Feasibility for fixed \(H\) is a 1D interval reachability problem on a path: maintain reachable interval for \(u_i\), expand by \(\pm X\), intersect with position \(i+1\)’s allowed box; feasible iff never empty and initial box nonempty. Key monotonicity: if some sequence works for \(H\), then \(u'_i=\min(u_i,h)\) works for any \(h<H\), preserving box constraints and adjacency, so binary search on \(H\) is valid.

Pitfalls: don’t DP over length values (up to \(1e9\)); don’t minimize cost by choosing splits for fixed \(H\) because cost is fixed; watch integer interval endpoints/off-by-one; infeasible if \(H>\min_i(U_i+D_i)\) or any box empty; use 64-bit/Python big ints for answer; prove/check monotonicity carefully; lower bound for \(H\) can be \(0\); complexity target \(O(N\log(1e9))\).

## worker: Implement the complete Python solution: fast stdin
- For a fixed common sum \(H\), the final upper length at position \(i\) must lie in \([\max(0,H-D_i),\min(U_i,H)]\) (since we can only grind down and lengths stay nonnegative). If any valid split exists, the total cost is \(\sum(U_i+D_i)-NH\) regardless of the split, so we maximize feasible \(H\).
- `feasible(H)` propagates the reachable upper-length interval along the path: intersect each position's allowed box with the previous reachable interval expanded by \(\pm X\). Empty intersection ⇒ infeasible. Runs in \(O(N)\).
- Monotonicity: if a sequence \(u_i\) works for \(H\), then \(u'_i=\min(u_i,h)\) works for any \(h<H\) (boxes and the \(|u'_i-u'_{i+1}|\le X\) condition are preserved), so binary search over \(H\in[0,\min_i(U_i+D_i)]\) is valid.
- Verified against samples 1–3 by hand (15, 0, 5999999994). Complexity \(O(N\log(2\cdot10^9))\approx 31\) feasibility passes; Python big ints handle the 64-bit answer.
