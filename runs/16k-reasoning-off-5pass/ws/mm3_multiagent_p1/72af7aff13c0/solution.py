import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

MOD = 998244353

def solve():
    H, W = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(H)]
    Q, sh, sw = map(int, input().split())
    sh -= 1; sw -= 1

    # If one dimension is 1, simple product
    if H == 1:
        out = []
        for _ in range(Q):
            d, a = input().split()
            a = int(a)
            if d == 'L': sw -= 1
            elif d == 'R': sw += 1
            elif d == 'U': sh -= 1
            else: sh += 1
            A[sh][sw] = a
            ans = 1
            for x in A[0]:
                ans = ans * x % MOD
            out.append(ans)
        print('\n'.join(map(str, out)))
        return
    if W == 1:
        out = []
        for _ in range(Q):
            d, a = input().split()
            a = int(a)
            if d == 'L': sw -= 1
            elif d == 'R': sw += 1
            elif d == 'U': sh -= 1
            else: sh += 1
            A[sh][sw] = a
            ans = 1
            for i in range(H):
                ans = ans * A[i][0] % MOD
            out.append(ans)
        print('\n'.join(map(str, out)))
        return

    # Ensure W is the smaller dimension to keep matrices small
    if W > H:
        H, W = W, H
        A = [list(row) for row in zip(*A)]
        sh, sw = sw, sh

    # DP via rows with segment tree of lower triangular matrices
    # Build row transformation matrix M_h (h from 1 to H-1)
    def build_matrix(row_above, row_curr):
        M = [[0] * W for _ in range(W)]
        for i in range(W):
            M[i][i] = row_above[i] % MOD
        for i in range(1, W):
            prod = 1
            for j in range(i-1, -1, -1):
                M[i][j] = row_above[j] * prod % MOD
                prod = prod * row_curr[j] % MOD
        return M

    def mat_mult(A_mat, B_mat):
        C = [[0] * W for _ in range(W)]
        for i in range(W):
            Ai = A_mat[i]
            Ci = C[i]
            for k in range(i+1):
                aik = Ai[k]
                if aik:
                    Bk = B_mat[k]
                    for j in range(k, W):
                        Ci[j] = (Ci[j] + aik * Bk[j]) % MOD
        return C

    def mat_vec(M, v):
        res = [0] * W
        for i in range(W):
            s = 0
            row = M[i]
            for j in range(i+1):
                s += row[j] * v[j]
            res[i] = s % MOD
        return res

    n = H - 1
    mats = [build_matrix(A[h-1], A[h]) for h in range(1, H)]

    size = 1
    while size < n:
        size <<= 1
    seg = [None] * (2 * size)
    for i in range(n):
        seg[size + i] = mats[i]
    for i in range(size - 1, 0, -1):
        seg[i] = mat_mult(seg[2*i], seg[2*i+1])

    out = []
    for _ in range(Q):
        d, a_str = input().split()
        a = int(a_str)
        if d == 'L': sw -= 1
        elif d == 'R': sw += 1
        elif d == 'U': sh -= 1
        else: sh += 1
        A[sh][sw] = a
        affected = []
        if sh > 0:
            affected.append(sh - 1)
        if sh < H - 1:
            affected.append(sh)
        for idx in affected:
            h = idx + 1
            mats[idx] = build_matrix(A[h-1], A[h])
            i = size + idx
            seg[i] = mats[idx]
            i >>= 1
            while i:
                seg[i] = mat_mult(seg[2*i], seg[2*i+1])
                i >>= 1
        v = [1] + [0] * (W-1)
        for m in mats:
            v = mat_vec(m, v)
        ans = v[W-1] * A[H-1][W-1] % MOD
        out.append(ans)

    print('\n'.join(map(str, out)))

solve()