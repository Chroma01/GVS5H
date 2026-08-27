
## ideation
The core difficulty lies in efficiently computing the sum of powers of subarray sums. A naive $O(N^2)$ approach is too slow given $N \le 2 \times 10^5$. The key insight is using the binomial expansion on $(S_j - S_i)^K$. Since $K$ is very small ($K \le 10$), we can maintain $K+1$ cumulative sums of powers of prefix sums ($S_i^0, S_i^1, \dots, S_i^K$) as we iterate through the array. This reduces the complexity to $O(NK)$, which is well within the limits.

Pitfalls to avoid:
1.  **Modulo Arithmetic**: Ensure all additions, subtractions, and multiplications are performed modulo 998244353. Specifically, handle negative results from $(-S_i)^m$ by adding the modulus before taking the modulo.
2.  **Indexing**: The problem asks for $1 \le l \le r \le N$. In terms of prefix sums $S$, this corresponds to pairs $(i, j)$ where $0 \le i < j \le N$. $S_0 = 0$ must be included in the initial state of the cumulative sums.
3.  **Data Types**: Use 64-bit integers for intermediate calculations to prevent overflow before modulo, although Python handles large integers automatically.

## worker: none
The solution uses the binomial expansion of $(S_j - S_i)^K$ where $S_i$ are prefix sums. By expanding the expression, we can separate the terms involving $S_j$ and $S_i$. Specifically, $(S_j - S_i)^K = \sum_{m=0}^K \binom{K}{m} S_j^{K-m} (-S_i)^m$. 

The algorithm iterates through each possible right endpoint $j$ (from 1 to $N$). For each $j$, it computes the sum over all previous left endpoints $i$ (from 0 to $j-1$) by maintaining cumulative sums of powers of prefix sums $S_i^m$. Since $K$ is small ($\le 10$), maintaining $K+1$ cumulative sums is efficient.

The time complexity is $O(NK)$ because for each of the $N$ elements, we perform $O(K)$ work to compute powers and update cumulative sums. The space complexity is $O(N)$ to store the prefix sums and $O(K)$ for the cumulative sums and binomial coefficients.

Key considerations:
1. Modulo arithmetic is applied at each step to prevent overflow and keep numbers manageable.
2. Negative values from $(-S_i)^m$ are handled by checking the parity of $m$ and subtracting the corresponding term.
3. The initial state includes $S_0 = 0$, which contributes $S_0^0 = 1$ to `cum_pow[0]` and $0$ to all other `cum_pow[m]`.
