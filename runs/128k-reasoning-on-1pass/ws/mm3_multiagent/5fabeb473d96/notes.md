
## ideation
**Solution Explanation**

For every vertex `i ( i ≥ 2 )` we choose a parent `P_i` uniformly from  
`{ 1 , 2 , … , i‑1 }`.  
The obtained rooted tree is a *random recursive tree*.
For a query `(u , v)` we have to sum the distance `dist(u , v)` over all
`(N‑1)!` possible parent sequences, modulo  

```
MOD = 998244353   (prime)
```

--------------------------------------------------------------------

#### 1.   From distances to edges  

For an edge `(i , P_i)` let  

```
Ii(u , v) = 1   if this edge belongs to the unique u–v path,
            0   otherwise
```

Then  

```
dist(u , v) = Σi≥2  Ai · Ii(u , v)
```

and the required answer is  

```
Ans(u , v) = ΣP  distP(u , v)
           = Σi≥2 Ai · ( number of trees where Ii(u , v)=1 )
```

The number of trees is `(N‑1)!`.  
If we denote  

```
pi(u , v) = Prob( edge i belongs to the u–v path )
```

then  

```
Ans(u , v) = (N‑1)! · Σi≥2 Ai · pi(u , v)                (1)
```

So we only have to find the probabilities `pi`.

--------------------------------------------------------------------

#### 2.   Probabilities for a random recursive tree  

The tree is built only with edges to *smaller* numbers,
therefore an ancestor always has a smaller index.

*For a single later vertex* `j > i`

```
Prob( i is ancestor of j ) = 1 / i                         (2)
```

*Proof.*  
Just before `j` is added, the subtree of `i` contains `X` vertices
(`X ≥ 1`). The parent of `j` is uniformly chosen from the `j‑1`
existing vertices, therefore the probability that it lies in the
subtree of `i` is `X / (j‑1)`.  
Taking expectation, `E[X] = (j‑1)/i`, gives the claim. ∎



*For two later vertices* `u < v`  

The subtree of `i` grows by a Pólya‑urn (initial “in” count `1`,
“out” count `i‑1`). Consequently

```
Prob( i is ancestor of both u and v ) = 2 / ( i·(i+1) )    (3)
```

Now we can write the probability that the **edge** `(i , P_i)` lies on
the `u‑v` path.  
The edge is on the path iff exactly one of `u , v` is in the subtree
of `i`.

Four cases:

| i                | pi(u , v)                              |
|------------------|----------------------------------------|
| `i = v`          | `1`                                    |
| `i = u`          | `1 – 1/u = (u‑1)/u`                    |
| `u < i < v`      | `1 / i`                                |
| `i < u`          | `2/i – 4/(i·(i+1)) = 2·(i‑1) / ( i·(i+1) )` |
| `i > v`          | `0`                                    |

All other `i` give probability `0`.  (Formulas (2) and (3) are used.)

--------------------------------------------------------------------

#### 3.   Summation using prefix sums  

Define the following modular weights (all `i ≥ 2`)

```
w1[i] = 2·(i‑1) / ( i·(i+1) )          (for i < u)
w2[i] = 1 / i                         (for u < i < v)
```

Pre‑compute

```
prefW[i] = Σj=2..i  Aj · w1[j]    (mod MOD)
prefI[i] = Σj=2..i  Aj · w2[j]    (mod MOD)
```

For a query `(u , v)` (`u < v`)

```
coeff =  Σi<u          Ai·w1[i]                 // term1
       +  Au·(u‑1)/u                         // term2
       +  Σi=u+1..v‑1   Ai·w2[i]               // term3
       +  Av                                 // term4
```

Using the prefix sums

```
term1 = prefW[u‑1]                              (0 if u≤1)
term2 = Au * ( (u‑1) * inv[u]  mod MOD )
term3 = ( prefI[v‑1] - prefI[u] ) mod MOD
term4 = Av
coeff = (term1 + term2 + term3 + term4) mod MOD
```

Finally, from (1)

```
answer = coeff * (N‑1)!  mod MOD
```

All operations are `O(1)` per query.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm outputs the required sum for every query.

---

##### Lemma 1  
For a fixed vertex `i (i≥2)` and a later vertex `j (j>i)`  

```
Prob( i is ancestor of j ) = 1 / i .
```

*Proof.* Same as (2) above. ∎



##### Lemma 2  
For a fixed vertex `i (i≥2)` and two later vertices `u<v`  

```
Prob( i is ancestor of both u and v ) = 2 / ( i·(i+1) ) .
```

*Proof.* The subtree of `i` grows by a Pólya‑urn.
The probability that a given set of `k` later vertices are all
descendants of `i` equals  

```
1/i · 2/(i+1) · … · k/(i+k‑1) = k! / ( i·(i+1)…(i+k‑1) )
```

