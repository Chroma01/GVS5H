import sys

MOD = 998244353

def solve():
    input = sys.stdin.readline
    N, Q = map(int, input().split())
    A = [0] * (N + 1)
    if N >= 2:
        A_list = list(map(int, input().split()))
        for i in range(2, N + 1):
            A[i] = A_list[i - 2]
    
    # Precompute modular inverses
    inv = [0] * (N + 2)
    if N >= 1:
        inv[1] = 1
    for i in range(2, N + 2):
        inv[i] = MOD - MOD // i * inv[MOD % i] % MOD
    
    # Precompute factorial (N-1)!
    fact = 1
    for i in range(2, N):
        fact = fact * i % MOD
    
    # Precompute prefix sums
    pre1 = [0] * (N + 1)  # sum of A_i * 2(i-1)/(i(i+1)) for i=2..x
    pre2 = [0] * (N + 1)  # sum of A_i / i for i=2..x
    
    for i in range(2, N + 1):
        # c1(i) = 2*(i-1) * inv[i] * inv[i+1] % MOD
        c1 = 2 * (i - 1) % MOD * inv[i] % MOD * inv[i + 1] % MOD
        pre1[i] = (pre1[i - 1] + A[i] * c1) % MOD
        # c2(i) = inv[i]
        c2 = inv[i]
        pre2[i] = (pre2[i - 1] + A[i] * c2) % MOD
    
    # Process queries
    out_lines = []
    for _ in range(Q):
        u, v = map(int, input().split())
        if u == 1:
            sum2 = pre2[v - 1] if v - 1 >= 2 else 0
            ans = fact * (sum2 + A[v]) % MOD
        else:
            sum1 = pre1[u]
            if v - 1 > u:
                sum2 = (pre2[v - 1] - pre2[u]) % MOD
            else:
                sum2 = 0
            ans = fact * (sum1 + sum2 + A[v]) % MOD
        out_lines.append(str(ans % MOD))
    
    print('\n'.join(out_lines))

if __name__ == "__main__":
    solve()