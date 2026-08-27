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
    except StopIteration:
        return

    A = []
    for _ in range(N):
        row = []
        for _ in range(N):
            row.append(int(next(iterator)))
        A.append(row)

    # Identify zero positions (S)
    S = set()
    for r in range(N):
        for c in range(N):
            if A[r][c] == 0:
                S.add((r, c))
    
    K = len(S)
    
    # Construct matrix M where M[i][j] = A[i][j] if A[i][j] != 0 else 0
    M = [[0] * N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            if A[r][c] != 0:
                M[r][c] = A[r][c]
    
    # Matrix Multiplication modulo p
    def mat_mul(X, Y, mod):
        Z = [[0] * N for _ in range(N)]
        for i in range(N):
            for k in range(N):
                if X[i][k] == 0:
                    continue
                val_x = X[i][k]
                for j in range(N):
                    Z[i][j] = (Z[i][j] + val_x * Y[k][j]) % mod
        return Z

    # Matrix Exponentiation modulo p
    def mat_pow(X, power, mod):
        res = [[0] * N for _ in range(N)]
        for i in range(N):
            res[i][i] = 1
        
        base = X
        while power > 0:
            if power % 2 == 1:
                res = mat_mul(res, base, mod)
            base = mat_mul(base, base, mod)
            power //= 2
        return res

    # Compute M^p
    Mp = mat_pow(M, p, p)
    
    # Precompute (-1)^|S| mod p
    # If K is even, (-1)^K = 1. If K is odd, (-1)^K = -1 = p-1.
    sign = 1 if K % 2 == 0 else p - 1
    
    results = []
    
    for i in range(N):
        row_res = []
        for j in range(N):
            base_val = Mp[i][j]
            add_val = 0
            
            # Iterate over all (r, c) in S
            for (r, c) in S:
                if p == 2:
                    # p=2. Path length 2.
                    # Case 1: i=r, j=v. Edge (c, j) not in S.
                    if i == r:
                        u, v = c, j
                        if (u, v) not in S:
                            add_val = (add_val + A[u][v]) % p
                    
                    # Case 2: i=u, j=c. Edge (i, r) not in S.
                    if j == c:
                        u, v = i, r
                        if (u, v) not in S:
                            add_val = (add_val + A[u][v]) % p
                            
                else:
                    # p is odd.
                    # Logic derived:
                    # If j == c:
                    #   k=1: i arbitrary, edge (i,r). Count 1.
                    #   k=p: i=r, edge (c,j). Count 1.
                    #   1<k<p: i=r. Even k: edge (c,r). Odd k: edge (r,c).
                    # If j == r:
                    #   k=p: i=r, edge (c,j). Count 1.
                    # Else: 0.
                    
                    if j == c:
                        # k=1
                        if (i, r) not in S:
                            add_val = (add_val + A[i][r]) % p
                        
                        # k=p
                        if i == r:
                            if (c, j) not in S:
                                add_val = (add_val + A[c][j]) % p
                        
                        # 1 < k < p
                        if i == r:
                            # Even k in (1, p) -> 2, 4, ..., p-1
                            cnt_even = (p - 1) // 2
                            if cnt_even > 0:
                                if (c, r) not in S:
                                    add_val = (add_val + A[c][r] * cnt_even) % p
                            # Odd k in (1, p) -> 3, 5, ..., p-2
                            cnt_odd = (p - 3) // 2
                            if cnt_odd > 0:
                                if (r, c) not in S:
                                    add_val = (add_val + A[r][c] * cnt_odd) % p
                                    
                    elif j == r:
                        # k=p
                        if i == r:
                            if (c, j) not in S:
                                add_val = (add_val + A[c][j]) % p
            
            total_val = (base_val + add_val) % p
            total_val = (total_val * sign) % p
            row_res.append(total_val)
        results.append(row_res)

    for row in results:
        print(*(row))

if __name__ == '__main__':
    solve()