import sys
import heapq

# Increase recursion depth just in case, though we use iterative Dijkstra
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin efficiently
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
    # graph[u] contains list of v such that u -> v exists
    graph = [[] for _ in range(N + 1)]
    
    # Adjacency list for the reversed graph logic
    # rev_graph[u] contains list of v such that v -> u exists in original graph
    # This corresponds to edges in the reversed state: u -> v in reversed state
    # means v -> u in original state.
    rev_graph = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        graph[u].append(v)
        rev_graph[v].append(u)

    # Dijkstra's Algorithm
    # State representation:
    # Node i (1 <= i <= N) represents being at vertex i with edges in original orientation.
    # Node i + N (1 <= i <= N) represents being at vertex i with edges in reversed orientation.
    # Total nodes: 2 * N
    
    # Distance array initialized to infinity
    INF = float('inf')
    dist = [INF] * (2 * N + 1)
    
    # Priority queue: (cost, current_node_index)
    # current_node_index is 1-based vertex number mapped to state space
    pq = []
    
    # Start at vertex 1, orientation 0 (original) -> index 1
    dist[1] = 0
    heapq.heappush(pq, (0, 1))
    
    while pq:
        d, u = heapq.heappop(pq)
        
        # Check if we found a shorter path to this state already
        if d > dist[u]:
            continue
        
        # Option 1: Reverse all edges (Cost X)
        # Transition from state u to state u + N (or vice versa)
        # If u <= N, we go to u + N. If u > N, we go to u - N.
        if u <= N:
            target = u + N
        else:
            target = u - N
            
        new_cost = d + X
        
        if new_cost < dist[target]:
            dist[target] = new_cost
            heapq.heappush(pq, (new_cost, target))
        
        # Option 2: Move along an edge (Cost 1)
        if u <= N:
            # In original orientation (u), we can move u -> v if edge exists in graph
            for v in graph[u]:
                if d + 1 < dist[v]:
                    dist[v] = d + 1
                    heapq.heappush(pq, (d + 1, v))
        else:
            # In reversed orientation (u > N), let real_vertex = u - N
            # We can move real_vertex -> v if edge exists in rev_graph
            # (because v -> real_vertex in original becomes real_vertex -> v in reversed)
            real_vertex = u - N
            for v in rev_graph[real_vertex]:
                if d + 1 < dist[v]:
                    dist[v] = d + 1
                    heapq.heappush(pq, (d + 1, v))
    
    # The answer is the minimum cost to reach vertex N in either orientation
    # dist[N] is cost to reach N in original orientation
    # dist[N + N] is cost to reach N in reversed orientation
    ans = min(dist[N], dist[N + N])
    print(ans)

if __name__ == '__main__':
    solve()