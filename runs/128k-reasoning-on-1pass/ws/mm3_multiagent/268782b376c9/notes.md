
## ideation
**Solution Explanation**

For a target minimum score `X` we need every cell `i` to be visited at least  

```
need[i] = ceil( X / points[i] )
```

times.  
During a walk we start at the virtual index `-1` and the first move must be to
`0`, therefore the visit count of cell `0` is

```
visits[0] = 1 + g0
visits[i] = f(i‑1) + g(i)      (i ≥ 1)
```

`f(i)` – moves from `i` to `i+1`, `g(i)` – moves from `i+1` to `i`.  
The walk ends at some final index `p (0 ≤ p ≤ n‑1)`.  
Let `d(i) = f(i) - g(i)`. Because the walk never leaves the segment,
`d(i)` is forced to be

```
d(i) = 1   for i < p
d(i) = 0   for i ≥ p
```

Hence `Σ d(i) = p`.  
The total number of performed moves is

```
L = 1 (first step) + Σ (f(i) + g(i))
  = 1 + p + 2· Σ g(i)                (because f(i) = g(i) + d(i))
```

For a fixed `p` the only variables are the `g(i) (≥0)`.  
The constraints become

```
g0                     ≥ need0 - 1
g(i‑1) + g(i)          ≥ needi - 1{ i ≤ p }      (i ≥ 1)
```

(The `1` for `i=0` comes from the mandatory first step,
the `1{ i ≤ p }` comes from `d(i‑1)`.)

Define

```
w0 = max(0, need0 - 1)
wi = max(0, needi - 1{ i ≤ p })   (i ≥ 1)
```

Then the problem for a fixed `p` is

```
minimise Σ g(i)      subject to
    g(i‑1) + g(i) ≥ wi   (i ≥ 1)
    g0          ≥ w0
    g(i) ≥ 0
```

The linear program above is totally unimodular, its dual is a **maximum‑weight
independent set on a path**:

* vertex `i` (the i‑th constraint) has weight `wi`,
* two consecutive vertices share the variable `gi` → they are adjacent,
* we must not select adjacent vertices.

Let `S(p)` be the weight of a maximum independent set.
By strong duality the minimum possible `Σ g(i)` equals `S(p)`.
Consequently the minimum number of moves for this `p` is

```
L(p) = 1 + p + 2·S(p)
```

`X` is feasible iff there exists a `p` with `L(p) ≤ m`.

--------------------------------------------------------------------

### 1.  Computing `S(p)` for all `p` in `O(n log n)`

During the scan `p = 0 … n‑1` the weights change only for the newly entered
index `p` (for `p ≥ 1` we subtract `1` from the current weight).
Thus we need a data structure that

* stores a path of independent‑set weights,
* supports **point update** (`wi` changes) and
* returns `S(p) =` max weight independent set of the whole path.

A path of independent sets can be represented by a `2×2` matrix in the
*max‑plus* semiring.
For a single vertex with weight `w`

```
T = [ [0, w],
      [0, -∞] ]
```

`T[a][b]` = best value of the vertex when the previous vertex is in state
`a` (`0` = not taken, `1` = taken) and this vertex is in state `b`.
For a concatenation of two segments the matrix product is

```
(C = A ⊗ B)  with  C[i][k] = max_j ( A[i][j] + B[j][k] )
```

The product of all leaves gives the DP of the whole path; the answer is
`max( root[0][0] , root[0][1] )` (the first element corresponds to the
nonexistent vertex left of the array).

A segment tree (iterative, size = next power of two) stores those matrices.
A point update changes one leaf and recomputes the ancestors in `O(log n)`.
Thus scanning all `p` costs `O(n log n)`.

--------------------------------------------------------------------

### 2.  Whole algorithm

```
binary search answer X in [0 , m·max(points)]

check(X):
    need[i] = ceil( X / points[i] )
    w0 = max(0, need0-1)
    wi = needi               (i ≥ 1)   // for p = 0
    build segment tree from w
    for p = 0 … n-1:
        S = maxWeightIndependentSet()
        L = 1 + p + 2·S
        if L ≤ m: return True
        if p+1 < n:
            // p grows, weight of vertex p+1 is reduced by one
            new_w = max(0, need[p+1] - 1)
            pointUpdate(p+1, new_w)
    return False
```

`check` runs in `O(n log n)`.  
Binary search needs at most 60 iterations (`m·max(points) ≤ 10^15`), so the
total complexity is `O( n log n log( m·max(points) ) )`  
(~ 4·10^7 elementary operations for the maximal input), well inside limits.

--------------------------------------------------------------------

### 3.  Correctness Proof  

We prove that the algorithm returns the maximum possible minimum score.

---

#### Lemma 1  
For a fixed final index `p` the walk constraints are equivalent to

```
g0                ≥ w0
g(i‑1) + g(i)     ≥ wi     (i ≥ 1)
g(i) ≥ 0
```

where  

```
w0 = max(0, need0 - 1)
wi = max(0, needi - 1{ i ≤ p })   (i ≥ 1)
```

