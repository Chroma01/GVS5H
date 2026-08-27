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
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # Part 1: Sum of distinct counts for all subarrays
    # For each distinct value x, count the number of subarrays that contain x.
    # This is equivalent to: Total Subarrays - Subarrays NOT containing x.
    # Subarrays not containing x are those strictly located within the gaps between 
    # consecutive occurrences of x (including before the first and after the last).
    
    positions = {}
    for i, x in enumerate(A):
        if x not in positions:
            positions[x] = []
        positions[x].append(i)
        
    total_distinct_sum = 0
    
    for x, idxs in positions.items():
        # Gap before first occurrence: indices [0, idxs[0] - 1]
        gap_len = idxs[0]
        total_distinct_sum += gap_len * (gap_len + 1) // 2
        
        # Gaps between occurrences: indices [idxs[i-1] + 1, idxs[i] - 1]
        for i in range(1, len(idxs)):
            gap_len = idxs[i] - idxs[i-1] - 1
            total_distinct_sum += gap_len * (gap_len + 1) // 2
            
        # Gap after last occurrence: indices [idxs[-1] + 1, N - 1]
        gap_len = (N - 1) - idxs[-1]
        total_distinct_sum += gap_len * (gap_len + 1) // 2

    # Part 2: Sum of pairs (v, v+1) present in all subarrays
    # We iterate R from 0 to N-1. For each R, we consider the value A[R].
    # We check pairs (A[R]-1, A[R]) and (A[R], A[R]+1).
    # If both values in a pair have been seen previously, the number of subarrays ending at R
    # that contain BOTH values is min(last_pos[v], last_pos[v+1]) + 1.
    # Since we update last_pos_pair[val] = r at the start of the loop, 
    # last_pos_pair[val] is always r. So min(last_pos_pair[v], r) is just last_pos_pair[v].
    
    last_pos_pair = {}
    total_pairs_sum = 0
    
    for r in range(N):
        val = A[r]
        last_pos_pair[val] = r
        
        # Check pair (val-1, val)
        if val - 1 in last_pos_pair:
            p1 = last_pos_pair[val - 1]
            # The subarray must start at or before p1 to include both occurrences.
            # Indices for L are 0, 1, ..., p1. Count is p1 + 1.
            total_pairs_sum += (p1 + 1)
            
        # Check pair (val, val+1)
        if val + 1 in last_pos_pair:
            p1 = last_pos_pair[val + 1]
            total_pairs_sum += (p1 + 1)

    # The answer is Total Distinct Sum - Total Pairs Sum
    ans = total_distinct_sum - total_pairs_sum
    print(ans)

if __name__ == '__main__':
    solve()