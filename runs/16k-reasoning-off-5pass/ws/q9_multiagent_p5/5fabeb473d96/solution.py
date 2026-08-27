import sys

# Increase recursion depth just in case, though we use iterative approach
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

    # A is 1-indexed in problem logic (A_2 ... A_N)
    # We store A such that A[i] is weight of edge for node i.
    # A[1] is unused (0).
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(next(iterator))
        
    queries = []
    for _ in range(Q):
        u = int(next(iterator))
        v = int(next(iterator))
        queries.append((u, v))
        
    MOD = 998244353
    
    # Precompute factorials to get (N-1)!
    fact = [1] * (N + 1)
    for i in range(2, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    total_trees = fact[N-1]
    
    # Precompute modular inverses for 1..N
    inv = [1] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
        
    # Precompute prefix sums
    # S2[i] = sum(A[j] * inv[j] for j in 2..i) -> Used for u < k < v
    # S3[i] = sum(A[j] * (2*(j-1))/(j*(j+1)) for j in 2..i) -> Used for k < u
    
    S2 = [0] * (N + 1)
    S3 = [0] * (N + 1)
    
    curr_s2 = 0
    curr_s3 = 0
    
    for i in range(2, N + 1):
        # Term for S3: A[i] * 2*(i-1) / (i*(i+1))
        # We compute numerator and denominator carefully
        num = (2 * (i - 1)) % MOD
        den = (i * (i + 1)) % MOD
        term_s3 = (A[i] * num) % MOD
        term_s3 = (term_s3 * pow(den, MOD - 2, MOD)) % MOD
        
        # Term for S2: A[i] / i
        term_s2 = (A[i] * inv[i]) % MOD
        
        curr_s2 = (curr_s2 + term_s2) % MOD
        curr_s3 = (curr_s3 + term_s3) % MOD
        
        S2[i] = curr_s2
        S3[i] = curr_s3
        
    results = []
    for u, v in queries:
        if u > v:
            u, v = v, u
            
        ans = 0
        
        # Case k=v: Prob = 1
        # Contribution: A[v] * 1
        ans = (ans + A[v]) % MOD
        
        # Case k=u: Prob = 1 - 1/u
        # Contribution: A[u] * (1 - inv[u])
        term_u = (A[u] * (1 - inv[u])) % MOD
        ans = (ans + term_u) % MOD
        
        # Case u < k < v: Prob = 1/k
        # Sum A[k]/k for k in [u+1, v-1]
        if u + 1 <= v - 1:
            val = (S2[v-1] - S2[u+1]) % MOD
            ans = (ans + val) % MOD
            
        # Case k < u: Prob = 2(k-1)/(k(k+1))
        # Sum A[k] * 2(k-1)/(k(k+1)) for k in [2, u-1]
        if u - 1 >= 2:
            val = S3[u-1]
            ans = (ans + val) % MOD
            
        ans = (ans * total_trees) % MOD
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()