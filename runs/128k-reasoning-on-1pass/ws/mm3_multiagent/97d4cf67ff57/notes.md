
## ideation
**Solution Explanation**

For a tree `T` we have to choose a connected subgraph `S`
which is again a tree and satisfies  

* every vertex of `S` has degree `1` or `4`,
* at least one vertex of `S` has degree `4`.

If we root an alkane at an arbitrary vertex `r`

* `r` may be a leaf – then `r` has exactly one neighbour,
* otherwise `r` is an internal vertex – then `r` has exactly four neighbours,
* every other vertex is internal and has exactly **three** neighbours inside the
  alkane (the remaining edge is the one to its parent).

So an alkane is a rooted tree where each internal vertex has **three**
children, except the root which has either one (leaf‑root) or four
(internal‑root) children.

--------------------------------------------------------------------

#### 1.   DP values

Root the original tree at vertex `0`.  
For a vertex `v`

* `best3[v]` – the maximum size of a *partial* alkane that lies completely
  inside the subtree of `v`, where `v` has **three** children of that partial
  alkane (i.e. `v` is internal, the fourth edge will be the edge to its
  parent).  
  If such a partial alkane does not exist `best3[v] = -∞`.

* `up[v]` – the same quantity for the part of the tree **outside** the
  subtree of `v` (the side that contains the parent of `v`).  
  Again `-∞` means “impossible”.

Only the values above are necessary.
(For a leaf we only need the size `1`, for an internal vertex we need the
size of a partial alkane with three children.)

--------------------------------------------------------------------

#### 2.   Computing `best3`  (post‑order)

For a child `c` of `v` we can either

* use the whole child subtree as a leaf – size `1`,
* or use `best3[c]` – a partial alkane rooted at `c`.

The contribution of the child is `max(1 , best3[c])`.  
If `v` has at least three children we take the three largest contributions
and add `v` itself:

```
best3[v] = 1 + sum of three largest  max(1 , best3[child])
```

If `v` has fewer than three children `best3[v] = -∞`.

The values are computed in a reverse preorder walk, therefore all children
are already known.

--------------------------------------------------------------------

#### 3.   Computing `up`  (pre‑order)

For a vertex `v` all neighbours are known:

* for every child `c` the contribution of the *c*‑side is `max(1 , best3[c])`,
* for the parent side (if it exists) the contribution is `max(1 , up[v])`.

Let `value(u)` be that contribution of neighbour `u`.
We need, for every child `c`, the sum of the three largest `value(u)` **excluding**
`c`.  
Only the four largest neighbour contributions are necessary – we store them
(`top4`).  
If `v` has at least four neighbours we compute for each child `c`

```
if c is not among the three biggest:
        sum_without_c = sum of the three biggest
else:
        replace c's value by the fourth biggest value
        sum_without_c = (sum of the three biggest) - value(c) + fourth
up[c] = 1 + sum_without_c
```

If `v` has less than four neighbours the required sum does not exist and
`up[child] = -∞` for all children.

The walk follows the preorder, therefore `up[parent]` is already known.

--------------------------------------------------------------------

#### 4.   Final answer

For every vertex `v` we look at the values of all neighbour sides:

```
leaf_best = 1 + max{ best3 side of a neighbour }        (v is a leaf)
internal_best = 1 + sum of four largest  max(1 , best3 side)   (v is internal)
```

`best3 side` of a neighbour `u` is

* `best3[u]`            if `u` is a child of `v`,
* `up[v]`               if `u` is the parent of `v`.

The answer is the maximum of all `leaf_best` and `internal_best`
that are feasible.  
If none exists we output `-1`.

--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm prints the size of the largest alkane
subgraph, or `-1` if none exists.

---

##### Lemma 1  
A connected subgraph of a tree is an alkane **iff** it can be obtained by the
following construction:

* choose a root `r`;
* every vertex different from `r` is attached to exactly one of its neighbours
  (its *parent*);
* the root has either one neighbour (leaf‑root) or four neighbours
  (internal‑root);
* every other vertex has degree `1` (leaf) or `4` (internal).

**Proof.**  
In a tree there is exactly one simple path between any two vertices.
Keeping the parent–child edges of a rooted tree yields a connected subgraph
which is still a tree.  
The degree of the root equals the number of its kept children,
the degree of any other vertex equals (kept children) + 1.
Therefore a vertex has degree `1` exactly when it has `0` children
(and only its parent edge); it has degree `4` exactly when it has `3` children
(and the parent edge). ∎



##### Lemma 2  
`best3[v]` (computed in the post‑order pass) equals the maximum possible
size of a partial alkane completely inside the subtree of `v` where `v`
has exactly three children of that partial alkane.
If such a partial alkane does not exist, `best3[v] = -∞`.

**Proof.**  
Induction over the post‑order.

*Base.*  
A leaf has no children, consequently it cannot have three children ⇒
`best3[leaf] = -∞`.

*Induction step.*  
Assume the statement true for all children of `v`.  
In a partial alkane counted by `best3[v]` every child `c` is either

* a leaf (contributes `1` vertex) or
* an internal vertex (contributes exactly `best3[c]` vertices).

