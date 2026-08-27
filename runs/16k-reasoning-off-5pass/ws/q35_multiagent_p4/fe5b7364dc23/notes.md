
## ideation
The core difficulty lies in efficiently computing the sum of $K$-th powers of all subarray sums. A naive $O(N^2)$ approach is too slow given $N \le 2 \cdot 10^5$. The key insight is to use prefix sums and the binomial theorem. By expressing the subarray sum $A_l + \dots + A_r$ as $S_r - S_{l-1}$, we can expand $(S_r - S_{l-1})^K$. Swapping the order of summation allows us to compute the total sum in $O(NK)$ time by maintaining running sums of powers of prefix sums. The constraints $K \le 10$ make this $O(NK)$ approach very efficient.

Pitfalls to avoid:
1.  Modulo arithmetic: Ensure all additions, subtractions, and multiplications are performed modulo 998244353. Specifically, handle negative results from subtraction by adding the modulus before taking the modulo.
2.  Binomial coefficients: Precompute or compute on the fly $\binom{K}{j}$ modulo 998244353.
3.  Indices: Be careful with the indices of the prefix sums. $S_0 = 0$, and the subarray from $l$ to $r$ corresponds to $S_r - S_{l-1}$ where $1 \le l \le r \le N$. This means we iterate $r$ from $1$ to $N$ and consider all $l-1$ from $0$ to $r-1$.
4.  Power calculation: Since $K$ is small, we can compute powers directly or precompute them. Given $N$ is large, computing $S_i^m$ for each $i$ and each $m \in [0, K]$ inside the loop is $O(NK)$, which is acceptable.

## worker: (None)
The solution uses the binomial expansion of $(S_r - S_l)^K$ where $S_i$ are prefix sums. By swapping the order of summation, we can compute the total sum in $O(NK)$ time. For each right endpoint $r$, we maintain running sums of powers of prefix sums $S_l$ for all $l < r$. This allows us to efficiently compute the contribution of each $r$ to the total sum. The constraints $N \le 2 \cdot 10^5$ and $K \le 10$ make this approach feasible.

Key steps:
1. Compute prefix sums $S_0, \dots, S_N$.
2. Precompute binomial coefficients $\binom{K}{j}$.
3. Initialize running sums $T[m] = \sum_{l=0}^{r-1} S_l^m$ with $T[0] = 1$ (since $S_0 = 0$ and $0^0 = 1$).
4. For each $r$ from 1 to $N$:
   - Compute powers of $S_r$.
   - Add contributions to the total sum using the binomial expansion.
   - Update $T[m]$ by adding $S_r^m$.
5. Output the result modulo 998244353.
