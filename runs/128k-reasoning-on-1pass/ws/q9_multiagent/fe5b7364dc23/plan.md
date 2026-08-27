The problem asks to compute the sum of the K-th power of all subarray sums.
Let $S_{l,r}$ be the sum of $A_l \dots A_r$. We want $\sum_{1 \le l \le r \le N} (S_{l,r})^K$.
We can rewrite $S_{l,r}$ as $S_r - S_{l-1}$ where $S_x$ is the prefix sum of $A$ up to $x$ ($S_0=0$).
The expression becomes $\sum_{r=1}^N \sum_{j=0}^{r-1} (S_r - S_j)^K$.
Using the binomial theorem, $(S_r - S_j)^K = \sum_{i=0}^K \binom{K}{i} S_r^i (-S_j)^{K-i}$.
Substituting this back, the total sum is $\sum_{i=0}^K \binom{K}{i} (-1)^{K-i} \sum_{r=1}^N S_r^i \left( \sum_{j=0}^{r-1} S_j^{K-i} \right)$.
Let $P_m(x) = \sum_{k=0}^x S_k^m$. The inner term is $P_{K-i}(r-1)$.
We can maintain $P_m(x)$ as we iterate $r$ from 1 to $N$.
Since $K$ is small ($K \le 10$), we can compute powers of $S_r$ and update $P_m$ values in $O(K)$ per step.
The total time complexity will be $O(NK)$, which fits within the time limits.