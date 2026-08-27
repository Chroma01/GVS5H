import sys

def mat_mul(A, B, mod):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if A[i][k] == 0:
                continue
            aik = A[i][k]
            for j in range(n):
                C[i][j] = (C[i][j] + aik * B[k][j]) % mod
    return C

def mat_pow(M, p, mod):
    n = len(M)
    # Identity
    R = [[0]*n for _ in range(n)]
    for i in range(n):
        R[i][i] = 1
    base = [row[:] for row in M]
    while p > 0:
        if p & 1:
            R = mat_mul(R, base, mod)
        base = mat_mul(base, base, mod)
        p >>= 1
    return R

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it))
    p = int(next(it))
    A = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(next(it)))
        A.append(row)
    
    # Count zeros
    K = 0
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                K += 1
    
    # Build C: A with zeros replaced by 0 (so walks using zero edges contribute 0)
    # Actually, we need the matrix where non-zero entries are A[i][j] and zero entries are 0
    C = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if A[i][j] != 0:
                C[i][j] = A[i][j] % p
    
    # Compute C^p mod p
    Cp = mat_pow(C, p, p)
    
    # (-1)^K mod p
    sign = 1 if K % 2 == 0 else (p - 1)
    
    # Result is (-1)^K * C^p mod p
    res = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            res[i][j] = (sign * Cp[i][j]) % p
    
    # Output
    out_lines = []
    for i in range(N):
        out_lines.append(' '.join(str(res[i][j]) for j in range(N)))
    sys.stdout.write('\n'.join(out_lines))

solve()