import sys
from collections import deque

def main():
    input = sys.stdin.readline
    N, M, K = map(int, input().split())
    edges = []
    for _ in range(M):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))

    # Reachable set from vertex 0 (original vertex 1)
    adj = [[] for _ in range(N)]
    for u, v in edges:
        adj[u].append(v)
    reachable = [False] * N
    reachable[0] = True
    dq = deque([0])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if not reachable[y]:
                reachable[y] = True
                dq.append(y)

    # Compress to reachable vertices only (vertex N-1 is guaranteed reachable)
    verts = [i for i in range(N) if reachable[i]]
    idx = {v: i for i, v in enumerate(verts)}
    r = len(verts)
    src = idx[0]
    dst = idx[N - 1]

    # Filter edges to those with both endpoints reachable
    E = []
    in_edges = [[] for _ in range(r)]
    for u, v in edges:
        if reachable[u] and reachable[v]:
            a, b = idx[u], idx[v]
            E.append((a, b))
            in_edges[b].append(a)

    # Unweighted shortest path distances sp[] from source (within reachable graph)
    INF = 10 ** 9
    sp = [INF] * r
    sp[src] = 0
    radj = [[] for _ in range(r)]
    for a, b in E:
        radj[a].append(b)
    dq = deque([src])
    while dq:
        x = dq.popleft()
        for y in radj[x]:
            if sp[y] == INF:
                sp[y] = sp[x] + 1
                dq.append(y)

    # Cap each potential by min(sp, K); source fixed at 0
    cap = [0] * r
    for i in range(r):
        cap[i] = min(sp[i], K)
    cap[src] = 0

    max_possible = min(sp[dst], K)

    start = tuple([0] * r)
    visited = set([start])
    stack = [start]
    ans = 0

    while stack:
        p = stack.pop()
        if p[dst] > ans:
            ans = p[dst]
            if ans >= max_possible:
                break
        # Try raising each vertex by 1
        for i in range(r):
            if i == src or p[i] >= cap[i]:
                continue
            q = list(p)
            q[i] += 1
            qt = tuple(q)
            if qt in visited:
                continue
            # Feasibility: for every edge (a,b): q[b] <= q[a] + 1
            ok = True
            for a, b in E:
                if q[b] > q[a] + 1:
                    ok = False
                    break
            if not ok:
                continue
            # Tightness: each b != src has an incoming edge with q[a] <= q[b]
            # (given feasibility, q[a] >= q[b]-1 always, so q[a] in {q[b]-1, q[b]})
            for b in range(r):
                if b == src:
                    continue
                found = False
                for a in in_edges[b]:
                    if q[a] <= q[b]:
                        found = True
                        break
                if not found:
                    ok = False
                    break
            if not ok:
                continue
            # Cost = number of edges forced to weight 1 = #{edges with q[b]-q[a] == 1}
            cost = 0
            for a, b in E:
                if q[b] - q[a] == 1:
                    cost += 1
                    if cost > K:
                        break
            if cost > K:
                continue
            visited.add(qt)
            stack.append(qt)

    print(ans)

main()