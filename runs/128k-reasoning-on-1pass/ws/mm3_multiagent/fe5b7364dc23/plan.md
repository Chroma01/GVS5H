**Solution Explanation**

For a sub‑array `l … r`

```
sum(l,r) = A_l + A_{l+1} + … + A_r .
```

Let  

```
S_0 = 0
S_i = A_1 + A_2 + … + A_i   (1 ≤ i ≤ N) .
```

Then `sum(l,r) = S_r – S_{l-1}` and the required answer is

```
∑_{1 ≤ l ≤ r ≤ N} (S_r – S_{l-1})^K
 = ∑_{0 ≤ i < j ≤ N} (S_j – S_i)^K .
```

---

### Binomial expansion

```
(S_j – S_i)^K = ∑_{t=0..K} C(K,t) · S_j^t · (–S_i)^{K‑t}
             = ∑_{t=0..K} (–1)^{K‑t} C(K,t) · S_j^t · S_i^{K‑t}.
```

Define  

```
coeff[t] = (–1)^{K‑t} C(K,t)   (mod MOD) .
```

The answer becomes

```
Ans = ∑_{t=0..K} coeff[t] ·  ( ∑_{0 ≤ i < j ≤ N} S_j^t · S_i^{K‑t} )
```

---

### Computing the double sum in O(N·K)

For a fixed `j` the inner sum only depends on all previous
`i < j`.  
While scanning `j = 1 … N` we keep

```
acc[e] = ∑_{i = 0 … j‑1} S_i^e   (e = 0 … K) .
```

Initially only `i = 0` is present: `S_0 = 0`, so `acc[0] = 1` and
`acc[e>0] = 0`.

For the current `j`

```
cur[t] = S_j^t   (t = 0 … K)   – computed by one multiplication each.
```

The contribution of this `j` is

```
∑_{t=0..K} coeff[t] · cur[t] · acc[K‑t] .
```

After adding it to the answer we insert `S_j` into the accumulator:

```
acc[e] ← acc[e] + cur[e]   for all e .
```

Both steps need only `O(K)` time, therefore total complexity is
`O(N·K)`.  
`N ≤ 2·10^5`, `K ≤ 10`, easily fits.

All operations are performed modulo the prime `P = 998244353`.
Factorials and inverse factorials up to `K` are pre‑computed to obtain
the binomial coefficients.

---

### Correctness Proof  

We prove that the algorithm returns the required sum.

#### Lemma 1  
For any `0 ≤ i < j ≤ N`

```
(S_j – S_i)^K = ∑_{t=0..K} coeff[t] · S_j^t · S_i^{K‑t},
```

where `coeff[t] = (–1)^{K‑t}·C(K,t)` (taken modulo `P`).

*Proof.* Direct binomial expansion of `(S_j – S_i)^K` and grouping the
terms with `S_j^t` yields the formula. ∎



#### Lemma 2  
During the iteration for a fixed `j` the variable `acc[e]` equals
`∑_{i=0}^{j‑1} S_i^e` (mod `P`).

*Proof by induction on `j`.*  

*Base (`j=1`).* Before the loop `acc[0]=1=S_0^0` and `acc[e>0]=0=S_0^e`,
so the invariant holds.

*Induction step.* Assume the invariant holds for current `j`.  
After processing `j` we add `S_j^e` to each `acc[e]`. Hence after the
update

```
acc[e] = (∑_{i=0}^{j‑1} S_i^e) + S_j^e = ∑_{i=0}^{j} S_i^e ,
```

which is exactly the required value for the next `j+1`. ∎



#### Lemma 3  
For a fixed `j` the value added to `ans` by the algorithm equals

```
∑_{i=0}^{j‑1} (S_j – S_i)^K .
```

*Proof.* By Lemma&nbsp;2, at the moment the contribution of `j` is
computed we have `acc[K‑t] = ∑_{i=0}^{j‑1} S_i^{K‑t}`.  
The algorithm adds

```
∑_{t=0..K} coeff[t] · S_j^t · acc[K‑t]
 = ∑_{t=0..K} coeff[t] · S_j^t · (∑_{i=0}^{j‑1} S_i^{K‑t})
 = ∑_{i=0}^{j‑1} ∑_{t=0..K} coeff[t] · S_j^t · S_i^{K‑t}
 = ∑_{i=0}^{j‑1} (S_j – S_i)^K          (by Lemma 1) .
```

∎



#### Lemma 4  
After processing all `j = 1 … N` the variable `ans` equals
`∑_{0 ≤ i < j ≤ N} (S_j – S_i)^K`.

*Proof.* By Lemma 3 the contribution added at step `j` is exactly the
sum over all `i < j` of the same term. Summing these contributions for
`j = 1 … N` yields the double sum over all ordered pairs `(i,j)` with
`i < j`. ∎



#### Theorem  
The algorithm outputs  

```
∑_{1 ≤ l ≤ r ≤ N} ( A_l + … + A_r )^K   (mod 998244353) .
```

*Proof.* For any sub‑array `[l,r]` let `i = l‑1` and `j = r`. Then
`0 ≤ i < j ≤ N` and `S_j – S_i` equals the sub‑array sum. Conversely,
every pair `(i,j)` with `i<j` corresponds to exactly one sub‑array.
Therefore the required sum equals `∑_{0 ≤ i < j ≤ N} (S_j – S_i)^K`,
which by Lemma 4 is the value stored in `ans` after the loop. The
program prints `ans` modulo the prime, completing the proof. ∎



---

### Complexity Analysis

*Time* : For each of the `N` positions we perform `O(K)` operations
(building powers, updating accumulator, adding contributions).  
`O(N·K) ≤ 2·10^5·10 = 2·10^6` elementary steps.

*Memory* : The prefix array `S` (`N+1` integers) and a few vectors of
size `K+1`.  
`O(N + K)`, well below the limits.

---

### Reference Implementation (Python 3)

```python
import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # prefix sums modulo MOD
    S = [0] * (N + 1)
    for i in range(1, N + 1):
        S[i] = (S[i - 1] + A[i - 1]) % MOD

    # factorials and inverse factorials up to K
    fact = [1] * (K + 1)
    for i in range(1, K + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (K + 1)
    inv_fact[K] = pow(fact[K], MOD - 2, MOD)
    for i in range(K, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # coefficient[t] = (-1)^{K-t} * C(K, t) (mod MOD)
    coeff = [0] * (K + 1)
    for t in range(K + 1):
        c = fact[K] * inv_fact[t] % MOD * inv_fact[K - t] % MOD
        if (K - t) & 1:          # odd exponent → negative sign
            c = (-c) % MOD
        coeff[t] = c

    # acc[e] = sum_{i processed} S_i^e
    acc = [0] * (K + 1)
    acc[0] = 1                     # S_0^0 = 1, all other powers are 0

    cur = [1] * (K + 1)            # powers of current S_j
    ans = 0

    for j in range(1, N + 1):
        sj = S[j]
        # compute cur[t] = sj^t
        cur[0] = 1
        for t in range(1, K + 1):
            cur[t] = cur[t - 1] * sj % MOD

        # add contributions of this j
        for t in range(K + 1):
            term = coeff[t] * cur[t] % MOD * acc[K - t] % MOD
            ans = (ans + term) % MOD

        # insert S_j into the accumulator
        for e in range(K + 1):
            acc[e] = (acc[e] + cur[e]) % MOD

    print(ans % MOD)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.