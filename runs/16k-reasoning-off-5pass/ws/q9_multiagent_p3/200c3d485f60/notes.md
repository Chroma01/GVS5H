
## ideation
**Core Difficulty**: The problem asks for the number of arrays of length `n` with values in `[1, m]` having exactly `k` adjacent equal pairs. The constraints ($n, m \le 10^5$) require an $O(1)$ or $O(\log n)$ solution, ruling out dynamic programming that iterates through all states or combinatorial approaches that don't simplify to a closed form.

**Candidate Approaches**:
1.  **Combinatorial Logic (Selected)**:
    *   There are `n-1` adjacent positions (indices $0$ to $n-2$ between elements).
    *   We need to choose exactly `k` of these positions to be "equal" ($arr[i] == arr[i+1]$). The number of ways to choose these positions is $\binom{n-1}{k}$.
    *   Once the equality pattern is fixed:
        *   The first element $arr[0]$ can be any of the `m` values.
        *   For any position $i$ where $arr[i] \neq arr[i+1]$ (there are $(n-1) - k$ such transitions), $arr[i+1]$ must be different from $arr[i]$. There are `m-1` choices.
        *   For any position $i$ where $arr[i] == arr[i+1]$, $arr[i+1]$ is determined by $arr[i]$. There is 1 choice.
    *   Total count = $\binom{n-1}{k} \times m \times (m-1)^{(n-1)-k}$.
    *   All calculations must be modulo $10^9 + 7$.

2.  **Dynamic Programming**:
    *   Define $dp[i][j]$ as the number of arrays of length $i+1$ with exactly $j$ equal pairs.
    *   Transition: To form an array of length $i+1$ with $j$ pairs, we can append a value equal to the last (increasing pair count) or different (keeping pair count).
    *   $dp[i][j] = dp[i-1][j-1] \times m + dp[i-1][j] \times (m-1)$.
    *   Complexity: $O(n \times k)$. Given $n, k \le 10^5$, this is $O(10^{10})$, which will TLE. This confirms the combinatorial approach is necessary.

## worker: Write the Python code implementing the combinatori
The solution uses the combinatorial approach derived in the plan:
1.  **Combinatorics**: There are `n-1` adjacent slots. We choose `k` of them to be equal pairs. The number of ways to choose these positions is $\binom{n-1}{k}$.
2.  **Value Assignment**:
    *   The first element has `m` choices.
    *   For the remaining `n-1` transitions, `k` are fixed (equal, 1 choice) and `(n-1)-k` are free (different, `m-1` choices).
    *   Total value assignments: $m \times (m-1)^{n-1-k}$.
3.  **Modular Arithmetic**: Since the result can be very large, all calculations are performed modulo $10^9 + 7$. This includes factorial calculations, modular inverse (using Fermat's Little Theorem for prime modulus), and exponentiation.
4.  **Edge Cases**: Handled `k > n-1` (returns 0) and cases where `m=1` (if `k > 0`, result is 0; if `k=0`, result is 1). The formula naturally handles `m=1` because `(m-1)` becomes 0, raising to a positive power yields 0, which is correct (only possible if `k=n-1`, but if `k < n-1`, result is 0).

## worker: Verify the solution against provided examples and 
The solution implements the combinatorial logic derived in the plan:
1.  **Combinatorics**: There are `n-1` adjacent slots. We choose `k` of them to be equal pairs. The number of ways to choose these positions is $\binom{n-1}{k}$.
2.  **Value Assignment**:
    *   The first element has `m` choices.
    *   For the remaining `n-1` transitions, `k` are fixed (equal, 1 choice) and `(n-1)-k` are free (different, `m-1` choices).
    *   Total value assignments: $m \times (m-1)^{n-1-k}$.
3.  **Modular Arithmetic**: Since the result can be very large, all calculations are performed modulo $10^9 + 7$. This includes factorial calculations, modular inverse (using Fermat's Little Theorem for prime modulus), and exponentiation.
4.  **Edge Cases**: Handled `k > n-1` (returns 0) and cases where `m=1` (if `k > 0`, result is 0; if `k=0`, result is 1). The formula naturally handles `m=1` because `(m-1)` becomes 0, raising to a positive power yields 0, which is correct (only possible if `k=n-1`, but if `k < n-1`, result is 0).

Verification against examples:
- Example 1: n=3, m=2, k=1. N=2. C(2,1)=2. Term2 = 2 * (1)^1 = 2. Result = 2*2 = 4. Correct.
- Example 2: n=4, m=2, k=2. N=3. C(3,2)=3. Term2 = 2 * (1)^1 = 2. Result = 3*2 = 6. Correct.
- Example 3: n=5, m=2, k=0. N=4. C(4,0)=1. Term2 = 2 * (1)^4 = 2. Result = 1*2 = 2. Correct.
