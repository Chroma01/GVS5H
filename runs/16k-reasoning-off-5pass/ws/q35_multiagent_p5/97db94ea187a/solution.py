import sys

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    P = int(input_data[1])
    
    # Precompute binomial coefficients modulo P
    # We need nCr for n up to N*(N-1)//2, but actually we only need C(A, M)
    # where A is the number of allowed edges. Max edges is N*(N-1)//2.
    # However, computing factorials up to ~450 is cheap.
    MAX_EDGES = N * (N - 1) // 2
    fact = [1] * (MAX_EDGES + 1)
    inv = [1] * (MAX_EDGES + 1)
    
    for i in range(1, MAX_EDGES + 1):
        fact[i] = (fact[i-1] * i) % P
        
    inv[MAX_EDGES] = pow(fact[MAX_EDGES], P - 2, P)
    for i in range(MAX_EDGES - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % P
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % P
        return (num * den) % P

    # Generate all valid layering size sequences
    # L[0] = 1
    # Sum(L) = N
    # Sum(L[k] for k even) = N/2
    # Sum(L[k] for k odd) = N/2
    
    half_N = N // 2
    target_even_sum = half_N  # Includes L[0]=1, so remaining even layers sum to half_N - 1
    target_odd_sum = half_N
    
    layerings = []
    
    def generate_layerings(current_sum, current_even_sum, current_odd_sum, current_layers):
        if current_sum == N:
            if current_even_sum == target_even_sum and current_odd_sum == target_odd_sum:
                layerings.append(list(current_layers))
            return
        
        # Determine the parity of the next layer index
        # current_layers has length D, next is index D
        next_idx = len(current_layers)
        is_even_idx = (next_idx % 2 == 0)
        
        # Remaining vertices to distribute
        remaining = N - current_sum
        
        # We need to distribute 'remaining' vertices into layers next_idx, next_idx+1, ...
        # Let's try all possible sizes for the next layer
        # The next layer size L can be from 1 to remaining
        # But we must ensure that the remaining sum constraints are satisfiable.
        
        # Max possible sum for even/odd layers from here?
        # If we put all remaining in next layer, that's one option.
        # We can prune if it's impossible to reach the target sums.
        
        for L in range(1, remaining + 1):
            new_sum = current_sum + L
            new_even = current_even_sum
            new_odd = current_odd_sum
            
            if is_even_idx:
                new_even += L
                if new_even > target_even_sum:
                    break # Since L increases, new_even will only increase
            else:
                new_odd += L
                if new_odd > target_odd_sum:
                    break
            
            # Check if it's possible to satisfy the remaining constraints
            # Remaining vertices: remaining - L
            # If next_idx + 1 is even, we need to add to even sum.
            # If next_idx + 1 is odd, we need to add to odd sum.
            # Actually, we just need to check if the remaining sum can be distributed.
            # The remaining vertices must be split into layers.
            # The parity of the next layer (next_idx+1) determines which sum it adds to.
            # Let rem = remaining - L.
            # If we put all rem in the next layer (if valid), does it exceed?
            # We already checked the immediate addition.
            # We need to ensure that the remaining sum can be formed by subsequent layers.
            # Since subsequent layers can be any size >= 1, the only constraint is that
            # we have enough "room" in the target sums.
            # Specifically, if we need to add X to even sum and Y to odd sum from the remaining 'rem' vertices,
            # we must have X >= 0, Y >= 0, X+Y = rem.
            # And we must be able to partition 'rem' into layers that sum to X (even layers) and Y (odd layers).
            # This is always possible if X >= 0 and Y >= 0, because we can just have one layer of size X (if next is even)
            # and then stop? No, we need to form the sequence.
            # Actually, the only hard constraint is that we don't exceed the targets.
            # And we must be able to finish exactly.
            # Since we can always add a layer of size 1, we can always adjust.
            # The only pruning is if new_even > target or new_odd > target.
            
            current_layers.append(L)
            generate_layerings(new_sum, new_even, new_odd, current_layers)
            current_layers.pop()

    generate_layerings(1, 1, 0, [1])

    # For each layering, compute the contribution to the answer for each M
    # Answers for M = N-1 to N(N-1)/2
    ans = [0] * (MAX_EDGES + 1)
    
    for layers in layerings:
        # layers is a list [L0, L1, ..., LD]
        # L0 = 1
        # Compute the DP for inclusion-exclusion
        
        # DP state: dp[j][a] = sum of (-1)^j for subsets chosen so far
        # where j is the total number of vertices chosen in the subset S
        # and a is the number of allowed edges in the reduced graph
        # We process layer by layer.
        
        # Initialize DP
        # dp[j][a]
        # Max j is N, Max a is MAX_EDGES
        # Use a dictionary or list of lists. List of lists is faster.
        
        # dp[j][a]
        dp = [[0] * (MAX_EDGES + 1) for _ in range(N + 1)]
        dp[0][0] = 1
        
        num_layers = len(layers)
        
        for k in range(num_layers):
            Lk = layers[k]
            # Next layer size
            if k + 1 < num_layers:
                Lk1 = layers[k + 1]
            else:
                Lk1 = 0
            
            # Edges within Sk: always allowed
            edges_within = Lk * (Lk - 1) // 2
            
            # Edges between Sk and Sk+1
            # Total possible: Lk * Lk1
            # If we choose s_{k+1} vertices in S_{k+1} to be in subset S,
            # then edges between these s_{k+1} vertices and Sk are forbidden.
            # Number of forbidden edges = s_{k+1} * Lk
            # So allowed edges between Sk and Sk+1 = Lk * Lk1 - s_{k+1} * Lk
            
            # We iterate over the current DP states and update for the next layer
            # The new DP will be for layers 0..k+1
            
            new_dp = [[0] * (MAX_EDGES + 1) for _ in range(N + 1)]
            
            # We need to iterate over all possible s_k (number of vertices in Sk chosen for S)
            # s_k ranges from 0 to Lk
            # For each s_k, there are C(Lk, s_k) ways to choose the vertices.
            # The sign contribution is (-1)^s_k.
            
            # Precompute binomial coeffs for this layer
            # C(Lk, s)
            C_Lk = [1] * (Lk + 1)
            for s in range(1, Lk + 1):
                # C(n, k) = C(n, k-1) * (n-k+1) / k
                # But we need modulo P. Since P is large prime, we can use precomputed factorials.
                # However, Lk is small (<=30), so we can compute directly or use the global nCr_mod
                pass
            
            # To optimize, we can iterate over previous DP states
            # prev_dp[j][a]
            # For each (j, a), we try all s_k in 0..Lk
            # new_j = j + s_k
            # new_a = a + edges_within + (Lk * Lk1 - s_k * Lk)  <-- Wait, this is wrong.
            
            # Correction:
            # The term (Lk * Lk1 - s_{k+1} * Lk) depends on s_{k+1}, which is chosen in the NEXT step.
            # So when processing layer k, we only add edges within Sk and edges between Sk-1 and Sk?
            # No, the edge count A_S is global.
            # Let's redefine the DP transition.
            
            # When we are at layer k, we choose s_k vertices from Sk.
            # This choice affects:
            # 1. Edges within Sk: always added.
            # 2. Edges between Sk and Sk+1: The number of allowed edges depends on s_{k+1}.
            #    But s_{k+1} is not chosen yet.
            #    So we can't add the inter-layer edges yet?
            #    Or we can add them partially?
            
            # Alternative: Add inter-layer edges between Sk-1 and Sk when processing Sk.
            # Let's say when processing layer k, we add:
            # - Edges within Sk
            # - Edges between Sk-1 and Sk, adjusted for s_k.
            #   Specifically, if we chose s_k vertices in Sk, then edges between these s_k vertices and Sk-1 are forbidden.
            #   So allowed edges between Sk-1 and Sk = L_{k-1} * Lk - s_k * L_{k-1}.
            #   Note: For k=0, there is no previous layer.
            
            # So, transition for layer k (k>=1):
            # new_a = a + edges_within_Sk + (L_{k-1} * Lk - s_k * L_{k-1})
            
            # For k=0:
            # new_a = a + edges_within_S0
            
            # This works!
            
            for j in range(N + 1):
                for a in range(MAX_EDGES + 1):
                    if dp[j][a] == 0:
                        continue
                    
                    current_val = dp[j][a]
                    
                    # Try all s_k
                    for s_k in range(Lk + 1):
                        new_j = j + s_k
                        if new_j > N:
                            break
                        
                        # Calculate added edges
                        added_edges = edges_within
                        
                        if k > 0:
                            L_prev = layers[k-1]
                            # Forbidden edges: s_k * L_prev
                            added_edges += L_prev * Lk - s_k * L_prev
                        
                        new_a = a + added_edges
                        if new_a > MAX_EDGES:
                            # Since s_k increases, added_edges decreases (if k>0) or stays same (if k=0)
                            # If k=0, added_edges is constant. If new_a > MAX, all larger s_k will also exceed?
                            # No, for k=0, added_edges is constant. So if it exceeds, we can break?
                            # But new_a = a + constant. If a + constant > MAX, then for this a, no s_k works.
                            # But we are iterating s_k.
                            # Actually, if new_a > MAX, we can just skip.
                            pass
                        else:
                            # Sign: (-1)^s_k
                            sign = 1 if s_k % 2 == 0 else -1
                            term = (current_val * nCr_mod(Lk, s_k)) % P
                            if sign == -1:
                                term = (-term) % P
                            
                            new_dp[new_j][new_a] = (new_dp[new_j][new_a] + term) % P

            dp = new_dp

        # After processing all layers, sum up the contributions for each M
        # The answer for M is sum_{j, a} dp[j][a] * C(a, M)
        # But wait, dp[j][a] is the sum of (-1)^|S| for subsets S that result in a allowed edges.
        # The number of graphs with exactly M edges is sum_{S} (-1)^|S| * C(A_S, M).
        # So we need to compute sum_{a} dp[N][a] * C(a, M)?
        # No, dp[j][a] sums over all j. But the inclusion-exclusion is over all subsets S of U.
        # U is all vertices except root. So |S| can be anything from 0 to N-1.
        # The term is (-1)^|S|.
        # So we sum over all j and a: dp[j][a] * C(a, M).
        
        for a in range(MAX_EDGES + 1):
            if dp[j][a] == 0: # This line is wrong, j is not defined here
                continue
            
            # We need to sum over all j
            total_val = 0
            for j in range(N + 1):
                total_val = (total_val + dp[j][a]) % P
            
            if total_val != 0:
                # Add to answer for M = a? No.
                # The term is C(a, M).
                # We want to add total_val * C(a, M) to ans[M].
                # But we are iterating a.
                # So for each M, ans[M] += total_val * C(a, M).
                # This is O(N^2) per layering.
                # Total complexity: Num_layerings * N^2 * N^2? No.
                # The DP is O(N * MAX_EDGES * N).
                # The final summation is O(MAX_EDGES * N).
                # Total per layering: O(N^2 * MAX_EDGES).
                # MAX_EDGES ~ 450, N=30. 30^2 * 450 = 405,000.
                # Num_layerings? For N=30, this might be large.
                # But let's hope it's small enough.
                
                for M in range(N - 1, MAX_EDGES + 1):
                    comb = nCr_mod(a, M)
                    if comb != 0:
                        ans[M] = (ans[M] + total_val * comb) % P

    # Output answers for M = N-1 to N(N-1)/2
    results = []
    for M in range(N - 1, MAX_EDGES + 1):
        results.append(str(ans[M]))
        
    print(" ".join(results))

solve()