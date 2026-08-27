import sys

# Set recursion limit just in case, though we don't use recursion
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

    # A is 1-indexed in problem, but we'll store 0-indexed or adjust
    # A_2, A_3, ..., A_N
    # Let's store A in a list where index i corresponds to node i+2?
    # Or better: create an array A of size N+1, where A[i] is the weight of edge connected to node i (parent is P_i)
    # A[2] ... A[N] are given.
    
    A = [0] * (N + 1)
    for i in range(2, N + 1):
        A[i] = int(next(iterator))
        
    # Precompute modular inverse for numbers 1 to N
    # We need 1/k mod 998244353 for k in 2..N
    MOD = 998244353
    
    inv = [1] * (N + 1)
    for i in range(2, N + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD
        
    # Precompute prefix sums for the three types of coefficients
    # Type 1: For k < min(u, v), coeff = 2/k * (1 - 1/k) = 2/k - 2/k^2
    # Type 2: For min(u, v) < k < max(u, v), coeff = 1/k
    # Type 3: For k = min(u, v), coeff = 1 - 1/k
    # Type 4: For k = max(u, v), coeff = 1
    
    # Let's define:
    # C1[k] = A[k] * (2 * inv[k] - 2 * inv[k] * inv[k]) % MOD
    # C2[k] = A[k] * inv[k] % MOD
    
    # We need prefix sums for C1 and C2.
    
    prefix_C1 = [0] * (N + 1)
    prefix_C2 = [0] * (N + 1)
    
    for k in range(2, N + 1):
        val_A = A[k]
        inv_k = inv[k]
        
        # C1 coefficient: 2/k - 2/k^2
        # 2/k
        term1 = (2 * inv_k) % MOD
        # 2/k^2
        term2 = (2 * inv_k * inv_k) % MOD
        coeff1 = (term1 - term2) % MOD
        
        # C2 coefficient: 1/k
        coeff2 = inv_k
        
        prefix_C1[k] = (prefix_C1[k-1] + val_A * coeff1) % MOD
        prefix_C2[k] = (prefix_C2[k-1] + val_A * coeff2) % MOD
        
    # Process queries
    results = []
    
    for _ in range(Q):
        u = int(next(iterator))
        v = int(next(iterator))
        
        if u > v:
            u, v = v, u
            
        # u < v
        # Sum = sum_{k=2}^{u-1} A[k] * C1[k] + A[u] * C3[u] + sum_{k=u+1}^{v-1} A[k] * C2[k] + A[v] * 1
        
        # Part 1: k from 2 to u-1
        if u - 1 >= 2:
            part1 = prefix_C1[u-1]
        else:
            part1 = 0
            
        # Part 2: k = u
        # Coeff: 1 - 1/u
        coeff_u = (1 - inv[u]) % MOD
        part2 = (A[u] * coeff_u) % MOD
        
        # Part 3: k from u+1 to v-1
        if v - 1 >= u + 1:
            part3 = (prefix_C2[v-1] - prefix_C2[u]) % MOD
        else:
            part3 = 0
            
        # Part 4: k = v
        # Coeff: 1
        part4 = A[v] % MOD
        
        total = (part1 + part2 + part3 + part4) % MOD
        results.append(str(total))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()