import sys
import random

def mat_mul(A, B, mod):
    n = len(A)
    m = len(B[0])
    p = len(B)
    C = [[0]*m for _ in range(n)]
    for i in range(n):
        for k in range(p):
            aik = A[i][k]
            if aik == 0:
                continue
            for j in range(m):
                C[i][j] = (C[i][j] + aik * B[k][j]) % mod
    return C

def mat_pow(M, power, mod):
    n = len(M)
    result = [[0]*n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    base = M
    while power > 0:
        if power & 1:
            result = mat_mul(result, base, mod)
        base = mat_mul(base, base, mod)
        power >>= 1
    return result

def brute_force(N, p, A):
    """Compute the sum of B^p for all B by brute force (for small N and K)."""
    zeros = [(i,j) for i in range(N) for j in range(N) if A[i][j] == 0]
    K = len(zeros)
    if K > 10:
        return None  # Too large
    total = [[0]*N for _ in range(N)]
    choices = list(range(1, p))
    from itertools import product
    for assignment in product(choices, repeat=K):
        B = [row[:] for row in A]
        for (i,j), val in zip(zeros, assignment):
            B[i][j] = val
        Bp = mat_pow(B, p, p)
        for i in range(N):
            for j in range(N):
                total[i][j] = (total[i][j] + Bp[i][j]) % p
    return total

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    p = int(input_data[idx]); idx += 1
    A = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[idx]) % p)
            idx += 1
        A.append(row)
    
    if p == 2:
        C = [[0]*N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if A[i][j] != 0:
                    C[i][j] = A[i][j] % p
        Cp = mat_pow(C, 2, p)
        row_sum = [[0]*N for _ in range(N)]
        for i in range(N):
            s = sum(C[i][j] for j in range(N)) % p
            for j in range(N):
                row_sum[i][j] = s
        col_sum = [[0]*N for _ in range(N)]
        for j in range(N):
            s = sum(C[i][j] for i in range(N)) % p
            for i in range(N):
                col_sum[i][j] = s
        M = [[0]*N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if A[i][j] == 0:
                    M[i][j] = 1
        M2 = mat_mul(M, M, p)
        S = [[0]*N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                S[i][j] = (Cp[i][j] + row_sum[i][j] + col_sum[i][j] + M2[i][j]) % p
        out_lines = []
        for i in range(N):
            out_lines.append(' '.join(str(x) for x in S[i]))
        sys.stdout.write('\n'.join(out_lines))
        return
    
    C = [[0]*N for _ in range(N)]
    K = 0
    for i in range(N):
        for j in range(N):
            if A[i][j] != 0:
                C[i][j] = A[i][j] % p
            else:
                K += 1
    
    if K == 0:
        S = mat_pow(A, p, p)
        out_lines = []
        for i in range(N):
            out_lines.append(' '.join(str(x) for x in S[i]))
        sys.stdout.write('\n'.join(out_lines))
        return
    
    pow_full = 1 if K % 2 == 0 else (p-1)
    pow_corr = 1 if (K-1) % 2 == 0 else (p-1)
    
    Cp = mat_pow(C, p, p)
    S = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            S[i][j] = (pow_full * Cp[i][j]) % p
    
    T = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                if i != j:
                    if A[j][i] != 0:
                        T[i][j] = (T[i][j] + C[j][i]) % p
                else:
                    for l in range(N):
                        if A[i][l] != 0:
                            T[i][l] = (T[i][l] + C[i][l]) % p
                    for k in range(N):
                        if A[k][i] != 0:
                            T[k][i] = (T[k][i] + C[k][i]) % p
    
    for i in range(N):
        for j in range(N):
            S[i][j] = (S[i][j] - pow_corr * T[i][j]) % p
            if S[i][j] < 0:
                S[i][j] += p
    
    out_lines = []
    for i in range(N):
        out_lines.append(' '.join(str(x) for x in S[i]))
    sys.stdout.write('\n'.join(out_lines))

def test():
    # Test sample 1
    N, p = 2, 3
    A = [[0,1],[0,2]]
    expected = [[0,2],[1,2]]
    
    import io
    sys.stdin = io.StringIO(f"{N} {p}\n{A[0][0]} {A[0][1]}\n{A[1][0]} {A[1][1]}\n")
    output = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    result = sys.stdout.getvalue().strip().split('\n')
    sys.stdout = output
    result = [[int(x) for x in line.split()] for line in result]
    assert result == expected, f"Sample 1 failed: got {result}, expected {expected}"
    print("Sample 1 passed")
    
    # Test sample 2
    N, p = 3, 2
    A = [[1,0,0],[0,1,0],[0,0,1]]
    expected = [[1,1,1],[1,1,1],[1,1,1]]
    
    sys.stdin = io.StringIO(f"{N} {p}\n{A[0][0]} {A[0][1]} {A[0][2]}\n{A[1][0]} {A[1][1]} {A[1][2]}\n{A[2][0]} {A[2][1]} {A[2][2]}\n")
    sys.stdout = io.StringIO()
    solve()
    result = sys.stdout.getvalue().strip().split('\n')
    sys.stdout = output
    result = [[int(x) for x in line.split()] for line in result]
    assert result == expected, f"Sample 2 failed: got {result}, expected {expected}"
    print("Sample 2 passed")
    
    # Test sample 3
    N, p = 4, 13
    A = [[0,1,2,0],[3,4,0,5],[0,6,0,7],[8,9,0,0]]
    expected = [[8,0,6,5],[11,1,8,5],[8,0,4,12],[8,0,1,9]]
    
    sys.stdin = io.StringIO(f"{N} {p}\n" + '\n'.join(' '.join(map(str, row)) for row in A) + '\n')
    sys.stdout = io.StringIO()
    solve()
    result = sys.stdout.getvalue().strip().split('\n')
    sys.stdout = output
    result = [[int(x) for x in line.split()] for line in result]
    assert result == expected, f"Sample 3 failed: got {result}, expected {expected}"
    print("Sample 3 passed")
    
    # Random tests for small N and p
    random.seed(42)
    for _ in range(50):
        N = random.randint(1, 3)
        p = random.choice([2, 3, 5, 7])
        A = [[random.randint(0, p-1) for _ in range(N)] for _ in range(N)]
        
        # Compute via our algorithm
        import io
        sys.stdin = io.StringIO(f"{N} {p}\n" + '\n'.join(' '.join(map(str, row)) for row in A) + '\n')
        sys.stdout = io.StringIO()
        solve()
        result = sys.stdout.getvalue().strip().split('\n')
        sys.stdout = output
        result = [[int(x) for x in line.split()] for line in result]
        
        # Compute via brute force
        brute = brute_force(N, p, A)
        if brute is not None:
            assert result == brute, f"Mismatch for N={N}, p={p}, A={A}: got {result}, expected {brute}"
    
    print("All random tests passed")

if __name__ == "__main__":
    test()