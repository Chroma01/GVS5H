- **Fixed common sum:** For a chosen integer \(H\), let \(u'_i\) be the final upper-tooth length. Then the final lower length is \(d'_i=H-u'_i\).
- **Per-tooth interval:** Grinding only decreases lengths and lengths must remain nonnegative, so
  \[
  \max(0,H-D_i)\le u'_i\le \min(U_i,H).
  \]
  The lower bound ensures \(d'_i\le D_i\), and the upper bound ensures both \(u'_i\le U_i\) and \(d'_i\ge0\).
- **Interval propagation:** Maintain the interval of all reachable values for the current upper tooth. If the previous reachable interval is \([L,R]\), values differing by at most \(X\) can reach \([L-X,R+X]\). Intersect this with the current tooth’s allowed interval. The reachable set remains an interval; if it becomes empty, \(H\) is infeasible.
- **Monotonicity:** If \(H\) is feasible and \(H'\le H\), take a feasible upper sequence \(u'_i\) and replace each value by \(\min(u'_i,H')\). Clipping preserves the adjacent-difference bound because \(z\mapsto\min(z,H')\) is non-expansive. The new upper values remain within original bounds, and \(H'-\min(u'_i,H')\le H-u'_i\le D_i\). Thus every smaller \(H'\) is feasible.
- **Binary search:** \(H=0\) is always feasible. Also \(H\le\min_i(U_i+D_i)\). Binary search the largest feasible \(H\).
- **Cost:** For fixed \(H\), total grinding is
  \[
  \sum_i(U_i+D_i)-NH,
  \]
  so maximizing \(H\) minimizes cost.
- **Complexity:** Each feasibility check is \(O(N)\), and binary search takes \(O(\log \min_i(U_i+D_i))\), giving \(O(N\log V)\) time and \(O(N)\) memory.
