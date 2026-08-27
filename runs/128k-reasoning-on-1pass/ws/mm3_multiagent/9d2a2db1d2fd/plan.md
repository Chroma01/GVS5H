**Solution Explanation**

For every block `(i , j)` there is a building with `F[i][j]` floors.
While Takahashi is on floor `X`

* he can move to the next floor inside the same building – this costs **1**
  stair step,
* he can move to a cardinally adjacent building whose height is at least `X`
  – this costs **0** stair steps (a walkway).

For a query  

```
(A , B , Y)  →  (C , D , Z)
```

we have to minimise the total number of stair steps.



--------------------------------------------------------------------

#### 1.   From floors to a graph

For a fixed floor `L ( 1 ≤ L ≤ 10^6 )`

```
cells with height ≥ L   form a sub‑graph G(L)
edge (u , v) exists  ⇔  both cells have height ≥ L
```

Walking on a walkway never changes the floor, therefore inside `G(L)`
all moves are free.

*If we are on floor `L` we may walk arbitrarily inside the connected
component of `G(L)`.*

--------------------------------------------------------------------

#### 2.   How high can we walk?

For two cells `s , t`

```
M(s , t) = max L  such that s and t are in the same component of G(L)
```

`M(s , t)` is the **maximum floor** at which we can reach `t` from `s`
using only walkways.  
If we know `M` we can finish the query:

* let `Y , Z` be the required start / target floors,
* `L` may be any value `≤ M`.

The cheapest choice is

```
if  min(Y , Z) ≤ M          →  answer = |Y – Z|                (stay inside the interval)
else                         answer = |Y – M| + |Z – M|
                               = Y + Z – 2·M                 (both floors must be lowered)
```

*Proof* – `M` is the largest floor on which a walkway path exists.
If the interval `[ min(Y,Z) , max(Y,Z) ]` contains a value `≤ M`
we can keep a floor inside this interval, walk for free, and only have
to change the floor inside the start / target building: cost `|Y‑Z|`.
Otherwise we must go down to the highest possible floor `M`
in **both** buildings, the cost is exactly `Y+Z‑2M`. ∎



--------------------------------------------------------------------

#### 3.   Computing `M(s , t)` – the maximum bottleneck

For an adjacent pair of cells

```
edge weight w(u , v) = min( F[u] , F[v] )
```

`w(u , v)` is the highest floor on which this edge can be used,
because both buildings must have at least that many floors.

For any floor `L` the edge belongs to `G(L)` **iff** `w(u , v) ≥ L`.
Consequently

```
s and t are connected in G(L)  ⇔  there exists a path whose every edge has weight ≥ L
```

The largest `L` is therefore the **maximum bottleneck** of the graph,
i.e. the maximum possible value of the minimum edge weight on a path
between `s` and `t`.

A classic theorem (MST property) states:

> In a *maximum* spanning tree (MST) of a weighted graph,
> for every pair of vertices the minimum edge weight on their unique
> tree‑path equals the maximum bottleneck value of the original graph.

So it is enough to

* build a **maximum spanning tree** of the whole grid,
  edge weight `w = min( heights )`,
* for a query answer the **minimum edge weight on the tree path**
  between the two cells – that value is exactly `M(s , t)`.



--------------------------------------------------------------------

#### 4.   Building the maximum spanning tree

```
edges = all cardinally adjacent pairs
weight = min( height of the two cells )
```

Sort edges decreasing by weight, run Kruskal’s algorithm
(Union‑Find).  
Whenever two different components are merged we add this edge to the
tree (both directions).  
The grid is connected, therefore the result is a spanning **tree**
with `N‑1` edges (`N = H·W ≤ 250 000`).

Complexities  

```
edges ≤ 2·N ≤ 5·10^5
sorting                 : O(E log E)
Union‑Find unions       : O(E α(N))
building adjacency list : O(N)
```

--------------------------------------------------------------------

#### 5.   Queries on a tree – LCA with binary lifting

The tree is rooted (arbitrarily, node `0`).  
For every node we store

* `depth[node]`,
* `up[k][node]` – the 2^k‑th ancestor,
* `minEdge[k][node]` – the minimum edge weight on the upward path of
  length `2^k`.

Pre‑computation (`log = ⌈log2 N⌉ ≤ 19`)

```
up[0]      = parent
minEdge[0] = weight of edge to parent (∞ for the root)

for k = 1 … log‑1
        up[k][v]      = up[k‑1][ up[k‑1][v] ]
        minEdge[k][v] = min( minEdge[k‑1][v] , minEdge[k‑1][ up[k‑1][v] ] )
```

Both tables need `N·log` integers – about 5·10^6 integers.
Storing them in `array('I')` (C‑unsigned int) needs only ~20 MiB.

**Query `M(s , t)`**

```
if s == t : return ∞

bring deeper node up to the same depth,
   each jump updates current answer with the corresponding minEdge

if now equal → answer is the best value found

else lift both nodes together from the highest power downwards
while their ancestors differ,
   again update answer with the two minEdge values

finally add the two last edges to the parents
```

