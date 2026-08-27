import sys

# Increase recursion depth just in case, though iterative BFS is used
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

    # A tree with N < 5 cannot have a node with degree 4
    if N < 5:
        print("-1")
        return

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
    high_degree_nodes = [i for i in range(1, N + 1) if degree[i] >= 4]
    
    if not high_degree_nodes:
        print("-1")
        return

    # Find connected components among high_degree_nodes
    visited = [False] * (N + 1)
    max_component_size = 0

    for start_node in high_degree_nodes:
        if not visited[start_node]:
            # BFS to find component size
            queue = [start_node]
            visited[start_node] = True
            count = 0
            
            idx = 0
            while idx < len(queue):
                u = queue[idx]
                idx += 1
                count += 1
                
                for v in adj[u]:
                    # We only care about connectivity within the set of high-degree nodes
                    # The component is defined by the subgraph induced by high-degree nodes.
                    # So we only traverse to neighbors that are also high-degree nodes.
                    if not visited[v] and degree[v] >= 4:
                        visited[v] = True
                        queue.append(v)
            
            if count > max_component_size:
                max_component_size = count

    if max_component_size == 0:
        print("-1")
    elif max_component_size == 1:
        print("5")
    else:
        # Formula for |S| >= 2: 3*|S| + 2
        print(3 * max_component_size + 2)

if __name__ == '__main__':
    solve()