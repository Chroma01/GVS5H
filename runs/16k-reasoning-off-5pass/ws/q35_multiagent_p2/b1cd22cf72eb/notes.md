
## ideation
The core difficulty lies in efficiently determining the maximum possible sum $H$ such that there exists a valid sequence of upper tooth lengths $U'_i$ satisfying:
1. $1 \le U'_i \le \min(U_i, H-1)$
2. $|U'_i - U'_{i+1}| \le X$

The cost function is $\sum (U_i + D_i) - N \cdot H$. Since $\sum (U_i + D_i)$ is constant, minimizing cost is equivalent to maximizing $H$.

We can use binary search on $H$. For a fixed $H$, we check feasibility by maintaining the feasible interval $[L_i, R_i]$ for each $U'_i$ iteratively:
- Initialize $[L_1, R_1] = [1, \min(U_1, H-1)]$.
- For $i > 1$, the feasible interval for $U'_i$ is constrained by:
  - The upper bound $M_i(H) = \min(U_i, H-1)$.
  - The previous interval $[L_{i-1}, R_{i-1}]$ via the difference constraint $|U'_i - U'_{i-1}| \le X$.
  - Specifically, $L_i = \max(1, L_{i-1} - X)$ and $R_i = \min(M_i(H), R_{i-1} + X)$.
- If at any step $L_i > R_i$, then $H$ is not feasible.

The range for binary search is $[2, 2 \cdot 10^9 + 7]$ (since max $U_i, D_i$ is $10^9$, max sum is $2 \cdot 10^9$, and min tooth length is 1, so max $H$ is $10^9 + 10^9 = 2 \cdot 10^9$). Actually, since $U'_i \ge 1$ and $D'_i \ge 1$, $H \ge 2$. The upper bound can be set to $2 \cdot 10^9 + 1$ to be safe.

Pitfalls:
- Integer overflow: Use 64-bit integers for sums and costs.
- Boundary conditions: Ensure $H$ is large enough to allow $U'_i \ge 1$ and $D'_i \ge 1$.
- Efficiency: The feasibility check is $O(N)$, and binary search takes $O(\log(\text{max\_H}))$, so total time is $O(N \log(\text{max\_H}))$, which is acceptable for $N \le 2 \cdot 10^5$.

## worker: (None)
The problem requires finding the minimum cost to make teeth "fit together well". The cost is defined as the total reduction in tooth lengths. The conditions for fitting are:
1. $U_i + D_i = H$ for all $i$.
2. $|U_i - U_{i+1}| \le X$ for all $i$.

Since we can only reduce tooth lengths, let the final lengths be $U'_i \le U_i$ and $D'_i \le D_i$. The condition $U'_i + D'_i = H$ implies $D'_i = H - U'_i$. Since $D'_i \ge 1$, we must have $U'_i \le H - 1$. Also $U'_i \ge 1$. Thus, for a fixed $H$, each $U'_i$ is constrained by $1 \le U'_i \le \min(U_i, H-1)$.

The cost for a fixed $H$ is $\sum_{i=1}^N (U_i - U'_i) + (D_i - D'_i) = \sum_{i=1}^N (U_i + D_i - H) = \sum (U_i + D_i) - N \cdot H$. To minimize cost, we need to maximize $H$.

For a fixed $H$, we check if there exists a valid sequence $U'_i$ satisfying the bounds and the difference constraint. This is done by maintaining the feasible interval $[low_i, high_i]$ for each $U'_i$ iteratively:
- $low_1 = 1, high_1 = \min(U_1, H-1)$.
- $low_i = \max(1, low_{i-1} - X)$, $high_i = \min(\min(U_i, H-1), high_{i-1} + X)$.
- If $low_i > high_i$ at any point, $H$ is not feasible.

We binary search for the maximum feasible $H$ in the range $[2, 2 \cdot 10^9 + 1]$. The feasibility check is $O(N)$, and binary search takes $O(\log(\text{max\_H}))$, leading to an overall complexity of $O(N \log(\text{max\_H}))$, which is efficient enough for $N \le 2 \cdot 10^5$.
