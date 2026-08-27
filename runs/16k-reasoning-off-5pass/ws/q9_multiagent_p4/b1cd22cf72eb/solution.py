import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        X = int(next(iterator))
        
        U = []
        D = []
        
        for _ in range(N):
            u_val = int(next(iterator))
            d_val = int(next(iterator))
            U.append(u_val)
            D.append(d_val)
            
    except StopIteration:
        return

    # Problem Analysis:
    # We need to find a target height H such that we can reduce U_i and D_i to U'_i and D'_i
    # satisfying:
    # 1. U'_i + D'_i = H
    # 2. 1 <= U'_i <= U_i (can only reduce)
    # 3. 1 <= D'_i <= D_i (can only reduce)
    # 4. |U'_i - U'_{i+1}| <= X
    #
    # From 1 and 3: D'_i = H - U'_i <= D_i  =>  U'_i >= H - D_i
    # From 2: U'_i <= U_i
    # So we need a sequence U'_i such that:
    #   H - D_i <= U'_i <= U_i
    #   |U'_i - U'_{i+1}| <= X
    #
    # Let L_i = H - D_i and R_i = U_i.
    # We need to check if there exists a sequence U'_i in [L_i, R_i] with step constraint X.
    # The necessary and sufficient condition for existence is:
    #   max_k (L_k - |i - k| * X) <= R_i   for all i
    #
    # Substituting L_k = H - D_k:
    #   max_k (H - D_k - |i - k| * X) <= U_i
    #   H + max_k (-D_k - |i - k| * X) <= U_i
    #   H - min_k (D_k + |i - k| * X) <= U_i
    #   H <= U_i + min_k (D_k + |i - k| * X)
    #
    # Let C[i] = min_k (D_k + |i - k| * X).
    # Then the maximum valid H is min_i (U_i + C[i]).
    #
    # We compute C[i] using the 1D distance transform (two passes) in O(N).
    
    # Forward pass: F[i] = min(F[i-1] + X, D[i])
    # Computes min_{k <= i} (D[k] + (i - k) * X)
    F = [0] * N
    F[0] = D[0]
    for i in range(1, N):
        F[i] = min(F[i-1] + X, D[i])
        
    # Backward pass: B[i] = min(B[i+1] + X, D[i])
    # Computes min_{k >= i} (D[k] + (k - i) * X)
    B = [0] * N
    B[N-1] = D[N-1]
    for i in range(N-2, -1, -1):
        B[i] = min(B[i+1] + X, D[i])
        
    # Combine to get C[i] = min(F[i], B[i])
    # C[i] represents min_k (D[k] + |i - k| * X)
    C = [min(F[i], B[i]) for i in range(N)]
    
    # Calculate max_H = min_i (U[i] + C[i])
    max_H = float('inf')
    
    for i in range(N):
        val = U[i] + C[i]
        if val < max_H:
            max_H = val
            
    # Calculate total cost
    # Cost = sum(U_i + D_i) - N * H
    # Since we can only reduce, the cost is the total reduction needed.
    # The minimal cost is achieved when H is maximized.
    total_original = sum(U) + sum(D)
    cost = total_original - N * max_H
    
    print(cost)

if __name__ == '__main__':
    solve()