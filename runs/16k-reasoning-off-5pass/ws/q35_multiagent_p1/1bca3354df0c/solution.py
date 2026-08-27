import sys
from collections import deque

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    iterator = iter(data)
    N = int(next(iterator))
    M = int(next(iterator))
    
    adj = [[] for _ in range(N + 1)]
    edges = []
    
    for i in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u, v))
    
    # Color array: 0 = unvisited, 1 and 2 are the two colors
    color = [0] * (N + 1)
    
    total_moves = 0
    
    for start_node in range(1, N + 1):
        if color[start_node] != 0:
            continue
            
        # BFS to find connected component and bipartition
        component_nodes = []
        queue = deque([start_node])
        color[start_node] = 1
        component_nodes.append(start_node)
        
        while queue:
            node = queue.popleft()
            for neighbor in adj[node]:
                if color[neighbor] == 0:
                    color[neighbor] = 3 - color[node]
                    component_nodes.append(neighbor)
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
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
        
        # Count edges in this component
        # Each edge is counted twice if we iterate over all nodes, so we need to be careful
        # Better: count edges by checking both endpoints are in this component
        # But since we have the original edges list, we can just count edges where both endpoints are in component_nodes
        # However, that's O(M) per component which could be slow.
        # Instead, we can count during BFS or use a set for component nodes.
        
        # Let's use a set for O(1) lookup
        comp_set = set(component_nodes)
        comp_edges = 0
        for u, v in edges:
            if u in comp_set and v in comp_set:
                comp_edges += 1
        
        # Number of available moves in this component
        max_edges = count1 * count2
        available_moves = max_edges - comp_edges
        total_moves += available_moves
    
    if total_moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

solve()