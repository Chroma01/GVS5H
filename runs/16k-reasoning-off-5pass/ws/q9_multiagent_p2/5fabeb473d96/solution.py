import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    # A is 1-indexed in problem description for A_2...A_N
    # We will store A such that A[i] corresponds to A_i (weight of edge i -> P_i)
    # Input gives A_2, A_3, ..., A_N
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(next(iterator))
    
    queries = []
    for _ in range(Q):
        u = int(next(iterator))
        v = int(next(iterator))
        queries.append((u, v))

    MOD = 998244353

    # Precompute factorials and inverse factorials
    # We need factorials up to N
    fact = [1] * (N + 1)
    inv = [1] * (N + 1)
    
    for i in range(2, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, 1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    # Precompute prefix sums of A to answer range sum queries in O(1)
    # We need sum of A[k] for k in range [L, R]
    # Let's define prefix_sum_A[i] = sum(A[2]...A[i])
    # Then sum(L, R) = prefix_sum_A[R] - prefix_sum_A[L-1]
    
    prefix_sum_A = [0] * (N + 1)
    current_sum = 0
    for i in range(2, N + 1):
        current_sum = (current_sum + A[i]) % MOD
        prefix_sum_A[i] = current_sum
        
    def get_sum_A(l, r):
        if l > r:
            return 0
        res = (prefix_sum_A[r] - prefix_sum_A[l-1]) % MOD
        return res

    # Precompute modular inverse harmonic sums
    # H_inv[i] = sum(inv[k] for k in 1..i)
    # Note: inv[k] here is the modular inverse of k, not the inverse factorial
    H_inv = [0] * (N + 1)
    for i in range(1, N + 1):
        H_inv[i] = (H_inv[i-1] + inv[i]) % MOD
        
    total_A = prefix_sum_A[N]
    fact_N_minus_1 = fact[N-1]
    
    results = []
    for u, v in queries:
        if u > v:
            u, v = v, u
        min_uv = u
        max_uv = v
        
        # Sum A in [min+1, max]
        # Range is [min_uv + 1, max_uv]
        sum_mid = get_sum_A(min_uv + 1, max_uv)
        
        # Term 1: (Total Sum A) * (N-1)! / min_uv
        term1 = (total_A * fact_N_minus_1) % MOD
        term1 = (term1 * inv[min_uv]) % MOD
        
        # Term 2: sum_mid * (N-1)! * (H_inv[max] - H_inv[min])
        # The range for harmonic sum is [min_uv + 1, max_uv]
        h_diff = (H_inv[max_uv] - H_inv[min_uv]) % MOD
        term2 = (sum_mid * fact_N_minus_1) % MOD
        term2 = (term2 * h_diff) % MOD
        
        ans = (term1 - term2) % MOD
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()