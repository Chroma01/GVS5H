import sys
from math import comb

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    P = int(input_data[1])
    
    # Precompute binomial coefficients modulo P
    # We need C(n, k) for n up to N*(N-1)//2 (max edges) and k up to N*(N-1)//2
    # But actually we need C(K, M) where K can be up to N*(N-1)//2 and M up to N*(N-1)//2
    # Since N <= 30, max edges = 30*29//2 = 435
    MAX_EDGES = N * (N - 1) // 2
    
    # Precompute factorials for combinations
    fact = [1] * (MAX_EDGES + 1)
    inv_fact = [1] * (MAX_EDGES + 1)
    
    for i in range(1, MAX_EDGES + 1):
        fact[i] = (fact[i-1] * i) % P
        
    # Fermat's little theorem for inverse since P is prime
    inv_fact[MAX_EDGES] = pow(fact[MAX_EDGES], P - 2, P)
    for i in range(MAX_EDGES - 1, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % P
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv_fact[r] * inv_fact[n-r]) % P
        return (num * den) % P
    
    half_N = N // 2
    
    # Number of ways to choose the even-distance set S containing vertex 1
    # with |S| = N/2. Vertex 1 is fixed in S, so we choose N/2 - 1 from N-1 remaining vertices.
    num_partitions = nCr_mod(N - 1, half_N - 1)
    
    # Precompute C(K, M) for all relevant K and M
    # K ranges from 0 to MAX_EDGES, M ranges from N-1 to MAX_EDGES
    # We'll compute a table C_table[K][M] = C(K, M) % P
    # But since we need this for many K values, let's just compute on the fly or precompute
    
    # Actually, let's precompute the entire Pascal triangle mod P
    C_table = [[0] * (MAX_EDGES + 1) for _ in range(MAX_EDGES + 1)]
    for n in range(MAX_EDGES + 1):
        C_table[n][0] = 1
        for k in range(1, n + 1):
            C_table[n][k] = (C_table[n-1][k-1] + C_table[n-1][k]) % P
            
    # For each M from N-1 to MAX_EDGES, compute the answer
    results = []
    
    # Precompute the inclusion-exclusion sum
    # Sum over i (bad vertices in T), j (bad vertices in S\{1}), k (bad: 1 not connected to T)
    # i ranges from 0 to half_N
    # j ranges from 0 to half_N - 1
    # k ranges from 0 to 1
    
    ie_sum_by_K = [0] * (MAX_EDGES + 1)
    
    for i in range(half_N + 1):
        for j in range(half_N):
            for k in range(2):
                # Sign: (-1)^(i + j + k)
                sign = 1 if (i + j + k) % 2 == 0 else -1
                
                # Coefficient: C(half_N, i) * C(half_N - 1, j) * C(1, k)
                coeff_i = nCr_mod(half_N, i)
                coeff_j = nCr_mod(half_N - 1, j)
                coeff_k = 1 if k == 0 else 1 # C(1, 0) = 1, C(1, 1) = 1
                
                term_coeff = (coeff_i * coeff_j) % P
                if k == 1:
                    term_coeff = (term_coeff * 1) % P # C(1, 1) = 1
                
                if sign == -1:
                    term_coeff = (P - term_coeff) % P
                
                # Calculate K_{i,j,k}
                # Edges within S: C(half_N, 2)
                # Edges within T: C(half_N, 2)
                # Edges between S\{1} and T: (half_N - 1 - j) * (half_N - i)
                # Edges between 1 and T: 
                #   if k == 1: 0
                #   if k == 0: half_N - i
                
                edges_within_S = half_N * (half_N - 1) // 2
                edges_within_T = half_N * (half_N - 1) // 2
                
                edges_S1_T = (half_N - 1 - j) * (half_N - i)
                
                if k == 1:
                    edges_1_T = 0
                else:
                    edges_1_T = half_N - i
                    
                K = edges_within_S + edges_within_T + edges_S1_T + edges_1_T
                
                if K <= MAX_EDGES:
                    ie_sum_by_K[K] = (ie_sum_by_K[K] + term_coeff) % P
                    
    # Now compute the answer for each M
    for M in range(N - 1, MAX_EDGES + 1):
        ans = 0
        for K in range(M, MAX_EDGES + 1):
            # We need C(K, M) * ie_sum_by_K[K]
            # But wait, the inclusion-exclusion gives us the count for a fixed partition
            # The term ie_sum_by_K[K] is the sum over all bad configurations for a fixed partition
            # when exactly K edges are available.
            # For a fixed M, we need to sum over all K >= M: ie_sum_by_K[K] * C(K, M)
            
            c_km = C_table[K][M]
            term = (ie_sum_by_K[K] * c_km) % P
            ans = (ans + term) % P
            
        ans = (ans * num_partitions) % P
        results.append(str(ans))
        
    print(' '.join(results))

solve()