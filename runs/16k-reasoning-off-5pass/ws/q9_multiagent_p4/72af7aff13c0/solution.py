import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
        
        # Read grid A
        A = []
        for _ in range(H):
            row = []
            for _ in range(W):
                row.append(int(next(iterator)))
            A.append(row)
            
        Q = int(next(iterator))
        sh = int(next(iterator))
        sw = int(next(iterator))
        
        queries = []
        for _ in range(Q):
            d = next(iterator)
            a = int(next(iterator))
            queries.append((d, a))
            
    except StopIteration:
        return

    MOD = 998244353

    # Determine which dimension is smaller to optimize
    # We will treat the smaller dimension as the 'rows' (H) for our DP state vector
    # and the larger dimension as 'columns' (W) for the segment tree.
    # This ensures H <= sqrt(200000) approx 450.
    
    if H > W:
        # Swap H and W, and transpose the grid A
        # New H is old W, New W is old H
        # We need to transpose A: A[i][j] becomes A[j][i]
        new_A = [[0] * H for _ in range(W)]
        for r in range(H):
            for c in range(W):
                new_A[c][r] = A[r][c]
        A = new_A
        H, W = W, H
        
        # Also swap start position
        sh, sw = sw, sh
        
    # Now H is the smaller dimension (number of rows in our DP state)
    # W is the larger dimension (number of columns)
    
    # Precompute prefix products for each column to build the transition matrices
    # P[i][j] = product of A[0..i][j]
    # We need to handle zeros carefully. If P[i][j] is 0, we can't invert it.
    
    P = [[1] * W for _ in range(H)]
    invP = [[0] * W for _ in range(H)]
    
    def power(a, b, m):
        res = 1
        a %= m
        while b > 0:
            if b % 2 == 1:
                res = (res * a) % m
            a = (a * a) % m
            b //= 2
        return res

    def modInverse(n):
        return power(n, MOD - 2, MOD)

    for j in range(W):
        curr = 1
        for i in range(H):
            val = A[i][j]
            curr = (curr * val) % MOD
            P[i][j] = curr
            if curr != 0:
                invP[i][j] = modInverse(curr)
            else:
                invP[i][j] = 0
                
    # Matrix multiplication function optimized for sparse/upper triangular matrices
    def mat_mul_opt(A, B):
        C = [[0] * H for _ in range(H)]
        for i in range(H):
            for k in range(H):
                if A[i][k] == 0:
                    continue
                val = A[i][k]
                row_b = B[k]
                row_c = C[i]
                for j in range(H):
                    if row_b[j] != 0:
                        row_c[j] = (row_c[j] + val * row_b[j]) % MOD
        return C

    # Helper to get matrix for column j
    def get_mat(j):
        mat = [[0] * H for _ in range(H)]
        col_P = [P[i][j] for i in range(H)]
        col_invP = [invP[i][j] for i in range(H)]
        
        for i in range(H):
            if col_P[i] == 0:
                continue
            val = col_P[i]
            for k in range(i + 1):
                if col_invP[k] != 0:
                    mat[i][k] = (val * col_invP[k]) % MOD
        return mat

    # Segment Tree Implementation
    tree = [None] * (4 * W)
    
    def build(node, start, end):
        if start == end:
            tree[node] = get_mat(start)
            return
        mid = (start + end) // 2
        build(2 * node, start, mid)
        build(2 * node + 1, mid + 1, end)
        tree[node] = mat_mul_opt(tree[2 * node], tree[2 * node + 1])

    def update(node, start, end, idx, new_mat):
        if start == end:
            tree[node] = new_mat
            return
        mid = (start + end) // 2
        if idx <= mid:
            update(2 * node, start, mid, idx, new_mat)
        else:
            update(2 * node + 1, mid + 1, end, idx, new_mat)
        tree[node] = mat_mul_opt(tree[2 * node], tree[2 * node + 1])

    if W > 0:
        build(1, 0, W - 1)
    else:
        # Should not happen based on constraints (H, W >= 2)
        pass
        
    results = []
    
    # Current position tracking
    cur_h, cur_w = sh, sw
    
    for d, a in queries:
        # Move
        if d == 'L':
            cur_w -= 1
        elif d == 'R':
            cur_w += 1
        elif d == 'U':
            cur_h -= 1
        elif d == 'D':
            cur_h += 1
            
        # Update A
        A[cur_h][cur_w] = a
        
        # Update P and invP for column cur_w
        col = cur_w
        curr = 1
        for i in range(H):
            val = A[i][col]
            curr = (curr * val) % MOD
            P[i][col] = curr
            if curr != 0:
                invP[i][col] = modInverse(curr)
            else:
                invP[i][col] = 0
                
        # Recompute M_col
        new_mat = get_mat(col)
        
        # Update segment tree
        update(1, 0, W - 1, col, new_mat)
        
        # The answer is the last element of the first column of the total product matrix.
        # Total product = M_{W-1} * ... * M_0
        # We stored this in tree[1].
        # We need tree[1][H-1][0] because V_{-1} = [1, 0, ..., 0]^T.
        
        ans = tree[1][H-1][0]
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()