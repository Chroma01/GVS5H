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

    # Adjacency list for original graph: adj[u] contains list of v such that u->v exists
    adj = [[] for _ in range(N + 1)]
    # Adjacency list for reversed graph: rev_adj[u] contains list of v such that v->u exists in original (i.e., u->v in reversed)
    rev_adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        rev_adj[v].append(u)
        
    # Dijkstra's algorithm
    # State: (cost, vertex, orientation)
    # orientation 0: original graph
    # orientation 1: reversed graph
    # dist[v][0] = min cost to reach vertex v in original orientation
    # dist[v][1] = min cost to reach vertex v in reversed orientation
    
    INF = float('inf')
    dist = [[INF, INF] for _ in range(N + 1)]
    dist[1][0] = 0
    
    # Priority queue: (cost, vertex, orientation)
    pq = [(0, 1, 0)]
    
    while pq:
        d, u, ori = heapq.heappop(pq)
        
        # If we found a shorter path already, skip
        if d > dist[u][ori]:
            continue
            
        # If we reached vertex N, we can't stop early because there might be a cheaper way to reach N in the other orientation
        # But we continue until the queue is empty or we process all reachable states
        
        # Transition 1: Move along an edge in current orientation
        if ori == 0:
            # In original orientation, move along edges u -> v
            for v in adj[u]:
                new_cost = d + 1
                if new_cost < dist[v][0]:
                    dist[v][0] = new_cost
                    heapq.heappush(pq, (new_cost, v, 0))
        else:
            # In reversed orientation, move along edges u -> v which correspond to v -> u in original
            # So we look at rev_adj[u] which gives us all v such that there's an edge v->u in original,
            # meaning in reversed graph there's an edge u->v
            for v in rev_adj[u]:
                new_cost = d + 1
                if new_cost < dist[v][1]:
                    dist[v][1] = new_cost
                    heapq.heappush(pq, (new_cost, v, 1))
                    
        # Transition 2: Reverse all edges (cost X)
        # From (u, 0) to (u, 1) with cost X
        new_cost_rev = d + X
        if new_cost_rev < dist[u][1]:
            dist[u][1] = new_cost_rev
            heapq.heappush(pq, (new_cost_rev, u, 1))
            
        # From (u, 1) to (u, 0) with cost X
        new_cost_rev = d + X
        if new_cost_rev < dist[u][0]:
            dist[u][0] = new_cost_rev
            heapq.heappush(pq, (new_cost_rev, u, 0))
            
    # The answer is the minimum cost to reach vertex N in either orientation
    ans = min(dist[N][0], dist[N][1])
    print(ans)

if __name__ == '__main__':
    solve()