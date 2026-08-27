import sys
from math import comb

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    P = int(input_data[1])
    
    # Precompute combinations modulo P
    # We need combinations up to N(N-1)/2 which is at most 30*29/2 = 435.
    # But for inclusion-exclusion in Ways, we might need comb(A*(B-j), k).
    # Max A*B is 15*15 = 225. So max n for comb is around 435.
    MAX_N = N * (N - 1) // 2 + 10
    
    # Precompute factorials for combinations
    fact = [1] * (MAX_N + 1)
    inv = [1] * (MAX_N + 1)
    
    for i in range(1, MAX_N + 1):
        fact[i] = (fact[i-1] * i) % P
        
    inv[MAX_N] = pow(fact[MAX_N], P - 2, P)
    for i in range(MAX_N - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % P
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % P
        return (num * den) % P

    # Precompute Ways(A, B, k)
    # Ways(A, B, k) = sum_{j=0}^{B} (-1)^j * C(B, j) * C(A*(B-j), k)
    # We will store this in a dictionary or list of lists for quick access.
    # A, B <= N. k <= A*B.
    
    # To save space and time, we can compute on the fly or precompute a table.
    # Given N <= 30, A*B <= 225. k <= 225.
    # Table size 30*30*225 is manageable.
    
    ways_table = {}
    
    for A in range(1, N + 1):
        for B in range(1, N + 1):
            max_k = A * B
            ways = [0] * (max_k + 1)
            
            # Inclusion-Exclusion
            # Sum_{j=0}^{B} (-1)^j * C(B, j) * C(A*(B-j), k)
            # We can compute this for each k.
            # Alternatively, compute the polynomial coefficients.
            
            # Let's compute for each k directly
            for k in range(max_k + 1):
                val = 0
                for j in range(B + 1):
                    # Term: (-1)^j * C(B, j) * C(A*(B-j), k)
                    term = nCr_mod(B, j) * nCr_mod(A * (B - j), k) % P
                    if j % 2 == 1:
                        val = (val - term + P) % P
                    else:
                        val = (val + term) % P
                ways[k] = val
            ways_table[(A, B)] = ways

    # Generate all valid BFS layerings
    # A layering is a sequence s_0, s_1, ..., s_D such that:
    # s_0 = 1
    # sum(s_i) = N
    # sum_{i even} s_i = N/2
    # s_i >= 1 for all i
    
    # We use recursion to generate layerings.
    # State: (current_sum, current_layer_index, current_even_sum, current_odd_sum, layering_list)
    
    valid_layerings = []
    target_even = N // 2
    
    def generate_layerings(current_sum, current_layer_idx, current_even_sum, current_odd_sum, layering):
        if current_sum == N:
            if current_even_sum == target_even:
                valid_layerings.append(list(layering))
            return
        
        # Determine the maximum possible size for the next layer
        # Remaining vertices: N - current_sum
        # We need to leave at least 1 vertex for each subsequent layer.
        # But we don't know how many layers.
        # However, we can just iterate possible sizes for the next layer.
        
        remaining = N - current_sum
        
        # The next layer is at index current_layer_idx + 1
        # If current_layer_idx is 0, next is 1 (odd index)
        # If current_layer_idx is 1, next is 2 (even index)
        
        # Max size for next layer is remaining - (number of future layers - 1)
        # But we don't know number of future layers.
        # Just iterate size from 1 to remaining.
        
        for size in range(1, remaining + 1):
            # Check if adding this size exceeds N
            if current_sum + size > N:
                break
                
            # Update sums
            next_layer_idx = current_layer_idx + 1
            if next_layer_idx % 2 == 0:
                new_even = current_even_sum + size
                new_odd = current_odd_sum
            else:
                new_even = current_even_sum
                new_odd = current_odd_sum + size
                
            # Pruning: if even sum exceeds target, stop
            if new_even > target_even:
                continue
                
            # Pruning: if odd sum exceeds target, stop
            if new_odd > target_even: # Since total N/2 for odd too
                continue
                
            layering.append(size)
            generate_layerings(current_sum + size, next_layer_idx, new_even, new_odd, layering)
            layering.pop()

    generate_layerings(1, 0, 1, 0, [1])
    
    # For each layering, compute the polynomial of edge counts
    # P(x) = Product_{i=1 to D} (Poly_inter(i)) * Product_{i=0 to D} (Poly_intra(i))
    # Poly_inter(i) corresponds to edges between L_{i-1} and L_i
    # Poly_intra(i) corresponds to edges within L_i
    
    # We will accumulate the total count for each M
    # Since we need to output for M from N-1 to N(N-1)/2, we can use a dictionary or array.
    
    # Max edges
    max_edges = N * (N - 1) // 2
    total_counts = [0] * (max_edges + 1)
    
    for layering in valid_layerings:
        # layering is [s_0, s_1, ..., s_D]
        D = len(layering) - 1
        
        # Start with polynomial [1] (representing x^0)
        # We will convolve polynomials.
        # Represent polynomial as list of coefficients, index is power of x.
        
        poly = [1]
        
        # Inter-layer edges
        for i in range(1, D + 1):
            A = layering[i-1]
            B = layering[i]
            ways = ways_table[(A, B)]
            
            # Convolve poly with ways
            new_poly = [0] * (len(poly) + len(ways) - 1)
            for p_idx, p_val in enumerate(poly):
                if p_val == 0: continue
                for w_idx, w_val in enumerate(ways):
                    if w_val == 0: continue
                    new_poly[p_idx + w_idx] = (new_poly[p_idx + w_idx] + p_val * w_val) % P
            poly = new_poly
            
        # Intra-layer edges
        for i in range(D + 1):
            s = layering[i]
            if s <= 1:
                # No internal edges possible, poly *= [1]
                continue
            
            max_w = s * (s - 1) // 2
            # Coefficients are C(max_w, w)
            intra_poly = [0] * (max_w + 1)
            for w in range(max_w + 1):
                intra_poly[w] = nCr_mod(max_w, w)
                
            # Convolve
            new_poly = [0] * (len(poly) + len(intra_poly) - 1)
            for p_idx, p_val in enumerate(poly):
                if p_val == 0: continue
                for w_idx, w_val in enumerate(intra_poly):
                    if w_val == 0: continue
                    new_poly[p_idx + w_idx] = (new_poly[p_idx + w_idx] + p_val * w_val) % P
            poly = new_poly
            
        # Add to total_counts
        for m, count in enumerate(poly):
            if m <= max_edges:
                total_counts[m] = (total_counts[m] + count) % P
                
    # Output results for M from N-1 to max_edges
    results = []
    for m in range(N - 1, max_edges + 1):
        results.append(str(total_counts[m]))
        
    print(" ".join(results))

solve()