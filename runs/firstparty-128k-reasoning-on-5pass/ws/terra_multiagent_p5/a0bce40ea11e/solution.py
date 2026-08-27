import sys

def solve():
    input = sys.stdin.readline
    N, p = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(N)]

    if p == 2:
        x = N & 1
        line = " ".join([str(x)] * N)
        print("\n".join([line] * N))
        return

    zeros = []
    K = 0
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                zeros.append((i, j))
                K += 1

    C = A

    def matmul(X, Y):
        Z = [[0] * N for _ in range(N)]
        for i in range(N):
            zi = Z[i]
            xi = X[i]
            for k, x in enumerate(xi):
                if x:
                    yk = Y[k]
                    for j in range(N):
                        zi[j] += x * yk[j]
            for j in range(N):
                zi[j] %= p
        return Z

    def matpow(X, e):
        R = [[0] * N for _ in range(N)]
        for i in range(N):
            R[i][i] = 1
        while e:
            if e & 1:
                R = matmul(R, X)
            X = matmul(X, X)
            e >>= 1
        return R

    if p == 3:
        answer = matmul(matmul(C, C), C)

        # For every zero edge E_(u,v), add ECE.
        # If it is a loop, also add CE^2 + E^2C = CE + EC.
        for u, v in zeros:
            answer[u][v] = (answer[u][v] + C[v][u]) % p
            if u == v:
                for r in range(N):
                    answer[r][u] = (answer[r][u] + C[r][u]) % p
                for c in range(N):
                    answer[u][c] = (answer[u][c] + C[u][c]) % p
    else:
        answer = matpow(C, p)

        # Only zero loops can occur p-1 times in a length-p walk.
        # Their total extra contribution is CE + EC - 2*CEE.
        for i in range(N):
            if C[i][i] == 0:
                for r in range(N):
                    answer[r][i] = (answer[r][i] + C[r][i]) % p
                for c in range(N):
                    answer[i][c] = (answer[i][c] + C[i][c]) % p
                answer[i][i] = (answer[i][i] - 2 * C[i][i]) % p

    if K & 1:
        for i in range(N):
            for j in range(N):
                answer[i][j] = (-answer[i][j]) % p

    for row in answer:
        print(*row)

if __name__ == "__main__":
    solve()