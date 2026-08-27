import sys

def solve():
    sys.setrecursionlimit(1 << 25)
    MOD = 998244353
    
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    H_orig = int(next(it))
    W_orig = int(next(it))
    A_orig = [[0] * (W_orig + 1) for _ in range(H_orig + 1)]
    for i in range(1, H_orig + 1):
        for j in range(1, W_orig + 1):
            A_orig[i][j] = int(next(it))
    Q = int(next(it))
    sh_orig = int(next(it))
    sw_orig = int(next(it))
    
    # Transpose if H > W to ensure H <= W, reducing the matrix size.
    if H_orig > W_orig:
        H, W = W_orig, H_orig
        A = [[0] * (W + 1) for _ in range(H + 1)]
        for i in range(1, H + 1):
            for j in range(1, W + 1):
                A[i][j] = A_orig[j][i]
        transposed = True
        sh, sw = sw_orig, sh_orig
    else:
        H, W = H_orig, W_orig
        A = A_orig
        transposed = False
        sh, sw = sh_orig, sw_orig
    
    # H <= W, H*W <= 200000, so H <= 447.
    # Build segment tree over columns.
    # Each node stores a vector v of length H, where v[i] = product of A[1..i+1][col] for the segment.
    # The matrix is determined by this first column, and the product of two matrices can be computed in O(H) time.
    
    # Precompute prefix products for each column.
    P = [[0] * (H + 1) for _ in range(W)]
    for j in range(1, W + 1):
        P[j-1][0] = 1
        for i in range(1, H + 1):
            P[j-1][i] = P[j-1][i-1] * A[i][j] % MOD
    
    # Build segment tree.
    size = 1
    while size < W:
        size <<= 1
    tree = [0] * (2 * size * H)
    
    def set_leaf(node, col):
        base = node * H
        vec = P[col-1]
        for i in range(H):
            tree[base + i] = vec[i+1]
    
    # Build leaves
    for i in range(W):
        set_leaf(size + i, i+1)
    
    # Build internal nodes
    for i in range(size - 1, 0, -1):
        left = 2 * i
        right = 2 * i + 1
        base = i * H
        left_base = left * H
        right_base = right * H
        sum_val = tree[left_base]
        for ii in range(H):
            v_right_i = tree[right_base + ii]
            tree[base + ii] = v_right_i * sum_val % MOD
            if ii < H - 1:
                inv = pow(v_right_i, MOD-2, MOD)
                sum_val = (sum_val + tree[left_base + ii + 1] * inv) % MOD
    
    def pull(i):
        left = 2 * i
        right = 2 * i + 1
        base = i * H
        left_base = left * H
        right_base = right * H
        sum_val = tree[left_base]
        for ii in range(H):
            v_right_i = tree[right_base + ii]
            tree[base + ii] = v_right_i * sum_val % MOD
            if ii < H - 1:
                inv = pow(v_right_i, MOD-2, MOD)
                sum_val = (sum_val + tree[left_base + ii + 1] * inv) % MOD
    
    # Process updates
    out = []
    for _ in range(Q):
        d = next(it).decode()
        a_val = int(next(it))
        if transposed:
            if d == 'U': d = 'L'
            elif d == 'D': d = 'R'
            elif d == 'L': d = 'U'
            elif d == 'R': d = 'D'
        if d == 'L': sw -= 1
        elif d == 'R': sw += 1
        elif d == 'U': sh -= 1
        elif d == 'D': sh += 1
        x, y = sh, sw
        # Update A[x][y]
        A[x][y] = a_val
        # Update prefix products for column y
        col = y - 1
        P[col][0] = 1
        for i in range(1, H + 1):
            P[col][i] = P[col][i-1] * A[i][y] % MOD
        # Update the leaf node
        leaf = size + col
        base = leaf * H
        vec = P[col]
        for i in range(H):
            tree[base + i] = vec[i+1]
        # Recompute up the tree
        i = leaf // 2
        while i >= 1:
            pull(i)
            i //= 2
        # The answer is the last element of the root's vector
        root_vec_base = H  # node 1, base = 1 * H = H
        out.append(str(tree[root_vec_base + H - 1]))
    sys.stdout.write('\n'.join(out))

if __name__ == "__main__":
    solve()