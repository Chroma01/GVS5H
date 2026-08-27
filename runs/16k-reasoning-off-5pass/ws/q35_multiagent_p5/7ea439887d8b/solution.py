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
    # adj_forward[u] contains list of v such that u -> v exists
    # adj_backward[u] contains list of v such that v -> u exists (i.e., u <- v)
    adj_forward = [[] for _ in range(N + 1)]
    adj_backward = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj_forward[u].append(v)
        adj_backward[v].append(u)

    # Dijkstra's algorithm
    # State: (cost, vertex, orientation)
    # orientation 0: original edges
    # orientation 1: reversed edges
    
    # dist[u][0] = min cost to reach vertex u with original orientation
    # dist[u][1] = min cost to reach vertex u with reversed orientation
    INF = float('inf')
    dist = [[INF, INF] for _ in range(N + 1)]
    
    # Priority queue: (cost, vertex, orientation)
    pq = []
    
    # Start at vertex 1 with orientation 0, cost 0
    dist[1][0] = 0
    heapq.heappush(pq, (0, 1, 0))
    
    while pq:
        d, u, k = heapq.heappop(pq)
        
        # If we found a shorter path already, skip
        if d > dist[u][k]:
            continue
        
        # Transition 1: Move along an edge
        if k == 0:
            # Original orientation: traverse edges forward
            for v in adj_forward[u]:
                new_cost = d + 1
                if new_cost < dist[v][0]:
                    dist[v][0] = new_cost
                    heapq.heappush(pq, (new_cost, v, 0))
        else:
            # Reversed orientation: traverse edges backward (original edge v->u becomes u->v)
            # So we can go from u to v if there's an original edge v->u
            for v in adj_backward[u]:
                new_cost = d + 1
                if new_cost < dist[v][1]:
                    dist[v][1] = new_cost
                    heapq.heappush(pq, (new_cost, v, 1))
        
        # Transition 2: Reverse all edges
        # From orientation 0 to 1 with cost X
        new_cost_rev = d + X
        if new_cost_rev < dist[u][1]:
            dist[u][1] = new_cost_rev
            heapq.heappush(pq, (new_cost_rev, u, 1))
        
        # From orientation 1 to 0 with cost X
        new_cost_rev = d + X
        if new_cost_rev < dist[u][0]:
            dist[u][0] = new_cost_rev
            heapq.heappush(pq, (new_cost_rev, u, 0))
    
    # The answer is the minimum cost to reach vertex N in either orientation
    ans = min(dist[N][0], dist[N][1])
    print(ans)

solve()