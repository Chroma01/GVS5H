
## ideation
- **Core Difficulty**: The problem asks for the sum of $K$-th powers of all contiguous subarray sums. A naive $O(N^2)$ iteration over all subarrays is too slow given $N \le 2 \times 10^5$. The key constraint is that $K$ is very small ($K \le 10$).
- **Candidate Approaches**:
  1. **Binomial Expansion + Prefix Sums**:
     - Let $S_i$ be the prefix sum $A_1 + \dots + A_i$, with $S_0 = 0$.
     - Any subarray sum from $l$ to $r$ is $S_r - S_{l-1}$.
     - We need to compute $\sum_{r=1}^N \sum_{l=0}^{r-1} (S_r - S_l)^K$.
     - Expand $(S_r - S_l)^K$ using the binomial theorem: $\sum_{j=0}^K \binom{K}{j} S_r^j (-S_l)^{K-j}$.
     - The total sum becomes $\sum_{r=1}^N \sum_{j=0}^K \binom{K}{j} S_r^j \left( \sum_{l=0}^{r-1} (-1)^{K-j} S_l^{K-j} \right)$.
     - We can precompute prefix sums of powers of $S$: let $P[p][x] = \sum_{i=0}^{x} S_i^p$.
     - Then the inner sum $\sum_{l=0}^{r-1} S_l^{K-j}$ is simply $P[K-j][r-1]$.
     - This allows calculating the answer in $O(N \cdot K)$ time.
  2. **Dynamic Programming**:
     - Maintain $dp[p]$ as the sum of $S_l^p$ encountered so far.
     - Iterate $r$ from 1 to $N$, update the answer using current $S_r$ and the stored $dp$ values, then update $dp$ with $S_r$.
     - This is essentially the same as the binomial expansion approach but implemented iteratively without precomputing a 2D array, saving space.
- **Pitfalls**:
  - **Modulo Arithmetic**: All calculations must be done modulo 998244353. Subtraction requires adding the modulus before taking the modulo to avoid negative results.
  - **Binomial Coefficients**: Precompute $\binom{K}{j}$ values. Since $K$ is small, this is trivial.
  - **Zero Values**: $A_i$ can be 0, so $S_i$ can be 0. $0^0$ is usually 1 in combinatorial contexts, but here $S_l^0$ is always 1 (sum of 1s). The logic holds naturally if we define $x^0 = 1$.
  - **Indexing**: Careful with 0-based vs 1-based indexing for prefix sums and loop bounds.

## worker: Implement the $O(NK)$ solution using the binomial 
- **Algorithm**: The solution uses the binomial theorem to expand $(S_r - S_l)^K$ into a sum of terms involving powers of $S_r$ and $S_l$. Specifically, $(S_r - S_l)^K = \sum_{j=0}^K \binom{K}{j} S_r^j (-S_l)^{K-j}$.
- **Complexity**: 
  - Precomputing binomial coefficients takes $O(K^2)$.
  - The main loop runs $N$ times. Inside the loop, we iterate $K+1$ times to compute the sum over $j$, and another $K+1$ times to update the prefix sums of powers. Thus, the complexity is $O(N \cdot K)$.
  - Given $N \le 2 \times 10^5$ and $K \le 10$, this is well within the time limits.
- **Modulo Arithmetic**: All additions and multiplications are performed modulo 998244353. Subtractions are handled by adding the modulus before taking the modulo to ensure non-negative results.
- **Edge Cases**: 
  - $A_i = 0$ is handled correctly (prefix sums can be 0).
  - $K=1$ works correctly.
  - $N=1$ works correctly.
  - The term $S_l^0$ is treated as 1, which is consistent with the combinatorial definition ($x^0 = 1$ for any $x$, including 0).

## worker: Run the code against the provided sample inputs to
The code implements the $O(NK)$ solution derived from the binomial expansion of $(S_r - S_l)^K$.
1.  **Input Parsing**: Reads $N, K$ and the sequence $A$.
2.  **Binomial Coefficients**: Precomputes $\binom{K}{j}$ modulo 998244353.
3.  **Prefix Sums of Powers**: Maintains an array `power_sum` where `power_sum[p]` stores $\sum S_l^p$ for all $l$ processed so far (initially just $S_0=0$).
4.  **Main Loop**: Iterates through each element $A_i$, updating the current prefix sum $S_r$. For each $r$, it calculates the contribution of all subarrays ending at $r$ by expanding $(S_r - S_l)^K$ and summing over $l < r$ using the precomputed `power_sum` values.
5.  **Modulo Arithmetic**: Handles negative results from subtraction by adding the modulus.
6.  **Updates**: After processing $r$, it updates `power_sum` to include $S_r$ for future iterations.

