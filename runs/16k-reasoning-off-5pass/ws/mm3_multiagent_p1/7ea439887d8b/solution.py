import sys
import heapq

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = int(next(it))
    
    # Build adjacency list for 2N state graph
    # state (v, 0) is index v (0..N-1)
    # state (v, 1) is index v + N
    size = 2 * N
    adj = [[] for _ in range(size)]
    
    for _ in range(M):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        # original orientation: a -> b in state 0
        adj[a].append((b, 1))
        # reversed orientation: b -> a in state 1
        adj[b + N].append((a + N, 1))
    
    # flip edges
    for v in range(N):
        adj[v].append((v + N, X))
        adj[v + N].append((v, X))
    
    # Dijkstra
    INF = 10**30
    dist = [INF] * size
    src = 0  # (1,0) -> 0
    dist[src] = 0
    pq = [(0, src)]
    
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for w, cost in adj[u]:
            nd = d + cost
            if nd < dist[w]:
                dist[w] = nd
                heapq.heappush(pq, (nd, w))
    
    ans = min(dist[N - 1], dist[N - 1 + N])
    print(ans)

if __name__ == "__main__":
    solve()