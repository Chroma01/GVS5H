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

    # Adjacency list for original graph
    adj = [[] for _ in range(N + 1)]
    # Adjacency list for reversed graph (to handle moves in reversed state)
    rev_adj = [[] for _ in range(N + 1)]

    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        rev_adj[v].append(u)

    # Dijkstra's algorithm
    # States: (vertex, orientation)
    # orientation 0: original graph
    # orientation 1: reversed graph
    # We map state (u, 0) to index u-1 and (u, 1) to index u-1 + N
    # Total nodes in our state graph: 2*N
    
    # dist[i] will store the minimum cost to reach state i
    # i ranges from 0 to 2*N - 1
    # i < N corresponds to orientation 0, vertex i+1
    # i >= N corresponds to orientation 1, vertex i+1 - N
    
    INF = float('inf')
    dist = [INF] * (2 * N)
    
    # Start at vertex 1, orientation 0
    start_node = 0 # (1, 0) -> index 0
    dist[start_node] = 0
    
    # Priority queue: (cost, state_index)
    pq = [(0, start_node)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        # Determine vertex and orientation
        if u < N:
            vertex = u + 1
            orientation = 0
        else:
            vertex = u - N + 1
            orientation = 1
            
        # Transition 1: Move along an edge (cost 1)
        if orientation == 0:
            # In original graph, move from vertex to neighbors
            for v in adj[vertex]:
                # New state: (v, 0) -> index v-1
                v_idx = v - 1
                new_dist = d + 1
                if new_dist < dist[v_idx]:
                    dist[v_idx] = new_dist
                    heapq.heappush(pq, (new_dist, v_idx))
        else:
            # In reversed graph, move from vertex to neighbors
            # This means in original graph, there was an edge v -> vertex
            # So we can move to v in the reversed graph
            for v in rev_adj[vertex]:
                # New state: (v, 1) -> index v-1 + N
                v_idx = v - 1 + N
                new_dist = d + 1
                if new_dist < dist[v_idx]:
                    dist[v_idx] = new_dist
                    heapq.heappush(pq, (new_dist, v_idx))
                    
        # Transition 2: Reverse all edges (cost X)
        # From (vertex, 0) to (vertex, 1)
        if orientation == 0:
            # New state: (vertex, 1) -> index vertex-1 + N
            v_idx = vertex - 1 + N
            new_dist = d + X
            if new_dist < dist[v_idx]:
                dist[v_idx] = new_dist
                heapq.heappush(pq, (new_dist, v_idx))
        else:
            # From (vertex, 1) to (vertex, 0)
            # New state: (vertex, 0) -> index vertex-1
            v_idx = vertex - 1
            new_dist = d + X
            if new_dist < dist[v_idx]:
                dist[v_idx] = new_dist
                heapq.heappush(pq, (new_dist, v_idx))

    # The answer is the minimum cost to reach vertex N in either orientation
    # State (N, 0) -> index N-1
    # State (N, 1) -> index N-1 + N = 2*N - 1
    ans = min(dist[N - 1], dist[2 * N - 1])
    
    print(ans)

if __name__ == '__main__':
    solve()