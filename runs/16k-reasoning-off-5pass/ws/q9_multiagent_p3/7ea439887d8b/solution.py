import sys
import heapq

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read
    data = input_data().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        X = int(next(iterator))
    except StopIteration:
        return

    # Adjacency list for the original graph
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)

    # We will model the state as (vertex, orientation)
    # orientation 0: original graph
    # orientation 1: reversed graph
    # Nodes are 0..2N-1 where node u in layer 0 is u, and node u in layer 1 is u + N
    
    # Build the graph for Dijkstra
    # expanded_adj[u] contains neighbors of u in layer 0
    # expanded_adj[u + N] contains neighbors of u in layer 1
    # Each entry is a tuple (neighbor, weight)
    
    expanded_adj = [[] for _ in range(2 * N + 1)]
    
    # Layer 0: Original edges (weight 1)
    for u in range(1, N + 1):
        for v in adj[u]:
            expanded_adj[u].append((v, 1))
            
    # Layer 1: Reversed edges (weight 1)
    # If original edge is u -> v, then in reversed graph, the edge becomes v -> u.
    # So for each u in layer 1, we look at incoming edges in original graph.
    # To implement this, if original has u -> v, then in layer 1, node v connects to node u.
    for u in range(1, N + 1):
        for v in adj[u]:
            # Original: u -> v
            # Reversed: v -> u. So in layer 1, node v connects to node u.
            expanded_adj[v + N].append((u + N, 1))
            
    # Transition edges: Cost X to switch layers
    # (u, 0) -> (u, 1) with cost X
    # (u, 1) -> (u, 0) with cost X
    for u in range(1, N + 1):
        expanded_adj[u].append((u + N, X))
        expanded_adj[u + N].append((u, X))
        
    # Dijkstra's Algorithm
    # dist[i] stores min cost to reach node i (where i is 1..N for layer 0, N+1..2N for layer 1)
    # Initialize with infinity
    INF = float('inf')
    dist = [INF] * (2 * N + 1)
    
    start_node = 1 # Vertex 1 in layer 0
    dist[start_node] = 0
    
    pq = [(0, start_node)] # (cost, node)
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        for v, weight in expanded_adj[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))
                
    ans = min(dist[N], dist[N + N])
    print(ans)

if __name__ == '__main__':
    solve()