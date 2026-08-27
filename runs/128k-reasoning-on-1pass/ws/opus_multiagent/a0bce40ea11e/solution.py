import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    p = int(data[idx]); idx += 1
    A = [[int(data[idx + i * n + j]) for j in range(n)] for i in range(n)]
    idx += n * n

    K = sum(1 for i in range(n) for j in range(n) if A[i][j] == 0)

    out = []

    if p == 2:
        # only one B: all zeros replaced by 1
        M = [[(1 if A[i][j] == 0 else A[i][j] % 2) for j in range(n)] for i in range(n)]
        # compute M*M mod 2
        try:
            import numpy as np
            Mn = np.array(M, dtype=np.int64)
            R = (Mn @ Mn) % 2
            for i in range(n):
                out.append(' '.join(map(str, R[i].tolist())))
        except Exception:
            R = [[0] * n for _ in range(n)]
            for i in range(n):
                Mi = M[i]
                acc = [0] * n
                for k in range(n):
                    v = Mi[k]
                    if v:
                        Mk = M[k]
                        for j in range(n):
                            acc[j] += v * Mk[j]
                R[i] = [x % 2 for x in acc]
            for i in range(n):
                out.append(' '.join(map(str, R[i])))
        sys.stdout.write('\n'.join(out) + '\n')
        return

    # p >= 3
    use_numpy = True
    try:
        import numpy as np
    except Exception:
        use_numpy = False

    if use_numpy:
        An = np.array(A, dtype=np.int64) % p

        def mul(X, Y):
            Xh = X >> 15
            Xl = X & 32767
            return ((((Xh @ Y) % p) << 15) + (Xl @ Y)) % p

        # matrix power A^p mod p
        e = p
        Rm = np.eye(n, dtype=np.int64) % p
        Base = An.copy()
        while e > 0:
            if e & 1:
                Rm = mul(Rm, Base)
            e >>= 1
            if e:
                Base = mul(Base, Base)

        R = Rm.astype(object) if False else Rm.copy()
        # corrections
        C = np.zeros((n, n), dtype=np.int64)
        for a in range(n):
            if A[a][a] == 0:
                # first step i->a then p-1 loops : entry (i,a) += A[i][a]
                C[:, a] = (C[:, a] + An[:, a]) % p
                # loops then a->j : entry (a,j) += A[a][j]
                C[a, :] = (C[a, :] + An[a, :]) % p
        if p == 3:
            for a in range(n):
                for b in range(n):
                    if a != b and A[a][b] == 0:
                        C[a][b] = (C[a][b] + An[b][a]) % p
        R = (R + C) % p
        if K & 1:
            R = (-R) % p
        R = R % p
        for i in range(n):
            out.append(' '.join(map(str, R[i].tolist())))
        sys.stdout.write('\n'.join(out) + '\n')
        return

    # pure python fallback
    Am = [[A[i][j] % p for j in range(n)] for i in range(n)]

    def mul(X, Y):
        res = []
        for i in range(n):
            Xi = X[i]
            acc = [0] * n
            for k in range(n):
                v = Xi[k]
                if v:
                    Yk = Y[k]
                    for j in range(n):
                        acc[j] += v * Yk[j]
            res.append([x % p for x in acc])
        return res

    e = p
    Rm = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    Base = [row[:] for row in Am]
    while e > 0:
        if e & 1:
            Rm = mul(Rm, Base)
        e >>= 1
        if e:
            Base = mul(Base, Base)

    C = [[0] * n for _ in range(n)]
    for a in range(n):
        if A[a][a] == 0:
            for i in range(n):
                C[i][a] = (C[i][a] + Am[i][a]) % p
            for j in range(n):
                C[a][j] = (C[a][j] + Am[a][j]) % p
    if p == 3:
        for a in range(n):
            for b in range(n):
                if a != b and A[a][b] == 0:
                    C[a][b] = (C[a][b] + Am[b][a]) % p

    sign = -1 if (K & 1) else 1
    for i in range(n):
        row = [(sign * ((Rm[i][j] + C[i][j]) % p)) % p for j in range(n)]
        out.append(' '.join(map(str, row)))
    sys.stdout.write('\n'.join(out) + '\n')


main()