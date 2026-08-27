
## ideation
- **Core Difficulty**: The problem asks for the number of arrays of length `n` with elements in `[1, m]` such that exactly `k` adjacent pairs are equal. The constraints ($n, m \le 10^5$) require an $O(n)$ or $O(1)$ solution (after precomputation) with modular arithmetic to avoid overflow.
- **Candidate Approaches**:
    1. **Combinatorial Formula**: Identify that choosing `k` positions for equality out of `n-1` possible adjacent slots determines the structure. This gives $\binom{n-1}{k}$ ways to choose the "equality" positions. Once these positions are fixed, the array is split into `n - k` blocks of consecutive identical numbers. The first block can be any of `m` values. Each subsequent block must differ from the previous one, giving `m-1` choices. Total = $\binom{n-1}{k} \times m \times (m-1)^{n-k-1}$.
    2. **Dynamic Programming**: Let `dp[i][j]` be the number of arrays of length `i` with `j` equal adjacent pairs. Transition: `dp[i][j] = dp[i-1][j] * (m-1) + dp[i-1][j-1] * 1`. This is $O(n \cdot k)$, which might be too slow if $k$ is large (up to $10^5$), leading to $10^{10}$ operations. The combinatorial approach is superior.
- **Pitfalls**:
    - Handling modular arithmetic correctly at every multiplication and exponentiation step.
    - Edge cases: $k=0$ (formula still holds: $m \times (m-1)^{n-1}$), $k=n-1$ (all equal, formula: $m \times (m-1)^0 = m$), $m=1$ (if $k>0$ impossible unless $n=1$? Actually if $m=1$, only one array exists. If $k < n-1$, answer is 0. The formula $\binom{n-1}{k} \times 1 \times 0^{n-k-1}$ handles this naturally if $0^0=1$ and $0^x=0$ for $x>0$).
    - Precomputing factorials and inverse factorials for combinations to handle large $n$ efficiently.

## worker: Implement the combinatorial solution by precomputi
- **Algorithm**: The solution uses a combinatorial approach. We choose `k` positions out of `n-1` adjacent slots to be equal, which is `C(n-1, k)`. This splits the array into `n-k` segments. The first segment has `m` choices, and each subsequent segment has `m-1` choices (must differ from the previous). Total = `C(n-1, k) * m * (m-1)^(n-k-1)`.
- **Complexity**: Precomputing factorials takes `O(n)`. Modular exponentiation takes `O(log(n))`. Overall time complexity is `O(n)`, space complexity is `O(n)` for the arrays. Given `n <= 10^5`, this is efficient.
- **Edge Cases**: 
  - `k > n-1`: Returns 0 immediately.
  - `m=1`: If `k < n-1`, `(m-1)` is 0, so result is 0 (correct, as only one array exists and it has `n-1` equal pairs). If `k = n-1`, exponent is 0, `0^0` is treated as 1 by `pow`, result is `1 * 1 * 1 = 1` (correct).
  - `n=1, k=0`: `C(0,0) * 1 * (m-1)^0 = 1 * 1 * 1 = 1` (correct).
- **Modular Arithmetic**: All multiplications and the final result are taken modulo `10^9 + 7`. Inverse factorials are computed using Fermat's Little Theorem since `MOD` is prime.
