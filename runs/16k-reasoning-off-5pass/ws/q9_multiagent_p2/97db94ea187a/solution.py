import sys

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(2000)

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    P = int(input_data[1])

    # Precompute binomial coefficients modulo P
    # N is up to 30, so we need up to C(30, 15)
    MAX_N = N + 5
    C = [[0] * MAX_N for _ in range(MAX_N)]
    for i in range(MAX_N):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % P

    # Function to compute combinations
    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        return C[n][r]

    # Generate all valid compositions (c_0, c_1, ...)
    # Constraints:
    # 1. sum(c_i) = N
    # 2. c_0 >= 1
    # 3. sum(c_even) == sum(c_odd) == N/2
    # We use a recursive generator to find these sequences.
    
    valid_compositions = []
    
    def generate_compositions(current_layer, current_sum, current_even_sum, current_odd_sum, current_seq):
        if current_sum == N:
            if current_even_sum == N // 2 and current_odd_sum == N // 2:
                valid_compositions.append(tuple(current_seq))
            return
        
        if current_sum > N:
            return

        # Determine the range for the next layer size
        # Remaining vertices: rem = N - current_sum
        # Remaining even/odd constraints depend on the next index parity
        rem = N - current_sum
        
        # If we are at the last layer (index == len(current_seq)), we must take all remaining
        if len(current_seq) == 0:
            # First layer must have at least 1 vertex
            # Also, we need to ensure the final balance is met.
            # But we can just iterate and check at the end.
            pass
        
        # Optimization: Prune if remaining vertices cannot satisfy the balance
        rem_even_needed = (N // 2) - current_even_sum
        rem_odd_needed = (N // 2) - current_odd_sum
        
        # If we are about to place an even layer, we add to even sum
        # If odd, we add to odd sum.
        # We need to ensure that we can reach the target sums.
        
        # Max possible even sum we can get from remaining layers?
        # This is complex to prune tightly, but N is small (30), so brute force generation is fine.
        # However, we can limit the loop range.
        
        # The next layer index will be len(current_seq).
        # If len(current_seq) == 0, next is 0 (even).
        # If len(current_seq) == 1, next is 1 (odd).
        
        next_idx = len(current_seq)
        
        # Determine min and max for next layer size
        # We must leave enough vertices for the remaining layers to satisfy balance.
        # Let's just iterate 1 to rem, but prune based on balance feasibility.
        
        # If next_idx is even, we add to even_sum.
        # If next_idx is odd, we add to odd_sum.
        
        # Check feasibility:
        # If next_idx is even:
        #   new_even = current_even + k
        #   We need to be able to form rem_odd_needed using future odd layers.
        #   The number of future odd layers is at most (rem - k) (if we alternate 1,1,1...)
        #   Actually, simpler: just iterate and check at leaf. N=30 is small enough for DFS.
        
        for k in range(1, rem + 1):
            # Pruning:
            # If we pick k, remaining vertices = rem - k.
            # If next_idx is even, we used k for even.
            # We need to ensure that we can still satisfy the odd sum requirement.
            # The maximum odd sum we can get from remaining vertices is (rem - k) (if all remaining are odd layers).
            # The minimum is 0.
            # So we need: rem_odd_needed <= (rem - k)
            # Similarly, if next_idx is odd, we need: rem_even_needed <= (rem - k)
            
            if next_idx % 2 == 0: # Even layer
                if (N // 2) - (current_even_sum + k) < 0: continue
                if (N // 2) - current_odd_sum > (rem - k): continue
            else: # Odd layer
                if (N // 2) - current_odd_sum - k < 0: continue
                if (N // 2) - current_even_sum > (rem - k): continue
            
            current_seq.append(k)
            if next_idx % 2 == 0:
                generate_compositions(current_layer + 1, current_sum + k, current_even_sum + k, current_odd_sum, current_seq)
            else:
                generate_compositions(current_layer + 1, current_sum + k, current_even_sum, current_odd_sum + k, current_seq)
            current_seq.pop()

    generate_compositions(0, 0, 0, 0, [])
    
    # DP to store the polynomial for each composition
    # We need to sum the polynomials for all compositions.
    # The polynomial P(x) = sum(count * x^edges)
    # Since max edges is N*(N-1)/2 ~ 435, we can use a list of size ~450.
    
    MAX_EDGES = N * (N - 1) // 2 + 1
    total_poly = [0] * MAX_EDGES
    
    # Precompute binomials for vertex assignment
    # For a composition (c_0, c_1, ...), ways to assign vertices is (N-1)! / (c_0! c_1! ...)
    # We can compute this on the fly.
    
    # Precompute powers of 2
    pow2 = [1] * (MAX_EDGES + 1)
    for i in range(1, MAX_EDGES + 1):
        pow2[i] = (pow2[i-1] * 2) % P

    # Function to calculate ways to connect layer i-1 (size u) to layer i (size v)
    # such that every node in v has at least one neighbor in u.
    # Formula: sum_{j=0 to v} (-1)^j * C(v, j) * 2^(u * (v-j))
    def count_valid_bipartite(u, v):
        if u == 0:
            return 0 if v > 0 else 1 # If u=0 and v>0, impossible (0 ways). If u=0, v=0, 1 way (empty).
        # But in our problem, c_0 >= 1, and for i>=1, c_i >= 1 (since sum is N and we stop when sum=N).
        # Actually, can c_i be 0? 
        # If c_i = 0, then we skip a layer. But BFS layers are contiguous. 
        # If c_i = 0, then no nodes at distance i. This is allowed? 
        # Yes, if no nodes are at distance i, then the graph effectively has max distance < i.
        # However, the problem says "shortest distance from 1 is even/odd". 
        # If a layer is empty, it doesn't contribute to counts.
        # But if c_i = 0, then c_{i+1} must be 0 too? No, if c_i=0, then no node can have distance i+1 
        # because to have distance i+1, you need a neighbor at distance i.
        # So if c_i = 0, then all subsequent layers must be 0.
        # Thus, we only consider compositions where c_i > 0 for all i < k, and c_k can be anything (but sum is N).
        # Wait, if c_i = 0, then no nodes at distance i. Then no nodes at distance i+1.
        # So the sequence must be strictly positive until the last element?
        # Actually, if c_i = 0, then the set S_i is empty. Then S_{i+1} must be empty.
        # So the sequence looks like (c_0, c_1, ..., c_k, 0, 0...).
        # Our generator produces sequences summing to N. If we allow 0s, we might generate (1, 0, 3) which is invalid 
        # because nodes in S_2 cannot exist if S_1 is empty.
        # So we must enforce c_i >= 1 for all i < k, and c_k >= 1? 
        # Actually, the last layer c_k must be >= 1 because sum is N and c_0 >= 1.
        # So all c_i >= 1.
        # Let's enforce c_i >= 1 in the generator.
        # My generator already starts with k >= 1.
        # And if we are not at the end, we can't have k=0 because if k=0, then rem must be 0? 
        # No, if k=0, then rem = N - current_sum. If we pick 0, we are stuck with rem > 0 and next layer must be > 0?
        # If we allow 0, we need to handle the logic.
        # But logically, if S_i is empty, S_{i+1} is empty. So we can just stop the sequence.
        # So we only generate sequences with c_i >= 1.
        # My generator loop `range(1, rem+1)` ensures c_i >= 1.
        # But what if rem > 0 and we are at the last layer? We must take all rem.
        # My generator handles this by iterating up to rem.
        # Is it possible that we need to stop early? 
        # No, the sequence ends when sum == N.
        # So all c_i >= 1.
        
        res = 0
        for j in range(v + 1):
            term = (nCr(v, j) * pow2[u * (v - j)]) % P
            if j % 2 == 1:
                res = (res - term + P) % P
            else:
                res = (res + term) % P
        return res

    # Iterate over all valid compositions
    for comp in valid_compositions:
        # comp is a tuple (c_0, c_1, ..., c_k)
        # Calculate vertex assignment ways
        # Ways = (N-1)! / (c_0! c_1! ... c_k!)
        # We can compute this iteratively.
        
        ways_assign = 1
        fact_inv = [1] * (N + 1)
        # We don't need modular inverse since we can just compute factorials and divide? 
        # No, we need modular inverse for division.
        # But P is prime, so we can use Fermat's Little Theorem.
        # Or precompute factorials and inverse factorials.
        
        # Let's precompute factorials and inverse factorials once outside the loop?
        # But N is small, we can do it inside or precompute globally.
        # Let's precompute now.
        pass

    # Precompute factorials and inverse factorials
    fact = [1] * (N + 1)
    inv = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % P
    inv[N] = pow(fact[N], P - 2, P)
    for i in range(N - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % P
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % P
        return (num * den) % P

    def multinomial(n, parts):
        # n! / (p1! p2! ...)
        res = fact[n]
        for p in parts:
            res = (res * inv[p]) % P
        return res

    # Process each composition
    for comp in valid_compositions:
        # Vertex assignment
        ways_assign = multinomial(N - 1, comp) # Note: c_0 is included in comp, but we fix vertex 1 in S_0.
        # The number of ways to assign the remaining N-1 vertices to the layers c_0-1, c_1, ..., c_k
        # Wait, c_0 includes vertex 1. So we have c_0 - 1 spots in S_0, and c_1 spots in S_1, etc.
        # Total spots = (c_0 - 1) + c_1 + ... + c_k = N - 1.
        # So we need multinomial(N-1, (c_0-1, c_1, ..., c_k))
        
        parts = [comp[0] - 1] + list(comp[1:])
        ways_assign = multinomial(N - 1, parts)
        
        # Now compute the polynomial for edge counts
        # Start with polynomial [1] (0 edges, 1 way)
        poly = [1] + [0] * MAX_EDGES
        
        # Internal edges within layers
        # For each layer i, we can have any subset of edges within S_i.
        # Number of edges within S_i can be k, where 0 <= k <= c_i*(c_i-1)/2.
        # Ways to choose k edges: C(c_i, 2) choose k.
        # We convolve this for each layer.
        
        # Precompute internal edge polynomials for each possible layer size
        # internal_poly[s] = list where coeff[k] = C(s, 2 choose k)
        internal_polys = {}
        for s in range(1, N + 1):
            max_int_edges = s * (s - 1) // 2
            poly_int = [0] * (max_int_edges + 1)
            for k in range(max_int_edges + 1):
                poly_int[k] = nCr_mod(s, 2) # Wait, C(s, 2) is the number of pairs.
                # We need C(num_pairs, k). num_pairs = s*(s-1)//2.
                num_pairs = s * (s - 1) // 2
                poly_int[k] = nCr_mod(num_pairs, k)
            internal_polys[s] = poly_int

        # Convolve internal edges for all layers
        current_poly = [1]
        for s in comp:
            p_int = internal_polys[s]
            new_poly = [0] * (len(current_poly) + len(p_int) - 1)
            for i, c1 in enumerate(current_poly):
                if c1 == 0: continue
                for j, c2 in enumerate(p_int):
                    if c2 == 0: continue
                    new_poly[i+j] = (new_poly[i+j] + c1 * c2) % P
            current_poly = new_poly
        
        # Now handle inter-layer edges
        # For each interface (S_{i-1}, S_i), we need valid bipartite graphs.
        # The number of edges between S_{i-1} and S_i can vary.
        # We need to convolve the distribution of edges for each interface.
        # Let's compute the polynomial for each interface.
        
        # Interface polynomial: coeff[e] = number of valid bipartite graphs with e edges.
        # Valid means every node in S_i has degree >= 1.
        # Total edges possible: u * v.
        # We can iterate over all possible edge counts? 
        # No, we need the distribution.
        # The number of valid bipartite graphs with exactly e edges is:
        # Sum_{j=0 to v} (-1)^j * C(v, j) * (number of graphs with e edges where j specific nodes in S_i have degree 0)
        # If j nodes have degree 0, they are isolated from S_{i-1}.
        # The remaining v-j nodes can have any edges to S_{i-1}.
        # Number of edges can be anything from 0 to u*(v-j).
        # So for a fixed j, the number of graphs with e edges is C(u*(v-j), e).
        # So coeff[e] = Sum_{j=0 to v} (-1)^j * C(v, j) * C(u*(v-j), e)
        
        # We can compute this polynomial for each interface.
        
        # Let's build the full polynomial by convolving interface polynomials.
        
        # Optimization: Since N is small, we can just compute the full polynomial for the current composition.
        # Start with poly = current_poly (internal edges)
        # For each interface (u, v):
        #   Compute interface_poly
        #   Convolve
        
        # But wait, we need to sum over all compositions.
        # We can accumulate into total_poly.
        
        # Let's do the convolution step by step.
        # Current poly represents the distribution of edges so far.
        
        # We need to handle the interfaces one by one.
        # The interfaces are between (comp[i-1], comp[i]) for i from 1 to len(comp)-1.
        
        # Let's create a list of interface polynomials.
        interface_polys = []
        for i in range(1, len(comp)):
            u = comp[i-1]
            v = comp[i]
            max_edges = u * v
            iface_poly = [0] * (max_edges + 1)
            for e in range(max_edges + 1):
                val = 0
                for j in range(v + 1):
                    term = (nCr_mod(v, j) * nCr_mod(u * (v - j), e)) % P
                    if j % 2 == 1:
                        val = (val - term + P) % P
                    else:
                        val = (val + term) % P
                iface_poly[e] = val
            interface_polys.append(iface_poly)
        
        # Now convolve current_poly with all interface_polys
        # Since we already have current_poly (internal edges), we convolve with interface_polys sequentially.
        
        # To optimize, we can do one big convolution or sequential. Sequential is easier.
        
        # But wait, we need to be careful with the size of the polynomial.
        # Max edges is N*(N-1)/2.
        # Let's ensure the arrays are large enough.
        
        # We can just maintain a single polynomial for the current composition.
        # Start with internal edges.
        # Then convolve with each interface.
        
        # Let's restart the poly for this composition.
        poly = [1] # 0 edges, 1 way (from internal edges of empty layers? No, internal edges are handled)
        # Wait, I already computed internal edges into current_poly.
        # Let's use that.
        
        # Re-compute internal edges properly
        poly = [1]
        for s in comp:
            p_int = internal_polys[s]
            new_poly = [0] * (len(poly) + len(p_int) - 1)
            for i, c1 in enumerate(poly):
                if c1 == 0: continue
                for j, c2 in enumerate(p_int):
                    if c2 == 0: continue
                    new_poly[i+j] = (new_poly[i+j] + c1 * c2) % P
            poly = new_poly
            
        # Now convolve with interfaces
        for iface_poly in interface_polys:
            new_poly = [0] * (len(poly) + len(iface_poly) - 1)
            for i, c1 in enumerate(poly):
                if c1 == 0: continue
                for j, c2 in enumerate(iface_poly):
                    if c2 == 0: continue
                    new_poly[i+j] = (new_poly[i+j] + c1 * c2) % P
            poly = new_poly
            
        # Multiply by vertex assignment ways
        for i in range(len(poly)):
            poly[i] = (poly[i] * ways_assign) % P
            
        # Add to total_poly
        for i in range(len(poly)):
            total_poly[i] = (total_poly[i] + poly[i]) % P

    # Output results for M = N-1 to N(N-1)/2
    results = []
    start_M = N - 1
    end_M = N * (N - 1) // 2
    for m in range(start_M, end_M + 1):
        results.append(str(total_poly[m]))
    
    print(" ".join(results))

solve()