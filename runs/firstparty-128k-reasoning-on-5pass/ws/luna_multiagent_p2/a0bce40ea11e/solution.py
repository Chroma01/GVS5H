import sys


def mat_mul(X, Y, mod):
    n = len(X)
    Z = [[0] * n for _ in range(n)]
    for i in range(n):
        zi = Z[i]
        xi = X[i]
        for k, x in enumerate(xi):
            if x:
                yk = Y[k]
                for j in range(n):
                    zi[j] += x * yk[j]
        for j in range(n):
            zi[j] %= mod
    return Z


def mat_pow(A, e, mod):
    n = len(A)
    R = [[0] * n for _ in range(n)]
    for i in range(n):
        R[i][i] = 1 % mod

    while e:
        if e & 1:
            R = mat_mul(R, A, mod)
        A = mat_mul(A, A, mod)
        e >>= 1
    return R


def main():
    input = sys.stdin.readline
    N, p = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(N)]

    if p == 2:
        B = [row[:] for row in A]
        for i in range(N):
            for j in range(N):
                if B[i][j] == 0:
                    B[i][j] = 1
        ans = mat_mul(B, B, 2)
        for row in ans:
            print(*row)
        return

    zeros = []
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                zeros.append((i, j))

    ans = mat_pow(A, p, p)

    correction = [[0] * N for _ in range(N)]

    if p == 3:
        for u, v in zeros:
            if u == v:
                for j in range(N):
                    correction[u][j] += A[u][j]
                for i in range(N):
                    correction[i][u] += A[i][u]
            else:
                correction[u][v] += A[v][u]
    else:
        for u, v in zeros:
            if u == v:
                for j in range(N):
                    correction[u][j] += A[u][j]
                for i in range(N):
                    correction[i][u] += A[i][u]

    sign = 1 if len(zeros) % 2 == 0 else p - 1
    for i in range(N):
        for j in range(N):
            ans[i][j] = sign * (ans[i][j] + correction[i][j]) % p

    for row in ans:
        print(*row)


if __name__ == "__main__":
    main()