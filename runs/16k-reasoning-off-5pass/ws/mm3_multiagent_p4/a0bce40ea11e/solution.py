import sys

def mat_mul(A, B, mod):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(n):
            aik = Ai[k]
            if aik:
                Bk = B[k]
                for j in range(n):
                    Ci[j] = (Ci[j] + aik * Bk[j]) % mod
    return C

def mat_pow(F, power, mod):
    n = len(F)
    # Identity matrix
    res = [[0]*n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    while power > 0:
        if power & 1:
            res = mat_mul(res, F, mod)
        F = mat_mul(F, F, mod)
        power >>= 1
    return res

def solve():
    input = sys.stdin.readline
    N, p = map(int, input().split())
    A = [list(map(int, input().split())) for _ in range(N)]
    
    if p == 2:
        val = N % 2
        for i in range(N):
            print(' '.join([str(val)] * N))
        return
    
    mod = p
    K = 0
    zeros = []
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                K += 1
                zeros.append((i, j))
    
    sign = 1 if K % 2 == 0 else mod - 1
    
    # Build F: nonzero entries of A, zero elsewhere
    F = [[A[i][j] if A[i][j] != 0 else 0 for j in range(N)] for i in range(N)]
    
    # Compute F^p mod p
    P = mat_pow(F, p, mod)
    
    # Build extra matrix E
    E = [[0]*N for _ in range(N)]
    for (i, j) in zeros:
        if i == j:
            # self-loop zero
            for y in range(N):
                if F[i][y] != 0:
                    E[i][y] = (E[i][y] + F[i][y]) % mod
            for x in range(N):
                if F[x][i] != 0:
                    E[x][i] = (E[x][i] + F[x][i]) % mod
        elif p == 3:
            # non-self-loop zero, only p=3 contributes
            if F[j][i] != 0:
                E[i][j] = (E[i][j] + F[j][i]) % mod
    
    T = [[(P[i][j] + E[i][j]) % mod for j in range(N)] for i in range(N)]
    S = [[(sign * T[i][j]) % mod for j in range(N)] for i in range(N)]
    
    out_lines = []
    for i in range(N):
        out_lines.append(' '.join(map(str, S[i])))
    print('\n'.join(out_lines))

if __name__ == "__main__":
    solve()