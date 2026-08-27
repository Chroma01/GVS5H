import sys
import heapq

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        X = int(next(iterator))
    except StopIteration:
        return

    # Adjacency lists for original graph and reversed graph
    # adj_orig[u] contains list of v such that u -> v
    # adj_rev[u] contains list of v such that v -> u (i.e., in reversed graph, u <- v becomes u -> v)
    adj_orig = [[] for _ in range(N + 1)]
    adj_rev = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj_orig[u].append(v)
        adj_rev[v].append(u)
    
    # Dijkstra's algorithm on state graph (vertex, orientation)
    # orientation 0: original edges
    # orientation 1: reversed edges
    # dist[(u, 0)] = minimum cost to reach vertex u with original orientation
    # dist[(u, 1)] = minimum cost to reach vertex u with reversed orientation
    
    INF = float('inf')
    # We'll use a flat array for distances: dist[2*u + orientation]
    # State index: 2*u + o where u is 1-indexed vertex, o is 0 or 1
    # So state for (u, o) is at index 2*u + o
    # Total states: 2*(N+1) to be safe, but we only care about 1..N
    
    dist = [INF] * (2 * (N + 1))
    
    # Start at vertex 1, orientation 0, cost 0
    start_state = 2 * 1 + 0
    dist[start_state] = 0
    
    # Priority queue: (cost, vertex, orientation)
    pq = [(0, 1, 0)]
    
    while pq:
        d, u, o = heapq.heappop(pq)
        
        # If we found a shorter path already, skip
        if d > dist[2 * u + o]:
            continue
        
        if o == 0:
            # Original orientation
            # Option 1: Move along an edge u -> v in original graph, cost 1
            for v in adj_orig[u]:
                new_cost = d + 1
                if new_cost < dist[2 * v + 0]:
                    dist[2 * v + 0] = new_cost
                    heapq.heappush(pq, (new_cost, v, 0))
            
            # Option 2: Reverse all edges, cost X, go to state (u, 1)
            new_cost = d + X
            if new_cost < dist[2 * u + 1]:
                dist[2 * u + 1] = new_cost
                heapq.heappush(pq, (new_cost, u, 1))
        else:
            # Reversed orientation
            # Option 1: Move along an edge in reversed graph, which means original edge v -> u becomes u -> v
            # So we look at adj_rev[u] which gives us v such that v -> u in original, meaning u -> v in reversed
            for v in adj_rev[u]:
                new_cost = d + 1
                if new_cost < dist[2 * v + 1]:
                    dist[2 * v + 1] = new_cost
                    heapq.heappush(pq, (new_cost, v, 1))
            
            # Option 2: Reverse all edges, cost X, go to state (u, 0)
            new_cost = d + X
            if new_cost < dist[2 * u + 0]:
                dist[2 * u + 0] = new_cost
                heapq.heappush(pq, (new_cost, u, 0))
    
    # Answer is min cost to reach vertex N in either orientation
    ans = min(dist[2 * N + 0], dist[2 * N + 1])
    print(ans)

solve()