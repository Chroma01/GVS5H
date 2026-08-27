import sys

# Set recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
        
        # A is 1-indexed in problem description for A_2...A_N
        # We will store A such that A[i] corresponds to A_i (weight of edge i -> P_i)
        # Input gives A_2, A_3, ..., A_N
        A = [0] * (N + 1)
        for i in range(2, N + 1):
            A[i] = int(next(iterator))
            
    except StopIteration:
        return

    MOD = 998244353

    # Precompute modular inverses for 1 to N
    # We need inverses for i where i goes from 2 to N
    inv = [1] * (N + 1)
    for i in range(2, N + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # Precompute prefix sums of (A[i] * inv[i]) % MOD
    # S[x] = sum_{k=2}^{x} (A[k] * inv[k])
    S = [0] * (N + 1)
    current_sum = 0
    for i in range(2, N + 1):
        term = (A[i] * inv[i]) % MOD
        current_sum = (current_sum + term) % MOD
        S[i] = current_sum

    # Precompute (N-1)! % MOD
    fact_N_minus_1 = 1
    for i in range(1, N):
        fact_N_minus_1 = (fact_N_minus_1 * i) % MOD

    # Process queries
    results = []
    for _ in range(Q):
        u = int(next(iterator))
        v = int(next(iterator))
        
        # Ensure u < v as per problem constraints (u < v)
        # The problem statement says u_i < v_i, so we don't need to swap.
        # However, logic holds for u < v.
        
        # Formula: Ans = (N-1)! * ( sum_{i=u+1}^{v-1} (A[i]/i) + A[v] )
        
        term_sum = 0
        if v - 1 >= u + 1:
            # Sum from u+1 to v-1
            # S[v-1] - S[u]
            term_sum = (S[v-1] - S[u] + MOD) % MOD
        
        # Add A[v]
        term_sum = (term_sum + A[v]) % MOD
        
        # Multiply by (N-1)!
        ans = (term_sum * fact_N_minus_1) % MOD
        results.append(str(ans))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()