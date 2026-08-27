
## ideation
### Solution Explanation
For a permutation `P = (P1, P2, …, PN)` let `L(x)` be the number of decimal digits of `x`.  
When the numbers are concatenated, the value contributed by an element `x` placed at some position is  

```
x · 10^{ sum of L(y) over all y that appear after x } .
```

For a fixed `x` the set of elements after it is a random subset of the other `N‑1` elements.  
Using the identity  

```
10^{ sum L(y) } = ∏_{y≠x} ( 1 + (10^{L(y)}-1)·I(y after x) )
```

and expanding the product, the sum over all permutations of `10^{shift(x)}` becomes  

```
N! · ∑_{S ⊆ others} ( ∏_{y∈S} (10^{L(y)}-1) ) / (|S|+1) .
```

Let `v_y = 10^{L(y)}-1`.  For the whole set `M = {v_1, v_2, …, v_N}` define the polynomial  

```
F(t) = ∏_{y=1}^N (1 + v_y t) = ∑_{k=0}^N e_k t^k .
```

For a fixed `x` the elementary symmetric sums of `{v_y : y≠x}` are the coefficients of  
`F(t) / (1 + v_x t)`.  The sum over all subsets becomes an integral:

```
∑_{S} ∏_{y∈S} v_y / (|S|+1) = ∫_0^1 F(t) / (1 + v_x t) dt .
```

Hence the total answer is

```
Ans = N! · ∑_{x=1}^N x · ∫_0^1 F(t) / (1 + v_x t) dt .
```

Grouping by the number of digits `d` (at most 6) we get

```
Ans = N! · ∑_{d} S_d · ∫_0^1 H_d(t) dt ,
```

where `S_d = sum of all numbers with d digits` and  

```
H_d(t) = F(t) / (1 + v_d t) = (1 + v_d t)^{cnt[d]-1} · ∏_{d'≠d} (1 + v_{d'} t)^{cnt[d']} .
```

`H_d(t)` is a polynomial of degree `N-1`.  Its integral from `0` to `1` is simply  

```
∫_0^1 H_d(t) dt = ∑_{k=0}^{N-1} h_{d,k} / (k+1) ,
```

where `h_{d,k}` are its coefficients.  The full algorithm:

1. Compute `cnt[d]`, `S_d`, `v_d = 10^d-1 (mod MOD)` for `d = 1..6`.
2. Build the polynomial `F(t) = ∏_{d} (1 + v_d t)^{cnt[d]}`.
   Each factor `(1 + v t)^m` is expanded binomially, giving a dense polynomial of degree `m`.  
   The product of at most six such polynomials is computed using NTT (Number Theoretic Transform) – `O(N log N)`.
3. From the coefficients `p_k` of `F(t)`, recover the coefficients of `H_d(t)` by the recurrence  
   `h_0 = p_0`, `h_k = p_k - v_d·h_{k-1}` (since `(1+v_d t)·H_d(t) = F(t)`).
4. For each `d` compute `I_d = ∑_{k=0}^{N-1} h_k · (k+1)^{-1} (mod MOD)`.
5. Answer = `fact[N] · ∑_d (S_d mod MOD) · I_d (mod MOD)`.

All operations are performed modulo `998244353`.  The NTT uses the primitive root `3`.  
The total time complexity is `O(N log N)` and memory `O(N)`.

### Correctness Proof
We prove that the algorithm returns exactly the required sum.

**Lemma 1.** For a fixed element `x`, the sum over all permutations `P` of `10^{shift(x)}` equals  

```
N! · ∑_{S ⊆ {y≠x}} ( ∏_{y∈S} v_y ) / (|S|+1) ,   where v_y = 10^{L(y)}-1 .
```

*Proof.*  In a permutation the indicator `I(y after x)` is 1 iff `y` is after `x`.  
The exponent `shift(x) = ∑_{y≠x} L(y)·I(y after x)`, so  

