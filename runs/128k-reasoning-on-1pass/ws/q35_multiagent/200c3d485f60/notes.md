
## ideation
<analysis>
The problem requires counting arrays of length `n` with values in `[1, m]` such that exactly `k` adjacent pairs are equal. This structure implies the array consists of `n - k` contiguous blocks of identical values. The core difficulty lies in correctly modeling this combinatorial structure and performing calculations under modulo arithmetic to handle large numbers efficiently.

Candidate approaches:
1. **Combinatorial Formula**: The array can be viewed as choosing `k` positions out of `n-1` gaps to be "equal" (same value), and the remaining `n-1-k` gaps to be "different" (value changes). This gives $\binom{n-1}{k}$ ways to choose gap types. For each valid gap configuration, there are `n-k` blocks. The first block has `m` choices, and each subsequent block has `m-1` choices (must differ from the previous). This yields $m \times (m-1)^{n-k-1}$ value assignments. The total count is $\binom{n-1}{k} \times m \times (m-1)^{n-k-1} \pmod{10^9+7}$.
2. **Dynamic Programming**: Define `dp[i][j]` as the number of arrays of length `i` with `j` equal adjacent pairs. Transition involves appending a value equal to the last one or different. This would be $O(nk)$ or $O(n)$ with optimization, but the combinatorial approach is more direct and efficient.

Pitfalls:
- Computing $\binom{n-1}{k} \pmod P$ requires modular inverse since division isn't directly supported. Fermat's Little Theorem can be used as $P = 10^9+7$ is prime.
- Edge case `m = 1`: The term $(m-1)^{n-k-1}$ becomes $0^{\text{positive}} = 0$, which correctly yields 0 unless `n-k-1 = 0` (i.e., `k = n-1`), where $0^0 = 1$ in Python's `pow`, matching the single valid array `[1, 1, ..., 1]`.
- Time complexity must be $O(n)$ or better to handle `n = 10^5`. Precomputing factorials or iterative combination calculation works.
</analysis>

## worker: finalize
The solution uses a combinatorial approach:
1. **Gap selection**: An array of size `n` has `n-1` adjacent gaps. We choose exactly `k` of these to be "equal" (same value), which can be done in $\binom{n-1}{k}$ ways.
2. **Block structure**: This partitions the array into `n-k` contiguous blocks of identical values.
3. **Value assignment**: The first block has `m` choices, and each subsequent block has `m-1` choices (must differ from its predecessor), giving $m \times (m-1)^{n-k-1}$ assignments.
4. **Final answer**: $\binom{n-1}{k} \times m \times (m-1)^{n-k-1} \pmod{10^9+7}$.

Edge cases handled:
- `m = 1`: `pow(0, positive, MOD) = 0` (correct, no valid arrays unless all equal).
- `m = 1, k = n-1`: `pow(0, 0, MOD) = 1` in Python, giving exactly 1 valid array `[1,1,...,1]`.
- `n = 1`: `comb(0,0) = 1`, `pow(m-1, 0, MOD) = 1`, result = `m` (any single value).

Time complexity: $O(n)$ for factorial precomputation. Space: $O(n)$.
