
## ideation
### Answer
```python
import sys
from collections import deque
from array import array

INF = 2000000000          # larger than any building height ( ≤ 10^6 )


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
    edges.sort(reverse=True)          # sort by weight descending

    parent = list(range(N))
    size = [1] * N

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> bool:
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    adj = [[] for _ in range(N)]      # tree adjacency (only MST edges)
    for w, u, v in edges:
        if union(u, v):
            adj[u].append((v, w))
            adj[v].append((u, w))

    # ----- root the tree, compute depth and edge to parent -----
    par = [-1] * N
    depth = [0] * N
    edge_to_par = [INF] * N
    visited = [False] * N

    q = deque([0])
    visited[0] = True
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if visited[v]:
                continue
            visited[v] = True
            par[v] = u
            depth[v] = depth[u] + 1
            edge_to_par[v] = w
            q.append(v)

    # ----- binary lifting tables (up, minEdge) -----
    LOG = (N + 1).bit_length()
    up = [array('I', [0]) * (N + 1) for _ in range(LOG)]
    minW = [array('I', [INF]) * (N + 1) for _ in range(LOG)]

    up0 = up[0]
    minW0 = minW[0]
    for i in range(N):
        p = par[i]
        up0[i] = N if p == -1 else p
        minW0[i] = edge_to_par[i]
    up0[N] = N               # sentinel
    minW0[N] = INF

    for k in range(1, LOG):
        upk = up[k]
        upkm1 = up[k - 1]
        minWk = minW[k]
        minWkm1 = minW[k - 1]
        for i in range(N + 1):
            anc = upkm1[i]
            upk[i] = upkm1[anc]
            a = minWkm1[i]
            b = minWkm1[anc]
            minWk[i] = a if a < b else b

    # ----- function: minimum edge weight on the tree path -----
    def min_edge_on_path(u: int, v: int) -> int:
        if u == v:
            return INF
        best = INF
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        bit = 0
        while diff:
            if diff & 1:
                wgt = minW[bit][u]
                if wgt < best:
                    best = wgt
                u = up[bit][u]
            diff >>= 1
            bit += 1
        if u == v:
            return best
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                wgt = minW[k][u]
                if wgt < best:
                    best = wgt
                wgt2 = minW[k][v]
                if wgt2 < best:
                    best = wgt2
                u = up[k][u]
                v = up[k][v]
        wgt = minW[0][u]
        if wgt < best:
            best = wgt
        wgt2 = minW[0][v]
        if wgt2 < best:
            best = wgt2
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

## worker: finalize
**Algorithm Overview**

1. **Graph model** – For two adjacent cells `u , v` define the edge weight `w(u,v) = min(F[u], F[v])`.  
   On any floor `L` the walkway can be used exactly on the edges with `w ≥ L`.  
   Thus the largest floor on which a walkway path exists between cells `s` and `t` is the **maximum bottleneck** of the graph:
   ```
   M(s,t) = max over all paths P  min_{(u,v)∈P} w(u,v)
   ```

2. **Maximum bottleneck via MST** – In a *maximum* spanning tree (MST) of the whole grid the minimum edge weight on the unique tree‑path between two vertices equals `M(s,t)`.  
   Therefore we only need:
   * Build a maximum spanning tree (Kruskal on the edges sorted descending).
   * Answer the query for `M(s,t)` as the minimum edge weight on that tree path.

3. **Answering a query** – Let `M = M(s,t)`.  
   *If `min(Y,Z) ≤ M`* we can walk on a floor inside the interval `[min(Y,Z), max(Y,Z)]`; the stair cost is `|Y‑Z|`.  
   *Otherwise* we must descend both buildings to floor `M`, costing `Y + Z – 2·M`.

4. **Tree queries** – The tree is rooted arbitrarily (cell 0).  
   Binary lifting (`up` table) and a parallel `minEdge` table are pre‑computed in `O(N log N)`.  
   Minimum edge on a path is found in `O(log N)` time.
