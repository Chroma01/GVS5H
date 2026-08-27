- **Particle model:** Label the initial pieces from left to right, with positions \(a_1\le\cdots\le a_m\). Their order is preserved forever. Assign them to final positions \(y_1\le\cdots\le y_m\), where every position marked 1 in \(B\) appears at least once and no position marked 0 appears.
- **Reachability criterion:** An order-preserving assignment is reachable in \(K=\max_j|y_j-a_j|\) operations exactly when the displacements \(d_j=y_j-a_j\) are nonincreasing. This condition is sufficient; no additional constraint is needed.
- **Construction idea:** Induct on \(K\). At one operation, choose a target square so that particles needing the extreme displacement \(+K\) move right and particles needing \(-K\) move left. Because displacements are nonincreasing, these particles form a prefix and suffix. At the boundary, choose the target at a particle position when a zero step is required. Subtracting the resulting \(-1,0,+1\) step vector leaves a nonincreasing displacement sequence bounded by \(K-1\). Repeating gives a construction in \(K\) operations. The order condition on final positions guarantees that the required boundary target positions can be chosen even when particles collide.
- **Block formulation:** Let target occupied positions be \(q_1<\cdots<q_r\). Pieces assigned to each \(q_j\) form a nonempty consecutive block. For a fixed \(K\), every piece in block \(j\) must lie in \([q_j-K,q_j+K]\).
- **Boundary condition:** If block \(j\) ends at source index \(e\), then nonincreasing displacement requires
  \[
  q_j-p_e\ge q_{j+1}-p_{e+1},
  \]
  equivalently \(p_{e+1}-p_e\ge q_{j+1}-q_j\).
- **Feasibility scan:** For each target, compute the allowable source-index interval \([L_j,R_j]\). The possible ending indices of each processed block form an interval. To transition across a boundary, scan from the smallest reachable endpoint until finding a source gap large enough. The scan pointer only moves right over the entire feasibility check, so one check is \(O(N)\).
- **Optimization:** Feasibility is monotone in \(K\), so binary search \(K\) from 0 through \(N\). Total complexity is \(O(N\log N)\) over all test cases, with \(O(N)\) memory.