```
10^{shift(x)} = ∏_{y≠x} 10^{L(y)·I(y after x)} = ∏_{y≠x} ( 1 + (10^{L(y)}-1)·I(y after x) ) .
```

Expand the product.  For a subset `S ⊆ {y≠x}` the coefficient of `∏_{y∈S} v_y` is the indicator that **all** elements of `S` are after `x`.  The number of permutations with this property is `N! / (|S|+1)` (among the `|S|+1` elements `{x}∪S` the relative order is uniform, and `x` must be the earliest).  Summing over `S` gives the stated formula. ∎



**Lemma 2.** Let `F(t) = ∏_{y=1}^N (1 + v_y t) = ∑_{k=0}^N e_k t^k`.  For a fixed `x`,

```
∑_{S ⊆ {y≠x}} ( ∏_{y∈S} v_y ) / (|S|+1) = ∫_0^1 F(t) / (1 + v_x t) dt .
```

*Proof.*  The set `{v_y : y≠x}` has generating function `F(t) / (1 + v_x t) = ∑_{k=0}^{N-1} e'_k t^k`, where `e'_k` is the elementary symmetric sum of degree `k`.  The integral of this polynomial is  

```
∫_0^1 ∑_{k=0}^{N-1} e'_k t^k dt = ∑_{k=0}^{N-1} e'_k / (k+1) ,
```

which is exactly the left hand side by the expansion of the product. ∎



**Lemma 3.** For each digit length `d` let `cnt[d]` be the number of integers with `d` digits, `v_d = 10^d-1`, and `S_d` their sum.  Define  

```
H_d(t) = (1 + v_d t)^{cnt[d]-1} · ∏_{d'≠d} (1 + v_{d'} t)^{cnt[d']} .
```

Then  

```
∫_0^1 H_d(t) dt = ∑_{k=0}^{N-1} h_{d,k} / (k+1) ,
```

where `h_{d,k}` are the coefficients of `H_d(t)`.

*Proof.*  `H_d(t)` is a polynomial of degree `N-1`; integrating termwise gives the sum. ∎



**Lemma 4.** Let `F(t) = ∏_{d} (1 + v_d t)^{cnt[d]}` and let its coefficients be `p_k`.  The coefficients `h_{d,k}` of `H_d(t)` satisfy  

```
h_{d,0} = p_0 ,      h_{d,k} = p_k - v_d·h_{d,k-1}   (k ≥ 1) .
```

*Proof.*  By construction `F(t) = (1 + v_d t)·H_d(t)`.  Comparing coefficients of `t^k` gives `p_k = h_{d,k} + v_d·h_{d,k-1}`, which rearranges to the recurrence. ∎



**Lemma 5.** The total sum of `f(P)` over all permutations equals  

```
Ans = N! · ∑_{d} S_d · ∫_0^1 H_d(t) dt .
```

*Proof.*  Starting from the definition  

```
∑_P f(P) = ∑_{x=1}^N x · ∑_P 10^{shift(x)} .
```

Apply Lemma&nbsp;1 to the inner sum and Lemma&nbsp;2 to replace it with an integral.  Group the `x` by their number of digits `d`.  All `x` with the same `d` share the same `v_x = v_d`, and their sum is `S_d`.  The integrand becomes `F(t) / (1 + v_d t) = H_d(t)`.  Summing over all `x` yields the formula. ∎



**Lemma 6.** The algorithm computes the right hand side of Lemma&nbsp;5.

*Proof.*  
- Step&nbsp;2 builds the polynomial `F(t)` exactly as defined.  
- Step&nbsp;3 uses Lemma&nbsp;4 to obtain the coefficients of each `H_d(t)` from those of `F(t)`.  
- Step&nbsp;4 computes the integral of `H_d(t)` via Lemma&nbsp;3, using precomputed modular inverses of `1,2,…,N`.  
- Step&nbsp;5 multiplies by `S_d` (taken modulo `MOD`) and by `N!`, exactly matching Lemma&nbsp;5. ∎



