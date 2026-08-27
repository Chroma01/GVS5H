
## ideation
### PLAN
We rewrite the sum in terms of prefix sums \(P_0=0\) and \(P_i=\sum_{j=1}^i A_j\). For each subarray \(l..r\), the sum is \(P_r-P_{l-1}\). Thus the answer is
\[
S = \sum_{0\le i<j\le N} (P_j-P_i)^K.
\]
Expanding by the binomial theorem,
\[
(P_j-P_i)^K = \sum_{t=0}^{K} \binom{K}{t} P_j^t (-P_i)^{K-t},
\]
so
\[
S = \sum_{t=0}^{K} \binom{K}{t} (-1)^{K-t} \sum_{i<j} P_j^t P_i^{K-t}.
\]
The inner sum \(\sum_{i<j} P_j^t P_i^{K-t}\) can be computed in a single left‑to‑right pass:
keep an array \(\text{cur}[m]=\sum_{i\ \text{processed}} P_i^m\) and accumulate
\(V[t] \mathrel{+}= P_j^t \cdot \text{cur}[K-t]\) at each step \(j\), then update \(\text{cur}\) with \(P_j^m\).  
All operations are performed modulo \(M=998244353\). The overall complexity is \(O(NK)\) with \(O(K)\) extra memory.

### CODE
```python
import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # Precompute binomial coefficients C(K, t) modulo MOD
    C = [0] * (K + 1)
    C[0] = 1
    for t in range(1, K + 1):
        # C(K, t) = C(K, t-1) * (K - t + 1) / t
        C[t] = C[t - 1] * (K - t + 1) % MOD
        C[t] = C[t] * pow(t, MOD - 2, MOD) % MOD

    # cur[m] = sum_{i processed} P_i^m, initially only i=0 (P_0=0)
    cur = [0] * (K + 1)
    cur[0] = 1  # P_0^0 = 1
    # V[t] = sum_{i<j} P_j^t * P_i^{K-t}
    V = [0] * (K + 1)

    prefix = 0
    for a in A:
        prefix = (prefix + a) % MOD
        p = prefix
        # compute powers of p: p_pow[m] = p^m
        p_pow = [1] * (K + 1)
        for m in range(1, K + 1):
            p_pow[m] = p_pow[m - 1] * p % MOD

        # update V[t]
        for t in range(K + 1):
            V[t] = (V[t] + p_pow[t] * cur[K - t]) % MOD

        # update cur[m] with current prefix powers
        for m in range(K + 1):
            cur[m] = (cur[m] + p_pow[m]) % MOD

    # combine with binomial coefficients and signs
    ans = 0
    for t in range(K + 1):
        sign = 1 if (K - t) % 2 == 0 else -1
        ans = (ans + sign * C[t] * V[t]) % MOD

    ans = (ans + MOD) % MOD
    print(ans)

if __name__ == "__main__":
    main()
```

## worker: Implement the solution in Python: read inputs, pre
The solution uses prefix sums \(P_i = \sum_{j=1}^i A_j\) and rewrites the required sum as \(\sum_{0\le i<j\le N} (P_j-P_i)^K\). Expanding via the binomial theorem yields a sum over \(t\) of \(\binom{K}{t}(-1)^{K-t} \sum_{i<j} P_j^t P_i^{K-t}\). The inner double sum is computed in one left‑to‑right pass: maintain `cur[m] = \sum_{processed} P_i^m` and accumulate `V[t] += P_j^t * cur[K-t]`. All operations are modulo \(998244353\). Complexity is \(O(NK)\) time and \(O(K)\) memory, easily handling \(N\le 2\cdot10^5\), \(K\le 10\).
