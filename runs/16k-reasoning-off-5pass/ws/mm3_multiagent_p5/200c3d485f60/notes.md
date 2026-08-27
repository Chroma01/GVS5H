
## ideation
The problem reduces to counting sequences of length n over an alphabet of size m where exactly k of the n-1 adjacent pairs are equal.  
Key observations:
- The positions of the k equal pairs can be any subset of the n-1 adjacent indices → C(n-1, k) ways.
- The first element is free → m choices.
- At each of the remaining (n-1-k) positions where the value changes, we can pick any of the m-1 values different from the previous one → (m-1)^(n-1-k) ways.
- If k = n-1, the exponent is 0, giving (m-1)^0 = 1, so the formula still holds and the result is m (only constant arrays).

Therefore the answer is:  
`answer = m * C(n-1, k) * (m-1)^(n-1-k) mod (1e9+7)`

Pitfalls:
- Large n (≤1e5) but small enough for precomputed factorials/inverses.
- Modulo exponentiation with base (m-1) and exponent (n-1-k) which may be 0.
- m = 1 special case: if m=1, then all entries must be 1, so k must equal n-1 for a valid array; the formula gives `1 * C(n-1,k) * 0^(n-1-k)` which is 0 unless exponent is 0, correctly yielding 1 when k=n-1.
- Must use modular inverse factorials to compute combinations efficiently.

## worker: Implement the `countGoodArrays` method in the `Sol
The solution implements the combinatorial derivation:
- Choose k positions out of n-1 to be "equal pairs" → `C(n-1, k)`.
- Pick the first value → `m`.
- For each of the remaining `n-1-k` positions where a change occurs, there are `m-1` new choices → `(m-1)^(n-1-k)`.
- Modulo multiplication yields the final answer.

Edge cases handled:
- `k > n-1` or `k < 0` → 0.
- `m == 1` → only one possible array, valid only when `k == n-1`.
- `k == n-1` → exponent becomes 0, yielding `1`, so formula naturally simplifies to `m`.
- Large `n` (≤ 10^5) handled by precomputing factorials once and reusing across calls (cache is class-level).

Complexity: O(n) preprocessing, O(log n) for exponentiation, O(1) per query after that.
