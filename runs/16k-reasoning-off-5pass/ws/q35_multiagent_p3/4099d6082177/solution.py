import sys

# Increase recursion depth to handle deep trees
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return

    total_vertices = N * K
    
    # Build adjacency list
    adj = [[] for _ in range(total_vertices + 1)]
    for _ in range(total_vertices - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # If K == 1, every vertex is a path of length 1, so it's always possible
    if K == 1:
        print("Yes")
        return

    # Root the tree at vertex 1
    root = 1
    
    # Perform DFS to compute pending path lengths
    # We'll use an iterative DFS to avoid recursion limit issues and stack overflow
    # First, build parent pointers and processing order using BFS/DFS
    
    parent = [0] * (total_vertices + 1)
    order = []
    stack = [root]
    visited = [False] * (total_vertices + 1)
    visited[root] = True
    
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Process nodes in reverse order (bottom-up)
    # f[u] = length of pending path segment ending at u going upward
    # f[u] = 0 means no pending segment (subtree fully decomposed)
    f = [0] * (total_vertices + 1)
    
    possible = True
    
    for u in reversed(order):
        # Collect pending path lengths from children
        children_pending = []
        for v in adj[u]:
            if v == parent[u]:
                continue
            if f[v] > 0:
                children_pending.append(f[v])
        
        # Count how many children have pending paths
        num_pending = len(children_pending)
        
        if num_pending > 1:
            # Can't merge more than one pending path through a single node
            possible = False
            break
        elif num_pending == 1:
            # Extend the one pending path from child
            new_len = children_pending[0] + 1
        else:
            # No pending paths from children, start a new path at u
            new_len = 1
        
        # Check if the new path length exceeds K
        if new_len > K:
            possible = False
            break
        elif new_len == K:
            # Path is complete, so no pending segment from u
            f[u] = 0
        else:
            # Path is incomplete, pending segment of length new_len
            f[u] = new_len
    
    # At the root, there should be no pending path (all paths must be complete)
    if possible and f[root] != 0:
        possible = False
    
    if possible:
        print("Yes")
    else:
        print("No")

solve()