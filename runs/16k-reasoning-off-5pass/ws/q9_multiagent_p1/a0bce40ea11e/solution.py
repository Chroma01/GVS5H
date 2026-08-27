import sys

# Increase recursion depth just in case
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        p = int(next(iterator))
        
        A = []
        for _ in range(N):
            row = []
            for _ in range(N):
                row.append(int(next(iterator)))
            A.append(row)
    except StopIteration:
        return

    # Count zeros
    K = 0
    for r in range(N):
        for c in range(N):
            if A[r][c] == 0:
                K += 1

    # If there are no zeros, the answer is simply A^p mod p
    if K == 0:
        def mat_mul(X, Y, mod):
            Z = [[0] * N for _ in range(N)]
            for i in range(N):
                for k in range(N):
                    if X[i][k] == 0: continue
                    for j in range(N):
                        Z[i][j] = (Z[i][j] + X[i][k] * Y[k][j]) % mod
            return Z

        def mat_pow(X, power, mod):
            res = [[0] * N for _ in range(N)]
            for i in range(N): res[i][i] = 1
            base = X
            while power > 0:
                if power % 2 == 1:
                    res = mat_mul(res, base, mod)
                base = mat_mul(base, base, mod)
                power //= 2
            return res

        res = mat_pow(A, p, p)
        for row in res:
            print(*(row))
        return

    # Build M (A with zeros replaced by 0)
    M = [[0]*N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if A[r][c] != 0:
                M[r][c] = A[r][c]
            else:
                M[r][c] = 0

    # Matrix multiplication and exponentiation
    def mat_mul(X, Y, mod):
        Z = [[0] * N for _ in range(N)]
        for i in range(N):
            for k in range(N):
                if X[i][k] == 0: continue
                for j in range(N):
                    Z[i][j] = (Z[i][j] + X[i][k] * Y[k][j]) % mod
        return Z

    def mat_pow(X, power, mod):
        res = [[0] * N for _ in range(N)]
        for i in range(N): res[i][i] = 1
        base = X
        while power > 0:
            if power % 2 == 1:
                res = mat_mul(res, base, mod)
            base = mat_mul(base, base, mod)
            power //= 2
        return res

    Mp = mat_pow(M, p, p)

    # Compute S_row[u] = sum(M[x][u]) and S_col[v] = sum(M[v][y])
    S_row = [0] * N
    S_col = [0] * N
    for r in range(N):
        for c in range(N):
            if M[r][c] != 0:
                S_row[c] = (S_row[c] + M[r][c]) % p
                S_col[r] = (S_col[r] + M[r][c]) % p

    # Compute (p-1)^K mod p
    base = (p - 1) % p
    pow_K = pow(base, K, p)

    # Compute correction terms
    # Corr[i][j] accumulates contributions from paths with exactly one zero edge (u,v) appearing p-1 times
    Corr = [[0]*N for _ in range(N)]
    
    for r in range(N):
        for c in range(N):
            if A[r][c] == 0:
                # Zero edge (r,c)
                # Contribution type 1: Start with non-zero edge (x,r), then (r,c) repeated p-1 times.
                # Path: x -> r -> c -> r -> c ... -> c.
                # Requires j == c. Contribution: (p-1) * M[x][r].
                # Sum over x: (p-1) * S_row[r].
                # We add this to Corr[i][c] for all i.
                val1 = S_row[r]
                for i in range(N):
                    Corr[i][c] = (Corr[i][c] + val1) % p
                
                # Contribution type 2: End with non-zero edge (c,y).
                # Path: r -> c -> r -> c ... -> c -> y.
                # Requires i == r. Contribution: (p-1) * M[c][y].
                # Sum over y: (p-1) * S_col[c].
                # We add this to Corr[r][j] for all j.
                val2 = S_col[c]
                for j in range(N):
                    Corr[r][j] = (Corr[r][j] + val2) % p
                
                # Contribution type 3: Cycle r -> c -> r -> c ... -> r -> c.
                # Requires i == r, j == c. Contribution: (p-1) * M[c][r].
                # Note: This path is distinct from type 1 and 2 in terms of structure (non-zero edge in middle).
                # However, type 1 with x=r gives r->r->c...->c (edge r->r).
                # Type 2 with y=r gives r->c...->c->r (edge c->r).
                # The cycle r->c->r...->r->c has edges (r,c) x (p-1) and (c,r) x 1.
                # This is valid if M[c][r] != 0.
                val3 = M[c][r]
                Corr[r][c] = (Corr[r][c] + val3) % p

    # Final Answer
    for i in range(N):
        row_res = []
        for j in range(N):
            # Total sum = (p-1)^K * (Mp[i][j] + Corr[i][j])
            term = (Mp[i][j] + Corr[i][j]) % p
            ans = (pow_K * term) % p
            row_res.append(str(ans))
        print(" ".join(row_res))

if __name__ == '__main__':
    solve()