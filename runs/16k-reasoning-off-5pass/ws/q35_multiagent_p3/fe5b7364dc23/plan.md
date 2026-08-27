1. Expand the term $(\sum_{i=l}^r A_i)^K$ using the multinomial theorem or by expressing it as a sum over products of prefix sums. Specifically, let $S_i$ be the prefix sum $A_1 + \dots + A_i$ with $S_0=0$. Then $\sum_{i=l}^r A_i = S_r - S_{l-1}$.
2. We need to compute $\sum_{1\leq l\leq r\leq N} (S_r - S_{l-1})^K$. Let $j = l-1$, so $0 \leq j < r \leq N$. The sum becomes $\sum_{0\leq j < r \leq N} (S_r - S_j)^K$.
3. Expand $(S_r - S_j)^K$ using the binomial theorem: $\sum_{m=0}^K \binom{K}{m} S_r^m (-1)^{K-m} S_j^{K-m}$.
4. Swap the summations: $\sum_{m=0}^K \binom{K}{m} (-1)^{K-m} \left( \sum_{0\leq j < r \leq N} S_r^m S_j^{K-m} \right)$.
5. For each $m$, the inner sum is $\sum_{r=1}^N S_r^m \left( \sum_{j=0}^{r-1} S_j^{K-m} \right)$. We can compute this in $O(NK)$ time by maintaining prefix sums of powers of $S_i$.
6. Compute all required powers $S_i^p$ for $p=0,\dots,K$, maintain running prefix sums of these powers, and accumulate the answer.