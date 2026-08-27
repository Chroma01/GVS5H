import sys

def solve():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    it = iter(data)
    N = next(it)
    p = next(it)
    A = [[next(it) % p for _ in range(N)] for _ in range(N)]

    # Count zeros in each row and column.
    rowz = [0] * N
    colz = [0] * N
    for i in range(N):
        ri = A[i]
        c = 0
        for j in range(N):
            if ri[j] == 0:
                c += 1
                colz[j] += 1
        rowz[i] = c

    # Compute A^p mod p by fast exponentiation.
    def matmul(X, Y):
        n = len(X)
        Z = [[0] * n for _ in range(n)]
        for i in range(n):
            Xi = X[i]
            Zi = Z[i]
            for k in range(n):
                a = Xi[k]
                if a:
                    Yk = Y[k]
                    for j in range(n):
                        Zi[j] = (Zi[j] + a * Yk[j]) % p
        return Z

    def matpow(M, e):
        n = len(M)
        R = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        B = [row[:] for row in M]
        while e:
            if e & 1:
                R = matmul(R, B)
            e >>= 1
            if e:
                B = matmul(B, B)
        return R

    AP = matpow(A, p)

    out = []
    for i in range(N):
        line = []
        for j in range(N):
            val = (-AP[i][j]) % p
            if rowz[i] and colz[j]:
                val = (val + pow(A[i][j], p - 1, p)) % p
            line.append(str(val))
        out.append(' '.join(line))
    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    solve()