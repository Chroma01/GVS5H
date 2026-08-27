**Solution Explanation**

For a permutation `P = (P1 , … , PN)` we write the decimal strings of the
numbers one after another

```
f(P) = integer represented by   str(P1)·str(P2)· … ·str(PN)
```

`len(i)` – number of decimal digits of `i` ( `len(10)=2` etc. )  
`b_i = 10^{len(i)} (mod M)`  (`M = 998244353`)

For a fixed permutation

```
f(P) = Σ i·10^{ Σ_{j after i} len(j) }
```

The exponent depends only on the set of numbers placed after `i`.

--------------------------------------------------------------------

#### 1.   The set behind a number

For a fixed `i`

```
S_i = Σ_{all permutations} 10^{ Σ_{j after i} len(j) }
```

Take the `N-1` other numbers.
Choose a subset `T` of them, `|T| = k`.  
All `k!` orders of `T` and all `(N-1‑k)!` orders of the rest give a
permutation where exactly the set `T` is behind `i`.

```
S_i = Σ_{T⊆[N]\{i}}  (N-1-|T|)!·|T|!· Π_{j∈T} b_j                (1)
```

Define the elementary symmetric sums

```
e_k = Σ_{|T|=k} Π_{j∈T} b_j               (including all N numbers)
e_k^{(i)} = same sum, but i is excluded
```

Then (1) becomes

```
S_i = Σ_{k=0}^{N-1}  (N-1-k)!·k!· e_k^{(i)}                     (2)
```

--------------------------------------------------------------------

#### 2.   The total answer

The required sum

```
Ans = Σ_{i=1}^{N} i·S_i
    = Σ_{k=0}^{N-1}  (N-1-k)!·k!  ·  Σ_i i·e_k^{(i)}           (3)
```

For the inner sum we use the identity  

```
e_k = e_k^{(i)} + b_i·e_{k-1}^{(i)}          (choose i or not)
```

Therefore

```
Σ_i i·e_k^{(i)} = total· e_k  –  Σ_i i·b_i·e_{k-1}^{(i)}    (4)
```

where `total = N(N+1)/2`.

Define  

```
F(t) = Π_{j=1}^{N} (1 + b_j·t) = Σ_{k=0}^{N} f_k·t^k
G(t) = Σ_{i=1}^{N} i·b_i·t· Π_{j≠i} (1 + b_j·t) = Σ_{k=0}^{N} g_k·t^k
```

From the definition

```
f_k = e_k
g_k = Σ_i i·b_i·e_{k-1}^{(i)}                         (5)
```

Insert (4) and (5) into (3).  
The factor `(N-1-k)!·k!` equals `k!·(N-1-k)!`.  
Using `(N-1)!·invC(N-1,k) = 1` the whole answer simplifies dramatically to

```
Ans = Σ_{k=0}^{N-1}  k!·(N-1-k)! · ( total·f_k  –  g_k )      (6)
```

All we need are the coefficients `f_k` (from `F`) and `g_k` (from `G`).

--------------------------------------------------------------------

#### 3.   Grouping equal `b_i`

`b_i` depends only on the number of digits of `i`.

```
L = 1 … 6   ( because N ≤ 2·10^5 )
c_L = #{ i | len(i)=L }          (0 ≤ c_L ≤ N)
a_L = 10^L  (mod M)
S_L = Σ_{i with len(i)=L} i      (mod M)
```

All numbers with the same length have the same factor
`(1 + a_L·t)`.  
Thus

```
F(t) = Π_{L} (1 + a_L·t)^{c_L}
     = Π_{L} Σ_{k=0}^{c_L} C(c_L,k)·a_L^k·t^k                (7)
```

The polynomial for a group is simply the binomial expansion,
all its coefficients are known in `O(c_L)` time.
Multiplying the at most six group‑polynomials gives `F` in
`O(N log N)` using an NTT (fast convolution).

--------------------------------------------------------------------

#### 4.   Computing `G(t)`

From the definition of `G`

```
G(t) = t·F(t)· Σ_{L} a_L·S_L· (1/(1 + a_L·t))                (8)
```

`1/(1 + a_L·t) = Σ_{m≥0} (-a_L)^m·t^m`.  
Only the first `N` powers are needed (the degree of `F` is `N`).

For each length `L`

```
term_L(t) = a_L·S_L· Σ_{m=0}^{N-1} (-a_L)^m·t^m
```

All `term_L` are summed – a simple `O(N·#groups)` loop.
Let `H(t) = Σ_L term_L(t)`.  
Finally

