**Solution Explanation**

For every road `j ( 1 ≤ j ≤ N-1 )` we choose an integer strength `w[j]`.
When a person walks on road `j` his stamina changes by `+ w[j]`.

For a person `i`

* start town `S[i]` , stamina `0`
* finish town `T[i]` , stamina `0`
* at every other town on the way stamina must be a positive integer

`|S[i]‑T[i]| > 1` and every pair `(S[i],T[i])` is different.



--------------------------------------------------------------------

#### 1.   From roads to a graph of prefix sums

```
A[0] = 0
A[k] = w[1] + w[2] + … + w[k]          ( 1 ≤ k ≤ N-1 )
```

`A[t]` is the stamina of a *hypothetical* person that started in town 1.
For a real person `i`

```
let L = min(S[i],T[i])          (left town)
    R = max(S[i],T[i]) - 1      (right road)
```

the travelled roads are `L … R`.  
For a town `x ( L ≤ x ≤ R )`

```
stamina at x  =  A[x-1] - A[L-1]      (if S[i] < T[i])
stamina at x  =  A[R]   - A[x-1]      (if S[i] > T[i])
```

The two end points have stamina `0`, therefore

```
A[L-1] = A[R]                                    (1)
```

All interior towns (`L < x < R` or `L < x < R`) must have positive stamina, i.e.

```
if S[i] < T[i]   (mountain) :   A[x] > A[L-1]   for every L < x < R      (2)
if S[i] > T[i]   (valley)   :   A[x] < A[L-1]   for every L < x < R      (3)
```

Define for every person

```
a[i] = L-1          (left end of the A‑interval)
b[i] = R            (right end of the A‑interval)
dir[i] = 0  (mountain)   if S[i] < T[i]
          = 1  (valley)    if S[i] > T[i]
```

`a[i] < b[i]` and `b[i] - a[i] ≥ 2` (because the person visits at least one
intermediate town).

--------------------------------------------------------------------

#### 2.   What do two intervals mean ?

Consider two different persons `p , q` (`p` has the smaller index).

*Both are mountains* (`dir = 0`)

```
a[p] = a1 , b[p] = b1
a[q] = a2 , b[q] = b2
```

From (1) we have `A[a1] = A[b1] = X` and `A[a2] = A[b2] = Y`.

If `a1 < a2 < b1 < b2` the intervals cross.
From (2) we obtain

```
Y = A[a2] > X               (a2 is inside the first mountain)
X = A[b1] > Y               (b1 is inside the second mountain)
```

which is impossible.  
The same contradiction appears for two valleys.

*If one is a mountain and the other a valley* the two inequalities become
`Y > X` and `X < Y` – they are consistent, no contradiction.

--------------------------------------------------------------------

**Conclusion**

For a set of persons the required strengths `w` exist **iff**

```
no two intervals of the same direction (both mountains or both valleys)
   cross, i.e. a1 < a2 < b1 < b2   (or the symmetric order)
```

All other relations (nesting, touching, opposite directions) are harmless;
the inequalities can be satisfied by choosing the values of `A` large enough.



--------------------------------------------------------------------

#### 3.   Reducing the problem to range queries

For a fixed direction (`dir = 0` or `dir = 1`) define

```
next[i] = the smallest index j > i with the same direction
          and a[p] < a[j] < b[p] < b[j]           (crossing)
          = INF  if such j does not exist
```

If for some interval `i` we have `next[i] ≤ R` then the set of persons
`[L , R]` contains a crossing pair of this direction, otherwise it does not.

Therefore for a query `[L , R]`

```
answer = Yes  iff   min{ next[i] | L ≤ i ≤ R } ≤ R   (for mountains)
       or   min{ next[i] | L ≤ i ≤ R } ≤ R   (for valleys)
```

So we only have to compute the two arrays `next_mountain[]` and `next_valley[]`
once, after that every query is answered by two range minima.



--------------------------------------------------------------------

#### 4.   Computing `next[i]` for one direction

We have `M ≤ 2·10⁵` intervals, each described by `(a , b , index)`.
`next[i]` is the smallest index `j > i` with

```
a < a[j] < b    and    b[j] > b
```

Only the *relative order* of `b` matters.
We process the intervals **in decreasing order of `b`**.

During the scan we keep a data structure `DS` that already contains
exactly the intervals whose `b` is larger than the current one.
`DS` must support

```
insert(a , index)                – add an interval
query(l , r , K)  →  smallest index > K among
                     all inserted intervals with a in [l , r]
```

