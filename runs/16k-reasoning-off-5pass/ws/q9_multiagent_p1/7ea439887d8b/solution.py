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
    adj = [[] for _ in range(N + 1)]
    # Adjacency list for the reversed graph (needed for state 1)
    # If there is an edge u -> v in original, then in reversed graph there is v -> u.
    # So if we are at v in reversed state, we can go to u.
    rev_adj = [[] for _ in range(N + 1)]

    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        rev_adj[v].append(u)

    # Dijkstra's Algorithm
    # State: (cost, u, orientation)
    # orientation 0: original edges
    # orientation 1: reversed edges
    # We want to find min cost to reach (N, 0) or (N, 1)
    
    # dist[u][orientation] stores the minimum cost to reach vertex u with given orientation
    # Initialize with infinity
    INF = float('inf')
    dist = [[INF, INF] for _ in range(N + 1)]
    
    # Priority queue: (cost, u, orientation)
    # Start at vertex 1 with original orientation (0) and cost 0
    pq = [(0, 1, 0)]
    dist[1][0] = 0
    
    while pq:
        d, u, orientation = heapq.heappop(pq)
        
        # If we found a shorter path to this state already, skip
        if d > dist[u][orientation]:
            continue
        
        # If we reached the target vertex N, we can't stop immediately because 
        # reaching N in orientation 1 might be cheaper than 0, or vice versa.
        # However, since edge weights are non-negative, once we pop (N, 0) or (N, 1),
        # that is the shortest path to that specific state. We need min of both.
        # We continue until the queue is empty or we have processed the optimal path.
        # Given the constraints and graph size, running fully is safe and fast enough.
        
        # Try to reverse edges (switch orientation)
        # Cost X
        new_orientation = 1 - orientation
        new_cost = d + X
        if new_cost < dist[u][new_orientation]:
            dist[u][new_orientation] = new_cost
            heapq.heappush(pq, (new_cost, u, new_orientation))
        
        # Try to move along edges
        if orientation == 0:
            # Move in original graph
            for v in adj[u]:
                new_cost = d + 1
                if new_cost < dist[v][0]:
                    dist[v][0] = new_cost
                    heapq.heappush(pq, (new_cost, v, 0))
        else:
            # Move in reversed graph
            for v in rev_adj[u]:
                new_cost = d + 1
                if new_cost < dist[v][1]:
                    dist[v][1] = new_cost
                    heapq.heappush(pq, (new_cost, v, 1))
    
    # The answer is the minimum cost to reach vertex N in either orientation
    ans = min(dist[N][0], dist[N][1])
    print(ans)

if __name__ == '__main__':
    solve()