import sys

# Increase recursion depth just in case, though iterative find is used
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

    # Precompute powers of 2 up to max possible H+W (10^6)
    # Constraints: sum of HW <= 10^6, so H, W <= 10^6 individually in worst case
    MAX_VAL = 1000005
    pow2 = [1] * MAX_VAL
    for i in range(1, MAX_VAL):
        pow2[i] = (pow2[i-1] * 2) % MOD

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

        # Logic:
        # The problem asks for the number of ways to orient tiles such that no "dead ends" exist.
        # This condition implies that for every boundary between cells, the connection status must be consistent.
        # This forces the horizontal connection status to be constant for each row (r_i)
        # and the vertical connection status to be constant for each column (c_j).
        #
        # For Type A tiles: Any combination of (r_i, c_j) is valid with exactly 1 orientation.
        # For Type B tiles: The tile connects opposite edges.
        #   - Orientation 1: Connects Right and Left. This requires r_i = 1 (Right active) and c_j = 0 (Vertical inactive).
        #   - Orientation 2: Connects Top and Bottom. This requires r_i = 0 (Horizontal inactive) and c_j = 1 (Vertical active).
        #   - Thus, for a Type B tile at (i, j), we must have r_i != c_j.
        #
        # We need to count pairs of vectors r (size H) and c (size W) such that for all (i, j) with grid[i][j] == 'B', r_i != c_j.
        # This implies c_j = 1 - r_i for all i where (i, j) is 'B'.
        # This creates constraints on r: if column j has 'B's in rows i1, i2, ..., then r_i1 = r_i2 = ...
        # This defines connected components of rows. Let M be the number of such components.
        # We can choose r freely for each component (2 choices).
        # Once r is chosen, c_j is determined for all columns containing at least one 'B'.
        # Columns containing no 'B's are unconstrained (2 choices each). Let K be the count of such columns.
        # Total ways = 2^M * 2^K.
        
        # DSU initialization
        parent = list(range(H))
        
        def find(i):
            path = []
            while i != parent[i]:
                path.append(i)
                i = parent[i]
            for node in path:
                parent[node] = i
            return i

        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False

        # Identify columns with 'B' and union rows
        cols_with_B = [False] * W
        col_rows = [[] for _ in range(W)]
        
        for r in range(H):
            row_str = grid[r]
            for c in range(W):
                if row_str[c] == 'B':
                    cols_with_B[c] = True
                    col_rows[c].append(r)
        
        # Perform unions
        for c in range(W):
            if col_rows[c]:
                first = col_rows[c][0]
                for r in col_rows[c][1:]:
                    union(first, r)
        
        # Count components
        components = 0
        for i in range(H):
            if parent[i] == i:
                components += 1
        
        # Count columns with no 'B'
        cols_no_B = 0
        for c in range(W):
            if not cols_with_B[c]:
                cols_no_B += 1
        
        # Result
        # Ensure indices are within bounds
        idx1 = components
        idx2 = cols_no_B
        
        # Safety check for array bounds
        if idx1 >= len(pow2):
            val1 = pow(2, idx1, MOD)
        else:
            val1 = pow2[idx1]
            
        if idx2 >= len(pow2):
            val2 = pow(2, idx2, MOD)
        else:
            val2 = pow2[idx2]
            
        ans = (val1 * val2) % MOD
        results.append(str(ans))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()