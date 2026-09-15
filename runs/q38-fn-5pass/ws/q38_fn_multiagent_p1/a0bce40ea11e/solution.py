import sys

def mat_mul_loop(X, Y, mod):
    n = len(X)
    rng = range(n)
    Z = [[0] * n for _ in rng]
    for i in rng:
        Xi = X[i]
        Zi = Z[i]
        for k in rng:
            x = Xi[k]
            if x:
                Yk = Y[k]
                for j in rng:
                    Zi[j] += x * Yk[j]
        for j in rng:
            Zi[j] %= mod
    return Z

def mat_mul_comp(X, Y, mod):
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
                Zi = [z + x * y for z, y in zip(Zi, Yk)]
        Z.append([z % mod for z in Zi])
    return Z

_impl = getattr(sys, 'implementation', None)
if _impl is not None and _impl.name == 'pypy':
    mat_mul = mat_mul_loop
else:
    mat_mul = mat_mul_comp

def mat_pow(A, e, mod):
    n = len(A)
    mul = mat_mul
    res = None
    base = A
    while e:
        if e & 1:
            if res is None:
                res = base
            else:
                res = mul(res, base, mod)
        e >>= 1
        if e:
            base = mul(base, base, mod)
    if res is None:
        res = [[0] * n for _ in range(n)]
        for i in range(n):
            res[i][i] = 1
    elif res is A:
        res = [row[:] for row in res]
    return res

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    p = int(data[1])

    if p == 1:
        line = ' '.join(['0'] * n)
        sys.stdout.write('\n'.join([line] * n))
        return

    if p == 2:
        val = str(n & 1)
        line = ' '.join([val] * n)
        sys.stdout.write('\n'.join([line] * n))
        return

    if n == 1:
        a = int(data[2]) % p if len(data) > 2 else 0
        sys.stdout.write(str(pow(a, p, p)))
        return

    A = []
    zeros = []
    idx = 2
    for i in range(n):
        row = [0] * n
        for j in range(n):
            v = int(data[idx])
            idx += 1
            row[j] = v
            if v == 0:
                zeros.append((i, j))
        A.append(row)

    if len(zeros) == n * n:
        line = ' '.join(['0'] * n)
        sys.stdout.write('\n'.join([line] * n))
        return

    P = mat_pow(A, p, p)
    rng = range(n)

    if p == 3:
        for r, c in zeros:
            if r == c:
                Ar = A[r]
                Pr = P[r]
                for j in rng:
                    Pr[j] += Ar[j]
                for i in rng:
                    P[i][r] += A[i][r]
            else:
                P[r][c] += A[c][r]
    else:
        for r, c in zeros:
            if r == c:
                Ar = A[r]
                Pr = P[r]
                for j in rng:
                    Pr[j] += Ar[j]
                for i in rng:
                    P[i][r] += A[i][r]

    if len(zeros) & 1:
        for i in rng:
            row = P[i]
            for j in rng:
                v = row[j] % p
                row[j] = 0 if v == 0 else p - v
    else:
        for i in rng:
            row = P[i]
            for j in rng:
                row[j] %= p

    out = [' '.join(map(str, row)) for row in P]
    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    solve()