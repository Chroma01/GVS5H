import sys

def solve_scipy(data, n, m, x):
    import numpy as np
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import dijkstra

    arr = np.array(list(map(int, data[3:3 + 2 * m])), dtype=np.int64)
    u = arr[0::2] - 1
    v = arr[1::2] - 1
    # dedupe (u,v) pairs so that csr_matrix does not sum duplicate weights
    key = np.unique(u * np.int64(n) + v)
    uu = key // n
    vv = key % n
    idx = np.arange(n, dtype=np.int64)
    rows = np.concatenate([uu, vv + n, idx, idx + n])
    cols = np.concatenate([vv, uu + n, idx + n, idx])
    w = np.concatenate([np.ones(2 * uu.shape[0], dtype=np.float64),
                        np.full(2 * n, float(x), dtype=np.float64)])
    g = csr_matrix((w, (rows, cols)), shape=(2 * n, 2 * n))
    d = dijkstra(g, directed=True, indices=0)
    ans = d[n - 1] if d[n - 1] < d[2 * n - 1] else d[2 * n - 1]
    return int(round(ans))


def solve_pure(data, n, m, x):
    from heapq import heappush, heappop
    S = 2 * n
    us = []
    vs = []
    seen = set()
    ptr = 3
    for _ in range(m):
        a = int(data[ptr]) - 1
        b = int(data[ptr + 1]) - 1
        ptr += 2
        k = a * n + b
        if k in seen:
            continue
        seen.add(k)
        us.append(a)
        vs.append(b)
    del seen
    mm = len(us)
    E = 2 * mm + 2 * n
    deg = [0] * S
    for a in us:
        deg[a] += 1
    for b in vs:
        deg[b + n] += 1
    for i in range(n):
        deg[i] += 1
        deg[i + n] += 1
    start = [0] * (S + 1)
    s = 0
    for i in range(S):
        start[i] = s
        s += deg[i]
    start[S] = s
    pos = start[:]  # copy of size S+1, use first S
    to = [0] * E
    wt = [0] * E
    for i in range(mm):
        a = us[i]
        b = vs[i]
        p = pos[a]
        to[p] = b
        wt[p] = 1
        pos[a] = p + 1
        q = pos[b + n]
        to[q] = a + n
        wt[q] = 1
        pos[b + n] = q + 1
    for i in range(n):
        p = pos[i]
        to[p] = i + n
        wt[p] = x
        pos[i] = p + 1
        q = pos[i + n]
        to[q] = i
        wt[q] = x
        pos[i + n] = q + 1

    INF = float('inf')
    dist = [INF] * S
    dist[0] = 0
    h = [(0, 0)]
    while h:
        d, v = heappop(h)
        if d > dist[v]:
            continue
        i = start[v]
        e = start[v + 1]
        while i < e:
            nv = to[i]
            nd = d + wt[i]
            if nd < dist[nv]:
                dist[nv] = nd
                heappush(h, (nd, nv))
            i += 1
    a1 = dist[n - 1]
    a2 = dist[2 * n - 1]
    return a1 if a1 < a2 else a2


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    x = int(data[2])
    try:
        ans = solve_scipy(data, n, m, x)
    except ImportError:
        ans = solve_pure(data, n, m, x)
    sys.stdout.write(str(ans) + "\n")


main()