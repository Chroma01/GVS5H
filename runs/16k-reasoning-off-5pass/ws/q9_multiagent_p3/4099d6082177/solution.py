import sys

# Increase recursion depth just in case, though we use iterative DFS
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
    
    # If K=1, every vertex is a path of length 1. Always possible for a tree.
    if K == 1:
        print("Yes")
        return

    # Adjacency list
    adj = [[] for _ in range(total_vertices + 1)]
    
    # Read edges
    # There are total_vertices - 1 edges
    for _ in range(total_vertices - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Iterative DFS to establish order and parents
    parent = [0] * (total_vertices + 1)
    order = []
    stack = [1]
    visited = [False] * (total_vertices + 1)
    visited[1] = True
    
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Check 1: Subtree size / path segment logic
    # rem[u] stores the size of the path segment ending at u going downwards
    # that hasn't been cut yet.
    rem = [0] * (total_vertices + 1)
    cut_edge = [False] * (total_vertices + 1) # cut_edge[u] is true if edge (parent[u], u) is cut
    
    possible = True
    
    for u in reversed(order):
        current_rem = 1
        for v in adj[u]:
            if v == parent[u]:
                continue
            # Child v
            if rem[v] == K:
                # The segment from v is complete (size K), so we cut the edge (u, v)
                # This means v's segment is finished and does not contribute to u.
                # We mark that the edge above v is cut.
                cut_edge[v] = True
            else:
                # The segment from v is incomplete, so we keep the edge (u, v)
                # and merge it with u's segment.
                current_rem += rem[v]
        
        if current_rem > K:
            possible = False
            break
        
        if current_rem == K:
            # The segment ending at u is complete. We cut the edge above u.
            rem[u] = 0
            cut_edge[u] = True
        else:
            rem[u] = current_rem
            
    if not possible:
        print("No")
        return

    # After processing all nodes, the root (1) must have rem[1] == 0
    # because the total number of vertices is NK, which is a multiple of K.
    # If rem[1] != 0, it means we have a remainder that didn't form a complete path.
    if rem[1] != 0:
        print("No")
        return

    # Check 2: Verify that every component is a path (max degree <= 2 within component)
    # A tree component is a path if and only if no vertex in the component has a degree > 2.
    # The degree of a vertex u within its component is:
    # original_degree[u] - (number of incident edges that were cut)
    # An edge (u, v) is cut if cut_edge[u] is True (where v is parent) or cut_edge[v] is True (where u is parent).
    
    for u in range(1, total_vertices + 1):
        deg = len(adj[u])
        
        # Check edge to parent
        if parent[u] != 0 and cut_edge[u]:
            deg -= 1
        
        # Check edges to children
        for v in adj[u]:
            if v == parent[u]:
                continue
            if cut_edge[v]:
                deg -= 1
        
        if deg > 2:
            possible = False
            break
    
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()