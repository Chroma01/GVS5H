import sys, heapq

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    M = next(it)
    X = next(it)
    total_nodes = 2 * N
    adj = [[] for _ in range(total_nodes)]
    # reversal edges (toggle orientation)
    for i in range(N):
        u = i * 2
        v = i * 2 + 1
        adj[u].append((v, X))
        adj[v].append((u, X))
    # add movement edges
    for _ in range(M):
        u = next(it) - 1
        v = next(it) - 1
        # original orientation: layer 0
        adj[u * 2].append((v * 2, 1))
        # reversed orientation: layer 1
        adj[v * 2 + 1].append((u * 2 + 1, 1))
    # Dijkstra
    INF = 10 ** 30
    dist = [INF] * total_nodes
    start = 0  # vertex 1 (index 0) in original orientation (layer 0)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, node = heapq.heappop(pq)
        if d != dist[node]:
            continue
        for nb, w in adj[node]:
            nd = d + w
            if nd < dist[nb]:
                dist[nb] = nd
                heapq.heappush(pq, (nd, nb))
    target0 = (N - 1) * 2
    target1 = target0 + 1
    ans = min(dist[target0], dist[target1])
    print(ans)

if __name__ == "__main__":
    solve()