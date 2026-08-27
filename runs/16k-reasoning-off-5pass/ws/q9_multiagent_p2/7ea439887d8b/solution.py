import sys
import heapq

# Set recursion depth just in case, though we use iterative approach
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

    # Adjacency list for the original graph: graph[u] contains v if u -> v
    graph = [[] for _ in range(N + 1)]
    
    # Adjacency list for the reverse graph: rev_graph[u] contains v if v -> u (i.e., u <- v)
    # This is needed because when edges are reversed, an edge u->v becomes v->u.
    # So if we are at u in the reversed state, we can move to v if there was an edge v->u originally.
    rev_graph = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        graph[u].append(v)
        rev_graph[v].append(u)

    # Dijkstra's Algorithm
    # We have 2*N states: 
    # State i (1 <= i <= N): At vertex i, original orientation.
    # State i+N (1 <= i <= N): At vertex i, reversed orientation.
    # Total nodes: 2*N + 1 (ignoring index 0)
    
    INF = float('inf')
    dist = [INF] * (2 * N + 1)
    
    # Priority queue: (cost, u, orientation)
    # orientation 0 = original, 1 = reversed
    # We map state to index: u + orientation * N
    pq = []
    
    # Start at vertex 1 with original orientation
    start_node = 1
    dist[start_node] = 0
    heapq.heappush(pq, (0, start_node, 0))
    
    while pq:
        d, u, orientation = heapq.heappop(pq)
        
        current_state_idx = u + orientation * N
        
        if d > dist[current_state_idx]:
            continue
        
        # Operation 1: Flip all edges (Cost X)
        # Transition from (u, orientation) to (u, 1-orientation)
        new_cost = d + X
        new_state_idx = u + (1 - orientation) * N
        
        if new_cost < dist[new_state_idx]:
            dist[new_state_idx] = new_cost
            heapq.heappush(pq, (new_cost, u, 1 - orientation))
        
        # Operation 2: Move along an edge
        if orientation == 0:
            # Original orientation: traverse u -> v
            # We need edge u -> v in original graph
            for v in graph[u]:
                new_cost = d + 1
                new_state_idx = v # Still original orientation
                if new_cost < dist[new_state_idx]:
                    dist[new_state_idx] = new_cost
                    heapq.heappush(pq, (new_cost, v, 0))
        else:
            # Reversed orientation: traverse u -> v means in original graph v -> u exists
            # So we look for incoming edges to u in the original graph
            # These are stored in rev_graph[u]
            for v in rev_graph[u]:
                new_cost = d + 1
                new_state_idx = v + N # Still reversed orientation
                if new_cost < dist[new_state_idx]:
                    dist[new_state_idx] = new_cost
                    heapq.heappush(pq, (new_cost, v, 1))

    # The target is to reach vertex N.
    # We can be at vertex N in original orientation (state N) or reversed orientation (state N+N).
    # Both represent being physically at vertex N.
    ans = min(dist[N], dist[N + N])
    
    print(ans)

if __name__ == '__main__':
    solve()