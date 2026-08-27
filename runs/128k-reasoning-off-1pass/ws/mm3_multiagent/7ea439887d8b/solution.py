import sys
import heapq

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = int(next(it))
    
    # Build adjacency list for 2*N nodes
    # Node index: v in [0, N-1] -> layer0 = v, layer1 = v + N
    size = 2 * N
    adj = [[] for _ in range(size)]
    
    # Store edges to build reversed adjacency
    edges = []
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        edges.append((u, v))
        # Original orientation: from u0 to v0, cost 1
        adj[u].append((v, 1))
        # Reversed orientation: from v1 to u1, cost 1
        adj[v + N].append((u + N, 1))
    
    # Add flip transitions: from v0 to v1 and v1 to v0, cost X
    for v in range(N):
        adj[v].append((v + N, X))
        adj[v + N].append((v, X))
    
    INF = 10**30
    dist = [INF] * size
    start = 0  # vertex 1 -> index 0, layer 0
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        # Early exit? We need min over both layers for vertex N.
        if u == N - 1 or u == N - 1 + N:
            # But we need min over both, so can't early exit safely.
            pass
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    
    target0 = N - 1          # layer 0
    target1 = N - 1 + N      # layer 1
    ans = min(dist[target0], dist[target1])
    print(ans)

if __name__ == "__main__":
    solve()