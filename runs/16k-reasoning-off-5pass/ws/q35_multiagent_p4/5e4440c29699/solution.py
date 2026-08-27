import sys

# Set recursion depth just in case, though we aim for iterative
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    W = int(input_data[0])
    H = int(input_data[1])
    L = int(input_data[2])
    R = int(input_data[3])
    D = int(input_data[4])
    U = int(input_data[5])

    MOD = 998244353

    # Precompute factorials and inverse factorials for combinations
    MAX_N = W + H + 5
    fact = [1] * MAX_N
    inv_fact = [1] * MAX_N

    for i in range(1, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD

    inv_fact[MAX_N-1] = pow(fact[MAX_N-1], MOD - 2, MOD)
    for i in range(MAX_N-2, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv_fact[r] * inv_fact[n-r]) % MOD
        return (num * den) % MOD

    # Function to compute S(u, v) = sum_{dx=0}^u sum_{dy=0}^v C(dx+dy, dx)
    # Identity: sum_{i=0}^n sum_{j=0}^m C(i+j, i) = C(n+m+2, 2) - 1
    def S(u, v):
        if u < 0 or v < 0:
            return 0
        return (nCr(u + v + 2, 2) - 1 + MOD) % MOD

    # Function to compute End(x, y) = sum_{dx=0}^{W-x} sum_{dy=0}^{H-y} C(dx+dy, dx)
    def End(x, y):
        dx_max = W - x
        dy_max = H - y
        if dx_max < 0 or dy_max < 0:
            return 0
        return (nCr(dx_max + dy_max + 2, 2) - 1 + MOD) % MOD

    # Calculate Total Full Paths
    # Total = sum_{dx=0}^W sum_{dy=0}^H (W-dx+1)(H-dy+1) C(dx+dy, dx)
    # Let A = W+1, B = H+1.
    # Total = sum_{dx=0}^W (A-dx) * sum_{dy=0}^H (B-dy) * C(dx+dy, dx)
    
    # We can compute this in O(W+H) by iterating dx and maintaining a running sum for dy.
    # Let T(dx) = sum_{dy=0}^H (B-dy) * C(dx+dy, dx)
    # We know C(dx+dy, dx) = C(dx+dy, dy).
    # Let's use the identity: sum_{j=0}^n (n+1-j) * C(r+j, j) = C(r+n+2, n+1) - 1 ? No.
    # Let's derive:
    # sum_{dy=0}^H (H+1-dy) * C(dx+dy, dx)
    # Let k = dx+dy. dy = k-dx. Range k: dx to dx+H.
    # Term: (H+1 - (k-dx)) * C(k, dx) = (H+1+dx - k) * C(k, dx)
    # = (H+1+dx) * C(k, dx) - k * C(k, dx)
    # Note k * C(k, dx) = k * k! / (dx! (k-dx)!) = (k-dx+dx) ... 
    # Actually k * C(k, dx) = (dx+1) * C(k+1, dx+1) ? No.
    # k * C(k, dx) = (dx+1) * C(k, dx+1) + dx * C(k, dx) ? No.
    # Identity: k * C(k, r) = (r+1) * C(k+1, r+1) - C(k, r) ? No.
    # k * C(k, r) = (r+1) * C(k+1, r+1) is false.
    # k * C(k, r) = (k-r) * C(k, r) + r * C(k, r) = (k-r) C(k,r) + r C(k,r).
    # (k-r) C(k,r) = (k-r) k! / (r! (k-r)!) = k! / (r! (k-r-1)!) = (r+1) k! / ((r+1)! (k-r-1)!) = (r+1) C(k, r+1) ? No.
    # (k-r) C(k,r) = (k-r) * k! / (r! (k-r)!) = k! / (r! (k-r-1)!) = (r+1) * k! / ((r+1)! (k-r-1)!) = (r+1) C(k, r+1) is wrong dimension.
    # Correct: (k-r) C(k,r) = (k-r) * k! / (r! (k-r)!) = k! / (r! (k-r-1)!) = (r+1) * [ k! / ((r+1)! (k-r-1)!) ] = (r+1) C(k, r+1) ?
    # Let's check k=2, r=1. (2-1)C(2,1) = 1*2=2. (1+1)C(2,2) = 2*1=2. Yes.
    # So k C(k,r) = (r+1) C(k, r+1) + r C(k,r). This doesn't simplify sum easily.
    
    # Alternative: Use prefix sums of binomials.
    # Let F(dx, H) = sum_{dy=0}^H (H+1-dy) C(dx+dy, dx).
    # We can compute F(dx, H) for all dx in O(W+H) using recurrence or direct formula.
    # Direct formula:
    # sum_{j=0}^n C(r+j, j) = C(r+n+1, n)
    # sum_{j=0}^n j C(r+j, j) = ...
    # Let's just compute the total full paths using the O(W+H) method with precomputed sums.
    
    # Total = sum_{dx=0}^W (W-dx+1) * G(dx)
    # where G(dx) = sum_{dy=0}^H (H-dy+1) * C(dx+dy, dx)
    
    # We can compute G(dx) for all dx.
    # G(dx) = sum_{dy=0}^H (H+1) C(dx+dy, dx) - sum_{dy=0}^H dy C(dx+dy, dx)
    # Let S1(dx) = sum_{dy=0}^H C(dx+dy, dx) = C(dx+H+1, H)
    # Let S2(dx) = sum_{dy=0}^H dy C(dx+dy, dx)
    # dy C(dx+dy, dx) = (dx+dy - dx) C(dx+dy, dx) = (dx+dy) C(dx+dy, dx) - dx C(dx+dy, dx)
    # (dx+dy) C(dx+dy, dx) = (dx+dy) * (dx+dy)! / (dx! dy!) = (dx+dy+1-1) ...
    # Note: (k) C(k, r) = (r+1) C(k+1, r+1) - C(k, r) ? No.
    # k C(k, r) = (r+1) C(k+1, r+1) is false.
    # (k+1) C(k, r) = (r+1) C(k+1, r+1) + (k-r) C(k, r) ?
    # Standard identity: sum_{i=0}^n C(r+i, i) = C(r+n+1, n)
    # sum_{i=0}^n i C(r+i, i) = (r+1) C(r+n+2, n-1) ? No.
    # Let's use: i C(r+i, i) = (r+1) C(r+i+1, i+1) - C(r+i, i) ?
    # (r+1) C(r+i+1, i+1) = (r+1) (r+i+1)! / ((i+1)! r!) = (r+i+1)! / (i! r!) = (r+i+1) C(r+i, i)
    # So (r+1) C(r+i+1, i+1) = (r+i+1) C(r+i, i) = (r+1) C(r+i, i) + i C(r+i, i)
    # => i C(r+i, i) = (r+1) [ C(r+i+1, i+1) - C(r+i, i) ]
    # Sum_{i=0}^H i C(r+i, i) = (r+1) [ sum_{i=0}^H C(r+i+1, i+1) - sum_{i=0}^H C(r+i, i) ]
    # = (r+1) [ sum_{j=1}^{H+1} C(r+j, j) - sum_{i=0}^H C(r+i, i) ]
    # = (r+1) [ (C(r+H+2, H+1) - 1) - C(r+H+1, H) ] ?
    # sum_{j=0}^{H+1} C(r+j, j) = C(r+H+2, H+1). So sum_{j=1}^{H+1} = C(r+H+2, H+1) - C(r,0) = C(r+H+2, H+1) - 1.
    # So S2(dx) = (dx+1) * ( C(dx+H+2, H+1) - 1 - C(dx+H+1, H) )
    
    # G(dx) = (H+1) * C(dx+H+1, H) - S2(dx)
    
    total_full_paths = 0
    
    # Precompute C(dx+H+1, H) and C(dx+H+2, H+1) for dx in 0..W
    # We can just compute them on the fly.
    
    for dx in range(W + 1):
        # S1 = C(dx+H+1, H)
        s1 = nCr(dx + H + 1, H)
        
        # S2 = (dx+1) * ( C(dx+H+2, H+1) - 1 - C(dx+H+1, H) )
        c1 = nCr(dx + H + 2, H + 1)
        c2 = s1 # C(dx+H+1, H)
        s2 = ((dx + 1) * (c1 - 1 - c2)) % MOD
        
        g_dx = ((H + 1) * s1 - s2) % MOD
        
        term = (W - dx + 1) * g_dx % MOD
        total_full_paths = (total_full_paths + term) % MOD

    # Calculate Invalid Paths
    # Invalid = sum_{x=L+1}^R sum_{y=D+1}^U First(x,y) * End(x,y)
    # First(x,y) = S(L, y) + S(x, D)
    # S(u,v) = C(u+v+2, 2) - 1
    
    # We need to compute Sum_{x=L+1}^R Sum_{y=D+1}^U (S(L,y) + S(x,D)) * End(x,y)
    # = Sum_{x=L+1}^R Sum_{y=D+1}^U S(L,y) * End(x,y) + Sum_{x=L+1}^R Sum_{y=D+1}^U S(x,D) * End(x,y)
    
    # Term 1: Sum_{x=L+1}^R [ Sum_{y=D+1}^U S(L,y) * End(x,y) ]
    # Term 2: Sum_{y=D+1}^U [ Sum_{x=L+1}^R S(x,D) * End(x,y) ]
    
    # Let's compute Term 1
    term1 = 0
    # Precompute S(L, y) for y in D+1..U
    # S(L, y) = C(L+y+2, 2) - 1
    
    # We can iterate x and y, but that's O((R-L)*(U-D)) which can be 10^12.
    # We need to expand End(x,y) and sum.
    # End(x,y) = C(W-x + H-y + 2, 2) - 1
    # Let A = W-x, B = H-y. End = C(A+B+2, 2) - 1.
    # C(A+B+2, 2) = (A+B+2)(A+B+1)/2.
    
    # This expansion is complex. Given constraints W,H <= 10^6, the hole can be large.
    # However, we can swap sums.
    # Term 1 = Sum_{y=D+1}^U S(L,y) * [ Sum_{x=L+1}^R End(x,y) ]
    # Let H1(y) = Sum_{x=L+1}^R End(x,y)
    # End(x,y) = C(W-x + H-y + 2, 2) - 1
    # Let K = H-y. End(x,y) = C(W-x + K + 2, 2) - 1
    # Sum_{x=L+1}^R [ C(W-x + K + 2, 2) - 1 ]
    # Let j = W-x. As x goes L+1..R, j goes W-(L+1)..W-R.
    # Sum_{j=W-R}^{W-L-1} [ C(j + K + 2, 2) - 1 ]
    # = Sum_{j=W-R}^{W-L-1} C(j + K + 2, 2) - (R - L)
    
    # Sum_{j=A}^B C(j+C, 2) = Sum_{j=A}^B C(j+C, j+C-2)
    # Identity: Sum_{i=0}^n C(r+i, i) = C(r+n+1, n)
    # Sum_{j=A}^B C(j+C, 2) = Sum_{j=0}^B C(j+C, 2) - Sum_{j=0}^{A-1} C(j+C, 2)
    # Let F(N, C) = Sum_{j=0}^N C(j+C, 2)
    # C(j+C, 2) = C(j+C, j+C-2).
    # Sum_{j=0}^N C(j+C, j+C-2) = C(N+C+1, N+C-1) ? No.
    # Sum_{i=0}^n C(r+i, r) = C(r+n+1, r+1).
    # Here r=2. Sum_{j=0}^N C(j+2, 2) = C(N+3, 3).
    # But we have C(j+C, 2). Let k = j+C. Sum_{k=C}^{N+C} C(k, 2).
    # Sum_{k=0}^{M} C(k, 2) = C(M+1, 3).
    # So Sum_{j=0}^N C(j+C, 2) = Sum_{k=C}^{N+C} C(k, 2) = C(N+C+1, 3) - C(C, 3).
    
    # So H1(y) = [ C(W-L-1 + K + 1, 3) - C(W-R + K + 1, 3) ] - (R - L)
    # Wait, range is j from W-R to W-L-1.
    # Sum_{j=W-R}^{W-L-1} C(j+K+2, 2) = F(W-L-1, K+2) - F(W-R-1, K+2)
    # F(N, C) = C(N+C+1, 3) - C(C, 3) ? No, F(N, C) = Sum_{j=0}^N C(j+C, 2).
    # Let M = N+C. Sum_{k=C}^{M} C(k, 2) = C(M+1, 3) - C(C, 3).
    # So F(N, C) = C(N+C+1, 3) - C(C, 3).
    # Here C = K+2.
    # Sum_{j=0}^{W-L-1} C(j+K+2, 2) = C(W-L-1 + K + 2 + 1, 3) - C(K+2, 3)
    # = C(W-L+K+2, 3) - C(K+2, 3)
    # Sum_{j=0}^{W-R-1} C(j+K+2, 2) = C(W-R-1 + K + 2 + 1, 3) - C(K+2, 3)
    # = C(W-R+K+2, 3) - C(K+2, 3)
    # Difference = C(W-L+K+2, 3) - C(W-R+K+2, 3)
    
    # So H1(y) = C(W-L + H-y + 2, 3) - C(W-R + H-y + 2, 3) - (R - L)
    
    # Term 1 = Sum_{y=D+1}^U S(L,y) * H1(y)
    
    # Similarly for Term 2:
    # Term 2 = Sum_{x=L+1}^R S(x,D) * [ Sum_{y=D+1}^U End(x,y) ]
    # Let H2(x) = Sum_{y=D+1}^U End(x,y)
    # End(x,y) = C(W-x + H-y + 2, 2) - 1
    # Let K' = W-x. End(x,y) = C(K' + H-y + 2, 2) - 1
    # Sum_{y=D+1}^U C(K' + H-y + 2, 2) - (U - D)
    # Let j = H-y. y=D+1 => j=H-D-1. y=U => j=H-U.
    # Sum_{j=H-U}^{H-D-1} C(K' + j + 2, 2)
    # = F(H-D-1, K'+2) - F(H-U-1, K'+2)
    # = C(H-D-1 + K' + 2 + 1, 3) - C(H-U-1 + K' + 2 + 1, 3)
    # = C(H-D + K' + 2, 3) - C(H-U + K' + 2, 3)
    # H2(x) = C(H-D + W-x + 2, 3) - C(H-U + W-x + 2, 3) - (U - D)
    
    # Term 2 = Sum_{x=L+1}^R S(x,D) * H2(x)
    
    # We can compute Term 1 and Term 2 in O(U-D) and O(R-L) respectively.
    
    def sum_c3(n):
        return nCr(n, 3)

    # Term 1
    term1_val = 0
    for y in range(D + 1, U + 1):
        s_ly = (nCr(L + y + 2, 2) - 1 + MOD) % MOD
        
        k = H - y
        c1 = sum_c3(W - L + k + 2)
        c2 = sum_c3(W - R + k + 2)
        h1 = (c1 - c2 - (R - L)) % MOD
        
        term1_val = (term1_val + s_ly * h1) % MOD

    # Term 2
    term2_val = 0
    for x in range(L + 1, R + 1):
        s_xd = (nCr(x + D + 2, 2) - 1 + MOD) % MOD
        
        k = W - x
        c1 = sum_c3(H - D + k + 2)
        c2 = sum_c3(H - U + k + 2)
        h2 = (c1 - c2 - (U - D)) % MOD
        
        term2_val = (term2_val + s_xd * h2) % MOD

    invalid_paths = (term1_val + term2_val) % MOD

    ans = (total_full_paths - invalid_paths) % MOD
    print(ans)

solve()