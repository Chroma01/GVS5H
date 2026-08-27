import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    grid = input_data[1:1+N]
    
    # Precompute adjacency lists
    # adj_in[u][c] = list of nodes v such that v -> u has label c
    # adj_out[v][c] = list of nodes u such that v -> u has label c
    adj_in = [[[] for _ in range(26)] for _ in range(N)]
    adj_out = [[[] for _ in range(26)] for _ in range(N)]
    
    for i in range(N):
        for j in range(N):
            c_char = grid[i][j]
            if c_char != '-':
                c_idx = ord(c_char) - ord('a')
                adj_in[j][c_idx].append(i)
                adj_out[i][c_idx].append(j)
                
    # dist[i][j] stores the shortest palindrome path length from i to j
    # Initialize with -1 (unreachable)
    dist = [[-1] * N for _ in range(N)]
    queue = deque()
    
    # Initialize:
    # 1. Empty paths: dist[i][i] = 0
    for i in range(N):
        dist[i][i] = 0
        queue.append((i, i, 0))
        
    # 2. Single edge paths: if edge i->j exists, dist[i][j] = 1
    # Note: If i==j, dist[i][i] is already 0, which is better than 1.
    for i in range(N):
        for j in range(N):
            c_char = grid[i][j]
            if c_char != '-':
                if dist[i][j] == -1:
                    dist[i][j] = 1
                    queue.append((i, j, 1))
                    
    # BFS on pairs (u, v)
    # We expand by finding edges a->u and v->b with same label c
    # This creates a palindrome path from a to b of length current_len + 2
    
    while queue:
        u, v, d = queue.popleft()
        
        # Try all possible labels
        for c_idx in range(26):
            # Get predecessors of u with label c
            preds_u = adj_in[u][c_idx]
            # Get successors of v with label c
            succs_v = adj_out[v][c_idx]
            
            if not preds_u or not succs_v:
                continue
                
            # For each pair (a, b) where a->u and v->b have label c
            for a in preds_u:
                for b in succs_v:
                    if dist[a][b] == -1:
                        dist[a][b] = d + 2
                        queue.append((a, b, d + 2))
                        
    # Output the results
    for i in range(N):
        print(' '.join(map(str, dist[i])))

solve()