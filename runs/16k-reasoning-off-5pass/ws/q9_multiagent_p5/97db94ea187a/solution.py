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
    
    K = N // 2
    
    # Precompute binomial coefficients modulo P
    # We need C(n, k) for n up to K*K (for F) and n up to N (for partition count)
    # Max n for F is K*K = 225. Max n for partition is 30.
    # Let's compute up to 300 to be safe.
    MAX_N = 300
    C = [[0] * (MAX_N + 1) for _ in range(MAX_N + 1)]
    for i in range(MAX_N + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % P
            
    # DP state: dp[i][j][m] = number of connected bipartite graphs with i vertices in A, j in B, m edges
    # Dimensions: i in [1, K], j in [0, K], m in [0, K*K]
    # We can flatten or use list of lists.
    # Since K <= 15, K*K <= 225.
    # Size: 16 * 16 * 226 approx 57000.
    
    max_m = K * K
    # dp[i][j] will be a list of size max_m + 1
    dp = [[ [0] * (max_m + 1) for _ in range(K + 1)] for _ in range(K + 1)]
    
    # Base cases
    # H(1, 0, 0) = 1 (single vertex in A, 0 in B, 0 edges)
    dp[1][0][0] = 1
    
    # Iterate over total vertices in A (i) and B (j)
    # Order: increasing i+j is not strictly required if we iterate i then j, 
    # because (k, l) with k < i are already computed, and (i, l) with l < j are computed.
    # So simple nested loops work.
    
    for i in range(1, K + 1):
        for j in range(0, K + 1):
            if i == 1 and j == 0:
                continue
            
            # Initialize with F(i, j, m) = C(i*j, m)
            edges_total = i * j
            for m in range(max_m + 1):
                if edges_total == 0:
                    dp[i][j][m] = 1 if m == 0 else 0
                else:
                    dp[i][j][m] = C[edges_total][m]
            
            # Subtract contributions from smaller components
            # Formula: F(i, j, m) = sum_{k=1..i, l=0..j} C(i-1, k-1)*C(j, l) * sum_{p} H(k, l, p) * F(i-k, j-l, m-p)
            # We solve for H(i, j, m) by subtracting terms where (k, l) != (i, j).
            
            for k in range(1, i + 1):
                for l in range(0, j + 1):
                    if k == i and l == j:
                        continue
                    
                    ways = (C[i-1][k-1] * C[j][l]) % P
                    if ways == 0:
                        continue
                    
                    rem_u = i - k
                    rem_v = j - l
                    rem_edges = rem_u * rem_v
                    
                    # If dp[k][l] is all zero, skip
                    # Check if any non-zero to save time
                    # Since we are inside loops, checking all might be costly.
                    # But dp[k][l] is computed.
                    
                    if rem_edges == 0:
                        # F(rem_u, rem_v, x) is 1 if x=0 else 0.
                        # So we subtract ways * dp[k][l][m] for all m.
                        for m in range(max_m + 1):
                            if dp[k][l][m] == 0:
                                continue
                            dp[i][j][m] = (dp[i][j][m] - ways * dp[k][l][m]) % P
                    else:
                        # Convolution: subtract ways * sum_p dp[k][l][p] * C[rem_edges][m-p]
                        # We iterate p and update dp[i][j]
                        
                        # Optimization: Pre-check if dp[k][l] has any non-zero
                        # We can do this by checking the first non-zero or just iterating.
                        # Given the constraints and Python speed, iterating p is safer.
                        
                        # We iterate p where dp[k][l][p] is non-zero.
                        
                        # To avoid O(M^2), we iterate p and x.
                        # Complexity: sum_{k,l} (k*l * rem_edges) ~ K^4 * M.
                        
                        # We need to be careful: we are subtracting from dp[i][j].
                        # We can accumulate the total subtraction for dp[i][j].
                        # So we can just update dp[i][j] directly.
                        
                        # Note: We must not use updated values of dp[i][j] for the same (k,l) step?
                        # No, because (k, l) != (i, j), and we process each (i, j) once, it's fine.
                        
                        # However, we are iterating k, l.
                        # We should accumulate the total subtraction for dp[i][j].
                        # So we can just update dp[i][j] directly.
                        
                        # But wait, if we update dp[i][j] in place, does it affect subsequent (k', l')?
                        # No, because subsequent (k', l') will read dp[i][j] (which is being computed)
                        # but they are subtracting FROM it.
                        # The formula is: H = F - sum_{smaller} ...
                        # So we start with F, and subtract terms.
                        # The order of subtraction doesn't matter.
                        
                        # So:
                        for p in range(k * l + 1):
                            if dp[k][l][p] == 0:
                                continue
                            val = (ways * dp[k][l][p]) % P
                            # Iterate x
                            # C[rem_edges][x] is non-zero for 0 <= x <= rem_edges
                            # We need to update dp[i][j][p+x]
                            # We can iterate x from 0 to rem_edges
                            # But we can also check if p+x > max_m
                            
                            # Optimization: limit x such that p+x <= max_m
                            limit_x = min(rem_edges, max_m - p)
                            
                            for x in range(limit_x + 1):
                                term = (val * C[rem_edges][x]) % P
                                dp[i][j][p+x] = (dp[i][j][p+x] - term) % P

    # Final Answer
    # Ans[M] = C(N-1, K-1) * dp[K][K][M]
    # Output for M = N-1 to N(N-1)/2
    
    # Precompute C(N-1, K-1)
    ways_partition = C[N-1][K-1]
    
    results = []
    max_M = N * (N - 1) // 2
    
    for M in range(N - 1, max_M + 1):
        if M > max_m:
            res = 0
        else:
            res = (ways_partition * dp[K][K][M]) % P
        results.append(str(res))
        
    print(" ".join(results))

if __name__ == '__main__':
    solve()