The best we can do for that child is `max(1 , best3[c])`.  
Choosing the three largest such values and adding the root `v` gives the
largest possible size; if fewer than three children exist the construction is
impossible. ∎



##### Lemma 3  
`up[v]` (computed in the pre‑order pass) equals the maximum possible size
of a partial alkane lying completely **outside** the subtree of `v`
(the side that contains the parent of `v`) where the neighbour of `v`
on that side has exactly three children of that partial alkane.
If such a partial alkane does not exist, `up[v] = -∞`.

**Proof.**  
Consider the parent `p` of `v`.  
All neighbours of `p` except `v` are precisely the neighbours that may be
used as the three children of the partial alkane on the parent side.
For each such neighbour `u` the contribution is

```
max( 1 ,   best3 of the side of u that does not contain p )
```

which is already known (`best3[child]` for a child,
`up[p]` for the parent of `p`).  
Choosing the three largest contributions and adding `p` itself yields the
largest possible size of the required partial alkane, exactly the value
assigned to `up[v]`.  
If fewer than three such neighbours exist the construction is impossible,
hence `up[v] = -∞`. ∎



##### Lemma 4  
For every vertex `v`

* `leaf_best[v] = 1 + max{ best3 side of a neighbour }`  
  is the size of the largest alkane whose root is `v` and `v` is a leaf,
* `internal_best[v] = 1 + sum of four largest max(1 , best3 side)`  
  is the size of the largest alkane whose root is `v` and `v` is internal.

**Proof.**  
Take an alkane with root `v`.

*If `v` is a leaf* (degree = 1) it has exactly one neighbour `u`.  
The rest of the alkane is a partial alkane rooted at `u` where `u` has three
children (the fourth edge is the edge `u–v`).  
Its size is `best3 side(u)`. Adding the vertex `v` gives
`1 + best3 side(u)`. Maximising over all neighbours yields `leaf_best[v]`.

*If `v` is internal* (degree = 4) it has exactly four neighbours.
For each neighbour `u` we may attach it either as a leaf (size = 1) or as an
internal vertex (size = `best3 side(u)`).  
The best we can do for that neighbour is `max(1 , best3 side(u))`,
and we may freely choose which four neighbours to keep.
Choosing the four largest such values and adding the root `v` gives
`internal_best[v]`. ∎



##### Lemma 5  
The algorithm computes the exact values `leaf_best[v]` and `internal_best[v]`
described in Lemma&nbsp;4.

**Proof.**  
The algorithm uses for every neighbour `u` of `v`

* `best3[u]`  if `u` is a child,
* `up[v]`     if `u` is the parent,

exactly the values `best3 side(u)` required in Lemma&nbsp;4.
It then performs the same maximisation (leaf case) and the same
“four largest” selection (internal case), therefore the obtained numbers are
the true `leaf_best[v]` and `internal_best[v]`. ∎



##### Lemma 6  
The maximum of all `leaf_best[v]` and `internal_best[v]` equals the size of
the largest alkane subgraph of the original tree.

**Proof.**  
*Existence.*  
Let `A` be any alkane subgraph and `r` an arbitrary vertex of `A`.
By Lemma&nbsp;1, `r` is either a leaf or an internal vertex of `A`.  
If `r` is a leaf, `A` is counted by `leaf_best[r]`; otherwise it is counted
by `internal_best[r]`. Hence `|A|` does not exceed the maximum of all those
values.

*Achievability.*  
For any vertex `v`, Lemma&nbsp;5 tells us that a concrete alkane of size
`leaf_best[v]` (leaf‑root) or `internal_best[v]` (internal‑root) can be built
by taking, for every neighbour, the best possible attachment described by the
DP values. Therefore every value considered in the maximum is realised by an
actual alkane.

Thus the maximum equals the optimum size. ∎



##### Lemma 7  
If the algorithm outputs `-1` then the original tree contains no alkane
subgraph.

**Proof.**  
`-1` is printed only when every `leaf_best[v]` and `internal_best[v]` is
impossible.  By Lemma&nbsp;5 an impossible value means that no alkane with that
root exists. Consequently no alkane exists at all. ∎



##### Theorem  
The program prints  

* the maximum possible number of vertices of a subgraph of the given tree
  that is an alkane, or  
* `-1` if no such subgraph exists.

**Proof.**  
If the program prints a positive number, it is the maximum of all
`leaf_best[v]` and `internal_best[v]`.  By Lemma&nbsp;6 this number equals the
size of the largest alkane.  
If the program prints `-1`, Lemma&nbsp;7 shows that no alkane exists.
Hence the output is correct in all cases. ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis

*Building the rooted tree* – `O(N)` time, `O(N)` memory.  
*Down DP (`best3`)* – each edge inspected once → `O(N)` time, `O(N)` memory.  
*Up DP (`up`)* – each edge inspected a constant number of times → `O(N)`
time, `O(N)` memory.  
*Final scan* – again `O(N)`.

Overall  

```
Time   :  O(N)      ( ≤ 2·10⁵ operations )
Memory :  O(N)
```

Both satisfy the limits.

