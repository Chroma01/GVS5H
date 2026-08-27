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

    # If K=1, every vertex is a path of length 1. Always possible.
    if K == 1:
        print("Yes")
        return

    # Parent array to help with post-order traversal or just use DFS with parent check
    # We will use a recursive DFS with parent pointer to avoid cycles
    
    # We need to return:
    # - 0 if the subtree is perfectly decomposed (no pending path)
    # - L in [1, K-1] if there is a pending path of length L ending at this node
    # - -1 if decomposition is impossible
    
    # To avoid recursion limit issues on very deep trees, we can use iterative post-order traversal
    # But given NK <= 2*10^5, recursion might be okay if we set recursion limit.
    # Let's use iterative post-order to be safe.
    
    parent = [0] * (total_vertices + 1)
    order = []
    stack = [1]
    visited = [False] * (total_vertices + 1)
    visited[1] = True
    
    # BFS/DFS to establish parent pointers and processing order
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Process in reverse order (post-order: children before parent)
    # pending[u] stores the length of the pending path ending at u, or -1 if impossible
    pending = [0] * (total_vertices + 1)
    
    for u in reversed(order):
        # Collect pending lengths from children
        # Children are neighbors except parent
        children_pending = []
        for v in adj[u]:
            if v == parent[u]:
                continue
            
            p_val = pending[v]
            if p_val == -1:
                pending[u] = -1
                break
            
            # Extend the path from child v to u
            # The path length becomes p_val + 1
            new_len = p_val + 1
            
            if new_len == K:
                # Path is complete, so it doesn't contribute to pending at u
                pass
            else:
                # It's a pending path ending at u
                children_pending.append(new_len)
        
        if pending[u] == -1:
            continue
            
        # Now process children_pending at node u
        # Constraint: u can connect to at most 2 children in the path decomposition
        if len(children_pending) > 2:
            pending[u] = -1
            continue
        
        if len(children_pending) == 0:
            # No pending paths from children. Start a new path at u of length 1.
            pending[u] = 1
        elif len(children_pending) == 1:
            # One pending path from a child. It ends at u.
            # It can be extended to parent.
            pending[u] = children_pending[0]
        else: # len == 2
            # Two pending paths. Must merge them at u.
            a, b = children_pending[0], children_pending[1]
            merged_len = a + b
            if merged_len == K:
                # Complete path
                pending[u] = 0
            elif merged_len < K:
                # Pending path of merged length
                pending[u] = merged_len
            else:
                # Merged path exceeds K, impossible
                pending[u] = -1

    # After processing root (vertex 1)
    # If pending[1] == 0, it means all paths are complete.
    # If pending[1] > 0, there is an incomplete path.
    # If pending[1] == -1, impossible.
    
    if pending[1] == 0:
        print("Yes")
    else:
        print("No")

solve()