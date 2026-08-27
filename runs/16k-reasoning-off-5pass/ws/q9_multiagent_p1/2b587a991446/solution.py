import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300000)

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

    # BFS from S to find shortest distances and count paths
    distS = [-1] * (N + 1)
    parent = [0] * (N + 1)
    path_count = [0] * (N + 1)
    
    distS[S] = 0
    path_count[S] = 1
    
    queue = deque([S])
    
    while queue:
        u = queue.popleft()
        
        d_u = distS[u]
        cnt_u = path_count[u]
        
        for v in adj[u]:
            if distS[v] == -1:
                distS[v] = d_u + 1
                parent[v] = u
                path_count[v] = cnt_u
                queue.append(v)
            elif distS[v] == d_u + 1:
                # Found another shortest path to v from u
                path_count[v] += cnt_u
                # Cap at 2 to avoid overflow and just check existence of multiple paths
                if path_count[v] > 1:
                    path_count[v] = 2
    
    D = distS[T]
    
    # Case 1: S and T are adjacent
    if D == 1:
        # Check if there is any vertex adjacent to S or T other than the other
        possible = False
        for v in adj[S]:
            if v != T:
                possible = True
                break
        if not possible:
            for v in adj[T]:
                if v != S:
                    possible = True
                    break
        
        if possible:
            print(3)
        else:
            print(-1)
        return

    # Case 2: D > 1
    if path_count[T] > 1:
        # Multiple shortest paths exist (vertex disjoint internally)
        print(2 * D)
    else:
        # Unique shortest path, check for branches
        # Reconstruct path
        path = []
        curr = T
        while curr != 0:
            path.append(curr)
            if curr == S:
                break
            curr = parent[curr]
        
        path.reverse()
        
        # Check if any vertex on the path has a neighbor NOT on the path
        path_set = set(path)
        has_branch = False
        
        for u in path:
            for v in adj[u]:
                if v not in path_set:
                    has_branch = True
                    break
            if has_branch:
                break
        
        if has_branch:
            print(2 * D + 2)
        else:
            print(-1)

if __name__ == '__main__':
    solve()