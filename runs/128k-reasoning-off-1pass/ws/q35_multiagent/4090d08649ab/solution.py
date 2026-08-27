import sys

def solve():
    # Increase recursion depth just in case, though we use iterative approach
    sys.setrecursionlimit(2000000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    n = int(data[0])
    a = list(map(int, data[1:]))
    
    # 0-indexed internally
    # a[0] ... a[n-1]
    
    # Precompute next occurrence for each position
    # nxt[i] = index of the next occurrence of a[i] after i, or n if none
    nxt = [n] * n
    last_pos = {}
    
    # Traverse from right to left
    for i in range(n - 1, -1, -1):
        val = a[i]
        if val in last_pos:
            nxt[i] = last_pos[val]
        last_pos[val] = i
        
    # Calculate Total sum of lengths of all subarrays
    # Sum_{L=0}^{N-1} Sum_{R=L}^{N-1} (R - L + 1)
    # Let len = R - L + 1. len ranges from 1 to N.
    # Number of subarrays of length len is N - len + 1.
    # Total = Sum_{len=1}^{N} len * (N - len + 1)
    
    # This can be computed in O(1) or O(N). Given N=3e5, O(N) is fine.
    total_len_sum = 0
    for length in range(1, n + 1):
        count = n - length + 1
        total_len_sum += length * count
        
    # Calculate Cuts
    # Cuts = Sum_{k=0}^{N-2} Sum_{L=0}^{k} max(0, min_{j=L}^{k} nxt[j] - (k + 1))
    # Note: k is the split point. Subarray is A[L...k] and A[k+1...R].
    # The split point k corresponds to index k in 0-indexed array.
    # The right part starts at k+1.
    # The limit is min_{j=L}^{k} nxt[j].
    # Valid R are in [k+1, limit - 1]. Count is max(0, limit - (k + 1)).
    
    cuts = 0
    
    # We iterate k from 0 to N-2.
    # We maintain a monotonic stack of indices j such that nxt[j] is increasing.
    # Stack stores indices.
    stack = [] # Stores indices j
    
    for k in range(n - 1):
        current_val = nxt[k]
        
        # Maintain monotonic stack: nxt[stack[-1]] < current_val
        # Pop elements that are >= current_val
        while stack and nxt[stack[-1]] >= current_val:
            stack.pop()
            
        stack.append(k)
        
        # Now stack contains indices idx_0 < idx_1 < ... < idx_p = k
        # such that nxt[idx_0] < nxt[idx_1] < ... < nxt[idx_p]
        
        # For L in (idx_{i-1}, idx_i], the min_{j=L}^{k} nxt[j] is nxt[idx_i]
        # Let idx_{-1} = -1
        
        prev_idx = -1
        for idx in stack:
            # Range of L is (prev_idx, idx]
            # Number of L's is idx - prev_idx
            count_L = idx - prev_idx
            
            limit = nxt[idx]
            # Valid R starts at k+1.
            # We need R < limit. So R in [k+1, limit-1].
            # Count of R is max(0, limit - (k + 1))
            
            if limit > k + 1:
                count_R = limit - (k + 1)
            else:
                count_R = 0
                
            cuts += count_L * count_R
            
            prev_idx = idx
            
    ans = total_len_sum - cuts
    print(ans)

solve()