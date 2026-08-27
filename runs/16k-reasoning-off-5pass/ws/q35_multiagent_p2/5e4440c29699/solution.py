import sys

# Set recursion depth just in case, though we won't use recursion
sys.setrecursionlimit(2000)

def solve():
    # Read input
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
    MAX_N = W + H + 10
    fact = [1] * MAX_N
    inv_fact = [1] * MAX_N
    
    for i in range(1, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv_fact[MAX_N-1] = pow(fact[MAX_N-1], MOD-2, MOD)
    for i in range(MAX_N-2, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i+1)) % MOD
        
    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv_fact[r] * inv_fact[n-r]) % MOD
        return (num * den) % MOD

    # Function to calculate sum of paths from (0,0) to (x,y)
    # N(0,0 -> x,y) = C(x+y, x)
    # But we need sum over all S <= E.
    # Let's define a helper to compute sum of paths from any S in [0, x1]x[0, y1] to a fixed E=(x2, y2)
    # Sum_{x1=0..x2, y1=0..y2} C((x2-x1)+(y2-y1), x2-x1)
    # Let dx = x2-x1, dy = y2-y1.
    # Sum_{dx=0..x2, dy=0..y2} C(dx+dy, dx)
    # This sum is equal to C(x2+y2+2, x2+1) - 1? No.
    # Identity: Sum_{i=0..n} Sum_{j=0..m} C(i+j, i) = C(n+m+2, n+1) - 1?
    # Let's verify for small n,m.
    # n=1, m=1:
    # i=0,j=0: C(0,0)=1
    # i=0,j=1: C(1,0)=1
    # i=1,j=0: C(1,1)=1
    # i=1,j=1: C(2,1)=2
    # Sum = 5.
    # Formula: C(1+1+2, 1+1) - 1 = C(4,2)-1 = 6-1=5. Correct.
    # So Sum_{dx=0..x2, dy=0..y2} C(dx+dy, dx) = C(x2+y2+2, x2+1) - 1.
    
    def sum_paths_to(x, y):
        # Sum of paths from any S in [0,x]x[0,y] to (x,y)
        # This is equivalent to sum_{dx=0..x, dy=0..y} C(dx+dy, dx)
        return (nCr(x + y + 2, x + 1) - 1 + MOD) % MOD

    # Total paths in full grid [0,W]x[0,H]
    # Sum over all E=(x,y) in [0,W]x[0,H] of sum_paths_to(x,y)
    # We can compute this by iterating x and y.
    # Total = Sum_{x=0..W} Sum_{y=0..H} (C(x+y+2, x+1) - 1)
    
    # To optimize, we can precompute row sums or just iterate since W,H <= 10^6 is too big for O(WH).
    # We need O(W+H).
    # Let S(x,y) = C(x+y+2, x+1) - 1.
    # Total = Sum_{x=0..W} Sum_{y=0..H} S(x,y).
    
    # Let's compute Sum_{y=0..H} C(x+y+2, x+1).
    # Identity: Sum_{i=0..n} C(r+i, r) = C(r+n+1, r+1).
    # Here, let k = x+1. We want Sum_{y=0..H} C(k+y+1, k).
    # Let j = y+1. Sum_{j=1..H+1} C(k+j, k).
    # Sum_{j=0..H+1} C(k+j, k) = C(k+H+2, k+1).
    # So Sum_{y=0..H} C(x+y+2, x+1) = C(x+H+2, x+1) - C(x+1, x+1) = C(x+H+2, x+1) - 1.
    
    # So Sum_{y=0..H} S(x,y) = C(x+H+2, x+1) - 1 - (H+1).
    # Total = Sum_{x=0..W} [ C(x+H+2, x+1) - H - 2 ].
    
    # Now Sum_{x=0..W} C(x+H+2, x+1).
    # Let k = H+2. Sum_{x=0..W} C(k+x, x+1).
    # Let j = x+1. Sum_{j=1..W+1} C(k+j-1, j).
    # This doesn't have a simple closed form like the previous one.
    # However, we can compute the sum iteratively or use another identity.
    # Sum_{i=0..n} C(r+i, i) = C(r+n+1, n).
    # Here we have C(H+2+x, x+1).
    # Let's just compute the sum in O(W) or O(H).
    
    # Let's compute Total directly using the derived formula for inner sum:
    # InnerSum(x) = C(x+H+2, x+1) - H - 2
    # Total = Sum_{x=0..W} InnerSum(x)
    
    total_full = 0
    for x in range(W + 1):
        term = (nCr(x + H + 2, x + 1) - H - 2) % MOD
        total_full = (total_full + term) % MOD
        
    # Now compute Bad paths (paths that touch the hole [L,R]x[D,U])
    # Bad = Sum_{P in Entry} WaysToHit(P) * SuffixSum(P)
    
    # Entry points:
    # Left edge: P_L = (L, y) for y in [D, U]
    # Bottom edge: P_B = (x, D) for x in [L, R]
    
    # WaysToHit(P) for P=(L,y), y>D:
    # A_L[y] = (Sum_{S in [0,L]x[0,y], S avoids H\{P}} Paths(S->P))
    # As derived, this is:
    # A_L[y] = (Sum_{dx=0..L, dy=0..y} C(dx+dy, dx) avoiding H\{P})
    # Since P=(L,y) is on the left edge, and we assume it's the first hit,
    # the path must stay in x <= L and not touch (L, y') for D <= y' < y.
    # This is equivalent to:
    # Total paths from S in [0,L]x[0,y] to (L,y) MINUS paths that hit (L, y') for D<=y'<y first.
    # Let T_L[y] = Sum_{S in [0,L]x[0,y]} Paths(S->(L,y))
    # T_L[y] = Sum_{dx=0..L, dy=0..y} C(dx+dy, dx)
    # Using the identity: Sum_{dx=0..L, dy=0..y} C(dx+dy, dx) = C(L+y+2, L+1) - 1.
    
    # So A_L[y] = T_L[y] - Sum_{y'=D}^{y-1} A_L[y'] * Paths((L,y') -> (L,y))
    # Paths((L,y') -> (L,y)) = C((L-L)+(y-y'), L-L) = C(y-y', 0) = 1.
    # So A_L[y] = T_L[y] - Sum_{y'=D}^{y-1} A_L[y'].
    
    # Similarly for Bottom edge:
    # A_B[x] = T_B[x] - Sum_{x'=L}^{x-1} A_B[x'] * Paths((x',D) -> (x,D))
    # Paths((x',D) -> (x,D)) = C(x-x', 0) = 1.
    # T_B[x] = Sum_{S in [0,x]x[0,D]} Paths(S->(x,D)) = C(x+D+2, x+1) - 1.
    
    # We can compute A_L and A_B in O(U-D) and O(R-L) respectively.
    
    # SuffixSum(P) for P=(x,y):
    # Sum_{E in Valid, E >= P} Paths(P->E)
    # Valid E are in [0,W]x[0,H] \ [L,R]x[D,U].
    # E >= P means x_E >= x, y_E >= y.
    # So E is in [x, W]x[y, H] \ ([L,R]x[D,U] intersected with [x,W]x[y,H]).
    # Since P is on the boundary of the hole, the intersection is the part of the hole "above/right" of P.
    # If P=(L,y) with y>=D, the hole part is [L,R]x[max(D,y), U].
    # If P=(x,D) with x>=L, the hole part is [max(L,x), R]x[D,U].
    
    # Let's compute SuffixSum(P) = Total paths from P to any E in [x,W]x[y,H] MINUS paths from P to any E in HolePart.
    # Total paths from P to any E in [x,W]x[y,H]:
    # Let dx = x_E - x, dy = y_E - y.
    # Sum_{dx=0..W-x, dy=0..H-y} C(dx+dy, dx) = C((W-x)+(H-y)+2, (W-x)+1) - 1.
    
    # Paths from P to any E in HolePart:
    # HolePart is a rectangle [x1, x2]x[y1, y2].
    # We need Sum_{E in HolePart} Paths(P->E).
    # This is Sum_{x_E=x1..x2, y_E=y1..y2} C((x_E-x)+(y_E-y), x_E-x).
    # Let dx = x_E-x, dy = y_E-y.
    # Sum_{dx=x1-x..x2-x, dy=y1-y..y2-y} C(dx+dy, dx).
    # This can be computed using 2D prefix sums of binomials or inclusion-exclusion on the rectangle sum.
    # Let F(a,b) = Sum_{dx=0..a, dy=0..b} C(dx+dy, dx) = C(a+b+2, a+1) - 1.
    # Sum_{dx=a1..a2, dy=b1..b2} C(dx+dy, dx) = F(a2,b2) - F(a1-1,b2) - F(a2,b1-1) + F(a1-1,b1-1).
    
    def sum_paths_rect(x_start, y_start, x_end, y_end):
        # Sum of paths from (x_start, y_start) to any (x,y) in [x_start, x_end]x[y_start, y_end]
        # Let dx = x - x_start, dy = y - y_start.
        # Sum_{dx=0..x_end-x_start, dy=0..y_end-y_start} C(dx+dy, dx)
        a = x_end - x_start
        b = y_end - y_start
        if a < 0 or b < 0:
            return 0
        return (nCr(a + b + 2, a + 1) - 1 + MOD) % MOD

    def sum_paths_rect_inclusion(x1, y1, x2, y2, x3, y3, x4, y4):
        # Sum in [x1,x2]x[y1,y2] minus [x3,x4]x[y3,y4]
        # Assuming [x3,x4]x[y3,y4] is inside [x1,x2]x[y1,y2]
        s1 = sum_paths_rect(x1, y1, x2, y2)
        s2 = sum_paths_rect(x3, y3, x4, y4)
        return (s1 - s2 + MOD) % MOD

    # Compute A_L
    A_L = {}
    current_sum_A_L = 0
    for y in range(D, U + 1):
        # T_L[y] = C(L+y+2, L+1) - 1
        t_l = (nCr(L + y + 2, L + 1) - 1 + MOD) % MOD
        a_l = (t_l - current_sum_A_L + MOD) % MOD
        A_L[y] = a_l
        current_sum_A_L = (current_sum_A_L + a_l) % MOD
        
    # Compute A_B
    A_B = {}
    current_sum_A_B = 0
    for x in range(L, R + 1):
        # T_B[x] = C(x+D+2, x+1) - 1
        t_b = (nCr(x + D + 2, x + 1) - 1 + MOD) % MOD
        a_b = (t_b - current_sum_A_B + MOD) % MOD
        A_B[x] = a_b
        current_sum_A_B = (current_sum_A_B + a_b) % MOD
        
    # Compute Bad
    bad = 0
    
    # For Left Edge
    for y in range(D, U + 1):
        P = (L, y)
        # SuffixSum(P) = Paths from P to Valid E >= P
        # Valid E >= P are in [L, W]x[y, H] \ ([L,R]x[max(D,y), U])
        # Since y >= D, max(D,y) = y.
        # Hole part is [L, R]x[y, U].
        # But we must intersect with [L, W]x[y, H].
        # Hole part in valid range: [L, min(R,W)]x[y, min(U,H)].
        # Since R<=W and U<=H, it's [L, R]x[y, U].
        
        # Total paths from P to [L,W]x[y,H]
        total_suffix = sum_paths_rect(L, y, W, H)
        
        # Paths from P to HolePart [L,R]x[y,U]
        hole_suffix = sum_paths_rect(L, y, R, U)
        
        suffix_sum = (total_suffix - hole_suffix + MOD) % MOD
        
        bad = (bad + A_L[y] * suffix_sum) % MOD
        
    # For Bottom Edge
    for x in range(L, R + 1):
        P = (x, D)
        # SuffixSum(P) = Paths from P to Valid E >= P
        # Valid E >= P are in [x, W]x[D, H] \ ([max(L,x), R]x[D, U])
        # Since x >= L, max(L,x) = x.
        # Hole part is [x, R]x[D, U].
        
        # Total paths from P to [x,W]x[D,H]
        total_suffix = sum_paths_rect(x, D, W, H)
        
        # Paths from P to HolePart [x,R]x[D,U]
        hole_suffix = sum_paths_rect(x, D, R, U)
        
        suffix_sum = (total_suffix - hole_suffix + MOD) % MOD
        
        bad = (bad + A_B[x] * suffix_sum) % MOD
        
    # Overlap: (L,D) is counted in both A_L and A_B.
    # We need to subtract the double counting.
    # The term for (L,D) in Left Edge loop:
    # A_L[D] * SuffixSum((L,D))
    # The term for (L,D) in Bottom Edge loop:
    # A_B[L] * SuffixSum((L,D))
    # But A_L[D] and A_B[L] are both equal to T_L[D] = T_B[L] = C(L+D+2, L+1)-1.
    # And SuffixSum is the same.
    # So we subtracted it twice? No, we added it twice.
    # We should have added it once.
    # So subtract one instance.
    
    P0 = (L, D)
    # Recalculate A_L[D] and A_B[L]
    t_0 = (nCr(L + D + 2, L + 1) - 1 + MOD) % MOD
    a_0 = t_0 # Since sum before D is 0
    
    total_suffix_0 = sum_paths_rect(L, D, W, H)
    hole_suffix_0 = sum_paths_rect(L, D, R, U)
    suffix_sum_0 = (total_suffix_0 - hole_suffix_0 + MOD) % MOD
    
    overlap = (a_0 * suffix_sum_0) % MOD
    bad = (bad - overlap + MOD) % MOD
    
    ans = (total_full - bad + MOD) % MOD
    print(ans)

solve()