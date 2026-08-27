1. Let $S_i$ be the prefix sum $A_1 + \dots + A_i$ (with $S_0 = 0$). The sum of $A[l..r]$ is $S_r - S_{l-1}$.
2. We need to compute $\sum_{0 \leq i < j \leq N} (S_j - S_i)^K$.
3. Expand $(S_j - S_i)^K$ using the binomial theorem: $\sum_{m=0}^K \binom{K}{m} S_j^{K-m} (-S_i)^m$.
4. Swap the summations: for each $m$, we need $\sum_{0 \leq i < j \leq N} S_j^{K-m} (-1)^m S_i^m$.
5. This can be computed by iterating $j$ from $1$ to $N$, and maintaining a running sum of $S_i^m$ for all $i < j$. Specifically, for each $m$, keep a cumulative sum $C_m = \sum_{i=0}^{j-1} S_i^m$.
6. For each $j$, add $\sum_{m=0}^K \binom{K}{m} (-1)^m S_j^{K-m} C_m$ to the total answer, then update all $C_m$ by adding $S_j^m$.