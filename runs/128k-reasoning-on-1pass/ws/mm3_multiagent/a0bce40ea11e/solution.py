import sys

def mat_mul(A, B, mod):
    n = len(A)
    # Initialize result matrix
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        Ai = A[i]
        Ci = C[i]
        for k in range(n):
            aik = Ai[k]
            if aik:
                Bk = B[k]
                # unroll inner loop
                for j in range(n):
                    Ci[j] = (Ci[j] + aik * Bk[j]) % mod
    return C

def mat_pow(mat, exp, mod):
    n = len(mat)
    # identity matrix
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1 % mod
    base = mat
    e = exp
    while e > 0:
        if e & 1:
            result = mat_mul(result, base, mod)
        base = mat_mul(base, base, mod)
        e >>= 1
    return result

def mat_add(A, B, mod):
    n = len(A)
    C = [[(A[i][j] + B[i][j]) % mod for j in range(n)] for i in range(n)]
    return C

def mat_scalar_mul(A, scalar, mod):
    n = len(A)
    C = [[(A[i][j] * scalar) % mod for j in range(n)] for i in range(n)]
    return C

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    p = int(next(it))
    A = [[int(next(it)) for _ in range(N)] for _ in range(N)]
    
    # Special case p == 2
    if p == 2:
        # Construct B: replace zeros with 1
        B = [row[:] for row in A]
        for i in range(N):
            for j in range(N):
                if B[i][j] == 0:
                    B[i][j] = 1
        # Compute B^2 mod 2
        res = mat_mul(B, B, 2)
        out_lines = [' '.join(str(x % 2) for x in row) for row in res]
        sys.stdout.write('\n'.join(out_lines))
        return
    
    # p > 2
    # C is A with zeros treated as 0 (already)
    C = A
    # Compute C^p
    C_pow = mat_pow(C, p, p)
    
    # Count zeros and accumulate sum_T
    sum_T = [[0] * N for _ in range(N)]
    K = 0
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                K += 1
                if i == j:
                    # Diagonal zero: add C * E_{ii}
                    # C * E_{ii} has column i = column i of C
                    col = i
                    for k in range(N):
                        sum_T[k][col] = (sum_T[k][col] + C[k][col]) % p
                    # E_{ii} * C has row i = row i of C
                    row = i
                    for k in range(N):
                        sum_T[row][k] = (sum_T[row][k] + C[row][k]) % p
                    # add (p-2) * C[i][i] to (i,i)
                    sum_T[i][i] = (sum_T[i][i] + ((p - 2) * C[i][i])) % p
                else:
                    # Off-diagonal zero
                    if p == 3:
                        # add C[j][i] to (i,j)
                        sum_T[i][j] = (sum_T[i][j] + C[j][i]) % p
                    # else: nothing
    
    # Compute (C_pow + sum_T) mod p
    res = [[(C_pow[i][j] + sum_T[i][j]) % p for j in range(N)] for i in range(N)]
    
    # Apply factor (-1)^K
    if K % 2 == 1:
        for i in range(N):
            for j in range(N):
                res[i][j] = (p - res[i][j]) % p
    
    out_lines = [' '.join(str(x) for x in row) for row in res]
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()