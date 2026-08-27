
## ideation
The core difficulty is efficiently computing the sum of the K-th power of all subarray sums. A naive $O(N^2)$ approach is too slow for $N \le 2 \times 10^5$. The key insight is to use prefix sums $S_i$ and expand $(S_r - S_{l-1})^K$ using the binomial theorem. This transforms the problem into computing sums of products of powers of prefix sums, which can be done in $O(NK)$ time by maintaining running prefix sums of powers $S_i^p$ for $p \in [0, K]$. Since $K$ is small ($K \le 10$), this approach is efficient.

Pitfalls:
1. Modular arithmetic must be applied at every step to prevent overflow and ensure correctness.
2. The binomial expansion involves alternating signs, so careful handling of negative results modulo $P$ is needed.
3. The constraints say $A_i$ can be 0, which is fine as prefix sums can be 0.
4. The indices: $l$ ranges from $1$ to $N$, $r$ from $l$ to $N$. Letting $j = l-1$, we have $0 \le j < r \le N$. So we consider prefix sums $S_0, S_1, \dots, S_N$.

## worker: [todo] **Task 1**: Read input N, K, and array A. C
The solution uses the binomial expansion of $(S_r - S_{l-1})^K$ to transform the problem into computing sums of products of powers of prefix sums. By maintaining running prefix sums of $S_i^p$ for $p \in [0, K]$, we can compute the answer in $O(NK)$ time, which is efficient given $N \le 2 \times 10^5$ and $K \le 10$.

Key steps:
1. Compute prefix sums $S_0, S_1, \ldots, S_N$ modulo 998244353.
2. Precompute binomial coefficients $\binom{K}{m}$ using Pascal's triangle.
3. Iterate $r$ from 1 to $N$, maintaining running prefix sums of powers $S_j^p$ for $j < r$.
4. For each $r$, compute the contribution using the binomial expansion and update the running prefix sums.
5. Handle negative signs from $(-1)^{K-m}$ carefully with modular arithmetic.
