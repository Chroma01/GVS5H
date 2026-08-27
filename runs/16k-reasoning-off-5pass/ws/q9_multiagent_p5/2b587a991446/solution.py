import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        S = int(next(iterator))
        T = int(next(iterator))
    except StopIteration:
        return

    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # BFS to find shortest distances and count number of shortest paths
    def bfs_count(start_node):
        dist = [-1] * (N + 1)
        cnt = [0] * (N + 1)
        dist[start_node] = 0
        cnt[start_node] = 1
        queue = deque([start_node])
        
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    cnt[v] = cnt[u]
                    queue.append(v)
                elif dist[v] == dist[u] + 1:
                    cnt[v] = (cnt[v] + cnt[u]) % 1000000007
        return dist, cnt

    dist_S, cnt_S = bfs_count(S)
    dist_T, cnt_T = bfs_count(T)
    
    dist_ST = dist_S[T]
    
    # Check for impossibility
    # If the graph is a simple path between S and T, swapping is impossible.
    # This happens if and only if:
    # 1. The shortest path is unique (cnt_S[T] == 1)
    # 2. All vertices lie on this shortest path.
    
    unique_path = (cnt_S[T] == 1)
    
    all_on_path = True
    if unique_path:
        for v in range(1, N + 1):
            if dist_S[v] != -1 and dist_T[v] != -1:
                if dist_S[v] + dist_T[v] != dist_ST:
                    all_on_path = False
                    break
    
    if unique_path and all_on_path:
        print("-1")
        return

    # Calculate minimum operations
    if not unique_path:
        # Multiple shortest paths exist, pieces can cross without detour
        print(2 * dist_ST)
    else:
        # Unique shortest path, must use a detour (pivot)
        # Cost = dist(S, T) + 2 * min_{v} (dist(S, v) + dist(T, v) - dist(S, T))
        min_diff = float('inf')
        for v in range(1, N + 1):
            if dist_S[v] != -1 and dist_T[v] != -1:
                diff = dist_S[v] + dist_T[v] - dist_ST
                if diff < min_diff:
                    min_diff = diff
        print(dist_ST + 2 * min_diff)

if __name__ == '__main__':
    solve()