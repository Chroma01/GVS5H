
## ideation
The core difficulty lies in efficiently checking if a valid configuration exists for a given target sum $H$. The problem can be transformed into finding the maximum $H$ such that there exists a sequence $U'_i$ satisfying:
1. $L_i(H) \le U'_i \le R_i(H)$, where $L_i(H) = \max(0, H - D_i)$ and $R_i(H) = U_i$.
2. $|U'_i - U'_{i+1}| \le X$.

This is a classic "feasibility of a sequence with bounded differences and interval constraints" problem. We can solve the check for a fixed $H$ in $O(N)$ time using interval propagation:
- Maintain a feasible interval $[min\_val, max\_val]$ for the current $U'_i$.
- Initially, for $i=1$, the feasible interval is $[L_1(H), R_1(H)]$.
- For each subsequent $i$, the previous feasible values $U'_{i-1} \in [min\_val, max\_val]$ allow $U'_i$ to be in $[min\_val - X, max\_val + X]$.
- Intersect this expanded interval with $[L_i(H), R_i(H)]$. If the intersection is empty, $H$ is invalid. Otherwise, update $[min\_val, max\_val]$ to the intersection.

Since the cost function $\sum (U_i + D_i) - N \cdot H$ is linear and decreasing in $H$, we want the largest valid $H$. The function "is_valid(H)" is monotonic: if $H$ is valid, any $H' < H$ is also valid (because the intervals $[L_i(H'), R_i(H')]$ are wider or shifted in a way that preserves feasibility, specifically $L_i(H') \le L_i(H)$ and $R_i(H') = R_i(H)$, so the constraints are looser). Wait, let's verify monotonicity.
$L_i(H) = \max(0, H - D_i)$. As $H$ increases, $L_i(H)$ increases (or stays 0). $R_i(H) = U_i$ is constant. So the interval $[L_i(H), R_i(H)]$ shrinks from the left as $H$ increases.
The propagation step: $[min, max] \to [min-X, max+X] \cap [L_i, R_i]$.
If we decrease $H$, $L_i$ decreases, so the intersection $[L_i, R_i]$ becomes larger (extends to the left). The propagated interval from the left also allows smaller values. It is intuitive that if a sequence exists for $H$, it exists for any $H' < H$. Let's assume monotonicity holds.
Thus, we can binary search for the maximum $H$.
Range for $H$:
Lower bound: 0 (or min possible sum, but 0 is safe since lengths are non-negative).
Upper bound: $\max(U_i) + \max(D_i) \approx 2 \cdot 10^9$.

Pitfalls:
- The binary search range must be large enough. $2 \cdot 10^9$ fits in standard integer types, but calculations involving sums might exceed $2^{31}-1$, so use 64-bit integers.
- The check function must be efficient ($O(N)$).
- Edge case: $N$ up to $2 \cdot 10^5$, so $O(N \log (\text{range}))$ is acceptable.

## worker: Implement the `check(H)` function that verifies if
The problem asks to minimize the total reduction in tooth lengths such that the new upper teeth $U'_i$ and lower teeth $D'_i$ satisfy $U'_i + D'_i = H$ for some constant $H$, and $|U'_i - U'_{i+1}| \le X$. Since we can only reduce lengths, $U'_i \le U_i$ and $D'_i \le D_i$. The condition $U'_i + D'_i = H$ implies $D'_i = H - U'_i$, so $H - U'_i \le D_i \implies U'_i \ge H - D_i$. Also $U'_i \ge 0$. Thus, for a fixed $H$, we need $U'_i \in [\max(0, H - D_i), U_i]$. Additionally, $|U'_i - U'_{i+1}| \le X$.

This is a feasibility problem for a sequence with bounded differences and interval constraints. We can check if a valid sequence exists for a given $H$ in $O(N)$ time by propagating the feasible interval. Let $[min\_val, max\_val]$ be the feasible range for $U'_i$. For $i=1$, it's $[\max(0, H-D_1), U_1]$. For $i > 1$, the feasible range for $U'_i$ based on the previous step is $[min\_val - X, max\_val + X]$. We intersect this with $[\max(0, H-D_i), U_i]$. If the intersection is empty at any point, $H$ is invalid.

The cost function is $\sum (U_i - U'_i) + \sum (D_i - D'_i) = \sum (U_i + D_i) - \sum (U'_i + D'_i) = \sum (U_i + D_i) - N \cdot H$. To minimize cost, we maximize $H$. The feasibility function `is_valid(H)` is monotonic: if $H$ is valid, any $H' < H$ is also valid because the intervals $[\max(0, H'-D_i), U_i]$ are wider (or equal) to $[\max(0, H-D_i), U_i]$ for all $i$, making constraints looser.

We binary search for the maximum $H$ in the range $[0, 2 \cdot 10^9]$. The check function runs in $O(N)$, and the binary search takes $O(\log(2 \cdot 10^9)) \approx 31$ steps. Total complexity is $O(N \log (\text{max\_H}))$, which fits within the time limits for $N \le 2 \cdot 10^5$.
