
## ideation
Core difficulty: We must choose final upper lengths $u_i \le U_i$ and lower lengths $d_i \le D_i$ with $u_i + d_i = H$ (common sum), $|u_i - u_{i+1}| \le X$, minimizing cost $= \sum(U_i - u_i) + \sum(D_i - d_i) = \sum(U_i + D_i) - N H$. Since the first term is constant, minimizing cost = maximizing $H$, subject to feasibility.

For fixed $H$: each $u_i$ must lie in $[L_i, R_i] = [\max(0, H - D_i), U_i]$ (also need $d_i = H - u_i \ge 0$, i.e. $u_i \le H$, but $H \le \min(U_i+D_i)$ and $u_i \le U_i$... actually need $u_i \le H$ too if $D_i$ could exceed... no: $d_i = H - u_i \le D_i \iff u_i \ge H - D_i$, and $d_i \ge 0 \iff u_i \le H$. So interval is $[\max(0, H-D_i), \min(U_i, H)]$.) Feasibility with Lipschitz constraint $|u_i - u_{i+1}| \le X$ is checkable by interval propagation: forward pass $R_{i+1} = \min(R_{i+1}, R_i + X)$, $L_{i+1} = \max(L_{i+1}, L_i - X)$... standard approach: forward tighten upper bounds ($R'_{i+1} = \min(R_{i+1}, R'_i + X)$), backward tighten ($R''_i = \min(R''_i, R''_{i+1} + X)$), then check exists $u_i \in [L_i, R''_i]$ chain — actually the tightest correct method: iteratively intersect each interval with $[L_{i-1} - X, R_{i-1} + X]$ style constraints. A clean sufficient-and-necessary method: forward pass computing reachable range: reachable set at position $i$ given we start anywhere in $[L_1, R_1]$: $S_1 = [L_1, R_1]$; $S_{i+1} = [L_{i+1}, R_{i+1}] \cap [S_i.lo - X, S_i.hi + X]$. If any $S_i$ empty → infeasible. This forward-only reachability is necessary and sufficient for existence of a sequence (since any reachable endpoint can be extended, and we only need existence of full chain — forward reachable set at $N$ nonempty means some chain exists? Forward reachability computes exactly the set of values $u_i$ can take in some valid prefix; if $S_N \ne \emptyset$, we can backtrack to construct a valid full sequence. Yes, sufficient.)

Monotonicity: If $H$ is feasible, is every $H' < H$ feasible? Intervals shift: as $H$ decreases by 1, $L_i = H - D_i$ decreases by 1 (lower bound drops), upper bound $\min(U_i, H)$ may decrease by 1 where $U_i > H$. Hmm, upper bounds shrinking could break feasibility? If $H$ feasible with values $u_i$, then for $H-1$ use $u_i' = \min(u_i, H-1)$... check: $|u_i' - u_{i+1}'| \le |u_i - u_{i+1}| \le X$ (min with constant is 1-Lipschitz). And $u_i' \le \min(U_i, H-1)$, $u_i' \ge ?$ need $u_i' \ge H-1-D_i$: if $u_i \le H-1$, $u_i' = u_i \ge H - D_i > H-1-D_i$. If $u_i = H$ (i.e. $u_i > H-1$), then $u_i' = H-1 \ge H-1-D_i$. Also $u_i' \ge 0$. So feasibility is monotone downward. Binary search max feasible $H$ in $[0, \min_i(U_i + D_i)]$ works. Answer $= \sum(U_i + D_i) - N \cdot H^*$.

Pitfalls:
- 64-bit overflow (use Python ints — fine).
- Binary search bounds: $H \le \min(U_i + D_i)$; also $H \ge 0$.
- $O(N \log(\text{range}))$ with $N = 2\times10^5$ and range up to $2\times10^9$ → ~31 iterations × $2\times10^5$ = $6.2\times10^6$ ops, fine in Python if written tightly (maybe use lists and local vars).
- Edge: reachable interval intersection formula: $S_{i+1} = [\max(L_{i+1}, lo_i - X), \min(R_{i+1}, hi_i + X)]$, empty if lo > hi.

Alternative approaches: parametric search / direct LP, but binary search + propagation is simplest and provably correct given monotonicity proof above.

## worker: Implement the full Python solution: feasibility ch
- **Reduction**: Final upper lengths $u_i \le U_i$, lower $d_i = H - u_i \le D_i$, $d_i \ge 0$. Cost $= \sum(U_i - u_i) + \sum(D_i - d_i) = \sum(U_i + D_i) - N H$. So minimize cost $\iff$ maximize feasible $H$.
- **Feasibility for fixed $H$**: each $u_i \in [\max(0, H - D_i), \min(U_i, H)]$ with $|u_i - u_{i+1}| \le X$. Forward reachable-set scan: $S_1 = [L_1, R_1]$, $S_{i+1} = [L_{i+1}, R_{i+1}] \cap [S_i.lo - X, S_i.hi + X]$; infeasible iff some $S_i$ is empty. Nonempty $S_N$ lets us backtrack a valid chain, so it's necessary and sufficient. $O(N)$.
- **Monotonicity**: If $H$ is feasible with values $u_i$, then $H-1$ is feasible via $u_i' = \min(u_i, H-1)$ (min with a constant is 1-Lipschitz, bounds check out). Hence binary search over $H \in [0, \min_i(U_i + D_i)]$ is valid.
- **Complexity**: $O(N \log(2 \times 10^9)) \approx 6 \times 10^6$ simple operations — fine in Python.
- **Sample checks**:
  - Sample 1: sums = [4,5,14,8], total=31, min=4. $H=4$: intervals $u \in [\max(0,4-D_i), \min(U_i,4)]$ = [3,3],[3,4],[0,4],[0,2]; with $X=3$: reachable [3,3]→[3,4]∩[0,6]=[3,4]→[0,4]∩[0,7]=[0,4]→[0,2]∩[0,7]=[0,2] ✓. Cost $=31-16=15$ ✓.
  - Sample 2: all sums 6, $H=6$ feasible ($u_i=3$), cost 0 ✓.
  - Sample 3: sums = [$2\times10^9$ ×3, 2], min=2, $H=2$: intervals for first three: $[\max(0, 2-10^9), \min(10^9,2)] = [0,2]$; last: $[1,1]$. With $X=1$: reachable [0,2]→[0,2]→[0,2]→[1,1]∩[0,3]=[1,1] ✓. Cost $= 6\times10^9 + 2 - 4\cdot2 = 5999999994$ ✓.
