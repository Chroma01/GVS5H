import sys

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        T_str = next(iterator)
        T = int(T_str)
    except StopIteration:
        return

    MOD = 998244353
    
    results = []
    
    for _ in range(T):
        try:
            H = int(next(iterator))
            W = int(next(iterator))
            grid = []
            for _ in range(H):
                grid.append(next(iterator))
        except StopIteration:
            break
            
        # Condition 1: Every column must have an even number of 'A's.
        # Condition 2: Every row must have an even number of 'A's.
        # If either fails, the answer is 0.
        
        possible = True
        
        # We will build the graph on the fly.
        # Nodes 0..W-1 represent x_{-1, j} (vertical state entering row 0 at col j).
        # Nodes W..W+H-1 represent H_{i, -1} (horizontal state entering row i at col 0).
        # Total nodes = W + H.
        
        adj = [[] for _ in range(W + H)]
        
        # col_counts[j] will store the number of 'A's in column j from row 0 to current row i-1.
        col_counts = [0] * W
        
        for i in range(H):
            row_prefix = 0
            for j in range(W):
                char = grid[i][j]
                
                if char == 'A':
                    row_prefix += 1
                    col_counts[j] += 1
                elif char == 'B':
                    # For a 'B' tile at (i, j), we add an edge between node j and node W+i.
                    # The weight w is determined by the consistency equation:
                    # H_{i, -1} = x_{-1, j} ^ col_counts[j] ^ row_prefix ^ 1
                    # So the edge weight w = col_counts[j] ^ row_prefix ^ 1
                    w = col_counts[j] ^ row_prefix ^ 1
                    u = j
                    v = W + i
                    adj[u].append((v, w))
                    adj[v].append((u, w))
            
            # Check row parity
            if row_prefix % 2 != 0:
                possible = False
                break
        
        if not possible:
            results.append("0")
            continue
            
        # Check column parities
        for j in range(W):
            if col_counts[j] % 2 != 0:
                possible = False
                break
        
        if not possible:
            results.append("0")
            continue
            
        # If we are here, parities are valid.
        # Now count connected components in the graph and check for consistency.
        # Variables: W + H nodes.
        # We use BFS to traverse components.
        
        visited = [False] * (W + H)
        val = [0] * (W + H) # Stores value relative to component root
        components = 0
        consistent = True
        
        for start_node in range(W + H):
            if not visited[start_node]:
                components += 1
                queue = [start_node]
                visited[start_node] = True
                val[start_node] = 0
                
                idx = 0
                while idx < len(queue):
                    u = queue[idx]
                    idx += 1
                    
                    for v, w in adj[u]:
                        if not visited[v]:
                            visited[v] = True
                            val[v] = val[u] ^ w
                            queue.append(v)
                        else:
                            # Check consistency
                            if val[u] ^ w != val[v]:
                                consistent = False
                                break
                    if not consistent:
                        break
                if not consistent:
                    break
        
        if not consistent:
            results.append("0")
        else:
            # Number of ways is 2^(number of connected components)
            ans = pow(2, components, MOD)
            results.append(str(ans))
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()