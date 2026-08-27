import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # 1-based indexing for logic, but 0-based for array access
    # A is 0-indexed: A[0]...A[N-1]
    # Values are 1 to N
    
    # Precompute positions for each value
    # positions[v] = list of indices (0-based) where value v appears
    positions = [[] for _ in range(N + 1)]
    for idx, val in enumerate(A):
        positions[val].append(idx)
        
    # Helper function to calculate number of subarrays completely within gaps
    # given a sorted list of "blocked" indices.
    # The gaps are segments of indices that do NOT contain any blocked value.
    # If blocked indices are b_1, b_2, ..., b_k, the gaps are:
    # [0, b_1-1], [b_1+1, b_2-1], ..., [b_k+1, N-1]
    # We sum len*(len+1)//2 for each gap length.
    def count_subarrays_missing(blocked_indices):
        if not blocked_indices:
            # If no values are blocked, all subarrays are "missing" nothing?
            # Wait, this function is for "subarrays missing value X".
            # If value X never appears, blocked_indices is empty.
            # Then ALL subarrays are missing X.
            return N * (N + 1) // 2
        
        total_missing = 0
        prev_idx = -1
        
        for b in blocked_indices:
            # Gap is from prev_idx + 1 to b - 1
            # Length of gap
            gap_len = b - 1 - (prev_idx + 1) + 1
            gap_len = b - prev_idx - 1
            
            if gap_len > 0:
                total_missing += gap_len * (gap_len + 1) // 2
            
            prev_idx = b
            
        # Last gap from last blocked index + 1 to N - 1
        gap_len = (N - 1) - (prev_idx + 1) + 1
        gap_len = N - 1 - prev_idx
        
        if gap_len > 0:
            total_missing += gap_len * (gap_len + 1) // 2
            
        return total_missing

    # Calculate S1: Sum of distinct counts over all subarrays
    # S1 = sum_{i=0}^{N-1} (i - prev_occurrence_index) * (N - i)
    # Note: indices are 0-based.
    # For A[i], let prev[i] be the previous index of the same value.
    # If none, prev[i] = -1.
    # Valid L ranges from prev[i]+1 to i. Count: i - prev[i].
    # Valid R ranges from i to N-1. Count: N - i.
    
    S1 = 0
    last_pos = {}
    for i in range(N):
        val = A[i]
        prev_i = last_pos.get(val, -1)
        count_L = i - prev_i
        count_R = N - i
        S1 += count_L * count_R
        last_pos[val] = i

    # Calculate S2: Sum over v of (subarrays containing both v and v+1)
    # C(v, v+1) = Total - Missing(v) - Missing(v+1) + Missing(v and v+1)
    
    S2 = 0
    total_subarrays = N * (N + 1) // 2
    
    # We only need to check v from 1 to N-1
    for v in range(1, N):
        # Get positions for v and v+1
        pos_v = positions[v]
        pos_v1 = positions[v + 1]
        
        # Count subarrays missing v
        miss_v = count_subarrays_missing(pos_v)
        
        # Count subarrays missing v+1
        miss_v1 = count_subarrays_missing(pos_v1)
        
        # Count subarrays missing both v and v+1
        # Combine positions and sort
        combined = pos_v + pos_v1
        combined.sort()
        miss_both = count_subarrays_missing(combined)
        
        # Inclusion-Exclusion
        # Subarrays containing BOTH = Total - (Missing v OR Missing v+1)
        # Missing v OR Missing v+1 = Missing v + Missing v+1 - Missing Both
        missing_either = miss_v + miss_v1 - miss_both
        containing_both = total_subarrays - missing_either
        
        S2 += containing_both

    ans = S1 - S2
    print(ans)

if __name__ == '__main__':
    solve()