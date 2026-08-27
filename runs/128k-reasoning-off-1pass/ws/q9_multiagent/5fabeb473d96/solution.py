import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
        
        # A is 1-indexed in problem description (A_2 ... A_N)
        # We will store A such that A[i] corresponds to A_i
        # Input gives A_2, A_3, ..., A_N
        A = [0] * (N + 1)
        for i in range(2, N + 1):
            A[i] = int(next(iterator))
            
    except StopIteration:
        return

    MOD = 998244353

    # Precompute factorials and modular inverses
    # We need (N-1)! for the total count of trees
    # We need modular inverse for i in range [2, N]
    
    fact = [1] * (N + 1)
    inv = [1] * (N + 1)
    
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Modular inverse using Fermat's Little Theorem: a^(MOD-2) % MOD
    # We compute inv[N] first, then work backwards to get inv[1]...inv[N]
    # This is O(N) instead of O(N log MOD)
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, 1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    # Precompute prefix sums of (A[i] * inv[i]) % MOD
    # Let B[i] = A[i] * inv[i]
    # Prefix sum P[x] = sum(B[i] for i in 2..x)
    # We need sum from L to R-1.
    
    # P[i] will store sum_{k=2}^{i} (A[k] * inv[k])
    P = [0] * (N + 1)
    current_sum = 0
    for i in range(2, N + 1):
        term = (A[i] * inv[i]) % MOD
        current_sum = (current_sum + term) % MOD
        P[i] = current_sum
        
    # Total number of trees
    total_trees = fact[N-1]
    
    results = []
    
    for _ in range(Q):
        u = int(next(iterator))
        v = int(next(iterator))
        
        if u > v:
            u, v = v, u
            
        # L = u, R = v
        # Formula: (N-1)! * ( A[R] + sum_{i=L}^{R-1} (A[i]/i) )
        # Note: if L=1, the sum starts from i=2 because A[1] doesn't exist/is not an edge.
        
        term_R = A[v]
        
        if u == 1:
            # Sum from 2 to v-1
            if v - 1 >= 2:
                # P[v-1] is sum(2..v-1), P[1] is 0
                range_sum = P[v-1]
            else:
                range_sum = 0
        else:
            # Sum from u to v-1
            if v - 1 >= u:
                # P[v-1] - P[u-1]
                range_sum = (P[v-1] - P[u-1]) % MOD
            else:
                range_sum = 0
                
        # Ensure positive modulo
        range_sum = (range_sum + MOD) % MOD
        
        # Total contribution
        ans = (total_trees * (term_R + range_sum)) % MOD
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()