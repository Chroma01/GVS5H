**Solution Explanation**

For every vertex `i`

* weight                : `W[i]`
* interval on a line   : `[L[i] , R[i]]`   (both ends are included)

```
edge (i , j)  ⇔  the two intervals are disjoint
                ⇔  R[i] < L[j]   or   R[j] < L[i]                (1)
```

The graph is the *comparability graph* of the strict partial order

```
i < j   ⇔   R[i] < L[j]                 (i is completely left of j)
```

--------------------------------------------------------------------

#### 1.   When does a path exist ?

*If the two intervals are disjoint* – by (1) they are adjacent, a
direct edge exists, the answer is `W[s] + W[t]`.

*If the intervals intersect* (`s` and `t` overlap)

```
   s ──► a ──► b ──► t          (a and b are intermediate vertices)
```

`a` must be disjoint from `s` → `a` is left of `s` (`R[a] < L[s]`)
or right of `s` (`L[a] > R[s]`).  
`b` must be disjoint from `t` → `b` is left of `t` (`R[b] < L[t]`)
or right of `t` (`L[b] > R[t]`).

The two edges of the path must also be disjoint.
Because the original intervals overlap we have `L[s] ≤ R[t]` and
`L[t] ≤ R[s]`.  
Consequently

* `a` left of `s`  **and** `b` right of `t`  ⇒ `a` and `b` are disjoint
* `a` right of `s` **and** `b` left of `t`   ⇒ `a` and `b` are disjoint

All other possibilities (both on the same side) need a third vertex
which would add a positive weight and can never be optimal.
So **every shortest path uses at most two intermediate vertices** and
its shape is one of the three

```
1) a single vertex outside the union of s and t
2) a left‑of‑s vertex  + a right‑of‑t vertex
```

`a` and `b` may also be outside the union, in that case the path
has length two (the same as case 1).

--------------------------------------------------------------------

#### 2.   Minimal weight

All weights are positive, therefore a shorter path is never heavier.
Only the three possibilities above have to be examined.

```
let  leftS   = minimum W[i] with  R[i] < L[s]        (i left of s)
let  rightT  = minimum W[i] with  L[i] > R[t]        (i right of t)

let  outL    = minimum W[i] with  R[i] < min(L[s],L[t])   (left of the union)
let  outR    = minimum W[i] with  L[i] > max(R[s],R[t])   (right of the union)

candidate 1 (one outside vertex) :
        if outL or outR exists →  W[s] + W[t] + min(outL,outR)

candidate 2 (left of s  +  right of t) :
        if leftS and rightT exist →  W[s] + W[t] + leftS + rightT
```

The answer is the minimum existing candidate, `-1` if none exists.

--------------------------------------------------------------------

#### 3.   Queries in O(log N)

The only operations needed are minima of intervals whose right end
is ≤ a given value and minima of intervals whose left end is ≥ a given
value.

* sort all intervals by `R` → `R[]`
  prefix minima `prefR[i] = min_{k≤i} W[k]`
* sort all intervals by `L` → `L[]`
  suffix minima `sufL[i] = min_{k≥i} W[k]`

For a value `x`

```
min weight with R ≤ x      = prefR[ largest i with R[i] ≤ x ]      (binary search)
min weight with L ≥ x      = sufL [ smallest i with L[i] ≥ x ]      (binary search)
```

Both queries need `O(log N)`.  
For each of the `Q` queries we perform at most six such queries,
overall `O((N+Q) log N)` time and `O(N)` memory.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm prints the required answer for every
query.

---

##### Lemma 1  
If intervals `s` and `t` are disjoint then they are adjacent in `G`
and the minimum possible path weight equals `W[s]+W[t]`.

**Proof.**  
Disjoint means `R[s] < L[t]` or `R[t] < L[s]`; by definition (1) the
edge exists.  
All vertex weights are positive, any path containing an additional
vertex adds at least its weight, therefore a direct edge is optimal. ∎



##### Lemma 2  
Assume intervals `s` and `t` intersect.
Every `s‑t` path contains a vertex that is either

* left of **both** (`R < min(L[s],L[t])`), or
* right of **both** (`L > max(R[s],R[t])`), or
* a vertex left of `s` **and** a vertex right of `t`.

**Proof.**  
Because `s` and `t` intersect, they are not adjacent, therefore any
path has at least one intermediate vertex.

*If the first intermediate vertex `x` is left of `s`*  
(`R[x] < L[s]`).  
If also `R[x] < L[t]` then `x` is left of both and we are done.
Otherwise `x` intersects `t`.  
Since the path must reach `t`, some later vertex `y` is disjoint from
`t`; the first such vertex must be right of `t`.  
Thus we have a vertex left of `s` (`x`) and a vertex right of `t` (`y`).

*If the first intermediate vertex `x` is right of `s`* the symmetric
argument gives a vertex right of `s` and a vertex left of `t`.  
The right‑of‑`s` vertex is also right of the union because
`R[s] ≥ max(R[s],R[t])`, i.e. it is the “right of both’’ case. ∎



##### Lemma 3  
For intersecting `s` and `t` a path with minimum total weight is either

* a single vertex `u` with `R[u] < min(L[s],L[t])` or `L[u] > max(R[s],R[t])`,
* or two vertices `a , b` with `R[a] < L[s]` and `L[b] > R[t]`.

