import sys

# Increase recursion depth to handle deep recursion in find if necessary
sys.setrecursionlimit(2000000)

def solve():
    # Read all input from stdin
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

    for _ in range(T):
        try:
            H = int(next(iterator))
            W = int(next(iterator))
            grid = []
            for _ in range(H):
                grid.append(next(iterator))
        except StopIteration:
            break

        # Precompute prefix XOR sums for rows and columns
        # row_parity[i][j] = parity of 'A' in grid[i][0...j]
        # col_parity[i][j] = parity of 'A' in grid[0...i][j]
        
        row_parity = [[0] * W for _ in range(H)]
        for r in range(H):
            curr = 0
            for c in range(W):
                if grid[r][c] == 'A':
                    curr ^= 1
                row_parity[r][c] = curr

        col_parity = [[0] * W for _ in range(H)]
        for c in range(W):
            curr = 0
            for r in range(H):
                if grid[r][c] == 'A':
                    curr ^= 1
                col_parity[r][c] = curr

        # Check row and column constraints
        # For each row, total 'A' count must be even
        # For each col, total 'A' count must be even
        possible = True
        for r in range(H):
            if row_parity[r][W-1] == 1:
                possible = False
                break
        if possible:
            for c in range(W):
                if col_parity[H-1][c] == 1:
                    possible = False
                    break
        
        if not possible:
            print(0)
            continue

        # Union-Find with XOR tracking
        # Nodes: 0..H-1 represent rows, H..H+W-1 represent columns
        # parent[i] stores the parent of i
        # xor_val[i] stores the XOR difference between i and parent[i]
        
        parent = list(range(H + W))
        xor_val = [0] * (H + W)
        
        def find(i):
            if parent[i] != i:
                root, path_xor = find(parent[i])
                parent[i] = root
                xor_val[i] ^= path_xor
            return parent[i]

        def union(i, j, w):
            root_i = find(i)
            root_j = find(j)
            
            if root_i != root_j:
                # Merge root_j into root_i
                # We want: val[i] ^ val[j] = w
                # We know: val[i] ^ val[root_i] = xor_val[i]
                #          val[j] ^ val[root_j] = xor_val[j]
                # So: (val[root_i] ^ xor_val[i]) ^ (val[root_j] ^ xor_val[j]) = w
                # => val[root_i] ^ val[root_j] = w ^ xor_val[i] ^ xor_val[j]
                parent[root_j] = root_i
                xor_val[root_j] = w ^ xor_val[i] ^ xor_val[j]
                return True
            else:
                # Check consistency
                # val[i] ^ val[j] should be w
                # Current implied: val[i] ^ val[j] = xor_val[i] ^ xor_val[j]
                if xor_val[i] ^ xor_val[j] != w:
                    return False
                return True

        components = H + W
        consistent = True
        
        for r in range(H):
            for c in range(W):
                if grid[r][c] == 'B':
                    # Calculate weight
                    # P_row(r, c) is row_parity[r][c]
                    # P_col(r, c) is col_parity[r][c]
                    w = row_parity[r][c] ^ col_parity[r][c]
                    
                    u = r
                    v = H + c
                    
                    if not union(u, v, w):
                        consistent = False
                        break
                    if not consistent:
                        break
            if not consistent:
                break
        
        if not consistent:
            print(0)
        else:
            # Number of solutions is 2^(number of connected components)
            ans = pow(2, components, MOD)
            print(ans)

if __name__ == '__main__':
    solve()