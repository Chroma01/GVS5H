
## ideation
**Solution Explanation (already given in the plan)**  

The required sum can be written as  

\[
\sum_{k=0}^{N-1} (N-1-k)!\,k!\;\bigl(\text{total}\cdot e_k - g_k\bigr)
\]

where  

* `total = N(N+1)/2`,  
* `e_k` are the elementary symmetric sums of the numbers \(b_i = 10^{\text{len}(i)}\pmod{M}\),
* `g_k` is defined by the generating function  

\[
G(t)=\sum_{k\ge 0} g_k t^k
     = t\;F(t)\;\sum_{L} a_L S_L\frac{1}{1+a_Lt},
\qquad 
F(t)=\prod_{i=1}^{N}(1+b_i t)=\sum_{k=0}^{N} e_k t^k .
\]

All numbers with the same decimal length have the same `b_i`.  
Let  

* `L` – the number of digits ( 1…6 ),  
* `c_L` – how many integers in \([1,N]\) have `L` digits,  
* `S_L` – their sum,  
* `a_L = 10^{L}\bmod M`.

Then  

\[
F(t)=\prod_{L} (1+a_L t)^{c_L},
\qquad
H(t)=\sum_{L} a_L S_L \sum_{m=0}^{N-1}(-a_L)^m t^m,
\qquad
G(t)=t\;F(t)\;H(t).
\]

All coefficients of `F` and `H` are computed, the product `R(t)=F(t)·H(t)` is
obtained (only the first `N` coefficients are needed) and  

```
g[0] = 0
g[k] = coefficient of t^{k-1} in R(t)   (k≥1)
```

Finally the answer is accumulated with the formula above.
All polynomial multiplications are performed with a Number‑Theoretic Transform
(NTT) modulo `998244353` in `O(N log N)` time.

--------------------------------------------------------------------

**Correctness Proof** (sketch – the full proof is in the plan)

*Lemma 1* For a fixed element `i` the total contribution of `i` equals  
\(S_i=\sum_{k=0}^{N-1}(N-1-k)!\,k!\,e_k^{(i)}\), where `e_k^{(i)}` is the `k`‑th elementary symmetric sum of the other `N‑1` numbers.

*Lemma 2* \( \sum_{i=1}^{N} i\,e_k^{(i)} = \text{total}\,e_k - g_k\).

*Lemma 3* The whole sum equals  
\(\displaystyle \sum_{k=0}^{N-1} (N-1-k)!\,k!\,(\text{total}\,e_k-g_k)\).

*Lemma 4* `F(t)=∏(1+b_i t)` has coefficients `e_k`; `G(t)=∑ i b_i t ∏_{j≠i}(1+b_j t)` has coefficients `g_k`.

*Lemma 5* Grouping by digit length gives the closed forms for `F(t)`, `H(t)` and the relation `G(t)=t·F(t)·H(t)`.

*Lemma 6* The algorithm computes the coefficients `e_k` (from `F`) and `g_k` (from `R=F·H`) exactly.

*Lemma 7* The final accumulation performed by the program is exactly the expression of Lemma 3.

*Theorem* The program outputs  
\(\displaystyle\sum_{P\in\text{perm}(1..N)} f(P) \pmod{998244353}\).

--------------------------------------------------------------------

**Complexity Analysis**

* building groups, factorials, `H(t)` – `O(N)`;
* at most six NTT multiplications for the groups (size ≤ `N`);
* one final NTT for `F·H` (size ≤ `2N`);
* final summation – `O(N)`.

Overall time `O(N log N)`, memory `O(N)`.

--------------------------------------------------------------------

**Reference Implementation (Python 3)**

