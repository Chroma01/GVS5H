import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    p = int(next(it))
    A = [[int(next(it)) for _ in range(N)] for _ in range(N)]
    K = sum(1 for i in range(N) for j in range(N) if A[i][j] == 0)

    if p == 2:
        val = N % 2
        out = '\n'.join(' '.join([str(val)] * N) for _ in range(N))
        sys.stdout.write(out)
        return

    # p > 2
    A0 = [[A[i][j] % p for j in range(N)] for i in range(N)]

    # Compute C = A0^p mod p
    try:
        import numpy as np

        def matmul_np(X, Y):
            n = X.shape[0]
            C = np.zeros((n, n), dtype=np.int64)
            L = 8
            for k in range(0, n, L):
                end = min(k + L, n)
                C += X[:, k:end] @ Y[k:end, :]
                C %= p
            return C

        n = N
        res = np.eye(n, dtype=np.int64)
        base = np.array(A0, dtype=np.int64)
        e = p
        while e > 0:
            if e & 1:
                res = matmul_np(res, base)
            e >>= 1
            if e:
                base = matmul_np(base, base)
        C = res.tolist()
    except ImportError:
        def matmul(X, Y):
            n = len(X)
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                Xi = X[i]
                Ci = C[i]
                for k in range(n):
                    aik = Xi[k]
                    if aik:
                        Yk = Y[k]
                        for j in range(n):
                            Ci[j] += aik * Yk[j]
                for j in range(n):
                    Ci[j] %= p
            return C

        n = N
        res = [[0] * n for _ in range(n)]
        for i in range(n):
            res[i][i] = 1
        base = [row[:] for row in A0]
        e = p
        while e > 0:
            if e & 1:
                res = matmul(res, base)
            e >>= 1
            if e:
                base = matmul(base, base)
        C = res

    # Build T
    T = [[0] * N for _ in range(N)]

    # Diagonal zero entries (all p > 2)
    for u in range(N):
        if A0[u][u] == 0:
            for b in range(N):
                T[u][b] = (T[u][b] + A0[u][b]) % p
            for a in range(N):
                T[a][u] = (T[a][u] + A0[a][u]) % p

    # Off-diagonal zero entries only for p == 3
    if p == 3:
        for u in range(N):
            for v in range(N):
                if u != v and A0[u][v] == 0:
                    T[u][v] = (T[u][v] + A0[v][u]) % p

    sign = pow(p - 1, K, p)  # (-1)^K mod p
    out_lines = []
    for i in range(N):
        row = []
        for j in range(N):
            val = (C[i][j] + T[i][j]) % p
            val = (val * sign) % p
            row.append(str(val))
        out_lines.append(' '.join(row))
    sys.stdout.write('\n'.join(out_lines))


if __name__ == "__main__":
    solve()