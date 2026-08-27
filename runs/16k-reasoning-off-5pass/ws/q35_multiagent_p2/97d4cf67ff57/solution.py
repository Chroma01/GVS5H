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
        # An alkane needs at least one degree-4 node and 4 branches.
        # Minimum vertices: 1 (center) + 4 (leaves) = 5.
        # Actually, branches can be longer. But if N < 5, impossible.
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
    # Using a stack for DFS order to get a topological sort from leaves to root
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Reverse order to process from leaves up to root for 'down' DP
    down = [0] * (N + 1)
    # down[u] = max length (in edges) of a path starting at u and going down into its subtree
    
    for u in reversed(order):
        max_child_down = 0
        for v in adj[u]:
            if v == parent[u]:
                continue
            if down[v] + 1 > max_child_down:
                max_child_down = down[v] + 1
        down[u] = max_child_down

    # Compute 'up' DP
    # up[u] = max length (in edges) of a path starting at u and going up through its parent
    up = [0] * (N + 1)
    # up[1] = 0 (no parent)
    
    # Process from root down to leaves
    for u in order:
        # For each child v of u, compute up[v]
        # up[v] = 1 + max(up[u], max(down[w] for w in children(u) if w != v))
        
        # Find the top two down values among children to efficiently compute max for each child
        children_down = []
        for v in adj[u]:
            if v == parent[u]:
                continue
            children_down.append(down[v])
        
        # Sort descending to get top 2
        children_down.sort(reverse=True)
        
        # If no children, up[v] is not needed for any v (u is leaf)
        # But we still need to propagate up[u] to children
        
        # The best path going up from u is either through parent (up[u])
        # or through another child (children_down[0] if exists)
        
        best_up_from_u = up[u]
        if children_down:
            best_up_from_u = max(best_up_from_u, children_down[0])
        
        for v in adj[u]:
            if v == parent[u]:
                continue
            
            # For child v, the best alternative path from u (excluding v's subtree)
            # is either up[u] or the best down from other children.
            
            # Check if v's down value is the maximum among children
            # If children_down has only one element, or v's down is not the max
            val_v = down[v]
            
            # Find the max of (up[u], down[w] for w != v)
            # If children_down[0] == val_v, we might need children_down[1]
            # But there could be multiple children with same max value.
            # Safest way:
            candidates = [up[u]]
            for w in adj[u]:
                if w == parent[u] or w == v:
                    continue
                candidates.append(down[w])
            
            max_alt = 0
            if candidates:
                max_alt = max(candidates)
            
            up[v] = 1 + max_alt

    # Now, for each node u, collect all branch lengths
    # Branch length from u to child v: 1 + down[v]
    # Branch length from u to parent: up[u]
    
    max_alkane = -1
    
    for u in range(1, N + 1):
        branches = []
        
        # Branches to children
        for v in adj[u]:
            if v == parent[u]:
                continue
            branches.append(1 + down[v])
            
        # Branch to parent
        if parent[u] != 0:
            branches.append(up[u])
            
        if len(branches) >= 4:
            branches.sort(reverse=True)
            # Take top 4
            total_vertices = 1 + sum(branches[:4])
            if total_vertices > max_alkane:
                max_alkane = total_vertices
                
    print(max_alkane)

if __name__ == '__main__':
    solve()