```
R(t) = F(t)·H(t)        (convolution, truncate to degree N-1)
g_k = coefficient of t^{k-1} in R(t)   (k≥1),   g_0 = 0
```

All convolutions are performed with the same NTT routine.

--------------------------------------------------------------------

#### 5.   Whole algorithm

```
read N
pre‑compute factorials and inverse factorials modulo M
for each possible length L (1 … 6)
        count c_L and sum S_L of the numbers with that length
        a_L = 10^L (mod M)
        build poly_L = (1 + a_L·t)^{c_L}  using binomial coefficients
        multiply it into F(t)  (truncate to degree N)
build H(t) = Σ_L a_L·S_L· Σ_{m=0}^{N-1} (-a_L)^m·t^m   (O(N·#groups))
R(t) = F(t) * H(t)   (NTT, keep first N coefficients)
g[0]=0 ;  for k=1..N-1 : g[k] = R[k-1]

answer = 0
total = N·(N+1)/2  (mod M)
for k = 0 … N-1
        term = ( total·F[k]  –  g[k] ) mod M
        answer += k!·(N-1-k)!·term   (mod M)
print answer
```

All steps are `O(N log N)` (the NTTs) and need `O(N)` memory.

--------------------------------------------------------------------

#### 6.   Correctness Proof  

We prove that the algorithm returns the required sum.

---

##### Lemma 1  
For a fixed number `i` the total contribution of `i` over all
permutations equals  

```
S_i = Σ_{k=0}^{N-1} (N-1-k)!·k!· e_k^{(i)}                (2)
```

**Proof.**  
Choose the set `T` of the `k` numbers that appear after `i`.  
`T` can be any `k`‑subset of the other `N-1` numbers.
All `k!` orders of `T` and all `(N-1-k)!` orders of the remaining
`N-1-k` numbers produce a distinct permutation where exactly `T`
is after `i`.  
The factor contributed by this permutation is `Π_{j∈T} b_j`.
Summation over all subsets gives the formula. ∎



##### Lemma 2  
Let `total = N(N+1)/2`. For every `k (0≤k≤N-1)`

```
Σ_{i=1}^{N} i·e_k^{(i)} = total·f_k  –  g_k                (4')
```

where `f_k = e_k` and `g_k` is defined by (5).

**Proof.**  
`e_k = e_k^{(i)} + b_i·e_{k-1}^{(i)}` (choose whether `i` belongs to the
subset). Multiplying by `i` and summing over `i`

```
Σ i·e_k^{(i)} = total·e_k  –  Σ i·b_i·e_{k-1}^{(i)} .
```

By definition of `g_k` the last sum is exactly `g_k`. ∎



##### Lemma 3  
For all `k (0≤k≤N-1)`

```
Ans = Σ_{k=0}^{N-1} k!·(N-1-k)!· ( total·f_k  –  g_k )   (6)
```

**Proof.**  
Starting from the definition of the answer and Lemma&nbsp;1

```
Ans = Σ_i i·S_i
    = Σ_i i· Σ_k (N-1-k)!·k!· e_k^{(i)}
    = Σ_k (N-1-k)!·k!· Σ_i i·e_k^{(i)} .
```

Insert Lemma&nbsp;2 and use `f_k = e_k`. ∎



##### Lemma 4  
`F(t) = Π_{j=1}^{N} (1 + b_j·t) = Σ_{k=0}^{N} f_k·t^k`
and `G(t) = Σ_{i} i·b_i·t· Π_{j≠i} (1 + b_j·t) = Σ_{k=0}^{N} g_k·t^k`.

**Proof.**  
Both statements are just the definitions of the elementary symmetric
sums `e_k` and of `g_k`. ∎



##### Lemma 5  
For every length `L` let `a_L = 10^L (mod M)`, `c_L` the amount of numbers
with that length and `S_L` their sum.
Then  

```
F(t) = Π_{L} (1 + a_L·t)^{c_L},
H(t) = Σ_{L} a_L·S_L· Σ_{m≥0} (-a_L)^m·t^m,
G(t) = t·F(t)·H(t)      (8)
```

**Proof.**  
All numbers with length `L` have the same factor `(1 + a_L·t)`, therefore
the whole product `F(t)` is the product over `L` of their `c_L`‑th powers,
which is the stated expression.