**Proof.**  
By Lemma&nbsp;2 every `s‑t` path contains a vertex satisfying one of the
three listed properties.
If the path already contains a vertex left of **both** (or right of
**both**) we may delete all other intermediate vertices and obtain a
shorter `s‑u‑t` path, whose weight is not larger because all
`W` are positive.
If the path contains a vertex left of `s` and a vertex right of `t`,
the sub‑path between them consists of pairwise disjoint vertices,
hence any two of them are adjacent.  Removing the whole sub‑path and
keeping only the leftmost and the rightmost vertex yields a path
`s‑a‑b‑t` of the described form, again not heavier. ∎



##### Lemma 4  
For intersecting `s` and `t` the algorithm returns exactly the minimum
weight among the two possibilities of Lemma&nbsp;3.

**Proof.**  

*Outside vertex*  
`outL` (resp. `outR`) is the minimum weight among all intervals with
`R < min(L[s],L[t])` (resp. `L > max(R[s],R[t])`).
If at least one of them exists, the algorithm forms the candidate
`W[s] + W[t] + min(outL,outR)`, which is the weight of the best
single‑vertex path of Lemma&nbsp;3.

*Two‑vertex path*  
`leftS` is the minimum weight among all intervals left of `s`
(`R < L[s]`).  
`rightT` is the minimum weight among all intervals right of `t`
(`L > R[t]`).  
If both exist, the algorithm forms the candidate
`W[s] + W[t] + leftS + rightT`.  
Choosing the leftmost interval of weight `leftS` and the rightmost of
weight `rightT` gives a concrete `s‑a‑b‑t` path, therefore the candidate
is attainable and is the smallest possible weight of a two‑vertex
path of Lemma&nbsp;3.

The algorithm finally takes the minimum of the existing candidates,
hence returns the smallest possible weight among all optimal paths. ∎



##### Lemma 5  
If intervals `s` and `t` intersect and none of the three quantities
`outL , outR , leftS+rightT` exists, then `s` and `t` are disconnected
in `G`.

**Proof.**  
`outL` missing ⇒ no interval left of both.  
`outR` missing ⇒ no interval right of both.  
`leftS` missing ⇒ no interval left of `s`.  
`rightT` missing ⇒ no interval right of `t`.  
Consequently there is **no** vertex left of `s` and no vertex right of
`t`.  By Lemma&nbsp;2 any `s‑t` path would need either a vertex left of
both, a vertex right of both, or a left‑of‑`s` together with a right‑of‑`t`
vertex – all impossible.  Hence no path exists. ∎



##### Theorem  
For every query `(s,t)` the algorithm outputs

* `-1` iff `s` and `t` are disconnected in `G`,
* otherwise the minimum possible weight of an `s‑t` path.

**Proof.**  

*If `s` and `t` are disjoint* – Lemma&nbsp;1 shows the algorithm prints
`W[s]+W[t]`, the correct minimum.

*If `s` and `t` intersect* –  
If the algorithm finds at least one candidate, Lemma&nbsp;4 proves the
printed value equals the minimum weight of all paths.  
If it finds none, Lemma&nbsp;5 proves that no path exists, so the
algorithm correctly prints `-1`. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis  

*Pre‑processing*  

* sorting by `R` and building prefix minima – `O(N log N)`
* sorting by `L` and building suffix minima – `O(N log N)`

*Each query*  

* up to six binary searches (`O(log N)`) and a few constant‑time
  operations – `O(log N)`

Overall  

```
Time   :  O((N + Q) · log N)      ( ≤ 2·10⁵·log 2·10⁵  easily fits )
Memory :  O(N)    (arrays of size N)
```

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys
import bisect

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    N = next(it)
    W = [0] * N
    for i in range(N):
        W[i] = next(it)
    L = [0] * N
    R = [0] * N
    for i in range(N):
        L[i] = next(it)
        R[i] = next(it)

    # sort by right endpoint
    intervals_by_R = sorted(((R[i], W[i]) for i in range(N)), key=lambda x: x[0])
    sorted_R = [r for r, _ in intervals_by_R]
    pref_min_R = [0] * N
    for i, (_, w) in enumerate(intervals_by_R):
        pref_min_R[i] = w if i == 0 else min(pref_min_R[i - 1], w)

    # sort by left endpoint
    intervals_by_L = sorted(((L[i], W[i]) for i in range(N)), key=lambda x: x[0])
    sorted_L = [l for l, _ in intervals_by_L]
    suf_min_L = [0] * N
    for i in range(N - 1, -1, -1):
        _, w = intervals_by_L[i]
        suf_min_L[i] = w if i == N - 1 else min(suf_min_L[i + 1], w)

    INF = 10 ** 18

    def query_R(x: int) -> int:          # min weight with R <= x
        idx = bisect.bisect_right(sorted_R, x) - 1
        return pref_min_R[idx] if idx >= 0 else INF

    def query_L(y: int) -> int:          # min weight with L >= y
        idx = bisect.bisect_left(sorted_L, y)
        return suf_min_L[idx] if idx < N else INF

    Q = next(it)
    out_lines = []
    for _ in range(Q):
        s = next(it) - 1
        t = next(it) - 1
        if R[s] < L[t] or R[t] < L[s]:          # disjoint, direct edge
            out_lines.append(str(W[s] + W[t]))
            continue

        # overlapping intervals
        # left of s
        leftS = query_R(L[s] - 1)
        # right of t
        rightT = query_L(R[t] + 1)

        # outside the union
        outL = query_R(min(L[s], L[t]) - 1)
        outR = query_L(max(R[s], R[t]) + 1)
        best = INF
        if outL != INF or outR != INF:
            best = W[s] + W[t] + min(outL, outR)
        if leftS != INF and rightT != INF:
            cand = W[s] + W[t] + leftS + rightT
            if cand < best:
                best = cand

        out_lines.append(str(best if best != INF else -1))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input and output format.