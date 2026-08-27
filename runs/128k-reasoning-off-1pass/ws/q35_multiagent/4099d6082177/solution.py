import sys

# Increase recursion depth just in case, though we will use iterative post-order
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
    
    # If K=1, every vertex is a path of length 0 (1 vertex). Always possible.
    if K == 1:
        print("Yes")
        return

    # Build adjacency list
    adj = [[] for _ in range(total_vertices + 1)]
    for _ in range(total_vertices - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Root the tree at vertex 1
    root = 1
    
    # Perform BFS/DFS to determine parent pointers and processing order (post-order)
    parent = [0] * (total_vertices + 1)
    order = []
    stack = [root]
    visited = [False] * (total_vertices + 1)
    visited[root] = True
    
    # Iterative DFS to build order and parents
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Process in reverse order (bottom-up: leaves to root)
    # len[u] stores the length of the path segment ending at u coming from its subtree.
    # If the path is completed at u (length K), we can mark it as -1 or similar.
    # Actually, let's use -1 to indicate "completed/removed".
    # len[u] = 0 means a path of 1 vertex ends at u (just the vertex itself).
    # len[u] = L means a path of L+1 vertices ends at u.
    
    path_len = [-1] * (total_vertices + 1)
    
    # Reverse order gives us children before parents
    for u in reversed(order):
        # Collect path lengths from children
        # A child v contributes a path segment of length path_len[v] + 1 to u,
        # provided path_len[v] != -1 (not completed) and path_len[v] + 1 < K.
        # If path_len[v] + 1 == K, the path is completed at u (via edge u-v), so it's removed.
        
        active_segments = []
        
        for v in adj[u]:
            if v == parent[u]:
                continue
            
            if path_len[v] == -1:
                # Path from v's subtree is already completed, ignore
                continue
            
            # The path segment from v extends to u
            new_len = path_len[v] + 1
            
            if new_len == K:
                # This path is completed at u. It doesn't propagate up.
                # So we don't add it to active_segments.
                pass
            elif new_len < K:
                active_segments.append(new_len)
            else:
                # new_len > K, impossible
                print("No")
                return
        
        # Now, node u can connect at most 2 active segments from its children.
        # If it has more than 2, it's impossible because u can only belong to one path
        # and have at most 2 neighbors in that path.
        if len(active_segments) > 2:
            print("No")
            return
        
        if len(active_segments) == 0:
            # No active paths coming from children.
            # u starts a new path segment of length 0 (1 vertex).
            path_len[u] = 0
        elif len(active_segments) == 1:
            # One active segment from a child. Extend it to u.
            path_len[u] = active_segments[0] + 1
        elif len(active_segments) == 2:
            # Two active segments. Merge them through u.
            # The new path segment ending at u has length L1 + L2 + 1.
            L1, L2 = active_segments
            new_len = L1 + L2 + 1
            
            if new_len == K:
                # Path completed at u
                path_len[u] = -1
            elif new_len < K:
                path_len[u] = new_len
            else:
                # new_len > K, impossible
                print("No")
                return

    # After processing the root, check if the root's path is completed.
    # If path_len[root] != -1, it means there's an incomplete path ending at the root.
    if path_len[root] != -1:
        print("No")
    else:
        print("Yes")

solve()