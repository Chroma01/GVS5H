
## ideation
**Restating the mechanics.** Operating box $i$ moves *all* red balls at $i$ to $P_i$ and *all* blue balls at $i$ to $Q_i$ simultaneously. So a red ball only ever travels along the $P$-cycle it starts on, and a blue ball only along its $Q$-cycle. A ball at $v$ advances one step exactly when its *current* box is operated.

**Feasibility.** Let $d_P[v]$ = number of steps $k$ with $P^k(v)=X$ (defined only on the $P$-cycle containing $X$; $d_P[X]=0$), and $d_Q$ analogously. Then:
- If some $i$ with $A_i=1$ is not on $X$'s $P$-cycle → `-1`.
- If some $i$ with $B_i=1$ is not on $X$'s $Q$-cycle → `-1`.
(Balls already at $X$ have distance 0 and need nothing.)

**Reduction to Shortest Common Supersequence.** Let $D_r=\max\{d_P[i] : A_i=1\}$ (0 if none) and $D_b=\max\{d_Q[i]:B_i=1\}$. Define
- Rchain = nodes with $d_P = D_r, D_r-1,\dots,1$ (in that order), length $D_r$;
- Bchain = nodes with $d_Q = D_b,\dots,1$, length $D_b$.

*Necessity:* the deepest red ball must be moved $D_r$ times through exactly those nodes in that order, so any valid operation sequence contains Rchain as a subsequence (same for Bchain). This lower bound holds even for sequences that operate $X$ (a ball leaving $X$ just has to come back, still passing through the whole chain), which justifies "never operate $X$" without extra argument.

*Sufficiency (key lemma):* if the operation word contains Rchain as a subsequence at times $t_{D_r}<\dots<t_1$, then any red ball starting at distance $d\le D_r$ ends at $X$. Induction: after time $t_k$ the ball's distance is $\le k-1$ — extra/early operations only push a ball *forward* along the same chain, never hurt, and it can never overshoot $X$ because $X$ is never operated. Same for blue independently. Hence *any* common supersequence of Rchain and Bchain works.

Therefore answer $=D_r+D_b-\mathrm{LCS}(\text{Rchain},\text{Bchain})$. Both chains consist of distinct elements, so LCS = longest strictly increasing subsequence of (positions in Bchain) taken over the common nodes read in Rchain order → $O(N\log N)$ with `bisect`.

**Verification on samples.** S1: $D_r=3$ (chain [2,1,4]), $D_b=2$ (chain [5,1]), common {1}, LCS=1 → 4 ✓. S2: 0+0-0 = 0 ✓. S3: red at box 1 not on $X$'s cycle (P is identity) → -1 ✓. S4: Rchain [7,3,9], Bchain [5,6,3,9,8,2,4], common {3,9} in same relative order → 3+7-2 = 8 ✓.

**Pitfalls.**
- Computing $d_P$ must walk *backwards* from $X$: use `invP[P[i]] = i`, start `cur = X, d = 0`, repeatedly `cur = invP[cur]; d += 1` until returning to $X$. Don't accidentally overwrite $d_P[X]=0$ with the cycle length.
- Nodes off $X$'s cycle need a sentinel (e.g. -1/INF); only boxes actually holding a ball make it infeasible.
- $A_X$ / $B_X$ = 1 is fine (distance 0, no contribution to $D_r$/$D_b$).
- Chains contain only distances $\ge 1$, so $X$ is never in a chain — consistent with "never operate $X$".
- $D_r$ or $D_b$ may be 0 (all balls already at $X$ or no balls) → answer is just the other; LCS = 0.
- 1- vs 0-indexing; fast IO (`sys.stdin.buffer.read().split()`); avoid recursion; $N\le 2\cdot10^5$ so O(N log N) Python is fine.
- LIS must be **strictly** increasing (`bisect_left`) since Bchain positions are distinct and order must be preserved strictly.

## worker: *Implement the full solution in one Python file** 
Implemented exactly per the plan:

- Fast IO via `sys.stdin.buffer.read().split()`.
- Built `invP`/`invQ` (`invP[P[i]] = i`), then walked backward from `X` to fill `distP`/`distQ` (only on X's cycle; `dist[X]=0`, off-cycle stays `-1`) plus `nodeAtDistP[d]` / `nodeAtDistQ[d]`. The walk stops when returning to `X`, so `dist[X]=0` is never overwritten by the cycle length.
- Infeasibility: any box with `A_i==1` and `distP[i]<0`, or `B_i==1` and `distQ[i]<0` → print `-1`. Balls already at X have distance 0 and contribute nothing.
- `Dr` = max `distP` over red balls, `Db` = max `distQ` over blue balls (0 if none / all at X). If both are 0, answer 0.
- Rchain = `nodeAtDistP[Dr], …, nodeAtDistP[1]`; `posB[v] = Db - distQ[v]` for v with `1 ≤ distQ[v] ≤ Db` (built by iterating Bchain directly, so no off-cycle/out-of-range issues), else `-1`.
- LCS of the two distinct-element chains = strictly increasing LIS of `posB` values read in Rchain order (`bisect_left`), O(N log N).
- Answer `Dr + Db - L`.

Hand-checks: S1 → 3+2−1=4; S2 → 0; S3 → red at box 1 off X's P-cycle → −1; S4 → 3+7−2=8. No recursion; all loops are O(N) or O(N log N).