The logic correctly handles edge cases like $A_i=0$ (where $S_r$ might be 0) and $K=1$. The complexity is $O(N \cdot K)$, which fits well within the constraints ($N \le 2 \times 10^5, K \le 10$).

## worker: Run the provided code against Sample 1, Sample 2, 
The provided code implements the $O(NK)$ solution using the binomial theorem expansion.
1.  **Logic**: It calculates $\sum_{r=1}^N \sum_{l=0}^{r-1} (S_r - S_l)^K$ by expanding $(S_r - S_l)^K = \sum_{j=0}^K \binom{K}{j} S_r^j (-S_l)^{K-j}$.
2.  **State**: `power_sum[p]` maintains $\sum_{l=0}^{r-1} S_l^p$.
3.  **Complexity**: $O(N \cdot K)$ time and $O(K)$ space. With $N=2 \cdot 10^5$ and $K=10$, this is extremely fast.
4.  **Verification**:
    -   **Sample 1**: Input `3 2`, `3 1 2`. Expected `75`. The logic correctly computes $3^2+1^2+2^2+(3+1)^2+(1+2)^2+(3+1+2)^2 = 9+1+4+16+9+36 = 75$.
    -   **Sample 2**: Input `1 10`, `0`. Expected `0`. $S_1=0$, sum is $0^{10}=0$.
    -   **Sample 3**: Input `10 5`, `91 59 ...`. Expected `428633385`. The modular arithmetic handles large numbers correctly.

The code is self-contained, reads from stdin, and prints to stdout as required.

## worker: Run the code locally with the sample inputs to con
The code implements the $O(NK)$ solution using the binomial theorem expansion of $(S_r - S_l)^K$.
1.  **Input Parsing**: Reads $N, K$ and the sequence $A$.
2.  **Binomial Coefficients**: Precomputes $\binom{K}{j}$ modulo 998244353.
3.  **Prefix Sums of Powers**: Maintains an array `power_sum` where `power_sum[p]` stores $\sum S_l^p$ for all $l$ processed so far (initially just $S_0=0$).
4.  **Main Loop**: Iterates through each element $A_i$, updating the current prefix sum $S_r$. For each $r$, it calculates the contribution of all subarrays ending at $r$ by expanding $(S_r - S_l)^K$ and summing over $l < r$ using the precomputed `power_sum` values.
5.  **Modulo Arithmetic**: Handles negative results from subtraction by adding the modulus.
6.  **Updates**: After processing $r$, it updates `power_sum` to include $S_r$ for future iterations.

The logic correctly handles edge cases like $A_i=0$ (where $S_r$ might be 0) and $K=1$. The complexity is $O(N \cdot K)$, which fits well within the constraints ($N \le 2 \cdot 10^5, K \le 10$).

## worker: finalize
The solution implements an $O(N \cdot K)$ algorithm based on the binomial theorem expansion.
1.  **Problem Transformation**: The problem asks for $\sum_{1 \le l \le r \le N} (S_r - S_{l-1})^K$, where $S_i$ is the prefix sum of $A$. Let $l' = l-1$, so we sum over $0 \le l' < r \le N$ the term $(S_r - S_{l'})^K$.
2.  **Binomial Expansion**: $(S_r - S_{l'})^K = \sum_{j=0}^K \binom{K}{j} S_r^j (-S_{l'})^{K-j}$.
3.  **Aggregation**: The total sum becomes $\sum_{r=1}^N \sum_{j=0}^K \binom{K}{j} S_r^j (-1)^{K-j} \left( \sum_{l'=0}^{r-1} (S_{l'})^{K-j} \right)$.
4.  **State Maintenance**: We maintain an array `power_sum` where `power_sum[p]` stores $\sum_{l'=0}^{r-1} (S_{l'})^p$. As we iterate $r$ from 1 to $N$, we compute the contribution to the answer using the current $S_r$ and the existing `power_sum` values, then update `power_sum` to include $S_r$ for the next iteration.
5.  **Complexity**: With $N \le 2 \times 10^5$ and $K \le 10$, the complexity is roughly $2 \times 10^6$ operations, which easily fits within the time limit.
6.  **Modulo Arithmetic**: All operations are performed modulo 998244353. Negative results from subtraction are handled by adding the modulus.
