
## ideation
The problem reduces to counting arrays of length n over an alphabet of size m with exactly k adjacent equalities.  

Key observations:
- An adjacent equality means `arr[i-1] == arr[i]`. Counting exactly k such indices is equivalent to selecting k positions among the n-1 gaps where the value stays the same, and at the remaining n-1-k gaps the value changes.
- The "change" positions partition the array into `k+1` maximal runs of equal values. Adjacent runs must have distinct values.
- The number of ways to pick which k gaps are "stays" is `C(n-1, k)`.
- For the values: the first run can be any of `m` values. Each subsequent run (there are k of them) can be any value except the previous run's value, giving `m-1` choices. So total value assignments = `m * (m-1)^k`.
- Total = `C(n-1, k) * m * (m-1)^k` modulo `MOD = 1_000_000_007`.

Pitfalls / details:
- n up to 1e5, so precomputing factorials up to n (or n-1) is fine.
- Need modular inverses to compute `C(n-1, k)` quickly, using Fermat's little theorem since MOD is prime.
- k can be 0, so handle `(m-1)^0 = 1`. Also k = n-1, then `m * (m-1)^{n-1} * C(n-1, n-1) = m * (m-1)^{n-1}`.
- Edge cases: m=1. Then m-1=0. Only possible if k=0 (all values must be 1, giving exactly 0 equal adjacent pairs? Wait: if m=1, all entries are 1, so there are n-1 equal adjacent pairs, not 0. So answer should be 1 if k = n-1 else 0. Our formula gives: C(n-1, k) * 1 * 0^k. If k=0, 0^0 interpreted as 1? We need to be careful. Actually for m=1, (m-1)^k = 0^k. For k=0, 0^0 is mathematically 1 by convention in combinatorics (empty product). But also C(n-1,0)=1, so product =1, but the array of all 1s has n-1 equal pairs, not 0. So for m=1, k must be n-1. We should explicitly handle: if m==1, return 1 if k == n-1 else 0. Or more generally, the formula works for m>=2. For m=1, treat separately. Let's verify: if m=1, k=0, formula gives 1 * 1 * 0^0 = 1 (wrong). So we need the special case.

Complexities:
- Precompute factorials and inv factorials up to max(n, m) (n is enough, but m can be larger; we only need up to n for binomial, but pow mod needs exponent up to k which is <= n-1. So precomputing factorials up to n is enough.
- O(n) time, O(n) memory.

## worker: Implement the `countGoodArrays` method with modula
- The problem reduces to selecting `k` positions among the `n-1` adjacent pairs where the values stay the same. The remaining `n-1-k` positions are "breaks" that partition the array into `k+1` runs of equal values.
- The first run can take any of the `m` values. Each subsequent run must differ from the previous run, giving `m-1` choices. With `k` breaks, there are `k` subsequent runs.
- Therefore the answer is `C(n-1, k) * m * (m-1)^k` modulo `10^9+7`.
- For `m == 1`, the only array is all 1's, which has exactly `n-1` equal adjacent pairs. So the answer is `1` if `k == n-1`, else `0`. The general formula would incorrectly give `1` for `k=0` due to the `0^0` convention, so this case is handled explicitly.
- Factorials and inverse factorials up to `n` are precomputed to evaluate the binomial coefficient in `O(1)` time using Fermat's little theorem. The overall time complexity is `O(n)` for precomputation and `O(log MOD)` for the modular exponentiation, with `O(n)` extra memory.
