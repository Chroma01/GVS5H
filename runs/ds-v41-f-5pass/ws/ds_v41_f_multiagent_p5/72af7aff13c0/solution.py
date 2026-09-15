import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    MOD = 998244353
    H = int(data[pos]); pos += 1
    W = int(data[pos]); pos += 1
    A = [[0]*W for _ in range(H)]
    for i in range(H):
        base = pos
        Ai = A[i]
        for j in range(W):
            Ai[j] = int(data[base+j])
        pos += W
    Q = int(data[pos]); pos += 1
    sh = int(data[pos]) - 1; pos += 1
    sw = int(data[pos]) - 1; pos += 1

    # Orient so that min(H,W) is the matrix dimension d (rows), max is L (columns).
    transposed = False
    if H > W:
        transposed = True
        A = [[A[i][j] for i in range(H)] for j in range(W)]
        H, W = W, H
        sh, sw = sw, sh

    d = H          # state vector size
    L = W          # number of leaves (columns)

    size = 1
    while size < L:
        size <<= 1
    mat = [None] * (2 * size)

    # leaf j : M_j[i][k] = prod_{t=k..i} A[t][j],  lower triangular
    for j in range(L):
        m = [0] * (d * d)
        for i in range(d):
            prod = 1
            bi = i * d
            for k in range(i, -1, -1):
                prod = prod * A[k][j] % MOD
                m[bi + k] = prod
        mat[size + j] = m
    # padding leaves = identity
    for j in range(L, size):
        m = [0] * (d * d)
        for i in range(d):
            m[i * d + i] = 1
        mat[size + j] = m

    # build : node = right_child * left_child
    for v in range(size - 1, 0, -1):
        R = mat[2 * v + 1]; Lm = mat[2 * v]
        C = [0] * (d * d)
        for i in range(d):
            Ri = i * d; Ci = i * d
            for k in range(i + 1):
                s = 0
                for t in range(k, i + 1):
                    s += R[Ri + t] * Lm[t * d + k]
                C[Ci + k] = s % MOD
        mat[v] = C

    mod = MOD
    ans = mat[1][(d - 1) * d]          # entry [d-1][0] = (root * e_1)[d-1]
    out = []

    for _ in range(Q):
        dc = data[pos]; pos += 1
        a = int(data[pos]); pos += 1
        if transposed:
            if dc == b'L': dc = 'U'
            elif dc == b'U': dc = 'L'
            elif dc == b'R': dc = 'D'
            else: dc = 'R'
        else:
            dc = dc.decode()
        if dc == 'L': sw -= 1
        elif dc == 'R': sw += 1
        elif dc == 'U': sh -= 1
        else: sh += 1

        h = sh; w = sw
        old = A[h][w]
        if old != a:
            A[h][w] = a
            delta = (a - old) % mod

            # rank-1 delta of leaf w
            u = [0] * d
            prod = 1
            for i in range(h, d):
                if i > h:
                    prod = prod * A[i][w] % mod
                u[i] = prod
            v = [0] * d
            prod = 1
            for k in range(h, -1, -1):
                if k < h:
                    prod = prod * A[k][w] % mod
                v[k] = prod * delta % mod

            leaf = size + w
            m = mat[leaf]
            for i in range(h, d):
                ui = u[i]
                bi = i * d
                for k in range(h + 1):
                    m[bi + k] = (m[bi + k] + ui * v[k]) % mod

            cur = leaf
            while cur > 1:
                parent = cur >> 1
                sib = cur ^ 1
                Sm = mat[sib]
                if (cur & 1) == 0:          # cur is left child -> sibling is right
                    up = [0] * d
                    for i in range(d):
                        s = 0
                        bi = i * d
                        for t in range(i + 1):
                            s += Sm[bi + t] * u[t]
                        up[i] = s % mod
                    vp = v
                else:                        # cur is right child -> sibling is left
                    up = u
                    vp = [0] * d
                    for k in range(d):
                        s = 0
                        for t in range(k, d):
                            s += Sm[t * d + k] * v[t]
                        vp[k] = s % mod
                Pm = mat[parent]
                for i in range(d):
                    ui = up[i]
                    if ui:
                        bi = i * d
                        for k in range(i + 1):
                            Pm[bi + k] = (Pm[bi + k] + ui * vp[k]) % mod
                cur = parent
                u = up
                v = vp

            ans = mat[1][(d - 1) * d] % mod
        out.append(ans)

    sys.stdout.write('\n'.join(map(str, out)))
    sys.stdout.write('\n')

main()