The whole procedure needs `O(log N)` time.



--------------------------------------------------------------------

#### 6.   Answering the original query

For each of the `Q` queries

```
u = id(A , B)          # 0‑based linear id
v = id(C , D)

if u == v                     → answer = |Y – Z|
else
        M = minimum_edge_on_path(u , v)   # from the tree
        if min(Y , Z) ≤ M   → answer = |Y – Z|
        else                → answer = Y + Z – 2·M
```

All operations are `O(log N)`.  
With `Q ≤ 2·10^5` the total work is below `4·10^6` elementary steps.



--------------------------------------------------------------------

#### 7.   Correctness Proof  

We prove that the algorithm outputs the minimal possible number of
stair uses for every query.

---

##### Lemma 1  
For a fixed floor `L` the cells with height `≥ L` together with the
adjacent pairs among them form the graph `G(L)`.  
Inside a connected component of `G(L)` Takahashi can move arbitrarily
without using stairs.

*Proof.*  
All edges of `G(L)` connect two buildings that both have at least `L`
floors, therefore the walkway can be used on any floor `≤ L`.  
No stair movement is needed while staying on the same floor, and the
graph is precisely the set of possible walkway moves. ∎



##### Lemma 2  
Let `M(s , t)` be the largest floor `L` such that `s` and `t` lie in the
same component of `G(L)`.  
For every floor `L > M(s , t)` the cells `s` and `t` are **not**
connected in `G(L)`.

*Proof.*  
If they were connected for some `L > M`, then by definition `L` would be
a feasible floor, contradicting the maximality of `M`. ∎



##### Lemma 3  
For any two cells `s , t` let `w(u , v) = min(F[u] , F[v])` be the weight
of the edge `(u , v)`.  
The value  

```
B(s , t) = max over all paths P   min_{(u , v)∈P} w(u , v)
```

equals `M(s , t)`.

*Proof.*  
A path `P` is usable on floor `L` **iff** every edge of `P` has
`w ≥ L`.  
Thus a floor `L` is feasible exactly when there exists a path whose
minimum edge weight is at least `L`.  
The largest such `L` is precisely the maximum bottleneck `B(s , t)`. ∎



##### Lemma 4  
In a **maximum** spanning tree `T` of the whole grid,
for any two vertices `s , t`

```
min_{(u , v) on the unique tree path} w(u , v)  =  B(s , t)
```

*Proof.*  
Standard property of maximum spanning trees:  
among all paths between the two vertices, the tree path maximises the
minimum edge weight, i.e. the tree path is a *maximum bottleneck path*.
Therefore the minimum weight on the tree path equals `B(s , t)`. ∎



##### Lemma 5  
For a query `(A , B , Y) → (C , D , Z)` let  

```
M = minimum edge weight on the tree path between the two cells.
```

Then the optimal number of stair uses is

```
| Y – Z |                     if  min(Y , Z) ≤ M
Y + Z – 2·M                  otherwise.
```

*Proof.*  
From Lemma&nbsp;4 the value `M` equals `B(s , t) = M(s , t)`,
the highest floor on which a walkway path exists.
*Case 1* – `min(Y , Z) ≤ M`.  
Choose any floor `L` with `min(Y , Z) ≤ L ≤ max(Y , Z)`.
Both start and target buildings contain `L`,
the two cells are connected in `G(L)`, thus Takahashi walks for free,
only the vertical moves inside the two buildings are needed:
`|Y‑Z|` stairs.

*Case 2* – `min(Y , Z) > M`.  
No floor `L` inside the interval `[min(Y,Z), max(Y,Z)]` is feasible
(because it is larger than `M`).  
The best we can do is to lower both buildings to the highest feasible
floor `L = M`.  
Stair usage: `Y‑M` down in the start building, `Z‑M` up (or down) in the
target building, total `Y+Z‑2M`.  
Any other strategy would need a floor larger than `M` on at least one
building, impossible by Lemma&nbsp;2. ∎



##### Lemma 6  
The algorithm outputs exactly the value described in Lemma&nbsp;5.

*Proof.*  
The algorithm

* builds the maximum spanning tree,
* for each query computes `M` as the minimum edge weight on the tree
  path (binary lifting) – exactly the value of Lemma&nbsp;5,
* applies the case distinction of Lemma&nbsp;5 and prints the
  corresponding formula.

Thus the printed number coincides with the optimum. ∎



##### Theorem  
For every query the program prints the minimum possible number of times
Takahashi uses stairs.

*Proof.*  
By Lemma&nbsp;4 the tree path’s minimum edge weight equals the
maximum bottleneck `M(s , t)`.  
Lemma&nbsp;5 shows that the optimum stair count depends only on this
value and on the start / target floors, and gives its exact value.
Lemma&nbsp;6 proves that the program computes exactly that value.
Therefore the program’s output equals the true optimum for every
query. ∎



--------------------------------------------------------------------

