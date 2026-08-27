import sys

# Increase recursion depth just in case
sys.setrecursionlimit(2000)

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    P = int(input_data[1])

    # Constraints: N <= 30, P is prime.
    # We need to count connected graphs where |EvenDist| == |OddDist|.
    # This implies the graph is bipartite with parts S, T where |S| = |T| = N/2,
    # and 1 is in S (since dist(1)=0 is even).
    # We sum the counts of connected bipartite graphs for each valid bipartition.
    
    half_N = N // 2
    
    # Precompute binomial coefficients modulo P
    # We need C(n, k) for n up to N (approx 30)
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(N + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % P

    # DP to compute dp[i][j][k]: number of connected bipartite graphs with parts of size i, j and k edges.
    # i ranges from 1 to half_N
    # j ranges from 0 to half_N
    # k ranges from 0 to i*j
    
    max_edges = half_N * half_N
    # dp[i][j] will be a list of size (i*j + 1)
    dp = [[None] * (half_N + 1) for _ in range(half_N + 1)]
    
    # Base case: i=1, j=0. Single node, 0 edges. Connected.
    dp[1][0] = [1]

    # Iterate n from 1 to half_N
    for n in range(1, half_N + 1):
        # Iterate m from 0 to half_N
        for m in range(half_N + 1):
            if n == 1 and m == 0:
                continue
            
            # Total graphs with parts n, m and k edges: C(n*m, k)
            # We want to compute dp[n][m][k]
            # Equation: Total[n][m][k] = Sum_{x=1}^{n-1} C(n-1, x-1) * Sum_{y=0}^m C(m, y) * dp[x][y][p] * C((n-x)(m-y), k-p)
            #                                       + Sum_{y=0}^m C(m, y) * dp[n][y][k]
            # Thus: Sum_{y=0}^m C(m, y) * dp[n][y][k] = Total[n][m][k] - (Sum_{x=1}^{n-1} ...)
            # Let RHS = Total[n][m][k] - (Sum_{x=1}^{n-1} ...)
            # Then we have a system of equations for dp[n][0][k], ..., dp[n][m][k].
            # Specifically, for a fixed k, we have:
            # C(m, 0)*dp[n][0][k] + ... + C(m, m)*dp[n][m][k] = RHS
            # We can solve this by iterating m from 0 to half_N.
            # When we are at m, we assume dp[n][y][k] for y < m are already computed.
            # Then we can solve for dp[n][m][k].
            
            size_nm = n * m
            dp_nm = [0] * (size_nm + 1)
            
            # We need to compute the subtraction term: Sum_{x=1}^{n-1} C(n-1, x-1) * Sum_{y=0}^m C(m, y) * dp[x][y][p] * C((n-x)(m-y), k-p)
            # Let's call this `sub_total[k]`.
            # We also need the term Sum_{y=0}^{m-1} C(m, y) * dp[n][y][k] to isolate dp[n][m][k].
            # Let's call this `prefix_sum[k]`.
            
            sub_total = [0] * (size_nm + 1)
            prefix_sum = [0] * (size_nm + 1)
            
            # Compute sub_total
            # Iterate x from 1 to n-1
            for x in range(1, n):
                # Iterate y from 0 to m
                for y in range(0, m + 1):
                    if dp[x][y] is None: continue
                    
                    ways_choose_x = C[n-1][x-1]
                    ways_choose_y = C[m][y]
                    if ways_choose_x == 0 or ways_choose_y == 0: continue
                    
                    # Edges in rest: (n-x)*(m-y)
                    rest_edges = (n - x) * (m - y)
                    if rest_edges < 0: continue
                    
                    # We need to convolve dp[x][y] with C(rest_edges, .)
                    # dp[x][y][p] * C(rest_edges, k-p)
                    
                    # Optimization: iterate p and k
                    # Since we are adding to sub_total, we can do it directly.
                    # To speed up, we can check if dp[x][y] has non-zero entries.
                    
                    # We iterate p over the range of dp[x][y]
                    # dp[x][y] has length x*y + 1
                    len_dp = x * y + 1
                    for p in range(len_dp):
                        val = dp[x][y][p]
                        if val == 0: continue
                        
                        # k ranges from p to p + rest_edges
                        # Also k <= size_nm
                        start_k = p
                        end_k = min(size_nm, p + rest_edges)
                        
                        # We can unroll or just loop
                        for k in range(start_k, end_k + 1):
                            # C(rest_edges, k-p)
                            # Since rest_edges can be up to 225, and k-p up to 225
                            # We access C table
                            term = C[rest_edges][k - p]
                            if term == 0: continue
                            
                            sub_total[k] = (sub_total[k] + ways_choose_x * ways_choose_y * val * term) % P
            
            # Compute prefix_sum for y < m
            # prefix_sum[k] = Sum_{y=0}^{m-1} C(m, y) * dp[n][y][k]
            for y in range(0, m):
                if dp[n][y] is None: continue
                coeff = C[m][y]
                if coeff == 0: continue
                
                len_dp = n * y + 1
                for k in range(len_dp):
                    if k > size_nm: break
                    val = dp[n][y][k]
                    if val == 0: continue
                    prefix_sum[k] = (prefix_sum[k] + coeff * val) % P
            
            # Now compute dp[n][m][k]
            # dp[n][m][k] = Total[n][m][k] - sub_total[k] - prefix_sum[k]
            # Total[n][m][k] = C(n*m, k)
            
            for k in range(size_nm + 1):
                total_ways = C[size_nm][k]
                val = (total_ways - sub_total[k] - prefix_sum[k]) % P
                dp_nm[k] = val
            
            dp[n][m] = dp_nm

    # After filling dp, compute answer.
    # Answer for M: Sum_{S} dp[N/2][N/2][M]
    # Number of S: C(N-1, N/2-1).
    
    comb_S = C[N-1][half_N-1]
    max_edges_bip = half_N * half_N
    
    results = []
    # M ranges from N-1 to N(N-1)/2
    for M in range(N-1, N*(N-1)//2 + 1):
        if M > max_edges_bip:
            results.append(0)
        else:
            val = (comb_S * dp[half_N][half_N][M]) % P
            results.append(val)
            
    print(*(results))

if __name__ == '__main__':
    solve()