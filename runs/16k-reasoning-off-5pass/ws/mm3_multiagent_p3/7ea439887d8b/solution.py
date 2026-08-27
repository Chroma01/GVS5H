import sys
import heapq

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = int(next(it))
    
    # Build adjacency for doubled graph.
    # State index: v in [0, N-1] for mode 0, v+N for mode 1.
    adj = [[] for _ in range(2 * N)]
    
    edges = []
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        edges.append((u, v))
        # original mode (0): u -> v
        adj[u].append((v, 1))
        # reversed mode (1): v -> u (since direction flips)
        adj[v + N].append((u + N, 1))
    
    # Add reversal edges between modes
    for v in range(N):
        adj[v].append((v + N, X))
        adj[v + N].append((v, X))
    
    # Dijkstra
    INF = 10**30
    dist = [INF] * (2 * N)
    start = 0  # vertex 0, mode 0
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    
    ans = min(dist[N - 1], dist[N - 1 + N])
    print(ans)

if __name__ == "__main__":
    solve()