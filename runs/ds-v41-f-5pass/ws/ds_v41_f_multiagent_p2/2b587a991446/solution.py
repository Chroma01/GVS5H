import sys
from collections import deque

INF = float('inf')


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0]); m = int(data[1]); S = int(data[2]); T = int(data[3])
    adj = [[] for _ in range(n + 1)]
    edges = []
    idx = 4
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v); adj[v].append(u)
        edges.append((u, v))
    ans = solve(n, m, S, T, adj, edges)
    sys.stdout.write(str(ans) + "\n")


def bfs(n, adj, src):
    dist = [-1] * (n + 1)
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        du = dist[u] + 1
        for w in adj[u]:
            if dist[w] < 0:
                dist[w] = du
                dq.append(w)
    return dist


def brute(n, adj, S, T):
    base = n + 1
    size = base * base
    dist = [-1] * size
    start = S * base + T
    target = T * base + S
    dist[start] = 0
    dq = deque([start])
    while dq:
        st = dq.popleft()
        d = dist[st]
        a = st // base
        b = st - a * base
        for na in adj[a]:
            if na != b:
                ns = na * base + b
                if dist[ns] < 0:
                    if ns == target:
                        return d + 1
                    dist[ns] = d + 1
                    dq.append(ns)
        for nb in adj[b]:
            if nb != a:
                ns = a * base + nb
                if dist[ns] < 0:
                    if ns == target:
                        return d + 1
                    dist[ns] = d + 1
                    dq.append(ns)
    return -1


def min_cycle_term(n, adj, edges, root, d_root, d_other):
    # BFS tree from root
    parent = [0] * (n + 1)
    visited = bytearray(n + 1)
    visited[root] = 1
    dq = deque([root])
    while dq:
        u = dq.popleft()
        for w in adj[u]:
            if not visited[w]:
                visited[w] = 1
                parent[w] = u
                dq.append(w)

    LOG = n.bit_length()
    up = [parent]
    down = [d_other]
    for k in range(1, LOG):
        pu = up[k - 1]; pm = down[k - 1]
        cu = [0] * (n + 1); cm = [0] * (n + 1)
        for v in range(1, n + 1):
            mid = pu[v]
            if mid:
                cu[v] = pu[mid]
                a = pm[v]; b = pm[mid]
                cm[v] = a if a < b else b
            else:
                cm[v] = pm[v]
        up.append(cu); down.append(cm)

    depth = d_root
    best = INF
    for (a0, b0) in edges:
        if parent[a0] == b0 or parent[b0] == a0:
            continue
        a = a0; b = b0
        res = INF
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        k = 0
        while diff:
            if diff & 1:
                v = down[k][a]
                if v < res: res = v
                a = up[k][a]
            diff >>= 1
            k += 1
        if a != b:
            for k in range(LOG - 1, -1, -1):
                ua = up[k][a]; ub = up[k][b]
                if ua != ub:
                    va = down[k][a]; vb = down[k][b]
                    if va < res: res = va
                    if vb < res: res = vb
                    a = ua; b = ub
            L = up[0][a]
            va = d_other[a]; vb = d_other[b]
            if va < res: res = va
            if vb < res: res = vb
        else:
            L = a
        base = depth[a0] + depth[b0]
        cost1 = 2 * res + base + 1
        cost2 = 2 * d_other[L] + base + 3
        cost = cost1 if cost1 < cost2 else cost2
        if cost < best:
            best = cost
    return best


def solve(n, m, S, T, adj, edges):
    if n <= 100:
        return brute(n, adj, S, T)

    dS = bfs(n, adj, S)
    dT = bfs(n, adj, T)
    best = INF

    deg = [len(adj[v]) for v in range(n + 1)]

    # ---- BRANCH term ----
    # entry neighbour counts / unique entries
    cntS = [0] * (n + 1); s_entry = [0] * (n + 1)
    cntT = [0] * (n + 1); t_entry = [0] * (n + 1)
    for (u, v) in edges:
        if dS[v] == dS[u] + 1:
            cntS[v] += 1; s_entry[v] = u
        elif dS[u] == dS[v] + 1:
            cntS[u] += 1; s_entry[u] = v
        if dT[v] == dT[u] + 1:
            cntT[v] += 1; t_entry[v] = u
        elif dT[u] == dT[v] + 1:
            cntT[u] += 1; t_entry[u] = v

    for v in range(1, n + 1):
        if deg[v] < 3:
            continue
        if v == S or v == T:
            extra = 4
        elif cntS[v] == 1 and cntT[v] == 1 and s_entry[v] == t_entry[v]:
            extra = 4
        else:
            extra = 2
        c = 2 * dS[v] + 2 * dT[v] + extra
        if c < best:
            best = c

    # ---- CYCLE term ----
    if m > n - 1:
        c1 = min_cycle_term(n, adj, edges, S, dS, dT)
        if c1 < best:
            best = c1
        c2 = min_cycle_term(n, adj, edges, T, dT, dS)
        if c2 < best:
            best = c2

    return -1 if best == INF else best


if __name__ == "__main__":
    main()