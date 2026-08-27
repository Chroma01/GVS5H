import sys
import numpy as np


def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    p = int(data[idx]); idx += 1
    A = [[int(data[idx + i * N + j]) % p for j in range(N)] for i in range(N)]
    idx += N * N

    if p == 2:
        # Only filling value is 1; answer is B^2 mod 2 with zeros -> 1
        B = [[1 if A[i][j] == 0 else A[i][j] for j in range(N)] for i in range(N)]
        C = [[0] * N for _ in range(N)]
        for i in range(N):
            Bi = B[i]
            Ci = C[i]
            for k in range(N):
                if Bi[k]:
                    Bk = B[k]
                    for j in range(N):
                        Ci[j] ^= Bi[k] & Bk[j]
        out = "\n".join(" ".join(map(str, row)) for row in C)
        sys.stdout.write(out + "\n")
        return

    # Count zeros
    K = sum(1 for i in range(N) for j in range(N) if A[i][j] == 0)
    S = (p - 1) if (K & 1) else 1  # (-1)^K mod p

    # Build correction matrix M
    M = [[0] * N for _ in range(N)]
    for s in range(N):
        if A[s][s] == 0:
            # diagonal zero cell (s,s)
            for i in range(N):
                M[i][s] += A[i][s]
            for j in range(N):
                M[s][j] += A[s][j]
            M[s][s] += (p - 2) * A[s][s]
    if p == 3:
        for s in range(N):
            for t in range(N):
                if s != t and A[s][t] == 0:
                    M[s][t] += A[t][s]
    for i in range(N):
        for j in range(N):
            M[i][j] %= p

    # Compute A^p mod p with numpy float64 split matmul (15-bit halves)
    MASK = (1 << 15) - 1
    SHIFT2 = (1 << 30) % p
    SHIFT1 = (1 << 15) % p

    def matmul(X, Y):
        Xh = (X >> 15).astype(np.float64)
        Xl = (X & MASK).astype(np.float64)
        Yh = (Y >> 15).astype(np.float64)
        Yl = (Y & MASK).astype(np.float64)
        hh = np.matmul(Xh, Yh).astype(np.int64) % p
        hl = np.matmul(Xh, Yl).astype(np.int64)
        lh = np.matmul(Xl, Yh).astype(np.int64)
        mid = (hl + lh) % p
        ll = np.matmul(Xl, Yl).astype(np.int64) % p
        return (hh * SHIFT2 + mid * SHIFT1 + ll) % p

    Anp = np.array(A, dtype=np.int64)
    result = np.identity(N, dtype=np.int64)
    base = Anp
    e = p
    while e > 0:
        if e & 1:
            result = matmul(result, base)
        e >>= 1
        if e:
            base = matmul(base, base)

    Mnp = np.array(M, dtype=np.int64)
    ans = (result + (S * Mnp) % p) % p

    out = "\n".join(" ".join(str(int(x)) for x in row) for row in ans)
    sys.stdout.write(out + "\n")


solve()