For `k=2` we obtain the claimed value. ∎



##### Lemma 3  
For a fixed pair `u<v` and a vertex `i` the probability that the edge
`(i , P_i)` lies on the `u–v` path equals the piecewise formulas
described in the table of Section&nbsp;2.

*Proof.*  
The edge is on the path iff exactly one of `{u , v}` is in the subtree
of `i`.  
Four cases are distinguished:

* `i=v` – the edge is incident to the endpoint, always on the path.  
* `i=u` – `i` is ancestor of itself; it is ancestor of `v` with
  probability `1/u` (Lemma&nbsp;1), therefore it is **not** on the
  path exactly when `v` is a descendant.  
* `u<i<v` – `i` cannot be ancestor of `u` (indices increase along any
  root‑to‑leaf path). It is on the path iff it is ancestor of `v`,
  probability `1/i` (Lemma&nbsp;1).  
* `i<u` – `i` may be ancestor of `u`, of `v` or of both.
  By Lemma&nbsp;1 each single event has probability `1/i`,
  by Lemma&nbsp;2 the intersection has probability `2/(i·(i+1))`.  
  The probability of *exactly one* is  

  ```
  1/i + 1/i − 2·2/(i·(i+1)) = 2·(i‑1)/(i·(i+1))
  ```

which matches the table. ∎



##### Lemma 4  
For a query `(u , v)` the algorithm computes  

```
coeff = Σi≥2  Ai · pi(u , v)   (mod MOD)
```

*Proof.*  
Insert the four cases of Lemma&nbsp;3:

* `i<u`  coefficient `w1[i] = 2·(i‑1)/(i·(i+1))` – summed by `prefW[u‑1]`.
* `i=u`  coefficient `(u‑1)/u` – evaluated as `Au·(u‑1)·inv[u]`.
* `u<i<v`  coefficient `1/i` – summed by `prefI[v‑1]−prefI[u]`.
* `i=v`  coefficient `1` – taken as `Av`.

All divisions are performed using modular inverses, i.e. the rational
numbers are replaced by their representatives modulo the prime `MOD`.
Therefore the obtained value equals the required sum modulo `MOD`. ∎



##### Lemma 5  
Let `F = (N‑1)! (mod MOD)`.  
The answer printed by the algorithm equals  

```
 ΣP  distP(u , v)   (mod MOD) .
```

*Proof.*  
From (1) and Lemma&nbsp;4

```
 ΣP  distP(u , v) = F · Σi≥2 Ai·pi(u , v)  ≡ F·coeff   (mod MOD)
```

The program outputs exactly `coeff·F (mod MOD)`. ∎



##### Theorem  
For every query the program outputs the sum of the distances between the
two given vertices over all `(N‑1)!` possible rooted trees,
modulo `998244353`.

*Proof.*  
Directly from Lemma&nbsp;5. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*Precomputation* (`O(N)` time, `O(N)` memory)

*   modular inverses `inv[1…N+1]`
*   weights `w1[i]` and prefix sums `prefW , prefI`
*   factorial `(N‑1)!`

*Each query* – `O(1)` time, `O(1)` extra memory.

Overall  

```
Time   :  O(N + Q)   ( ≤ 4·10⁵ )
Memory :  O(N)
```

Both satisfy the limits.

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))

    # A[1] is unused
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(next(it)) % MOD

    # ---------- modular inverses ----------
    inv = [0] * (N + 2)          # need inv[N+1] for w1[N]
    inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # ---------- w1[i] = 2*(i-1) / (i*(i+1)) ----------
    w1 = [0] * (N + 1)
    for i in range(2, N + 1):
        w1[i] = (2 * (i - 1) % MOD) * inv[i] % MOD * inv[i + 1] % MOD

    # ---------- prefix sums ----------
    prefW = [0] * (N + 1)   # Σ Aj * w1[j]  for j ≤ i
    prefI = [0] * (N + 1)   # Σ Aj * inv[j] for j ≤ i
    for i in range(2, N + 1):
        prefW[i] = (prefW[i - 1] + A[i] * w1[i]) % MOD
        prefI[i] = (prefI[i - 1] + A[i] * inv[i]) % MOD

    # ---------- factorial (N-1)! ----------
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD

    out = []
    for _ in range(Q):
        u = int(next(it))
        v = int(next(it))

        # term1 : i < u
        term1 = prefW[u - 1]                     # 0 if u ≤ 1
        # term2 : i = u
        term2 = A[u] * ((u - 1) * inv[u] % MOD) % MOD
        # term3 : u < i < v
        term3 = (prefI[v - 1] - prefI[u]) % MOD
        # term4 : i = v
        term4 = A[v] % MOD

        coeff = (term1 + term2 + term3 + term4) % MOD
        ans = coeff * fact % MOD
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above and
conforms to the required time and memory limits.