#### 8.   Complexity Analysis  

```
N = H·W          ≤ 250 000
E = number of adjacent pairs ≤ 2·N ≤ 500 000
Q ≤ 200 000
log = ⌈log2 N⌉ ≤ 19
```

* building edges & sorting                : `O(E log E)`
* Kruskal (Union‑Find)                    : `O(E α(N))`
* building the tree adjacency             : `O(N)`
* binary lifting preprocessing            : `O(N log N)`
* each query (LCA + formula)             : `O(log N)`

Overall  

```
Time   :  O( (E + N) log N + Q log N )   <  2·10^7 elementary operations
Memory :  edges  (~5·10^5)  +  tree adjacency  (2·(N‑1) edges)
          +  up / minEdge tables  (2·N·log integers)
          +  Union‑Find arrays  (2·N)
          ≤  150 MiB   (well inside typical limits)
```

--------------------------------------------------------------------

#### 9.   Reference Implementation  (Python 3)

```python
import sys
from collections import deque
from array import array

INF = 0xFFFFFFFF          # larger than any building height ( ≤ 10^6 )


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    H = int(next(it))
    W = int(next(it))
    N = H * W                     # number of cells, 0‑based id = i*W + j

    # read heights
    F = [[0] * W for _ in range(H)]
    for i in range(H):
        row = F[i]
        for j in range(W):
            row[j] = int(next(it))

    # ----- build edges (weight = min of the two heights) -----
    edges = []
    for i in range(H):
        for j in range(W):
            uid = i * W + j
            if j + 1 < W:
                vid = uid + 1
                w = F[i][j] if F[i][j] < F[i][j + 1] else F[i][j + 1]
                edges.append((w, uid, vid))
            if i + 1 < H:
                vid = uid + W
                w = F[i][j] if F[i][j] < F[i + 1][j] else F[i + 1][j]
                edges.append((w, uid, vid))

    # ----- maximum spanning tree (Kruskal) -----
    edges.sort(key=lambda x: x[0], reverse=True)

    parent = list(range(N))
    size = [1] * N

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> bool:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    adj = [[] for _ in range(N)]          # tree adjacency
    for w, u, v in edges:
        if union(u, v):
            adj[u].append((v, w))
            adj[v].append((u, w))

    # ----- root the tree, compute depth and edge to parent -----
    par = [-1] * N
    depth = [0] * N
    edge_to_par = [INF] * N

    q = deque([0])
    par[0] = -1
    depth[0] = 0
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if v == par[u]:
                continue
            par[v] = u
            depth[v] = depth[u] + 1
            edge_to_par[v] = w
            q.append(v)

    # ----- binary lifting tables (up, minEdge) -----
    LOG = (N).bit_length()
    up = [array('I', [0]) * N for _ in range(LOG)]
    minW = [array('I', [INF]) * N for _ in range(LOG)]

    up0 = up[0]
    minW0 = minW[0]
    for i in range(N):
        p = par[i]
        up0[i] = N if p == -1 else p
        minW0[i] = edge_to_par[i]

    for k in range(1, LOG):
        upk = up[k]
        upkm1 = up[k - 1]
        minWk = minW[k]
        minWkm1 = minW[k - 1]
        for i in range(N):
            anc = upkm1[i]
            if anc != N:
                upk[i] = upkm1[anc]
                a = minWkm1[i]
                b = minWkm1[anc]
                minWk[i] = a if a < b else b
            else:
                upk[i] = N
                minWk[i] = minWkm1[i]

    # ----- function: minimum edge weight on the tree path -----
    def min_edge_on_path(u: int, v: int) -> int:
        if u == v:
            return INF
        du = depth[u]
        dv = depth[v]
        if du < dv:
            u, v = v, u
            du, dv = dv, du

        best = INF
        diff = du - dv
        bit = 0
        while diff:
            if diff & 1:
                w = minW[bit][u]
                if w < best:
                    best = w
                u = up[bit][u]
            diff >>= 1
            bit += 1

        if u == v:
            return best

        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                wu = minW[k][u]
                if wu < best:
                    best = wu
                wv = minW[k][v]
                if wv < best:
                    best = wv
                u = up[k][u]
                v = up[k][v]

        # last edges to LCA
        wu = minW[0][u]
        if wu < best:
            best = wu
        wv = minW[0][v]
        if wv < best:
            best = wv
        return best

    # ----- answer queries -----
    Q = int(next(it))
    out = []
    for _ in range(Q):
        A = int(next(it)) - 1
        B = int(next(it)) - 1
        Y = int(next(it))
        C = int(next(it)) - 1
        D = int(next(it)) - 1
        Z = int(next(it))

        u = A * W + B
        v = C * W + D

        if u == v:                     # same building, only stairs needed
            ans = abs(Y - Z)
        else:
            M = min_edge_on_path(u, v)   # maximum feasible floor
            if min(Y, Z) <= M:
                ans = abs(Y - Z)
            else:
                ans = Y + Z - 2 * M
        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input‑output format.