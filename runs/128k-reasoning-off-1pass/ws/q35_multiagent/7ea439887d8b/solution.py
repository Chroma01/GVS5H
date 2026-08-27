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

    # Adjacency list for the original graph
    # adj[u] contains list of v such that u -> v
    adj = [[] for _ in range(N + 1)]
    # rev_adj[u] contains list of v such that v -> u (i.e., u <- v)
    rev_adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        rev_adj[v].append(u)

    # We have 2*N states: (vertex, orientation)
    # orientation 0: original graph
    # orientation 1: reversed graph
    # Node index for (u, 0) is u
    # Node index for (u, 1) is u + N
    
    # Total nodes in state graph: 2*N + 1 (using 1-based indexing for vertices)
    # We'll use 0-based indexing for the priority queue but map carefully.
    # Let's use 1..N for orientation 0, and N+1..2N for orientation 1.
    
    start_node = 1  # (1, 0)
    target_node_0 = N  # (N, 0)
    target_node_1 = N + N  # (N, 1)
    
    # Dijkstra's algorithm
    # dist[i] stores the minimum cost to reach node i in the state graph
    INF = float('inf')
    dist = [INF] * (2 * N + 1)
    dist[start_node] = 0
    
    # Priority queue: (cost, node)
    pq = [(0, start_node)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
            
        # Determine orientation
        if u <= N:
            orientation = 0
            vertex = u
        else:
            orientation = 1
            vertex = u - N
            
        # Transition 1: Move along an edge in current orientation
        if orientation == 0:
            # Can move from vertex to v if there's an edge vertex -> v in original graph
            for v in adj[vertex]:
                new_node = v  # (v, 0)
                new_cost = d + 1
                if new_cost < dist[new_node]:
                    dist[new_node] = new_cost
                    heapq.heappush(pq, (new_cost, new_node))
        else:
            # Can move from vertex to v if there's an edge v -> vertex in original graph
            # Because in reversed graph, the edge is vertex -> v
            for v in rev_adj[vertex]:
                new_node = v + N  # (v, 1)
                new_cost = d + 1
                if new_cost < dist[new_node]:
                    dist[new_node] = new_cost
                    heapq.heappush(pq, (new_cost, new_node))
                    
        # Transition 2: Reverse all edges (cost X)
        # From (vertex, 0) to (vertex, 1) and vice versa
        if orientation == 0:
            new_node = vertex + N  # (vertex, 1)
            new_cost = d + X
            if new_cost < dist[new_node]:
                dist[new_node] = new_cost
                heapq.heappush(pq, (new_cost, new_node))
        else:
            new_node = vertex  # (vertex, 0)
            new_cost = d + X
            if new_cost < dist[new_node]:
                dist[new_node] = new_cost
                heapq.heappush(pq, (new_cost, new_node))
                
    ans = min(dist[target_node_0], dist[target_node_1])
    print(ans)

if __name__ == '__main__':
    solve()