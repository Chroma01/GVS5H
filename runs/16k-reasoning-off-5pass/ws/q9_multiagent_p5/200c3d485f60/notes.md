
## ideation
**Core Difficulty**: The problem asks for the number of arrays of length `n` with values in `[1, m]` having exactly `k` adjacent equal pairs. The constraints ($n, m \le 10^5$) require an $O(n)$ or $O(1)$ solution after precomputation, ruling out exponential brute force or simple DP without optimization.

**Candidate Approaches**:
1.  **Combinatorial Derivation (Chosen)**:
    *   There are `n-1` adjacent positions (indices $0$ to $n-2$) where a pair $(arr[i], arr[i+1])$ can be equal or different.
    *   We need to choose exactly `k` of these `n-1` positions to be "equal" ($=$). The remaining `(n-1) - k` positions must be "different" ($\neq$).
    *   Number of ways to choose positions: $\binom{n-1}{k}$.
    *   Once positions are chosen:
        *   The first element $arr[0]$ can be any of `m` values.
        *   For each "equal" transition, the next value is fixed (1 choice).
        *   For each "different" transition, the next value must be different from the previous one ($m-1$ choices).
    *   Total formula: $m \times (m-1)^{(n-1-k)} \times \binom{n-1}{k}$.
    *   Implementation requires modular arithmetic for large numbers and precomputed factorials/inverse factorials to compute $\binom{n}{r} \pmod{10^9+7}$ efficiently.

2.  **Dynamic Programming**:
    *   Let $dp[i][j]$ be the number of arrays of length $i$ with exactly $j$ equal pairs.
    *   Transition: To form an array of length $i$ with $j$ pairs, we can append a value equal to the last (if $j > 0$) or different (if $j < k$).
    *   State space: $n \times k$. Complexity $O(nk)$. Given $n, k \le 10^5$, this is $O(10^{10})$ in worst case, which is TLE.
    *   Optimization: The DP essentially sums up paths which leads back to the combinatorial formula. Not efficient enough directly.

## worker: Implement the `countGoodArrays` method using the c
The solution implements the combinatorial formula derived in the plan:
1.  **Combinatorics**: We choose `k` positions out of `n-1` adjacent slots to be equal. This is calculated as $\binom{n-1}{k}$.
2.  **Value Assignment**:
    *   The first element has `m` choices.
    *   Each of the `n-1-k` "different" transitions has `m-1` choices.
    *   The `k` "equal" transitions have 1 choice (fixed by the previous element).
3.  **Modular Arithmetic**: Since the result can be very large, all calculations are performed modulo $10^9 + 7$.
4.  **Efficiency**:
    *   Factorials and their modular inverses are precomputed in $O(n)$ time.
    *   The binomial coefficient $\binom{n-1}{k}$ is computed in $O(1)$ using the precomputed arrays.
    *   The power term $(m-1)^{n-1-k}$ is computed in $O(\log(n))$ using Python's built-in `pow(base, exp, mod)`.
    *   Overall time complexity is $O(n)$ due to precomputation, which fits within the constraints ($n \le 10^5$).
5.  **Edge Cases**:
    *   If $k > n-1$, the answer is 0 (handled explicitly).
    *   If $m=1$ and $k < n-1$, the term $(m-1)^{...}$ becomes $0^{\text{positive}} = 0$, correctly returning 0.
    *   If $m=1$ and $k = n-1$, the term is $0^0 = 1$, and the result is $1 \times 1 \times \binom{n-1}{n-1} = 1$, which is correct (only one array of all 1s).
