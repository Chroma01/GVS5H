**Solution Explanation**

For the whole tree we have `NK` vertices.
We have to cut it into `N` vertex–disjoint simple paths, each path must contain
exactly `K` vertices.
In a path every vertex has degree `1` (an end) or `2` (an interior vertex), therefore
in the whole tree every vertex belongs to **exactly one** of the paths and
its degree inside the used edges is `1` or `2`.

--------------------------------------------------------------------

#### 1.   Tree DP

Root the tree at an arbitrary vertex (vertex `1`).  
For a vertex `v` we look only at the edges to its children.
For a child `c` let `dp[c]` be the length of the *open* part of a path that
ends in `c` (including `c`).  
If a child returns `0` the whole subtree of that child is already a collection of
closed paths, the edge `v‑c` is a *cut* edge (it connects two different path
components).

```
dp[v] = 0                     no open part, v is already inside closed paths
dp[v] = L ( 1 ≤ L < K )       an open part of length L ends in v,
                               it will be continued through the edge to the parent
```

Only the following possibilities are allowed at a vertex

* **no child contributes an open part** – the vertex itself starts a new open
  part of length `1` (it will be an endpoint of the path that goes to the
  parent)

* **exactly one child contributes an open part `x`**

        * `x = K‑1`                     the edge `v‑c` finishes a path,
                                         `v` becomes an endpoint → `dp[v] = 0`
        * `x < K‑1`                     the open part is continued through the
                                         parent → `dp[v] = x+1`

* **exactly two children contribute open parts `x , y`**

        * `x + y = K‑1`                 the two open parts are joined through `v`,
                                         a path of length `K` is finished,
                                         `v` is an interior vertex → `dp[v] = 0`
        * otherwise                     impossible (the vertex would belong to
                                         more than one path)

* **more than two children with an open part** – impossible, the vertex would
  have degree larger than `2` inside the used edges.

All the above rules are local, they only use the `dp` values of the children,
therefore a single post‑order traversal computes the whole array.

--------------------------------------------------------------------

#### 2.   The root

The root has no parent, consequently it may not pass an open part upward.
The only allowed situations for the root are

```
no child with open part                → only possible when K = 1
exactly one child with open part x
        x = K‑1   (the path ends in the root)   → success
        otherwise                              → failure
exactly two children with open parts x , y
        x + y = K‑1                           → success
        otherwise                              → failure
more than two children with open part          → failure
```

If after the whole DFS the root satisfies the condition, a decomposition
exists, otherwise it does not.

`K = 1` is a trivial case: every vertex already is a path of length `1`,
so the answer is always `Yes`.

--------------------------------------------------------------------

#### 3.   Correctness Proof  

We prove that the algorithm prints “Yes” **iff** the required decomposition
exists.

---

##### Lemma 1  
For a vertex `v` (different from the root) the value `dp[v]` returned by the
algorithm is the length of a unique open path segment that starts at a leaf of
the subtree of `v` and ends in `v`.  
If `dp[v]=0` the whole subtree of `v` is already partitioned into closed
paths of length `K`.

**Proof.**  
Induction over the post‑order of the DFS.

*Base – leaf.*  
A leaf has no child, the algorithm sets `dp = 1`.  
The unique open segment consists of the leaf itself, length `1`.  

*Induction step.*  
Assume the statement holds for all children of `v`.  
For every child `c`

* if `dp[c]=0` the child’s subtree is already closed,
  the edge `v‑c` is a cut edge – it does not belong to any open segment,
  and the algorithm ignores it.

* if `dp[c]≠0` the child supplies an open segment of length `dp[c]`.
  Adding the vertex `v` lengthens it to `dp[c]+1`.

All those lengthened segments end in `v`.  
The algorithm pairs at most two of them, exactly when their lengths satisfy
`x + y = K‑1`; then the two segments together with `v` form a closed path of
length `K` and `v` becomes an interior vertex, `dp[v]=0`.  
If no pair can be closed, at most one segment may stay open
(because a vertex can be incident to at most two used edges).
* if there is no such segment, `v` starts a new open segment of length `1`.
* if there is one segment of length `x`  
  – when `x = K‑1` the segment together with `v` already has length `K`,
    it is closed, `dp[v]=0`;  
  – otherwise it is continued, `dp[v]=x+1`.

All cases respect the definition of an open segment, and the construction
covers every vertex of the subtree exactly once. ∎



##### Lemma 2  
If the algorithm finishes with `dp[root] = 0` then the whole tree can be
decomposed into `N` paths of length `K`.

**Proof.**  
By Lemma&nbsp;1 every vertex belongs to exactly one of the three groups

* a closed path of length `K`,
* an open segment that will be continued through the parent,
* a new segment of length `1` (only possible for non‑root vertices).

