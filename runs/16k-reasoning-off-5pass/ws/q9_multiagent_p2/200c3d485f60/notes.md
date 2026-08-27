
## ideation
The problem asks for the number of arrays of length `n` with elements in `[1, m]` such that exactly `k` adjacent pairs are equal.

**Core Difficulty:**
1.  **Combinatorial Selection:** We need to choose exactly `k` positions out of the `n-1` available adjacent slots (indices `0` to `n-2`) where the condition `arr[i] == arr[i+1]` holds. The remaining `n-1-k` slots must have `arr[i] != arr[i+1]`.
2.  **Value Assignment:** Once the positions of equality are fixed, we need to count how many ways we can assign values from `[1, m]` to satisfy these constraints.
    *   If a slot is "equal", the value at `i+1` is determined by `i`.
    *   If a slot is "different", the value at `i+1` can be any of the `m-1` values different from `arr[i]`.
    *   The very first element `arr[0]` can be any of the `m` values.

**Candidate Approaches:**
1.  **Direct Combinatorial Formula:**
    *   Step 1: Choose `k` positions for equality from `n-1` slots: $\binom{n-1}{k}$.
    *   Step 2: Assign values.
        *   Pick `arr[0]`: `m` choices.
        *   For each of the `n-1` transitions:
            *   If it's an "equal" transition (there are `k` of them), there is `1` choice (must match previous).
            *   If it's a "different" transition (there are `n-1-k` of them), there are `m-1` choices.
        *   Total ways to assign values given the pattern: $m \times (m-1)^{n-1-k}$.
    *   Total Answer: $\binom{n-1}{k} \times m \times (m-1)^{n-1-k} \pmod{10^9+7}$.
    *   This approach is $O(n)$ or $O(\log n)$ depending on how we compute the binomial coefficient and power. Given constraints $n, m \le 10^5$, $O(n)$ precomputation for factorials is feasible.

2.  **Dynamic Programming (Alternative verification):**
    *   Let `dp[i][j]` be the number of arrays of length `i+1` (indices 0 to i) with exactly `j` equal adjacent pairs.
    *   Transition:
        *   Append a value equal to the last one: `dp[i][j] += dp[i-1][j-1] * 1` (1 choice).
        *   Append a value different from the last one: `dp[i][j] += dp[i-1][j] * (m-1)` (`m-1` choices).
    *   Base case: `dp[0][0] = m`.
    *   Result: `dp[n-1][k]`.
    *   Complexity: $O(n \cdot k)$. Since $k$ can be up to $n$, this is $O(n^2)$, which is too slow ($10^{10}$ operations).
    *   *Conclusion:* DP is not viable for the given constraints. The combinatorial formula is the correct path.

**Pitfalls:**
1.  **Modulo Arithmetic:** All multiplications and additions must be modulo $10^9 + 7$.
2.  **Factorial Precomputation:** Computing $\binom{n-1}{k}$ requires factorials and inverse factorials. Since we only need one combination, we can compute factorials iteratively up to $n$ and then use modular inverse (Fermat's Little Theorem) for the result, or precompute factorials if multiple queries were involved (here it's a single call, so $O(n)$ precalc is fine).
3.  **Edge Cases:**
    *   $k = 0$: No equal pairs. Formula gives $\binom{n-1}{0} \times m \times (m-1)^{n-1} = m(m-1)^{n-1}$. Correct.
    *   $k = n-1$: All pairs equal. Formula gives $\binom{n-1}{n-1} \times m \times (m-1)^0 = m$. Correct (all elements same).
    *   $m = 1$: If $k > 0$, answer should be 1 (only array of all 1s). If $k=0$, answer should be 0 (impossible to have different elements if only 1 exists).
        *   Check formula for $m=1, k=0$: $1 \times 1 \times 0^{n-1}$. If $n>1$, $0$. Correct. If $n=1$, $1 \times 1 \times 0^0 = 1$. Correct.
        *   Check formula for $m=1, k>0$: $(m-1)^{...} = 0$. Correct.
4.  **Power Function:** Use modular exponentiation for $(m-1)^{n-1-k}$.
5.  **Constraints:** $n$ up to $10^5$. An $O(n)$ loop to compute factorials is acceptable.

**Plan Refinement:**
1.  Define MOD = $10^9 + 7$.
2.  Handle edge case where $k > n-1$ (though constraints say $k \le n-1$, good to be safe).
3.  Compute factorials and inverse factorials up to $n-1$ to get $\binom{n-1}{k}$.
    *   Actually, since we only need one combination, we can compute `fact[n-1]`, `fact[k]`, `fact[n-1-k]` in one pass up to `n-1`.
    *   Compute modular inverse of `fact[k] * fact[n-1-k]` using `pow(..., MOD-2, MOD)`.
4.  Calculate result = `(comb * m) % MOD * pow(m-1, n-1-k, MOD) % MOD`.

## worker: Implement the `countGoodArrays` method using the d
The solution implements the derived combinatorial formula:
1.  **Combinatorial Selection**: We choose `k` positions out of `n-1` adjacent slots to be equal. This is calculated as $\binom{n-1}{k}$.
2.  **Value Assignment**:
    *   The first element has `m` choices.
    *   For the `k` equal transitions, there is only 1 choice (must match the previous element).
    *   For the remaining `n-1-k` different transitions, there are `m-1` choices (any value except the previous one).
    *   Total ways to assign values given the pattern: $m \times (m-1)^{n-1-k}$.
3.  **Final Formula**: The total count is $m \times \binom{n-1}{k} \times (m-1)^{n-1-k}$.
4.  **Implementation Details**:
    *   Factorials are precomputed up to `n-1` in $O(n)$ time.
    *   Modular inverse is computed using Fermat's Little Theorem ($a^{MOD-2} \pmod{MOD}$) since $MOD$ is prime.
    *   Modular exponentiation is used for the power term.
    *   All intermediate calculations are performed modulo $10^9 + 7$.
    *   Edge cases like $k > n-1$ are handled.

## worker: Verify the solution against the provided examples 
The solution implements the combinatorial formula derived:
1.  **Combinatorial Selection**: Choose `k` positions out of `n-1` adjacent slots to be equal. This is $\binom{n-1}{k}$.
2.  **Value Assignment**:
    *   First element: `m` choices.
    *   `k` equal transitions: 1 choice each (must match previous).
    *   `n-1-k` different transitions: `m-1` choices each.
    *   Total ways: $m \times (m-1)^{n-1-k}$.
3.  **Final Formula**: $m \times \binom{n-1}{k} \times (m-1)^{n-1-k} \pmod{10^9+7}$.
4.  **Verification**:
    *   Example 1: `n=3, m=2, k=1`. Formula: $2 \times \binom{2}{1} \times (1)^1 = 2 \times 2 \times 1 = 4$. Matches.
    *   Example 2: `n=4, m=2, k=2`. Formula: $2 \times \binom{3}{2} \times (1)^1 = 2 \times 3 \times 1 = 6$. Matches.
    *   Example 3: `n=5, m=2, k=0`. Formula: $2 \times \binom{4}{0} \times (1)^4 = 2 \times 1 \times 1 = 2$. Matches.
5.  **Complexity**: $O(n)$ for factorial precomputation, $O(\log MOD)$ for modular inverse and power. Given $n \le 10^5$, this is efficient.
