import sys
from collections import deque

# Increase recursion depth just in case, though we will use BFS
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

    # Colors array: 0 for unvisited, 1 and -1 for the two partitions
    colors = [0] * (N + 1)
    
    total_max_edges = 0
    
    for i in range(1, N + 1):
        if colors[i] != 0:
            continue
            
        # Start BFS for this connected component
        queue = deque([i])
        colors[i] = 1
        count1 = 0
        count2 = 0
        
        while queue:
            u = queue.popleft()
            
            if colors[u] == 1:
                count1 += 1
            else:
                count2 += 1
                
            for v in adj[u]:
                if colors[v] == 0:
                    colors[v] = -colors[u]
                    queue.append(v)
                elif colors[v] == colors[u]:
                    # This should not happen based on problem statement
                    # "The given graph does not contain an odd cycle"
                    pass
        
        total_max_edges += count1 * count2

    moves = total_max_edges - M
    
    if moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

if __name__ == '__main__':
    solve()