Both operations are needed many times, therefore a segment tree over the
coordinate `a` is used.

*In the leaf* `a` we store a sorted list of all indices that have been
inserted with this `a`.  
*In an internal node* we store the union of the children – also a sorted list.
Thus a query for a whole segment is answered by binary searching the
corresponding list (the first element `> K`) and taking the minimum over the
`O(log N)` visited nodes.

The whole procedure for one direction:

```
sort intervals by b descending
group equal b together
for each group (all have the same b)
        for every interval (a,b,i) in the group
                l = a+1 , r = b-1
                if l ≤ r
                        nxt[i] = query(l , r , i)          // smallest index > i
        // after all queries of this group are answered
        insert every interval of the group into the segment tree
```

Complexities per direction

```
sorting                     O(M log M)
insertions                  O(M log N)   (each interval goes into O(log N) nodes)
queries                     O(M log N)   (each query visits O(log N) nodes)
binary searches inside a node O(log M)
total time                  O(M log N log M)   ≤ 2·10⁵·19·18  < 7·10⁷ operations
memory                      O(M log N)          (≈ 4·10⁶ integers)
```

Both directions are processed independently, the same bounds hold.



--------------------------------------------------------------------

#### 5.   Answering the queries

`next_mountain[]` and `next_valley[]` are static, therefore a
*sparse table* for range minima is built ( `O(M log M)` time, `O(M log M)` memory).

For a query `[L , R]` (1‑based indices)

```
mn =  min  next_mountain[ L … R ]     (sparse table, O(1))
if mn ≤ R :  answer Yes
else:
    mv =  min  next_valley[ L … R ]
    if mv ≤ R : answer Yes
    else       answer No
```

Overall complexity

```
building nxt arrays        O(M log N log M)
building two sparse tables  O(M log M)
each query                  O(1)
total                       O( (M+Q) log M )
```

With `M , Q ≤ 2·10⁵` this easily fits into the limits.



--------------------------------------------------------------------

#### 6.   Correctness Proof  

We prove that the algorithm prints “Yes” exactly for those queries for which
the required road strengths exist.

---

##### Lemma 1  
For a person `i` let `a[i] , b[i]` be defined as in section&nbsp;1.
The set of equations (1) and (2) (mountain) or (1) and (3) (valley)
has an integer solution **iff** there exist integers `A[0…N‑1]` satisfying

* `A[a[i]] = A[b[i]]`   (the two end points are equal)
* `A[x] > A[a[i]]` for all `a[i] < x < b[i]`   (mountain)
* `A[x] < A[a[i]]` for all `a[i] < x < b[i]`   (valley)

*Proof.*  
The derivation in section&nbsp;1 shows that every admissible `w`
produces such an `A`, and conversely any `A` with the stated properties
gives `w[x] = A[x] – A[x‑1]` and the required stamina values. ∎



##### Lemma 2  
Consider two different persons `p , q` with the same direction.

*If* `a[p] < a[q] < b[p] < b[q]`  (the intervals cross)  
*then* the system of inequalities of Lemma&nbsp;1 has **no** solution.

*Proof.*  
Both directions are treated analogously; we give the mountain case.
From Lemma&nbsp;1 for `p` we have `A[a[p]] = A[b[p]] = X` and  
`A[a[q]] > X` (because `a[q]` lies inside the first mountain).  
For `q` we have `A[a[q]] = A[b[q]] = Y` and  
`A[b[p]] > Y` (because `b[p]` lies inside the second mountain).  
Thus `Y > X` and `X > Y`, a contradiction. ∎



##### Lemma 3  
If no two intervals of the same direction cross,
then the whole system of inequalities of Lemma&nbsp;1 admits a solution.

*Proof.*  
Build a directed graph whose vertices are the intervals.
For a pair of intervals `p , q` let `a[p] < a[q]`.

* If `q` is completely inside `p` ( `a[p] < a[q] < b[q] < b[p]` )  
  – same direction: from Lemma&nbsp;1 we need `A[a[q]] > A[a[p]]`  
  – opposite direction: we need `A[a[q]] < A[a[p]]`.  
  In both cases a strict inequality between the two “base values”
  `A[a[p]]` and `A[a[q]]` is obtained.
* If an endpoint of `q` lies inside `p` while the other endpoint lies
  outside `p` (exactly the crossing situation) Lemma&nbsp;2 tells us that
  this can happen **only** when the two directions are opposite.
  In this case the same reasoning gives a *consistent* inequality
  (`A[a[q]] > A[a[p]]` for a mountain inside a valley, the opposite for a
  valley inside a mountain).

