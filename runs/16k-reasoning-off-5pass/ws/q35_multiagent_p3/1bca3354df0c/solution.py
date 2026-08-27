import sys
sys.setrecursionlimit(300000)

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    M = int(data[1])
    
    adj = [[] for _ in range(N + 1)]
    idx = 2
    for _ in range(M):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
    
    # Find connected components and compute bipartition sizes
    visited = [False] * (N + 1)
    color = [0] * (N + 1)  # 0 or 1 for the two partitions
    
    total_max_edges = 0
    
    for i in range(1, N + 1):
        if not visited[i]:
            # BFS to find the component and bipartition
            component_nodes = []
            queue = [i]
            visited[i] = True
            color[i] = 0
            component_nodes.append(i)
            
            head = 0
            while head < len(queue):
                u = queue[head]
                head += 1
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        color[v] = 1 - color[u]
                        queue.append(v)
                        component_nodes.append(v)
                    else:
                        # Check consistency (should be fine per problem statement)
                        pass
            
            # Count partition sizes
            count0 = 0
            count1 = 0
            for node in component_nodes:
                if color[node] == 0:
                    count0 += 1
                else:
                    count1 += 1
            
            total_max_edges += count0 * count1
    
    num_moves = total_max_edges - M
    
    if num_moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

solve()