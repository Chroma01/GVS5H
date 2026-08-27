**Solution Explanation**

For a sequence  

```
P = (P2 , P3 , … , PN)      ( 1 ≤ Pi ≤ i-1 )
```

the parent of vertex `i ( i≥2 )` is `Pi` and the edge `(i , Pi)` has weight `Ai`.
The vertex `1` is the root, therefore the obtained graph is a rooted tree.
For a fixed pair of vertices `u , v ( u < v )`

```
distP(u , v) = Σ  Ai        ( i is on the unique u–v path )
```

The required answer is

```
Ans(u , v) = ΣP  distP(u , v)    (mod 998244353)                (1)
```

`P` runs over all `(N‑1)!` possible sequences – every vertex `i` chooses a
parent among the earlier vertices uniformly.



--------------------------------------------------------------------

#### 1.   When does an edge belong to the u‑v path ?

The rooted tree is oriented from the root to the leaves.
For an edge `(i , parent(i))` (`i≥2`)

```
i is on the u‑v path  ⇔  exactly one of {u , v} lies in the subtree of i
```

(If both are in the subtree, the path goes above `i`;
if none is in the subtree, the path never reaches `i`).

Denote  

```
Ii(u , v) = 1   if i is on the u–v path,   else 0
```

Then from (1)

```
Ans(u , v) = Σi≥2   Ai ·  ΣP  Ii(u , v)                     (2)
```

`ΣP  Ii(u , v)` is the number of trees where `i` lies on the path,
i.e. the *expected* number multiplied by the number of trees.
Because the number of trees is the same for all `i`,
it is enough to know the **probability**

```
pi(u , v) = Prob( i is on the u–v path )
```

and finally

```
Ans(u , v) = (N‑1)! · Σi≥2  Ai · pi(u , v)    (mod MOD)      (3)
```

--------------------------------------------------------------------

#### 2.   The probability that a vertex is an ancestor of a later vertex

Construction of a random recursive tree :

```
for i = 2 … N
        choose parent of i uniformly among {1,…,i-1}
```

Only the relative order matters, therefore the process is **exchangeable**:
for any set `S ⊂ {i+1,…,N}` the probability that all vertices of `S`
are descendants of `i` depends only on `|S|`.

For a single vertex `j>i`

```
Prob( i is ancestor of j ) = 1 / i                (4)
```

*Proof.*  
Consider the moment just before `j` is attached.
Let `X` be the size of the subtree of `i` (including `i` itself).
`X` is at least `1`.  
The parent of `j` is chosen uniformly from the `j‑1` already existing
vertices, therefore the probability that it belongs to the subtree of `i`
equals `X / (j-1)`.  
Taking expectation over `X` gives `E[X] = (j-1)/i`,
hence the total probability is `1/i`. ∎



--------------------------------------------------------------------

#### 3.   Two vertices are both descendants of `i`

Let `i ≤ u < v`.  
Both events “`i` is ancestor of `u`” and “`i` is ancestor of `v`”
are positively correlated.
The process of the subtree of `i` is exactly a **Pólya‑urn**:

```
initial balls : 1 “in”   (the vertex i)      +   (i‑1) “out”
each new vertex j (j>i) :
        draw a ball uniformly,
        add a new ball of the same colour
```

Consequently the number of later vertices that become descendants of `i`
has a Beta‑binomial distribution.
A well known property of this urn is

```
Prob( a given set of k later vertices are all descendants of i )
        = k! / ( i·(i+1)·…·(i+k-1) )                     (5)
```

For `k = 2`

```
g(i) = Prob( i is ancestor of both u and v )
     = 2 / ( i·(i+1) )                                 (6)
```

--------------------------------------------------------------------

#### 4.   Exact value of `pi(u , v)`

We distinguish three cases.

*`i = v`*  
the edge `(v , parent(v))` is always on the path → `pi = 1`.

*`i = u`*  
`i` is always ancestor of itself,
it is ancestor of `v` with probability `1/u` (by (4)).
Hence  

```
pi = 1 – 1/u = (u‑1)/u                                 (7)
```

*`u < i < v`*  
`i` cannot be ancestor of `u` (it is larger), it is ancestor of `v`
with probability `1/i` (4).  
Therefore  

```
pi = 1 / i                                            (8)
```

*`i < u`*  
now `i` may be ancestor of `u`, of `v` or of both.
Using inclusion–exclusion and (4),(6)

