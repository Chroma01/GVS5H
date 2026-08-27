
## ideation
**Solution Explanation**

For a fixed board `m × n` let  

```
N = m·n   (total number of cells)
```

A *valid arrangement* is just a set of `k` different cells.  
For a concrete unordered pair of cells `{u , v}` the Manhattan distance `dist(u,v)`
appears in the total sum once for every arrangement that contains **both** `u` and `v`.

--------------------------------------------------------------------

#### 1.  How many arrangements contain a given pair?

The remaining `k‑2` cells can be chosen arbitrarily from the other `N‑2` cells, therefore

```
cnt = C(N‑2 , k‑2)                         (1)
```

--------------------------------------------------------------------

#### 2.  Sum of distances over **all** unordered cell pairs

The Manhattan distance is the sum of a row part and a column part

```
dist( (r1,c1) , (r2,c2) ) = |r1‑r2| + |c1‑c2|
```

*Row part* – choose two different rows `r1 < r2`.  
Their distance is `r2‑r1`. For each such row pair the columns can be any of the
`n` possibilities, independent for the two cells, i.e. `n²` pairs.
Hence

```
rowSum = n² · Σ_{0≤r1<r2<m} (r2‑r1)          (2)
```

The inner sum is a classic arithmetic sum

```
Σ_{r1<r2} (r2‑r1) = 1·(m‑1) + 2·(m‑2) + … + (m‑1)·1
                 = m·(m‑1)·(m+1) / 6
```

*Column part* is completely symmetric

```
colSum = m² · Σ_{0≤c1<c2<n} (c2‑c1) = m² · n·(n‑1)·(n+1) / 6
```

Therefore the total sum of distances over all unordered cell pairs is

```
T = n²·m·(m‑1)·(m+1) / 6  +  m²·n·(n‑1)·(n+1) / 6          (3)
```

Both numerators are multiples of `6`, so `T` is an integer.

--------------------------------------------------------------------

#### 3.  Final formula

From (1) and (3)

```
answer = C(N‑2 , k‑2)  ·  T          (4)
```

All computations are required modulo  

```
MOD = 1 000 000 007   (prime)
```

`T` can be taken modulo `MOD` first, then multiplied by the binomial coefficient.
Because the numerator of `T` is divisible by `6` we may multiply by the modular
inverse of `6` (`inv6 = 6^{MOD‑2} (mod MOD)`).

--------------------------------------------------------------------

#### 4.  Computing `C(N‑2 , k‑2)` modulo `MOD`

`N ≤ 10⁵`.  
Pre‑compute factorials `fact[i] = i! (mod MOD)` and inverse factorials
`invFact[i] = (i!)^{-1} (mod MOD)` for `0 ≤ i ≤ N`.  
Then

```
C(N‑2 , k‑2) = fact[N‑2] · invFact[k‑2] · invFact[N‑k]   (mod MOD)
```

--------------------------------------------------------------------

#### 5.  Correctness Proof  

We prove that the algorithm returns the required sum.

---

##### Lemma 1  
For any unordered pair of distinct cells `{u,v}` the number of valid
arrangements that contain both cells equals `C(N‑2 , k‑2)`.

**Proof.**  
Fix the two cells `u` and `v`. The remaining `k‑2` cells must be chosen from the
other `N‑2` cells, each at most once. The number of ways to do that is the
binomial coefficient `C(N‑2 , k‑2)`. ∎



##### Lemma 2  
The sum of Manhattan distances over **all** unordered cell pairs of an
`m × n` grid is the value `T` given by formula (3).

**Proof.**  
Separate the Manhattan distance into row and column contributions.

*Row part.*  
Take a pair of distinct rows `r1 < r2`. Their distance is `r2‑r1`.  
For any column choice `c1` for the first cell and `c2` for the second,
`c1` and `c2` can be any of the `n` columns, giving `n²` unordered cell pairs.
Thus the total contribution of this row pair is `(r2‑r1)·n²`. Summation over all
`r1<r2` yields (2). The closed form of the inner sum is a standard arithmetic
series and equals `m·(m‑1)·(m+1)/6`. Substituting gives the first term of (3).

*Column part* is symmetric, giving the second term of (3). Adding both parts
produces `T`. ∎



##### Lemma 3  
For the whole board the total sum of Manhattan distances over all valid
arrangements equals `C(N‑2 , k‑2) · T   (mod MOD)`.

**Proof.**  
By Lemma&nbsp;1 each unordered cell pair `{u,v}` contributes its distance
`dist(u,v)` exactly `C(N‑2 , k‑2)` times – once for each arrangement that
contains the pair. Summing over all unordered pairs gives

```
Σ_{pairs {u,v}} dist(u,v) · C(N‑2 , k‑2) = C(N‑2 , k‑2) · T .
```

