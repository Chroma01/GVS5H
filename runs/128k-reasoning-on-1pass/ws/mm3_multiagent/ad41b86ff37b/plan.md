**Solution Explanation**

For a tree `T` we may delete any vertices (and all incident edges).  
The remaining vertices must form a *Snowflake Tree* :

```
red vertex r
│
├── b1 ── y leaves
├── b2 ── y leaves
│   …
└── bx ── y leaves          (x ≥ 1 , y ≥ 1)
```

`r` is the only vertex that may have neighbours of degree `> 1`
(the blue vertices `b1 … bx`).  
Every blue vertex has exactly one neighbour `r` and `y` leaf neighbours,
all of degree `1` in the remaining graph.

--------------------------------------------------------------------

#### 1.   What can a snowflake look like after deletions ?

Assume we decided to keep a vertex `r` as the red vertex and a set
`B ⊆ N(r)` of its neighbours as the blue vertices.
For a blue vertex `b`

```
deg(b) in the original tree  =  1 (edge to r)  +  number of other neighbours
```

To be able to attach `y` leaves we need  

```
deg(b) - 1  ≥  y                (1)
```

If a set `B` is chosen, the same `y` must work for **all** vertices of `B`,
therefore

```
y ≤  min_{b∈B} (deg(b)-1)                (2)
```

The best we can do for this `B` is to use the maximal possible `y`

```
y* = min_{b∈B} (deg(b)-1)
```

All blue vertices get exactly `y*` leaves (any `y*` of their original
neighbours may be kept, the rest are deleted).  
The number of kept vertices becomes

```
1           (red r)
+ |B|        (the blue vertices)
+ |B|·y*     (the leaves)
= 1 + |B|·(y*+1)
= 1 + |B|· min_{b∈B} deg(b)                (3)
```

So for a fixed red vertex `r` the problem is

```
choose a non‑empty subset B of neighbours of r
maximise  |B| · min_{b∈B} deg(b)            (4)
```

--------------------------------------------------------------------

#### 2.   The optimal subset for a fixed `r`

Sort the neighbour degrees of `r` in **decreasing** order

```
d1 ≥ d2 ≥ … ≥ dk      (k = degree of r)
```

For a subset of size `t` the smallest degree inside the subset
cannot be larger than `dt`.  
Conversely, taking the first `t` vertices gives exactly `min = dt`.
Therefore the best value for size `t` is `t·dt`.

Consequently the optimum for vertex `r` is obtained by scanning the
sorted list and keeping the maximum of `t·dt` (`t = 1 … k`).

Only neighbours with `deg ≥ 2` can be blue,
otherwise `y = deg-1 = 0` which is forbidden.
All neighbours with `deg = 1` are ignored.

--------------------------------------------------------------------

#### 3.   Whole tree

For every vertex `r`

```
cand = [ deg(v) for v in N(r) if deg(v) ≥ 2 ]
if cand is empty:   r cannot be the red vertex
else:
    sort cand decreasing
    best_r = max_{i=1..len(cand)}  i * cand[i-1]
    size_r = 1 + best_r                (from (3))
```

The answer is

```
maxSize = max_r size_r
answer  = N - maxSize                (deleted vertices)
```

`N ≤ 3·10⁵`, the total number of edges is `2·(N‑1)`.
Sorting all neighbour lists costs  

```
 Σ deg(v)·log deg(v)  ≤  N·log N
```

which is easily fast enough.

--------------------------------------------------------------------

#### 4.   Correctness Proof  

We prove that the algorithm outputs the minimum possible number of
deleted vertices.

---

##### Lemma 1  
For a fixed red vertex `r` and a fixed set of blue vertices `B ⊆ N(r)`,
the largest possible number of kept vertices equals `1 + |B|·min_{b∈B}deg(b)`.

**Proof.**  
All blue vertices must have the same number `y` of leaves.
From (2) we have `y ≤ min_{b∈B}(deg(b)-1)`.  
Choosing `y = min_{b∈B}(deg(b)-1)` satisfies (1) for every `b∈B`,
so we can keep exactly `y` leaves for each blue vertex.
The number of kept vertices is then

```
1 (r) + |B| (blue) + |B|·y
= 1 + |B|·(y+1)
= 1 + |B|·min_{b∈B}deg(b)               (by definition of y)
```

No larger `y` is possible, therefore no larger number of kept vertices
is possible. ∎



