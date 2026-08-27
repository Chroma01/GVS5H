
## ideation
The core difficulty lies in efficiently computing the binomial coefficient $C(n-1, k)$ modulo $10^9 + 7$ given that $n$ can be up to $10^5$. Since the modulus is a prime number, we can use Fermat's Little Theorem to compute the modular inverse of the factorials. The formula derived is:
$$ \text{Answer} = \binom{n-1}{k} \times m \times (m-1)^{n-1-k} \pmod{10^9+7} $$

Candidate approaches:
1.  **Direct Formula with Precomputed Factorials**: Calculate factorials and their modular inverses up to $n$. This is $O(n)$ precomputation and $O(1)$ per query (though here we only have one query, so $O(n)$ is acceptable).
2.  **Compute Factorials on the Fly**: Since there is only one test case per run, we don't strictly need a global precomputed array. We can compute $(n-1)!$, $k!$, and $(n-1-k)!$ directly in $O(n)$ time, then compute the modular inverse of the denominator using `pow(denominator, MOD-2, MOD)`.
3.  **Iterative Combination Calculation**: Compute $C(n-1, k)$ iteratively: $C(n, k) = C(n, k-1) \times (n-k+1) \times k^{-1}$. This avoids full factorials but still requires modular inverse for each step or precomputed inverses. Given the constraints, the direct factorial approach with a single modular inverse at the end is likely the simplest and most efficient.

Pitfalls:
-   **Modulo Arithmetic**: All multiplications must be modulo $10^9 + 7$.
-   **Edge Cases**: 
    -   $k = 0$: The term $(m-1)^{n-1}$ should be handled correctly (if $m=1$ and $k=0$, result should be 0 unless $n=1$? Wait, if $m=1$, elements must be all 1. If $k=0$, no adjacent equal pairs. If $n > 1$, impossible. If $n=1$, $k=0$ is valid. The formula handles this: if $m=1, k=0, n>1$, then $(1-1)^{n-1} = 0$, correct).
    -   $m = 1$: If $k > 0$, answer is 0 (cannot have equal pairs if only 1 value exists and $n>1$? Actually if $m=1$, all elements are 1, so all $n-1$ pairs are equal. So if $k \neq n-1$, answer is 0. The formula: if $k \neq n-1$, then $(m-1)^{n-1-k} = 0^{positive} = 0$, correct).
    -   $n=1$: Then $k$ must be 0. Formula gives $C(0,0) \times m \times (m-1)^0 = 1 \times m \times 1 = m$. Correct.
-   **Large Exponents**: Use `pow(base, exp, mod)` for modular exponentiation.
-   **Negative Base**: $(m-1)$ could be 0, which is fine. Python handles negative bases in pow correctly if needed, but here $m \ge 1$, so $m-1 \ge 0$.

## worker: Define the modulus `MOD = 10**9 + 7`, calculate th
The solution implements the derived formula: $ \text{Answer} = \binom{n-1}{k} \times m \times (m-1)^{n-1-k} \pmod{10^9+7} $.
1.  **Binomial Coefficient**: Calculated as $\frac{(n-1)!}{k!(n-1-k)!}$. Since $n$ is up to $10^5$, we compute the factorials in $O(n)$ time. The modular inverse of the denominator is computed using Fermat's Little Theorem ($a^{MOD-2} \pmod{MOD}$), which is efficient ($O(\log MOD)$).
2.  **Power Term**: Computed using Python's built-in `pow(base, exp, mod)` for $O(\log(\text{exponent}))$ complexity.
3.  **Edge Cases**:
    -   If $k > n-1$, the loop ranges for factorials would be invalid or the logic would fail, so an explicit check returns 0.
    -   If $m=1$ and $k < n-1$, $(m-1)^{n-1-k}$ becomes $0^{positive} = 0$, correctly returning 0.
    -   If $n=1$, then $k$ must be 0. The code computes $C(0,0)=1$, $m$, and $(m-1)^0=1$, returning $m$, which is correct.
4.  **Complexity**: Time complexity is $O(n)$ due to factorial computation, which fits well within the $10^5$ constraint. Space complexity is $O(1)$.
