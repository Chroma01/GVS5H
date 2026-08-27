import sys
from collections import deque

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

    total_nodes = N * K
    
    # Build adjacency list
    adj = [[] for _ in range(total_nodes + 1)]
    for _ in range(total_nodes - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
    
    # Edge case: K=1, each node is a path of length 1, always possible
    if K == 1:
        print("Yes")
        return

    # Root the tree at node 1
    # Compute parent and depth using BFS
    parent = [0] * (total_nodes + 1)
    depth = [0] * (total_nodes + 1)
    visited = [False] * (total_nodes + 1)
    
    queue = deque([1])
    visited[1] = True
    depth[1] = 0
    parent[1] = 0  # Root has no parent
    
    # BFS to compute depths and parents
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                depth[v] = depth[u] + 1
                queue.append(v)
    
    # Sort nodes by depth in descending order
    nodes_by_depth = list(range(1, total_nodes + 1))
    nodes_by_depth.sort(key=lambda x: depth[x], reverse=True)
    
    covered = [False] * (total_nodes + 1)
    
    for u in nodes_by_depth:
        if covered[u]:
            continue
        
        # This node must be the bottom of a new path
        # Trace up K-1 steps
        current = u
        path_nodes = []
        valid = True
        
        for _ in range(K):
            if current == 0:
                # Hit above root
                valid = False
                break
            if covered[current]:
                # Already covered, can't use it
                valid = False
                break
            path_nodes.append(current)
            current = parent[current]
        
        if not valid:
            print("No")
            return
        
        # Mark all nodes in this path as covered
        for node in path_nodes:
            covered[node] = True
    
    # If we got here, all nodes are covered successfully
    print("Yes")

solve()