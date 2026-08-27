**Solution Explanation**

For the given tree we have to choose a *connected* subgraph which is again a tree.
In the chosen subgraph every vertex must have degree `1` (leaf) or `4`
(internal vertex) and at least one vertex must have degree `4`.
The number of vertices of such a tree is always

```
L = 2·B + 2          ( L – leaves, B – internal vertices )
|V| = L + B = 3·B + 2                ( 5 , 8 , 11 , … )
```

--------------------------------------------------------------------

#### 1.   Tree DP

Root the original tree at an arbitrary vertex (vertex `0`).
For every vertex `v` we need the size of the best **partial** alkane
which

* is completely inside the subtree of `v` (i.e. it does **not** use the
  edge to the parent of `v`);
* `v` is connected to exactly `k` of its children inside this partial
  alkane (`k = 0,1,2,3,4`).

Only the following values are useful

```
k = 0 : v is a leaf for its parent                (size = 1)
k = 1 : v will be a leaf in the final alkane       (root of the alkane)
k = 3 : v will be an internal vertex, the fourth
        neighbour is its parent                     (size of a subtree
                                                    where v has three
                                                    children)
k = 4 : v will be an internal root of the alkane
```

`k = 2` can never lead to a valid alkane.

--------------------------------------------------------------------
#### 2.   Down DP   (only children are used)

For a child `c` of `v`

```
leaf contribution   = 1                     (c becomes a leaf)
internal contribution = best3[c]            (c is an internal vertex,
                                            it needs three more children)
```

The value of attaching a child is `max(1 , best3[c])`.

```
best0[v] = 1                                   (just v)
best1[v] = 1 + max( best3[child] )            (one internal child)
best3[v] = 1 + sum of three largest values   (v is internal, will get
                                                a parent edge)
best4[v] = 1 + sum of four  largest values    (v is an internal root)
```

`best3[v]` is defined only if `v` has at least three children,
otherwise it is “impossible”.

All `best3` are computed by a post‑order walk – the children are already
known.

--------------------------------------------------------------------
#### 3.   Up DP   (the part of the tree above a vertex)

For a vertex `v` we also need the value `best3` of the *rest* of the tree
(the side of its parent).  
Let `up[v]` be that value (`up[root] = impossible`).

For a neighbour `u` of `v`

```
value(u → v) = max( 1 , best3 of the side of u that does NOT contain v )
```

* if `u` is a child : the side is the whole subtree of `u`,
  value = `max(1 , best3[u])`;
* if `u` is the parent : the side is the rest of the tree,
  value = `max(1 , up[v])`.

For a fixed vertex `v` all neighbour values are known.
For every child `c` we have to know the sum of the three largest values
*excluding* `c`.  
Only the four largest values of `v` are needed – we keep them, and for
each child we either use the three largest (if the child is not among
them) or replace the child by the fourth largest value.

All `up[child]` are computed in a pre‑order walk, therefore the parent
value is already known.

--------------------------------------------------------------------
#### 4.   Final answer

For every vertex `v`

```
neighbour_best3 = {   best3[child]  for all children,
                       up[v]        if v has a parent }

best1(v) = 1 + max( neighbour_best3 )          (v is a leaf root)
contrib   = { 1 if neighbour_best3 = impossible,
              neighbour_best3 otherwise }   (leaf = 1, internal = its size)

best4(v) = 1 + sum of four largest contrib      (v is an internal root)
```

The answer is the maximum of `best1(v)` and `best4(v)` over all vertices.
If no such value exists we output `-1`.

--------------------------------------------------------------------
#### 5.   Correctness Proof  

We prove that the algorithm prints the size of the largest alkane subgraph
or `-1` when none exists.

---

##### Lemma 1  
For a fixed rooted tree, a connected subgraph is a valid alkane
iff it can be obtained by the following local construction:

* choose a root `r`;
* every vertex different from `r` is attached to exactly one of its
  neighbours (its parent in the rooted tree);
* the root has either exactly one neighbour (leaf root) or exactly four
  neighbours (internal root);
* every vertex has degree `1` or `4` in the obtained tree.

**Proof.**  
A tree has a unique simple path between any two vertices.
Choosing a root and keeping exactly the parent–child edges of the rooted
tree gives a connected subgraph (still a tree) and every vertex has
degree equal to the number of kept incident edges.
The degree of the root is the number of its kept children.
All other vertices have degree = (number of kept children) + 1
(the edge to the parent).  
Thus the degrees are `1` (leaf) or `4` (internal) exactly when the root
has `1` or `4` children and each other vertex has `0` or `3` children
(internal) or only the parent edge (leaf). ∎



