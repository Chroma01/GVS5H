
## ideation
The core difficulty lies in efficiently determining the maximum possible constant sum $H$ such that a valid sequence of upper teeth lengths $U'$ exists. The constraints are:
1. $U'_i + D'_i = H$ with $U'_i, D'_i \ge 1 \implies 1 \le U'_i \le H-1$.
2. We can only reduce tooth lengths, so $U'_i \le U_i$.
3. Adjacent upper teeth must satisfy $|U'_i - U'_{i+1}| \le X$.

Combining 1 and 2, each $U'_i$ is bounded by $[1, \min(U_i, H-1)]$.
Condition 3 implies that the feasible range for $U'_i$ depends on the feasible range of $U'_{i-1}$. Specifically, if $U'_{i-1} \in [L_{i-1}, R_{i-1}]$, then $U'_i$ must be in $[L_{i-1}-X, R_{i-1}+X]$. Intersecting this with the absolute bounds $[1, \min(U_i, H-1)]$ gives the new feasible range $[L_i, R_i]$. If at any point $L_i > R_i$, the chosen $H$ is invalid.

Since the feasibility is monotonic with respect to $H$ (if $H$ works, any $H' < H$ might not necessarily work due to the $U'_i \le H'-1$ constraint tightening, but actually, let's re-evaluate monotonicity).
Wait, if $H$ increases, the upper bound $H-1$ increases, which relaxes the constraint $U'_i \le H-1$. However, the cost function is $\sum (U_i+D_i) - N \cdot H$. To minimize cost, we want to maximize $H$.
Is the property "feasible" monotonic?
If a sequence $U'$ exists for $H$, does it exist for $H+1$?
For $H+1$, the bounds are $[1, \min(U_i, H)]$. Since $\min(U_i, H) \ge \min(U_i, H-1)$, the feasible intervals are larger or equal. Thus, if $H$ is feasible, $H+1$ is also feasible?
Let's check. The condition is existence of *some* sequence. If we have a valid sequence for $H$, say $U'$, then $U'_i \le H-1 < H$. So $U'_i \le \min(U_i, H)$ is still satisfied. The difference constraints are unchanged. So yes, if $H$ is feasible, any $H' > H$ is also feasible (provided $H'$ doesn't exceed $\min(U_i+D_i)$).
Actually, the maximum possible $H$ is bounded by $\min_i (U_i + D_i)$. Let $H_{max} = \min_i (U_i + D_i)$.
We want the largest $H \in [2, H_{max}]$ such that the feasibility check passes.
Since feasibility is monotonic (if $H$ works, $H+1$ works), we can binary search for the maximum feasible $H$.

Algorithm:
1. Calculate $S_i = U_i + D_i$. Let $H_{limit} = \min_i S_i$.
2. Binary search for $H$ in range $[2, H_{limit}]$.
3. For a given $H$, run the linear scan to check feasibility:
   - Maintain current feasible interval $[L, R]$.
   - Initialize $L=1, R=\min(U_1, H-1)$.
   - For $i=2$ to $N$:
     - Expand previous interval: $L_{new} = L - X, R_{new} = R + X$.
     - Clip to absolute bounds: $L_{new} = \max(1, L_{new}), R_{new} = \min(U_i, H-1)$.
     - If $L_{new} > R_{new}$, return False.
     - Update $L=L_{new}, R=R_{new}$.
   - If loop completes, return True.
4. The answer is $\sum S_i - N \cdot H_{best}$.

Pitfalls:
- Integer overflow: Sum of $S_i$ can exceed $2^{31}-1$. Use 64-bit integers.
- Edge cases: $N=2$, large $X$, etc. The logic holds.
- Binary search range: Lower bound 2, upper bound $H_{limit}$.

## worker: (None)
The problem asks to minimize the cost of grinding teeth such that the new lengths $U'_i, D'_i$ satisfy $U'_i + D'_i = H$ for some constant $H$, and $|U'_i - U'_{i+1}| \le X$. The cost is $\sum (U_i - U'_i) + \sum (D_i - D'_i) = \sum (U_i + D_i) - \sum (U'_i + D'_i) = \sum (U_i + D_i) - N \cdot H$. To minimize cost, we must maximize $H$.

The constraints on $U'_i$ are:
1. $1 \le U'_i \le H - 1$ (since $D'_i \ge 1$).
2. $U'_i \le U_i$ (since we can only grind teeth).
3. $|U'_i - U'_{i+1}| \le X$.

Combining 1 and 2, we have $1 \le U'_i \le \min(U_i, H-1)$.
Condition 3 implies that the feasible range for $U'_i$ is constrained by the feasible range of $U'_{i-1}$. Specifically, if $U'_{i-1} \in [L_{i-1}, R_{i-1}]$, then $U'_i$ must be in $[L_{i-1}-X, R_{i-1}+X]$. Intersecting this with the absolute bounds $[1, \min(U_i, H-1)]$ gives the new feasible range $[L_i, R_i]$. If at any point $L_i > R_i$, the chosen $H$ is invalid.

The feasibility of $H$ is monotonic: if a valid sequence exists for $H$, it also exists for any $H' > H$ (up to the limit imposed by $U_i+D_i$) because the upper bound $H-1$ increases, relaxing the constraints. Thus, we can binary search for the maximum feasible $H$ in the range $[2, \min_i(U_i+D_i)]$.

The algorithm runs in $O(N \log (\min(U_i+D_i)))$ time, which is efficient enough for $N \le 2 \times 10^5$ and values up to $10^9$.
