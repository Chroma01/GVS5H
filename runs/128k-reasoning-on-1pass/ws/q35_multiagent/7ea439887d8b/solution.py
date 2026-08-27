import sys
import heapq

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    iterator = iter(input_data)
    
    N = int(next(iterator))
    M = int(next(iterator))
    X = int(next(iterator))
    
    adj = [[] for _ in range(N)]
    rev_adj = [[] for _ in range(N)]
    
    for _ in range(M):
        u = int(next(iterator)) - 1
        v = int(next(iterator)) - 1
        adj[u].append(v)
        rev_adj[v].append(u)
        
    INF = 10**18
    # dist array stores minimum cost to reach state (u, dir)
    # Index mapping: state (u, 0) -> 2*u, state (u, 1) -> 2*u + 1
    dist = [INF] * (2 * N)
    dist[0] = 0  # Start at vertex 0 (1-indexed: 1) with original orientation
    
    # Priority queue stores tuples: (cost, u, dir)
    pq = [(0, 0, 0)] 
    
    while pq:
        d, u, dir = heapq.heappop(pq)
        idx = 2 * u + dir
        
        # Skip if we found a shorter path to this state already
        if d > dist[idx]:
            continue
            
        # If we reached the target vertex, this is the minimum cost
        if u == N - 1:
            print(d)
            return
            
        # Transition 1: Move along edges
        if dir == 0:
            # Original orientation: follow edges u -> v
            for v in adj[u]:
                n_idx = 2 * v
                if dist[n_idx] > d + 1:
                    dist[n_idx] = d + 1
                    heapq.heappush(pq, (dist[n_idx], v, 0))
        else:
            # Reversed orientation: follow edges u -> v in reversed graph
            # which corresponds to v -> u in original graph
            for v in rev_adj[u]:
                n_idx = 2 * v + 1
                if dist[n_idx] > d + 1:
                    dist[n_idx] = d + 1
                    heapq.heappush(pq, (dist[n_idx], v, 1))
                    
        # Transition 2: Reverse all edges
        new_dir = 1 - dir
        n_idx = 2 * u + new_dir
        if dist[n_idx] > d + X:
            dist[n_idx] = d + X
            heapq.heappush(pq, (dist[n_idx], u, new_dir))
            
    # Should not be reached given problem constraints guarantee reachability
    print(-1)

if __name__ == '__main__':
    solve()