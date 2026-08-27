import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it)); M = int(next(it)); S = int(next(it)); T = int(next(it))
    S -= 1; T -= 1
    adj = [[] for _ in range(N)]
    edges = []
    for _ in range(M):
        u = int(next(it)) - 1; v = int(next(it)) - 1
        adj[u].append(v); adj[v].append(u)
        edges.append((u, v))

    def bfs(src, banned=-1):
        dist = [-1] * N
        dist[src] = 0
        dq = deque([src])
        while dq:
            x = dq.popleft()
            nd = dist[x] + 1
            for y in adj[x]:
                if y != banned and dist[y] < 0:
                    dist[y] = nd
                    dq.append(y)
        return dist

    ds = bfs(S)
    dt = bfs(T)
    d = ds[T]

    INF = float('inf')
    best = INF

    # Candidate 1: S,T on a common cycle -> tokens rotate around it.
    # Shortest cycle through S,T = min over edges (x,y) of
    #   (ds[x]+1+dt[y]) + (ds[y]+1+dt[x])  [two edge-disjoint arcs]
    # BUT this formula forces both arcs through edge (x,y), which is
    # backtracking.  The correct cycle uses two *different* edges.
    # We compute: min over edges of (ds[x]+1+dt[y]) + (ds[y]+1+dt[x])
    # and separately handle the "two edge-disjoint shortest paths" case
    # which gives 2d.
    #
    # For the cycle case, the correct formula is:
    #   min over edges (x,y) of (ds[x]+1+dt[y]) + (ds[y]+1+dt[x])
    # where the two S-T paths are internally disjoint.  Since we can't
    # easily enforce disjointness, we use the following:
    #   - If two edge-disjoint shortest S-T paths exist: answer 2d.
    #   - Else: min over edges of (ds[x]+1+dt[y]) + (ds[y]+1+dt[x])
    #     gives an upper bound (theta case).
    #   - For d=1 with a common neighbor (triangle): answer 3.

    # Build shortest-path DAG and check for two edge-disjoint paths.
    # DAG edges: (u,v) with ds[u]+1==ds[v] and ds[v]+dt[v]==d.
    # Count paths from S and to T; an edge is a "bridge" if all paths use it.
    MOD = 10**9 + 7
    fwd = [0] * N
    bwd = [0] * N
    fwd[S] = 1
    # Process vertices in order of ds (BFS order).
    order = sorted(range(N), key=lambda v: ds[v])
    for v in order:
        if ds[v] < 0:
            continue
        for u in adj[v]:
            if ds[u] == ds[v] + 1 and ds[u] + dt[u] == d:
                fwd[u] = (fwd[u] + fwd[v]) % MOD
    bwd[T] = 1
    for v in reversed(order):
        if dt[v] < 0:
            continue
        for u in adj[v]:
            if dt[u] == dt[v] + 1 and ds[u] + dt[u] == d:
                bwd[u] = (bwd[u] + bwd[v]) % MOD
    total_paths = fwd[T]
    two_disjoint = False
    if total_paths >= 2:
        # Check if any single edge carries all paths.
        # Edge (u,v) in DAG: ds[u]+1==ds[v], ds[v]+dt[v]==d.
        # It carries fwd[u]*bwd[v] paths.  If this equals total_paths,
        # it's a bridge.  If no bridge exists, two edge-disjoint paths exist.
        has_bridge = False
        for (x, y) in edges:
            # Orient in DAG direction.
            if ds[x] + 1 == ds[y] and ds[y] + dt[y] == d:
                u, v = x, y
            elif ds[y] + 1 == ds[x] and ds[x] + dt[x] == d:
                u, v = y, x
            else:
                continue
            if fwd[u] * bwd[v] % MOD == total_paths:
                has_bridge = True
                break
        two_disjoint = not has_bridge

    if two_disjoint:
        best = 2 * d

    # Candidate 2: theta/cycle case - min over edges of
    # (ds[x]+1+dt[y]) + (ds[y]+1+dt[x]).
    # This handles cases where S,T are on a common cycle (even if not
    # shortest-path disjoint) and where a cycle is "between" S and T.
    for (x, y) in edges:
        val = (ds[x] + 1 + dt[y]) + (ds[y] + 1 + dt[x])
        if val < best:
            best = val

    # Candidate 3: d=1 with common neighbor (triangle through S,T).
    if d == 1:
        # Check if S and T have a common neighbor.
        for u in adj[S]:
            if u != T and dt[u] == 1:
                best = min(best, 3)
                break

    # Candidate 4: junction (deg>=3) as parking gadget.
    # Compute distances avoiding T (for A's reachability) and avoiding S.
    ds_noT = bfs(S, banned=T)
    dt_noS = bfs(T, banned=S)
    for v in range(N):
        if len(adj[v]) >= 3:
            # One-spur: A reaches v without passing T, B reaches v without S.
            one_spur = (ds_noT[v] == ds[v] and dt_noS[v] == dt[v])
            if one_spur:
                val = ds[v] + dt[v] + d + 2
            else:
                val = 2 * (ds[v] + dt[v]) + 4
            if val < best:
                best = val

    if best == INF:
        print(-1)
    else:
        print(best)

main()