##### Lemma 2  
For a fixed vertex `r` the maximum of `|B|·min_{b∈B}deg(b)` over all
non‑empty `B ⊆ N(r)` is attained by a set consisting of the `t`
neighbours with largest degrees, for some `t`.

**Proof.**  
Take any optimal set `B`.  
If `|B| = t`, let `d_min = min_{b∈B}deg(b)`.  
Among all `t` neighbours of `r` the `t` largest degrees have minimum
`d* ≥ d_min`.  
Replacing `B` by those `t` neighbours does not decrease the product
`t·d*` and therefore also does not decrease the objective.
Hence an optimal set can be chosen as the first `t` elements of the
sorted degree list. ∎



##### Lemma 3  
For a vertex `r` the algorithm computes  

```
best_r = max_{B⊆N(r), B≠∅} |B|·min_{b∈B}deg(b)
```

and `size_r = 1 + best_r`.

**Proof.**  
The algorithm discards neighbours of degree `1` because they cannot be
blue (they would require `y = 0`).  
For the remaining neighbours it sorts their degrees decreasingly.
Scanning the sorted list it evaluates `i·cand[i‑1]` for every `i`.
By Lemma&nbsp;2 the maximum over all non‑empty subsets is exactly the
maximum of these values, thus `best_r` is correct.
Formula `size_r = 1 + best_r` follows from Lemma&nbsp;1. ∎



##### Lemma 4  
`maxSize = max_r size_r` equals the maximum possible number of vertices
that can stay after deletions.

**Proof.**  
*Upper bound.*  
Any feasible resulting snowflake has a unique red vertex `r`.  
By Lemma&nbsp;1 its size is at most `1 + best_r = size_r`.  
Therefore it is at most `maxSize`.

*Achievability.*  
Take a vertex `r*` attaining `maxSize`.  
By Lemma&nbsp;3 there exists a subset `B` of neighbours of `r*`
with `|B|·min_{b∈B}deg(b) = best_{r*}`.  
Using Lemma&nbsp;1 we can keep exactly `1 + best_{r*}` vertices:
`r*`, all vertices of `B` and, for each `b∈B`, exactly
`min_{b∈B}deg(b)-1` of its leaf neighbours.
All other vertices are deleted, and the remaining graph is a snowflake
tree. Hence a snowflake of size `maxSize` can be obtained. ∎



##### Lemma 5  
The answer printed by the algorithm,
`N - maxSize`, is the minimum possible number of deletions.

**Proof.**  
Any solution deletes at least `N - maxSize` vertices because
no snowflake can contain more than `maxSize` vertices (Lemma&nbsp;4).
Conversely, deleting exactly `N - maxSize` vertices is possible:
keep a snowflake of size `maxSize` (Lemma&nbsp;4) and delete all other
vertices. ∎



##### Theorem  
The algorithm always outputs the minimum number of vertices that have
to be deleted so that the remaining graph is a Snowflake Tree.

**Proof.**  
Directly from Lemma&nbsp;5. ∎



--------------------------------------------------------------------

#### 5.   Complexity Analysis

```
building adjacency list          :  O(N)
computing degrees                :  O(N)
for every vertex:
        collect neighbour degrees (deg ≥ 2)   :  O(deg(v))
        sort the list                         :  O(deg(v) log deg(v))
        scan the list                         :  O(deg(v))
total time                       :  O( Σ deg(v) log deg(v) ) = O(N log N)
memory                           :  O(N)   (adjacency + degree array)
```

With `N ≤ 3·10⁵` this easily fits into the limits.

--------------------------------------------------------------------

#### 6.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))

    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    deg = [0] * (n + 1)
    for v in range(1, n + 1):
        deg[v] = len(adj[v])

    max_total = 0                     # maximal number of kept vertices

    for r in range(1, n + 1):
        # candidate neighbour degrees (must be at least 2)
        cand = [deg[nb] for nb in adj[r] if deg[nb] >= 2]
        if not cand:
            continue                  # r cannot be the red vertex
        cand.sort(reverse=True)

        best = 0
        # i = number of chosen blue vertices (1‑based)
        for i, d in enumerate(cand, start=1):
            val = i * d                # i * min degree among first i neighbours
            if val > best:
                best = val
        size_r = 1 + best              # Lemma 1
        if size_r > max_total:
            max_total = size_r

    answer = n - max_total
    sys.stdout.write(str(answer))


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.