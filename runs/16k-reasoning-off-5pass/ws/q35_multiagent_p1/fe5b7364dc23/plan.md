1. Let $S_i$ be the prefix sum $A_1 + \dots + A_i$ (with $S_0 = 0$). The sum of subarray $A[l..r]$ is $S_r - S_{l-1}$.
2. We need to compute $\sum_{0 \leq l < r \leq N} (S_r - S_l)^K$.
3. Expand $(S_r - S_l)^K$ using the binomial theorem: $\sum_{j=0}^K \binom{K}{j} S_r^j (-S_l)^{K-j}$.
4. Swap the summations: $\sum_{j=0}^K \binom{K}{j} \left( \sum_{0 \leq l < r \leq N} S_r^j (-1)^{K-j} S_l^{K-j} \right)$.
5. For each $j$, the inner sum can be computed by iterating $r$ from $1$ to $N$ and maintaining the sum of $S_l^{K-j}$ for all $l < r$. This allows an $O(NK)$ solution.