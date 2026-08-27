import sys

# Increase recursion depth just in case, though we use iterative BFS/DFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return

    # Total vertices should be N*K
    total_vertices = N * K
    
    # Adjacency list for the tree
    adj = [[] for _ in range(total_vertices + 1)]
    
    # Read NK-1 edges
    for _ in range(total_vertices - 1):
        try:
            u = int(next(iterator))
            v = int(next(iterator))
            adj[u].append(v)
            adj[v].append(u)
        except StopIteration:
            break
            
    # Root the tree at vertex 1
    # We use BFS to establish parent-child relationships and processing order
    # This avoids recursion depth issues for deep trees
    parent = [0] * (total_vertices + 1)
    order = []
    stack = [1]
    visited = [False] * (total_vertices + 1)
    visited[1] = True
    
    # Use a list as a stack for DFS to get processing order
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Compute subtree sizes
    sz = [1] * (total_vertices + 1)
    
    # Process nodes in reverse order (children before parents)
    for u in reversed(order):
        if u == 1:
            continue
        p = parent[u]
        sz[p] += sz[u]
        
    # Check the two necessary and sufficient conditions:
    # 1. For every node u, sz[u] % K <= 1
    # 2. For every node u, the number of children v with sz[v] % K == 1 is at most 1
    
    possible = True
    
    for u in range(1, total_vertices + 1):
        rem_u = sz[u] % K
        
        # Condition 1: Subtree size modulo K must be 0 or 1
        if rem_u > 1:
            possible = False
            break
        
        # Condition 2: Count children with remainder 1
        # We only care about children (neighbors excluding parent)
        count_rem1 = 0
        for v in adj[u]:
            if v == parent[u]:
                continue
            if sz[v] % K == 1:
                count_rem1 += 1
        
        # If more than one child has a remainder of 1, we cannot form valid paths
        # without violating the length constraint or connectivity for K >= 2.
        # Specifically for K=2 (Sample 2), this is the failure case.
        if count_rem1 > 1:
            possible = False
            break
            
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()