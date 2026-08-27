import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    p = int(data[idx]); idx += 1
    A = []
    for i in range(N):
        row = [int(x) % p for x in data[idx:idx+N]]
        idx += N
        A.append(row)

    # p = 2 special case: only filling is x=1, answer = B^2 mod 2
    if p == 2:
        B = [[1 if A[i][j] == 0 else A[i][j] for j in range(N)] for i in range(N)]
        C = [[0]*N for _ in range(N)]
        for i in range(N):
            Bi = B[i]
            Ci = C[i]
            for k in range(N):
                if Bi[k]:
                    Bk = B[k]
                    a = Bi[k]
                    for j in range(N):
                        Ci[j] = (Ci[j] + a * Bk[j]) & 1
        out = "\n".join(" ".join(map(str, row)) for row in C)
        sys.stdout.write(out + "\n")
        return

    # A' = A with zeros kept as 0 (already the case)
    Ap = A

    def matmul(X, Y):
        Z = [[0]*N for _ in range(N)]
        mod = p
        for i in range(N):
            Xi = X[i]
            Zi = Z[i]
            for k in range(N):
                a = Xi[k]
                if a:
                    Yk = Y[k]
                    for j in range(N):
                        Zi[j] = (Zi[j] + a * Yk[j]) % mod
        return Z

    def matpow(M, e):
        R = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
        base = M
        while e > 0:
            if e & 1:
                R = matmul(R, base)
            e >>= 1
            if e:
                base = matmul(base, base)
        return R

    P = matpow(Ap, p)

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

    ans = P
    mod = p

    # Diagonal zero at (u,u): add A'E_u + E_u A'
    # (A'E_u) has column u = column u of A'; (E_u A') has row u = row u of A'
    for u in diag_zeros:
        # add column u of Ap into column u of ans
        for i in range(N):
            ans[i][u] = (ans[i][u] + Ap[i][u]) % mod
        # add row u of Ap into row u of ans
        rowu = Ap[u]
        ansu = ans[u]
        for j in range(N):
            ansu[j] = (ansu[j] + rowu[j]) % mod

    # Off-diagonal zeros contribute only when p == 3: add A'[v][u] at (u,v)
    if p == 3:
        for (u, v) in offdiag_zeros:
            ans[u][v] = (ans[u][v] + Ap[v][u]) % mod

    # Global factor (-1)^K
    if K % 2 == 1:
        for i in range(N):
            for j in range(N):
                if ans[i][j]:
                    ans[i][j] = mod - ans[i][j]

    out = "\n".join(" ".join(map(str, row)) for row in ans)
    sys.stdout.write(out + "\n")

solve()