```
pi = 2·(1/i) – 2·g(i)
    = 2/i – 4/(i·(i+1))
    = 2·(i‑1) / ( i·(i+1) )                           (9)
```

For completeness: `i > v` → `pi = 0`.

All formulas are **purely rational numbers**; after multiplying by
`(N‑1)!` they become integers, therefore we can safely work with them
modulo the prime `998244353` using modular inverses.



--------------------------------------------------------------------

#### 5.   Reducing the whole sum to prefix sums  

For a query `(u , v)` (`u < v`)

```
coeff(u , v) = Σi≥2  Ai · pi(u , v)
```

Insert the piecewise formulas (7)–(9) and collect the contributions

```
i < u                 :  Ai · 2·(i‑1) / ( i·(i+1) )
i = u                 :  Au · (u‑1) / u
u < i < v             :  Ai · 1 / i
i = v                 :  Av
```

All three remaining ranges are simple prefix sums.

Define for every `i (2 ≤ i ≤ N)`

```
w1[i] = 2·(i‑1) / ( i·(i+1) )   (mod MOD)
w2[i] = 1 / i                    (mod MOD)
```

Pre‑compute

```
prefW[i] = Σj=2..i   Aj · w1[j]          (mod MOD)
prefI[i] = Σj=2..i   Aj · w2[j]          (mod MOD)
```

(`prefW[0]=prefW[1]=prefI[0]=prefI[1]=0`)

Now a query is answered in O(1)

```
term1 = prefW[u-1]                                 // i < u
term2 = Au * ( (u-1) * inv[u]  mod MOD )           // i = u   (omit if u=1)
term3 = ( prefI[v-1] - prefI[u] ) mod MOD          // u < i < v
term4 = Av                                          // i = v

coeff = ( term1 + term2 + term3 + term4 ) mod MOD
answer = coeff * fact[N-1]  mod MOD
```

`fact[N-1] = (N-1)!  (mod MOD)` is pre‑computed once.

All operations are O(1) per query, the whole algorithm works in  
`O(N + Q)` time and `O(N)` memory.



--------------------------------------------------------------------

#### 6.   Correctness Proof  

We prove that the algorithm returns the required sum for every query.

---

##### Lemma 1  
For a fixed `i (i≥2)` and a later vertex `j (j>i)`  

```
Prob( i is ancestor of j ) = 1 / i .
```

**Proof.**  
Exactly the argument of section&nbsp;2. ∎



##### Lemma 2  
For a fixed `i (i≥2)` and two later vertices `u<v`  

```
Prob( i is ancestor of both u and v ) = 2 / ( i·(i+1) ) .
```

**Proof.**  
The subtree of `i` grows by a Pólya‑urn with initial “in” count `1`
and “out” count `i‑1`.  
The probability that a given set of `k` later vertices are all “in”
equals the product of the successive conditional probabilities

```
1/i  ·  2/(i+1)  ·  …  ·  k/(i+k-1) = k! / (i·(i+1)…(i+k-1))
```

(see any textbook on the Pólya urn).
For `k=2` we obtain `2 / ( i·(i+1) )`. ∎



##### Lemma 3  
For a fixed pair `u<v` and a vertex `i` the probability that the edge
`(i , parent(i))` belongs to the `u–v` path equals the piecewise
formulas (7)–(9).

**Proof.**  

*`i = v`* – the edge is incident to the endpoint `v`, therefore it is
always on the path, `pi = 1`.

*`i = u`* – `i` is ancestor of itself, it is ancestor of `v` exactly when
`i` is ancestor of `v`.  
By Lemma&nbsp;1 this happens with probability `1/u`, consequently
`pi = 1 – 1/u = (u‑1)/u`.

*`u < i < v`* – because `i > u`, `i` can never be an ancestor of `u`.
It is on the path iff it is an ancestor of `v`; by Lemma&nbsp;1 this
probability is `1/i`.

*`i < u`* – `i` can be ancestor of `u`, of `v` or of both.
By Lemma&nbsp;1 each single event has probability `1/i`,
by Lemma&nbsp;2 the intersection has probability `2/(i·(i+1))`.
Hence

```
pi = 1/i + 1/i – 2· 2/(i·(i+1))
    = 2/i – 4/(i·(i+1))
    = 2·(i‑1) / ( i·(i+1) ) .
```
∎



