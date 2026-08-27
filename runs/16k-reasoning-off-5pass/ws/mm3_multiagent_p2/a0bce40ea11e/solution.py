import sys

def mat_mult(A, B, mod):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(n):
            a = Ai[k]
            if a == 0:
                continue
            Bk = B[k]
            for j in range(n):
                Ci[j] = (Ci[j] + a * Bk[j]) % mod
    return C

def mat_pow(M, power, mod):
    n = len(M)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    base = M
    while power > 0:
        if power & 1:
            result = mat_mult(result, base, mod)
        base = mat_mult(base, base, mod)
        power >>= 1
    return result

def solve():
    input = sys.stdin.readline
    N, p = map(int, input().split())
    A = []
    zeros = []
    for i in range(N):
        row = list(map(int, input().split()))
        A.append(row)
        for j in range(N):
            if row[j] == 0:
                zeros.append((i, j))
    K = len(zeros)
    
    if p == 2:
        B = [[1 if A[i][j] == 0 else A[i][j] for j in range(N)] for i in range(N)]
        M = mat_pow(B, p, p)
        for row in M:
            print(' '.join(map(str, row)))
        return
    
    # p is odd prime
    Aprime = [[A[i][j] for j in range(N)] for i in range(N)]
    M = mat_pow(Aprime, p, p)
    
    L = [[0]*N for _ in range(N)]
    if p == 3:
        for (i, j) in zeros:
            if i == j:
                # loop contribution
                for k in range(N):
                    if A[i][k] != 0:
                        L[i][k] = (L[i][k] + A[i][k]) % p
                    if A[k][i] != 0:
                        L[k][i] = (L[k][i] + A[k][i]) % p
            else:
                # non-loop: check reverse edge
                if A[j][i] != 0:
                    L[i][j] = (L[i][j] + A[j][i]) % p
    else:
        # p > 3: only loops contribute
        for (i, j) in zeros:
            if i == j:
                for k in range(N):
                    if A[i][k] != 0:
                        L[i][k] = (L[i][k] + A[i][k]) % p
                    if A[k][i] != 0:
                        L[k][i] = (L[k][i] + A[k][i]) % p
    
    # Combine M and L
    S = [[(M[i][j] + L[i][j]) % p for j in range(N)] for i in range(N)]
    
    # Multiply by (-1)^K
    factor = 1 if K % 2 == 0 else p - 1
    if factor != 1:
        for i in range(N):
            for j in range(N):
                S[i][j] = (S[i][j] * factor) % p
    
    for row in S:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    solve()