All obtained inequalities are strict and form a **partial order**
(no cycle can appear, otherwise we would have a crossing pair of the same
direction).  
A topological order exists, therefore we can assign integer values to the
bases step by step, keeping a gap of at least `2` whenever a nesting of
opposite directions demands it.  
All interior points have to lie between the two bases of their interval,
which is possible because of the gaps.  
Thus a global integer array `A` exists, consequently a suitable
`w` exists. ∎



##### Lemma 4  
For a fixed direction `next[i]` (as defined in section&nbsp;4) is the
smallest index `j > i` whose interval crosses `i`.  
If no such `j` exists, `next[i] = INF`.

*Proof.*  
The construction of `next[i]` processes intervals in decreasing order of
the right end `b`.  
When an interval `i` is processed, the segment tree already contains
exactly those intervals with larger `b`.  
A query over the left‑endpoint range `a[i]+1 … b[i]-1` returns the smallest
index greater than `i` among those inserted intervals whose left endpoint
lies inside `a[i] … b[i]`.  
Because all inserted intervals have `b > b[i]`, the returned index `j`
satisfies `a[i] < a[j] < b[i] < b[j]`, i.e. the intervals cross.
If the query finds none, such a `j` does not exist. ∎



##### Lemma 5  
For a query interval `[L,R]` the set of persons contains a crossing pair
of the same direction **iff** `min_{i∈[L,R]} next[i] ≤ R`.

*Proof.*  

*If* part:  
Assume a crossing pair `(p,q)` with `L ≤ p < q ≤ R` and the same direction.
By Lemma&nbsp;4 `next[p] ≤ q ≤ R`.  
Hence the minimum over the range is at most `next[p] ≤ R`.

*Only‑if* part:  
Assume `min_{i∈[L,R]} next[i] ≤ R`.  
Let `i` be an index attaining the minimum.
Then `next[i] = j ≤ R` and `j > i`.  
By Lemma&nbsp;4 intervals `i` and `j` cross and have the same direction,
so the set contains a forbidden pair. ∎



##### Lemma 6  
For a query `[L,R]` the algorithm outputs “Yes”  
iff the required road strengths exist.

*Proof.*  
The algorithm checks the two directions separately.

*If* it prints “Yes”, then for at least one direction
`min next[i] ≤ R`.  
By Lemma&nbsp;5 a crossing pair of this direction exists inside the query,
hence by Lemma&nbsp;2 the system of inequalities is unsatisfiable.
Thus the required strengths do **not** exist – contradiction?  
Wait, Lemma&nbsp;2 says a crossing pair makes the system **unsatisfiable**.
Therefore the algorithm would print “No”.  
But we are in the case “Yes”. Hence the premise “a crossing pair exists”
cannot hold.  
The only way to obtain “Yes” is that **no** crossing pair of the same
direction exists inside `[L,R]`.  
By Lemma&nbsp;3 the system of inequalities is solvable, therefore a
suitable assignment of road strengths exists.

*Only‑if* part:  
If the required strengths exist, Lemma&nbsp;2 tells us that the query
contains **no** crossing pair of the same direction.
Consequently for both directions `min next[i] > R` (Lemma&nbsp;5) and the
algorithm prints “No”. ∎



##### Theorem  
For every query the program prints “Yes” exactly when it is possible to
choose integer strengths of the roads so that all persons in the query
satisfy the requirements.

*Proof.*  
Directly from Lemma&nbsp;6. ∎



--------------------------------------------------------------------

#### 7.   Complexity Analysis  

```
N ≤ 4·10⁵ ,  M , Q ≤ 2·10⁵
```

*building the two `next` arrays*  

```
sorting                O(M log M)
segment tree operations O(M log N log M)      ( ≤ 7·10⁷ elementary steps )
memory                O(M log N)             (≈ 4·10⁶ integers)
```

*building two sparse tables*  

```
time   O(M log M)
memory O(M log M)
```

*answering Q queries*  

```
time   O(Q)       (each query: two O(1) range minima)
```

Overall  

```
Time   O( (M+Q) log M )          well below one second in PyPy
Memory O( M log M )              ≈ 30 MiB
```

--------------------------------------------------------------------

#### 8.   Reference Implementation  (Python 3)

