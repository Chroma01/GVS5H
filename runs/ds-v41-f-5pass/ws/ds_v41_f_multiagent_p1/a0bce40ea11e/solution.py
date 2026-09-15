import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    p = int(data[pos]); pos += 1
    A = []
    for _ in range(N):
        A.append([int(x) for x in data[pos:pos + N]])
        pos += N

    # ---- p == 2 special case -------------------------------------------
    # Entries are 0/1 and zeros must become 1, so B is the all-ones matrix,
    # B^2 mod 2 has every entry equal to N mod 2.
    if p == 2:
        v = N & 1
        line = ' '.join(str(v) for _ in range(N))
        sys.stdout.write((line + '\n') * N)
        return

    # ---- count zeros, build M (zeros kept as 0) -------------------------
    K = 0
    M = [[0] * N for _ in range(N)]
    for i in range(N):
        Ai = A[i]; Mi = M[i]
        for j in range(N):
            v = Ai[j]
            if v == 0:
                K += 1
            else:
                Mi[j] = v % p

    # ---- M^p mod p ------------------------------------------------------
    try:
        import numpy as np
    except Exception:
        np = None

    if np is not None:
        Mp = matpow_np(M, p, p, N, np)
    else:
        Mp = matpow_py(M, p, p, N)

    # ---- correction matrix C -------------------------------------------
    C = [[0] * N for _ in range(N)]
    for i in range(N):
        Ai = A[i]
        for j in range(N):
            if Ai[j] == 0:
                if i == j:
                    # zero self-loop used p-1 times -> row i and column i of M
                    Mi = M[i]
                    Ci = C[i]
                    for t in range(N):
                        Ci[t] += Mi[t]
                        C[t][i] += M[t][i]
                elif p == 3:
                    # non self-loop zero (i,j) used twice, glued by fixed (j,i)
                    C[i][j] += M[j][i]

    sign = 1 if (K & 1) == 0 else p - 1
    out = []
    for i in range(N):
        Mpi = Mp[i]; Ci = C[i]
        out.append(' '.join(str(((Mpi[j] + Ci[j]) % p) * sign % p)
                            for j in range(N)))
    sys.stdout.write('\n'.join(out) + '\n')


def matpow_py(M, e, p, N):
    def mul(A, B):
        C = [[0] * N for _ in range(N)]
        for i in range(N):
            Ai = A[i]; Ci = C[i]
            for k in range(N):
                a = Ai[k]
                if a:
                    Bk = B[k]
                    for j in range(N):
                        Ci[j] += a * Bk[j]
            for j in range(N):
                Ci[j] %= p
        return C

    res = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    base = [row[:] for row in M]
    while e:
        if e & 1:
            res = mul(res, base)
        e >>= 1
        if e:
            base = mul(base, base)
    return res


def matpow_np(M, e, p, N, np):
    c1 = 32768            # 2^15
    c2 = (1 << 30) % p

    def mul(A, B):
        # split each entry (< 2^30) into two 15-bit halves so the four
        # int64 products never overflow (max ~ N * 2^30 < 2^63).
        A0 = A & 32767
        A1 = A >> 15
        B0 = B & 32767
        B1 = B >> 15
        P00 = A0.dot(B0)
        P01 = A0.dot(B1)
        P10 = A1.dot(B0)
        P11 = A1.dot(B1)
        mid = (P01 + P10) % p
        res = P00 % p
        res = (res + (mid * c1) % p) % p
        res = (res + ((P11 % p) * c2) % p) % p
        return res

    base = np.array(M, dtype=np.int64)
    res = np.eye(N, dtype=np.int64)
    while e:
        if e & 1:
            res = mul(res, base)
        e >>= 1
        if e:
            base = mul(base, base)
    return res.tolist()


if __name__ == '__main__':
    main()