##### Lemma 2  
`best3[v]` (down DP) equals the maximum possible number of vertices of a
partial alkane rooted at `v` that uses **only** vertices in the subtree
of `v` and where `v` has exactly three children inside the alkane.
If such a partial alkane does not exist, `best3[v] = -∞`.

**Proof.**  
Induction over the post‑order.

*Base.*  
If `v` is a leaf, it has no children, therefore it cannot have three
children – `best3[v] = -∞`.  

*Induction step.*  
Assume the statement true for all children of `v`.  
Any partial alkane counted by `best3[v]` must attach each child either

* as a leaf – contributes `1` vertex,
* as an internal vertex – contributes exactly `best3[child]` vertices
  (induction hypothesis).

The size contributed by a child is therefore `max(1 , best3[child])`.
Choosing the three largest such values gives the maximal possible size,
and `best3[v] = 1 + sum_of_three_largest` is exactly that size.
If `v` has fewer than three children the construction is impossible,
hence `best3[v] = -∞`. ∎



##### Lemma 3  
`up[v]` (up DP) equals the maximum possible number of vertices of a
partial alkane rooted at the parent side of `v` (i.e. the whole tree
without the subtree of `v`) where the parent of `v` has exactly three
children inside that partial alkane.  
If it does not exist, `up[v] = -∞`.

**Proof.**  
`up[v]` is computed from the already known values of the parent `p`
of `v`.  
All neighbours of `p` except `v` are exactly the neighbours that the
parent‑side may use as its three children.
For every such neighbour the contribution is `max(1 , best3 of that side)`,
which is already known (`best3[child]` for a child, `up[p]` for the
parent of `p`).  
Choosing the three largest of those contributions yields the maximal
size of a valid partial alkane for the parent side,
and `up[v]` is set to `1 + that_sum`.  
If fewer than three contributions exist, the construction is impossible
and `up[v] = -∞`. ∎



##### Lemma 4  
For every vertex `v`

* `best1[v] = 1 + max_{neighbour u} best3_side(u)`  
  is the size of the largest alkane whose root is `v` and `v` is a leaf.
* `best4[v] = 1 + sum of four largest max(1 , best3_side(u))`  
  is the size of the largest alkane whose root is `v` and `v` is an
  internal vertex.

**Proof.**  
Consider an alkane rooted at `v`.

*If `v` is a leaf* (`deg = 1` in the alkane) it has exactly one neighbour
`u`. The rest of the alkane is a partial alkane rooted at `u` where `u`
has three children (the fourth edge is the edge `u–v`).  
Its size is `best3_side(u)`. Adding the vertex `v` gives
`1 + best3_side(u)`. Maximising over all neighbours yields `best1[v]`.

*If `v` is internal* (`deg = 4` in the alkane) it has exactly four
neighbours. For each neighbour `u` the attached part is either a leaf
(size `1`) or a partial alkane where `u` has three children
(size `best3_side(u)`). The best we can do is to take, for every
neighbour, the larger of the two possibilities, i.e.
`max(1 , best3_side(u))`, and then choose the four neighbours with the
largest such values. Adding the root `v` gives `best4[v]`. ∎



##### Lemma 5  
For every vertex `v` the values `best1[v]` and `best4[v]` computed by the
algorithm are exactly the sizes described in Lemma&nbsp;4.

**Proof.**  
`best3_side(u)` is

* `best3[u]` if `u` is a child of `v` – already computed,
* `up[v]`   if `u` is the parent of `v` – already computed in the
  pre‑order pass.

Consequently the algorithm uses precisely the values required in
Lemma&nbsp;4 and applies the same maximisation / sum‑of‑four operations,
hence obtains the correct sizes. ∎



##### Lemma 6  
The maximum of `best1[v]` and `best4[v]` over all vertices `v`
equals the size of the largest alkane subgraph of the original tree.

**Proof.**  
*Existence.*  
Take any alkane subgraph `A`. Choose an arbitrary vertex `r` of `A` as
its root. By Lemma&nbsp;1 `r` is either a leaf or an internal vertex of
`A`. In the first case `A` is counted by `best1[r]`, in the second case
by `best4[r]`. Therefore the size of `A` does not exceed the maximum of
all those values.

*Achievability.*  
For any vertex `v`, Lemma&nbsp;5 tells us that a concrete alkane of size
`best1[v]` (leaf root) or `best4[v]` (internal root) can be built by
taking, for every neighbour, the best possible attachment described by
the DP values. Hence every value considered in the maximum is realised
by an actual alkane.

Thus the maximum of all `best1[v]` and `best4[v]` is exactly the optimum
size. ∎



##### Lemma 7  
If the algorithm outputs `-1` then the original tree contains no alkane
subgraph.

**Proof.**  
`-1` is printed only when every `best1[v]` and `best4[v]` is impossible.
By Lemma&nbsp;5 an impossible value means that no alkane with that root
exists. Consequently no alkane exists at all. ∎



