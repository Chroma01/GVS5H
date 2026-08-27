1.  **Analyze Conditions**: The teeth fit if $U_i + D_i = H$ for all $i$, and $|U_i - U_{i+1}| \le X$. Since we can only reduce tooth lengths, let the final lengths be $U'_i \le U_i$ and $D'_i \le D_i$. The condition $U'_i + D'_i = H$ implies $D'_i = H - U'_i$. Since $D'_i \ge 1$, we must have $U'_i \le H - 1$. Also $U'_i \ge 1$. Thus, for a fixed $H$, each $U'_i$ is constrained by $1 \le U'_i \le \min(U_i, H-1)$. Let $M_i(H) = \min(U_i, H-1)$.
2.  **Formulate Cost**: The cost for a fixed $H$ is $\sum_{i=1}^N (U_i - U'_i) + (D_i - D'_i) = \sum_{i=1}^N (U_i + D_i - H)$. Note that $U_i + D_i - H$ is constant for fixed $H$ and $i$. However, we must ensure there exists a valid sequence $U'_1, \dots, U'_N$ such that $1 \le U'_i \le M_i(H)$ and $|U'_i - U'_{i+1}| \le X$. If such a sequence exists, the cost is $\sum (U_i + D_i) - N \cdot H$. To minimize cost, we want to maximize $H$ subject to the existence of such a sequence? No, wait. The cost decreases as $H$ increases. So we want the largest possible $H$ for which a valid configuration exists?
    *   Correction: The cost is $\sum (U_i - U'_i + D_i - D'_i)$. Since $U'_i + D'_i = H$, the term for index $i$ is $U_i + D_i - H$. Total cost = $\sum (U_i + D_i) - N \cdot H$.
    *   Yes, minimizing cost is equivalent to maximizing $H$.
3.  **Feasibility Check for Fixed H**: For a fixed $H$, we need to check if there exists a sequence $U'_i$ such that:
    *   $L_i \le U'_i \le R_i$ where $L_i = 1, R_i = M_i(H)$.
    *   $|U'_i - U'_{i+1}| \le X$.
    This is a classic problem. We can maintain the feasible interval for $U'_i$ iteratively. Let $[low_i, high_i]$ be the range of valid values for $U'_i$ given the constraints from $1 \dots i$.
    *   $low_1 = 1, high_1 = R_1$.
    *   $low_{i} = \max(1, low_{i-1} - X)$, $high_{i} = \min(R_i, high_{i-1} + X)$.
    *   If at any point $low_i > high_i$, then $H$ is not feasible.
4.  **Binary Search on H**: The possible values for $H$ range from $2$ (since min tooth is 1) to $2 \cdot 10^9$. We can binary search for the maximum feasible $H$.
5.  **Calculate Answer**: Once the maximum feasible $H$ is found, compute the total cost.