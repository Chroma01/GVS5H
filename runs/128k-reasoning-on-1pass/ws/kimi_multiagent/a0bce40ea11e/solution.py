import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); p = int(data[1])
    A = [list(map(int, data[2 + i * N: 2 + (i + 1) * N])) for i in range(N)]

    # p = 2: the only nonzero residue is 1, so B is the all-ones matrix J,
    # and B^2 = N * J. Answer is (N mod 2) in every cell.
    if p == 2:
        r = str(N & 1)
        line = " ".join([r] * N)
        sys.stdout.write("\n".join([line] * N) + "\n")
        return

    K = sum(row.count(0) for row in A)

    # ---- Compute P = F^p mod p, where F = A with zeros kept as 0 ----
    try:
        import numpy as np
    except ImportError:
        np = None

    if np is not None:
        F = np.array(A, dtype=np.int64)

        def matmul(X, Y):
            # Blocked over the inner dimension in chunks of 4:
            # each partial sum <= 4*(p-1)^2 < 2^63, no int64 overflow.
            acc = np.zeros((N, N), dtype=np.int64)
            for s in range(0, N, 4):
                acc += X[:, s:s + 4] @ Y[s:s + 4, :]
                acc %= p
            return acc

        R = np.eye(N, dtype=np.int64)
        base = F
        e = p
        while e:
            if e & 1:
                R = matmul(R, base)
            e >>= 1
            if e:
                base = matmul(base, base)
        P = R.tolist()
    else:
        n = N
        mod = p

        def matmul(X, Y):
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                Xi = X[i]; Ci = C[i]
                for k in range(n):
                    x = Xi[k]
                    if x:
                        Yk = Y[k]
                        for j in range(n):
                            Ci[j] += x * Yk[j]
                for j in range(n):
                    Ci[j] %= mod
            return C

        R = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        base = [row[:] for row in A]
        e = p
        while e:
            if e & 1:
                R = matmul(R, base)
            e >>= 1
            if e:
                base = matmul(base, base)
        P = R

    # ---- Correction matrix C ----
    # Walks using exactly one zero edge e exactly p-1 times plus one fixed edge.
    # For odd p this forces e to be a diagonal zero loop (a,a), with the fixed
    # edge entering (F D) or leaving (D F). For p = 3, an off-diagonal zero
    # edge (a,b) can appear twice as a->b->a->b when (b,a) is fixed.
    C = [[0] * N for _ in range(N)]
    for a in range(N):
        if A[a][a] == 0:
            for i in range(N):
                C[i][a] += A[i][a]   # column a of F  (F D)
                C[a][i] += A[a][i]   # row a of F     (D F)
    if p == 3:
        for a in range(N):
            Aa = A[a]
            for b in range(N):
                if a != b and Aa[b] == 0:
                    C[a][b] += A[b][a]

    # ---- Answer = (-1)^K * (F^p + C) mod p ----
    neg = K & 1
    out = []
    for i in range(N):
        Pi = P[i]; Ci = C[i]
        row = []
        for j in range(N):
            v = (Pi[j] + Ci[j]) % p
            if neg and v:
                v = p - v
            row.append(str(v))
        out.append(" ".join(row))
    sys.stdout.write("\n".join(out) + "\n")

main()