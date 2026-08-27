
## ideation
We need to compute  
\(S = \sum_{1\le l\le r\le N} \big( \sum_{i=l}^r A_i \big)^K\) modulo \(M = 998244353\), with \(N \le 2\cdot 10^5\), \(K \le 10\).

Let \(P_0 = 0\), and \(P_i = A_1 + \dots + A_i\) for \(i=1..N\). Then  
\(\sum_{i=l}^r A_i = P_r - P_{l-1}\). So  
\(S = \sum_{0\le i<j\le N} (P_j - P_i)^K\).

Using binomial theorem:
\((P_j - P_i)^K = \sum_{t=0}^K \binom{K}{t} P_j^t (-P_i)^{K-t}\).

Therefore
\(S = \sum_{t=0}^K \binom{K}{t} (-1)^{K-t} \left( \sum_{0\le i<j\le N} P_i^{K-t} P_j^t \right)\).

Define
\(C_t = \sum_{0\le i<j\le N} P_i^{K-t} P_j^t = \frac{1}{2}\left( \left( \sum_{i=0}^N P_i^t \right) \left( \sum_{i=0}^N P_i^{K-t} \right) - \sum_{i=0}^N P_i^{K} \right)\).

Because the sum over all ordered pairs \(i \neq j\) equals product of sums, subtract diagonal (i=j) to get unordered i<j.

Then
\(S = \sum_{t=0}^K \binom{K}{t} (-1)^{K-t} C_t\).

We can precompute:
- \(S_m = \sum_{i=0}^N P_i^m\) for \(m = 0..K\).
- Binomial coefficients \(\binom{K}{t}\) modulo M.

Then compute each \(C_t\) in O(1) using the formula above, accumulate the weighted sum.

Complexities: O(N*K) time, O(K) memory. K<=10, N<=2e5, so fast enough.

Pitfalls:
- Modulo operations must be done correctly; the division by 2 is multiplication by the modular inverse of 2.
- Use \(P_0 = 0\) in the sums.
- Handle negative (-1)^{K-t} via multiplication with M-1 (i.e., -1 mod M).
- A_i can be 0, prefix sums fit modulo M but note that we are working modulo M, and the original problem asks for sum modulo M, so prefix sums can be computed modulo M safely.
- Ensure to use pow with mod, but exponents up to K=10, so we can precompute powers of each prefix sum by repeatedly multiplying.

Implementation details:
- Precompute prefix sums array pref[0..N] modulo M.
- Maintain running sums power_sum[m] for m=0..K: start with 0^0=1 and 0^m=0 for m>0 for pref[0]=0. For each pref[i] from 0..N:
  - compute x = pref[i]
  - update power_sum[0] += 1
  - For m=1..K: power_sum[m] = (power_sum[m] + x^m) mod M. Since K small, we can compute x^m on the fly by maintaining a small loop or by calling pow(x,m,M). Using pow each time is okay (2e5 * 10 * log) fine.
- After processing all, we have S_m = power_sum[m].
- Compute factorials or binomial coefficients via Pascal or precomputed comb. K small, so we can precompute comb[K][t] easily.

Edge cases: N=1, K up to 10, A_i=0 => answer 0. Works.

Check sample: Let's manually verify? Not needed.

We need to output answer modulo M.

## worker: Implement the `solve()` function in Python that re
- The sum over intervals is rewritten using prefix sums: \(\sum_{1\le l\le r\le N} (P_r - P_{l-1})^K = \sum_{0\le i<j\le N} (P_j - P_i)^K\).
- Binomial expansion: \((P_j - P_i)^K = \sum_{t=0}^K \binom{K}{t} (-1)^{K-t} P_j^t P_i^{K-t}\).
- Interchanging sums yields \(S = \sum_{t=0}^K \binom{K}{t} (-1)^{K-t} C_t\) where \(C_t = \sum_{i<j} P_i^{K-t} P_j^t\).
- \(C_t\) can be computed from the full sums of powers:  
  \(C_t = \frac{1}{2}\big((\sum_i P_i^t)(\sum_i P_i^{K-t}) - \sum_i P_i^K\big)\).
- We precompute \(S_m = \sum_{i=0}^N P_i^m\) for \(m=0..K\) in \(O(NK)\) time by maintaining running products.
- The modular inverse of 2 is \((MOD+1)//2\) because \(MOD = 998244353\) is prime and odd.
- All operations are performed modulo \(998244353\); the final answer is normalized to the range \([0, MOD)\).
