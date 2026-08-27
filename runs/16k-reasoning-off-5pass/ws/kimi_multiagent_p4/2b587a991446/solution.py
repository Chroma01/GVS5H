import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it)); M = int(next(it)); S = int(next(it)); T = int(next(it))
    adj = [[] for _ in range(N + 1)]
    deg = [0] * (N + 1)
    for _ in range(M):
        u = int(next(it)); v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    # Feasibility shortcut: on a path graph (M = N-1, all degrees <= 2) the
    # order of the two pieces along the path is invariant, so swapping is
    # impossible. This covers Sample 2 (N = 2, single edge).
    if M == N - 1 and all(deg[v] <= 2 for v in range(1, N + 1)):
        print(-1)
        return

    # Exact BFS on the ordered-pair configuration graph.
    # State (a, b): piece A on a, piece B on b, a != b, encoded a*(N+1)+b.
    W = N + 1
    start = S * W + T
    goal = T * W + S

    dist = {start: 0}
    q = deque([start])
    ans = -1
    while q:
        cur = q.popleft()
        if cur == goal:
            ans = dist[cur]
            break
        a, b = divmod(cur, W)
        d = dist[cur] + 1
        for na in adj[a]:          # move piece A
            if na != b:
                ns = na * W + b
                if ns not in dist:
                    dist[ns] = d
                    q.append(ns)
        for nb in adj[b]:          # move piece B
            if nb != a:
                ns = a * W + nb
                if ns not in dist:
                    dist[ns] = d
                    q.append(ns)

    print(ans)

solve()