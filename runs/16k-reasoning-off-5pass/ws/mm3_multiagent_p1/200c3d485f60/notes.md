
## ideation
The core difficulty is to translate the condition "exactly k equal adjacent pairs" into a combinatorial construction. The natural way: an array of length n with exactly k indices i where arr[i-1]==arr[i] consists of r = n - k "runs" (maximal blocks of equal values). The number of runs determines the number of "breaks" (i where neighbors differ): n-1 - k breaks. Conversely, choose the r-1 break positions among the n-1 gaps, then assign values to runs: first run any of m values, each subsequent run any value ≠ previous (m-1 choices). So total = C(n-1, k) * m * (m-1)^{r-1} = C(n-1, k) * m * (m-1)^{n-k-1}. This is the well-known formula.

Pitfalls:
- k can be n-1, in which case r = 1 and exponent becomes (m-1)^0 = 1; only the first term matters, but we still need C(n-1, n-1) = 1, and there is exactly m such arrays.
- k must be between 0 and n-1; formula works for boundary cases.
- Modulus is prime 1e9+7, so modular inverses via Fermat's little theorem work.
- Need to handle large n up to 1e5; precompute factorials and inverse factorials up to n-1 (or n) in O(n).
- Exponentiation of (m-1) to (n-k-1) must be modular fast pow; if n-k-1 = 0, result is 1.
- Edge case: m=1. Then only one possible value. The formula gives m * (m-1)^{...} = 0 unless exponent of (m-1) is 0 (i.e., n-k-1=0 ⇒ k=n-1). For m=1, only the constant array is possible, and it has n-1 equal adjacent pairs, so answer is 1 if k=n-1, else 0. The formula handles this because (m-1)=0, and 0^0 is treated as 1 only when exponent is 0. In code, fast pow should return 1 when exponent is 0, so the formula yields m * 1 = 1 only when k=n-1, else gives 0, which is correct.

Candidate approaches:
- Direct combinatorial formula: C(n-1, k) * m * (m-1)^{n-k-1} mod MOD.
- Alternative DP: dp[i][j] = number of arrays of length i with j equal pairs ending with some value; but combinatorial solution is O(n) precomputation and O(log MOD) exponentiation.
- Verify with given examples: n=3, m=2, k=1 → C(2,1)*2*1^{1} = 2*2*1=4 ✓; n=4,m=2,k=2 → C(3,2)*2*1^{1} = 3*2*1=6 ✓; n=5,m=2,k=0 → C(4,0)*2*1^{4} = 1*2*1=2 ✓.

Implementation plan:
- Precompute factorials fac[0..n-1] and invfac similarly using pow(fac[n-1], MOD-2, MOD) and inverse.
- nCk = fac[n-1] * invfac[k] * invfac[n-1-k] % MOD.
- pow_m1 = pow(m-1, n-k-1, MOD) with proper handling of m-1 (could be 0).
- result = nCk * m % MOD * pow_m1 % MOD.
- Return result.

## worker: Implement the `countGoodArrays` method using the c
The solution uses the standard combinatorial decomposition: an array with exactly k equal-adjacent pairs consists of r = n - k runs. Choose which k of the n-1 gaps are "equal" (i.e., not breaks) in C(n-1, k) ways. Assign values to runs: first run has m choices, each of the remaining r-1 runs must differ from the previous, giving (m-1) choices each. Total = C(n-1, k) * m * (m-1)^{n-k-1}.

Key implementation details:
- Precompute factorials and inverse factorials up to n-1 in O(n) time.
- Use Fermat's little theorem for modular inverses since MOD = 10^9+7 is prime.
- `pow(m-1, n-k-1, MOD)` correctly handles the case where m=1 (base 0) and exponent 0 (returns 1), matching the expected behavior: only constant arrays exist when m=1, valid only when k=n-1.
- Verified against all three examples: (3,2,1)→4, (4,2,2)→6, (5,2,0)→2.
