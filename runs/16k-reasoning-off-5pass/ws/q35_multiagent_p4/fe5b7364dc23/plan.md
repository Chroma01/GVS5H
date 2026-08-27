1. Let $S_i$ be the prefix sum $A_1 + \dots + A_i$ (with $S_0 = 0$). The sum of $A_l \dots A_r$ is $S_r - S_{l-1}$.
2. We need to compute $\sum_{0 \leq l < r \leq N} (S_r - S_l)^K$.
3. Expand $(S_r - S_l)^K$ using the binomial theorem: $\sum_{j=0}^K \binom{K}{j} S_r^j (-1)^{K-j} S_l^{K-j}$.
4. Swap the summations: for each $j$, we need $\sum_{0 \leq l < r \leq N} S_r^j S_l^{K-j}$.
5. This can be computed efficiently by iterating $r$ from $1$ to $N$, maintaining a running sum of $S_l^{K-j}$ for all $l < r$. Specifically, let $T_{K-j} = \sum_{l=0}^{r-1} S_l^{K-j}$. Then the contribution for a fixed $r$ and $j$ is $S_r^j \cdot T_{K-j}$.
6. Update the running sums $T_m$ by adding $S_r^m$ after processing $r$. The total complexity will be $O(NK)$, which fits within constraints since $N \leq 2 \cdot 10^5$ and $K \leq 10$.