**Theorem.** The algorithm outputs the sum of `f(P)` over all `N!` permutations of `(1,2,…,N)`, modulo `998244353`.

*Proof.*  By Lemma&nbsp;5 the desired sum equals the expression computed in Lemma&nbsp;6.  The algorithm evaluates that expression exactly (all operations are modulo a prime, and divisions are performed using modular inverses).  Therefore the output is correct. ∎



### Complexity Analysis
- Precomputations (`cnt`, `S_d`, `v_d`, factorials, inverses): `O(N)`.
- Building the `cnt[d]+1` binomial coefficients: `O(N)`.
- Multiplying the at most six factors with NTT: each multiplication costs `O(M log M)` where `M` is the resulting degree.  The total work is `O(N log N)`.
- Recovering the `H_d` coefficients and the integrals: `O(N·maxlen) = O(N)`.
- Memory consumption: the largest polynomial has size `O(N)`.

For `N ≤ 2·10^5` this easily fits the limits.

### Reference Implementation  (Python 3, PyPy-friendly)

```python
import sys

MOD = 998244353
G = 3

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
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v + MOD) % MOD
                w = w * wlen % MOD
        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def multiply(a, b):
    """return convolution of a and b modulo MOD"""
    n = len(a) + len(b) - 1
    size = 1
    while size < n:
        size <<= 1
    fa = a + [0] * (size - len(a))
    fb = b + [0] * (size - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:n]


# ---------- main ----------
def main():
    sys.setrecursionlimit(1 << 25)
    N_line = sys.stdin.readline()
    while N_line.strip() == "":
        N_line = sys.stdin.readline()
    N = int(N_line)

    # precompute inverses 1..N
    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - MOD // i * inv[MOD % i] % MOD

    # factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD

    # count numbers and their sums for each length d = 1..6
    cnt = [0] * 7
    S = [0] * 7
    for d in range(1, 7):
        start = 10 ** (d - 1)
        end = min(10 ** d - 1, N)
        if start <= end:
            c = end - start + 1
            cnt[d] = c
            S[d] = c * (start + end) // 2

    # v_d = 10^d - 1 (mod MOD)
    v = [0] * 7
    for d in range(1, 7):
        v[d] = (pow(10, d, MOD) - 1) % MOD

    # function: coefficients of (1 + v t)^m
    def binom_poly(m, v_val):
        if m == 0:
            return [1]
        res = [1] * (m + 1)
        for j in range(1, m + 1):
            # C(m, j) * v^j
            res[j] = res[j - 1] * (m - j + 1) % MOD
            res[j] = res[j] * inv[j] % MOD
            res[j] = res[j] * v_val % MOD
        return res

    # list of polynomials to multiply (only those with cnt>0)
    polys = []
    for d in range(1, 7):
        if cnt[d] > 0:
            polys.append((cnt[d], binom_poly(cnt[d], v[d])))

    # sort by length to keep intermediate degrees small
    polys.sort(key=lambda x: x[0])

    # multiply all factors to obtain F(t)
    F = [1]
    for _, poly in polys:
        F = multiply(F, poly)          # F now has length = current total degree + 1

    # F has length N+1, coefficients p[0..N]
    total = 0
    for d in range(1, 7):
        if cnt[d] == 0:
            continue
        # compute coefficients of H_d(t) = F(t) / (1 + v_d t)
        h = [0] * (N)                  # we need h[0..N-1]
        h[0] = F[0]
        for k in range(1, N):
            h[k] = (F[k] - v[d] * h[k - 1]) % MOD
        # integral of H_d from 0 to 1 = sum h[k] / (k+1)
        integral = 0
        for k in range(N):
            integral = (integral + h[k] * inv[k + 1]) % MOD
        total = (total + (S[d] % MOD) * integral) % MOD

    answer = fact[N] * total % MOD
    print(answer)


if __name__ == "__main__":
    main()
```

The program follows exactly the algorithm proven correct above and conforms to the required time and memory limits.
