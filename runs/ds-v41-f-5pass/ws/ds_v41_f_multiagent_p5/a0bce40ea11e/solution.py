import sys
from operator import mul


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    p = int(data[pos]); pos += 1
    A = []
    for _ in range(N):
        A.append([int(data[pos + j]) for j in range(N)])
        pos += N

    # p = 2 special case: zeros replaced by 1 -> B is the all-ones matrix.
    # answer = J^2 mod 2 = (N mod 2) * J
    if p == 2:
        val = N % 2
        sys.stdout.write('\n'.join(' '.join([str(val)] * N) for _ in range(N)))
        return

    # ---- matrix exponentiation M^p mod p (M = A, zeros kept as 0) ----
    try:
        import numpy as np
        use_np = True
    except Exception:
        use_np = False

    half = 1 << 15
    mask = half - 1
    h2 = (half * half) % p
    hm = half % p

    if use_np:
        def matmul(X, Y):
            X0 = X & mask; X1 = X >> 15
            Y0 = Y & mask; Y1 = Y >> 15
            P00 = X0.dot(Y0)
            P01 = X0.dot(Y1)
            P10 = X1.dot(Y0)
            P11 = X1.dot(Y1)
            return ((P11 % p) * h2 + ((P01 + P10) % p) * hm + (P00 % p)) % p

        base = np.array(A, dtype=np.int64) % p
        result = np.zeros((N, N), dtype=np.int64)
        for i in range(N):
            result[i, i] = 1 % p
    else:
        def matmul(X, Y):
            Yt = list(zip(*Y))
            return [[sum(map(mul, Xi, Yj)) % p for Yj in Yt] for Xi in X]

        base = [[A[i][j] % p for j in range(N)] for i in range(N)]
        result = [[1 % p if i == j else 0 for j in range(N)] for i in range(N)]

    e = p
    while e > 0:
        if e & 1:
            result = matmul(result, base)
        e >>= 1
        if e:
            base = matmul(base, base)

    P = result.tolist() if use_np else result

    # ---- corrections: walks using exactly one zero edge p-1 times + one fixed edge ----
    C = [[0] * N for _ in range(N)]
    K = 0
    for a in range(N):
        Aa = A[a]
        for b in range(N):
            if Aa[b] == 0:
                K += 1
                if a == b:
                    # self-loop zero: nonzero edge at start or at end
                    for c in range(N):
                        v = A[c][a]
                        if v:
                            C[c][a] = (C[c][a] + v) % p
                    for d in range(N):
                        v = Aa[d]
                        if v:
                            C[a][d] = (C[a][d] + v) % p
                elif p == 3:
                    # non self-loop zero, only possible when p == 3
                    v = A[b][a]
                    if v:
                        C[a][b] = (C[a][b] + v) % p

    sign = (p - 1) if (K & 1) else 1
    out = []
    for i in range(N):
        Pi = P[i]; Ci = C[i]
        out.append(' '.join(str((sign * ((Pi[j] + Ci[j]) % p)) % p) for j in range(N)))
    sys.stdout.write('\n'.join(out))


main()