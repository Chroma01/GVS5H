import sys


def mat_mul(A, B, mod):
    n = len(A)
    C = [None] * n
    rng = range(n)
    enum = enumerate
    any_ = any
    neg = mod - 1

    for i in rng:
        Ai = A[i]
        if not any_(Ai):
            C[i] = [0] * n
            continue

        Ci = [0] * n
        for k in rng:
            a = Ai[k]
            if a:
                Bk = B[k]
                if a == 1:
                    for j, b in enum(Bk):
                        Ci[j] += b
                elif a == neg:
                    for j, b in enum(Bk):
                        Ci[j] -= b
                else:
                    for j, b in enum(Bk):
                        Ci[j] += a * b

        C[i] = [x % mod for x in Ci]

    return C


def mat_pow(A, p, mod):
    n = len(A)
    any_ = any

    base = mat_mul(A, A, mod)
    if not any_(any_(row) for row in base):
        return [[0] * n for _ in range(n)]

    exp = (p - 1) // 2
    result = A

    while exp:
        if exp & 1:
            result = mat_mul(result, base, mod)
            if not any_(any_(row) for row in result):
                return [[0] * n for _ in range(n)]

        exp >>= 1
        if exp:
            base = mat_mul(base, base, mod)
            if not any_(any_(row) for row in base):
                return [[0] * n for _ in range(n)]

    return result


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    p = data[1]

    if p == 1:
        line = ' '.join(['0'] * N)
        sys.stdout.write('\n'.join([line] * N))
        return

    vals = data[2:]

    if p == 2:
        v = N & 1
        line = ' '.join([str(v)] * N)
        sys.stdout.write('\n'.join([line] * N))
        return

    A = [vals[i * N:(i + 1) * N] for i in range(N)]

    K = 0
    for row in A:
        K += row.count(0)

    if K == N * N:
        line = ' '.join(['0'] * N)
        sys.stdout.write('\n'.join([line] * N))
        return

    R = mat_pow(A, p, p)

    for i in range(N):
        if A[i][i] == 0:
            Ai = A[i]
            Ri = R[i]
            for j in range(N):
                Ri[j] += Ai[j]
            for r in range(N):
                R[r][i] += A[r][i]

    if p == 3:
        for i in range(N):
            Ai = A[i]
            Ri = R[i]
            for j in range(N):
                if i != j and Ai[j] == 0:
                    Ri[j] += A[j][i]

    if K & 1:
        neg = p - 1
        R = [[(x * neg) % p for x in row] for row in R]
    else:
        R = [[x % p for x in row] for row in R]

    out = [' '.join(map(str, row)) for row in R]
    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    solve()