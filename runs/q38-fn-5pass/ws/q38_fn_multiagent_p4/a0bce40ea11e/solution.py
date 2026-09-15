import sys

if sys.implementation.name == 'cpython':
    from operator import mul

    def matmul(X, Y, mod):
        YT = list(zip(*Y))
        mul_local = mul
        sum_local = sum
        Z = []
        for row in X:
            Z.append([sum_local(map(mul_local, row, col)) % mod for col in YT])
        return Z
else:
    def matmul(X, Y, mod):
        n = len(X)
        rng = range(n)
        Z = []
        for i in rng:
            Xi = X[i]
            Zi = [0] * n
            for k in rng:
                x = Xi[k]
                if x:
                    Yk = Y[k]
                    for j in rng:
                        Zi[j] += x * Yk[j]
            Z.append([v % mod for v in Zi])
        return Z


def mat_pow(A, exp, mod):
    if exp == 1:
        return [row[:] for row in A]

    res = [row[:] for row in A]
    e = exp >> 1
    base = matmul(A, A, mod)

    while e:
        if e & 1:
            res = matmul(res, base, mod)
        e >>= 1
        if e:
            base = matmul(base, base, mod)

    return res


def matmul_np(A, B, mod, np, block):
    n = A.shape[0]
    C = np.zeros((n, n), dtype=np.int64)
    for k in range(0, n, block):
        C += A[:, k:k + block].dot(B[k:k + block, :])
        C %= mod
    return C


def mat_pow_np(A, exp, mod, np):
    n = len(A)
    arr = np.array(A, dtype=np.int64)

    if exp == 1:
        return arr.tolist()

    max_prod = (mod - 1) * (mod - 1)
    block = 8_000_000_000_000_000_000 // max_prod
    if block < 1:
        block = 1
    if block > n:
        block = n

    res = arr.copy()
    e = exp >> 1
    base = matmul_np(arr, arr, mod, np, block)

    while e:
        if e & 1:
            res = matmul_np(res, base, mod, np, block)
        e >>= 1
        if e:
            base = matmul_np(base, base, mod, np, block)

    return res.tolist()


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
        val = N & 1
        line = ' '.join([str(val)] * N)
        sys.stdout.write('\n'.join([line] * N))
        return

    vals = data[2:]
    A = []
    zeros = []
    idx = 0

    for i in range(N):
        row = vals[idx:idx + N]
        idx += N
        A.append(row)
        for j, x in enumerate(row):
            if x == 0:
                zeros.append((i, j))

    if N == 1:
        sys.stdout.write(str(A[0][0] % p) + '\n')
        return

    np = None
    if N >= 30 and p > 1000:
        try:
            import numpy as np
        except Exception:
            np = None

    if np is not None:
        ans = mat_pow_np(A, p, p, np)
    else:
        ans = mat_pow(A, p, p)

    if p == 3:
        for r, c in zeros:
            if r == c:
                for i in range(N):
                    ans[i][r] += A[i][r]
                    ans[r][i] += A[r][i]
            else:
                ans[r][c] += A[c][r]
    else:
        for r, c in zeros:
            if r == c:
                for i in range(N):
                    ans[i][r] += A[i][r]
                    ans[r][i] += A[r][i]

    if len(zeros) & 1:
        for i in range(N):
            ans[i] = [(-x) % p for x in ans[i]]
    else:
        for i in range(N):
            ans[i] = [x % p for x in ans[i]]

    out = [' '.join(map(str, row)) for row in ans]
    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    solve()