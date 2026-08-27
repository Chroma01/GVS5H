import sys

# Increase recursion depth just in case, though not needed for this iterative solution
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
    except StopIteration:
        return

    U = []
    D = []
    S = []
    
    # Read N pairs
    for _ in range(N):
        u_val = int(next(iterator))
        d_val = int(next(iterator))
        U.append(u_val)
        D.append(d_val)
        S.append(u_val + d_val)

    # Calculate global upper bound for H based on sum constraints
    # H <= U_i + D_i for all i
    min_S = min(S)
    
    # We need to find the maximum H such that there exists a sequence U'_i satisfying:
    # 1. 0 <= U'_i <= U_i
    # 2. 0 <= H - U'_i <= D_i  =>  H - D_i <= U'_i
    # 3. |U'_i - U'_{i+1}| <= X
    #
    # Combining 1 and 2: max(0, H - D_i) <= U'_i <= U_i
    # Let L_i = max(0, H - D_i) and R_i = U_i.
    # We need to check if there exists a sequence U'_i in [L_i, R_i] with adjacent diff <= X.
    # This is possible iff for all i, j: L_i <= R_j + X * |i - j| (and symmetric).
    # This simplifies to: L_i <= min_j (R_j + X * |i - j|) for all i.
    # Let K_i = min_j (R_j + X * |i - j|).
    # Then we need max(0, H - D_i) <= K_i.
    # This implies two conditions:
    # 1. 0 <= K_i (otherwise impossible for any H >= 0)
    # 2. H - D_i <= K_i  =>  H <= D_i + K_i
    
    # Precompute R_j = U_j
    # Compute K_i efficiently using prefix and suffix minimums.
    # K_i = min( min_{j<=i} (U_j - X*j) + X*i,  min_{j>=i} (U_j + X*j) - X*i )
    
    # Arrays are 0-indexed in Python, but logic uses 1-based indexing for math derivation.
    # Let's stick to 0-based index k for array access, but use k+1 for the 'j' in formula.
    # Formula: min_j (U_j + X * |i - j|) where i, j are 1-based indices.
    # In 0-based: min_k (U[k] + X * |i - k|) where i, k are 0-based.
    # |i - k| = i - k if k <= i, k - i if k > i.
    # Term 1 (k <= i): U[k] + X*(i - k) = (U[k] - X*k) + X*i
    # Term 2 (k > i): U[k] + X*(k - i) = (U[k] + X*k) - X*i
    
    # We need prefix min of (U[k] - X*k) and suffix min of (U[k] + X*k).
    
    n = N
    # Precompute values
    # Using 0-based index k
    # val1[k] = U[k] - X * k
    # val2[k] = U[k] + X * k
    
    # We can compute prefix mins and suffix mins on the fly or store them.
    # Storing is O(N) space, acceptable.
    
    val1 = [U[k] - X * k for k in range(n)]
    val2 = [U[k] + X * k for k in range(n)]
    
    # Prefix min of val1
    pref_min = [0] * n
    curr = val1[0]
    for k in range(n):
        if curr > val1[k]:
            curr = val1[k]
        pref_min[k] = curr
        
    # Suffix min of val2
    suff_min = [0] * n
    curr = val2[n-1]
    for k in range(n-1, -1, -1):
        if curr > val2[k]:
            curr = val2[k]
        suff_min[k] = curr
        
    # Calculate K_i for each i (0-based)
    # K[i] = min(pref_min[i] + X*i, suff_min[i] - X*i)
    # Note: i here is the 0-based index.
    # The formula derivation:
    # min_{k<=i} (U[k] - X*k) + X*i  -> pref_min[i] + X*i
    # min_{k>=i} (U[k] + X*k) - X*i  -> suff_min[i] - X*i
    
    K = [0] * n
    
    for i in range(n):
        term1 = pref_min[i] + X * i
        term2 = suff_min[i] - X * i
        K[i] = term1 if term1 < term2 else term2
        
    # Calculate H_limit based on D[i] + K[i]
    # H <= D[i] + K[i] for all i
    # Also H <= min_S
    
    h_limit = float('inf')
    
    for i in range(n):
        val = D[i] + K[i]
        if val < h_limit:
            h_limit = val
            
    # Final H
    ans_H = min_S
    if h_limit < ans_H:
        ans_H = h_limit
        
    # If ans_H < 0, it means even H=0 is not possible? But H=0 is always possible.
    # So ans_H should be at least 0.
    if ans_H < 0:
        ans_H = 0
        
    # Calculate cost
    # Cost = sum(S_i) - N * H
    total_S = sum(S)
    cost = total_S - n * ans_H
    
    print(cost)

if __name__ == '__main__':
    solve()