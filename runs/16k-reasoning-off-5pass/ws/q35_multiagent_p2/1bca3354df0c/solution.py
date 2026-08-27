import sys
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        
    # Colors: 0 for unvisited, 1 and 2 for the two partitions
    color = [0] * (N + 1)
    
    total_possible_edges = 0
    
    for i in range(1, N + 1):
        if color[i] != 0:
            continue
            
        # Start BFS/DFS for this connected component
        # We'll use a stack for DFS
        stack = [i]
        color[i] = 1
        count1 = 0
        count2 = 0
        
        while stack:
            node = stack.pop()
            c = color[node]
            if c == 1:
                count1 += 1
            else:
                count2 += 1
                
            for neighbor in adj[node]:
                if color[neighbor] == 0:
                    color[neighbor] = 3 - c  # Toggle between 1 and 2
                    stack.append(neighbor)
                # If color[neighbor] is already set, we don't need to do anything
                # because the graph is guaranteed to be bipartite initially.
        
        total_possible_edges += count1 * count2
        
    # Total moves available = total_possible_edges - M
    total_moves = total_possible_edges - M
    
    if total_moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

if __name__ == '__main__':
    solve()