1. Let $S_i$ be the prefix sum $A_1 + \dots + A_i$ (with $S_0 = 0$). The sum of $A[l..r]$ is $S_r - S_{l-1}$.
2. We need to compute $\sum_{1 \le l \le r \le N} (S_r - S_{l-1})^K$. Let $j = l-1$, so $0 \le j < r \le N$. The sum becomes $\sum_{0 \le j < r \le N} (S_r - S_j)^K$.
3. Expand $(S_r - S_j)^K$ using the binomial theorem: $\sum_{k=0}^K \binom{K}{k} S_r^{K-k} (-S_j)^k$.
4. Swap the summations: $\sum_{k=0}^K \binom{K}{k} (-1)^k \left( \sum_{0 \le j < r \le N} S_r^{K-k} S_j^k \right)$.
5. For each $k$, the inner sum is $\sum_{r=1}^N S_r^{K-k} \left( \sum_{j=0}^{r-1} S_j^k \right)$. We can compute prefix sums of $S_j^k$ as we iterate $r$ from 1 to $N$.
6. Compute the result modulo 998244353.