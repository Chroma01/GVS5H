
## ideation
The core difficulty lies in efficiently minimizing the cost over the possible values of $H$. The cost function for a fixed $H$ involves finding a sequence $U'_i$ that satisfies local bounds $[L_i, R_i]$ and smoothness constraints $|U'_i - U'_{i+1}| \le X$, while minimizing $\sum U'_i$. This subproblem can be solved in $O(N)$ by propagating constraints forward and backward to tighten the bounds, then taking the lower bound of each interval. The overall cost function $f(H)$ is convex with respect to $H$, allowing us to use ternary search over the valid range of $H$. The valid range for $H$ is $[\max(D_i) + 1, \min(U_i + D_i)]$. If this range is empty, no solution exists (though constraints imply one does). The constraints on $N$ ($2 \times 10^5$) and values ($10^9$) require an $O(N \log (\text{range}))$ or similar efficient approach. Ternary search with $O(N)$ evaluation fits this.

Pitfalls:
1.  Integer overflow: Costs and $H$ can be large, so use 64-bit integers.
2.  Invalid $H$: If $L_i > R_i$ for any $i$ during propagation, $H$ is invalid. The ternary search should handle this by returning infinity.
3.  Convexity: The function $f(H)$ is indeed convex because the feasible region for $U'$ expands/contracts linearly with $H$, and the minimum sum of a sequence with linear bounds is a convex function.
4.  Boundary conditions: Ensure $H$ is within $[H_{min}, H_{max}]$.

## worker: Implement the `get_min_sum_U_prime(H, N, X, U, D)`
The problem asks to minimize the total reduction cost to make teeth "fit together well". This involves finding a target sum $H$ and modified lengths $U'_i, D'_i$ such that $U'_i + D'_i = H$, $|U'_i - U'_{i+1}| \le X$, and $U'_i \le U_i, D'_i \le D_i$. The cost is $\sum (U_i - U'_i) + \sum (D_i - D'_i) = \sum (U_i + D_i) - N \cdot H + \sum U'_i$.

For a fixed $H$, the problem reduces to minimizing $\sum U'_i$ subject to:
1. $L_i \le U'_i \le R_i$ where $L_i = \max(1, H - D_i)$ and $R_i = \min(U_i, H - 1)$.
2. $|U'_i - U'_{i+1}| \le X$.

This subproblem is solved by propagating constraints forward and backward to tighten the feasible intervals for each $U'_i$. The minimum sum is then the sum of the lower bounds of these tightened intervals.

The overall cost function $f(H)$ is convex with respect to $H$. We determine the valid range for $H$ as $[2, \min(U_i + D_i)]$ and use ternary search to find the $H$ that minimizes the cost. The constraints $N \le 2 \times 10^5$ and large values of $U_i, D_i$ necessitate an efficient $O(N \log (\text{range}))$ approach, which ternary search provides.
