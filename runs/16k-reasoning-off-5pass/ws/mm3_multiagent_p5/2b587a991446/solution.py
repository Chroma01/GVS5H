import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    S = int(next(it)) - 1
    T = int(next(it)) - 1
    adj = [[] for _ in range(N)]
    deg = [0] * N
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    if S == T:
        print(0)
        return

    def bfs(src):
        dist = [-1] * N
        dist[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return dist

    distS = bfs(S)
    distT = bfs(T)
    D = distS[T]
    DT = distT[S]

    if D == -1 or DT == -1:
        print(-1)
        return

    # Case 1: S and T are adjacent.
    if D == 1:
        # Need at least one branch to maneuver.
        if deg[S] >= 2 or deg[T] >= 2:
            print(3)
        else:
            print(-1)
        return

    # Case 2: D >= 2.
    # Detect if the graph is a simple path (all degrees <= 2).
    # On a path, two pieces cannot swap.
    is_path = (N > 2 and all(d <= 2 for d in deg))
    if is_path:
        print(-1)
        return

    # BFS on state graph (a, b) with a != b.
    # State space: O(N^2) in worst case, but for non-path graphs
    # with M <= 2e5, the BFS is feasible.
    # We use an array indexed by a*N + b for fast visited check.
    # This requires O(N^2) memory which may be too large.
    # Instead, use a dict or a set of encoded states.
    # For efficiency, we use a dict {key: distance}.
    # key = a * N + b
    visited = {}
    start_key = S * N + T
    visited[start_key] = 0
    q = deque([(S, T)])
    goal_key = T * N + S
    cut_off = D + DT + 2
    ans = -1
    while q:
        a, b = q.popleft()
        d = visited[a * N + b]
        if a * N + b == goal_key:
            ans = d
            break
        if d >= cut_off:
            continue
        # Move A to a neighbor na of a, na != b
        for na in adj[a]:
            if na != b:
                key = na * N + b
                if key not in visited:
                    visited[key] = d + 1
                    q.append((na, b))
        # Move B to a neighbor nb of b, nb != a
        for nb in adj[b]:
            if nb != a:
                key = a * N + nb
                if key not in visited:
                    visited[key] = d + 1
                    q.append((a, nb))
    print(ans if ans != -1 else -1)

solve()