```python
import sys

MOD = 998244353
ROOT = 3                     # primitive root of MOD

# ---------- NTT ----------
def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def multiply(a, b, need=None):
    """convolution of a and b, truncated to at most need coefficients"""
    if not a or not b:
        return [0] * (need if need is not None else 0)
    total_len = len(a) + len(b) - 1
    if need is None:
        need = total_len
    else:
        need = min(need, total_len)
    n = 1
    while n < total_len:
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:need]


# ---------- main ----------
def solve() -> None:
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.read().strip()
    if not data:
        return
    N = int(data)

    # factorials and inverse factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # group numbers by decimal length
    max_len = len(str(N))
    cnt = [0] * (max_len + 1)          # c_L
    sum_grp = [0] * (max_len + 1)      # S_L (mod MOD)
    a = [0] * (max_len + 1)            # a_L = 10^L mod MOD

    for L in range(1, max_len + 1):
        low = 10 ** (L - 1)
        high = 10 ** L - 1
        if low > N:
            break
        high = min(high, N)
        c = high - low + 1
        cnt[L] = c
        # arithmetic series sum
        s = (low + high) * c // 2
        sum_grp[L] = s % MOD
        a[L] = pow(10, L, MOD)

    # build F(t) = product_L (1 + a_L t)^{c_L}
    F = [1]                     # start with constant polynomial
    need = N + 1                # we need coefficients 0..N
    for L in range(1, max_len + 1):
        c = cnt[L]
        if c == 0:
            continue
        al = a[L]
        # polynomial (1 + al t)^c  via binomial expansion
        poly = [0] * (c + 1)
        pow_al = 1
        fact_c = fact[c]
        for k in range(c + 1):
            binom = fact_c * inv_fact[k] % MOD * inv_fact[c - k] % MOD
            poly[k] = binom * pow_al % MOD
            pow_al = pow_al * al % MOD
        F = multiply(F, poly, need=need)
    if len(F) < need:
        F += [0] * (need - len(F))

    # build H(t) = Σ_L a_L * S_L * Σ_{m=0}^{N-1} (-a_L)^m t^m
    H = [0] * N
    for L in range(1, max_len + 1):
        if cnt[L] == 0:
            continue
        al = a[L]
        coeff = al * sum_grp[L] % MOD
        cur = 1
        neg_al = (MOD - al) % MOD
        for m in range(N):
            H[m] = (H[m] + coeff * cur) % MOD
            cur = cur * neg_al % MOD

    # R(t) = F(t) * H(t)   (only first N coefficients are needed)
    R = multiply(F, H, need=N)

    # g_k : g_0 = 0, g_k = coefficient of t^{k-1} in R(t)  (k>=1)
    g = [0] * N
    for k in range(1, N):
        g[k] = R[k - 1]

    total_sum = N * (N + 1) // 2 % MOD
    ans = 0
    for k in range(N):
        term = (total_sum * F[k] - g[k]) % MOD
        ans = (ans + fact[k] * fact[N - 1 - k] % MOD * term) % MOD

    print(ans)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required time (`O(N log N)`) and memory (`O(N)`) limits.

## worker: finalize
The solution uses generating functions and Number-Theoretic Transform (NTT) to compute the sum efficiently. The key steps are:
1. Group numbers by decimal length to handle the factor \(10^{\text{len}(i)}\) efficiently.
2. Build the polynomial \(F(t) = \prod_{i=1}^{N} (1 + 10^{\text{len}(i)} t)\) via grouped binomial expansions and NTT multiplications.
3. Build the polynomial \(H(t) = \sum_{L} 10^L S_L \sum_{m=0}^{N-1} (-10^L)^m t^m\) where \(S_L\) is the sum of numbers with \(L\) digits.
4. Compute \(R(t) = F(t) \cdot H(t)\) using NTT, then extract the coefficients \(g_k\).
5. Accumulate the answer using the derived formula:  
   \[
   \text{Ans} = \sum_{k=0}^{N-1} k! \cdot (N-1-k)! \cdot \left( \text{total} \cdot f_k - g_k \right)
   \]  
   where \(f_k\) are coefficients of \(F(t)\) and \(\text{total} = N(N+1)/2\).
The algorithm runs in \(O(N \log N)\) time and uses \(O(N)\) memory, suitable for \(N \le 2 \times 10^5\).
