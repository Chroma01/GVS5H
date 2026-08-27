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

    # Function to calculate total paths in a grid of size w x h
    # Coordinates 0..w, 0..h
    # Sum_{dx=0 to w} Sum_{dy=0 to h} (w - dx + 1) * (h - dy + 1) * C(dx+dy, dx)
    def count_paths(w, h):
        if w < 0 or h < 0:
            return 0
        
        # We need to compute:
        # Sum_{dx=0}^w (w - dx + 1) * Sum_{dy=0}^h (h - dy + 1) * C(dx+dy, dx)
        
        # Let's precompute the inner sum for a fixed dx over all dy?
        # Or better, iterate dx and maintain a running sum for dy.
        
        # Let S(dx) = Sum_{dy=0}^h (h - dy + 1) * C(dx+dy, dx)
        # Then Total = Sum_{dx=0}^w (w - dx + 1) * S(dx)
        
        # We can compute S(dx) iteratively.
        # S(0) = Sum_{dy=0}^h (h - dy + 1) * C(dy, 0) = Sum_{k=1}^{h+1} k = (h+1)(h+2)/2
        
        # Relation between S(dx) and S(dx+1):
        # C(dx+1+dy, dx+1) = C(dx+dy, dx) + C(dx+dy, dx+1)
        # This might be complex. Let's just iterate. O(W+H) is fine since W,H <= 10^6.
        
        total = 0
        
        # Precompute terms for dy to avoid recomputing combinations repeatedly if possible?
        # Actually, for a fixed dx, we iterate dy. Total complexity O(W*H) is too slow.
        # We need O(W+H).
        
        # Let's use the identity:
        # Sum_{i=0}^n Sum_{j=0}^m C(i+j, i) = C(n+m+2, n+1) - 1 ? No.
        # Identity: Sum_{j=0}^m C(n+j, n) = C(n+m+1, n+1)
        
        # S(dx) = Sum_{dy=0}^h (h - dy + 1) * C(dx+dy, dx)
        # Let k = dy. S(dx) = Sum_{k=0}^h (h+1 - k) * C(dx+k, dx)
        # S(dx) = (h+1) * Sum_{k=0}^h C(dx+k, dx) - Sum_{k=0}^h k * C(dx+k, dx)
        
        # Term 1: Sum_{k=0}^h C(dx+k, dx) = C(dx+h+1, dx+1)
        
        # Term 2: Sum_{k=0}^h k * C(dx+k, dx)
        # Note: k * C(dx+k, dx) = (dx+k - dx) * C(dx+k, dx)
        # = (dx+k) * C(dx+k, dx) - dx * C(dx+k, dx)
        # = (dx+k) * (dx+k)! / (dx! k!) - dx * C(dx+k, dx)
        # = (dx+k)! / ((dx-1)! k!) - dx * C(dx+k, dx)  [if dx > 0]
        # = (dx+k) * C(dx+k-1, dx-1) ? No.
        # k * C(n, k) = n * C(n-1, k-1). Here n=dx+k.
        # k * C(dx+k, k) = (dx+k) * C(dx+k-1, k-1).
        # C(dx+k, dx) = C(dx+k, k).
        # So k * C(dx+k, dx) = (dx+k) * C(dx+k-1, dx).
        # This doesn't simplify nicely to a single binomial sum directly.
        
        # Alternative for Term 2:
        # Sum_{k=0}^h k * C(dx+k, dx)
        # Let j = k. Sum_{j=0}^h j * C(dx+j, dx)
        # Use identity: Sum_{i=r}^n C(i, r) = C(n+1, r+1)
        # We know C(dx+k, dx) = C(dx+k, k).
        # k * C(dx+k, k) = (dx+k) * C(dx+k-1, k-1) ? No.
        # k * C(n, k) = n * C(n-1, k-1). Here n=dx+k.
        # k * C(dx+k, k) = (dx+k) * C(dx+k-1, k-1).
        # So Sum_{k=1}^h (dx+k) * C(dx+k-1, k-1)
        # = dx * Sum_{k=1}^h C(dx+k-1, k-1) + Sum_{k=1}^h (k) * C(dx+k-1, k-1) ? No, the coefficient is (dx+k).
        # = dx * Sum_{j=0}^{h-1} C(dx+j, j) + Sum_{j=0}^{h-1} (j+1) * C(dx+j, j)
        # This is getting recursive.
        
        # Let's stick to the O(W+H) iterative calculation of S(dx).
        # S(dx) = Sum_{dy=0}^h (h - dy + 1) * C(dx+dy, dx)
        # S(dx+1) = Sum_{dy=0}^h (h - dy + 1) * C(dx+1+dy, dx+1)
        # C(dx+1+dy, dx+1) = C(dx+dy, dx+1) + C(dx+dy, dx)
        # This doesn't help directly.
        
        # Let's compute S(dx) for all dx in O(H) each? No, O(W*H).
        # We need a faster way.
        
        # Let's expand the total sum:
        # Total = Sum_{dx=0}^w Sum_{dy=0}^h (w - dx + 1)(h - dy + 1) C(dx+dy, dx)
        # Let i = dx, j = dy.
        # Total = Sum_{i=0}^w Sum_{j=0}^h (w+1-i)(h+1-j) C(i+j, i)
        
        # We can swap sums or use generating functions.
        # Let A_i = w+1-i, B_j = h+1-j.
        # Total = Sum_{i=0}^w A_i Sum_{j=0}^h B_j C(i+j, i)
        
        # Let T_i = Sum_{j=0}^h B_j C(i+j, i)
        # T_i = Sum_{j=0}^h (h+1-j) C(i+j, i)
        # T_i = (h+1) Sum_{j=0}^h C(i+j, i) - Sum_{j=0}^h j C(i+j, i)
        
        # Sum_{j=0}^h C(i+j, i) = C(i+h+1, i+1)
        
        # Sum_{j=0}^h j C(i+j, i)
        # Note j C(i+j, i) = j * (i+j)! / (i! j!) = (i+j)! / (i! (j-1)!)
        # = (i+1) * (i+j)! / ((i+1)! (j-1)!) + (j-1) * ... ?
        # j C(i+j, i) = (i+j) C(i+j-1, i) ? No.
        # j C(i+j, i) = (i+j) C(i+j-1, i) - i C(i+j-1, i) ?
        # C(i+j, i) = C(i+j-1, i) + C(i+j-1, i-1)
        # j C(i+j, i) = j C(i+j-1, i) + j C(i+j-1, i-1)
        
        # Let's use the identity: Sum_{k=0}^n k C(r+k, k) = (n+1) C(r+n+1, n-1) ? No.
        # Known identity: Sum_{k=0}^n C(r+k, k) = C(r+n+1, n)
        # Sum_{k=0}^n k C(r+k, k) = (n+1) C(r+n+1, n-1) ? Let's check for small n.
        # n=1, r=0: Sum = 0*C(0,0) + 1*C(1,1) = 1. Formula: 2*C(2,0) = 2. No.
        # Correct identity: Sum_{k=0}^n k C(r+k, k) = (n+1) C(r+n+1, n-1) is wrong.
        # Actually, Sum_{k=0}^n k C(r+k, r) = (n+1) C(r+n+1, r+1) - C(r+n+2, r+2) ?
        
        # Let's just compute T_i iteratively.
        # T_i = Sum_{j=0}^h (h+1-j) C(i+j, i)
        # T_{i+1} = Sum_{j=0}^h (h+1-j) C(i+1+j, i+1)
        # C(i+1+j, i+1) = C(i+j, i+1) + C(i+j, i)
        # T_{i+1} = Sum_{j=0}^h (h+1-j) [C(i+j, i+1) + C(i+j, i)]
        # = Sum_{j=0}^h (h+1-j) C(i+j, i+1) + T_i
        
        # Let U_i = Sum_{j=0}^h (h+1-j) C(i+j, i+1)
        # This seems to shift the problem.
        
        # Given the constraints and time, let's use the O(W+H) direct summation with precomputed factorials.
        # We can compute the double sum by iterating i from 0 to w, and maintaining the sum over j.
        # But the term C(i+j, i) changes with i.
        
        # Let's use the property:
        # Sum_{j=0}^h (h+1-j) C(i+j, i)
        # = Sum_{k=i}^{i+h} (h+1 - (k-i)) C(k, i)
        # = Sum_{k=i}^{i+h} (h+1+i-k) C(k, i)
        # = (h+1+i) Sum_{k=i}^{i+h} C(k, i) - Sum_{k=i}^{i+h} k C(k, i)
        
        # Sum_{k=i}^{i+h} C(k, i) = C(i+h+1, i+1)
        
        # Sum_{k=i}^{i+h} k C(k, i)
        # k C(k, i) = k * k! / (i! (k-i)!)
        # = (i+1) * (k! / ((i+1)! (k-i-1)!)) + (k-i) * ... ?
        # k C(k, i) = (i+1) C(k, i+1) + i C(k, i) ?
        # (i+1) C(k, i+1) + i C(k, i) = (i+1) k! / ((i+1)! (k-i-1)!) + i k! / (i! (k-i)!)
        # = k! / (i! (k-i-1)!) + i k! / (i! (k-i)!)
        # = k! / (i! (k-i-1)!) [ 1 + i/(k-i) ]
        # = k! / (i! (k-i-1)!) [ (k-i+i)/(k-i) ] = k! / (i! (k-i-1)!) * k/(k-i)
        # This is not k C(k, i).
        
        # Correct identity: k C(k, i) = (i+1) C(k, i+1) + i C(k, i) is FALSE.
        # k C(k, i) = (i+1) C(k+1, i+1) - (i+1) C(k, i+1) ? No.
        # k C(k, i) = (i+1) C(k, i+1) + i C(k, i) -> Let's test k=2, i=1.
        # 2 C(2,1) = 4.
        # 2 C(2,2) + 1 C(2,1) = 2*1 + 1*2 = 4. It works!
        # So k C(k, i) = (i+1) C(k, i+1) + i C(k, i).
        
        # Sum_{k=i}^{i+h} k C(k, i) = (i+1) Sum_{k=i}^{i+h} C(k, i+1) + i Sum_{k=i}^{i+h} C(k, i)
        # Sum_{k=i}^{i+h} C(k, i) = C(i+h+1, i+1)
        # Sum_{k=i}^{i+h} C(k, i+1) = C(i+h+1, i+2)
        
        # So Sum_{k=i}^{i+h} k C(k, i) = (i+1) C(i+h+1, i+2) + i C(i+h+1, i+1)
        
        # Therefore, T_i = (h+1+i) C(i+h+1, i+1) - [ (i+1) C(i+h+1, i+2) + i C(i+h+1, i+1) ]
        # T_i = (h+1) C(i+h+1, i+1) - (i+1) C(i+h+1, i+2)
        
        # Now Total = Sum_{i=0}^w (w+1-i) T_i
        # Total = Sum_{i=0}^w (w+1-i) [ (h+1) C(i+h+1, i+1) - (i+1) C(i+h+1, i+2) ]
        
        # This can be computed in O(W) time.
        
        total_sum = 0
        
        for i in range(w + 1):
            # Calculate T_i
            # Term1 = (h+1) * C(i+h+1, i+1)
            term1 = ((h + 1) * nCr(i + h + 1, i + 1)) % MOD
            
            # Term2 = (i+1) * C(i+h+1, i+2)
            term2 = ((i + 1) * nCr(i + h + 1, i + 2)) % MOD
            
            Ti = (term1 - term2 + MOD) % MOD
            
            # Add to total
            coeff = (w + 1 - i) % MOD
            total_sum = (total_sum + coeff * Ti) % MOD
            
        return total_sum

    # Define the 4 rectangles
    # 1. Left: x in [0, L-1], y in [0, H] -> Width L-1, Height H
    # 2. Right: x in [R, W], y in [0, H] -> Width W-R, Height H
    # 3. Bottom: x in [0, W], y in [0, D-1] -> Width W, Height D-1
    # 4. Top: x in [0, W], y in [U, H] -> Width W, Height H-U
    
    # Intersections:
    # Left & Bottom: x in [0, L-1], y in [0, D-1] -> Width L-1, Height D-1
    # Left & Top: x in [0, L-1], y in [U, H] -> Width L-1, Height H-U
    # Right & Bottom: x in [R, W], y in [0, D-1] -> Width W-R, Height D-1
    # Right & Top: x in [R, W], y in [U, H] -> Width W-R, Height H-U
    
    # All other intersections are empty (e.g., Left & Right is empty)
    
    def get_rect(w, h):
        return count_paths(w, h)

    # Single rectangles
    s1 = get_rect(L - 1, H)
    s2 = get_rect(W - R, H)
    s3 = get_rect(W, D - 1)
    s4 = get_rect(W, H - U)
    
    # Pair intersections
    s12 = get_rect(L - 1, D - 1) # Left & Bottom
    s13 = get_rect(L - 1, H - U) # Left & Top
    s23 = get_rect(W - R, D - 1) # Right & Bottom
    s24 = get_rect(W - R, H - U) # Right & Top
    
    # Note: s12 is Left & Bottom. s13 is Left & Top.
    # s23 is Right & Bottom. s24 is Right & Top.
    
    # PIE: Sum singles - Sum pairs
    ans = (s1 + s2 + s3 + s4) % MOD
    ans = (ans - s12 - s13 - s23 - s24) % MOD
    ans = (ans + MOD) % MOD # Ensure positive
    
    print(ans)

solve()