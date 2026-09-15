import sys
from operator import mul as _mul

_IS_PYPY = sys.implementation.name == 'pypy'


def mat_mul_manual(A, B, mod):
    n = len(A)
    rng = range(n)
    mod_minus_1 = mod - 1
    C = [None] * n

    for i in rng:
        Ai = A[i]
        Ci = [0] * n
        for k, a in enumerate(Ai):
            if a:
                Bk = B[k]
                if a == 1:
                    for j in rng:
                        Ci[j] += Bk[j]
                elif a == mod_minus_1:
                    for j in rng:
                        Ci[j] -= Bk[j]
                else:
                    for j in rng:
                        Ci[j] += a * Bk[j]
        C[i] = [x % mod for x in Ci]

    return C


def mat_mul_dot(A, B, mod):
    Bt = list(zip(*B))
    mul = _mul
    return [[sum(map(mul, row, col)) % mod for col in Bt] for row in A]


def mat_mul(A, B, mod):
    if _IS_PYPY:
        return mat_mul_manual(A, B, mod)

    n = len(A)
    if n <= 32:
        return mat_mul_manual(A, B, mod)

    limit = (n * n) // 2
    nnz = 0
    for row in A:
        for x in row:
            if x:
                nnz += 1
                if nnz > limit:
                    return mat_mul_dot(A, B, mod)

    if nnz == 0:
        return [[0] * n for _ in range(n)]

    return mat_mul_manual(A, B, mod)


def mat_pow_py(A, e, mod):
    res = None
    base = A

    while e:
        if e & 1:
            if res is None:
                res = base
            else:
                res = mat_mul(res, base, mod)
        e >>= 1
        if e:
            base = mat_mul(base, base, mod)

    if res is None:
        n = len(A)
        res = [[0] * n for _ in range(n)]
        one = 1 % mod
        for i in range(n):
            res[i][i] = one

    return [row[:] for row in res]


def mat_mul_np(A, B, mod, np, block):
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.uint64)

    for s in range(0, n, block):
        e = min(n, s + block)
        partial = np.matmul(A[:, s:e], B[s:e, :])
        C += partial
        C %= mod

    return C


def mat_pow_np(A, e, mod, np, block):
    res = None
    base = A

    while e:
        if e & 1:
            if res is None:
                res = base
            else:
                res = mat_mul_np(res, base, mod, np, block)
        e >>= 1
        if e:
            base = mat_mul_np(base, base, mod, np, block)

    if res is None:
        n = A.shape[0]
        res = np.eye(n, dtype=np.uint64)
        if mod != 1:
            res %= mod

    return res


def compute_np_block(n, mod):
    max_prod = (mod - 1) * (mod - 1)
    if max_prod == 0:
        return n

    safe = (1 << 63) - 1
    b = (safe - mod) // max_prod
    if b < 1:
        b = 1
    if b > n:
        b = n
    return b


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, p = data[0], data[1]

    if p == 1:
        line = ' '.join(['0'] * N)
        sys.stdout.write('\n'.join([line] * N))
        return

    if p == 2:
        v = str(N & 1)
        line = ' '.join([v] * N)
        sys.stdout.write('\n'.join([line] * N))
        return

    vals = data[2:]
    A = [vals[i * N:(i + 1) * N] for i in range(N)]

    K = sum(row.count(0) for row in A)

    if K == N * N:
        line = ' '.join(['0'] * N)
        sys.stdout.write('\n'.join([line] * N))
        return

    P = None

    if N >= 30:
        try:
            import numpy as np
            A_np = np.array(A, dtype=np.uint64)
            block = compute_np_block(N, p)
            P_np = mat_pow_np(A_np, p, p, np, block)
            P = P_np.tolist()
        except Exception:
            P = None

    if P is None:
        P = mat_pow_py(A, p, p)

    for i in range(N):
        if A[i][i] == 0:
            for r in range(N):
                P[r][i] += A[r][i]
            for c in range(N):
                P[i][c] += A[i][c]

    if p == 3:
        for i in range(N):
            Pi = P[i]
            Ai = A[i]
            for j in range(N):
                if i != j and Ai[j] == 0:
                    v = A[j][i]
                    if v:
                        Pi[j] += v

    odd = K & 1
    out = []

    for i in range(N):
        row = P[i]
        if odd:
            row = [(-x) % p for x in row]
        else:
            row = [x % p for x in row]
        out.append(' '.join(map(str, row)))

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    solve()