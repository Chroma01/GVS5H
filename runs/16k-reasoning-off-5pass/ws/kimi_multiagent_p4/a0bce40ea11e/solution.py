import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    p = int(data[idx]); idx += 1
    A = np.array([[int(data[idx + i * N + j]) for j in range(N)] for i in range(N)],
                 dtype=np.int64)

    if p == 2:
        # p-1 = 1 divides every multiplicity, so every walk survives and
        # T(c) = 1 for all c. There is exactly one B (zeros -> 1); answer is B^2 mod 2.
        B = np.where(A == 0, 1, A % 2).astype(np.int64)
        M = (B @ B) % 2
        out = "\n".join(" ".join(str(int(M[i, j])) for j in range(N)) for i in range(N))
        sys.stdout.write(out + "\n")
        return

    # Modular matrix multiplication mod p, entries < p <= 1e9 < 2^30.
    # Split left operand X = X0 + 2^15 * X1 with X0, X1 < 2^15.
    # X0@Y, X1@Y entries <= N * (2^15-1) * (p-1) <= 100*32767*1e9 < 3.3e15 < 2^63: safe.
    # Combination: (X1@Y % p) < p <= 1e9, times SHIFT_MOD < 2^15 gives < 3.3e13: safe.
    MASK = (1 << 15) - 1
    SHIFT_MOD = (1 << 15) % p

    def matmul(X, Y):
        X0 = X & MASK
        X1 = X >> 15
        return ((X0 @ Y) % p + ((X1 @ Y) % p) * SHIFT_MOD) % p

    def matpow(M, e):
        R = np.eye(N, dtype=np.int64) % p
        base = M % p
        while e > 0:
            if e & 1:
                R = matmul(R, base)
            e >>= 1
            if e:
                base = matmul(base, base)
        return R

    Amod = A % p
    M = matpow(Amod, p)

    # Corrections C1/C2: for each zero loop u (A[u,u] == 0),
    #   t = 1: fixed edge (i, u) gives walk i -> u -> (loop u)^(p-1): M[i,u] += A[i,u]
    #   t = p: fixed edge (u, j) gives walk (loop u)^(p-1) -> u -> j: M[u,j] += A[u,j]
    for u in range(N):
        if Amod[u, u] == 0:
            col = Amod[:, u]
            for i in range(N):
                if col[i] != 0:
                    M[i, u] += col[i]
            row = Amod[u]
            for j in range(N):
                if row[j] != 0:
                    M[u, j] += row[j]
    M %= p

    # Correction C3 (p = 3 only): zero edge (u,v) with fixed reverse edge (v,u)
    # gives walk u -> v -> u -> v: M[u,v] += A[v,u]. (u == v impossible since
    # A[v,u] != 0 then contradicts A[u,v] == 0.)
    if p == 3:
        for u in range(N):
            for v in range(N):
                if Amod[u, v] == 0 and Amod[v, u] != 0:
                    M[u, v] += Amod[v, u]
        M %= p

    # Global sign (-1)^K: each of the K zero entries contributes T(0) = p-1 == -1
    # when unused, T(p-1) == -1 when used.
    K = int(np.count_nonzero(Amod == 0))
    if K & 1:
        M = (-M) % p

    out = "\n".join(" ".join(str(int(M[i, j])) for j in range(N)) for i in range(N))
    sys.stdout.write(out + "\n")


main()