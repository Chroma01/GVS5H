
## ideation
```python
import sys

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(2000000)

def solve():
    # Read all input at once for speed
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        num_test_cases = int(next(iterator))
    except StopIteration:
        return

    MOD = 998244353

    for _ in range(num_test_cases):
        try:
            H = int(next(iterator))
            W = int(next(iterator))
            S = []
            for _ in range(H):
                S.append(next(iterator))
        except StopIteration:
            break

        # Parity check for rows
        # Each row must have an even number of 'A's for the horizontal system to be consistent.
        row_parity_ok = True
        for r in range(H):
            if S[r].count('A') % 2 != 0:
                row_parity_ok = False
                break
        if not row_parity_ok:
            print(0)
            continue

        # Parity check for columns
        # Each column must have an even number of 'A's for the vertical system to be consistent.
        # We compute column parities efficiently.
        col_parity = [0] * W
        for r in range(H):
            row_str = S[r]
            for c, char in enumerate(row_str):
                if char == 'A':
                    col_parity[c] ^= 1
        
        col_parity_ok = True
        for p in col_parity:
            if p != 0:
                col_parity_ok = False
                break
        
        if not col_parity_ok:
            print(0)
            continue

        # Compute R^(0): Particular solution for horizontal constraints
        # R[r][c] represents the status of the right edge of cell (r, c).
        # Constraint: R[r][c-1] ^ R[r][c] = 1 if S[r][c]=='A' else 0.
        # We fix R[r][0] = 0.
        R = [[0] * W for _ in range(H)]
        for r in range(H):
            row_str = S[r]
            current = 0
            # R[r][0] is 0
            for c in range(1, W):
                if row_str[c] == 'A':
                    current ^= 1
                R[r][c] = current
        
        # Compute B^(0): Particular solution for vertical constraints
        # B[r][c] represents the status of the bottom edge of cell (r, c).
        # Constraint: B[r-1][c] ^ B[r][c] = 1 if S[r][c]=='A' else 0.
        # We fix B[0][c] = 0.
        # Optimized computation to be row-major friendly
        B = [None] * H
        B[0] = [0] * W
        current_B = [0] * W # Holds B[r-1][c]
        
        for r in range(1, H):
            row_str = S[r]
            new_row = [0] * W
            for c in range(W):
                if row_str[c] == 'A':
                    current_B[c] ^= 1
                new_row[c] = current_B[c]
            B[r] = new_row

        # Build Graph
        # Nodes 0..H-1 represent rows, H..H+W-1 represent columns.
        # Edges exist between row r and col c if S[r][c] == 'B'.
        # Weight w = (R[r][c] ^ B[r][c]) ^ 1.
        # This weight comes from the condition R[r][c] != B[r][c] for 'B' tiles.
        adj = [[] for _ in range(H + W)]
        
        for r in range(H):
            row_str = S[r]
            row_R = R[r]
            row_B = B[r]
            
            # Find 'B' cells
            for c in range(W):
                if row_str[c] == 'B':
                    w = (row_R[c] ^ row_B[c]) ^ 1
                    u = r
                    v = H + c
                    adj[u].append((v, w))
                    adj[v].append((u, w))

        # BFS to find connected components and check consistency
        visited = [False] * (H + W)
        val = [0] * (H + W)
        comp_count = 0
        possible = True
        
        for i in range(H + W):
            if not visited[i]:
                comp_count += 1
                # Start BFS
                queue = [i]
                visited[i] = True
                val[i] = 0
                
                head = 0
                while head < len(queue):
                    u = queue[head]
                    head += 1
                    
                    current_val = val[u]
                    
                    for v, w in adj[u]:
                        expected = current_val ^ w
                        if not visited[v]:
                            visited[v] = True
                            val[v] = expected
                            queue.append(v)
                        else:
                            if val[v] != expected:
                                possible = False
                                break
                    if not possible:
                        break
                if not possible:
                    break
        
        if not possible:
            print(0)
        else:
            # The number of solutions is 2^(number of connected components)
            print(pow(2, comp_count, MOD))

if __name__ == '__main__':
    solve()
```
