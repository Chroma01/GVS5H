
## ideation
The core difficulty lies in efficiently determining the maximum valid sum $H$ such that there exists a sequence of reduced upper tooth lengths $U'_i$ satisfying:
1. $L_i(H) \le U'_i \le R_i(H)$ where $L_i(H) = \max(0, H - D_i)$ and $R_i(H) = \min(U_i, H)$.
2. $|U'_i - U'_{i+1}| \le X$ for all $i$.

The cost function is $\sum (U_i + D_i) - N \cdot H$. Since $\sum (U_i + D_i)$ is constant, minimizing cost is equivalent to maximizing $H$.

The constraints on $U'_i$ can be propagated iteratively. Let $[a_i, b_i]$ be the feasible interval for $U'_i$ considering constraints from $1$ to $i$.
- Base case: $a_1 = L_1(H), b_1 = R_1(H)$.
- Recursive step: $a_i = \max(L_i(H), a_{i-1} - X)$, $b_i = \min(R_i(H), b_{i-1} + X)$.
If at any point $a_i > b_i$, then $H$ is invalid.

The function "is_valid(H)" is monotonic in a specific way: if $H$ is valid, any $H' < H$ might not necessarily be valid due to the $L_i, R_i$ bounds shifting, but generally, smaller $H$ allows more flexibility in $U'_i$ being closer to 0. However, note that $L_i(H)$ increases with $H$ and $R_i(H)$ increases with $H$. The condition $a_i \le b_i$ becomes harder to satisfy as $H$ increases because the intervals $[L_i, R_i]$ shift right and potentially shrink or move out of reach of the propagation constraints. Specifically, if $H$ is too large, $R_i(H)$ might be small relative to required $U'_i$ from previous steps, or $L_i(H)$ might be too large relative to allowed $U'_i$ from previous steps. Thus, we can binary search for the maximum valid $H$.

The range for $H$ is $[0, \max(U_i) + \max(D_i)]$. Given constraints, max $H \approx 2 \cdot 10^9$. Binary search takes $O(\log(10^9))$ steps. Each validation step takes $O(N)$. Total time $O(N \log(\max(H)))$, which fits within limits for $N=2 \cdot 10^5$.

Pitfalls:
- Integer overflow: Costs and sums can exceed $2^{31}-1$, so use 64-bit integers.
- Edge cases: $N$ small, $X$ very large or small.
- The binary search range lower bound: $H$ must be at least $\max(L_i(H))$? No, $H$ can be small. Lower bound 0 is safe.
- The binary search upper bound: $\max(U_i) + \max(D_i)$ is a safe upper bound because $U'_i \le U_i$ and $D'_i \le D_i$ implies $H = U'_i + D'_i \le U_i + D_i$.

## worker: Implement the `is_valid(H)` function that checks i
The problem asks to minimize the total reduction in tooth lengths such that the teeth "fit together well". This means:
1. $U'_i + D'_i = H$ for all $i$, for some integer $H$.
2. $|U'_i - U'_{i+1}| \leq X$ for all $i$.
3. $0 \leq U'_i \leq U_i$ and $0 \leq D'_i \leq D_i$.

From condition 1, $D'_i = H - U'_i$. The cost is $\sum (U_i - U'_i) + (D_i - D'_i) = \sum (U_i + D_i) - N \cdot H$. Since $\sum (U_i + D_i)$ is constant, minimizing cost is equivalent to maximizing $H$.

For a fixed $H$, the constraints on $U'_i$ are:
- $0 \leq U'_i \leq U_i$
- $0 \leq H - U'_i \leq D_i \implies H - D_i \leq U'_i \leq H$
- $|U'_i - U'_{i+1}| \leq X$

Combining the first two, $U'_i$ must lie in $[L_i, R_i]$ where $L_i = \max(0, H - D_i)$ and $R_i = \min(U_i, H)$. If $L_i > R_i$ for any $i$, $H$ is invalid.

To check if a valid sequence $U'_i$ exists, we can propagate feasible intervals. Let $[a_i, b_i]$ be the feasible range for $U'_i$ considering constraints from indices $1$ to $i$.
- $a_1 = L_1, b_1 = R_1$.
- For $i > 1$, $U'_i$ must be in $[L_i, R_i]$ and also within $X$ of some value in $[a_{i-1}, b_{i-1}]$. So the feasible range from the previous step is $[a_{i-1} - X, b_{i-1} + X]$. Intersecting with $[L_i, R_i]$ gives $[a_i, b_i]$.
- If at any point $a_i > b_i$, then $H$ is invalid.

The function `is_valid(H)` implements this check in $O(N)$ time. Since larger $H$ makes the constraints tighter (intervals shift right and potentially shrink), the validity is monotonic in the sense that if $H$ is valid, smaller $H$ are more likely to be valid. We binary search for the maximum valid $H$ in the range $[0, \max(U) + \max(D)]$. The total complexity is $O(N \log(\max(H)))$, which is efficient enough for $N=2 \cdot 10^5$.
