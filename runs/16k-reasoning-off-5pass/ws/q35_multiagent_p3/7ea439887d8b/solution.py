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

    # Build adjacency lists for original and reversed graphs
    # adj_orig[u] contains list of v such that u -> v in original graph
    # adj_rev[u] contains list of v such that v -> u in original graph (i.e., u <- v)
    adj_orig = [[] for _ in range(N + 1)]
    adj_rev = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj_orig[u].append(v)
        adj_rev[v].append(u)

    # Dijkstra's algorithm on state graph (vertex, orientation)
    # orientation 0: original direction
    # orientation 1: reversed direction
    # dist[v][0] = min cost to reach vertex v with original orientation
    # dist[v][1] = min cost to reach vertex v with reversed orientation
    
    INF = float('inf')
    dist = [[INF] * 2 for _ in range(N + 1)]
    
    # Priority queue: (cost, vertex, orientation)
    pq = []
    
    # Start at vertex 1 with original orientation, cost 0
    dist[1][0] = 0
    heapq.heappush(pq, (0, 1, 0))
    
    while pq:
        d, u, ori = heapq.heappop(pq)
        
        # If we found a shorter path already, skip
        if d > dist[u][ori]:
            continue
        
        # Transition 1: Move along an edge in current orientation
        if ori == 0:
            # In original orientation, move along original edges
            for v in adj_orig[u]:
                new_cost = d + 1
                if new_cost < dist[v][0]:
                    dist[v][0] = new_cost
                    heapq.heappush(pq, (new_cost, v, 0))
        else:
            # In reversed orientation, move along reversed edges
            # This means we can go from u to v if there was an edge v -> u originally
            # Which is equivalent to traversing adj_rev[u]
            for v in adj_rev[u]:
                new_cost = d + 1
                if new_cost < dist[v][1]:
                    dist[v][1] = new_cost
                    heapq.heappush(pq, (new_cost, v, 1))
        
        # Transition 2: Reverse all edges (cost X)
        new_cost = d + X
        new_ori = 1 - ori
        if new_cost < dist[u][new_ori]:
            dist[u][new_ori] = new_cost
            heapq.heappush(pq, (new_cost, u, new_ori))
    
    # The answer is the minimum cost to reach vertex N in either orientation
    ans = min(dist[N][0], dist[N][1])
    print(ans)

if __name__ == '__main__':
    solve()