import sys

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    A = [int(input_data[idx + i]) for i in range(N)]
    
    # Compute prefix sums
    P = [0] * (N + 1)
    for i in range(N):
        P[i+1] = P[i] + A[i]
    
    # Compute L[K]: max absorbable from the left into K
    L = [0] * N
    # Stack: list of (index, C_value), C strictly decreasing from bottom to top
    # C_j = A_j + P_j for j >= 1, C_0 = +infinity
    stack = [(0, float('inf'))]
    
    for K in range(1, N + 1):
        T = P[K]
        # Pop from top while C < T
        while stack and stack[-1][1] < T:
            stack.pop()
        j_star = stack[-1][0]
        L[K-1] = P[K-1] - P[j_star]
        
        # Add C_K = A_K + P_K to the stack
        C_K = A[K-1] + P[K]
        while stack and stack[-1][1] <= C_K:
            stack.pop()
        stack.append((K, C_K))
    
    # Compute R[K]: max absorbable from the right into K
    # Process the reversed array
    R = [0] * N
    # Compute suffix sums
    S = [0] * (N + 1)
    for i in range(N - 1, -1, -1):
        S[i] = S[i+1] + A[i]
    
    # For the right side, we process from right to left
    # Define D_j = A_j + S_j (suffix sum + A_j)
    # Condition: D_j < S_K for all j in [K+1, R]
    # R[K] = S_{K+1} - S_{R+1} = S_{K+1} - S_{j*} where j* is rightmost in [K+1, N] with D_j >= S_K
    # Actually, let's process from right to left, treating K as going from N down to 1
    
    stack = [(N, float('inf'))]  # sentinel at index N (beyond the array)
    
    for K in range(N - 1, -1, -1):
        T = S[K]
        # Pop from top while C < T
        while stack and stack[-1][1] < T:
            stack.pop()
        j_star = stack[-1][0]
        R[K] = S[K+1] - S[j_star]
        
        # Add D_K = A_K + S_K to the stack
        D_K = A[K] + S[K]
        while stack and stack[-1][1] <= D_K:
            stack.pop()
        stack.append((K, D_K))
    
    # Compute answers
    result = [A[K] + L[K] + R[K] for K in range(N)]
    print(' '.join(map(str, result)))

solve()