import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    N = int(next(it))
    Q = int(next(it))
    A = [0] * (N + 1)  # 1-indexed
    for i in range(2, N + 1):
        A[i] = int(next(it))
    
    # Precompute factorial (N-1)! mod MOD
    fact = [1] * (N + 1)
    for i in range(2, N + 1):
        fact[i] = fact[i-1] * i % MOD
    
    # Precompute modular inverses up to N
    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - MOD // i * inv[MOD % i] % MOD
    
    # Prefix sums: prefix_A[i] = sum_{k=2}^{i} A_k mod MOD
    prefix_A = [0] * (N + 1)
    for i in range(2, N + 1):
        prefix_A[i] = (prefix_A[i-1] + A[i]) % MOD
    
    # Prefix sums: prefix_Adiv[i] = sum_{k=2}^{i} A_k * inv(k) mod MOD
    prefix_Adiv = [0] * (N + 1)
    for i in range(2, N + 1):
        prefix_Adiv[i] = (prefix_Adiv[i-1] + A[i] * inv[i]) % MOD
    
    total_fact = fact[N-1]  # (N-1)! mod MOD
    
    out_lines = []
    for _ in range(Q):
        u = int(next(it))
        v = int(next(it))
        if u > v:
            u, v = v, u
        
        # ans = total_fact * (A_u + A_v + sum_{i=u+1}^{v-1} A_i * inv(i) + (1/u) * sum_{i=2}^{u-1} A_i) mod MOD
        part = (A[u] + A[v]) % MOD
        if u + 1 <= v - 1:
            part = (part + (prefix_Adiv[v-1] - prefix_Adiv[u])) % MOD
        if u >= 3:  # there exists i from 2 to u-1
            sum_A_lower = (prefix_A[u-1] - prefix_A[1]) % MOD
            part = (part + sum_A_lower * inv[u]) % MOD
        
        ans = total_fact * part % MOD
        out_lines.append(str(ans))
    
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()