`G(t) = Σ_i i·b_i·t·Π_{j≠i}(1+b_j t)`.  
Group the terms by the length `L` of `i`.  
For a fixed `L` the inner product is `F(t)/(1+a_L t)`.  
All `i` of this length have the same `b_i = a_L` and their `i`‑values sum
to `S_L`.  Hence the contribution of length `L` is
`a_L·t·S_L·F(t)/(1+a_L t)`.  Summation over all lengths yields
`t·F(t)· Σ_L a_L·S_L· 1/(1+a_L t)`.  Using the geometric series
`1/(1+a_L t)= Σ_{m≥0} (-a_L)^m t^m` gives the formula for `H(t)`. ∎



##### Lemma 6  
The algorithm computes the coefficients `f_k` and `g_k` correctly.

**Proof.**  

*`f_k`* – By Lemma&nbsp;5 the product `F(t)` is exactly the product of the
group polynomials (7). The algorithm builds each group polynomial
by the binomial expansion and multiplies them, therefore the resulting
coefficients are the `f_k`.

*`g_k`* – Lemma&nbsp;5 expresses `G(t) = t·F(t)·H(t)`.  
The algorithm builds `H(t)` by the explicit sum of the truncated
geometric series, then computes `R(t) = F(t)·H(t)` (convolution, truncated
to degree `N-1`).  For `k≥1` the coefficient of `t^{k-1}` in `R(t)` is
exactly the coefficient of `t^k` in `G(t)`, i.e. `g_k`.  `g_0` is zero,
which the algorithm also sets. ∎



##### Lemma 7  
The value `ans` produced by the algorithm equals the right hand side of
(6).

**Proof.**  
The loop of the algorithm computes for every `k`

```
term = ( total·f_k – g_k )  (mod M)
add  k!·(N-1-k)!·term   to ans
```

which is exactly the sum (6). ∎



##### Theorem  
The algorithm outputs  

```
 Σ_{all permutations P of (1,…,N)}  f(P)   (mod 998244353)
```

**Proof.**  
By Lemma&nbsp;3 the desired sum equals the expression (6).  
Lemma&nbsp;6 shows that the algorithm obtains the needed coefficients
`f_k` and `g_k`.  
Lemma&nbsp;7 proves that the final accumulation equals (6).  
Therefore the printed value is exactly the required sum modulo `M`. ∎



--------------------------------------------------------------------

#### 7.   Complexity Analysis

* `c_L` and `S_L` – `O(N)`  
* building the at most six group polynomials – `O(N)`  
* multiplying them – `O(N log N)` (NTT)  
* building `H(t)` – `O(N·#groups) = O(N)`  
* final convolution `F * H` – `O(N log N)`  
* final accumulation – `O(N)`

Overall  

```
Time   :  O(N log N)      ( N ≤ 2·10^5 )
Memory :  O(N)
```

Both satisfy the limits.

--------------------------------------------------------------------

#### 8.   Reference Implementation  (Python 3)

```python
import sys

MOD = 998244353
ROOT = 3                     # primitive root for MOD

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

    # factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # groups by length
    max_len = len(str(N))
    cnt = [0] * (max_len + 1)      # c_L
    sum_grp = [0] * (max_len + 1)  # S_L
    a = [0] * (max_len + 1)        # a_L = 10^L mod MOD

    for L in range(1, max_len + 1):
        low = 10 ** (L - 1)
        high = 10 ** L - 1
        if low > N:
            break
        high = min(high, N)
        c = high - low + 1
        cnt[L] = c
        s = (low + high) * c // 2
        sum_grp[L] = s % MOD
        a[L] = pow(10, L, MOD)

    # build F(t) = product of (1 + a_L t)^{c_L}
    F = [1]  # start with constant polynomial
    need = N + 1
    for L in range(1, max_len + 1):
        c = cnt[L]
        if c == 0:
            continue
        al = a[L]
        # polynomial (1 + al t)^c
        poly = [0] * (c + 1)
        pow_al = 1
        fact_c = fact[c]
        for k in range(c + 1):
            binom = fact_c * inv_fact[k] % MOD * inv_fact[c - k] % MOD
            poly[k] = binom * pow_al % MOD
            pow_al = pow_al * al % MOD
        F = multiply(F, poly, need=need)
    # ensure length N+1
    if len(F) < need:
        F += [0] * (need - len(F))

    # build H(t) = Σ a_L * S_L * Σ_{m=0}^{N-1} (-a_L)^m t^m
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

    # R(t) = F(t) * H(t)  (need only first N coefficients)
    R = multiply(F, H, need=N)

    # g_k : g_0 = 0, g_k = R_{k-1} for k>=1
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
and conforms to the required time and memory limits.