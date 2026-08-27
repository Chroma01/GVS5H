import sys

def solve():
    # Increase recursion depth just in case, though we don't use recursion here
    sys.setrecursionlimit(200005)
    
    # Fast I/O
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    M = int(data[1])
    
    A = []
    for i in range(N):
        A.append(int(data[2 + i]))
        
    # Step 1: Compute initial inversion count for k=0
    # Using Fenwick Tree (Binary Indexed Tree)
    # Values are in range [0, M-1]
    
    def update(bit, i, delta):
        """Add delta to element at index i (1-based) in BIT."""
        while i < len(bit):
            bit[i] += delta
            i += i & (-i)
            
    def query(bit, i):
        """Return sum from index 1 to i (1-based) in BIT."""
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s
    
    # Initialize BIT with size M+1
    bit = [0] * (M + 1)
    
    inv_count = 0
    # Process from left to right
    # For each element A[i], count how many elements to its left are greater than A[i]
    # This is equivalent to: (total elements processed so far) - (elements <= A[i])
    # Or: query(bit, M) - query(bit, A[i] + 1) if we store frequencies
    
    # Let's use 1-based indexing for BIT where index x corresponds to value x-1?
    # Or just map value v to index v+1.
    # Values are 0..M-1. Map to 1..M.
    
    for x in A:
        # Number of elements already in BIT that are greater than x
        # Total elements so far = i (0-indexed loop counter)
        # Elements <= x = query(bit, x+1)
        # Elements > x = i - query(bit, x+1)
        
        # But wait, standard inversion counting:
        # Iterate j from 0 to N-1.
        # Count i < j such that A[i] > A[j].
        # When we are at j, we have inserted A[0]...A[j-1] into BIT.
        # We want to count how many of those are > A[j].
        
        # Let's restructure the loop
        pass

    # Reset BIT and count
    bit = [0] * (M + 2)
    inv_count = 0
    
    for i, x in enumerate(A):
        # x is in [0, M-1]. Map to 1..M for BIT.
        val = x + 1
        
        # Count elements already in BIT that are greater than x
        # Total elements inserted so far = i
        # Count of elements <= x = query(bit, val)
        # Count of elements > x = i - query(bit, val)
        
        count_le = query(bit, val)
        count_gt = i - count_le
        inv_count += count_gt
        
        update(bit, val, 1)
        
    # Step 2: Precompute positions for each value
    # pos[v] = sorted list of indices i where A[i] == v
    pos = [[] for _ in range(M)]
    for i, x in enumerate(A):
        pos[x].append(i)
        
    # Step 3: Iterate k from 0 to M-1
    # For each k, we have the inversion count for B where B_i = (A_i + k) % M.
    # We start with k=0, which we computed.
    # Then we transition to k=1, 2, ..., M-1.
    
    # Transition from k to k+1:
    # The value that wraps around is v = (M - 1 - k) % M.
    # These elements become 0. All others increase by 1.
    # Change in inversions:
    # Delta = sum_{idx in pos[v]} (R_idx - L_idx)
    # where L_idx = number of non-wrapping elements to the left of idx
    #       R_idx = number of non-wrapping elements to the right of idx
    
    # Let cnt = len(pos[v])
    # For the m-th element in pos[v] (0-indexed) at index idx = pos[v][m]:
    # L_idx = idx - m
    # R_idx = (N - 1 - idx) - (cnt - 1 - m) = N - idx - cnt + m
    # Contribution = R_idx - L_idx = N - cnt - 2*idx + 2*m
    
    results = []
    results.append(inv_count)
    
    current_inv = inv_count
    
    for k in range(M - 1):
        # We are transitioning from k to k+1
        # The value that wraps is v = (M - 1 - k) % M
        v = (M - 1 - k) % M
        
        indices = pos[v]
        cnt = len(indices)
        
        if cnt > 0:
            delta = 0
            # Sum over m from 0 to cnt-1
            # delta += sum(N - cnt - 2*idx + 2*m)
            #        = cnt * (N - cnt) - 2 * sum(indices) + 2 * sum(m for m in 0..cnt-1)
            # sum(m for m in 0..cnt-1) = cnt * (cnt - 1) // 2
            
            sum_indices = sum(indices)
            sum_m = cnt * (cnt - 1) // 2
            
            term1 = cnt * (N - cnt)
            term2 = 2 * sum_indices
            term3 = 2 * sum_m
            
            delta = term1 - term2 + term3
            current_inv += delta
            
        results.append(current_inv)
        
    # Output results
    for res in results:
        print(res)

solve()