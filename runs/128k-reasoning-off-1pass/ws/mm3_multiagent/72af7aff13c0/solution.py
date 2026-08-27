import sys
import numpy as np

MOD = 998244353

def mat_mul(A, B, d):
    A_np = np.array(A, dtype=np.int64).reshape(d, d)
    B_np = np.array(B, dtype=np.int64).reshape(d, d)
    C_np = A_np @ B_np % MOD
    return C_np.flatten().tolist()

def solve():
    input = sys.stdin.readline
    H, W = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(H)]
    Q, sh, sw = map(int, input().split())
    sh -= 1
    sw -= 1
    
    moves = []
    for _ in range(Q):
        d, a = input().split()
        a = int(a)
        moves.append((d, a))
    
    if H <= W:
        d = H
        L = W
        transpose = False
    else:
        d = W
        L = H
        transpose = True
        A = [list(row) for row in zip(*A)]
        sh, sw = sw, sh
    
    size = 1
    while size < L:
        size *= 2
    
    tree = [None] * (2 * size)
    identity = [0] * (d * d)
    for k in range(d):
        identity[k * d + k] = 1
    
    def build_leaf(j):
        if transpose:
            col = [A[j][i] for i in range(d)]
        else:
            col = [A[i][j] for i in range(d)]
        prefix = [1] * (d + 1)
        for i in range(d):
            prefix[i+1] = prefix[i] * col[i] % MOD
        mat = [0] * (d * d)
        for i in range(d):
            for k in range(i + 1):
                mat[i * d + k] = prefix[i+1] * pow(prefix[k], MOD-2, MOD) % MOD
        return mat
    
    for j in range(L):
        tree[size + j] = build_leaf(j)
    for j in range(L, size):
        tree[size + j] = identity[:]
    
    for i in range(size - 1, 0, -1):
        left = tree[2*i]
        right = tree[2*i+1]
        if left is not None and right is not None:
            tree[i] = mat_mul(left, right, d)
        elif left is not None:
            tree[i] = left[:]
        elif right is not None:
            tree[i] = right[:]
        else:
            tree[i] = identity[:]
    
    v = [0] * d
    v[0] = 1
    
    output = []
    for move_char, a_val in moves:
        if move_char == 'L': sw -= 1
        elif move_char == 'R': sw += 1
        elif move_char == 'U': sh -= 1
        elif move_char == 'D': sh += 1
        
        if transpose:
            A[sw][sh] = a_val
        else:
            A[sh][sw] = a_val
        
        j = sw
        tree[size + j] = build_leaf(j)
        
        idx = (size + j) // 2
        while idx >= 1:
            left = tree[2*idx]
            right = tree[2*idx+1]
            if left is not None and right is not None:
                tree[idx] = mat_mul(left, right, d)
            elif left is not None:
                tree[idx] = left[:]
            elif right is not None:
                tree[idx] = right[:]
            else:
                tree[idx] = identity[:]
            idx //= 2
        
        root_mat = tree[1]
        new_v = [0] * d
        for i in range(d):
            for j in range(i + 1):
                new_v[i] = (new_v[i] + root_mat[i * d + j] * v[j]) % MOD
        
        output.append(str(new_v[-1]))
    
    sys.stdout.write('\n'.join(output) + '\n')

solve()