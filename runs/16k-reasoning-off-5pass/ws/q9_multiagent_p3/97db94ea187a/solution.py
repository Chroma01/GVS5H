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

    half_N = N // 2
    
    # Precompute binomial coefficients modulo P
    # We need up to (N/2)*(N/2) for the DP combinations.
    max_n_comb = (half_N * half_N) + 10
    C = [[0] * (max_n_comb + 1) for _ in range(max_n_comb + 1)]
    for i in range(max_n_comb + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % P

    # dp[a][b][x] = number of connected bipartite graphs with parts of size a and b
    # (where the part of size a contains vertex 1) with exactly x edges.
    # a ranges from 1 to half_N, b ranges from 0 to half_N.
    # x ranges from 0 to a*b.
    
    # Initialize DP table
    # Dimensions: (half_N + 1) x (half_N + 1)
    # Each entry will be a list of size a*b + 1
    dp = [[None] * (half_N + 1) for _ in range(half_N + 1)]

    # Base case: a=1, b=0. One vertex in part A, zero in part B.
    # Connected graph with 1 vertex and 0 edges.
    dp[1][0] = [1]

    # Iterate over total size S = a + b from 2 to N
    for S in range(2, N + 1):
        for a in range(1, half_N + 1):
            b = S - a
            if b < 0 or b > half_N:
                continue
            
            limit = a * b
            # Initialize dp[a][b] with total bipartite graphs C(a*b, x)
            current_dp = [C[limit][x] for x in range(limit + 1)]
            
            # Subtract disconnected cases using inclusion-exclusion
            # Iterate over the size of the component containing vertex 1: i (from A), l (from B)
            # i ranges from 1 to a, l ranges from 0 to b
            # Condition: i + l < a + b (strictly smaller component)
            
            for i in range(1, a + 1):
                for l in range(0, b + 1):
                    if i + l == a + b:
                        continue
                    
                    # Number of ways to choose the specific vertices for the component
                    # Choose i-1 from remaining a-1 in A, and l from b in B
                    ways_choose = (C[a-1][i-1] * C[b][l]) % P
                    if ways_choose == 0:
                        continue
                    
                    # Max edges in the component
                    comp_max = i * l
                    # Max edges in the remaining part
                    rem_max = (a - i) * (b - l)
                    
                    # We need to convolve dp[i][l] (polynomial of connected graphs on component)
                    # with C[rem_max] (polynomial of any graphs on remaining vertices)
                    # Then subtract ways_choose * convolution from current_dp
                    
                    dp_i_l = dp[i][l]
                    C_rem = C[rem_max]
                    
                    # Temporary array to store the sum of products to subtract
                    # Size needed is up to limit
                    sub = [0] * (limit + 1)
                    
                    # Perform convolution: sum_{p} dp[i][l][p] * C[rem_max][k-p]
                    # Iterate p (edges in component)
                    for p in range(comp_max + 1):
                        if dp_i_l[p] == 0:
                            continue
                        val_p = dp_i_l[p]
                        # Iterate rem (edges in remaining)
                        for rem in range(rem_max + 1):
                            idx = p + rem
                            if idx > limit:
                                break
                            term = (val_p * C_rem[rem]) % P
                            sub[idx] = (sub[idx] + term) % P
                    
                    # Subtract from current_dp
                    for k in range(limit + 1):
                        if sub[k] > 0:
                            current_dp[k] = (current_dp[k] - ways_choose * sub[k]) % P
                            
            dp[a][b] = current_dp

    # The problem asks for the number of connected graphs with N vertices and M edges
    # such that the bipartition sizes are equal (N/2, N/2).
    # Vertex 1 must be in the "even" set.
    # We have computed dp[half_N][half_N][M] which counts connected bipartite graphs
    # with parts of size half_N and half_N (containing vertex 1 in the first part).
    # We need to multiply by the number of ways to choose the other half_N - 1 vertices
    # for the even set from the remaining N - 1 vertices.
    
    ways_choose = C[N-1][half_N - 1]
    
    results = []
    max_M = N * (N - 1) // 2
    dp_final = dp[half_N][half_N]
    limit_final = half_N * half_N
    
    for M in range(N - 1, max_M + 1):
        if M > limit_final:
            ans = 0
        else:
            ans = (ways_choose * dp_final[M]) % P
        results.append(str(ans))
        
    print(" ".join(results))

if __name__ == '__main__':
    solve()