**Proof.**  
`visits0 = 1 + g0 ≥ need0`  ⇒  `g0 ≥ need0 – 1`.  
For `i ≥ 1` we have `visitsi = f(i‑1) + g(i)`.  
Since `f(i‑1) = g(i‑1) + d(i‑1)` and `d(i‑1) = 1{ i‑1 < p } = 1{ i ≤ p }`,
`g(i‑1) + g(i) ≥ needi – 1{ i ≤ p }`.  
Taking the non‑negative lower bound gives the stated `wi`. ∎



#### Lemma 2  
For a fixed `p` the minimum possible value of `Σ g(i)` equals the weight
`S(p)` of a maximum‑weight independent set on the path whose vertex `i`
has weight `wi` (as defined in Lemma&nbsp;1).

**Proof.**  
The primal linear program (variables `g(i) ≥ 0`, constraints of Lemma&nbsp;1,
objective minimise `Σ g(i)`) is a covering linear program with a
consecutive‑ones coefficient matrix, therefore its matrix is totally
unimodular and the linear program has an integer optimal solution.

Its dual has a variable `yi` for every primal constraint, i.e. for every
vertex `i`. The dual constraints are

```
y0 + y1 ≤ 1
yi + y(i+1) ≤ 1   (1 ≤ i ≤ n‑2)
y(n‑1) ≤ 1
yi ≥ 0
```

and the dual objective is `max Σ wi·yi`.  
The constraints say that at most one of two adjacent `yi` may be positive,
hence an optimal dual solution can be taken integer (`yi ∈ {0,1}`) and
corresponds exactly to an independent set on the path.
By strong duality the optimal primal value (minimum `Σ g(i)`) equals the
optimal dual value, i.e. the maximum independent‑set weight `S(p)`. ∎



#### Lemma 3  
For a fixed `p` the minimum number of moves that can achieve a given
minimum score `X` equals  

```
L(p) = 1 + p + 2·S(p)
```

**Proof.**  
From Lemma&nbsp;1 the walk constraints are satisfied iff the `g(i)` fulfil
the inequalities of Lemma&nbsp;1.  
By Lemma&nbsp;2 the smallest possible sum of the `g(i)` is `S(p)`.  
With `Σ d(i) = p` we have

```
L = 1 + Σ (f(i)+g(i))
  = 1 + Σ (2·g(i) + d(i))
  = 1 + p + 2·Σ g(i)
  ≥ 1 + p + 2·S(p)
```

Choosing the `g(i)` that achieve the minimum `Σ g(i) = S(p)` (they exist by
Lemma&nbsp;2) gives equality, therefore the minimum number of moves is exactly
`L(p)`. ∎



#### Lemma 4  
`check(X)` returns *True*  **iff**  there exists a walk of at most `m`
moves whose every gameScore is at least `X`.

**Proof.**  
`check` computes `need[i] = ceil(X/points[i])`.  
For each possible final index `p` it evaluates `L(p)` using the current
weights `wi(p)` (the algorithm maintains exactly the `wi` of Lemma&nbsp;1).
By Lemma&nbsp;3 `L(p)` is the smallest possible number of moves for that
`p`.  
If any `p` yields `L(p) ≤ m` the walk with those `g(i)` and the appropriate
`f(i) = g(i) + d(i)` uses at most `m` moves and satisfies all visit
requirements, therefore the answer is feasible.  
Conversely, if a feasible walk exists, let its final index be `p`.  
Its `g(i)` satisfy the constraints of Lemma&nbsp;1, hence
`Σ g(i) ≥ S(p)`.  By Lemma&nbsp;3 the walk needs at least `L(p)` moves,
so `L(p) ≤ m`.  The scan over all `p` will discover this `p` and return
*True*. ∎



#### Lemma 5  
For any integer `X`, the binary‑search predicate “`X` is feasible”
is monotone: if `X` is feasible then every `Y ≤ X` is feasible.

**Proof.**  
A walk that gives every cell at least `X` points automatically gives at
least `Y` points to every cell, because `Y ≤ X`.  Hence any walk feasible
for `X` is also feasible for any smaller `Y`. ∎



#### Lemma 6  
The binary search returns the largest feasible `X`.

**Proof.**  
Because of Lemma&nbsp;5 the feasible set is an interval `[0, X*]`.  
The search maintains the invariant `low` feasible, `high` infeasible
(or `high = low` at termination).  The standard “upper‑mid” binary search
keeps the invariant and finishes with `low = X*`. ∎



#### Theorem  
`maxScore(points, m)` returns the maximum possible minimum value among
all gameScore arrays after at most `m` moves.

**Proof.**  
Let `Ans` be the value returned by the binary search.
By Lemma&nbsp;6 `Ans` is feasible, therefore a walk with at most `m`
moves achieving a minimum score of `Ans` exists.
If there existed a larger feasible value `Ans' > Ans`,
Lemma&nbsp;5 would imply `Ans` infeasible, contradicting the result of
`check(Ans)`.  Hence no larger value is feasible and `Ans` is optimal. ∎



