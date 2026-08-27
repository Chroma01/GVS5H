
## ideation
We need to count arrays of length `n` with elements in `[1, m]` that have exactly `k` indices `i` (`1 ≤ i < n`) where `arr[i-1] == arr[i]`.

**Key observation:**  
Each array with exactly `k` equal-adjacent pairs consists of some number of contiguous "runs" (maximal blocks of equal values). If there are `k` equal pairs among the `n-1` adjacent positions, then the number of runs is:

```
runs = (n - 1) - k + 1 = n - k
```

**Construction approach:**  
To build such an array:
1. Choose which `k` of the `n-1` gaps are "non-breaks" (i.e., equal adjacencies). The number of ways is `C(n-1, k)`.
2. Pick values for each of the `n-k` runs:
   - The first run can be any of `m` values.
   - Each subsequent run must differ from the previous one, so `m-1` choices each.
3. Total ways: `C(n-1, k) * m * (m-1)^(n-k-1)`.

**Edge cases:**
- If `k > n-1`, the answer is `0` (impossible).
- If `k = n-1` (all adjacencies equal), the exponent `n-k-1 = 0`, so we get `C(n-1, n-1) * m * 1 = m`. Correct.
- If `k = 0` (all adjacencies differ), the exponent is `n-1`, so we get `C(n-1, 0) * m * (m-1)^(n-1) = m * (m-1)^(n-1)`. Correct.

**Modular arithmetic:**  
We need modulo `10^9 + 7` (prime). Precompute factorials and inverse factorials up to `n` (or `n-1`) to compute binomial coefficients in `O(1)`. Use Fermat's little theorem to compute modular inverses: `a^(-1) ≡ a^(p-2) (mod p)`. Also precompute powers of `m-1` up to `n`.

**Complexities:**  
- Precomputation: `O(n)`.  
- Per query: `O(1)`.  
- Memory: `O(n)`.

**Pitfalls:**
- Make sure to handle `m = 1`: then the only array is all 1's, so the number of equal pairs is `n-1`. The formula gives `C(n-1, k) * 1 * 0^(n-k-1)`, which is `1` if `k = n-1`, else `0` (since `0^0` should be `1` when exponent is `0`). Be careful with the exponentiation when `m-1 = 0` and exponent is `0`.
- Modular exponentiation must handle the case where base is `0` and exponent is `0` correctly (return `1`).

## worker: Implement the full `Solution` class with precomput
The solution follows the combinatorial derivation:
- An array with exactly `k` equal-adjacent pairs has `n-k` runs (blocks of equal values).
- Choose which `k` of the `n-1` gaps are equal: `C(n-1, k)`.
- First run: `m` choices; each subsequent run: `m-1` choices (must differ from previous).
- Total: `C(n-1, k) * m * (m-1)^(n-k-1)`.

Precomputation of factorials, inverse factorials (via Fermat's little theorem), and powers of `m-1` up to `n` allows `O(1)` query time after `O(n)` preprocessing. Edge cases handled: `k > n-1` returns 0; `m=1` works correctly because `0^0 = 1` in the precomputed array (when exponent is 0, `pow_base[0] = 1`).