All closed paths are disjoint and have the required size `K`.  
All open segments are directed towards the root; they never meet
(because a vertex can be incident to at most one open segment that goes
upward).  
At the root the algorithm accepts only the three possibilities listed in
section&nbsp;2, each of them joins the incoming open segments so that they also
become closed paths of length `K`.  
Consequently every vertex lies in a closed path of length `K` and the set of
paths is a partition of the whole tree. ∎



##### Lemma 3  
If a decomposition of the tree into `N` paths of length `K` exists, the
algorithm returns `dp[root] = 0`.

**Proof.**  
Take such a decomposition and orient every path from one endpoint to the other
so that the direction of each used edge is **towards the root** (if a path does
not contain the root, orient it arbitrarily; the root lies in exactly one of the
paths, which is oriented towards the root as well).  
Now look at a vertex `v` (different from the root).

* If the edge to the parent is not used, the whole subtree of `v` is a union
  of complete paths – in the DP the children return `0`.

* If the edge to the parent is used, the path containing `v` enters `v`
  from exactly one child (the previous vertex of the path) and possibly also
  leaves `v` to another child (if `v` is interior) or to the parent (if `v`
  is an endpoint).  
  Consequently at most two children of `v` are incident to used edges.
  Their `dp` values are exactly the lengths of the open parts that have to
  be joined, and they satisfy the conditions used in the algorithm
  (`x = K‑1` or `x + y = K‑1`).  
  The algorithm therefore produces the same value as the real decomposition:
  either `0` (the path is closed at `v`) or `x+1` (the open part is continued).

Proceeding from the leaves upwards the DP reproduces the values forced by the
given decomposition, in particular it never fails.  
At the root the three possibilities of section&nbsp;2 are exactly the three
ways a path that contains the root can end (endpoint, interior, or a single
vertex when `K = 1`).  Hence the algorithm finishes with `dp[root] = 0`. ∎



##### Lemma 4  
`K = 1` is a trivial “Yes” case.

**Proof.**  
When `K = 1` each vertex already is a path of length `1`. ∎



##### Theorem  
The program prints “Yes” if and only if the given tree can be decomposed
into `N` vertex‑disjoint simple paths, each containing exactly `K` vertices.

**Proof.**  

*If the program prints “Yes”.*  
`K = 1` case is covered by Lemma&nbsp;4.  
Otherwise the program finishes with `dp[root] = 0`.  
By Lemma&nbsp;2 the tree can be decomposed as required.

*If such a decomposition exists.*  
`K = 1` is covered by Lemma&nbsp;4.  
Otherwise Lemma&nbsp;3 shows that the DP can never fail and ends with
`dp[root] = 0`, therefore the program prints “Yes”. ∎



--------------------------------------------------------------------

#### 4.   Complexity Analysis

`NK ≤ 2·10⁵`.

* building the adjacency list: `O(NK)`
* one iterative DFS traversal (post‑order): `O(NK)`
* each vertex processes at most two non‑zero child results,
  all operations are `O(1)`

```
Time   :  O(NK)
Memory :  O(NK)
```

Both limits satisfy the constraints.

--------------------------------------------------------------------

#### 5.   Reference Implementation  (Python 3)

```python
import sys

def solve() -> None:
    sys.setrecursionlimit(1 << 25)
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    NK = N * K

    # K = 1 : every vertex is a path of length 1
    if K == 1:
        print("Yes")
        return

    adj = [[] for _ in range(NK + 1)]
    for _ in range(NK - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # ---------- iterative DFS, obtain parent and order ----------
    parent = [0] * (NK + 1)
    order = []
    stack = [1]
    parent[1] = -1            # root marker
    while stack:
        v = stack.pop()
        order.append(v)
        for nb in adj[v]:
            if nb == parent[v]:
                continue
            parent[nb] = v
            stack.append(nb)

    # ---------- DP from leaves upwards ----------
    dp = [0] * (NK + 1)       # 0 .. K-1 ,  -1 means impossible
    for v in reversed(order):
        # collect lengths of open parts coming from children
        active = []
        bad = False
        for nb in adj[v]:
            if nb == parent[v]:
                continue
            if dp[nb] == -1:
                bad = True
                break
            if dp[nb] != 0:
                active.append(dp[nb])
        if bad:
            dp[v] = -1
            continue

        m = len(active)
        if parent[v] == -1:               # root
            if m == 0:
                dp[v] = 0                 # only possible when K == 1 (handled before)
            elif m == 1:
                dp[v] = 0 if active[0] == K - 1 else -1
            elif m == 2:
                dp[v] = 0 if active[0] + active[1] == K - 1 else -1
            else:
                dp[v] = -1
        else:                             # non‑root
            if m == 0:
                dp[v] = 1                 # start a new open segment
            elif m == 1:
                x = active[0]
                if x == K - 1:
                    dp[v] = 0
                elif x < K - 1:
                    dp[v] = x + 1
                else:
                    dp[v] = -1
            elif m == 2:
                dp[v] = 0 if active[0] + active[1] == K - 1 else -1
            else:
                dp[v] = -1

    print("Yes" if dp[1] == 0 else "No")


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required time and memory limits.