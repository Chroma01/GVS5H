import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
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

    # Calculate S_i = U_i + D_i
    S = [U[i] + D[i] for i in range(N)]
    
    # Calculate max(S)
    max_S = max(S)
    
    # Calculate P_i = max_{1<=j<=i} (j*X - D_j) - i*X
    # Using 0-based indexing for implementation:
    # j in 0..i corresponds to 1..i+1 in problem statement
    # term = (j+1)*X - D[j]
    # P[i] = max(term for j in 0..i) - (i+1)*X
    
    # We can compute this iteratively
    current_max_term = -float('inf')
    P = []
    
    for i in range(N):
        # j = i (current index)
        # term for current j
        term = (i + 1) * X - D[i]
        if term > current_max_term:
            current_max_term = term
        
        # P[i] = current_max_term - (i+1)*X
        P.append(current_max_term - (i + 1) * X)
        
    # Calculate Q_i = min_{i<=j<=N} (U_j + j*X) - i*X
    # Using 0-based indexing:
    # j in i..N-1 corresponds to i+1..N in problem statement
    # term = U[j] + (j+1)*X
    # Q[i] = min(term for j in i..N-1) - (i+1)*X
    
    # Compute suffix minimums
    # We can do this by iterating backwards
    current_min_term = float('inf')
    Q = [0] * N
    
    for i in range(N - 1, -1, -1):
        # j = i (current index)
        term = U[i] + (i + 1) * X
        if term < current_min_term:
            current_min_term = term
        
        # Q[i] = current_min_term - (i+1)*X
        Q[i] = current_min_term - (i + 1) * X
        
    # Calculate M = min_i (Q_i - P_i)
    M = float('inf')
    for i in range(N):
        val = Q[i] - P[i]
        if val < M:
            M = val
            
    # Determine optimal H
    # H_opt = min(M, max_S)
    # Since M can be very small (negative), and max_S is positive, we take min.
    # If M >= max_S, we can achieve cost 0.
    
    H_opt = min(M, max_S)
    
    # Calculate cost
    total_cost = 0
    for s in S:
        if s > H_opt:
            total_cost += (s - H_opt)
            
    print(total_cost)

if __name__ == '__main__':
    solve()