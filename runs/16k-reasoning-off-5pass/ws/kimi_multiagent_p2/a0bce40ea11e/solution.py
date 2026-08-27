import sys
import numpy as np

def solve():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    p = int(data[pos]); pos += 1
    A = [[int(data[pos + i * N + j]) % p for j in range(N)] for i in range(N)]
    pos += N * N

    if p == 2:
        # Every walk survives; B is forced to be all-ones; B^2 = N * ones.
        v = N % 2
        row = ' '.join([str(v)] * N)
        sys.stdout.write('\n'.join([row] * N) + '\n')
        return

    M = np.array(A, dtype=np.int64)

    def matmul(X, Y):
        # chunked inner dimension to avoid int64 overflow:
        # each partial sum < 8 * (p-1)^2 < 8e18 < int64 max (~9.22e18)
        Z = np.zeros((N, N), dtype=np.int64)
        for k in range(0, N, 8):
            Z += X[:, k:k + 8] @ Y[k:k + 8, :]
            Z %= p
        return Z

    # T = A^p mod p (zeros stay zero -> all-fixed walks)
    R = np.eye(N, dtype=np.int64)
    base = M.copy()
    e = p
    while e:
        if e & 1:
            R = matmul(R, base)
        base = matmul(base, base)
        e >>= 1
    T = R

    K = 0
    diag_zeros = []
    offdiag_zeros = []
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                K += 1
                if i == j:
                    diag_zeros.append(i)
                else:
                    offdiag_zeros.append((i, j))

    # Corrections: walks using exactly one variable with multiplicity p-1
    # plus one fixed edge, contributing (+fixed weight) inside (-1)^K factor.
    for u in diag_zeros:
        for i in range(N):
            if A[i][u]:
                T[i, u] = (T[i, u] + A[i][u]) % p
        for j in range(N):
            if A[u][j]:
                T[u, j] = (T[u, j] + A[u][j]) % p

    if p == 3:
        # walk u->v->u->v using variable (u,v) twice and fixed edge v->u
        for (u, v) in offdiag_zeros:
            if A[v][u]:
                T[u, v] = (T[u, v] + A[v][u]) % p

    if K % 2 == 1:
        T = (p - T) % p

    out_lines = []
    for i in range(N):
        out_lines.append(' '.join(str(int(x) % p) for x in T[i]))
    sys.stdout.write('\n'.join(out_lines) + '\n')

solve()