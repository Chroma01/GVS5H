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

    # Precompute Binomial Coefficients modulo P
    # Max degree needed is N*(N-1)/2 which is approx 435 for N=30
    max_edges = N * (N - 1) // 2
    
    # Pascal's triangle for binomial coefficients
    # C[n][k] stores nCk % P
    # We only need up to max_edges for the binomial coefficients
    # However, the exponents in (1+x)^K can be up to max_edges.
    # So we need C[n][k] for n up to max_edges.
    C = [[0] * (max_edges + 1) for _ in range(max_edges + 1)]
    for i in range(max_edges + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = (C[i-1][j-1] + C[i-1][j]) % P

    # DP State: dp[(i, j, d, p)] = list of coefficients
    # i: number of vertices used (1 to N)
    # j: size of the last layer (1 to N-i)
    # d: difference |Even| - |Odd| (range -N/2 to N/2)
    # p: parity of the last layer index (0 for even index, 1 for odd index)
    # Value: A list of coefficients representing the polynomial for edge counts.
    
    # Initial State:
    # L0 = {1}. i=1, j=1.
    # d = 1 (1 vertex in Even, 0 in Odd).
    # p = 0 (Layer 0 is even index).
    # Polynomial: (1+x)^0 = 1. Coeffs: [1] (0 edges).
    
    dp = {}
    start_key = (1, 1, 1, 0)
    dp[start_key] = [1] 
    
    min_d = -N // 2
    max_d = N // 2
    
    # Iterate i from 1 to N-1
    for i in range(1, N):
        current_states = list(dp.keys())
        
        for (u, last_sz, d, parity) in current_states:
            poly = dp[(u, last_sz, d, parity)]
            if not poly:
                continue
            
            remaining = N - u
            for k in range(1, remaining + 1):
                new_parity = 1 - parity
                if parity == 0:
                    new_d = d - k
                else:
                    new_d = d + k
                
                if new_d < min_d or new_d > max_d:
                    continue
                
                P_k = k * (k - 1) // 2
                Q = u * k
                
                A = P_k + Q
                B = P_k
                
                current_deg = len(poly) - 1
                new_deg = current_deg + A
                
                # Optimization for base case [1]
                if len(poly) == 1:
                    res = [0] * (A + 1)
                    for t in range(A + 1):
                        val = C[A][t]
                        if t <= B:
                            val = (val - C[B][t]) % P
                        res[t] = val
                else:
                    res = [0] * (new_deg + 1)
                    for idx, val in enumerate(poly):
                        if val == 0:
                            continue
                        # Add (1+x)^A
                        for t in range(A + 1):
                            res[t + idx] = (res[t + idx] + val * C[A][t]) % P
                        # Subtract (1+x)^B
                        for t in range(B + 1):
                            res[t + idx] = (res[t + idx] - val * C[B][t]) % P
                
                new_key = (i + k, k, new_d, new_parity)
                
                if new_key in dp:
                    existing = dp[new_key]
                    len_res = len(res)
                    len_existing = len(existing)
                    if len_res > len_existing:
                        existing.extend([0] * (len_res - len_existing))
                    for m in range(len_res):
                        existing[m] = (existing[m] + res[m]) % P
                else:
                    dp[new_key] = res

    # Collect answers
    ans = [0] * (max_edges + 1)
    
    for j in range(1, N + 1):
        for d in range(min_d, max_d + 1):
            for p in range(2):
                key = (N, j, d, p)
                if key in dp:
                    poly = dp[key]
                    len_poly = len(poly)
                    for m in range(len_poly):
                        if m <= max_edges:
                            ans[m] = (ans[m] + poly[m]) % P
                            
    # Output
    results = []
    for m in range(N - 1, max_edges + 1):
        results.append(str(ans[m]))
    
    print(" ".join(results))

if __name__ == '__main__':
    solve()