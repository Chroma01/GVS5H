import sys

MOD = 998244353
MAX = 2 * 10**6 + 10

fac = [1] * MAX
ifac = [1] * MAX
for i in range(1, MAX):
    fac[i] = fac[i-1] * i % MOD
ifac[MAX-1] = pow(fac[MAX-1], MOD-2, MOD)
for i in range(MAX-2, -1, -1):
    ifac[i] = ifac[i+1] * (i+1) % MOD

def C(n, k):
    if k < 0 or k > n:
        return 0
    return fac[n] * ifac[k] % MOD * ifac[n-k] % MOD

def solve():
    W, H, L, R, D, U = map(int, sys.stdin.readline().split())
    
    # Full grid total: G = sum_{x=0..W} sum_{y=0..H} (C(x+y+2, x+1) - 1)
    # = C(W+H+4, H+2) - (H+3) - (W+1)(H+2)
    G = C(W+H+4, H+2) - (H+3) - (W+1)*(H+2)
    G %= MOD
    
    # Subtract the paths that visit the hole using inclusion–exclusion on the four corners
    ans = G
    ans -= C(L+D+2, L+1) * C((W-R)+(H-U)+2, W-R+1) % MOD
    ans -= C(L+U+2, L+1) * C((W-R-1)+(H-D-1)+2, W-R-1+1) % MOD
    ans -= C(R+D+2, R+1) * C((W-L-1)+(H-U-1)+2, W-L-1+1) % MOD
    ans -= C(R+U+2, R+1) * C((W-L-1)+(H-D-1)+2, W-L-1+1) % MOD
    ans += 2 * C(L+U+2, L+1) % MOD * C(R+D+2, R+1) % MOD * C((W-L-1-R)+(H-U-1-D)+2, W-L-1-R+1) % MOD
    ans += 2 * C(R+U+2, R+1) % MOD * C(L+D+2, L+1) % MOD * C((W-L-1)+(H-U-1)+2, W-L-1+1) % MOD
    ans %= MOD
    
    print(ans)

if __name__ == "__main__":
    solve()