--------------------------------------------------------------------

### 4.  Complexity Analysis  

*`n = len(points)`, `M = m·max(points)`.*

* **Feasibility test** `check(X)`  
  * computing `need[i]` – `O(n)`  
  * building the segment tree – `O(n)`  
  * scanning all `p` (`n` iterations, each `O(log n)`) – `O(n log n)`  

  **Time:** `O(n log n)`  
  **Memory:** segment tree (`2·2^⌈log₂ n⌉` matrices) → `O(n)`.

* **Binary search** – at most `⌈log₂ M⌉ ≤ 60` iterations.  

  **Total time:** `O( n log n log M )`  ≤ 4·10⁷ elementary operations for the
  maximal limits.  
  **Total memory:** `O(n)`.

Both limits easily satisfy the constraints (`n ≤ 5·10⁴`).

--------------------------------------------------------------------

### 5.  Reference Implementation  (Python 3)

```python
from typing import List

class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        NEG = -10**18                     # -infinity for max‑plus

        # ---------- segment tree for max‑weight independent set ----------
        class SegTree:
            __slots__ = ('size', 'tree')
            def __init__(self, w: List[int]):
                sz = 1 << (len(w) - 1).bit_length()
                self.size = sz
                # identity matrix for max‑plus: [[0,-inf],[-inf,0]]
                ID = (0, NEG, NEG, 0)
                self.tree = [ID] * (2 * sz)
                # leaves
                for i, wi in enumerate(w):
                    self.tree[sz + i] = (0, wi, 0, NEG)
                # internal nodes
                for i in range(sz - 1, 0, -1):
                    self.tree[i] = self._combine(self.tree[2*i],
                                                 self.tree[2*i+1])

            @staticmethod
            def _combine(A, B):
                a00, a01, a10, a11 = A
                b00, b01, b10, b11 = B
                c00 = a00 + b00
                if a01 + b10 > c00:
                    c00 = a01 + b10
                c01 = a00 + b01
                if a01 + b11 > c01:
                    c01 = a01 + b11
                c10 = a10 + b00
                if a11 + b10 > c10:
                    c10 = a11 + b10
                c11 = a10 + b01
                if a11 + b11 > c11:
                    c11 = a11 + b11
                return (c00, c01, c10, c11)

            def update(self, idx: int, w: int):
                i = self.size + idx
                self.tree[i] = (0, w, 0, NEG)
                i //= 2
                while i:
                    self.tree[i] = self._combine(self.tree[2*i],
                                                 self.tree[2*i+1])
                    i //= 2

            def query(self) -> int:
                root = self.tree[1]
                return root[0] if root[0] > root[1] else root[1]

        # ---------- feasibility test for a given X ----------
        def can(X: int) -> bool:
            # minimal number of visits for each cell
            need = [(X + points[i] - 1) // points[i] for i in range(n)]

            # initialise weights w[i] for p = 0
            w = [0] * n
            w[0] = need[0] - 1
            if w[0] < 0:
                w[0] = 0
            for i in range(1, n):
                w[i] = need[i]                     # i > p, so no subtraction

            seg = SegTree(w)

            for p in range(n):
                S = seg.query()                     # max independent set weight
                L = 1 + p + 2 * S
                if L <= m:
                    return True

                if p + 1 < n:
                    # when p grows, weight of vertex p+1 is reduced by one
                    new_w = need[p + 1] - 1
                    if new_w < 0:
                        new_w = 0
                    seg.update(p + 1, new_w)

            return False

        # ---------- binary search on the answer ----------
        lo, hi = 0, m * max(points)          # inclusive hi
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
```

The program follows exactly the algorithm proven correct above and conforms
to the required `O(n log n log(m·max(points)))` time and `O(n)` memory.

## worker: Implement the complete `maxScore` method in Python
The algorithm reduces the problem to checking, for a candidate minimum score `X`, whether the required number of visits `need[i] = ceil(X / points[i])` can be achieved within `m` moves.  
For a fixed final index `p`, the walk constraints become a covering linear program whose dual is a maximum‑weight independent set on a path with weights `w_i = max(0, need_i - 1_{i ≤ p})`. The minimum number of moves for that `p` is `L(p) = 1 + p + 2·S(p)`, where `S(p)` is the independent‑set weight.  

The independent‑set problem on a path is solved by a segment tree storing `2×2` matrices in the max‑plus semiring. Point updates (changing a weight) and root queries are `O(log n)`. Scanning all `p` from `0` to `n‑1` costs `O(n log n)`.  

A binary search on `X` (range `0 … m·max(points)`) yields the maximum feasible minimum score. Overall complexity: `O(n log n log(m·max(points)))`, well within the limits (`n ≤ 5·10⁴`).  

The implementation uses a large negative sentinel (`-10³⁰`) to represent `-∞` safely, and all arithmetic is performed with Python's arbitrary‑precision integers.
