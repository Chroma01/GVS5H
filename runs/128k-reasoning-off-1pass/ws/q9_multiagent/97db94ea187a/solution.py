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

    # N is even, so we split into two sets of size N/2
    n_half = N // 2
    
    # Maximum number of edges in a bipartite graph with parts n_half, n_half
    max_edges = n_half * n_half
    
    # Precompute factorials and inverse factorials modulo P
    # We need up to max_edges for combinations C(nm, k)
    # Also need up to n_half for binomial coefficients in the recurrence
    limit = max(max_edges, n_half) + 5
    
    fact = [1] * limit
    inv = [1] * limit
    
    for i in range(1, limit):
        fact[i] = (fact[i-1] * i) % P
        
    inv[limit-1] = pow(fact[limit-1], P - 2, P)
    for i in range(limit-2, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % P
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % P
        return (num * den) % P

    # DP State:
    # dp[i][j][k] = number of connected bipartite graphs with parts of size i and j having exactly k edges
    # Dimensions: (n_half + 1) x (n_half + 1) x (max_edges + 1)
    
    # Initialize DP table with 0
    dp = [[[0] * (max_edges + 1) for _ in range(n_half + 1)] for _ in range(n_half + 1)]
    
    # Base case: dp[1][0][0] = 1.
    # A connected bipartite graph with 1 node in part A and 0 nodes in part B is just a single node.
    dp[1][0][0] = 1
    
    # We need to compute dp[i][j][k] for all i, j.
    # Iterate i from 1 to n_half, j from 0 to n_half.
    for i in range(1, n_half + 1):
        for j in range(0, n_half + 1):
            if i == 1 and j == 0:
                continue
            
            # Total(i, j, k) = C(i*j, k)
            total_edges = i * j
            
            # Initialize sub array for subtraction sum
            sub = [0] * (total_edges + 1)
            
            # Iterate over a, b (size of component containing vertex 1)
            for a in range(1, i + 1):
                for b in range(0, j + 1):
                    if a == i and b == j:
                        continue
                    
                    # Ways to choose the component vertices
                    # C(i-1, a-1) * C(j, b)
                    ways_choose = (nCr_mod(i-1, a-1) * nCr_mod(j, b)) % P
                    
                    if ways_choose == 0:
                        continue
                    
                    # Remaining nodes
                    rem_i = i - a
                    rem_j = j - b
                    rem_edges = rem_i * rem_j
                    
                    # Iterate p (edges in component)
                    max_p = a * b
                    for p in range(0, max_p + 1):
                        if dp[a][b][p] == 0:
                            continue
                        
                        # Iterate z (edges in rest)
                        # z goes from 0 to rem_edges
                        # k = p + z
                        # We only care about k <= total_edges
                        
                        z_max = rem_edges
                        if p + z_max > total_edges:
                            z_max = total_edges - p
                        
                        for z in range(0, z_max + 1):
                            term = (dp[a][b][p] * nCr_mod(rem_edges, z)) % P
                            val = (ways_choose * term) % P
                            sub[p + z] = (sub[p + z] + val) % P
            
            # Compute dp[i][j][k]
            for k in range(0, total_edges + 1):
                val = nCr_mod(total_edges, k)
                res = (val - sub[k]) % P
                dp[i][j][k] = res

    # The answer for each M is dp[n_half][n_half][M]
    # M ranges from N-1 to N(N-1)/2
    start_M = N - 1
    end_M = N * (N - 1) // 2
    
    results = []
    max_dp_edges = n_half * n_half
    
    for m in range(start_M, end_M + 1):
        if m > max_dp_edges:
            results.append(0)
        else:
            res = dp[n_half][n_half][m]
            results.append(res)
            
    print(" ".join(map(str, results)))

if __name__ == '__main__':
    solve()