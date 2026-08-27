import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    # Read A (A_2 to A_N)
    # A will be 0-indexed, so A[i] corresponds to A_{i+2}
    A = []
    for _ in range(N - 1):
        A.append(int(next(iterator)))
    
    # Queries
    queries = []
    for _ in range(Q):
        u = int(next(iterator))
        v = int(next(iterator))
        queries.append((u, v))

    MOD = 998244353

    # Precompute modular inverses for 1 to N
    inv = [1] * (N + 1)
    for i in range(2, N + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
        
    # Precompute harmonic numbers H_n = sum(1/k for k=1..n)
    # We need H_{x-2}. Let's store H[x] = sum(1/k for k=1..x)
    H = [0] * (N + 1)
    curr = 0
    for i in range(1, N + 1):
        curr = (curr + inv[i]) % MOD
        H[i] = curr
        
    # Helper to get S(x) = 1 + H_{x-2}
    # If x=1, S(1) = 1.
    # If x=2, S(2) = 1 + H_0 = 1.
    # If x>=3, S(x) = 1 + H[x-2]
    def get_S(x):
        if x <= 2:
            return 1
        return (1 + H[x-2]) % MOD

    # Precompute B[i] = A[i-1] * inv[i-1]^2 for i from 2 to N
    # A is 0-indexed, so A[i-1] corresponds to A_i (since A_2 is at index 0)
    # We use 1-based indexing for logic, so let's align arrays.
    # B[i] stores value for node i.
    B = [0] * (N + 1)
    for i in range(2, N + 1):
        # A_i is at A[i-2]
        val = A[i-2]
        inv_sq = (inv[i-1] * inv[i-1]) % MOD
        B[i] = (val * inv_sq) % MOD

    # Prefix sums of B
    # P[x] = sum(B[2]...B[x])
    P = [0] * (N + 1)
    current_sum = 0
    for i in range(2, N + 1):
        current_sum = (current_sum + B[i]) % MOD
        P[i] = current_sum

    # Precompute (N-1)!
    fact_N_minus_1 = 1
    for i in range(1, N):
        fact_N_minus_1 = (fact_N_minus_1 * i) % MOD

    results = []
    
    for u, v in queries:
        mn = min(u, v)
        mx = max(u, v)
        
        # We need to compute:
        # Sum = (N-1)! * [ Term(mn) + Sum(mn+1 to mx-1) + Term(mx) ]
        # Term(i) = A_i * S(target) / (i-1)^2
        #        = S(target) * B[i]
        
        total_coeff = 0
        
        if mn == 1:
            # S(1) = 1
            # Sum for i from 2 to mx-1: B[i] * 1
            if mx - 1 >= 2:
                term_mid = (P[mx-1] - P[1]) % MOD
            else:
                term_mid = 0
            
            # Term for i = mx: B[mx] * 1
            if mx <= N:
                term_mx = B[mx]
            else:
                term_mx = 0
                
            total_coeff = (term_mid + term_mx) % MOD
            
        else:
            # Term for i = mn: B[mn] * S(mx)
            s_mx = get_S(mx)
            term_mn = (B[mn] * s_mx) % MOD
            
            # Sum for i from mn+1 to mx-1: B[i] * S(mn)
            s_mn = get_S(mn)
            if mx - 1 >= mn + 1:
                term_mid = (P[mx-1] - P[mn]) % MOD
                term_mid = (term_mid * s_mn) % MOD
            else:
                term_mid = 0
            
            # Term for i = mx: B[mx] * S(mn)
            term_mx = (B[mx] * s_mn) % MOD
            
            total_coeff = (term_mn + term_mid + term_mx) % MOD
            
        ans = (fact_N_minus_1 * total_coeff) % MOD
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()