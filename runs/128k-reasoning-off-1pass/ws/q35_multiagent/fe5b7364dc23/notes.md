
## ideation
The core difficulty is efficiently computing the sum of K-th powers of all subarray sums. A naive O(N^2) approach is too slow for N up to 2*10^5. However, since K is small (K <= 10), we can use the binomial expansion of (S_r - S_{l-1})^K. This allows us to separate the terms involving S_r and S_{l-1}. By maintaining prefix sums of powers of prefix sums (i.e., sum of S_i^p for i from 0 to current), we can compute the contribution of each r in O(K) time, leading to an overall O(NK) solution.

Key steps:
1. Compute prefix sums S_0, S_1, ..., S_N where S_0 = 0.
2. For each r from 1 to N, the subarray sum A[l..r] is S_r - S_{l-1} for l from 1 to r.
3. Expand (S_r - S_{l-1})^K using binomial theorem: sum_{j=0}^K binom(K, j) * S_r^j * (-1)^{K-j} * S_{l-1}^{K-j}.
4. Sum over all l from 1 to r: sum_{l=1}^r (S_r - S_{l-1})^K = sum_{j=0}^K binom(K, j) * S_r^j * (-1)^{K-j} * (sum_{l=1}^r S_{l-1}^{K-j}).
5. Maintain an array `sum_powers[p]` which stores sum_{i=0}^{r-1} S_i^p for the current r.
6. For each r, compute the contribution using the formula above, then update `sum_powers` with S_r^p for all p from 0 to K.

Pitfalls:
- Modulo arithmetic must be applied carefully, especially with negative numbers (use (a % MOD + MOD) % MOD).
- Precompute binomial coefficients modulo 998244353.
- Ensure that S_0 = 0 is included in the prefix sums and that `sum_powers` is updated after processing each r.

## worker: finalize
The solution uses the binomial expansion of $(S_r - S_{l-1})^K$ where $S_i$ is the prefix sum. For each right endpoint $r$, we expand the sum over all left endpoints $l$ using the binomial theorem:

$$\sum_{l=1}^r (S_r - S_{l-1})^K = \sum_{j=0}^K \binom{K}{j} S_r^j (-1)^{K-j} \sum_{l=1}^r S_{l-1}^{K-j}$$

We maintain `sum_powers[p]` which stores $\sum_{i=0}^{r-1} S_i^p$. For each $r$, we compute the contribution in $O(K)$ time, then update `sum_powers` with $S_r^p$ for all $p \in [0, K]$. This gives an $O(NK)$ overall solution, which is efficient since $K \leq 10$.

Key details:
- Modulo arithmetic is applied at each step.
- Negative values from $(-1)^{K-j}$ are handled by taking modulo.
- $S_0 = 0$ is included, with $0^0 = 1$ and $0^p = 0$ for $p > 0$.
- Binomial coefficients are precomputed using the multiplicative formula.