--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import sys
import heapq

INF_NEG = -10 ** 9          # value meaning “impossible”

def solve() -> None:
    it = iter(map(int, sys.stdin.buffer.read().split()))
    n = next(it)
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a = next(it) - 1
        b = next(it) - 1
        adj[a].append(b)
        adj[b].append(a)

    # ---------- root the tree (iterative DFS) ----------
    parent = [-1] * n           # parent[v] = -1  -> root
    order = []                  # preorder
    stack = [0]
    parent[0] = -2              # mark the root, different from “no parent”
    while stack:
        v = stack.pop()
        order.append(v)
        for u in adj[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            stack.append(u)

    # ---------- down DP : best3 ----------
    best3 = [INF_NEG] * n
    for v in reversed(order):               # postorder
        child_vals = []
        for u in adj[v]:
            if parent[u] == v:              # child
                val = best3[u] if best3[u] != INF_NEG else 1
                child_vals.append(val)
        if len(child_vals) >= 3:
            top3 = heapq.nlargest(3, child_vals)
            best3[v] = 1 + sum(top3)

    # ---------- up DP ----------
    up = [INF_NEG] * n
    up[0] = INF_NEG                          # root has no parent side

    for v in order:                         # preorder, parent already processed
        # collect (neighbour, contribution) pairs
        neigh = []
        p = parent[v]
        if p != -2:                          # has a parent
            val = up[v] if up[v] != INF_NEG else 1
            neigh.append((p, val))

        for u in adj[v]:
            if parent[u] == v:              # child
                val = best3[u] if best3[u] != INF_NEG else 1
                neigh.append((u, val))

        if len(neigh) < 4:                  # not enough neighbours for up[child]
            for u in adj[v]:
                if parent[u] == v:
                    up[u] = INF_NEG
            continue

        # four largest contributions
        top4 = heapq.nlargest(4, neigh, key=lambda x: x[1])
        sum_top3 = top4[0][1] + top4[1][1] + top4[2][1]
        top3_set = {top4[0][0], top4[1][0], top4[2][0]}

        for u in adj[v]:
            if parent[u] != v:
                continue
            if u not in top3_set:
                sum_excl = sum_top3
            else:
                # find u's value among the three biggest
                val_u = None
                for nid, val in top4[:3]:
                    if nid == u:
                        val_u = val
                        break
                # the fourth value always exists because len(neigh) >= 4
                next_val = top4[3][1]
                sum_excl = sum_top3 - val_u + next_val
            up[u] = 1 + sum_excl

    # ---------- final answer ----------
    answer = INF_NEG
    for v in range(n):
        # collect best3 values of all neighbour sides
        neigh_best3 = []
        for u in adj[v]:
            if parent[u] == v:          # child
                neigh_best3.append(best3[u])
        if parent[v] != -2:            # has a parent
            neigh_best3.append(up[v])

        # ----- leaf root (v is leaf) -----
        max_internal = INF_NEG
        for x in neigh_best3:
            if x != INF_NEG and x > max_internal:
                max_internal = x
        if max_internal != INF_NEG:
            leaf_best = 1 + max_internal
            if leaf_best > answer:
                answer = leaf_best

        # ----- internal root (v has degree 4 in the alkane) -----
        if len(neigh_best3) >= 4:
            # contribution of a neighbour = max(1, best3 side)
            contribs = [x if x != INF_NEG else 1 for x in neigh_best3]
            top4 = heapq.nlargest(4, contribs)
            internal_best = 1 + sum(top4)
            if internal_best > answer:
                answer = internal_best

    if answer == INF_NEG:
        print(-1)
    else:
        print(answer)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required time (`O(N)`) and memory (`O(N)`) limits.

## worker: (omitted - task complete)
The solution uses a DP on a rooted tree.

* **Alkane structure** – an alkane is a tree where each internal vertex has degree 4 and leaves have degree 1. If we root the alkane, the root has either one child (leaf‑root) or four children (internal‑root); every other internal vertex has exactly three children.

* **`best3[v]`** – size of the best partial alkane completely inside the subtree of `v` where `v` has three children. It is computed bottom‑up: the contribution of a child is `max(1, best3[child])`; we take the three largest contributions and add the vertex `v`.

* **`up[v]`** – the same value for the part of the tree **outside** the subtree of `v` (the side containing the parent). It is computed top‑down. For a vertex `v`, the contribution of a neighbour side is `max(1, best3 side)` for a child or `max(1, up[v])` for the parent side. For each child `c` of `v` we need the sum of the three largest contributions among the neighbours of `v` **excluding** `c`. Only the four largest neighbour contributions are needed, which lets us compute `up[c]` in O(1) per child.

* **Final answer** – for every vertex we consider two possibilities:
  * the vertex is a leaf‑root → size `1 + max(best3 side of a neighbour)`,
  * the vertex is an internal‑root → size `1 + sum of four largest max(1, best3 side)`.
  The maximum over all vertices is the answer. If no such value exists we output `-1`.

The algorithm runs in `O(N)` time and `O(N)` memory, well within the limits (`N ≤ 2·10⁵`).
