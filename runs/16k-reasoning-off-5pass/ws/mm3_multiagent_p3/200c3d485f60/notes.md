
## ideation
The core difficulty: Counting arrays of length `n` with entries in `[1,m]` that have exactly `k` indices `i` where `arr[i-1] == arr[i]`.  
Observation: The condition only depends on transitions between consecutive elements. If we group the array into maximal runs of equal values, each run contributes 0 equal pairs inside, and each boundary between two runs contributes exactly 1 equal pair.  
If there are `r` runs, the number of equal pairs is `r-1`. So we must have `r = k+1` runs.

To construct an array with `r` runs:
- Choose the value of the first run: `m` ways.
- For each subsequent run, its value must differ from the previous run: `m-1` ways each. So `m * (m-1)^(r-1) = m * (m-1)^k`.
- Choose the positions of the `r-1` boundaries among the `n-1` gaps between elements: `C(n-1, r-1) = C(n-1, k)`.

Total:  
`answer = C(n-1, k) * m * (m-1)^k mod (1e9+7)`.

Pitfalls:
- `m = 1`: then `m-1 = 0`. The formula still works: if `k > 0`, answer is 0 because we cannot have runs with different values. If `k = 0`, the whole array must be constant, giving exactly 1 array (`[1]`, `[2]`, ... but with `m=1` only one value). `C(n-1,0) * 1 * 0^0 = 1 * 1 * 1 = 1`. Need to handle `0^0` as 1 in the power computation.
- `k = n-1`: All adjacent pairs equal, i.e., all runs must be length 1? No, `k = n-1` means `r = n` runs. Then each run is exactly one element. Number of ways: `C(n-1, n-1) * m * (m-1)^(n-1) = 1 * m * (m-1)^(n-1)`. Works.
- Large `n, m, k` up to 10^5, so precompute factorials up to `n` (or up to `n-1` is enough) and modular inverses using Fermat's little theorem (mod is prime `1e9+7`).
- Use fast exponentiation for `(m-1)^k`.

Approach summary:
1. Precompute `fact` and `inv_fact` up to `n` (or `n-1`).
2. Compute `binom = C(n-1, k) = fact[n-1] * inv_fact[k] % MOD * inv_fact[n-1-k] % MOD`.
3. Compute `pow_term = pow(m-1, k, MOD)`. (Handle `m-1 == 0` and `k == 0` correctly: `0^0` should be 1.)
4. Return `binom * m % MOD * pow_term % MOD`.

Edge cases to test mentally:
- `n=1, k=0`: any of `m` values, no adjacent pairs to check. Formula: `C(0,0)=1, m, (m-1)^0=1` => `m`. Correct.
- `m=1, k=0`: Formula gives `1 * 1 * 1 = 1`. Correct (only array `[1]`).
- `m=1, k>0`: `C(n-1,k) * 1 * 0^k = 0` (since `0^k = 0` for `k>0`). Correct.
- Example 1: `n=3, m=2, k=1`. `C(2,1)=2`, `m=2`, `(m-1)^1=1` => `4`. Matches.
- Example 2: `n=4, m=2, k=2`. `C(3,2)=3`, `m=2`, `(1)^2=1` => `6`. Matches.
- Example 3: `n=5, m=2, k=0`. `C(4,0)=1`, `m=2`, `(1)^0=1` => `2`. Matches.

The derivation is solid, and the implementation will be straightforward.

## worker: Implement the `Solution` class with `countGoodArra
The solution follows the combinatorial derivation:
- An array with exactly `k` equal adjacent pairs must have exactly `k+1` runs (maximal segments of equal values).
- Choose values for runs: `m` choices for first run, `m-1` for each subsequent run → `m * (m-1)^k`.
- Choose positions of the `k` boundaries among `n-1` gaps → `C(n-1, k)`.
- Total: `C(n-1, k) * m * (m-1)^k mod (10^9+7)`.

Implementation details:
- Precomputed factorials and inverse factorials up to `n` using Fermat's little theorem (mod is prime).
- Handled edge case `k == 0` for the power term to ensure `0^0 = 1`.
- Handled `k > n-1` by returning 0 (though constraints guarantee `k <= n-1`).
- Verified against all three examples: (3,2,1)→4, (4,2,2)→6, (5,2,0)→2.
