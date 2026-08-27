import sys

# Set recursion depth just in case, though we won't use recursion
sys.setrecursionlimit(2000)

MOD = 998244353

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    W, H, L, R, D, U = map(int, input_data)

    # Precompute factorials
    max_val = W + H + 10
    fact = [1] * (max_val + 1)
    inv_fact = [1] * (max_val + 1)
    
    for i in range(1, max_val + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv_fact[max_val] = pow(fact[max_val], MOD - 2, MOD)
    for i in range(max_val - 1, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv_fact[r] * inv_fact[n-r]) % MOD
        return (num * den) % MOD

    def T(x, y):
        # Total paths in grid [0, x] x [0, y]
        # Formula: binom(x+y+4, x+2) - xy - 2x - 2y - 5
        term1 = nCr(x + y + 4, x + 2)
        term2 = (x * y) % MOD
        term3 = (2 * x) % MOD
        term4 = (2 * y) % MOD
        term5 = 5
        res = (term1 - term2 - term3 - term4 - term5) % MOD
        return res

    def T_total(W, H):
        return T(W, H)

    def sum_T_in_F(L, R, D, U, W, H):
        # Sum of T(W-x, H-y) for (x, y) in [L, R] x [D, U]
        # Let u = W-x, v = H-y. u in [W-R, W-L], v in [H-U, H-D]
        # Sum of binom(u+v+4, u+2) - uv - 2u - 2v - 5
        
        u_min, u_max = W - R, W - L
        v_min, v_max = H - U, H - D
        
        # Sum of binom(u+v+4, u+2)
        # Sum over v first: sum_{v=v_min}^{v_max} binom(u+v+4, u+2)
        # = binom(u+v_max+5, u+3) - binom(u+v_min+4, u+3)
        # Then sum over u
        
        # We need a function to sum binom(u+k, u+3) over u
        # sum_{u=u_min}^{u_max} binom(u+k, u+3) = binom(u_max+k+1, u_max+4) - binom(u_min-1+k+1, u_min+3)
        # Wait, identity: sum_{i=0}^n binom(i+k, k) = binom(n+k+1, k+1)
        # Here we have binom(u+v+4, u+2) = binom(u+v+4, v+2)
        # Let's use the identity directly.
        
        # Sum_{u=u_min}^{u_max} Sum_{v=v_min}^{v_max} binom(u+v+4, u+2)
        # = Sum_{u=u_min}^{u_max} [ binom(u+v_max+5, u+3) - binom(u+v_min+4, u+3) ]
        # = [ Sum_{u=u_min}^{u_max} binom(u+v_max+5, u+3) ] - [ Sum_{u=u_min}^{u_max} binom(u+v_min+4, u+3) ]
        
        # Sum_{u=A}^{B} binom(u+C, u+3) = Sum_{u=A}^{B} binom(u+C, C-3) ? No.
        # binom(u+C, u+3) = binom(u+C, C-3) is not helpful.
        # Use identity: sum_{i=0}^n binom(i+k, k) = binom(n+k+1, k+1)
        # Here k = C-3? No.
        # binom(u+C, u+3) = binom(u+C, C-3) if we fix C.
        # Let's rewrite binom(u+v+4, u+2) = binom(u+v+4, v+2).
        # Sum over v: binom(u+v+4, v+2). Let k = u+4. binom(k+v, v+2).
        # This is not standard.
        # Let's use the property: binom(n, k) = binom(n-1, k) + binom(n-1, k-1).
        # Actually, there is a known identity for sum of binom(i+j, i).
        # sum_{i=0}^m sum_{j=0}^n binom(i+j, i) = binom(m+n+2, m+1) - 1.
        # But we have weights (W-u+1)(H-v+1).
        # Wait, I already derived the formula for sum_T_in_F in the thought process.
        # It involves summing binom(u+v+4, u+2).
        # Let's compute it directly using the identity:
        # sum_{v=0}^n binom(u+v+4, u+2) = binom(u+n+5, u+3).
        # So sum_{v=v_min}^{v_max} binom(u+v+4, u+2) = binom(u+v_max+5, u+3) - binom(u+v_min+4, u+3).
        # Now sum over u:
        # sum_{u=u_min}^{u_max} binom(u+v_max+5, u+3) = sum_{u=u_min}^{u_max} binom(u+v_max+5, v_max+2).
        # Let k = v_max+2. sum_{u=u_min}^{u_max} binom(u+k, k).
        # = binom(u_max+k+1, k+1) - binom(u_min-1+k+1, k+1).
        # = binom(u_max+v_max+6, v_max+3) - binom(u_min+v_max+6, v_max+3).
        
        # Similarly for the second term with v_min.
        
        def sum_binom_u(A, B, C):
            # Sum_{u=A}^{B} binom(u+C, u+3) = Sum_{u=A}^{B} binom(u+C, C-3) ? No.
            # binom(u+C, u+3) = binom(u+C, C-3) is only if C-3 >= 0.
            # But we can use the identity sum_{i=0}^n binom(i+k, k) = binom(n+k+1, k+1).
            # Here we have binom(u+C, u+3). Let i = u. k = C-3? No.
            # binom(u+C, u+3) = binom(u+C, C-3).
            # So sum_{u=A}^{B} binom(u+C, C-3) = binom(B+C+1, C-2) - binom(A-1+C+1, C-2).
            # Wait, the identity is sum_{i=0}^n binom(i+k, k) = binom(n+k+1, k+1).
            # Here the lower index is fixed (C-3). So k = C-3.
            # So sum_{u=0}^n binom(u+C, C-3) = binom(n+C+1, C-2).
            # So sum_{u=A}^{B} binom(u+C, C-3) = binom(B+C+1, C-2) - binom(A-1+C+1, C-2).
            
            # But we need to be careful with C-3 < 0.
            # If C-3 < 0, then binom(u+C, C-3) = 0.
            # So we need C >= 3.
            # In our case, C = v_max+5 or v_min+4.
            # v_max >= 0, so C >= 5. So C-3 >= 2.
            # So it's safe.
            
            k = C - 3
            term1 = nCr(B + C + 1, k + 1)
            term2 = nCr(A - 1 + C + 1, k + 1)
            return (term1 - term2) % MOD

        # Sum of binom(u+v+4, u+2)
        # = sum_{u=u_min}^{u_max} [ binom(u+v_max+5, u+3) - binom(u+v_min+4, u+3) ]
        # = sum_binom_u(u_min, u_max, v_max+5) - sum_binom_u(u_min, u_max, v_min+4)
        
        sum_binom = (sum_binom_u(u_min, u_max, v_max + 5) - sum_binom_u(u_min, u_max, v_min + 4)) % MOD
        
        # Sum of -uv
        # sum_{u=u_min}^{u_max} sum_{v=v_min}^{v_max} -uv
        # = - (sum_u u) * (sum_v v)
        sum_u = (u_min + u_max) * (u_max - u_min + 1) // 2
        sum_v = (v_min + v_max) * (v_max - v_min + 1) // 2
        sum_uv = (sum_u * sum_v) % MOD
        
        # Sum of -2u
        # = -2 * (sum_u u) * (v_max - v_min + 1)
        count_v = v_max - v_min + 1
        sum_2u = (2 * sum_u * count_v) % MOD
        
        # Sum of -2v
        # = -2 * (sum_v v) * (u_max - u_min + 1)
        count_u = u_max - u_min + 1
        sum_2v = (2 * sum_v * count_u) % MOD
        
        # Sum of -5
        # = -5 * count_u * count_v
        sum_5 = (5 * count_u * count_v) % MOD
        
        res = (sum_binom - sum_uv - sum_2u - sum_2v - sum_5) % MOD
        return res

    def T_point(x, y):
        # T(W-x, H-y)
        return T(W - x, H - y)

    def T_in_F(p_x, p_y, R, U):
        # T(R-p_x, U-p_y)
        return T(R - p_x, U - p_y)

    # Compute sum_T_in_F
    sum_T_F = sum_T_in_F(L, R, D, U, W, H)
    
    # Compute B_p for p in boundary of F
    # Boundary points
    points = []
    # Bottom: (x, D) for x in [L, R]
    for x in range(L, R + 1):
        points.append((x, D))
    # Right: (R, y) for y in [D+1, U]
    for y in range(D + 1, U + 1):
        points.append((R, y))
    # Top: (x, U) for x in [R-1, L-1] (reverse)
    for x in range(R - 1, L - 1, -1):
        points.append((x, U))
    # Left: (L, y) for y in [U-1, D+1] (reverse)
    for y in range(U - 1, D, -1):
        points.append((L, y))
        
    N = len(points)
    C = [0] * N
    diag = [0] * N
    
    for i, (x, y) in enumerate(points):
        # Neighbors outside F
        neighbors_out = []
        if x - 1 < L:
            neighbors_out.append((x - 1, y))
        if x + 1 > R:
            neighbors_out.append((x + 1, y))
        if y - 1 < D:
            neighbors_out.append((x, y - 1))
        if y + 1 > U:
            neighbors_out.append((x, y + 1))
            
        diag[i] = 1 + len(neighbors_out)
        c_val = 0
        for nx, ny in neighbors_out:
            c_val = (c_val + T(nx, ny)) % MOD
        C[i] = c_val
        
    # Solve tridiagonal system A B = C
    # A is tridiagonal with diag[i] on diagonal, -1 on off-diagonals
    # We can use Gaussian elimination for tridiagonal matrix
    
    # Forward elimination
    # A[i][i] * B[i] + A[i][i+1] * B[i+1] = C[i]
    # A[i][i-1] * B[i-1] + A[i][i] * B[i] + A[i][i+1] * B[i+1] = C[i]
    # Here A[i][i+1] = -1, A[i][i-1] = -1
    
    # Modify C and diag
    # For i = 0:
    # diag[0] * B[0] - B[1] = C[0]
    # B[1] = diag[0] * B[0] - C[0]
    # Substitute into i=1:
    # -B[0] + diag[1] * B[1] - B[2] = C[1]
    # -B[0] + diag[1] * (diag[0] * B[0] - C[0]) - B[2] = C[1]
    # (diag[1]*diag[0] - 1) * B[0] - B[2] = C[1] + diag[1]*C[0]
    
    # General step:
    # We want to eliminate B[i-1] from equation i.
    # Equation i-1: a_{i-1} B[i-1] + b_{i-1} B[i] = c_{i-1}
    # Equation i: a_i B[i-1] + b_i B[i] + c_i B[i+1] = d_i
    # Here a_i = -1, b_i = diag[i], c_i = -1, d_i = C[i].
    # From eq i-1: B[i-1] = (c_{i-1} - b_{i-1} B[i]) / a_{i-1}
    # Substitute into eq i:
    # a_i * (c_{i-1} - b_{i-1} B[i]) / a_{i-1} + b_i B[i] + c_i B[i+1] = d_i
    # (b_i - a_i * b_{i-1} / a_{i-1}) B[i] + c_i B[i+1] = d_i - a_i * c_{i-1} / a_{i-1}
    
    # So new b_i' = b_i - a_i * b_{i-1} / a_{i-1}
    # new d_i' = d_i - a_i * c_{i-1} / a_{i-1}
    # And a_i' = 0 (eliminated)
    # c_i' = c_i
    
    # We store modified b and d.
    # Let's use arrays for modified coefficients.
    
    mod_inv_1 = pow(-1, MOD - 2, MOD) # -1 mod MOD
    
    b = list(diag)
    d = list(C)
    
    # Forward pass
    for i in range(1, N):
        # Eliminate B[i-1] from equation i
        # a_i = -1, b_{i-1} = b[i-1], a_{i-1} = 1 (since we normalized? No)
        # Wait, the standard form is a_i B[i-1] + b_i B[i] + c_i B[i+1] = d_i
        # Here a_i = -1, b_i = diag[i], c_i = -1.
        # From previous step, we have equation for i-1: b'[i-1] B[i-1] + c'[i-1] B[i] = d'[i-1]
        # But c'[i-1] is -1.
        # So B[i-1] = (d'[i-1] - (-1) B[i]) / b'[i-1] = (d'[i-1] + B[i]) / b'[i-1]
        # Substitute into eq i:
        # -1 * (d'[i-1] + B[i]) / b'[i-1] + b[i] B[i] - B[i+1] = d[i]
        # (b[i] - (-1)/b'[i-1]) B[i] - B[i+1] = d[i] - (-1)*d'[i-1]/b'[i-1]
        # (b[i] + 1/b'[i-1]) B[i] - B[i+1] = d[i] + d'[i-1]/b'[i-1]
        
        inv_b_prev = pow(b[i-1], MOD - 2, MOD)
        b[i] = (b[i] + inv_b_prev) % MOD
        d[i] = (d[i] + d[i-1] * inv_b_prev) % MOD
        
    # Backward substitution
    B = [0] * N
    B[N-1] = (d[N-1] * pow(b[N-1], MOD - 2, MOD)) % MOD
    for i in range(N - 2, -1, -1):
        # Equation i: b[i] B[i] - B[i+1] = d[i]
        # B[i] = (d[i] + B[i+1]) / b[i]
        B[i] = (d[i] + B[i+1]) * pow(b[i], MOD - 2, MOD) % MOD
        
    # Now B[i] is BadFirst[points[i]]
    
    # Compute sum B_p * (StartCount(p) - StartCountInF(p))
    sum_bad = 0
    for i, (x, y) in enumerate(points):
        start_count = T_point(x, y)
        start_count_in_F = T_in_F(x, y, R, U)
        diff = (start_count - start_count_in_F) % MOD
        term = (B[i] * diff) % MOD
        sum_bad = (sum_bad + term) % MOD
        
    # Total answer
    total_paths = T_total(W, H)
    ans = (total_paths - sum_T_F - sum_bad) % MOD
    print(ans)

solve()