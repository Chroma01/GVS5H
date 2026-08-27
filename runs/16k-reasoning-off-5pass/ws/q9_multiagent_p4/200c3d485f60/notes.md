
## ideation
**Core Difficulty**: The problem asks for the count of arrays with specific constraints on adjacent equalities. The main challenge is efficiently calculating the number of ways to choose positions for equalities and then multiplying by the number of valid value assignments, all under modulo arithmetic. The constraints ($n, m \le 10^5$) require an $O(n)$ or $O(\log n)$ solution, ruling out brute force or dynamic programming with $O(n^2)$ complexity.

**Candidate Approaches**:
1.  **Combinatorial Formula**:
    *   Identify that we need to choose exactly $k$ indices out of $n-1$ possible adjacent pairs to be equal. This is given by the binomial coefficient $\binom{n-1}{k}$.
    *   Once positions are chosen:
        *   The first element can be any of the $m$ values.
        *   For the $k$ equal pairs, the next element is fixed (1 choice).
        *   For the remaining $(n-1) - k$ non-equal pairs, the next element must differ from the previous one, giving $(m-1)$ choices each.
    *   Total formula: $m \times (m-1)^{n-1-k} \times \binom{n-1}{k}$.
    *   Implementation requires modular exponentiation for the power term and modular inverse (using Fermat's Little Theorem since the modulus $10^9+7$ is prime) for the binomial coefficient.

2.  **Dynamic Programming (DP)**:
    *   Define $dp[i][j]$ as the number of arrays of length $i$ with exactly $j$ equal adjacent pairs.
    *   Transition:
        *   If the $i$-th element equals the $(i-1)$-th: $dp[i][j] += dp[i-1][j-1] \times 1$.
        *   If the $i$-th element differs from the $(i-1)$-th: $dp[i][j] += dp[i-1][j] \times (m-1)$.
    *   Base case: $dp[1][0] = m$.
    *   Complexity: $O(n \cdot k)$. Given $n, k \le 10^5$, this could be $O(10^{10})$ in the worst case, which is too slow. However, we only need the final state $dp[n][k]$. We can optimize space, but time complexity remains an issue unless $k$ is small. The combinatorial approach is strictly better here.

## worker: Implement the `countGoodArrays` method using the c
The solution implements the combinatorial formula derived in the plan:
1.  **Combinatorics**: We need to choose $k$ positions out of $n-1$ adjacent slots to be equal. This is $\binom{n-1}{k}$.
2.  **Value Assignment**:
    *   The first element has $m$ choices.
    *   Each of the $k$ equal pairs forces the next element to be the same (1 choice).
    *   Each of the remaining $(n-1) - k$ non-equal pairs allows $m-1$ choices (must differ from the previous).
    *   Total ways = $m \times (m-1)^{n-1-k}$.
3.  **Modular Arithmetic**: Since the result can be very large, all calculations are performed modulo $10^9 + 7$.
4.  **Efficiency**: To compute $\binom{n-1}{k}$ efficiently, we precompute factorials and their modular inverses in $O(n)$ time. The power term is computed in $O(\log n)$ using modular exponentiation. The overall time complexity is $O(n)$, which fits within the constraints ($n \le 10^5$).
5.  **Edge Cases**: Handled the case where $k > n-1$ (impossible) and cases where $m=1$ (if $k > 0$, result is 0; if $k=0$, result is 1).
