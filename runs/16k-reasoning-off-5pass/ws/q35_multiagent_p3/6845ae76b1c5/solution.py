import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    idx = 0
    N = int(data[idx]); idx += 1
    A = [int(data[idx + i]) for i in range(N)]; idx += N
    B = [int(data[idx + i]) for i in range(N)]; idx += N
    K = int(data[idx]); idx += 1
    
    # Sort A and B
    A.sort()
    B.sort()
    
    # Precompute prefix sums for B
    # SB[i] = sum of B[0] + B[1] + ... + B[i-1]
    SB = [0] * (N + 1)
    for i in range(N):
        SB[i + 1] = SB[i] + B[i]
    
    # Precompute prefix sums for A (not strictly needed for the two-pointer approach per query, but let's see)
    # Actually, we don't need prefix sums for A for the two-pointer approach per query.
    
    results = []
    
    for _ in range(K):
        X = int(data[idx]); idx += 1
        Y = int(data[idx]); idx += 1
        
        # We need to compute sum_{i=0}^{X-1} sum_{j=0}^{Y-1} |A[i] - B[j]|
        # Using two-pointer approach:
        # For each A[i], find how many B[j] (j < Y) are <= A[i].
        # Since A is sorted, as i increases, the split point in B also increases (non-decreasing).
        
        total = 0
        ptr = 0  # ptr will be the count of elements in B[0..Y-1] that are <= A[i]
        
        # SB is prefix sum of sorted B, SB[k] = sum of first k elements of B
        sum_B_Y = SB[Y]  # sum of B[0..Y-1]
        
        for i in range(X):
            a_val = A[i]
            # Advance ptr while B[ptr] <= a_val and ptr < Y
            while ptr < Y and B[ptr] <= a_val:
                ptr += 1
            
            # Now ptr is the number of elements in B[0..Y-1] that are <= a_val
            # Elements B[0..ptr-1] are <= a_val: contribution is a_val - B[j]
            # Elements B[ptr..Y-1] are > a_val: contribution is B[j] - a_val
            
            sum_le = SB[ptr]  # sum of B[0..ptr-1]
            sum_gt = sum_B_Y - sum_le  # sum of B[ptr..Y-1]
            
            # Contribution from this A[i]:
            # sum_{j=0}^{ptr-1} (a_val - B[j]) + sum_{j=ptr}^{Y-1} (B[j] - a_val)
            # = a_val * ptr - sum_le + sum_gt - a_val * (Y - ptr)
            # = a_val * (2 * ptr - Y) - 2 * sum_le + sum_B_Y
            
            contrib = a_val * (2 * ptr - Y) - 2 * sum_le + sum_B_Y
            total += contrib
        
        results.append(str(total))
    
    sys.stdout.write('\n'.join(results) + '\n')

solve()