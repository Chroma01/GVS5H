import sys
import heapq

# Set recursion depth just in case, though not used here
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
    # adj[u] contains list of v such that there is an edge u -> v
    adj = [[] for _ in range(N + 1)]
    
    # rev_adj[u] contains list of v such that there is an edge v -> u in the original graph
    # This is needed because in the reversed state, an edge v->u becomes u->v.
    # So if we are at u in the reversed state, we can move to v if there was an edge v->u originally.
    rev_adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        rev_adj[v].append(u)

    # Dijkstra's Algorithm
    # State: (cost, u, orientation)
    # orientation: 0 for original, 1 for reversed
    # dist[u][0] = min cost to reach u in original orientation
    # dist[u][1] = min cost to reach u in reversed orientation
    
    # Use a large number for infinity. Since max cost can be large, float('inf') is safe.
    INF = float('inf')
    dist = [[INF] * 2 for _ in range(N + 1)]
    
    start_node = 1
    dist[start_node][0] = 0
    
    # Priority queue: (cost, u, orientation)
    pq = [(0, start_node, 0)]
    
    while pq:
        d, u, orientation = heapq.heappop(pq)
        
        if d > dist[u][orientation]:
            continue
        
        # Transition 1: Move along an edge
        if orientation == 0:
            # Original orientation: edges are u -> v
            for v in adj[u]:
                if dist[v][0] > d + 1:
                    dist[v][0] = d + 1
                    heapq.heappush(pq, (dist[v][0], v, 0))
        else:
            # Reversed orientation: 
            # The graph edges are reversed. An original edge v -> u becomes u -> v.
            # So if we are at u, we can move to v if there was an original edge v -> u.
            # rev_adj[u] stores exactly those v.
            for v in rev_adj[u]:
                if dist[v][1] > d + 1:
                    dist[v][1] = d + 1
                    heapq.heappush(pq, (dist[v][1], v, 1))
        
        # Transition 2: Reverse all edges
        # Cost X, switch orientation, stay at same vertex
        new_orientation = 1 - orientation
        if dist[u][new_orientation] > d + X:
            dist[u][new_orientation] = d + X
            heapq.heappush(pq, (dist[u][new_orientation], u, new_orientation))

    ans = min(dist[N][0], dist[N][1])
    print(ans)

if __name__ == '__main__':
    solve()