##### Theorem  
The program prints  

* the maximum possible number of vertices of a subgraph of the given
  tree that is an alkane, or  
* `-1` if no such subgraph exists.

**Proof.**  
If the program prints a positive number, it is the maximum of
`best1[v]` and `best4[v]`. By Lemma&nbsp;6 this number equals the size of
the largest alkane.  
If the program prints `-1`, by Lemma&nbsp;7 no alkane exists.
Therefore in all cases the output is correct. ∎



--------------------------------------------------------------------
#### 6.   Complexity Analysis  

*`N` – number of vertices, `deg(v)` – degree of `v`.*

* building the rooted tree, the three DP passes and the final scan  
  – each edge is inspected a constant number of times  

```
Time   :  O(N)
Memory :  O(N)
```

Both satisfy the limits (`N ≤ 2·10⁵`).

--------------------------------------------------------------------
#### 7.   Reference Implementation  (Python 3)

```python
import sys
import heapq

INF_NEG = -10 ** 9          # value meaning "impossible"


def solve() -> None:
    it = iter(map(int, sys.stdin.buffer.read().split()))
    n = next(it)
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a = next(it) - 1
        b = next(it) - 1
        adj[a].append(b)
        adj[b].append(a)

    # ----------  root the tree ----------
    parent = [-1] * n
    order = []                     # preorder
    stack = [0]
    parent[0] = -2                 # mark root, no parent
    while stack:
        v = stack.pop()
        order.append(v)
        for u in adj[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            stack.append(u)

    # ----------  down DP : best3 ----------
    best3 = [INF_NEG] * n           # only this value is needed
    for v in reversed(order):       # postorder
        child_vals = []
        for u in adj[v]:
            if parent[u] == v:     # child
                val = best3[u] if best3[u] != INF_NEG else 1
                child_vals.append(val)
        if len(child_vals) >= 3:
            top3 = heapq.nlargest(3, child_vals)
            best3[v] = 1 + sum(top3)
        # else stays INF_NEG

    # ----------  up DP ----------
    up = [INF_NEG] * n
    up[0] = INF_NEG                 # root has no parent side

    for v in order:                # preorder, parent already processed
        # build list of neighbour contributions (neighbour id, value)
        neigh = []
        p = parent[v]
        if p != -2:                # has a parent
            if up[v] != INF_NEG:
                val = up[v]
            else:
                val = 1
            neigh.append((p, val))

        for u in adj[v]:
            if parent[u] == v:     # child
                if best3[u] != INF_NEG:
                    val = best3[u]
                else:
                    val = 1
                neigh.append((u, val))

        # we need the best three contributions for each child,
        # therefore we keep the four largest values of the whole list
        if len(neigh) < 4:
            for u in adj[v]:
                if parent[u] == v:
                    up[u] = INF_NEG
            continue

        top_pairs = heapq.nlargest(4, neigh, key=lambda x: x[1])
        sum_top3 = top_pairs[0][1] + top_pairs[1][1] + top_pairs[2][1]
        top3_set = {top_pairs[0][0], top_pairs[1][0], top_pairs[2][0]}

        for u in adj[v]:
            if parent[u] != v:
                continue
            if u not in top3_set:
                sum_excl = sum_top3
            else:
                # child is among the three largest, need the 4th value
                # find its value among the three
                val_u = None
                for nid, val in top_pairs[:3]:
                    if nid == u:
                        val_u = val
                        break
                # there is a fourth entry because len(neigh) >= 4
                next_val = top_pairs[3][1]
                sum_excl = sum_top3 - val_u + next_val
            up[u] = 1 + sum_excl

    # ----------  final answer ----------
    answer = INF_NEG
    for v in range(n):
        # collect best3 of all neighbour sides
        neigh_best3 = []
        for u in adj[v]:
            if parent[u] == v:          # child
                neigh_best3.append(best3[u])
        if parent[v] != -2:            # has a parent
            neigh_best3.append(up[v])

        # ----- leaf root -----
        max_internal = INF_NEG
        for x in neigh_best3:
            if x != INF_NEG and x > max_internal:
                max_internal = x
        if max_internal != INF_NEG:
            best1 = 1 + max_internal
            if best1 > answer:
                answer = best1

        # ----- internal root -----
        if len(neigh_best3) >= 4:
            # contribution of a neighbour = max(1, best3 of that side)
            contribs = [x if x != INF_NEG else 1 for x in neigh_best3]
            top4 = heapq.nlargest(4, contribs)
            best4 = 1 + sum(top4)
            if best4 > answer:
                answer = best4

    if answer == INF_NEG:
        print(-1)
    else:
        print(answer)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required time and memory limits.