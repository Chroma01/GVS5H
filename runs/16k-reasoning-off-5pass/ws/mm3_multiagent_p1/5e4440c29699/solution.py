import sys

MOD = 998244353
MAX = 2 * 10**6 + 10

# Precompute factorials and inverse factorials
fact = [1] * (MAX + 1)
for i in range(1, MAX + 1):
    fact[i] = fact[i-1] * i % MOD

inv_fact = [1] * (MAX + 1)
inv_fact[MAX] = pow(fact[MAX], MOD-2, MOD)
for i in range(MAX, 0, -1):
    inv_fact[i-1] = inv_fact[i] * i % MOD

def C(n, k):
    if k < 0 or k > n or n < 0:
        return 0
    return fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD

def solve():
    W, H, L, R, D, U = map(int, sys.stdin.read().split())
    
    # Number of paths from (0,0) to (W,H) avoiding rectangle [L,R]x[D,U]
    # Using inclusion-exclusion over the four corners of the forbidden rectangle.
    # The formula comes from the reflection principle / Lindström-Gessel-Viennot lemma.
    
    ans = 0
    
    # Term 1: C(W+H, W) - total paths in full grid
    ans = C(W+H, W)
    
    # Subtract paths that go through the four entry points on the rectangle boundary
    
    # Term 2: paths entering at bottom-left corner (L, D)
    ans = (ans - C(L+D, L) * C((W-R)+(H-D), W-R)) % MOD
    
    # Term 3: paths entering at top-left corner (L, U+1) 
    ans = (ans - C(L+U+1, L) * C((W-R)+(H-U-1), W-R)) % MOD
    
    # Term 4: paths entering at bottom-right corner (R+1, D)
    ans = (ans - C(R+D+1, R+1) * C((W-R-1)+(H-D), W-R-1)) % MOD
    
    # Term 5: paths entering at top-right corner (R+1, U+1)
    ans = (ans - C(R+U+2, R+1) * C((W-R-1)+(H-U-1), W-R-1)) % MOD
    
    # Add back detour paths that go around the rectangle
    
    # Term 6: + C(L+D, L) * C((R-L)+(U-D), R-L) * C((W-R)+(H-U), W-R)
    ans = (ans + C(L+D, L) * C((R-L)+(U-D), R-L) % MOD * C((W-R)+(H-U), W-R)) % MOD
    
    # Term 7: + C(L+U+1, L) * C((R-L)+(U-D), R-L) * C((W-R)+(H-D), W-R)
    ans = (ans + C(L+U+1, L) * C((R-L)+(U-D), R-L) % MOD * C((W-R)+(H-D), W-R)) % MOD
    
    # Term 8: + C(R+D+1, R+1) * C((R-L)+(U-D), U-D) * C((W-L)+(H-U-1), W-L)
    ans = (ans + C(R+D+1, R+1) * C((R-L)+(U-D), U-D) % MOD * C((W-L)+(H-U-1), W-L)) % MOD
    
    # Term 9: + C(R+U+2, R+1) * C((R-L)+(U-D), U-D) * C((W-L)+(H-D), W-L)
    ans = (ans + C(R+U+2, R+1) * C((R-L)+(U-D), U-D) % MOD * C((W-L)+(H-D), W-L)) % MOD
    
    # Subtract double-counted terms (paths going around two sides)
    
    # Term 10: - C(R+D+1, R+1) * C((R-L)+(U-D), R-L) * C((W-L)+(H-U-1), W-L)
    ans = (ans - C(R+D+1, R+1) * C((R-L)+(U-D), R-L) % MOD * C((W-L)+(H-U-1), W-L)) % MOD
    
    # Term 11: - C(L+U+1, L) * C((R-L)+(U-D), U-D) * C((W-R)+(H-D), W-R)
    ans = (ans - C(L+U+1, L) * C((R-L)+(U-D), U-D) % MOD * C((W-R)+(H-D), W-R)) % MOD
    
    print(ans % MOD)

solve()