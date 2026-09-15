import sys
from operator import mul

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    p = int(data[pos]); pos += 1
    A = []
    for i in range(N):
        row = [int(x) for x in data[pos:pos + N]]
        pos += N
        A.append(row)

    # p == 2 is special: F_2^* = {1}, so sum over x of x^e = 1 for all e.
    if p == 2:
        B = [[(1 if A[i][j] == 0 else A[i][j]) & 1 for j in range(N)] for i in range(N)]
        res = [[0] * N for _ in range(N)]
        for i in range(N):
            Bi = B[i]; ri = res[i]
            for k in range(N):
                if Bi[k]:
                    Bk = B[k]
                    for j in range(N):
                        ri[j] ^= Bk[j]
        sys.stdout.write('\n'.join(' '.join(map(str, res[i])) for i in range(N)) + '\n')
        return

    K = sum(1 for i in range(N) for j in range(N) if A[i][j] == 0)

    # Correction terms C: walks using exactly one zero entry, p-1 times, plus one fixed edge.
    C = [[0] * N for _ in range(N)]
    for u in range(N):
        for v in range(N):
            if A[u][v] == 0:
                if u == v:
                    # zero self-loop at u: off-diagonal contributions only (diagonal cancels mod p)
                    for a in range(N):
                        if a != u and A[a][u]:
                            C[a][u] = (C[a][u] + A[a][u]) % p
                    for b in range(N):
                        if b != u and A[u][b]:
                            C[u][b] = (C[u][b] + A[u][b]) % p
                elif p == 3 and A[v][u]:
                    # zero edge (u,v), pattern z,f,z needs fixed edge (v,u)
                    C[u][v] = (C[u][v] + A[v][u]) % p

    F = [[A[i][j] % p for j in range(N)] for i in range(N)]

    try:
        import numpy as np
    except Exception:
        np = None

    if np is not None:
        def matmul(X, Y):
            Z = np.zeros((N, N), dtype=np.int64)
            for k in range(N):
                Z += np.outer(X[:, k], Y[k, :])
                Z %= p
            return Z
        R = np.eye(N, dtype=np.int64)
        base = np.array(F, dtype=np.int64)
        e = p
        while e:
            if e & 1:
                R = matmul(R, base)
            e >>= 1
            if e:
                base = matmul(base, base)
        P = R.tolist()
    else:
        def matmul(X, Y):
            Yt = list(zip(*Y))
            return [[sum(map(mul, xr, yc)) % p for yc in Yt] for xr in X]
        R = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
        base = [row[:] for row in F]
        e = p
        while e:
            if e & 1:
                R = matmul(R, base)
            e >>= 1
            if e:
                base = matmul(base, base)
        P = R

    sign = 1 if (K & 1) == 0 else (p - 1)
    out = []
    for i in range(N):
        out.append(' '.join(str((P[i][j] + C[i][j]) % p * sign % p) for j in range(N)))
    sys.stdout.write('\n'.join(out) + '\n')

main()