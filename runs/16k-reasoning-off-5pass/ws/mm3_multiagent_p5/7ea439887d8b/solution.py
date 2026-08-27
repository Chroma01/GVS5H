import sys
import heapq

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = int(next(it))
    
    # Build adjacency list for original orientation
    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
    
    # Dijkstra over 2N states: (v, parity) where parity 0 = original, 1 = reversed
    # State id: v-1 + parity*N, or use 2D distances
    INF = 10**30
    dist = [[INF, INF] for _ in range(N + 1)]
    dist[1][0] = 0
    # heap elements: (cost, vertex, parity)
    heap = [(0, 1, 0)]
    
    while heap:
        d, v, p = heapq.heappop(heap)
        if d != dist[v][p]:
            continue
        # Option 1: reverse all edges, cost X, flip parity
        nd = d + X
        if nd < dist[v][1 - p]:
            dist[v][1 - p] = nd
            heapq.heappush(heap, (nd, v, 1 - p))
        # Option 2: traverse an edge in current orientation
        if p == 0:
            # original orientation: follow original edges
            for to in adj[v]:
                nd = d + 1
                if nd < dist[to][p]:
                    dist[to][p] = nd
                    heapq.heappush(heap, (nd, to, p))
        else:
            # reversed orientation: follow edges opposite to original
            # which means we can go to any u such that there is an edge u -> v in original
            # i.e., incoming edges in original graph become outgoing in reversed graph
            for to in radj[v]:  # need radj built
                nd = d + 1
                if nd < dist[to][p]:
                    dist[to][p] = nd
                    heapq.heappush(heap, (nd, to, p))
    
    print(min(dist[N][0], dist[N][1]))

# Need reverse adjacency
def solve_full():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    X = int(next(it))
    
    adj = [[] for _ in range(N + 1)]
    radj = [[] for _ in range(N + 1)]  # reverse adjacency: edges incoming to v
    for _ in range(M):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        radj[v].append(u)
    
    INF = 10**30
    dist = [[INF, INF] for _ in range(N + 1)]
    dist[1][0] = 0
    heap = [(0, 1, 0)]
    
    while heap:
        d, v, p = heapq.heappop(heap)
        if d != dist[v][p]:
            continue
        # Reverse operation
        nd = d + X
        if nd < dist[v][1 - p]:
            dist[v][1 - p] = nd
            heapq.heappush(heap, (nd, v, 1 - p))
        # Traverse edge in current orientation
        neighbors = adj[v] if p == 0 else radj[v]
        for to in neighbors:
            nd = d + 1
            if nd < dist[to][p]:
                dist[to][p] = nd
                heapq.heappush(heap, (nd, to, p))
    
    print(min(dist[N][0], dist[N][1]))

solve_full()