The product is taken modulo `MOD`. ∎



##### Lemma 4  
The algorithm computes `T (mod MOD)` correctly.

**Proof.**  
Both terms of `T` are of the form  

```
A = X·Y·(Y‑1)·(Y+1) / 6
```

with `X,Y` equal to `m` or `n`.  
`A` is an integer because the numerator is a multiple of `6`.  
Modulo a prime `MOD` we have  

```
A (mod MOD) = (X·Y·(Y‑1)·(Y+1) (mod MOD)) · inv6 (mod MOD)
```

The algorithm performs exactly this computation for the row term and the
column term, then adds them (mod `MOD`). Hence the result equals `T (mod MOD)`. ∎



##### Lemma 5  
The algorithm computes `C(N‑2 , k‑2) (mod MOD)` correctly.

**Proof.**  
Factorials and inverse factorials are pre‑computed using Fermat’s little
theorem, which is valid because `MOD` is prime and none of the numbers
`1 … N` is divisible by `MOD`. The standard identity  

```
C(a,b) = a! · (b!)^{-1} · ((a‑b)!)^{-1}   (mod MOD)
```

holds, and the program uses `a = N‑2`, `b = k‑2`. ∎



##### Theorem  
`distanceSum(m,n,k)` returned by the algorithm equals the sum of Manhattan
distances over all valid arrangements of `k` pieces on an `m × n` board,
modulo `10⁹+7`.

**Proof.**  
By Lemma&nbsp;2 the value `T` is the sum of distances over all unordered cell
pairs. Lemma&nbsp;4 shows the algorithm evaluates `T (mod MOD)`.  
Lemma&nbsp;5 shows it evaluates the binomial coefficient `C(N‑2,k‑2) (mod MOD)`.  
Lemma&nbsp;3 states that the desired answer is exactly the product of those two
quantities. The algorithm multiplies them and reduces the result modulo `MOD`,
therefore it returns the required value. ∎



--------------------------------------------------------------------

#### 6.  Complexity Analysis  

```
N = m·n ≤ 10⁵
```

* Pre‑computing factorials and inverse factorials: `O(N)` time, `O(N)` memory.  
* Computing `T` and the binomial coefficient: `O(1)` time.  

Overall `O(N)` time and `O(N)` memory, well within the limits.

--------------------------------------------------------------------

#### 7.  Reference Implementation  (Python 3)

```python
import sys

MOD = 10**9 + 7
INV6 = pow(6, MOD - 2, MOD)          # modular inverse of 6

class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        N = m * n                     # total cells

        # ---------- pre‑compute factorials ----------
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i - 1] * i % MOD

        inv_fact = [1] * (N + 1)
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % MOD

        # ---------- binomial coefficient C(N-2, k-2) ----------
        # given constraints guarantee 0 <= k-2 <= N-2
        comb = (fact[N - 2] *
                inv_fact[k - 2] % MOD *
                inv_fact[N - k]) % MOD

        # ---------- compute T (sum of distances over all pairs) ----------
        m_mod = m % MOD
        n_mod = n % MOD

        # row term : n^2 * m * (m-1) * (m+1) / 6
        term1 = n_mod * n_mod % MOD
        term1 = term1 * m_mod % MOD
        term1 = term1 * ((m_mod - 1) % MOD) % MOD
        term1 = term1 * ((m_mod + 1) % MOD) % MOD
        term1 = term1 * INV6 % MOD

        # column term : m^2 * n * (n-1) * (n+1) / 6
        term2 = m_mod * m_mod % MOD
        term2 = term2 * n_mod % MOD
        term2 = term2 * ((n_mod - 1) % MOD) % MOD
        term2 = term2 * ((n_mod + 1) % MOD) % MOD
        term2 = term2 * INV6 % MOD

        T_mod = (term1 + term2) % MOD

        # ---------- final answer ----------
        return T_mod * comb % MOD
```

The program follows exactly the algorithm proven correct above and conforms to
the required `O(N)` time and memory limits.

## worker: finalize
- The total sum over all arrangements equals `C(N‑2, k‑2) * T`, where `N = m·n` and `T` is the sum of Manhattan distances over every unordered pair of cells.
- `T` is derived by separating row and column contributions:  
  `T = n²·m·(m‑1)·(m+1)/6 + m²·n·(n‑1)·(n+1)/6`.  
  Division by `6` is performed modulo `MOD` using its modular inverse.
- Binomial coefficient is computed with pre‑computed factorials and inverse factorials (Fermat’s little theorem, valid because `MOD` is prime).
- The algorithm runs in `O(N)` time for factorial pre‑computation and `O(1)` thereafter, with `O(N)` memory. Since `N ≤ 10⁵`, this easily satisfies the limits.
- Verified against the two provided examples (yields 8 and 20 respectively).
