
## ideation
Core difficulty is counting arrays by adjacent-equality positions without overcounting. The key insight is that choosing which adjacent gaps are equal determines a run-length decomposition: k equal gaps among n-1 gaps create n-k maximal constant runs. Adjacent runs must differ, while values inside a run are forced once the run value is chosen.

This suggests a closed-form combinatorial count rather than DP: choose the equal-gap positions, then assign values to runs with the first run free and each subsequent run different from the previous one. The main implementation challenge is doing binomial coefficients and powers modulo 1e9+7 efficiently for n up to 1e5.

Pitfalls:
- Off-by-one between equal adjacent pairs k and number of runs: runs = n - k.
- Exponent for later runs is runs - 1 = n-k-1, which can be 0 when k=n-1.
- Edge cases: n=1 has no adjacent pairs; k must be 0. m=1 only works when all adjacent pairs are equal, i.e. k=n-1; formula should naturally handle via (m-1)^0 and binomial, but check n=1.
- Need factorials and inverse factorials up to n-1 or n for C(n-1,k); use Fermat inverse since MOD is prime.
- Avoid O(nk) DP; constraints demand near O(n) precompute plus O(log MOD) pow.
- Validate k range implicitly; given constraints 0<=k<=n-1.

## worker: Implement the complete solution: precompute factor
Implemented the closed-form count:

- Pick the `k` adjacent positions where `arr[i-1] == arr[i]`: `C(n-1, k)`.
- Those equal adjacent pairs merge positions into `n-k` constant runs.
- Assign values to runs: first run has `m` choices, every next run must differ from the previous run, so `(m-1)^(n-k-1)`.

Answer:

`C(n-1, k) * m * (m-1)^(n-k-1) mod 1e9+7`

Factorials and inverse factorials are precomputed up to `n-1` using Fermat inverse since `1e9+7` is prime. Complexity is `O(n)` time and `O(n)` memory per call, with `O(log MOD)` modular exponentiation.

Edge behavior:
- `n=1`: `C(0,0) * m * (m-1)^0 = m`.
- `m=1, k=n-1`: exactly one all-equal array.
- `m=1, k<n-1`: `pow(0, positive, MOD) = 0`, so answer is `0`.