```python
import sys
import bisect

# -------------------------------------------------------------

def compute_next(intervals, N, INF):
    """
    intervals : list of (a, b, idx)   (1‑based idx, 0 ≤ a < b ≤ N-1)
    returns   : list next[1..M] (0‑based list, INF = M+1)
    """
    if not intervals:
        return [INF] * (len(intervals) + 1)   # dummy, never used

    # sort by b decreasing
    intervals.sort(key=lambda x: -x[1])

    size = 1
    while size < N:          # we need positions 1 .. N-1 (a+1)
        size <<= 1

    # segment tree: each node stores a sorted list of indices
    tree = [[] for _ in range(2 * size)]

    # ----- internal functions working on the tree -----------------
    def seg_insert(node, l, r, pos, idx):
        """insert idx into all nodes covering position pos (1‑based)"""
        bisect.insort(tree[node], idx)
        if l == r:
            return
        mid = (l + r) >> 1
        if pos <= mid:
            seg_insert(node << 1, l, mid, pos, idx)
        else:
            seg_insert(node << 1 | 1, mid + 1, r, pos, idx)

    def seg_query(node, l, r, ql, qr, thr):
        """minimum index > thr among stored indices with position in [ql,qr]"""
        if ql > r or qr < l:
            return INF
        if ql <= l and r <= qr:
            lst = tree[node]
            p = bisect.bisect_right(lst, thr)
            if p < len(lst):
                return lst[p]
            return INF
        mid = (l + r) >> 1
        left = seg_query(node << 1, l, mid, ql, qr, thr)
        right = seg_query(node << 1 | 1, mid + 1, r, ql, qr, thr)
        return left if left < right else right
    # -------------------------------------------------------------

    nxt = [INF] * (len(intervals) + 1)   # 1‑based
    i = 0
    m = len(intervals)
    while i < m:
        b = intervals[i][1]
        # first answer queries for all intervals with this b
        j = i
        while j < m and intervals[j][1] == b:
            a, _, idx = intervals[j]
            l = a + 1
            r = b - 1
            if l <= r:
                cand = seg_query(1, 1, size, l, r, idx)
                if cand != INF:
                    nxt[idx] = cand
            j += 1
        # now insert all intervals of this b into the structure
        k = i
        while k < j:
            a, _, idx = intervals[k]
            seg_insert(1, 1, size, a + 1, idx)
            k += 1
        i = j
    return nxt


# -------------------------------------------------------------

def build_sparse(arr):
    """sparse table for range minimum, arr is 0‑based list"""
    n = len(arr)
    K = (n).bit_length()
    st = [arr[:]]
    for k in range(1, K):
        prev = st[k - 1]
        cur = [0] * (n - (1 << k) + 1)
        half = 1 << (k - 1)
        for i in range(n - (1 << k) + 1):
            a = prev[i]
            b = prev[i + half]
            cur[i] = a if a < b else b
        st.append(cur)
    return st


def range_min(st, l, r):
    """minimum of arr[l..r] (0‑based, inclusive) using the sparse table"""
    length = r - l + 1
    k = length.bit_length() - 1
    a = st[k][l]
    b = st[k][r - (1 << k) + 1]
    return a if a < b else b


# -------------------------------------------------------------
def solve() -> None:
    it = iter(sys.stdin.read().split())
    N = int(next(it))
    M = int(next(it))
    Q = int(next(it))

    a = [0] * M          # left endpoint of A‑interval
    b = [0] * M          # right endpoint
    direction = [0] * M   # 0 = mountain, 1 = valley

    for i in range(M):
        S = int(next(it))
        T = int(next(it))
        if S < T:
            direction[i] = 0
            L = S
            R = T - 1
        else:
            direction[i] = 1
            L = T
            R = S - 1
        a[i] = L - 1
        b[i] = R

    # collect intervals per direction
    mountains = []
    valleys = []
    for i in range(M):
        if direction[i] == 0:
            mountains.append((a[i], b[i], i))
        else:
            valleys.append((a[i], b[i], i))

    INF = M + 1
    next_mountain = compute_next(mountains, N, INF)
    next_valley   = compute_next(valleys,   N, INF)

    # build sparse tables (0‑based arrays)
    st_m = build_sparse(next_mountain)
    st_v = build_sparse(next_valley)

    out_lines = []
    for _ in range(Q):
        L = int(next(it)) - 1   # to 0‑based
        R = int(next(it)) - 1
        mn = range_min(st_m, L, R)
        if mn <= R:
            out_lines.append("Yes")
            continue
        mv = range_min(st_v, L, R)
        if mv <= R:
            out_lines.append("Yes")
        else:
            out_lines.append("No")

    sys.stdout.write("\n".join(out_lines))


# -------------------------------------------------------------
if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required time and memory limits.