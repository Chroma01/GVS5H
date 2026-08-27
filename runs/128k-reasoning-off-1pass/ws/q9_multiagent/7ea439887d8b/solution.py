import sys
import heapq

# Increase recursion depth just in case, though we use iterative Dijkstra
sys.setrecursionlimit(200005)

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

    # Adjacency list for the 2-layer graph
    # Layer 0: Original edges (nodes 1 to N)
    # Layer 1: Reversed edges (nodes N+1 to 2N)
    # Node u in layer 0 is represented as u.
    # Node u in layer 1 is represented as u + N.
    
    adj = [[] for _ in range(2 * N + 1)]
    
    # Read M edges
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        
        # Original edge: u -> v in layer 0
        adj[u].append((v, 1))
        
        # Reversed edge: v -> u in layer 1 (since u->v becomes v->u)
        adj[v + N].append((u + N, 1))
    
    # Add "Reverse" edges: switching between layers costs X
    # For each vertex u, we can switch from layer 0 to layer 1 (u -> u+N)
    # and from layer 1 to layer 0 (u+N -> u) with cost X.
    for u in range(1, N + 1):
        adj[u].append((u + N, X))
        adj[u + N].append((u, X))
    
    # Dijkstra's Algorithm
    # Start at node 1 in layer 0 (index 1)
    # Target is node N in layer 0 (index N) or node N in layer 1 (index N + N)
    
    start_node = 1
    target_nodes = [N, N + N]
    
    # Distance array initialized to infinity
    # Using a list. Size: 2*N + 1
    INF = float('inf')
    dist = [INF] * (2 * N + 1)
    dist[start_node] = 0
    
    # Priority queue: (cost, u)
    pq = [(0, start_node)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        # Optimization: If we have found the shortest path to both targets, we can stop.
        # However, standard Dijkstra just runs until the queue is empty or we pop the target.
        # Since we need min(dist[N], dist[N+N]), we can just let it run.
        # To optimize slightly, we can check if both targets are finalized.
        # But given the constraints and logic, running fully is safe and fast enough.
        
        for v, weight in adj[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                heapq.heappush(pq, (dist[v], v))
    
    # The answer is the minimum distance to reach N in either layer
    # Note: If N is unreachable in one layer, dist will be INF.
    # The problem guarantees reachability, so at least one will be finite.
    ans = min(dist[N], dist[N + N])
    print(ans)

if __name__ == '__main__':
    solve()