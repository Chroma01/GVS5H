import sys

# Set recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    S = input_data[1]
    
    MOD = 998244353
    
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Identify cut points
    # A cut point at index k (1-based) means W_k == B_k
    # We are interested in indices 2*j for j in 1..N
    # Let's compute prefix counts of W and B
    # S is 0-indexed in Python, so S[i] corresponds to vertex i+1
    
    w_count = 0
    b_count = 0
    
    # is_cut[j] will be True if the prefix of length 2*j has equal W and B
    is_cut = [False] * (N + 1)
    
    for i in range(2 * N):
        if S[i] == 'W':
            w_count += 1
        else:
            b_count += 1
        
        # Vertex index is i+1.
        # We check if i+1 is even and w_count == b_count
        if (i + 1) % 2 == 0:
            j = (i + 1) // 2
            if w_count == b_count:
                is_cut[j] = True
                
    # DP array
    # A[j] stores the number of strongly connected matchings for the first 2*j vertices
    # such that the prefix 2*j is the FIRST closed prefix.
    A = [0] * (N + 1)
    
    # We compute A[j] for j from 1 to N
    # Recurrence: A[j] = j! - sum_{k=1}^{j-1} A[k] * (j-k)!
    # Only if is_cut[j] is True. Otherwise A[j] = 0.
    
    for j in range(1, N + 1):
        if not is_cut[j]:
            A[j] = 0
            continue
            
        # Calculate sum_{k=1}^{j-1} A[k] * (j-k)!
        total_bad = 0
        for k in range(1, j):
            if A[k] == 0:
                continue
            term = (A[k] * fact[j - k]) % MOD
            total_bad = (total_bad + term) % MOD
            
        A[j] = (fact[j] - total_bad) % MOD
        
    print(A[N])

if __name__ == '__main__':
    solve()