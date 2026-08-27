import sys
import numpy as np
from collections import deque

def solve():
    data = np.fromstring(sys.stdin.buffer.read(), sep=' ', dtype=np.int64)
    pos = 0
    H = int(data[pos]); W = int(data[pos+1]); pos += 2
    N = H * W
    F = data[pos:pos+N].copy(); pos += N
    Q = int(data[pos]); pos += 1
    qs = data[pos:pos+6*Q].reshape(Q, 6)
    A = qs[:,0]-1; B = qs[:,1]-1; Y = qs[:,2]
    C = qs[:,3]-1; D = qs[:,4]-1; Z = qs[:,5]
    U0 = (A * W + B).astype(np.int32)
    V0 = (C * W + D).astype(np.int32)

    INF = 1 << 30

    # ---- Build maximum spanning tree (Kruskal via descending vertex activation) ----
    parent = list(range(N))
    size = [1] * N

    def find(x, parent=parent):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    order = np.argsort(F, kind='stable')[::-1].tolist()
    added = bytearray(N)
    adj = [[] for _ in range(N)]
    Flist = F.tolist()
    for vtx in order:
        added[vtx] = 1
        i, j = divmod(vtx, W)
        wv = Flist[vtx]
        # neighbors
        if i > 0:
            nb = vtx - W
            if added[nb]:
                ra, rb = find(vtx), find(nb)
                if ra != rb:
                    if size[ra] < size[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    size[ra] += size[rb]
                    adj[vtx].append((nb, wv))
                    adj[nb].append((vtx, wv))
        if i < H - 1:
            nb = vtx + W
            if added[nb]:
                ra, rb = find(vtx), find(nb)
                if ra != rb:
                    if size[ra] < size[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    size[ra] += size[rb]
                    adj[vtx].append((nb, wv))
                    adj[nb].append((vtx, wv))
        if j > 0:
            nb = vtx - 1
            if added[nb]:
                ra, rb = find(vtx), find(nb)
                if ra != rb:
                    if size[ra] < size[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    size[ra] += size[rb]
                    adj[vtx].append((nb, wv))
                    adj[nb].append((vtx, wv))
        if j < W - 1:
            nb = vtx + 1
            if added[nb]:
                ra, rb = find(vtx), find(nb)
                if ra != rb:
                    if size[ra] < size[rb]:
                        ra, rb = rb, ra
                    parent[rb] = ra
                    size[ra] += size[rb]
                    adj[vtx].append((nb, wv))
                    adj[nb].append((vtx, wv))

    # ---- BFS for depth / parent / edge-weight-to-parent ----
    depth = [-1] * N
    par = [0] * N
    pw = [INF] * N
    depth[0] = 0
    par[0] = 0
    dq = deque([0])
    while dq:
        x = dq.popleft()
        dx = depth[x]
        for nb, w in adj[x]:
            if depth[nb] == -1:
                depth[nb] = dx + 1
                par[nb] = x
                pw[nb] = w
                dq.append(nb)

    # ---- Binary lifting tables ----
    LOG = 18
    while (1 << LOG) < N:
        LOG += 1
    up = np.empty((LOG, N), dtype=np.int32)
    mn = np.empty((LOG, N), dtype=np.int32)
    up[0] = np.array(par, dtype=np.int32)
    mn[0] = np.array(pw, dtype=np.int32)
    for k in range(1, LOG):
        prev = up[k-1]
        up[k] = prev[prev]
        mn[k] = np.minimum(mn[k-1], mn[k-1][prev])

    # ---- Answer queries (vectorized) ----
    darr = np.array(depth, dtype=np.int32)
    U = U0.copy()
    V = V0.copy()

    # ensure depth[U] >= depth[V]
    swap = darr[U] < darr[V]
    tmp = U[swap].copy()
    U[swap] = V[swap]
    V[swap] = tmp

    ans = np.full(Q, INF, dtype=np.int64)

    diff = (darr[U] - darr[V]).astype(np.int64)
    for k in range(LOG):
        cond = ((diff >> k) & 1).astype(bool)
        if cond.any():
            ans = np.where(cond, np.minimum(ans, mn[k][U].astype(np.int64)), ans)
            U = np.where(cond, up[k][U], U)

    neq = U != V
    for k in range(LOG - 1, -1, -1):
        cond = neq & (up[k][U] != up[k][V])
        if cond.any():
            m = np.minimum(mn[k][U], mn[k][V]).astype(np.int64)
            ans = np.where(cond, np.minimum(ans, m), ans)
            U = np.where(cond, up[k][U], U)
            V = np.where(cond, up[k][V], V)
    cond = U != V
    if cond.any():
        m = np.minimum(mn[0][U], mn[0][V]).astype(np.int64)
        ans = np.where(cond, np.minimum(ans, m), ans)

    # same block: x_max = F of the block
    same = U0 == V0
    if same.any():
        ans = np.where(same, F[U0].astype(np.int64), ans)

    x_max = ans
    mnYZ = np.minimum(Y, Z)
    res = np.where(x_max >= mnYZ, np.abs(Y - Z), Y + Z - 2 * x_max)
    sys.stdout.write('\n'.join(map(str, res.tolist())) + '\n')

solve()