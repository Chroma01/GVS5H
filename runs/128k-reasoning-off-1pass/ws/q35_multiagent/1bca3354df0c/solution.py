import sys
from collections import deque

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    M = int(data[1])
    
    adj = [[] for _ in range(N + 1)]
    edges = []
    
    idx = 2
    for _ in range(M):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))
    
    # Color array: 0 = unvisited, 1 and 2 are the two colors
    color = [0] * (N + 1)
    
    total_moves = 0
    
    for i in range(1, N + 1):
        if color[i] != 0:
            continue
        
        # BFS to find connected component and bipartition
        component_nodes = []
        queue = deque([i])
        color[i] = 1
        component_nodes.append(i)
        
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if color[v] == 0:
                    color[v] = 3 - color[u]  # Toggle between 1 and 2
                    component_nodes.append(v)
                    queue.append(v)
                elif color[v] == color[u]:
                    # This should not happen as the graph is bipartite
                    pass
        
        # Count nodes in each partition
        count1 = 0
        count2 = 0
        for node in component_nodes:
            if color[node] == 1:
                count1 += 1
            else:
                count2 += 1
        
        # Maximum edges in complete bipartite graph
        max_edges = count1 * count2
        
        # Count existing edges within this component
        existing_edges = 0
        for u, v in edges:
            # Check if both u and v are in this component
            # We can check by comparing colors, but need to be careful
            # Actually, we need to know which component each edge belongs to
            # Let's use a different approach: mark nodes with component ID
            pass
    
    # Let's redo with component IDs
    color = [0] * (N + 1)
    comp_id = [0] * (N + 1)
    comp_count1 = []
    comp_count2 = []
    comp_edges = []
    
    comp_idx = 0
    for i in range(1, N + 1):
        if color[i] != 0:
            continue
        
        comp_idx += 1
        component_nodes = []
        queue = deque([i])
        color[i] = 1
        comp_id[i] = comp_idx
        component_nodes.append(i)
        
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if color[v] == 0:
                    color[v] = 3 - color[u]
                    comp_id[v] = comp_idx
                    component_nodes.append(v)
                    queue.append(v)
        
        c1 = sum(1 for node in component_nodes if color[node] == 1)
        c2 = len(component_nodes) - c1
        comp_count1.append(c1)
        comp_count2.append(c2)
        comp_edges.append(0)
    
    # Count edges per component
    for u, v in edges:
        cid = comp_id[u]
        # cid is 1-indexed, comp_edges is 0-indexed
        comp_edges[cid - 1] += 1
    
    total_moves = 0
    for i in range(len(comp_count1)):
        max_e = comp_count1[i] * comp_count2[i]
        moves = max_e - comp_edges[i]
        total_moves += moves
    
    if total_moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

solve()