
## ideation
The problem requires calculating the sum of the $K$-th power of all subarray sums modulo 998244353.
- **Constraints:** $N \le 2 \times 10^5$, $K \le 10$.
- **Naive Approach:** Iterating over all pairs $(l, r)$ takes $O(N^2)$, which is too slow ($4 \times 10^{10}$ operations).
- **Key Insight:** Let $S_i$ be the prefix sum of $A$ up to index $i$ (with $S_0 = 0$). The sum of subarray $A[l \dots r]$ is $S_r - S_{l-1}$.
- **Transformation:** The total sum becomes $\sum_{r=1}^N \sum_{j=0}^{r-1} (S_r - S_j)^K$.
- **Binomial Theorem:** Expand $(S_r - S_j)^K = \sum_{i=0}^K \binom{K}{i} S_r^i (-S_j)^{K-i}$.
- **Separation of Variables:** The expression can be rewritten as $\sum_{i=0}^K \binom{K}{i} (-1)^{K-i} S_r^i \left( \sum_{j=0}^{r-1} S_j^{K-i} \right)$.
- **Efficient Calculation:** Let `sum_pow[m]` store $\sum_{j=0}^{r-1} S_j^m$. We can maintain this array as we iterate $r$ from 1 to $N$.
- **Complexity:** For each $r$, we iterate $i$ from 0 to $K$. Total time complexity is $O(N \cdot K)$. With $N=2 \cdot 10^5$ and $K=10$, this is approximately $2 \cdot 10^6$ operations, well within time limits.
- **Modulo Arithmetic:** All operations must be performed modulo 998244353. Note that $(-1)^{K-i}$ needs to be handled correctly (e.g., $MOD - 1$ for odd powers).
- **Initialization:** Since the inner sum ranges $j=0 \dots r-1$, initially for $r=1$, we need $S_0$. $S_0=0$. So `sum_pow` should be initialized with $S_0^m$. Specifically, `sum_pow[0] = 1` (since $0^0=1$) and `sum_pow[m] = 0` for $m > 0$.
