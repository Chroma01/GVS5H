import sys

def solve():
    import sys
    input = sys.stdin.readline
    MOD = 998244353
    N, Q = map(int, input().split())
    A = [0] * (N + 1)
    A_list = list(map(int, input().split()))
    for i in range(2, N + 1):
        A[i] = A_list[i - 2]
    
    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - MOD // i * inv[MOD % i] % MOD
    
    prefix = [0] * (N + 1)
    for i in range(2, N + 1):
        prefix[i] = (prefix[i-1] + A[i] * inv[i]) % MOD
    
    fact = [1] * (N + 1)
    for i in range(2, N + 1):
        fact[i] = fact[i-1] * i % MOD
    total_trees = fact[N-1]
    
    out_lines = []
    for _ in range(Q):
        u, v = map(int, input().split())
        if u > v:
            u, v = v, u
        if u == v:
            out_lines.append("0")
            continue
        
        if u == 1:
            ans = total_trees * (prefix[v-1] - prefix[1]) % MOD
            out_lines.append(str(ans))
            continue
        
        sum1 = prefix[u-1]
        sum2 = (prefix[v-1] - prefix[u-1]) % MOD
        
        coeff = (2 - 4 * inv[u]) % MOD
        part1 = coeff * sum1 % MOD
        total = (part1 + sum2) % MOD
        ans = total_trees * total % MOD
        out_lines.append(str(ans))
    
    sys.stdout.write("\n".join(out_lines) + "\n")

if __name__ == "__main__":
    solve()