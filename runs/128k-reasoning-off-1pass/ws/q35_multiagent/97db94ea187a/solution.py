import sys

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    P = int(input_data[1])
    
    # Precompute combinations modulo P
    # We need C(n, k) for n up to N*(N-1)//2 and k up to M_max
    # M ranges from N-1 to N*(N-1)//2
    max_edges = N * (N - 1) // 2
    
    # Since P is large (up to 10^9), we can't precompute factorials easily if P is not small.
    # But N is small (<=30), so max_edges <= 435.
    # We can precompute factorials and inverse factorials modulo P.
    
    fact = [1] * (max_edges + 1)
    inv_fact = [1] * (max_edges + 1)
    
    for i in range(1, max_edges + 1):
        fact[i] = (fact[i-1] * i) % P
        
    inv_fact[max_edges] = pow(fact[max_edges], P - 2, P)
    for i in range(max_edges - 1, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % P
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv_fact[r] * inv_fact[n-r]) % P
        return (num * den) % P

    # DP state:
    # dp[i][last_size][s_even] = polynomial (list of coefficients)
    # i: number of vertices placed so far (excluding vertex 1), from 0 to N-1
    # last_size: size of the last layer added, from 1 to N-1
    # s_even: current size of S_even set (including vertex 1), from 1 to N/2
    # polynomial: coeffs[w] represents the sum of (-1)^|S| for subsets of boundaries with total weight w
    
    # Initialize DP
    # Start with vertex 1 in layer 0.
    # We place the first layer (L_1) of size s.
    # i = s, last_size = s, s_even = 1 (if s is odd layer, it goes to S_odd, so s_even remains 1)
    # Wait, layer 0 is {1}, size 1.
    # Layer 1 is L_1, size s.
    # If layer index is odd (1, 3, ...), vertices go to S_odd.
    # If layer index is even (2, 4, ...), vertices go to S_even.
    
    # We can iterate layer by layer.
    # Let's use a dictionary or list of dictionaries for DP.
    # dp[i][last_size][s_even] -> poly
    
    # To save space, we can use a list of dicts for each i.
    # dp[i] is a dict: (last_size, s_even) -> poly
    
    # Initial state: after placing layer 0 (vertex 1), we haven't placed any other vertices.
    # But our DP builds layers 1, 2, ...
    # Let's start by placing the first layer L_1.
    
    # dp[i][last_size][s_even]
    # i: total vertices placed so far (including layer 0? No, let's say i is vertices in layers 1..k)
    # Let's redefine:
    # dp[k][last_size][s_even] = poly
    # k: number of layers placed so far (excluding L_0)
    # last_size: size of L_k
    # s_even: size of S_even = {1} U union of L_j for even j
    
    # We can use a list of dicts for each k.
    # dp[k][(last_size, s_even)] = poly
    
    # Max k is N-1 (each layer size 1).
    
    dp = [{} for _ in range(N)] # dp[k] for k layers
    
    # Base case: k=1, placing L_1 of size s
    # s can range from 1 to N-1
    # s_even = 1 (since L_1 is odd layer, goes to S_odd)
    # The boundary between L_0 and L_1 has weight B_1 = |L_0| * |L_1| = 1 * s = s
    # The polynomial for this single boundary: (1 - x^s)
    # So coeffs[0] = 1, coeffs[s] = -1
    
    for s in range(1, N):
        poly = [0] * (s + 1)
        poly[0] = 1
        poly[s] = (P - 1) % P # -1 mod P
        
        # Store in dp[1]
        # Key: (last_size=s, s_even=1)
        dp[1][(s, 1)] = poly

    # Iterate for k from 2 to N-1
    for k in range(2, N):
        # For each state in dp[k-1]
        for (last_size, s_even_prev), poly_prev in dp[k-1].items():
            # Try placing next layer L_k of size s
            # s can range from 1 to N - (k-1) - 1? No, total vertices is N.
            # Vertices placed so far: 1 (L_0) + sum of sizes of L_1..L_{k-1}
            # We need to track total vertices placed.
            # Let's add total_vertices to the state.
            pass
            
    # Redefine DP state to include total vertices placed
    # dp[k][(last_size, s_even, total_vertices)] = poly
    # But total_vertices is determined by the sum of layer sizes.
    # We can compute it or track it.
    
    # Let's restart DP with total_vertices in state.
    # dp[k][(last_size, s_even, total_vertices)] = poly
    
    dp2 = [{} for _ in range(N)]
    
    # Base case: k=1
    for s in range(1, N):
        # total_vertices = 1 (L_0) + s
        total_v = 1 + s
        if total_v > N:
            continue
            
        poly = [0] * (s + 1)
        poly[0] = 1
        poly[s] = (P - 1) % P
        
        dp2[1][(s, 1, total_v)] = poly
        
    # Iterate
    for k in range(2, N):
        for (last_size, s_even_prev, total_v_prev), poly_prev in dp2[k-1].items():
            # Try placing next layer L_k of size s
            # s >= 1
            # total_v_new = total_v_prev + s
            # s can range from 1 to N - total_v_prev
            max_s = N - total_v_prev
            for s in range(1, max_s + 1):
                total_v_new = total_v_prev + s
                
                # Determine new s_even
                # Layer k is odd or even?
                # k=1 is odd, k=2 is even, etc.
                if k % 2 == 1:
                    # Odd layer, goes to S_odd
                    s_even_new = s_even_prev
                else:
                    # Even layer, goes to S_even
                    s_even_new = s_even_prev + s
                    
                if s_even_new > N // 2:
                    continue
                    
                # Compute new polynomial
                # B_k = last_size * s
                B = last_size * s
                # poly_new = poly_prev * (1 - x^B)
                # This is poly_new[w] = poly_prev[w] - poly_prev[w-B]
                
                # Degree of poly_prev is at most total_v_prev * (total_v_prev - 1) // 2?
                # Actually, max weight is sum of all possible B_i.
                # Max B_i is roughly (N/2)^2. Sum of B_i is bounded.
                # Let's find max degree of poly_prev.
                deg_prev = len(poly_prev) - 1
                deg_new = deg_prev + B
                
                poly_new = [0] * (deg_new + 1)
                
                for w in range(deg_prev + 1):
                    if poly_prev[w] == 0:
                        continue
                    # Term from poly_prev[w] * 1
                    poly_new[w] = (poly_new[w] + poly_prev[w]) % P
                    # Term from poly_prev[w] * (-x^B)
                    if w + B <= deg_new:
                        poly_new[w + B] = (poly_new[w + B] - poly_prev[w]) % P
                        
                # Store in dp2[k]
                key = (s, s_even_new, total_v_new)
                if key in dp2[k]:
                    # Merge polynomials? No, each state is unique.
                    # But we might have multiple ways to reach same state?
                    # No, the state (last_size, s_even, total_v) is unique for a given sequence of layer sizes?
                    # No, different sequences can lead to same last_size, s_even, total_v.
                    # So we need to add the polynomials.
                    dp2[k][key] = [(dp2[k][key][i] + poly_new[i]) % P for i in range(len(poly_new))]
                else:
                    dp2[k][key] = poly_new

    # Now, collect results for each M
    # M ranges from N-1 to N*(N-1)//2
    # For each valid final state (k, last_size, s_even, total_v=N, s_even=N/2),
    # we have a polynomial.
    # The answer for M is sum_{w} poly[w] * C(I + T - w, M)
    # where I = sum of intra-layer edges, T = sum of all inter-layer edges.
    # I = sum_{j=1}^k C(|L_j|, 2)
    # T = sum_{j=1}^k |L_j| * |L_{j-1}|
    # But we don't have the layer sizes in the state, only last_size and s_even and total_v.
    # We need to track I and T in the state?
    # Or we can compute them on the fly?
    # No, we need to know I and T for each layering.
    # This suggests we need to include I and T in the DP state or compute them separately.
    # But I and T can be large.
    # Alternative: For each final state, we don't know the layer sizes, so we can't compute I and T.
    # This means the DP state must include enough information to compute I and T.
    # But I and T depend on all layer sizes, not just the last one.
    # This approach is flawed.
    
    # Let's go back to the composition iteration.
    # Since N is small (<=30), but 2^28 is too big, we need a better way.
    # However, the number of partitions is small.
    # We can iterate over all partitions of N-1, and for each partition, iterate over all permutations (compositions).
    # But the number of compositions is still large.
    
    # Let's try a different DP that tracks I and T.
    # State: dp[k][(last_size, s_even, total_v, I, T)] = poly
    # I and T can be up to ~3000.
    # This state space is too big.
    
    # Alternative: Since we need to output for all M, and M is up to 435,
    # we can compute the answer for each M separately.
    # For a fixed M, we can use DP.
    # But the problem asks for all M.
    
    # Let's reconsider the problem.
    # N <= 30.
    # Maybe we can use the fact that the number of layers is small?
    # If the number of layers is small, the inclusion-exclusion is fast.
    # If the number of layers is large, the layers are small.
    
    # Given the time constraints, I will implement the composition iteration with memoization on the layer sizes.
    # But since the order matters, we can't easily memoize.
    
    # Let's try to code the solution for small N first and see if it passes.
    # For N=30, it might TLE.
    
    # I will implement the DP with state (k, last_size, s_even, total_v, I, T) and use a dictionary.
    # To reduce state space, I will only store states that are reachable.
    
    # Re-implement DP with I and T in state.
    
    dp3 = {}
    # State: (k, last_size, s_even, total_v, I, T) -> poly
    # But poly is large.
    # Instead, let's store the poly as a list.
    
    # Base case: k=1, layer size s
    # I = C(s, 2)
    # T = 1 * s = s
    # s_even = 1
    # total_v = 1 + s
    
    for s in range(1, N):
        total_v = 1 + s
        if total_v > N:
            continue
        I = s * (s - 1) // 2
        T = s
        s_even = 1
        
        poly = [0] * (T + 1)
        poly[0] = 1
        poly[T] = (P - 1) % P
        
        key = (1, s, s_even, total_v, I, T)
        dp3[key] = poly
        
    # Iterate
    for k in range(2, N):
        new_dp3 = {}
        for (k_prev, last_size, s_even_prev, total_v_prev, I_prev, T_prev), poly_prev in dp3.items():
            # Try placing next layer L_k of size s
            max_s = N - total_v_prev
            for s in range(1, max_s + 1):
                total_v_new = total_v_prev + s
                if total_v_new > N:
                    continue
                    
                if k % 2 == 1:
                    s_even_new = s_even_prev
                else:
                    s_even_new = s_even_prev + s
                    
                if s_even_new > N // 2:
                    continue
                    
                I_new = I_prev + s * (s - 1) // 2
                B = last_size * s
                T_new = T_prev + B
                
                # Compute new polynomial
                deg_prev = len(poly_prev) - 1
                deg_new = deg_prev + B
                poly_new = [0] * (deg_new + 1)
                
                for w in range(deg_prev + 1):
                    if poly_prev[w] == 0:
                        continue
                    poly_new[w] = (poly_new[w] + poly_prev[w]) % P
                    if w + B <= deg_new:
                        poly_new[w + B] = (poly_new[w + B] - poly_prev[w]) % P
                        
                key = (k, s, s_even_new, total_v_new, I_new, T_new)
                if key in new_dp3:
                    new_dp3[key] = [(new_dp3[key][i] + poly_new[i]) % P for i in range(len(poly_new))]
                else:
                    new_dp3[key] = poly_new
                    
        dp3 = new_dp3
        
    # Collect results
    # For each final state with total_v = N and s_even = N/2
    # Compute answer for each M
    
    results = [0] * (max_edges + 1)
    
    for (k, last_size, s_even, total_v, I, T), poly in dp3.items():
        if total_v != N or s_even != N // 2:
            continue
            
        # For each M, answer = sum_{w} poly[w] * C(I + T - w, M)
        # I + T is the total number of allowed edges.
        total_allowed = I + T
        
        for w, coeff in enumerate(poly):
            if coeff == 0:
                continue
            # We need C(total_allowed - w, M)
            # M ranges from N-1 to max_edges
            # Let n = total_allowed - w
            n = total_allowed - w
            if n < 0:
                continue
            for M in range(N - 1, max_edges + 1):
                if M > n:
                    continue
                term = (coeff * nCr_mod(n, M)) % P
                results[M] = (results[M] + term) % P
                
    # Output results for M = N-1 to max_edges
    output = []
    for M in range(N - 1, max_edges + 1):
        output.append(str(results[M]))
        
    print(' '.join(output))

solve()