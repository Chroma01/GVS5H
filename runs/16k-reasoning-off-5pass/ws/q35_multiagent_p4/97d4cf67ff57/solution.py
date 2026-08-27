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
    except StopIteration:
        return

    if N < 5:
        # An alkane must have at least one vertex of degree 4, so at least 5 vertices (1 center + 4 leaves)
        # Actually, a center with 4 leaves is 5 vertices.
        # But let's check constraints: N >= 1.
        # If N < 5, it's impossible to have a degree 4 node.
        print(-1)
        return

    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Root the tree at 1
    parent = [0] * (N + 1)
    order = []
    stack = [1]
    visited = [False] * (N + 1)
    visited[1] = True
    
    # BFS/DFS to establish parent pointers and processing order
    # Using a stack for DFS to get a post-order traversal easily
    # We need to process children before parents, so reverse the order of a BFS or DFS
    queue = [1]
    visited = [False] * (N + 1)
    visited[1] = True
    bfs_order = []
    
    import collections
    q = collections.deque([1])
    while q:
        u = q.popleft()
        bfs_order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                q.append(v)
    
    # Process in reverse BFS order (leaves to root)
    # dp1[u]: max size of a valid branch rooted at u, where u has degree 1 in the alkane subgraph.
    #         This means u connects to exactly one child in the subgraph.
    # dp4[u]: max size of a valid alkane component rooted at u, where u has degree 4 in the alkane subgraph.
    #         This means u connects to exactly 4 children in the subgraph.
    
    dp1 = [0] * (N + 1)
    dp4 = [-float('inf')] * (N + 1)
    
    # Initialize for leaves
    # We'll compute based on children
    
    for u in reversed(bfs_order):
        children = [v for v in adj[u] if v != parent[u]]
        
        if not children:
            # Leaf node
            dp1[u] = 1
            dp4[u] = -float('inf')
        else:
            # Calculate potential contributions from each child
            # For a child v, the max size of a valid component attached to u via v is max(dp1[v], dp4[v])
            # dp1[v]: v is a leaf in the alkane (degree 1). The edge (u,v) is its only edge.
            # dp4[v]: v is a center in the alkane (degree 4). The edge (u,v) is one of its 4 edges.
            
            child_vals = []
            for v in children:
                val = max(dp1[v], dp4[v])
                if val > -float('inf'):
                    child_vals.append(val)
            
            if not child_vals:
                # No valid branches from children
                dp1[u] = 1 # u itself can be a branch of length 1 (degree 0 in subtree, degree 1 when connected to parent)
                dp4[u] = -float('inf')
            else:
                # dp1[u]: u connects to exactly one child. Pick the best one.
                dp1[u] = 1 + max(child_vals)
                
                # dp4[u]: u connects to exactly 4 children. Pick the 4 best ones.
                if len(child_vals) >= 4:
                    child_vals.sort(reverse=True)
                    dp4[u] = 1 + sum(child_vals[:4])
                else:
                    dp4[u] = -float('inf')

    ans = -float('inf')
    for u in range(1, N + 1):
        if dp4[u] > ans:
            ans = dp4[u]
            
    if ans == -float('inf'):
        print(-1)
    else:
        print(ans)

solve()