import sys
from collections import deque


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, S, T = data[0], data[1], data[2], data[3]
    adj = [[] for _ in range(N + 1)]
    pos = 4
    for _ in range(M):
        u = data[pos]
        v = data[pos + 1]
        pos += 2
        adj[u].append(v)
        adj[v].append(u)
    data = None

    def bfs(start, keep_order=False):
        dist = [-1] * (N + 1)
        q = deque([start])
        dist[start] = 0
        order = [] if keep_order else None
        while q:
            u = q.popleft()
            if keep_order:
                order.append(u)
            nd = dist[u] + 1
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = nd
                    q.append(v)
        return dist, order

    distS, orderS = bfs(S, True)
    distT, _ = bfs(T, False)
    d = distS[T]

    # Count shortest S-T paths in the shortest-path DAG, capped at 2.
    dp = [0] * (N + 1)
    dp[S] = 1
    for u in orderS:
        du = dp[u]
        if du == 0:
            continue
        dsu = distS[u]
        for v in adj[u]:
            if distS[v] == dsu + 1 and dsu + 1 + distT[v] == d:
                if dp[v] < 2:
                    nv = dp[v] + du
                    if nv > 2:
                        nv = 2
                    dp[v] = nv
                    if v == T and nv == 2:
                        print(2 * d)
                        return

    if dp[T] >= 2:
        print(2 * d)
        return

    # Reconstruct the unique shortest path P.
    p = [S]
    for i in range(1, d + 1):
        prev = p[-1]
        nxt = 0
        for v in adj[prev]:
            if distS[v] == i and distT[v] == d - i:
                nxt = v
                break
        if nxt == 0:
            print(-1)
            return
        p.append(nxt)

    on = bytearray(N + 1)
    for v in p:
        on[v] = 1

    # Free memory no longer needed.
    dp = None
    orderS = None
    distT = None

    INF = 10 ** 18
    dist = [INF] * (N + 1)

    # Small-weight Dijkstra (weights 0, 1, 2) using three buckets.
    buckets = [deque(), deque(), deque()]
    cur = 0
    idx = 0

    # Sources: leave P at any P[i] with i < d.
    for i in range(d):
        u = p[i]
        for x in adj[u]:
            if not on[x]:
                w = 1 - (distS[x] - i)
                if w < dist[x]:
                    dist[x] = w
                    buckets[w % 3].append(x)

    while True:
        if not buckets[idx]:
            if not buckets[(idx + 1) % 3]:
                if not buckets[(idx + 2) % 3]:
                    break
                cur += 2
                idx = (idx + 2) % 3
            else:
                cur += 1
                idx = (idx + 1) % 3

        u = buckets[idx].popleft()
        if dist[u] != cur:
            continue

        dsu = distS[u]
        for v in adj[u]:
            if on[v]:
                continue
            w = 1 - (distS[v] - dsu)
            nd = cur + w
            if nd < dist[v]:
                dist[v] = nd
                buckets[(idx + w) % 3].append(v)

    # Targets: re-enter P at any P[j] with j > 0.
    best = INF
    for j in range(1, d + 1):
        u = p[j]
        for x in adj[u]:
            if not on[x]:
                dx = dist[x]
                if dx != INF:
                    extra = dx + 1 - (j - distS[x])
                    if extra < best:
                        best = extra

    if best == INF:
        print(-1)
    else:
        print(2 * d + best)


if __name__ == "__main__":
    main()