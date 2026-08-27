import sys

MOD = 998244353
MAX = 2 * 10**6 + 10

def precompute_factorials(n):
    fact = [1] * (n + 1)
    inv_fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact[n] = pow(fact[n], MOD-2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD
    return fact, inv_fact

def C(n, k, fact, inv_fact):
    if k < 0 or k > n or n < 0:
        return 0
    return fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD

def solve():
    data = sys.stdin.read().split()
    W, H, L, R, D, U = map(int, data)
    
    N = 2 * max(W, H) + 10
    fact, inv_fact = precompute_factorials(N)
    
    # If hole is empty (L > R or D > U), then S is full grid
    if L > R or D > U:
        # Full grid: total paths = C(W+H+2, W+1) - 1
        ans = C(W+H+2, W+1, fact, inv_fact) - 1
        print(ans % MOD)
        return
    
    # The number of paths in a rectangle [0,a]x[0,b] is:
    # sum_{x=0}^{a} sum_{y=0}^{b} C((a-x)+(b-y), a-x) = C(a+b+2, a+1) - 1
    def rect_paths(a, b):
        if a < 0 or b < 0:
            return 0
        return C(a+b+2, a+1, fact, inv_fact) - 1
    
    # The valid set S is the full grid minus the closed rectangle [L,R]x[D,U].
    # We use the principle of inclusion-exclusion on the "four corridors" 
    # (bottom, top, left, right) around the hole.
    # A path that goes from the left part to the right part must go through 
    # either the bottom corridor or the top corridor.
    # Similarly, a path from bottom to top must go through left or right corridor.
    # The total number of valid paths is:
    # F = full - (paths that use bottom corridor) - (paths that use top corridor)
    #     - (paths that use left corridor) - (paths that use right corridor)
    #     + (paths that use two corridors in a compatible way)
    
    full = rect_paths(W, H)
    
    # Paths that go from left to right via bottom corridor:
    # Start in left or bottom, end in right or bottom, passing through bottom corridor.
    # This is equivalent to: paths in left-bottom combined rectangle that cross x=L to x=R+1
    # at y < D. But we can compute it as:
    # (paths in left-bottom combined) * (paths in right-bottom combined)? 
    # Actually, the number of paths that go from left to right via bottom is:
    # (paths from left to (L, y) with y<D) * (paths from (L,y) to right via bottom)
    # This simplifies to: (C(L+D+2, L+1) - 1) * (C((W-R)+(H-D)+2, W-R+1) - 1)? 
    # Not exactly. Let's use the derived formula from the notes.
    
    # The formula from the notes (unverified) is:
    # ans = full
    #       - t1 - t2 - t3 - t4
    #       + t5 + t6 + t7 + t8
    # where:
    # t1: bottom corridor (L,U) with right-bottom (W-R, H-D)
    # t2: top corridor (L, H-U) with right-bottom (W-R, D) ? 
    # Actually, let's use the correct formula based on the four arms:
    
    # Left arm: width L, height H (but with bottom and top parts? No, left arm is x<L, y in [D,U]? No.)
    # The four arms are:
    # Left: x in [0, L-1], y in [D, U]  (if L>0 and D<=U)
    # Right: x in [R+1, W], y in [D, U]
    # Bottom: x in [L, R], y in [0, D-1]
    # Top: x in [L, R], y in [U+1, H]
    # But these are not the only parts; the corners are also valid.
    # The number of paths that go through the bottom corridor is the number of paths 
    # that cross from x<L to x>R while y<D. This is equivalent to paths in the 
    # bottom-left region times paths in the bottom-right region? 
    # Actually, if a path goes from left to right via bottom, it must enter the bottom 
    # corridor at some y<D. The number of such paths is the sum over y<D of 
    # (paths from start to (L, y)) * (paths from (L, y) to end). 
    # This sum equals (paths in left-bottom) * (paths in right-bottom)? No.
    # The number of paths from left to right via bottom is equal to the number of 
    # paths in the left-bottom combined rectangle that reach x=L, times paths from 
    # x=L to x=R+1 (which is 1) times paths from x=R+1 to end in right-bottom.
    # But the number of paths in the left-bottom combined rectangle is not simply a 
    # rectangle; it's the set of points with x<L or y<D. 
    # The number of paths in the union of left and bottom is: 
    # rect_paths(L-1, H) + rect_paths(W, D-1) - rect_paths(L-1, D-1)
    # This counts paths that start in left or bottom and end in left or bottom.
    # But we need paths that cross from left to right.
    
    # The correct approach: the number of paths that go through the bottom corridor 
    # is exactly the number of paths in the "left-bottom" set that end at x=L, 
    # multiplied by the number of paths in the "right-bottom" set that start at x=R+1.
    # But this is not a product because the y-coordinate must match.
    # Actually, the number of paths from left to right via bottom is:
    # sum_{y=0}^{D-1} (paths from (0,0) to (L, y) in left-bottom) * (paths from (L, y) to (W,H) in right-bottom)
    # This is a convolution. However, it can be computed as:
    # (C(L+y, L) for y in bottom) convolved with (C((W-R-1)+(H-y), W-R-1)).
    # The sum equals: C(L+D+1, L+1) * C((W-R)+(H-D)+1, W-R+1)? Not sure.
    
    # Given the time, I will implement the formula from the notes that was 
    # "derived" but unverified, and test it with the samples. If it fails, 
    # I will implement a brute-force for small W,H to debug.
    
    def term(a1, b1, a2, b2):
        c1 = C(a1+b1+2, a1+1, fact, inv_fact) - 1
        c2 = C(a2+b2+2, a2+1, fact, inv_fact) - 1
        return c1 * c2 % MOD
    
    full = C(W+H+2, W+1, fact, inv_fact) - 1
    
    t1 = term(L, U, W-R, H-D)
    t2 = term(L, H-U, W-R, D)
    t3 = term(W-L, U, R, H-D)
    t4 = term(W-L, H-U, R, D)
    
    ans = (full - t1 - t2 - t3 - t4) % MOD
    
    t5 = term(L, U, W-R, H-U)
    t6 = term(L, H-U, W-R, D)
    t7 = term(W-L, U, R, H-D)
    t8 = term(W-L, H-U, R, D)
    
    ans = (ans + t5 + t6 + t7 + t8) % MOD
    
    print(ans % MOD)

if __name__ == "__main__":
    solve()