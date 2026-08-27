import sys
from collections import defaultdict

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    adj = [[] for _ in range(N+1)]
    degree = [0]*(N+1)
    for _ in range(N-1):
        u = int(next(it)); v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1
    
    is_leaf = [False]*(N+1)
    for i in range(1, N+1):
        if degree[i] == 1:
            is_leaf[i] = True
    
    leaf_count = [0]*(N+1)
    for v in range(1, N+1):
        if is_leaf[v]:
            u = adj[v][0]
            leaf_count[u] += 1
    
    non_leaf_count = [0]*(N+1)
    for v in range(1, N+1):
        non_leaf_count[v] = degree[v] - leaf_count[v]
    
    # For each center u, we need to count valid neighbors v with y = degree[v]-1
    # A neighbor v is valid with center u if:
    # - degree[v] >= 2 (so y >= 1)
    # - (non_leaf_count[v] == 0 and is_leaf[u]) OR (non_leaf_count[v] == 1 and not is_leaf[u])
    # In both cases, y = degree[v] - 1.
    
    counts = [None]*(N+1)
    for u in range(1, N+1):
        for v in adj[u]:
            if degree[v] < 2:
                continue
            y = degree[v] - 1
            if non_leaf_count[v] == 0:
                if not is_leaf[u]:
                    continue
            elif non_leaf_count[v] == 1:
                if is_leaf[u]:
                    continue
            else:
                continue
            if counts[u] is None:
                counts[u] = {}
            d = counts[u]
            d[y] = d.get(y, 0) + 1
    
    max_size = 0
    for u in range(1, N+1):
        d = counts[u]
        if d:
            best_u = 1 + max((y+1)*cnt for y, cnt in d.items())
            if best_u > max_size:
                max_size = best_u
    
    # If no valid snowflake found, we still can always form one (e.g., a path of 3 vertices)
    # but according to problem constraints, there is always a solution.
    # For safety, if max_size is 0, we can take size 3.
    if max_size == 0:
        max_size = 3  # minimal snowflake tree
    
    print(N - max_size)

if __name__ == "__main__":
    solve()