import sys

# Increase recursion depth just in case, though not needed for this iterative solution
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
    except StopIteration:
        return

    # Read A (A_2 to A_N)
    # A is 0-indexed in our list, so A[i] corresponds to A_{i+2}
    # But the problem says A = (A_2, ..., A_N).
    # Let's store A such that A[i] is the weight of edge i (connecting i to P_i).
    # So we need an array of size N+1, where index i holds A_i.
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(next(iterator))

    # Precompute modular inverses for 1 to N
    # inv_num[i] will store the modular inverse of i
    MOD = 998244353
    inv_num = [1] * (N + 1)
    inv_num[1] = 1
    for i in range(2, N + 1):
        inv_num[i] = (MOD - (MOD // i) * inv_num[MOD % i] % MOD) % MOD
        
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(2, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Total number of trees is (N-1)!
    total_trees = fact[N-1]
    
    # Common factor for the formula: 2 * (N-1)!
    common_factor = (total_trees * 2) % MOD
    
    # Precompute prefix sums
    # P1[i] stores sum_{j=2}^{i} A[j]
    # P2[i] stores sum_{j=2}^{i} (A[j] * inv_num[j])
    P1 = [0] * (N + 1)
    P2 = [0] * (N + 1)
    
    current_p1 = 0
    current_p2 = 0
    
    for i in range(2, N + 1):
        current_p1 = (current_p1 + A[i]) % MOD
        current_p2 = (current_p2 + A[i] * inv_num[i]) % MOD
        P1[i] = current_p1
        P2[i] = current_p2
        
    # Process queries
    results = []
    
    for _ in range(Q):
        u = int(next(iterator))
        v = int(next(iterator))
        
        # Ensure u < v for consistency
        if u > v:
            u, v = v, u
            
        # We need to calculate sum_{i=2}^{u} A[i] * (2/i - 2/v)
        # = 2 * ( (1/v) * sum_{i=2}^{u} A[i] - sum_{i=2}^{u} (A[i]/i) )
        
        sum_A = P1[u]
        sum_A_div_i = P2[u]
        
        # Calculate (1/v) * sum_A
        term1 = (sum_A * inv_num[v]) % MOD
        
        # Calculate difference
        diff = (term1 - sum_A_div_i + MOD) % MOD
        
        # Multiply by common factor (2 * (N-1)!)
        ans = (diff * common_factor) % MOD
        
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()