import sys

# Increase recursion depth just in case, though iterative approach is used below
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

    # Adjacency list
    adj = [[] for _ in range(N + 1)]
    degree = [0] * (N + 1)
    
    # Read N-1 edges
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    # Identify nodes with degree >= 4
    # We need to find the largest connected component consisting ONLY of such nodes.
    # Let's mark these nodes.
    valid_nodes = [i for i in range(1, N + 1) if degree[i] >= 4]
    
    if not valid_nodes:
        print("-1")
        return

    visited = [False] * (N + 1)
    max_component_size = 0

    # Iterate through all valid nodes to find connected components
    for start_node in valid_nodes:
        if visited[start_node]:
            continue
        
        # BFS to find the size of the connected component
        stack = [start_node]
        visited[start_node] = True
        current_size = 0
        
        while stack:
            u = stack.pop()
            current_size += 1
            
            for v in adj[u]:
                # Only traverse to neighbors that are also valid (degree >= 4)
                if not visited[v] and degree[v] >= 4:
                    visited[v] = True
                    stack.append(v)
        
        if current_size > max_component_size:
            max_component_size = current_size

    # If we found a component, the answer is 3 * size + 2
    # If max_component_size is 0 (should not happen if valid_nodes is not empty), handle it
    if max_component_size == 0:
        print("-1")
    else:
        print(3 * max_component_size + 2)

if __name__ == '__main__':
    solve()