##### Lemma 4  
For a query `(u , v)` the algorithm computes  

```
coeff(u , v) = Σi≥2  Ai · pi(u , v)    (mod MOD)
```

**Proof.**  
According to Lemma&nbsp;3 the sum splits exactly into the four ranges
handled by the algorithm:

* `i < u`   – coefficient `w1[i] = 2·(i‑1)/(i·(i+1))`,
  summed by `prefW[u‑1]`.
* `i = u`   – coefficient `(u‑1)/u`,
  evaluated as `Au * (u‑1) * inv[u]`.
* `u < i < v` – coefficient `1/i`,
  summed by `prefI[v‑1] – prefI[u]`.
* `i = v`   – coefficient `1`,
  taken as `Av`.

All arithmetic is performed modulo a prime, i.e. the rational numbers are
replaced by their modular equivalents.
Therefore the obtained `coeff` equals the required sum modulo `MOD`. ∎



##### Lemma 5  
Let  

```
F = (N‑1)!  (mod MOD) .
```

The answer printed by the algorithm equals  

```
 ΣP  distP(u , v)   (mod MOD) .
```

**Proof.**  
From (2) and (3)

```
 ΣP  distP(u , v) = (N‑1)! · Σi≥2  Ai · pi(u , v)   (mod MOD) .
```

By Lemma&nbsp;4 the inner sum is exactly the variable `coeff`
computed by the program, and the program multiplies it by `F`.
Thus the printed value equals the desired sum. ∎



##### Theorem  
For every query `(u_i , v_i)` the program outputs the sum of the
distances between the two vertices over all `(N‑1)!` possible rooted
trees, modulo `998244353`.

**Proof.**  
Directly from Lemma&nbsp;5. ∎



--------------------------------------------------------------------

#### 7.   Complexity Analysis  

*Precomputation*  

* `inv[1…N+1]` – `O(N)` time, `O(N)` memory  
* `w1[2…N]`, `prefW`, `prefI` – `O(N)` time, `O(N)` memory  
* factorial `(N‑1)!` – `O(N)` time, `O(1)` memory  

*Each query* – `O(1)` time, `O(1)` extra memory.

Overall  

```
Time   :  O(N + Q)    ( ≤ 4·10⁵ )
Memory :  O(N)
```

Both satisfy the limits.



--------------------------------------------------------------------

#### 8.   Reference Implementation  (Python 3)

```python
import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))

    A = [0] * (N + 1)          # 1‑based, A[1] unused
    for i in range(2, N + 1):
        A[i] = int(next(it)) % MOD

    # ---------- modular inverses ----------
    inv = [0] * (N + 2)        # need up to N+1
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # ---------- w1[i] = 2*(i-1) / (i*(i+1)) ----------
    w1 = [0] * (N + 1)        # only i >= 2 are used
    for i in range(2, N + 1):
        w1[i] = (2 * (i - 1) % MOD) * inv[i] % MOD * inv[i + 1] % MOD

    # ---------- prefix sums ----------
    prefW = [0] * (N + 1)      # prefW[i] = sum_{j=2..i} A[j] * w1[j]
    prefI = [0] * (N + 1)      # prefI[i] = sum_{j=2..i} A[j] * inv[j]
    for i in range(2, N + 1):
        prefW[i] = (prefW[i - 1] + A[i] * w1[i]) % MOD
        prefI[i] = (prefI[i - 1] + A[i] * inv[i]) % MOD

    # ---------- factorial (N-1)! ----------
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out_lines = []
    for _ in range(Q):
        u = int(next(it))
        v = int(next(it))

        if u == 1:
            # term1 = term2 = 0
            term3 = prefI[v - 1]                     # sum_{i=2}^{v-1} A[i]/i
            term4 = A[v] % MOD
            coeff = (term3 + term4) % MOD
        else:
            term1 = prefW[u - 1]                     # i < u
            # i = u
            term2 = A[u] * ((u - 1) * inv[u] % MOD) % MOD
            # u < i < v
            term3 = (prefI[v - 1] - prefI[u]) % MOD
            if term3 < 0:
                term3 += MOD
            term4 = A[v] % MOD
            coeff = (term1 + term2 + term3 + term4) % MOD

        ans = coeff * fact % MOD
        out_lines.append(str(ans))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required time and memory limits.