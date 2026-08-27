
## ideation
The core difficulty lies in efficiently determining the valid range of $H$ such that there exists a sequence $U'_i$ satisfying the constraints. The cost function is linear in $H$ ($Cost = \sum(U_i+D_i) - N \cdot H$), so minimizing cost is equivalent to maximizing $H$. The constraints on $U'_i$ for a fixed $H$ are:
1. $L_i(H) \le U'_i \le R_i(H)$ where $L_i(H) = \max(1, H - D_i)$ and $R_i(H) = \min(U_i, H - 1)$.
2. $|U'_i - U'_{i+1}| \le X$.

We can check if a specific $H$ is valid in $O(N)$ by propagating the feasible interval $[a_i, b_i]$ for each $U'_i$. The interval updates as:
$a_i = \max(L_i(H), a_{i-1} - X)$
$b_i = \min(R_i(H), b_{i-1} + X)$
If $a_i > b_i$ at any step, $H$ is invalid.

The set of valid $H$ values forms an interval (possibly empty). Since the cost decreases as $H$ increases, we want the largest valid $H$. We can binary search for the maximum valid $H$. The lower bound for $H$ is 2 (since $U'_i, D'_i \ge 1 \implies H \ge 2$) and the upper bound is $\max(U_i + D_i)$.

Pitfalls:
- The range of $H$ is large ($2 \cdot 10^9$), so $O(N \log (\max H))$ is acceptable.
- Need to handle the case where no valid $H$ exists (though constraints say $U_i, D_i \ge 1$, so $H=U_1+D_1$ might not be valid due to adjacent constraints, but a valid $H$ always exists if we reduce enough? Actually, if we reduce everything to 1, $H=2$ is always valid if $X \ge 0$. So valid $H$ always exists).
- Use 64-bit integers for sums and costs.

## worker: Implement a function `is_valid(H, N, X, U, D)` tha
The problem asks to minimize the total reduction in tooth lengths such that $U'_i + D'_i = H$ for all $i$ and $|U'_i - U'_{i+1}| \le X$. The cost is $\sum (U_i + D_i) - N \cdot H$. Thus, minimizing cost is equivalent to maximizing $H$.

For a fixed $H$, we need to check if there exists a sequence $U'_i$ such that:
1. $L_i(H) \le U'_i \le R_i(H)$ where $L_i(H) = \max(1, H - D_i)$ and $R_i(H) = \min(U_i, H - 1)$.
2. $|U'_i - U'_{i+1}| \le X$.

We can check this in $O(N)$ by maintaining the feasible interval $[a_i, b_i]$ for each $U'_i$. Starting with $[a_0, b_0] = [L_0, R_0]$, we update for each subsequent $i$:
$a_i = \max(L_i, a_{i-1} - X)$
$b_i = \min(R_i, b_{i-1} + X)$
If $a_i > b_i$ at any point, $H$ is invalid.

The set of valid $H$ values forms an interval. We binary search for the largest valid $H$ in the range $[2, \max(U_i + D_i)]$. The check function runs in $O(N)$, and the binary search takes $O(\log(\max H))$ steps, leading to an overall time complexity of $O(N \log (\max H))$, which is efficient enough for $N \le 2 \times 10^5$.
